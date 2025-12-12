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
    jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_config": "applicationConfig",
        "application_source_config": "applicationSourceConfig",
        "description": "description",
        "iframe_config": "iframeConfig",
        "initialization_timeout": "initializationTimeout",
        "is_service": "isService",
        "name": "name",
        "namespace": "namespace",
        "permissions": "permissions",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        application_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        application_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationSourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        iframe_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.IframeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        initialization_timeout: typing.Optional[jsii.Number] = None,
        is_service: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param application_config: 
        :param application_source_config: The configuration for where the application should be loaded from.
        :param description: The description of the application.
        :param iframe_config: 
        :param initialization_timeout: The initialization timeout in milliseconds. Required when IsService is true.
        :param is_service: Indicates whether the application is a service. Default: - false
        :param name: The name of the application.
        :param namespace: The namespace of the application.
        :param permissions: The configuration of events or requests that the application has access to.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
            
            cfn_application_mixin_props = appintegrations_mixins.CfnApplicationMixinProps(
                application_config=appintegrations_mixins.CfnApplicationPropsMixin.ApplicationConfigProperty(
                    contact_handling=appintegrations_mixins.CfnApplicationPropsMixin.ContactHandlingProperty(
                        scope="scope"
                    )
                ),
                application_source_config=appintegrations_mixins.CfnApplicationPropsMixin.ApplicationSourceConfigProperty(
                    external_url_config=appintegrations_mixins.CfnApplicationPropsMixin.ExternalUrlConfigProperty(
                        access_url="accessUrl",
                        approved_origins=["approvedOrigins"]
                    )
                ),
                description="description",
                iframe_config=appintegrations_mixins.CfnApplicationPropsMixin.IframeConfigProperty(
                    allow=["allow"],
                    sandbox=["sandbox"]
                ),
                initialization_timeout=123,
                is_service=False,
                name="name",
                namespace="namespace",
                permissions=["permissions"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2d04ce9b4b559a149e4d68ebd87f02c1ebefb04561797d2dafc03157531e1a8)
            check_type(argname="argument application_config", value=application_config, expected_type=type_hints["application_config"])
            check_type(argname="argument application_source_config", value=application_source_config, expected_type=type_hints["application_source_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument iframe_config", value=iframe_config, expected_type=type_hints["iframe_config"])
            check_type(argname="argument initialization_timeout", value=initialization_timeout, expected_type=type_hints["initialization_timeout"])
            check_type(argname="argument is_service", value=is_service, expected_type=type_hints["is_service"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_config is not None:
            self._values["application_config"] = application_config
        if application_source_config is not None:
            self._values["application_source_config"] = application_source_config
        if description is not None:
            self._values["description"] = description
        if iframe_config is not None:
            self._values["iframe_config"] = iframe_config
        if initialization_timeout is not None:
            self._values["initialization_timeout"] = initialization_timeout
        if is_service is not None:
            self._values["is_service"] = is_service
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if permissions is not None:
            self._values["permissions"] = permissions
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-applicationconfig
        '''
        result = self._values.get("application_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationConfigProperty"]], result)

    @builtins.property
    def application_source_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationSourceConfigProperty"]]:
        '''The configuration for where the application should be loaded from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-applicationsourceconfig
        '''
        result = self._values.get("application_source_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationSourceConfigProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iframe_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.IframeConfigProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-iframeconfig
        '''
        result = self._values.get("iframe_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.IframeConfigProperty"]], result)

    @builtins.property
    def initialization_timeout(self) -> typing.Optional[jsii.Number]:
        '''The initialization timeout in milliseconds.

        Required when IsService is true.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-initializationtimeout
        '''
        result = self._values.get("initialization_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def is_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the application is a service.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-isservice
        '''
        result = self._values.get("is_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The namespace of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The configuration of events or requests that the application has access to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-permissions
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html#cfn-appintegrations-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnApplicationPropsMixin",
):
    '''Creates and persists an Application resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-application.html
    :cloudformationResource: AWS::AppIntegrations::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
        
        cfn_application_props_mixin = appintegrations_mixins.CfnApplicationPropsMixin(appintegrations_mixins.CfnApplicationMixinProps(
            application_config=appintegrations_mixins.CfnApplicationPropsMixin.ApplicationConfigProperty(
                contact_handling=appintegrations_mixins.CfnApplicationPropsMixin.ContactHandlingProperty(
                    scope="scope"
                )
            ),
            application_source_config=appintegrations_mixins.CfnApplicationPropsMixin.ApplicationSourceConfigProperty(
                external_url_config=appintegrations_mixins.CfnApplicationPropsMixin.ExternalUrlConfigProperty(
                    access_url="accessUrl",
                    approved_origins=["approvedOrigins"]
                )
            ),
            description="description",
            iframe_config=appintegrations_mixins.CfnApplicationPropsMixin.IframeConfigProperty(
                allow=["allow"],
                sandbox=["sandbox"]
            ),
            initialization_timeout=123,
            is_service=False,
            name="name",
            namespace="namespace",
            permissions=["permissions"],
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
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppIntegrations::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad7d2e2e6d1a8635bbcebd8035441dbeaf22154e66bcd3d87851a0724ae69ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cea4f1feb36d7963831ad0eb980f57d57336f4d1ac4f448accfaf3faf97089ee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19ed1e29429150218b409e93f26fbbc7b4fcbe09a3b1bc32dc5490f93d69082)
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
        jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnApplicationPropsMixin.ApplicationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_handling": "contactHandling"},
    )
    class ApplicationConfigProperty:
        def __init__(
            self,
            *,
            contact_handling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ContactHandlingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param contact_handling: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-applicationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
                
                application_config_property = appintegrations_mixins.CfnApplicationPropsMixin.ApplicationConfigProperty(
                    contact_handling=appintegrations_mixins.CfnApplicationPropsMixin.ContactHandlingProperty(
                        scope="scope"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae2d3d100db55a28e8364eb0112fdad607e90b3add6f17a337c38eed0521365c)
                check_type(argname="argument contact_handling", value=contact_handling, expected_type=type_hints["contact_handling"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contact_handling is not None:
                self._values["contact_handling"] = contact_handling

        @builtins.property
        def contact_handling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ContactHandlingProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-applicationconfig.html#cfn-appintegrations-application-applicationconfig-contacthandling
            '''
            result = self._values.get("contact_handling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ContactHandlingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnApplicationPropsMixin.ApplicationSourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"external_url_config": "externalUrlConfig"},
    )
    class ApplicationSourceConfigProperty:
        def __init__(
            self,
            *,
            external_url_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ExternalUrlConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for where the application should be loaded from.

            :param external_url_config: The external URL source for the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-applicationsourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
                
                application_source_config_property = appintegrations_mixins.CfnApplicationPropsMixin.ApplicationSourceConfigProperty(
                    external_url_config=appintegrations_mixins.CfnApplicationPropsMixin.ExternalUrlConfigProperty(
                        access_url="accessUrl",
                        approved_origins=["approvedOrigins"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d75054fe16eef6f4351b447287da4b94d3c4710faea94466a95f08b92379669)
                check_type(argname="argument external_url_config", value=external_url_config, expected_type=type_hints["external_url_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if external_url_config is not None:
                self._values["external_url_config"] = external_url_config

        @builtins.property
        def external_url_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ExternalUrlConfigProperty"]]:
            '''The external URL source for the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-applicationsourceconfig.html#cfn-appintegrations-application-applicationsourceconfig-externalurlconfig
            '''
            result = self._values.get("external_url_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ExternalUrlConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationSourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnApplicationPropsMixin.ContactHandlingProperty",
        jsii_struct_bases=[],
        name_mapping={"scope": "scope"},
    )
    class ContactHandlingProperty:
        def __init__(self, *, scope: typing.Optional[builtins.str] = None) -> None:
            '''
            :param scope: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-contacthandling.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
                
                contact_handling_property = appintegrations_mixins.CfnApplicationPropsMixin.ContactHandlingProperty(
                    scope="scope"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96bbbd1a80dcd73e07c1bb192df21a6ea67c51101652c4b4f3a7128c6963f8ca)
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if scope is not None:
                self._values["scope"] = scope

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-contacthandling.html#cfn-appintegrations-application-contacthandling-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContactHandlingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnApplicationPropsMixin.ExternalUrlConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_url": "accessUrl",
            "approved_origins": "approvedOrigins",
        },
    )
    class ExternalUrlConfigProperty:
        def __init__(
            self,
            *,
            access_url: typing.Optional[builtins.str] = None,
            approved_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The external URL source for the application.

            :param access_url: The URL to access the application.
            :param approved_origins: Additional URLs to allow list if different than the access URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-externalurlconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
                
                external_url_config_property = appintegrations_mixins.CfnApplicationPropsMixin.ExternalUrlConfigProperty(
                    access_url="accessUrl",
                    approved_origins=["approvedOrigins"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d0d38c89803e23f832703a300a3158833c5908b55f16d151f5cc24c27ef9302)
                check_type(argname="argument access_url", value=access_url, expected_type=type_hints["access_url"])
                check_type(argname="argument approved_origins", value=approved_origins, expected_type=type_hints["approved_origins"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_url is not None:
                self._values["access_url"] = access_url
            if approved_origins is not None:
                self._values["approved_origins"] = approved_origins

        @builtins.property
        def access_url(self) -> typing.Optional[builtins.str]:
            '''The URL to access the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-externalurlconfig.html#cfn-appintegrations-application-externalurlconfig-accessurl
            '''
            result = self._values.get("access_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def approved_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Additional URLs to allow list if different than the access URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-externalurlconfig.html#cfn-appintegrations-application-externalurlconfig-approvedorigins
            '''
            result = self._values.get("approved_origins")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExternalUrlConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnApplicationPropsMixin.IframeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"allow": "allow", "sandbox": "sandbox"},
    )
    class IframeConfigProperty:
        def __init__(
            self,
            *,
            allow: typing.Optional[typing.Sequence[builtins.str]] = None,
            sandbox: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param allow: 
            :param sandbox: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-iframeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
                
                iframe_config_property = appintegrations_mixins.CfnApplicationPropsMixin.IframeConfigProperty(
                    allow=["allow"],
                    sandbox=["sandbox"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50ec3b5ce74ed84bfe4340d1d8b47cf0bf2cb527eb6cea8dc8af4f3f25f1fa7f)
                check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
                check_type(argname="argument sandbox", value=sandbox, expected_type=type_hints["sandbox"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow is not None:
                self._values["allow"] = allow
            if sandbox is not None:
                self._values["sandbox"] = sandbox

        @builtins.property
        def allow(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-iframeconfig.html#cfn-appintegrations-application-iframeconfig-allow
            '''
            result = self._values.get("allow")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def sandbox(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-application-iframeconfig.html#cfn-appintegrations-application-iframeconfig-sandbox
            '''
            result = self._values.get("sandbox")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IframeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnDataIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "file_configuration": "fileConfiguration",
        "kms_key": "kmsKey",
        "name": "name",
        "object_configuration": "objectConfiguration",
        "schedule_config": "scheduleConfig",
        "source_uri": "sourceUri",
        "tags": "tags",
    },
)
class CfnDataIntegrationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        file_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataIntegrationPropsMixin.FileConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        object_configuration: typing.Any = None,
        schedule_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataIntegrationPropsMixin.ScheduleConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_uri: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataIntegrationPropsMixin.

        :param description: A description of the DataIntegration.
        :param file_configuration: The configuration for what files should be pulled from the source.
        :param kms_key: The KMS key for the DataIntegration.
        :param name: The name of the DataIntegration.
        :param object_configuration: The configuration for what data should be pulled from the source.
        :param schedule_config: The name of the data and how often it should be pulled from the source.
        :param source_uri: The URI of the data source.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
            
            # filters: Any
            # object_configuration: Any
            
            cfn_data_integration_mixin_props = appintegrations_mixins.CfnDataIntegrationMixinProps(
                description="description",
                file_configuration=appintegrations_mixins.CfnDataIntegrationPropsMixin.FileConfigurationProperty(
                    filters=filters,
                    folders=["folders"]
                ),
                kms_key="kmsKey",
                name="name",
                object_configuration=object_configuration,
                schedule_config=appintegrations_mixins.CfnDataIntegrationPropsMixin.ScheduleConfigProperty(
                    first_execution_from="firstExecutionFrom",
                    object="object",
                    schedule_expression="scheduleExpression"
                ),
                source_uri="sourceUri",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187196a660afc3fed3533d1b1d9f3766c66cdcf30c6d5e86c18ed69990ec85d6)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument file_configuration", value=file_configuration, expected_type=type_hints["file_configuration"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument object_configuration", value=object_configuration, expected_type=type_hints["object_configuration"])
            check_type(argname="argument schedule_config", value=schedule_config, expected_type=type_hints["schedule_config"])
            check_type(argname="argument source_uri", value=source_uri, expected_type=type_hints["source_uri"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if file_configuration is not None:
            self._values["file_configuration"] = file_configuration
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if name is not None:
            self._values["name"] = name
        if object_configuration is not None:
            self._values["object_configuration"] = object_configuration
        if schedule_config is not None:
            self._values["schedule_config"] = schedule_config
        if source_uri is not None:
            self._values["source_uri"] = source_uri
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the DataIntegration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataIntegrationPropsMixin.FileConfigurationProperty"]]:
        '''The configuration for what files should be pulled from the source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-fileconfiguration
        '''
        result = self._values.get("file_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataIntegrationPropsMixin.FileConfigurationProperty"]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key for the DataIntegration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-kmskey
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the DataIntegration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_configuration(self) -> typing.Any:
        '''The configuration for what data should be pulled from the source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-objectconfiguration
        '''
        result = self._values.get("object_configuration")
        return typing.cast(typing.Any, result)

    @builtins.property
    def schedule_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataIntegrationPropsMixin.ScheduleConfigProperty"]]:
        '''The name of the data and how often it should be pulled from the source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-scheduleconfig
        '''
        result = self._values.get("schedule_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataIntegrationPropsMixin.ScheduleConfigProperty"]], result)

    @builtins.property
    def source_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-sourceuri
        '''
        result = self._values.get("source_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html#cfn-appintegrations-dataintegration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataIntegrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataIntegrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnDataIntegrationPropsMixin",
):
    '''Creates and persists a DataIntegration resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-dataintegration.html
    :cloudformationResource: AWS::AppIntegrations::DataIntegration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
        
        # filters: Any
        # object_configuration: Any
        
        cfn_data_integration_props_mixin = appintegrations_mixins.CfnDataIntegrationPropsMixin(appintegrations_mixins.CfnDataIntegrationMixinProps(
            description="description",
            file_configuration=appintegrations_mixins.CfnDataIntegrationPropsMixin.FileConfigurationProperty(
                filters=filters,
                folders=["folders"]
            ),
            kms_key="kmsKey",
            name="name",
            object_configuration=object_configuration,
            schedule_config=appintegrations_mixins.CfnDataIntegrationPropsMixin.ScheduleConfigProperty(
                first_execution_from="firstExecutionFrom",
                object="object",
                schedule_expression="scheduleExpression"
            ),
            source_uri="sourceUri",
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
        props: typing.Union[CfnDataIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppIntegrations::DataIntegration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1801ed529bd25c01e0849fa9e60e7dde844e52dc045ceb77fb10ab838fb091)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aef13fa5fe3d58ccbd09363872241287f8a0f92d74aedc5eb088fb5c47b33dc7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0ea500505004a895426a6e015e191aa7220e6583ee1bf7df684de8e46ba798)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataIntegrationMixinProps:
        return typing.cast(CfnDataIntegrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnDataIntegrationPropsMixin.FileConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"filters": "filters", "folders": "folders"},
    )
    class FileConfigurationProperty:
        def __init__(
            self,
            *,
            filters: typing.Any = None,
            folders: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration for what files should be pulled from the source.

            :param filters: Restrictions for what files should be pulled from the source.
            :param folders: Identifiers for the source folders to pull all files from recursively.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-fileconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
                
                # filters: Any
                
                file_configuration_property = appintegrations_mixins.CfnDataIntegrationPropsMixin.FileConfigurationProperty(
                    filters=filters,
                    folders=["folders"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d37fea3045edcb51c15de3075e5cf480a106d33d849c2c00de4e5064169e32c7)
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
                check_type(argname="argument folders", value=folders, expected_type=type_hints["folders"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filters is not None:
                self._values["filters"] = filters
            if folders is not None:
                self._values["folders"] = folders

        @builtins.property
        def filters(self) -> typing.Any:
            '''Restrictions for what files should be pulled from the source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-fileconfiguration.html#cfn-appintegrations-dataintegration-fileconfiguration-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def folders(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Identifiers for the source folders to pull all files from recursively.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-fileconfiguration.html#cfn-appintegrations-dataintegration-fileconfiguration-folders
            '''
            result = self._values.get("folders")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnDataIntegrationPropsMixin.ScheduleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "first_execution_from": "firstExecutionFrom",
            "object": "object",
            "schedule_expression": "scheduleExpression",
        },
    )
    class ScheduleConfigProperty:
        def __init__(
            self,
            *,
            first_execution_from: typing.Optional[builtins.str] = None,
            object: typing.Optional[builtins.str] = None,
            schedule_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the data and how often it should be pulled from the source.

            :param first_execution_from: The start date for objects to import in the first flow run as an Unix/epoch timestamp in milliseconds or in ISO-8601 format.
            :param object: The name of the object to pull from the data source.
            :param schedule_expression: How often the data should be pulled from data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-scheduleconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
                
                schedule_config_property = appintegrations_mixins.CfnDataIntegrationPropsMixin.ScheduleConfigProperty(
                    first_execution_from="firstExecutionFrom",
                    object="object",
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9e9b1993246a4014bc759601d0252edfcf6437cabbb7ee6450f9e8f934818d2)
                check_type(argname="argument first_execution_from", value=first_execution_from, expected_type=type_hints["first_execution_from"])
                check_type(argname="argument object", value=object, expected_type=type_hints["object"])
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if first_execution_from is not None:
                self._values["first_execution_from"] = first_execution_from
            if object is not None:
                self._values["object"] = object
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression

        @builtins.property
        def first_execution_from(self) -> typing.Optional[builtins.str]:
            '''The start date for objects to import in the first flow run as an Unix/epoch timestamp in milliseconds or in ISO-8601 format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-scheduleconfig.html#cfn-appintegrations-dataintegration-scheduleconfig-firstexecutionfrom
            '''
            result = self._values.get("first_execution_from")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object(self) -> typing.Optional[builtins.str]:
            '''The name of the object to pull from the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-scheduleconfig.html#cfn-appintegrations-dataintegration-scheduleconfig-object
            '''
            result = self._values.get("object")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''How often the data should be pulled from data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-dataintegration-scheduleconfig.html#cfn-appintegrations-dataintegration-scheduleconfig-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnEventIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "event_bridge_bus": "eventBridgeBus",
        "event_filter": "eventFilter",
        "name": "name",
        "tags": "tags",
    },
)
class CfnEventIntegrationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_bridge_bus: typing.Optional[builtins.str] = None,
        event_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventIntegrationPropsMixin.EventFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEventIntegrationPropsMixin.

        :param description: The event integration description.
        :param event_bridge_bus: The Amazon EventBridge bus for the event integration.
        :param event_filter: The event integration filter.
        :param name: The name of the event integration.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
            
            cfn_event_integration_mixin_props = appintegrations_mixins.CfnEventIntegrationMixinProps(
                description="description",
                event_bridge_bus="eventBridgeBus",
                event_filter=appintegrations_mixins.CfnEventIntegrationPropsMixin.EventFilterProperty(
                    source="source"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1060b1e6f8bea7a1fe468105402428c3b16ac835e4b86cf4e741b9559bc200)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_bridge_bus", value=event_bridge_bus, expected_type=type_hints["event_bridge_bus"])
            check_type(argname="argument event_filter", value=event_filter, expected_type=type_hints["event_filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_bridge_bus is not None:
            self._values["event_bridge_bus"] = event_bridge_bus
        if event_filter is not None:
            self._values["event_filter"] = event_filter
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The event integration description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_bridge_bus(self) -> typing.Optional[builtins.str]:
        '''The Amazon EventBridge bus for the event integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-eventbridgebus
        '''
        result = self._values.get("event_bridge_bus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_filter(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventIntegrationPropsMixin.EventFilterProperty"]]:
        '''The event integration filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-eventfilter
        '''
        result = self._values.get("event_filter")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventIntegrationPropsMixin.EventFilterProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the event integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html#cfn-appintegrations-eventintegration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventIntegrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventIntegrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnEventIntegrationPropsMixin",
):
    '''Creates an event integration.

    You provide a name, description, and a reference to an Amazon EventBridge bus in your account and a partner event source that will push events to that bus. No objects are created in your account, only metadata that is persisted on the EventIntegration control plane.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appintegrations-eventintegration.html
    :cloudformationResource: AWS::AppIntegrations::EventIntegration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
        
        cfn_event_integration_props_mixin = appintegrations_mixins.CfnEventIntegrationPropsMixin(appintegrations_mixins.CfnEventIntegrationMixinProps(
            description="description",
            event_bridge_bus="eventBridgeBus",
            event_filter=appintegrations_mixins.CfnEventIntegrationPropsMixin.EventFilterProperty(
                source="source"
            ),
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
        props: typing.Union[CfnEventIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AppIntegrations::EventIntegration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7312689dda7b3e9ed6ee0e1787912ea86bd2b8331684b9583afb92c6e3ad40e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5158613c274ca037467e5565b44b0f1e2a0917f68ada73a590bb558a898fdc93)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ca44eadb9fdd3708f9f44b388e451709c8edcbf58bd5a1a3ac4a27900f0d13)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventIntegrationMixinProps:
        return typing.cast(CfnEventIntegrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_appintegrations.mixins.CfnEventIntegrationPropsMixin.EventFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class EventFilterProperty:
        def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
            '''The event integration filter.

            :param source: The source of the events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-eventintegration-eventfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_appintegrations import mixins as appintegrations_mixins
                
                event_filter_property = appintegrations_mixins.CfnEventIntegrationPropsMixin.EventFilterProperty(
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb70d9ba8b5dba2d3323caf936f261a3ac3c8a19234a32a22d375d63ad6121e9)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The source of the events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appintegrations-eventintegration-eventfilter.html#cfn-appintegrations-eventintegration-eventfilter-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnDataIntegrationMixinProps",
    "CfnDataIntegrationPropsMixin",
    "CfnEventIntegrationMixinProps",
    "CfnEventIntegrationPropsMixin",
]

publication.publish()

def _typecheckingstub__b2d04ce9b4b559a149e4d68ebd87f02c1ebefb04561797d2dafc03157531e1a8(
    *,
    application_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    application_source_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationSourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    iframe_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.IframeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initialization_timeout: typing.Optional[jsii.Number] = None,
    is_service: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad7d2e2e6d1a8635bbcebd8035441dbeaf22154e66bcd3d87851a0724ae69ed(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea4f1feb36d7963831ad0eb980f57d57336f4d1ac4f448accfaf3faf97089ee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19ed1e29429150218b409e93f26fbbc7b4fcbe09a3b1bc32dc5490f93d69082(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2d3d100db55a28e8364eb0112fdad607e90b3add6f17a337c38eed0521365c(
    *,
    contact_handling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ContactHandlingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d75054fe16eef6f4351b447287da4b94d3c4710faea94466a95f08b92379669(
    *,
    external_url_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ExternalUrlConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96bbbd1a80dcd73e07c1bb192df21a6ea67c51101652c4b4f3a7128c6963f8ca(
    *,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0d38c89803e23f832703a300a3158833c5908b55f16d151f5cc24c27ef9302(
    *,
    access_url: typing.Optional[builtins.str] = None,
    approved_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ec3b5ce74ed84bfe4340d1d8b47cf0bf2cb527eb6cea8dc8af4f3f25f1fa7f(
    *,
    allow: typing.Optional[typing.Sequence[builtins.str]] = None,
    sandbox: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187196a660afc3fed3533d1b1d9f3766c66cdcf30c6d5e86c18ed69990ec85d6(
    *,
    description: typing.Optional[builtins.str] = None,
    file_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataIntegrationPropsMixin.FileConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    object_configuration: typing.Any = None,
    schedule_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataIntegrationPropsMixin.ScheduleConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_uri: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1801ed529bd25c01e0849fa9e60e7dde844e52dc045ceb77fb10ab838fb091(
    props: typing.Union[CfnDataIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef13fa5fe3d58ccbd09363872241287f8a0f92d74aedc5eb088fb5c47b33dc7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0ea500505004a895426a6e015e191aa7220e6583ee1bf7df684de8e46ba798(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37fea3045edcb51c15de3075e5cf480a106d33d849c2c00de4e5064169e32c7(
    *,
    filters: typing.Any = None,
    folders: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e9b1993246a4014bc759601d0252edfcf6437cabbb7ee6450f9e8f934818d2(
    *,
    first_execution_from: typing.Optional[builtins.str] = None,
    object: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1060b1e6f8bea7a1fe468105402428c3b16ac835e4b86cf4e741b9559bc200(
    *,
    description: typing.Optional[builtins.str] = None,
    event_bridge_bus: typing.Optional[builtins.str] = None,
    event_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventIntegrationPropsMixin.EventFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7312689dda7b3e9ed6ee0e1787912ea86bd2b8331684b9583afb92c6e3ad40e8(
    props: typing.Union[CfnEventIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5158613c274ca037467e5565b44b0f1e2a0917f68ada73a590bb558a898fdc93(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ca44eadb9fdd3708f9f44b388e451709c8edcbf58bd5a1a3ac4a27900f0d13(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb70d9ba8b5dba2d3323caf936f261a3ac3c8a19234a32a22d375d63ad6121e9(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
