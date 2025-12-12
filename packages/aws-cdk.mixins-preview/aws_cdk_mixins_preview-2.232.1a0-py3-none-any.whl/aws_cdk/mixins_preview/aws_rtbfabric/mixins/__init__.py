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
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnInboundExternalLinkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_id": "gatewayId",
        "link_attributes": "linkAttributes",
        "link_log_settings": "linkLogSettings",
        "tags": "tags",
    },
)
class CfnInboundExternalLinkMixinProps:
    def __init__(
        self,
        *,
        gateway_id: typing.Optional[builtins.str] = None,
        link_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInboundExternalLinkPropsMixin.LinkAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        link_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInboundExternalLinkPropsMixin.LinkLogSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnInboundExternalLinkPropsMixin.

        :param gateway_id: 
        :param link_attributes: 
        :param link_log_settings: 
        :param tags: Tags to assign to the Link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-inboundexternallink.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
            
            cfn_inbound_external_link_mixin_props = rtbfabric_mixins.CfnInboundExternalLinkMixinProps(
                gateway_id="gatewayId",
                link_attributes=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkAttributesProperty(
                    customer_provided_id="customerProvidedId",
                    responder_error_masking=[rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                        action="action",
                        http_code="httpCode",
                        logging_types=["loggingTypes"],
                        response_logging_percentage=123
                    )]
                ),
                link_log_settings=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkLogSettingsProperty(
                    application_logs=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.ApplicationLogsProperty(
                        link_application_log_sampling=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                            error_log=123,
                            filter_log=123
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d4f2379f175559b561055fd3152ec899e59de8b7dc27be5d947d0a8b964da7)
            check_type(argname="argument gateway_id", value=gateway_id, expected_type=type_hints["gateway_id"])
            check_type(argname="argument link_attributes", value=link_attributes, expected_type=type_hints["link_attributes"])
            check_type(argname="argument link_log_settings", value=link_log_settings, expected_type=type_hints["link_log_settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway_id is not None:
            self._values["gateway_id"] = gateway_id
        if link_attributes is not None:
            self._values["link_attributes"] = link_attributes
        if link_log_settings is not None:
            self._values["link_log_settings"] = link_log_settings
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def gateway_id(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-inboundexternallink.html#cfn-rtbfabric-inboundexternallink-gatewayid
        '''
        result = self._values.get("gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.LinkAttributesProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-inboundexternallink.html#cfn-rtbfabric-inboundexternallink-linkattributes
        '''
        result = self._values.get("link_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.LinkAttributesProperty"]], result)

    @builtins.property
    def link_log_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.LinkLogSettingsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-inboundexternallink.html#cfn-rtbfabric-inboundexternallink-linklogsettings
        '''
        result = self._values.get("link_log_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.LinkLogSettingsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the Link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-inboundexternallink.html#cfn-rtbfabric-inboundexternallink-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInboundExternalLinkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInboundExternalLinkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnInboundExternalLinkPropsMixin",
):
    '''Resource Type definition for AWS::RTBFabric::InboundExternalLink Resource Type.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-inboundexternallink.html
    :cloudformationResource: AWS::RTBFabric::InboundExternalLink
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
        
        cfn_inbound_external_link_props_mixin = rtbfabric_mixins.CfnInboundExternalLinkPropsMixin(rtbfabric_mixins.CfnInboundExternalLinkMixinProps(
            gateway_id="gatewayId",
            link_attributes=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkAttributesProperty(
                customer_provided_id="customerProvidedId",
                responder_error_masking=[rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                    action="action",
                    http_code="httpCode",
                    logging_types=["loggingTypes"],
                    response_logging_percentage=123
                )]
            ),
            link_log_settings=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkLogSettingsProperty(
                application_logs=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.ApplicationLogsProperty(
                    link_application_log_sampling=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                        error_log=123,
                        filter_log=123
                    )
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
        props: typing.Union[CfnInboundExternalLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RTBFabric::InboundExternalLink``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4110e1a9b89f6f8e9c25978f4034209b9dbe5facaa6b25d03302a93eb4837d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fafab914893d54bf5be2ea2ff70f01eb017cd90d4b5bfc5c34735d8a0533baf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cacf0f41d6b97ff6f343c2618568986263d17c1b8a8e499e8c9fb220d07ce07a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInboundExternalLinkMixinProps:
        return typing.cast(CfnInboundExternalLinkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnInboundExternalLinkPropsMixin.ApplicationLogsProperty",
        jsii_struct_bases=[],
        name_mapping={"link_application_log_sampling": "linkApplicationLogSampling"},
    )
    class ApplicationLogsProperty:
        def __init__(
            self,
            *,
            link_application_log_sampling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param link_application_log_sampling: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-applicationlogs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                application_logs_property = rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.ApplicationLogsProperty(
                    link_application_log_sampling=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                        error_log=123,
                        filter_log=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__01bb6fdac6106f7f9fe6f7e75b6c37d040e9d36b649e2adf0fdffd550eee30ba)
                check_type(argname="argument link_application_log_sampling", value=link_application_log_sampling, expected_type=type_hints["link_application_log_sampling"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if link_application_log_sampling is not None:
                self._values["link_application_log_sampling"] = link_application_log_sampling

        @builtins.property
        def link_application_log_sampling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-applicationlogs.html#cfn-rtbfabric-inboundexternallink-applicationlogs-linkapplicationlogsampling
            '''
            result = self._values.get("link_application_log_sampling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationLogsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty",
        jsii_struct_bases=[],
        name_mapping={"error_log": "errorLog", "filter_log": "filterLog"},
    )
    class LinkApplicationLogSamplingProperty:
        def __init__(
            self,
            *,
            error_log: typing.Optional[jsii.Number] = None,
            filter_log: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param error_log: 
            :param filter_log: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-linkapplicationlogsampling.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                link_application_log_sampling_property = rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                    error_log=123,
                    filter_log=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__20054ca4936e9e6b1b4a884b100e7c910645f4fcb47c8e614f66ebffb1aae1e3)
                check_type(argname="argument error_log", value=error_log, expected_type=type_hints["error_log"])
                check_type(argname="argument filter_log", value=filter_log, expected_type=type_hints["filter_log"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_log is not None:
                self._values["error_log"] = error_log
            if filter_log is not None:
                self._values["filter_log"] = filter_log

        @builtins.property
        def error_log(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-linkapplicationlogsampling.html#cfn-rtbfabric-inboundexternallink-linkapplicationlogsampling-errorlog
            '''
            result = self._values.get("error_log")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def filter_log(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-linkapplicationlogsampling.html#cfn-rtbfabric-inboundexternallink-linkapplicationlogsampling-filterlog
            '''
            result = self._values.get("filter_log")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkApplicationLogSamplingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnInboundExternalLinkPropsMixin.LinkAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_provided_id": "customerProvidedId",
            "responder_error_masking": "responderErrorMasking",
        },
    )
    class LinkAttributesProperty:
        def __init__(
            self,
            *,
            customer_provided_id: typing.Optional[builtins.str] = None,
            responder_error_masking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param customer_provided_id: 
            :param responder_error_masking: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-linkattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                link_attributes_property = rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkAttributesProperty(
                    customer_provided_id="customerProvidedId",
                    responder_error_masking=[rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                        action="action",
                        http_code="httpCode",
                        logging_types=["loggingTypes"],
                        response_logging_percentage=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d8a78fe694a8caf6454484c37eb615eff9194ae1b828d79f814c5d10505d76f)
                check_type(argname="argument customer_provided_id", value=customer_provided_id, expected_type=type_hints["customer_provided_id"])
                check_type(argname="argument responder_error_masking", value=responder_error_masking, expected_type=type_hints["responder_error_masking"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_provided_id is not None:
                self._values["customer_provided_id"] = customer_provided_id
            if responder_error_masking is not None:
                self._values["responder_error_masking"] = responder_error_masking

        @builtins.property
        def customer_provided_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-linkattributes.html#cfn-rtbfabric-inboundexternallink-linkattributes-customerprovidedid
            '''
            result = self._values.get("customer_provided_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def responder_error_masking(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-linkattributes.html#cfn-rtbfabric-inboundexternallink-linkattributes-respondererrormasking
            '''
            result = self._values.get("responder_error_masking")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnInboundExternalLinkPropsMixin.LinkLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"application_logs": "applicationLogs"},
    )
    class LinkLogSettingsProperty:
        def __init__(
            self,
            *,
            application_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInboundExternalLinkPropsMixin.ApplicationLogsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param application_logs: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-linklogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                link_log_settings_property = rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkLogSettingsProperty(
                    application_logs=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.ApplicationLogsProperty(
                        link_application_log_sampling=rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                            error_log=123,
                            filter_log=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__029035f103da3c97bf83df8090286f2fb08aec0cae2533c9d4badac363f2dcfc)
                check_type(argname="argument application_logs", value=application_logs, expected_type=type_hints["application_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_logs is not None:
                self._values["application_logs"] = application_logs

        @builtins.property
        def application_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.ApplicationLogsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-linklogsettings.html#cfn-rtbfabric-inboundexternallink-linklogsettings-applicationlogs
            '''
            result = self._values.get("application_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInboundExternalLinkPropsMixin.ApplicationLogsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnInboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "http_code": "httpCode",
            "logging_types": "loggingTypes",
            "response_logging_percentage": "responseLoggingPercentage",
        },
    )
    class ResponderErrorMaskingForHttpCodeProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            http_code: typing.Optional[builtins.str] = None,
            logging_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            response_logging_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param action: 
            :param http_code: 
            :param logging_types: 
            :param response_logging_percentage: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-respondererrormaskingforhttpcode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                responder_error_masking_for_http_code_property = rtbfabric_mixins.CfnInboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                    action="action",
                    http_code="httpCode",
                    logging_types=["loggingTypes"],
                    response_logging_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__496baeb78356149c63f8a78321c5f35a2f03774f0fb7178682278b3b743cc6b2)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument http_code", value=http_code, expected_type=type_hints["http_code"])
                check_type(argname="argument logging_types", value=logging_types, expected_type=type_hints["logging_types"])
                check_type(argname="argument response_logging_percentage", value=response_logging_percentage, expected_type=type_hints["response_logging_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if http_code is not None:
                self._values["http_code"] = http_code
            if logging_types is not None:
                self._values["logging_types"] = logging_types
            if response_logging_percentage is not None:
                self._values["response_logging_percentage"] = response_logging_percentage

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-respondererrormaskingforhttpcode.html#cfn-rtbfabric-inboundexternallink-respondererrormaskingforhttpcode-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_code(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-respondererrormaskingforhttpcode.html#cfn-rtbfabric-inboundexternallink-respondererrormaskingforhttpcode-httpcode
            '''
            result = self._values.get("http_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logging_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-respondererrormaskingforhttpcode.html#cfn-rtbfabric-inboundexternallink-respondererrormaskingforhttpcode-loggingtypes
            '''
            result = self._values.get("logging_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def response_logging_percentage(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-inboundexternallink-respondererrormaskingforhttpcode.html#cfn-rtbfabric-inboundexternallink-respondererrormaskingforhttpcode-responseloggingpercentage
            '''
            result = self._values.get("response_logging_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResponderErrorMaskingForHttpCodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_id": "gatewayId",
        "http_responder_allowed": "httpResponderAllowed",
        "link_attributes": "linkAttributes",
        "link_log_settings": "linkLogSettings",
        "module_configuration_list": "moduleConfigurationList",
        "peer_gateway_id": "peerGatewayId",
        "tags": "tags",
    },
)
class CfnLinkMixinProps:
    def __init__(
        self,
        *,
        gateway_id: typing.Optional[builtins.str] = None,
        http_responder_allowed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        link_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.LinkAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        link_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.LinkLogSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        module_configuration_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.ModuleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        peer_gateway_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLinkPropsMixin.

        :param gateway_id: The unique identifier of the gateway.
        :param http_responder_allowed: Boolean to specify if an HTTP responder is allowed.
        :param link_attributes: Attributes of the link.
        :param link_log_settings: Settings for the application logs.
        :param module_configuration_list: 
        :param peer_gateway_id: The unique identifier of the peer gateway.
        :param tags: A map of the key-value pairs of the tag or tags to assign to the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-link.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
            
            cfn_link_mixin_props = rtbfabric_mixins.CfnLinkMixinProps(
                gateway_id="gatewayId",
                http_responder_allowed=False,
                link_attributes=rtbfabric_mixins.CfnLinkPropsMixin.LinkAttributesProperty(
                    customer_provided_id="customerProvidedId",
                    responder_error_masking=[rtbfabric_mixins.CfnLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                        action="action",
                        http_code="httpCode",
                        logging_types=["loggingTypes"],
                        response_logging_percentage=123
                    )]
                ),
                link_log_settings=rtbfabric_mixins.CfnLinkPropsMixin.LinkLogSettingsProperty(
                    application_logs=rtbfabric_mixins.CfnLinkPropsMixin.ApplicationLogsProperty(
                        link_application_log_sampling=rtbfabric_mixins.CfnLinkPropsMixin.LinkApplicationLogSamplingProperty(
                            error_log=123,
                            filter_log=123
                        )
                    )
                ),
                module_configuration_list=[rtbfabric_mixins.CfnLinkPropsMixin.ModuleConfigurationProperty(
                    depends_on=["dependsOn"],
                    module_parameters=rtbfabric_mixins.CfnLinkPropsMixin.ModuleParametersProperty(
                        no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidModuleParametersProperty(
                            pass_through_percentage=123,
                            reason="reason",
                            reason_code=123
                        ),
                        open_rtb_attribute=rtbfabric_mixins.CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty(
                            action=rtbfabric_mixins.CfnLinkPropsMixin.ActionProperty(
                                header_tag=rtbfabric_mixins.CfnLinkPropsMixin.HeaderTagActionProperty(
                                    name="name",
                                    value="value"
                                ),
                                no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidActionProperty(
                                    no_bid_reason_code=123
                                )
                            ),
                            filter_configuration=[rtbfabric_mixins.CfnLinkPropsMixin.FilterProperty(
                                criteria=[rtbfabric_mixins.CfnLinkPropsMixin.FilterCriterionProperty(
                                    path="path",
                                    values=["values"]
                                )]
                            )],
                            filter_type="filterType",
                            holdback_percentage=123
                        )
                    ),
                    name="name",
                    version="version"
                )],
                peer_gateway_id="peerGatewayId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3ff89fa52825055f8950344ffe82849dd00c7b9c5e9e701cd5aaa97c5d2ac1)
            check_type(argname="argument gateway_id", value=gateway_id, expected_type=type_hints["gateway_id"])
            check_type(argname="argument http_responder_allowed", value=http_responder_allowed, expected_type=type_hints["http_responder_allowed"])
            check_type(argname="argument link_attributes", value=link_attributes, expected_type=type_hints["link_attributes"])
            check_type(argname="argument link_log_settings", value=link_log_settings, expected_type=type_hints["link_log_settings"])
            check_type(argname="argument module_configuration_list", value=module_configuration_list, expected_type=type_hints["module_configuration_list"])
            check_type(argname="argument peer_gateway_id", value=peer_gateway_id, expected_type=type_hints["peer_gateway_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway_id is not None:
            self._values["gateway_id"] = gateway_id
        if http_responder_allowed is not None:
            self._values["http_responder_allowed"] = http_responder_allowed
        if link_attributes is not None:
            self._values["link_attributes"] = link_attributes
        if link_log_settings is not None:
            self._values["link_log_settings"] = link_log_settings
        if module_configuration_list is not None:
            self._values["module_configuration_list"] = module_configuration_list
        if peer_gateway_id is not None:
            self._values["peer_gateway_id"] = peer_gateway_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def gateway_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-link.html#cfn-rtbfabric-link-gatewayid
        '''
        result = self._values.get("gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_responder_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Boolean to specify if an HTTP responder is allowed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-link.html#cfn-rtbfabric-link-httpresponderallowed
        '''
        result = self._values.get("http_responder_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def link_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkAttributesProperty"]]:
        '''Attributes of the link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-link.html#cfn-rtbfabric-link-linkattributes
        '''
        result = self._values.get("link_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkAttributesProperty"]], result)

    @builtins.property
    def link_log_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkLogSettingsProperty"]]:
        '''Settings for the application logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-link.html#cfn-rtbfabric-link-linklogsettings
        '''
        result = self._values.get("link_log_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkLogSettingsProperty"]], result)

    @builtins.property
    def module_configuration_list(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ModuleConfigurationProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-link.html#cfn-rtbfabric-link-moduleconfigurationlist
        '''
        result = self._values.get("module_configuration_list")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ModuleConfigurationProperty"]]]], result)

    @builtins.property
    def peer_gateway_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the peer gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-link.html#cfn-rtbfabric-link-peergatewayid
        '''
        result = self._values.get("peer_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map of the key-value pairs of the tag or tags to assign to the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-link.html#cfn-rtbfabric-link-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLinkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLinkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin",
):
    '''Creates a new link between gateways.

    Establishes a connection that allows gateways to communicate and exchange bid requests and responses.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-link.html
    :cloudformationResource: AWS::RTBFabric::Link
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
        
        cfn_link_props_mixin = rtbfabric_mixins.CfnLinkPropsMixin(rtbfabric_mixins.CfnLinkMixinProps(
            gateway_id="gatewayId",
            http_responder_allowed=False,
            link_attributes=rtbfabric_mixins.CfnLinkPropsMixin.LinkAttributesProperty(
                customer_provided_id="customerProvidedId",
                responder_error_masking=[rtbfabric_mixins.CfnLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                    action="action",
                    http_code="httpCode",
                    logging_types=["loggingTypes"],
                    response_logging_percentage=123
                )]
            ),
            link_log_settings=rtbfabric_mixins.CfnLinkPropsMixin.LinkLogSettingsProperty(
                application_logs=rtbfabric_mixins.CfnLinkPropsMixin.ApplicationLogsProperty(
                    link_application_log_sampling=rtbfabric_mixins.CfnLinkPropsMixin.LinkApplicationLogSamplingProperty(
                        error_log=123,
                        filter_log=123
                    )
                )
            ),
            module_configuration_list=[rtbfabric_mixins.CfnLinkPropsMixin.ModuleConfigurationProperty(
                depends_on=["dependsOn"],
                module_parameters=rtbfabric_mixins.CfnLinkPropsMixin.ModuleParametersProperty(
                    no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidModuleParametersProperty(
                        pass_through_percentage=123,
                        reason="reason",
                        reason_code=123
                    ),
                    open_rtb_attribute=rtbfabric_mixins.CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty(
                        action=rtbfabric_mixins.CfnLinkPropsMixin.ActionProperty(
                            header_tag=rtbfabric_mixins.CfnLinkPropsMixin.HeaderTagActionProperty(
                                name="name",
                                value="value"
                            ),
                            no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidActionProperty(
                                no_bid_reason_code=123
                            )
                        ),
                        filter_configuration=[rtbfabric_mixins.CfnLinkPropsMixin.FilterProperty(
                            criteria=[rtbfabric_mixins.CfnLinkPropsMixin.FilterCriterionProperty(
                                path="path",
                                values=["values"]
                            )]
                        )],
                        filter_type="filterType",
                        holdback_percentage=123
                    )
                ),
                name="name",
                version="version"
            )],
            peer_gateway_id="peerGatewayId",
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
        props: typing.Union[CfnLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RTBFabric::Link``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66049fb8bb42cc1a202cf79cfc1532eb32b83808b4a872a507022ad8e83594c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e313ccd79e3625c537e8717af69254a9bd5d1b9c85e41cb030a459dd80918f2f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0524019da572c792d2a4b05c20b470d31439153978f2075bd018de8b98d69e4e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLinkMixinProps:
        return typing.cast(CfnLinkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"header_tag": "headerTag", "no_bid": "noBid"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            header_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.HeaderTagActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            no_bid: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.NoBidActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a bid action.

            :param header_tag: Describes the header tag for a bid action.
            :param no_bid: Describes the parameters of a no bid module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                action_property = rtbfabric_mixins.CfnLinkPropsMixin.ActionProperty(
                    header_tag=rtbfabric_mixins.CfnLinkPropsMixin.HeaderTagActionProperty(
                        name="name",
                        value="value"
                    ),
                    no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidActionProperty(
                        no_bid_reason_code=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77dbb802837e9b2968062565f05b85a53e72ef2da2e8ba0fb38c714324d237f5)
                check_type(argname="argument header_tag", value=header_tag, expected_type=type_hints["header_tag"])
                check_type(argname="argument no_bid", value=no_bid, expected_type=type_hints["no_bid"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_tag is not None:
                self._values["header_tag"] = header_tag
            if no_bid is not None:
                self._values["no_bid"] = no_bid

        @builtins.property
        def header_tag(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.HeaderTagActionProperty"]]:
            '''Describes the header tag for a bid action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-action.html#cfn-rtbfabric-link-action-headertag
            '''
            result = self._values.get("header_tag")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.HeaderTagActionProperty"]], result)

        @builtins.property
        def no_bid(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.NoBidActionProperty"]]:
            '''Describes the parameters of a no bid module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-action.html#cfn-rtbfabric-link-action-nobid
            '''
            result = self._values.get("no_bid")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.NoBidActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.ApplicationLogsProperty",
        jsii_struct_bases=[],
        name_mapping={"link_application_log_sampling": "linkApplicationLogSampling"},
    )
    class ApplicationLogsProperty:
        def __init__(
            self,
            *,
            link_application_log_sampling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.LinkApplicationLogSamplingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the configuration of a link application log.

            :param link_application_log_sampling: Describes a link application log sample.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-applicationlogs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                application_logs_property = rtbfabric_mixins.CfnLinkPropsMixin.ApplicationLogsProperty(
                    link_application_log_sampling=rtbfabric_mixins.CfnLinkPropsMixin.LinkApplicationLogSamplingProperty(
                        error_log=123,
                        filter_log=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09acbbc4b6bac4ca8f2844a4f2443935f82c2e6b547fab123a64749927f9ae92)
                check_type(argname="argument link_application_log_sampling", value=link_application_log_sampling, expected_type=type_hints["link_application_log_sampling"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if link_application_log_sampling is not None:
                self._values["link_application_log_sampling"] = link_application_log_sampling

        @builtins.property
        def link_application_log_sampling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkApplicationLogSamplingProperty"]]:
            '''Describes a link application log sample.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-applicationlogs.html#cfn-rtbfabric-link-applicationlogs-linkapplicationlogsampling
            '''
            result = self._values.get("link_application_log_sampling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkApplicationLogSamplingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationLogsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.FilterCriterionProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path", "values": "values"},
    )
    class FilterCriterionProperty:
        def __init__(
            self,
            *,
            path: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes the criteria for a filter.

            :param path: The path to filter.
            :param values: The value to filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-filtercriterion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                filter_criterion_property = rtbfabric_mixins.CfnLinkPropsMixin.FilterCriterionProperty(
                    path="path",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b64bdb92b50a8c1b59da54c1b346bcfb59e225f2ea1c5e089bcfdab5e55a540)
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path is not None:
                self._values["path"] = path
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The path to filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-filtercriterion.html#cfn-rtbfabric-link-filtercriterion-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The value to filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-filtercriterion.html#cfn-rtbfabric-link-filtercriterion-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterCriterionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"criteria": "criteria"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.FilterCriterionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes the configuration of a filter.

            :param criteria: Describes the criteria for a filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                filter_property = rtbfabric_mixins.CfnLinkPropsMixin.FilterProperty(
                    criteria=[rtbfabric_mixins.CfnLinkPropsMixin.FilterCriterionProperty(
                        path="path",
                        values=["values"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1964e86a723f4d656095ff45785706ec9aa2b69e50d9a99fdbe99f46df590ab)
                check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if criteria is not None:
                self._values["criteria"] = criteria

        @builtins.property
        def criteria(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.FilterCriterionProperty"]]]]:
            '''Describes the criteria for a filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-filter.html#cfn-rtbfabric-link-filter-criteria
            '''
            result = self._values.get("criteria")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.FilterCriterionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.HeaderTagActionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class HeaderTagActionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the header tag for a bid action.

            :param name: The name of the bid action.
            :param value: The value of the bid action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-headertagaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                header_tag_action_property = rtbfabric_mixins.CfnLinkPropsMixin.HeaderTagActionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2a128e08267fce9fd57012aa30fb12db4fa3797d49b51e715c7c980d540a160)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the bid action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-headertagaction.html#cfn-rtbfabric-link-headertagaction-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the bid action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-headertagaction.html#cfn-rtbfabric-link-headertagaction-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderTagActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.LinkApplicationLogSamplingProperty",
        jsii_struct_bases=[],
        name_mapping={"error_log": "errorLog", "filter_log": "filterLog"},
    )
    class LinkApplicationLogSamplingProperty:
        def __init__(
            self,
            *,
            error_log: typing.Optional[jsii.Number] = None,
            filter_log: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a link application log sample.

            :param error_log: An error log entry.
            :param filter_log: A filter log entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-linkapplicationlogsampling.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                link_application_log_sampling_property = rtbfabric_mixins.CfnLinkPropsMixin.LinkApplicationLogSamplingProperty(
                    error_log=123,
                    filter_log=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88be7d0c83549dccec57bbbb24859295c483d9aa0824e9a7d888c51e1b1068c2)
                check_type(argname="argument error_log", value=error_log, expected_type=type_hints["error_log"])
                check_type(argname="argument filter_log", value=filter_log, expected_type=type_hints["filter_log"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_log is not None:
                self._values["error_log"] = error_log
            if filter_log is not None:
                self._values["filter_log"] = filter_log

        @builtins.property
        def error_log(self) -> typing.Optional[jsii.Number]:
            '''An error log entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-linkapplicationlogsampling.html#cfn-rtbfabric-link-linkapplicationlogsampling-errorlog
            '''
            result = self._values.get("error_log")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def filter_log(self) -> typing.Optional[jsii.Number]:
            '''A filter log entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-linkapplicationlogsampling.html#cfn-rtbfabric-link-linkapplicationlogsampling-filterlog
            '''
            result = self._values.get("filter_log")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkApplicationLogSamplingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.LinkAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_provided_id": "customerProvidedId",
            "responder_error_masking": "responderErrorMasking",
        },
    )
    class LinkAttributesProperty:
        def __init__(
            self,
            *,
            customer_provided_id: typing.Optional[builtins.str] = None,
            responder_error_masking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes the attributes of a link.

            :param customer_provided_id: The customer-provided unique identifier of the link.
            :param responder_error_masking: Describes the masking for HTTP error codes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-linkattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                link_attributes_property = rtbfabric_mixins.CfnLinkPropsMixin.LinkAttributesProperty(
                    customer_provided_id="customerProvidedId",
                    responder_error_masking=[rtbfabric_mixins.CfnLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                        action="action",
                        http_code="httpCode",
                        logging_types=["loggingTypes"],
                        response_logging_percentage=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2aadc11f4c7497f05db358b5817b56e044e5e7ecbf1902d610ff28daebc02119)
                check_type(argname="argument customer_provided_id", value=customer_provided_id, expected_type=type_hints["customer_provided_id"])
                check_type(argname="argument responder_error_masking", value=responder_error_masking, expected_type=type_hints["responder_error_masking"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_provided_id is not None:
                self._values["customer_provided_id"] = customer_provided_id
            if responder_error_masking is not None:
                self._values["responder_error_masking"] = responder_error_masking

        @builtins.property
        def customer_provided_id(self) -> typing.Optional[builtins.str]:
            '''The customer-provided unique identifier of the link.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-linkattributes.html#cfn-rtbfabric-link-linkattributes-customerprovidedid
            '''
            result = self._values.get("customer_provided_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def responder_error_masking(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty"]]]]:
            '''Describes the masking for HTTP error codes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-linkattributes.html#cfn-rtbfabric-link-linkattributes-respondererrormasking
            '''
            result = self._values.get("responder_error_masking")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.LinkLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"application_logs": "applicationLogs"},
    )
    class LinkLogSettingsProperty:
        def __init__(
            self,
            *,
            application_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.ApplicationLogsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the settings for a link log.

            :param application_logs: Describes the configuration of a link application log.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-linklogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                link_log_settings_property = rtbfabric_mixins.CfnLinkPropsMixin.LinkLogSettingsProperty(
                    application_logs=rtbfabric_mixins.CfnLinkPropsMixin.ApplicationLogsProperty(
                        link_application_log_sampling=rtbfabric_mixins.CfnLinkPropsMixin.LinkApplicationLogSamplingProperty(
                            error_log=123,
                            filter_log=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__180e6c87c3669c27aaf8753f9c8db378f932989fad0ad077efa0814604da70bc)
                check_type(argname="argument application_logs", value=application_logs, expected_type=type_hints["application_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_logs is not None:
                self._values["application_logs"] = application_logs

        @builtins.property
        def application_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ApplicationLogsProperty"]]:
            '''Describes the configuration of a link application log.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-linklogsettings.html#cfn-rtbfabric-link-linklogsettings-applicationlogs
            '''
            result = self._values.get("application_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ApplicationLogsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.ModuleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "depends_on": "dependsOn",
            "module_parameters": "moduleParameters",
            "name": "name",
            "version": "version",
        },
    )
    class ModuleConfigurationProperty:
        def __init__(
            self,
            *,
            depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
            module_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.ModuleParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration of a module.

            :param depends_on: The dependencies of the module.
            :param module_parameters: Describes the parameters of a module.
            :param name: The name of the module.
            :param version: The version of the module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-moduleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                module_configuration_property = rtbfabric_mixins.CfnLinkPropsMixin.ModuleConfigurationProperty(
                    depends_on=["dependsOn"],
                    module_parameters=rtbfabric_mixins.CfnLinkPropsMixin.ModuleParametersProperty(
                        no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidModuleParametersProperty(
                            pass_through_percentage=123,
                            reason="reason",
                            reason_code=123
                        ),
                        open_rtb_attribute=rtbfabric_mixins.CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty(
                            action=rtbfabric_mixins.CfnLinkPropsMixin.ActionProperty(
                                header_tag=rtbfabric_mixins.CfnLinkPropsMixin.HeaderTagActionProperty(
                                    name="name",
                                    value="value"
                                ),
                                no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidActionProperty(
                                    no_bid_reason_code=123
                                )
                            ),
                            filter_configuration=[rtbfabric_mixins.CfnLinkPropsMixin.FilterProperty(
                                criteria=[rtbfabric_mixins.CfnLinkPropsMixin.FilterCriterionProperty(
                                    path="path",
                                    values=["values"]
                                )]
                            )],
                            filter_type="filterType",
                            holdback_percentage=123
                        )
                    ),
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fddaa78343fbbe80298058010d12fb55e223e400110c279920022b8c98503bf)
                check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
                check_type(argname="argument module_parameters", value=module_parameters, expected_type=type_hints["module_parameters"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if depends_on is not None:
                self._values["depends_on"] = depends_on
            if module_parameters is not None:
                self._values["module_parameters"] = module_parameters
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The dependencies of the module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-moduleconfiguration.html#cfn-rtbfabric-link-moduleconfiguration-dependson
            '''
            result = self._values.get("depends_on")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def module_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ModuleParametersProperty"]]:
            '''Describes the parameters of a module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-moduleconfiguration.html#cfn-rtbfabric-link-moduleconfiguration-moduleparameters
            '''
            result = self._values.get("module_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ModuleParametersProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-moduleconfiguration.html#cfn-rtbfabric-link-moduleconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-moduleconfiguration.html#cfn-rtbfabric-link-moduleconfiguration-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ModuleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.ModuleParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"no_bid": "noBid", "open_rtb_attribute": "openRtbAttribute"},
    )
    class ModuleParametersProperty:
        def __init__(
            self,
            *,
            no_bid: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.NoBidModuleParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            open_rtb_attribute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the parameters of a module.

            :param no_bid: Describes the parameters of a no bid module.
            :param open_rtb_attribute: Describes the parameters of an open RTB attribute module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-moduleparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                module_parameters_property = rtbfabric_mixins.CfnLinkPropsMixin.ModuleParametersProperty(
                    no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidModuleParametersProperty(
                        pass_through_percentage=123,
                        reason="reason",
                        reason_code=123
                    ),
                    open_rtb_attribute=rtbfabric_mixins.CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty(
                        action=rtbfabric_mixins.CfnLinkPropsMixin.ActionProperty(
                            header_tag=rtbfabric_mixins.CfnLinkPropsMixin.HeaderTagActionProperty(
                                name="name",
                                value="value"
                            ),
                            no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidActionProperty(
                                no_bid_reason_code=123
                            )
                        ),
                        filter_configuration=[rtbfabric_mixins.CfnLinkPropsMixin.FilterProperty(
                            criteria=[rtbfabric_mixins.CfnLinkPropsMixin.FilterCriterionProperty(
                                path="path",
                                values=["values"]
                            )]
                        )],
                        filter_type="filterType",
                        holdback_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90e7e69a9573ae87da5a47ac6a13d9f268721082f2838cdfde1454d15d2dabfc)
                check_type(argname="argument no_bid", value=no_bid, expected_type=type_hints["no_bid"])
                check_type(argname="argument open_rtb_attribute", value=open_rtb_attribute, expected_type=type_hints["open_rtb_attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if no_bid is not None:
                self._values["no_bid"] = no_bid
            if open_rtb_attribute is not None:
                self._values["open_rtb_attribute"] = open_rtb_attribute

        @builtins.property
        def no_bid(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.NoBidModuleParametersProperty"]]:
            '''Describes the parameters of a no bid module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-moduleparameters.html#cfn-rtbfabric-link-moduleparameters-nobid
            '''
            result = self._values.get("no_bid")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.NoBidModuleParametersProperty"]], result)

        @builtins.property
        def open_rtb_attribute(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty"]]:
            '''Describes the parameters of an open RTB attribute module.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-moduleparameters.html#cfn-rtbfabric-link-moduleparameters-openrtbattribute
            '''
            result = self._values.get("open_rtb_attribute")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ModuleParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.NoBidActionProperty",
        jsii_struct_bases=[],
        name_mapping={"no_bid_reason_code": "noBidReasonCode"},
    )
    class NoBidActionProperty:
        def __init__(
            self,
            *,
            no_bid_reason_code: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a no bid action.

            :param no_bid_reason_code: The reason code for the no bid action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-nobidaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                no_bid_action_property = rtbfabric_mixins.CfnLinkPropsMixin.NoBidActionProperty(
                    no_bid_reason_code=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d473b110f54c549009384b109b2709d9f187cae87d17df426db465a8481aba76)
                check_type(argname="argument no_bid_reason_code", value=no_bid_reason_code, expected_type=type_hints["no_bid_reason_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if no_bid_reason_code is not None:
                self._values["no_bid_reason_code"] = no_bid_reason_code

        @builtins.property
        def no_bid_reason_code(self) -> typing.Optional[jsii.Number]:
            '''The reason code for the no bid action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-nobidaction.html#cfn-rtbfabric-link-nobidaction-nobidreasoncode
            '''
            result = self._values.get("no_bid_reason_code")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NoBidActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.NoBidModuleParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pass_through_percentage": "passThroughPercentage",
            "reason": "reason",
            "reason_code": "reasonCode",
        },
    )
    class NoBidModuleParametersProperty:
        def __init__(
            self,
            *,
            pass_through_percentage: typing.Optional[jsii.Number] = None,
            reason: typing.Optional[builtins.str] = None,
            reason_code: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the parameters of a no bid module.

            :param pass_through_percentage: The pass through percentage.
            :param reason: The reason description.
            :param reason_code: The reason code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-nobidmoduleparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                no_bid_module_parameters_property = rtbfabric_mixins.CfnLinkPropsMixin.NoBidModuleParametersProperty(
                    pass_through_percentage=123,
                    reason="reason",
                    reason_code=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3081571623474d6ee6303ad845c1638cbb985a94cf373f6e2f72b7a590b4bde)
                check_type(argname="argument pass_through_percentage", value=pass_through_percentage, expected_type=type_hints["pass_through_percentage"])
                check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                check_type(argname="argument reason_code", value=reason_code, expected_type=type_hints["reason_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pass_through_percentage is not None:
                self._values["pass_through_percentage"] = pass_through_percentage
            if reason is not None:
                self._values["reason"] = reason
            if reason_code is not None:
                self._values["reason_code"] = reason_code

        @builtins.property
        def pass_through_percentage(self) -> typing.Optional[jsii.Number]:
            '''The pass through percentage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-nobidmoduleparameters.html#cfn-rtbfabric-link-nobidmoduleparameters-passthroughpercentage
            '''
            result = self._values.get("pass_through_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def reason(self) -> typing.Optional[builtins.str]:
            '''The reason description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-nobidmoduleparameters.html#cfn-rtbfabric-link-nobidmoduleparameters-reason
            '''
            result = self._values.get("reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reason_code(self) -> typing.Optional[jsii.Number]:
            '''The reason code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-nobidmoduleparameters.html#cfn-rtbfabric-link-nobidmoduleparameters-reasoncode
            '''
            result = self._values.get("reason_code")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NoBidModuleParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "filter_configuration": "filterConfiguration",
            "filter_type": "filterType",
            "holdback_percentage": "holdbackPercentage",
        },
    )
    class OpenRtbAttributeModuleParametersProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.FilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            filter_type: typing.Optional[builtins.str] = None,
            holdback_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the parameters of an open RTB attribute module.

            :param action: Describes a bid action.
            :param filter_configuration: Describes the configuration of a filter.
            :param filter_type: The filter type.
            :param holdback_percentage: The hold back percentage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-openrtbattributemoduleparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                open_rtb_attribute_module_parameters_property = rtbfabric_mixins.CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty(
                    action=rtbfabric_mixins.CfnLinkPropsMixin.ActionProperty(
                        header_tag=rtbfabric_mixins.CfnLinkPropsMixin.HeaderTagActionProperty(
                            name="name",
                            value="value"
                        ),
                        no_bid=rtbfabric_mixins.CfnLinkPropsMixin.NoBidActionProperty(
                            no_bid_reason_code=123
                        )
                    ),
                    filter_configuration=[rtbfabric_mixins.CfnLinkPropsMixin.FilterProperty(
                        criteria=[rtbfabric_mixins.CfnLinkPropsMixin.FilterCriterionProperty(
                            path="path",
                            values=["values"]
                        )]
                    )],
                    filter_type="filterType",
                    holdback_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49718a4eee4792d4bd50e8cc8326770bf925ef4b8e1d0169fd9dd3f5ddbab1d9)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument filter_configuration", value=filter_configuration, expected_type=type_hints["filter_configuration"])
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
                check_type(argname="argument holdback_percentage", value=holdback_percentage, expected_type=type_hints["holdback_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if filter_configuration is not None:
                self._values["filter_configuration"] = filter_configuration
            if filter_type is not None:
                self._values["filter_type"] = filter_type
            if holdback_percentage is not None:
                self._values["holdback_percentage"] = holdback_percentage

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ActionProperty"]]:
            '''Describes a bid action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-openrtbattributemoduleparameters.html#cfn-rtbfabric-link-openrtbattributemoduleparameters-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.ActionProperty"]], result)

        @builtins.property
        def filter_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.FilterProperty"]]]]:
            '''Describes the configuration of a filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-openrtbattributemoduleparameters.html#cfn-rtbfabric-link-openrtbattributemoduleparameters-filterconfiguration
            '''
            result = self._values.get("filter_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.FilterProperty"]]]], result)

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The filter type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-openrtbattributemoduleparameters.html#cfn-rtbfabric-link-openrtbattributemoduleparameters-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def holdback_percentage(self) -> typing.Optional[jsii.Number]:
            '''The hold back percentage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-openrtbattributemoduleparameters.html#cfn-rtbfabric-link-openrtbattributemoduleparameters-holdbackpercentage
            '''
            result = self._values.get("holdback_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenRtbAttributeModuleParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "http_code": "httpCode",
            "logging_types": "loggingTypes",
            "response_logging_percentage": "responseLoggingPercentage",
        },
    )
    class ResponderErrorMaskingForHttpCodeProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            http_code: typing.Optional[builtins.str] = None,
            logging_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            response_logging_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the masking for HTTP error codes.

            :param action: The action for the error..
            :param http_code: The HTTP error code.
            :param logging_types: The error log type.
            :param response_logging_percentage: The percentage of response logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-respondererrormaskingforhttpcode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                responder_error_masking_for_http_code_property = rtbfabric_mixins.CfnLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                    action="action",
                    http_code="httpCode",
                    logging_types=["loggingTypes"],
                    response_logging_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4695ccddcd911c9a194e85d87f44b0d6f68061080c9d263359f32293cf95c02f)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument http_code", value=http_code, expected_type=type_hints["http_code"])
                check_type(argname="argument logging_types", value=logging_types, expected_type=type_hints["logging_types"])
                check_type(argname="argument response_logging_percentage", value=response_logging_percentage, expected_type=type_hints["response_logging_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if http_code is not None:
                self._values["http_code"] = http_code
            if logging_types is not None:
                self._values["logging_types"] = logging_types
            if response_logging_percentage is not None:
                self._values["response_logging_percentage"] = response_logging_percentage

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action for the error..

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-respondererrormaskingforhttpcode.html#cfn-rtbfabric-link-respondererrormaskingforhttpcode-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_code(self) -> typing.Optional[builtins.str]:
            '''The HTTP error code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-respondererrormaskingforhttpcode.html#cfn-rtbfabric-link-respondererrormaskingforhttpcode-httpcode
            '''
            result = self._values.get("http_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logging_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The error log type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-respondererrormaskingforhttpcode.html#cfn-rtbfabric-link-respondererrormaskingforhttpcode-loggingtypes
            '''
            result = self._values.get("logging_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def response_logging_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of response logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-link-respondererrormaskingforhttpcode.html#cfn-rtbfabric-link-respondererrormaskingforhttpcode-responseloggingpercentage
            '''
            result = self._values.get("response_logging_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResponderErrorMaskingForHttpCodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnOutboundExternalLinkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_id": "gatewayId",
        "link_attributes": "linkAttributes",
        "link_log_settings": "linkLogSettings",
        "public_endpoint": "publicEndpoint",
        "tags": "tags",
    },
)
class CfnOutboundExternalLinkMixinProps:
    def __init__(
        self,
        *,
        gateway_id: typing.Optional[builtins.str] = None,
        link_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOutboundExternalLinkPropsMixin.LinkAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        link_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOutboundExternalLinkPropsMixin.LinkLogSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        public_endpoint: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOutboundExternalLinkPropsMixin.

        :param gateway_id: 
        :param link_attributes: 
        :param link_log_settings: 
        :param public_endpoint: 
        :param tags: Tags to assign to the Link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-outboundexternallink.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
            
            cfn_outbound_external_link_mixin_props = rtbfabric_mixins.CfnOutboundExternalLinkMixinProps(
                gateway_id="gatewayId",
                link_attributes=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkAttributesProperty(
                    customer_provided_id="customerProvidedId",
                    responder_error_masking=[rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                        action="action",
                        http_code="httpCode",
                        logging_types=["loggingTypes"],
                        response_logging_percentage=123
                    )]
                ),
                link_log_settings=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkLogSettingsProperty(
                    application_logs=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.ApplicationLogsProperty(
                        link_application_log_sampling=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                            error_log=123,
                            filter_log=123
                        )
                    )
                ),
                public_endpoint="publicEndpoint",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ad5275d3c39b39280d0d61e506f9a8e17d1d1a0819aeebd45ea09a0b859863)
            check_type(argname="argument gateway_id", value=gateway_id, expected_type=type_hints["gateway_id"])
            check_type(argname="argument link_attributes", value=link_attributes, expected_type=type_hints["link_attributes"])
            check_type(argname="argument link_log_settings", value=link_log_settings, expected_type=type_hints["link_log_settings"])
            check_type(argname="argument public_endpoint", value=public_endpoint, expected_type=type_hints["public_endpoint"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway_id is not None:
            self._values["gateway_id"] = gateway_id
        if link_attributes is not None:
            self._values["link_attributes"] = link_attributes
        if link_log_settings is not None:
            self._values["link_log_settings"] = link_log_settings
        if public_endpoint is not None:
            self._values["public_endpoint"] = public_endpoint
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def gateway_id(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-outboundexternallink.html#cfn-rtbfabric-outboundexternallink-gatewayid
        '''
        result = self._values.get("gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.LinkAttributesProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-outboundexternallink.html#cfn-rtbfabric-outboundexternallink-linkattributes
        '''
        result = self._values.get("link_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.LinkAttributesProperty"]], result)

    @builtins.property
    def link_log_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.LinkLogSettingsProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-outboundexternallink.html#cfn-rtbfabric-outboundexternallink-linklogsettings
        '''
        result = self._values.get("link_log_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.LinkLogSettingsProperty"]], result)

    @builtins.property
    def public_endpoint(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-outboundexternallink.html#cfn-rtbfabric-outboundexternallink-publicendpoint
        '''
        result = self._values.get("public_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags to assign to the Link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-outboundexternallink.html#cfn-rtbfabric-outboundexternallink-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOutboundExternalLinkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOutboundExternalLinkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnOutboundExternalLinkPropsMixin",
):
    '''Resource Type definition for AWS::RTBFabric::OutboundExternalLink Resource Type.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-outboundexternallink.html
    :cloudformationResource: AWS::RTBFabric::OutboundExternalLink
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
        
        cfn_outbound_external_link_props_mixin = rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin(rtbfabric_mixins.CfnOutboundExternalLinkMixinProps(
            gateway_id="gatewayId",
            link_attributes=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkAttributesProperty(
                customer_provided_id="customerProvidedId",
                responder_error_masking=[rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                    action="action",
                    http_code="httpCode",
                    logging_types=["loggingTypes"],
                    response_logging_percentage=123
                )]
            ),
            link_log_settings=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkLogSettingsProperty(
                application_logs=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.ApplicationLogsProperty(
                    link_application_log_sampling=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                        error_log=123,
                        filter_log=123
                    )
                )
            ),
            public_endpoint="publicEndpoint",
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
        props: typing.Union[CfnOutboundExternalLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RTBFabric::OutboundExternalLink``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb69b27465c9ec182e5c22aba12efa3f9b0355d2df7ba6212c000feaf675012)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b8d859731bad5da9f8862b8f8ec8e0890f5dfb55658dee3caee3bbafa47a29d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b29c7cb1272860d1ff60ae744c5b9f7348f7e0affc6119d744270b3ee96e13)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOutboundExternalLinkMixinProps:
        return typing.cast(CfnOutboundExternalLinkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnOutboundExternalLinkPropsMixin.ApplicationLogsProperty",
        jsii_struct_bases=[],
        name_mapping={"link_application_log_sampling": "linkApplicationLogSampling"},
    )
    class ApplicationLogsProperty:
        def __init__(
            self,
            *,
            link_application_log_sampling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param link_application_log_sampling: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-applicationlogs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                application_logs_property = rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.ApplicationLogsProperty(
                    link_application_log_sampling=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                        error_log=123,
                        filter_log=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3c3a5def8bbb013e5a83459ee0beabfa387dccfed6c70b721b2efb13001549e)
                check_type(argname="argument link_application_log_sampling", value=link_application_log_sampling, expected_type=type_hints["link_application_log_sampling"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if link_application_log_sampling is not None:
                self._values["link_application_log_sampling"] = link_application_log_sampling

        @builtins.property
        def link_application_log_sampling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-applicationlogs.html#cfn-rtbfabric-outboundexternallink-applicationlogs-linkapplicationlogsampling
            '''
            result = self._values.get("link_application_log_sampling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationLogsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty",
        jsii_struct_bases=[],
        name_mapping={"error_log": "errorLog", "filter_log": "filterLog"},
    )
    class LinkApplicationLogSamplingProperty:
        def __init__(
            self,
            *,
            error_log: typing.Optional[jsii.Number] = None,
            filter_log: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param error_log: 
            :param filter_log: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-linkapplicationlogsampling.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                link_application_log_sampling_property = rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                    error_log=123,
                    filter_log=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93ac55424e3df1eed8f90aa49120e59a6ccc0e6ad72c0772f2d2c680d3b1ca62)
                check_type(argname="argument error_log", value=error_log, expected_type=type_hints["error_log"])
                check_type(argname="argument filter_log", value=filter_log, expected_type=type_hints["filter_log"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_log is not None:
                self._values["error_log"] = error_log
            if filter_log is not None:
                self._values["filter_log"] = filter_log

        @builtins.property
        def error_log(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-linkapplicationlogsampling.html#cfn-rtbfabric-outboundexternallink-linkapplicationlogsampling-errorlog
            '''
            result = self._values.get("error_log")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def filter_log(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-linkapplicationlogsampling.html#cfn-rtbfabric-outboundexternallink-linkapplicationlogsampling-filterlog
            '''
            result = self._values.get("filter_log")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkApplicationLogSamplingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnOutboundExternalLinkPropsMixin.LinkAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_provided_id": "customerProvidedId",
            "responder_error_masking": "responderErrorMasking",
        },
    )
    class LinkAttributesProperty:
        def __init__(
            self,
            *,
            customer_provided_id: typing.Optional[builtins.str] = None,
            responder_error_masking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOutboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param customer_provided_id: 
            :param responder_error_masking: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-linkattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                link_attributes_property = rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkAttributesProperty(
                    customer_provided_id="customerProvidedId",
                    responder_error_masking=[rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                        action="action",
                        http_code="httpCode",
                        logging_types=["loggingTypes"],
                        response_logging_percentage=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__faa474de1a17d644097fe0bddd48fb2813f0b52108ba962364aabda934e6f334)
                check_type(argname="argument customer_provided_id", value=customer_provided_id, expected_type=type_hints["customer_provided_id"])
                check_type(argname="argument responder_error_masking", value=responder_error_masking, expected_type=type_hints["responder_error_masking"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_provided_id is not None:
                self._values["customer_provided_id"] = customer_provided_id
            if responder_error_masking is not None:
                self._values["responder_error_masking"] = responder_error_masking

        @builtins.property
        def customer_provided_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-linkattributes.html#cfn-rtbfabric-outboundexternallink-linkattributes-customerprovidedid
            '''
            result = self._values.get("customer_provided_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def responder_error_masking(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-linkattributes.html#cfn-rtbfabric-outboundexternallink-linkattributes-respondererrormasking
            '''
            result = self._values.get("responder_error_masking")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnOutboundExternalLinkPropsMixin.LinkLogSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"application_logs": "applicationLogs"},
    )
    class LinkLogSettingsProperty:
        def __init__(
            self,
            *,
            application_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnOutboundExternalLinkPropsMixin.ApplicationLogsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param application_logs: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-linklogsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                link_log_settings_property = rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkLogSettingsProperty(
                    application_logs=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.ApplicationLogsProperty(
                        link_application_log_sampling=rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty(
                            error_log=123,
                            filter_log=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afb168c58e137274458dfe0fdda93a6fd8e912dfc7300d2f9dd9942b3f11fa71)
                check_type(argname="argument application_logs", value=application_logs, expected_type=type_hints["application_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_logs is not None:
                self._values["application_logs"] = application_logs

        @builtins.property
        def application_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.ApplicationLogsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-linklogsettings.html#cfn-rtbfabric-outboundexternallink-linklogsettings-applicationlogs
            '''
            result = self._values.get("application_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnOutboundExternalLinkPropsMixin.ApplicationLogsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkLogSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnOutboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "http_code": "httpCode",
            "logging_types": "loggingTypes",
            "response_logging_percentage": "responseLoggingPercentage",
        },
    )
    class ResponderErrorMaskingForHttpCodeProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            http_code: typing.Optional[builtins.str] = None,
            logging_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            response_logging_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param action: 
            :param http_code: 
            :param logging_types: 
            :param response_logging_percentage: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-respondererrormaskingforhttpcode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                responder_error_masking_for_http_code_property = rtbfabric_mixins.CfnOutboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty(
                    action="action",
                    http_code="httpCode",
                    logging_types=["loggingTypes"],
                    response_logging_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd1e7aa13d2f09dc7f909db5c1a8cc611c5dbf113bd1ee99c7e722be87c3b6df)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument http_code", value=http_code, expected_type=type_hints["http_code"])
                check_type(argname="argument logging_types", value=logging_types, expected_type=type_hints["logging_types"])
                check_type(argname="argument response_logging_percentage", value=response_logging_percentage, expected_type=type_hints["response_logging_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if http_code is not None:
                self._values["http_code"] = http_code
            if logging_types is not None:
                self._values["logging_types"] = logging_types
            if response_logging_percentage is not None:
                self._values["response_logging_percentage"] = response_logging_percentage

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-respondererrormaskingforhttpcode.html#cfn-rtbfabric-outboundexternallink-respondererrormaskingforhttpcode-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_code(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-respondererrormaskingforhttpcode.html#cfn-rtbfabric-outboundexternallink-respondererrormaskingforhttpcode-httpcode
            '''
            result = self._values.get("http_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logging_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-respondererrormaskingforhttpcode.html#cfn-rtbfabric-outboundexternallink-respondererrormaskingforhttpcode-loggingtypes
            '''
            result = self._values.get("logging_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def response_logging_percentage(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-outboundexternallink-respondererrormaskingforhttpcode.html#cfn-rtbfabric-outboundexternallink-respondererrormaskingforhttpcode-responseloggingpercentage
            '''
            result = self._values.get("response_logging_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResponderErrorMaskingForHttpCodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnRequesterGatewayMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "vpc_id": "vpcId",
    },
)
class CfnRequesterGatewayMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRequesterGatewayPropsMixin.

        :param description: An optional description for the requester gateway.
        :param security_group_ids: The unique identifiers of the security groups.
        :param subnet_ids: The unique identifiers of the subnets.
        :param tags: A map of the key-value pairs of the tag or tags to assign to the resource.
        :param vpc_id: The unique identifier of the Virtual Private Cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-requestergateway.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
            
            cfn_requester_gateway_mixin_props = rtbfabric_mixins.CfnRequesterGatewayMixinProps(
                description="description",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ffe299131038ab7ef3a31d25d8c02d39df01b0eef4141a047f5fdabe9de5d73)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the requester gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-requestergateway.html#cfn-rtbfabric-requestergateway-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the security groups.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-requestergateway.html#cfn-rtbfabric-requestergateway-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the subnets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-requestergateway.html#cfn-rtbfabric-requestergateway-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map of the key-value pairs of the tag or tags to assign to the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-requestergateway.html#cfn-rtbfabric-requestergateway-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Virtual Private Cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-requestergateway.html#cfn-rtbfabric-requestergateway-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRequesterGatewayMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRequesterGatewayPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnRequesterGatewayPropsMixin",
):
    '''Creates a requester gateway.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-requestergateway.html
    :cloudformationResource: AWS::RTBFabric::RequesterGateway
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
        
        cfn_requester_gateway_props_mixin = rtbfabric_mixins.CfnRequesterGatewayPropsMixin(rtbfabric_mixins.CfnRequesterGatewayMixinProps(
            description="description",
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
        props: typing.Union[CfnRequesterGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RTBFabric::RequesterGateway``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e32fde45ce339041e4e0abc34ec9a6c961062d3056d424c46fe9a92bcdde110)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dfea8a8317e37520520a1f767cdba2247b7830420928c474e74b9f73d223537)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606b596bd8cfcaa85552dcb609075b76bcbfbe158d52e01efc6ca4b3bf320c2a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRequesterGatewayMixinProps:
        return typing.cast(CfnRequesterGatewayMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnResponderGatewayMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "domain_name": "domainName",
        "managed_endpoint_configuration": "managedEndpointConfiguration",
        "port": "port",
        "protocol": "protocol",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "trust_store_configuration": "trustStoreConfiguration",
        "vpc_id": "vpcId",
    },
)
class CfnResponderGatewayMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        managed_endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponderGatewayPropsMixin.ManagedEndpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trust_store_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponderGatewayPropsMixin.TrustStoreConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResponderGatewayPropsMixin.

        :param description: An optional description for the responder gateway.
        :param domain_name: The domain name for the responder gateway.
        :param managed_endpoint_configuration: The configuration for the managed endpoint.
        :param port: The networking port to use.
        :param protocol: The networking protocol to use.
        :param security_group_ids: The unique identifiers of the security groups.
        :param subnet_ids: The unique identifiers of the subnets.
        :param tags: A map of the key-value pairs of the tag or tags to assign to the resource.
        :param trust_store_configuration: The configuration of the trust store.
        :param vpc_id: The unique identifier of the Virtual Private Cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
            
            cfn_responder_gateway_mixin_props = rtbfabric_mixins.CfnResponderGatewayMixinProps(
                description="description",
                domain_name="domainName",
                managed_endpoint_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.ManagedEndpointConfigurationProperty(
                    auto_scaling_groups_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.AutoScalingGroupsConfigurationProperty(
                        auto_scaling_group_name_list=["autoScalingGroupNameList"],
                        role_arn="roleArn"
                    ),
                    eks_endpoints_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.EksEndpointsConfigurationProperty(
                        cluster_api_server_ca_certificate_chain="clusterApiServerCaCertificateChain",
                        cluster_api_server_endpoint_uri="clusterApiServerEndpointUri",
                        cluster_name="clusterName",
                        endpoints_resource_name="endpointsResourceName",
                        endpoints_resource_namespace="endpointsResourceNamespace",
                        role_arn="roleArn"
                    )
                ),
                port=123,
                protocol="protocol",
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trust_store_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.TrustStoreConfigurationProperty(
                    certificate_authority_certificates=["certificateAuthorityCertificates"]
                ),
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6919fd42f9a23f4293e6d2ebad74fe785f75f059526700ea40e2baaa6d37c16)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument managed_endpoint_configuration", value=managed_endpoint_configuration, expected_type=type_hints["managed_endpoint_configuration"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trust_store_configuration", value=trust_store_configuration, expected_type=type_hints["trust_store_configuration"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if managed_endpoint_configuration is not None:
            self._values["managed_endpoint_configuration"] = managed_endpoint_configuration
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if trust_store_configuration is not None:
            self._values["trust_store_configuration"] = trust_store_configuration
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the responder gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the responder gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponderGatewayPropsMixin.ManagedEndpointConfigurationProperty"]]:
        '''The configuration for the managed endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-managedendpointconfiguration
        '''
        result = self._values.get("managed_endpoint_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponderGatewayPropsMixin.ManagedEndpointConfigurationProperty"]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The networking port to use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The networking protocol to use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the security groups.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the subnets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map of the key-value pairs of the tag or tags to assign to the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def trust_store_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponderGatewayPropsMixin.TrustStoreConfigurationProperty"]]:
        '''The configuration of the trust store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-truststoreconfiguration
        '''
        result = self._values.get("trust_store_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponderGatewayPropsMixin.TrustStoreConfigurationProperty"]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the Virtual Private Cloud (VPC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html#cfn-rtbfabric-respondergateway-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResponderGatewayMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResponderGatewayPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnResponderGatewayPropsMixin",
):
    '''Creates a responder gateway.

    .. epigraph::

       A domain name or managed endpoint is required.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rtbfabric-respondergateway.html
    :cloudformationResource: AWS::RTBFabric::ResponderGateway
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
        
        cfn_responder_gateway_props_mixin = rtbfabric_mixins.CfnResponderGatewayPropsMixin(rtbfabric_mixins.CfnResponderGatewayMixinProps(
            description="description",
            domain_name="domainName",
            managed_endpoint_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.ManagedEndpointConfigurationProperty(
                auto_scaling_groups_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.AutoScalingGroupsConfigurationProperty(
                    auto_scaling_group_name_list=["autoScalingGroupNameList"],
                    role_arn="roleArn"
                ),
                eks_endpoints_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.EksEndpointsConfigurationProperty(
                    cluster_api_server_ca_certificate_chain="clusterApiServerCaCertificateChain",
                    cluster_api_server_endpoint_uri="clusterApiServerEndpointUri",
                    cluster_name="clusterName",
                    endpoints_resource_name="endpointsResourceName",
                    endpoints_resource_namespace="endpointsResourceNamespace",
                    role_arn="roleArn"
                )
            ),
            port=123,
            protocol="protocol",
            security_group_ids=["securityGroupIds"],
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trust_store_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.TrustStoreConfigurationProperty(
                certificate_authority_certificates=["certificateAuthorityCertificates"]
            ),
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResponderGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::RTBFabric::ResponderGateway``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3873046d0c654e8c7573895adbad2993cda09f34b2221645c7f94e266790bbd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afc88f82e0487fd92fffc823ae2c030309f687c3802d1e52044ac54f78d10b67)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0502533b6c2f7624c7fa771a6cf3c93e58799f0fa03e1b5a819a8ca5e946fb6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResponderGatewayMixinProps:
        return typing.cast(CfnResponderGatewayMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnResponderGatewayPropsMixin.AutoScalingGroupsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_scaling_group_name_list": "autoScalingGroupNameList",
            "role_arn": "roleArn",
        },
    )
    class AutoScalingGroupsConfigurationProperty:
        def __init__(
            self,
            *,
            auto_scaling_group_name_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration of an auto scaling group.

            :param auto_scaling_group_name_list: The names of the auto scaling group.
            :param role_arn: The role ARN of the auto scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-autoscalinggroupsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                auto_scaling_groups_configuration_property = rtbfabric_mixins.CfnResponderGatewayPropsMixin.AutoScalingGroupsConfigurationProperty(
                    auto_scaling_group_name_list=["autoScalingGroupNameList"],
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f97564fa0b0b4033ca5c387f3ce63e6cf44a4f47441cbbfc4053db436cc95944)
                check_type(argname="argument auto_scaling_group_name_list", value=auto_scaling_group_name_list, expected_type=type_hints["auto_scaling_group_name_list"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_scaling_group_name_list is not None:
                self._values["auto_scaling_group_name_list"] = auto_scaling_group_name_list
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def auto_scaling_group_name_list(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of the auto scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-autoscalinggroupsconfiguration.html#cfn-rtbfabric-respondergateway-autoscalinggroupsconfiguration-autoscalinggroupnamelist
            '''
            result = self._values.get("auto_scaling_group_name_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The role ARN of the auto scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-autoscalinggroupsconfiguration.html#cfn-rtbfabric-respondergateway-autoscalinggroupsconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingGroupsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnResponderGatewayPropsMixin.EksEndpointsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cluster_api_server_ca_certificate_chain": "clusterApiServerCaCertificateChain",
            "cluster_api_server_endpoint_uri": "clusterApiServerEndpointUri",
            "cluster_name": "clusterName",
            "endpoints_resource_name": "endpointsResourceName",
            "endpoints_resource_namespace": "endpointsResourceNamespace",
            "role_arn": "roleArn",
        },
    )
    class EksEndpointsConfigurationProperty:
        def __init__(
            self,
            *,
            cluster_api_server_ca_certificate_chain: typing.Optional[builtins.str] = None,
            cluster_api_server_endpoint_uri: typing.Optional[builtins.str] = None,
            cluster_name: typing.Optional[builtins.str] = None,
            endpoints_resource_name: typing.Optional[builtins.str] = None,
            endpoints_resource_namespace: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration of an Amazon Elastic Kubernetes Service endpoint.

            :param cluster_api_server_ca_certificate_chain: The CA certificate chain of the cluster API server.
            :param cluster_api_server_endpoint_uri: The URI of the cluster API server endpoint.
            :param cluster_name: The name of the cluster.
            :param endpoints_resource_name: The name of the endpoint resource.
            :param endpoints_resource_namespace: The namespace of the endpoint resource.
            :param role_arn: The role ARN for the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-eksendpointsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                eks_endpoints_configuration_property = rtbfabric_mixins.CfnResponderGatewayPropsMixin.EksEndpointsConfigurationProperty(
                    cluster_api_server_ca_certificate_chain="clusterApiServerCaCertificateChain",
                    cluster_api_server_endpoint_uri="clusterApiServerEndpointUri",
                    cluster_name="clusterName",
                    endpoints_resource_name="endpointsResourceName",
                    endpoints_resource_namespace="endpointsResourceNamespace",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5f995825a11a961013dcbc4c75ebd15850e103bffcee68bf42b390914404d30)
                check_type(argname="argument cluster_api_server_ca_certificate_chain", value=cluster_api_server_ca_certificate_chain, expected_type=type_hints["cluster_api_server_ca_certificate_chain"])
                check_type(argname="argument cluster_api_server_endpoint_uri", value=cluster_api_server_endpoint_uri, expected_type=type_hints["cluster_api_server_endpoint_uri"])
                check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
                check_type(argname="argument endpoints_resource_name", value=endpoints_resource_name, expected_type=type_hints["endpoints_resource_name"])
                check_type(argname="argument endpoints_resource_namespace", value=endpoints_resource_namespace, expected_type=type_hints["endpoints_resource_namespace"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_api_server_ca_certificate_chain is not None:
                self._values["cluster_api_server_ca_certificate_chain"] = cluster_api_server_ca_certificate_chain
            if cluster_api_server_endpoint_uri is not None:
                self._values["cluster_api_server_endpoint_uri"] = cluster_api_server_endpoint_uri
            if cluster_name is not None:
                self._values["cluster_name"] = cluster_name
            if endpoints_resource_name is not None:
                self._values["endpoints_resource_name"] = endpoints_resource_name
            if endpoints_resource_namespace is not None:
                self._values["endpoints_resource_namespace"] = endpoints_resource_namespace
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def cluster_api_server_ca_certificate_chain(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The CA certificate chain of the cluster API server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-eksendpointsconfiguration.html#cfn-rtbfabric-respondergateway-eksendpointsconfiguration-clusterapiservercacertificatechain
            '''
            result = self._values.get("cluster_api_server_ca_certificate_chain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cluster_api_server_endpoint_uri(self) -> typing.Optional[builtins.str]:
            '''The URI of the cluster API server endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-eksendpointsconfiguration.html#cfn-rtbfabric-respondergateway-eksendpointsconfiguration-clusterapiserverendpointuri
            '''
            result = self._values.get("cluster_api_server_endpoint_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cluster_name(self) -> typing.Optional[builtins.str]:
            '''The name of the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-eksendpointsconfiguration.html#cfn-rtbfabric-respondergateway-eksendpointsconfiguration-clustername
            '''
            result = self._values.get("cluster_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoints_resource_name(self) -> typing.Optional[builtins.str]:
            '''The name of the endpoint resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-eksendpointsconfiguration.html#cfn-rtbfabric-respondergateway-eksendpointsconfiguration-endpointsresourcename
            '''
            result = self._values.get("endpoints_resource_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoints_resource_namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the endpoint resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-eksendpointsconfiguration.html#cfn-rtbfabric-respondergateway-eksendpointsconfiguration-endpointsresourcenamespace
            '''
            result = self._values.get("endpoints_resource_namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The role ARN for the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-eksendpointsconfiguration.html#cfn-rtbfabric-respondergateway-eksendpointsconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksEndpointsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnResponderGatewayPropsMixin.ManagedEndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_scaling_groups_configuration": "autoScalingGroupsConfiguration",
            "eks_endpoints_configuration": "eksEndpointsConfiguration",
        },
    )
    class ManagedEndpointConfigurationProperty:
        def __init__(
            self,
            *,
            auto_scaling_groups_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponderGatewayPropsMixin.AutoScalingGroupsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            eks_endpoints_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResponderGatewayPropsMixin.EksEndpointsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the configuration of a managed endpoint.

            :param auto_scaling_groups_configuration: Describes the configuration of an auto scaling group.
            :param eks_endpoints_configuration: Describes the configuration of an Amazon Elastic Kubernetes Service endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-managedendpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                managed_endpoint_configuration_property = rtbfabric_mixins.CfnResponderGatewayPropsMixin.ManagedEndpointConfigurationProperty(
                    auto_scaling_groups_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.AutoScalingGroupsConfigurationProperty(
                        auto_scaling_group_name_list=["autoScalingGroupNameList"],
                        role_arn="roleArn"
                    ),
                    eks_endpoints_configuration=rtbfabric_mixins.CfnResponderGatewayPropsMixin.EksEndpointsConfigurationProperty(
                        cluster_api_server_ca_certificate_chain="clusterApiServerCaCertificateChain",
                        cluster_api_server_endpoint_uri="clusterApiServerEndpointUri",
                        cluster_name="clusterName",
                        endpoints_resource_name="endpointsResourceName",
                        endpoints_resource_namespace="endpointsResourceNamespace",
                        role_arn="roleArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a8b4f89d56027a4feae4300cdae6d8840289d9fa74682dbbe1391807fd45d21)
                check_type(argname="argument auto_scaling_groups_configuration", value=auto_scaling_groups_configuration, expected_type=type_hints["auto_scaling_groups_configuration"])
                check_type(argname="argument eks_endpoints_configuration", value=eks_endpoints_configuration, expected_type=type_hints["eks_endpoints_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_scaling_groups_configuration is not None:
                self._values["auto_scaling_groups_configuration"] = auto_scaling_groups_configuration
            if eks_endpoints_configuration is not None:
                self._values["eks_endpoints_configuration"] = eks_endpoints_configuration

        @builtins.property
        def auto_scaling_groups_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponderGatewayPropsMixin.AutoScalingGroupsConfigurationProperty"]]:
            '''Describes the configuration of an auto scaling group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-managedendpointconfiguration.html#cfn-rtbfabric-respondergateway-managedendpointconfiguration-autoscalinggroupsconfiguration
            '''
            result = self._values.get("auto_scaling_groups_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponderGatewayPropsMixin.AutoScalingGroupsConfigurationProperty"]], result)

        @builtins.property
        def eks_endpoints_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponderGatewayPropsMixin.EksEndpointsConfigurationProperty"]]:
            '''Describes the configuration of an Amazon Elastic Kubernetes Service endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-managedendpointconfiguration.html#cfn-rtbfabric-respondergateway-managedendpointconfiguration-eksendpointsconfiguration
            '''
            result = self._values.get("eks_endpoints_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResponderGatewayPropsMixin.EksEndpointsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedEndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rtbfabric.mixins.CfnResponderGatewayPropsMixin.TrustStoreConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_authority_certificates": "certificateAuthorityCertificates",
        },
    )
    class TrustStoreConfigurationProperty:
        def __init__(
            self,
            *,
            certificate_authority_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes the configuration of a trust store.

            :param certificate_authority_certificates: The certificate authority certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-truststoreconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rtbfabric import mixins as rtbfabric_mixins
                
                trust_store_configuration_property = rtbfabric_mixins.CfnResponderGatewayPropsMixin.TrustStoreConfigurationProperty(
                    certificate_authority_certificates=["certificateAuthorityCertificates"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a57ac11eb6e8a07811f7c34b5d88266ce63f13d2d5a6479a520facd5d4b4420)
                check_type(argname="argument certificate_authority_certificates", value=certificate_authority_certificates, expected_type=type_hints["certificate_authority_certificates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_authority_certificates is not None:
                self._values["certificate_authority_certificates"] = certificate_authority_certificates

        @builtins.property
        def certificate_authority_certificates(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The certificate authority certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rtbfabric-respondergateway-truststoreconfiguration.html#cfn-rtbfabric-respondergateway-truststoreconfiguration-certificateauthoritycertificates
            '''
            result = self._values.get("certificate_authority_certificates")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrustStoreConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnInboundExternalLinkMixinProps",
    "CfnInboundExternalLinkPropsMixin",
    "CfnLinkMixinProps",
    "CfnLinkPropsMixin",
    "CfnOutboundExternalLinkMixinProps",
    "CfnOutboundExternalLinkPropsMixin",
    "CfnRequesterGatewayMixinProps",
    "CfnRequesterGatewayPropsMixin",
    "CfnResponderGatewayMixinProps",
    "CfnResponderGatewayPropsMixin",
]

publication.publish()

def _typecheckingstub__89d4f2379f175559b561055fd3152ec899e59de8b7dc27be5d947d0a8b964da7(
    *,
    gateway_id: typing.Optional[builtins.str] = None,
    link_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInboundExternalLinkPropsMixin.LinkAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    link_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInboundExternalLinkPropsMixin.LinkLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4110e1a9b89f6f8e9c25978f4034209b9dbe5facaa6b25d03302a93eb4837d(
    props: typing.Union[CfnInboundExternalLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fafab914893d54bf5be2ea2ff70f01eb017cd90d4b5bfc5c34735d8a0533baf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacf0f41d6b97ff6f343c2618568986263d17c1b8a8e499e8c9fb220d07ce07a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01bb6fdac6106f7f9fe6f7e75b6c37d040e9d36b649e2adf0fdffd550eee30ba(
    *,
    link_application_log_sampling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20054ca4936e9e6b1b4a884b100e7c910645f4fcb47c8e614f66ebffb1aae1e3(
    *,
    error_log: typing.Optional[jsii.Number] = None,
    filter_log: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8a78fe694a8caf6454484c37eb615eff9194ae1b828d79f814c5d10505d76f(
    *,
    customer_provided_id: typing.Optional[builtins.str] = None,
    responder_error_masking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029035f103da3c97bf83df8090286f2fb08aec0cae2533c9d4badac363f2dcfc(
    *,
    application_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInboundExternalLinkPropsMixin.ApplicationLogsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496baeb78356149c63f8a78321c5f35a2f03774f0fb7178682278b3b743cc6b2(
    *,
    action: typing.Optional[builtins.str] = None,
    http_code: typing.Optional[builtins.str] = None,
    logging_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    response_logging_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3ff89fa52825055f8950344ffe82849dd00c7b9c5e9e701cd5aaa97c5d2ac1(
    *,
    gateway_id: typing.Optional[builtins.str] = None,
    http_responder_allowed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    link_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.LinkAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    link_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.LinkLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    module_configuration_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.ModuleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    peer_gateway_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66049fb8bb42cc1a202cf79cfc1532eb32b83808b4a872a507022ad8e83594c(
    props: typing.Union[CfnLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e313ccd79e3625c537e8717af69254a9bd5d1b9c85e41cb030a459dd80918f2f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0524019da572c792d2a4b05c20b470d31439153978f2075bd018de8b98d69e4e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dbb802837e9b2968062565f05b85a53e72ef2da2e8ba0fb38c714324d237f5(
    *,
    header_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.HeaderTagActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    no_bid: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.NoBidActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09acbbc4b6bac4ca8f2844a4f2443935f82c2e6b547fab123a64749927f9ae92(
    *,
    link_application_log_sampling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.LinkApplicationLogSamplingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b64bdb92b50a8c1b59da54c1b346bcfb59e225f2ea1c5e089bcfdab5e55a540(
    *,
    path: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1964e86a723f4d656095ff45785706ec9aa2b69e50d9a99fdbe99f46df590ab(
    *,
    criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.FilterCriterionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a128e08267fce9fd57012aa30fb12db4fa3797d49b51e715c7c980d540a160(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88be7d0c83549dccec57bbbb24859295c483d9aa0824e9a7d888c51e1b1068c2(
    *,
    error_log: typing.Optional[jsii.Number] = None,
    filter_log: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aadc11f4c7497f05db358b5817b56e044e5e7ecbf1902d610ff28daebc02119(
    *,
    customer_provided_id: typing.Optional[builtins.str] = None,
    responder_error_masking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180e6c87c3669c27aaf8753f9c8db378f932989fad0ad077efa0814604da70bc(
    *,
    application_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.ApplicationLogsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fddaa78343fbbe80298058010d12fb55e223e400110c279920022b8c98503bf(
    *,
    depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    module_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.ModuleParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e7e69a9573ae87da5a47ac6a13d9f268721082f2838cdfde1454d15d2dabfc(
    *,
    no_bid: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.NoBidModuleParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_rtb_attribute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.OpenRtbAttributeModuleParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d473b110f54c549009384b109b2709d9f187cae87d17df426db465a8481aba76(
    *,
    no_bid_reason_code: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3081571623474d6ee6303ad845c1638cbb985a94cf373f6e2f72b7a590b4bde(
    *,
    pass_through_percentage: typing.Optional[jsii.Number] = None,
    reason: typing.Optional[builtins.str] = None,
    reason_code: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49718a4eee4792d4bd50e8cc8326770bf925ef4b8e1d0169fd9dd3f5ddbab1d9(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.FilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    filter_type: typing.Optional[builtins.str] = None,
    holdback_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4695ccddcd911c9a194e85d87f44b0d6f68061080c9d263359f32293cf95c02f(
    *,
    action: typing.Optional[builtins.str] = None,
    http_code: typing.Optional[builtins.str] = None,
    logging_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    response_logging_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ad5275d3c39b39280d0d61e506f9a8e17d1d1a0819aeebd45ea09a0b859863(
    *,
    gateway_id: typing.Optional[builtins.str] = None,
    link_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOutboundExternalLinkPropsMixin.LinkAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    link_log_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOutboundExternalLinkPropsMixin.LinkLogSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    public_endpoint: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb69b27465c9ec182e5c22aba12efa3f9b0355d2df7ba6212c000feaf675012(
    props: typing.Union[CfnOutboundExternalLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8d859731bad5da9f8862b8f8ec8e0890f5dfb55658dee3caee3bbafa47a29d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b29c7cb1272860d1ff60ae744c5b9f7348f7e0affc6119d744270b3ee96e13(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c3a5def8bbb013e5a83459ee0beabfa387dccfed6c70b721b2efb13001549e(
    *,
    link_application_log_sampling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOutboundExternalLinkPropsMixin.LinkApplicationLogSamplingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ac55424e3df1eed8f90aa49120e59a6ccc0e6ad72c0772f2d2c680d3b1ca62(
    *,
    error_log: typing.Optional[jsii.Number] = None,
    filter_log: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa474de1a17d644097fe0bddd48fb2813f0b52108ba962364aabda934e6f334(
    *,
    customer_provided_id: typing.Optional[builtins.str] = None,
    responder_error_masking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOutboundExternalLinkPropsMixin.ResponderErrorMaskingForHttpCodeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb168c58e137274458dfe0fdda93a6fd8e912dfc7300d2f9dd9942b3f11fa71(
    *,
    application_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnOutboundExternalLinkPropsMixin.ApplicationLogsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1e7aa13d2f09dc7f909db5c1a8cc611c5dbf113bd1ee99c7e722be87c3b6df(
    *,
    action: typing.Optional[builtins.str] = None,
    http_code: typing.Optional[builtins.str] = None,
    logging_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    response_logging_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffe299131038ab7ef3a31d25d8c02d39df01b0eef4141a047f5fdabe9de5d73(
    *,
    description: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e32fde45ce339041e4e0abc34ec9a6c961062d3056d424c46fe9a92bcdde110(
    props: typing.Union[CfnRequesterGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dfea8a8317e37520520a1f767cdba2247b7830420928c474e74b9f73d223537(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606b596bd8cfcaa85552dcb609075b76bcbfbe158d52e01efc6ca4b3bf320c2a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6919fd42f9a23f4293e6d2ebad74fe785f75f059526700ea40e2baaa6d37c16(
    *,
    description: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    managed_endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponderGatewayPropsMixin.ManagedEndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trust_store_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponderGatewayPropsMixin.TrustStoreConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3873046d0c654e8c7573895adbad2993cda09f34b2221645c7f94e266790bbd3(
    props: typing.Union[CfnResponderGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc88f82e0487fd92fffc823ae2c030309f687c3802d1e52044ac54f78d10b67(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0502533b6c2f7624c7fa771a6cf3c93e58799f0fa03e1b5a819a8ca5e946fb6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97564fa0b0b4033ca5c387f3ce63e6cf44a4f47441cbbfc4053db436cc95944(
    *,
    auto_scaling_group_name_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f995825a11a961013dcbc4c75ebd15850e103bffcee68bf42b390914404d30(
    *,
    cluster_api_server_ca_certificate_chain: typing.Optional[builtins.str] = None,
    cluster_api_server_endpoint_uri: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    endpoints_resource_name: typing.Optional[builtins.str] = None,
    endpoints_resource_namespace: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8b4f89d56027a4feae4300cdae6d8840289d9fa74682dbbe1391807fd45d21(
    *,
    auto_scaling_groups_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponderGatewayPropsMixin.AutoScalingGroupsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    eks_endpoints_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResponderGatewayPropsMixin.EksEndpointsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a57ac11eb6e8a07811f7c34b5d88266ce63f13d2d5a6479a520facd5d4b4420(
    *,
    certificate_authority_certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
