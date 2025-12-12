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
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_configs": "appConfigs",
        "data_sources": "dataSources",
        "endpoint": "endpoint",
        "iam_identity_center_options": "iamIdentityCenterOptions",
        "name": "name",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        app_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.AppConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        data_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.DataSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        endpoint: typing.Optional[builtins.str] = None,
        iam_identity_center_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.IamIdentityCenterOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param app_configs: List of application configurations.
        :param data_sources: List of data sources.
        :param endpoint: The endpoint URL of an OpenSearch application.
        :param iam_identity_center_options: Settings container for integrating IAM Identity Center with OpenSearch UI applications, which enables enabling secure user authentication and access control across multiple data sources. This setup supports single sign-on (SSO) through IAM Identity Center, allowing centralized user management.
        :param name: The name of an OpenSearch application.
        :param tags: An arbitrary set of tags (key-value pairs) for this application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
            
            cfn_application_mixin_props = opensearchservice_mixins.CfnApplicationMixinProps(
                app_configs=[opensearchservice_mixins.CfnApplicationPropsMixin.AppConfigProperty(
                    key="key",
                    value="value"
                )],
                data_sources=[opensearchservice_mixins.CfnApplicationPropsMixin.DataSourceProperty(
                    data_source_arn="dataSourceArn",
                    data_source_description="dataSourceDescription"
                )],
                endpoint="endpoint",
                iam_identity_center_options=opensearchservice_mixins.CfnApplicationPropsMixin.IamIdentityCenterOptionsProperty(
                    enabled=False,
                    iam_identity_center_instance_arn="iamIdentityCenterInstanceArn",
                    iam_role_for_identity_center_application_arn="iamRoleForIdentityCenterApplicationArn"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca0c0e19ce192448cb10526c9f2c1d27f90d0211ab255020c5db596d5d31963b)
            check_type(argname="argument app_configs", value=app_configs, expected_type=type_hints["app_configs"])
            check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument iam_identity_center_options", value=iam_identity_center_options, expected_type=type_hints["iam_identity_center_options"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_configs is not None:
            self._values["app_configs"] = app_configs
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if iam_identity_center_options is not None:
            self._values["iam_identity_center_options"] = iam_identity_center_options
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AppConfigProperty"]]]]:
        '''List of application configurations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-application.html#cfn-opensearchservice-application-appconfigs
        '''
        result = self._values.get("app_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.AppConfigProperty"]]]], result)

    @builtins.property
    def data_sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.DataSourceProperty"]]]]:
        '''List of data sources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-application.html#cfn-opensearchservice-application-datasources
        '''
        result = self._values.get("data_sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.DataSourceProperty"]]]], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''The endpoint URL of an OpenSearch application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-application.html#cfn-opensearchservice-application-endpoint
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_identity_center_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.IamIdentityCenterOptionsProperty"]]:
        '''Settings container for integrating IAM Identity Center with OpenSearch UI applications, which enables enabling secure user authentication and access control across multiple data sources.

        This setup supports single sign-on (SSO) through IAM Identity Center, allowing centralized user management.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-application.html#cfn-opensearchservice-application-iamidentitycenteroptions
        '''
        result = self._values.get("iam_identity_center_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.IamIdentityCenterOptionsProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of an OpenSearch application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-application.html#cfn-opensearchservice-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An arbitrary set of tags (key-value pairs) for this application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-application.html#cfn-opensearchservice-application-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnApplicationPropsMixin",
):
    '''Creates an OpenSearch UI application.

    For more information, see `Using the OpenSearch user interface in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/application.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-application.html
    :cloudformationResource: AWS::OpenSearchService::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
        
        cfn_application_props_mixin = opensearchservice_mixins.CfnApplicationPropsMixin(opensearchservice_mixins.CfnApplicationMixinProps(
            app_configs=[opensearchservice_mixins.CfnApplicationPropsMixin.AppConfigProperty(
                key="key",
                value="value"
            )],
            data_sources=[opensearchservice_mixins.CfnApplicationPropsMixin.DataSourceProperty(
                data_source_arn="dataSourceArn",
                data_source_description="dataSourceDescription"
            )],
            endpoint="endpoint",
            iam_identity_center_options=opensearchservice_mixins.CfnApplicationPropsMixin.IamIdentityCenterOptionsProperty(
                enabled=False,
                iam_identity_center_instance_arn="iamIdentityCenterInstanceArn",
                iam_role_for_identity_center_application_arn="iamRoleForIdentityCenterApplicationArn"
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
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpenSearchService::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d6396271250d64fe03967754ba80d242059cd4b549c0d06aad307895245d51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd82ac716e1e30e6d239fcf0941239031546f01454351bede46da23f147227de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6264a2e45476bc1f95f5409599e4c07a8addea684b3a618cdcff4db2cef876f7)
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
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnApplicationPropsMixin.AppConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class AppConfigProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for an OpenSearch application.

            For more information, see see `Using the OpenSearch user interface in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/application.html>`_ .

            :param key: The configuration item to set, such as the admin role for the OpenSearch application.
            :param value: The value assigned to the configuration key, such as an IAM user ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-appconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                app_config_property = opensearchservice_mixins.CfnApplicationPropsMixin.AppConfigProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6fd33ad4e6542a1a283fa5c6ee9facb2aa1fb97be38183111ae00e3a702855a8)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The configuration item to set, such as the admin role for the OpenSearch application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-appconfig.html#cfn-opensearchservice-application-appconfig-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value assigned to the configuration key, such as an IAM user ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-appconfig.html#cfn-opensearchservice-application-appconfig-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnApplicationPropsMixin.DataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_arn": "dataSourceArn",
            "data_source_description": "dataSourceDescription",
        },
    )
    class DataSourceProperty:
        def __init__(
            self,
            *,
            data_source_arn: typing.Optional[builtins.str] = None,
            data_source_description: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Data sources that are associated with an OpenSearch application.

            :param data_source_arn: Amazon Resource Name (ARN) format.
            :param data_source_description: Detailed description of a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-datasource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                data_source_property = opensearchservice_mixins.CfnApplicationPropsMixin.DataSourceProperty(
                    data_source_arn="dataSourceArn",
                    data_source_description="dataSourceDescription"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a22319b561da36a4b807aab7774ab06a65c96568fa0c53f08b5e81ba8ab166c9)
                check_type(argname="argument data_source_arn", value=data_source_arn, expected_type=type_hints["data_source_arn"])
                check_type(argname="argument data_source_description", value=data_source_description, expected_type=type_hints["data_source_description"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source_arn is not None:
                self._values["data_source_arn"] = data_source_arn
            if data_source_description is not None:
                self._values["data_source_description"] = data_source_description

        @builtins.property
        def data_source_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-datasource.html#cfn-opensearchservice-application-datasource-datasourcearn
            '''
            result = self._values.get("data_source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_source_description(self) -> typing.Optional[builtins.str]:
            '''Detailed description of a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-datasource.html#cfn-opensearchservice-application-datasource-datasourcedescription
            '''
            result = self._values.get("data_source_description")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnApplicationPropsMixin.IamIdentityCenterOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "iam_identity_center_instance_arn": "iamIdentityCenterInstanceArn",
            "iam_role_for_identity_center_application_arn": "iamRoleForIdentityCenterApplicationArn",
        },
    )
    class IamIdentityCenterOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            iam_identity_center_instance_arn: typing.Optional[builtins.str] = None,
            iam_role_for_identity_center_application_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for IAM Identity Center in an OpenSearch application.

            :param enabled: Indicates whether IAM Identity Center is enabled for the OpenSearch application.
            :param iam_identity_center_instance_arn: Amazon Resource Name (ARN) format.
            :param iam_role_for_identity_center_application_arn: The Amazon Resource Name (ARN) of the IAM role assigned to the IAM Identity Center application for the OpenSearch application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-iamidentitycenteroptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                iam_identity_center_options_property = opensearchservice_mixins.CfnApplicationPropsMixin.IamIdentityCenterOptionsProperty(
                    enabled=False,
                    iam_identity_center_instance_arn="iamIdentityCenterInstanceArn",
                    iam_role_for_identity_center_application_arn="iamRoleForIdentityCenterApplicationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7be4891ef864731ea9b5f4a33576d6b515b6501c6d0116eb8c815efbf230cb8a)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument iam_identity_center_instance_arn", value=iam_identity_center_instance_arn, expected_type=type_hints["iam_identity_center_instance_arn"])
                check_type(argname="argument iam_role_for_identity_center_application_arn", value=iam_role_for_identity_center_application_arn, expected_type=type_hints["iam_role_for_identity_center_application_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if iam_identity_center_instance_arn is not None:
                self._values["iam_identity_center_instance_arn"] = iam_identity_center_instance_arn
            if iam_role_for_identity_center_application_arn is not None:
                self._values["iam_role_for_identity_center_application_arn"] = iam_role_for_identity_center_application_arn

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether IAM Identity Center is enabled for the OpenSearch application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-iamidentitycenteroptions.html#cfn-opensearchservice-application-iamidentitycenteroptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def iam_identity_center_instance_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-iamidentitycenteroptions.html#cfn-opensearchservice-application-iamidentitycenteroptions-iamidentitycenterinstancearn
            '''
            result = self._values.get("iam_identity_center_instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam_role_for_identity_center_application_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role assigned to the IAM Identity Center application for the OpenSearch application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-application-iamidentitycenteroptions.html#cfn-opensearchservice-application-iamidentitycenteroptions-iamroleforidentitycenterapplicationarn
            '''
            result = self._values.get("iam_role_for_identity_center_application_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamIdentityCenterOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "advanced_options": "advancedOptions",
        "advanced_security_options": "advancedSecurityOptions",
        "aiml_options": "aimlOptions",
        "cluster_config": "clusterConfig",
        "cognito_options": "cognitoOptions",
        "domain_arn": "domainArn",
        "domain_endpoint_options": "domainEndpointOptions",
        "domain_name": "domainName",
        "ebs_options": "ebsOptions",
        "encryption_at_rest_options": "encryptionAtRestOptions",
        "engine_version": "engineVersion",
        "identity_center_options": "identityCenterOptions",
        "ip_address_type": "ipAddressType",
        "log_publishing_options": "logPublishingOptions",
        "node_to_node_encryption_options": "nodeToNodeEncryptionOptions",
        "off_peak_window_options": "offPeakWindowOptions",
        "skip_shard_migration_wait": "skipShardMigrationWait",
        "snapshot_options": "snapshotOptions",
        "software_update_options": "softwareUpdateOptions",
        "tags": "tags",
        "vpc_options": "vpcOptions",
    },
)
class CfnDomainMixinProps:
    def __init__(
        self,
        *,
        access_policies: typing.Any = None,
        advanced_options: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        advanced_security_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.AdvancedSecurityOptionsInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        aiml_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.AIMLOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cluster_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.ClusterConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cognito_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.CognitoOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        domain_arn: typing.Optional[builtins.str] = None,
        domain_endpoint_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.DomainEndpointOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.EBSOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption_at_rest_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.EncryptionAtRestOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        identity_center_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.IdentityCenterOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        log_publishing_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.LogPublishingOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        node_to_node_encryption_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.NodeToNodeEncryptionOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        off_peak_window_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.OffPeakWindowOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        skip_shard_migration_wait: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        snapshot_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.SnapshotOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        software_update_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.SoftwareUpdateOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.VPCOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainPropsMixin.

        :param access_policies: An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions. For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param advanced_options: Additional options to specify for the OpenSearch Service domain. For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.
        :param advanced_security_options: Specifies options for fine-grained access control and SAML authentication. If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.
        :param aiml_options: Container for parameters required to enable all machine learning features.
        :param cluster_config: Container for the cluster configuration of a domain.
        :param cognito_options: Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.
        :param domain_arn: 
        :param domain_endpoint_options: Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.
        :param domain_name: A name for the OpenSearch Service domain. The name must have a minimum length of 3 and a maximum length of 28. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . Required when creating a new domain. .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param ebs_options: The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .
        :param encryption_at_rest_options: Whether the domain should encrypt data at rest, and if so, the AWS key to use. See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ . If no encryption at rest options were initially specified in the template, updating this property by adding it causes no interruption. However, if you change this property after it's already been set within a template, the domain is deleted and recreated in order to modify the property.
        :param engine_version: The version of OpenSearch to use. The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* . If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param identity_center_options: Configuration options for controlling IAM Identity Center integration within a domain.
        :param ip_address_type: Choose either dual stack or IPv4 as your IP address type. Dual stack allows you to share domain resources across IPv4 and IPv6 address types, and is the recommended option. If you set your IP address type to dual stack, you can't change your address type later.
        :param log_publishing_options: An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish. Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .
        :param node_to_node_encryption_options: Specifies whether node-to-node encryption is enabled. See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .
        :param off_peak_window_options: Options for a domain's off-peak window, during which OpenSearch Service can perform mandatory configuration changes on the domain.
        :param skip_shard_migration_wait: 
        :param snapshot_options: *DEPRECATED* . The automated snapshot configuration for the OpenSearch Service domain indexes.
        :param software_update_options: Service software update options for the domain.
        :param tags: An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.
        :param vpc_options: The virtual private cloud (VPC) configuration for the OpenSearch Service domain. For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* . If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
            
            # access_policies: Any
            
            cfn_domain_mixin_props = opensearchservice_mixins.CfnDomainMixinProps(
                access_policies=access_policies,
                advanced_options={
                    "advanced_options_key": "advancedOptions"
                },
                advanced_security_options=opensearchservice_mixins.CfnDomainPropsMixin.AdvancedSecurityOptionsInputProperty(
                    anonymous_auth_disable_date="anonymousAuthDisableDate",
                    anonymous_auth_enabled=False,
                    enabled=False,
                    iam_federation_options={
                        "enabled": False,
                        "roles_key": "rolesKey",
                        "subject_key": "subjectKey"
                    },
                    internal_user_database_enabled=False,
                    jwt_options=opensearchservice_mixins.CfnDomainPropsMixin.JWTOptionsProperty(
                        enabled=False,
                        public_key="publicKey",
                        roles_key="rolesKey",
                        subject_key="subjectKey"
                    ),
                    master_user_options=opensearchservice_mixins.CfnDomainPropsMixin.MasterUserOptionsProperty(
                        master_user_arn="masterUserArn",
                        master_user_name="masterUserName",
                        master_user_password="masterUserPassword"
                    ),
                    saml_options=opensearchservice_mixins.CfnDomainPropsMixin.SAMLOptionsProperty(
                        enabled=False,
                        idp=opensearchservice_mixins.CfnDomainPropsMixin.IdpProperty(
                            entity_id="entityId",
                            metadata_content="metadataContent"
                        ),
                        master_backend_role="masterBackendRole",
                        master_user_name="masterUserName",
                        roles_key="rolesKey",
                        session_timeout_minutes=123,
                        subject_key="subjectKey"
                    )
                ),
                aiml_options=opensearchservice_mixins.CfnDomainPropsMixin.AIMLOptionsProperty(
                    s3_vectors_engine=opensearchservice_mixins.CfnDomainPropsMixin.S3VectorsEngineProperty(
                        enabled=False
                    )
                ),
                cluster_config=opensearchservice_mixins.CfnDomainPropsMixin.ClusterConfigProperty(
                    cold_storage_options=opensearchservice_mixins.CfnDomainPropsMixin.ColdStorageOptionsProperty(
                        enabled=False
                    ),
                    dedicated_master_count=123,
                    dedicated_master_enabled=False,
                    dedicated_master_type="dedicatedMasterType",
                    instance_count=123,
                    instance_type="instanceType",
                    multi_az_with_standby_enabled=False,
                    node_options=[opensearchservice_mixins.CfnDomainPropsMixin.NodeOptionProperty(
                        node_config=opensearchservice_mixins.CfnDomainPropsMixin.NodeConfigProperty(
                            count=123,
                            enabled=False,
                            type="type"
                        ),
                        node_type="nodeType"
                    )],
                    warm_count=123,
                    warm_enabled=False,
                    warm_type="warmType",
                    zone_awareness_config=opensearchservice_mixins.CfnDomainPropsMixin.ZoneAwarenessConfigProperty(
                        availability_zone_count=123
                    ),
                    zone_awareness_enabled=False
                ),
                cognito_options=opensearchservice_mixins.CfnDomainPropsMixin.CognitoOptionsProperty(
                    enabled=False,
                    identity_pool_id="identityPoolId",
                    role_arn="roleArn",
                    user_pool_id="userPoolId"
                ),
                domain_arn="domainArn",
                domain_endpoint_options=opensearchservice_mixins.CfnDomainPropsMixin.DomainEndpointOptionsProperty(
                    custom_endpoint="customEndpoint",
                    custom_endpoint_certificate_arn="customEndpointCertificateArn",
                    custom_endpoint_enabled=False,
                    enforce_https=False,
                    tls_security_policy="tlsSecurityPolicy"
                ),
                domain_name="domainName",
                ebs_options=opensearchservice_mixins.CfnDomainPropsMixin.EBSOptionsProperty(
                    ebs_enabled=False,
                    iops=123,
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                ),
                encryption_at_rest_options=opensearchservice_mixins.CfnDomainPropsMixin.EncryptionAtRestOptionsProperty(
                    enabled=False,
                    kms_key_id="kmsKeyId"
                ),
                engine_version="engineVersion",
                identity_center_options=opensearchservice_mixins.CfnDomainPropsMixin.IdentityCenterOptionsProperty(
                    enabled_api_access=False,
                    identity_center_application_arn="identityCenterApplicationArn",
                    identity_center_instance_arn="identityCenterInstanceArn",
                    identity_store_id="identityStoreId",
                    roles_key="rolesKey",
                    subject_key="subjectKey"
                ),
                ip_address_type="ipAddressType",
                log_publishing_options={
                    "log_publishing_options_key": opensearchservice_mixins.CfnDomainPropsMixin.LogPublishingOptionProperty(
                        cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                        enabled=False
                    )
                },
                node_to_node_encryption_options=opensearchservice_mixins.CfnDomainPropsMixin.NodeToNodeEncryptionOptionsProperty(
                    enabled=False
                ),
                off_peak_window_options=opensearchservice_mixins.CfnDomainPropsMixin.OffPeakWindowOptionsProperty(
                    enabled=False,
                    off_peak_window=opensearchservice_mixins.CfnDomainPropsMixin.OffPeakWindowProperty(
                        window_start_time=opensearchservice_mixins.CfnDomainPropsMixin.WindowStartTimeProperty(
                            hours=123,
                            minutes=123
                        )
                    )
                ),
                skip_shard_migration_wait=False,
                snapshot_options=opensearchservice_mixins.CfnDomainPropsMixin.SnapshotOptionsProperty(
                    automated_snapshot_start_hour=123
                ),
                software_update_options=opensearchservice_mixins.CfnDomainPropsMixin.SoftwareUpdateOptionsProperty(
                    auto_software_update_enabled=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_options=opensearchservice_mixins.CfnDomainPropsMixin.VPCOptionsProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7094369dea89efb248c37dfd6b717935a084c92d05fb2407b5d4e6cfc6c17825)
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument advanced_options", value=advanced_options, expected_type=type_hints["advanced_options"])
            check_type(argname="argument advanced_security_options", value=advanced_security_options, expected_type=type_hints["advanced_security_options"])
            check_type(argname="argument aiml_options", value=aiml_options, expected_type=type_hints["aiml_options"])
            check_type(argname="argument cluster_config", value=cluster_config, expected_type=type_hints["cluster_config"])
            check_type(argname="argument cognito_options", value=cognito_options, expected_type=type_hints["cognito_options"])
            check_type(argname="argument domain_arn", value=domain_arn, expected_type=type_hints["domain_arn"])
            check_type(argname="argument domain_endpoint_options", value=domain_endpoint_options, expected_type=type_hints["domain_endpoint_options"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument ebs_options", value=ebs_options, expected_type=type_hints["ebs_options"])
            check_type(argname="argument encryption_at_rest_options", value=encryption_at_rest_options, expected_type=type_hints["encryption_at_rest_options"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument identity_center_options", value=identity_center_options, expected_type=type_hints["identity_center_options"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument log_publishing_options", value=log_publishing_options, expected_type=type_hints["log_publishing_options"])
            check_type(argname="argument node_to_node_encryption_options", value=node_to_node_encryption_options, expected_type=type_hints["node_to_node_encryption_options"])
            check_type(argname="argument off_peak_window_options", value=off_peak_window_options, expected_type=type_hints["off_peak_window_options"])
            check_type(argname="argument skip_shard_migration_wait", value=skip_shard_migration_wait, expected_type=type_hints["skip_shard_migration_wait"])
            check_type(argname="argument snapshot_options", value=snapshot_options, expected_type=type_hints["snapshot_options"])
            check_type(argname="argument software_update_options", value=software_update_options, expected_type=type_hints["software_update_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_options", value=vpc_options, expected_type=type_hints["vpc_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if advanced_options is not None:
            self._values["advanced_options"] = advanced_options
        if advanced_security_options is not None:
            self._values["advanced_security_options"] = advanced_security_options
        if aiml_options is not None:
            self._values["aiml_options"] = aiml_options
        if cluster_config is not None:
            self._values["cluster_config"] = cluster_config
        if cognito_options is not None:
            self._values["cognito_options"] = cognito_options
        if domain_arn is not None:
            self._values["domain_arn"] = domain_arn
        if domain_endpoint_options is not None:
            self._values["domain_endpoint_options"] = domain_endpoint_options
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if ebs_options is not None:
            self._values["ebs_options"] = ebs_options
        if encryption_at_rest_options is not None:
            self._values["encryption_at_rest_options"] = encryption_at_rest_options
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if identity_center_options is not None:
            self._values["identity_center_options"] = identity_center_options
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if log_publishing_options is not None:
            self._values["log_publishing_options"] = log_publishing_options
        if node_to_node_encryption_options is not None:
            self._values["node_to_node_encryption_options"] = node_to_node_encryption_options
        if off_peak_window_options is not None:
            self._values["off_peak_window_options"] = off_peak_window_options
        if skip_shard_migration_wait is not None:
            self._values["skip_shard_migration_wait"] = skip_shard_migration_wait
        if snapshot_options is not None:
            self._values["snapshot_options"] = snapshot_options
        if software_update_options is not None:
            self._values["software_update_options"] = software_update_options
        if tags is not None:
            self._values["tags"] = tags
        if vpc_options is not None:
            self._values["vpc_options"] = vpc_options

    @builtins.property
    def access_policies(self) -> typing.Any:
        '''An AWS Identity and Access Management ( IAM ) policy document that specifies who can access the OpenSearch Service domain and their permissions.

        For more information, see `Configuring access policies <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ac.html#ac-creating>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-accesspolicies
        '''
        result = self._values.get("access_policies")
        return typing.cast(typing.Any, result)

    @builtins.property
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''Additional options to specify for the OpenSearch Service domain.

        For more information, see `AdvancedOptions <https://docs.aws.amazon.com/opensearch-service/latest/APIReference/API_CreateDomain.html#API_CreateDomain_RequestBody>`_ in the OpenSearch Service API reference.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedoptions
        '''
        result = self._values.get("advanced_options")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def advanced_security_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.AdvancedSecurityOptionsInputProperty"]]:
        '''Specifies options for fine-grained access control and SAML authentication.

        If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-advancedsecurityoptions
        '''
        result = self._values.get("advanced_security_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.AdvancedSecurityOptionsInputProperty"]], result)

    @builtins.property
    def aiml_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.AIMLOptionsProperty"]]:
        '''Container for parameters required to enable all machine learning features.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-aimloptions
        '''
        result = self._values.get("aiml_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.AIMLOptionsProperty"]], result)

    @builtins.property
    def cluster_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ClusterConfigProperty"]]:
        '''Container for the cluster configuration of a domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-clusterconfig
        '''
        result = self._values.get("cluster_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ClusterConfigProperty"]], result)

    @builtins.property
    def cognito_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.CognitoOptionsProperty"]]:
        '''Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-cognitooptions
        '''
        result = self._values.get("cognito_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.CognitoOptionsProperty"]], result)

    @builtins.property
    def domain_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainarn
        '''
        result = self._values.get("domain_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_endpoint_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.DomainEndpointOptionsProperty"]]:
        '''Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainendpointoptions
        '''
        result = self._values.get("domain_endpoint_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.DomainEndpointOptionsProperty"]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''A name for the OpenSearch Service domain.

        The name must have a minimum length of 3 and a maximum length of 28. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the domain name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        Required when creating a new domain.
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.EBSOptionsProperty"]]:
        '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.

        For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-ebsoptions
        '''
        result = self._values.get("ebs_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.EBSOptionsProperty"]], result)

    @builtins.property
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.EncryptionAtRestOptionsProperty"]]:
        '''Whether the domain should encrypt data at rest, and if so, the AWS  key to use.

        See `Encryption of data at rest for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/encryption-at-rest.html>`_ .

        If no encryption at rest options were initially specified in the template, updating this property by adding it causes no interruption. However, if you change this property after it's already been set within a template, the domain is deleted and recreated in order to modify the property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-encryptionatrestoptions
        '''
        result = self._values.get("encryption_at_rest_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.EncryptionAtRestOptionsProperty"]], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version of OpenSearch to use.

        The value must be in the format ``OpenSearch_X.Y`` or ``Elasticsearch_X.Y`` . If not specified, the latest version of OpenSearch is used. For information about the versions that OpenSearch Service supports, see `Supported versions of OpenSearch and Elasticsearch <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html#choosing-version>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you set the `EnableVersionUpgrade <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeopensearchdomain>`_ update policy to ``true`` , you can update ``EngineVersion`` without interruption. When ``EnableVersionUpgrade`` is set to ``false`` , or is not specified, updating ``EngineVersion`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_center_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.IdentityCenterOptionsProperty"]]:
        '''Configuration options for controlling IAM Identity Center integration within a domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-identitycenteroptions
        '''
        result = self._values.get("identity_center_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.IdentityCenterOptionsProperty"]], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Choose either dual stack or IPv4 as your IP address type.

        Dual stack allows you to share domain resources across IPv4 and IPv6 address types, and is the recommended option. If you set your IP address type to dual stack, you can't change your address type later.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.LogPublishingOptionProperty"]]]]:
        '''An object with one or more of the following keys: ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , ``AUDIT_LOGS`` , depending on the types of logs you want to publish.

        Each key needs a valid ``LogPublishingOption`` value. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-logpublishingoptions
        '''
        result = self._values.get("log_publishing_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.LogPublishingOptionProperty"]]]], result)

    @builtins.property
    def node_to_node_encryption_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.NodeToNodeEncryptionOptionsProperty"]]:
        '''Specifies whether node-to-node encryption is enabled.

        See `Node-to-node encryption for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ntn.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-nodetonodeencryptionoptions
        '''
        result = self._values.get("node_to_node_encryption_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.NodeToNodeEncryptionOptionsProperty"]], result)

    @builtins.property
    def off_peak_window_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.OffPeakWindowOptionsProperty"]]:
        '''Options for a domain's off-peak window, during which OpenSearch Service can perform mandatory configuration changes on the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-offpeakwindowoptions
        '''
        result = self._values.get("off_peak_window_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.OffPeakWindowOptionsProperty"]], result)

    @builtins.property
    def skip_shard_migration_wait(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-skipshardmigrationwait
        '''
        result = self._values.get("skip_shard_migration_wait")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def snapshot_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SnapshotOptionsProperty"]]:
        '''*DEPRECATED* .

        The automated snapshot configuration for the OpenSearch Service domain indexes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-snapshotoptions
        '''
        result = self._values.get("snapshot_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SnapshotOptionsProperty"]], result)

    @builtins.property
    def software_update_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SoftwareUpdateOptionsProperty"]]:
        '''Service software update options for the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-softwareupdateoptions
        '''
        result = self._values.get("software_update_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SoftwareUpdateOptionsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An arbitrary set of tags (key–value pairs) to associate with the OpenSearch Service domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.VPCOptionsProperty"]]:
        '''The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

        For more information, see `Launching your Amazon OpenSearch Service domains within a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

        If you remove this entity altogether, along with its associated properties, it causes a replacement. You might encounter this scenario if you're updating your security configuration from a VPC to a public endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#cfn-opensearchservice-domain-vpcoptions
        '''
        result = self._values.get("vpc_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.VPCOptionsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin",
):
    '''The AWS::OpenSearchService::Domain resource creates an Amazon OpenSearch Service domain.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html
    :cloudformationResource: AWS::OpenSearchService::Domain
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
        
        # access_policies: Any
        
        cfn_domain_props_mixin = opensearchservice_mixins.CfnDomainPropsMixin(opensearchservice_mixins.CfnDomainMixinProps(
            access_policies=access_policies,
            advanced_options={
                "advanced_options_key": "advancedOptions"
            },
            advanced_security_options=opensearchservice_mixins.CfnDomainPropsMixin.AdvancedSecurityOptionsInputProperty(
                anonymous_auth_disable_date="anonymousAuthDisableDate",
                anonymous_auth_enabled=False,
                enabled=False,
                iam_federation_options={
                    "enabled": False,
                    "roles_key": "rolesKey",
                    "subject_key": "subjectKey"
                },
                internal_user_database_enabled=False,
                jwt_options=opensearchservice_mixins.CfnDomainPropsMixin.JWTOptionsProperty(
                    enabled=False,
                    public_key="publicKey",
                    roles_key="rolesKey",
                    subject_key="subjectKey"
                ),
                master_user_options=opensearchservice_mixins.CfnDomainPropsMixin.MasterUserOptionsProperty(
                    master_user_arn="masterUserArn",
                    master_user_name="masterUserName",
                    master_user_password="masterUserPassword"
                ),
                saml_options=opensearchservice_mixins.CfnDomainPropsMixin.SAMLOptionsProperty(
                    enabled=False,
                    idp=opensearchservice_mixins.CfnDomainPropsMixin.IdpProperty(
                        entity_id="entityId",
                        metadata_content="metadataContent"
                    ),
                    master_backend_role="masterBackendRole",
                    master_user_name="masterUserName",
                    roles_key="rolesKey",
                    session_timeout_minutes=123,
                    subject_key="subjectKey"
                )
            ),
            aiml_options=opensearchservice_mixins.CfnDomainPropsMixin.AIMLOptionsProperty(
                s3_vectors_engine=opensearchservice_mixins.CfnDomainPropsMixin.S3VectorsEngineProperty(
                    enabled=False
                )
            ),
            cluster_config=opensearchservice_mixins.CfnDomainPropsMixin.ClusterConfigProperty(
                cold_storage_options=opensearchservice_mixins.CfnDomainPropsMixin.ColdStorageOptionsProperty(
                    enabled=False
                ),
                dedicated_master_count=123,
                dedicated_master_enabled=False,
                dedicated_master_type="dedicatedMasterType",
                instance_count=123,
                instance_type="instanceType",
                multi_az_with_standby_enabled=False,
                node_options=[opensearchservice_mixins.CfnDomainPropsMixin.NodeOptionProperty(
                    node_config=opensearchservice_mixins.CfnDomainPropsMixin.NodeConfigProperty(
                        count=123,
                        enabled=False,
                        type="type"
                    ),
                    node_type="nodeType"
                )],
                warm_count=123,
                warm_enabled=False,
                warm_type="warmType",
                zone_awareness_config=opensearchservice_mixins.CfnDomainPropsMixin.ZoneAwarenessConfigProperty(
                    availability_zone_count=123
                ),
                zone_awareness_enabled=False
            ),
            cognito_options=opensearchservice_mixins.CfnDomainPropsMixin.CognitoOptionsProperty(
                enabled=False,
                identity_pool_id="identityPoolId",
                role_arn="roleArn",
                user_pool_id="userPoolId"
            ),
            domain_arn="domainArn",
            domain_endpoint_options=opensearchservice_mixins.CfnDomainPropsMixin.DomainEndpointOptionsProperty(
                custom_endpoint="customEndpoint",
                custom_endpoint_certificate_arn="customEndpointCertificateArn",
                custom_endpoint_enabled=False,
                enforce_https=False,
                tls_security_policy="tlsSecurityPolicy"
            ),
            domain_name="domainName",
            ebs_options=opensearchservice_mixins.CfnDomainPropsMixin.EBSOptionsProperty(
                ebs_enabled=False,
                iops=123,
                throughput=123,
                volume_size=123,
                volume_type="volumeType"
            ),
            encryption_at_rest_options=opensearchservice_mixins.CfnDomainPropsMixin.EncryptionAtRestOptionsProperty(
                enabled=False,
                kms_key_id="kmsKeyId"
            ),
            engine_version="engineVersion",
            identity_center_options=opensearchservice_mixins.CfnDomainPropsMixin.IdentityCenterOptionsProperty(
                enabled_api_access=False,
                identity_center_application_arn="identityCenterApplicationArn",
                identity_center_instance_arn="identityCenterInstanceArn",
                identity_store_id="identityStoreId",
                roles_key="rolesKey",
                subject_key="subjectKey"
            ),
            ip_address_type="ipAddressType",
            log_publishing_options={
                "log_publishing_options_key": opensearchservice_mixins.CfnDomainPropsMixin.LogPublishingOptionProperty(
                    cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                    enabled=False
                )
            },
            node_to_node_encryption_options=opensearchservice_mixins.CfnDomainPropsMixin.NodeToNodeEncryptionOptionsProperty(
                enabled=False
            ),
            off_peak_window_options=opensearchservice_mixins.CfnDomainPropsMixin.OffPeakWindowOptionsProperty(
                enabled=False,
                off_peak_window=opensearchservice_mixins.CfnDomainPropsMixin.OffPeakWindowProperty(
                    window_start_time=opensearchservice_mixins.CfnDomainPropsMixin.WindowStartTimeProperty(
                        hours=123,
                        minutes=123
                    )
                )
            ),
            skip_shard_migration_wait=False,
            snapshot_options=opensearchservice_mixins.CfnDomainPropsMixin.SnapshotOptionsProperty(
                automated_snapshot_start_hour=123
            ),
            software_update_options=opensearchservice_mixins.CfnDomainPropsMixin.SoftwareUpdateOptionsProperty(
                auto_software_update_enabled=False
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_options=opensearchservice_mixins.CfnDomainPropsMixin.VPCOptionsProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpenSearchService::Domain``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a795dc8e5dcfc936f281e31747952417209159c39f9fb6f086dcabc2f9bba81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8b3e5e038a8da8aa2745470b06219c91be5d4d6dc15361d294a7c9a462965b2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d3332981a3f85ca9f12c7823542b76da02831ada2fd0cfda7dd2c5012e1b93)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainMixinProps:
        return typing.cast(CfnDomainMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.AIMLOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_vectors_engine": "s3VectorsEngine"},
    )
    class AIMLOptionsProperty:
        def __init__(
            self,
            *,
            s3_vectors_engine: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.S3VectorsEngineProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param s3_vectors_engine: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-aimloptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                a_iMLOptions_property = opensearchservice_mixins.CfnDomainPropsMixin.AIMLOptionsProperty(
                    s3_vectors_engine=opensearchservice_mixins.CfnDomainPropsMixin.S3VectorsEngineProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b17a3584d7d0f7cf2d325cfd842a9a604146cc02c696283dee1dfdc1c18464ce)
                check_type(argname="argument s3_vectors_engine", value=s3_vectors_engine, expected_type=type_hints["s3_vectors_engine"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_vectors_engine is not None:
                self._values["s3_vectors_engine"] = s3_vectors_engine

        @builtins.property
        def s3_vectors_engine(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.S3VectorsEngineProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-aimloptions.html#cfn-opensearchservice-domain-aimloptions-s3vectorsengine
            '''
            result = self._values.get("s3_vectors_engine")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.S3VectorsEngineProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AIMLOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.AdvancedSecurityOptionsInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "anonymous_auth_disable_date": "anonymousAuthDisableDate",
            "anonymous_auth_enabled": "anonymousAuthEnabled",
            "enabled": "enabled",
            "iam_federation_options": "iamFederationOptions",
            "internal_user_database_enabled": "internalUserDatabaseEnabled",
            "jwt_options": "jwtOptions",
            "master_user_options": "masterUserOptions",
            "saml_options": "samlOptions",
        },
    )
    class AdvancedSecurityOptionsInputProperty:
        def __init__(
            self,
            *,
            anonymous_auth_disable_date: typing.Optional[builtins.str] = None,
            anonymous_auth_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            iam_federation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.IAMFederationOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            jwt_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.JWTOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            master_user_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.MasterUserOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            saml_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.SAMLOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies options for fine-grained access control.

            If you specify advanced security options, you must also enable node-to-node encryption ( `NodeToNodeEncryptionOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html>`_ ) and encryption at rest ( `EncryptionAtRestOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html>`_ ). You must also enable ``EnforceHTTPS`` within `DomainEndpointOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html>`_ , which requires HTTPS for all traffic to the domain.

            :param anonymous_auth_disable_date: Date and time when the migration period will be disabled. Only necessary when `enabling fine-grained access control on an existing domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-enabling-existing>`_ .
            :param anonymous_auth_enabled: True to enable a 30-day migration period during which administrators can create role mappings. Only necessary when `enabling fine-grained access control on an existing domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-enabling-existing>`_ .
            :param enabled: True to enable fine-grained access control. You must also enable encryption of data at rest and node-to-node encryption. See `Fine-grained access control in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html>`_ .
            :param iam_federation_options: Input configuration for IAM identity federation within advanced security options.
            :param internal_user_database_enabled: True to enable the internal user database.
            :param jwt_options: Container for information about the JWT configuration of the Amazon OpenSearch Service.
            :param master_user_options: Specifies information about the master user.
            :param saml_options: Container for information about the SAML configuration for OpenSearch Dashboards.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                advanced_security_options_input_property = opensearchservice_mixins.CfnDomainPropsMixin.AdvancedSecurityOptionsInputProperty(
                    anonymous_auth_disable_date="anonymousAuthDisableDate",
                    anonymous_auth_enabled=False,
                    enabled=False,
                    iam_federation_options={
                        "enabled": False,
                        "roles_key": "rolesKey",
                        "subject_key": "subjectKey"
                    },
                    internal_user_database_enabled=False,
                    jwt_options=opensearchservice_mixins.CfnDomainPropsMixin.JWTOptionsProperty(
                        enabled=False,
                        public_key="publicKey",
                        roles_key="rolesKey",
                        subject_key="subjectKey"
                    ),
                    master_user_options=opensearchservice_mixins.CfnDomainPropsMixin.MasterUserOptionsProperty(
                        master_user_arn="masterUserArn",
                        master_user_name="masterUserName",
                        master_user_password="masterUserPassword"
                    ),
                    saml_options=opensearchservice_mixins.CfnDomainPropsMixin.SAMLOptionsProperty(
                        enabled=False,
                        idp=opensearchservice_mixins.CfnDomainPropsMixin.IdpProperty(
                            entity_id="entityId",
                            metadata_content="metadataContent"
                        ),
                        master_backend_role="masterBackendRole",
                        master_user_name="masterUserName",
                        roles_key="rolesKey",
                        session_timeout_minutes=123,
                        subject_key="subjectKey"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6cd4d2449c04c98649e0d1e99a7bc6e62402889b14b06404d6d558b4e3007e73)
                check_type(argname="argument anonymous_auth_disable_date", value=anonymous_auth_disable_date, expected_type=type_hints["anonymous_auth_disable_date"])
                check_type(argname="argument anonymous_auth_enabled", value=anonymous_auth_enabled, expected_type=type_hints["anonymous_auth_enabled"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument iam_federation_options", value=iam_federation_options, expected_type=type_hints["iam_federation_options"])
                check_type(argname="argument internal_user_database_enabled", value=internal_user_database_enabled, expected_type=type_hints["internal_user_database_enabled"])
                check_type(argname="argument jwt_options", value=jwt_options, expected_type=type_hints["jwt_options"])
                check_type(argname="argument master_user_options", value=master_user_options, expected_type=type_hints["master_user_options"])
                check_type(argname="argument saml_options", value=saml_options, expected_type=type_hints["saml_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if anonymous_auth_disable_date is not None:
                self._values["anonymous_auth_disable_date"] = anonymous_auth_disable_date
            if anonymous_auth_enabled is not None:
                self._values["anonymous_auth_enabled"] = anonymous_auth_enabled
            if enabled is not None:
                self._values["enabled"] = enabled
            if iam_federation_options is not None:
                self._values["iam_federation_options"] = iam_federation_options
            if internal_user_database_enabled is not None:
                self._values["internal_user_database_enabled"] = internal_user_database_enabled
            if jwt_options is not None:
                self._values["jwt_options"] = jwt_options
            if master_user_options is not None:
                self._values["master_user_options"] = master_user_options
            if saml_options is not None:
                self._values["saml_options"] = saml_options

        @builtins.property
        def anonymous_auth_disable_date(self) -> typing.Optional[builtins.str]:
            '''Date and time when the migration period will be disabled.

            Only necessary when `enabling fine-grained access control on an existing domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-enabling-existing>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-anonymousauthdisabledate
            '''
            result = self._values.get("anonymous_auth_disable_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def anonymous_auth_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''True to enable a 30-day migration period during which administrators can create role mappings.

            Only necessary when `enabling fine-grained access control on an existing domain <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html#fgac-enabling-existing>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-anonymousauthenabled
            '''
            result = self._values.get("anonymous_auth_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''True to enable fine-grained access control.

            You must also enable encryption of data at rest and node-to-node encryption. See `Fine-grained access control in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/fgac.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def iam_federation_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.IAMFederationOptionsProperty"]]:
            '''Input configuration for IAM identity federation within advanced security options.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-iamfederationoptions
            '''
            result = self._values.get("iam_federation_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.IAMFederationOptionsProperty"]], result)

        @builtins.property
        def internal_user_database_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''True to enable the internal user database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-internaluserdatabaseenabled
            '''
            result = self._values.get("internal_user_database_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def jwt_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.JWTOptionsProperty"]]:
            '''Container for information about the JWT configuration of the Amazon OpenSearch Service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-jwtoptions
            '''
            result = self._values.get("jwt_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.JWTOptionsProperty"]], result)

        @builtins.property
        def master_user_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.MasterUserOptionsProperty"]]:
            '''Specifies information about the master user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-masteruseroptions
            '''
            result = self._values.get("master_user_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.MasterUserOptionsProperty"]], result)

        @builtins.property
        def saml_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SAMLOptionsProperty"]]:
            '''Container for information about the SAML configuration for OpenSearch Dashboards.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html#cfn-opensearchservice-domain-advancedsecurityoptionsinput-samloptions
            '''
            result = self._values.get("saml_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SAMLOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedSecurityOptionsInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.ClusterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cold_storage_options": "coldStorageOptions",
            "dedicated_master_count": "dedicatedMasterCount",
            "dedicated_master_enabled": "dedicatedMasterEnabled",
            "dedicated_master_type": "dedicatedMasterType",
            "instance_count": "instanceCount",
            "instance_type": "instanceType",
            "multi_az_with_standby_enabled": "multiAzWithStandbyEnabled",
            "node_options": "nodeOptions",
            "warm_count": "warmCount",
            "warm_enabled": "warmEnabled",
            "warm_type": "warmType",
            "zone_awareness_config": "zoneAwarenessConfig",
            "zone_awareness_enabled": "zoneAwarenessEnabled",
        },
    )
    class ClusterConfigProperty:
        def __init__(
            self,
            *,
            cold_storage_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.ColdStorageOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dedicated_master_count: typing.Optional[jsii.Number] = None,
            dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            dedicated_master_type: typing.Optional[builtins.str] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            instance_type: typing.Optional[builtins.str] = None,
            multi_az_with_standby_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            node_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.NodeOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            warm_count: typing.Optional[jsii.Number] = None,
            warm_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            warm_type: typing.Optional[builtins.str] = None,
            zone_awareness_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.ZoneAwarenessConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The cluster configuration for the OpenSearch Service domain.

            You can specify options such as the instance type and the number of instances. For more information, see `Creating and managing Amazon OpenSearch Service domains <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createupdatedomains.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :param cold_storage_options: Container for cold storage configuration options.
            :param dedicated_master_count: The number of instances to use for the master node. If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property.
            :param dedicated_master_enabled: Indicates whether to use a dedicated master node for the OpenSearch Service domain. A dedicated master node is a cluster node that performs cluster management tasks, but doesn't hold data or respond to data upload requests. Dedicated master nodes offload cluster management tasks to increase the stability of your search clusters. See `Dedicated master nodes in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html>`_ .
            :param dedicated_master_type: The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search`` . If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property. For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .
            :param instance_count: The number of data nodes (instances) to use in the OpenSearch Service domain.
            :param instance_type: The instance type for your data nodes, such as ``m3.medium.search`` . For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .
            :param multi_az_with_standby_enabled: Indicates whether Multi-AZ with Standby deployment option is enabled. For more information, see `Multi-AZ with Standby <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html#managedomains-za-standby>`_ .
            :param node_options: List of node options for the domain.
            :param warm_count: The number of warm nodes in the cluster.
            :param warm_enabled: Whether to enable UltraWarm storage for the cluster. See `UltraWarm storage for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ultrawarm.html>`_ .
            :param warm_type: The instance type for the cluster's warm nodes.
            :param zone_awareness_config: Specifies zone awareness configuration options. Only use if ``ZoneAwarenessEnabled`` is ``true`` .
            :param zone_awareness_enabled: Indicates whether to enable zone awareness for the OpenSearch Service domain. When you enable zone awareness, OpenSearch Service allocates the nodes and replica index shards that belong to a cluster across two Availability Zones (AZs) in the same region to prevent data loss and minimize downtime in the event of node or data center failure. Don't enable zone awareness if your cluster has no replica index shards or is a single-node cluster. For more information, see `Configuring a multi-AZ domain in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                cluster_config_property = opensearchservice_mixins.CfnDomainPropsMixin.ClusterConfigProperty(
                    cold_storage_options=opensearchservice_mixins.CfnDomainPropsMixin.ColdStorageOptionsProperty(
                        enabled=False
                    ),
                    dedicated_master_count=123,
                    dedicated_master_enabled=False,
                    dedicated_master_type="dedicatedMasterType",
                    instance_count=123,
                    instance_type="instanceType",
                    multi_az_with_standby_enabled=False,
                    node_options=[opensearchservice_mixins.CfnDomainPropsMixin.NodeOptionProperty(
                        node_config=opensearchservice_mixins.CfnDomainPropsMixin.NodeConfigProperty(
                            count=123,
                            enabled=False,
                            type="type"
                        ),
                        node_type="nodeType"
                    )],
                    warm_count=123,
                    warm_enabled=False,
                    warm_type="warmType",
                    zone_awareness_config=opensearchservice_mixins.CfnDomainPropsMixin.ZoneAwarenessConfigProperty(
                        availability_zone_count=123
                    ),
                    zone_awareness_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e2181dd2836f159ba83eced9e9a2d1a9d80fbf9d12512464e9e89c241880572)
                check_type(argname="argument cold_storage_options", value=cold_storage_options, expected_type=type_hints["cold_storage_options"])
                check_type(argname="argument dedicated_master_count", value=dedicated_master_count, expected_type=type_hints["dedicated_master_count"])
                check_type(argname="argument dedicated_master_enabled", value=dedicated_master_enabled, expected_type=type_hints["dedicated_master_enabled"])
                check_type(argname="argument dedicated_master_type", value=dedicated_master_type, expected_type=type_hints["dedicated_master_type"])
                check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument multi_az_with_standby_enabled", value=multi_az_with_standby_enabled, expected_type=type_hints["multi_az_with_standby_enabled"])
                check_type(argname="argument node_options", value=node_options, expected_type=type_hints["node_options"])
                check_type(argname="argument warm_count", value=warm_count, expected_type=type_hints["warm_count"])
                check_type(argname="argument warm_enabled", value=warm_enabled, expected_type=type_hints["warm_enabled"])
                check_type(argname="argument warm_type", value=warm_type, expected_type=type_hints["warm_type"])
                check_type(argname="argument zone_awareness_config", value=zone_awareness_config, expected_type=type_hints["zone_awareness_config"])
                check_type(argname="argument zone_awareness_enabled", value=zone_awareness_enabled, expected_type=type_hints["zone_awareness_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cold_storage_options is not None:
                self._values["cold_storage_options"] = cold_storage_options
            if dedicated_master_count is not None:
                self._values["dedicated_master_count"] = dedicated_master_count
            if dedicated_master_enabled is not None:
                self._values["dedicated_master_enabled"] = dedicated_master_enabled
            if dedicated_master_type is not None:
                self._values["dedicated_master_type"] = dedicated_master_type
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if multi_az_with_standby_enabled is not None:
                self._values["multi_az_with_standby_enabled"] = multi_az_with_standby_enabled
            if node_options is not None:
                self._values["node_options"] = node_options
            if warm_count is not None:
                self._values["warm_count"] = warm_count
            if warm_enabled is not None:
                self._values["warm_enabled"] = warm_enabled
            if warm_type is not None:
                self._values["warm_type"] = warm_type
            if zone_awareness_config is not None:
                self._values["zone_awareness_config"] = zone_awareness_config
            if zone_awareness_enabled is not None:
                self._values["zone_awareness_enabled"] = zone_awareness_enabled

        @builtins.property
        def cold_storage_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ColdStorageOptionsProperty"]]:
            '''Container for cold storage configuration options.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-coldstorageoptions
            '''
            result = self._values.get("cold_storage_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ColdStorageOptionsProperty"]], result)

        @builtins.property
        def dedicated_master_count(self) -> typing.Optional[jsii.Number]:
            '''The number of instances to use for the master node.

            If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-dedicatedmastercount
            '''
            result = self._values.get("dedicated_master_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dedicated_master_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to use a dedicated master node for the OpenSearch Service domain.

            A dedicated master node is a cluster node that performs cluster management tasks, but doesn't hold data or respond to data upload requests. Dedicated master nodes offload cluster management tasks to increase the stability of your search clusters. See `Dedicated master nodes in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-dedicatedmasternodes.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-dedicatedmasterenabled
            '''
            result = self._values.get("dedicated_master_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def dedicated_master_type(self) -> typing.Optional[builtins.str]:
            '''The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.search`` . If you specify this property, you must specify ``true`` for the ``DedicatedMasterEnabled`` property. For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-dedicatedmastertype
            '''
            result = self._values.get("dedicated_master_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            '''The number of data nodes (instances) to use in the OpenSearch Service domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-instancecount
            '''
            result = self._values.get("instance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The instance type for your data nodes, such as ``m3.medium.search`` . For valid values, see `Supported instance types in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/supported-instance-types.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multi_az_with_standby_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Multi-AZ with Standby deployment option is enabled.

            For more information, see `Multi-AZ with Standby <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html#managedomains-za-standby>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-multiazwithstandbyenabled
            '''
            result = self._values.get("multi_az_with_standby_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def node_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.NodeOptionProperty"]]]]:
            '''List of node options for the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-nodeoptions
            '''
            result = self._values.get("node_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.NodeOptionProperty"]]]], result)

        @builtins.property
        def warm_count(self) -> typing.Optional[jsii.Number]:
            '''The number of warm nodes in the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-warmcount
            '''
            result = self._values.get("warm_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def warm_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to enable UltraWarm storage for the cluster.

            See `UltraWarm storage for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/ultrawarm.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-warmenabled
            '''
            result = self._values.get("warm_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def warm_type(self) -> typing.Optional[builtins.str]:
            '''The instance type for the cluster's warm nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-warmtype
            '''
            result = self._values.get("warm_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zone_awareness_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ZoneAwarenessConfigProperty"]]:
            '''Specifies zone awareness configuration options.

            Only use if ``ZoneAwarenessEnabled`` is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-zoneawarenessconfig
            '''
            result = self._values.get("zone_awareness_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.ZoneAwarenessConfigProperty"]], result)

        @builtins.property
        def zone_awareness_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to enable zone awareness for the OpenSearch Service domain.

            When you enable zone awareness, OpenSearch Service allocates the nodes and replica index shards that belong to a cluster across two Availability Zones (AZs) in the same region to prevent data loss and minimize downtime in the event of node or data center failure. Don't enable zone awareness if your cluster has no replica index shards or is a single-node cluster. For more information, see `Configuring a multi-AZ domain in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-multiaz.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html#cfn-opensearchservice-domain-clusterconfig-zoneawarenessenabled
            '''
            result = self._values.get("zone_awareness_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClusterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.CognitoOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "identity_pool_id": "identityPoolId",
            "role_arn": "roleArn",
            "user_pool_id": "userPoolId",
        },
    )
    class CognitoOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            identity_pool_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures OpenSearch Service to use Amazon Cognito authentication for OpenSearch Dashboards.

            :param enabled: Whether to enable or disable Amazon Cognito authentication for OpenSearch Dashboards. See `Amazon Cognito authentication for OpenSearch Dashboards <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html>`_ .
            :param identity_pool_id: The Amazon Cognito identity pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication. Required if you enabled Cognito Authentication for OpenSearch Dashboards.
            :param role_arn: The ``AmazonOpenSearchServiceCognitoAccess`` role that allows OpenSearch Service to configure your user pool and identity pool. Required if you enabled Cognito Authentication for OpenSearch Dashboards.
            :param user_pool_id: The Amazon Cognito user pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication. Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                cognito_options_property = opensearchservice_mixins.CfnDomainPropsMixin.CognitoOptionsProperty(
                    enabled=False,
                    identity_pool_id="identityPoolId",
                    role_arn="roleArn",
                    user_pool_id="userPoolId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__556ed60c56eebc7f90a7d78af2beb82db78156fab9572f844527a1d37f3308b2)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument user_pool_id", value=user_pool_id, expected_type=type_hints["user_pool_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if identity_pool_id is not None:
                self._values["identity_pool_id"] = identity_pool_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to enable or disable Amazon Cognito authentication for OpenSearch Dashboards.

            See `Amazon Cognito authentication for OpenSearch Dashboards <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cognito-auth.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def identity_pool_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Cognito identity pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication.

            Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-identitypoolid
            '''
            result = self._values.get("identity_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ``AmazonOpenSearchServiceCognitoAccess`` role that allows OpenSearch Service to configure your user pool and identity pool.

            Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Cognito user pool ID that you want OpenSearch Service to use for OpenSearch Dashboards authentication.

            Required if you enabled Cognito Authentication for OpenSearch Dashboards.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-cognitooptions.html#cfn-opensearchservice-domain-cognitooptions-userpoolid
            '''
            result = self._values.get("user_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.ColdStorageOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class ColdStorageOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Container for the parameters required to enable cold storage for an OpenSearch Service domain.

            For more information, see `Cold storage for Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cold-storage.html>`_ .

            :param enabled: Whether to enable or disable cold storage on the domain. You must enable UltraWarm storage to enable cold storage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-coldstorageoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                cold_storage_options_property = opensearchservice_mixins.CfnDomainPropsMixin.ColdStorageOptionsProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea14dc72b46f2962d29ed059334b38198e7b83c6f4f66a4e80abe639d635a8ce)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to enable or disable cold storage on the domain.

            You must enable UltraWarm storage to enable cold storage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-coldstorageoptions.html#cfn-opensearchservice-domain-coldstorageoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColdStorageOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.DomainEndpointOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_endpoint": "customEndpoint",
            "custom_endpoint_certificate_arn": "customEndpointCertificateArn",
            "custom_endpoint_enabled": "customEndpointEnabled",
            "enforce_https": "enforceHttps",
            "tls_security_policy": "tlsSecurityPolicy",
        },
    )
    class DomainEndpointOptionsProperty:
        def __init__(
            self,
            *,
            custom_endpoint: typing.Optional[builtins.str] = None,
            custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
            custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enforce_https: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            tls_security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies additional options for the domain endpoint, such as whether to require HTTPS for all traffic or whether to use a custom endpoint rather than the default endpoint.

            :param custom_endpoint: The fully qualified URL for your custom endpoint. Required if you enabled a custom endpoint for the domain.
            :param custom_endpoint_certificate_arn: The Certificate Manager ARN for your domain's SSL/TLS certificate. Required if you enabled a custom endpoint for the domain.
            :param custom_endpoint_enabled: True to enable a custom endpoint for the domain. If enabled, you must also provide values for ``CustomEndpoint`` and ``CustomEndpointCertificateArn`` .
            :param enforce_https: True to require that all traffic to the domain arrive over HTTPS. Required if you enable fine-grained access control in `AdvancedSecurityOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .
            :param tls_security_policy: The minimum TLS version required for traffic to the domain. The policy can be one of the following values:. - *Policy-Min-TLS-1-0-2019-07:* TLS security policy that supports TLS version 1.0 to TLS version 1.2 - *Policy-Min-TLS-1-2-2019-07:* TLS security policy that supports only TLS version 1.2 - *Policy-Min-TLS-1-2-PFS-2023-10:* TLS security policy that supports TLS version 1.2 to TLS version 1.3 with perfect forward secrecy cipher suites

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                domain_endpoint_options_property = opensearchservice_mixins.CfnDomainPropsMixin.DomainEndpointOptionsProperty(
                    custom_endpoint="customEndpoint",
                    custom_endpoint_certificate_arn="customEndpointCertificateArn",
                    custom_endpoint_enabled=False,
                    enforce_https=False,
                    tls_security_policy="tlsSecurityPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5084d9b57b689a1f1e2383f05112ffe76a4377aa0ef4d73592b1e97af7f334f)
                check_type(argname="argument custom_endpoint", value=custom_endpoint, expected_type=type_hints["custom_endpoint"])
                check_type(argname="argument custom_endpoint_certificate_arn", value=custom_endpoint_certificate_arn, expected_type=type_hints["custom_endpoint_certificate_arn"])
                check_type(argname="argument custom_endpoint_enabled", value=custom_endpoint_enabled, expected_type=type_hints["custom_endpoint_enabled"])
                check_type(argname="argument enforce_https", value=enforce_https, expected_type=type_hints["enforce_https"])
                check_type(argname="argument tls_security_policy", value=tls_security_policy, expected_type=type_hints["tls_security_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_endpoint is not None:
                self._values["custom_endpoint"] = custom_endpoint
            if custom_endpoint_certificate_arn is not None:
                self._values["custom_endpoint_certificate_arn"] = custom_endpoint_certificate_arn
            if custom_endpoint_enabled is not None:
                self._values["custom_endpoint_enabled"] = custom_endpoint_enabled
            if enforce_https is not None:
                self._values["enforce_https"] = enforce_https
            if tls_security_policy is not None:
                self._values["tls_security_policy"] = tls_security_policy

        @builtins.property
        def custom_endpoint(self) -> typing.Optional[builtins.str]:
            '''The fully qualified URL for your custom endpoint.

            Required if you enabled a custom endpoint for the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-customendpoint
            '''
            result = self._values.get("custom_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_endpoint_certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Certificate Manager ARN for your domain's SSL/TLS certificate.

            Required if you enabled a custom endpoint for the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-customendpointcertificatearn
            '''
            result = self._values.get("custom_endpoint_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_endpoint_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''True to enable a custom endpoint for the domain.

            If enabled, you must also provide values for ``CustomEndpoint`` and ``CustomEndpointCertificateArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-customendpointenabled
            '''
            result = self._values.get("custom_endpoint_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enforce_https(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''True to require that all traffic to the domain arrive over HTTPS.

            Required if you enable fine-grained access control in `AdvancedSecurityOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-enforcehttps
            '''
            result = self._values.get("enforce_https")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def tls_security_policy(self) -> typing.Optional[builtins.str]:
            '''The minimum TLS version required for traffic to the domain. The policy can be one of the following values:.

            - *Policy-Min-TLS-1-0-2019-07:* TLS security policy that supports TLS version 1.0 to TLS version 1.2
            - *Policy-Min-TLS-1-2-2019-07:* TLS security policy that supports only TLS version 1.2
            - *Policy-Min-TLS-1-2-PFS-2023-10:* TLS security policy that supports TLS version 1.2 to TLS version 1.3 with perfect forward secrecy cipher suites

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-domainendpointoptions.html#cfn-opensearchservice-domain-domainendpointoptions-tlssecuritypolicy
            '''
            result = self._values.get("tls_security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainEndpointOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.EBSOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ebs_enabled": "ebsEnabled",
            "iops": "iops",
            "throughput": "throughput",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EBSOptionsProperty:
        def __init__(
            self,
            *,
            ebs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the OpenSearch Service domain.

            For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :param ebs_enabled: Specifies whether Amazon EBS volumes are attached to data nodes in the OpenSearch Service domain.
            :param iops: The number of I/O operations per second (IOPS) that the volume supports. This property applies only to the ``gp3`` and provisioned IOPS EBS volume types.
            :param throughput: The throughput (in MiB/s) of the EBS volumes attached to data nodes. Applies only to the ``gp3`` volume type.
            :param volume_size: The size (in GiB) of the EBS volume for each data node. The minimum and maximum size of an EBS volume depends on the EBS volume type and the instance type to which it is attached. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .
            :param volume_type: The EBS volume type to use with the OpenSearch Service domain. If you choose ``gp3`` , you must also specify values for ``Iops`` and ``Throughput`` . For more information about each type, see `Amazon EBS volume types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                e_bSOptions_property = opensearchservice_mixins.CfnDomainPropsMixin.EBSOptionsProperty(
                    ebs_enabled=False,
                    iops=123,
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b3228dc32e039695047c7abd04cda2dcf8fb484c8345735ad83d6b1caff155b)
                check_type(argname="argument ebs_enabled", value=ebs_enabled, expected_type=type_hints["ebs_enabled"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ebs_enabled is not None:
                self._values["ebs_enabled"] = ebs_enabled
            if iops is not None:
                self._values["iops"] = iops
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def ebs_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon EBS volumes are attached to data nodes in the OpenSearch Service domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-ebsenabled
            '''
            result = self._values.get("ebs_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of I/O operations per second (IOPS) that the volume supports.

            This property applies only to the ``gp3`` and provisioned IOPS EBS volume types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''The throughput (in MiB/s) of the EBS volumes attached to data nodes.

            Applies only to the ``gp3`` volume type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''The size (in GiB) of the EBS volume for each data node.

            The minimum and maximum size of an EBS volume depends on the EBS volume type and the instance type to which it is attached. For more information, see `EBS volume size limits <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html#ebsresource>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''The EBS volume type to use with the OpenSearch Service domain.

            If you choose ``gp3`` , you must also specify values for ``Iops`` and ``Throughput`` . For more information about each type, see `Amazon EBS volume types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-ebsoptions.html#cfn-opensearchservice-domain-ebsoptions-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EBSOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.EncryptionAtRestOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "kms_key_id": "kmsKeyId"},
    )
    class EncryptionAtRestOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Whether the domain should encrypt data at rest, and if so, the AWS Key Management Service key to use.

            :param enabled: Specify ``true`` to enable encryption at rest. Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ . If no encryption at rest options were initially specified in the template, updating this property by adding it causes no interruption. However, if you change this property after it's already been set within a template, the domain is deleted and recreated in order to modify the property.
            :param kms_key_id: The KMS key ID. Takes the form ``1a2a3a4-1a2a-3a4a-5a6a-1a2a3a4a5a6a`` . Required if you enable encryption at rest. You can also use ``keyAlias`` as a value. If no encryption at rest options were initially specified in the template, updating this property by adding it causes no interruption. However, if you change this property after it's already been set within a template, the domain is deleted and recreated in order to modify the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                encryption_at_rest_options_property = opensearchservice_mixins.CfnDomainPropsMixin.EncryptionAtRestOptionsProperty(
                    enabled=False,
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4e0589933c168502f95e87a8edad4d3e6dab4b9bf6cd368004d16e1dc70d2f1)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify ``true`` to enable encryption at rest. Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            If no encryption at rest options were initially specified in the template, updating this property by adding it causes no interruption. However, if you change this property after it's already been set within a template, the domain is deleted and recreated in order to modify the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html#cfn-opensearchservice-domain-encryptionatrestoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The KMS key ID. Takes the form ``1a2a3a4-1a2a-3a4a-5a6a-1a2a3a4a5a6a`` . Required if you enable encryption at rest.

            You can also use ``keyAlias`` as a value.

            If no encryption at rest options were initially specified in the template, updating this property by adding it causes no interruption. However, if you change this property after it's already been set within a template, the domain is deleted and recreated in order to modify the property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-encryptionatrestoptions.html#cfn-opensearchservice-domain-encryptionatrestoptions-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionAtRestOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.IAMFederationOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "roles_key": "rolesKey",
            "subject_key": "subjectKey",
        },
    )
    class IAMFederationOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            roles_key: typing.Optional[builtins.str] = None,
            subject_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param enabled: 
            :param roles_key: 
            :param subject_key: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-iamfederationoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                i_aMFederation_options_property = {
                    "enabled": False,
                    "roles_key": "rolesKey",
                    "subject_key": "subjectKey"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6604723555356dcf4b22bd42f92a582f3b05ceb624391a9b4b256074329f95f6)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument roles_key", value=roles_key, expected_type=type_hints["roles_key"])
                check_type(argname="argument subject_key", value=subject_key, expected_type=type_hints["subject_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if roles_key is not None:
                self._values["roles_key"] = roles_key
            if subject_key is not None:
                self._values["subject_key"] = subject_key

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-iamfederationoptions.html#cfn-opensearchservice-domain-iamfederationoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def roles_key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-iamfederationoptions.html#cfn-opensearchservice-domain-iamfederationoptions-roleskey
            '''
            result = self._values.get("roles_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subject_key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-iamfederationoptions.html#cfn-opensearchservice-domain-iamfederationoptions-subjectkey
            '''
            result = self._values.get("subject_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IAMFederationOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.IdentityCenterOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled_api_access": "enabledApiAccess",
            "identity_center_application_arn": "identityCenterApplicationArn",
            "identity_center_instance_arn": "identityCenterInstanceArn",
            "identity_store_id": "identityStoreId",
            "roles_key": "rolesKey",
            "subject_key": "subjectKey",
        },
    )
    class IdentityCenterOptionsProperty:
        def __init__(
            self,
            *,
            enabled_api_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            identity_center_application_arn: typing.Optional[builtins.str] = None,
            identity_center_instance_arn: typing.Optional[builtins.str] = None,
            identity_store_id: typing.Optional[builtins.str] = None,
            roles_key: typing.Optional[builtins.str] = None,
            subject_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings container for integrating IAM Identity Center with OpenSearch UI applications, which enables enabling secure user authentication and access control across multiple data sources.

            This setup supports single sign-on (SSO) through IAM Identity Center, allowing centralized user management.

            :param enabled_api_access: Indicates whether IAM Identity Center is enabled for the application.
            :param identity_center_application_arn: The ARN of the IAM Identity Center application that integrates with Amazon OpenSearch Service.
            :param identity_center_instance_arn: The Amazon Resource Name (ARN) of the IAM Identity Center instance.
            :param identity_store_id: The identifier of the IAM Identity Store.
            :param roles_key: Specifies the attribute that contains the backend role identifier (such as group name or group ID) in IAM Identity Center.
            :param subject_key: Specifies the attribute that contains the subject identifier (such as username, user ID, or email) in IAM Identity Center.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-identitycenteroptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                identity_center_options_property = opensearchservice_mixins.CfnDomainPropsMixin.IdentityCenterOptionsProperty(
                    enabled_api_access=False,
                    identity_center_application_arn="identityCenterApplicationArn",
                    identity_center_instance_arn="identityCenterInstanceArn",
                    identity_store_id="identityStoreId",
                    roles_key="rolesKey",
                    subject_key="subjectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c64cad3c316cf76166079ce7d960664d2c2d5eef17109c4b3c62d7a8c5140e8)
                check_type(argname="argument enabled_api_access", value=enabled_api_access, expected_type=type_hints["enabled_api_access"])
                check_type(argname="argument identity_center_application_arn", value=identity_center_application_arn, expected_type=type_hints["identity_center_application_arn"])
                check_type(argname="argument identity_center_instance_arn", value=identity_center_instance_arn, expected_type=type_hints["identity_center_instance_arn"])
                check_type(argname="argument identity_store_id", value=identity_store_id, expected_type=type_hints["identity_store_id"])
                check_type(argname="argument roles_key", value=roles_key, expected_type=type_hints["roles_key"])
                check_type(argname="argument subject_key", value=subject_key, expected_type=type_hints["subject_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled_api_access is not None:
                self._values["enabled_api_access"] = enabled_api_access
            if identity_center_application_arn is not None:
                self._values["identity_center_application_arn"] = identity_center_application_arn
            if identity_center_instance_arn is not None:
                self._values["identity_center_instance_arn"] = identity_center_instance_arn
            if identity_store_id is not None:
                self._values["identity_store_id"] = identity_store_id
            if roles_key is not None:
                self._values["roles_key"] = roles_key
            if subject_key is not None:
                self._values["subject_key"] = subject_key

        @builtins.property
        def enabled_api_access(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether IAM Identity Center is enabled for the application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-identitycenteroptions.html#cfn-opensearchservice-domain-identitycenteroptions-enabledapiaccess
            '''
            result = self._values.get("enabled_api_access")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def identity_center_application_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM Identity Center application that integrates with Amazon OpenSearch Service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-identitycenteroptions.html#cfn-opensearchservice-domain-identitycenteroptions-identitycenterapplicationarn
            '''
            result = self._values.get("identity_center_application_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identity_center_instance_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM Identity Center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-identitycenteroptions.html#cfn-opensearchservice-domain-identitycenteroptions-identitycenterinstancearn
            '''
            result = self._values.get("identity_center_instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identity_store_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the IAM Identity Store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-identitycenteroptions.html#cfn-opensearchservice-domain-identitycenteroptions-identitystoreid
            '''
            result = self._values.get("identity_store_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def roles_key(self) -> typing.Optional[builtins.str]:
            '''Specifies the attribute that contains the backend role identifier (such as group name or group ID) in IAM Identity Center.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-identitycenteroptions.html#cfn-opensearchservice-domain-identitycenteroptions-roleskey
            '''
            result = self._values.get("roles_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subject_key(self) -> typing.Optional[builtins.str]:
            '''Specifies the attribute that contains the subject identifier (such as username, user ID, or email) in IAM Identity Center.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-identitycenteroptions.html#cfn-opensearchservice-domain-identitycenteroptions-subjectkey
            '''
            result = self._values.get("subject_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentityCenterOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.IdpProperty",
        jsii_struct_bases=[],
        name_mapping={"entity_id": "entityId", "metadata_content": "metadataContent"},
    )
    class IdpProperty:
        def __init__(
            self,
            *,
            entity_id: typing.Optional[builtins.str] = None,
            metadata_content: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The SAML Identity Provider's information.

            :param entity_id: The unique entity ID of the application in the SAML identity provider.
            :param metadata_content: The metadata of the SAML application, in XML format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-idp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                idp_property = opensearchservice_mixins.CfnDomainPropsMixin.IdpProperty(
                    entity_id="entityId",
                    metadata_content="metadataContent"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7057330927b477344be8652e6ba30cb5db16870f6f4e48c272309bbefc772fd4)
                check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
                check_type(argname="argument metadata_content", value=metadata_content, expected_type=type_hints["metadata_content"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entity_id is not None:
                self._values["entity_id"] = entity_id
            if metadata_content is not None:
                self._values["metadata_content"] = metadata_content

        @builtins.property
        def entity_id(self) -> typing.Optional[builtins.str]:
            '''The unique entity ID of the application in the SAML identity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-idp.html#cfn-opensearchservice-domain-idp-entityid
            '''
            result = self._values.get("entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metadata_content(self) -> typing.Optional[builtins.str]:
            '''The metadata of the SAML application, in XML format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-idp.html#cfn-opensearchservice-domain-idp-metadatacontent
            '''
            result = self._values.get("metadata_content")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdpProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.JWTOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "public_key": "publicKey",
            "roles_key": "rolesKey",
            "subject_key": "subjectKey",
        },
    )
    class JWTOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            public_key: typing.Optional[builtins.str] = None,
            roles_key: typing.Optional[builtins.str] = None,
            subject_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param enabled: 
            :param public_key: 
            :param roles_key: 
            :param subject_key: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-jwtoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                j_wTOptions_property = opensearchservice_mixins.CfnDomainPropsMixin.JWTOptionsProperty(
                    enabled=False,
                    public_key="publicKey",
                    roles_key="rolesKey",
                    subject_key="subjectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0633a95f5bb7ff9a59cfd588de7bac2781e39ae33b3bfb3fcd4484eef16e2c68)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
                check_type(argname="argument roles_key", value=roles_key, expected_type=type_hints["roles_key"])
                check_type(argname="argument subject_key", value=subject_key, expected_type=type_hints["subject_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if public_key is not None:
                self._values["public_key"] = public_key
            if roles_key is not None:
                self._values["roles_key"] = roles_key
            if subject_key is not None:
                self._values["subject_key"] = subject_key

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-jwtoptions.html#cfn-opensearchservice-domain-jwtoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def public_key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-jwtoptions.html#cfn-opensearchservice-domain-jwtoptions-publickey
            '''
            result = self._values.get("public_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def roles_key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-jwtoptions.html#cfn-opensearchservice-domain-jwtoptions-roleskey
            '''
            result = self._values.get("roles_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subject_key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-jwtoptions.html#cfn-opensearchservice-domain-jwtoptions-subjectkey
            '''
            result = self._values.get("subject_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JWTOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.LogPublishingOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_log_group_arn": "cloudWatchLogsLogGroupArn",
            "enabled": "enabled",
        },
    )
    class LogPublishingOptionProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies whether the OpenSearch Service domain publishes application, search slow logs, or index slow logs to Amazon CloudWatch.

            Each option must be an object of name ``SEARCH_SLOW_LOGS`` , ``ES_APPLICATION_LOGS`` , ``INDEX_SLOW_LOGS`` , or ``AUDIT_LOGS`` depending on the type of logs you want to publish. For the full syntax, see the `examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchservice-domain.html#aws-resource-opensearchservice-domain--examples>`_ .

            Before you enable log publishing, you need to create a CloudWatch log group and provide OpenSearch Service the correct permissions to write to it. To learn more, see `Enabling log publishing ( AWS CloudFormation) <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/createdomain-configure-slow-logs.html#createdomain-configure-slow-logs-cfn>`_ .

            :param cloud_watch_logs_log_group_arn: Specifies the CloudWatch log group to publish to. Required if you enable log publishing.
            :param enabled: If ``true`` , enables the publishing of logs to CloudWatch. Default: ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-logpublishingoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                log_publishing_option_property = opensearchservice_mixins.CfnDomainPropsMixin.LogPublishingOptionProperty(
                    cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84d4fe5877cff89da07c3c8ab32d084bc7e427e6f2e68c4b2ba59c92da29994b)
                check_type(argname="argument cloud_watch_logs_log_group_arn", value=cloud_watch_logs_log_group_arn, expected_type=type_hints["cloud_watch_logs_log_group_arn"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_log_group_arn is not None:
                self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def cloud_watch_logs_log_group_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the CloudWatch log group to publish to.

            Required if you enable log publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-logpublishingoption.html#cfn-opensearchservice-domain-logpublishingoption-cloudwatchlogsloggrouparn
            '''
            result = self._values.get("cloud_watch_logs_log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If ``true`` , enables the publishing of logs to CloudWatch.

            Default: ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-logpublishingoption.html#cfn-opensearchservice-domain-logpublishingoption-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPublishingOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.MasterUserOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "master_user_arn": "masterUserArn",
            "master_user_name": "masterUserName",
            "master_user_password": "masterUserPassword",
        },
    )
    class MasterUserOptionsProperty:
        def __init__(
            self,
            *,
            master_user_arn: typing.Optional[builtins.str] = None,
            master_user_name: typing.Optional[builtins.str] = None,
            master_user_password: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information about the master user.

            Required if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :param master_user_arn: Amazon Resource Name (ARN) for the master user. The ARN can point to an IAM user or role. This property is required for Amazon Cognito to work, and it must match the role configured for Cognito. Only specify if ``InternalUserDatabaseEnabled`` is false in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .
            :param master_user_name: Username for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ . If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.
            :param master_user_password: Password for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ . If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                master_user_options_property = opensearchservice_mixins.CfnDomainPropsMixin.MasterUserOptionsProperty(
                    master_user_arn="masterUserArn",
                    master_user_name="masterUserName",
                    master_user_password="masterUserPassword"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5365d1cfa4025c0c9f55d823a49619240f0eaafe602c7e3552c0fe8dabf46c19)
                check_type(argname="argument master_user_arn", value=master_user_arn, expected_type=type_hints["master_user_arn"])
                check_type(argname="argument master_user_name", value=master_user_name, expected_type=type_hints["master_user_name"])
                check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if master_user_arn is not None:
                self._values["master_user_arn"] = master_user_arn
            if master_user_name is not None:
                self._values["master_user_name"] = master_user_name
            if master_user_password is not None:
                self._values["master_user_password"] = master_user_password

        @builtins.property
        def master_user_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) for the master user.

            The ARN can point to an IAM user or role. This property is required for Amazon Cognito to work, and it must match the role configured for Cognito. Only specify if ``InternalUserDatabaseEnabled`` is false in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html#cfn-opensearchservice-domain-masteruseroptions-masteruserarn
            '''
            result = self._values.get("master_user_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_name(self) -> typing.Optional[builtins.str]:
            '''Username for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html#cfn-opensearchservice-domain-masteruseroptions-masterusername
            '''
            result = self._values.get("master_user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_password(self) -> typing.Optional[builtins.str]:
            '''Password for the master user. Only specify if ``InternalUserDatabaseEnabled`` is true in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            If you don't want to specify this value directly within the template, you can use a `dynamic reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html>`_ instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-masteruseroptions.html#cfn-opensearchservice-domain-masteruseroptions-masteruserpassword
            '''
            result = self._values.get("master_user_password")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MasterUserOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.NodeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"count": "count", "enabled": "enabled", "type": "type"},
    )
    class NodeConfigProperty:
        def __init__(
            self,
            *,
            count: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration options for defining the setup of any node type within the cluster.

            :param count: The number of nodes of a specific type within the cluster.
            :param enabled: A boolean value indicating whether a specific node type is active or inactive.
            :param type: The instance type of a particular node within the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                node_config_property = opensearchservice_mixins.CfnDomainPropsMixin.NodeConfigProperty(
                    count=123,
                    enabled=False,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6a4daed3a6a987d63e7c91baf7470d45c4f63f7ee9c6631f6dcf56dc05e88b7)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if enabled is not None:
                self._values["enabled"] = enabled
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''The number of nodes of a specific type within the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodeconfig.html#cfn-opensearchservice-domain-nodeconfig-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value indicating whether a specific node type is active or inactive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodeconfig.html#cfn-opensearchservice-domain-nodeconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The instance type of a particular node within the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodeconfig.html#cfn-opensearchservice-domain-nodeconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.NodeOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"node_config": "nodeConfig", "node_type": "nodeType"},
    )
    class NodeOptionProperty:
        def __init__(
            self,
            *,
            node_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.NodeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            node_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for defining the node type within a cluster.

            :param node_config: Configuration options for defining the setup of any node type.
            :param node_type: Defines the type of node, such as coordinating nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodeoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                node_option_property = opensearchservice_mixins.CfnDomainPropsMixin.NodeOptionProperty(
                    node_config=opensearchservice_mixins.CfnDomainPropsMixin.NodeConfigProperty(
                        count=123,
                        enabled=False,
                        type="type"
                    ),
                    node_type="nodeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb9f81450ca5d78140f2fa680582ca562a0b7152696b6c43602d379b7e9c82a3)
                check_type(argname="argument node_config", value=node_config, expected_type=type_hints["node_config"])
                check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if node_config is not None:
                self._values["node_config"] = node_config
            if node_type is not None:
                self._values["node_type"] = node_type

        @builtins.property
        def node_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.NodeConfigProperty"]]:
            '''Configuration options for defining the setup of any node type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodeoption.html#cfn-opensearchservice-domain-nodeoption-nodeconfig
            '''
            result = self._values.get("node_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.NodeConfigProperty"]], result)

        @builtins.property
        def node_type(self) -> typing.Optional[builtins.str]:
            '''Defines the type of node, such as coordinating nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodeoption.html#cfn-opensearchservice-domain-nodeoption-nodetype
            '''
            result = self._values.get("node_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.NodeToNodeEncryptionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class NodeToNodeEncryptionOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies options for node-to-node encryption.

            :param enabled: Specifies to enable or disable node-to-node encryption on the domain. Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                node_to_node_encryption_options_property = opensearchservice_mixins.CfnDomainPropsMixin.NodeToNodeEncryptionOptionsProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__692d5697243e5b96d58732c8188e155e13dc6a96539f0a3630e50493cd35152e)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies to enable or disable node-to-node encryption on the domain.

            Required if you enable fine-grained access control in `AdvancedSecurityOptionsInput <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-advancedsecurityoptionsinput.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-nodetonodeencryptionoptions.html#cfn-opensearchservice-domain-nodetonodeencryptionoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeToNodeEncryptionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.OffPeakWindowOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "off_peak_window": "offPeakWindow"},
    )
    class OffPeakWindowOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            off_peak_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.OffPeakWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Off-peak window settings for the domain.

            :param enabled: Specifies whether off-peak window settings are enabled for the domain.
            :param off_peak_window: Off-peak window settings for the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindowoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                off_peak_window_options_property = opensearchservice_mixins.CfnDomainPropsMixin.OffPeakWindowOptionsProperty(
                    enabled=False,
                    off_peak_window=opensearchservice_mixins.CfnDomainPropsMixin.OffPeakWindowProperty(
                        window_start_time=opensearchservice_mixins.CfnDomainPropsMixin.WindowStartTimeProperty(
                            hours=123,
                            minutes=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1232be18ea232c04deba54250bbbf35ebc8ba599699e16e7c89041376abff479)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument off_peak_window", value=off_peak_window, expected_type=type_hints["off_peak_window"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if off_peak_window is not None:
                self._values["off_peak_window"] = off_peak_window

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether off-peak window settings are enabled for the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindowoptions.html#cfn-opensearchservice-domain-offpeakwindowoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def off_peak_window(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.OffPeakWindowProperty"]]:
            '''Off-peak window settings for the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindowoptions.html#cfn-opensearchservice-domain-offpeakwindowoptions-offpeakwindow
            '''
            result = self._values.get("off_peak_window")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.OffPeakWindowProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OffPeakWindowOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.OffPeakWindowProperty",
        jsii_struct_bases=[],
        name_mapping={"window_start_time": "windowStartTime"},
    )
    class OffPeakWindowProperty:
        def __init__(
            self,
            *,
            window_start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.WindowStartTimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A custom 10-hour, low-traffic window during which OpenSearch Service can perform mandatory configuration changes on the domain.

            These actions can include scheduled service software updates and blue/green Auto-Tune enhancements. OpenSearch Service will schedule these actions during the window that you specify. If you don't specify a window start time, it defaults to 10:00 P.M. local time.

            :param window_start_time: The desired start time for an off-peak maintenance window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                off_peak_window_property = opensearchservice_mixins.CfnDomainPropsMixin.OffPeakWindowProperty(
                    window_start_time=opensearchservice_mixins.CfnDomainPropsMixin.WindowStartTimeProperty(
                        hours=123,
                        minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87038e503b824de24dbf538c314cbafa90f93343b666edc88f0cf40de3fd03d7)
                check_type(argname="argument window_start_time", value=window_start_time, expected_type=type_hints["window_start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if window_start_time is not None:
                self._values["window_start_time"] = window_start_time

        @builtins.property
        def window_start_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.WindowStartTimeProperty"]]:
            '''The desired start time for an off-peak maintenance window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-offpeakwindow.html#cfn-opensearchservice-domain-offpeakwindow-windowstarttime
            '''
            result = self._values.get("window_start_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.WindowStartTimeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OffPeakWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.S3VectorsEngineProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class S3VectorsEngineProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Options for enabling S3 vectors engine features on the specified domain.

            :param enabled: Enables S3 vectors engine features.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-s3vectorsengine.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                s3_vectors_engine_property = opensearchservice_mixins.CfnDomainPropsMixin.S3VectorsEngineProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f85106beb499acc9f34b01dbbdd7632b429d7b5179071f4ebd68489e48b74898)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables S3 vectors engine features.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-s3vectorsengine.html#cfn-opensearchservice-domain-s3vectorsengine-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3VectorsEngineProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.SAMLOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "idp": "idp",
            "master_backend_role": "masterBackendRole",
            "master_user_name": "masterUserName",
            "roles_key": "rolesKey",
            "session_timeout_minutes": "sessionTimeoutMinutes",
            "subject_key": "subjectKey",
        },
    )
    class SAMLOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            idp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.IdpProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            master_backend_role: typing.Optional[builtins.str] = None,
            master_user_name: typing.Optional[builtins.str] = None,
            roles_key: typing.Optional[builtins.str] = None,
            session_timeout_minutes: typing.Optional[jsii.Number] = None,
            subject_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Container for information about the SAML configuration for OpenSearch Dashboards.

            :param enabled: True to enable SAML authentication for a domain.
            :param idp: The SAML Identity Provider's information.
            :param master_backend_role: The backend role that the SAML master user is mapped to.
            :param master_user_name: The SAML master user name, which is stored in the domain's internal user database.
            :param roles_key: Element of the SAML assertion to use for backend roles. Default is ``roles`` .
            :param session_timeout_minutes: The duration, in minutes, after which a user session becomes inactive. Acceptable values are between 1 and 1440, and the default value is 60.
            :param subject_key: Element of the SAML assertion to use for the user name. Default is ``NameID`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                s_aMLOptions_property = opensearchservice_mixins.CfnDomainPropsMixin.SAMLOptionsProperty(
                    enabled=False,
                    idp=opensearchservice_mixins.CfnDomainPropsMixin.IdpProperty(
                        entity_id="entityId",
                        metadata_content="metadataContent"
                    ),
                    master_backend_role="masterBackendRole",
                    master_user_name="masterUserName",
                    roles_key="rolesKey",
                    session_timeout_minutes=123,
                    subject_key="subjectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab6f7318a214c627f1ae2cd81e3fc8e8535feb101f20d2ad70a35d7411d5f202)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument idp", value=idp, expected_type=type_hints["idp"])
                check_type(argname="argument master_backend_role", value=master_backend_role, expected_type=type_hints["master_backend_role"])
                check_type(argname="argument master_user_name", value=master_user_name, expected_type=type_hints["master_user_name"])
                check_type(argname="argument roles_key", value=roles_key, expected_type=type_hints["roles_key"])
                check_type(argname="argument session_timeout_minutes", value=session_timeout_minutes, expected_type=type_hints["session_timeout_minutes"])
                check_type(argname="argument subject_key", value=subject_key, expected_type=type_hints["subject_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if idp is not None:
                self._values["idp"] = idp
            if master_backend_role is not None:
                self._values["master_backend_role"] = master_backend_role
            if master_user_name is not None:
                self._values["master_user_name"] = master_user_name
            if roles_key is not None:
                self._values["roles_key"] = roles_key
            if session_timeout_minutes is not None:
                self._values["session_timeout_minutes"] = session_timeout_minutes
            if subject_key is not None:
                self._values["subject_key"] = subject_key

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''True to enable SAML authentication for a domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def idp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.IdpProperty"]]:
            '''The SAML Identity Provider's information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-idp
            '''
            result = self._values.get("idp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.IdpProperty"]], result)

        @builtins.property
        def master_backend_role(self) -> typing.Optional[builtins.str]:
            '''The backend role that the SAML master user is mapped to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-masterbackendrole
            '''
            result = self._values.get("master_backend_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_name(self) -> typing.Optional[builtins.str]:
            '''The SAML master user name, which is stored in the domain's internal user database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-masterusername
            '''
            result = self._values.get("master_user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def roles_key(self) -> typing.Optional[builtins.str]:
            '''Element of the SAML assertion to use for backend roles.

            Default is ``roles`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-roleskey
            '''
            result = self._values.get("roles_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The duration, in minutes, after which a user session becomes inactive.

            Acceptable values are between 1 and 1440, and the default value is 60.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-sessiontimeoutminutes
            '''
            result = self._values.get("session_timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def subject_key(self) -> typing.Optional[builtins.str]:
            '''Element of the SAML assertion to use for the user name.

            Default is ``NameID`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-samloptions.html#cfn-opensearchservice-domain-samloptions-subjectkey
            '''
            result = self._values.get("subject_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMLOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.ServiceSoftwareOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automated_update_date": "automatedUpdateDate",
            "cancellable": "cancellable",
            "current_version": "currentVersion",
            "description": "description",
            "new_version": "newVersion",
            "optional_deployment": "optionalDeployment",
            "update_available": "updateAvailable",
            "update_status": "updateStatus",
        },
    )
    class ServiceSoftwareOptionsProperty:
        def __init__(
            self,
            *,
            automated_update_date: typing.Optional[builtins.str] = None,
            cancellable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            current_version: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            new_version: typing.Optional[builtins.str] = None,
            optional_deployment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            update_available: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            update_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The current status of the service software for an Amazon OpenSearch Service domain.

            For more information, see `Service software updates in Amazon OpenSearch Service <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/service-software.html>`_ .

            :param automated_update_date: The timestamp, in Epoch time, until which you can manually request a service software update. After this date, we automatically update your service software.
            :param cancellable: True if you're able to cancel your service software version update. False if you can't cancel your service software update.
            :param current_version: The current service software version present on the domain.
            :param description: A description of the service software update status.
            :param new_version: The new service software version, if one is available.
            :param optional_deployment: True if a service software is never automatically updated. False if a service software is automatically updated after the automated update date.
            :param update_available: True if you're able to update your service software version. False if you can't update your service software version.
            :param update_status: The status of your service software update.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                service_software_options_property = opensearchservice_mixins.CfnDomainPropsMixin.ServiceSoftwareOptionsProperty(
                    automated_update_date="automatedUpdateDate",
                    cancellable=False,
                    current_version="currentVersion",
                    description="description",
                    new_version="newVersion",
                    optional_deployment=False,
                    update_available=False,
                    update_status="updateStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6db4135e1c963952dc3ba55cd3250544a3ce94b0e157a7f478e9ec929902745)
                check_type(argname="argument automated_update_date", value=automated_update_date, expected_type=type_hints["automated_update_date"])
                check_type(argname="argument cancellable", value=cancellable, expected_type=type_hints["cancellable"])
                check_type(argname="argument current_version", value=current_version, expected_type=type_hints["current_version"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument new_version", value=new_version, expected_type=type_hints["new_version"])
                check_type(argname="argument optional_deployment", value=optional_deployment, expected_type=type_hints["optional_deployment"])
                check_type(argname="argument update_available", value=update_available, expected_type=type_hints["update_available"])
                check_type(argname="argument update_status", value=update_status, expected_type=type_hints["update_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automated_update_date is not None:
                self._values["automated_update_date"] = automated_update_date
            if cancellable is not None:
                self._values["cancellable"] = cancellable
            if current_version is not None:
                self._values["current_version"] = current_version
            if description is not None:
                self._values["description"] = description
            if new_version is not None:
                self._values["new_version"] = new_version
            if optional_deployment is not None:
                self._values["optional_deployment"] = optional_deployment
            if update_available is not None:
                self._values["update_available"] = update_available
            if update_status is not None:
                self._values["update_status"] = update_status

        @builtins.property
        def automated_update_date(self) -> typing.Optional[builtins.str]:
            '''The timestamp, in Epoch time, until which you can manually request a service software update.

            After this date, we automatically update your service software.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-automatedupdatedate
            '''
            result = self._values.get("automated_update_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cancellable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''True if you're able to cancel your service software version update.

            False if you can't cancel your service software update.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-cancellable
            '''
            result = self._values.get("cancellable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def current_version(self) -> typing.Optional[builtins.str]:
            '''The current service software version present on the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-currentversion
            '''
            result = self._values.get("current_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the service software update status.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def new_version(self) -> typing.Optional[builtins.str]:
            '''The new service software version, if one is available.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-newversion
            '''
            result = self._values.get("new_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def optional_deployment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''True if a service software is never automatically updated.

            False if a service software is automatically updated after the automated update date.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-optionaldeployment
            '''
            result = self._values.get("optional_deployment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def update_available(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''True if you're able to update your service software version.

            False if you can't update your service software version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-updateavailable
            '''
            result = self._values.get("update_available")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def update_status(self) -> typing.Optional[builtins.str]:
            '''The status of your service software update.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-servicesoftwareoptions.html#cfn-opensearchservice-domain-servicesoftwareoptions-updatestatus
            '''
            result = self._values.get("update_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceSoftwareOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.SnapshotOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"automated_snapshot_start_hour": "automatedSnapshotStartHour"},
    )
    class SnapshotOptionsProperty:
        def __init__(
            self,
            *,
            automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''*DEPRECATED* .

            This setting is only relevant to domains running legacy Elasticsearch OSS versions earlier than 5.3. It does not apply to OpenSearch domains.

            The automated snapshot configuration for the OpenSearch Service domain indexes.

            :param automated_snapshot_start_hour: The hour in UTC during which the service takes an automated daily snapshot of the indexes in the OpenSearch Service domain. For example, if you specify 0, OpenSearch Service takes an automated snapshot everyday between midnight and 1 am. You can specify a value between 0 and 23.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-snapshotoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                snapshot_options_property = opensearchservice_mixins.CfnDomainPropsMixin.SnapshotOptionsProperty(
                    automated_snapshot_start_hour=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6984dc2647c174136f4df4de4c9c3537aefd8829966a23f99ef27b59ca7bf50)
                check_type(argname="argument automated_snapshot_start_hour", value=automated_snapshot_start_hour, expected_type=type_hints["automated_snapshot_start_hour"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automated_snapshot_start_hour is not None:
                self._values["automated_snapshot_start_hour"] = automated_snapshot_start_hour

        @builtins.property
        def automated_snapshot_start_hour(self) -> typing.Optional[jsii.Number]:
            '''The hour in UTC during which the service takes an automated daily snapshot of the indexes in the OpenSearch Service domain.

            For example, if you specify 0, OpenSearch Service takes an automated snapshot everyday between midnight and 1 am. You can specify a value between 0 and 23.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-snapshotoptions.html#cfn-opensearchservice-domain-snapshotoptions-automatedsnapshotstarthour
            '''
            result = self._values.get("automated_snapshot_start_hour")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapshotOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.SoftwareUpdateOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"auto_software_update_enabled": "autoSoftwareUpdateEnabled"},
    )
    class SoftwareUpdateOptionsProperty:
        def __init__(
            self,
            *,
            auto_software_update_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Options for configuring service software updates for a domain.

            :param auto_software_update_enabled: Specifies whether automatic service software updates are enabled for the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-softwareupdateoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                software_update_options_property = opensearchservice_mixins.CfnDomainPropsMixin.SoftwareUpdateOptionsProperty(
                    auto_software_update_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70e6380093fca010ef5ca8f1ee9456de3e2c32e063c2f1c51c0654dbf7e6463c)
                check_type(argname="argument auto_software_update_enabled", value=auto_software_update_enabled, expected_type=type_hints["auto_software_update_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_software_update_enabled is not None:
                self._values["auto_software_update_enabled"] = auto_software_update_enabled

        @builtins.property
        def auto_software_update_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether automatic service software updates are enabled for the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-softwareupdateoptions.html#cfn-opensearchservice-domain-softwareupdateoptions-autosoftwareupdateenabled
            '''
            result = self._values.get("auto_software_update_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SoftwareUpdateOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.VPCOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VPCOptionsProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The virtual private cloud (VPC) configuration for the OpenSearch Service domain.

            For more information, see `Launching your Amazon OpenSearch Service domains using a VPC <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vpc.html>`_ in the *Amazon OpenSearch Service Developer Guide* .

            :param security_group_ids: The list of security group IDs that are associated with the VPC endpoints for the domain. If you don't provide a security group ID, OpenSearch Service uses the default security group for the VPC. To learn more, see `Security groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .
            :param subnet_ids: Provide one subnet ID for each Availability Zone that your domain uses. For example, you must specify three subnet IDs for a three-AZ domain. To learn more, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* . If you specify more than one subnet, you must also configure ``ZoneAwarenessEnabled`` and ``ZoneAwarenessConfig`` within `ClusterConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html>`_ , otherwise you'll see the error "You must specify exactly one subnet" during template creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-vpcoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                v_pCOptions_property = opensearchservice_mixins.CfnDomainPropsMixin.VPCOptionsProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e18dc4d9f2713c9c8546521fcd6a9320f079a8cf1f290710d0844921b49a8713)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of security group IDs that are associated with the VPC endpoints for the domain.

            If you don't provide a security group ID, OpenSearch Service uses the default security group for the VPC. To learn more, see `Security groups for your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-vpcoptions.html#cfn-opensearchservice-domain-vpcoptions-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Provide one subnet ID for each Availability Zone that your domain uses.

            For example, you must specify three subnet IDs for a three-AZ domain. To learn more, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* .

            If you specify more than one subnet, you must also configure ``ZoneAwarenessEnabled`` and ``ZoneAwarenessConfig`` within `ClusterConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-clusterconfig.html>`_ , otherwise you'll see the error "You must specify exactly one subnet" during template creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-vpcoptions.html#cfn-opensearchservice-domain-vpcoptions-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.WindowStartTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"hours": "hours", "minutes": "minutes"},
    )
    class WindowStartTimeProperty:
        def __init__(
            self,
            *,
            hours: typing.Optional[jsii.Number] = None,
            minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A custom start time for the off-peak window, in Coordinated Universal Time (UTC).

            The window length will always be 10 hours, so you can't specify an end time. For example, if you specify 11:00 P.M. UTC as a start time, the end time will automatically be set to 9:00 A.M.

            :param hours: The start hour of the window in Coordinated Universal Time (UTC), using 24-hour time. For example, 17 refers to 5:00 P.M. UTC. The minimum value is 0 and the maximum value is 23.
            :param minutes: The start minute of the window, in UTC. The minimum value is 0 and the maximum value is 59.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-windowstarttime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                window_start_time_property = opensearchservice_mixins.CfnDomainPropsMixin.WindowStartTimeProperty(
                    hours=123,
                    minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e59466bd757a08383112080852a88e9768cf0949bafff7cf20706a4104069f7c)
                check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
                check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hours is not None:
                self._values["hours"] = hours
            if minutes is not None:
                self._values["minutes"] = minutes

        @builtins.property
        def hours(self) -> typing.Optional[jsii.Number]:
            '''The start hour of the window in Coordinated Universal Time (UTC), using 24-hour time.

            For example, 17 refers to 5:00 P.M. UTC. The minimum value is 0 and the maximum value is 23.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-windowstarttime.html#cfn-opensearchservice-domain-windowstarttime-hours
            '''
            result = self._values.get("hours")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minutes(self) -> typing.Optional[jsii.Number]:
            '''The start minute of the window, in UTC.

            The minimum value is 0 and the maximum value is 59.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-windowstarttime.html#cfn-opensearchservice-domain-windowstarttime-minutes
            '''
            result = self._values.get("minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WindowStartTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opensearchservice.mixins.CfnDomainPropsMixin.ZoneAwarenessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"availability_zone_count": "availabilityZoneCount"},
    )
    class ZoneAwarenessConfigProperty:
        def __init__(
            self,
            *,
            availability_zone_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies zone awareness configuration options.

            Only use if ``ZoneAwarenessEnabled`` is ``true`` .

            :param availability_zone_count: If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use. Valid values are ``2`` and ``3`` . Default is 2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-zoneawarenessconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opensearchservice import mixins as opensearchservice_mixins
                
                zone_awareness_config_property = opensearchservice_mixins.CfnDomainPropsMixin.ZoneAwarenessConfigProperty(
                    availability_zone_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14972fae9ef3305ffe2f8232b8949c8e5cfd1fda07c0415979aab45a09b972e7)
                check_type(argname="argument availability_zone_count", value=availability_zone_count, expected_type=type_hints["availability_zone_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone_count is not None:
                self._values["availability_zone_count"] = availability_zone_count

        @builtins.property
        def availability_zone_count(self) -> typing.Optional[jsii.Number]:
            '''If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use.

            Valid values are ``2`` and ``3`` . Default is 2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchservice-domain-zoneawarenessconfig.html#cfn-opensearchservice-domain-zoneawarenessconfig-availabilityzonecount
            '''
            result = self._values.get("availability_zone_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZoneAwarenessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnDomainMixinProps",
    "CfnDomainPropsMixin",
]

publication.publish()

def _typecheckingstub__ca0c0e19ce192448cb10526c9f2c1d27f90d0211ab255020c5db596d5d31963b(
    *,
    app_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.AppConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    data_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.DataSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    endpoint: typing.Optional[builtins.str] = None,
    iam_identity_center_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.IamIdentityCenterOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d6396271250d64fe03967754ba80d242059cd4b549c0d06aad307895245d51(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd82ac716e1e30e6d239fcf0941239031546f01454351bede46da23f147227de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6264a2e45476bc1f95f5409599e4c07a8addea684b3a618cdcff4db2cef876f7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd33ad4e6542a1a283fa5c6ee9facb2aa1fb97be38183111ae00e3a702855a8(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22319b561da36a4b807aab7774ab06a65c96568fa0c53f08b5e81ba8ab166c9(
    *,
    data_source_arn: typing.Optional[builtins.str] = None,
    data_source_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be4891ef864731ea9b5f4a33576d6b515b6501c6d0116eb8c815efbf230cb8a(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iam_identity_center_instance_arn: typing.Optional[builtins.str] = None,
    iam_role_for_identity_center_application_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7094369dea89efb248c37dfd6b717935a084c92d05fb2407b5d4e6cfc6c17825(
    *,
    access_policies: typing.Any = None,
    advanced_options: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    advanced_security_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.AdvancedSecurityOptionsInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    aiml_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.AIMLOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.ClusterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cognito_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.CognitoOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_arn: typing.Optional[builtins.str] = None,
    domain_endpoint_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.DomainEndpointOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    ebs_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.EBSOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_at_rest_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.EncryptionAtRestOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    identity_center_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.IdentityCenterOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    log_publishing_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.LogPublishingOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    node_to_node_encryption_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.NodeToNodeEncryptionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    off_peak_window_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.OffPeakWindowOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    skip_shard_migration_wait: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    snapshot_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.SnapshotOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    software_update_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.SoftwareUpdateOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.VPCOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a795dc8e5dcfc936f281e31747952417209159c39f9fb6f086dcabc2f9bba81(
    props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b3e5e038a8da8aa2745470b06219c91be5d4d6dc15361d294a7c9a462965b2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d3332981a3f85ca9f12c7823542b76da02831ada2fd0cfda7dd2c5012e1b93(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b17a3584d7d0f7cf2d325cfd842a9a604146cc02c696283dee1dfdc1c18464ce(
    *,
    s3_vectors_engine: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.S3VectorsEngineProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd4d2449c04c98649e0d1e99a7bc6e62402889b14b06404d6d558b4e3007e73(
    *,
    anonymous_auth_disable_date: typing.Optional[builtins.str] = None,
    anonymous_auth_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iam_federation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.IAMFederationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    jwt_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.JWTOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    master_user_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.MasterUserOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    saml_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.SAMLOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2181dd2836f159ba83eced9e9a2d1a9d80fbf9d12512464e9e89c241880572(
    *,
    cold_storage_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.ColdStorageOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dedicated_master_count: typing.Optional[jsii.Number] = None,
    dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    dedicated_master_type: typing.Optional[builtins.str] = None,
    instance_count: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[builtins.str] = None,
    multi_az_with_standby_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    node_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.NodeOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    warm_count: typing.Optional[jsii.Number] = None,
    warm_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    warm_type: typing.Optional[builtins.str] = None,
    zone_awareness_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.ZoneAwarenessConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556ed60c56eebc7f90a7d78af2beb82db78156fab9572f844527a1d37f3308b2(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    identity_pool_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    user_pool_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea14dc72b46f2962d29ed059334b38198e7b83c6f4f66a4e80abe639d635a8ce(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5084d9b57b689a1f1e2383f05112ffe76a4377aa0ef4d73592b1e97af7f334f(
    *,
    custom_endpoint: typing.Optional[builtins.str] = None,
    custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
    custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enforce_https: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tls_security_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3228dc32e039695047c7abd04cda2dcf8fb484c8345735ad83d6b1caff155b(
    *,
    ebs_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e0589933c168502f95e87a8edad4d3e6dab4b9bf6cd368004d16e1dc70d2f1(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6604723555356dcf4b22bd42f92a582f3b05ceb624391a9b4b256074329f95f6(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    roles_key: typing.Optional[builtins.str] = None,
    subject_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c64cad3c316cf76166079ce7d960664d2c2d5eef17109c4b3c62d7a8c5140e8(
    *,
    enabled_api_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    identity_center_application_arn: typing.Optional[builtins.str] = None,
    identity_center_instance_arn: typing.Optional[builtins.str] = None,
    identity_store_id: typing.Optional[builtins.str] = None,
    roles_key: typing.Optional[builtins.str] = None,
    subject_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7057330927b477344be8652e6ba30cb5db16870f6f4e48c272309bbefc772fd4(
    *,
    entity_id: typing.Optional[builtins.str] = None,
    metadata_content: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0633a95f5bb7ff9a59cfd588de7bac2781e39ae33b3bfb3fcd4484eef16e2c68(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    public_key: typing.Optional[builtins.str] = None,
    roles_key: typing.Optional[builtins.str] = None,
    subject_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d4fe5877cff89da07c3c8ab32d084bc7e427e6f2e68c4b2ba59c92da29994b(
    *,
    cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5365d1cfa4025c0c9f55d823a49619240f0eaafe602c7e3552c0fe8dabf46c19(
    *,
    master_user_arn: typing.Optional[builtins.str] = None,
    master_user_name: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a4daed3a6a987d63e7c91baf7470d45c4f63f7ee9c6631f6dcf56dc05e88b7(
    *,
    count: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9f81450ca5d78140f2fa680582ca562a0b7152696b6c43602d379b7e9c82a3(
    *,
    node_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.NodeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    node_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692d5697243e5b96d58732c8188e155e13dc6a96539f0a3630e50493cd35152e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1232be18ea232c04deba54250bbbf35ebc8ba599699e16e7c89041376abff479(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    off_peak_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.OffPeakWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87038e503b824de24dbf538c314cbafa90f93343b666edc88f0cf40de3fd03d7(
    *,
    window_start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.WindowStartTimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85106beb499acc9f34b01dbbdd7632b429d7b5179071f4ebd68489e48b74898(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6f7318a214c627f1ae2cd81e3fc8e8535feb101f20d2ad70a35d7411d5f202(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    idp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.IdpProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    master_backend_role: typing.Optional[builtins.str] = None,
    master_user_name: typing.Optional[builtins.str] = None,
    roles_key: typing.Optional[builtins.str] = None,
    session_timeout_minutes: typing.Optional[jsii.Number] = None,
    subject_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6db4135e1c963952dc3ba55cd3250544a3ce94b0e157a7f478e9ec929902745(
    *,
    automated_update_date: typing.Optional[builtins.str] = None,
    cancellable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    current_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    new_version: typing.Optional[builtins.str] = None,
    optional_deployment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    update_available: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    update_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6984dc2647c174136f4df4de4c9c3537aefd8829966a23f99ef27b59ca7bf50(
    *,
    automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e6380093fca010ef5ca8f1ee9456de3e2c32e063c2f1c51c0654dbf7e6463c(
    *,
    auto_software_update_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18dc4d9f2713c9c8546521fcd6a9320f079a8cf1f290710d0844921b49a8713(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59466bd757a08383112080852a88e9768cf0949bafff7cf20706a4104069f7c(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14972fae9ef3305ffe2f8232b8949c8e5cfd1fda07c0415979aab45a09b972e7(
    *,
    availability_zone_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
