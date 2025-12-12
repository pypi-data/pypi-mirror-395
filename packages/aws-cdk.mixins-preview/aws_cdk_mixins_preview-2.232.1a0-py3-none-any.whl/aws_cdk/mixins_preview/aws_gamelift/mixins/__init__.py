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
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnAliasMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "routing_strategy": "routingStrategy",
        "tags": "tags",
    },
)
class CfnAliasMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        routing_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAliasPropsMixin.RoutingStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAliasPropsMixin.

        :param description: A human-readable description of the alias.
        :param name: A descriptive label that is associated with an alias. Alias names do not need to be unique.
        :param routing_strategy: The routing configuration, including routing type and fleet target, for the alias.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_alias_mixin_props = gamelift_mixins.CfnAliasMixinProps(
                description="description",
                name="name",
                routing_strategy=gamelift_mixins.CfnAliasPropsMixin.RoutingStrategyProperty(
                    fleet_id="fleetId",
                    message="message",
                    type="type"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91450d50d611e1f2b22f07f6fffee9b049401ae231a89cfe5cca1ce3c995b0c0)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument routing_strategy", value=routing_strategy, expected_type=type_hints["routing_strategy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if routing_strategy is not None:
            self._values["routing_strategy"] = routing_strategy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A descriptive label that is associated with an alias.

        Alias names do not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_strategy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAliasPropsMixin.RoutingStrategyProperty"]]:
        '''The routing configuration, including routing type and fleet target, for the alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-routingstrategy
        '''
        result = self._values.get("routing_strategy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAliasPropsMixin.RoutingStrategyProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAliasMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAliasPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnAliasPropsMixin",
):
    '''The ``AWS::GameLift::Alias`` resource creates an alias for an Amazon GameLift (GameLift) fleet destination.

    There are two types of routing strategies for aliases: simple and terminal. A simple alias points to an active fleet. A terminal alias displays a message instead of routing players to an active fleet. For example, a terminal alias might display a URL link that directs players to an upgrade site. You can use aliases to define destinations in a game session queue or when requesting new game sessions.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html
    :cloudformationResource: AWS::GameLift::Alias
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_alias_props_mixin = gamelift_mixins.CfnAliasPropsMixin(gamelift_mixins.CfnAliasMixinProps(
            description="description",
            name="name",
            routing_strategy=gamelift_mixins.CfnAliasPropsMixin.RoutingStrategyProperty(
                fleet_id="fleetId",
                message="message",
                type="type"
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
        props: typing.Union[CfnAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::Alias``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f846d0d7ed60a4d1fddbe532365aa9f9564e8ac0b681b8c5f0ddc8363cced5ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76fb307ef66a4c7076b310eb08f2061797826790e90018f384d0cff4bfe503e1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8a556e0a7e39845542e9f03c741a0044d37373dfa09a31ab29a7abb6375ed9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAliasMixinProps:
        return typing.cast(CfnAliasMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnAliasPropsMixin.RoutingStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"fleet_id": "fleetId", "message": "message", "type": "type"},
    )
    class RoutingStrategyProperty:
        def __init__(
            self,
            *,
            fleet_id: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The routing configuration for a fleet alias.

            :param fleet_id: A unique identifier for a fleet that the alias points to. If you specify ``SIMPLE`` for the ``Type`` property, you must specify this property.
            :param message: The message text to be used with a terminal routing strategy. If you specify ``TERMINAL`` for the ``Type`` property, you must specify this property.
            :param type: A type of routing strategy. Possible routing types include the following: - *SIMPLE* - The alias resolves to one specific fleet. Use this type when routing to active fleets. - *TERMINAL* - The alias does not resolve to a fleet but instead can be used to display a message to the user. A terminal alias throws a ``TerminalRoutingStrategyException`` with the message that you specified in the ``Message`` property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                routing_strategy_property = gamelift_mixins.CfnAliasPropsMixin.RoutingStrategyProperty(
                    fleet_id="fleetId",
                    message="message",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c394fc75b932a2f06b895412190eb02ac72ec9e2da878bc628a43466e931be10)
                check_type(argname="argument fleet_id", value=fleet_id, expected_type=type_hints["fleet_id"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fleet_id is not None:
                self._values["fleet_id"] = fleet_id
            if message is not None:
                self._values["message"] = message
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def fleet_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for a fleet that the alias points to.

            If you specify ``SIMPLE`` for the ``Type`` property, you must specify this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html#cfn-gamelift-alias-routingstrategy-fleetid
            '''
            result = self._values.get("fleet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The message text to be used with a terminal routing strategy.

            If you specify ``TERMINAL`` for the ``Type`` property, you must specify this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html#cfn-gamelift-alias-routingstrategy-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''A type of routing strategy.

            Possible routing types include the following:

            - *SIMPLE* - The alias resolves to one specific fleet. Use this type when routing to active fleets.
            - *TERMINAL* - The alias does not resolve to a fleet but instead can be used to display a message to the user. A terminal alias throws a ``TerminalRoutingStrategyException`` with the message that you specified in the ``Message`` property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html#cfn-gamelift-alias-routingstrategy-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnBuildMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "operating_system": "operatingSystem",
        "server_sdk_version": "serverSdkVersion",
        "storage_location": "storageLocation",
        "tags": "tags",
        "version": "version",
    },
)
class CfnBuildMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        operating_system: typing.Optional[builtins.str] = None,
        server_sdk_version: typing.Optional[builtins.str] = None,
        storage_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBuildPropsMixin.StorageLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnBuildPropsMixin.

        :param name: A descriptive label that is associated with a build. Build names do not need to be unique.
        :param operating_system: The operating system that your game server binaries run on. This value determines the type of fleet resources that you use for this build. If your game build contains multiple executables, they all must run on the same operating system. You must specify a valid operating system in this request. There is no default value. You can't change a build's operating system later. .. epigraph:: Amazon Linux 2 (AL2) will reach end of support on 6/30/2025. See more details in the `Amazon Linux 2 FAQs <https://docs.aws.amazon.com/amazon-linux-2/faqs/>`_ . For game servers that are hosted on AL2 and use server SDK version 4.x for Amazon GameLift Servers, first update the game server build to server SDK 5.x, and then deploy to AL2023 instances. See `Migrate to server SDK version 5. <https://docs.aws.amazon.com/gamelift/latest/developerguide/reference-serversdk5-migration.html>`_
        :param server_sdk_version: A server SDK version you used when integrating your game server build with Amazon GameLift Servers. For more information see `Integrate games with custom game servers <https://docs.aws.amazon.com/gamelift/latest/developerguide/integration-custom-intro.html>`_ . By default Amazon GameLift Servers sets this value to ``4.0.2`` .
        :param storage_location: Information indicating where your game build files are stored. Use this parameter only when creating a build with files stored in an Amazon S3 bucket that you own. The storage location must specify an Amazon S3 bucket name and key. The location must also specify a role ARN that you set up to allow Amazon GameLift Servers to access your Amazon S3 bucket. The S3 bucket and your new build must be in the same Region. If a ``StorageLocation`` is specified, the size of your file can be found in your Amazon S3 bucket. Amazon GameLift Servers will report a ``SizeOnDisk`` of 0.
        :param tags: An array of key-value pairs to apply to this resource.
        :param version: Version information that is associated with this build. Version strings do not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_build_mixin_props = gamelift_mixins.CfnBuildMixinProps(
                name="name",
                operating_system="operatingSystem",
                server_sdk_version="serverSdkVersion",
                storage_location=gamelift_mixins.CfnBuildPropsMixin.StorageLocationProperty(
                    bucket="bucket",
                    key="key",
                    object_version="objectVersion",
                    role_arn="roleArn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                version="version"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edcf26e7d75b41888220c5ea4c44921788a309cf35a0c40281b3cb7198a7e404)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
            check_type(argname="argument server_sdk_version", value=server_sdk_version, expected_type=type_hints["server_sdk_version"])
            check_type(argname="argument storage_location", value=storage_location, expected_type=type_hints["storage_location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if server_sdk_version is not None:
            self._values["server_sdk_version"] = server_sdk_version
        if storage_location is not None:
            self._values["storage_location"] = storage_location
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A descriptive label that is associated with a build.

        Build names do not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''The operating system that your game server binaries run on.

        This value determines the type of fleet resources that you use for this build. If your game build contains multiple executables, they all must run on the same operating system. You must specify a valid operating system in this request. There is no default value. You can't change a build's operating system later.
        .. epigraph::

           Amazon Linux 2 (AL2) will reach end of support on 6/30/2025. See more details in the `Amazon Linux 2 FAQs <https://docs.aws.amazon.com/amazon-linux-2/faqs/>`_ . For game servers that are hosted on AL2 and use server SDK version 4.x for Amazon GameLift Servers, first update the game server build to server SDK 5.x, and then deploy to AL2023 instances. See `Migrate to server SDK version 5. <https://docs.aws.amazon.com/gamelift/latest/developerguide/reference-serversdk5-migration.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-operatingsystem
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_sdk_version(self) -> typing.Optional[builtins.str]:
        '''A server SDK version you used when integrating your game server build with Amazon GameLift Servers.

        For more information see `Integrate games with custom game servers <https://docs.aws.amazon.com/gamelift/latest/developerguide/integration-custom-intro.html>`_ . By default Amazon GameLift Servers sets this value to ``4.0.2`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-serversdkversion
        '''
        result = self._values.get("server_sdk_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBuildPropsMixin.StorageLocationProperty"]]:
        '''Information indicating where your game build files are stored.

        Use this parameter only when creating a build with files stored in an Amazon S3 bucket that you own. The storage location must specify an Amazon S3 bucket name and key. The location must also specify a role ARN that you set up to allow Amazon GameLift Servers to access your Amazon S3 bucket. The S3 bucket and your new build must be in the same Region.

        If a ``StorageLocation`` is specified, the size of your file can be found in your Amazon S3 bucket. Amazon GameLift Servers will report a ``SizeOnDisk`` of 0.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-storagelocation
        '''
        result = self._values.get("storage_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBuildPropsMixin.StorageLocationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version information that is associated with this build.

        Version strings do not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBuildMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBuildPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnBuildPropsMixin",
):
    '''The ``AWS::GameLift::Build`` resource creates a game server build that is installed and run on instances in an Amazon GameLift fleet.

    This resource points to an Amazon S3 location that contains a zip file with all of the components of the game server build.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html
    :cloudformationResource: AWS::GameLift::Build
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_build_props_mixin = gamelift_mixins.CfnBuildPropsMixin(gamelift_mixins.CfnBuildMixinProps(
            name="name",
            operating_system="operatingSystem",
            server_sdk_version="serverSdkVersion",
            storage_location=gamelift_mixins.CfnBuildPropsMixin.StorageLocationProperty(
                bucket="bucket",
                key="key",
                object_version="objectVersion",
                role_arn="roleArn"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            version="version"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBuildMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::Build``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a40ac46e58397d424fef96f7e29ed6065816bfb67548dc067fd2a65e5e618f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a88be5b614ed0c8069bea87fce9af8d1239e5e045e9d5873178283d2306e026)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc5d128189860d88dea5a6207dad91f10a817f457844f0152cf495148d430753)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBuildMixinProps:
        return typing.cast(CfnBuildMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnBuildPropsMixin.StorageLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "object_version": "objectVersion",
            "role_arn": "roleArn",
        },
    )
    class StorageLocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            object_version: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location in Amazon S3 where build or script files are stored for access by Amazon GameLift.

            :param bucket: An Amazon S3 bucket identifier. The name of the S3 bucket. .. epigraph:: Amazon GameLift doesn't support uploading from Amazon S3 buckets with names that contain a dot (.).
            :param key: The name of the zip file that contains the build files or script files.
            :param object_version: A version of a stored file to retrieve, if the object versioning feature is turned on for the S3 bucket. Use this parameter to specify a specific version. If this parameter isn't set, Amazon GameLift Servers retrieves the latest version of the file.
            :param role_arn: The ARNfor an IAM role that allows Amazon GameLift to access the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                storage_location_property = gamelift_mixins.CfnBuildPropsMixin.StorageLocationProperty(
                    bucket="bucket",
                    key="key",
                    object_version="objectVersion",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efe6320fe06a44a35467d6e086bd85566645ca91f13f15c01ff9ae02ff8378ad)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument object_version", value=object_version, expected_type=type_hints["object_version"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if object_version is not None:
                self._values["object_version"] = object_version
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''An Amazon S3 bucket identifier. The name of the S3 bucket.

            .. epigraph::

               Amazon GameLift doesn't support uploading from Amazon S3 buckets with names that contain a dot (.).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storagelocation-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the zip file that contains the build files or script files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storagelocation-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            '''A version of a stored file to retrieve, if the object versioning feature is turned on for the S3 bucket.

            Use this parameter to specify a specific version. If this parameter isn't set, Amazon GameLift Servers retrieves the latest version of the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storagelocation-objectversion
            '''
            result = self._values.get("object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARNfor an IAM role that allows Amazon GameLift to access the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storagelocation-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "billing_type": "billingType",
        "deployment_configuration": "deploymentConfiguration",
        "description": "description",
        "fleet_role_arn": "fleetRoleArn",
        "game_server_container_group_definition_name": "gameServerContainerGroupDefinitionName",
        "game_server_container_groups_per_instance": "gameServerContainerGroupsPerInstance",
        "game_session_creation_limit_policy": "gameSessionCreationLimitPolicy",
        "instance_connection_port_range": "instanceConnectionPortRange",
        "instance_inbound_permissions": "instanceInboundPermissions",
        "instance_type": "instanceType",
        "locations": "locations",
        "log_configuration": "logConfiguration",
        "metric_groups": "metricGroups",
        "new_game_session_protection_policy": "newGameSessionProtectionPolicy",
        "per_instance_container_group_definition_name": "perInstanceContainerGroupDefinitionName",
        "scaling_policies": "scalingPolicies",
        "tags": "tags",
    },
)
class CfnContainerFleetMixinProps:
    def __init__(
        self,
        *,
        billing_type: typing.Optional[builtins.str] = None,
        deployment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerFleetPropsMixin.DeploymentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        fleet_role_arn: typing.Optional[builtins.str] = None,
        game_server_container_group_definition_name: typing.Optional[builtins.str] = None,
        game_server_container_groups_per_instance: typing.Optional[jsii.Number] = None,
        game_session_creation_limit_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerFleetPropsMixin.GameSessionCreationLimitPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_connection_port_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerFleetPropsMixin.ConnectionPortRangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_inbound_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerFleetPropsMixin.IpPermissionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerFleetPropsMixin.LocationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerFleetPropsMixin.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metric_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        new_game_session_protection_policy: typing.Optional[builtins.str] = None,
        per_instance_container_group_definition_name: typing.Optional[builtins.str] = None,
        scaling_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerFleetPropsMixin.ScalingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnContainerFleetPropsMixin.

        :param billing_type: Indicates whether the fleet uses On-Demand or Spot instances for this fleet. Learn more about when to use `On-Demand versus Spot Instances <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-ec2-instances.html#gamelift-ec2-instances-spot>`_ . You can't update this fleet property. By default, this property is set to ``ON_DEMAND`` .
        :param deployment_configuration: Set of rules for processing a deployment for a container fleet update.
        :param description: A meaningful description of the container fleet.
        :param fleet_role_arn: The unique identifier for an AWS Identity and Access Management (IAM) role with permissions to run your containers on resources that are managed by Amazon GameLift Servers. See `Set up an IAM service role <https://docs.aws.amazon.com/gamelift/latest/developerguide/setting-up-role.html>`_ . This fleet property can't be changed.
        :param game_server_container_group_definition_name: The name of the fleet's game server container group definition, which describes how to deploy containers with your game server build and support software onto each fleet instance.
        :param game_server_container_groups_per_instance: The number of times to replicate the game server container group on each fleet instance.
        :param game_session_creation_limit_policy: A policy that limits the number of game sessions that each individual player can create on instances in this fleet. The limit applies for a specified span of time.
        :param instance_connection_port_range: The set of port numbers to open on each instance in a container fleet. Connection ports are used by inbound traffic to connect with processes that are running in containers on the fleet.
        :param instance_inbound_permissions: The IP address ranges and port settings that allow inbound traffic to access game server processes and other processes on this fleet.
        :param instance_type: The Amazon EC2 instance type to use for all instances in the fleet. Instance type determines the computing resources and processing power that's available to host your game servers. This includes including CPU, memory, storage, and networking capacity. You can't update this fleet property.
        :param locations: 
        :param log_configuration: The method that is used to collect container logs for the fleet. Amazon GameLift Servers saves all standard output for each container in logs, including game session logs. - ``CLOUDWATCH`` -- Send logs to an Amazon CloudWatch log group that you define. Each container emits a log stream, which is organized in the log group. - ``S3`` -- Store logs in an Amazon S3 bucket that you define. - ``NONE`` -- Don't collect container logs.
        :param metric_groups: The name of an AWS CloudWatch metric group to add this fleet to. Metric groups aggregate metrics for multiple fleets.
        :param new_game_session_protection_policy: Determines whether Amazon GameLift Servers can shut down game sessions on the fleet that are actively running and hosting players. Amazon GameLift Servers might prompt an instance shutdown when scaling down fleet capacity or when retiring unhealthy instances. You can also set game session protection for individual game sessions using `UpdateGameSession <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateGameSession.html>`_ . - *NoProtection* -- Game sessions can be shut down during active gameplay. - *FullProtection* -- Game sessions in ``ACTIVE`` status can't be shut down.
        :param per_instance_container_group_definition_name: The name of the fleet's per-instance container group definition.
        :param scaling_policies: A list of rules that control how a fleet is scaled.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_container_fleet_mixin_props = gamelift_mixins.CfnContainerFleetMixinProps(
                billing_type="billingType",
                deployment_configuration=gamelift_mixins.CfnContainerFleetPropsMixin.DeploymentConfigurationProperty(
                    impairment_strategy="impairmentStrategy",
                    minimum_healthy_percentage=123,
                    protection_strategy="protectionStrategy"
                ),
                description="description",
                fleet_role_arn="fleetRoleArn",
                game_server_container_group_definition_name="gameServerContainerGroupDefinitionName",
                game_server_container_groups_per_instance=123,
                game_session_creation_limit_policy=gamelift_mixins.CfnContainerFleetPropsMixin.GameSessionCreationLimitPolicyProperty(
                    new_game_sessions_per_creator=123,
                    policy_period_in_minutes=123
                ),
                instance_connection_port_range=gamelift_mixins.CfnContainerFleetPropsMixin.ConnectionPortRangeProperty(
                    from_port=123,
                    to_port=123
                ),
                instance_inbound_permissions=[gamelift_mixins.CfnContainerFleetPropsMixin.IpPermissionProperty(
                    from_port=123,
                    ip_range="ipRange",
                    protocol="protocol",
                    to_port=123
                )],
                instance_type="instanceType",
                locations=[gamelift_mixins.CfnContainerFleetPropsMixin.LocationConfigurationProperty(
                    location="location",
                    location_capacity=gamelift_mixins.CfnContainerFleetPropsMixin.LocationCapacityProperty(
                        desired_ec2_instances=123,
                        max_size=123,
                        min_size=123
                    ),
                    stopped_actions=["stoppedActions"]
                )],
                log_configuration=gamelift_mixins.CfnContainerFleetPropsMixin.LogConfigurationProperty(
                    log_destination="logDestination",
                    log_group_arn="logGroupArn",
                    s3_bucket_name="s3BucketName"
                ),
                metric_groups=["metricGroups"],
                new_game_session_protection_policy="newGameSessionProtectionPolicy",
                per_instance_container_group_definition_name="perInstanceContainerGroupDefinitionName",
                scaling_policies=[gamelift_mixins.CfnContainerFleetPropsMixin.ScalingPolicyProperty(
                    comparison_operator="comparisonOperator",
                    evaluation_periods=123,
                    metric_name="metricName",
                    name="name",
                    policy_type="policyType",
                    scaling_adjustment=123,
                    scaling_adjustment_type="scalingAdjustmentType",
                    target_configuration=gamelift_mixins.CfnContainerFleetPropsMixin.TargetConfigurationProperty(
                        target_value=123
                    ),
                    threshold=123
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0160f048a2c427fcdaca1b76c7bbb31d8358fa0211340651f1649327b55143c1)
            check_type(argname="argument billing_type", value=billing_type, expected_type=type_hints["billing_type"])
            check_type(argname="argument deployment_configuration", value=deployment_configuration, expected_type=type_hints["deployment_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument fleet_role_arn", value=fleet_role_arn, expected_type=type_hints["fleet_role_arn"])
            check_type(argname="argument game_server_container_group_definition_name", value=game_server_container_group_definition_name, expected_type=type_hints["game_server_container_group_definition_name"])
            check_type(argname="argument game_server_container_groups_per_instance", value=game_server_container_groups_per_instance, expected_type=type_hints["game_server_container_groups_per_instance"])
            check_type(argname="argument game_session_creation_limit_policy", value=game_session_creation_limit_policy, expected_type=type_hints["game_session_creation_limit_policy"])
            check_type(argname="argument instance_connection_port_range", value=instance_connection_port_range, expected_type=type_hints["instance_connection_port_range"])
            check_type(argname="argument instance_inbound_permissions", value=instance_inbound_permissions, expected_type=type_hints["instance_inbound_permissions"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument metric_groups", value=metric_groups, expected_type=type_hints["metric_groups"])
            check_type(argname="argument new_game_session_protection_policy", value=new_game_session_protection_policy, expected_type=type_hints["new_game_session_protection_policy"])
            check_type(argname="argument per_instance_container_group_definition_name", value=per_instance_container_group_definition_name, expected_type=type_hints["per_instance_container_group_definition_name"])
            check_type(argname="argument scaling_policies", value=scaling_policies, expected_type=type_hints["scaling_policies"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if billing_type is not None:
            self._values["billing_type"] = billing_type
        if deployment_configuration is not None:
            self._values["deployment_configuration"] = deployment_configuration
        if description is not None:
            self._values["description"] = description
        if fleet_role_arn is not None:
            self._values["fleet_role_arn"] = fleet_role_arn
        if game_server_container_group_definition_name is not None:
            self._values["game_server_container_group_definition_name"] = game_server_container_group_definition_name
        if game_server_container_groups_per_instance is not None:
            self._values["game_server_container_groups_per_instance"] = game_server_container_groups_per_instance
        if game_session_creation_limit_policy is not None:
            self._values["game_session_creation_limit_policy"] = game_session_creation_limit_policy
        if instance_connection_port_range is not None:
            self._values["instance_connection_port_range"] = instance_connection_port_range
        if instance_inbound_permissions is not None:
            self._values["instance_inbound_permissions"] = instance_inbound_permissions
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if locations is not None:
            self._values["locations"] = locations
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if metric_groups is not None:
            self._values["metric_groups"] = metric_groups
        if new_game_session_protection_policy is not None:
            self._values["new_game_session_protection_policy"] = new_game_session_protection_policy
        if per_instance_container_group_definition_name is not None:
            self._values["per_instance_container_group_definition_name"] = per_instance_container_group_definition_name
        if scaling_policies is not None:
            self._values["scaling_policies"] = scaling_policies
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def billing_type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the fleet uses On-Demand or Spot instances for this fleet.

        Learn more about when to use `On-Demand versus Spot Instances <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-ec2-instances.html#gamelift-ec2-instances-spot>`_ . You can't update this fleet property.

        By default, this property is set to ``ON_DEMAND`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-billingtype
        '''
        result = self._values.get("billing_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.DeploymentConfigurationProperty"]]:
        '''Set of rules for processing a deployment for a container fleet update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-deploymentconfiguration
        '''
        result = self._values.get("deployment_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.DeploymentConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A meaningful description of the container fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fleet_role_arn(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for an AWS Identity and Access Management (IAM) role with permissions to run your containers on resources that are managed by Amazon GameLift Servers.

        See `Set up an IAM service role <https://docs.aws.amazon.com/gamelift/latest/developerguide/setting-up-role.html>`_ . This fleet property can't be changed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-fleetrolearn
        '''
        result = self._values.get("fleet_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def game_server_container_group_definition_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The name of the fleet's game server container group definition, which describes how to deploy containers with your game server build and support software onto each fleet instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-gameservercontainergroupdefinitionname
        '''
        result = self._values.get("game_server_container_group_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def game_server_container_groups_per_instance(self) -> typing.Optional[jsii.Number]:
        '''The number of times to replicate the game server container group on each fleet instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-gameservercontainergroupsperinstance
        '''
        result = self._values.get("game_server_container_groups_per_instance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def game_session_creation_limit_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.GameSessionCreationLimitPolicyProperty"]]:
        '''A policy that limits the number of game sessions that each individual player can create on instances in this fleet.

        The limit applies for a specified span of time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-gamesessioncreationlimitpolicy
        '''
        result = self._values.get("game_session_creation_limit_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.GameSessionCreationLimitPolicyProperty"]], result)

    @builtins.property
    def instance_connection_port_range(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.ConnectionPortRangeProperty"]]:
        '''The set of port numbers to open on each instance in a container fleet.

        Connection ports are used by inbound traffic to connect with processes that are running in containers on the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-instanceconnectionportrange
        '''
        result = self._values.get("instance_connection_port_range")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.ConnectionPortRangeProperty"]], result)

    @builtins.property
    def instance_inbound_permissions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.IpPermissionProperty"]]]]:
        '''The IP address ranges and port settings that allow inbound traffic to access game server processes and other processes on this fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-instanceinboundpermissions
        '''
        result = self._values.get("instance_inbound_permissions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.IpPermissionProperty"]]]], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 instance type to use for all instances in the fleet.

        Instance type determines the computing resources and processing power that's available to host your game servers. This includes including CPU, memory, storage, and networking capacity. You can't update this fleet property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.LocationConfigurationProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-locations
        '''
        result = self._values.get("locations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.LocationConfigurationProperty"]]]], result)

    @builtins.property
    def log_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.LogConfigurationProperty"]]:
        '''The method that is used to collect container logs for the fleet.

        Amazon GameLift Servers saves all standard output for each container in logs, including game session logs.

        - ``CLOUDWATCH`` -- Send logs to an Amazon CloudWatch log group that you define. Each container emits a log stream, which is organized in the log group.
        - ``S3`` -- Store logs in an Amazon S3 bucket that you define.
        - ``NONE`` -- Don't collect container logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-logconfiguration
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.LogConfigurationProperty"]], result)

    @builtins.property
    def metric_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of an AWS CloudWatch metric group to add this fleet to.

        Metric groups aggregate metrics for multiple fleets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-metricgroups
        '''
        result = self._values.get("metric_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def new_game_session_protection_policy(self) -> typing.Optional[builtins.str]:
        '''Determines whether Amazon GameLift Servers can shut down game sessions on the fleet that are actively running and hosting players.

        Amazon GameLift Servers might prompt an instance shutdown when scaling down fleet capacity or when retiring unhealthy instances. You can also set game session protection for individual game sessions using `UpdateGameSession <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateGameSession.html>`_ .

        - *NoProtection* -- Game sessions can be shut down during active gameplay.
        - *FullProtection* -- Game sessions in ``ACTIVE`` status can't be shut down.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-newgamesessionprotectionpolicy
        '''
        result = self._values.get("new_game_session_protection_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def per_instance_container_group_definition_name(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The name of the fleet's per-instance container group definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-perinstancecontainergroupdefinitionname
        '''
        result = self._values.get("per_instance_container_group_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.ScalingPolicyProperty"]]]]:
        '''A list of rules that control how a fleet is scaled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-scalingpolicies
        '''
        result = self._values.get("scaling_policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.ScalingPolicyProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html#cfn-gamelift-containerfleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContainerFleetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContainerFleetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin",
):
    '''Describes an Amazon GameLift Servers managed container fleet.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containerfleet.html
    :cloudformationResource: AWS::GameLift::ContainerFleet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_container_fleet_props_mixin = gamelift_mixins.CfnContainerFleetPropsMixin(gamelift_mixins.CfnContainerFleetMixinProps(
            billing_type="billingType",
            deployment_configuration=gamelift_mixins.CfnContainerFleetPropsMixin.DeploymentConfigurationProperty(
                impairment_strategy="impairmentStrategy",
                minimum_healthy_percentage=123,
                protection_strategy="protectionStrategy"
            ),
            description="description",
            fleet_role_arn="fleetRoleArn",
            game_server_container_group_definition_name="gameServerContainerGroupDefinitionName",
            game_server_container_groups_per_instance=123,
            game_session_creation_limit_policy=gamelift_mixins.CfnContainerFleetPropsMixin.GameSessionCreationLimitPolicyProperty(
                new_game_sessions_per_creator=123,
                policy_period_in_minutes=123
            ),
            instance_connection_port_range=gamelift_mixins.CfnContainerFleetPropsMixin.ConnectionPortRangeProperty(
                from_port=123,
                to_port=123
            ),
            instance_inbound_permissions=[gamelift_mixins.CfnContainerFleetPropsMixin.IpPermissionProperty(
                from_port=123,
                ip_range="ipRange",
                protocol="protocol",
                to_port=123
            )],
            instance_type="instanceType",
            locations=[gamelift_mixins.CfnContainerFleetPropsMixin.LocationConfigurationProperty(
                location="location",
                location_capacity=gamelift_mixins.CfnContainerFleetPropsMixin.LocationCapacityProperty(
                    desired_ec2_instances=123,
                    max_size=123,
                    min_size=123
                ),
                stopped_actions=["stoppedActions"]
            )],
            log_configuration=gamelift_mixins.CfnContainerFleetPropsMixin.LogConfigurationProperty(
                log_destination="logDestination",
                log_group_arn="logGroupArn",
                s3_bucket_name="s3BucketName"
            ),
            metric_groups=["metricGroups"],
            new_game_session_protection_policy="newGameSessionProtectionPolicy",
            per_instance_container_group_definition_name="perInstanceContainerGroupDefinitionName",
            scaling_policies=[gamelift_mixins.CfnContainerFleetPropsMixin.ScalingPolicyProperty(
                comparison_operator="comparisonOperator",
                evaluation_periods=123,
                metric_name="metricName",
                name="name",
                policy_type="policyType",
                scaling_adjustment=123,
                scaling_adjustment_type="scalingAdjustmentType",
                target_configuration=gamelift_mixins.CfnContainerFleetPropsMixin.TargetConfigurationProperty(
                    target_value=123
                ),
                threshold=123
            )],
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
        props: typing.Union[CfnContainerFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::ContainerFleet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865cd7025104b5b6a8c79841c7b53a080512b42a4816a268382ed993060179e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a094601ae7a2cf1f2ad8b395c0c7ef602cbd8cd7bb09c4f46c9de8e800e196)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e784e4f53653e230c04441f47693e546c819033be894b4cf966c5b67bf962b52)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContainerFleetMixinProps:
        return typing.cast(CfnContainerFleetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.ConnectionPortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"from_port": "fromPort", "to_port": "toPort"},
    )
    class ConnectionPortRangeProperty:
        def __init__(
            self,
            *,
            from_port: typing.Optional[jsii.Number] = None,
            to_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The set of port numbers to open on each instance in a container fleet.

            Connection ports are used by inbound traffic to connect with processes that are running in containers on the fleet.

            :param from_port: Starting value for the port range.
            :param to_port: Ending value for the port. Port numbers are end-inclusive. This value must be equal to or greater than ``FromPort`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-connectionportrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                connection_port_range_property = gamelift_mixins.CfnContainerFleetPropsMixin.ConnectionPortRangeProperty(
                    from_port=123,
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78bd1c76b2ea1eb156e82e67ab9d1a425c0fd40e9bf51afb43b431bb29de780e)
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if from_port is not None:
                self._values["from_port"] = from_port
            if to_port is not None:
                self._values["to_port"] = to_port

        @builtins.property
        def from_port(self) -> typing.Optional[jsii.Number]:
            '''Starting value for the port range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-connectionportrange.html#cfn-gamelift-containerfleet-connectionportrange-fromport
            '''
            result = self._values.get("from_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def to_port(self) -> typing.Optional[jsii.Number]:
            '''Ending value for the port.

            Port numbers are end-inclusive. This value must be equal to or greater than ``FromPort`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-connectionportrange.html#cfn-gamelift-containerfleet-connectionportrange-toport
            '''
            result = self._values.get("to_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionPortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.DeploymentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "impairment_strategy": "impairmentStrategy",
            "minimum_healthy_percentage": "minimumHealthyPercentage",
            "protection_strategy": "protectionStrategy",
        },
    )
    class DeploymentConfigurationProperty:
        def __init__(
            self,
            *,
            impairment_strategy: typing.Optional[builtins.str] = None,
            minimum_healthy_percentage: typing.Optional[jsii.Number] = None,
            protection_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Set of rules for processing a deployment for a container fleet update.

            :param impairment_strategy: Determines what actions to take if a deployment fails. If the fleet is multi-location, this strategy applies across all fleet locations. With a rollback strategy, updated fleet instances are rolled back to the last successful deployment. Alternatively, you can maintain a few impaired containers for the purpose of debugging, while all other tasks return to the last successful deployment.
            :param minimum_healthy_percentage: Sets a minimum level of healthy tasks to maintain during deployment activity.
            :param protection_strategy: Determines how fleet deployment activity affects active game sessions on the fleet. With protection, a deployment honors game session protection, and delays actions that would interrupt a protected active game session until the game session ends. Without protection, deployment activity can shut down all running tasks, including active game sessions, regardless of game session protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-deploymentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                deployment_configuration_property = gamelift_mixins.CfnContainerFleetPropsMixin.DeploymentConfigurationProperty(
                    impairment_strategy="impairmentStrategy",
                    minimum_healthy_percentage=123,
                    protection_strategy="protectionStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87bd90e576ee23bcbb2c3e3b3133914729ad9f2a6c5496fd950bb5c30f8a7bca)
                check_type(argname="argument impairment_strategy", value=impairment_strategy, expected_type=type_hints["impairment_strategy"])
                check_type(argname="argument minimum_healthy_percentage", value=minimum_healthy_percentage, expected_type=type_hints["minimum_healthy_percentage"])
                check_type(argname="argument protection_strategy", value=protection_strategy, expected_type=type_hints["protection_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if impairment_strategy is not None:
                self._values["impairment_strategy"] = impairment_strategy
            if minimum_healthy_percentage is not None:
                self._values["minimum_healthy_percentage"] = minimum_healthy_percentage
            if protection_strategy is not None:
                self._values["protection_strategy"] = protection_strategy

        @builtins.property
        def impairment_strategy(self) -> typing.Optional[builtins.str]:
            '''Determines what actions to take if a deployment fails.

            If the fleet is multi-location, this strategy applies across all fleet locations. With a rollback strategy, updated fleet instances are rolled back to the last successful deployment. Alternatively, you can maintain a few impaired containers for the purpose of debugging, while all other tasks return to the last successful deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-deploymentconfiguration.html#cfn-gamelift-containerfleet-deploymentconfiguration-impairmentstrategy
            '''
            result = self._values.get("impairment_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def minimum_healthy_percentage(self) -> typing.Optional[jsii.Number]:
            '''Sets a minimum level of healthy tasks to maintain during deployment activity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-deploymentconfiguration.html#cfn-gamelift-containerfleet-deploymentconfiguration-minimumhealthypercentage
            '''
            result = self._values.get("minimum_healthy_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protection_strategy(self) -> typing.Optional[builtins.str]:
            '''Determines how fleet deployment activity affects active game sessions on the fleet.

            With protection, a deployment honors game session protection, and delays actions that would interrupt a protected active game session until the game session ends. Without protection, deployment activity can shut down all running tasks, including active game sessions, regardless of game session protection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-deploymentconfiguration.html#cfn-gamelift-containerfleet-deploymentconfiguration-protectionstrategy
            '''
            result = self._values.get("protection_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.DeploymentDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"latest_deployment_id": "latestDeploymentId"},
    )
    class DeploymentDetailsProperty:
        def __init__(
            self,
            *,
            latest_deployment_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the most recent deployment for the container fleet.

            :param latest_deployment_id: A unique identifier for a fleet deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-deploymentdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                deployment_details_property = gamelift_mixins.CfnContainerFleetPropsMixin.DeploymentDetailsProperty(
                    latest_deployment_id="latestDeploymentId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__460bd0751f93015f004b51bcccae652b2dc928ac07ac922ec4d17589659bf0a9)
                check_type(argname="argument latest_deployment_id", value=latest_deployment_id, expected_type=type_hints["latest_deployment_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if latest_deployment_id is not None:
                self._values["latest_deployment_id"] = latest_deployment_id

        @builtins.property
        def latest_deployment_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for a fleet deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-deploymentdetails.html#cfn-gamelift-containerfleet-deploymentdetails-latestdeploymentid
            '''
            result = self._values.get("latest_deployment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.GameSessionCreationLimitPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "new_game_sessions_per_creator": "newGameSessionsPerCreator",
            "policy_period_in_minutes": "policyPeriodInMinutes",
        },
    )
    class GameSessionCreationLimitPolicyProperty:
        def __init__(
            self,
            *,
            new_game_sessions_per_creator: typing.Optional[jsii.Number] = None,
            policy_period_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A policy that puts limits on the number of game sessions that a player can create within a specified span of time.

            With this policy, you can control players' ability to consume available resources.

            The policy is evaluated when a player tries to create a new game session. On receiving a ``CreateGameSession`` request, Amazon GameLift Servers checks that the player (identified by ``CreatorId`` ) has created fewer than game session limit in the specified time period.

            :param new_game_sessions_per_creator: A policy that puts limits on the number of game sessions that a player can create within a specified span of time. With this policy, you can control players' ability to consume available resources. The policy evaluates when a player tries to create a new game session. On receiving a ``CreateGameSession`` request, Amazon GameLift Servers checks that the player (identified by ``CreatorId`` ) has created fewer than game session limit in the specified time period.
            :param policy_period_in_minutes: The time span used in evaluating the resource creation limit policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-gamesessioncreationlimitpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                game_session_creation_limit_policy_property = gamelift_mixins.CfnContainerFleetPropsMixin.GameSessionCreationLimitPolicyProperty(
                    new_game_sessions_per_creator=123,
                    policy_period_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__718011e55fcc9480872cc9e20af0c614288873586273958c7e4cb802ed3bf339)
                check_type(argname="argument new_game_sessions_per_creator", value=new_game_sessions_per_creator, expected_type=type_hints["new_game_sessions_per_creator"])
                check_type(argname="argument policy_period_in_minutes", value=policy_period_in_minutes, expected_type=type_hints["policy_period_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if new_game_sessions_per_creator is not None:
                self._values["new_game_sessions_per_creator"] = new_game_sessions_per_creator
            if policy_period_in_minutes is not None:
                self._values["policy_period_in_minutes"] = policy_period_in_minutes

        @builtins.property
        def new_game_sessions_per_creator(self) -> typing.Optional[jsii.Number]:
            '''A policy that puts limits on the number of game sessions that a player can create within a specified span of time.

            With this policy, you can control players' ability to consume available resources.

            The policy evaluates when a player tries to create a new game session. On receiving a ``CreateGameSession`` request, Amazon GameLift Servers checks that the player (identified by ``CreatorId`` ) has created fewer than game session limit in the specified time period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-gamesessioncreationlimitpolicy.html#cfn-gamelift-containerfleet-gamesessioncreationlimitpolicy-newgamesessionspercreator
            '''
            result = self._values.get("new_game_sessions_per_creator")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def policy_period_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The time span used in evaluating the resource creation limit policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-gamesessioncreationlimitpolicy.html#cfn-gamelift-containerfleet-gamesessioncreationlimitpolicy-policyperiodinminutes
            '''
            result = self._values.get("policy_period_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GameSessionCreationLimitPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.IpPermissionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "from_port": "fromPort",
            "ip_range": "ipRange",
            "protocol": "protocol",
            "to_port": "toPort",
        },
    )
    class IpPermissionProperty:
        def __init__(
            self,
            *,
            from_port: typing.Optional[jsii.Number] = None,
            ip_range: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            to_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A range of IP addresses and port settings that allow inbound traffic to connect to processes on an instance in a fleet.

            Processes are assigned an IP address/port number combination, which must fall into the fleet's allowed ranges.

            For Amazon GameLift Servers Realtime fleets, Amazon GameLift Servers automatically opens two port ranges, one for TCP messaging and one for UDP.

            :param from_port: A starting value for a range of allowed port numbers. For fleets using Linux builds, only ports ``22`` and ``1026-60000`` are valid. For fleets using Windows builds, only ports ``1026-60000`` are valid.
            :param ip_range: A range of allowed IP addresses. This value must be expressed in CIDR notation. Example: " ``000.000.000.000/[subnet mask]`` " or optionally the shortened version " ``0.0.0.0/[subnet mask]`` ".
            :param protocol: The network communication protocol used by the fleet.
            :param to_port: An ending value for a range of allowed port numbers. Port numbers are end-inclusive. This value must be equal to or greater than ``FromPort`` . For fleets using Linux builds, only ports ``22`` and ``1026-60000`` are valid. For fleets using Windows builds, only ports ``1026-60000`` are valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-ippermission.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                ip_permission_property = gamelift_mixins.CfnContainerFleetPropsMixin.IpPermissionProperty(
                    from_port=123,
                    ip_range="ipRange",
                    protocol="protocol",
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0745f27d2db98b383642bbc81eadced14044caf456ad25e6316ab8e74b7c8de2)
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument ip_range", value=ip_range, expected_type=type_hints["ip_range"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if from_port is not None:
                self._values["from_port"] = from_port
            if ip_range is not None:
                self._values["ip_range"] = ip_range
            if protocol is not None:
                self._values["protocol"] = protocol
            if to_port is not None:
                self._values["to_port"] = to_port

        @builtins.property
        def from_port(self) -> typing.Optional[jsii.Number]:
            '''A starting value for a range of allowed port numbers.

            For fleets using Linux builds, only ports ``22`` and ``1026-60000`` are valid.

            For fleets using Windows builds, only ports ``1026-60000`` are valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-ippermission.html#cfn-gamelift-containerfleet-ippermission-fromport
            '''
            result = self._values.get("from_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ip_range(self) -> typing.Optional[builtins.str]:
            '''A range of allowed IP addresses.

            This value must be expressed in CIDR notation. Example: " ``000.000.000.000/[subnet mask]`` " or optionally the shortened version " ``0.0.0.0/[subnet mask]`` ".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-ippermission.html#cfn-gamelift-containerfleet-ippermission-iprange
            '''
            result = self._values.get("ip_range")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The network communication protocol used by the fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-ippermission.html#cfn-gamelift-containerfleet-ippermission-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def to_port(self) -> typing.Optional[jsii.Number]:
            '''An ending value for a range of allowed port numbers.

            Port numbers are end-inclusive. This value must be equal to or greater than ``FromPort`` .

            For fleets using Linux builds, only ports ``22`` and ``1026-60000`` are valid.

            For fleets using Windows builds, only ports ``1026-60000`` are valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-ippermission.html#cfn-gamelift-containerfleet-ippermission-toport
            '''
            result = self._values.get("to_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpPermissionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.LocationCapacityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "desired_ec2_instances": "desiredEc2Instances",
            "max_size": "maxSize",
            "min_size": "minSize",
        },
    )
    class LocationCapacityProperty:
        def __init__(
            self,
            *,
            desired_ec2_instances: typing.Optional[jsii.Number] = None,
            max_size: typing.Optional[jsii.Number] = None,
            min_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Current resource capacity settings in a specified fleet or location.

            The location value might refer to a fleet's remote location or its home Region.

            :param desired_ec2_instances: Defaults to MinSize if not defined. The number of EC2 instances you want to maintain in the specified fleet location. This value must fall between the minimum and maximum size limits. If any auto-scaling policy is defined for the container fleet, the desired instance will only be applied once during fleet creation and will be ignored in updates to avoid conflicts with auto-scaling. During updates with any auto-scaling policy defined, if current desired instance is lower than the new MinSize, it will be increased to the new MinSize; if current desired instance is larger than the new MaxSize, it will be decreased to the new MaxSize.
            :param max_size: The maximum value that is allowed for the fleet's instance count for a location.
            :param min_size: The minimum value allowed for the fleet's instance count for a location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-locationcapacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                location_capacity_property = gamelift_mixins.CfnContainerFleetPropsMixin.LocationCapacityProperty(
                    desired_ec2_instances=123,
                    max_size=123,
                    min_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__095e46f30e28a6aa1af3171ee420ac4bf29cbaf5c20516bd4f9ce656b2d64ea6)
                check_type(argname="argument desired_ec2_instances", value=desired_ec2_instances, expected_type=type_hints["desired_ec2_instances"])
                check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
                check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if desired_ec2_instances is not None:
                self._values["desired_ec2_instances"] = desired_ec2_instances
            if max_size is not None:
                self._values["max_size"] = max_size
            if min_size is not None:
                self._values["min_size"] = min_size

        @builtins.property
        def desired_ec2_instances(self) -> typing.Optional[jsii.Number]:
            '''Defaults to MinSize if not defined.

            The number of EC2 instances you want to maintain in the specified fleet location. This value must fall between the minimum and maximum size limits. If any auto-scaling policy is defined for the container fleet, the desired instance will only be applied once during fleet creation and will be ignored in updates to avoid conflicts with auto-scaling. During updates with any auto-scaling policy defined, if current desired instance is lower than the new MinSize, it will be increased to the new MinSize; if current desired instance is larger than the new MaxSize, it will be decreased to the new MaxSize.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-locationcapacity.html#cfn-gamelift-containerfleet-locationcapacity-desiredec2instances
            '''
            result = self._values.get("desired_ec2_instances")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum value that is allowed for the fleet's instance count for a location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-locationcapacity.html#cfn-gamelift-containerfleet-locationcapacity-maxsize
            '''
            result = self._values.get("max_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_size(self) -> typing.Optional[jsii.Number]:
            '''The minimum value allowed for the fleet's instance count for a location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-locationcapacity.html#cfn-gamelift-containerfleet-locationcapacity-minsize
            '''
            result = self._values.get("min_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationCapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.LocationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "location": "location",
            "location_capacity": "locationCapacity",
            "stopped_actions": "stoppedActions",
        },
    )
    class LocationConfigurationProperty:
        def __init__(
            self,
            *,
            location: typing.Optional[builtins.str] = None,
            location_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerFleetPropsMixin.LocationCapacityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stopped_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A remote location where a multi-location fleet can deploy game servers for game hosting.

            :param location: An AWS Region code, such as ``us-west-2`` . For a list of supported Regions and Local Zones, see `Amazon GameLift Servers service locations <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-regions.html>`_ for managed hosting.
            :param location_capacity: Current resource capacity settings in a specified fleet or location. The location value might refer to a fleet's remote location or its home Region.
            :param stopped_actions: A list of fleet actions that have been suspended in the fleet location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-locationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                location_configuration_property = gamelift_mixins.CfnContainerFleetPropsMixin.LocationConfigurationProperty(
                    location="location",
                    location_capacity=gamelift_mixins.CfnContainerFleetPropsMixin.LocationCapacityProperty(
                        desired_ec2_instances=123,
                        max_size=123,
                        min_size=123
                    ),
                    stopped_actions=["stoppedActions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2dc46f078bd9bf4a94109f7130800dc9095d2fee829f4bd4b7cbb21c2bf1eee)
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument location_capacity", value=location_capacity, expected_type=type_hints["location_capacity"])
                check_type(argname="argument stopped_actions", value=stopped_actions, expected_type=type_hints["stopped_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if location is not None:
                self._values["location"] = location
            if location_capacity is not None:
                self._values["location_capacity"] = location_capacity
            if stopped_actions is not None:
                self._values["stopped_actions"] = stopped_actions

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''An AWS Region code, such as ``us-west-2`` .

            For a list of supported Regions and Local Zones, see `Amazon GameLift Servers service locations <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-regions.html>`_ for managed hosting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-locationconfiguration.html#cfn-gamelift-containerfleet-locationconfiguration-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location_capacity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.LocationCapacityProperty"]]:
            '''Current resource capacity settings in a specified fleet or location.

            The location value might refer to a fleet's remote location or its home Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-locationconfiguration.html#cfn-gamelift-containerfleet-locationconfiguration-locationcapacity
            '''
            result = self._values.get("location_capacity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.LocationCapacityProperty"]], result)

        @builtins.property
        def stopped_actions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of fleet actions that have been suspended in the fleet location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-locationconfiguration.html#cfn-gamelift-containerfleet-locationconfiguration-stoppedactions
            '''
            result = self._values.get("stopped_actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_destination": "logDestination",
            "log_group_arn": "logGroupArn",
            "s3_bucket_name": "s3BucketName",
        },
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            log_destination: typing.Optional[builtins.str] = None,
            log_group_arn: typing.Optional[builtins.str] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A method for collecting container logs for the fleet.

            Amazon GameLift Servers saves all standard output for each container in logs, including game session logs. You can select from the following methods:

            :param log_destination: The type of log collection to use for a fleet. - ``CLOUDWATCH`` -- (default value) Send logs to an Amazon CloudWatch log group that you define. Each container emits a log stream, which is organized in the log group. - ``S3`` -- Store logs in an Amazon S3 bucket that you define. This bucket must reside in the fleet's home AWS Region. - ``NONE`` -- Don't collect container logs.
            :param log_group_arn: If log destination is ``CLOUDWATCH`` , logs are sent to the specified log group in Amazon CloudWatch.
            :param s3_bucket_name: If log destination is ``S3`` , logs are sent to the specified Amazon S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                log_configuration_property = gamelift_mixins.CfnContainerFleetPropsMixin.LogConfigurationProperty(
                    log_destination="logDestination",
                    log_group_arn="logGroupArn",
                    s3_bucket_name="s3BucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__343c7a19e92e065d3d2a3f44ff609d3ab378adef3c498013bab4a659e67dd2af)
                check_type(argname="argument log_destination", value=log_destination, expected_type=type_hints["log_destination"])
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_destination is not None:
                self._values["log_destination"] = log_destination
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name

        @builtins.property
        def log_destination(self) -> typing.Optional[builtins.str]:
            '''The type of log collection to use for a fleet.

            - ``CLOUDWATCH`` -- (default value) Send logs to an Amazon CloudWatch log group that you define. Each container emits a log stream, which is organized in the log group.
            - ``S3`` -- Store logs in an Amazon S3 bucket that you define. This bucket must reside in the fleet's home AWS Region.
            - ``NONE`` -- Don't collect container logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-logconfiguration.html#cfn-gamelift-containerfleet-logconfiguration-logdestination
            '''
            result = self._values.get("log_destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''If log destination is ``CLOUDWATCH`` , logs are sent to the specified log group in Amazon CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-logconfiguration.html#cfn-gamelift-containerfleet-logconfiguration-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''If log destination is ``S3`` , logs are sent to the specified Amazon S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-logconfiguration.html#cfn-gamelift-containerfleet-logconfiguration-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
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
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.ScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "evaluation_periods": "evaluationPeriods",
            "metric_name": "metricName",
            "name": "name",
            "policy_type": "policyType",
            "scaling_adjustment": "scalingAdjustment",
            "scaling_adjustment_type": "scalingAdjustmentType",
            "target_configuration": "targetConfiguration",
            "threshold": "threshold",
        },
    )
    class ScalingPolicyProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            evaluation_periods: typing.Optional[jsii.Number] = None,
            metric_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            policy_type: typing.Optional[builtins.str] = None,
            scaling_adjustment: typing.Optional[jsii.Number] = None,
            scaling_adjustment_type: typing.Optional[builtins.str] = None,
            target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerFleetPropsMixin.TargetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Rule that controls how a fleet is scaled.

            Scaling policies are uniquely identified by the combination of name and fleet ID.

            :param comparison_operator: Comparison operator to use when measuring a metric against the threshold value.
            :param evaluation_periods: Length of time (in minutes) the metric must be at or beyond the threshold before a scaling event is triggered.
            :param metric_name: Name of the Amazon GameLift Servers-defined metric that is used to trigger a scaling adjustment. For detailed descriptions of fleet metrics, see `Monitor Amazon GameLift Servers with Amazon CloudWatch <https://docs.aws.amazon.com/gamelift/latest/developerguide/monitoring-cloudwatch.html>`_ . - *ActivatingGameSessions* -- Game sessions in the process of being created. - *ActiveGameSessions* -- Game sessions that are currently running. - *ActiveInstances* -- Fleet instances that are currently running at least one game session. - *AvailableGameSessions* -- Additional game sessions that fleet could host simultaneously, given current capacity. - *AvailablePlayerSessions* -- Empty player slots in currently active game sessions. This includes game sessions that are not currently accepting players. Reserved player slots are not included. - *CurrentPlayerSessions* -- Player slots in active game sessions that are being used by a player or are reserved for a player. - *IdleInstances* -- Active instances that are currently hosting zero game sessions. - *PercentAvailableGameSessions* -- Unused percentage of the total number of game sessions that a fleet could host simultaneously, given current capacity. Use this metric for a target-based scaling policy. - *PercentIdleInstances* -- Percentage of the total number of active instances that are hosting zero game sessions. - *QueueDepth* -- Pending game session placement requests, in any queue, where the current fleet is the top-priority destination. - *WaitTime* -- Current wait time for pending game session placement requests, in any queue, where the current fleet is the top-priority destination.
            :param name: A descriptive label that is associated with a fleet's scaling policy. Policy names do not need to be unique.
            :param policy_type: The type of scaling policy to create. For a target-based policy, set the parameter *MetricName* to 'PercentAvailableGameSessions' and specify a *TargetConfiguration* . For a rule-based policy set the following parameters: *MetricName* , *ComparisonOperator* , *Threshold* , *EvaluationPeriods* , *ScalingAdjustmentType* , and *ScalingAdjustment* .
            :param scaling_adjustment: Amount of adjustment to make, based on the scaling adjustment type.
            :param scaling_adjustment_type: The type of adjustment to make to a fleet's instance count. - *ChangeInCapacity* -- add (or subtract) the scaling adjustment value from the current instance count. Positive values scale up while negative values scale down. - *ExactCapacity* -- set the instance count to the scaling adjustment value. - *PercentChangeInCapacity* -- increase or reduce the current instance count by the scaling adjustment, read as a percentage. Positive values scale up while negative values scale down.
            :param target_configuration: An object that contains settings for a target-based scaling policy.
            :param threshold: Metric value used to trigger a scaling event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                scaling_policy_property = gamelift_mixins.CfnContainerFleetPropsMixin.ScalingPolicyProperty(
                    comparison_operator="comparisonOperator",
                    evaluation_periods=123,
                    metric_name="metricName",
                    name="name",
                    policy_type="policyType",
                    scaling_adjustment=123,
                    scaling_adjustment_type="scalingAdjustmentType",
                    target_configuration=gamelift_mixins.CfnContainerFleetPropsMixin.TargetConfigurationProperty(
                        target_value=123
                    ),
                    threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b63a4d8b9482488dabe8dd8072c7e3d78fddd9985ea3e1f10cb9ca80ce58b62b)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
                check_type(argname="argument scaling_adjustment", value=scaling_adjustment, expected_type=type_hints["scaling_adjustment"])
                check_type(argname="argument scaling_adjustment_type", value=scaling_adjustment_type, expected_type=type_hints["scaling_adjustment_type"])
                check_type(argname="argument target_configuration", value=target_configuration, expected_type=type_hints["target_configuration"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if evaluation_periods is not None:
                self._values["evaluation_periods"] = evaluation_periods
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if name is not None:
                self._values["name"] = name
            if policy_type is not None:
                self._values["policy_type"] = policy_type
            if scaling_adjustment is not None:
                self._values["scaling_adjustment"] = scaling_adjustment
            if scaling_adjustment_type is not None:
                self._values["scaling_adjustment_type"] = scaling_adjustment_type
            if target_configuration is not None:
                self._values["target_configuration"] = target_configuration
            if threshold is not None:
                self._values["threshold"] = threshold

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''Comparison operator to use when measuring a metric against the threshold value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html#cfn-gamelift-containerfleet-scalingpolicy-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluation_periods(self) -> typing.Optional[jsii.Number]:
            '''Length of time (in minutes) the metric must be at or beyond the threshold before a scaling event is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html#cfn-gamelift-containerfleet-scalingpolicy-evaluationperiods
            '''
            result = self._values.get("evaluation_periods")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''Name of the Amazon GameLift Servers-defined metric that is used to trigger a scaling adjustment.

            For detailed descriptions of fleet metrics, see `Monitor Amazon GameLift Servers with Amazon CloudWatch <https://docs.aws.amazon.com/gamelift/latest/developerguide/monitoring-cloudwatch.html>`_ .

            - *ActivatingGameSessions* -- Game sessions in the process of being created.
            - *ActiveGameSessions* -- Game sessions that are currently running.
            - *ActiveInstances* -- Fleet instances that are currently running at least one game session.
            - *AvailableGameSessions* -- Additional game sessions that fleet could host simultaneously, given current capacity.
            - *AvailablePlayerSessions* -- Empty player slots in currently active game sessions. This includes game sessions that are not currently accepting players. Reserved player slots are not included.
            - *CurrentPlayerSessions* -- Player slots in active game sessions that are being used by a player or are reserved for a player.
            - *IdleInstances* -- Active instances that are currently hosting zero game sessions.
            - *PercentAvailableGameSessions* -- Unused percentage of the total number of game sessions that a fleet could host simultaneously, given current capacity. Use this metric for a target-based scaling policy.
            - *PercentIdleInstances* -- Percentage of the total number of active instances that are hosting zero game sessions.
            - *QueueDepth* -- Pending game session placement requests, in any queue, where the current fleet is the top-priority destination.
            - *WaitTime* -- Current wait time for pending game session placement requests, in any queue, where the current fleet is the top-priority destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html#cfn-gamelift-containerfleet-scalingpolicy-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A descriptive label that is associated with a fleet's scaling policy.

            Policy names do not need to be unique.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html#cfn-gamelift-containerfleet-scalingpolicy-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_type(self) -> typing.Optional[builtins.str]:
            '''The type of scaling policy to create.

            For a target-based policy, set the parameter *MetricName* to 'PercentAvailableGameSessions' and specify a *TargetConfiguration* . For a rule-based policy set the following parameters: *MetricName* , *ComparisonOperator* , *Threshold* , *EvaluationPeriods* , *ScalingAdjustmentType* , and *ScalingAdjustment* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html#cfn-gamelift-containerfleet-scalingpolicy-policytype
            '''
            result = self._values.get("policy_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
            '''Amount of adjustment to make, based on the scaling adjustment type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html#cfn-gamelift-containerfleet-scalingpolicy-scalingadjustment
            '''
            result = self._values.get("scaling_adjustment")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scaling_adjustment_type(self) -> typing.Optional[builtins.str]:
            '''The type of adjustment to make to a fleet's instance count.

            - *ChangeInCapacity* -- add (or subtract) the scaling adjustment value from the current instance count. Positive values scale up while negative values scale down.
            - *ExactCapacity* -- set the instance count to the scaling adjustment value.
            - *PercentChangeInCapacity* -- increase or reduce the current instance count by the scaling adjustment, read as a percentage. Positive values scale up while negative values scale down.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html#cfn-gamelift-containerfleet-scalingpolicy-scalingadjustmenttype
            '''
            result = self._values.get("scaling_adjustment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.TargetConfigurationProperty"]]:
            '''An object that contains settings for a target-based scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html#cfn-gamelift-containerfleet-scalingpolicy-targetconfiguration
            '''
            result = self._values.get("target_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerFleetPropsMixin.TargetConfigurationProperty"]], result)

        @builtins.property
        def threshold(self) -> typing.Optional[jsii.Number]:
            '''Metric value used to trigger a scaling event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-scalingpolicy.html#cfn-gamelift-containerfleet-scalingpolicy-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerFleetPropsMixin.TargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"target_value": "targetValue"},
    )
    class TargetConfigurationProperty:
        def __init__(
            self,
            *,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Settings for a target-based scaling policy.

            A target-based policy tracks a particular fleet metric specifies a target value for the metric. As player usage changes, the policy triggers Amazon GameLift Servers to adjust capacity so that the metric returns to the target value. The target configuration specifies settings as needed for the target based policy, including the target value.

            :param target_value: Desired value to use with a target-based scaling policy. The value must be relevant for whatever metric the scaling policy is using. For example, in a policy using the metric PercentAvailableGameSessions, the target value should be the preferred size of the fleet's buffer (the percent of capacity that should be idle and ready for new game sessions).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-targetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                target_configuration_property = gamelift_mixins.CfnContainerFleetPropsMixin.TargetConfigurationProperty(
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33dd30c51d7e2f526bdc1b2e98bbe27b76233551efe9ac250dd16488d5851024)
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''Desired value to use with a target-based scaling policy.

            The value must be relevant for whatever metric the scaling policy is using. For example, in a policy using the metric PercentAvailableGameSessions, the target value should be the preferred size of the fleet's buffer (the percent of capacity that should be idle and ready for new game sessions).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containerfleet-targetconfiguration.html#cfn-gamelift-containerfleet-targetconfiguration-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_group_type": "containerGroupType",
        "game_server_container_definition": "gameServerContainerDefinition",
        "name": "name",
        "operating_system": "operatingSystem",
        "source_version_number": "sourceVersionNumber",
        "support_container_definitions": "supportContainerDefinitions",
        "tags": "tags",
        "total_memory_limit_mebibytes": "totalMemoryLimitMebibytes",
        "total_vcpu_limit": "totalVcpuLimit",
        "version_description": "versionDescription",
    },
)
class CfnContainerGroupDefinitionMixinProps:
    def __init__(
        self,
        *,
        container_group_type: typing.Optional[builtins.str] = None,
        game_server_container_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.GameServerContainerDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        operating_system: typing.Optional[builtins.str] = None,
        source_version_number: typing.Optional[jsii.Number] = None,
        support_container_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.SupportContainerDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        total_memory_limit_mebibytes: typing.Optional[jsii.Number] = None,
        total_vcpu_limit: typing.Optional[jsii.Number] = None,
        version_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnContainerGroupDefinitionPropsMixin.

        :param container_group_type: The type of container group. Container group type determines how Amazon GameLift Servers deploys the container group on each fleet instance.
        :param game_server_container_definition: The definition for the game server container in this group. This property is used only when the container group type is ``GAME_SERVER`` . This container definition specifies a container image with the game server build.
        :param name: A descriptive identifier for the container group definition. The name value is unique in an AWS Region.
        :param operating_system: The platform that all containers in the container group definition run on. .. epigraph:: Amazon Linux 2 (AL2) will reach end of support on 6/30/2026. See more details in the `Amazon Linux 2 FAQs <https://docs.aws.amazon.com/amazon-linux-2/faqs/>`_ . For game servers that are hosted on AL2 and use server SDK version 4.x for Amazon GameLift Servers, first update the game server build to server SDK 5.x, and then deploy to AL2023 instances. See `Migrate to server SDK version 5. <https://docs.aws.amazon.com/gamelift/latest/developerguide/reference-serversdk5-migration.html>`_
        :param source_version_number: A specific ContainerGroupDefinition version to be updated.
        :param support_container_definitions: The set of definitions for support containers in this group. A container group definition might have zero support container definitions. Support container can be used in any type of container group.
        :param tags: An array of key-value pairs to apply to this resource.
        :param total_memory_limit_mebibytes: The amount of memory (in MiB) on a fleet instance to allocate for the container group. All containers in the group share these resources. You can set a limit for each container definition in the group. If individual containers have limits, this total value must be greater than any individual container's memory limit.
        :param total_vcpu_limit: The amount of vCPU units on a fleet instance to allocate for the container group (1 vCPU is equal to 1024 CPU units). All containers in the group share these resources. You can set a limit for each container definition in the group. If individual containers have limits, this total value must be equal to or greater than the sum of the limits for each container in the group.
        :param version_description: An optional description that was provided for a container group definition update. Each version can have a unique description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_container_group_definition_mixin_props = gamelift_mixins.CfnContainerGroupDefinitionMixinProps(
                container_group_type="containerGroupType",
                game_server_container_definition=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.GameServerContainerDefinitionProperty(
                    container_name="containerName",
                    depends_on=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty(
                        condition="condition",
                        container_name="containerName"
                    )],
                    environment_override=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty(
                        name="name",
                        value="value"
                    )],
                    image_uri="imageUri",
                    mount_points=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty(
                        access_level="accessLevel",
                        container_path="containerPath",
                        instance_path="instancePath"
                    )],
                    port_configuration=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty(
                        container_port_ranges=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty(
                            from_port=123,
                            protocol="protocol",
                            to_port=123
                        )]
                    ),
                    resolved_image_digest="resolvedImageDigest",
                    server_sdk_version="serverSdkVersion"
                ),
                name="name",
                operating_system="operatingSystem",
                source_version_number=123,
                support_container_definitions=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.SupportContainerDefinitionProperty(
                    container_name="containerName",
                    depends_on=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty(
                        condition="condition",
                        container_name="containerName"
                    )],
                    environment_override=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty(
                        name="name",
                        value="value"
                    )],
                    essential=False,
                    health_check=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerHealthCheckProperty(
                        command=["command"],
                        interval=123,
                        retries=123,
                        start_period=123,
                        timeout=123
                    ),
                    image_uri="imageUri",
                    memory_hard_limit_mebibytes=123,
                    mount_points=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty(
                        access_level="accessLevel",
                        container_path="containerPath",
                        instance_path="instancePath"
                    )],
                    port_configuration=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty(
                        container_port_ranges=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty(
                            from_port=123,
                            protocol="protocol",
                            to_port=123
                        )]
                    ),
                    resolved_image_digest="resolvedImageDigest",
                    vcpu=123
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                total_memory_limit_mebibytes=123,
                total_vcpu_limit=123,
                version_description="versionDescription"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a35eb32d22f0e925d0cb226e23c0a6539c8f43017917db7508de7a80610a75)
            check_type(argname="argument container_group_type", value=container_group_type, expected_type=type_hints["container_group_type"])
            check_type(argname="argument game_server_container_definition", value=game_server_container_definition, expected_type=type_hints["game_server_container_definition"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
            check_type(argname="argument source_version_number", value=source_version_number, expected_type=type_hints["source_version_number"])
            check_type(argname="argument support_container_definitions", value=support_container_definitions, expected_type=type_hints["support_container_definitions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument total_memory_limit_mebibytes", value=total_memory_limit_mebibytes, expected_type=type_hints["total_memory_limit_mebibytes"])
            check_type(argname="argument total_vcpu_limit", value=total_vcpu_limit, expected_type=type_hints["total_vcpu_limit"])
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_group_type is not None:
            self._values["container_group_type"] = container_group_type
        if game_server_container_definition is not None:
            self._values["game_server_container_definition"] = game_server_container_definition
        if name is not None:
            self._values["name"] = name
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if source_version_number is not None:
            self._values["source_version_number"] = source_version_number
        if support_container_definitions is not None:
            self._values["support_container_definitions"] = support_container_definitions
        if tags is not None:
            self._values["tags"] = tags
        if total_memory_limit_mebibytes is not None:
            self._values["total_memory_limit_mebibytes"] = total_memory_limit_mebibytes
        if total_vcpu_limit is not None:
            self._values["total_vcpu_limit"] = total_vcpu_limit
        if version_description is not None:
            self._values["version_description"] = version_description

    @builtins.property
    def container_group_type(self) -> typing.Optional[builtins.str]:
        '''The type of container group.

        Container group type determines how Amazon GameLift Servers deploys the container group on each fleet instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-containergrouptype
        '''
        result = self._values.get("container_group_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def game_server_container_definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.GameServerContainerDefinitionProperty"]]:
        '''The definition for the game server container in this group.

        This property is used only when the container group type is ``GAME_SERVER`` . This container definition specifies a container image with the game server build.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-gameservercontainerdefinition
        '''
        result = self._values.get("game_server_container_definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.GameServerContainerDefinitionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A descriptive identifier for the container group definition.

        The name value is unique in an AWS Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''The platform that all containers in the container group definition run on.

        .. epigraph::

           Amazon Linux 2 (AL2) will reach end of support on 6/30/2026. See more details in the `Amazon Linux 2 FAQs <https://docs.aws.amazon.com/amazon-linux-2/faqs/>`_ . For game servers that are hosted on AL2 and use server SDK version 4.x for Amazon GameLift Servers, first update the game server build to server SDK 5.x, and then deploy to AL2023 instances. See `Migrate to server SDK version 5. <https://docs.aws.amazon.com/gamelift/latest/developerguide/reference-serversdk5-migration.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-operatingsystem
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_version_number(self) -> typing.Optional[jsii.Number]:
        '''A specific ContainerGroupDefinition version to be updated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-sourceversionnumber
        '''
        result = self._values.get("source_version_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def support_container_definitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.SupportContainerDefinitionProperty"]]]]:
        '''The set of definitions for support containers in this group.

        A container group definition might have zero support container definitions. Support container can be used in any type of container group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinitions
        '''
        result = self._values.get("support_container_definitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.SupportContainerDefinitionProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def total_memory_limit_mebibytes(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory (in MiB) on a fleet instance to allocate for the container group.

        All containers in the group share these resources.

        You can set a limit for each container definition in the group. If individual containers have limits, this total value must be greater than any individual container's memory limit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-totalmemorylimitmebibytes
        '''
        result = self._values.get("total_memory_limit_mebibytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def total_vcpu_limit(self) -> typing.Optional[jsii.Number]:
        '''The amount of vCPU units on a fleet instance to allocate for the container group (1 vCPU is equal to 1024 CPU units).

        All containers in the group share these resources. You can set a limit for each container definition in the group. If individual containers have limits, this total value must be equal to or greater than the sum of the limits for each container in the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-totalvcpulimit
        '''
        result = self._values.get("total_vcpu_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version_description(self) -> typing.Optional[builtins.str]:
        '''An optional description that was provided for a container group definition update.

        Each version can have a unique description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html#cfn-gamelift-containergroupdefinition-versiondescription
        '''
        result = self._values.get("version_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContainerGroupDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContainerGroupDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionPropsMixin",
):
    '''The properties that describe a container group resource.

    You can update all properties of a container group definition properties. Updates to a container group definition are saved as new versions.

    *Used with:* `CreateContainerGroupDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_CreateContainerGroupDefinition.html>`_

    *Returned by:* `DescribeContainerGroupDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeContainerGroupDefinition.html>`_ , `ListContainerGroupDefinitions <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ListContainerGroupDefinitions.html>`_ , `UpdateContainerGroupDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateContainerGroupDefinition.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-containergroupdefinition.html
    :cloudformationResource: AWS::GameLift::ContainerGroupDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_container_group_definition_props_mixin = gamelift_mixins.CfnContainerGroupDefinitionPropsMixin(gamelift_mixins.CfnContainerGroupDefinitionMixinProps(
            container_group_type="containerGroupType",
            game_server_container_definition=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.GameServerContainerDefinitionProperty(
                container_name="containerName",
                depends_on=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty(
                    condition="condition",
                    container_name="containerName"
                )],
                environment_override=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty(
                    name="name",
                    value="value"
                )],
                image_uri="imageUri",
                mount_points=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty(
                    access_level="accessLevel",
                    container_path="containerPath",
                    instance_path="instancePath"
                )],
                port_configuration=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty(
                    container_port_ranges=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty(
                        from_port=123,
                        protocol="protocol",
                        to_port=123
                    )]
                ),
                resolved_image_digest="resolvedImageDigest",
                server_sdk_version="serverSdkVersion"
            ),
            name="name",
            operating_system="operatingSystem",
            source_version_number=123,
            support_container_definitions=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.SupportContainerDefinitionProperty(
                container_name="containerName",
                depends_on=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty(
                    condition="condition",
                    container_name="containerName"
                )],
                environment_override=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty(
                    name="name",
                    value="value"
                )],
                essential=False,
                health_check=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerHealthCheckProperty(
                    command=["command"],
                    interval=123,
                    retries=123,
                    start_period=123,
                    timeout=123
                ),
                image_uri="imageUri",
                memory_hard_limit_mebibytes=123,
                mount_points=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty(
                    access_level="accessLevel",
                    container_path="containerPath",
                    instance_path="instancePath"
                )],
                port_configuration=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty(
                    container_port_ranges=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty(
                        from_port=123,
                        protocol="protocol",
                        to_port=123
                    )]
                ),
                resolved_image_digest="resolvedImageDigest",
                vcpu=123
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            total_memory_limit_mebibytes=123,
            total_vcpu_limit=123,
            version_description="versionDescription"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnContainerGroupDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::ContainerGroupDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf1d2f7d79c08dc598e10352eeed50c2ea1ff41003e44786c008e1c454dafc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68a2efae64cd9790582184d2cba9a66f60a6a84a63b96364f27ce09b7a84d47d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__749c680059ce24f7babecaad07614f8decf04b0445e71cf5d8130f99a5cf7e14)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContainerGroupDefinitionMixinProps:
        return typing.cast(CfnContainerGroupDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty",
        jsii_struct_bases=[],
        name_mapping={"condition": "condition", "container_name": "containerName"},
    )
    class ContainerDependencyProperty:
        def __init__(
            self,
            *,
            condition: typing.Optional[builtins.str] = None,
            container_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A container's dependency on another container in the same container group.

            The dependency impacts how the dependent container is able to start or shut down based the status of the other container.

            For example, *ContainerA* is configured with the following dependency: a ``START`` dependency on *ContainerB* . This means that *ContainerA* can't start until *ContainerB* has started. It also means that *ContainerA* must shut down before *ContainerB* .

            *Part of:* `GameServerContainerDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_GameServerContainerDefinition.html>`_ , `GameServerContainerDefinitionInput <https://docs.aws.amazon.com/gamelift/latest/apireference/API_GameServerContainerDefinitionInput.html>`_ , `SupportContainerDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_SupportContainerDefinition.html>`_ , `SupportContainerDefinitionInput <https://docs.aws.amazon.com/gamelift/latest/apireference/API_SupportContainerDefinitionInput.html>`_

            :param condition: The condition that the dependency container must reach before the dependent container can start. Valid conditions include:. - START - The dependency container must have started. - COMPLETE - The dependency container has run to completion (exits). Use this condition with nonessential containers, such as those that run a script and then exit. The dependency container can't be an essential container. - SUCCESS - The dependency container has run to completion and exited with a zero status. The dependency container can't be an essential container. - HEALTHY - The dependency container has passed its Docker health check. Use this condition with dependency containers that have health checks configured. This condition is confirmed at container group startup only.
            :param container_name: A descriptive label for the container definition that this container depends on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerdependency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                container_dependency_property = gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty(
                    condition="condition",
                    container_name="containerName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66d3ca2a3305364f5eb068f233c995a7bd218639848f125a57a4307e5e1168ac)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition is not None:
                self._values["condition"] = condition
            if container_name is not None:
                self._values["container_name"] = container_name

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''The condition that the dependency container must reach before the dependent container can start. Valid conditions include:.

            - START - The dependency container must have started.
            - COMPLETE - The dependency container has run to completion (exits). Use this condition with nonessential containers, such as those that run a script and then exit. The dependency container can't be an essential container.
            - SUCCESS - The dependency container has run to completion and exited with a zero status. The dependency container can't be an essential container.
            - HEALTHY - The dependency container has passed its Docker health check. Use this condition with dependency containers that have health checks configured. This condition is confirmed at container group startup only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerdependency.html#cfn-gamelift-containergroupdefinition-containerdependency-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def container_name(self) -> typing.Optional[builtins.str]:
            '''A descriptive label for the container definition that this container depends on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerdependency.html#cfn-gamelift-containergroupdefinition-containerdependency-containername
            '''
            result = self._values.get("container_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerDependencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ContainerEnvironmentProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An environment variable to set inside a container, in the form of a key-value pair.

            *Part of:* `GameServerContainerDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_GameServerContainerDefinition.html>`_ , `GameServerContainerDefinitionInput <https://docs.aws.amazon.com/gamelift/latest/apireference/API_GameServerContainerDefinitionInput.html>`_ , `SupportContainerDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_SupportContainerDefinition.html>`_ , `SupportContainerDefinitionInput <https://docs.aws.amazon.com/gamelift/latest/apireference/API_SupportContainerDefinitionInput.html>`_

            :param name: The environment variable name.
            :param value: The environment variable value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerenvironment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                container_environment_property = gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__553c5176d1d6922da5395ad7f47b3590f2e0aa9625a100de27c24b2e8ef4bf7c)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The environment variable name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerenvironment.html#cfn-gamelift-containergroupdefinition-containerenvironment-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The environment variable value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerenvironment.html#cfn-gamelift-containergroupdefinition-containerenvironment-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerEnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionPropsMixin.ContainerHealthCheckProperty",
        jsii_struct_bases=[],
        name_mapping={
            "command": "command",
            "interval": "interval",
            "retries": "retries",
            "start_period": "startPeriod",
            "timeout": "timeout",
        },
    )
    class ContainerHealthCheckProperty:
        def __init__(
            self,
            *,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            interval: typing.Optional[jsii.Number] = None,
            retries: typing.Optional[jsii.Number] = None,
            start_period: typing.Optional[jsii.Number] = None,
            timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Instructions on when and how to check the health of a support container in a container fleet.

            These properties override any Docker health checks that are set in the container image. For more information on container health checks, see `HealthCheck command <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_HealthCheck.html#ECS-Type-HealthCheck-command>`_ in the *Amazon Elastic Container Service API* . Game server containers don't have a health check parameter; Amazon GameLift Servers automatically handles health checks for these containers.

            The following example instructs the container to initiate a health check command every 60 seconds and wait 10 seconds for it to succeed. If it fails, retry the command 3 times before flagging the container as unhealthy. It also tells the container to wait 100 seconds after launch before counting failed health checks.

            ``{"Command": [ "CMD-SHELL", "ps cax | grep "processmanager" || exit 1" ], "Interval": 60, "Timeout": 10, "Retries": 3, "StartPeriod": 100 }``

            *Part of:* `SupportContainerDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_SupportContainerDefinition.html>`_ , `SupportContainerDefinitionInput <https://docs.aws.amazon.com/gamelift/latest/apireference/API_SupportContainerDefinitionInput.html>`_

            :param command: A string array that specifies the command that the container runs to determine if it's healthy.
            :param interval: The time period (in seconds) between each health check.
            :param retries: The number of times to retry a failed health check before flagging the container unhealthy. The first run of the command does not count as a retry.
            :param start_period: The optional grace period (in seconds) to give a container time to bootstrap before the first failed health check counts toward the number of retries.
            :param timeout: The time period (in seconds) to wait for a health check to succeed before counting a failed health check.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerhealthcheck.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                container_health_check_property = gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerHealthCheckProperty(
                    command=["command"],
                    interval=123,
                    retries=123,
                    start_period=123,
                    timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6f386832e8b9ef268f5af36107df2d70cc755dcc2c02fcca12801cf9e4da04c)
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
                check_type(argname="argument start_period", value=start_period, expected_type=type_hints["start_period"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command is not None:
                self._values["command"] = command
            if interval is not None:
                self._values["interval"] = interval
            if retries is not None:
                self._values["retries"] = retries
            if start_period is not None:
                self._values["start_period"] = start_period
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A string array that specifies the command that the container runs to determine if it's healthy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerhealthcheck.html#cfn-gamelift-containergroupdefinition-containerhealthcheck-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            '''The time period (in seconds) between each health check.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerhealthcheck.html#cfn-gamelift-containergroupdefinition-containerhealthcheck-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def retries(self) -> typing.Optional[jsii.Number]:
            '''The number of times to retry a failed health check before flagging the container unhealthy.

            The first run of the command does not count as a retry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerhealthcheck.html#cfn-gamelift-containergroupdefinition-containerhealthcheck-retries
            '''
            result = self._values.get("retries")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def start_period(self) -> typing.Optional[jsii.Number]:
            '''The optional grace period (in seconds) to give a container time to bootstrap before the first failed health check counts toward the number of retries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerhealthcheck.html#cfn-gamelift-containergroupdefinition-containerhealthcheck-startperiod
            '''
            result = self._values.get("start_period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The time period (in seconds) to wait for a health check to succeed before counting a failed health check.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerhealthcheck.html#cfn-gamelift-containergroupdefinition-containerhealthcheck-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerHealthCheckProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_level": "accessLevel",
            "container_path": "containerPath",
            "instance_path": "instancePath",
        },
    )
    class ContainerMountPointProperty:
        def __init__(
            self,
            *,
            access_level: typing.Optional[builtins.str] = None,
            container_path: typing.Optional[builtins.str] = None,
            instance_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A mount point that binds a container to a file or directory on the host system.

            *Part of:* `GameServerContainerDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_GameServerContainerDefinition.html>`_ , ` <https://docs.aws.amazon.com/gamelift/latest/apireference/API_GameServerContainerDefinitionInput.html>`_ , `SupportContainerDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_SupportContainerDefinition.html>`_ , ` <https://docs.aws.amazon.com/gamelift/latest/apireference/API_SupportContainerDefinitionInput.html>`_

            :param access_level: The type of access for the container.
            :param container_path: The mount path on the container. If this property isn't set, the instance path is used.
            :param instance_path: The path to the source file or directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containermountpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                container_mount_point_property = gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty(
                    access_level="accessLevel",
                    container_path="containerPath",
                    instance_path="instancePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2198c218d347b478d50031ef2c06d9527ece48e768bc850117aa5f26b486b89c)
                check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
                check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
                check_type(argname="argument instance_path", value=instance_path, expected_type=type_hints["instance_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_level is not None:
                self._values["access_level"] = access_level
            if container_path is not None:
                self._values["container_path"] = container_path
            if instance_path is not None:
                self._values["instance_path"] = instance_path

        @builtins.property
        def access_level(self) -> typing.Optional[builtins.str]:
            '''The type of access for the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containermountpoint.html#cfn-gamelift-containergroupdefinition-containermountpoint-accesslevel
            '''
            result = self._values.get("access_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def container_path(self) -> typing.Optional[builtins.str]:
            '''The mount path on the container.

            If this property isn't set, the instance path is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containermountpoint.html#cfn-gamelift-containergroupdefinition-containermountpoint-containerpath
            '''
            result = self._values.get("container_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_path(self) -> typing.Optional[builtins.str]:
            '''The path to the source file or directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containermountpoint.html#cfn-gamelift-containergroupdefinition-containermountpoint-instancepath
            '''
            result = self._values.get("instance_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerMountPointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "from_port": "fromPort",
            "protocol": "protocol",
            "to_port": "toPort",
        },
    )
    class ContainerPortRangeProperty:
        def __init__(
            self,
            *,
            from_port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
            to_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A set of one or more port numbers that can be opened on the container, and the supported network protocol.

            *Part of:* `ContainerPortConfiguration <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ContainerPortConfiguration.html>`_

            :param from_port: A starting value for the range of allowed port numbers.
            :param protocol: The network protocol that these ports support.
            :param to_port: An ending value for the range of allowed port numbers. Port numbers are end-inclusive. This value must be equal to or greater than ``FromPort`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerportrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                container_port_range_property = gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty(
                    from_port=123,
                    protocol="protocol",
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__031b98314d098a0da56eabdc02c9707db046e38c4c7bbba91e94b7fd2a2cc37e)
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if from_port is not None:
                self._values["from_port"] = from_port
            if protocol is not None:
                self._values["protocol"] = protocol
            if to_port is not None:
                self._values["to_port"] = to_port

        @builtins.property
        def from_port(self) -> typing.Optional[jsii.Number]:
            '''A starting value for the range of allowed port numbers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerportrange.html#cfn-gamelift-containergroupdefinition-containerportrange-fromport
            '''
            result = self._values.get("from_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The network protocol that these ports support.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerportrange.html#cfn-gamelift-containergroupdefinition-containerportrange-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def to_port(self) -> typing.Optional[jsii.Number]:
            '''An ending value for the range of allowed port numbers.

            Port numbers are end-inclusive. This value must be equal to or greater than ``FromPort`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-containerportrange.html#cfn-gamelift-containergroupdefinition-containerportrange-toport
            '''
            result = self._values.get("to_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerPortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionPropsMixin.GameServerContainerDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_name": "containerName",
            "depends_on": "dependsOn",
            "environment_override": "environmentOverride",
            "image_uri": "imageUri",
            "mount_points": "mountPoints",
            "port_configuration": "portConfiguration",
            "resolved_image_digest": "resolvedImageDigest",
            "server_sdk_version": "serverSdkVersion",
        },
    )
    class GameServerContainerDefinitionProperty:
        def __init__(
            self,
            *,
            container_name: typing.Optional[builtins.str] = None,
            depends_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            environment_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            image_uri: typing.Optional[builtins.str] = None,
            mount_points: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            port_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resolved_image_digest: typing.Optional[builtins.str] = None,
            server_sdk_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the game server container in an existing game server container group.

            A game server container identifies a container image with your game server build. A game server container is automatically considered essential; if an essential container fails, the entire container group restarts.

            You can update a container definition and deploy the updates to an existing fleet. When creating or updating a game server container group definition, use the property ` <https://docs.aws.amazon.com/gamelift/latest/apireference/API_GameServerContainerDefinitionInput>`_ .

            *Part of:* `ContainerGroupDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ContainerGroupDefinition.html>`_

            *Returned by:* `DescribeContainerGroupDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeContainerGroupDefinition.html>`_ , `ListContainerGroupDefinitions <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ListContainerGroupDefinitions.html>`_ , `UpdateContainerGroupDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateContainerGroupDefinition.html>`_

            :param container_name: The container definition identifier. Container names are unique within a container group definition.
            :param depends_on: Indicates that the container relies on the status of other containers in the same container group during startup and shutdown sequences. A container might have dependencies on multiple containers.
            :param environment_override: A set of environment variables that's passed to the container on startup. See the `ContainerDefinition::environment <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDefinition.html#ECS-Type-ContainerDefinition-environment>`_ parameter in the *Amazon Elastic Container Service API Reference* .
            :param image_uri: The URI to the image that Amazon GameLift Servers uses when deploying this container to a container fleet. For a more specific identifier, see ``ResolvedImageDigest`` .
            :param mount_points: A mount point that binds a path inside the container to a file or directory on the host system and lets it access the file or directory.
            :param port_configuration: The set of ports that are available to bind to processes in the container. For example, a game server process requires a container port to allow game clients to connect to it. Container ports aren't directly accessed by inbound traffic. Amazon GameLift Servers maps these container ports to externally accessible connection ports, which are assigned as needed from the container fleet's ``ConnectionPortRange`` .
            :param resolved_image_digest: A unique and immutable identifier for the container image. The digest is a SHA 256 hash of the container image manifest.
            :param server_sdk_version: The Amazon GameLift Servers server SDK version that the game server is integrated with. Only game servers using 5.2.0 or higher are compatible with container fleets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-gameservercontainerdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                game_server_container_definition_property = gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.GameServerContainerDefinitionProperty(
                    container_name="containerName",
                    depends_on=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty(
                        condition="condition",
                        container_name="containerName"
                    )],
                    environment_override=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty(
                        name="name",
                        value="value"
                    )],
                    image_uri="imageUri",
                    mount_points=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty(
                        access_level="accessLevel",
                        container_path="containerPath",
                        instance_path="instancePath"
                    )],
                    port_configuration=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty(
                        container_port_ranges=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty(
                            from_port=123,
                            protocol="protocol",
                            to_port=123
                        )]
                    ),
                    resolved_image_digest="resolvedImageDigest",
                    server_sdk_version="serverSdkVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c706d3ce0d959f9b6ae51cd8783eb941c2fc6dde096fd98c74c030892f3e2e35)
                check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
                check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
                check_type(argname="argument environment_override", value=environment_override, expected_type=type_hints["environment_override"])
                check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
                check_type(argname="argument mount_points", value=mount_points, expected_type=type_hints["mount_points"])
                check_type(argname="argument port_configuration", value=port_configuration, expected_type=type_hints["port_configuration"])
                check_type(argname="argument resolved_image_digest", value=resolved_image_digest, expected_type=type_hints["resolved_image_digest"])
                check_type(argname="argument server_sdk_version", value=server_sdk_version, expected_type=type_hints["server_sdk_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_name is not None:
                self._values["container_name"] = container_name
            if depends_on is not None:
                self._values["depends_on"] = depends_on
            if environment_override is not None:
                self._values["environment_override"] = environment_override
            if image_uri is not None:
                self._values["image_uri"] = image_uri
            if mount_points is not None:
                self._values["mount_points"] = mount_points
            if port_configuration is not None:
                self._values["port_configuration"] = port_configuration
            if resolved_image_digest is not None:
                self._values["resolved_image_digest"] = resolved_image_digest
            if server_sdk_version is not None:
                self._values["server_sdk_version"] = server_sdk_version

        @builtins.property
        def container_name(self) -> typing.Optional[builtins.str]:
            '''The container definition identifier.

            Container names are unique within a container group definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-gameservercontainerdefinition.html#cfn-gamelift-containergroupdefinition-gameservercontainerdefinition-containername
            '''
            result = self._values.get("container_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def depends_on(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty"]]]]:
            '''Indicates that the container relies on the status of other containers in the same container group during startup and shutdown sequences.

            A container might have dependencies on multiple containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-gameservercontainerdefinition.html#cfn-gamelift-containergroupdefinition-gameservercontainerdefinition-dependson
            '''
            result = self._values.get("depends_on")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty"]]]], result)

        @builtins.property
        def environment_override(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty"]]]]:
            '''A set of environment variables that's passed to the container on startup.

            See the `ContainerDefinition::environment <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDefinition.html#ECS-Type-ContainerDefinition-environment>`_ parameter in the *Amazon Elastic Container Service API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-gameservercontainerdefinition.html#cfn-gamelift-containergroupdefinition-gameservercontainerdefinition-environmentoverride
            '''
            result = self._values.get("environment_override")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty"]]]], result)

        @builtins.property
        def image_uri(self) -> typing.Optional[builtins.str]:
            '''The URI to the image that Amazon GameLift Servers uses when deploying this container to a container fleet.

            For a more specific identifier, see ``ResolvedImageDigest`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-gameservercontainerdefinition.html#cfn-gamelift-containergroupdefinition-gameservercontainerdefinition-imageuri
            '''
            result = self._values.get("image_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mount_points(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty"]]]]:
            '''A mount point that binds a path inside the container to a file or directory on the host system and lets it access the file or directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-gameservercontainerdefinition.html#cfn-gamelift-containergroupdefinition-gameservercontainerdefinition-mountpoints
            '''
            result = self._values.get("mount_points")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty"]]]], result)

        @builtins.property
        def port_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty"]]:
            '''The set of ports that are available to bind to processes in the container.

            For example, a game server process requires a container port to allow game clients to connect to it. Container ports aren't directly accessed by inbound traffic. Amazon GameLift Servers maps these container ports to externally accessible connection ports, which are assigned as needed from the container fleet's ``ConnectionPortRange`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-gameservercontainerdefinition.html#cfn-gamelift-containergroupdefinition-gameservercontainerdefinition-portconfiguration
            '''
            result = self._values.get("port_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty"]], result)

        @builtins.property
        def resolved_image_digest(self) -> typing.Optional[builtins.str]:
            '''A unique and immutable identifier for the container image.

            The digest is a SHA 256 hash of the container image manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-gameservercontainerdefinition.html#cfn-gamelift-containergroupdefinition-gameservercontainerdefinition-resolvedimagedigest
            '''
            result = self._values.get("resolved_image_digest")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_sdk_version(self) -> typing.Optional[builtins.str]:
            '''The Amazon GameLift Servers server SDK version that the game server is integrated with.

            Only game servers using 5.2.0 or higher are compatible with container fleets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-gameservercontainerdefinition.html#cfn-gamelift-containergroupdefinition-gameservercontainerdefinition-serversdkversion
            '''
            result = self._values.get("server_sdk_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GameServerContainerDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"container_port_ranges": "containerPortRanges"},
    )
    class PortConfigurationProperty:
        def __init__(
            self,
            *,
            container_port_ranges: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Defines the ports on a container.

            :param container_port_ranges: Specifies one or more ranges of ports on a container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-portconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                port_configuration_property = gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty(
                    container_port_ranges=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty(
                        from_port=123,
                        protocol="protocol",
                        to_port=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e12db5eed490dc850420ee078541a56f811a0b750174b27f9071cfb4b54ef70a)
                check_type(argname="argument container_port_ranges", value=container_port_ranges, expected_type=type_hints["container_port_ranges"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_port_ranges is not None:
                self._values["container_port_ranges"] = container_port_ranges

        @builtins.property
        def container_port_ranges(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty"]]]]:
            '''Specifies one or more ranges of ports on a container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-portconfiguration.html#cfn-gamelift-containergroupdefinition-portconfiguration-containerportranges
            '''
            result = self._values.get("container_port_ranges")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnContainerGroupDefinitionPropsMixin.SupportContainerDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_name": "containerName",
            "depends_on": "dependsOn",
            "environment_override": "environmentOverride",
            "essential": "essential",
            "health_check": "healthCheck",
            "image_uri": "imageUri",
            "memory_hard_limit_mebibytes": "memoryHardLimitMebibytes",
            "mount_points": "mountPoints",
            "port_configuration": "portConfiguration",
            "resolved_image_digest": "resolvedImageDigest",
            "vcpu": "vcpu",
        },
    )
    class SupportContainerDefinitionProperty:
        def __init__(
            self,
            *,
            container_name: typing.Optional[builtins.str] = None,
            depends_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            environment_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            essential: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.ContainerHealthCheckProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_uri: typing.Optional[builtins.str] = None,
            memory_hard_limit_mebibytes: typing.Optional[jsii.Number] = None,
            mount_points: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            port_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resolved_image_digest: typing.Optional[builtins.str] = None,
            vcpu: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a support container in a container group.

            A support container might be in a game server container group or a per-instance container group. Support containers don't run game server processes.

            You can update a support container definition and deploy the updates to an existing fleet. When creating or updating a game server container group definition, use the property `GameServerContainerDefinitionInput <https://docs.aws.amazon.com/gamelift/latest/apireference/API_GameServerContainerDefinitionInput.html>`_ .

            *Part of:* `ContainerGroupDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ContainerGroupDefinition.html>`_

            *Returned by:* `DescribeContainerGroupDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeContainerGroupDefinition.html>`_ , `ListContainerGroupDefinitions <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ListContainerGroupDefinitions.html>`_ , `UpdateContainerGroupDefinition <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateContainerGroupDefinition.html>`_

            :param container_name: The container definition identifier. Container names are unique within a container group definition.
            :param depends_on: Indicates that the container relies on the status of other containers in the same container group during its startup and shutdown sequences. A container might have dependencies on multiple containers.
            :param environment_override: A set of environment variables that's passed to the container on startup. See the `ContainerDefinition::environment <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDefinition.html#ECS-Type-ContainerDefinition-environment>`_ parameter in the *Amazon Elastic Container Service API Reference* .
            :param essential: Indicates whether the container is vital to the container group. If an essential container fails, the entire container group restarts.
            :param health_check: A configuration for a non-terminal health check. A support container automatically restarts if it stops functioning or if it fails this health check.
            :param image_uri: The URI to the image that Amazon GameLift Servers deploys to a container fleet. For a more specific identifier, see ``ResolvedImageDigest`` .
            :param memory_hard_limit_mebibytes: The amount of memory that Amazon GameLift Servers makes available to the container. If memory limits aren't set for an individual container, the container shares the container group's total memory allocation. *Related data type:* `ContainerGroupDefinition TotalMemoryLimitMebibytes <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ContainerGroupDefinition.html>`_
            :param mount_points: A mount point that binds a path inside the container to a file or directory on the host system and lets it access the file or directory.
            :param port_configuration: A set of ports that allow access to the container from external users. Processes running in the container can bind to a one of these ports. Container ports aren't directly accessed by inbound traffic. Amazon GameLift Servers maps these container ports to externally accessible connection ports, which are assigned as needed from the container fleet's ``ConnectionPortRange`` .
            :param resolved_image_digest: A unique and immutable identifier for the container image. The digest is a SHA 256 hash of the container image manifest.
            :param vcpu: The number of vCPU units that are reserved for the container. If no resources are reserved, the container shares the total vCPU limit for the container group. *Related data type:* `ContainerGroupDefinition TotalVcpuLimit <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ContainerGroupDefinition.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                support_container_definition_property = gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.SupportContainerDefinitionProperty(
                    container_name="containerName",
                    depends_on=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty(
                        condition="condition",
                        container_name="containerName"
                    )],
                    environment_override=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty(
                        name="name",
                        value="value"
                    )],
                    essential=False,
                    health_check=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerHealthCheckProperty(
                        command=["command"],
                        interval=123,
                        retries=123,
                        start_period=123,
                        timeout=123
                    ),
                    image_uri="imageUri",
                    memory_hard_limit_mebibytes=123,
                    mount_points=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty(
                        access_level="accessLevel",
                        container_path="containerPath",
                        instance_path="instancePath"
                    )],
                    port_configuration=gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty(
                        container_port_ranges=[gamelift_mixins.CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty(
                            from_port=123,
                            protocol="protocol",
                            to_port=123
                        )]
                    ),
                    resolved_image_digest="resolvedImageDigest",
                    vcpu=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e16b343652b34e3941b00974ccb5f8bbbadf839fa56d422c440ddfeccb1941c)
                check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
                check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
                check_type(argname="argument environment_override", value=environment_override, expected_type=type_hints["environment_override"])
                check_type(argname="argument essential", value=essential, expected_type=type_hints["essential"])
                check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
                check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
                check_type(argname="argument memory_hard_limit_mebibytes", value=memory_hard_limit_mebibytes, expected_type=type_hints["memory_hard_limit_mebibytes"])
                check_type(argname="argument mount_points", value=mount_points, expected_type=type_hints["mount_points"])
                check_type(argname="argument port_configuration", value=port_configuration, expected_type=type_hints["port_configuration"])
                check_type(argname="argument resolved_image_digest", value=resolved_image_digest, expected_type=type_hints["resolved_image_digest"])
                check_type(argname="argument vcpu", value=vcpu, expected_type=type_hints["vcpu"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_name is not None:
                self._values["container_name"] = container_name
            if depends_on is not None:
                self._values["depends_on"] = depends_on
            if environment_override is not None:
                self._values["environment_override"] = environment_override
            if essential is not None:
                self._values["essential"] = essential
            if health_check is not None:
                self._values["health_check"] = health_check
            if image_uri is not None:
                self._values["image_uri"] = image_uri
            if memory_hard_limit_mebibytes is not None:
                self._values["memory_hard_limit_mebibytes"] = memory_hard_limit_mebibytes
            if mount_points is not None:
                self._values["mount_points"] = mount_points
            if port_configuration is not None:
                self._values["port_configuration"] = port_configuration
            if resolved_image_digest is not None:
                self._values["resolved_image_digest"] = resolved_image_digest
            if vcpu is not None:
                self._values["vcpu"] = vcpu

        @builtins.property
        def container_name(self) -> typing.Optional[builtins.str]:
            '''The container definition identifier.

            Container names are unique within a container group definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-containername
            '''
            result = self._values.get("container_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def depends_on(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty"]]]]:
            '''Indicates that the container relies on the status of other containers in the same container group during its startup and shutdown sequences.

            A container might have dependencies on multiple containers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-dependson
            '''
            result = self._values.get("depends_on")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty"]]]], result)

        @builtins.property
        def environment_override(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty"]]]]:
            '''A set of environment variables that's passed to the container on startup.

            See the `ContainerDefinition::environment <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDefinition.html#ECS-Type-ContainerDefinition-environment>`_ parameter in the *Amazon Elastic Container Service API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-environmentoverride
            '''
            result = self._values.get("environment_override")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty"]]]], result)

        @builtins.property
        def essential(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the container is vital to the container group.

            If an essential container fails, the entire container group restarts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-essential
            '''
            result = self._values.get("essential")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def health_check(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerHealthCheckProperty"]]:
            '''A configuration for a non-terminal health check.

            A support container automatically restarts if it stops functioning or if it fails this health check.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-healthcheck
            '''
            result = self._values.get("health_check")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerHealthCheckProperty"]], result)

        @builtins.property
        def image_uri(self) -> typing.Optional[builtins.str]:
            '''The URI to the image that Amazon GameLift Servers deploys to a container fleet.

            For a more specific identifier, see ``ResolvedImageDigest`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-imageuri
            '''
            result = self._values.get("image_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory_hard_limit_mebibytes(self) -> typing.Optional[jsii.Number]:
            '''The amount of memory that Amazon GameLift Servers makes available to the container.

            If memory limits aren't set for an individual container, the container shares the container group's total memory allocation.

            *Related data type:* `ContainerGroupDefinition TotalMemoryLimitMebibytes <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ContainerGroupDefinition.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-memoryhardlimitmebibytes
            '''
            result = self._values.get("memory_hard_limit_mebibytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mount_points(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty"]]]]:
            '''A mount point that binds a path inside the container to a file or directory on the host system and lets it access the file or directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-mountpoints
            '''
            result = self._values.get("mount_points")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty"]]]], result)

        @builtins.property
        def port_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty"]]:
            '''A set of ports that allow access to the container from external users.

            Processes running in the container can bind to a one of these ports. Container ports aren't directly accessed by inbound traffic. Amazon GameLift Servers maps these container ports to externally accessible connection ports, which are assigned as needed from the container fleet's ``ConnectionPortRange`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-portconfiguration
            '''
            result = self._values.get("port_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty"]], result)

        @builtins.property
        def resolved_image_digest(self) -> typing.Optional[builtins.str]:
            '''A unique and immutable identifier for the container image.

            The digest is a SHA 256 hash of the container image manifest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-resolvedimagedigest
            '''
            result = self._values.get("resolved_image_digest")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vcpu(self) -> typing.Optional[jsii.Number]:
            '''The number of vCPU units that are reserved for the container.

            If no resources are reserved, the container shares the total vCPU limit for the container group.

            *Related data type:* `ContainerGroupDefinition TotalVcpuLimit <https://docs.aws.amazon.com/gamelift/latest/apireference/API_ContainerGroupDefinition.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-containergroupdefinition-supportcontainerdefinition.html#cfn-gamelift-containergroupdefinition-supportcontainerdefinition-vcpu
            '''
            result = self._values.get("vcpu")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SupportContainerDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "anywhere_configuration": "anywhereConfiguration",
        "apply_capacity": "applyCapacity",
        "build_id": "buildId",
        "certificate_configuration": "certificateConfiguration",
        "compute_type": "computeType",
        "description": "description",
        "desired_ec2_instances": "desiredEc2Instances",
        "ec2_inbound_permissions": "ec2InboundPermissions",
        "ec2_instance_type": "ec2InstanceType",
        "fleet_type": "fleetType",
        "instance_role_arn": "instanceRoleArn",
        "instance_role_credentials_provider": "instanceRoleCredentialsProvider",
        "locations": "locations",
        "log_paths": "logPaths",
        "max_size": "maxSize",
        "metric_groups": "metricGroups",
        "min_size": "minSize",
        "name": "name",
        "new_game_session_protection_policy": "newGameSessionProtectionPolicy",
        "peer_vpc_aws_account_id": "peerVpcAwsAccountId",
        "peer_vpc_id": "peerVpcId",
        "resource_creation_limit_policy": "resourceCreationLimitPolicy",
        "runtime_configuration": "runtimeConfiguration",
        "scaling_policies": "scalingPolicies",
        "script_id": "scriptId",
        "server_launch_parameters": "serverLaunchParameters",
        "server_launch_path": "serverLaunchPath",
        "tags": "tags",
    },
)
class CfnFleetMixinProps:
    def __init__(
        self,
        *,
        anywhere_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.AnywhereConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        apply_capacity: typing.Optional[builtins.str] = None,
        build_id: typing.Optional[builtins.str] = None,
        certificate_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.CertificateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        compute_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        desired_ec2_instances: typing.Optional[jsii.Number] = None,
        ec2_inbound_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.IpPermissionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ec2_instance_type: typing.Optional[builtins.str] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        instance_role_arn: typing.Optional[builtins.str] = None,
        instance_role_credentials_provider: typing.Optional[builtins.str] = None,
        locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.LocationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        log_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        metric_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        min_size: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        new_game_session_protection_policy: typing.Optional[builtins.str] = None,
        peer_vpc_aws_account_id: typing.Optional[builtins.str] = None,
        peer_vpc_id: typing.Optional[builtins.str] = None,
        resource_creation_limit_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ResourceCreationLimitPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        runtime_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.RuntimeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scaling_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ScalingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        script_id: typing.Optional[builtins.str] = None,
        server_launch_parameters: typing.Optional[builtins.str] = None,
        server_launch_path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFleetPropsMixin.

        :param anywhere_configuration: Amazon GameLift Servers Anywhere configuration options.
        :param apply_capacity: Current resource capacity settings for managed EC2 fleets and managed container fleets. For multi-location fleets, location values might refer to a fleet's remote location or its home Region. *Returned by:* `DescribeFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetCapacity.html>`_ , `DescribeFleetLocationCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetLocationCapacity.html>`_ , `UpdateFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateFleetCapacity.html>`_
        :param build_id: A unique identifier for a build to be deployed on the new fleet. If you are deploying the fleet with a custom game build, you must specify this property. The build must have been successfully uploaded to Amazon GameLift and be in a ``READY`` status. This fleet setting cannot be changed once the fleet is created.
        :param certificate_configuration: Prompts Amazon GameLift Servers to generate a TLS/SSL certificate for the fleet. Amazon GameLift Servers uses the certificates to encrypt traffic between game clients and the game servers running on Amazon GameLift Servers. By default, the ``CertificateConfiguration`` is ``DISABLED`` . You can't change this property after you create the fleet. Certificate Manager (ACM) certificates expire after 13 months. Certificate expiration can cause fleets to fail, preventing players from connecting to instances in the fleet. We recommend you replace fleets before 13 months, consider using fleet aliases for a smooth transition. .. epigraph:: ACM isn't available in all AWS regions. A fleet creation request with certificate generation enabled in an unsupported Region, fails with a 4xx error. For more information about the supported Regions, see `Supported Regions <https://docs.aws.amazon.com/acm/latest/userguide/acm-regions.html>`_ in the *Certificate Manager User Guide* .
        :param compute_type: The type of compute resource used to host your game servers. - ``EC2`` – The game server build is deployed to Amazon EC2 instances for cloud hosting. This is the default setting. - ``ANYWHERE`` – Game servers and supporting software are deployed to compute resources that you provide and manage. With this compute type, you can also set the ``AnywhereConfiguration`` parameter.
        :param description: A description for the fleet.
        :param desired_ec2_instances: (deprecated) [DEPRECATED] The number of EC2 instances that you want this fleet to host. When creating a new fleet, GameLift automatically sets this value to "1" and initiates a single instance. Once the fleet is active, update this value to trigger GameLift to add or remove instances from the fleet.
        :param ec2_inbound_permissions: The IP address ranges and port settings that allow inbound traffic to access game server processes and other processes on this fleet. Set this parameter for managed EC2 fleets. You can leave this parameter empty when creating the fleet, but you must call ` <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateFleetPortSettings>`_ to set it before players can connect to game sessions. As a best practice, we recommend opening ports for remote access only when you need them and closing them when you're finished. For Amazon GameLift Servers Realtime fleets, Amazon GameLift Servers automatically sets TCP and UDP ranges.
        :param ec2_instance_type: The Amazon GameLift Servers-supported Amazon EC2 instance type to use with managed EC2 fleets. Instance type determines the computing resources that will be used to host your game servers, including CPU, memory, storage, and networking capacity. See `Amazon Elastic Compute Cloud Instance Types <https://docs.aws.amazon.com/ec2/instance-types/>`_ for detailed descriptions of Amazon EC2 instance types.
        :param fleet_type: Indicates whether to use On-Demand or Spot instances for this fleet. By default, this property is set to ``ON_DEMAND`` . Learn more about when to use `On-Demand versus Spot Instances <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-ec2-instances.html#gamelift-ec2-instances-spot>`_ . This fleet property can't be changed after the fleet is created.
        :param instance_role_arn: A unique identifier for an IAM role that manages access to your AWS services. With an instance role ARN set, any application that runs on an instance in this fleet can assume the role, including install scripts, server processes, and daemons (background processes). Create a role or look up a role's ARN by using the `IAM dashboard <https://docs.aws.amazon.com/iam/>`_ in the AWS Management Console . Learn more about using on-box credentials for your game servers at `Access external resources from a game server <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-sdk-server-resources.html>`_ . This attribute is used with fleets where ``ComputeType`` is ``EC2`` .
        :param instance_role_credentials_provider: Indicates that fleet instances maintain a shared credentials file for the IAM role defined in ``InstanceRoleArn`` . Shared credentials allow applications that are deployed with the game server executable to communicate with other AWS resources. This property is used only when the game server is integrated with the server SDK version 5.x. For more information about using shared credentials, see `Communicate with other AWS resources from your fleets <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-sdk-server-resources.html>`_ . This attribute is used with fleets where ``ComputeType`` is ``EC2`` .
        :param locations: A set of remote locations to deploy additional instances to and manage as a multi-location fleet. Use this parameter when creating a fleet in AWS Regions that support multiple locations. You can add any AWS Region or Local Zone that's supported by Amazon GameLift Servers. Provide a list of one or more AWS Region codes, such as ``us-west-2`` , or Local Zone names. When using this parameter, Amazon GameLift Servers requires you to include your home location in the request. For a list of supported Regions and Local Zones, see `Amazon GameLift Servers service locations <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-regions.html>`_ for managed hosting.
        :param log_paths: (deprecated) This parameter is no longer used. When hosting a custom game build, specify where Amazon GameLift should store log files using the Amazon GameLift server API call ProcessReady()
        :param max_size: (deprecated) [DEPRECATED] The maximum value that is allowed for the fleet's instance count. When creating a new fleet, GameLift automatically sets this value to "1". Once the fleet is active, you can change this value.
        :param metric_groups: The name of an AWS CloudWatch metric group to add this fleet to. A metric group is used to aggregate the metrics for multiple fleets. You can specify an existing metric group name or set a new name to create a new metric group. A fleet can be included in only one metric group at a time.
        :param min_size: (deprecated) [DEPRECATED] The minimum value allowed for the fleet's instance count. When creating a new fleet, GameLift automatically sets this value to "0". After the fleet is active, you can change this value.
        :param name: A descriptive label that is associated with a fleet. Fleet names do not need to be unique.
        :param new_game_session_protection_policy: The status of termination protection for active game sessions on the fleet. By default, this property is set to ``NoProtection`` . - *NoProtection* - Game sessions can be terminated during active gameplay as a result of a scale-down event. - *FullProtection* - Game sessions in ``ACTIVE`` status cannot be terminated during a scale-down event.
        :param peer_vpc_aws_account_id: Used when peering your Amazon GameLift Servers fleet with a VPC, the unique identifier for the AWS account that owns the VPC. You can find your account ID in the AWS Management Console under account settings.
        :param peer_vpc_id: A unique identifier for a VPC with resources to be accessed by your Amazon GameLift Servers fleet. The VPC must be in the same Region as your fleet. To look up a VPC ID, use the `VPC Dashboard <https://docs.aws.amazon.com/vpc/>`_ in the AWS Management Console . Learn more about VPC peering in `VPC Peering with Amazon GameLift Servers Fleets <https://docs.aws.amazon.com/gamelift/latest/developerguide/vpc-peering.html>`_ .
        :param resource_creation_limit_policy: A policy that limits the number of game sessions that an individual player can create on instances in this fleet within a specified span of time.
        :param runtime_configuration: Instructions for how to launch and maintain server processes on instances in the fleet. The runtime configuration defines one or more server process configurations, each identifying a build executable or Realtime script file and the number of processes of that type to run concurrently. .. epigraph:: The ``RuntimeConfiguration`` parameter is required unless the fleet is being configured using the older parameters ``ServerLaunchPath`` and ``ServerLaunchParameters`` , which are still supported for backward compatibility.
        :param scaling_policies: Rule that controls how a fleet is scaled. Scaling policies are uniquely identified by the combination of name and fleet ID.
        :param script_id: The unique identifier for a Realtime configuration script to be deployed on fleet instances. You can use either the script ID or ARN. Scripts must be uploaded to Amazon GameLift Servers prior to creating the fleet. This fleet property cannot be changed later. .. epigraph:: You can't use the ``!Ref`` command to reference a script created with a CloudFormation template for the fleet property ``ScriptId`` . Instead, use ``Fn::GetAtt Script.Arn`` or ``Fn::GetAtt Script.Id`` to retrieve either of these properties as input for ``ScriptId`` . Alternatively, enter a ``ScriptId`` string manually.
        :param server_launch_parameters: (deprecated) This parameter is no longer used but is retained for backward compatibility. Instead, specify server launch parameters in the RuntimeConfiguration parameter. A request must specify either a runtime configuration or values for both ServerLaunchParameters and ServerLaunchPath.
        :param server_launch_path: (deprecated) This parameter is no longer used. Instead, specify a server launch path using the RuntimeConfiguration parameter. Requests that specify a server launch path and launch parameters instead of a runtime configuration will continue to work.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_fleet_mixin_props = gamelift_mixins.CfnFleetMixinProps(
                anywhere_configuration=gamelift_mixins.CfnFleetPropsMixin.AnywhereConfigurationProperty(
                    cost="cost"
                ),
                apply_capacity="applyCapacity",
                build_id="buildId",
                certificate_configuration=gamelift_mixins.CfnFleetPropsMixin.CertificateConfigurationProperty(
                    certificate_type="certificateType"
                ),
                compute_type="computeType",
                description="description",
                desired_ec2_instances=123,
                ec2_inbound_permissions=[gamelift_mixins.CfnFleetPropsMixin.IpPermissionProperty(
                    from_port=123,
                    ip_range="ipRange",
                    protocol="protocol",
                    to_port=123
                )],
                ec2_instance_type="ec2InstanceType",
                fleet_type="fleetType",
                instance_role_arn="instanceRoleArn",
                instance_role_credentials_provider="instanceRoleCredentialsProvider",
                locations=[gamelift_mixins.CfnFleetPropsMixin.LocationConfigurationProperty(
                    location="location",
                    location_capacity=gamelift_mixins.CfnFleetPropsMixin.LocationCapacityProperty(
                        desired_ec2_instances=123,
                        max_size=123,
                        min_size=123
                    )
                )],
                log_paths=["logPaths"],
                max_size=123,
                metric_groups=["metricGroups"],
                min_size=123,
                name="name",
                new_game_session_protection_policy="newGameSessionProtectionPolicy",
                peer_vpc_aws_account_id="peerVpcAwsAccountId",
                peer_vpc_id="peerVpcId",
                resource_creation_limit_policy=gamelift_mixins.CfnFleetPropsMixin.ResourceCreationLimitPolicyProperty(
                    new_game_sessions_per_creator=123,
                    policy_period_in_minutes=123
                ),
                runtime_configuration=gamelift_mixins.CfnFleetPropsMixin.RuntimeConfigurationProperty(
                    game_session_activation_timeout_seconds=123,
                    max_concurrent_game_session_activations=123,
                    server_processes=[gamelift_mixins.CfnFleetPropsMixin.ServerProcessProperty(
                        concurrent_executions=123,
                        launch_path="launchPath",
                        parameters="parameters"
                    )]
                ),
                scaling_policies=[gamelift_mixins.CfnFleetPropsMixin.ScalingPolicyProperty(
                    comparison_operator="comparisonOperator",
                    evaluation_periods=123,
                    location="location",
                    metric_name="metricName",
                    name="name",
                    policy_type="policyType",
                    scaling_adjustment=123,
                    scaling_adjustment_type="scalingAdjustmentType",
                    status="status",
                    target_configuration=gamelift_mixins.CfnFleetPropsMixin.TargetConfigurationProperty(
                        target_value=123
                    ),
                    threshold=123,
                    update_status="updateStatus"
                )],
                script_id="scriptId",
                server_launch_parameters="serverLaunchParameters",
                server_launch_path="serverLaunchPath",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d98948d00934efa740094800752932e1a366fa298a66d2ef63cb3a3d0cd6ae3)
            check_type(argname="argument anywhere_configuration", value=anywhere_configuration, expected_type=type_hints["anywhere_configuration"])
            check_type(argname="argument apply_capacity", value=apply_capacity, expected_type=type_hints["apply_capacity"])
            check_type(argname="argument build_id", value=build_id, expected_type=type_hints["build_id"])
            check_type(argname="argument certificate_configuration", value=certificate_configuration, expected_type=type_hints["certificate_configuration"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument desired_ec2_instances", value=desired_ec2_instances, expected_type=type_hints["desired_ec2_instances"])
            check_type(argname="argument ec2_inbound_permissions", value=ec2_inbound_permissions, expected_type=type_hints["ec2_inbound_permissions"])
            check_type(argname="argument ec2_instance_type", value=ec2_instance_type, expected_type=type_hints["ec2_instance_type"])
            check_type(argname="argument fleet_type", value=fleet_type, expected_type=type_hints["fleet_type"])
            check_type(argname="argument instance_role_arn", value=instance_role_arn, expected_type=type_hints["instance_role_arn"])
            check_type(argname="argument instance_role_credentials_provider", value=instance_role_credentials_provider, expected_type=type_hints["instance_role_credentials_provider"])
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument log_paths", value=log_paths, expected_type=type_hints["log_paths"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument metric_groups", value=metric_groups, expected_type=type_hints["metric_groups"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument new_game_session_protection_policy", value=new_game_session_protection_policy, expected_type=type_hints["new_game_session_protection_policy"])
            check_type(argname="argument peer_vpc_aws_account_id", value=peer_vpc_aws_account_id, expected_type=type_hints["peer_vpc_aws_account_id"])
            check_type(argname="argument peer_vpc_id", value=peer_vpc_id, expected_type=type_hints["peer_vpc_id"])
            check_type(argname="argument resource_creation_limit_policy", value=resource_creation_limit_policy, expected_type=type_hints["resource_creation_limit_policy"])
            check_type(argname="argument runtime_configuration", value=runtime_configuration, expected_type=type_hints["runtime_configuration"])
            check_type(argname="argument scaling_policies", value=scaling_policies, expected_type=type_hints["scaling_policies"])
            check_type(argname="argument script_id", value=script_id, expected_type=type_hints["script_id"])
            check_type(argname="argument server_launch_parameters", value=server_launch_parameters, expected_type=type_hints["server_launch_parameters"])
            check_type(argname="argument server_launch_path", value=server_launch_path, expected_type=type_hints["server_launch_path"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if anywhere_configuration is not None:
            self._values["anywhere_configuration"] = anywhere_configuration
        if apply_capacity is not None:
            self._values["apply_capacity"] = apply_capacity
        if build_id is not None:
            self._values["build_id"] = build_id
        if certificate_configuration is not None:
            self._values["certificate_configuration"] = certificate_configuration
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if description is not None:
            self._values["description"] = description
        if desired_ec2_instances is not None:
            self._values["desired_ec2_instances"] = desired_ec2_instances
        if ec2_inbound_permissions is not None:
            self._values["ec2_inbound_permissions"] = ec2_inbound_permissions
        if ec2_instance_type is not None:
            self._values["ec2_instance_type"] = ec2_instance_type
        if fleet_type is not None:
            self._values["fleet_type"] = fleet_type
        if instance_role_arn is not None:
            self._values["instance_role_arn"] = instance_role_arn
        if instance_role_credentials_provider is not None:
            self._values["instance_role_credentials_provider"] = instance_role_credentials_provider
        if locations is not None:
            self._values["locations"] = locations
        if log_paths is not None:
            self._values["log_paths"] = log_paths
        if max_size is not None:
            self._values["max_size"] = max_size
        if metric_groups is not None:
            self._values["metric_groups"] = metric_groups
        if min_size is not None:
            self._values["min_size"] = min_size
        if name is not None:
            self._values["name"] = name
        if new_game_session_protection_policy is not None:
            self._values["new_game_session_protection_policy"] = new_game_session_protection_policy
        if peer_vpc_aws_account_id is not None:
            self._values["peer_vpc_aws_account_id"] = peer_vpc_aws_account_id
        if peer_vpc_id is not None:
            self._values["peer_vpc_id"] = peer_vpc_id
        if resource_creation_limit_policy is not None:
            self._values["resource_creation_limit_policy"] = resource_creation_limit_policy
        if runtime_configuration is not None:
            self._values["runtime_configuration"] = runtime_configuration
        if scaling_policies is not None:
            self._values["scaling_policies"] = scaling_policies
        if script_id is not None:
            self._values["script_id"] = script_id
        if server_launch_parameters is not None:
            self._values["server_launch_parameters"] = server_launch_parameters
        if server_launch_path is not None:
            self._values["server_launch_path"] = server_launch_path
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def anywhere_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AnywhereConfigurationProperty"]]:
        '''Amazon GameLift Servers Anywhere configuration options.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-anywhereconfiguration
        '''
        result = self._values.get("anywhere_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.AnywhereConfigurationProperty"]], result)

    @builtins.property
    def apply_capacity(self) -> typing.Optional[builtins.str]:
        '''Current resource capacity settings for managed EC2 fleets and managed container fleets.

        For multi-location fleets, location values might refer to a fleet's remote location or its home Region.

        *Returned by:* `DescribeFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetCapacity.html>`_ , `DescribeFleetLocationCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetLocationCapacity.html>`_ , `UpdateFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateFleetCapacity.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-applycapacity
        '''
        result = self._values.get("apply_capacity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for a build to be deployed on the new fleet.

        If you are deploying the fleet with a custom game build, you must specify this property. The build must have been successfully uploaded to Amazon GameLift and be in a ``READY`` status. This fleet setting cannot be changed once the fleet is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-buildid
        '''
        result = self._values.get("build_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.CertificateConfigurationProperty"]]:
        '''Prompts Amazon GameLift Servers to generate a TLS/SSL certificate for the fleet.

        Amazon GameLift Servers uses the certificates to encrypt traffic between game clients and the game servers running on Amazon GameLift Servers. By default, the ``CertificateConfiguration`` is ``DISABLED`` . You can't change this property after you create the fleet.

        Certificate Manager (ACM) certificates expire after 13 months. Certificate expiration can cause fleets to fail, preventing players from connecting to instances in the fleet. We recommend you replace fleets before 13 months, consider using fleet aliases for a smooth transition.
        .. epigraph::

           ACM isn't available in all AWS regions. A fleet creation request with certificate generation enabled in an unsupported Region, fails with a 4xx error. For more information about the supported Regions, see `Supported Regions <https://docs.aws.amazon.com/acm/latest/userguide/acm-regions.html>`_ in the *Certificate Manager User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-certificateconfiguration
        '''
        result = self._values.get("certificate_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.CertificateConfigurationProperty"]], result)

    @builtins.property
    def compute_type(self) -> typing.Optional[builtins.str]:
        '''The type of compute resource used to host your game servers.

        - ``EC2`` – The game server build is deployed to Amazon EC2 instances for cloud hosting. This is the default setting.
        - ``ANYWHERE`` – Game servers and supporting software are deployed to compute resources that you provide and manage. With this compute type, you can also set the ``AnywhereConfiguration`` parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-computetype
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the fleet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_ec2_instances(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) [DEPRECATED] The number of EC2 instances that you want this fleet to host.

        When creating a new fleet, GameLift automatically sets this value to "1" and initiates a single instance. Once the fleet is active, update this value to trigger GameLift to add or remove instances from the fleet.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-desiredec2instances
        :stability: deprecated
        '''
        result = self._values.get("desired_ec2_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ec2_inbound_permissions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.IpPermissionProperty"]]]]:
        '''The IP address ranges and port settings that allow inbound traffic to access game server processes and other processes on this fleet.

        Set this parameter for managed EC2 fleets. You can leave this parameter empty when creating the fleet, but you must call ` <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateFleetPortSettings>`_ to set it before players can connect to game sessions. As a best practice, we recommend opening ports for remote access only when you need them and closing them when you're finished. For Amazon GameLift Servers Realtime fleets, Amazon GameLift Servers automatically sets TCP and UDP ranges.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-ec2inboundpermissions
        '''
        result = self._values.get("ec2_inbound_permissions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.IpPermissionProperty"]]]], result)

    @builtins.property
    def ec2_instance_type(self) -> typing.Optional[builtins.str]:
        '''The Amazon GameLift Servers-supported Amazon EC2 instance type to use with managed EC2 fleets.

        Instance type determines the computing resources that will be used to host your game servers, including CPU, memory, storage, and networking capacity. See `Amazon Elastic Compute Cloud Instance Types <https://docs.aws.amazon.com/ec2/instance-types/>`_ for detailed descriptions of Amazon EC2 instance types.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-ec2instancetype
        '''
        result = self._values.get("ec2_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fleet_type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether to use On-Demand or Spot instances for this fleet.

        By default, this property is set to ``ON_DEMAND`` . Learn more about when to use `On-Demand versus Spot Instances <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-ec2-instances.html#gamelift-ec2-instances-spot>`_ . This fleet property can't be changed after the fleet is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-fleettype
        '''
        result = self._values.get("fleet_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_role_arn(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for an IAM role that manages access to your AWS services.

        With an instance role ARN set, any application that runs on an instance in this fleet can assume the role, including install scripts, server processes, and daemons (background processes). Create a role or look up a role's ARN by using the `IAM dashboard <https://docs.aws.amazon.com/iam/>`_ in the AWS Management Console . Learn more about using on-box credentials for your game servers at `Access external resources from a game server <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-sdk-server-resources.html>`_ . This attribute is used with fleets where ``ComputeType`` is ``EC2`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-instancerolearn
        '''
        result = self._values.get("instance_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_role_credentials_provider(self) -> typing.Optional[builtins.str]:
        '''Indicates that fleet instances maintain a shared credentials file for the IAM role defined in ``InstanceRoleArn`` .

        Shared credentials allow applications that are deployed with the game server executable to communicate with other AWS resources. This property is used only when the game server is integrated with the server SDK version 5.x. For more information about using shared credentials, see `Communicate with other AWS resources from your fleets <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-sdk-server-resources.html>`_ . This attribute is used with fleets where ``ComputeType`` is ``EC2`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-instancerolecredentialsprovider
        '''
        result = self._values.get("instance_role_credentials_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.LocationConfigurationProperty"]]]]:
        '''A set of remote locations to deploy additional instances to and manage as a multi-location fleet.

        Use this parameter when creating a fleet in AWS Regions that support multiple locations. You can add any AWS Region or Local Zone that's supported by Amazon GameLift Servers. Provide a list of one or more AWS Region codes, such as ``us-west-2`` , or Local Zone names. When using this parameter, Amazon GameLift Servers requires you to include your home location in the request. For a list of supported Regions and Local Zones, see `Amazon GameLift Servers service locations <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-regions.html>`_ for managed hosting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-locations
        '''
        result = self._values.get("locations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.LocationConfigurationProperty"]]]], result)

    @builtins.property
    def log_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) This parameter is no longer used.

        When hosting a custom game build, specify where Amazon GameLift should store log files using the Amazon GameLift server API call ProcessReady()

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-logpaths
        :stability: deprecated
        '''
        result = self._values.get("log_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) [DEPRECATED] The maximum value that is allowed for the fleet's instance count.

        When creating a new fleet, GameLift automatically sets this value to "1". Once the fleet is active, you can change this value.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-maxsize
        :stability: deprecated
        '''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of an AWS CloudWatch metric group to add this fleet to.

        A metric group is used to aggregate the metrics for multiple fleets. You can specify an existing metric group name or set a new name to create a new metric group. A fleet can be included in only one metric group at a time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-metricgroups
        '''
        result = self._values.get("metric_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) [DEPRECATED] The minimum value allowed for the fleet's instance count.

        When creating a new fleet, GameLift automatically sets this value to "0". After the fleet is active, you can change this value.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-minsize
        :stability: deprecated
        '''
        result = self._values.get("min_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A descriptive label that is associated with a fleet.

        Fleet names do not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def new_game_session_protection_policy(self) -> typing.Optional[builtins.str]:
        '''The status of termination protection for active game sessions on the fleet.

        By default, this property is set to ``NoProtection`` .

        - *NoProtection* - Game sessions can be terminated during active gameplay as a result of a scale-down event.
        - *FullProtection* - Game sessions in ``ACTIVE`` status cannot be terminated during a scale-down event.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-newgamesessionprotectionpolicy
        '''
        result = self._values.get("new_game_session_protection_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_vpc_aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Used when peering your Amazon GameLift Servers fleet with a VPC, the unique identifier for the AWS account that owns the VPC.

        You can find your account ID in the AWS Management Console under account settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-peervpcawsaccountid
        '''
        result = self._values.get("peer_vpc_aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_vpc_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for a VPC with resources to be accessed by your Amazon GameLift Servers fleet.

        The VPC must be in the same Region as your fleet. To look up a VPC ID, use the `VPC Dashboard <https://docs.aws.amazon.com/vpc/>`_ in the AWS Management Console . Learn more about VPC peering in `VPC Peering with Amazon GameLift Servers Fleets <https://docs.aws.amazon.com/gamelift/latest/developerguide/vpc-peering.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-peervpcid
        '''
        result = self._values.get("peer_vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_creation_limit_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ResourceCreationLimitPolicyProperty"]]:
        '''A policy that limits the number of game sessions that an individual player can create on instances in this fleet within a specified span of time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-resourcecreationlimitpolicy
        '''
        result = self._values.get("resource_creation_limit_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ResourceCreationLimitPolicyProperty"]], result)

    @builtins.property
    def runtime_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.RuntimeConfigurationProperty"]]:
        '''Instructions for how to launch and maintain server processes on instances in the fleet.

        The runtime configuration defines one or more server process configurations, each identifying a build executable or Realtime script file and the number of processes of that type to run concurrently.
        .. epigraph::

           The ``RuntimeConfiguration`` parameter is required unless the fleet is being configured using the older parameters ``ServerLaunchPath`` and ``ServerLaunchParameters`` , which are still supported for backward compatibility.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-runtimeconfiguration
        '''
        result = self._values.get("runtime_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.RuntimeConfigurationProperty"]], result)

    @builtins.property
    def scaling_policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ScalingPolicyProperty"]]]]:
        '''Rule that controls how a fleet is scaled.

        Scaling policies are uniquely identified by the combination of name and fleet ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-scalingpolicies
        '''
        result = self._values.get("scaling_policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ScalingPolicyProperty"]]]], result)

    @builtins.property
    def script_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for a Realtime configuration script to be deployed on fleet instances.

        You can use either the script ID or ARN. Scripts must be uploaded to Amazon GameLift Servers prior to creating the fleet. This fleet property cannot be changed later.
        .. epigraph::

           You can't use the ``!Ref`` command to reference a script created with a CloudFormation template for the fleet property ``ScriptId`` . Instead, use ``Fn::GetAtt Script.Arn`` or ``Fn::GetAtt Script.Id`` to retrieve either of these properties as input for ``ScriptId`` . Alternatively, enter a ``ScriptId`` string manually.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-scriptid
        '''
        result = self._values.get("script_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_launch_parameters(self) -> typing.Optional[builtins.str]:
        '''(deprecated) This parameter is no longer used but is retained for backward compatibility.

        Instead, specify server launch parameters in the RuntimeConfiguration parameter. A request must specify either a runtime configuration or values for both ServerLaunchParameters and ServerLaunchPath.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-serverlaunchparameters
        :stability: deprecated
        '''
        result = self._values.get("server_launch_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_launch_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) This parameter is no longer used.

        Instead, specify a server launch path using the RuntimeConfiguration parameter. Requests that specify a server launch path and launch parameters instead of a runtime configuration will continue to work.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-serverlaunchpath
        :stability: deprecated
        '''
        result = self._values.get("server_launch_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin",
):
    '''The ``AWS::GameLift::Fleet`` resource creates an Amazon GameLift (GameLift) fleet to host custom game server or Realtime Servers.

    A fleet is a set of EC2 instances, configured with instructions to run game servers on each instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html
    :cloudformationResource: AWS::GameLift::Fleet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_fleet_props_mixin = gamelift_mixins.CfnFleetPropsMixin(gamelift_mixins.CfnFleetMixinProps(
            anywhere_configuration=gamelift_mixins.CfnFleetPropsMixin.AnywhereConfigurationProperty(
                cost="cost"
            ),
            apply_capacity="applyCapacity",
            build_id="buildId",
            certificate_configuration=gamelift_mixins.CfnFleetPropsMixin.CertificateConfigurationProperty(
                certificate_type="certificateType"
            ),
            compute_type="computeType",
            description="description",
            desired_ec2_instances=123,
            ec2_inbound_permissions=[gamelift_mixins.CfnFleetPropsMixin.IpPermissionProperty(
                from_port=123,
                ip_range="ipRange",
                protocol="protocol",
                to_port=123
            )],
            ec2_instance_type="ec2InstanceType",
            fleet_type="fleetType",
            instance_role_arn="instanceRoleArn",
            instance_role_credentials_provider="instanceRoleCredentialsProvider",
            locations=[gamelift_mixins.CfnFleetPropsMixin.LocationConfigurationProperty(
                location="location",
                location_capacity=gamelift_mixins.CfnFleetPropsMixin.LocationCapacityProperty(
                    desired_ec2_instances=123,
                    max_size=123,
                    min_size=123
                )
            )],
            log_paths=["logPaths"],
            max_size=123,
            metric_groups=["metricGroups"],
            min_size=123,
            name="name",
            new_game_session_protection_policy="newGameSessionProtectionPolicy",
            peer_vpc_aws_account_id="peerVpcAwsAccountId",
            peer_vpc_id="peerVpcId",
            resource_creation_limit_policy=gamelift_mixins.CfnFleetPropsMixin.ResourceCreationLimitPolicyProperty(
                new_game_sessions_per_creator=123,
                policy_period_in_minutes=123
            ),
            runtime_configuration=gamelift_mixins.CfnFleetPropsMixin.RuntimeConfigurationProperty(
                game_session_activation_timeout_seconds=123,
                max_concurrent_game_session_activations=123,
                server_processes=[gamelift_mixins.CfnFleetPropsMixin.ServerProcessProperty(
                    concurrent_executions=123,
                    launch_path="launchPath",
                    parameters="parameters"
                )]
            ),
            scaling_policies=[gamelift_mixins.CfnFleetPropsMixin.ScalingPolicyProperty(
                comparison_operator="comparisonOperator",
                evaluation_periods=123,
                location="location",
                metric_name="metricName",
                name="name",
                policy_type="policyType",
                scaling_adjustment=123,
                scaling_adjustment_type="scalingAdjustmentType",
                status="status",
                target_configuration=gamelift_mixins.CfnFleetPropsMixin.TargetConfigurationProperty(
                    target_value=123
                ),
                threshold=123,
                update_status="updateStatus"
            )],
            script_id="scriptId",
            server_launch_parameters="serverLaunchParameters",
            server_launch_path="serverLaunchPath",
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
        props: typing.Union[CfnFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::Fleet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe7f7e884acdd9c27d4db10533f6a90b52632b6661a4e7766e72c909d2147582)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cbc952e33e5cb60ef169aa016bddb056a872f6c1f1e9edb39742bf3c6268953)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783788d78930f86a7f4bbab21f7786133142dd8b9cf12f4c1a372dbd2b06d9d8)
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
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.AnywhereConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"cost": "cost"},
    )
    class AnywhereConfigurationProperty:
        def __init__(self, *, cost: typing.Optional[builtins.str] = None) -> None:
            '''Amazon GameLift Servers configuration options for your Anywhere fleets.

            :param cost: The cost to run your fleet per hour. Amazon GameLift Servers uses the provided cost of your fleet to balance usage in queues. For more information about queues, see `Setting up queues <https://docs.aws.amazon.com/gamelift/latest/developerguide/queues-intro.html>`_ in the *Amazon GameLift Servers Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-anywhereconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                anywhere_configuration_property = gamelift_mixins.CfnFleetPropsMixin.AnywhereConfigurationProperty(
                    cost="cost"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc3da749dd6288aa86e70677fcd2cf302e678369a8d37cc7f54d79f48414fe9d)
                check_type(argname="argument cost", value=cost, expected_type=type_hints["cost"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cost is not None:
                self._values["cost"] = cost

        @builtins.property
        def cost(self) -> typing.Optional[builtins.str]:
            '''The cost to run your fleet per hour.

            Amazon GameLift Servers uses the provided cost of your fleet to balance usage in queues. For more information about queues, see `Setting up queues <https://docs.aws.amazon.com/gamelift/latest/developerguide/queues-intro.html>`_ in the *Amazon GameLift Servers Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-anywhereconfiguration.html#cfn-gamelift-fleet-anywhereconfiguration-cost
            '''
            result = self._values.get("cost")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnywhereConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.CertificateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_type": "certificateType"},
    )
    class CertificateConfigurationProperty:
        def __init__(
            self,
            *,
            certificate_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Determines whether a TLS/SSL certificate is generated for a fleet.

            This feature must be enabled when creating the fleet. All instances in a fleet share the same certificate. The certificate can be retrieved by calling the `GameLift Server SDK <https://docs.aws.amazon.com/gamelift/latest/developerguide/reference-serversdk.html>`_ operation ``GetInstanceCertificate`` .

            :param certificate_type: Indicates whether a TLS/SSL certificate is generated for a fleet. Valid values include: - *GENERATED* - Generate a TLS/SSL certificate for this fleet. - *DISABLED* - (default) Do not generate a TLS/SSL certificate for this fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-certificateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                certificate_configuration_property = gamelift_mixins.CfnFleetPropsMixin.CertificateConfigurationProperty(
                    certificate_type="certificateType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b89f5c2bf840b272b96f988c45243eb8112fb7def70773ec8e0b4e90a2cd6fb5)
                check_type(argname="argument certificate_type", value=certificate_type, expected_type=type_hints["certificate_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_type is not None:
                self._values["certificate_type"] = certificate_type

        @builtins.property
        def certificate_type(self) -> typing.Optional[builtins.str]:
            '''Indicates whether a TLS/SSL certificate is generated for a fleet.

            Valid values include:

            - *GENERATED* - Generate a TLS/SSL certificate for this fleet.
            - *DISABLED* - (default) Do not generate a TLS/SSL certificate for this fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-certificateconfiguration.html#cfn-gamelift-fleet-certificateconfiguration-certificatetype
            '''
            result = self._values.get("certificate_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.IpPermissionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "from_port": "fromPort",
            "ip_range": "ipRange",
            "protocol": "protocol",
            "to_port": "toPort",
        },
    )
    class IpPermissionProperty:
        def __init__(
            self,
            *,
            from_port: typing.Optional[jsii.Number] = None,
            ip_range: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            to_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A range of IP addresses and port settings that allow inbound traffic to connect to server processes on an instance in a fleet.

            New game sessions are assigned an IP address/port number combination, which must fall into the fleet's allowed ranges. Fleets with custom game builds must have permissions explicitly set. For Realtime Servers fleets, GameLift automatically opens two port ranges, one for TCP messaging and one for UDP.

            :param from_port: A starting value for a range of allowed port numbers. For fleets using Linux builds, only ports ``22`` and ``1026-60000`` are valid. For fleets using Windows builds, only ports ``1026-60000`` are valid.
            :param ip_range: A range of allowed IP addresses. This value must be expressed in CIDR notation. Example: " ``000.000.000.000/[subnet mask]`` " or optionally the shortened version " ``0.0.0.0/[subnet mask]`` ".
            :param protocol: The network communication protocol used by the fleet.
            :param to_port: An ending value for a range of allowed port numbers. Port numbers are end-inclusive. This value must be equal to or greater than ``FromPort`` . For fleets using Linux builds, only ports ``22`` and ``1026-60000`` are valid. For fleets using Windows builds, only ports ``1026-60000`` are valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ippermission.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                ip_permission_property = gamelift_mixins.CfnFleetPropsMixin.IpPermissionProperty(
                    from_port=123,
                    ip_range="ipRange",
                    protocol="protocol",
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e386586abb4109e222af5aa3e2a7e4dc0e27ff97a51832dd07fff3935f33d88)
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument ip_range", value=ip_range, expected_type=type_hints["ip_range"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if from_port is not None:
                self._values["from_port"] = from_port
            if ip_range is not None:
                self._values["ip_range"] = ip_range
            if protocol is not None:
                self._values["protocol"] = protocol
            if to_port is not None:
                self._values["to_port"] = to_port

        @builtins.property
        def from_port(self) -> typing.Optional[jsii.Number]:
            '''A starting value for a range of allowed port numbers.

            For fleets using Linux builds, only ports ``22`` and ``1026-60000`` are valid.

            For fleets using Windows builds, only ports ``1026-60000`` are valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ippermission.html#cfn-gamelift-fleet-ippermission-fromport
            '''
            result = self._values.get("from_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ip_range(self) -> typing.Optional[builtins.str]:
            '''A range of allowed IP addresses.

            This value must be expressed in CIDR notation. Example: " ``000.000.000.000/[subnet mask]`` " or optionally the shortened version " ``0.0.0.0/[subnet mask]`` ".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ippermission.html#cfn-gamelift-fleet-ippermission-iprange
            '''
            result = self._values.get("ip_range")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The network communication protocol used by the fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ippermission.html#cfn-gamelift-fleet-ippermission-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def to_port(self) -> typing.Optional[jsii.Number]:
            '''An ending value for a range of allowed port numbers.

            Port numbers are end-inclusive. This value must be equal to or greater than ``FromPort`` .

            For fleets using Linux builds, only ports ``22`` and ``1026-60000`` are valid.

            For fleets using Windows builds, only ports ``1026-60000`` are valid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ippermission.html#cfn-gamelift-fleet-ippermission-toport
            '''
            result = self._values.get("to_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpPermissionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.LocationCapacityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "desired_ec2_instances": "desiredEc2Instances",
            "max_size": "maxSize",
            "min_size": "minSize",
        },
    )
    class LocationCapacityProperty:
        def __init__(
            self,
            *,
            desired_ec2_instances: typing.Optional[jsii.Number] = None,
            max_size: typing.Optional[jsii.Number] = None,
            min_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Current resource capacity settings for managed EC2 fleets and managed container fleets.

            For multi-location fleets, location values might refer to a fleet's remote location or its home Region.

            *Returned by:* `DescribeFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetCapacity.html>`_ , `DescribeFleetLocationCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetLocationCapacity.html>`_ , `UpdateFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateFleetCapacity.html>`_

            :param desired_ec2_instances: The number of Amazon EC2 instances you want to maintain in the specified fleet location. This value must fall between the minimum and maximum size limits. Changes in desired instance value can take up to 1 minute to be reflected when viewing the fleet's capacity settings.
            :param max_size: The maximum number of instances that are allowed in the specified fleet location. If this parameter is not set, the default is 1.
            :param min_size: The minimum number of instances that are allowed in the specified fleet location. If this parameter is not set, the default is 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-locationcapacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                location_capacity_property = gamelift_mixins.CfnFleetPropsMixin.LocationCapacityProperty(
                    desired_ec2_instances=123,
                    max_size=123,
                    min_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95348d5cfaacd4e5d2b106fb874f56d5eed8f213c5fbaf56b73fe9b79209dee8)
                check_type(argname="argument desired_ec2_instances", value=desired_ec2_instances, expected_type=type_hints["desired_ec2_instances"])
                check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
                check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if desired_ec2_instances is not None:
                self._values["desired_ec2_instances"] = desired_ec2_instances
            if max_size is not None:
                self._values["max_size"] = max_size
            if min_size is not None:
                self._values["min_size"] = min_size

        @builtins.property
        def desired_ec2_instances(self) -> typing.Optional[jsii.Number]:
            '''The number of Amazon EC2 instances you want to maintain in the specified fleet location.

            This value must fall between the minimum and maximum size limits. Changes in desired instance value can take up to 1 minute to be reflected when viewing the fleet's capacity settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-locationcapacity.html#cfn-gamelift-fleet-locationcapacity-desiredec2instances
            '''
            result = self._values.get("desired_ec2_instances")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of instances that are allowed in the specified fleet location.

            If this parameter is not set, the default is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-locationcapacity.html#cfn-gamelift-fleet-locationcapacity-maxsize
            '''
            result = self._values.get("max_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_size(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of instances that are allowed in the specified fleet location.

            If this parameter is not set, the default is 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-locationcapacity.html#cfn-gamelift-fleet-locationcapacity-minsize
            '''
            result = self._values.get("min_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationCapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.LocationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"location": "location", "location_capacity": "locationCapacity"},
    )
    class LocationConfigurationProperty:
        def __init__(
            self,
            *,
            location: typing.Optional[builtins.str] = None,
            location_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.LocationCapacityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A remote location where a multi-location fleet can deploy game servers for game hosting.

            :param location: An AWS Region code, such as ``us-west-2`` . For a list of supported Regions and Local Zones, see `Amazon GameLift Servers service locations <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-regions.html>`_ for managed hosting.
            :param location_capacity: Current resource capacity settings for managed EC2 fleets and managed container fleets. For multi-location fleets, location values might refer to a fleet's remote location or its home Region. *Returned by:* `DescribeFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetCapacity.html>`_ , `DescribeFleetLocationCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetLocationCapacity.html>`_ , `UpdateFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateFleetCapacity.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-locationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                location_configuration_property = gamelift_mixins.CfnFleetPropsMixin.LocationConfigurationProperty(
                    location="location",
                    location_capacity=gamelift_mixins.CfnFleetPropsMixin.LocationCapacityProperty(
                        desired_ec2_instances=123,
                        max_size=123,
                        min_size=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41c64a833baad7070389c39b43af363e72de9e6ec03ce82d9734f3cd96854e1a)
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument location_capacity", value=location_capacity, expected_type=type_hints["location_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if location is not None:
                self._values["location"] = location
            if location_capacity is not None:
                self._values["location_capacity"] = location_capacity

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''An AWS Region code, such as ``us-west-2`` .

            For a list of supported Regions and Local Zones, see `Amazon GameLift Servers service locations <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-regions.html>`_ for managed hosting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-locationconfiguration.html#cfn-gamelift-fleet-locationconfiguration-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location_capacity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.LocationCapacityProperty"]]:
            '''Current resource capacity settings for managed EC2 fleets and managed container fleets.

            For multi-location fleets, location values might refer to a fleet's remote location or its home Region.

            *Returned by:* `DescribeFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetCapacity.html>`_ , `DescribeFleetLocationCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_DescribeFleetLocationCapacity.html>`_ , `UpdateFleetCapacity <https://docs.aws.amazon.com/gamelift/latest/apireference/API_UpdateFleetCapacity.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-locationconfiguration.html#cfn-gamelift-fleet-locationconfiguration-locationcapacity
            '''
            result = self._values.get("location_capacity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.LocationCapacityProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.ResourceCreationLimitPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "new_game_sessions_per_creator": "newGameSessionsPerCreator",
            "policy_period_in_minutes": "policyPeriodInMinutes",
        },
    )
    class ResourceCreationLimitPolicyProperty:
        def __init__(
            self,
            *,
            new_game_sessions_per_creator: typing.Optional[jsii.Number] = None,
            policy_period_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A policy that limits the number of game sessions a player can create on the same fleet.

            This optional policy gives game owners control over how players can consume available game server resources. A resource creation policy makes the following statement: "An individual player can create a maximum number of new game sessions within a specified time period".

            The policy is evaluated when a player tries to create a new game session. For example, assume you have a policy of 10 new game sessions and a time period of 60 minutes. On receiving a ``CreateGameSession`` request, Amazon GameLift checks that the player (identified by ``CreatorId`` ) has created fewer than 10 game sessions in the past 60 minutes.

            :param new_game_sessions_per_creator: A policy that puts limits on the number of game sessions that a player can create within a specified span of time. With this policy, you can control players' ability to consume available resources. The policy is evaluated when a player tries to create a new game session. On receiving a ``CreateGameSession`` request, Amazon GameLift Servers checks that the player (identified by ``CreatorId`` ) has created fewer than game session limit in the specified time period.
            :param policy_period_in_minutes: The time span used in evaluating the resource creation limit policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-resourcecreationlimitpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                resource_creation_limit_policy_property = gamelift_mixins.CfnFleetPropsMixin.ResourceCreationLimitPolicyProperty(
                    new_game_sessions_per_creator=123,
                    policy_period_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e34cc098a96f554471f33ec98799068914a9800d47b4602d15e91e09c84f8eaa)
                check_type(argname="argument new_game_sessions_per_creator", value=new_game_sessions_per_creator, expected_type=type_hints["new_game_sessions_per_creator"])
                check_type(argname="argument policy_period_in_minutes", value=policy_period_in_minutes, expected_type=type_hints["policy_period_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if new_game_sessions_per_creator is not None:
                self._values["new_game_sessions_per_creator"] = new_game_sessions_per_creator
            if policy_period_in_minutes is not None:
                self._values["policy_period_in_minutes"] = policy_period_in_minutes

        @builtins.property
        def new_game_sessions_per_creator(self) -> typing.Optional[jsii.Number]:
            '''A policy that puts limits on the number of game sessions that a player can create within a specified span of time.

            With this policy, you can control players' ability to consume available resources.

            The policy is evaluated when a player tries to create a new game session. On receiving a ``CreateGameSession`` request, Amazon GameLift Servers checks that the player (identified by ``CreatorId`` ) has created fewer than game session limit in the specified time period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-resourcecreationlimitpolicy.html#cfn-gamelift-fleet-resourcecreationlimitpolicy-newgamesessionspercreator
            '''
            result = self._values.get("new_game_sessions_per_creator")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def policy_period_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The time span used in evaluating the resource creation limit policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-resourcecreationlimitpolicy.html#cfn-gamelift-fleet-resourcecreationlimitpolicy-policyperiodinminutes
            '''
            result = self._values.get("policy_period_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceCreationLimitPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.RuntimeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "game_session_activation_timeout_seconds": "gameSessionActivationTimeoutSeconds",
            "max_concurrent_game_session_activations": "maxConcurrentGameSessionActivations",
            "server_processes": "serverProcesses",
        },
    )
    class RuntimeConfigurationProperty:
        def __init__(
            self,
            *,
            game_session_activation_timeout_seconds: typing.Optional[jsii.Number] = None,
            max_concurrent_game_session_activations: typing.Optional[jsii.Number] = None,
            server_processes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.ServerProcessProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A collection of server process configurations that describe the set of processes to run on each instance in a fleet.

            Server processes run either an executable in a custom game build or a Realtime Servers script. GameLift launches the configured processes, manages their life cycle, and replaces them as needed. Each instance checks regularly for an updated runtime configuration.

            A GameLift instance is limited to 50 processes running concurrently. To calculate the total number of processes in a runtime configuration, add the values of the ``ConcurrentExecutions`` parameter for each ServerProcess. Learn more about `Running Multiple Processes on a Fleet <https://docs.aws.amazon.com/gamelift/latest/developerguide/fleets-multiprocess.html>`_ .

            :param game_session_activation_timeout_seconds: The maximum amount of time (in seconds) allowed to launch a new game session and have it report ready to host players. During this time, the game session is in status ``ACTIVATING`` . If the game session does not become active before the timeout, it is ended and the game session status is changed to ``TERMINATED`` .
            :param max_concurrent_game_session_activations: The number of game sessions in status ``ACTIVATING`` to allow on an instance or compute. This setting limits the instance resources that can be used for new game activations at any one time.
            :param server_processes: A collection of server process configurations that identify what server processes to run on fleet computes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-runtimeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                runtime_configuration_property = gamelift_mixins.CfnFleetPropsMixin.RuntimeConfigurationProperty(
                    game_session_activation_timeout_seconds=123,
                    max_concurrent_game_session_activations=123,
                    server_processes=[gamelift_mixins.CfnFleetPropsMixin.ServerProcessProperty(
                        concurrent_executions=123,
                        launch_path="launchPath",
                        parameters="parameters"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39c48bd572e7f66e8b617e9db95dc4f0594734c9c7cf545338fe86b43ee8d408)
                check_type(argname="argument game_session_activation_timeout_seconds", value=game_session_activation_timeout_seconds, expected_type=type_hints["game_session_activation_timeout_seconds"])
                check_type(argname="argument max_concurrent_game_session_activations", value=max_concurrent_game_session_activations, expected_type=type_hints["max_concurrent_game_session_activations"])
                check_type(argname="argument server_processes", value=server_processes, expected_type=type_hints["server_processes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if game_session_activation_timeout_seconds is not None:
                self._values["game_session_activation_timeout_seconds"] = game_session_activation_timeout_seconds
            if max_concurrent_game_session_activations is not None:
                self._values["max_concurrent_game_session_activations"] = max_concurrent_game_session_activations
            if server_processes is not None:
                self._values["server_processes"] = server_processes

        @builtins.property
        def game_session_activation_timeout_seconds(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time (in seconds) allowed to launch a new game session and have it report ready to host players.

            During this time, the game session is in status ``ACTIVATING`` . If the game session does not become active before the timeout, it is ended and the game session status is changed to ``TERMINATED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-runtimeconfiguration.html#cfn-gamelift-fleet-runtimeconfiguration-gamesessionactivationtimeoutseconds
            '''
            result = self._values.get("game_session_activation_timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_concurrent_game_session_activations(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The number of game sessions in status ``ACTIVATING`` to allow on an instance or compute.

            This setting limits the instance resources that can be used for new game activations at any one time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-runtimeconfiguration.html#cfn-gamelift-fleet-runtimeconfiguration-maxconcurrentgamesessionactivations
            '''
            result = self._values.get("max_concurrent_game_session_activations")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def server_processes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ServerProcessProperty"]]]]:
            '''A collection of server process configurations that identify what server processes to run on fleet computes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-runtimeconfiguration.html#cfn-gamelift-fleet-runtimeconfiguration-serverprocesses
            '''
            result = self._values.get("server_processes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.ServerProcessProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuntimeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.ScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "evaluation_periods": "evaluationPeriods",
            "location": "location",
            "metric_name": "metricName",
            "name": "name",
            "policy_type": "policyType",
            "scaling_adjustment": "scalingAdjustment",
            "scaling_adjustment_type": "scalingAdjustmentType",
            "status": "status",
            "target_configuration": "targetConfiguration",
            "threshold": "threshold",
            "update_status": "updateStatus",
        },
    )
    class ScalingPolicyProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            evaluation_periods: typing.Optional[jsii.Number] = None,
            location: typing.Optional[builtins.str] = None,
            metric_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            policy_type: typing.Optional[builtins.str] = None,
            scaling_adjustment: typing.Optional[jsii.Number] = None,
            scaling_adjustment_type: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFleetPropsMixin.TargetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            threshold: typing.Optional[jsii.Number] = None,
            update_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Rule that controls how a fleet is scaled.

            Scaling policies are uniquely identified by the combination of name and fleet ID.

            :param comparison_operator: Comparison operator to use when measuring a metric against the threshold value.
            :param evaluation_periods: Length of time (in minutes) the metric must be at or beyond the threshold before a scaling event is triggered.
            :param location: The fleet location.
            :param metric_name: Name of the Amazon GameLift Servers-defined metric that is used to trigger a scaling adjustment. For detailed descriptions of fleet metrics, see `Monitor Amazon GameLift Servers with Amazon CloudWatch <https://docs.aws.amazon.com/gamelift/latest/developerguide/monitoring-cloudwatch.html>`_ . - *ActivatingGameSessions* -- Game sessions in the process of being created. - *ActiveGameSessions* -- Game sessions that are currently running. - *ActiveInstances* -- Fleet instances that are currently running at least one game session. - *AvailableGameSessions* -- Additional game sessions that fleet could host simultaneously, given current capacity. - *AvailablePlayerSessions* -- Empty player slots in currently active game sessions. This includes game sessions that are not currently accepting players. Reserved player slots are not included. - *CurrentPlayerSessions* -- Player slots in active game sessions that are being used by a player or are reserved for a player. - *IdleInstances* -- Active instances that are currently hosting zero game sessions. - *PercentAvailableGameSessions* -- Unused percentage of the total number of game sessions that a fleet could host simultaneously, given current capacity. Use this metric for a target-based scaling policy. - *PercentIdleInstances* -- Percentage of the total number of active instances that are hosting zero game sessions. - *QueueDepth* -- Pending game session placement requests, in any queue, where the current fleet is the top-priority destination. - *WaitTime* -- Current wait time for pending game session placement requests, in any queue, where the current fleet is the top-priority destination.
            :param name: A descriptive label that is associated with a fleet's scaling policy. Policy names do not need to be unique.
            :param policy_type: The type of scaling policy to create. For a target-based policy, set the parameter *MetricName* to 'PercentAvailableGameSessions' and specify a *TargetConfiguration* . For a rule-based policy set the following parameters: *MetricName* , *ComparisonOperator* , *Threshold* , *EvaluationPeriods* , *ScalingAdjustmentType* , and *ScalingAdjustment* .
            :param scaling_adjustment: Amount of adjustment to make, based on the scaling adjustment type.
            :param scaling_adjustment_type: The type of adjustment to make to a fleet's instance count. - *ChangeInCapacity* -- add (or subtract) the scaling adjustment value from the current instance count. Positive values scale up while negative values scale down. - *ExactCapacity* -- set the instance count to the scaling adjustment value. - *PercentChangeInCapacity* -- increase or reduce the current instance count by the scaling adjustment, read as a percentage. Positive values scale up while negative values scale down.
            :param status: Current status of the scaling policy. The scaling policy can be in force only when in an ``ACTIVE`` status. Scaling policies can be suspended for individual fleets. If the policy is suspended for a fleet, the policy status does not change. - *ACTIVE* -- The scaling policy can be used for auto-scaling a fleet. - *UPDATE_REQUESTED* -- A request to update the scaling policy has been received. - *UPDATING* -- A change is being made to the scaling policy. - *DELETE_REQUESTED* -- A request to delete the scaling policy has been received. - *DELETING* -- The scaling policy is being deleted. - *DELETED* -- The scaling policy has been deleted. - *ERROR* -- An error occurred in creating the policy. It should be removed and recreated.
            :param target_configuration: An object that contains settings for a target-based scaling policy.
            :param threshold: Metric value used to trigger a scaling event.
            :param update_status: The current status of the fleet's scaling policies in a requested fleet location. The status ``PENDING_UPDATE`` indicates that an update was requested for the fleet but has not yet been completed for the location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                scaling_policy_property = gamelift_mixins.CfnFleetPropsMixin.ScalingPolicyProperty(
                    comparison_operator="comparisonOperator",
                    evaluation_periods=123,
                    location="location",
                    metric_name="metricName",
                    name="name",
                    policy_type="policyType",
                    scaling_adjustment=123,
                    scaling_adjustment_type="scalingAdjustmentType",
                    status="status",
                    target_configuration=gamelift_mixins.CfnFleetPropsMixin.TargetConfigurationProperty(
                        target_value=123
                    ),
                    threshold=123,
                    update_status="updateStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__569f9bb9a234e7c322fc63a1fdef706d93ebc57d60466540b96f1ed79f33a1c6)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
                check_type(argname="argument scaling_adjustment", value=scaling_adjustment, expected_type=type_hints["scaling_adjustment"])
                check_type(argname="argument scaling_adjustment_type", value=scaling_adjustment_type, expected_type=type_hints["scaling_adjustment_type"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument target_configuration", value=target_configuration, expected_type=type_hints["target_configuration"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
                check_type(argname="argument update_status", value=update_status, expected_type=type_hints["update_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if evaluation_periods is not None:
                self._values["evaluation_periods"] = evaluation_periods
            if location is not None:
                self._values["location"] = location
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if name is not None:
                self._values["name"] = name
            if policy_type is not None:
                self._values["policy_type"] = policy_type
            if scaling_adjustment is not None:
                self._values["scaling_adjustment"] = scaling_adjustment
            if scaling_adjustment_type is not None:
                self._values["scaling_adjustment_type"] = scaling_adjustment_type
            if status is not None:
                self._values["status"] = status
            if target_configuration is not None:
                self._values["target_configuration"] = target_configuration
            if threshold is not None:
                self._values["threshold"] = threshold
            if update_status is not None:
                self._values["update_status"] = update_status

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''Comparison operator to use when measuring a metric against the threshold value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def evaluation_periods(self) -> typing.Optional[jsii.Number]:
            '''Length of time (in minutes) the metric must be at or beyond the threshold before a scaling event is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-evaluationperiods
            '''
            result = self._values.get("evaluation_periods")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''The fleet location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''Name of the Amazon GameLift Servers-defined metric that is used to trigger a scaling adjustment.

            For detailed descriptions of fleet metrics, see `Monitor Amazon GameLift Servers with Amazon CloudWatch <https://docs.aws.amazon.com/gamelift/latest/developerguide/monitoring-cloudwatch.html>`_ .

            - *ActivatingGameSessions* -- Game sessions in the process of being created.
            - *ActiveGameSessions* -- Game sessions that are currently running.
            - *ActiveInstances* -- Fleet instances that are currently running at least one game session.
            - *AvailableGameSessions* -- Additional game sessions that fleet could host simultaneously, given current capacity.
            - *AvailablePlayerSessions* -- Empty player slots in currently active game sessions. This includes game sessions that are not currently accepting players. Reserved player slots are not included.
            - *CurrentPlayerSessions* -- Player slots in active game sessions that are being used by a player or are reserved for a player.
            - *IdleInstances* -- Active instances that are currently hosting zero game sessions.
            - *PercentAvailableGameSessions* -- Unused percentage of the total number of game sessions that a fleet could host simultaneously, given current capacity. Use this metric for a target-based scaling policy.
            - *PercentIdleInstances* -- Percentage of the total number of active instances that are hosting zero game sessions.
            - *QueueDepth* -- Pending game session placement requests, in any queue, where the current fleet is the top-priority destination.
            - *WaitTime* -- Current wait time for pending game session placement requests, in any queue, where the current fleet is the top-priority destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A descriptive label that is associated with a fleet's scaling policy.

            Policy names do not need to be unique.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_type(self) -> typing.Optional[builtins.str]:
            '''The type of scaling policy to create.

            For a target-based policy, set the parameter *MetricName* to 'PercentAvailableGameSessions' and specify a *TargetConfiguration* . For a rule-based policy set the following parameters: *MetricName* , *ComparisonOperator* , *Threshold* , *EvaluationPeriods* , *ScalingAdjustmentType* , and *ScalingAdjustment* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-policytype
            '''
            result = self._values.get("policy_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scaling_adjustment(self) -> typing.Optional[jsii.Number]:
            '''Amount of adjustment to make, based on the scaling adjustment type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-scalingadjustment
            '''
            result = self._values.get("scaling_adjustment")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scaling_adjustment_type(self) -> typing.Optional[builtins.str]:
            '''The type of adjustment to make to a fleet's instance count.

            - *ChangeInCapacity* -- add (or subtract) the scaling adjustment value from the current instance count. Positive values scale up while negative values scale down.
            - *ExactCapacity* -- set the instance count to the scaling adjustment value.
            - *PercentChangeInCapacity* -- increase or reduce the current instance count by the scaling adjustment, read as a percentage. Positive values scale up while negative values scale down.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-scalingadjustmenttype
            '''
            result = self._values.get("scaling_adjustment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Current status of the scaling policy.

            The scaling policy can be in force only when in an ``ACTIVE`` status. Scaling policies can be suspended for individual fleets. If the policy is suspended for a fleet, the policy status does not change.

            - *ACTIVE* -- The scaling policy can be used for auto-scaling a fleet.
            - *UPDATE_REQUESTED* -- A request to update the scaling policy has been received.
            - *UPDATING* -- A change is being made to the scaling policy.
            - *DELETE_REQUESTED* -- A request to delete the scaling policy has been received.
            - *DELETING* -- The scaling policy is being deleted.
            - *DELETED* -- The scaling policy has been deleted.
            - *ERROR* -- An error occurred in creating the policy. It should be removed and recreated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.TargetConfigurationProperty"]]:
            '''An object that contains settings for a target-based scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-targetconfiguration
            '''
            result = self._values.get("target_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFleetPropsMixin.TargetConfigurationProperty"]], result)

        @builtins.property
        def threshold(self) -> typing.Optional[jsii.Number]:
            '''Metric value used to trigger a scaling event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def update_status(self) -> typing.Optional[builtins.str]:
            '''The current status of the fleet's scaling policies in a requested fleet location.

            The status ``PENDING_UPDATE`` indicates that an update was requested for the fleet but has not yet been completed for the location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-scalingpolicy.html#cfn-gamelift-fleet-scalingpolicy-updatestatus
            '''
            result = self._values.get("update_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.ServerProcessProperty",
        jsii_struct_bases=[],
        name_mapping={
            "concurrent_executions": "concurrentExecutions",
            "launch_path": "launchPath",
            "parameters": "parameters",
        },
    )
    class ServerProcessProperty:
        def __init__(
            self,
            *,
            concurrent_executions: typing.Optional[jsii.Number] = None,
            launch_path: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A set of instructions for launching server processes on each instance in a fleet.

            Server processes run either an executable in a custom game build or a Realtime Servers script.

            :param concurrent_executions: The number of server processes using this configuration that run concurrently on each instance or compute.
            :param launch_path: The location of a game build executable or Realtime script. Game builds and Realtime scripts are installed on instances at the root: - Windows (custom game builds only): ``C:\\game`` . Example: " ``C:\\game\\MyGame\\server.exe`` " - Linux: ``/local/game`` . Examples: " ``/local/game/MyGame/server.exe`` " or " ``/local/game/MyRealtimeScript.js`` " .. epigraph:: Amazon GameLift Servers doesn't support the use of setup scripts that launch the game executable. For custom game builds, this parameter must indicate the executable that calls the server SDK operations ``initSDK()`` and ``ProcessReady()`` .
            :param parameters: An optional list of parameters to pass to the server executable or Realtime script on launch. Length Constraints: Minimum length of 1. Maximum length of 1024. Pattern: [A-Za-z0-9_:.+/\\- =@{},?'[]"]+

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-serverprocess.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                server_process_property = gamelift_mixins.CfnFleetPropsMixin.ServerProcessProperty(
                    concurrent_executions=123,
                    launch_path="launchPath",
                    parameters="parameters"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80c0ce09074cc7894a2e59d4ea6f069786205c80e0f6cb2d6b91b59d7b606cbf)
                check_type(argname="argument concurrent_executions", value=concurrent_executions, expected_type=type_hints["concurrent_executions"])
                check_type(argname="argument launch_path", value=launch_path, expected_type=type_hints["launch_path"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if concurrent_executions is not None:
                self._values["concurrent_executions"] = concurrent_executions
            if launch_path is not None:
                self._values["launch_path"] = launch_path
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def concurrent_executions(self) -> typing.Optional[jsii.Number]:
            '''The number of server processes using this configuration that run concurrently on each instance or compute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-serverprocess.html#cfn-gamelift-fleet-serverprocess-concurrentexecutions
            '''
            result = self._values.get("concurrent_executions")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def launch_path(self) -> typing.Optional[builtins.str]:
            '''The location of a game build executable or Realtime script.

            Game builds and Realtime scripts are installed on instances at the root:

            - Windows (custom game builds only): ``C:\\game`` . Example: " ``C:\\game\\MyGame\\server.exe`` "
            - Linux: ``/local/game`` . Examples: " ``/local/game/MyGame/server.exe`` " or " ``/local/game/MyRealtimeScript.js`` "

            .. epigraph::

               Amazon GameLift Servers doesn't support the use of setup scripts that launch the game executable. For custom game builds, this parameter must indicate the executable that calls the server SDK operations ``initSDK()`` and ``ProcessReady()`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-serverprocess.html#cfn-gamelift-fleet-serverprocess-launchpath
            '''
            result = self._values.get("launch_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Optional[builtins.str]:
            '''An optional list of parameters to pass to the server executable or Realtime script on launch.

            Length Constraints: Minimum length of 1. Maximum length of 1024.

            Pattern: [A-Za-z0-9_:.+/- =@{},?'[]"]+

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-serverprocess.html#cfn-gamelift-fleet-serverprocess-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerProcessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnFleetPropsMixin.TargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"target_value": "targetValue"},
    )
    class TargetConfigurationProperty:
        def __init__(
            self,
            *,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Settings for a target-based scaling policy.

            A target-based policy tracks a particular fleet metric specifies a target value for the metric. As player usage changes, the policy triggers Amazon GameLift Servers to adjust capacity so that the metric returns to the target value. The target configuration specifies settings as needed for the target based policy, including the target value.

            :param target_value: Desired value to use with a target-based scaling policy. The value must be relevant for whatever metric the scaling policy is using. For example, in a policy using the metric PercentAvailableGameSessions, the target value should be the preferred size of the fleet's buffer (the percent of capacity that should be idle and ready for new game sessions).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-targetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                target_configuration_property = gamelift_mixins.CfnFleetPropsMixin.TargetConfigurationProperty(
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45a0ac463568f437d743c7a282c74f8a87f66f966c533cf91c305104e906d4aa)
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''Desired value to use with a target-based scaling policy.

            The value must be relevant for whatever metric the scaling policy is using. For example, in a policy using the metric PercentAvailableGameSessions, the target value should be the preferred size of the fleet's buffer (the percent of capacity that should be idle and ready for new game sessions).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-targetconfiguration.html#cfn-gamelift-fleet-targetconfiguration-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameServerGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_policy": "autoScalingPolicy",
        "balancing_strategy": "balancingStrategy",
        "delete_option": "deleteOption",
        "game_server_group_name": "gameServerGroupName",
        "game_server_protection_policy": "gameServerProtectionPolicy",
        "instance_definitions": "instanceDefinitions",
        "launch_template": "launchTemplate",
        "max_size": "maxSize",
        "min_size": "minSize",
        "role_arn": "roleArn",
        "tags": "tags",
        "vpc_subnets": "vpcSubnets",
    },
)
class CfnGameServerGroupMixinProps:
    def __init__(
        self,
        *,
        auto_scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGameServerGroupPropsMixin.AutoScalingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        balancing_strategy: typing.Optional[builtins.str] = None,
        delete_option: typing.Optional[builtins.str] = None,
        game_server_group_name: typing.Optional[builtins.str] = None,
        game_server_protection_policy: typing.Optional[builtins.str] = None,
        instance_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGameServerGroupPropsMixin.InstanceDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGameServerGroupPropsMixin.LaunchTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnGameServerGroupPropsMixin.

        :param auto_scaling_policy: Configuration settings to define a scaling policy for the Auto Scaling group that is optimized for game hosting. The scaling policy uses the metric ``"PercentUtilizedGameServers"`` to maintain a buffer of idle game servers that can immediately accommodate new games and players. After the Auto Scaling group is created, update this value directly in the Auto Scaling group using the AWS console or APIs.
        :param balancing_strategy: Indicates how Amazon GameLift Servers FleetIQ balances the use of Spot Instances and On-Demand Instances in the game server group. Method options include the following: - ``SPOT_ONLY`` - Only Spot Instances are used in the game server group. If Spot Instances are unavailable or not viable for game hosting, the game server group provides no hosting capacity until Spot Instances can again be used. Until then, no new instances are started, and the existing nonviable Spot Instances are terminated (after current gameplay ends) and are not replaced. - ``SPOT_PREFERRED`` - (default value) Spot Instances are used whenever available in the game server group. If Spot Instances are unavailable, the game server group continues to provide hosting capacity by falling back to On-Demand Instances. Existing nonviable Spot Instances are terminated (after current gameplay ends) and are replaced with new On-Demand Instances. - ``ON_DEMAND_ONLY`` - Only On-Demand Instances are used in the game server group. No Spot Instances are used, even when available, while this balancing strategy is in force.
        :param delete_option: The type of delete to perform. To delete a game server group, specify the ``DeleteOption`` . Options include the following: - ``SAFE_DELETE`` – (default) Terminates the game server group and Amazon EC2 Auto Scaling group only when it has no game servers that are in ``UTILIZED`` status. - ``FORCE_DELETE`` – Terminates the game server group, including all active game servers regardless of their utilization status, and the Amazon EC2 Auto Scaling group. - ``RETAIN`` – Does a safe delete of the game server group but retains the Amazon EC2 Auto Scaling group as is.
        :param game_server_group_name: A developer-defined identifier for the game server group. The name is unique for each Region in each AWS account.
        :param game_server_protection_policy: A flag that indicates whether instances in the game server group are protected from early termination. Unprotected instances that have active game servers running might be terminated during a scale-down event, causing players to be dropped from the game. Protected instances cannot be terminated while there are active game servers running except in the event of a forced game server group deletion (see ). An exception to this is with Spot Instances, which can be terminated by AWS regardless of protection status.
        :param instance_definitions: The set of Amazon EC2 instance types that Amazon GameLift Servers FleetIQ can use when balancing and automatically scaling instances in the corresponding Auto Scaling group.
        :param launch_template: The Amazon EC2 launch template that contains configuration settings and game server code to be deployed to all instances in the game server group. You can specify the template using either the template name or ID. For help with creating a launch template, see `Creating a Launch Template for an Auto Scaling Group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-template.html>`_ in the *Amazon Elastic Compute Cloud Auto Scaling User Guide* . After the Auto Scaling group is created, update this value directly in the Auto Scaling group using the AWS console or APIs. .. epigraph:: If you specify network interfaces in your launch template, you must explicitly set the property ``AssociatePublicIpAddress`` to "true". If no network interface is specified in the launch template, Amazon GameLift Servers FleetIQ uses your account's default VPC.
        :param max_size: The maximum number of instances allowed in the Amazon EC2 Auto Scaling group. During automatic scaling events, Amazon GameLift Servers FleetIQ and EC2 do not scale up the group above this maximum. After the Auto Scaling group is created, update this value directly in the Auto Scaling group using the AWS console or APIs.
        :param min_size: The minimum number of instances allowed in the Amazon EC2 Auto Scaling group. During automatic scaling events, Amazon GameLift Servers FleetIQ and Amazon EC2 do not scale down the group below this minimum. In production, this value should be set to at least 1. After the Auto Scaling group is created, update this value directly in the Auto Scaling group using the AWS console or APIs.
        :param role_arn: The Amazon Resource Name ( `ARN <https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-arn-format.html>`_ ) for an IAM role that allows Amazon GameLift Servers to access your Amazon EC2 Auto Scaling groups.
        :param tags: A list of labels to assign to the new game server group resource. Tags are developer-defined key-value pairs. Tagging AWS resources is useful for resource management, access management, and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags, respectively. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.
        :param vpc_subnets: A list of virtual private cloud (VPC) subnets to use with instances in the game server group. By default, all Amazon GameLift Servers FleetIQ-supported Availability Zones are used. You can use this parameter to specify VPCs that you've set up. This property cannot be updated after the game server group is created, and the corresponding Auto Scaling group will always use the property value that is set with this request, even if the Auto Scaling group is updated directly.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_game_server_group_mixin_props = gamelift_mixins.CfnGameServerGroupMixinProps(
                auto_scaling_policy=gamelift_mixins.CfnGameServerGroupPropsMixin.AutoScalingPolicyProperty(
                    estimated_instance_warmup=123,
                    target_tracking_configuration=gamelift_mixins.CfnGameServerGroupPropsMixin.TargetTrackingConfigurationProperty(
                        target_value=123
                    )
                ),
                balancing_strategy="balancingStrategy",
                delete_option="deleteOption",
                game_server_group_name="gameServerGroupName",
                game_server_protection_policy="gameServerProtectionPolicy",
                instance_definitions=[gamelift_mixins.CfnGameServerGroupPropsMixin.InstanceDefinitionProperty(
                    instance_type="instanceType",
                    weighted_capacity="weightedCapacity"
                )],
                launch_template=gamelift_mixins.CfnGameServerGroupPropsMixin.LaunchTemplateProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    version="version"
                ),
                max_size=123,
                min_size=123,
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_subnets=["vpcSubnets"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3375602a7736273e52043459b36956cc27c340327eea23088a4daa8dd223e4a8)
            check_type(argname="argument auto_scaling_policy", value=auto_scaling_policy, expected_type=type_hints["auto_scaling_policy"])
            check_type(argname="argument balancing_strategy", value=balancing_strategy, expected_type=type_hints["balancing_strategy"])
            check_type(argname="argument delete_option", value=delete_option, expected_type=type_hints["delete_option"])
            check_type(argname="argument game_server_group_name", value=game_server_group_name, expected_type=type_hints["game_server_group_name"])
            check_type(argname="argument game_server_protection_policy", value=game_server_protection_policy, expected_type=type_hints["game_server_protection_policy"])
            check_type(argname="argument instance_definitions", value=instance_definitions, expected_type=type_hints["instance_definitions"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
            check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_policy is not None:
            self._values["auto_scaling_policy"] = auto_scaling_policy
        if balancing_strategy is not None:
            self._values["balancing_strategy"] = balancing_strategy
        if delete_option is not None:
            self._values["delete_option"] = delete_option
        if game_server_group_name is not None:
            self._values["game_server_group_name"] = game_server_group_name
        if game_server_protection_policy is not None:
            self._values["game_server_protection_policy"] = game_server_protection_policy
        if instance_definitions is not None:
            self._values["instance_definitions"] = instance_definitions
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def auto_scaling_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameServerGroupPropsMixin.AutoScalingPolicyProperty"]]:
        '''Configuration settings to define a scaling policy for the Auto Scaling group that is optimized for game hosting.

        The scaling policy uses the metric ``"PercentUtilizedGameServers"`` to maintain a buffer of idle game servers that can immediately accommodate new games and players. After the Auto Scaling group is created, update this value directly in the Auto Scaling group using the AWS console or APIs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-autoscalingpolicy
        '''
        result = self._values.get("auto_scaling_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameServerGroupPropsMixin.AutoScalingPolicyProperty"]], result)

    @builtins.property
    def balancing_strategy(self) -> typing.Optional[builtins.str]:
        '''Indicates how Amazon GameLift Servers FleetIQ balances the use of Spot Instances and On-Demand Instances in the game server group.

        Method options include the following:

        - ``SPOT_ONLY`` - Only Spot Instances are used in the game server group. If Spot Instances are unavailable or not viable for game hosting, the game server group provides no hosting capacity until Spot Instances can again be used. Until then, no new instances are started, and the existing nonviable Spot Instances are terminated (after current gameplay ends) and are not replaced.
        - ``SPOT_PREFERRED`` - (default value) Spot Instances are used whenever available in the game server group. If Spot Instances are unavailable, the game server group continues to provide hosting capacity by falling back to On-Demand Instances. Existing nonviable Spot Instances are terminated (after current gameplay ends) and are replaced with new On-Demand Instances.
        - ``ON_DEMAND_ONLY`` - Only On-Demand Instances are used in the game server group. No Spot Instances are used, even when available, while this balancing strategy is in force.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-balancingstrategy
        '''
        result = self._values.get("balancing_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_option(self) -> typing.Optional[builtins.str]:
        '''The type of delete to perform.

        To delete a game server group, specify the ``DeleteOption`` . Options include the following:

        - ``SAFE_DELETE`` – (default) Terminates the game server group and Amazon EC2 Auto Scaling group only when it has no game servers that are in ``UTILIZED`` status.
        - ``FORCE_DELETE`` – Terminates the game server group, including all active game servers regardless of their utilization status, and the Amazon EC2 Auto Scaling group.
        - ``RETAIN`` – Does a safe delete of the game server group but retains the Amazon EC2 Auto Scaling group as is.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-deleteoption
        '''
        result = self._values.get("delete_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def game_server_group_name(self) -> typing.Optional[builtins.str]:
        '''A developer-defined identifier for the game server group.

        The name is unique for each Region in each AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-gameservergroupname
        '''
        result = self._values.get("game_server_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def game_server_protection_policy(self) -> typing.Optional[builtins.str]:
        '''A flag that indicates whether instances in the game server group are protected from early termination.

        Unprotected instances that have active game servers running might be terminated during a scale-down event, causing players to be dropped from the game. Protected instances cannot be terminated while there are active game servers running except in the event of a forced game server group deletion (see ). An exception to this is with Spot Instances, which can be terminated by AWS regardless of protection status.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-gameserverprotectionpolicy
        '''
        result = self._values.get("game_server_protection_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_definitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameServerGroupPropsMixin.InstanceDefinitionProperty"]]]]:
        '''The set of Amazon EC2 instance types that Amazon GameLift Servers FleetIQ can use when balancing and automatically scaling instances in the corresponding Auto Scaling group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-instancedefinitions
        '''
        result = self._values.get("instance_definitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameServerGroupPropsMixin.InstanceDefinitionProperty"]]]], result)

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameServerGroupPropsMixin.LaunchTemplateProperty"]]:
        '''The Amazon EC2 launch template that contains configuration settings and game server code to be deployed to all instances in the game server group.

        You can specify the template using either the template name or ID. For help with creating a launch template, see `Creating a Launch Template for an Auto Scaling Group <https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-launch-template.html>`_ in the *Amazon Elastic Compute Cloud Auto Scaling User Guide* . After the Auto Scaling group is created, update this value directly in the Auto Scaling group using the AWS console or APIs.
        .. epigraph::

           If you specify network interfaces in your launch template, you must explicitly set the property ``AssociatePublicIpAddress`` to "true". If no network interface is specified in the launch template, Amazon GameLift Servers FleetIQ uses your account's default VPC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-launchtemplate
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameServerGroupPropsMixin.LaunchTemplateProperty"]], result)

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of instances allowed in the Amazon EC2 Auto Scaling group.

        During automatic scaling events, Amazon GameLift Servers FleetIQ and EC2 do not scale up the group above this maximum. After the Auto Scaling group is created, update this value directly in the Auto Scaling group using the AWS console or APIs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-maxsize
        '''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of instances allowed in the Amazon EC2 Auto Scaling group.

        During automatic scaling events, Amazon GameLift Servers FleetIQ and Amazon EC2 do not scale down the group below this minimum. In production, this value should be set to at least 1. After the Auto Scaling group is created, update this value directly in the Auto Scaling group using the AWS console or APIs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-minsize
        '''
        result = self._values.get("min_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name ( `ARN <https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-arn-format.html>`_ ) for an IAM role that allows Amazon GameLift Servers to access your Amazon EC2 Auto Scaling groups.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of labels to assign to the new game server group resource.

        Tags are developer-defined key-value pairs. Tagging AWS resources is useful for resource management, access management, and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags, respectively. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of virtual private cloud (VPC) subnets to use with instances in the game server group.

        By default, all Amazon GameLift Servers FleetIQ-supported Availability Zones are used. You can use this parameter to specify VPCs that you've set up. This property cannot be updated after the game server group is created, and the corresponding Auto Scaling group will always use the property value that is set with this request, even if the Auto Scaling group is updated directly.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-vpcsubnets
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGameServerGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGameServerGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameServerGroupPropsMixin",
):
    '''*This operation is used with the Amazon GameLift FleetIQ solution and game server groups.*.

    Creates a GameLift FleetIQ game server group for managing game hosting on a collection of Amazon EC2 instances for game hosting. This operation creates the game server group, creates an Auto Scaling group in your AWS account , and establishes a link between the two groups. You can view the status of your game server groups in the GameLift console. Game server group metrics and events are emitted to Amazon CloudWatch.

    Before creating a new game server group, you must have the following:

    - An Amazon EC2 launch template that specifies how to launch Amazon EC2 instances with your game server build. For more information, see `Launching an Instance from a Launch Template <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html>`_ in the *Amazon EC2 User Guide* .
    - An IAM role that extends limited access to your AWS account to allow GameLift FleetIQ to create and interact with the Auto Scaling group. For more information, see `Create IAM roles for cross-service interaction <https://docs.aws.amazon.com/gamelift/latest/fleetiqguide/gsg-iam-permissions-roles.html>`_ in the *GameLift FleetIQ Developer Guide* .

    To create a new game server group, specify a unique group name, IAM role and Amazon EC2 launch template, and provide a list of instance types that can be used in the group. You must also set initial maximum and minimum limits on the group's instance count. You can optionally set an Auto Scaling policy with target tracking based on a GameLift FleetIQ metric.

    Once the game server group and corresponding Auto Scaling group are created, you have full access to change the Auto Scaling group's configuration as needed. Several properties that are set when creating a game server group, including maximum/minimum size and auto-scaling policy settings, must be updated directly in the Auto Scaling group. Keep in mind that some Auto Scaling group properties are periodically updated by GameLift FleetIQ as part of its balancing activities to optimize for availability and cost.

    *Learn more*

    `GameLift FleetIQ Guide <https://docs.aws.amazon.com/gamelift/latest/fleetiqguide/gsg-intro.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html
    :cloudformationResource: AWS::GameLift::GameServerGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_game_server_group_props_mixin = gamelift_mixins.CfnGameServerGroupPropsMixin(gamelift_mixins.CfnGameServerGroupMixinProps(
            auto_scaling_policy=gamelift_mixins.CfnGameServerGroupPropsMixin.AutoScalingPolicyProperty(
                estimated_instance_warmup=123,
                target_tracking_configuration=gamelift_mixins.CfnGameServerGroupPropsMixin.TargetTrackingConfigurationProperty(
                    target_value=123
                )
            ),
            balancing_strategy="balancingStrategy",
            delete_option="deleteOption",
            game_server_group_name="gameServerGroupName",
            game_server_protection_policy="gameServerProtectionPolicy",
            instance_definitions=[gamelift_mixins.CfnGameServerGroupPropsMixin.InstanceDefinitionProperty(
                instance_type="instanceType",
                weighted_capacity="weightedCapacity"
            )],
            launch_template=gamelift_mixins.CfnGameServerGroupPropsMixin.LaunchTemplateProperty(
                launch_template_id="launchTemplateId",
                launch_template_name="launchTemplateName",
                version="version"
            ),
            max_size=123,
            min_size=123,
            role_arn="roleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_subnets=["vpcSubnets"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGameServerGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::GameServerGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8c0f00d8c86d543bfadf529b058010002513e67d6d58ab28ec60181bfc3e23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a8bc467cd8b3f1af2a2ce7054718e93a0ab4f4792d8c24728c75f3c050ebaf4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e0f1d9c9c89541d488665ee3e2ae098632489d8e207cd95390050442786f7f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGameServerGroupMixinProps:
        return typing.cast(CfnGameServerGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameServerGroupPropsMixin.AutoScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "estimated_instance_warmup": "estimatedInstanceWarmup",
            "target_tracking_configuration": "targetTrackingConfiguration",
        },
    )
    class AutoScalingPolicyProperty:
        def __init__(
            self,
            *,
            estimated_instance_warmup: typing.Optional[jsii.Number] = None,
            target_tracking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGameServerGroupPropsMixin.TargetTrackingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''*This data type is used with the GameLift FleetIQ and game server groups.*.

            Configuration settings for intelligent automatic scaling that uses target tracking. After the Auto Scaling group is created, all updates to Auto Scaling policies, including changing this policy and adding or removing other policies, is done directly on the Auto Scaling group.

            :param estimated_instance_warmup: Length of time, in seconds, it takes for a new instance to start new game server processes and register with Amazon GameLift Servers FleetIQ. Specifying a warm-up time can be useful, particularly with game servers that take a long time to start up, because it avoids prematurely starting new instances.
            :param target_tracking_configuration: Settings for a target-based scaling policy applied to Auto Scaling group. These settings are used to create a target-based policy that tracks the GameLift FleetIQ metric ``PercentUtilizedGameServers`` and specifies a target value for the metric. As player usage changes, the policy triggers to adjust the game server group capacity so that the metric returns to the target value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-autoscalingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                auto_scaling_policy_property = gamelift_mixins.CfnGameServerGroupPropsMixin.AutoScalingPolicyProperty(
                    estimated_instance_warmup=123,
                    target_tracking_configuration=gamelift_mixins.CfnGameServerGroupPropsMixin.TargetTrackingConfigurationProperty(
                        target_value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea1e902451654b3058cc5380e12b07e9cfbc3feaabc3fb2ab36b3909b0fc52f1)
                check_type(argname="argument estimated_instance_warmup", value=estimated_instance_warmup, expected_type=type_hints["estimated_instance_warmup"])
                check_type(argname="argument target_tracking_configuration", value=target_tracking_configuration, expected_type=type_hints["target_tracking_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if estimated_instance_warmup is not None:
                self._values["estimated_instance_warmup"] = estimated_instance_warmup
            if target_tracking_configuration is not None:
                self._values["target_tracking_configuration"] = target_tracking_configuration

        @builtins.property
        def estimated_instance_warmup(self) -> typing.Optional[jsii.Number]:
            '''Length of time, in seconds, it takes for a new instance to start new game server processes and register with Amazon GameLift Servers FleetIQ.

            Specifying a warm-up time can be useful, particularly with game servers that take a long time to start up, because it avoids prematurely starting new instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-autoscalingpolicy.html#cfn-gamelift-gameservergroup-autoscalingpolicy-estimatedinstancewarmup
            '''
            result = self._values.get("estimated_instance_warmup")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def target_tracking_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameServerGroupPropsMixin.TargetTrackingConfigurationProperty"]]:
            '''Settings for a target-based scaling policy applied to Auto Scaling group.

            These settings are used to create a target-based policy that tracks the GameLift FleetIQ metric ``PercentUtilizedGameServers`` and specifies a target value for the metric. As player usage changes, the policy triggers to adjust the game server group capacity so that the metric returns to the target value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-autoscalingpolicy.html#cfn-gamelift-gameservergroup-autoscalingpolicy-targettrackingconfiguration
            '''
            result = self._values.get("target_tracking_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameServerGroupPropsMixin.TargetTrackingConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameServerGroupPropsMixin.InstanceDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_type": "instanceType",
            "weighted_capacity": "weightedCapacity",
        },
    )
    class InstanceDefinitionProperty:
        def __init__(
            self,
            *,
            instance_type: typing.Optional[builtins.str] = None,
            weighted_capacity: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*This data type is used with the Amazon GameLift FleetIQ and game server groups.*.

            An allowed instance type for a ``GameServerGroup`` . All game server groups must have at least two instance types defined for it. GameLift FleetIQ periodically evaluates each defined instance type for viability. It then updates the Auto Scaling group with the list of viable instance types.

            :param instance_type: An Amazon EC2 instance type designation.
            :param weighted_capacity: Instance weighting that indicates how much this instance type contributes to the total capacity of a game server group. Instance weights are used by Amazon GameLift Servers FleetIQ to calculate the instance type's cost per unit hour and better identify the most cost-effective options. For detailed information on weighting instance capacity, see `Instance Weighting <https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-instance-weighting.html>`_ in the *Amazon Elastic Compute Cloud Auto Scaling User Guide* . Default value is "1".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-instancedefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                instance_definition_property = gamelift_mixins.CfnGameServerGroupPropsMixin.InstanceDefinitionProperty(
                    instance_type="instanceType",
                    weighted_capacity="weightedCapacity"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__633faa659aa47c301aa973f55865f2eef79a6c97ea07cd0e2c0e86376c69260b)
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument weighted_capacity", value=weighted_capacity, expected_type=type_hints["weighted_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if weighted_capacity is not None:
                self._values["weighted_capacity"] = weighted_capacity

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''An Amazon EC2 instance type designation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-instancedefinition.html#cfn-gamelift-gameservergroup-instancedefinition-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weighted_capacity(self) -> typing.Optional[builtins.str]:
            '''Instance weighting that indicates how much this instance type contributes to the total capacity of a game server group.

            Instance weights are used by Amazon GameLift Servers FleetIQ to calculate the instance type's cost per unit hour and better identify the most cost-effective options. For detailed information on weighting instance capacity, see `Instance Weighting <https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-instance-weighting.html>`_ in the *Amazon Elastic Compute Cloud Auto Scaling User Guide* . Default value is "1".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-instancedefinition.html#cfn-gamelift-gameservergroup-instancedefinition-weightedcapacity
            '''
            result = self._values.get("weighted_capacity")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameServerGroupPropsMixin.LaunchTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_id": "launchTemplateId",
            "launch_template_name": "launchTemplateName",
            "version": "version",
        },
    )
    class LaunchTemplateProperty:
        def __init__(
            self,
            *,
            launch_template_id: typing.Optional[builtins.str] = None,
            launch_template_name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*This data type is used with the GameLift FleetIQ and game server groups.*.

            An Amazon EC2 launch template that contains configuration settings and game server code to be deployed to all instances in a game server group. The launch template is specified when creating a new game server group with ``GameServerGroup`` .

            :param launch_template_id: A unique identifier for an existing Amazon EC2 launch template.
            :param launch_template_name: A readable identifier for an existing Amazon EC2 launch template.
            :param version: The version of the Amazon EC2 launch template to use. If no version is specified, the default version will be used. With Amazon EC2, you can specify a default version for a launch template. If none is set, the default is the first version created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-launchtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                launch_template_property = gamelift_mixins.CfnGameServerGroupPropsMixin.LaunchTemplateProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d21a0ad8b86d60f198ef2ea55ed0e63fb9c11da3a9de2bdb2a11bf3d92c496ec)
                check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None:
                self._values["launch_template_name"] = launch_template_name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for an existing Amazon EC2 launch template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-launchtemplate.html#cfn-gamelift-gameservergroup-launchtemplate-launchtemplateid
            '''
            result = self._values.get("launch_template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_template_name(self) -> typing.Optional[builtins.str]:
            '''A readable identifier for an existing Amazon EC2 launch template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-launchtemplate.html#cfn-gamelift-gameservergroup-launchtemplate-launchtemplatename
            '''
            result = self._values.get("launch_template_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the Amazon EC2 launch template to use.

            If no version is specified, the default version will be used. With Amazon EC2, you can specify a default version for a launch template. If none is set, the default is the first version created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-launchtemplate.html#cfn-gamelift-gameservergroup-launchtemplate-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameServerGroupPropsMixin.TargetTrackingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"target_value": "targetValue"},
    )
    class TargetTrackingConfigurationProperty:
        def __init__(
            self,
            *,
            target_value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''*This data type is used with the Amazon GameLift FleetIQ and game server groups.*.

            Settings for a target-based scaling policy as part of a ``GameServerGroupAutoScalingPolicy`` . These settings are used to create a target-based policy that tracks the GameLift FleetIQ metric ``"PercentUtilizedGameServers"`` and specifies a target value for the metric. As player usage changes, the policy triggers to adjust the game server group capacity so that the metric returns to the target value.

            :param target_value: Desired value to use with a game server group target-based scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-targettrackingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                target_tracking_configuration_property = gamelift_mixins.CfnGameServerGroupPropsMixin.TargetTrackingConfigurationProperty(
                    target_value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5dd0cdc03286f3cc2b8df9b3026eaff1265d71d3256e2ffb7fc0db3e43214fc)
                check_type(argname="argument target_value", value=target_value, expected_type=type_hints["target_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_value is not None:
                self._values["target_value"] = target_value

        @builtins.property
        def target_value(self) -> typing.Optional[jsii.Number]:
            '''Desired value to use with a game server group target-based scaling policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-targettrackingconfiguration.html#cfn-gamelift-gameservergroup-targettrackingconfiguration-targetvalue
            '''
            result = self._values.get("target_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameSessionQueueMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "custom_event_data": "customEventData",
        "destinations": "destinations",
        "filter_configuration": "filterConfiguration",
        "name": "name",
        "notification_target": "notificationTarget",
        "player_latency_policies": "playerLatencyPolicies",
        "priority_configuration": "priorityConfiguration",
        "tags": "tags",
        "timeout_in_seconds": "timeoutInSeconds",
    },
)
class CfnGameSessionQueueMixinProps:
    def __init__(
        self,
        *,
        custom_event_data: typing.Optional[builtins.str] = None,
        destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGameSessionQueuePropsMixin.DestinationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGameSessionQueuePropsMixin.FilterConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        notification_target: typing.Optional[builtins.str] = None,
        player_latency_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGameSessionQueuePropsMixin.PlayerLatencyPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        priority_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGameSessionQueuePropsMixin.PriorityConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnGameSessionQueuePropsMixin.

        :param custom_event_data: Information to be added to all events that are related to this game session queue.
        :param destinations: A list of fleets and/or fleet aliases that can be used to fulfill game session placement requests in the queue. Destinations are identified by either a fleet ARN or a fleet alias ARN, and are listed in order of placement preference.
        :param filter_configuration: A list of locations where a queue is allowed to place new game sessions. Locations are specified in the form of AWS Region codes, such as ``us-west-2`` . If this parameter is not set, game sessions can be placed in any queue location.
        :param name: A descriptive label that is associated with game session queue. Queue names must be unique within each Region.
        :param notification_target: An SNS topic ARN that is set up to receive game session placement notifications. See `Setting up notifications for game session placement <https://docs.aws.amazon.com/gamelift/latest/developerguide/queue-notification.html>`_ .
        :param player_latency_policies: A set of policies that enforce a sliding cap on player latency when processing game sessions placement requests. Use multiple policies to gradually relax the cap over time if Amazon GameLift Servers can't make a placement. Policies are evaluated in order starting with the lowest maximum latency value.
        :param priority_configuration: Custom settings to use when prioritizing destinations and locations for game session placements. This configuration replaces the FleetIQ default prioritization process. Priority types that are not explicitly named will be automatically applied at the end of the prioritization process.
        :param tags: A list of labels to assign to the new game session queue resource. Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.
        :param timeout_in_seconds: The maximum time, in seconds, that a new game session placement request remains in the queue. When a request exceeds this time, the game session placement changes to a ``TIMED_OUT`` status. If you don't specify a request timeout, the queue uses a default value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_game_session_queue_mixin_props = gamelift_mixins.CfnGameSessionQueueMixinProps(
                custom_event_data="customEventData",
                destinations=[gamelift_mixins.CfnGameSessionQueuePropsMixin.DestinationProperty(
                    destination_arn="destinationArn"
                )],
                filter_configuration=gamelift_mixins.CfnGameSessionQueuePropsMixin.FilterConfigurationProperty(
                    allowed_locations=["allowedLocations"]
                ),
                name="name",
                notification_target="notificationTarget",
                player_latency_policies=[gamelift_mixins.CfnGameSessionQueuePropsMixin.PlayerLatencyPolicyProperty(
                    maximum_individual_player_latency_milliseconds=123,
                    policy_duration_seconds=123
                )],
                priority_configuration=gamelift_mixins.CfnGameSessionQueuePropsMixin.PriorityConfigurationProperty(
                    location_order=["locationOrder"],
                    priority_order=["priorityOrder"]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                timeout_in_seconds=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7849f682933af52c4d4b6d348a9f27d8135c547e03c52ac988e371b7ec2f8d2e)
            check_type(argname="argument custom_event_data", value=custom_event_data, expected_type=type_hints["custom_event_data"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument filter_configuration", value=filter_configuration, expected_type=type_hints["filter_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_target", value=notification_target, expected_type=type_hints["notification_target"])
            check_type(argname="argument player_latency_policies", value=player_latency_policies, expected_type=type_hints["player_latency_policies"])
            check_type(argname="argument priority_configuration", value=priority_configuration, expected_type=type_hints["priority_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_event_data is not None:
            self._values["custom_event_data"] = custom_event_data
        if destinations is not None:
            self._values["destinations"] = destinations
        if filter_configuration is not None:
            self._values["filter_configuration"] = filter_configuration
        if name is not None:
            self._values["name"] = name
        if notification_target is not None:
            self._values["notification_target"] = notification_target
        if player_latency_policies is not None:
            self._values["player_latency_policies"] = player_latency_policies
        if priority_configuration is not None:
            self._values["priority_configuration"] = priority_configuration
        if tags is not None:
            self._values["tags"] = tags
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds

    @builtins.property
    def custom_event_data(self) -> typing.Optional[builtins.str]:
        '''Information to be added to all events that are related to this game session queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-customeventdata
        '''
        result = self._values.get("custom_event_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameSessionQueuePropsMixin.DestinationProperty"]]]]:
        '''A list of fleets and/or fleet aliases that can be used to fulfill game session placement requests in the queue.

        Destinations are identified by either a fleet ARN or a fleet alias ARN, and are listed in order of placement preference.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-destinations
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameSessionQueuePropsMixin.DestinationProperty"]]]], result)

    @builtins.property
    def filter_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameSessionQueuePropsMixin.FilterConfigurationProperty"]]:
        '''A list of locations where a queue is allowed to place new game sessions.

        Locations are specified in the form of AWS Region codes, such as ``us-west-2`` . If this parameter is not set, game sessions can be placed in any queue location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-filterconfiguration
        '''
        result = self._values.get("filter_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameSessionQueuePropsMixin.FilterConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A descriptive label that is associated with game session queue.

        Queue names must be unique within each Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_target(self) -> typing.Optional[builtins.str]:
        '''An SNS topic ARN that is set up to receive game session placement notifications.

        See `Setting up notifications for game session placement <https://docs.aws.amazon.com/gamelift/latest/developerguide/queue-notification.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-notificationtarget
        '''
        result = self._values.get("notification_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def player_latency_policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameSessionQueuePropsMixin.PlayerLatencyPolicyProperty"]]]]:
        '''A set of policies that enforce a sliding cap on player latency when processing game sessions placement requests.

        Use multiple policies to gradually relax the cap over time if Amazon GameLift Servers can't make a placement. Policies are evaluated in order starting with the lowest maximum latency value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-playerlatencypolicies
        '''
        result = self._values.get("player_latency_policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameSessionQueuePropsMixin.PlayerLatencyPolicyProperty"]]]], result)

    @builtins.property
    def priority_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameSessionQueuePropsMixin.PriorityConfigurationProperty"]]:
        '''Custom settings to use when prioritizing destinations and locations for game session placements.

        This configuration replaces the FleetIQ default prioritization process. Priority types that are not explicitly named will be automatically applied at the end of the prioritization process.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-priorityconfiguration
        '''
        result = self._values.get("priority_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGameSessionQueuePropsMixin.PriorityConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of labels to assign to the new game session queue resource.

        Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The maximum time, in seconds, that a new game session placement request remains in the queue.

        When a request exceeds this time, the game session placement changes to a ``TIMED_OUT`` status. If you don't specify a request timeout, the queue uses a default value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-timeoutinseconds
        '''
        result = self._values.get("timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGameSessionQueueMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGameSessionQueuePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameSessionQueuePropsMixin",
):
    '''The ``AWS::GameLift::GameSessionQueue`` resource creates a placement queue that processes requests for new game sessions.

    A queue uses FleetIQ algorithms to determine the best placement locations and find an available game server, then prompts the game server to start a new game session. Queues can have destinations (GameLift fleets or aliases), which determine where the queue can place new game sessions. A queue can have destinations with varied fleet type (Spot and On-Demand), instance type, and AWS Region .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html
    :cloudformationResource: AWS::GameLift::GameSessionQueue
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_game_session_queue_props_mixin = gamelift_mixins.CfnGameSessionQueuePropsMixin(gamelift_mixins.CfnGameSessionQueueMixinProps(
            custom_event_data="customEventData",
            destinations=[gamelift_mixins.CfnGameSessionQueuePropsMixin.DestinationProperty(
                destination_arn="destinationArn"
            )],
            filter_configuration=gamelift_mixins.CfnGameSessionQueuePropsMixin.FilterConfigurationProperty(
                allowed_locations=["allowedLocations"]
            ),
            name="name",
            notification_target="notificationTarget",
            player_latency_policies=[gamelift_mixins.CfnGameSessionQueuePropsMixin.PlayerLatencyPolicyProperty(
                maximum_individual_player_latency_milliseconds=123,
                policy_duration_seconds=123
            )],
            priority_configuration=gamelift_mixins.CfnGameSessionQueuePropsMixin.PriorityConfigurationProperty(
                location_order=["locationOrder"],
                priority_order=["priorityOrder"]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            timeout_in_seconds=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGameSessionQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::GameSessionQueue``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6ac9074667b7532b78e3b0ab096339d5113cbd0becb4cbef9ee96c6e04efca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31f03aa871de78cf0de632168d74cd5891b5b8a251aa313c979f8f40b9f16e3f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74491a23ec43cd79f5e94e7c5af058f9ed39cce869753f066a1e60d568aaf695)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGameSessionQueueMixinProps:
        return typing.cast(CfnGameSessionQueueMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameSessionQueuePropsMixin.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn"},
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                destination_property = gamelift_mixins.CfnGameSessionQueuePropsMixin.DestinationProperty(
                    destination_arn="destinationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d374560826f0fb0e8defdb163087029528f8164db6c5e5e0620e267c075fbaf4)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-destination.html#cfn-gamelift-gamesessionqueue-destination-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameSessionQueuePropsMixin.FilterConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"allowed_locations": "allowedLocations"},
    )
    class FilterConfigurationProperty:
        def __init__(
            self,
            *,
            allowed_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A list of fleet locations where a game session queue can place new game sessions.

            You can use a filter to temporarily turn off placements for specific locations. For queues that have multi-location fleets, you can use a filter configuration allow placement with some, but not all of these locations.

            :param allowed_locations: A list of locations to allow game session placement in, in the form of AWS Region codes such as ``us-west-2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-filterconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                filter_configuration_property = gamelift_mixins.CfnGameSessionQueuePropsMixin.FilterConfigurationProperty(
                    allowed_locations=["allowedLocations"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__240e70ba928de8cedab13bf5f16e51e429a3d865f72a0abd486902fc43c20569)
                check_type(argname="argument allowed_locations", value=allowed_locations, expected_type=type_hints["allowed_locations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_locations is not None:
                self._values["allowed_locations"] = allowed_locations

        @builtins.property
        def allowed_locations(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of locations to allow game session placement in, in the form of AWS Region codes such as ``us-west-2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-filterconfiguration.html#cfn-gamelift-gamesessionqueue-filterconfiguration-allowedlocations
            '''
            result = self._values.get("allowed_locations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameSessionQueuePropsMixin.GameSessionQueueDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn"},
    )
    class GameSessionQueueDestinationProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A fleet or alias designated in a game session queue.

            Queues fulfill requests for new game sessions by placing a new game session on any of the queue's destinations.

            :param destination_arn: The Amazon Resource Name (ARN) that is assigned to fleet or fleet alias. ARNs, which include a fleet ID or alias ID and a Region name, provide a unique identifier across all Regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-gamesessionqueuedestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                game_session_queue_destination_property = gamelift_mixins.CfnGameSessionQueuePropsMixin.GameSessionQueueDestinationProperty(
                    destination_arn="destinationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__adba3c4f52c414eb285899ae803f9900d1943781913194cc980dee4f72791345)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that is assigned to fleet or fleet alias.

            ARNs, which include a fleet ID or alias ID and a Region name, provide a unique identifier across all Regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-gamesessionqueuedestination.html#cfn-gamelift-gamesessionqueue-gamesessionqueuedestination-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GameSessionQueueDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameSessionQueuePropsMixin.PlayerLatencyPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_individual_player_latency_milliseconds": "maximumIndividualPlayerLatencyMilliseconds",
            "policy_duration_seconds": "policyDurationSeconds",
        },
    )
    class PlayerLatencyPolicyProperty:
        def __init__(
            self,
            *,
            maximum_individual_player_latency_milliseconds: typing.Optional[jsii.Number] = None,
            policy_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The queue setting that determines the highest latency allowed for individual players when placing a game session.

            When a latency policy is in force, a game session cannot be placed with any fleet in a Region where a player reports latency higher than the cap. Latency policies are only enforced when the placement request contains player latency information.

            :param maximum_individual_player_latency_milliseconds: The maximum latency value that is allowed for any player, in milliseconds. All policies must have a value set for this property.
            :param policy_duration_seconds: The length of time, in seconds, that the policy is enforced while placing a new game session. A null value for this property means that the policy is enforced until the queue times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-playerlatencypolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                player_latency_policy_property = gamelift_mixins.CfnGameSessionQueuePropsMixin.PlayerLatencyPolicyProperty(
                    maximum_individual_player_latency_milliseconds=123,
                    policy_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6b76688239b74a2439f6fe26d1903f374910e33075baac2070a892088763dfb)
                check_type(argname="argument maximum_individual_player_latency_milliseconds", value=maximum_individual_player_latency_milliseconds, expected_type=type_hints["maximum_individual_player_latency_milliseconds"])
                check_type(argname="argument policy_duration_seconds", value=policy_duration_seconds, expected_type=type_hints["policy_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_individual_player_latency_milliseconds is not None:
                self._values["maximum_individual_player_latency_milliseconds"] = maximum_individual_player_latency_milliseconds
            if policy_duration_seconds is not None:
                self._values["policy_duration_seconds"] = policy_duration_seconds

        @builtins.property
        def maximum_individual_player_latency_milliseconds(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The maximum latency value that is allowed for any player, in milliseconds.

            All policies must have a value set for this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-playerlatencypolicy.html#cfn-gamelift-gamesessionqueue-playerlatencypolicy-maximumindividualplayerlatencymilliseconds
            '''
            result = self._values.get("maximum_individual_player_latency_milliseconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def policy_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''The length of time, in seconds, that the policy is enforced while placing a new game session.

            A null value for this property means that the policy is enforced until the queue times out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-playerlatencypolicy.html#cfn-gamelift-gamesessionqueue-playerlatencypolicy-policydurationseconds
            '''
            result = self._values.get("policy_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlayerLatencyPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnGameSessionQueuePropsMixin.PriorityConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "location_order": "locationOrder",
            "priority_order": "priorityOrder",
        },
    )
    class PriorityConfigurationProperty:
        def __init__(
            self,
            *,
            location_order: typing.Optional[typing.Sequence[builtins.str]] = None,
            priority_order: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Custom prioritization settings for use by a game session queue when placing new game sessions with available game servers.

            When defined, this configuration replaces the default FleetIQ prioritization process, which is as follows:

            - If player latency data is included in a game session request, destinations and locations are prioritized first based on lowest average latency (1), then on lowest hosting cost (2), then on destination list order (3), and finally on location (alphabetical) (4). This approach ensures that the queue's top priority is to place game sessions where average player latency is lowest, and--if latency is the same--where the hosting cost is less, etc.
            - If player latency data is not included, destinations and locations are prioritized first on destination list order (1), and then on location (alphabetical) (2). This approach ensures that the queue's top priority is to place game sessions on the first destination fleet listed. If that fleet has multiple locations, the game session is placed on the first location (when listed alphabetically).

            Changing the priority order will affect how game sessions are placed.

            :param location_order: The prioritization order to use for fleet locations, when the ``PriorityOrder`` property includes ``LOCATION`` . Locations can include AWS Region codes (such as ``us-west-2`` ), local zones, and custom locations (for Anywhere fleets). Each location must be listed only once. For details, see `Amazon GameLift Servers service locations. <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-regions.html>`_
            :param priority_order: A custom sequence to use when prioritizing where to place new game sessions. Each priority type is listed once. - ``LATENCY`` -- Amazon GameLift Servers prioritizes locations where the average player latency is lowest. Player latency data is provided in each game session placement request. - ``COST`` -- Amazon GameLift Servers prioritizes queue destinations with the lowest current hosting costs. Cost is evaluated based on the destination's location, instance type, and fleet type (Spot or On-Demand). - ``DESTINATION`` -- Amazon GameLift Servers prioritizes based on the list order of destinations in the queue configuration. - ``LOCATION`` -- Amazon GameLift Servers prioritizes based on the provided order of locations, as defined in ``LocationOrder`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-priorityconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                priority_configuration_property = gamelift_mixins.CfnGameSessionQueuePropsMixin.PriorityConfigurationProperty(
                    location_order=["locationOrder"],
                    priority_order=["priorityOrder"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07673b51c972e9b26ff73e28fe8a39d036b82751f90a3c02a30f9b0b1913ba98)
                check_type(argname="argument location_order", value=location_order, expected_type=type_hints["location_order"])
                check_type(argname="argument priority_order", value=priority_order, expected_type=type_hints["priority_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if location_order is not None:
                self._values["location_order"] = location_order
            if priority_order is not None:
                self._values["priority_order"] = priority_order

        @builtins.property
        def location_order(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The prioritization order to use for fleet locations, when the ``PriorityOrder`` property includes ``LOCATION`` .

            Locations can include AWS Region codes (such as ``us-west-2`` ), local zones, and custom locations (for Anywhere fleets). Each location must be listed only once. For details, see `Amazon GameLift Servers service locations. <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-regions.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-priorityconfiguration.html#cfn-gamelift-gamesessionqueue-priorityconfiguration-locationorder
            '''
            result = self._values.get("location_order")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def priority_order(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A custom sequence to use when prioritizing where to place new game sessions. Each priority type is listed once.

            - ``LATENCY`` -- Amazon GameLift Servers prioritizes locations where the average player latency is lowest. Player latency data is provided in each game session placement request.
            - ``COST`` -- Amazon GameLift Servers prioritizes queue destinations with the lowest current hosting costs. Cost is evaluated based on the destination's location, instance type, and fleet type (Spot or On-Demand).
            - ``DESTINATION`` -- Amazon GameLift Servers prioritizes based on the list order of destinations in the queue configuration.
            - ``LOCATION`` -- Amazon GameLift Servers prioritizes based on the provided order of locations, as defined in ``LocationOrder`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-priorityconfiguration.html#cfn-gamelift-gamesessionqueue-priorityconfiguration-priorityorder
            '''
            result = self._values.get("priority_order")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PriorityConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnLocationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"location_name": "locationName", "tags": "tags"},
)
class CfnLocationMixinProps:
    def __init__(
        self,
        *,
        location_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLocationPropsMixin.

        :param location_name: A descriptive name for the custom location.
        :param tags: A list of labels to assign to the new resource. Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management, and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Rareference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-location.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_location_mixin_props = gamelift_mixins.CfnLocationMixinProps(
                location_name="locationName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf10caf044ace312dabeb01e60055ef4e468de414f0a5e7feaf9991d5781606)
            check_type(argname="argument location_name", value=location_name, expected_type=type_hints["location_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if location_name is not None:
            self._values["location_name"] = location_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def location_name(self) -> typing.Optional[builtins.str]:
        '''A descriptive name for the custom location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-location.html#cfn-gamelift-location-locationname
        '''
        result = self._values.get("location_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of labels to assign to the new resource.

        Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management, and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Rareference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-location.html#cfn-gamelift-location-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLocationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnLocationPropsMixin",
):
    '''The AWS::GameLift::Location resource creates a custom location for use in an Anywhere fleet.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-location.html
    :cloudformationResource: AWS::GameLift::Location
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_location_props_mixin = gamelift_mixins.CfnLocationPropsMixin(gamelift_mixins.CfnLocationMixinProps(
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
        props: typing.Union[CfnLocationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::Location``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954abdc6d6fe0854a81c75fbc9596ae40e9dcdc350fefa04b18688a26ddd2f8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b3c9b81474d248a723b79e2dda9d84e4c42d4299b1a24d1273b17f21c7ecfbc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6537a6a4500d03980abf7c894615eaf270f159dc09d342a07d642d7ae3249409)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLocationMixinProps:
        return typing.cast(CfnLocationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnMatchmakingConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "acceptance_required": "acceptanceRequired",
        "acceptance_timeout_seconds": "acceptanceTimeoutSeconds",
        "additional_player_count": "additionalPlayerCount",
        "backfill_mode": "backfillMode",
        "creation_time": "creationTime",
        "custom_event_data": "customEventData",
        "description": "description",
        "flex_match_mode": "flexMatchMode",
        "game_properties": "gameProperties",
        "game_session_data": "gameSessionData",
        "game_session_queue_arns": "gameSessionQueueArns",
        "name": "name",
        "notification_target": "notificationTarget",
        "request_timeout_seconds": "requestTimeoutSeconds",
        "rule_set_arn": "ruleSetArn",
        "rule_set_name": "ruleSetName",
        "tags": "tags",
    },
)
class CfnMatchmakingConfigurationMixinProps:
    def __init__(
        self,
        *,
        acceptance_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        acceptance_timeout_seconds: typing.Optional[jsii.Number] = None,
        additional_player_count: typing.Optional[jsii.Number] = None,
        backfill_mode: typing.Optional[builtins.str] = None,
        creation_time: typing.Optional[builtins.str] = None,
        custom_event_data: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        flex_match_mode: typing.Optional[builtins.str] = None,
        game_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMatchmakingConfigurationPropsMixin.GamePropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        game_session_data: typing.Optional[builtins.str] = None,
        game_session_queue_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        notification_target: typing.Optional[builtins.str] = None,
        request_timeout_seconds: typing.Optional[jsii.Number] = None,
        rule_set_arn: typing.Optional[builtins.str] = None,
        rule_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMatchmakingConfigurationPropsMixin.

        :param acceptance_required: A flag that determines whether a match that was created with this configuration must be accepted by the matched players. To require acceptance, set to ``TRUE`` . With this option enabled, matchmaking tickets use the status ``REQUIRES_ACCEPTANCE`` to indicate when a completed potential match is waiting for player acceptance.
        :param acceptance_timeout_seconds: The length of time (in seconds) to wait for players to accept a proposed match, if acceptance is required.
        :param additional_player_count: The number of player slots in a match to keep open for future players. For example, if the configuration's rule set specifies a match for a single 12-person team, and the additional player count is set to 2, only 10 players are selected for the match. This parameter is not used if ``FlexMatchMode`` is set to ``STANDALONE`` .
        :param backfill_mode: The method used to backfill game sessions that are created with this matchmaking configuration. Specify ``MANUAL`` when your game manages backfill requests manually or does not use the match backfill feature. Specify ``AUTOMATIC`` to have GameLift create a ``StartMatchBackfill`` request whenever a game session has one or more open slots. Learn more about manual and automatic backfill in `Backfill Existing Games with FlexMatch <https://docs.aws.amazon.com/gamelift/latest/flexmatchguide/match-backfill.html>`_ . Automatic backfill is not available when ``FlexMatchMode`` is set to ``STANDALONE`` .
        :param creation_time: A time stamp indicating when this data object was created. Format is a number expressed in Unix time as milliseconds (for example ``"1469498468.057"`` ).
        :param custom_event_data: Information to add to all events related to the matchmaking configuration.
        :param description: A description for the matchmaking configuration.
        :param flex_match_mode: Indicates whether this matchmaking configuration is being used with Amazon GameLift Servers hosting or as a standalone matchmaking solution. - *STANDALONE* - FlexMatch forms matches and returns match information, including players and team assignments, in a `MatchmakingSucceeded <https://docs.aws.amazon.com/gamelift/latest/flexmatchguide/match-events.html#match-events-matchmakingsucceeded>`_ event. - *WITH_QUEUE* - FlexMatch forms matches and uses the specified Amazon GameLift Servers queue to start a game session for the match.
        :param game_properties: A set of custom properties for a game session, formatted as key-value pairs. These properties are passed to a game server process with a request to start a new game session. See `Start a Game Session <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-sdk-server-api.html#gamelift-sdk-server-startsession>`_ . This parameter is not used if ``FlexMatchMode`` is set to ``STANDALONE`` .
        :param game_session_data: A set of custom game session properties, formatted as a single string value. This data is passed to a game server process with a request to start a new game session. See `Start a Game Session <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-sdk-server-api.html#gamelift-sdk-server-startsession>`_ . This parameter is not used if ``FlexMatchMode`` is set to ``STANDALONE`` .
        :param game_session_queue_arns: The Amazon Resource Name ( `ARN <https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-arn-format.html>`_ ) that is assigned to a Amazon GameLift Servers game session queue resource and uniquely identifies it. ARNs are unique across all Regions. Format is ``arn:aws:gamelift:<region>::gamesessionqueue/<queue name>`` . Queues can be located in any Region. Queues are used to start new Amazon GameLift Servers-hosted game sessions for matches that are created with this matchmaking configuration. If ``FlexMatchMode`` is set to ``STANDALONE`` , do not set this parameter.
        :param name: A unique identifier for the matchmaking configuration. This name is used to identify the configuration associated with a matchmaking request or ticket.
        :param notification_target: An SNS topic ARN that is set up to receive matchmaking notifications. See `Setting up notifications for matchmaking <https://docs.aws.amazon.com/gamelift/latest/flexmatchguide/match-notification.html>`_ for more information.
        :param request_timeout_seconds: The maximum duration, in seconds, that a matchmaking ticket can remain in process before timing out. Requests that fail due to timing out can be resubmitted as needed.
        :param rule_set_arn: The Amazon Resource Name ( `ARN <https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-arn-format.html>`_ ) associated with the GameLift matchmaking rule set resource that this configuration uses.
        :param rule_set_name: A unique identifier for the matchmaking rule set to use with this configuration. You can use either the rule set name or ARN value. A matchmaking configuration can only use rule sets that are defined in the same Region.
        :param tags: A list of labels to assign to the new matchmaking configuration resource. Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_matchmaking_configuration_mixin_props = gamelift_mixins.CfnMatchmakingConfigurationMixinProps(
                acceptance_required=False,
                acceptance_timeout_seconds=123,
                additional_player_count=123,
                backfill_mode="backfillMode",
                creation_time="creationTime",
                custom_event_data="customEventData",
                description="description",
                flex_match_mode="flexMatchMode",
                game_properties=[gamelift_mixins.CfnMatchmakingConfigurationPropsMixin.GamePropertyProperty(
                    key="key",
                    value="value"
                )],
                game_session_data="gameSessionData",
                game_session_queue_arns=["gameSessionQueueArns"],
                name="name",
                notification_target="notificationTarget",
                request_timeout_seconds=123,
                rule_set_arn="ruleSetArn",
                rule_set_name="ruleSetName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cbe0bcda63e362e4b7a8722c0871187902f8437e1c97a33e01eb99f5ccc089)
            check_type(argname="argument acceptance_required", value=acceptance_required, expected_type=type_hints["acceptance_required"])
            check_type(argname="argument acceptance_timeout_seconds", value=acceptance_timeout_seconds, expected_type=type_hints["acceptance_timeout_seconds"])
            check_type(argname="argument additional_player_count", value=additional_player_count, expected_type=type_hints["additional_player_count"])
            check_type(argname="argument backfill_mode", value=backfill_mode, expected_type=type_hints["backfill_mode"])
            check_type(argname="argument creation_time", value=creation_time, expected_type=type_hints["creation_time"])
            check_type(argname="argument custom_event_data", value=custom_event_data, expected_type=type_hints["custom_event_data"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument flex_match_mode", value=flex_match_mode, expected_type=type_hints["flex_match_mode"])
            check_type(argname="argument game_properties", value=game_properties, expected_type=type_hints["game_properties"])
            check_type(argname="argument game_session_data", value=game_session_data, expected_type=type_hints["game_session_data"])
            check_type(argname="argument game_session_queue_arns", value=game_session_queue_arns, expected_type=type_hints["game_session_queue_arns"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_target", value=notification_target, expected_type=type_hints["notification_target"])
            check_type(argname="argument request_timeout_seconds", value=request_timeout_seconds, expected_type=type_hints["request_timeout_seconds"])
            check_type(argname="argument rule_set_arn", value=rule_set_arn, expected_type=type_hints["rule_set_arn"])
            check_type(argname="argument rule_set_name", value=rule_set_name, expected_type=type_hints["rule_set_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acceptance_required is not None:
            self._values["acceptance_required"] = acceptance_required
        if acceptance_timeout_seconds is not None:
            self._values["acceptance_timeout_seconds"] = acceptance_timeout_seconds
        if additional_player_count is not None:
            self._values["additional_player_count"] = additional_player_count
        if backfill_mode is not None:
            self._values["backfill_mode"] = backfill_mode
        if creation_time is not None:
            self._values["creation_time"] = creation_time
        if custom_event_data is not None:
            self._values["custom_event_data"] = custom_event_data
        if description is not None:
            self._values["description"] = description
        if flex_match_mode is not None:
            self._values["flex_match_mode"] = flex_match_mode
        if game_properties is not None:
            self._values["game_properties"] = game_properties
        if game_session_data is not None:
            self._values["game_session_data"] = game_session_data
        if game_session_queue_arns is not None:
            self._values["game_session_queue_arns"] = game_session_queue_arns
        if name is not None:
            self._values["name"] = name
        if notification_target is not None:
            self._values["notification_target"] = notification_target
        if request_timeout_seconds is not None:
            self._values["request_timeout_seconds"] = request_timeout_seconds
        if rule_set_arn is not None:
            self._values["rule_set_arn"] = rule_set_arn
        if rule_set_name is not None:
            self._values["rule_set_name"] = rule_set_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def acceptance_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A flag that determines whether a match that was created with this configuration must be accepted by the matched players.

        To require acceptance, set to ``TRUE`` . With this option enabled, matchmaking tickets use the status ``REQUIRES_ACCEPTANCE`` to indicate when a completed potential match is waiting for player acceptance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-acceptancerequired
        '''
        result = self._values.get("acceptance_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def acceptance_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''The length of time (in seconds) to wait for players to accept a proposed match, if acceptance is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-acceptancetimeoutseconds
        '''
        result = self._values.get("acceptance_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def additional_player_count(self) -> typing.Optional[jsii.Number]:
        '''The number of player slots in a match to keep open for future players.

        For example, if the configuration's rule set specifies a match for a single 12-person team, and the additional player count is set to 2, only 10 players are selected for the match. This parameter is not used if ``FlexMatchMode`` is set to ``STANDALONE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-additionalplayercount
        '''
        result = self._values.get("additional_player_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backfill_mode(self) -> typing.Optional[builtins.str]:
        '''The method used to backfill game sessions that are created with this matchmaking configuration.

        Specify ``MANUAL`` when your game manages backfill requests manually or does not use the match backfill feature. Specify ``AUTOMATIC`` to have GameLift create a ``StartMatchBackfill`` request whenever a game session has one or more open slots. Learn more about manual and automatic backfill in `Backfill Existing Games with FlexMatch <https://docs.aws.amazon.com/gamelift/latest/flexmatchguide/match-backfill.html>`_ . Automatic backfill is not available when ``FlexMatchMode`` is set to ``STANDALONE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-backfillmode
        '''
        result = self._values.get("backfill_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creation_time(self) -> typing.Optional[builtins.str]:
        '''A time stamp indicating when this data object was created.

        Format is a number expressed in Unix time as milliseconds (for example ``"1469498468.057"`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-creationtime
        '''
        result = self._values.get("creation_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_event_data(self) -> typing.Optional[builtins.str]:
        '''Information to add to all events related to the matchmaking configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-customeventdata
        '''
        result = self._values.get("custom_event_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the matchmaking configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flex_match_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates whether this matchmaking configuration is being used with Amazon GameLift Servers hosting or as a standalone matchmaking solution.

        - *STANDALONE* - FlexMatch forms matches and returns match information, including players and team assignments, in a `MatchmakingSucceeded <https://docs.aws.amazon.com/gamelift/latest/flexmatchguide/match-events.html#match-events-matchmakingsucceeded>`_ event.
        - *WITH_QUEUE* - FlexMatch forms matches and uses the specified Amazon GameLift Servers queue to start a game session for the match.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-flexmatchmode
        '''
        result = self._values.get("flex_match_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def game_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchmakingConfigurationPropsMixin.GamePropertyProperty"]]]]:
        '''A set of custom properties for a game session, formatted as key-value pairs.

        These properties are passed to a game server process with a request to start a new game session. See `Start a Game Session <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-sdk-server-api.html#gamelift-sdk-server-startsession>`_ . This parameter is not used if ``FlexMatchMode`` is set to ``STANDALONE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-gameproperties
        '''
        result = self._values.get("game_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMatchmakingConfigurationPropsMixin.GamePropertyProperty"]]]], result)

    @builtins.property
    def game_session_data(self) -> typing.Optional[builtins.str]:
        '''A set of custom game session properties, formatted as a single string value.

        This data is passed to a game server process with a request to start a new game session. See `Start a Game Session <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-sdk-server-api.html#gamelift-sdk-server-startsession>`_ . This parameter is not used if ``FlexMatchMode`` is set to ``STANDALONE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-gamesessiondata
        '''
        result = self._values.get("game_session_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def game_session_queue_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Name ( `ARN <https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-arn-format.html>`_ ) that is assigned to a Amazon GameLift Servers game session queue resource and uniquely identifies it. ARNs are unique across all Regions. Format is ``arn:aws:gamelift:<region>::gamesessionqueue/<queue name>`` . Queues can be located in any Region. Queues are used to start new Amazon GameLift Servers-hosted game sessions for matches that are created with this matchmaking configuration. If ``FlexMatchMode`` is set to ``STANDALONE`` , do not set this parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-gamesessionqueuearns
        '''
        result = self._values.get("game_session_queue_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the matchmaking configuration.

        This name is used to identify the configuration associated with a matchmaking request or ticket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_target(self) -> typing.Optional[builtins.str]:
        '''An SNS topic ARN that is set up to receive matchmaking notifications.

        See `Setting up notifications for matchmaking <https://docs.aws.amazon.com/gamelift/latest/flexmatchguide/match-notification.html>`_ for more information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-notificationtarget
        '''
        result = self._values.get("notification_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''The maximum duration, in seconds, that a matchmaking ticket can remain in process before timing out.

        Requests that fail due to timing out can be resubmitted as needed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-requesttimeoutseconds
        '''
        result = self._values.get("request_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_set_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name ( `ARN <https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-arn-format.html>`_ ) associated with the GameLift matchmaking rule set resource that this configuration uses.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-rulesetarn
        '''
        result = self._values.get("rule_set_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_set_name(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the matchmaking rule set to use with this configuration.

        You can use either the rule set name or ARN value. A matchmaking configuration can only use rule sets that are defined in the same Region.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-rulesetname
        '''
        result = self._values.get("rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of labels to assign to the new matchmaking configuration resource.

        Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMatchmakingConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMatchmakingConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnMatchmakingConfigurationPropsMixin",
):
    '''The ``AWS::GameLift::MatchmakingConfiguration`` resource defines a new matchmaking configuration for use with FlexMatch.

    Whether you're using FlexMatch with GameLift hosting or as a standalone matchmaking service, the matchmaking configuration sets out rules for matching players and forming teams. If you're using GameLift hosting, it also defines how to start game sessions for each match. Your matchmaking system can use multiple configurations to handle different game scenarios. All matchmaking requests identify the matchmaking configuration to use and provide player attributes that are consistent with that configuration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html
    :cloudformationResource: AWS::GameLift::MatchmakingConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_matchmaking_configuration_props_mixin = gamelift_mixins.CfnMatchmakingConfigurationPropsMixin(gamelift_mixins.CfnMatchmakingConfigurationMixinProps(
            acceptance_required=False,
            acceptance_timeout_seconds=123,
            additional_player_count=123,
            backfill_mode="backfillMode",
            creation_time="creationTime",
            custom_event_data="customEventData",
            description="description",
            flex_match_mode="flexMatchMode",
            game_properties=[gamelift_mixins.CfnMatchmakingConfigurationPropsMixin.GamePropertyProperty(
                key="key",
                value="value"
            )],
            game_session_data="gameSessionData",
            game_session_queue_arns=["gameSessionQueueArns"],
            name="name",
            notification_target="notificationTarget",
            request_timeout_seconds=123,
            rule_set_arn="ruleSetArn",
            rule_set_name="ruleSetName",
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
        props: typing.Union[CfnMatchmakingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::MatchmakingConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58a2b713398405d66edc8e6ac89f6be5a8b79d3a71d8fc8c7f85de623fd49bef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f3fb05c8d3fe026bf270a4aa0879268fcac3e16b167e3db1d0771eb5f88eb57)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d650cf48ad8eeefa73dc8b21c74048b75b4889330d98b64da08478c8958e28)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMatchmakingConfigurationMixinProps:
        return typing.cast(CfnMatchmakingConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnMatchmakingConfigurationPropsMixin.GamePropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class GamePropertyProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This key-value pair can store custom data about a game session.

            For example, you might use a ``GameProperty`` to track a game session's map, level of difficulty, or remaining time. The difficulty level could be specified like this: ``{"Key": "difficulty", "Value":"Novice"}`` .

            You can set game properties when creating a game session. You can also modify game properties of an active game session. When searching for game sessions, you can filter on game property keys and values. You can't delete game properties from a game session.

            For examples of working with game properties, see `Create a game session with properties <https://docs.aws.amazon.com/gamelift/latest/developerguide/gamelift-sdk-client-api.html#game-properties>`_ .

            :param key: The game property identifier.
            :param value: The game property value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-matchmakingconfiguration-gameproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                game_property_property = gamelift_mixins.CfnMatchmakingConfigurationPropsMixin.GamePropertyProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5135c214a018f2d5e16611ec082e4cd32d4429eab77fdabff29f6316ba5f5c06)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The game property identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-matchmakingconfiguration-gameproperty.html#cfn-gamelift-matchmakingconfiguration-gameproperty-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The game property value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-matchmakingconfiguration-gameproperty.html#cfn-gamelift-matchmakingconfiguration-gameproperty-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GamePropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnMatchmakingRuleSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "rule_set_body": "ruleSetBody", "tags": "tags"},
)
class CfnMatchmakingRuleSetMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        rule_set_body: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMatchmakingRuleSetPropsMixin.

        :param name: A unique identifier for the matchmaking rule set. A matchmaking configuration identifies the rule set it uses by this name value. Note that the rule set name is different from the optional ``name`` field in the rule set body.
        :param rule_set_body: A collection of matchmaking rules, formatted as a JSON string. Comments are not allowed in JSON, but most elements support a description field.
        :param tags: A list of labels to assign to the new matchmaking rule set resource. Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_matchmaking_rule_set_mixin_props = gamelift_mixins.CfnMatchmakingRuleSetMixinProps(
                name="name",
                rule_set_body="ruleSetBody",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d507e37812f2dcf0ad4191d5a47d1a66343afdc09ea113e076b60bf9275a3fdf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule_set_body", value=rule_set_body, expected_type=type_hints["rule_set_body"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if rule_set_body is not None:
            self._values["rule_set_body"] = rule_set_body
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the matchmaking rule set.

        A matchmaking configuration identifies the rule set it uses by this name value. Note that the rule set name is different from the optional ``name`` field in the rule set body.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html#cfn-gamelift-matchmakingruleset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_set_body(self) -> typing.Optional[builtins.str]:
        '''A collection of matchmaking rules, formatted as a JSON string.

        Comments are not allowed in JSON, but most elements support a description field.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html#cfn-gamelift-matchmakingruleset-rulesetbody
        '''
        result = self._values.get("rule_set_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of labels to assign to the new matchmaking rule set resource.

        Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html#cfn-gamelift-matchmakingruleset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMatchmakingRuleSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMatchmakingRuleSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnMatchmakingRuleSetPropsMixin",
):
    '''Creates a new rule set for FlexMatch matchmaking.

    A rule set describes the type of match to create, such as the number and size of teams. It also sets the parameters for acceptable player matches, such as minimum skill level or character type.

    To create a matchmaking rule set, provide unique rule set name and the rule set body in JSON format. Rule sets must be defined in the same Region as the matchmaking configuration they are used with.

    Since matchmaking rule sets cannot be edited, it is a good idea to check the rule set syntax.

    *Learn more*

    - `Build a rule set <https://docs.aws.amazon.com/gamelift/latest/flexmatchguide/match-rulesets.html>`_
    - `Design a matchmaker <https://docs.aws.amazon.com/gamelift/latest/flexmatchguide/match-configuration.html>`_
    - `Matchmaking with FlexMatch <https://docs.aws.amazon.com/gamelift/latest/flexmatchguide/match-intro.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html
    :cloudformationResource: AWS::GameLift::MatchmakingRuleSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_matchmaking_rule_set_props_mixin = gamelift_mixins.CfnMatchmakingRuleSetPropsMixin(gamelift_mixins.CfnMatchmakingRuleSetMixinProps(
            name="name",
            rule_set_body="ruleSetBody",
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
        props: typing.Union[CfnMatchmakingRuleSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::MatchmakingRuleSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3568ea1673d87c73eb89f4a034bf8ee325c3a6d7a15b7b5ee0753ca4f9ea5bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb894cd61a250e692c448b8fca46a4acf2648c052598fb2b8b3dd208b81fe4be)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a63655685328191d4b23b4cedc3b64305301273f671fac241073a67112cdaf75)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMatchmakingRuleSetMixinProps:
        return typing.cast(CfnMatchmakingRuleSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnScriptMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "storage_location": "storageLocation",
        "tags": "tags",
        "version": "version",
    },
)
class CfnScriptMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        storage_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnScriptPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnScriptPropsMixin.

        :param name: A descriptive label that is associated with a script. Script names do not need to be unique.
        :param storage_location: The location of the Amazon S3 bucket where a zipped file containing your Realtime scripts is stored. The storage location must specify the Amazon S3 bucket name, the zip file name (the "key"), and a role ARN that allows Amazon GameLift Servers to access the Amazon S3 storage location. The S3 bucket must be in the same Region where you want to create a new script. By default, Amazon GameLift Servers uploads the latest version of the zip file; if you have S3 object versioning turned on, you can use the ``ObjectVersion`` parameter to specify an earlier version.
        :param tags: A list of labels to assign to the new script resource. Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.
        :param version: The version that is associated with a build or script. Version strings do not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
            
            cfn_script_mixin_props = gamelift_mixins.CfnScriptMixinProps(
                name="name",
                storage_location=gamelift_mixins.CfnScriptPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    object_version="objectVersion",
                    role_arn="roleArn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                version="version"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb73e09c6e581245786661f6fafb425c1840d08f04944864b46f3f78a5a22c64)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument storage_location", value=storage_location, expected_type=type_hints["storage_location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if storage_location is not None:
            self._values["storage_location"] = storage_location
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A descriptive label that is associated with a script.

        Script names do not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScriptPropsMixin.S3LocationProperty"]]:
        '''The location of the Amazon S3 bucket where a zipped file containing your Realtime scripts is stored.

        The storage location must specify the Amazon S3 bucket name, the zip file name (the "key"), and a role ARN that allows Amazon GameLift Servers to access the Amazon S3 storage location. The S3 bucket must be in the same Region where you want to create a new script. By default, Amazon GameLift Servers uploads the latest version of the zip file; if you have S3 object versioning turned on, you can use the ``ObjectVersion`` parameter to specify an earlier version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-storagelocation
        '''
        result = self._values.get("storage_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnScriptPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of labels to assign to the new script resource.

        Tags are developer-defined key-value pairs. Tagging AWS resources are useful for resource management, access management and cost allocation. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in the *AWS General Reference* . Once the resource is created, you can use TagResource, UntagResource, and ListTagsForResource to add, remove, and view tags. The maximum tag limit may be lower than stated. See the AWS General Reference for actual tagging limits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The version that is associated with a build or script.

        Version strings do not need to be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScriptMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScriptPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnScriptPropsMixin",
):
    '''The ``AWS::GameLift::Script`` resource creates a new script record for your Realtime Servers script.

    Realtime scripts are JavaScript that provide configuration settings and optional custom game logic for your game. The script is deployed when you create a Realtime Servers fleet to host your game sessions. Script logic is executed during an active game session.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html
    :cloudformationResource: AWS::GameLift::Script
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
        
        cfn_script_props_mixin = gamelift_mixins.CfnScriptPropsMixin(gamelift_mixins.CfnScriptMixinProps(
            name="name",
            storage_location=gamelift_mixins.CfnScriptPropsMixin.S3LocationProperty(
                bucket="bucket",
                key="key",
                object_version="objectVersion",
                role_arn="roleArn"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            version="version"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnScriptMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GameLift::Script``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7233c00102fad87df5383d3c7b15a1466f821578d540dad6ed2aad446108a4a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc6306766dc9684cecaf8c1f988923b594fb6d42430faa638eb24b7ba4c171f6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ebb719f3ce8ccff5a2720cc2995703f0bbb1f5afa5aae941a13dbfe9583fbd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScriptMixinProps:
        return typing.cast(CfnScriptMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_gamelift.mixins.CfnScriptPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "object_version": "objectVersion",
            "role_arn": "roleArn",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            object_version: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location in Amazon S3 where build or script files can be stored for access by Amazon GameLift.

            :param bucket: An Amazon S3 bucket identifier. Thename of the S3 bucket. .. epigraph:: Amazon GameLift Servers doesn't support uploading from Amazon S3 buckets with names that contain a dot (.).
            :param key: The name of the zip file that contains the build files or script files.
            :param object_version: The version of the file, if object versioning is turned on for the bucket. Amazon GameLift Servers uses this information when retrieving files from an S3 bucket that you own. Use this parameter to specify a specific version of the file. If not set, the latest version of the file is retrieved.
            :param role_arn: The Amazon Resource Name ( `ARN <https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-arn-format.html>`_ ) for an IAM role that allows Amazon GameLift Servers to access the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_gamelift import mixins as gamelift_mixins
                
                s3_location_property = gamelift_mixins.CfnScriptPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    key="key",
                    object_version="objectVersion",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__125e565ede247d67ab5176270cda508027580376c813f6df3ad78675751aa760)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument object_version", value=object_version, expected_type=type_hints["object_version"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if object_version is not None:
                self._values["object_version"] = object_version
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''An Amazon S3 bucket identifier. Thename of the S3 bucket.

            .. epigraph::

               Amazon GameLift Servers doesn't support uploading from Amazon S3 buckets with names that contain a dot (.).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html#cfn-gamelift-script-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the zip file that contains the build files or script files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html#cfn-gamelift-script-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            '''The version of the file, if object versioning is turned on for the bucket.

            Amazon GameLift Servers uses this information when retrieving files from an S3 bucket that you own. Use this parameter to specify a specific version of the file. If not set, the latest version of the file is retrieved.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html#cfn-gamelift-script-s3location-objectversion
            '''
            result = self._values.get("object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name ( `ARN <https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-arn-format.html>`_ ) for an IAM role that allows Amazon GameLift Servers to access the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html#cfn-gamelift-script-s3location-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAliasMixinProps",
    "CfnAliasPropsMixin",
    "CfnBuildMixinProps",
    "CfnBuildPropsMixin",
    "CfnContainerFleetMixinProps",
    "CfnContainerFleetPropsMixin",
    "CfnContainerGroupDefinitionMixinProps",
    "CfnContainerGroupDefinitionPropsMixin",
    "CfnFleetMixinProps",
    "CfnFleetPropsMixin",
    "CfnGameServerGroupMixinProps",
    "CfnGameServerGroupPropsMixin",
    "CfnGameSessionQueueMixinProps",
    "CfnGameSessionQueuePropsMixin",
    "CfnLocationMixinProps",
    "CfnLocationPropsMixin",
    "CfnMatchmakingConfigurationMixinProps",
    "CfnMatchmakingConfigurationPropsMixin",
    "CfnMatchmakingRuleSetMixinProps",
    "CfnMatchmakingRuleSetPropsMixin",
    "CfnScriptMixinProps",
    "CfnScriptPropsMixin",
]

publication.publish()

def _typecheckingstub__91450d50d611e1f2b22f07f6fffee9b049401ae231a89cfe5cca1ce3c995b0c0(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    routing_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAliasPropsMixin.RoutingStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f846d0d7ed60a4d1fddbe532365aa9f9564e8ac0b681b8c5f0ddc8363cced5ae(
    props: typing.Union[CfnAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76fb307ef66a4c7076b310eb08f2061797826790e90018f384d0cff4bfe503e1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8a556e0a7e39845542e9f03c741a0044d37373dfa09a31ab29a7abb6375ed9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c394fc75b932a2f06b895412190eb02ac72ec9e2da878bc628a43466e931be10(
    *,
    fleet_id: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcf26e7d75b41888220c5ea4c44921788a309cf35a0c40281b3cb7198a7e404(
    *,
    name: typing.Optional[builtins.str] = None,
    operating_system: typing.Optional[builtins.str] = None,
    server_sdk_version: typing.Optional[builtins.str] = None,
    storage_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBuildPropsMixin.StorageLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a40ac46e58397d424fef96f7e29ed6065816bfb67548dc067fd2a65e5e618f6(
    props: typing.Union[CfnBuildMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a88be5b614ed0c8069bea87fce9af8d1239e5e045e9d5873178283d2306e026(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5d128189860d88dea5a6207dad91f10a817f457844f0152cf495148d430753(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe6320fe06a44a35467d6e086bd85566645ca91f13f15c01ff9ae02ff8378ad(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    object_version: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0160f048a2c427fcdaca1b76c7bbb31d8358fa0211340651f1649327b55143c1(
    *,
    billing_type: typing.Optional[builtins.str] = None,
    deployment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerFleetPropsMixin.DeploymentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    fleet_role_arn: typing.Optional[builtins.str] = None,
    game_server_container_group_definition_name: typing.Optional[builtins.str] = None,
    game_server_container_groups_per_instance: typing.Optional[jsii.Number] = None,
    game_session_creation_limit_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerFleetPropsMixin.GameSessionCreationLimitPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_connection_port_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerFleetPropsMixin.ConnectionPortRangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_inbound_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerFleetPropsMixin.IpPermissionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerFleetPropsMixin.LocationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerFleetPropsMixin.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metric_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    new_game_session_protection_policy: typing.Optional[builtins.str] = None,
    per_instance_container_group_definition_name: typing.Optional[builtins.str] = None,
    scaling_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerFleetPropsMixin.ScalingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865cd7025104b5b6a8c79841c7b53a080512b42a4816a268382ed993060179e2(
    props: typing.Union[CfnContainerFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a094601ae7a2cf1f2ad8b395c0c7ef602cbd8cd7bb09c4f46c9de8e800e196(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e784e4f53653e230c04441f47693e546c819033be894b4cf966c5b67bf962b52(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78bd1c76b2ea1eb156e82e67ab9d1a425c0fd40e9bf51afb43b431bb29de780e(
    *,
    from_port: typing.Optional[jsii.Number] = None,
    to_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bd90e576ee23bcbb2c3e3b3133914729ad9f2a6c5496fd950bb5c30f8a7bca(
    *,
    impairment_strategy: typing.Optional[builtins.str] = None,
    minimum_healthy_percentage: typing.Optional[jsii.Number] = None,
    protection_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460bd0751f93015f004b51bcccae652b2dc928ac07ac922ec4d17589659bf0a9(
    *,
    latest_deployment_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718011e55fcc9480872cc9e20af0c614288873586273958c7e4cb802ed3bf339(
    *,
    new_game_sessions_per_creator: typing.Optional[jsii.Number] = None,
    policy_period_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0745f27d2db98b383642bbc81eadced14044caf456ad25e6316ab8e74b7c8de2(
    *,
    from_port: typing.Optional[jsii.Number] = None,
    ip_range: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    to_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095e46f30e28a6aa1af3171ee420ac4bf29cbaf5c20516bd4f9ce656b2d64ea6(
    *,
    desired_ec2_instances: typing.Optional[jsii.Number] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2dc46f078bd9bf4a94109f7130800dc9095d2fee829f4bd4b7cbb21c2bf1eee(
    *,
    location: typing.Optional[builtins.str] = None,
    location_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerFleetPropsMixin.LocationCapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stopped_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343c7a19e92e065d3d2a3f44ff609d3ab378adef3c498013bab4a659e67dd2af(
    *,
    log_destination: typing.Optional[builtins.str] = None,
    log_group_arn: typing.Optional[builtins.str] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63a4d8b9482488dabe8dd8072c7e3d78fddd9985ea3e1f10cb9ca80ce58b62b(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    metric_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
    scaling_adjustment: typing.Optional[jsii.Number] = None,
    scaling_adjustment_type: typing.Optional[builtins.str] = None,
    target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerFleetPropsMixin.TargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33dd30c51d7e2f526bdc1b2e98bbe27b76233551efe9ac250dd16488d5851024(
    *,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a35eb32d22f0e925d0cb226e23c0a6539c8f43017917db7508de7a80610a75(
    *,
    container_group_type: typing.Optional[builtins.str] = None,
    game_server_container_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.GameServerContainerDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    operating_system: typing.Optional[builtins.str] = None,
    source_version_number: typing.Optional[jsii.Number] = None,
    support_container_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.SupportContainerDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    total_memory_limit_mebibytes: typing.Optional[jsii.Number] = None,
    total_vcpu_limit: typing.Optional[jsii.Number] = None,
    version_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf1d2f7d79c08dc598e10352eeed50c2ea1ff41003e44786c008e1c454dafc8(
    props: typing.Union[CfnContainerGroupDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a2efae64cd9790582184d2cba9a66f60a6a84a63b96364f27ce09b7a84d47d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749c680059ce24f7babecaad07614f8decf04b0445e71cf5d8130f99a5cf7e14(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d3ca2a3305364f5eb068f233c995a7bd218639848f125a57a4307e5e1168ac(
    *,
    condition: typing.Optional[builtins.str] = None,
    container_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553c5176d1d6922da5395ad7f47b3590f2e0aa9625a100de27c24b2e8ef4bf7c(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f386832e8b9ef268f5af36107df2d70cc755dcc2c02fcca12801cf9e4da04c(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    interval: typing.Optional[jsii.Number] = None,
    retries: typing.Optional[jsii.Number] = None,
    start_period: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2198c218d347b478d50031ef2c06d9527ece48e768bc850117aa5f26b486b89c(
    *,
    access_level: typing.Optional[builtins.str] = None,
    container_path: typing.Optional[builtins.str] = None,
    instance_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031b98314d098a0da56eabdc02c9707db046e38c4c7bbba91e94b7fd2a2cc37e(
    *,
    from_port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    to_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c706d3ce0d959f9b6ae51cd8783eb941c2fc6dde096fd98c74c030892f3e2e35(
    *,
    container_name: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    environment_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    mount_points: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    port_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resolved_image_digest: typing.Optional[builtins.str] = None,
    server_sdk_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12db5eed490dc850420ee078541a56f811a0b750174b27f9071cfb4b54ef70a(
    *,
    container_port_ranges: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.ContainerPortRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e16b343652b34e3941b00974ccb5f8bbbadf839fa56d422c440ddfeccb1941c(
    *,
    container_name: typing.Optional[builtins.str] = None,
    depends_on: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.ContainerDependencyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    environment_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.ContainerEnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    essential: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.ContainerHealthCheckProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_uri: typing.Optional[builtins.str] = None,
    memory_hard_limit_mebibytes: typing.Optional[jsii.Number] = None,
    mount_points: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.ContainerMountPointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    port_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerGroupDefinitionPropsMixin.PortConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resolved_image_digest: typing.Optional[builtins.str] = None,
    vcpu: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d98948d00934efa740094800752932e1a366fa298a66d2ef63cb3a3d0cd6ae3(
    *,
    anywhere_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.AnywhereConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    apply_capacity: typing.Optional[builtins.str] = None,
    build_id: typing.Optional[builtins.str] = None,
    certificate_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.CertificateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    compute_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    desired_ec2_instances: typing.Optional[jsii.Number] = None,
    ec2_inbound_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.IpPermissionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_instance_type: typing.Optional[builtins.str] = None,
    fleet_type: typing.Optional[builtins.str] = None,
    instance_role_arn: typing.Optional[builtins.str] = None,
    instance_role_credentials_provider: typing.Optional[builtins.str] = None,
    locations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.LocationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    log_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_size: typing.Optional[jsii.Number] = None,
    metric_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    min_size: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    new_game_session_protection_policy: typing.Optional[builtins.str] = None,
    peer_vpc_aws_account_id: typing.Optional[builtins.str] = None,
    peer_vpc_id: typing.Optional[builtins.str] = None,
    resource_creation_limit_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ResourceCreationLimitPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    runtime_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.RuntimeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scaling_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ScalingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    script_id: typing.Optional[builtins.str] = None,
    server_launch_parameters: typing.Optional[builtins.str] = None,
    server_launch_path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7f7e884acdd9c27d4db10533f6a90b52632b6661a4e7766e72c909d2147582(
    props: typing.Union[CfnFleetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbc952e33e5cb60ef169aa016bddb056a872f6c1f1e9edb39742bf3c6268953(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783788d78930f86a7f4bbab21f7786133142dd8b9cf12f4c1a372dbd2b06d9d8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3da749dd6288aa86e70677fcd2cf302e678369a8d37cc7f54d79f48414fe9d(
    *,
    cost: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89f5c2bf840b272b96f988c45243eb8112fb7def70773ec8e0b4e90a2cd6fb5(
    *,
    certificate_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e386586abb4109e222af5aa3e2a7e4dc0e27ff97a51832dd07fff3935f33d88(
    *,
    from_port: typing.Optional[jsii.Number] = None,
    ip_range: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    to_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95348d5cfaacd4e5d2b106fb874f56d5eed8f213c5fbaf56b73fe9b79209dee8(
    *,
    desired_ec2_instances: typing.Optional[jsii.Number] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c64a833baad7070389c39b43af363e72de9e6ec03ce82d9734f3cd96854e1a(
    *,
    location: typing.Optional[builtins.str] = None,
    location_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.LocationCapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34cc098a96f554471f33ec98799068914a9800d47b4602d15e91e09c84f8eaa(
    *,
    new_game_sessions_per_creator: typing.Optional[jsii.Number] = None,
    policy_period_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c48bd572e7f66e8b617e9db95dc4f0594734c9c7cf545338fe86b43ee8d408(
    *,
    game_session_activation_timeout_seconds: typing.Optional[jsii.Number] = None,
    max_concurrent_game_session_activations: typing.Optional[jsii.Number] = None,
    server_processes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.ServerProcessProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569f9bb9a234e7c322fc63a1fdef706d93ebc57d60466540b96f1ed79f33a1c6(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    location: typing.Optional[builtins.str] = None,
    metric_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
    scaling_adjustment: typing.Optional[jsii.Number] = None,
    scaling_adjustment_type: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFleetPropsMixin.TargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    threshold: typing.Optional[jsii.Number] = None,
    update_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c0ce09074cc7894a2e59d4ea6f069786205c80e0f6cb2d6b91b59d7b606cbf(
    *,
    concurrent_executions: typing.Optional[jsii.Number] = None,
    launch_path: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a0ac463568f437d743c7a282c74f8a87f66f966c533cf91c305104e906d4aa(
    *,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3375602a7736273e52043459b36956cc27c340327eea23088a4daa8dd223e4a8(
    *,
    auto_scaling_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGameServerGroupPropsMixin.AutoScalingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    balancing_strategy: typing.Optional[builtins.str] = None,
    delete_option: typing.Optional[builtins.str] = None,
    game_server_group_name: typing.Optional[builtins.str] = None,
    game_server_protection_policy: typing.Optional[builtins.str] = None,
    instance_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGameServerGroupPropsMixin.InstanceDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGameServerGroupPropsMixin.LaunchTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8c0f00d8c86d543bfadf529b058010002513e67d6d58ab28ec60181bfc3e23(
    props: typing.Union[CfnGameServerGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8bc467cd8b3f1af2a2ce7054718e93a0ab4f4792d8c24728c75f3c050ebaf4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e0f1d9c9c89541d488665ee3e2ae098632489d8e207cd95390050442786f7f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1e902451654b3058cc5380e12b07e9cfbc3feaabc3fb2ab36b3909b0fc52f1(
    *,
    estimated_instance_warmup: typing.Optional[jsii.Number] = None,
    target_tracking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGameServerGroupPropsMixin.TargetTrackingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633faa659aa47c301aa973f55865f2eef79a6c97ea07cd0e2c0e86376c69260b(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    weighted_capacity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21a0ad8b86d60f198ef2ea55ed0e63fb9c11da3a9de2bdb2a11bf3d92c496ec(
    *,
    launch_template_id: typing.Optional[builtins.str] = None,
    launch_template_name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5dd0cdc03286f3cc2b8df9b3026eaff1265d71d3256e2ffb7fc0db3e43214fc(
    *,
    target_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7849f682933af52c4d4b6d348a9f27d8135c547e03c52ac988e371b7ec2f8d2e(
    *,
    custom_event_data: typing.Optional[builtins.str] = None,
    destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGameSessionQueuePropsMixin.DestinationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGameSessionQueuePropsMixin.FilterConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    notification_target: typing.Optional[builtins.str] = None,
    player_latency_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGameSessionQueuePropsMixin.PlayerLatencyPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    priority_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGameSessionQueuePropsMixin.PriorityConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6ac9074667b7532b78e3b0ab096339d5113cbd0becb4cbef9ee96c6e04efca(
    props: typing.Union[CfnGameSessionQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f03aa871de78cf0de632168d74cd5891b5b8a251aa313c979f8f40b9f16e3f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74491a23ec43cd79f5e94e7c5af058f9ed39cce869753f066a1e60d568aaf695(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d374560826f0fb0e8defdb163087029528f8164db6c5e5e0620e267c075fbaf4(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240e70ba928de8cedab13bf5f16e51e429a3d865f72a0abd486902fc43c20569(
    *,
    allowed_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adba3c4f52c414eb285899ae803f9900d1943781913194cc980dee4f72791345(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b76688239b74a2439f6fe26d1903f374910e33075baac2070a892088763dfb(
    *,
    maximum_individual_player_latency_milliseconds: typing.Optional[jsii.Number] = None,
    policy_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07673b51c972e9b26ff73e28fe8a39d036b82751f90a3c02a30f9b0b1913ba98(
    *,
    location_order: typing.Optional[typing.Sequence[builtins.str]] = None,
    priority_order: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf10caf044ace312dabeb01e60055ef4e468de414f0a5e7feaf9991d5781606(
    *,
    location_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954abdc6d6fe0854a81c75fbc9596ae40e9dcdc350fefa04b18688a26ddd2f8f(
    props: typing.Union[CfnLocationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3c9b81474d248a723b79e2dda9d84e4c42d4299b1a24d1273b17f21c7ecfbc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6537a6a4500d03980abf7c894615eaf270f159dc09d342a07d642d7ae3249409(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cbe0bcda63e362e4b7a8722c0871187902f8437e1c97a33e01eb99f5ccc089(
    *,
    acceptance_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    acceptance_timeout_seconds: typing.Optional[jsii.Number] = None,
    additional_player_count: typing.Optional[jsii.Number] = None,
    backfill_mode: typing.Optional[builtins.str] = None,
    creation_time: typing.Optional[builtins.str] = None,
    custom_event_data: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    flex_match_mode: typing.Optional[builtins.str] = None,
    game_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMatchmakingConfigurationPropsMixin.GamePropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    game_session_data: typing.Optional[builtins.str] = None,
    game_session_queue_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    notification_target: typing.Optional[builtins.str] = None,
    request_timeout_seconds: typing.Optional[jsii.Number] = None,
    rule_set_arn: typing.Optional[builtins.str] = None,
    rule_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a2b713398405d66edc8e6ac89f6be5a8b79d3a71d8fc8c7f85de623fd49bef(
    props: typing.Union[CfnMatchmakingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3fb05c8d3fe026bf270a4aa0879268fcac3e16b167e3db1d0771eb5f88eb57(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d650cf48ad8eeefa73dc8b21c74048b75b4889330d98b64da08478c8958e28(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5135c214a018f2d5e16611ec082e4cd32d4429eab77fdabff29f6316ba5f5c06(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d507e37812f2dcf0ad4191d5a47d1a66343afdc09ea113e076b60bf9275a3fdf(
    *,
    name: typing.Optional[builtins.str] = None,
    rule_set_body: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3568ea1673d87c73eb89f4a034bf8ee325c3a6d7a15b7b5ee0753ca4f9ea5bf(
    props: typing.Union[CfnMatchmakingRuleSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb894cd61a250e692c448b8fca46a4acf2648c052598fb2b8b3dd208b81fe4be(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63655685328191d4b23b4cedc3b64305301273f671fac241073a67112cdaf75(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb73e09c6e581245786661f6fafb425c1840d08f04944864b46f3f78a5a22c64(
    *,
    name: typing.Optional[builtins.str] = None,
    storage_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnScriptPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7233c00102fad87df5383d3c7b15a1466f821578d540dad6ed2aad446108a4a(
    props: typing.Union[CfnScriptMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6306766dc9684cecaf8c1f988923b594fb6d42430faa638eb24b7ba4c171f6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ebb719f3ce8ccff5a2720cc2995703f0bbb1f5afa5aae941a13dbfe9583fbd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125e565ede247d67ab5176270cda508027580376c813f6df3ad78675751aa760(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    object_version: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
