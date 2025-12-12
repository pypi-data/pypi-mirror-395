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
    jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnDiscovererMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cross_account": "crossAccount",
        "description": "description",
        "source_arn": "sourceArn",
        "tags": "tags",
    },
)
class CfnDiscovererMixinProps:
    def __init__(
        self,
        *,
        cross_account: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        source_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnDiscovererPropsMixin.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDiscovererPropsMixin.

        :param cross_account: Allows for the discovery of the event schemas that are sent to the event bus from another account. Default: - true
        :param description: A description for the discoverer.
        :param source_arn: The ARN of the event bus.
        :param tags: Tags associated with the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
            
            cfn_discoverer_mixin_props = eventschemas_mixins.CfnDiscovererMixinProps(
                cross_account=False,
                description="description",
                source_arn="sourceArn",
                tags=[eventschemas_mixins.CfnDiscovererPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd3653e10aa73d2687d123bc8f84213de82576ad5e2f8658487eddc61349b6c)
            check_type(argname="argument cross_account", value=cross_account, expected_type=type_hints["cross_account"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cross_account is not None:
            self._values["cross_account"] = cross_account
        if description is not None:
            self._values["description"] = description
        if source_arn is not None:
            self._values["source_arn"] = source_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cross_account(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Allows for the discovery of the event schemas that are sent to the event bus from another account.

        :default: - true

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-crossaccount
        '''
        result = self._values.get("cross_account")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the discoverer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the event bus.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-sourcearn
        '''
        result = self._values.get("source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnDiscovererPropsMixin.TagsEntryProperty"]]:
        '''Tags associated with the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnDiscovererPropsMixin.TagsEntryProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDiscovererMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDiscovererPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnDiscovererPropsMixin",
):
    '''Use the ``AWS::EventSchemas::Discoverer`` resource to specify a *discoverer* that is associated with an event bus.

    A discoverer allows the Amazon EventBridge Schema Registry to automatically generate schemas based on events on an event bus.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html
    :cloudformationResource: AWS::EventSchemas::Discoverer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
        
        cfn_discoverer_props_mixin = eventschemas_mixins.CfnDiscovererPropsMixin(eventschemas_mixins.CfnDiscovererMixinProps(
            cross_account=False,
            description="description",
            source_arn="sourceArn",
            tags=[eventschemas_mixins.CfnDiscovererPropsMixin.TagsEntryProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDiscovererMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EventSchemas::Discoverer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24a592f5bd628e63da502cf57bd14923930f6769a9d4a7bfb93592b7fa28511)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89f2f6ade8772a6a7d17d6df51da3924350e687a8d9058ebb582742b38900d01)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63fa6390eae5d491bc984f4656d70e86c0a0fb873b6f8a62e90c8f813999597)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDiscovererMixinProps:
        return typing.cast(CfnDiscovererMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnDiscovererPropsMixin.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Tags to associate with the discoverer.

            :param key: The key of a key-value pair.
            :param value: The value of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-discoverer-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
                
                tags_entry_property = eventschemas_mixins.CfnDiscovererPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9919f8867e69acded77d8e7b8f1908672a054737d5d1766e05a708c5abd965e4)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-discoverer-tagsentry.html#cfn-eventschemas-discoverer-tagsentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-discoverer-tagsentry.html#cfn-eventschemas-discoverer-tagsentry-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnRegistryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "registry_name": "registryName",
        "tags": "tags",
    },
)
class CfnRegistryMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        registry_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnRegistryPropsMixin.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRegistryPropsMixin.

        :param description: A description of the registry to be created.
        :param registry_name: The name of the schema registry.
        :param tags: Tags to associate with the registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
            
            cfn_registry_mixin_props = eventschemas_mixins.CfnRegistryMixinProps(
                description="description",
                registry_name="registryName",
                tags=[eventschemas_mixins.CfnRegistryPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d509922d0b1a29922910b7e66fbef66017a40994db96ed9eeec4b5df03b892a9)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument registry_name", value=registry_name, expected_type=type_hints["registry_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if registry_name is not None:
            self._values["registry_name"] = registry_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the registry to be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schema registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-registryname
        '''
        result = self._values.get("registry_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnRegistryPropsMixin.TagsEntryProperty"]]:
        '''Tags to associate with the registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnRegistryPropsMixin.TagsEntryProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegistryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnRegistryPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "registry_name": "registryName",
        "revision_id": "revisionId",
    },
)
class CfnRegistryPolicyMixinProps:
    def __init__(
        self,
        *,
        policy: typing.Any = None,
        registry_name: typing.Optional[builtins.str] = None,
        revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRegistryPolicyPropsMixin.

        :param policy: A resource-based policy.
        :param registry_name: The name of the registry.
        :param revision_id: The revision ID of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
            
            # policy: Any
            
            cfn_registry_policy_mixin_props = eventschemas_mixins.CfnRegistryPolicyMixinProps(
                policy=policy,
                registry_name="registryName",
                revision_id="revisionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd887e2eded2542ed1aa1697364bbff171772c3b850f434f97d57c20173c16f)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument registry_name", value=registry_name, expected_type=type_hints["registry_name"])
            check_type(argname="argument revision_id", value=revision_id, expected_type=type_hints["revision_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy
        if registry_name is not None:
            self._values["registry_name"] = registry_name
        if revision_id is not None:
            self._values["revision_id"] = revision_id

    @builtins.property
    def policy(self) -> typing.Any:
        '''A resource-based policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def registry_name(self) -> typing.Optional[builtins.str]:
        '''The name of the registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-registryname
        '''
        result = self._values.get("registry_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def revision_id(self) -> typing.Optional[builtins.str]:
        '''The revision ID of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-revisionid
        '''
        result = self._values.get("revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegistryPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRegistryPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnRegistryPolicyPropsMixin",
):
    '''Use the ``AWS::EventSchemas::RegistryPolicy`` resource to specify resource-based policies for an EventBridge Schema Registry.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html
    :cloudformationResource: AWS::EventSchemas::RegistryPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
        
        # policy: Any
        
        cfn_registry_policy_props_mixin = eventschemas_mixins.CfnRegistryPolicyPropsMixin(eventschemas_mixins.CfnRegistryPolicyMixinProps(
            policy=policy,
            registry_name="registryName",
            revision_id="revisionId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRegistryPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EventSchemas::RegistryPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb161367223c8e3c3690d984755dd0ad12f18653ba8ed6b89f6d242aec7a20a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d54b62103ad34743abdff37a353c0d3674f1ed3e7bfa846a4efc900082335fa4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf8f1419cbc7c424f9697e8c897c2f74fb224cb9173872f168362421c06e7af)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRegistryPolicyMixinProps:
        return typing.cast(CfnRegistryPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnRegistryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnRegistryPropsMixin",
):
    '''Use the ``AWS::EventSchemas::Registry`` to specify a schema registry.

    Schema registries are containers for Schemas. Registries collect and organize schemas so that your schemas are in logical groups.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html
    :cloudformationResource: AWS::EventSchemas::Registry
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
        
        cfn_registry_props_mixin = eventschemas_mixins.CfnRegistryPropsMixin(eventschemas_mixins.CfnRegistryMixinProps(
            description="description",
            registry_name="registryName",
            tags=[eventschemas_mixins.CfnRegistryPropsMixin.TagsEntryProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRegistryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EventSchemas::Registry``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461b95edc205d1417828c374ee54487905da9862df6f3c36eb22d62aceaf295e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcb8999f3e4ce98d344abc8b9e2240f5f100c222e72e0c0ba70c7a0551fe8774)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97702e74d859a53d09a3394d3972609238de9c3c69b9875d0a2d7fb714559278)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRegistryMixinProps:
        return typing.cast(CfnRegistryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnRegistryPropsMixin.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Tags to associate with the schema registry.

            :param key: The key of a key-value pair.
            :param value: The value of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-registry-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
                
                tags_entry_property = eventschemas_mixins.CfnRegistryPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da23502329a315451b3931ee58494ae9607c827c89b8effb9766dded76eba36a)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-registry-tagsentry.html#cfn-eventschemas-registry-tagsentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-registry-tagsentry.html#cfn-eventschemas-registry-tagsentry-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnSchemaMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "description": "description",
        "registry_name": "registryName",
        "schema_name": "schemaName",
        "tags": "tags",
        "type": "type",
    },
)
class CfnSchemaMixinProps:
    def __init__(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        registry_name: typing.Optional[builtins.str] = None,
        schema_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnSchemaPropsMixin.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSchemaPropsMixin.

        :param content: The source of the schema definition.
        :param description: A description of the schema.
        :param registry_name: The name of the schema registry.
        :param schema_name: The name of the schema.
        :param tags: Tags associated with the schema.
        :param type: The type of schema. Valid types include ``OpenApi3`` and ``JSONSchemaDraft4`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
            
            cfn_schema_mixin_props = eventschemas_mixins.CfnSchemaMixinProps(
                content="content",
                description="description",
                registry_name="registryName",
                schema_name="schemaName",
                tags=[eventschemas_mixins.CfnSchemaPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9db4459bcb3cbe078d7c17a5360dd8c2837f1978afe0b96b6e64afa32ba6b6)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument registry_name", value=registry_name, expected_type=type_hints["registry_name"])
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if description is not None:
            self._values["description"] = description
        if registry_name is not None:
            self._values["registry_name"] = registry_name
        if schema_name is not None:
            self._values["schema_name"] = schema_name
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''The source of the schema definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schema registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-registryname
        '''
        result = self._values.get("registry_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-schemaname
        '''
        result = self._values.get("schema_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnSchemaPropsMixin.TagsEntryProperty"]]:
        '''Tags associated with the schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnSchemaPropsMixin.TagsEntryProperty"]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of schema.

        Valid types include ``OpenApi3`` and ``JSONSchemaDraft4`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchemaMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSchemaPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnSchemaPropsMixin",
):
    '''Use the ``AWS::EventSchemas::Schema`` resource to specify an event schema.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html
    :cloudformationResource: AWS::EventSchemas::Schema
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
        
        cfn_schema_props_mixin = eventschemas_mixins.CfnSchemaPropsMixin(eventschemas_mixins.CfnSchemaMixinProps(
            content="content",
            description="description",
            registry_name="registryName",
            schema_name="schemaName",
            tags=[eventschemas_mixins.CfnSchemaPropsMixin.TagsEntryProperty(
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
        props: typing.Union[CfnSchemaMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EventSchemas::Schema``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c95644890482ea2ec77b99976afbd8a435a46d644d94b8ef05c596f6bcff5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d0e474238d688beede9b29c6cdef2f5a009614169afef12df7bcbef0919cbf9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ea35f44cfd70660fe5a9b73fa0b460e852ea078544e3a9d53da0b7584db9d5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSchemaMixinProps:
        return typing.cast(CfnSchemaMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eventschemas.mixins.CfnSchemaPropsMixin.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Tags to associate with the schema.

            :param key: The key of a key-value pair.
            :param value: The value of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-schema-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eventschemas import mixins as eventschemas_mixins
                
                tags_entry_property = eventschemas_mixins.CfnSchemaPropsMixin.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbb80b713f2b731767c7b62fe5deb95e8155d5155e765c83bfd0a535ef6ebbf5)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-schema-tagsentry.html#cfn-eventschemas-schema-tagsentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-schema-tagsentry.html#cfn-eventschemas-schema-tagsentry-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDiscovererMixinProps",
    "CfnDiscovererPropsMixin",
    "CfnRegistryMixinProps",
    "CfnRegistryPolicyMixinProps",
    "CfnRegistryPolicyPropsMixin",
    "CfnRegistryPropsMixin",
    "CfnSchemaMixinProps",
    "CfnSchemaPropsMixin",
]

publication.publish()

def _typecheckingstub__2cd3653e10aa73d2687d123bc8f84213de82576ad5e2f8658487eddc61349b6c(
    *,
    cross_account: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDiscovererPropsMixin.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24a592f5bd628e63da502cf57bd14923930f6769a9d4a7bfb93592b7fa28511(
    props: typing.Union[CfnDiscovererMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f2f6ade8772a6a7d17d6df51da3924350e687a8d9058ebb582742b38900d01(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63fa6390eae5d491bc984f4656d70e86c0a0fb873b6f8a62e90c8f813999597(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9919f8867e69acded77d8e7b8f1908672a054737d5d1766e05a708c5abd965e4(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d509922d0b1a29922910b7e66fbef66017a40994db96ed9eeec4b5df03b892a9(
    *,
    description: typing.Optional[builtins.str] = None,
    registry_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnRegistryPropsMixin.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd887e2eded2542ed1aa1697364bbff171772c3b850f434f97d57c20173c16f(
    *,
    policy: typing.Any = None,
    registry_name: typing.Optional[builtins.str] = None,
    revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb161367223c8e3c3690d984755dd0ad12f18653ba8ed6b89f6d242aec7a20a(
    props: typing.Union[CfnRegistryPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54b62103ad34743abdff37a353c0d3674f1ed3e7bfa846a4efc900082335fa4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf8f1419cbc7c424f9697e8c897c2f74fb224cb9173872f168362421c06e7af(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461b95edc205d1417828c374ee54487905da9862df6f3c36eb22d62aceaf295e(
    props: typing.Union[CfnRegistryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb8999f3e4ce98d344abc8b9e2240f5f100c222e72e0c0ba70c7a0551fe8774(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97702e74d859a53d09a3394d3972609238de9c3c69b9875d0a2d7fb714559278(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da23502329a315451b3931ee58494ae9607c827c89b8effb9766dded76eba36a(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9db4459bcb3cbe078d7c17a5360dd8c2837f1978afe0b96b6e64afa32ba6b6(
    *,
    content: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    registry_name: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnSchemaPropsMixin.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c95644890482ea2ec77b99976afbd8a435a46d644d94b8ef05c596f6bcff5d(
    props: typing.Union[CfnSchemaMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0e474238d688beede9b29c6cdef2f5a009614169afef12df7bcbef0919cbf9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ea35f44cfd70660fe5a9b73fa0b460e852ea078544e3a9d53da0b7584db9d5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb80b713f2b731767c7b62fe5deb95e8155d5155e765c83bfd0a535ef6ebbf5(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
