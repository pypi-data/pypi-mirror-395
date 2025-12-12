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
    jsii_type="@aws-cdk/mixins-preview.aws_invoicing.mixins.CfnInvoiceUnitMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "invoice_receiver": "invoiceReceiver",
        "name": "name",
        "resource_tags": "resourceTags",
        "rule": "rule",
        "tax_inheritance_disabled": "taxInheritanceDisabled",
    },
)
class CfnInvoiceUnitMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        invoice_receiver: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        resource_tags: typing.Optional[typing.Sequence[typing.Union["CfnInvoiceUnitPropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInvoiceUnitPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tax_inheritance_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnInvoiceUnitPropsMixin.

        :param description: The assigned description for an invoice unit. This information can't be modified or deleted.
        :param invoice_receiver: The account that receives invoices related to the invoice unit.
        :param name: A unique name that is distinctive within your AWS .
        :param resource_tags: The tag structure that contains a tag key and value.
        :param rule: An ``InvoiceUnitRule`` object used the categorize invoice units.
        :param tax_inheritance_disabled: Whether the invoice unit based tax inheritance is/ should be enabled or disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-invoicing-invoiceunit.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_invoicing import mixins as invoicing_mixins
            
            cfn_invoice_unit_mixin_props = invoicing_mixins.CfnInvoiceUnitMixinProps(
                description="description",
                invoice_receiver="invoiceReceiver",
                name="name",
                resource_tags=[invoicing_mixins.CfnInvoiceUnitPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )],
                rule=invoicing_mixins.CfnInvoiceUnitPropsMixin.RuleProperty(
                    linked_accounts=["linkedAccounts"]
                ),
                tax_inheritance_disabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246767bb4b3dbaeeca5d1e9b515e8ae95ee0a72c3798ad47e8aeb465fe770233)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument invoice_receiver", value=invoice_receiver, expected_type=type_hints["invoice_receiver"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument tax_inheritance_disabled", value=tax_inheritance_disabled, expected_type=type_hints["tax_inheritance_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if invoice_receiver is not None:
            self._values["invoice_receiver"] = invoice_receiver
        if name is not None:
            self._values["name"] = name
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if rule is not None:
            self._values["rule"] = rule
        if tax_inheritance_disabled is not None:
            self._values["tax_inheritance_disabled"] = tax_inheritance_disabled

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The assigned description for an invoice unit.

        This information can't be modified or deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-invoicing-invoiceunit.html#cfn-invoicing-invoiceunit-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invoice_receiver(self) -> typing.Optional[builtins.str]:
        '''The account that receives invoices related to the invoice unit.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-invoicing-invoiceunit.html#cfn-invoicing-invoiceunit-invoicereceiver
        '''
        result = self._values.get("invoice_receiver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A unique name that is distinctive within your AWS .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-invoicing-invoiceunit.html#cfn-invoicing-invoiceunit-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.List["CfnInvoiceUnitPropsMixin.ResourceTagProperty"]]:
        '''The tag structure that contains a tag key and value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-invoicing-invoiceunit.html#cfn-invoicing-invoiceunit-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.List["CfnInvoiceUnitPropsMixin.ResourceTagProperty"]], result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInvoiceUnitPropsMixin.RuleProperty"]]:
        '''An ``InvoiceUnitRule`` object used the categorize invoice units.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-invoicing-invoiceunit.html#cfn-invoicing-invoiceunit-rule
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInvoiceUnitPropsMixin.RuleProperty"]], result)

    @builtins.property
    def tax_inheritance_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether the invoice unit based tax inheritance is/ should be enabled or disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-invoicing-invoiceunit.html#cfn-invoicing-invoiceunit-taxinheritancedisabled
        '''
        result = self._values.get("tax_inheritance_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInvoiceUnitMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInvoiceUnitPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_invoicing.mixins.CfnInvoiceUnitPropsMixin",
):
    '''An invoice unit is a set of mutually exclusive account that correspond to your business entity.

    Invoice units allow you separate AWS account costs and configures your invoice for each business entity going forward.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-invoicing-invoiceunit.html
    :cloudformationResource: AWS::Invoicing::InvoiceUnit
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_invoicing import mixins as invoicing_mixins
        
        cfn_invoice_unit_props_mixin = invoicing_mixins.CfnInvoiceUnitPropsMixin(invoicing_mixins.CfnInvoiceUnitMixinProps(
            description="description",
            invoice_receiver="invoiceReceiver",
            name="name",
            resource_tags=[invoicing_mixins.CfnInvoiceUnitPropsMixin.ResourceTagProperty(
                key="key",
                value="value"
            )],
            rule=invoicing_mixins.CfnInvoiceUnitPropsMixin.RuleProperty(
                linked_accounts=["linkedAccounts"]
            ),
            tax_inheritance_disabled=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInvoiceUnitMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Invoicing::InvoiceUnit``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6234dd7f3b7e30074227733e41c2e1d4ca8d92fac1f5db96179a1c125db7484d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ad5f8f5e261221c3c1903a7da190d6be5b0e787a03f1a3734af9be0d7fab75e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__755afa79165d918df5548d49eb34a3ce82dec74805ac71c79ab17fc17f33669f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInvoiceUnitMixinProps:
        return typing.cast(CfnInvoiceUnitMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_invoicing.mixins.CfnInvoiceUnitPropsMixin.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ResourceTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The tag structure that contains a tag key and value.

            :param key: The object key of your of your resource tag.
            :param value: The specific value of the resource tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-invoicing-invoiceunit-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_invoicing import mixins as invoicing_mixins
                
                resource_tag_property = invoicing_mixins.CfnInvoiceUnitPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f16f4bb05f4a29184ec315a55c71c4c147403b47d829c303a9e6b75c958614d)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The object key of your of your resource tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-invoicing-invoiceunit-resourcetag.html#cfn-invoicing-invoiceunit-resourcetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The specific value of the resource tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-invoicing-invoiceunit-resourcetag.html#cfn-invoicing-invoiceunit-resourcetag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_invoicing.mixins.CfnInvoiceUnitPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={"linked_accounts": "linkedAccounts"},
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            linked_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``InvoiceUnitRule`` object used to update invoice units.

            :param linked_accounts: The list of ``LINKED_ACCOUNT`` IDs where charges are included within the invoice unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-invoicing-invoiceunit-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_invoicing import mixins as invoicing_mixins
                
                rule_property = invoicing_mixins.CfnInvoiceUnitPropsMixin.RuleProperty(
                    linked_accounts=["linkedAccounts"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29fcedbdd609f2791157b14dcdc4080a9b9095d43e194bba33fc858985c1cd29)
                check_type(argname="argument linked_accounts", value=linked_accounts, expected_type=type_hints["linked_accounts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if linked_accounts is not None:
                self._values["linked_accounts"] = linked_accounts

        @builtins.property
        def linked_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of ``LINKED_ACCOUNT`` IDs where charges are included within the invoice unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-invoicing-invoiceunit-rule.html#cfn-invoicing-invoiceunit-rule-linkedaccounts
            '''
            result = self._values.get("linked_accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnInvoiceUnitMixinProps",
    "CfnInvoiceUnitPropsMixin",
]

publication.publish()

def _typecheckingstub__246767bb4b3dbaeeca5d1e9b515e8ae95ee0a72c3798ad47e8aeb465fe770233(
    *,
    description: typing.Optional[builtins.str] = None,
    invoice_receiver: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resource_tags: typing.Optional[typing.Sequence[typing.Union[CfnInvoiceUnitPropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInvoiceUnitPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tax_inheritance_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6234dd7f3b7e30074227733e41c2e1d4ca8d92fac1f5db96179a1c125db7484d(
    props: typing.Union[CfnInvoiceUnitMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad5f8f5e261221c3c1903a7da190d6be5b0e787a03f1a3734af9be0d7fab75e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755afa79165d918df5548d49eb34a3ce82dec74805ac71c79ab17fc17f33669f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f16f4bb05f4a29184ec315a55c71c4c147403b47d829c303a9e6b75c958614d(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fcedbdd609f2791157b14dcdc4080a9b9095d43e194bba33fc858985c1cd29(
    *,
    linked_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
