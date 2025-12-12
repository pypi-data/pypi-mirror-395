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
    jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnAcceleratorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "ip_addresses": "ipAddresses",
        "ip_address_type": "ipAddressType",
        "name": "name",
        "tags": "tags",
    },
)
class CfnAcceleratorMixinProps:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAcceleratorPropsMixin.

        :param enabled: Indicates whether the accelerator is enabled. The value is true or false. The default value is true. If the value is set to true, the accelerator cannot be deleted. If set to false, accelerator can be deleted. Default: - true
        :param ip_addresses: Optionally, if you've added your own IP address pool to Global Accelerator (BYOIP), you can choose IP addresses from your own pool to use for the accelerator's static IP addresses when you create an accelerator. You can specify one or two addresses, separated by a comma. Do not include the /32 suffix. Only one IP address from each of your IP address ranges can be used for each accelerator. If you specify only one IP address from your IP address range, Global Accelerator assigns a second static IP address for the accelerator from the AWS IP address pool. Note that you can't update IP addresses for an existing accelerator. To change them, you must create a new accelerator with the new addresses. For more information, see `Bring Your Own IP Addresses (BYOIP) <https://docs.aws.amazon.com/global-accelerator/latest/dg/using-byoip.html>`_ in the *AWS Global Accelerator Developer Guide* .
        :param ip_address_type: The IP address type that an accelerator supports. For a standard accelerator, the value can be IPV4 or DUAL_STACK. Default: - "IPV4"
        :param name: The name of the accelerator. The name must contain only alphanumeric characters or hyphens (-), and must not begin or end with a hyphen.
        :param tags: Create tags for an accelerator. For more information, see `Tagging <https://docs.aws.amazon.com/global-accelerator/latest/dg/tagging-in-global-accelerator.html>`_ in the *AWS Global Accelerator Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
            
            cfn_accelerator_mixin_props = globalaccelerator_mixins.CfnAcceleratorMixinProps(
                enabled=False,
                ip_addresses=["ipAddresses"],
                ip_address_type="ipAddressType",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2940337b3ba19495f83140a5a0b8deb159a5730f16ee1d1130dd745aad536803)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the accelerator is enabled. The value is true or false. The default value is true.

        If the value is set to true, the accelerator cannot be deleted. If set to false, accelerator can be deleted.

        :default: - true

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optionally, if you've added your own IP address pool to Global Accelerator (BYOIP), you can choose IP addresses from your own pool to use for the accelerator's static IP addresses when you create an accelerator.

        You can specify one or two addresses, separated by a comma. Do not include the /32 suffix.

        Only one IP address from each of your IP address ranges can be used for each accelerator. If you specify only one IP address from your IP address range, Global Accelerator assigns a second static IP address for the accelerator from the AWS IP address pool.

        Note that you can't update IP addresses for an existing accelerator. To change them, you must create a new accelerator with the new addresses.

        For more information, see `Bring Your Own IP Addresses (BYOIP) <https://docs.aws.amazon.com/global-accelerator/latest/dg/using-byoip.html>`_ in the *AWS Global Accelerator Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresses
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''The IP address type that an accelerator supports.

        For a standard accelerator, the value can be IPV4 or DUAL_STACK.

        :default: - "IPV4"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the accelerator.

        The name must contain only alphanumeric characters or hyphens (-), and must not begin or end with a hyphen.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Create tags for an accelerator.

        For more information, see `Tagging <https://docs.aws.amazon.com/global-accelerator/latest/dg/tagging-in-global-accelerator.html>`_ in the *AWS Global Accelerator Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAcceleratorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAcceleratorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnAcceleratorPropsMixin",
):
    '''The ``AWS::GlobalAccelerator::Accelerator`` resource is a Global Accelerator resource type that contains information about how you create an accelerator.

    An accelerator includes one or more listeners that process inbound connections and direct traffic to one or more endpoint groups, each of which includes endpoints, such as Application Load Balancers, Network Load Balancers, and Amazon EC2 instances.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
    :cloudformationResource: AWS::GlobalAccelerator::Accelerator
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
        
        cfn_accelerator_props_mixin = globalaccelerator_mixins.CfnAcceleratorPropsMixin(globalaccelerator_mixins.CfnAcceleratorMixinProps(
            enabled=False,
            ip_addresses=["ipAddresses"],
            ip_address_type="ipAddressType",
            name="name",
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
        props: typing.Union[CfnAcceleratorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GlobalAccelerator::Accelerator``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688d8eb0ed4ea8667f9b4df1d0123f38a330e4702501d6db40fa9cf0a61f827a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__001d6c4f9164c42340ea63df4f204034db98ce6b2ca16f615ce73f6e1a7a2a0b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459084997ae54ccee6819086dc170830d5717b6935cb91fe99190144c7734f53)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAcceleratorMixinProps:
        return typing.cast(CfnAcceleratorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnCrossAccountAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "principals": "principals",
        "resources": "resources",
        "tags": "tags",
    },
)
class CfnCrossAccountAttachmentMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrossAccountAttachmentPropsMixin.ResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCrossAccountAttachmentPropsMixin.

        :param name: The name of the cross-account attachment.
        :param principals: The principals included in the cross-account attachment.
        :param resources: The resources included in the cross-account attachment.
        :param tags: Add tags for a cross-account attachment. For more information, see `Tagging in AWS Global Accelerator <https://docs.aws.amazon.com/global-accelerator/latest/dg/tagging-in-global-accelerator.html>`_ in the *AWS Global Accelerator Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-crossaccountattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
            
            cfn_cross_account_attachment_mixin_props = globalaccelerator_mixins.CfnCrossAccountAttachmentMixinProps(
                name="name",
                principals=["principals"],
                resources=[globalaccelerator_mixins.CfnCrossAccountAttachmentPropsMixin.ResourceProperty(
                    cidr="cidr",
                    endpoint_id="endpointId",
                    region="region"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda14e0744786ce8e5da5ec6299445db9eb9a4676ce93e1eb519950459b6aa20)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if principals is not None:
            self._values["principals"] = principals
        if resources is not None:
            self._values["resources"] = resources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the cross-account attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-crossaccountattachment.html#cfn-globalaccelerator-crossaccountattachment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The principals included in the cross-account attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-crossaccountattachment.html#cfn-globalaccelerator-crossaccountattachment-principals
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrossAccountAttachmentPropsMixin.ResourceProperty"]]]]:
        '''The resources included in the cross-account attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-crossaccountattachment.html#cfn-globalaccelerator-crossaccountattachment-resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrossAccountAttachmentPropsMixin.ResourceProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Add tags for a cross-account attachment.

        For more information, see `Tagging in AWS Global Accelerator <https://docs.aws.amazon.com/global-accelerator/latest/dg/tagging-in-global-accelerator.html>`_ in the *AWS Global Accelerator Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-crossaccountattachment.html#cfn-globalaccelerator-crossaccountattachment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCrossAccountAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCrossAccountAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnCrossAccountAttachmentPropsMixin",
):
    '''Create a cross-account attachment in AWS Global Accelerator .

    You create a cross-account attachment to specify the *principals* who have permission to work with *resources* in accelerators in their own account. You specify, in the same attachment, the resources that are shared.

    A principal can be an AWS account number or the Amazon Resource Name (ARN) for an accelerator. For account numbers that are listed as principals, to work with a resource listed in the attachment, you must sign in to an account specified as a principal. Then, you can work with resources that are listed, with any of your accelerators. If an accelerator ARN is listed in the cross-account attachment as a principal, anyone with permission to make updates to the accelerator can work with resources that are listed in the attachment.

    Specify each principal and resource separately. To specify two CIDR address pools, list them individually under ``Resources`` , and so on. For a command line operation, for example, you might use a statement like the following:

    ``"Resources": [{"Cidr": "169.254.60.0/24"},{"Cidr": "169.254.59.0/24"}]``

    For more information, see `Working with cross-account attachments and resources in AWS Global Accelerator <https://docs.aws.amazon.com/global-accelerator/latest/dg/cross-account-resources.html>`_ in the *AWS Global Accelerator Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-crossaccountattachment.html
    :cloudformationResource: AWS::GlobalAccelerator::CrossAccountAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
        
        cfn_cross_account_attachment_props_mixin = globalaccelerator_mixins.CfnCrossAccountAttachmentPropsMixin(globalaccelerator_mixins.CfnCrossAccountAttachmentMixinProps(
            name="name",
            principals=["principals"],
            resources=[globalaccelerator_mixins.CfnCrossAccountAttachmentPropsMixin.ResourceProperty(
                cidr="cidr",
                endpoint_id="endpointId",
                region="region"
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
        props: typing.Union[CfnCrossAccountAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GlobalAccelerator::CrossAccountAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ea7fcbcfe2b78303a1b9c353a2f6635dd8016f474718d3dc35afb66f721ddb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9d068629dbebeaffdcdbf7dda68be7ce196cbffdd52de1593828c03b0c2bf8c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7adda35976c755287e48a69f8d3580f46abda31f7200fe12ebd5f1f238da1d27)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCrossAccountAttachmentMixinProps:
        return typing.cast(CfnCrossAccountAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnCrossAccountAttachmentPropsMixin.ResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr": "cidr", "endpoint_id": "endpointId", "region": "region"},
    )
    class ResourceProperty:
        def __init__(
            self,
            *,
            cidr: typing.Optional[builtins.str] = None,
            endpoint_id: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A resource is one of the following: the ARN for an AWS resource that is supported by AWS Global Accelerator to be added as an endpoint, or a CIDR range that specifies a bring your own IP (BYOIP) address pool.

            :param cidr: An IP address range, in CIDR format, that is specified as resource. The address must be provisioned and advertised in AWS Global Accelerator by following the bring your own IP address (BYOIP) process for Global Accelerator For more information, see `Bring your own IP addresses (BYOIP) <https://docs.aws.amazon.com/global-accelerator/latest/dg/using-byoip.html>`_ in the AWS Global Accelerator Developer Guide.
            :param endpoint_id: The endpoint ID for the endpoint that is specified as a AWS resource. An endpoint ID for the cross-account feature is the ARN of an AWS resource, such as a Network Load Balancer, that Global Accelerator supports as an endpoint for an accelerator.
            :param region: The AWS Region where a shared endpoint resource is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-crossaccountattachment-resource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
                
                resource_property = globalaccelerator_mixins.CfnCrossAccountAttachmentPropsMixin.ResourceProperty(
                    cidr="cidr",
                    endpoint_id="endpointId",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0db96f8d243a9beb40a7510a623e6dde07d8367fee96044cc40a0ae8e395fdda)
                check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
                check_type(argname="argument endpoint_id", value=endpoint_id, expected_type=type_hints["endpoint_id"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidr is not None:
                self._values["cidr"] = cidr
            if endpoint_id is not None:
                self._values["endpoint_id"] = endpoint_id
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def cidr(self) -> typing.Optional[builtins.str]:
            '''An IP address range, in CIDR format, that is specified as resource.

            The address must be provisioned and advertised in AWS Global Accelerator by following the bring your own IP address (BYOIP) process for Global Accelerator

            For more information, see `Bring your own IP addresses (BYOIP) <https://docs.aws.amazon.com/global-accelerator/latest/dg/using-byoip.html>`_ in the AWS Global Accelerator Developer Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-crossaccountattachment-resource.html#cfn-globalaccelerator-crossaccountattachment-resource-cidr
            '''
            result = self._values.get("cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The endpoint ID for the endpoint that is specified as a AWS resource.

            An endpoint ID for the cross-account feature is the ARN of an AWS resource, such as a Network Load Balancer, that Global Accelerator supports as an endpoint for an accelerator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-crossaccountattachment-resource.html#cfn-globalaccelerator-crossaccountattachment-resource-endpointid
            '''
            result = self._values.get("endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region where a shared endpoint resource is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-crossaccountattachment-resource.html#cfn-globalaccelerator-crossaccountattachment-resource-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnEndpointGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_configurations": "endpointConfigurations",
        "endpoint_group_region": "endpointGroupRegion",
        "health_check_interval_seconds": "healthCheckIntervalSeconds",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "listener_arn": "listenerArn",
        "port_overrides": "portOverrides",
        "threshold_count": "thresholdCount",
        "traffic_dial_percentage": "trafficDialPercentage",
    },
)
class CfnEndpointGroupMixinProps:
    def __init__(
        self,
        *,
        endpoint_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointGroupPropsMixin.EndpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        endpoint_group_region: typing.Optional[builtins.str] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        listener_arn: typing.Optional[builtins.str] = None,
        port_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEndpointGroupPropsMixin.PortOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        threshold_count: typing.Optional[jsii.Number] = None,
        traffic_dial_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnEndpointGroupPropsMixin.

        :param endpoint_configurations: The list of endpoint objects.
        :param endpoint_group_region: The AWS Regions where the endpoint group is located.
        :param health_check_interval_seconds: The time—10 seconds or 30 seconds—between health checks for each endpoint. The default value is 30. Default: - 30
        :param health_check_path: If the protocol is HTTP/S, then this value provides the ping path that Global Accelerator uses for the destination on the endpoints for health checks. The default is slash (/). Default: - "/"
        :param health_check_port: The port that Global Accelerator uses to perform health checks on endpoints that are part of this endpoint group. The default port is the port for the listener that this endpoint group is associated with. If the listener port is a list, Global Accelerator uses the first specified port in the list of ports. Default: - -1
        :param health_check_protocol: The protocol that Global Accelerator uses to perform health checks on endpoints that are part of this endpoint group. The default value is TCP. Default: - "TCP"
        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :param port_overrides: Allows you to override the destination ports used to route traffic to an endpoint. Using a port override lets you map a list of external destination ports (that your users send traffic to) to a list of internal destination ports that you want an application endpoint to receive traffic on.
        :param threshold_count: The number of consecutive health checks required to set the state of a healthy endpoint to unhealthy, or to set an unhealthy endpoint to healthy. The default value is 3. Default: - 3
        :param traffic_dial_percentage: The percentage of traffic to send to an AWS Regions . Additional traffic is distributed to other endpoint groups for this listener. Use this action to increase (dial up) or decrease (dial down) traffic to a specific Region. The percentage is applied to the traffic that would otherwise have been routed to the Region based on optimal routing. The default value is 100. Default: - 100

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
            
            cfn_endpoint_group_mixin_props = globalaccelerator_mixins.CfnEndpointGroupMixinProps(
                endpoint_configurations=[globalaccelerator_mixins.CfnEndpointGroupPropsMixin.EndpointConfigurationProperty(
                    attachment_arn="attachmentArn",
                    client_ip_preservation_enabled=False,
                    endpoint_id="endpointId",
                    weight=123
                )],
                endpoint_group_region="endpointGroupRegion",
                health_check_interval_seconds=123,
                health_check_path="healthCheckPath",
                health_check_port=123,
                health_check_protocol="healthCheckProtocol",
                listener_arn="listenerArn",
                port_overrides=[globalaccelerator_mixins.CfnEndpointGroupPropsMixin.PortOverrideProperty(
                    endpoint_port=123,
                    listener_port=123
                )],
                threshold_count=123,
                traffic_dial_percentage=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8207f86e5f3782c69d4bf0963d78188a3404a62023dc97316998a9a00a7c54)
            check_type(argname="argument endpoint_configurations", value=endpoint_configurations, expected_type=type_hints["endpoint_configurations"])
            check_type(argname="argument endpoint_group_region", value=endpoint_group_region, expected_type=type_hints["endpoint_group_region"])
            check_type(argname="argument health_check_interval_seconds", value=health_check_interval_seconds, expected_type=type_hints["health_check_interval_seconds"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument health_check_port", value=health_check_port, expected_type=type_hints["health_check_port"])
            check_type(argname="argument health_check_protocol", value=health_check_protocol, expected_type=type_hints["health_check_protocol"])
            check_type(argname="argument listener_arn", value=listener_arn, expected_type=type_hints["listener_arn"])
            check_type(argname="argument port_overrides", value=port_overrides, expected_type=type_hints["port_overrides"])
            check_type(argname="argument threshold_count", value=threshold_count, expected_type=type_hints["threshold_count"])
            check_type(argname="argument traffic_dial_percentage", value=traffic_dial_percentage, expected_type=type_hints["traffic_dial_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if endpoint_configurations is not None:
            self._values["endpoint_configurations"] = endpoint_configurations
        if endpoint_group_region is not None:
            self._values["endpoint_group_region"] = endpoint_group_region
        if health_check_interval_seconds is not None:
            self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if listener_arn is not None:
            self._values["listener_arn"] = listener_arn
        if port_overrides is not None:
            self._values["port_overrides"] = port_overrides
        if threshold_count is not None:
            self._values["threshold_count"] = threshold_count
        if traffic_dial_percentage is not None:
            self._values["traffic_dial_percentage"] = traffic_dial_percentage

    @builtins.property
    def endpoint_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointGroupPropsMixin.EndpointConfigurationProperty"]]]]:
        '''The list of endpoint objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointconfigurations
        '''
        result = self._values.get("endpoint_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointGroupPropsMixin.EndpointConfigurationProperty"]]]], result)

    @builtins.property
    def endpoint_group_region(self) -> typing.Optional[builtins.str]:
        '''The AWS Regions where the endpoint group is located.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointgroupregion
        '''
        result = self._values.get("endpoint_group_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time—10 seconds or 30 seconds—between health checks for each endpoint.

        The default value is 30.

        :default: - 30

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckintervalseconds
        '''
        result = self._values.get("health_check_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''If the protocol is HTTP/S, then this value provides the ping path that Global Accelerator uses for the destination on the endpoints for health checks.

        The default is slash (/).

        :default: - "/"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckpath
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        '''The port that Global Accelerator uses to perform health checks on endpoints that are part of this endpoint group.

        The default port is the port for the listener that this endpoint group is associated with. If the listener port is a list, Global Accelerator uses the first specified port in the list of ports.

        :default: - -1

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckport
        '''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol that Global Accelerator uses to perform health checks on endpoints that are part of this endpoint group.

        The default value is TCP.

        :default: - "TCP"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckprotocol
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def listener_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the listener.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-listenerarn
        '''
        result = self._values.get("listener_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_overrides(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointGroupPropsMixin.PortOverrideProperty"]]]]:
        '''Allows you to override the destination ports used to route traffic to an endpoint.

        Using a port override lets you map a list of external destination ports (that your users send traffic to) to a list of internal destination ports that you want an application endpoint to receive traffic on.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-portoverrides
        '''
        result = self._values.get("port_overrides")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEndpointGroupPropsMixin.PortOverrideProperty"]]]], result)

    @builtins.property
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive health checks required to set the state of a healthy endpoint to unhealthy, or to set an unhealthy endpoint to healthy.

        The default value is 3.

        :default: - 3

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-thresholdcount
        '''
        result = self._values.get("threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of traffic to send to an AWS Regions .

        Additional traffic is distributed to other endpoint groups for this listener.

        Use this action to increase (dial up) or decrease (dial down) traffic to a specific Region. The percentage is applied to the traffic that would otherwise have been routed to the Region based on optimal routing.

        The default value is 100.

        :default: - 100

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-trafficdialpercentage
        '''
        result = self._values.get("traffic_dial_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEndpointGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnEndpointGroupPropsMixin",
):
    '''The ``AWS::GlobalAccelerator::EndpointGroup`` resource is a Global Accelerator resource type that contains information about how you create an endpoint group for the specified listener.

    An endpoint group is a collection of endpoints in one AWS Region .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
    :cloudformationResource: AWS::GlobalAccelerator::EndpointGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
        
        cfn_endpoint_group_props_mixin = globalaccelerator_mixins.CfnEndpointGroupPropsMixin(globalaccelerator_mixins.CfnEndpointGroupMixinProps(
            endpoint_configurations=[globalaccelerator_mixins.CfnEndpointGroupPropsMixin.EndpointConfigurationProperty(
                attachment_arn="attachmentArn",
                client_ip_preservation_enabled=False,
                endpoint_id="endpointId",
                weight=123
            )],
            endpoint_group_region="endpointGroupRegion",
            health_check_interval_seconds=123,
            health_check_path="healthCheckPath",
            health_check_port=123,
            health_check_protocol="healthCheckProtocol",
            listener_arn="listenerArn",
            port_overrides=[globalaccelerator_mixins.CfnEndpointGroupPropsMixin.PortOverrideProperty(
                endpoint_port=123,
                listener_port=123
            )],
            threshold_count=123,
            traffic_dial_percentage=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEndpointGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GlobalAccelerator::EndpointGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75241963096047f8666ca6514965e507a54e8c5ae0417221bb48eb539075930c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72595283bc882c74062f113d7d255f3757f0130fc80f6186567f9a4f0efab4fd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04853d1e6247a4d99adaab88a66b671805d2f4e5fb7cd324e9bcf8b8c41955b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEndpointGroupMixinProps:
        return typing.cast(CfnEndpointGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnEndpointGroupPropsMixin.EndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_arn": "attachmentArn",
            "client_ip_preservation_enabled": "clientIpPreservationEnabled",
            "endpoint_id": "endpointId",
            "weight": "weight",
        },
    )
    class EndpointConfigurationProperty:
        def __init__(
            self,
            *,
            attachment_arn: typing.Optional[builtins.str] = None,
            client_ip_preservation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            endpoint_id: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A complex type for endpoints.

            A resource must be valid and active when you add it as an endpoint.

            :param attachment_arn: The Amazon Resource Name (ARN) of the cross-account attachment that specifies the endpoints (resources) that can be added to accelerators and principals that have permission to add the endpoints.
            :param client_ip_preservation_enabled: Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint. The value is true or false. The default value is true for new accelerators. If the value is set to true, the client's IP address is preserved in the ``X-Forwarded-For`` request header as traffic travels to applications on the Application Load Balancer endpoint fronted by the accelerator. For more information, see `Preserve Client IP Addresses <https://docs.aws.amazon.com/global-accelerator/latest/dg/preserve-client-ip-address.html>`_ in the *AWS Global Accelerator Developer Guide* . Default: - true
            :param endpoint_id: An ID for the endpoint. If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID. For Amazon EC2 instances, this is the EC2 instance ID. A resource must be valid and active when you add it as an endpoint. For cross-account endpoints, this must be the ARN of the resource.
            :param weight: The weight associated with the endpoint. When you add weights to endpoints, you configure Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. For more information, see `Endpoint Weights <https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints-endpoint-weights.html>`_ in the *AWS Global Accelerator Developer Guide* . Default: - 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
                
                endpoint_configuration_property = globalaccelerator_mixins.CfnEndpointGroupPropsMixin.EndpointConfigurationProperty(
                    attachment_arn="attachmentArn",
                    client_ip_preservation_enabled=False,
                    endpoint_id="endpointId",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b46368f4c45571a884beab7558467ba24b54578d5753d3e97fd6ca90cb520b7)
                check_type(argname="argument attachment_arn", value=attachment_arn, expected_type=type_hints["attachment_arn"])
                check_type(argname="argument client_ip_preservation_enabled", value=client_ip_preservation_enabled, expected_type=type_hints["client_ip_preservation_enabled"])
                check_type(argname="argument endpoint_id", value=endpoint_id, expected_type=type_hints["endpoint_id"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_arn is not None:
                self._values["attachment_arn"] = attachment_arn
            if client_ip_preservation_enabled is not None:
                self._values["client_ip_preservation_enabled"] = client_ip_preservation_enabled
            if endpoint_id is not None:
                self._values["endpoint_id"] = endpoint_id
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def attachment_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the cross-account attachment that specifies the endpoints (resources) that can be added to accelerators and principals that have permission to add the endpoints.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-attachmentarn
            '''
            result = self._values.get("attachment_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_ip_preservation_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether client IP address preservation is enabled for an Application Load Balancer endpoint.

            The value is true or false. The default value is true for new accelerators.

            If the value is set to true, the client's IP address is preserved in the ``X-Forwarded-For`` request header as traffic travels to applications on the Application Load Balancer endpoint fronted by the accelerator.

            For more information, see `Preserve Client IP Addresses <https://docs.aws.amazon.com/global-accelerator/latest/dg/preserve-client-ip-address.html>`_ in the *AWS Global Accelerator Developer Guide* .

            :default: - true

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-clientippreservationenabled
            '''
            result = self._values.get("client_ip_preservation_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def endpoint_id(self) -> typing.Optional[builtins.str]:
            '''An ID for the endpoint.

            If the endpoint is a Network Load Balancer or Application Load Balancer, this is the Amazon Resource Name (ARN) of the resource. If the endpoint is an Elastic IP address, this is the Elastic IP address allocation ID. For Amazon EC2 instances, this is the EC2 instance ID. A resource must be valid and active when you add it as an endpoint.

            For cross-account endpoints, this must be the ARN of the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-endpointid
            '''
            result = self._values.get("endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The weight associated with the endpoint.

            When you add weights to endpoints, you configure Global Accelerator to route traffic based on proportions that you specify. For example, you might specify endpoint weights of 4, 5, 5, and 6 (sum=20). The result is that 4/20 of your traffic, on average, is routed to the first endpoint, 5/20 is routed both to the second and third endpoints, and 6/20 is routed to the last endpoint. For more information, see `Endpoint Weights <https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints-endpoint-weights.html>`_ in the *AWS Global Accelerator Developer Guide* .

            :default: - 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnEndpointGroupPropsMixin.PortOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint_port": "endpointPort",
            "listener_port": "listenerPort",
        },
    )
    class PortOverrideProperty:
        def __init__(
            self,
            *,
            endpoint_port: typing.Optional[jsii.Number] = None,
            listener_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Override specific listener ports used to route traffic to endpoints that are part of an endpoint group.

            For example, you can create a port override in which the listener receives user traffic on ports 80 and 443, but your accelerator routes that traffic to ports 1080 and 1443, respectively, on the endpoints.

            For more information, see `Port overrides <https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoint-groups-port-override.html>`_ in the *AWS Global Accelerator Developer Guide* .

            :param endpoint_port: The endpoint port that you want a listener port to be mapped to. This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
            :param listener_port: The listener port that you want to map to a specific endpoint port. This is the port that user traffic arrives to the Global Accelerator on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-portoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
                
                port_override_property = globalaccelerator_mixins.CfnEndpointGroupPropsMixin.PortOverrideProperty(
                    endpoint_port=123,
                    listener_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__529f004872e50fe755b93d6b887bc30cef70b0c9fe1bc6d624618d44bd21c7d1)
                check_type(argname="argument endpoint_port", value=endpoint_port, expected_type=type_hints["endpoint_port"])
                check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint_port is not None:
                self._values["endpoint_port"] = endpoint_port
            if listener_port is not None:
                self._values["listener_port"] = listener_port

        @builtins.property
        def endpoint_port(self) -> typing.Optional[jsii.Number]:
            '''The endpoint port that you want a listener port to be mapped to.

            This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-portoverride.html#cfn-globalaccelerator-endpointgroup-portoverride-endpointport
            '''
            result = self._values.get("endpoint_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def listener_port(self) -> typing.Optional[jsii.Number]:
            '''The listener port that you want to map to a specific endpoint port.

            This is the port that user traffic arrives to the Global Accelerator on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-portoverride.html#cfn-globalaccelerator-endpointgroup-portoverride-listenerport
            '''
            result = self._values.get("listener_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnListenerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_arn": "acceleratorArn",
        "client_affinity": "clientAffinity",
        "port_ranges": "portRanges",
        "protocol": "protocol",
    },
)
class CfnListenerMixinProps:
    def __init__(
        self,
        *,
        accelerator_arn: typing.Optional[builtins.str] = None,
        client_affinity: typing.Optional[builtins.str] = None,
        port_ranges: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.PortRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        protocol: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnListenerPropsMixin.

        :param accelerator_arn: The Amazon Resource Name (ARN) of your accelerator.
        :param client_affinity: Client affinity lets you direct all requests from a user to the same endpoint, if you have stateful applications, regardless of the port and protocol of the client request. Client affinity gives you control over whether to always route each client to the same specific endpoint. AWS Global Accelerator uses a consistent-flow hashing algorithm to choose the optimal endpoint for a connection. If client affinity is ``NONE`` , Global Accelerator uses the "five-tuple" (5-tuple) properties—source IP address, source port, destination IP address, destination port, and protocol—to select the hash value, and then chooses the best endpoint. However, with this setting, if someone uses different ports to connect to Global Accelerator, their connections might not be always routed to the same endpoint because the hash value changes. If you want a given client to always be routed to the same endpoint, set client affinity to ``SOURCE_IP`` instead. When you use the ``SOURCE_IP`` setting, Global Accelerator uses the "two-tuple" (2-tuple) properties— source (client) IP address and destination IP address—to select the hash value. The default value is ``NONE`` . Default: - "NONE"
        :param port_ranges: The list of port ranges for the connections from clients to the accelerator.
        :param protocol: The protocol for the connections from clients to the accelerator. Default: - "TCP"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
            
            cfn_listener_mixin_props = globalaccelerator_mixins.CfnListenerMixinProps(
                accelerator_arn="acceleratorArn",
                client_affinity="clientAffinity",
                port_ranges=[globalaccelerator_mixins.CfnListenerPropsMixin.PortRangeProperty(
                    from_port=123,
                    to_port=123
                )],
                protocol="protocol"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ab305984ab6491694e1e2e07faa115db95b5040b8742dbecd4e8b5bb722226)
            check_type(argname="argument accelerator_arn", value=accelerator_arn, expected_type=type_hints["accelerator_arn"])
            check_type(argname="argument client_affinity", value=client_affinity, expected_type=type_hints["client_affinity"])
            check_type(argname="argument port_ranges", value=port_ranges, expected_type=type_hints["port_ranges"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_arn is not None:
            self._values["accelerator_arn"] = accelerator_arn
        if client_affinity is not None:
            self._values["client_affinity"] = client_affinity
        if port_ranges is not None:
            self._values["port_ranges"] = port_ranges
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def accelerator_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of your accelerator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-acceleratorarn
        '''
        result = self._values.get("accelerator_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_affinity(self) -> typing.Optional[builtins.str]:
        '''Client affinity lets you direct all requests from a user to the same endpoint, if you have stateful applications, regardless of the port and protocol of the client request.

        Client affinity gives you control over whether to always route each client to the same specific endpoint.

        AWS Global Accelerator uses a consistent-flow hashing algorithm to choose the optimal endpoint for a connection. If client affinity is ``NONE`` , Global Accelerator uses the "five-tuple" (5-tuple) properties—source IP address, source port, destination IP address, destination port, and protocol—to select the hash value, and then chooses the best endpoint. However, with this setting, if someone uses different ports to connect to Global Accelerator, their connections might not be always routed to the same endpoint because the hash value changes.

        If you want a given client to always be routed to the same endpoint, set client affinity to ``SOURCE_IP`` instead. When you use the ``SOURCE_IP`` setting, Global Accelerator uses the "two-tuple" (2-tuple) properties— source (client) IP address and destination IP address—to select the hash value.

        The default value is ``NONE`` .

        :default: - "NONE"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-clientaffinity
        '''
        result = self._values.get("client_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_ranges(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.PortRangeProperty"]]]]:
        '''The list of port ranges for the connections from clients to the accelerator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-portranges
        '''
        result = self._values.get("port_ranges")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.PortRangeProperty"]]]], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol for the connections from clients to the accelerator.

        :default: - "TCP"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnListenerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnListenerPropsMixin",
):
    '''The ``AWS::GlobalAccelerator::Listener`` resource is a Global Accelerator resource type that contains information about how you create a listener to process inbound connections from clients to an accelerator.

    Connections arrive to assigned static IP addresses on a port, port range, or list of port ranges that you specify.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
    :cloudformationResource: AWS::GlobalAccelerator::Listener
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
        
        cfn_listener_props_mixin = globalaccelerator_mixins.CfnListenerPropsMixin(globalaccelerator_mixins.CfnListenerMixinProps(
            accelerator_arn="acceleratorArn",
            client_affinity="clientAffinity",
            port_ranges=[globalaccelerator_mixins.CfnListenerPropsMixin.PortRangeProperty(
                from_port=123,
                to_port=123
            )],
            protocol="protocol"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnListenerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::GlobalAccelerator::Listener``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79277b0273ae50e2f18068adcfe6e06a0ea6405c2910945cc45e35f3f6cdd07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e58da65682871937073f82081c3df2960d865474f94ab05513afc7b0a3ed9738)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d357e93f7848ee6cc26129383d9d3f3a5338ac50afbf5edb1345b10cefc9c3e2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnListenerMixinProps:
        return typing.cast(CfnListenerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_globalaccelerator.mixins.CfnListenerPropsMixin.PortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"from_port": "fromPort", "to_port": "toPort"},
    )
    class PortRangeProperty:
        def __init__(
            self,
            *,
            from_port: typing.Optional[jsii.Number] = None,
            to_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A complex type for a range of ports for a listener.

            :param from_port: The first port in the range of ports, inclusive.
            :param to_port: The last port in the range of ports, inclusive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_globalaccelerator import mixins as globalaccelerator_mixins
                
                port_range_property = globalaccelerator_mixins.CfnListenerPropsMixin.PortRangeProperty(
                    from_port=123,
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__926e54d436e2f2d7f247ee670bd8057e56561c5cc24ff0eb165528f2ff409001)
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if from_port is not None:
                self._values["from_port"] = from_port
            if to_port is not None:
                self._values["to_port"] = to_port

        @builtins.property
        def from_port(self) -> typing.Optional[jsii.Number]:
            '''The first port in the range of ports, inclusive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-fromport
            '''
            result = self._values.get("from_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def to_port(self) -> typing.Optional[jsii.Number]:
            '''The last port in the range of ports, inclusive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-toport
            '''
            result = self._values.get("to_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAcceleratorMixinProps",
    "CfnAcceleratorPropsMixin",
    "CfnCrossAccountAttachmentMixinProps",
    "CfnCrossAccountAttachmentPropsMixin",
    "CfnEndpointGroupMixinProps",
    "CfnEndpointGroupPropsMixin",
    "CfnListenerMixinProps",
    "CfnListenerPropsMixin",
]

publication.publish()

def _typecheckingstub__2940337b3ba19495f83140a5a0b8deb159a5730f16ee1d1130dd745aad536803(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688d8eb0ed4ea8667f9b4df1d0123f38a330e4702501d6db40fa9cf0a61f827a(
    props: typing.Union[CfnAcceleratorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001d6c4f9164c42340ea63df4f204034db98ce6b2ca16f615ce73f6e1a7a2a0b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459084997ae54ccee6819086dc170830d5717b6935cb91fe99190144c7734f53(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda14e0744786ce8e5da5ec6299445db9eb9a4676ce93e1eb519950459b6aa20(
    *,
    name: typing.Optional[builtins.str] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrossAccountAttachmentPropsMixin.ResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ea7fcbcfe2b78303a1b9c353a2f6635dd8016f474718d3dc35afb66f721ddb(
    props: typing.Union[CfnCrossAccountAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d068629dbebeaffdcdbf7dda68be7ce196cbffdd52de1593828c03b0c2bf8c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7adda35976c755287e48a69f8d3580f46abda31f7200fe12ebd5f1f238da1d27(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db96f8d243a9beb40a7510a623e6dde07d8367fee96044cc40a0ae8e395fdda(
    *,
    cidr: typing.Optional[builtins.str] = None,
    endpoint_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8207f86e5f3782c69d4bf0963d78188a3404a62023dc97316998a9a00a7c54(
    *,
    endpoint_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointGroupPropsMixin.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    endpoint_group_region: typing.Optional[builtins.str] = None,
    health_check_interval_seconds: typing.Optional[jsii.Number] = None,
    health_check_path: typing.Optional[builtins.str] = None,
    health_check_port: typing.Optional[jsii.Number] = None,
    health_check_protocol: typing.Optional[builtins.str] = None,
    listener_arn: typing.Optional[builtins.str] = None,
    port_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEndpointGroupPropsMixin.PortOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    threshold_count: typing.Optional[jsii.Number] = None,
    traffic_dial_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75241963096047f8666ca6514965e507a54e8c5ae0417221bb48eb539075930c(
    props: typing.Union[CfnEndpointGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72595283bc882c74062f113d7d255f3757f0130fc80f6186567f9a4f0efab4fd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04853d1e6247a4d99adaab88a66b671805d2f4e5fb7cd324e9bcf8b8c41955b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b46368f4c45571a884beab7558467ba24b54578d5753d3e97fd6ca90cb520b7(
    *,
    attachment_arn: typing.Optional[builtins.str] = None,
    client_ip_preservation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    endpoint_id: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529f004872e50fe755b93d6b887bc30cef70b0c9fe1bc6d624618d44bd21c7d1(
    *,
    endpoint_port: typing.Optional[jsii.Number] = None,
    listener_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ab305984ab6491694e1e2e07faa115db95b5040b8742dbecd4e8b5bb722226(
    *,
    accelerator_arn: typing.Optional[builtins.str] = None,
    client_affinity: typing.Optional[builtins.str] = None,
    port_ranges: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79277b0273ae50e2f18068adcfe6e06a0ea6405c2910945cc45e35f3f6cdd07(
    props: typing.Union[CfnListenerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58da65682871937073f82081c3df2960d865474f94ab05513afc7b0a3ed9738(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d357e93f7848ee6cc26129383d9d3f3a5338ac50afbf5edb1345b10cefc9c3e2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926e54d436e2f2d7f247ee670bd8057e56561c5cc24ff0eb165528f2ff409001(
    *,
    from_port: typing.Optional[jsii.Number] = None,
    to_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
