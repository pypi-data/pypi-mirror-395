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
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnBrowserSettingsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_encryption_context": "additionalEncryptionContext",
        "browser_policy": "browserPolicy",
        "customer_managed_key": "customerManagedKey",
        "tags": "tags",
        "web_content_filtering_policy": "webContentFilteringPolicy",
    },
)
class CfnBrowserSettingsMixinProps:
    def __init__(
        self,
        *,
        additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        browser_policy: typing.Optional[builtins.str] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        web_content_filtering_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBrowserSettingsPropsMixin.WebContentFilteringPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBrowserSettingsPropsMixin.

        :param additional_encryption_context: Additional encryption context of the browser settings.
        :param browser_policy: A JSON string containing Chrome Enterprise policies that will be applied to all streaming sessions.
        :param customer_managed_key: The custom managed key of the browser settings. *Pattern* : ``^arn:[\\w+=\\/,.@-]+:kms:[a-zA-Z0-9\\-]*:[a-zA-Z0-9]{1,12}:key\\/[a-zA-Z0-9-]+$``
        :param tags: The tags to add to the browser settings resource. A tag is a key-value pair.
        :param web_content_filtering_policy: The policy that specifies which URLs end users are allowed to access or which URLs or domain categories they are restricted from accessing for enhanced security.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-browsersettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            cfn_browser_settings_mixin_props = workspacesweb_mixins.CfnBrowserSettingsMixinProps(
                additional_encryption_context={
                    "additional_encryption_context_key": "additionalEncryptionContext"
                },
                browser_policy="browserPolicy",
                customer_managed_key="customerManagedKey",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                web_content_filtering_policy=workspacesweb_mixins.CfnBrowserSettingsPropsMixin.WebContentFilteringPolicyProperty(
                    allowed_urls=["allowedUrls"],
                    blocked_categories=["blockedCategories"],
                    blocked_urls=["blockedUrls"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d4fabf1f50e3d5fe139f7a7c3637fd5ea75b335e089eaf485d8caa0f9620e9)
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument browser_policy", value=browser_policy, expected_type=type_hints["browser_policy"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument web_content_filtering_policy", value=web_content_filtering_policy, expected_type=type_hints["web_content_filtering_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if browser_policy is not None:
            self._values["browser_policy"] = browser_policy
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if tags is not None:
            self._values["tags"] = tags
        if web_content_filtering_policy is not None:
            self._values["web_content_filtering_policy"] = web_content_filtering_policy

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''Additional encryption context of the browser settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-browsersettings.html#cfn-workspacesweb-browsersettings-additionalencryptioncontext
        '''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def browser_policy(self) -> typing.Optional[builtins.str]:
        '''A JSON string containing Chrome Enterprise policies that will be applied to all streaming sessions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-browsersettings.html#cfn-workspacesweb-browsersettings-browserpolicy
        '''
        result = self._values.get("browser_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_managed_key(self) -> typing.Optional[builtins.str]:
        '''The custom managed key of the browser settings.

        *Pattern* : ``^arn:[\\w+=\\/,.@-]+:kms:[a-zA-Z0-9\\-]*:[a-zA-Z0-9]{1,12}:key\\/[a-zA-Z0-9-]+$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-browsersettings.html#cfn-workspacesweb-browsersettings-customermanagedkey
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the browser settings resource.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-browsersettings.html#cfn-workspacesweb-browsersettings-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def web_content_filtering_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserSettingsPropsMixin.WebContentFilteringPolicyProperty"]]:
        '''The policy that specifies which URLs end users are allowed to access or which URLs or domain categories they are restricted from accessing for enhanced security.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-browsersettings.html#cfn-workspacesweb-browsersettings-webcontentfilteringpolicy
        '''
        result = self._values.get("web_content_filtering_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBrowserSettingsPropsMixin.WebContentFilteringPolicyProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBrowserSettingsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBrowserSettingsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnBrowserSettingsPropsMixin",
):
    '''This resource specifies browser settings that can be associated with a web portal.

    Once associated with a web portal, browser settings control how the browser will behave once a user starts a streaming session for the web portal.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-browsersettings.html
    :cloudformationResource: AWS::WorkSpacesWeb::BrowserSettings
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        cfn_browser_settings_props_mixin = workspacesweb_mixins.CfnBrowserSettingsPropsMixin(workspacesweb_mixins.CfnBrowserSettingsMixinProps(
            additional_encryption_context={
                "additional_encryption_context_key": "additionalEncryptionContext"
            },
            browser_policy="browserPolicy",
            customer_managed_key="customerManagedKey",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            web_content_filtering_policy=workspacesweb_mixins.CfnBrowserSettingsPropsMixin.WebContentFilteringPolicyProperty(
                allowed_urls=["allowedUrls"],
                blocked_categories=["blockedCategories"],
                blocked_urls=["blockedUrls"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBrowserSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::BrowserSettings``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4bf87ddd8a51749b1417576d841be5e7fa4cb808db653dc47b4e656486d65ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bad683d781e1be73810d80efcc62bff4f00cc962a3ce1b27df9a35b4c42586d0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb735cae411f6da12d21c3f775ab7ac702325741edc80d65e401d57bd85f7aa6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBrowserSettingsMixinProps:
        return typing.cast(CfnBrowserSettingsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnBrowserSettingsPropsMixin.WebContentFilteringPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_urls": "allowedUrls",
            "blocked_categories": "blockedCategories",
            "blocked_urls": "blockedUrls",
        },
    )
    class WebContentFilteringPolicyProperty:
        def __init__(
            self,
            *,
            allowed_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
            blocked_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
            blocked_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The policy that specifies which URLs end users are allowed to access or which URLs or domain categories they are restricted from accessing for enhanced security.

            :param allowed_urls: URLs and domains that are always accessible to end users.
            :param blocked_categories: Categories of websites that are blocked on the end user's browsers.
            :param blocked_urls: URLs and domains that end users cannot access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-browsersettings-webcontentfilteringpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                web_content_filtering_policy_property = workspacesweb_mixins.CfnBrowserSettingsPropsMixin.WebContentFilteringPolicyProperty(
                    allowed_urls=["allowedUrls"],
                    blocked_categories=["blockedCategories"],
                    blocked_urls=["blockedUrls"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f4933eae949bea1440224977532ee3360641edac598ef486c631a911da74c87)
                check_type(argname="argument allowed_urls", value=allowed_urls, expected_type=type_hints["allowed_urls"])
                check_type(argname="argument blocked_categories", value=blocked_categories, expected_type=type_hints["blocked_categories"])
                check_type(argname="argument blocked_urls", value=blocked_urls, expected_type=type_hints["blocked_urls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_urls is not None:
                self._values["allowed_urls"] = allowed_urls
            if blocked_categories is not None:
                self._values["blocked_categories"] = blocked_categories
            if blocked_urls is not None:
                self._values["blocked_urls"] = blocked_urls

        @builtins.property
        def allowed_urls(self) -> typing.Optional[typing.List[builtins.str]]:
            '''URLs and domains that are always accessible to end users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-browsersettings-webcontentfilteringpolicy.html#cfn-workspacesweb-browsersettings-webcontentfilteringpolicy-allowedurls
            '''
            result = self._values.get("allowed_urls")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def blocked_categories(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Categories of websites that are blocked on the end user's browsers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-browsersettings-webcontentfilteringpolicy.html#cfn-workspacesweb-browsersettings-webcontentfilteringpolicy-blockedcategories
            '''
            result = self._values.get("blocked_categories")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def blocked_urls(self) -> typing.Optional[typing.List[builtins.str]]:
            '''URLs and domains that end users cannot access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-browsersettings-webcontentfilteringpolicy.html#cfn-workspacesweb-browsersettings-webcontentfilteringpolicy-blockedurls
            '''
            result = self._values.get("blocked_urls")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebContentFilteringPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnDataProtectionSettingsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_encryption_context": "additionalEncryptionContext",
        "customer_managed_key": "customerManagedKey",
        "description": "description",
        "display_name": "displayName",
        "inline_redaction_configuration": "inlineRedactionConfiguration",
        "tags": "tags",
    },
)
class CfnDataProtectionSettingsMixinProps:
    def __init__(
        self,
        *,
        additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        inline_redaction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProtectionSettingsPropsMixin.InlineRedactionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataProtectionSettingsPropsMixin.

        :param additional_encryption_context: The additional encryption context of the data protection settings.
        :param customer_managed_key: The customer managed key used to encrypt sensitive information in the data protection settings.
        :param description: The description of the data protection settings.
        :param display_name: The display name of the data protection settings.
        :param inline_redaction_configuration: The inline redaction configuration for the data protection settings.
        :param tags: The tags of the data protection settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-dataprotectionsettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            cfn_data_protection_settings_mixin_props = workspacesweb_mixins.CfnDataProtectionSettingsMixinProps(
                additional_encryption_context={
                    "additional_encryption_context_key": "additionalEncryptionContext"
                },
                customer_managed_key="customerManagedKey",
                description="description",
                display_name="displayName",
                inline_redaction_configuration=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.InlineRedactionConfigurationProperty(
                    global_confidence_level=123,
                    global_enforced_urls=["globalEnforcedUrls"],
                    global_exempt_urls=["globalExemptUrls"],
                    inline_redaction_patterns=[workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.InlineRedactionPatternProperty(
                        built_in_pattern_id="builtInPatternId",
                        confidence_level=123,
                        custom_pattern=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.CustomPatternProperty(
                            keyword_regex="keywordRegex",
                            pattern_description="patternDescription",
                            pattern_name="patternName",
                            pattern_regex="patternRegex"
                        ),
                        enforced_urls=["enforcedUrls"],
                        exempt_urls=["exemptUrls"],
                        redaction_place_holder=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty(
                            redaction_place_holder_text="redactionPlaceHolderText",
                            redaction_place_holder_type="redactionPlaceHolderType"
                        )
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ee5168844c0eee4cd69079bdfebfc0af9e15b61e7c7c47cbd12e0eef65d2ba)
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument inline_redaction_configuration", value=inline_redaction_configuration, expected_type=type_hints["inline_redaction_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if inline_redaction_configuration is not None:
            self._values["inline_redaction_configuration"] = inline_redaction_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The additional encryption context of the data protection settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-dataprotectionsettings.html#cfn-workspacesweb-dataprotectionsettings-additionalencryptioncontext
        '''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def customer_managed_key(self) -> typing.Optional[builtins.str]:
        '''The customer managed key used to encrypt sensitive information in the data protection settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-dataprotectionsettings.html#cfn-workspacesweb-dataprotectionsettings-customermanagedkey
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the data protection settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-dataprotectionsettings.html#cfn-workspacesweb-dataprotectionsettings-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the data protection settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-dataprotectionsettings.html#cfn-workspacesweb-dataprotectionsettings-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_redaction_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProtectionSettingsPropsMixin.InlineRedactionConfigurationProperty"]]:
        '''The inline redaction configuration for the data protection settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-dataprotectionsettings.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionconfiguration
        '''
        result = self._values.get("inline_redaction_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProtectionSettingsPropsMixin.InlineRedactionConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags of the data protection settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-dataprotectionsettings.html#cfn-workspacesweb-dataprotectionsettings-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataProtectionSettingsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataProtectionSettingsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnDataProtectionSettingsPropsMixin",
):
    '''The data protection settings resource that can be associated with a web portal.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-dataprotectionsettings.html
    :cloudformationResource: AWS::WorkSpacesWeb::DataProtectionSettings
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        cfn_data_protection_settings_props_mixin = workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin(workspacesweb_mixins.CfnDataProtectionSettingsMixinProps(
            additional_encryption_context={
                "additional_encryption_context_key": "additionalEncryptionContext"
            },
            customer_managed_key="customerManagedKey",
            description="description",
            display_name="displayName",
            inline_redaction_configuration=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.InlineRedactionConfigurationProperty(
                global_confidence_level=123,
                global_enforced_urls=["globalEnforcedUrls"],
                global_exempt_urls=["globalExemptUrls"],
                inline_redaction_patterns=[workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.InlineRedactionPatternProperty(
                    built_in_pattern_id="builtInPatternId",
                    confidence_level=123,
                    custom_pattern=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.CustomPatternProperty(
                        keyword_regex="keywordRegex",
                        pattern_description="patternDescription",
                        pattern_name="patternName",
                        pattern_regex="patternRegex"
                    ),
                    enforced_urls=["enforcedUrls"],
                    exempt_urls=["exemptUrls"],
                    redaction_place_holder=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty(
                        redaction_place_holder_text="redactionPlaceHolderText",
                        redaction_place_holder_type="redactionPlaceHolderType"
                    )
                )]
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
        props: typing.Union[CfnDataProtectionSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::DataProtectionSettings``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a889ec2493bba40ec6860616b9c5d500fd6e19b120035fb8a796ff73461a7742)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ac626623326c81b0f4d1bd8b86c59d75aedb7e44f668b8ea33ae558338107f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f96dd46edb5ce4f5d32c7bec3c8e7804f0712e31a4b76275019d5956cc48b9e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataProtectionSettingsMixinProps:
        return typing.cast(CfnDataProtectionSettingsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnDataProtectionSettingsPropsMixin.CustomPatternProperty",
        jsii_struct_bases=[],
        name_mapping={
            "keyword_regex": "keywordRegex",
            "pattern_description": "patternDescription",
            "pattern_name": "patternName",
            "pattern_regex": "patternRegex",
        },
    )
    class CustomPatternProperty:
        def __init__(
            self,
            *,
            keyword_regex: typing.Optional[builtins.str] = None,
            pattern_description: typing.Optional[builtins.str] = None,
            pattern_name: typing.Optional[builtins.str] = None,
            pattern_regex: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The pattern configuration for redacting custom data types in session.

            :param keyword_regex: The keyword regex for the customer pattern. After there is a match to the pattern regex, the keyword regex is used to search within the proximity of the match. If there is a keyword match, then the match is confirmed. If no keyword regex is provided, the pattern regex match will automatically be confirmed. The format must follow JavaScript regex format. The pattern must be enclosed between slashes, and can have flags behind the second slash. For example, “/ab+c/gi”
            :param pattern_description: The pattern description for the customer pattern.
            :param pattern_name: The pattern name for the custom pattern.
            :param pattern_regex: The pattern regex for the customer pattern. The format must follow JavaScript regex format. The pattern must be enclosed between slashes, and can have flags behind the second slash. For example: “/ab+c/gi”.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-custompattern.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                custom_pattern_property = workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.CustomPatternProperty(
                    keyword_regex="keywordRegex",
                    pattern_description="patternDescription",
                    pattern_name="patternName",
                    pattern_regex="patternRegex"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bfce9e4ca2de910f84f6f89b19f66a5f78806801762f0ecb69eb4185528a5a01)
                check_type(argname="argument keyword_regex", value=keyword_regex, expected_type=type_hints["keyword_regex"])
                check_type(argname="argument pattern_description", value=pattern_description, expected_type=type_hints["pattern_description"])
                check_type(argname="argument pattern_name", value=pattern_name, expected_type=type_hints["pattern_name"])
                check_type(argname="argument pattern_regex", value=pattern_regex, expected_type=type_hints["pattern_regex"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if keyword_regex is not None:
                self._values["keyword_regex"] = keyword_regex
            if pattern_description is not None:
                self._values["pattern_description"] = pattern_description
            if pattern_name is not None:
                self._values["pattern_name"] = pattern_name
            if pattern_regex is not None:
                self._values["pattern_regex"] = pattern_regex

        @builtins.property
        def keyword_regex(self) -> typing.Optional[builtins.str]:
            '''The keyword regex for the customer pattern.

            After there is a match to the pattern regex, the keyword regex is used to search within the proximity of the match. If there is a keyword match, then the match is confirmed. If no keyword regex is provided, the pattern regex match will automatically be confirmed. The format must follow JavaScript regex format. The pattern must be enclosed between slashes, and can have flags behind the second slash. For example, “/ab+c/gi”

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-custompattern.html#cfn-workspacesweb-dataprotectionsettings-custompattern-keywordregex
            '''
            result = self._values.get("keyword_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern_description(self) -> typing.Optional[builtins.str]:
            '''The pattern description for the customer pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-custompattern.html#cfn-workspacesweb-dataprotectionsettings-custompattern-patterndescription
            '''
            result = self._values.get("pattern_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern_name(self) -> typing.Optional[builtins.str]:
            '''The pattern name for the custom pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-custompattern.html#cfn-workspacesweb-dataprotectionsettings-custompattern-patternname
            '''
            result = self._values.get("pattern_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern_regex(self) -> typing.Optional[builtins.str]:
            '''The pattern regex for the customer pattern.

            The format must follow JavaScript regex format. The pattern must be enclosed between slashes, and can have flags behind the second slash. For example: “/ab+c/gi”.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-custompattern.html#cfn-workspacesweb-dataprotectionsettings-custompattern-patternregex
            '''
            result = self._values.get("pattern_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPatternProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnDataProtectionSettingsPropsMixin.InlineRedactionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "global_confidence_level": "globalConfidenceLevel",
            "global_enforced_urls": "globalEnforcedUrls",
            "global_exempt_urls": "globalExemptUrls",
            "inline_redaction_patterns": "inlineRedactionPatterns",
        },
    )
    class InlineRedactionConfigurationProperty:
        def __init__(
            self,
            *,
            global_confidence_level: typing.Optional[jsii.Number] = None,
            global_enforced_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
            global_exempt_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
            inline_redaction_patterns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProtectionSettingsPropsMixin.InlineRedactionPatternProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration for in-session inline redaction.

            :param global_confidence_level: The global confidence level for the inline redaction configuration. This indicates the certainty of data type matches in the redaction process. Confidence level 3 means high confidence, and requires a formatted text pattern match in order for content to be redacted. Confidence level 2 means medium confidence, and redaction considers both formatted and unformatted text, and adds keyword associate to the logic. Confidence level 1 means low confidence, and redaction is enforced for both formatted pattern + unformatted pattern without keyword. This is applied to patterns that do not have a pattern-level confidence level. Defaults to confidence level 2.
            :param global_enforced_urls: The global enforced URL configuration for the inline redaction configuration. This is applied to patterns that do not have a pattern-level enforced URL list.
            :param global_exempt_urls: The global exempt URL configuration for the inline redaction configuration. This is applied to patterns that do not have a pattern-level exempt URL list.
            :param inline_redaction_patterns: The inline redaction patterns to be enabled for the inline redaction configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                inline_redaction_configuration_property = workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.InlineRedactionConfigurationProperty(
                    global_confidence_level=123,
                    global_enforced_urls=["globalEnforcedUrls"],
                    global_exempt_urls=["globalExemptUrls"],
                    inline_redaction_patterns=[workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.InlineRedactionPatternProperty(
                        built_in_pattern_id="builtInPatternId",
                        confidence_level=123,
                        custom_pattern=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.CustomPatternProperty(
                            keyword_regex="keywordRegex",
                            pattern_description="patternDescription",
                            pattern_name="patternName",
                            pattern_regex="patternRegex"
                        ),
                        enforced_urls=["enforcedUrls"],
                        exempt_urls=["exemptUrls"],
                        redaction_place_holder=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty(
                            redaction_place_holder_text="redactionPlaceHolderText",
                            redaction_place_holder_type="redactionPlaceHolderType"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b30206064b71d63613fe98bbd2ae73b2ad3ea31009ae49094ab8329c1062c1a)
                check_type(argname="argument global_confidence_level", value=global_confidence_level, expected_type=type_hints["global_confidence_level"])
                check_type(argname="argument global_enforced_urls", value=global_enforced_urls, expected_type=type_hints["global_enforced_urls"])
                check_type(argname="argument global_exempt_urls", value=global_exempt_urls, expected_type=type_hints["global_exempt_urls"])
                check_type(argname="argument inline_redaction_patterns", value=inline_redaction_patterns, expected_type=type_hints["inline_redaction_patterns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if global_confidence_level is not None:
                self._values["global_confidence_level"] = global_confidence_level
            if global_enforced_urls is not None:
                self._values["global_enforced_urls"] = global_enforced_urls
            if global_exempt_urls is not None:
                self._values["global_exempt_urls"] = global_exempt_urls
            if inline_redaction_patterns is not None:
                self._values["inline_redaction_patterns"] = inline_redaction_patterns

        @builtins.property
        def global_confidence_level(self) -> typing.Optional[jsii.Number]:
            '''The global confidence level for the inline redaction configuration.

            This indicates the certainty of data type matches in the redaction process. Confidence level 3 means high confidence, and requires a formatted text pattern match in order for content to be redacted. Confidence level 2 means medium confidence, and redaction considers both formatted and unformatted text, and adds keyword associate to the logic. Confidence level 1 means low confidence, and redaction is enforced for both formatted pattern + unformatted pattern without keyword. This is applied to patterns that do not have a pattern-level confidence level. Defaults to confidence level 2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionconfiguration.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionconfiguration-globalconfidencelevel
            '''
            result = self._values.get("global_confidence_level")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def global_enforced_urls(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The global enforced URL configuration for the inline redaction configuration.

            This is applied to patterns that do not have a pattern-level enforced URL list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionconfiguration.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionconfiguration-globalenforcedurls
            '''
            result = self._values.get("global_enforced_urls")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def global_exempt_urls(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The global exempt URL configuration for the inline redaction configuration.

            This is applied to patterns that do not have a pattern-level exempt URL list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionconfiguration.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionconfiguration-globalexempturls
            '''
            result = self._values.get("global_exempt_urls")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def inline_redaction_patterns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProtectionSettingsPropsMixin.InlineRedactionPatternProperty"]]]]:
            '''The inline redaction patterns to be enabled for the inline redaction configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionconfiguration.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionconfiguration-inlineredactionpatterns
            '''
            result = self._values.get("inline_redaction_patterns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProtectionSettingsPropsMixin.InlineRedactionPatternProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InlineRedactionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnDataProtectionSettingsPropsMixin.InlineRedactionPatternProperty",
        jsii_struct_bases=[],
        name_mapping={
            "built_in_pattern_id": "builtInPatternId",
            "confidence_level": "confidenceLevel",
            "custom_pattern": "customPattern",
            "enforced_urls": "enforcedUrls",
            "exempt_urls": "exemptUrls",
            "redaction_place_holder": "redactionPlaceHolder",
        },
    )
    class InlineRedactionPatternProperty:
        def __init__(
            self,
            *,
            built_in_pattern_id: typing.Optional[builtins.str] = None,
            confidence_level: typing.Optional[jsii.Number] = None,
            custom_pattern: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProtectionSettingsPropsMixin.CustomPatternProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enforced_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
            exempt_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
            redaction_place_holder: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The set of patterns that determine the data types redacted in session.

            :param built_in_pattern_id: The built-in pattern from the list of preconfigured patterns. Either a customPattern or builtInPatternId is required. To view the entire list of data types and their corresponding built-in pattern IDs, see `Base inline redaction <https://docs.aws.amazon.com/workspaces-web/latest/adminguide/base-inline-redaction.html>`_ .
            :param confidence_level: The confidence level for inline redaction pattern. This indicates the certainty of data type matches in the redaction process. Confidence level 3 means high confidence, and requires a formatted text pattern match in order for content to be redacted. Confidence level 2 means medium confidence, and redaction considers both formatted and unformatted text, and adds keyword associate to the logic. Confidence level 1 means low confidence, and redaction is enforced for both formatted pattern + unformatted pattern without keyword. This overrides the global confidence level.
            :param custom_pattern: The configuration for a custom pattern. Either a customPattern or builtInPatternId is required.
            :param enforced_urls: The enforced URL configuration for the inline redaction pattern. This will override the global enforced URL configuration.
            :param exempt_urls: The exempt URL configuration for the inline redaction pattern. This will override the global exempt URL configuration for the inline redaction pattern.
            :param redaction_place_holder: The redaction placeholder that will replace the redacted text in session for the inline redaction pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionpattern.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                inline_redaction_pattern_property = workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.InlineRedactionPatternProperty(
                    built_in_pattern_id="builtInPatternId",
                    confidence_level=123,
                    custom_pattern=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.CustomPatternProperty(
                        keyword_regex="keywordRegex",
                        pattern_description="patternDescription",
                        pattern_name="patternName",
                        pattern_regex="patternRegex"
                    ),
                    enforced_urls=["enforcedUrls"],
                    exempt_urls=["exemptUrls"],
                    redaction_place_holder=workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty(
                        redaction_place_holder_text="redactionPlaceHolderText",
                        redaction_place_holder_type="redactionPlaceHolderType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72e7461a415703014ac29a1cd73a51ee5154c7de669ba8240673c883cd6acce9)
                check_type(argname="argument built_in_pattern_id", value=built_in_pattern_id, expected_type=type_hints["built_in_pattern_id"])
                check_type(argname="argument confidence_level", value=confidence_level, expected_type=type_hints["confidence_level"])
                check_type(argname="argument custom_pattern", value=custom_pattern, expected_type=type_hints["custom_pattern"])
                check_type(argname="argument enforced_urls", value=enforced_urls, expected_type=type_hints["enforced_urls"])
                check_type(argname="argument exempt_urls", value=exempt_urls, expected_type=type_hints["exempt_urls"])
                check_type(argname="argument redaction_place_holder", value=redaction_place_holder, expected_type=type_hints["redaction_place_holder"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if built_in_pattern_id is not None:
                self._values["built_in_pattern_id"] = built_in_pattern_id
            if confidence_level is not None:
                self._values["confidence_level"] = confidence_level
            if custom_pattern is not None:
                self._values["custom_pattern"] = custom_pattern
            if enforced_urls is not None:
                self._values["enforced_urls"] = enforced_urls
            if exempt_urls is not None:
                self._values["exempt_urls"] = exempt_urls
            if redaction_place_holder is not None:
                self._values["redaction_place_holder"] = redaction_place_holder

        @builtins.property
        def built_in_pattern_id(self) -> typing.Optional[builtins.str]:
            '''The built-in pattern from the list of preconfigured patterns.

            Either a customPattern or builtInPatternId is required. To view the entire list of data types and their corresponding built-in pattern IDs, see `Base inline redaction <https://docs.aws.amazon.com/workspaces-web/latest/adminguide/base-inline-redaction.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionpattern.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionpattern-builtinpatternid
            '''
            result = self._values.get("built_in_pattern_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def confidence_level(self) -> typing.Optional[jsii.Number]:
            '''The confidence level for inline redaction pattern.

            This indicates the certainty of data type matches in the redaction process. Confidence level 3 means high confidence, and requires a formatted text pattern match in order for content to be redacted. Confidence level 2 means medium confidence, and redaction considers both formatted and unformatted text, and adds keyword associate to the logic. Confidence level 1 means low confidence, and redaction is enforced for both formatted pattern + unformatted pattern without keyword. This overrides the global confidence level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionpattern.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionpattern-confidencelevel
            '''
            result = self._values.get("confidence_level")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def custom_pattern(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProtectionSettingsPropsMixin.CustomPatternProperty"]]:
            '''The configuration for a custom pattern.

            Either a customPattern or builtInPatternId is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionpattern.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionpattern-custompattern
            '''
            result = self._values.get("custom_pattern")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProtectionSettingsPropsMixin.CustomPatternProperty"]], result)

        @builtins.property
        def enforced_urls(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The enforced URL configuration for the inline redaction pattern.

            This will override the global enforced URL configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionpattern.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionpattern-enforcedurls
            '''
            result = self._values.get("enforced_urls")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exempt_urls(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The exempt URL configuration for the inline redaction pattern.

            This will override the global exempt URL configuration for the inline redaction pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionpattern.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionpattern-exempturls
            '''
            result = self._values.get("exempt_urls")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def redaction_place_holder(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty"]]:
            '''The redaction placeholder that will replace the redacted text in session for the inline redaction pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-inlineredactionpattern.html#cfn-workspacesweb-dataprotectionsettings-inlineredactionpattern-redactionplaceholder
            '''
            result = self._values.get("redaction_place_holder")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InlineRedactionPatternProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "redaction_place_holder_text": "redactionPlaceHolderText",
            "redaction_place_holder_type": "redactionPlaceHolderType",
        },
    )
    class RedactionPlaceHolderProperty:
        def __init__(
            self,
            *,
            redaction_place_holder_text: typing.Optional[builtins.str] = None,
            redaction_place_holder_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The redaction placeholder that will replace the redacted text in session.

            :param redaction_place_holder_text: The redaction placeholder text that will replace the redacted text in session for the custom text redaction placeholder type.
            :param redaction_place_holder_type: The redaction placeholder type that will replace the redacted text in session.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-redactionplaceholder.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                redaction_place_holder_property = workspacesweb_mixins.CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty(
                    redaction_place_holder_text="redactionPlaceHolderText",
                    redaction_place_holder_type="redactionPlaceHolderType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__68131c1aca5625aa4c1f2ad1d82eb7a5efc2597589f69c3417711ff0a66e6706)
                check_type(argname="argument redaction_place_holder_text", value=redaction_place_holder_text, expected_type=type_hints["redaction_place_holder_text"])
                check_type(argname="argument redaction_place_holder_type", value=redaction_place_holder_type, expected_type=type_hints["redaction_place_holder_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if redaction_place_holder_text is not None:
                self._values["redaction_place_holder_text"] = redaction_place_holder_text
            if redaction_place_holder_type is not None:
                self._values["redaction_place_holder_type"] = redaction_place_holder_type

        @builtins.property
        def redaction_place_holder_text(self) -> typing.Optional[builtins.str]:
            '''The redaction placeholder text that will replace the redacted text in session for the custom text redaction placeholder type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-redactionplaceholder.html#cfn-workspacesweb-dataprotectionsettings-redactionplaceholder-redactionplaceholdertext
            '''
            result = self._values.get("redaction_place_holder_text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def redaction_place_holder_type(self) -> typing.Optional[builtins.str]:
            '''The redaction placeholder type that will replace the redacted text in session.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-dataprotectionsettings-redactionplaceholder.html#cfn-workspacesweb-dataprotectionsettings-redactionplaceholder-redactionplaceholdertype
            '''
            result = self._values.get("redaction_place_holder_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedactionPlaceHolderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnIdentityProviderMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_provider_details": "identityProviderDetails",
        "identity_provider_name": "identityProviderName",
        "identity_provider_type": "identityProviderType",
        "portal_arn": "portalArn",
        "tags": "tags",
    },
)
class CfnIdentityProviderMixinProps:
    def __init__(
        self,
        *,
        identity_provider_details: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        identity_provider_name: typing.Optional[builtins.str] = None,
        identity_provider_type: typing.Optional[builtins.str] = None,
        portal_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnIdentityProviderPropsMixin.

        :param identity_provider_details: The identity provider details. The following list describes the provider detail keys for each identity provider type. - For Google and Login with Amazon: - ``client_id`` - ``client_secret`` - ``authorize_scopes`` - For Facebook: - ``client_id`` - ``client_secret`` - ``authorize_scopes`` - ``api_version`` - For Sign in with Apple: - ``client_id`` - ``team_id`` - ``key_id`` - ``private_key`` - ``authorize_scopes`` - For OIDC providers: - ``client_id`` - ``client_secret`` - ``attributes_request_method`` - ``oidc_issuer`` - ``authorize_scopes`` - ``authorize_url`` *if not available from discovery URL specified by oidc_issuer key* - ``token_url`` *if not available from discovery URL specified by oidc_issuer key* - ``attributes_url`` *if not available from discovery URL specified by oidc_issuer key* - ``jwks_uri`` *if not available from discovery URL specified by oidc_issuer key* - For SAML providers: - ``MetadataFile`` OR ``MetadataURL`` - ``IDPSignout`` (boolean) *optional* - ``IDPInit`` (boolean) *optional* - ``RequestSigningAlgorithm`` (string) *optional* - Only accepts ``rsa-sha256`` - ``EncryptedResponses`` (boolean) *optional*
        :param identity_provider_name: The identity provider name.
        :param identity_provider_type: The identity provider type.
        :param portal_arn: The ARN of the identity provider.
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-identityprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            cfn_identity_provider_mixin_props = workspacesweb_mixins.CfnIdentityProviderMixinProps(
                identity_provider_details={
                    "identity_provider_details_key": "identityProviderDetails"
                },
                identity_provider_name="identityProviderName",
                identity_provider_type="identityProviderType",
                portal_arn="portalArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a01b72433b6fb98dde81e4cfe784b2da72027a025cb91e08b1a6a36dc61cb0)
            check_type(argname="argument identity_provider_details", value=identity_provider_details, expected_type=type_hints["identity_provider_details"])
            check_type(argname="argument identity_provider_name", value=identity_provider_name, expected_type=type_hints["identity_provider_name"])
            check_type(argname="argument identity_provider_type", value=identity_provider_type, expected_type=type_hints["identity_provider_type"])
            check_type(argname="argument portal_arn", value=portal_arn, expected_type=type_hints["portal_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_provider_details is not None:
            self._values["identity_provider_details"] = identity_provider_details
        if identity_provider_name is not None:
            self._values["identity_provider_name"] = identity_provider_name
        if identity_provider_type is not None:
            self._values["identity_provider_type"] = identity_provider_type
        if portal_arn is not None:
            self._values["portal_arn"] = portal_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def identity_provider_details(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The identity provider details. The following list describes the provider detail keys for each identity provider type.

        - For Google and Login with Amazon:
        - ``client_id``
        - ``client_secret``
        - ``authorize_scopes``
        - For Facebook:
        - ``client_id``
        - ``client_secret``
        - ``authorize_scopes``
        - ``api_version``
        - For Sign in with Apple:
        - ``client_id``
        - ``team_id``
        - ``key_id``
        - ``private_key``
        - ``authorize_scopes``
        - For OIDC providers:
        - ``client_id``
        - ``client_secret``
        - ``attributes_request_method``
        - ``oidc_issuer``
        - ``authorize_scopes``
        - ``authorize_url`` *if not available from discovery URL specified by oidc_issuer key*
        - ``token_url`` *if not available from discovery URL specified by oidc_issuer key*
        - ``attributes_url`` *if not available from discovery URL specified by oidc_issuer key*
        - ``jwks_uri`` *if not available from discovery URL specified by oidc_issuer key*
        - For SAML providers:
        - ``MetadataFile`` OR ``MetadataURL``
        - ``IDPSignout`` (boolean) *optional*
        - ``IDPInit`` (boolean) *optional*
        - ``RequestSigningAlgorithm`` (string) *optional* - Only accepts ``rsa-sha256``
        - ``EncryptedResponses`` (boolean) *optional*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-identityprovider.html#cfn-workspacesweb-identityprovider-identityproviderdetails
        '''
        result = self._values.get("identity_provider_details")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def identity_provider_name(self) -> typing.Optional[builtins.str]:
        '''The identity provider name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-identityprovider.html#cfn-workspacesweb-identityprovider-identityprovidername
        '''
        result = self._values.get("identity_provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_type(self) -> typing.Optional[builtins.str]:
        '''The identity provider type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-identityprovider.html#cfn-workspacesweb-identityprovider-identityprovidertype
        '''
        result = self._values.get("identity_provider_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the identity provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-identityprovider.html#cfn-workspacesweb-identityprovider-portalarn
        '''
        result = self._values.get("portal_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-identityprovider.html#cfn-workspacesweb-identityprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentityProviderMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdentityProviderPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnIdentityProviderPropsMixin",
):
    '''This resource specifies an identity provider that is then associated with a web portal.

    This resource is not required if your portal's ``AuthenticationType`` is IAM Identity Center.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-identityprovider.html
    :cloudformationResource: AWS::WorkSpacesWeb::IdentityProvider
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        cfn_identity_provider_props_mixin = workspacesweb_mixins.CfnIdentityProviderPropsMixin(workspacesweb_mixins.CfnIdentityProviderMixinProps(
            identity_provider_details={
                "identity_provider_details_key": "identityProviderDetails"
            },
            identity_provider_name="identityProviderName",
            identity_provider_type="identityProviderType",
            portal_arn="portalArn",
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
        props: typing.Union[CfnIdentityProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::IdentityProvider``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2478c71da2277107ac09a88369f72f1637169307ec3f8c1a6e451754e2bfc6b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e08f1fc12c127abd5684889d43e8932aa96f35768fb8ff5c69903f70355f477)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a327355ddf516fab4bafb1382b8b81dc43af633c6fe7004f9ffcf2c47349a8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdentityProviderMixinProps:
        return typing.cast(CfnIdentityProviderMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnIpAccessSettingsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_encryption_context": "additionalEncryptionContext",
        "customer_managed_key": "customerManagedKey",
        "description": "description",
        "display_name": "displayName",
        "ip_rules": "ipRules",
        "tags": "tags",
    },
)
class CfnIpAccessSettingsMixinProps:
    def __init__(
        self,
        *,
        additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        ip_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIpAccessSettingsPropsMixin.IpRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnIpAccessSettingsPropsMixin.

        :param additional_encryption_context: Additional encryption context of the IP access settings.
        :param customer_managed_key: The custom managed key of the IP access settings. *Pattern* : ``^arn:[\\w+=\\/,.@-]+:kms:[a-zA-Z0-9\\-]*:[a-zA-Z0-9]{1,12}:key\\/[a-zA-Z0-9-]+$``
        :param description: The description of the IP access settings.
        :param display_name: The display name of the IP access settings.
        :param ip_rules: The IP rules of the IP access settings.
        :param tags: The tags to add to the IP access settings resource. A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-ipaccesssettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            cfn_ip_access_settings_mixin_props = workspacesweb_mixins.CfnIpAccessSettingsMixinProps(
                additional_encryption_context={
                    "additional_encryption_context_key": "additionalEncryptionContext"
                },
                customer_managed_key="customerManagedKey",
                description="description",
                display_name="displayName",
                ip_rules=[workspacesweb_mixins.CfnIpAccessSettingsPropsMixin.IpRuleProperty(
                    description="description",
                    ip_range="ipRange"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e24f990f985b880554221704351c3bda020779ccf61e81734f6bb3e061aa34)
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument ip_rules", value=ip_rules, expected_type=type_hints["ip_rules"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if ip_rules is not None:
            self._values["ip_rules"] = ip_rules
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''Additional encryption context of the IP access settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-ipaccesssettings.html#cfn-workspacesweb-ipaccesssettings-additionalencryptioncontext
        '''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def customer_managed_key(self) -> typing.Optional[builtins.str]:
        '''The custom managed key of the IP access settings.

        *Pattern* : ``^arn:[\\w+=\\/,.@-]+:kms:[a-zA-Z0-9\\-]*:[a-zA-Z0-9]{1,12}:key\\/[a-zA-Z0-9-]+$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-ipaccesssettings.html#cfn-workspacesweb-ipaccesssettings-customermanagedkey
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the IP access settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-ipaccesssettings.html#cfn-workspacesweb-ipaccesssettings-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the IP access settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-ipaccesssettings.html#cfn-workspacesweb-ipaccesssettings-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIpAccessSettingsPropsMixin.IpRuleProperty"]]]]:
        '''The IP rules of the IP access settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-ipaccesssettings.html#cfn-workspacesweb-ipaccesssettings-iprules
        '''
        result = self._values.get("ip_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIpAccessSettingsPropsMixin.IpRuleProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the IP access settings resource.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-ipaccesssettings.html#cfn-workspacesweb-ipaccesssettings-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIpAccessSettingsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIpAccessSettingsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnIpAccessSettingsPropsMixin",
):
    '''This resource specifies IP access settings that can be associated with a web portal.

    For more information, see `Set up IP access controls (optional) <https://docs.aws.amazon.com/workspaces-web/latest/adminguide/ip-access-controls.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-ipaccesssettings.html
    :cloudformationResource: AWS::WorkSpacesWeb::IpAccessSettings
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        cfn_ip_access_settings_props_mixin = workspacesweb_mixins.CfnIpAccessSettingsPropsMixin(workspacesweb_mixins.CfnIpAccessSettingsMixinProps(
            additional_encryption_context={
                "additional_encryption_context_key": "additionalEncryptionContext"
            },
            customer_managed_key="customerManagedKey",
            description="description",
            display_name="displayName",
            ip_rules=[workspacesweb_mixins.CfnIpAccessSettingsPropsMixin.IpRuleProperty(
                description="description",
                ip_range="ipRange"
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
        props: typing.Union[CfnIpAccessSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::IpAccessSettings``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7b9b8140881ef9bc0220792cce8829bea6cce1f3646b3bae772b3fb8f66951)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07f6616e961950c3868040854ff9f3cbf6991b4184a54c0c4b92e3f6f2d03040)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0870acf292beaea1022e1c1247b92c37e464f6a0934bae112e4902ecdf8897)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIpAccessSettingsMixinProps:
        return typing.cast(CfnIpAccessSettingsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnIpAccessSettingsPropsMixin.IpRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"description": "description", "ip_range": "ipRange"},
    )
    class IpRuleProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            ip_range: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The IP rules of the IP access settings.

            :param description: The description of the IP rule.
            :param ip_range: The IP range of the IP rule. This can either be a single IP address or a range using CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-ipaccesssettings-iprule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                ip_rule_property = workspacesweb_mixins.CfnIpAccessSettingsPropsMixin.IpRuleProperty(
                    description="description",
                    ip_range="ipRange"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c1bea04f4cb927de329c4cc2ffc4da938f728eebebee1bc9c782f0fc7824ea8)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument ip_range", value=ip_range, expected_type=type_hints["ip_range"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if ip_range is not None:
                self._values["ip_range"] = ip_range

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the IP rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-ipaccesssettings-iprule.html#cfn-workspacesweb-ipaccesssettings-iprule-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ip_range(self) -> typing.Optional[builtins.str]:
            '''The IP range of the IP rule.

            This can either be a single IP address or a range using CIDR notation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-ipaccesssettings-iprule.html#cfn-workspacesweb-ipaccesssettings-iprule-iprange
            '''
            result = self._values.get("ip_range")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnNetworkSettingsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "vpc_id": "vpcId",
    },
)
class CfnNetworkSettingsMixinProps:
    def __init__(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnNetworkSettingsPropsMixin.

        :param security_group_ids: One or more security groups used to control access from streaming instances to your VPC. *Pattern* : ``^[\\w+\\-]+$``
        :param subnet_ids: The subnets in which network interfaces are created to connect streaming instances to your VPC. At least two of these subnets must be in different availability zones. *Pattern* : ``^subnet-([0-9a-f]{8}|[0-9a-f]{17})$``
        :param tags: The tags to add to the network settings resource. A tag is a key-value pair.
        :param vpc_id: The VPC that streaming instances will connect to. *Pattern* : ``^vpc-[0-9a-z]*$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-networksettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            cfn_network_settings_mixin_props = workspacesweb_mixins.CfnNetworkSettingsMixinProps(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35ea1984fe77363d58912ec3eb8c818b565a143b92120d93fefc028f57ec31f)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more security groups used to control access from streaming instances to your VPC.

        *Pattern* : ``^[\\w+\\-]+$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-networksettings.html#cfn-workspacesweb-networksettings-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The subnets in which network interfaces are created to connect streaming instances to your VPC.

        At least two of these subnets must be in different availability zones.

        *Pattern* : ``^subnet-([0-9a-f]{8}|[0-9a-f]{17})$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-networksettings.html#cfn-workspacesweb-networksettings-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the network settings resource.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-networksettings.html#cfn-workspacesweb-networksettings-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The VPC that streaming instances will connect to.

        *Pattern* : ``^vpc-[0-9a-z]*$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-networksettings.html#cfn-workspacesweb-networksettings-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNetworkSettingsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNetworkSettingsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnNetworkSettingsPropsMixin",
):
    '''This resource specifies network settings that can be associated with a web portal.

    Once associated with a web portal, network settings define how streaming instances will connect with your specified VPC.

    The VPC must have default tenancy. VPCs with dedicated tenancy are not supported.

    For availability consideration, you must have at least two subnets created in two different Availability Zones. WorkSpaces Secure Browser is available in a subset of the Availability Zones for each supported Region. For more information, see `Supported Availability Zones <https://docs.aws.amazon.com/workspaces-web/latest/adminguide/availability-zones.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-networksettings.html
    :cloudformationResource: AWS::WorkSpacesWeb::NetworkSettings
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        cfn_network_settings_props_mixin = workspacesweb_mixins.CfnNetworkSettingsPropsMixin(workspacesweb_mixins.CfnNetworkSettingsMixinProps(
            security_group_ids=["securityGroupIds"],
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnNetworkSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::NetworkSettings``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a073c1c1549339249defb6a86a97f4c2cc789613f8dc32aad1a6f30b740f7b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3784e98999e79384bcb210552777743f90a693f1324da58dfbd3fe8d0890c48)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a438a76046457807e2070c549da0e9dfa1366b4e1f8676f859594f1f6a756b4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNetworkSettingsMixinProps:
        return typing.cast(CfnNetworkSettingsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnPortalMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_encryption_context": "additionalEncryptionContext",
        "authentication_type": "authenticationType",
        "browser_settings_arn": "browserSettingsArn",
        "customer_managed_key": "customerManagedKey",
        "data_protection_settings_arn": "dataProtectionSettingsArn",
        "display_name": "displayName",
        "instance_type": "instanceType",
        "ip_access_settings_arn": "ipAccessSettingsArn",
        "max_concurrent_sessions": "maxConcurrentSessions",
        "network_settings_arn": "networkSettingsArn",
        "session_logger_arn": "sessionLoggerArn",
        "tags": "tags",
        "trust_store_arn": "trustStoreArn",
        "user_access_logging_settings_arn": "userAccessLoggingSettingsArn",
        "user_settings_arn": "userSettingsArn",
    },
)
class CfnPortalMixinProps:
    def __init__(
        self,
        *,
        additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        authentication_type: typing.Optional[builtins.str] = None,
        browser_settings_arn: typing.Optional[builtins.str] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        data_protection_settings_arn: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        ip_access_settings_arn: typing.Optional[builtins.str] = None,
        max_concurrent_sessions: typing.Optional[jsii.Number] = None,
        network_settings_arn: typing.Optional[builtins.str] = None,
        session_logger_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trust_store_arn: typing.Optional[builtins.str] = None,
        user_access_logging_settings_arn: typing.Optional[builtins.str] = None,
        user_settings_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPortalPropsMixin.

        :param additional_encryption_context: The additional encryption context of the portal.
        :param authentication_type: The type of authentication integration points used when signing into the web portal. Defaults to ``Standard`` . ``Standard`` web portals are authenticated directly through your identity provider (IdP). User and group access to your web portal is controlled through your IdP. You need to include an IdP resource in your template to integrate your IdP with your web portal. Completing the configuration for your IdP requires exchanging WorkSpaces Secure Browser’s SP metadata with your IdP’s IdP metadata. If your IdP requires the SP metadata first before returning the IdP metadata, you should follow these steps: 1. Create and deploy a CloudFormation template with a ``Standard`` portal with no ``IdentityProvider`` resource. 2. Retrieve the SP metadata using ``Fn:GetAtt`` , the WorkSpaces Secure Browser console, or by the calling the ``GetPortalServiceProviderMetadata`` API. 3. Submit the data to your IdP. 4. Add an ``IdentityProvider`` resource to your CloudFormation template. ``IAM Identity Center`` web portals are authenticated through AWS IAM Identity Center . They provide additional features, such as IdP-initiated authentication. Identity sources (including external identity provider integration) and other identity provider information must be configured in IAM Identity Center . User and group assignment must be done through the WorkSpaces Secure Browser console. These cannot be configured in CloudFormation.
        :param browser_settings_arn: The ARN of the browser settings that is associated with this web portal.
        :param customer_managed_key: The customer managed key of the web portal. *Pattern* : ``^arn:[\\w+=\\/,.@-]+:kms:[a-zA-Z0-9\\-]*:[a-zA-Z0-9]{1,12}:key\\/[a-zA-Z0-9-]+$``
        :param data_protection_settings_arn: The ARN of the data protection settings.
        :param display_name: The name of the web portal.
        :param instance_type: The type and resources of the underlying instance.
        :param ip_access_settings_arn: The ARN of the IP access settings that is associated with the web portal.
        :param max_concurrent_sessions: The maximum number of concurrent sessions for the portal.
        :param network_settings_arn: The ARN of the network settings that is associated with the web portal.
        :param session_logger_arn: The ARN of the session logger that is associated with the portal.
        :param tags: The tags to add to the web portal. A tag is a key-value pair.
        :param trust_store_arn: The ARN of the trust store that is associated with the web portal.
        :param user_access_logging_settings_arn: The ARN of the user access logging settings that is associated with the web portal.
        :param user_settings_arn: The ARN of the user settings that is associated with the web portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            cfn_portal_mixin_props = workspacesweb_mixins.CfnPortalMixinProps(
                additional_encryption_context={
                    "additional_encryption_context_key": "additionalEncryptionContext"
                },
                authentication_type="authenticationType",
                browser_settings_arn="browserSettingsArn",
                customer_managed_key="customerManagedKey",
                data_protection_settings_arn="dataProtectionSettingsArn",
                display_name="displayName",
                instance_type="instanceType",
                ip_access_settings_arn="ipAccessSettingsArn",
                max_concurrent_sessions=123,
                network_settings_arn="networkSettingsArn",
                session_logger_arn="sessionLoggerArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trust_store_arn="trustStoreArn",
                user_access_logging_settings_arn="userAccessLoggingSettingsArn",
                user_settings_arn="userSettingsArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ed497d64c938f4f0bd9fa3893fda7435e9b337e8462c2eb8a7c816c9187358)
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument browser_settings_arn", value=browser_settings_arn, expected_type=type_hints["browser_settings_arn"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument data_protection_settings_arn", value=data_protection_settings_arn, expected_type=type_hints["data_protection_settings_arn"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument ip_access_settings_arn", value=ip_access_settings_arn, expected_type=type_hints["ip_access_settings_arn"])
            check_type(argname="argument max_concurrent_sessions", value=max_concurrent_sessions, expected_type=type_hints["max_concurrent_sessions"])
            check_type(argname="argument network_settings_arn", value=network_settings_arn, expected_type=type_hints["network_settings_arn"])
            check_type(argname="argument session_logger_arn", value=session_logger_arn, expected_type=type_hints["session_logger_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trust_store_arn", value=trust_store_arn, expected_type=type_hints["trust_store_arn"])
            check_type(argname="argument user_access_logging_settings_arn", value=user_access_logging_settings_arn, expected_type=type_hints["user_access_logging_settings_arn"])
            check_type(argname="argument user_settings_arn", value=user_settings_arn, expected_type=type_hints["user_settings_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if authentication_type is not None:
            self._values["authentication_type"] = authentication_type
        if browser_settings_arn is not None:
            self._values["browser_settings_arn"] = browser_settings_arn
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if data_protection_settings_arn is not None:
            self._values["data_protection_settings_arn"] = data_protection_settings_arn
        if display_name is not None:
            self._values["display_name"] = display_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if ip_access_settings_arn is not None:
            self._values["ip_access_settings_arn"] = ip_access_settings_arn
        if max_concurrent_sessions is not None:
            self._values["max_concurrent_sessions"] = max_concurrent_sessions
        if network_settings_arn is not None:
            self._values["network_settings_arn"] = network_settings_arn
        if session_logger_arn is not None:
            self._values["session_logger_arn"] = session_logger_arn
        if tags is not None:
            self._values["tags"] = tags
        if trust_store_arn is not None:
            self._values["trust_store_arn"] = trust_store_arn
        if user_access_logging_settings_arn is not None:
            self._values["user_access_logging_settings_arn"] = user_access_logging_settings_arn
        if user_settings_arn is not None:
            self._values["user_settings_arn"] = user_settings_arn

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The additional encryption context of the portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-additionalencryptioncontext
        '''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def authentication_type(self) -> typing.Optional[builtins.str]:
        '''The type of authentication integration points used when signing into the web portal. Defaults to ``Standard`` .

        ``Standard`` web portals are authenticated directly through your identity provider (IdP). User and group access to your web portal is controlled through your IdP. You need to include an IdP resource in your template to integrate your IdP with your web portal. Completing the configuration for your IdP requires exchanging WorkSpaces Secure Browser’s SP metadata with your IdP’s IdP metadata. If your IdP requires the SP metadata first before returning the IdP metadata, you should follow these steps:

        1. Create and deploy a CloudFormation template with a ``Standard`` portal with no ``IdentityProvider`` resource.
        2. Retrieve the SP metadata using ``Fn:GetAtt`` , the WorkSpaces Secure Browser console, or by the calling the ``GetPortalServiceProviderMetadata`` API.
        3. Submit the data to your IdP.
        4. Add an ``IdentityProvider`` resource to your CloudFormation template.

        ``IAM Identity Center`` web portals are authenticated through AWS IAM Identity Center . They provide additional features, such as IdP-initiated authentication. Identity sources (including external identity provider integration) and other identity provider information must be configured in IAM Identity Center . User and group assignment must be done through the WorkSpaces Secure Browser console. These cannot be configured in CloudFormation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-authenticationtype
        '''
        result = self._values.get("authentication_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def browser_settings_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the browser settings that is associated with this web portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-browsersettingsarn
        '''
        result = self._values.get("browser_settings_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_managed_key(self) -> typing.Optional[builtins.str]:
        '''The customer managed key of the web portal.

        *Pattern* : ``^arn:[\\w+=\\/,.@-]+:kms:[a-zA-Z0-9\\-]*:[a-zA-Z0-9]{1,12}:key\\/[a-zA-Z0-9-]+$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-customermanagedkey
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_protection_settings_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the data protection settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-dataprotectionsettingsarn
        '''
        result = self._values.get("data_protection_settings_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the web portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The type and resources of the underlying instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_access_settings_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IP access settings that is associated with the web portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-ipaccesssettingsarn
        '''
        result = self._values.get("ip_access_settings_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrent_sessions(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of concurrent sessions for the portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-maxconcurrentsessions
        '''
        result = self._values.get("max_concurrent_sessions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_settings_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the network settings that is associated with the web portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-networksettingsarn
        '''
        result = self._values.get("network_settings_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_logger_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the session logger that is associated with the portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-sessionloggerarn
        '''
        result = self._values.get("session_logger_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the web portal.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def trust_store_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the trust store that is associated with the web portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-truststorearn
        '''
        result = self._values.get("trust_store_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_access_logging_settings_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the user access logging settings that is associated with the web portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-useraccessloggingsettingsarn
        '''
        result = self._values.get("user_access_logging_settings_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_settings_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the user settings that is associated with the web portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html#cfn-workspacesweb-portal-usersettingsarn
        '''
        result = self._values.get("user_settings_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortalMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPortalPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnPortalPropsMixin",
):
    '''This resource specifies a web portal, which users use to start browsing sessions.

    A ``Standard`` web portal can't start browsing sessions unless you have at defined and associated an ``IdentityProvider`` and ``NetworkSettings`` resource. An ``IAM Identity Center`` web portal does not require an ``IdentityProvider`` resource.

    For more information about web portals, see `What is Amazon WorkSpaces Secure Browser? <https://docs.aws.amazon.com/workspaces-web/latest/adminguide/what-is-workspaces-web.html.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-portal.html
    :cloudformationResource: AWS::WorkSpacesWeb::Portal
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        cfn_portal_props_mixin = workspacesweb_mixins.CfnPortalPropsMixin(workspacesweb_mixins.CfnPortalMixinProps(
            additional_encryption_context={
                "additional_encryption_context_key": "additionalEncryptionContext"
            },
            authentication_type="authenticationType",
            browser_settings_arn="browserSettingsArn",
            customer_managed_key="customerManagedKey",
            data_protection_settings_arn="dataProtectionSettingsArn",
            display_name="displayName",
            instance_type="instanceType",
            ip_access_settings_arn="ipAccessSettingsArn",
            max_concurrent_sessions=123,
            network_settings_arn="networkSettingsArn",
            session_logger_arn="sessionLoggerArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trust_store_arn="trustStoreArn",
            user_access_logging_settings_arn="userAccessLoggingSettingsArn",
            user_settings_arn="userSettingsArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPortalMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::Portal``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d846700a3206958941d736b46c8b651a7c0ffa1d84fae87d94ac1a7888ba4b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0b344d19ebfe440e8d423ed4a409ff96ab8e30f0311dc8501af86c9929a5a66)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8ef750ad7f47e7b3217158309c1ddeb5a7f9423f68f261dc5f09877e74313e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPortalMixinProps:
        return typing.cast(CfnPortalMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnSessionLoggerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_encryption_context": "additionalEncryptionContext",
        "customer_managed_key": "customerManagedKey",
        "display_name": "displayName",
        "event_filter": "eventFilter",
        "log_configuration": "logConfiguration",
        "tags": "tags",
    },
)
class CfnSessionLoggerMixinProps:
    def __init__(
        self,
        *,
        additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        event_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSessionLoggerPropsMixin.EventFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSessionLoggerPropsMixin.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSessionLoggerPropsMixin.

        :param additional_encryption_context: The additional encryption context of the session logger.
        :param customer_managed_key: The custom managed key of the session logger.
        :param display_name: The human-readable display name.
        :param event_filter: The filter that specifies which events to monitor.
        :param log_configuration: The configuration that specifies where logs are fowarded.
        :param tags: The tags of the session logger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-sessionlogger.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            # all: Any
            
            cfn_session_logger_mixin_props = workspacesweb_mixins.CfnSessionLoggerMixinProps(
                additional_encryption_context={
                    "additional_encryption_context_key": "additionalEncryptionContext"
                },
                customer_managed_key="customerManagedKey",
                display_name="displayName",
                event_filter=workspacesweb_mixins.CfnSessionLoggerPropsMixin.EventFilterProperty(
                    all=all,
                    include=["include"]
                ),
                log_configuration=workspacesweb_mixins.CfnSessionLoggerPropsMixin.LogConfigurationProperty(
                    s3=workspacesweb_mixins.CfnSessionLoggerPropsMixin.S3LogConfigurationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        folder_structure="folderStructure",
                        key_prefix="keyPrefix",
                        log_file_format="logFileFormat"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41f341a4d2ab9f380d003f414a6af5c329395f2a9f5fab573b7d58778c611ad)
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument event_filter", value=event_filter, expected_type=type_hints["event_filter"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if display_name is not None:
            self._values["display_name"] = display_name
        if event_filter is not None:
            self._values["event_filter"] = event_filter
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The additional encryption context of the session logger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-sessionlogger.html#cfn-workspacesweb-sessionlogger-additionalencryptioncontext
        '''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def customer_managed_key(self) -> typing.Optional[builtins.str]:
        '''The custom managed key of the session logger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-sessionlogger.html#cfn-workspacesweb-sessionlogger-customermanagedkey
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The human-readable display name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-sessionlogger.html#cfn-workspacesweb-sessionlogger-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_filter(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSessionLoggerPropsMixin.EventFilterProperty"]]:
        '''The filter that specifies which events to monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-sessionlogger.html#cfn-workspacesweb-sessionlogger-eventfilter
        '''
        result = self._values.get("event_filter")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSessionLoggerPropsMixin.EventFilterProperty"]], result)

    @builtins.property
    def log_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSessionLoggerPropsMixin.LogConfigurationProperty"]]:
        '''The configuration that specifies where logs are fowarded.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-sessionlogger.html#cfn-workspacesweb-sessionlogger-logconfiguration
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSessionLoggerPropsMixin.LogConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags of the session logger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-sessionlogger.html#cfn-workspacesweb-sessionlogger-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSessionLoggerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSessionLoggerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnSessionLoggerPropsMixin",
):
    '''The session logger resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-sessionlogger.html
    :cloudformationResource: AWS::WorkSpacesWeb::SessionLogger
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        # all: Any
        
        cfn_session_logger_props_mixin = workspacesweb_mixins.CfnSessionLoggerPropsMixin(workspacesweb_mixins.CfnSessionLoggerMixinProps(
            additional_encryption_context={
                "additional_encryption_context_key": "additionalEncryptionContext"
            },
            customer_managed_key="customerManagedKey",
            display_name="displayName",
            event_filter=workspacesweb_mixins.CfnSessionLoggerPropsMixin.EventFilterProperty(
                all=all,
                include=["include"]
            ),
            log_configuration=workspacesweb_mixins.CfnSessionLoggerPropsMixin.LogConfigurationProperty(
                s3=workspacesweb_mixins.CfnSessionLoggerPropsMixin.S3LogConfigurationProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    folder_structure="folderStructure",
                    key_prefix="keyPrefix",
                    log_file_format="logFileFormat"
                )
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
        props: typing.Union[CfnSessionLoggerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::SessionLogger``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b1be5617e320dca0317293424310cee55619566ddc10732d78e89be8d1449f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5750260ac7a31e11424be39d6635c94f2d9f4856e139027fe59a2538abe8131e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dec29bd7a2d7596b97bc394428510b78ba85639466790e16659009b5e2528dd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSessionLoggerMixinProps:
        return typing.cast(CfnSessionLoggerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnSessionLoggerPropsMixin.EventFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"all": "all", "include": "include"},
    )
    class EventFilterProperty:
        def __init__(
            self,
            *,
            all: typing.Any = None,
            include: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The filter that specifies the events to monitor.

            :param all: The filter that monitors all of the available events, including any new events emitted in the future. The ``All`` and ``Include`` properties are not required, but one of them should be present. ``{}`` is a valid input.
            :param include: The filter that monitors only the listed set of events. New events are not auto-monitored. The ``All`` and ``Include`` properties are not required, but one of them should be present.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-eventfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                # all: Any
                
                event_filter_property = workspacesweb_mixins.CfnSessionLoggerPropsMixin.EventFilterProperty(
                    all=all,
                    include=["include"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0956f7e8f4e3e6e501b8cc100cbe698face56f267076119a58347277289dcb4a)
                check_type(argname="argument all", value=all, expected_type=type_hints["all"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if all is not None:
                self._values["all"] = all
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def all(self) -> typing.Any:
            '''The filter that monitors all of the available events, including any new events emitted in the future.

            The ``All`` and ``Include`` properties are not required, but one of them should be present. ``{}`` is a valid input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-eventfilter.html#cfn-workspacesweb-sessionlogger-eventfilter-all
            '''
            result = self._values.get("all")
            return typing.cast(typing.Any, result)

        @builtins.property
        def include(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The filter that monitors only the listed set of events.

            New events are not auto-monitored. The ``All`` and ``Include`` properties are not required, but one of them should be present.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-eventfilter.html#cfn-workspacesweb-sessionlogger-eventfilter-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnSessionLoggerPropsMixin.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSessionLoggerPropsMixin.S3LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of the log.

            :param s3: The configuration for delivering the logs to S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                log_configuration_property = workspacesweb_mixins.CfnSessionLoggerPropsMixin.LogConfigurationProperty(
                    s3=workspacesweb_mixins.CfnSessionLoggerPropsMixin.S3LogConfigurationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        folder_structure="folderStructure",
                        key_prefix="keyPrefix",
                        log_file_format="logFileFormat"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17e47f2f0d6e3472bf40d0aacc77653dfb7f8438c05b08ea52403856e838e62c)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSessionLoggerPropsMixin.S3LogConfigurationProperty"]]:
            '''The configuration for delivering the logs to S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-logconfiguration.html#cfn-workspacesweb-sessionlogger-logconfiguration-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSessionLoggerPropsMixin.S3LogConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnSessionLoggerPropsMixin.S3LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "bucket_owner": "bucketOwner",
            "folder_structure": "folderStructure",
            "key_prefix": "keyPrefix",
            "log_file_format": "logFileFormat",
        },
    )
    class S3LogConfigurationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            bucket_owner: typing.Optional[builtins.str] = None,
            folder_structure: typing.Optional[builtins.str] = None,
            key_prefix: typing.Optional[builtins.str] = None,
            log_file_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 log configuration.

            :param bucket: The S3 bucket name where logs are delivered.
            :param bucket_owner: The expected bucket owner of the target S3 bucket. The caller must have permissions to write to the target bucket.
            :param folder_structure: The folder structure that defines the organizational structure for log files in S3.
            :param key_prefix: The S3 path prefix that determines where log files are stored.
            :param log_file_format: The format of the LogFile that is written to S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-s3logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                s3_log_configuration_property = workspacesweb_mixins.CfnSessionLoggerPropsMixin.S3LogConfigurationProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    folder_structure="folderStructure",
                    key_prefix="keyPrefix",
                    log_file_format="logFileFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f13db1bfa9a368a31d9b6fd290285082e0851d51ada79a3ace07a73c05913781)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
                check_type(argname="argument folder_structure", value=folder_structure, expected_type=type_hints["folder_structure"])
                check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
                check_type(argname="argument log_file_format", value=log_file_format, expected_type=type_hints["log_file_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if bucket_owner is not None:
                self._values["bucket_owner"] = bucket_owner
            if folder_structure is not None:
                self._values["folder_structure"] = folder_structure
            if key_prefix is not None:
                self._values["key_prefix"] = key_prefix
            if log_file_format is not None:
                self._values["log_file_format"] = log_file_format

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket name where logs are delivered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-s3logconfiguration.html#cfn-workspacesweb-sessionlogger-s3logconfiguration-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The expected bucket owner of the target S3 bucket.

            The caller must have permissions to write to the target bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-s3logconfiguration.html#cfn-workspacesweb-sessionlogger-s3logconfiguration-bucketowner
            '''
            result = self._values.get("bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def folder_structure(self) -> typing.Optional[builtins.str]:
            '''The folder structure that defines the organizational structure for log files in S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-s3logconfiguration.html#cfn-workspacesweb-sessionlogger-s3logconfiguration-folderstructure
            '''
            result = self._values.get("folder_structure")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 path prefix that determines where log files are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-s3logconfiguration.html#cfn-workspacesweb-sessionlogger-s3logconfiguration-keyprefix
            '''
            result = self._values.get("key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_file_format(self) -> typing.Optional[builtins.str]:
            '''The format of the LogFile that is written to S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-sessionlogger-s3logconfiguration.html#cfn-workspacesweb-sessionlogger-s3logconfiguration-logfileformat
            '''
            result = self._values.get("log_file_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnTrustStoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={"certificate_list": "certificateList", "tags": "tags"},
)
class CfnTrustStoreMixinProps:
    def __init__(
        self,
        *,
        certificate_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTrustStorePropsMixin.

        :param certificate_list: A list of CA certificates to be added to the trust store.
        :param tags: The tags to add to the trust store. A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-truststore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            cfn_trust_store_mixin_props = workspacesweb_mixins.CfnTrustStoreMixinProps(
                certificate_list=["certificateList"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0359771b32693cab6a7447be3a5f6bed72ef21b8ec092b992e6f063144873dda)
            check_type(argname="argument certificate_list", value=certificate_list, expected_type=type_hints["certificate_list"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_list is not None:
            self._values["certificate_list"] = certificate_list
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of CA certificates to be added to the trust store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-truststore.html#cfn-workspacesweb-truststore-certificatelist
        '''
        result = self._values.get("certificate_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the trust store.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-truststore.html#cfn-workspacesweb-truststore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrustStoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrustStorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnTrustStorePropsMixin",
):
    '''This resource specifies a trust store that can be associated with a web portal.

    A trust store contains certificate authority (CA) certificates. Once associated with a web portal, the browser in a streaming session will recognize certificates that have been issued using any of the CAs in the trust store. If your organization has internal websites that use certificates issued by private CAs, you should add the private CA certificate to the trust store.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-truststore.html
    :cloudformationResource: AWS::WorkSpacesWeb::TrustStore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        cfn_trust_store_props_mixin = workspacesweb_mixins.CfnTrustStorePropsMixin(workspacesweb_mixins.CfnTrustStoreMixinProps(
            certificate_list=["certificateList"],
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
        props: typing.Union[CfnTrustStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::TrustStore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a3f5865f61ad089fce2dcae82cf868468bf826e5fa2adb43f8c0a45e6e24b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63db44ed540a0d6a72737064008f4e6092bd7ea2e8570d63eee377731010c9a0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307026fc2670d6e1235dfd2b51276d1287b543499f75ea5d3db27773d64448cf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrustStoreMixinProps:
        return typing.cast(CfnTrustStoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnUserAccessLoggingSettingsMixinProps",
    jsii_struct_bases=[],
    name_mapping={"kinesis_stream_arn": "kinesisStreamArn", "tags": "tags"},
)
class CfnUserAccessLoggingSettingsMixinProps:
    def __init__(
        self,
        *,
        kinesis_stream_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnUserAccessLoggingSettingsPropsMixin.

        :param kinesis_stream_arn: The ARN of the Kinesis stream.
        :param tags: The tags to add to the user access logging settings resource. A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-useraccessloggingsettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            cfn_user_access_logging_settings_mixin_props = workspacesweb_mixins.CfnUserAccessLoggingSettingsMixinProps(
                kinesis_stream_arn="kinesisStreamArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4dcbcc74ca9d3e241967c63bce775a7e30371247f15fb0e7c9aebe650e08782)
            check_type(argname="argument kinesis_stream_arn", value=kinesis_stream_arn, expected_type=type_hints["kinesis_stream_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kinesis_stream_arn is not None:
            self._values["kinesis_stream_arn"] = kinesis_stream_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def kinesis_stream_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the Kinesis stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-useraccessloggingsettings.html#cfn-workspacesweb-useraccessloggingsettings-kinesisstreamarn
        '''
        result = self._values.get("kinesis_stream_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the user access logging settings resource.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-useraccessloggingsettings.html#cfn-workspacesweb-useraccessloggingsettings-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserAccessLoggingSettingsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserAccessLoggingSettingsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnUserAccessLoggingSettingsPropsMixin",
):
    '''This resource specifies user access logging settings that can be associated with a web portal.

    In order to receive logs from WorkSpaces Secure Browser, you must have an Amazon Kinesis Data Stream that starts with "amazon-workspaces-web-*". Your Amazon Kinesis data stream must either have server-side encryption turned off, or must use AWS managed keys for server-side encryption.

    For more information about setting server-side encryption in Amazon Kinesis , see `How Do I Get Started with Server-Side Encryption? <https://docs.aws.amazon.com/streams/latest/dev/getting-started-with-sse.html>`_ .

    For more information about setting up user access logging, see `Set up user access logging <https://docs.aws.amazon.com/workspaces-web/latest/adminguide/user-logging.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-useraccessloggingsettings.html
    :cloudformationResource: AWS::WorkSpacesWeb::UserAccessLoggingSettings
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        cfn_user_access_logging_settings_props_mixin = workspacesweb_mixins.CfnUserAccessLoggingSettingsPropsMixin(workspacesweb_mixins.CfnUserAccessLoggingSettingsMixinProps(
            kinesis_stream_arn="kinesisStreamArn",
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
        props: typing.Union[CfnUserAccessLoggingSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::UserAccessLoggingSettings``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb9738769085c5a86b91ad5280a3c0bc0c18e559bfc240f9ef37b60ff806d45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2b32dadc6e2b844c0e77524e316f59271773c03f6ae1cfdacf8626385dcda8f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f785d0e7795c7f09afc2f527a11ed01ed255394040549122fdf1ec444a921b37)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserAccessLoggingSettingsMixinProps:
        return typing.cast(CfnUserAccessLoggingSettingsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnUserSettingsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_encryption_context": "additionalEncryptionContext",
        "cookie_synchronization_configuration": "cookieSynchronizationConfiguration",
        "copy_allowed": "copyAllowed",
        "customer_managed_key": "customerManagedKey",
        "deep_link_allowed": "deepLinkAllowed",
        "disconnect_timeout_in_minutes": "disconnectTimeoutInMinutes",
        "download_allowed": "downloadAllowed",
        "idle_disconnect_timeout_in_minutes": "idleDisconnectTimeoutInMinutes",
        "paste_allowed": "pasteAllowed",
        "print_allowed": "printAllowed",
        "tags": "tags",
        "toolbar_configuration": "toolbarConfiguration",
        "upload_allowed": "uploadAllowed",
    },
)
class CfnUserSettingsMixinProps:
    def __init__(
        self,
        *,
        additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        cookie_synchronization_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserSettingsPropsMixin.CookieSynchronizationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        copy_allowed: typing.Optional[builtins.str] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        deep_link_allowed: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        download_allowed: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        paste_allowed: typing.Optional[builtins.str] = None,
        print_allowed: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        toolbar_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserSettingsPropsMixin.ToolbarConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        upload_allowed: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserSettingsPropsMixin.

        :param additional_encryption_context: The additional encryption context of the user settings.
        :param cookie_synchronization_configuration: The configuration that specifies which cookies should be synchronized from the end user's local browser to the remote browser.
        :param copy_allowed: Specifies whether the user can copy text from the streaming session to the local device.
        :param customer_managed_key: The customer managed key used to encrypt sensitive information in the user settings.
        :param deep_link_allowed: Specifies whether the user can use deep links that open automatically when connecting to a session.
        :param disconnect_timeout_in_minutes: The amount of time that a streaming session remains active after users disconnect.
        :param download_allowed: Specifies whether the user can download files from the streaming session to the local device.
        :param idle_disconnect_timeout_in_minutes: The amount of time that users can be idle (inactive) before they are disconnected from their streaming session and the disconnect timeout interval begins.
        :param paste_allowed: Specifies whether the user can paste text from the local device to the streaming session.
        :param print_allowed: Specifies whether the user can print to the local device.
        :param tags: The tags to add to the user settings resource. A tag is a key-value pair.
        :param toolbar_configuration: The configuration of the toolbar. This allows administrators to select the toolbar type and visual mode, set maximum display resolution for sessions, and choose which items are visible to end users during their sessions. If administrators do not modify these settings, end users retain control over their toolbar preferences.
        :param upload_allowed: Specifies whether the user can upload files from the local device to the streaming session.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
            
            cfn_user_settings_mixin_props = workspacesweb_mixins.CfnUserSettingsMixinProps(
                additional_encryption_context={
                    "additional_encryption_context_key": "additionalEncryptionContext"
                },
                cookie_synchronization_configuration=workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSynchronizationConfigurationProperty(
                    allowlist=[workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSpecificationProperty(
                        domain="domain",
                        name="name",
                        path="path"
                    )],
                    blocklist=[workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSpecificationProperty(
                        domain="domain",
                        name="name",
                        path="path"
                    )]
                ),
                copy_allowed="copyAllowed",
                customer_managed_key="customerManagedKey",
                deep_link_allowed="deepLinkAllowed",
                disconnect_timeout_in_minutes=123,
                download_allowed="downloadAllowed",
                idle_disconnect_timeout_in_minutes=123,
                paste_allowed="pasteAllowed",
                print_allowed="printAllowed",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                toolbar_configuration=workspacesweb_mixins.CfnUserSettingsPropsMixin.ToolbarConfigurationProperty(
                    hidden_toolbar_items=["hiddenToolbarItems"],
                    max_display_resolution="maxDisplayResolution",
                    toolbar_type="toolbarType",
                    visual_mode="visualMode"
                ),
                upload_allowed="uploadAllowed"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581b1e02ec182fe64db3635b4bb1c0a2b4bb3d697d7019a013f9ddeec38f97e4)
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument cookie_synchronization_configuration", value=cookie_synchronization_configuration, expected_type=type_hints["cookie_synchronization_configuration"])
            check_type(argname="argument copy_allowed", value=copy_allowed, expected_type=type_hints["copy_allowed"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument deep_link_allowed", value=deep_link_allowed, expected_type=type_hints["deep_link_allowed"])
            check_type(argname="argument disconnect_timeout_in_minutes", value=disconnect_timeout_in_minutes, expected_type=type_hints["disconnect_timeout_in_minutes"])
            check_type(argname="argument download_allowed", value=download_allowed, expected_type=type_hints["download_allowed"])
            check_type(argname="argument idle_disconnect_timeout_in_minutes", value=idle_disconnect_timeout_in_minutes, expected_type=type_hints["idle_disconnect_timeout_in_minutes"])
            check_type(argname="argument paste_allowed", value=paste_allowed, expected_type=type_hints["paste_allowed"])
            check_type(argname="argument print_allowed", value=print_allowed, expected_type=type_hints["print_allowed"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument toolbar_configuration", value=toolbar_configuration, expected_type=type_hints["toolbar_configuration"])
            check_type(argname="argument upload_allowed", value=upload_allowed, expected_type=type_hints["upload_allowed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if cookie_synchronization_configuration is not None:
            self._values["cookie_synchronization_configuration"] = cookie_synchronization_configuration
        if copy_allowed is not None:
            self._values["copy_allowed"] = copy_allowed
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if deep_link_allowed is not None:
            self._values["deep_link_allowed"] = deep_link_allowed
        if disconnect_timeout_in_minutes is not None:
            self._values["disconnect_timeout_in_minutes"] = disconnect_timeout_in_minutes
        if download_allowed is not None:
            self._values["download_allowed"] = download_allowed
        if idle_disconnect_timeout_in_minutes is not None:
            self._values["idle_disconnect_timeout_in_minutes"] = idle_disconnect_timeout_in_minutes
        if paste_allowed is not None:
            self._values["paste_allowed"] = paste_allowed
        if print_allowed is not None:
            self._values["print_allowed"] = print_allowed
        if tags is not None:
            self._values["tags"] = tags
        if toolbar_configuration is not None:
            self._values["toolbar_configuration"] = toolbar_configuration
        if upload_allowed is not None:
            self._values["upload_allowed"] = upload_allowed

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The additional encryption context of the user settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-additionalencryptioncontext
        '''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cookie_synchronization_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserSettingsPropsMixin.CookieSynchronizationConfigurationProperty"]]:
        '''The configuration that specifies which cookies should be synchronized from the end user's local browser to the remote browser.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-cookiesynchronizationconfiguration
        '''
        result = self._values.get("cookie_synchronization_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserSettingsPropsMixin.CookieSynchronizationConfigurationProperty"]], result)

    @builtins.property
    def copy_allowed(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user can copy text from the streaming session to the local device.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-copyallowed
        '''
        result = self._values.get("copy_allowed")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_managed_key(self) -> typing.Optional[builtins.str]:
        '''The customer managed key used to encrypt sensitive information in the user settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-customermanagedkey
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deep_link_allowed(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user can use deep links that open automatically when connecting to a session.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-deeplinkallowed
        '''
        result = self._values.get("deep_link_allowed")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disconnect_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''The amount of time that a streaming session remains active after users disconnect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-disconnecttimeoutinminutes
        '''
        result = self._values.get("disconnect_timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def download_allowed(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user can download files from the streaming session to the local device.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-downloadallowed
        '''
        result = self._values.get("download_allowed")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_disconnect_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''The amount of time that users can be idle (inactive) before they are disconnected from their streaming session and the disconnect timeout interval begins.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-idledisconnecttimeoutinminutes
        '''
        result = self._values.get("idle_disconnect_timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def paste_allowed(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user can paste text from the local device to the streaming session.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-pasteallowed
        '''
        result = self._values.get("paste_allowed")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def print_allowed(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user can print to the local device.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-printallowed
        '''
        result = self._values.get("print_allowed")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to add to the user settings resource.

        A tag is a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def toolbar_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserSettingsPropsMixin.ToolbarConfigurationProperty"]]:
        '''The configuration of the toolbar.

        This allows administrators to select the toolbar type and visual mode, set maximum display resolution for sessions, and choose which items are visible to end users during their sessions. If administrators do not modify these settings, end users retain control over their toolbar preferences.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-toolbarconfiguration
        '''
        result = self._values.get("toolbar_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserSettingsPropsMixin.ToolbarConfigurationProperty"]], result)

    @builtins.property
    def upload_allowed(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the user can upload files from the local device to the streaming session.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html#cfn-workspacesweb-usersettings-uploadallowed
        '''
        result = self._values.get("upload_allowed")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserSettingsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserSettingsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnUserSettingsPropsMixin",
):
    '''This resource specifies user settings that can be associated with a web portal.

    Once associated with a web portal, user settings control how users can transfer data between a streaming session and the their local devices.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesweb-usersettings.html
    :cloudformationResource: AWS::WorkSpacesWeb::UserSettings
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
        
        cfn_user_settings_props_mixin = workspacesweb_mixins.CfnUserSettingsPropsMixin(workspacesweb_mixins.CfnUserSettingsMixinProps(
            additional_encryption_context={
                "additional_encryption_context_key": "additionalEncryptionContext"
            },
            cookie_synchronization_configuration=workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSynchronizationConfigurationProperty(
                allowlist=[workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSpecificationProperty(
                    domain="domain",
                    name="name",
                    path="path"
                )],
                blocklist=[workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSpecificationProperty(
                    domain="domain",
                    name="name",
                    path="path"
                )]
            ),
            copy_allowed="copyAllowed",
            customer_managed_key="customerManagedKey",
            deep_link_allowed="deepLinkAllowed",
            disconnect_timeout_in_minutes=123,
            download_allowed="downloadAllowed",
            idle_disconnect_timeout_in_minutes=123,
            paste_allowed="pasteAllowed",
            print_allowed="printAllowed",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            toolbar_configuration=workspacesweb_mixins.CfnUserSettingsPropsMixin.ToolbarConfigurationProperty(
                hidden_toolbar_items=["hiddenToolbarItems"],
                max_display_resolution="maxDisplayResolution",
                toolbar_type="toolbarType",
                visual_mode="visualMode"
            ),
            upload_allowed="uploadAllowed"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkSpacesWeb::UserSettings``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cace96b15e145207d07b5f027f20864e606dbf98b30b8f919d6318ca736a7b02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ef7b8b28d5a7962d42e76f6439028e8885a0a563b9953f51805b72df20c048e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e55100478a97003e6f203fad7baea6afff6499cebf561fba00710cb74e9149a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserSettingsMixinProps:
        return typing.cast(CfnUserSettingsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnUserSettingsPropsMixin.CookieSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"domain": "domain", "name": "name", "path": "path"},
    )
    class CookieSpecificationProperty:
        def __init__(
            self,
            *,
            domain: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a single cookie or set of cookies in an end user's browser.

            :param domain: The domain of the cookie.
            :param name: The name of the cookie.
            :param path: The path of the cookie.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-cookiespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                cookie_specification_property = workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSpecificationProperty(
                    domain="domain",
                    name="name",
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd8d8122615533c76c5ab57dd574ecf1449054a2bd01e6a9735d01ab5d185712)
                check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain is not None:
                self._values["domain"] = domain
            if name is not None:
                self._values["name"] = name
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def domain(self) -> typing.Optional[builtins.str]:
            '''The domain of the cookie.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-cookiespecification.html#cfn-workspacesweb-usersettings-cookiespecification-domain
            '''
            result = self._values.get("domain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the cookie.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-cookiespecification.html#cfn-workspacesweb-usersettings-cookiespecification-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The path of the cookie.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-cookiespecification.html#cfn-workspacesweb-usersettings-cookiespecification-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CookieSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnUserSettingsPropsMixin.CookieSynchronizationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"allowlist": "allowlist", "blocklist": "blocklist"},
    )
    class CookieSynchronizationConfigurationProperty:
        def __init__(
            self,
            *,
            allowlist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserSettingsPropsMixin.CookieSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            blocklist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserSettingsPropsMixin.CookieSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration that specifies which cookies should be synchronized from the end user's local browser to the remote browser.

            :param allowlist: The list of cookie specifications that are allowed to be synchronized to the remote browser.
            :param blocklist: The list of cookie specifications that are blocked from being synchronized to the remote browser.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-cookiesynchronizationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                cookie_synchronization_configuration_property = workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSynchronizationConfigurationProperty(
                    allowlist=[workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSpecificationProperty(
                        domain="domain",
                        name="name",
                        path="path"
                    )],
                    blocklist=[workspacesweb_mixins.CfnUserSettingsPropsMixin.CookieSpecificationProperty(
                        domain="domain",
                        name="name",
                        path="path"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d72e182ee32aa6be6e234ff69771df9c20bff4b681c6fddcdd648f30d63be988)
                check_type(argname="argument allowlist", value=allowlist, expected_type=type_hints["allowlist"])
                check_type(argname="argument blocklist", value=blocklist, expected_type=type_hints["blocklist"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowlist is not None:
                self._values["allowlist"] = allowlist
            if blocklist is not None:
                self._values["blocklist"] = blocklist

        @builtins.property
        def allowlist(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserSettingsPropsMixin.CookieSpecificationProperty"]]]]:
            '''The list of cookie specifications that are allowed to be synchronized to the remote browser.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-cookiesynchronizationconfiguration.html#cfn-workspacesweb-usersettings-cookiesynchronizationconfiguration-allowlist
            '''
            result = self._values.get("allowlist")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserSettingsPropsMixin.CookieSpecificationProperty"]]]], result)

        @builtins.property
        def blocklist(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserSettingsPropsMixin.CookieSpecificationProperty"]]]]:
            '''The list of cookie specifications that are blocked from being synchronized to the remote browser.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-cookiesynchronizationconfiguration.html#cfn-workspacesweb-usersettings-cookiesynchronizationconfiguration-blocklist
            '''
            result = self._values.get("blocklist")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserSettingsPropsMixin.CookieSpecificationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CookieSynchronizationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesweb.mixins.CfnUserSettingsPropsMixin.ToolbarConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hidden_toolbar_items": "hiddenToolbarItems",
            "max_display_resolution": "maxDisplayResolution",
            "toolbar_type": "toolbarType",
            "visual_mode": "visualMode",
        },
    )
    class ToolbarConfigurationProperty:
        def __init__(
            self,
            *,
            hidden_toolbar_items: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_display_resolution: typing.Optional[builtins.str] = None,
            toolbar_type: typing.Optional[builtins.str] = None,
            visual_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of the toolbar.

            This allows administrators to select the toolbar type and visual mode, set maximum display resolution for sessions, and choose which items are visible to end users during their sessions. If administrators do not modify these settings, end users retain control over their toolbar preferences.

            :param hidden_toolbar_items: The list of toolbar items to be hidden.
            :param max_display_resolution: The maximum display resolution that is allowed for the session.
            :param toolbar_type: The type of toolbar displayed during the session.
            :param visual_mode: The visual mode of the toolbar.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-toolbarconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesweb import mixins as workspacesweb_mixins
                
                toolbar_configuration_property = workspacesweb_mixins.CfnUserSettingsPropsMixin.ToolbarConfigurationProperty(
                    hidden_toolbar_items=["hiddenToolbarItems"],
                    max_display_resolution="maxDisplayResolution",
                    toolbar_type="toolbarType",
                    visual_mode="visualMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d730a2f075c3c44b95fb196656eae8e48a2e7b01e1c74567639ca70e97338d3)
                check_type(argname="argument hidden_toolbar_items", value=hidden_toolbar_items, expected_type=type_hints["hidden_toolbar_items"])
                check_type(argname="argument max_display_resolution", value=max_display_resolution, expected_type=type_hints["max_display_resolution"])
                check_type(argname="argument toolbar_type", value=toolbar_type, expected_type=type_hints["toolbar_type"])
                check_type(argname="argument visual_mode", value=visual_mode, expected_type=type_hints["visual_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hidden_toolbar_items is not None:
                self._values["hidden_toolbar_items"] = hidden_toolbar_items
            if max_display_resolution is not None:
                self._values["max_display_resolution"] = max_display_resolution
            if toolbar_type is not None:
                self._values["toolbar_type"] = toolbar_type
            if visual_mode is not None:
                self._values["visual_mode"] = visual_mode

        @builtins.property
        def hidden_toolbar_items(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of toolbar items to be hidden.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-toolbarconfiguration.html#cfn-workspacesweb-usersettings-toolbarconfiguration-hiddentoolbaritems
            '''
            result = self._values.get("hidden_toolbar_items")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_display_resolution(self) -> typing.Optional[builtins.str]:
            '''The maximum display resolution that is allowed for the session.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-toolbarconfiguration.html#cfn-workspacesweb-usersettings-toolbarconfiguration-maxdisplayresolution
            '''
            result = self._values.get("max_display_resolution")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def toolbar_type(self) -> typing.Optional[builtins.str]:
            '''The type of toolbar displayed during the session.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-toolbarconfiguration.html#cfn-workspacesweb-usersettings-toolbarconfiguration-toolbartype
            '''
            result = self._values.get("toolbar_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def visual_mode(self) -> typing.Optional[builtins.str]:
            '''The visual mode of the toolbar.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesweb-usersettings-toolbarconfiguration.html#cfn-workspacesweb-usersettings-toolbarconfiguration-visualmode
            '''
            result = self._values.get("visual_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ToolbarConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnBrowserSettingsMixinProps",
    "CfnBrowserSettingsPropsMixin",
    "CfnDataProtectionSettingsMixinProps",
    "CfnDataProtectionSettingsPropsMixin",
    "CfnIdentityProviderMixinProps",
    "CfnIdentityProviderPropsMixin",
    "CfnIpAccessSettingsMixinProps",
    "CfnIpAccessSettingsPropsMixin",
    "CfnNetworkSettingsMixinProps",
    "CfnNetworkSettingsPropsMixin",
    "CfnPortalMixinProps",
    "CfnPortalPropsMixin",
    "CfnSessionLoggerMixinProps",
    "CfnSessionLoggerPropsMixin",
    "CfnTrustStoreMixinProps",
    "CfnTrustStorePropsMixin",
    "CfnUserAccessLoggingSettingsMixinProps",
    "CfnUserAccessLoggingSettingsPropsMixin",
    "CfnUserSettingsMixinProps",
    "CfnUserSettingsPropsMixin",
]

publication.publish()

def _typecheckingstub__68d4fabf1f50e3d5fe139f7a7c3637fd5ea75b335e089eaf485d8caa0f9620e9(
    *,
    additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    browser_policy: typing.Optional[builtins.str] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    web_content_filtering_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBrowserSettingsPropsMixin.WebContentFilteringPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bf87ddd8a51749b1417576d841be5e7fa4cb808db653dc47b4e656486d65ec(
    props: typing.Union[CfnBrowserSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad683d781e1be73810d80efcc62bff4f00cc962a3ce1b27df9a35b4c42586d0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb735cae411f6da12d21c3f775ab7ac702325741edc80d65e401d57bd85f7aa6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4933eae949bea1440224977532ee3360641edac598ef486c631a911da74c87(
    *,
    allowed_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    blocked_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    blocked_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ee5168844c0eee4cd69079bdfebfc0af9e15b61e7c7c47cbd12e0eef65d2ba(
    *,
    additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    inline_redaction_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProtectionSettingsPropsMixin.InlineRedactionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a889ec2493bba40ec6860616b9c5d500fd6e19b120035fb8a796ff73461a7742(
    props: typing.Union[CfnDataProtectionSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ac626623326c81b0f4d1bd8b86c59d75aedb7e44f668b8ea33ae558338107f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f96dd46edb5ce4f5d32c7bec3c8e7804f0712e31a4b76275019d5956cc48b9e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfce9e4ca2de910f84f6f89b19f66a5f78806801762f0ecb69eb4185528a5a01(
    *,
    keyword_regex: typing.Optional[builtins.str] = None,
    pattern_description: typing.Optional[builtins.str] = None,
    pattern_name: typing.Optional[builtins.str] = None,
    pattern_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b30206064b71d63613fe98bbd2ae73b2ad3ea31009ae49094ab8329c1062c1a(
    *,
    global_confidence_level: typing.Optional[jsii.Number] = None,
    global_enforced_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    global_exempt_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_redaction_patterns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProtectionSettingsPropsMixin.InlineRedactionPatternProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e7461a415703014ac29a1cd73a51ee5154c7de669ba8240673c883cd6acce9(
    *,
    built_in_pattern_id: typing.Optional[builtins.str] = None,
    confidence_level: typing.Optional[jsii.Number] = None,
    custom_pattern: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProtectionSettingsPropsMixin.CustomPatternProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enforced_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    exempt_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    redaction_place_holder: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataProtectionSettingsPropsMixin.RedactionPlaceHolderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68131c1aca5625aa4c1f2ad1d82eb7a5efc2597589f69c3417711ff0a66e6706(
    *,
    redaction_place_holder_text: typing.Optional[builtins.str] = None,
    redaction_place_holder_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a01b72433b6fb98dde81e4cfe784b2da72027a025cb91e08b1a6a36dc61cb0(
    *,
    identity_provider_details: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    identity_provider_name: typing.Optional[builtins.str] = None,
    identity_provider_type: typing.Optional[builtins.str] = None,
    portal_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2478c71da2277107ac09a88369f72f1637169307ec3f8c1a6e451754e2bfc6b5(
    props: typing.Union[CfnIdentityProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e08f1fc12c127abd5684889d43e8932aa96f35768fb8ff5c69903f70355f477(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a327355ddf516fab4bafb1382b8b81dc43af633c6fe7004f9ffcf2c47349a8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e24f990f985b880554221704351c3bda020779ccf61e81734f6bb3e061aa34(
    *,
    additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    ip_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIpAccessSettingsPropsMixin.IpRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7b9b8140881ef9bc0220792cce8829bea6cce1f3646b3bae772b3fb8f66951(
    props: typing.Union[CfnIpAccessSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f6616e961950c3868040854ff9f3cbf6991b4184a54c0c4b92e3f6f2d03040(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0870acf292beaea1022e1c1247b92c37e464f6a0934bae112e4902ecdf8897(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1bea04f4cb927de329c4cc2ffc4da938f728eebebee1bc9c782f0fc7824ea8(
    *,
    description: typing.Optional[builtins.str] = None,
    ip_range: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35ea1984fe77363d58912ec3eb8c818b565a143b92120d93fefc028f57ec31f(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a073c1c1549339249defb6a86a97f4c2cc789613f8dc32aad1a6f30b740f7b5(
    props: typing.Union[CfnNetworkSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3784e98999e79384bcb210552777743f90a693f1324da58dfbd3fe8d0890c48(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a438a76046457807e2070c549da0e9dfa1366b4e1f8676f859594f1f6a756b4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ed497d64c938f4f0bd9fa3893fda7435e9b337e8462c2eb8a7c816c9187358(
    *,
    additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    authentication_type: typing.Optional[builtins.str] = None,
    browser_settings_arn: typing.Optional[builtins.str] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    data_protection_settings_arn: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    ip_access_settings_arn: typing.Optional[builtins.str] = None,
    max_concurrent_sessions: typing.Optional[jsii.Number] = None,
    network_settings_arn: typing.Optional[builtins.str] = None,
    session_logger_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust_store_arn: typing.Optional[builtins.str] = None,
    user_access_logging_settings_arn: typing.Optional[builtins.str] = None,
    user_settings_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d846700a3206958941d736b46c8b651a7c0ffa1d84fae87d94ac1a7888ba4b2(
    props: typing.Union[CfnPortalMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b344d19ebfe440e8d423ed4a409ff96ab8e30f0311dc8501af86c9929a5a66(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8ef750ad7f47e7b3217158309c1ddeb5a7f9423f68f261dc5f09877e74313e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41f341a4d2ab9f380d003f414a6af5c329395f2a9f5fab573b7d58778c611ad(
    *,
    additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    event_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSessionLoggerPropsMixin.EventFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSessionLoggerPropsMixin.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b1be5617e320dca0317293424310cee55619566ddc10732d78e89be8d1449f(
    props: typing.Union[CfnSessionLoggerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5750260ac7a31e11424be39d6635c94f2d9f4856e139027fe59a2538abe8131e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dec29bd7a2d7596b97bc394428510b78ba85639466790e16659009b5e2528dd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0956f7e8f4e3e6e501b8cc100cbe698face56f267076119a58347277289dcb4a(
    *,
    all: typing.Any = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e47f2f0d6e3472bf40d0aacc77653dfb7f8438c05b08ea52403856e838e62c(
    *,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSessionLoggerPropsMixin.S3LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13db1bfa9a368a31d9b6fd290285082e0851d51ada79a3ace07a73c05913781(
    *,
    bucket: typing.Optional[builtins.str] = None,
    bucket_owner: typing.Optional[builtins.str] = None,
    folder_structure: typing.Optional[builtins.str] = None,
    key_prefix: typing.Optional[builtins.str] = None,
    log_file_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0359771b32693cab6a7447be3a5f6bed72ef21b8ec092b992e6f063144873dda(
    *,
    certificate_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a3f5865f61ad089fce2dcae82cf868468bf826e5fa2adb43f8c0a45e6e24b7(
    props: typing.Union[CfnTrustStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63db44ed540a0d6a72737064008f4e6092bd7ea2e8570d63eee377731010c9a0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307026fc2670d6e1235dfd2b51276d1287b543499f75ea5d3db27773d64448cf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4dcbcc74ca9d3e241967c63bce775a7e30371247f15fb0e7c9aebe650e08782(
    *,
    kinesis_stream_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb9738769085c5a86b91ad5280a3c0bc0c18e559bfc240f9ef37b60ff806d45(
    props: typing.Union[CfnUserAccessLoggingSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b32dadc6e2b844c0e77524e316f59271773c03f6ae1cfdacf8626385dcda8f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f785d0e7795c7f09afc2f527a11ed01ed255394040549122fdf1ec444a921b37(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581b1e02ec182fe64db3635b4bb1c0a2b4bb3d697d7019a013f9ddeec38f97e4(
    *,
    additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    cookie_synchronization_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserSettingsPropsMixin.CookieSynchronizationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    copy_allowed: typing.Optional[builtins.str] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    deep_link_allowed: typing.Optional[builtins.str] = None,
    disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    download_allowed: typing.Optional[builtins.str] = None,
    idle_disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    paste_allowed: typing.Optional[builtins.str] = None,
    print_allowed: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    toolbar_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserSettingsPropsMixin.ToolbarConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    upload_allowed: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cace96b15e145207d07b5f027f20864e606dbf98b30b8f919d6318ca736a7b02(
    props: typing.Union[CfnUserSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef7b8b28d5a7962d42e76f6439028e8885a0a563b9953f51805b72df20c048e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e55100478a97003e6f203fad7baea6afff6499cebf561fba00710cb74e9149a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8d8122615533c76c5ab57dd574ecf1449054a2bd01e6a9735d01ab5d185712(
    *,
    domain: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72e182ee32aa6be6e234ff69771df9c20bff4b681c6fddcdd648f30d63be988(
    *,
    allowlist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserSettingsPropsMixin.CookieSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    blocklist: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserSettingsPropsMixin.CookieSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d730a2f075c3c44b95fb196656eae8e48a2e7b01e1c74567639ca70e97338d3(
    *,
    hidden_toolbar_items: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_display_resolution: typing.Optional[builtins.str] = None,
    toolbar_type: typing.Optional[builtins.str] = None,
    visual_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
