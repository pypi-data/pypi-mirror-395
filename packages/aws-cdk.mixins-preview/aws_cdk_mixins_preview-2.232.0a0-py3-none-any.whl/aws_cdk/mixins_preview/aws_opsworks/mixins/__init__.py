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
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnAppMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_source": "appSource",
        "attributes": "attributes",
        "data_sources": "dataSources",
        "description": "description",
        "domains": "domains",
        "enable_ssl": "enableSsl",
        "environment": "environment",
        "name": "name",
        "shortname": "shortname",
        "ssl_configuration": "sslConfiguration",
        "stack_id": "stackId",
        "type": "type",
    },
)
class CfnAppMixinProps:
    def __init__(
        self,
        *,
        app_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        data_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.DataSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_ssl: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        shortname: typing.Optional[builtins.str] = None,
        ssl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.SslConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stack_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAppPropsMixin.

        :param app_source: A ``Source`` object that specifies the app repository.
        :param attributes: One or more user-defined key/value pairs to be added to the stack attributes.
        :param data_sources: The app's data source.
        :param description: A description of the app.
        :param domains: The app virtual host settings, with multiple domains separated by commas. For example: ``'www.example.com, example.com'``
        :param enable_ssl: Whether to enable SSL for the app.
        :param environment: An array of ``EnvironmentVariable`` objects that specify environment variables to be associated with the app. After you deploy the app, these variables are defined on the associated app server instance. For more information, see `Environment Variables <https://docs.aws.amazon.com/opsworks/latest/userguide/workingapps-creating.html#workingapps-creating-environment>`_ . There is no specific limit on the number of environment variables. However, the size of the associated data structure - which includes the variables' names, values, and protected flag values - cannot exceed 20 KB. This limit should accommodate most if not all use cases. Exceeding it will cause an exception with the message, "Environment: is too large (maximum is 20KB)." .. epigraph:: If you have specified one or more environment variables, you cannot modify the stack's Chef version.
        :param name: The app name.
        :param shortname: The app's short name.
        :param ssl_configuration: An ``SslConfiguration`` object with the SSL configuration.
        :param stack_id: The stack ID.
        :param type: The app type. Each supported type is associated with a particular layer. For example, PHP applications are associated with a PHP layer. OpsWorks Stacks deploys an application to those instances that are members of the corresponding layer. If your app isn't one of the standard types, or you prefer to implement your own Deploy recipes, specify ``other`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
            
            cfn_app_mixin_props = opsworks_mixins.CfnAppMixinProps(
                app_source=opsworks_mixins.CfnAppPropsMixin.SourceProperty(
                    password="password",
                    revision="revision",
                    ssh_key="sshKey",
                    type="type",
                    url="url",
                    username="username"
                ),
                attributes={
                    "attributes_key": "attributes"
                },
                data_sources=[opsworks_mixins.CfnAppPropsMixin.DataSourceProperty(
                    arn="arn",
                    database_name="databaseName",
                    type="type"
                )],
                description="description",
                domains=["domains"],
                enable_ssl=False,
                environment=[opsworks_mixins.CfnAppPropsMixin.EnvironmentVariableProperty(
                    key="key",
                    secure=False,
                    value="value"
                )],
                name="name",
                shortname="shortname",
                ssl_configuration=opsworks_mixins.CfnAppPropsMixin.SslConfigurationProperty(
                    certificate="certificate",
                    chain="chain",
                    private_key="privateKey"
                ),
                stack_id="stackId",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a0e54bad443e9f37f3d08e982af92e4c0d4050f84813c7d8b0fa602bb082e0)
            check_type(argname="argument app_source", value=app_source, expected_type=type_hints["app_source"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument enable_ssl", value=enable_ssl, expected_type=type_hints["enable_ssl"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument shortname", value=shortname, expected_type=type_hints["shortname"])
            check_type(argname="argument ssl_configuration", value=ssl_configuration, expected_type=type_hints["ssl_configuration"])
            check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_source is not None:
            self._values["app_source"] = app_source
        if attributes is not None:
            self._values["attributes"] = attributes
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if description is not None:
            self._values["description"] = description
        if domains is not None:
            self._values["domains"] = domains
        if enable_ssl is not None:
            self._values["enable_ssl"] = enable_ssl
        if environment is not None:
            self._values["environment"] = environment
        if name is not None:
            self._values["name"] = name
        if shortname is not None:
            self._values["shortname"] = shortname
        if ssl_configuration is not None:
            self._values["ssl_configuration"] = ssl_configuration
        if stack_id is not None:
            self._values["stack_id"] = stack_id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def app_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.SourceProperty"]]:
        '''A ``Source`` object that specifies the app repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-appsource
        '''
        result = self._values.get("app_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.SourceProperty"]], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''One or more user-defined key/value pairs to be added to the stack attributes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def data_sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.DataSourceProperty"]]]]:
        '''The app's data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-datasources
        '''
        result = self._values.get("data_sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.DataSourceProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The app virtual host settings, with multiple domains separated by commas.

        For example: ``'www.example.com, example.com'``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-domains
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to enable SSL for the app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-enablessl
        '''
        result = self._values.get("enable_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.EnvironmentVariableProperty"]]]]:
        '''An array of ``EnvironmentVariable`` objects that specify environment variables to be associated with the app.

        After you deploy the app, these variables are defined on the associated app server instance. For more information, see `Environment Variables <https://docs.aws.amazon.com/opsworks/latest/userguide/workingapps-creating.html#workingapps-creating-environment>`_ .

        There is no specific limit on the number of environment variables. However, the size of the associated data structure - which includes the variables' names, values, and protected flag values - cannot exceed 20 KB. This limit should accommodate most if not all use cases. Exceeding it will cause an exception with the message, "Environment: is too large (maximum is 20KB)."
        .. epigraph::

           If you have specified one or more environment variables, you cannot modify the stack's Chef version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-environment
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.EnvironmentVariableProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The app name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shortname(self) -> typing.Optional[builtins.str]:
        '''The app's short name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-shortname
        '''
        result = self._values.get("shortname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.SslConfigurationProperty"]]:
        '''An ``SslConfiguration`` object with the SSL configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-sslconfiguration
        '''
        result = self._values.get("ssl_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.SslConfigurationProperty"]], result)

    @builtins.property
    def stack_id(self) -> typing.Optional[builtins.str]:
        '''The stack ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-stackid
        '''
        result = self._values.get("stack_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The app type.

        Each supported type is associated with a particular layer. For example, PHP applications are associated with a PHP layer. OpsWorks Stacks deploys an application to those instances that are members of the corresponding layer. If your app isn't one of the standard types, or you prefer to implement your own Deploy recipes, specify ``other`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAppPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnAppPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html
    :cloudformationResource: AWS::OpsWorks::App
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
        
        cfn_app_props_mixin = opsworks_mixins.CfnAppPropsMixin(opsworks_mixins.CfnAppMixinProps(
            app_source=opsworks_mixins.CfnAppPropsMixin.SourceProperty(
                password="password",
                revision="revision",
                ssh_key="sshKey",
                type="type",
                url="url",
                username="username"
            ),
            attributes={
                "attributes_key": "attributes"
            },
            data_sources=[opsworks_mixins.CfnAppPropsMixin.DataSourceProperty(
                arn="arn",
                database_name="databaseName",
                type="type"
            )],
            description="description",
            domains=["domains"],
            enable_ssl=False,
            environment=[opsworks_mixins.CfnAppPropsMixin.EnvironmentVariableProperty(
                key="key",
                secure=False,
                value="value"
            )],
            name="name",
            shortname="shortname",
            ssl_configuration=opsworks_mixins.CfnAppPropsMixin.SslConfigurationProperty(
                certificate="certificate",
                chain="chain",
                private_key="privateKey"
            ),
            stack_id="stackId",
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAppMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpsWorks::App``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef527aeec828773bf2844eb14201792c89b00d89543dffca0c8f1acf54e9e50d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f0f1adf73b36a3c5127876169face74ec978842575ec94ce6ec9f1d1989c9b4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb002427b5e037fdaec6e2579d27e091e3b5fa8ff66a6433e10e8a88141976d3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAppMixinProps:
        return typing.cast(CfnAppMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnAppPropsMixin.DataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "database_name": "databaseName", "type": "type"},
    )
    class DataSourceProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param arn: The data source's ARN.
            :param database_name: The database name.
            :param type: The data source's type, ``AutoSelectOpsworksMysqlInstance`` , ``OpsworksMysqlInstance`` , ``RdsDbInstance`` , or ``None`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                data_source_property = opsworks_mixins.CfnAppPropsMixin.DataSourceProperty(
                    arn="arn",
                    database_name="databaseName",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60e5935aff8c920a1158ccba84220c90337b91c6f789cfb7c171eae4dac5ec47)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The data source's ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The database name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The data source's type, ``AutoSelectOpsworksMysqlInstance`` , ``OpsworksMysqlInstance`` , ``RdsDbInstance`` , or ``None`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-type
            '''
            result = self._values.get("type")
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
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnAppPropsMixin.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "secure": "secure", "value": "value"},
    )
    class EnvironmentVariableProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            secure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key: (Required) The environment variable's name, which can consist of up to 64 characters and must be specified. The name can contain upper- and lowercase letters, numbers, and underscores (_), but it must start with a letter or underscore.
            :param secure: (Optional) Whether the variable's value is returned by the ``DescribeApps`` action. To hide an environment variable's value, set ``Secure`` to ``true`` . ``DescribeApps`` returns ``*****FILTERED*****`` instead of the actual value. The default value for ``Secure`` is ``false`` .
            :param value: (Optional) The environment variable's value, which can be left empty. If you specify a value, it can contain up to 256 characters, which must all be printable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                environment_variable_property = opsworks_mixins.CfnAppPropsMixin.EnvironmentVariableProperty(
                    key="key",
                    secure=False,
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00ff39d76264be19370d9eb098819836270ad4aaa3fbecc859a952b16894dae0)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument secure", value=secure, expected_type=type_hints["secure"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if secure is not None:
                self._values["secure"] = secure
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''(Required) The environment variable's name, which can consist of up to 64 characters and must be specified.

            The name can contain upper- and lowercase letters, numbers, and underscores (_), but it must start with a letter or underscore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environmentvariable.html#cfn-opsworks-app-environmentvariable-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secure(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''(Optional) Whether the variable's value is returned by the ``DescribeApps`` action.

            To hide an environment variable's value, set ``Secure`` to ``true`` . ``DescribeApps`` returns ``*****FILTERED*****`` instead of the actual value. The default value for ``Secure`` is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environmentvariable.html#cfn-opsworks-app-environmentvariable-secure
            '''
            result = self._values.get("secure")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''(Optional) The environment variable's value, which can be left empty.

            If you specify a value, it can contain up to 256 characters, which must all be printable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environmentvariable.html#cfn-opsworks-app-environmentvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnAppPropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "revision": "revision",
            "ssh_key": "sshKey",
            "type": "type",
            "url": "url",
            "username": "username",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            revision: typing.Optional[builtins.str] = None,
            ssh_key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param password: When included in a request, the parameter depends on the repository type. - For Amazon S3 bundles, set ``Password`` to the appropriate IAM secret access key. - For HTTP bundles and Subversion repositories, set ``Password`` to the password. For more information on how to safely handle IAM credentials, see ` <https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html>`_ . In responses, OpsWorks Stacks returns ``*****FILTERED*****`` instead of the actual value.
            :param revision: The application's version. OpsWorks Stacks enables you to easily deploy new versions of an application. One of the simplest approaches is to have branches or revisions in your repository that represent different versions that can potentially be deployed.
            :param ssh_key: In requests, the repository's SSH key. In responses, OpsWorks Stacks returns ``*****FILTERED*****`` instead of the actual value.
            :param type: The repository type.
            :param url: The source URL. The following is an example of an Amazon S3 source URL: ``https://s3.amazonaws.com/opsworks-demo-bucket/opsworks_cookbook_demo.tar.gz`` .
            :param username: This parameter depends on the repository type. - For Amazon S3 bundles, set ``Username`` to the appropriate IAM access key ID. - For HTTP bundles, Git repositories, and Subversion repositories, set ``Username`` to the user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                source_property = opsworks_mixins.CfnAppPropsMixin.SourceProperty(
                    password="password",
                    revision="revision",
                    ssh_key="sshKey",
                    type="type",
                    url="url",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1196cf9927815a8c26734d83cadcd752571097a31346dbad2f0ad146ddb41e7e)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
                check_type(argname="argument ssh_key", value=ssh_key, expected_type=type_hints["ssh_key"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if revision is not None:
                self._values["revision"] = revision
            if ssh_key is not None:
                self._values["ssh_key"] = ssh_key
            if type is not None:
                self._values["type"] = type
            if url is not None:
                self._values["url"] = url
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''When included in a request, the parameter depends on the repository type.

            - For Amazon S3 bundles, set ``Password`` to the appropriate IAM secret access key.
            - For HTTP bundles and Subversion repositories, set ``Password`` to the password.

            For more information on how to safely handle IAM credentials, see ` <https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html>`_ .

            In responses, OpsWorks Stacks returns ``*****FILTERED*****`` instead of the actual value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-source.html#cfn-opsworks-app-source-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def revision(self) -> typing.Optional[builtins.str]:
            '''The application's version.

            OpsWorks Stacks enables you to easily deploy new versions of an application. One of the simplest approaches is to have branches or revisions in your repository that represent different versions that can potentially be deployed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-source.html#cfn-opsworks-app-source-revision
            '''
            result = self._values.get("revision")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssh_key(self) -> typing.Optional[builtins.str]:
            '''In requests, the repository's SSH key.

            In responses, OpsWorks Stacks returns ``*****FILTERED*****`` instead of the actual value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-source.html#cfn-opsworks-app-source-sshkey
            '''
            result = self._values.get("ssh_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The repository type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-source.html#cfn-opsworks-app-source-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The source URL.

            The following is an example of an Amazon S3 source URL: ``https://s3.amazonaws.com/opsworks-demo-bucket/opsworks_cookbook_demo.tar.gz`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-source.html#cfn-opsworks-app-source-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''This parameter depends on the repository type.

            - For Amazon S3 bundles, set ``Username`` to the appropriate IAM access key ID.
            - For HTTP bundles, Git repositories, and Subversion repositories, set ``Username`` to the user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-source.html#cfn-opsworks-app-source-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnAppPropsMixin.SslConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate": "certificate",
            "chain": "chain",
            "private_key": "privateKey",
        },
    )
    class SslConfigurationProperty:
        def __init__(
            self,
            *,
            certificate: typing.Optional[builtins.str] = None,
            chain: typing.Optional[builtins.str] = None,
            private_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param certificate: The contents of the certificate's domain.crt file.
            :param chain: Optional. Can be used to specify an intermediate certificate authority key or client authentication.
            :param private_key: The private key; the contents of the certificate's domain.kex file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                ssl_configuration_property = opsworks_mixins.CfnAppPropsMixin.SslConfigurationProperty(
                    certificate="certificate",
                    chain="chain",
                    private_key="privateKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__211a775322b0e21cbdfc24be0aad50b503466c9c50ab97ab292d310c6334d360)
                check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
                check_type(argname="argument chain", value=chain, expected_type=type_hints["chain"])
                check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate is not None:
                self._values["certificate"] = certificate
            if chain is not None:
                self._values["chain"] = chain
            if private_key is not None:
                self._values["private_key"] = private_key

        @builtins.property
        def certificate(self) -> typing.Optional[builtins.str]:
            '''The contents of the certificate's domain.crt file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfiguration-certificate
            '''
            result = self._values.get("certificate")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def chain(self) -> typing.Optional[builtins.str]:
            '''Optional.

            Can be used to specify an intermediate certificate authority key or client authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfiguration-chain
            '''
            result = self._values.get("chain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_key(self) -> typing.Optional[builtins.str]:
            '''The private key;

            the contents of the certificate's domain.kex file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfiguration-privatekey
            '''
            result = self._values.get("private_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SslConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnElasticLoadBalancerAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "elastic_load_balancer_name": "elasticLoadBalancerName",
        "layer_id": "layerId",
    },
)
class CfnElasticLoadBalancerAttachmentMixinProps:
    def __init__(
        self,
        *,
        elastic_load_balancer_name: typing.Optional[builtins.str] = None,
        layer_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnElasticLoadBalancerAttachmentPropsMixin.

        :param elastic_load_balancer_name: The Elastic Load Balancing instance name.
        :param layer_id: The OpsWorks layer ID to which the Elastic Load Balancing load balancer is attached.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elasticloadbalancerattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
            
            cfn_elastic_load_balancer_attachment_mixin_props = opsworks_mixins.CfnElasticLoadBalancerAttachmentMixinProps(
                elastic_load_balancer_name="elasticLoadBalancerName",
                layer_id="layerId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e188ad118bf61c05eb87cecf79cd3fe0a7d31ccf5f5ee90cab14554732a17bc)
            check_type(argname="argument elastic_load_balancer_name", value=elastic_load_balancer_name, expected_type=type_hints["elastic_load_balancer_name"])
            check_type(argname="argument layer_id", value=layer_id, expected_type=type_hints["layer_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if elastic_load_balancer_name is not None:
            self._values["elastic_load_balancer_name"] = elastic_load_balancer_name
        if layer_id is not None:
            self._values["layer_id"] = layer_id

    @builtins.property
    def elastic_load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''The Elastic Load Balancing instance name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elasticloadbalancerattachment.html#cfn-opsworks-elasticloadbalancerattachment-elasticloadbalancername
        '''
        result = self._values.get("elastic_load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_id(self) -> typing.Optional[builtins.str]:
        '''The OpsWorks layer ID to which the Elastic Load Balancing load balancer is attached.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elasticloadbalancerattachment.html#cfn-opsworks-elasticloadbalancerattachment-layerid
        '''
        result = self._values.get("layer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnElasticLoadBalancerAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnElasticLoadBalancerAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnElasticLoadBalancerAttachmentPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elasticloadbalancerattachment.html
    :cloudformationResource: AWS::OpsWorks::ElasticLoadBalancerAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
        
        cfn_elastic_load_balancer_attachment_props_mixin = opsworks_mixins.CfnElasticLoadBalancerAttachmentPropsMixin(opsworks_mixins.CfnElasticLoadBalancerAttachmentMixinProps(
            elastic_load_balancer_name="elasticLoadBalancerName",
            layer_id="layerId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnElasticLoadBalancerAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa5e71c391d8e35dac5e90f70aa3fddf53f77e55ef8f4b38010fa6d1d04ff3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebc88a7e350838912534a914f1c8c336096e15f25ee8ab83c3ee1c740a33d71e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__561356eea75fcb54a9ec66ae5ff6a5ec55325ebd149f0d903e7fab97218f08b1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnElasticLoadBalancerAttachmentMixinProps:
        return typing.cast(CfnElasticLoadBalancerAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_version": "agentVersion",
        "ami_id": "amiId",
        "architecture": "architecture",
        "auto_scaling_type": "autoScalingType",
        "availability_zone": "availabilityZone",
        "block_device_mappings": "blockDeviceMappings",
        "ebs_optimized": "ebsOptimized",
        "elastic_ips": "elasticIps",
        "hostname": "hostname",
        "install_updates_on_boot": "installUpdatesOnBoot",
        "instance_type": "instanceType",
        "layer_ids": "layerIds",
        "os": "os",
        "root_device_type": "rootDeviceType",
        "ssh_key_name": "sshKeyName",
        "stack_id": "stackId",
        "subnet_id": "subnetId",
        "tenancy": "tenancy",
        "time_based_auto_scaling": "timeBasedAutoScaling",
        "virtualization_type": "virtualizationType",
        "volumes": "volumes",
    },
)
class CfnInstanceMixinProps:
    def __init__(
        self,
        *,
        agent_version: typing.Optional[builtins.str] = None,
        ami_id: typing.Optional[builtins.str] = None,
        architecture: typing.Optional[builtins.str] = None,
        auto_scaling_type: typing.Optional[builtins.str] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.BlockDeviceMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        elastic_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
        hostname: typing.Optional[builtins.str] = None,
        install_updates_on_boot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        layer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        os: typing.Optional[builtins.str] = None,
        root_device_type: typing.Optional[builtins.str] = None,
        ssh_key_name: typing.Optional[builtins.str] = None,
        stack_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tenancy: typing.Optional[builtins.str] = None,
        time_based_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.TimeBasedAutoScalingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        virtualization_type: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnInstancePropsMixin.

        :param agent_version: The default OpsWorks Stacks agent version. You have the following options:. - ``INHERIT`` - Use the stack's default agent version setting. - *version_number* - Use the specified agent version. This value overrides the stack's default setting. To update the agent version, edit the instance configuration and specify a new version. OpsWorks Stacks installs that version on the instance. The default setting is ``INHERIT`` . To specify an agent version, you must use the complete version number, not the abbreviated number shown on the console. For a list of available agent version numbers, call ``DescribeAgentVersions`` . AgentVersion cannot be set to Chef 12.2.
        :param ami_id: A custom AMI ID to be used to create the instance. The AMI should be based on one of the supported operating systems. For more information, see `Using Custom AMIs <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-custom-ami.html>`_ . .. epigraph:: If you specify a custom AMI, you must set ``Os`` to ``Custom`` .
        :param architecture: The instance architecture. The default option is ``x86_64`` . Instance types do not necessarily support both architectures. For a list of the architectures that are supported by the different instance types, see `Instance Families and Types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html>`_ .
        :param auto_scaling_type: For load-based or time-based instances, the type. Windows stacks can use only time-based instances.
        :param availability_zone: The Availability Zone of the OpsWorks instance, such as ``us-east-2a`` .
        :param block_device_mappings: An array of ``BlockDeviceMapping`` objects that specify the instance's block devices. For more information, see `Block Device Mapping <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html>`_ . Note that block device mappings are not supported for custom AMIs.
        :param ebs_optimized: Whether to create an Amazon EBS-optimized instance.
        :param elastic_ips: A list of Elastic IP addresses to associate with the instance.
        :param hostname: The instance host name. The following are character limits for instance host names. - Linux-based instances: 63 characters - Windows-based instances: 15 characters
        :param install_updates_on_boot: Whether to install operating system and package updates when the instance boots. The default value is ``true`` . To control when updates are installed, set this value to ``false`` . You must then update your instances manually by using ``CreateDeployment`` to run the ``update_dependencies`` stack command or by manually running ``yum`` (Amazon Linux) or ``apt-get`` (Ubuntu) on the instances. .. epigraph:: We strongly recommend using the default value of ``true`` to ensure that your instances have the latest security updates.
        :param instance_type: The instance type, such as ``t2.micro`` . For a list of supported instance types, open the stack in the console, choose *Instances* , and choose *+ Instance* . The *Size* list contains the currently supported types. For more information, see `Instance Families and Types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html>`_ . The parameter values that you use to specify the various types are in the *API Name* column of the *Available Instance Types* table.
        :param layer_ids: An array that contains the instance's layer IDs.
        :param os: The instance's operating system, which must be set to one of the following. - A supported Linux operating system: An Amazon Linux version, such as ``Amazon Linux 2`` , ``Amazon Linux 2018.03`` , ``Amazon Linux 2017.09`` , ``Amazon Linux 2017.03`` , ``Amazon Linux 2016.09`` , ``Amazon Linux 2016.03`` , ``Amazon Linux 2015.09`` , or ``Amazon Linux 2015.03`` . - A supported Ubuntu operating system, such as ``Ubuntu 18.04 LTS`` , ``Ubuntu 16.04 LTS`` , ``Ubuntu 14.04 LTS`` , or ``Ubuntu 12.04 LTS`` . - ``CentOS Linux 7`` - ``Red Hat Enterprise Linux 7`` - A supported Windows operating system, such as ``Microsoft Windows Server 2012 R2 Base`` , ``Microsoft Windows Server 2012 R2 with SQL Server Express`` , ``Microsoft Windows Server 2012 R2 with SQL Server Standard`` , or ``Microsoft Windows Server 2012 R2 with SQL Server Web`` . - A custom AMI: ``Custom`` . Not all operating systems are supported with all versions of Chef. For more information about the supported operating systems, see `OpsWorks Stacks Operating Systems <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-os.html>`_ . The default option is the current Amazon Linux version. If you set this parameter to ``Custom`` , you must use the ``CreateInstance`` action's AmiId parameter to specify the custom AMI that you want to use. Block device mappings are not supported if the value is ``Custom`` . For more information about how to use custom AMIs with OpsWorks Stacks, see `Using Custom AMIs <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-custom-ami.html>`_ .
        :param root_device_type: The instance root device type. For more information, see `Storage for the Root Device <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device>`_ .
        :param ssh_key_name: The instance's Amazon EC2 key-pair name.
        :param stack_id: The stack ID.
        :param subnet_id: The ID of the instance's subnet. If the stack is running in a VPC, you can use this parameter to override the stack's default subnet ID value and direct OpsWorks Stacks to launch the instance in a different subnet.
        :param tenancy: The instance's tenancy option. The default option is no tenancy, or if the instance is running in a VPC, inherit tenancy settings from the VPC. The following are valid values for this parameter: ``dedicated`` , ``default`` , or ``host`` . Because there are costs associated with changes in tenancy options, we recommend that you research tenancy options before choosing them for your instances. For more information about dedicated hosts, see `Dedicated Hosts Overview <https://docs.aws.amazon.com/ec2/dedicated-hosts/>`_ and `Amazon EC2 Dedicated Hosts <https://docs.aws.amazon.com/ec2/dedicated-hosts/>`_ . For more information about dedicated instances, see `Dedicated Instances <https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/dedicated-instance.html>`_ and `Amazon EC2 Dedicated Instances <https://docs.aws.amazon.com/ec2/purchasing-options/dedicated-instances/>`_ .
        :param time_based_auto_scaling: The time-based scaling configuration for the instance.
        :param virtualization_type: The instance's virtualization type, ``paravirtual`` or ``hvm`` .
        :param volumes: A list of OpsWorks volume IDs to associate with the instance. For more information, see ```AWS::OpsWorks::Volume`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
            
            cfn_instance_mixin_props = opsworks_mixins.CfnInstanceMixinProps(
                agent_version="agentVersion",
                ami_id="amiId",
                architecture="architecture",
                auto_scaling_type="autoScalingType",
                availability_zone="availabilityZone",
                block_device_mappings=[opsworks_mixins.CfnInstancePropsMixin.BlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=opsworks_mixins.CfnInstancePropsMixin.EbsBlockDeviceProperty(
                        delete_on_termination=False,
                        iops=123,
                        snapshot_id="snapshotId",
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device="noDevice",
                    virtual_name="virtualName"
                )],
                ebs_optimized=False,
                elastic_ips=["elasticIps"],
                hostname="hostname",
                install_updates_on_boot=False,
                instance_type="instanceType",
                layer_ids=["layerIds"],
                os="os",
                root_device_type="rootDeviceType",
                ssh_key_name="sshKeyName",
                stack_id="stackId",
                subnet_id="subnetId",
                tenancy="tenancy",
                time_based_auto_scaling=opsworks_mixins.CfnInstancePropsMixin.TimeBasedAutoScalingProperty(
                    friday={
                        "friday_key": "friday"
                    },
                    monday={
                        "monday_key": "monday"
                    },
                    saturday={
                        "saturday_key": "saturday"
                    },
                    sunday={
                        "sunday_key": "sunday"
                    },
                    thursday={
                        "thursday_key": "thursday"
                    },
                    tuesday={
                        "tuesday_key": "tuesday"
                    },
                    wednesday={
                        "wednesday_key": "wednesday"
                    }
                ),
                virtualization_type="virtualizationType",
                volumes=["volumes"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a24386e63afbcac332e48fea6ab9d26700a5057ab8ec49cdec0a11b14af693)
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument ami_id", value=ami_id, expected_type=type_hints["ami_id"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument auto_scaling_type", value=auto_scaling_type, expected_type=type_hints["auto_scaling_type"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
            check_type(argname="argument ebs_optimized", value=ebs_optimized, expected_type=type_hints["ebs_optimized"])
            check_type(argname="argument elastic_ips", value=elastic_ips, expected_type=type_hints["elastic_ips"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument install_updates_on_boot", value=install_updates_on_boot, expected_type=type_hints["install_updates_on_boot"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument layer_ids", value=layer_ids, expected_type=type_hints["layer_ids"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument root_device_type", value=root_device_type, expected_type=type_hints["root_device_type"])
            check_type(argname="argument ssh_key_name", value=ssh_key_name, expected_type=type_hints["ssh_key_name"])
            check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
            check_type(argname="argument time_based_auto_scaling", value=time_based_auto_scaling, expected_type=type_hints["time_based_auto_scaling"])
            check_type(argname="argument virtualization_type", value=virtualization_type, expected_type=type_hints["virtualization_type"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if ami_id is not None:
            self._values["ami_id"] = ami_id
        if architecture is not None:
            self._values["architecture"] = architecture
        if auto_scaling_type is not None:
            self._values["auto_scaling_type"] = auto_scaling_type
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if ebs_optimized is not None:
            self._values["ebs_optimized"] = ebs_optimized
        if elastic_ips is not None:
            self._values["elastic_ips"] = elastic_ips
        if hostname is not None:
            self._values["hostname"] = hostname
        if install_updates_on_boot is not None:
            self._values["install_updates_on_boot"] = install_updates_on_boot
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if layer_ids is not None:
            self._values["layer_ids"] = layer_ids
        if os is not None:
            self._values["os"] = os
        if root_device_type is not None:
            self._values["root_device_type"] = root_device_type
        if ssh_key_name is not None:
            self._values["ssh_key_name"] = ssh_key_name
        if stack_id is not None:
            self._values["stack_id"] = stack_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tenancy is not None:
            self._values["tenancy"] = tenancy
        if time_based_auto_scaling is not None:
            self._values["time_based_auto_scaling"] = time_based_auto_scaling
        if virtualization_type is not None:
            self._values["virtualization_type"] = virtualization_type
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        '''The default OpsWorks Stacks agent version. You have the following options:.

        - ``INHERIT`` - Use the stack's default agent version setting.
        - *version_number* - Use the specified agent version. This value overrides the stack's default setting. To update the agent version, edit the instance configuration and specify a new version. OpsWorks Stacks installs that version on the instance.

        The default setting is ``INHERIT`` . To specify an agent version, you must use the complete version number, not the abbreviated number shown on the console. For a list of available agent version numbers, call ``DescribeAgentVersions`` . AgentVersion cannot be set to Chef 12.2.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-agentversion
        '''
        result = self._values.get("agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ami_id(self) -> typing.Optional[builtins.str]:
        '''A custom AMI ID to be used to create the instance.

        The AMI should be based on one of the supported operating systems. For more information, see `Using Custom AMIs <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-custom-ami.html>`_ .
        .. epigraph::

           If you specify a custom AMI, you must set ``Os`` to ``Custom`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-amiid
        '''
        result = self._values.get("ami_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''The instance architecture.

        The default option is ``x86_64`` . Instance types do not necessarily support both architectures. For a list of the architectures that are supported by the different instance types, see `Instance Families and Types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-architecture
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_scaling_type(self) -> typing.Optional[builtins.str]:
        '''For load-based or time-based instances, the type.

        Windows stacks can use only time-based instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-autoscalingtype
        '''
        result = self._values.get("auto_scaling_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone of the OpsWorks instance, such as ``us-east-2a`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.BlockDeviceMappingProperty"]]]]:
        '''An array of ``BlockDeviceMapping`` objects that specify the instance's block devices.

        For more information, see `Block Device Mapping <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html>`_ . Note that block device mappings are not supported for custom AMIs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-blockdevicemappings
        '''
        result = self._values.get("block_device_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.BlockDeviceMappingProperty"]]]], result)

    @builtins.property
    def ebs_optimized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to create an Amazon EBS-optimized instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-ebsoptimized
        '''
        result = self._values.get("ebs_optimized")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def elastic_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Elastic IP addresses to associate with the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-elasticips
        '''
        result = self._values.get("elastic_ips")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''The instance host name. The following are character limits for instance host names.

        - Linux-based instances: 63 characters
        - Windows-based instances: 15 characters

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-hostname
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_updates_on_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to install operating system and package updates when the instance boots.

        The default value is ``true`` . To control when updates are installed, set this value to ``false`` . You must then update your instances manually by using ``CreateDeployment`` to run the ``update_dependencies`` stack command or by manually running ``yum`` (Amazon Linux) or ``apt-get`` (Ubuntu) on the instances.
        .. epigraph::

           We strongly recommend using the default value of ``true`` to ensure that your instances have the latest security updates.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-installupdatesonboot
        '''
        result = self._values.get("install_updates_on_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''The instance type, such as ``t2.micro`` . For a list of supported instance types, open the stack in the console, choose *Instances* , and choose *+ Instance* . The *Size* list contains the currently supported types. For more information, see `Instance Families and Types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html>`_ . The parameter values that you use to specify the various types are in the *API Name* column of the *Available Instance Types* table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-instancetype
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array that contains the instance's layer IDs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-layerids
        '''
        result = self._values.get("layer_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os(self) -> typing.Optional[builtins.str]:
        '''The instance's operating system, which must be set to one of the following.

        - A supported Linux operating system: An Amazon Linux version, such as ``Amazon Linux 2`` , ``Amazon Linux 2018.03`` , ``Amazon Linux 2017.09`` , ``Amazon Linux 2017.03`` , ``Amazon Linux 2016.09`` , ``Amazon Linux 2016.03`` , ``Amazon Linux 2015.09`` , or ``Amazon Linux 2015.03`` .
        - A supported Ubuntu operating system, such as ``Ubuntu 18.04 LTS`` , ``Ubuntu 16.04 LTS`` , ``Ubuntu 14.04 LTS`` , or ``Ubuntu 12.04 LTS`` .
        - ``CentOS Linux 7``
        - ``Red Hat Enterprise Linux 7``
        - A supported Windows operating system, such as ``Microsoft Windows Server 2012 R2 Base`` , ``Microsoft Windows Server 2012 R2 with SQL Server Express`` , ``Microsoft Windows Server 2012 R2 with SQL Server Standard`` , or ``Microsoft Windows Server 2012 R2 with SQL Server Web`` .
        - A custom AMI: ``Custom`` .

        Not all operating systems are supported with all versions of Chef. For more information about the supported operating systems, see `OpsWorks Stacks Operating Systems <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-os.html>`_ .

        The default option is the current Amazon Linux version. If you set this parameter to ``Custom`` , you must use the ``CreateInstance`` action's AmiId parameter to specify the custom AMI that you want to use. Block device mappings are not supported if the value is ``Custom`` . For more information about how to use custom AMIs with OpsWorks Stacks, see `Using Custom AMIs <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-custom-ami.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-os
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_device_type(self) -> typing.Optional[builtins.str]:
        '''The instance root device type.

        For more information, see `Storage for the Root Device <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-rootdevicetype
        '''
        result = self._values.get("root_device_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_key_name(self) -> typing.Optional[builtins.str]:
        '''The instance's Amazon EC2 key-pair name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-sshkeyname
        '''
        result = self._values.get("ssh_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_id(self) -> typing.Optional[builtins.str]:
        '''The stack ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-stackid
        '''
        result = self._values.get("stack_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the instance's subnet.

        If the stack is running in a VPC, you can use this parameter to override the stack's default subnet ID value and direct OpsWorks Stacks to launch the instance in a different subnet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-subnetid
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''The instance's tenancy option.

        The default option is no tenancy, or if the instance is running in a VPC, inherit tenancy settings from the VPC. The following are valid values for this parameter: ``dedicated`` , ``default`` , or ``host`` . Because there are costs associated with changes in tenancy options, we recommend that you research tenancy options before choosing them for your instances. For more information about dedicated hosts, see `Dedicated Hosts Overview <https://docs.aws.amazon.com/ec2/dedicated-hosts/>`_ and `Amazon EC2 Dedicated Hosts <https://docs.aws.amazon.com/ec2/dedicated-hosts/>`_ . For more information about dedicated instances, see `Dedicated Instances <https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/dedicated-instance.html>`_ and `Amazon EC2 Dedicated Instances <https://docs.aws.amazon.com/ec2/purchasing-options/dedicated-instances/>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-tenancy
        '''
        result = self._values.get("tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_based_auto_scaling(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.TimeBasedAutoScalingProperty"]]:
        '''The time-based scaling configuration for the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-timebasedautoscaling
        '''
        result = self._values.get("time_based_auto_scaling")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.TimeBasedAutoScalingProperty"]], result)

    @builtins.property
    def virtualization_type(self) -> typing.Optional[builtins.str]:
        '''The instance's virtualization type, ``paravirtual`` or ``hvm`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-virtualizationtype
        '''
        result = self._values.get("virtualization_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of OpsWorks volume IDs to associate with the instance.

        For more information, see ```AWS::OpsWorks::Volume`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-volumes
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnInstancePropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html
    :cloudformationResource: AWS::OpsWorks::Instance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
        
        cfn_instance_props_mixin = opsworks_mixins.CfnInstancePropsMixin(opsworks_mixins.CfnInstanceMixinProps(
            agent_version="agentVersion",
            ami_id="amiId",
            architecture="architecture",
            auto_scaling_type="autoScalingType",
            availability_zone="availabilityZone",
            block_device_mappings=[opsworks_mixins.CfnInstancePropsMixin.BlockDeviceMappingProperty(
                device_name="deviceName",
                ebs=opsworks_mixins.CfnInstancePropsMixin.EbsBlockDeviceProperty(
                    delete_on_termination=False,
                    iops=123,
                    snapshot_id="snapshotId",
                    volume_size=123,
                    volume_type="volumeType"
                ),
                no_device="noDevice",
                virtual_name="virtualName"
            )],
            ebs_optimized=False,
            elastic_ips=["elasticIps"],
            hostname="hostname",
            install_updates_on_boot=False,
            instance_type="instanceType",
            layer_ids=["layerIds"],
            os="os",
            root_device_type="rootDeviceType",
            ssh_key_name="sshKeyName",
            stack_id="stackId",
            subnet_id="subnetId",
            tenancy="tenancy",
            time_based_auto_scaling=opsworks_mixins.CfnInstancePropsMixin.TimeBasedAutoScalingProperty(
                friday={
                    "friday_key": "friday"
                },
                monday={
                    "monday_key": "monday"
                },
                saturday={
                    "saturday_key": "saturday"
                },
                sunday={
                    "sunday_key": "sunday"
                },
                thursday={
                    "thursday_key": "thursday"
                },
                tuesday={
                    "tuesday_key": "tuesday"
                },
                wednesday={
                    "wednesday_key": "wednesday"
                }
            ),
            virtualization_type="virtualizationType",
            volumes=["volumes"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpsWorks::Instance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647b45ee490b1a37f9f9ce98867161533c5dfe2afe10730970d653004d18674a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c629249eca5a64a8cc473128268d460a7ad55b1c410417785be6b5ada2ff84b8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8c689083be869abc5ffddc3fc42bc57926f98cce9b42972a92748533ed8304)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceMixinProps:
        return typing.cast(CfnInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnInstancePropsMixin.BlockDeviceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "device_name": "deviceName",
            "ebs": "ebs",
            "no_device": "noDevice",
            "virtual_name": "virtualName",
        },
    )
    class BlockDeviceMappingProperty:
        def __init__(
            self,
            *,
            device_name: typing.Optional[builtins.str] = None,
            ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.EbsBlockDeviceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            no_device: typing.Optional[builtins.str] = None,
            virtual_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param device_name: The device name that is exposed to the instance, such as ``/dev/sdh`` . For the root device, you can use the explicit device name or you can set this parameter to ``ROOT_DEVICE`` and OpsWorks Stacks will provide the correct device name.
            :param ebs: An ``EBSBlockDevice`` that defines how to configure an Amazon EBS volume when the instance is launched. You can specify either the ``VirtualName`` or ``Ebs`` , but not both.
            :param no_device: Suppresses the specified device included in the AMI's block device mapping.
            :param virtual_name: The virtual device name. For more information, see `BlockDeviceMapping <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_BlockDeviceMapping.html>`_ . You can specify either the ``VirtualName`` or ``Ebs`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                block_device_mapping_property = opsworks_mixins.CfnInstancePropsMixin.BlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=opsworks_mixins.CfnInstancePropsMixin.EbsBlockDeviceProperty(
                        delete_on_termination=False,
                        iops=123,
                        snapshot_id="snapshotId",
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device="noDevice",
                    virtual_name="virtualName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fba80c5e650f27c22f883eed40dcd1d5c0c9b9f3f95b07cf5554645570bcaa76)
                check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
                check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
                check_type(argname="argument no_device", value=no_device, expected_type=type_hints["no_device"])
                check_type(argname="argument virtual_name", value=virtual_name, expected_type=type_hints["virtual_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if device_name is not None:
                self._values["device_name"] = device_name
            if ebs is not None:
                self._values["ebs"] = ebs
            if no_device is not None:
                self._values["no_device"] = no_device
            if virtual_name is not None:
                self._values["virtual_name"] = virtual_name

        @builtins.property
        def device_name(self) -> typing.Optional[builtins.str]:
            '''The device name that is exposed to the instance, such as ``/dev/sdh`` .

            For the root device, you can use the explicit device name or you can set this parameter to ``ROOT_DEVICE`` and OpsWorks Stacks will provide the correct device name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-devicename
            '''
            result = self._values.get("device_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ebs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.EbsBlockDeviceProperty"]]:
            '''An ``EBSBlockDevice`` that defines how to configure an Amazon EBS volume when the instance is launched.

            You can specify either the ``VirtualName`` or ``Ebs`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-ebs
            '''
            result = self._values.get("ebs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.EbsBlockDeviceProperty"]], result)

        @builtins.property
        def no_device(self) -> typing.Optional[builtins.str]:
            '''Suppresses the specified device included in the AMI's block device mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-nodevice
            '''
            result = self._values.get("no_device")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def virtual_name(self) -> typing.Optional[builtins.str]:
            '''The virtual device name.

            For more information, see `BlockDeviceMapping <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_BlockDeviceMapping.html>`_ . You can specify either the ``VirtualName`` or ``Ebs`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-virtualname
            '''
            result = self._values.get("virtual_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockDeviceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnInstancePropsMixin.EbsBlockDeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_on_termination": "deleteOnTermination",
            "iops": "iops",
            "snapshot_id": "snapshotId",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EbsBlockDeviceProperty:
        def __init__(
            self,
            *,
            delete_on_termination: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            snapshot_id: typing.Optional[builtins.str] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param delete_on_termination: Whether the volume is deleted on instance termination.
            :param iops: The number of I/O operations per second (IOPS) that the volume supports. For more information, see `EbsBlockDevice <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EbsBlockDevice.html>`_ .
            :param snapshot_id: The snapshot ID.
            :param volume_size: The volume size, in GiB. For more information, see `EbsBlockDevice <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EbsBlockDevice.html>`_ .
            :param volume_type: The volume type. ``gp2`` for General Purpose (SSD) volumes, ``io1`` for Provisioned IOPS (SSD) volumes, ``st1`` for Throughput Optimized hard disk drives (HDD), ``sc1`` for Cold HDD,and ``standard`` for Magnetic volumes. If you specify the ``io1`` volume type, you must also specify a value for the ``Iops`` attribute. The maximum ratio of provisioned IOPS to requested volume size (in GiB) is 50:1. AWS uses the default volume size (in GiB) specified in the AMI attributes to set IOPS to 50 x (volume size).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                ebs_block_device_property = opsworks_mixins.CfnInstancePropsMixin.EbsBlockDeviceProperty(
                    delete_on_termination=False,
                    iops=123,
                    snapshot_id="snapshotId",
                    volume_size=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dedd2b0679b62402c70a92193ed6fcfb66c6d9a5c01810141b46495a30222dd0)
                check_type(argname="argument delete_on_termination", value=delete_on_termination, expected_type=type_hints["delete_on_termination"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
                check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_on_termination is not None:
                self._values["delete_on_termination"] = delete_on_termination
            if iops is not None:
                self._values["iops"] = iops
            if snapshot_id is not None:
                self._values["snapshot_id"] = snapshot_id
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def delete_on_termination(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the volume is deleted on instance termination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-deleteontermination
            '''
            result = self._values.get("delete_on_termination")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of I/O operations per second (IOPS) that the volume supports.

            For more information, see `EbsBlockDevice <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EbsBlockDevice.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def snapshot_id(self) -> typing.Optional[builtins.str]:
            '''The snapshot ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-snapshotid
            '''
            result = self._values.get("snapshot_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''The volume size, in GiB.

            For more information, see `EbsBlockDevice <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_EbsBlockDevice.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''The volume type.

            ``gp2`` for General Purpose (SSD) volumes, ``io1`` for Provisioned IOPS (SSD) volumes, ``st1`` for Throughput Optimized hard disk drives (HDD), ``sc1`` for Cold HDD,and ``standard`` for Magnetic volumes.

            If you specify the ``io1`` volume type, you must also specify a value for the ``Iops`` attribute. The maximum ratio of provisioned IOPS to requested volume size (in GiB) is 50:1. AWS uses the default volume size (in GiB) specified in the AMI attributes to set IOPS to 50 x (volume size).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsBlockDeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnInstancePropsMixin.TimeBasedAutoScalingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "friday": "friday",
            "monday": "monday",
            "saturday": "saturday",
            "sunday": "sunday",
            "thursday": "thursday",
            "tuesday": "tuesday",
            "wednesday": "wednesday",
        },
    )
    class TimeBasedAutoScalingProperty:
        def __init__(
            self,
            *,
            friday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            monday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            saturday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            sunday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            thursday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            tuesday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            wednesday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param friday: The schedule for Friday.
            :param monday: The schedule for Monday.
            :param saturday: The schedule for Saturday.
            :param sunday: The schedule for Sunday.
            :param thursday: The schedule for Thursday.
            :param tuesday: The schedule for Tuesday.
            :param wednesday: The schedule for Wednesday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                time_based_auto_scaling_property = opsworks_mixins.CfnInstancePropsMixin.TimeBasedAutoScalingProperty(
                    friday={
                        "friday_key": "friday"
                    },
                    monday={
                        "monday_key": "monday"
                    },
                    saturday={
                        "saturday_key": "saturday"
                    },
                    sunday={
                        "sunday_key": "sunday"
                    },
                    thursday={
                        "thursday_key": "thursday"
                    },
                    tuesday={
                        "tuesday_key": "tuesday"
                    },
                    wednesday={
                        "wednesday_key": "wednesday"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b7d2e8fbea71f6d83f9f4f65613a74f9b181967268619b8f0b1943ea36db860)
                check_type(argname="argument friday", value=friday, expected_type=type_hints["friday"])
                check_type(argname="argument monday", value=monday, expected_type=type_hints["monday"])
                check_type(argname="argument saturday", value=saturday, expected_type=type_hints["saturday"])
                check_type(argname="argument sunday", value=sunday, expected_type=type_hints["sunday"])
                check_type(argname="argument thursday", value=thursday, expected_type=type_hints["thursday"])
                check_type(argname="argument tuesday", value=tuesday, expected_type=type_hints["tuesday"])
                check_type(argname="argument wednesday", value=wednesday, expected_type=type_hints["wednesday"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if friday is not None:
                self._values["friday"] = friday
            if monday is not None:
                self._values["monday"] = monday
            if saturday is not None:
                self._values["saturday"] = saturday
            if sunday is not None:
                self._values["sunday"] = sunday
            if thursday is not None:
                self._values["thursday"] = thursday
            if tuesday is not None:
                self._values["tuesday"] = tuesday
            if wednesday is not None:
                self._values["wednesday"] = wednesday

        @builtins.property
        def friday(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The schedule for Friday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-friday
            '''
            result = self._values.get("friday")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def monday(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The schedule for Monday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-monday
            '''
            result = self._values.get("monday")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def saturday(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The schedule for Saturday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-saturday
            '''
            result = self._values.get("saturday")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sunday(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The schedule for Sunday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-sunday
            '''
            result = self._values.get("sunday")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def thursday(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The schedule for Thursday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-thursday
            '''
            result = self._values.get("thursday")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def tuesday(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The schedule for Tuesday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-tuesday
            '''
            result = self._values.get("tuesday")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def wednesday(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The schedule for Wednesday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-wednesday
            '''
            result = self._values.get("wednesday")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedAutoScalingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnLayerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "auto_assign_elastic_ips": "autoAssignElasticIps",
        "auto_assign_public_ips": "autoAssignPublicIps",
        "custom_instance_profile_arn": "customInstanceProfileArn",
        "custom_json": "customJson",
        "custom_recipes": "customRecipes",
        "custom_security_group_ids": "customSecurityGroupIds",
        "enable_auto_healing": "enableAutoHealing",
        "install_updates_on_boot": "installUpdatesOnBoot",
        "lifecycle_event_configuration": "lifecycleEventConfiguration",
        "load_based_auto_scaling": "loadBasedAutoScaling",
        "name": "name",
        "packages": "packages",
        "shortname": "shortname",
        "stack_id": "stackId",
        "tags": "tags",
        "type": "type",
        "use_ebs_optimized_instances": "useEbsOptimizedInstances",
        "volume_configurations": "volumeConfigurations",
    },
)
class CfnLayerMixinProps:
    def __init__(
        self,
        *,
        attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        auto_assign_elastic_ips: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        auto_assign_public_ips: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        custom_instance_profile_arn: typing.Optional[builtins.str] = None,
        custom_json: typing.Any = None,
        custom_recipes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLayerPropsMixin.RecipesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_auto_healing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        install_updates_on_boot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        lifecycle_event_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLayerPropsMixin.LifecycleEventConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        load_based_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLayerPropsMixin.LoadBasedAutoScalingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        shortname: typing.Optional[builtins.str] = None,
        stack_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        use_ebs_optimized_instances: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        volume_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLayerPropsMixin.VolumeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnLayerPropsMixin.

        :param attributes: One or more user-defined key-value pairs to be added to the stack attributes. To create a cluster layer, set the ``EcsClusterArn`` attribute to the cluster's ARN.
        :param auto_assign_elastic_ips: Whether to automatically assign an `Elastic IP address <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html>`_ to the layer's instances. For more information, see `How to Edit a Layer <https://docs.aws.amazon.com/opsworks/latest/userguide/workinglayers-basics-edit.html>`_ .
        :param auto_assign_public_ips: For stacks that are running in a VPC, whether to automatically assign a public IP address to the layer's instances. For more information, see `How to Edit a Layer <https://docs.aws.amazon.com/opsworks/latest/userguide/workinglayers-basics-edit.html>`_ .
        :param custom_instance_profile_arn: The ARN of an IAM profile to be used for the layer's EC2 instances. For more information about IAM ARNs, see `Using Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ .
        :param custom_json: A JSON-formatted string containing custom stack configuration and deployment attributes to be installed on the layer's instances. For more information, see `Using Custom JSON <https://docs.aws.amazon.com/opsworks/latest/userguide/workingcookbook-json-override.html>`_ . This feature is supported as of version 1.7.42 of the AWS CLI .
        :param custom_recipes: A ``LayerCustomRecipes`` object that specifies the layer custom recipes.
        :param custom_security_group_ids: An array containing the layer custom security group IDs.
        :param enable_auto_healing: Whether to disable auto healing for the layer.
        :param install_updates_on_boot: Whether to install operating system and package updates when the instance boots. The default value is ``true`` . To control when updates are installed, set this value to ``false`` . You must then update your instances manually by using ``CreateDeployment`` to run the ``update_dependencies`` stack command or by manually running ``yum`` (Amazon Linux) or ``apt-get`` (Ubuntu) on the instances. .. epigraph:: To ensure that your instances have the latest security updates, we strongly recommend using the default value of ``true`` .
        :param lifecycle_event_configuration: A ``LifeCycleEventConfiguration`` object that you can use to configure the Shutdown event to specify an execution timeout and enable or disable Elastic Load Balancer connection draining.
        :param load_based_auto_scaling: The load-based scaling configuration for the OpsWorks layer.
        :param name: The layer name, which is used by the console. Layer names can be a maximum of 32 characters.
        :param packages: An array of ``Package`` objects that describes the layer packages.
        :param shortname: For custom layers only, use this parameter to specify the layer's short name, which is used internally by OpsWorks Stacks and by Chef recipes. The short name is also used as the name for the directory where your app files are installed. It can have a maximum of 32 characters, which are limited to the alphanumeric characters, '-', '_', and '.'. Built-in layer short names are defined by OpsWorks Stacks. For more information, see the `Layer Reference <https://docs.aws.amazon.com/opsworks/latest/userguide/layers.html>`_ .
        :param stack_id: The layer stack ID.
        :param tags: Specifies one or more sets of tags (key–value pairs) to associate with this OpsWorks layer. Use tags to manage your resources.
        :param type: The layer type. A stack cannot have more than one built-in layer of the same type. It can have any number of custom layers. Built-in layers are not available in Chef 12 stacks.
        :param use_ebs_optimized_instances: Whether to use Amazon EBS-optimized instances.
        :param volume_configurations: A ``VolumeConfigurations`` object that describes the layer's Amazon EBS volumes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
            
            # custom_json: Any
            
            cfn_layer_mixin_props = opsworks_mixins.CfnLayerMixinProps(
                attributes={
                    "attributes_key": "attributes"
                },
                auto_assign_elastic_ips=False,
                auto_assign_public_ips=False,
                custom_instance_profile_arn="customInstanceProfileArn",
                custom_json=custom_json,
                custom_recipes=opsworks_mixins.CfnLayerPropsMixin.RecipesProperty(
                    configure=["configure"],
                    deploy=["deploy"],
                    setup=["setup"],
                    shutdown=["shutdown"],
                    undeploy=["undeploy"]
                ),
                custom_security_group_ids=["customSecurityGroupIds"],
                enable_auto_healing=False,
                install_updates_on_boot=False,
                lifecycle_event_configuration=opsworks_mixins.CfnLayerPropsMixin.LifecycleEventConfigurationProperty(
                    shutdown_event_configuration=opsworks_mixins.CfnLayerPropsMixin.ShutdownEventConfigurationProperty(
                        delay_until_elb_connections_drained=False,
                        execution_timeout=123
                    )
                ),
                load_based_auto_scaling=opsworks_mixins.CfnLayerPropsMixin.LoadBasedAutoScalingProperty(
                    down_scaling=opsworks_mixins.CfnLayerPropsMixin.AutoScalingThresholdsProperty(
                        cpu_threshold=123,
                        ignore_metrics_time=123,
                        instance_count=123,
                        load_threshold=123,
                        memory_threshold=123,
                        thresholds_wait_time=123
                    ),
                    enable=False,
                    up_scaling=opsworks_mixins.CfnLayerPropsMixin.AutoScalingThresholdsProperty(
                        cpu_threshold=123,
                        ignore_metrics_time=123,
                        instance_count=123,
                        load_threshold=123,
                        memory_threshold=123,
                        thresholds_wait_time=123
                    )
                ),
                name="name",
                packages=["packages"],
                shortname="shortname",
                stack_id="stackId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type",
                use_ebs_optimized_instances=False,
                volume_configurations=[opsworks_mixins.CfnLayerPropsMixin.VolumeConfigurationProperty(
                    encrypted=False,
                    iops=123,
                    mount_point="mountPoint",
                    number_of_disks=123,
                    raid_level=123,
                    size=123,
                    volume_type="volumeType"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ccb68cbc18c6d96b0eb5c724b8dfe1899bd2d85edc58bb113e20042a026376)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument auto_assign_elastic_ips", value=auto_assign_elastic_ips, expected_type=type_hints["auto_assign_elastic_ips"])
            check_type(argname="argument auto_assign_public_ips", value=auto_assign_public_ips, expected_type=type_hints["auto_assign_public_ips"])
            check_type(argname="argument custom_instance_profile_arn", value=custom_instance_profile_arn, expected_type=type_hints["custom_instance_profile_arn"])
            check_type(argname="argument custom_json", value=custom_json, expected_type=type_hints["custom_json"])
            check_type(argname="argument custom_recipes", value=custom_recipes, expected_type=type_hints["custom_recipes"])
            check_type(argname="argument custom_security_group_ids", value=custom_security_group_ids, expected_type=type_hints["custom_security_group_ids"])
            check_type(argname="argument enable_auto_healing", value=enable_auto_healing, expected_type=type_hints["enable_auto_healing"])
            check_type(argname="argument install_updates_on_boot", value=install_updates_on_boot, expected_type=type_hints["install_updates_on_boot"])
            check_type(argname="argument lifecycle_event_configuration", value=lifecycle_event_configuration, expected_type=type_hints["lifecycle_event_configuration"])
            check_type(argname="argument load_based_auto_scaling", value=load_based_auto_scaling, expected_type=type_hints["load_based_auto_scaling"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument shortname", value=shortname, expected_type=type_hints["shortname"])
            check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument use_ebs_optimized_instances", value=use_ebs_optimized_instances, expected_type=type_hints["use_ebs_optimized_instances"])
            check_type(argname="argument volume_configurations", value=volume_configurations, expected_type=type_hints["volume_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attributes is not None:
            self._values["attributes"] = attributes
        if auto_assign_elastic_ips is not None:
            self._values["auto_assign_elastic_ips"] = auto_assign_elastic_ips
        if auto_assign_public_ips is not None:
            self._values["auto_assign_public_ips"] = auto_assign_public_ips
        if custom_instance_profile_arn is not None:
            self._values["custom_instance_profile_arn"] = custom_instance_profile_arn
        if custom_json is not None:
            self._values["custom_json"] = custom_json
        if custom_recipes is not None:
            self._values["custom_recipes"] = custom_recipes
        if custom_security_group_ids is not None:
            self._values["custom_security_group_ids"] = custom_security_group_ids
        if enable_auto_healing is not None:
            self._values["enable_auto_healing"] = enable_auto_healing
        if install_updates_on_boot is not None:
            self._values["install_updates_on_boot"] = install_updates_on_boot
        if lifecycle_event_configuration is not None:
            self._values["lifecycle_event_configuration"] = lifecycle_event_configuration
        if load_based_auto_scaling is not None:
            self._values["load_based_auto_scaling"] = load_based_auto_scaling
        if name is not None:
            self._values["name"] = name
        if packages is not None:
            self._values["packages"] = packages
        if shortname is not None:
            self._values["shortname"] = shortname
        if stack_id is not None:
            self._values["stack_id"] = stack_id
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if use_ebs_optimized_instances is not None:
            self._values["use_ebs_optimized_instances"] = use_ebs_optimized_instances
        if volume_configurations is not None:
            self._values["volume_configurations"] = volume_configurations

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''One or more user-defined key-value pairs to be added to the stack attributes.

        To create a cluster layer, set the ``EcsClusterArn`` attribute to the cluster's ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def auto_assign_elastic_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to automatically assign an `Elastic IP address <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html>`_ to the layer's instances. For more information, see `How to Edit a Layer <https://docs.aws.amazon.com/opsworks/latest/userguide/workinglayers-basics-edit.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignelasticips
        '''
        result = self._values.get("auto_assign_elastic_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def auto_assign_public_ips(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''For stacks that are running in a VPC, whether to automatically assign a public IP address to the layer's instances.

        For more information, see `How to Edit a Layer <https://docs.aws.amazon.com/opsworks/latest/userguide/workinglayers-basics-edit.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignpublicips
        '''
        result = self._values.get("auto_assign_public_ips")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def custom_instance_profile_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM profile to be used for the layer's EC2 instances.

        For more information about IAM ARNs, see `Using Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-custominstanceprofilearn
        '''
        result = self._values.get("custom_instance_profile_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_json(self) -> typing.Any:
        '''A JSON-formatted string containing custom stack configuration and deployment attributes to be installed on the layer's instances.

        For more information, see `Using Custom JSON <https://docs.aws.amazon.com/opsworks/latest/userguide/workingcookbook-json-override.html>`_ . This feature is supported as of version 1.7.42 of the AWS CLI .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customjson
        '''
        result = self._values.get("custom_json")
        return typing.cast(typing.Any, result)

    @builtins.property
    def custom_recipes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.RecipesProperty"]]:
        '''A ``LayerCustomRecipes`` object that specifies the layer custom recipes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customrecipes
        '''
        result = self._values.get("custom_recipes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.RecipesProperty"]], result)

    @builtins.property
    def custom_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array containing the layer custom security group IDs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customsecuritygroupids
        '''
        result = self._values.get("custom_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_auto_healing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to disable auto healing for the layer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-enableautohealing
        '''
        result = self._values.get("enable_auto_healing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def install_updates_on_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to install operating system and package updates when the instance boots.

        The default value is ``true`` . To control when updates are installed, set this value to ``false`` . You must then update your instances manually by using ``CreateDeployment`` to run the ``update_dependencies`` stack command or by manually running ``yum`` (Amazon Linux) or ``apt-get`` (Ubuntu) on the instances.
        .. epigraph::

           To ensure that your instances have the latest security updates, we strongly recommend using the default value of ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-installupdatesonboot
        '''
        result = self._values.get("install_updates_on_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def lifecycle_event_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.LifecycleEventConfigurationProperty"]]:
        '''A ``LifeCycleEventConfiguration`` object that you can use to configure the Shutdown event to specify an execution timeout and enable or disable Elastic Load Balancer connection draining.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-lifecycleeventconfiguration
        '''
        result = self._values.get("lifecycle_event_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.LifecycleEventConfigurationProperty"]], result)

    @builtins.property
    def load_based_auto_scaling(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.LoadBasedAutoScalingProperty"]]:
        '''The load-based scaling configuration for the OpsWorks layer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-loadbasedautoscaling
        '''
        result = self._values.get("load_based_auto_scaling")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.LoadBasedAutoScalingProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The layer name, which is used by the console.

        Layer names can be a maximum of 32 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of ``Package`` objects that describes the layer packages.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-packages
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def shortname(self) -> typing.Optional[builtins.str]:
        '''For custom layers only, use this parameter to specify the layer's short name, which is used internally by OpsWorks Stacks and by Chef recipes.

        The short name is also used as the name for the directory where your app files are installed. It can have a maximum of 32 characters, which are limited to the alphanumeric characters, '-', '_', and '.'.

        Built-in layer short names are defined by OpsWorks Stacks. For more information, see the `Layer Reference <https://docs.aws.amazon.com/opsworks/latest/userguide/layers.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-shortname
        '''
        result = self._values.get("shortname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_id(self) -> typing.Optional[builtins.str]:
        '''The layer stack ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-stackid
        '''
        result = self._values.get("stack_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies one or more sets of tags (key–value pairs) to associate with this OpsWorks layer.

        Use tags to manage your resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The layer type.

        A stack cannot have more than one built-in layer of the same type. It can have any number of custom layers. Built-in layers are not available in Chef 12 stacks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_ebs_optimized_instances(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to use Amazon EBS-optimized instances.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-useebsoptimizedinstances
        '''
        result = self._values.get("use_ebs_optimized_instances")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def volume_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.VolumeConfigurationProperty"]]]]:
        '''A ``VolumeConfigurations`` object that describes the layer's Amazon EBS volumes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-volumeconfigurations
        '''
        result = self._values.get("volume_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.VolumeConfigurationProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLayerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLayerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnLayerPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html
    :cloudformationResource: AWS::OpsWorks::Layer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
        
        # custom_json: Any
        
        cfn_layer_props_mixin = opsworks_mixins.CfnLayerPropsMixin(opsworks_mixins.CfnLayerMixinProps(
            attributes={
                "attributes_key": "attributes"
            },
            auto_assign_elastic_ips=False,
            auto_assign_public_ips=False,
            custom_instance_profile_arn="customInstanceProfileArn",
            custom_json=custom_json,
            custom_recipes=opsworks_mixins.CfnLayerPropsMixin.RecipesProperty(
                configure=["configure"],
                deploy=["deploy"],
                setup=["setup"],
                shutdown=["shutdown"],
                undeploy=["undeploy"]
            ),
            custom_security_group_ids=["customSecurityGroupIds"],
            enable_auto_healing=False,
            install_updates_on_boot=False,
            lifecycle_event_configuration=opsworks_mixins.CfnLayerPropsMixin.LifecycleEventConfigurationProperty(
                shutdown_event_configuration=opsworks_mixins.CfnLayerPropsMixin.ShutdownEventConfigurationProperty(
                    delay_until_elb_connections_drained=False,
                    execution_timeout=123
                )
            ),
            load_based_auto_scaling=opsworks_mixins.CfnLayerPropsMixin.LoadBasedAutoScalingProperty(
                down_scaling=opsworks_mixins.CfnLayerPropsMixin.AutoScalingThresholdsProperty(
                    cpu_threshold=123,
                    ignore_metrics_time=123,
                    instance_count=123,
                    load_threshold=123,
                    memory_threshold=123,
                    thresholds_wait_time=123
                ),
                enable=False,
                up_scaling=opsworks_mixins.CfnLayerPropsMixin.AutoScalingThresholdsProperty(
                    cpu_threshold=123,
                    ignore_metrics_time=123,
                    instance_count=123,
                    load_threshold=123,
                    memory_threshold=123,
                    thresholds_wait_time=123
                )
            ),
            name="name",
            packages=["packages"],
            shortname="shortname",
            stack_id="stackId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type",
            use_ebs_optimized_instances=False,
            volume_configurations=[opsworks_mixins.CfnLayerPropsMixin.VolumeConfigurationProperty(
                encrypted=False,
                iops=123,
                mount_point="mountPoint",
                number_of_disks=123,
                raid_level=123,
                size=123,
                volume_type="volumeType"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLayerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpsWorks::Layer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b47bb06b9c94b588cedfb15607b5a1fa1f7d11cc0e5a833689a4f9b51b84a01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbb5f98f7ca330e67fb08d0b3f7fad9c0a015428594984dc8f0112fb959ede69)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27197eba6098d3b0ec0aa8d7178e026a2f810f6af5a67aa20aba2ee9b73a13e2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLayerMixinProps:
        return typing.cast(CfnLayerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnLayerPropsMixin.AutoScalingThresholdsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cpu_threshold": "cpuThreshold",
            "ignore_metrics_time": "ignoreMetricsTime",
            "instance_count": "instanceCount",
            "load_threshold": "loadThreshold",
            "memory_threshold": "memoryThreshold",
            "thresholds_wait_time": "thresholdsWaitTime",
        },
    )
    class AutoScalingThresholdsProperty:
        def __init__(
            self,
            *,
            cpu_threshold: typing.Optional[jsii.Number] = None,
            ignore_metrics_time: typing.Optional[jsii.Number] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            load_threshold: typing.Optional[jsii.Number] = None,
            memory_threshold: typing.Optional[jsii.Number] = None,
            thresholds_wait_time: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param cpu_threshold: The CPU utilization threshold, as a percent of the available CPU. A value of -1 disables the threshold.
            :param ignore_metrics_time: The amount of time (in minutes) after a scaling event occurs that OpsWorks Stacks should ignore metrics and suppress additional scaling events. For example, OpsWorks Stacks adds new instances following an upscaling event but the instances won't start reducing the load until they have been booted and configured. There is no point in raising additional scaling events during that operation, which typically takes several minutes. ``IgnoreMetricsTime`` allows you to direct OpsWorks Stacks to suppress scaling events long enough to get the new instances online.
            :param instance_count: The number of instances to add or remove when the load exceeds a threshold.
            :param load_threshold: The load threshold. A value of -1 disables the threshold. For more information about how load is computed, see `Load (computing) <https://docs.aws.amazon.com/http://en.wikipedia.org/wiki/Load_%28computing%29>`_ .
            :param memory_threshold: The memory utilization threshold, as a percent of the available memory. A value of -1 disables the threshold.
            :param thresholds_wait_time: The amount of time, in minutes, that the load must exceed a threshold before more instances are added or removed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-autoscalingthresholds.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                auto_scaling_thresholds_property = opsworks_mixins.CfnLayerPropsMixin.AutoScalingThresholdsProperty(
                    cpu_threshold=123,
                    ignore_metrics_time=123,
                    instance_count=123,
                    load_threshold=123,
                    memory_threshold=123,
                    thresholds_wait_time=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd88cdea05e245498039c4c732d99833d01e6109a5148f88b6fde11262f13062)
                check_type(argname="argument cpu_threshold", value=cpu_threshold, expected_type=type_hints["cpu_threshold"])
                check_type(argname="argument ignore_metrics_time", value=ignore_metrics_time, expected_type=type_hints["ignore_metrics_time"])
                check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
                check_type(argname="argument load_threshold", value=load_threshold, expected_type=type_hints["load_threshold"])
                check_type(argname="argument memory_threshold", value=memory_threshold, expected_type=type_hints["memory_threshold"])
                check_type(argname="argument thresholds_wait_time", value=thresholds_wait_time, expected_type=type_hints["thresholds_wait_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu_threshold is not None:
                self._values["cpu_threshold"] = cpu_threshold
            if ignore_metrics_time is not None:
                self._values["ignore_metrics_time"] = ignore_metrics_time
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if load_threshold is not None:
                self._values["load_threshold"] = load_threshold
            if memory_threshold is not None:
                self._values["memory_threshold"] = memory_threshold
            if thresholds_wait_time is not None:
                self._values["thresholds_wait_time"] = thresholds_wait_time

        @builtins.property
        def cpu_threshold(self) -> typing.Optional[jsii.Number]:
            '''The CPU utilization threshold, as a percent of the available CPU.

            A value of -1 disables the threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-autoscalingthresholds.html#cfn-opsworks-layer-autoscalingthresholds-cputhreshold
            '''
            result = self._values.get("cpu_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ignore_metrics_time(self) -> typing.Optional[jsii.Number]:
            '''The amount of time (in minutes) after a scaling event occurs that OpsWorks Stacks should ignore metrics and suppress additional scaling events.

            For example, OpsWorks Stacks adds new instances following an upscaling event but the instances won't start reducing the load until they have been booted and configured. There is no point in raising additional scaling events during that operation, which typically takes several minutes. ``IgnoreMetricsTime`` allows you to direct OpsWorks Stacks to suppress scaling events long enough to get the new instances online.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-autoscalingthresholds.html#cfn-opsworks-layer-autoscalingthresholds-ignoremetricstime
            '''
            result = self._values.get("ignore_metrics_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            '''The number of instances to add or remove when the load exceeds a threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-autoscalingthresholds.html#cfn-opsworks-layer-autoscalingthresholds-instancecount
            '''
            result = self._values.get("instance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def load_threshold(self) -> typing.Optional[jsii.Number]:
            '''The load threshold.

            A value of -1 disables the threshold. For more information about how load is computed, see `Load (computing) <https://docs.aws.amazon.com/http://en.wikipedia.org/wiki/Load_%28computing%29>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-autoscalingthresholds.html#cfn-opsworks-layer-autoscalingthresholds-loadthreshold
            '''
            result = self._values.get("load_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def memory_threshold(self) -> typing.Optional[jsii.Number]:
            '''The memory utilization threshold, as a percent of the available memory.

            A value of -1 disables the threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-autoscalingthresholds.html#cfn-opsworks-layer-autoscalingthresholds-memorythreshold
            '''
            result = self._values.get("memory_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def thresholds_wait_time(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in minutes, that the load must exceed a threshold before more instances are added or removed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-autoscalingthresholds.html#cfn-opsworks-layer-autoscalingthresholds-thresholdswaittime
            '''
            result = self._values.get("thresholds_wait_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingThresholdsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnLayerPropsMixin.LifecycleEventConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"shutdown_event_configuration": "shutdownEventConfiguration"},
    )
    class LifecycleEventConfigurationProperty:
        def __init__(
            self,
            *,
            shutdown_event_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLayerPropsMixin.ShutdownEventConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param shutdown_event_configuration: The Shutdown event configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                lifecycle_event_configuration_property = opsworks_mixins.CfnLayerPropsMixin.LifecycleEventConfigurationProperty(
                    shutdown_event_configuration=opsworks_mixins.CfnLayerPropsMixin.ShutdownEventConfigurationProperty(
                        delay_until_elb_connections_drained=False,
                        execution_timeout=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df7ed848eefb0c31a672f49417ab69d3b6989ec755ee3da7a82d1bdf498edeb1)
                check_type(argname="argument shutdown_event_configuration", value=shutdown_event_configuration, expected_type=type_hints["shutdown_event_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if shutdown_event_configuration is not None:
                self._values["shutdown_event_configuration"] = shutdown_event_configuration

        @builtins.property
        def shutdown_event_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.ShutdownEventConfigurationProperty"]]:
            '''The Shutdown event configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration.html#cfn-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration
            '''
            result = self._values.get("shutdown_event_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.ShutdownEventConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleEventConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnLayerPropsMixin.LoadBasedAutoScalingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "down_scaling": "downScaling",
            "enable": "enable",
            "up_scaling": "upScaling",
        },
    )
    class LoadBasedAutoScalingProperty:
        def __init__(
            self,
            *,
            down_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLayerPropsMixin.AutoScalingThresholdsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            up_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLayerPropsMixin.AutoScalingThresholdsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param down_scaling: An ``AutoScalingThresholds`` object that describes the downscaling configuration, which defines how and when OpsWorks Stacks reduces the number of instances.
            :param enable: Whether load-based auto scaling is enabled for the layer.
            :param up_scaling: An ``AutoScalingThresholds`` object that describes the upscaling configuration, which defines how and when OpsWorks Stacks increases the number of instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                load_based_auto_scaling_property = opsworks_mixins.CfnLayerPropsMixin.LoadBasedAutoScalingProperty(
                    down_scaling=opsworks_mixins.CfnLayerPropsMixin.AutoScalingThresholdsProperty(
                        cpu_threshold=123,
                        ignore_metrics_time=123,
                        instance_count=123,
                        load_threshold=123,
                        memory_threshold=123,
                        thresholds_wait_time=123
                    ),
                    enable=False,
                    up_scaling=opsworks_mixins.CfnLayerPropsMixin.AutoScalingThresholdsProperty(
                        cpu_threshold=123,
                        ignore_metrics_time=123,
                        instance_count=123,
                        load_threshold=123,
                        memory_threshold=123,
                        thresholds_wait_time=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17d7a5a4f09b6289b36517c635b24b470c0cded1bd85885193f38b6431fece38)
                check_type(argname="argument down_scaling", value=down_scaling, expected_type=type_hints["down_scaling"])
                check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
                check_type(argname="argument up_scaling", value=up_scaling, expected_type=type_hints["up_scaling"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if down_scaling is not None:
                self._values["down_scaling"] = down_scaling
            if enable is not None:
                self._values["enable"] = enable
            if up_scaling is not None:
                self._values["up_scaling"] = up_scaling

        @builtins.property
        def down_scaling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.AutoScalingThresholdsProperty"]]:
            '''An ``AutoScalingThresholds`` object that describes the downscaling configuration, which defines how and when OpsWorks Stacks reduces the number of instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-downscaling
            '''
            result = self._values.get("down_scaling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.AutoScalingThresholdsProperty"]], result)

        @builtins.property
        def enable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether load-based auto scaling is enabled for the layer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-enable
            '''
            result = self._values.get("enable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def up_scaling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.AutoScalingThresholdsProperty"]]:
            '''An ``AutoScalingThresholds`` object that describes the upscaling configuration, which defines how and when OpsWorks Stacks increases the number of instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-upscaling
            '''
            result = self._values.get("up_scaling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLayerPropsMixin.AutoScalingThresholdsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoadBasedAutoScalingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnLayerPropsMixin.RecipesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configure": "configure",
            "deploy": "deploy",
            "setup": "setup",
            "shutdown": "shutdown",
            "undeploy": "undeploy",
        },
    )
    class RecipesProperty:
        def __init__(
            self,
            *,
            configure: typing.Optional[typing.Sequence[builtins.str]] = None,
            deploy: typing.Optional[typing.Sequence[builtins.str]] = None,
            setup: typing.Optional[typing.Sequence[builtins.str]] = None,
            shutdown: typing.Optional[typing.Sequence[builtins.str]] = None,
            undeploy: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param configure: An array of custom recipe names to be run following a ``configure`` event.
            :param deploy: An array of custom recipe names to be run following a ``deploy`` event.
            :param setup: An array of custom recipe names to be run following a ``setup`` event.
            :param shutdown: An array of custom recipe names to be run following a ``shutdown`` event.
            :param undeploy: An array of custom recipe names to be run following a ``undeploy`` event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                recipes_property = opsworks_mixins.CfnLayerPropsMixin.RecipesProperty(
                    configure=["configure"],
                    deploy=["deploy"],
                    setup=["setup"],
                    shutdown=["shutdown"],
                    undeploy=["undeploy"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9634cc89c8c23d46cc2a888071e72c14db74d1a3b6386148e45de2ff00dd62be)
                check_type(argname="argument configure", value=configure, expected_type=type_hints["configure"])
                check_type(argname="argument deploy", value=deploy, expected_type=type_hints["deploy"])
                check_type(argname="argument setup", value=setup, expected_type=type_hints["setup"])
                check_type(argname="argument shutdown", value=shutdown, expected_type=type_hints["shutdown"])
                check_type(argname="argument undeploy", value=undeploy, expected_type=type_hints["undeploy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configure is not None:
                self._values["configure"] = configure
            if deploy is not None:
                self._values["deploy"] = deploy
            if setup is not None:
                self._values["setup"] = setup
            if shutdown is not None:
                self._values["shutdown"] = shutdown
            if undeploy is not None:
                self._values["undeploy"] = undeploy

        @builtins.property
        def configure(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of custom recipe names to be run following a ``configure`` event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-recipes-configure
            '''
            result = self._values.get("configure")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def deploy(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of custom recipe names to be run following a ``deploy`` event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-recipes-deploy
            '''
            result = self._values.get("deploy")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def setup(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of custom recipe names to be run following a ``setup`` event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-recipes-setup
            '''
            result = self._values.get("setup")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def shutdown(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of custom recipe names to be run following a ``shutdown`` event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-recipes-shutdown
            '''
            result = self._values.get("shutdown")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def undeploy(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of custom recipe names to be run following a ``undeploy`` event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-recipes-undeploy
            '''
            result = self._values.get("undeploy")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecipesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnLayerPropsMixin.ShutdownEventConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delay_until_elb_connections_drained": "delayUntilElbConnectionsDrained",
            "execution_timeout": "executionTimeout",
        },
    )
    class ShutdownEventConfigurationProperty:
        def __init__(
            self,
            *,
            delay_until_elb_connections_drained: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            execution_timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param delay_until_elb_connections_drained: Whether to enable Elastic Load Balancing connection draining. For more information, see `Connection Draining <https://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/TerminologyandKeyConcepts.html#conn-drain>`_
            :param execution_timeout: The time, in seconds, that OpsWorks Stacks waits after triggering a Shutdown event before shutting down an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-shutdowneventconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                shutdown_event_configuration_property = opsworks_mixins.CfnLayerPropsMixin.ShutdownEventConfigurationProperty(
                    delay_until_elb_connections_drained=False,
                    execution_timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8deb4c7236b02983da71b425282ab6fc7f6199b9c923882eeb79987c4b4e2048)
                check_type(argname="argument delay_until_elb_connections_drained", value=delay_until_elb_connections_drained, expected_type=type_hints["delay_until_elb_connections_drained"])
                check_type(argname="argument execution_timeout", value=execution_timeout, expected_type=type_hints["execution_timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delay_until_elb_connections_drained is not None:
                self._values["delay_until_elb_connections_drained"] = delay_until_elb_connections_drained
            if execution_timeout is not None:
                self._values["execution_timeout"] = execution_timeout

        @builtins.property
        def delay_until_elb_connections_drained(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to enable Elastic Load Balancing connection draining.

            For more information, see `Connection Draining <https://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/TerminologyandKeyConcepts.html#conn-drain>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-shutdowneventconfiguration.html#cfn-opsworks-layer-shutdowneventconfiguration-delayuntilelbconnectionsdrained
            '''
            result = self._values.get("delay_until_elb_connections_drained")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def execution_timeout(self) -> typing.Optional[jsii.Number]:
            '''The time, in seconds, that OpsWorks Stacks waits after triggering a Shutdown event before shutting down an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-shutdowneventconfiguration.html#cfn-opsworks-layer-shutdowneventconfiguration-executiontimeout
            '''
            result = self._values.get("execution_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ShutdownEventConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnLayerPropsMixin.VolumeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encrypted": "encrypted",
            "iops": "iops",
            "mount_point": "mountPoint",
            "number_of_disks": "numberOfDisks",
            "raid_level": "raidLevel",
            "size": "size",
            "volume_type": "volumeType",
        },
    )
    class VolumeConfigurationProperty:
        def __init__(
            self,
            *,
            encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            mount_point: typing.Optional[builtins.str] = None,
            number_of_disks: typing.Optional[jsii.Number] = None,
            raid_level: typing.Optional[jsii.Number] = None,
            size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param encrypted: Specifies whether an Amazon EBS volume is encrypted. For more information, see `Amazon EBS Encryption <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html>`_ .
            :param iops: The number of I/O operations per second (IOPS) to provision for the volume. For PIOPS volumes, the IOPS per disk. If you specify ``io1`` for the volume type, you must specify this property.
            :param mount_point: The volume mount point. For example "/dev/sdh".
            :param number_of_disks: The number of disks in the volume.
            :param raid_level: The volume `RAID level <https://docs.aws.amazon.com/http://en.wikipedia.org/wiki/Standard_RAID_levels>`_ .
            :param size: The volume size.
            :param volume_type: The volume type. For more information, see `Amazon EBS Volume Types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html>`_ . - ``standard`` - Magnetic. Magnetic volumes must have a minimum size of 1 GiB and a maximum size of 1024 GiB. - ``io1`` - Provisioned IOPS (SSD). PIOPS volumes must have a minimum size of 4 GiB and a maximum size of 16384 GiB. - ``gp2`` - General Purpose (SSD). General purpose volumes must have a minimum size of 1 GiB and a maximum size of 16384 GiB. - ``st1`` - Throughput Optimized hard disk drive (HDD). Throughput optimized HDD volumes must have a minimum size of 125 GiB and a maximum size of 16384 GiB. - ``sc1`` - Cold HDD. Cold HDD volumes must have a minimum size of 125 GiB and a maximum size of 16384 GiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                volume_configuration_property = opsworks_mixins.CfnLayerPropsMixin.VolumeConfigurationProperty(
                    encrypted=False,
                    iops=123,
                    mount_point="mountPoint",
                    number_of_disks=123,
                    raid_level=123,
                    size=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80e5503fb9c874df155881fa7cba7b3f015ec8d13754b5f1cabcf946f494d4f6)
                check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument mount_point", value=mount_point, expected_type=type_hints["mount_point"])
                check_type(argname="argument number_of_disks", value=number_of_disks, expected_type=type_hints["number_of_disks"])
                check_type(argname="argument raid_level", value=raid_level, expected_type=type_hints["raid_level"])
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encrypted is not None:
                self._values["encrypted"] = encrypted
            if iops is not None:
                self._values["iops"] = iops
            if mount_point is not None:
                self._values["mount_point"] = mount_point
            if number_of_disks is not None:
                self._values["number_of_disks"] = number_of_disks
            if raid_level is not None:
                self._values["raid_level"] = raid_level
            if size is not None:
                self._values["size"] = size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether an Amazon EBS volume is encrypted.

            For more information, see `Amazon EBS Encryption <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-encrypted
            '''
            result = self._values.get("encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of I/O operations per second (IOPS) to provision for the volume.

            For PIOPS volumes, the IOPS per disk.

            If you specify ``io1`` for the volume type, you must specify this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mount_point(self) -> typing.Optional[builtins.str]:
            '''The volume mount point.

            For example "/dev/sdh".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-mountpoint
            '''
            result = self._values.get("mount_point")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def number_of_disks(self) -> typing.Optional[jsii.Number]:
            '''The number of disks in the volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-numberofdisks
            '''
            result = self._values.get("number_of_disks")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def raid_level(self) -> typing.Optional[jsii.Number]:
            '''The volume `RAID level <https://docs.aws.amazon.com/http://en.wikipedia.org/wiki/Standard_RAID_levels>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-raidlevel
            '''
            result = self._values.get("raid_level")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''The volume size.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''The volume type. For more information, see `Amazon EBS Volume Types <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html>`_ .

            - ``standard`` - Magnetic. Magnetic volumes must have a minimum size of 1 GiB and a maximum size of 1024 GiB.
            - ``io1`` - Provisioned IOPS (SSD). PIOPS volumes must have a minimum size of 4 GiB and a maximum size of 16384 GiB.
            - ``gp2`` - General Purpose (SSD). General purpose volumes must have a minimum size of 1 GiB and a maximum size of 16384 GiB.
            - ``st1`` - Throughput Optimized hard disk drive (HDD). Throughput optimized HDD volumes must have a minimum size of 125 GiB and a maximum size of 16384 GiB.
            - ``sc1`` - Cold HDD. Cold HDD volumes must have a minimum size of 125 GiB and a maximum size of 16384 GiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnStackMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_version": "agentVersion",
        "attributes": "attributes",
        "chef_configuration": "chefConfiguration",
        "clone_app_ids": "cloneAppIds",
        "clone_permissions": "clonePermissions",
        "configuration_manager": "configurationManager",
        "custom_cookbooks_source": "customCookbooksSource",
        "custom_json": "customJson",
        "default_availability_zone": "defaultAvailabilityZone",
        "default_instance_profile_arn": "defaultInstanceProfileArn",
        "default_os": "defaultOs",
        "default_root_device_type": "defaultRootDeviceType",
        "default_ssh_key_name": "defaultSshKeyName",
        "default_subnet_id": "defaultSubnetId",
        "ecs_cluster_arn": "ecsClusterArn",
        "elastic_ips": "elasticIps",
        "hostname_theme": "hostnameTheme",
        "name": "name",
        "rds_db_instances": "rdsDbInstances",
        "service_role_arn": "serviceRoleArn",
        "source_stack_id": "sourceStackId",
        "tags": "tags",
        "use_custom_cookbooks": "useCustomCookbooks",
        "use_opsworks_security_groups": "useOpsworksSecurityGroups",
        "vpc_id": "vpcId",
    },
)
class CfnStackMixinProps:
    def __init__(
        self,
        *,
        agent_version: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        chef_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.ChefConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        clone_app_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        clone_permissions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        configuration_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.StackConfigurationManagerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_cookbooks_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_json: typing.Any = None,
        default_availability_zone: typing.Optional[builtins.str] = None,
        default_instance_profile_arn: typing.Optional[builtins.str] = None,
        default_os: typing.Optional[builtins.str] = None,
        default_root_device_type: typing.Optional[builtins.str] = None,
        default_ssh_key_name: typing.Optional[builtins.str] = None,
        default_subnet_id: typing.Optional[builtins.str] = None,
        ecs_cluster_arn: typing.Optional[builtins.str] = None,
        elastic_ips: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.ElasticIpProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        hostname_theme: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rds_db_instances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackPropsMixin.RdsDbInstanceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        source_stack_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_custom_cookbooks: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        use_opsworks_security_groups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStackPropsMixin.

        :param agent_version: The default OpsWorks Stacks agent version. You have the following options:. - Auto-update - Set this parameter to ``LATEST`` . OpsWorks Stacks automatically installs new agent versions on the stack's instances as soon as they are available. - Fixed version - Set this parameter to your preferred agent version. To update the agent version, you must edit the stack configuration and specify a new version. OpsWorks Stacks installs that version on the stack's instances. The default setting is the most recent release of the agent. To specify an agent version, you must use the complete version number, not the abbreviated number shown on the console. For a list of available agent version numbers, call ``DescribeAgentVersions`` . AgentVersion cannot be set to Chef 12.2. .. epigraph:: You can also specify an agent version when you create or update an instance, which overrides the stack's default setting.
        :param attributes: One or more user-defined key-value pairs to be added to the stack attributes.
        :param chef_configuration: A ``ChefConfiguration`` object that specifies whether to enable Berkshelf and the Berkshelf version on Chef 11.10 stacks. For more information, see `Create a New Stack <https://docs.aws.amazon.com/opsworks/latest/userguide/workingstacks-creating.html>`_ .
        :param clone_app_ids: If you're cloning an OpsWorks stack, a list of OpsWorks application stack IDs from the source stack to include in the cloned stack.
        :param clone_permissions: If you're cloning an OpsWorks stack, indicates whether to clone the source stack's permissions.
        :param configuration_manager: The configuration manager. When you create a stack we recommend that you use the configuration manager to specify the Chef version: 12, 11.10, or 11.4 for Linux stacks, or 12.2 for Windows stacks. The default value for Linux stacks is currently 12.
        :param custom_cookbooks_source: Contains the information required to retrieve an app or cookbook from a repository. For more information, see `Adding Apps <https://docs.aws.amazon.com/opsworks/latest/userguide/workingapps-creating.html>`_ or `Cookbooks and Recipes <https://docs.aws.amazon.com/opsworks/latest/userguide/workingcookbook.html>`_ .
        :param custom_json: A string that contains user-defined, custom JSON. It can be used to override the corresponding default stack configuration attribute values or to pass data to recipes. The string should be in the following format: ``"{\\"key1\\": \\"value1\\", \\"key2\\": \\"value2\\",...}"`` For more information about custom JSON, see `Use Custom JSON to Modify the Stack Configuration Attributes <https://docs.aws.amazon.com/opsworks/latest/userguide/workingstacks-json.html>`_ .
        :param default_availability_zone: The stack's default Availability Zone, which must be in the specified region. For more information, see `Regions and Endpoints <https://docs.aws.amazon.com/general/latest/gr/rande.html>`_ . If you also specify a value for ``DefaultSubnetId`` , the subnet must be in the same zone. For more information, see the ``VpcId`` parameter description.
        :param default_instance_profile_arn: The Amazon Resource Name (ARN) of an IAM profile that is the default profile for all of the stack's EC2 instances. For more information about IAM ARNs, see `Using Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ .
        :param default_os: The stack's default operating system, which is installed on every instance unless you specify a different operating system when you create the instance. You can specify one of the following. - A supported Linux operating system: An Amazon Linux version, such as ``Amazon Linux 2`` , ``Amazon Linux 2018.03`` , ``Amazon Linux 2017.09`` , ``Amazon Linux 2017.03`` , ``Amazon Linux 2016.09`` , ``Amazon Linux 2016.03`` , ``Amazon Linux 2015.09`` , or ``Amazon Linux 2015.03`` . - A supported Ubuntu operating system, such as ``Ubuntu 18.04 LTS`` , ``Ubuntu 16.04 LTS`` , ``Ubuntu 14.04 LTS`` , or ``Ubuntu 12.04 LTS`` . - ``CentOS Linux 7`` - ``Red Hat Enterprise Linux 7`` - A supported Windows operating system, such as ``Microsoft Windows Server 2012 R2 Base`` , ``Microsoft Windows Server 2012 R2 with SQL Server Express`` , ``Microsoft Windows Server 2012 R2 with SQL Server Standard`` , or ``Microsoft Windows Server 2012 R2 with SQL Server Web`` . - A custom AMI: ``Custom`` . You specify the custom AMI you want to use when you create instances. For more information, see `Using Custom AMIs <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-custom-ami.html>`_ . The default option is the current Amazon Linux version. Not all operating systems are supported with all versions of Chef. For more information about supported operating systems, see `OpsWorks Stacks Operating Systems <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-os.html>`_ .
        :param default_root_device_type: The default root device type. This value is the default for all instances in the stack, but you can override it when you create an instance. The default option is ``instance-store`` . For more information, see `Storage for the Root Device <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device>`_ .
        :param default_ssh_key_name: A default Amazon EC2 key pair name. The default value is none. If you specify a key pair name, OpsWorks installs the public key on the instance and you can use the private key with an SSH client to log in to the instance. For more information, see `Using SSH to Communicate with an Instance <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-ssh.html>`_ and `Managing SSH Access <https://docs.aws.amazon.com/opsworks/latest/userguide/security-ssh-access.html>`_ . You can override this setting by specifying a different key pair, or no key pair, when you `create an instance <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-add.html>`_ .
        :param default_subnet_id: The stack's default subnet ID. All instances are launched into this subnet unless you specify another subnet ID when you create the instance. This parameter is required if you specify a value for the ``VpcId`` parameter. If you also specify a value for ``DefaultAvailabilityZone`` , the subnet must be in that zone.
        :param ecs_cluster_arn: The Amazon Resource Name (ARN) of the ( Amazon ECS ) cluster to register with the OpsWorks stack. .. epigraph:: If you specify a cluster that's registered with another OpsWorks stack, CloudFormation deregisters the existing association before registering the cluster.
        :param elastic_ips: A list of Elastic IP addresses to register with the OpsWorks stack. .. epigraph:: If you specify an IP address that's registered with another OpsWorks stack, CloudFormation deregisters the existing association before registering the IP address.
        :param hostname_theme: The stack's host name theme, with spaces replaced by underscores. The theme is used to generate host names for the stack's instances. By default, ``HostnameTheme`` is set to ``Layer_Dependent`` , which creates host names by appending integers to the layer's short name. The other themes are: - ``Baked_Goods`` - ``Clouds`` - ``Europe_Cities`` - ``Fruits`` - ``Greek_Deities_and_Titans`` - ``Legendary_creatures_from_Japan`` - ``Planets_and_Moons`` - ``Roman_Deities`` - ``Scottish_Islands`` - ``US_Cities`` - ``Wild_Cats`` To obtain a generated host name, call ``GetHostNameSuggestion`` , which returns a host name based on the current theme.
        :param name: The stack name. Stack names can be a maximum of 64 characters.
        :param rds_db_instances: The Amazon Relational Database Service ( Amazon RDS ) database instance to register with the OpsWorks stack. .. epigraph:: If you specify a database instance that's registered with another OpsWorks stack, CloudFormation deregisters the existing association before registering the database instance.
        :param service_role_arn: The stack's IAM role, which allows OpsWorks Stacks to work with AWS resources on your behalf. You must set this parameter to the Amazon Resource Name (ARN) for an existing IAM role. For more information about IAM ARNs, see `Using Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ .
        :param source_stack_id: If you're cloning an OpsWorks stack, the stack ID of the source OpsWorks stack to clone.
        :param tags: A map that contains tag keys and tag values that are attached to a stack or layer. - The key cannot be empty. - The key can be a maximum of 127 characters, and can contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : /`` - The value can be a maximum 255 characters, and contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : /`` - Leading and trailing white spaces are trimmed from both the key and value. - A maximum of 40 tags is allowed for any resource.
        :param use_custom_cookbooks: Whether the stack uses custom cookbooks.
        :param use_opsworks_security_groups: Whether to associate the OpsWorks Stacks built-in security groups with the stack's layers. OpsWorks Stacks provides a standard set of built-in security groups, one for each layer, which are associated with layers by default. With ``UseOpsworksSecurityGroups`` you can instead provide your own custom security groups. ``UseOpsworksSecurityGroups`` has the following settings: - True - OpsWorks Stacks automatically associates the appropriate built-in security group with each layer (default setting). You can associate additional security groups with a layer after you create it, but you cannot delete the built-in security group. - False - OpsWorks Stacks does not associate built-in security groups with layers. You must create appropriate EC2 security groups and associate a security group with each layer that you create. However, you can still manually associate a built-in security group with a layer on creation; custom security groups are required only for those layers that need custom settings. For more information, see `Create a New Stack <https://docs.aws.amazon.com/opsworks/latest/userguide/workingstacks-creating.html>`_ .
        :param vpc_id: The ID of the VPC that the stack is to be launched into. The VPC must be in the stack's region. All instances are launched into this VPC. You cannot change the ID later. - If your account supports EC2-Classic, the default value is ``no VPC`` . - If your account does not support EC2-Classic, the default value is the default VPC for the specified region. If the VPC ID corresponds to a default VPC and you have specified either the ``DefaultAvailabilityZone`` or the ``DefaultSubnetId`` parameter only, OpsWorks Stacks infers the value of the other parameter. If you specify neither parameter, OpsWorks Stacks sets these parameters to the first valid Availability Zone for the specified region and the corresponding default VPC subnet ID, respectively. If you specify a nondefault VPC ID, note the following: - It must belong to a VPC in your account that is in the specified region. - You must specify a value for ``DefaultSubnetId`` . For more information about how to use OpsWorks Stacks with a VPC, see `Running a Stack in a VPC <https://docs.aws.amazon.com/opsworks/latest/userguide/workingstacks-vpc.html>`_ . For more information about default VPC and EC2-Classic, see `Supported Platforms <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
            
            # custom_json: Any
            
            cfn_stack_mixin_props = opsworks_mixins.CfnStackMixinProps(
                agent_version="agentVersion",
                attributes={
                    "attributes_key": "attributes"
                },
                chef_configuration=opsworks_mixins.CfnStackPropsMixin.ChefConfigurationProperty(
                    berkshelf_version="berkshelfVersion",
                    manage_berkshelf=False
                ),
                clone_app_ids=["cloneAppIds"],
                clone_permissions=False,
                configuration_manager=opsworks_mixins.CfnStackPropsMixin.StackConfigurationManagerProperty(
                    name="name",
                    version="version"
                ),
                custom_cookbooks_source=opsworks_mixins.CfnStackPropsMixin.SourceProperty(
                    password="password",
                    revision="revision",
                    ssh_key="sshKey",
                    type="type",
                    url="url",
                    username="username"
                ),
                custom_json=custom_json,
                default_availability_zone="defaultAvailabilityZone",
                default_instance_profile_arn="defaultInstanceProfileArn",
                default_os="defaultOs",
                default_root_device_type="defaultRootDeviceType",
                default_ssh_key_name="defaultSshKeyName",
                default_subnet_id="defaultSubnetId",
                ecs_cluster_arn="ecsClusterArn",
                elastic_ips=[opsworks_mixins.CfnStackPropsMixin.ElasticIpProperty(
                    ip="ip",
                    name="name"
                )],
                hostname_theme="hostnameTheme",
                name="name",
                rds_db_instances=[opsworks_mixins.CfnStackPropsMixin.RdsDbInstanceProperty(
                    db_password="dbPassword",
                    db_user="dbUser",
                    rds_db_instance_arn="rdsDbInstanceArn"
                )],
                service_role_arn="serviceRoleArn",
                source_stack_id="sourceStackId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                use_custom_cookbooks=False,
                use_opsworks_security_groups=False,
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb933e262de7f5a6952452c03824f857a66d934abbefd71aee720603ebd361ce)
            check_type(argname="argument agent_version", value=agent_version, expected_type=type_hints["agent_version"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument chef_configuration", value=chef_configuration, expected_type=type_hints["chef_configuration"])
            check_type(argname="argument clone_app_ids", value=clone_app_ids, expected_type=type_hints["clone_app_ids"])
            check_type(argname="argument clone_permissions", value=clone_permissions, expected_type=type_hints["clone_permissions"])
            check_type(argname="argument configuration_manager", value=configuration_manager, expected_type=type_hints["configuration_manager"])
            check_type(argname="argument custom_cookbooks_source", value=custom_cookbooks_source, expected_type=type_hints["custom_cookbooks_source"])
            check_type(argname="argument custom_json", value=custom_json, expected_type=type_hints["custom_json"])
            check_type(argname="argument default_availability_zone", value=default_availability_zone, expected_type=type_hints["default_availability_zone"])
            check_type(argname="argument default_instance_profile_arn", value=default_instance_profile_arn, expected_type=type_hints["default_instance_profile_arn"])
            check_type(argname="argument default_os", value=default_os, expected_type=type_hints["default_os"])
            check_type(argname="argument default_root_device_type", value=default_root_device_type, expected_type=type_hints["default_root_device_type"])
            check_type(argname="argument default_ssh_key_name", value=default_ssh_key_name, expected_type=type_hints["default_ssh_key_name"])
            check_type(argname="argument default_subnet_id", value=default_subnet_id, expected_type=type_hints["default_subnet_id"])
            check_type(argname="argument ecs_cluster_arn", value=ecs_cluster_arn, expected_type=type_hints["ecs_cluster_arn"])
            check_type(argname="argument elastic_ips", value=elastic_ips, expected_type=type_hints["elastic_ips"])
            check_type(argname="argument hostname_theme", value=hostname_theme, expected_type=type_hints["hostname_theme"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rds_db_instances", value=rds_db_instances, expected_type=type_hints["rds_db_instances"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument source_stack_id", value=source_stack_id, expected_type=type_hints["source_stack_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument use_custom_cookbooks", value=use_custom_cookbooks, expected_type=type_hints["use_custom_cookbooks"])
            check_type(argname="argument use_opsworks_security_groups", value=use_opsworks_security_groups, expected_type=type_hints["use_opsworks_security_groups"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if attributes is not None:
            self._values["attributes"] = attributes
        if chef_configuration is not None:
            self._values["chef_configuration"] = chef_configuration
        if clone_app_ids is not None:
            self._values["clone_app_ids"] = clone_app_ids
        if clone_permissions is not None:
            self._values["clone_permissions"] = clone_permissions
        if configuration_manager is not None:
            self._values["configuration_manager"] = configuration_manager
        if custom_cookbooks_source is not None:
            self._values["custom_cookbooks_source"] = custom_cookbooks_source
        if custom_json is not None:
            self._values["custom_json"] = custom_json
        if default_availability_zone is not None:
            self._values["default_availability_zone"] = default_availability_zone
        if default_instance_profile_arn is not None:
            self._values["default_instance_profile_arn"] = default_instance_profile_arn
        if default_os is not None:
            self._values["default_os"] = default_os
        if default_root_device_type is not None:
            self._values["default_root_device_type"] = default_root_device_type
        if default_ssh_key_name is not None:
            self._values["default_ssh_key_name"] = default_ssh_key_name
        if default_subnet_id is not None:
            self._values["default_subnet_id"] = default_subnet_id
        if ecs_cluster_arn is not None:
            self._values["ecs_cluster_arn"] = ecs_cluster_arn
        if elastic_ips is not None:
            self._values["elastic_ips"] = elastic_ips
        if hostname_theme is not None:
            self._values["hostname_theme"] = hostname_theme
        if name is not None:
            self._values["name"] = name
        if rds_db_instances is not None:
            self._values["rds_db_instances"] = rds_db_instances
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn
        if source_stack_id is not None:
            self._values["source_stack_id"] = source_stack_id
        if tags is not None:
            self._values["tags"] = tags
        if use_custom_cookbooks is not None:
            self._values["use_custom_cookbooks"] = use_custom_cookbooks
        if use_opsworks_security_groups is not None:
            self._values["use_opsworks_security_groups"] = use_opsworks_security_groups
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        '''The default OpsWorks Stacks agent version. You have the following options:.

        - Auto-update - Set this parameter to ``LATEST`` . OpsWorks Stacks automatically installs new agent versions on the stack's instances as soon as they are available.
        - Fixed version - Set this parameter to your preferred agent version. To update the agent version, you must edit the stack configuration and specify a new version. OpsWorks Stacks installs that version on the stack's instances.

        The default setting is the most recent release of the agent. To specify an agent version, you must use the complete version number, not the abbreviated number shown on the console. For a list of available agent version numbers, call ``DescribeAgentVersions`` . AgentVersion cannot be set to Chef 12.2.
        .. epigraph::

           You can also specify an agent version when you create or update an instance, which overrides the stack's default setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-agentversion
        '''
        result = self._values.get("agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''One or more user-defined key-value pairs to be added to the stack attributes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def chef_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.ChefConfigurationProperty"]]:
        '''A ``ChefConfiguration`` object that specifies whether to enable Berkshelf and the Berkshelf version on Chef 11.10 stacks. For more information, see `Create a New Stack <https://docs.aws.amazon.com/opsworks/latest/userguide/workingstacks-creating.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-chefconfiguration
        '''
        result = self._values.get("chef_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.ChefConfigurationProperty"]], result)

    @builtins.property
    def clone_app_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''If you're cloning an OpsWorks stack, a list of OpsWorks application stack IDs from the source stack to include in the cloned stack.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-cloneappids
        '''
        result = self._values.get("clone_app_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def clone_permissions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If you're cloning an OpsWorks stack, indicates whether to clone the source stack's permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-clonepermissions
        '''
        result = self._values.get("clone_permissions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def configuration_manager(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.StackConfigurationManagerProperty"]]:
        '''The configuration manager.

        When you create a stack we recommend that you use the configuration manager to specify the Chef version: 12, 11.10, or 11.4 for Linux stacks, or 12.2 for Windows stacks. The default value for Linux stacks is currently 12.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-configurationmanager
        '''
        result = self._values.get("configuration_manager")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.StackConfigurationManagerProperty"]], result)

    @builtins.property
    def custom_cookbooks_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.SourceProperty"]]:
        '''Contains the information required to retrieve an app or cookbook from a repository.

        For more information, see `Adding Apps <https://docs.aws.amazon.com/opsworks/latest/userguide/workingapps-creating.html>`_ or `Cookbooks and Recipes <https://docs.aws.amazon.com/opsworks/latest/userguide/workingcookbook.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-customcookbookssource
        '''
        result = self._values.get("custom_cookbooks_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.SourceProperty"]], result)

    @builtins.property
    def custom_json(self) -> typing.Any:
        '''A string that contains user-defined, custom JSON.

        It can be used to override the corresponding default stack configuration attribute values or to pass data to recipes. The string should be in the following format:

        ``"{\\"key1\\": \\"value1\\", \\"key2\\": \\"value2\\",...}"``

        For more information about custom JSON, see `Use Custom JSON to Modify the Stack Configuration Attributes <https://docs.aws.amazon.com/opsworks/latest/userguide/workingstacks-json.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-customjson
        '''
        result = self._values.get("custom_json")
        return typing.cast(typing.Any, result)

    @builtins.property
    def default_availability_zone(self) -> typing.Optional[builtins.str]:
        '''The stack's default Availability Zone, which must be in the specified region.

        For more information, see `Regions and Endpoints <https://docs.aws.amazon.com/general/latest/gr/rande.html>`_ . If you also specify a value for ``DefaultSubnetId`` , the subnet must be in the same zone. For more information, see the ``VpcId`` parameter description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultavailabilityzone
        '''
        result = self._values.get("default_availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_profile_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM profile that is the default profile for all of the stack's EC2 instances.

        For more information about IAM ARNs, see `Using Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultinstanceprofilearn
        '''
        result = self._values.get("default_instance_profile_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_os(self) -> typing.Optional[builtins.str]:
        '''The stack's default operating system, which is installed on every instance unless you specify a different operating system when you create the instance.

        You can specify one of the following.

        - A supported Linux operating system: An Amazon Linux version, such as ``Amazon Linux 2`` , ``Amazon Linux 2018.03`` , ``Amazon Linux 2017.09`` , ``Amazon Linux 2017.03`` , ``Amazon Linux 2016.09`` , ``Amazon Linux 2016.03`` , ``Amazon Linux 2015.09`` , or ``Amazon Linux 2015.03`` .
        - A supported Ubuntu operating system, such as ``Ubuntu 18.04 LTS`` , ``Ubuntu 16.04 LTS`` , ``Ubuntu 14.04 LTS`` , or ``Ubuntu 12.04 LTS`` .
        - ``CentOS Linux 7``
        - ``Red Hat Enterprise Linux 7``
        - A supported Windows operating system, such as ``Microsoft Windows Server 2012 R2 Base`` , ``Microsoft Windows Server 2012 R2 with SQL Server Express`` , ``Microsoft Windows Server 2012 R2 with SQL Server Standard`` , or ``Microsoft Windows Server 2012 R2 with SQL Server Web`` .
        - A custom AMI: ``Custom`` . You specify the custom AMI you want to use when you create instances. For more information, see `Using Custom AMIs <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-custom-ami.html>`_ .

        The default option is the current Amazon Linux version. Not all operating systems are supported with all versions of Chef. For more information about supported operating systems, see `OpsWorks Stacks Operating Systems <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-os.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultos
        '''
        result = self._values.get("default_os")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_root_device_type(self) -> typing.Optional[builtins.str]:
        '''The default root device type.

        This value is the default for all instances in the stack, but you can override it when you create an instance. The default option is ``instance-store`` . For more information, see `Storage for the Root Device <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultrootdevicetype
        '''
        result = self._values.get("default_root_device_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_ssh_key_name(self) -> typing.Optional[builtins.str]:
        '''A default Amazon EC2 key pair name.

        The default value is none. If you specify a key pair name, OpsWorks installs the public key on the instance and you can use the private key with an SSH client to log in to the instance. For more information, see `Using SSH to Communicate with an Instance <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-ssh.html>`_ and `Managing SSH Access <https://docs.aws.amazon.com/opsworks/latest/userguide/security-ssh-access.html>`_ . You can override this setting by specifying a different key pair, or no key pair, when you `create an instance <https://docs.aws.amazon.com/opsworks/latest/userguide/workinginstances-add.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultsshkeyname
        '''
        result = self._values.get("default_ssh_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_subnet_id(self) -> typing.Optional[builtins.str]:
        '''The stack's default subnet ID.

        All instances are launched into this subnet unless you specify another subnet ID when you create the instance. This parameter is required if you specify a value for the ``VpcId`` parameter. If you also specify a value for ``DefaultAvailabilityZone`` , the subnet must be in that zone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultsubnetid
        '''
        result = self._values.get("default_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecs_cluster_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the  ( Amazon ECS ) cluster to register with the OpsWorks stack.

        .. epigraph::

           If you specify a cluster that's registered with another OpsWorks stack, CloudFormation deregisters the existing association before registering the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-ecsclusterarn
        '''
        result = self._values.get("ecs_cluster_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elastic_ips(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.ElasticIpProperty"]]]]:
        '''A list of Elastic IP addresses to register with the OpsWorks stack.

        .. epigraph::

           If you specify an IP address that's registered with another OpsWorks stack, CloudFormation deregisters the existing association before registering the IP address.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-elasticips
        '''
        result = self._values.get("elastic_ips")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.ElasticIpProperty"]]]], result)

    @builtins.property
    def hostname_theme(self) -> typing.Optional[builtins.str]:
        '''The stack's host name theme, with spaces replaced by underscores.

        The theme is used to generate host names for the stack's instances. By default, ``HostnameTheme`` is set to ``Layer_Dependent`` , which creates host names by appending integers to the layer's short name. The other themes are:

        - ``Baked_Goods``
        - ``Clouds``
        - ``Europe_Cities``
        - ``Fruits``
        - ``Greek_Deities_and_Titans``
        - ``Legendary_creatures_from_Japan``
        - ``Planets_and_Moons``
        - ``Roman_Deities``
        - ``Scottish_Islands``
        - ``US_Cities``
        - ``Wild_Cats``

        To obtain a generated host name, call ``GetHostNameSuggestion`` , which returns a host name based on the current theme.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-hostnametheme
        '''
        result = self._values.get("hostname_theme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The stack name.

        Stack names can be a maximum of 64 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rds_db_instances(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.RdsDbInstanceProperty"]]]]:
        '''The Amazon Relational Database Service ( Amazon RDS ) database instance to register with the OpsWorks stack.

        .. epigraph::

           If you specify a database instance that's registered with another OpsWorks stack, CloudFormation deregisters the existing association before registering the database instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-rdsdbinstances
        '''
        result = self._values.get("rds_db_instances")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackPropsMixin.RdsDbInstanceProperty"]]]], result)

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''The stack's IAM role, which allows OpsWorks Stacks to work with AWS resources on your behalf.

        You must set this parameter to the Amazon Resource Name (ARN) for an existing IAM role. For more information about IAM ARNs, see `Using Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-servicerolearn
        '''
        result = self._values.get("service_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_stack_id(self) -> typing.Optional[builtins.str]:
        '''If you're cloning an OpsWorks stack, the stack ID of the source OpsWorks stack to clone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-sourcestackid
        '''
        result = self._values.get("source_stack_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A map that contains tag keys and tag values that are attached to a stack or layer.

        - The key cannot be empty.
        - The key can be a maximum of 127 characters, and can contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : /``
        - The value can be a maximum 255 characters, and contain only Unicode letters, numbers, or separators, or the following special characters: ``+ - = . _ : /``
        - Leading and trailing white spaces are trimmed from both the key and value.
        - A maximum of 40 tags is allowed for any resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def use_custom_cookbooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether the stack uses custom cookbooks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-usecustomcookbooks
        '''
        result = self._values.get("use_custom_cookbooks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def use_opsworks_security_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to associate the OpsWorks Stacks built-in security groups with the stack's layers.

        OpsWorks Stacks provides a standard set of built-in security groups, one for each layer, which are associated with layers by default. With ``UseOpsworksSecurityGroups`` you can instead provide your own custom security groups. ``UseOpsworksSecurityGroups`` has the following settings:

        - True - OpsWorks Stacks automatically associates the appropriate built-in security group with each layer (default setting). You can associate additional security groups with a layer after you create it, but you cannot delete the built-in security group.
        - False - OpsWorks Stacks does not associate built-in security groups with layers. You must create appropriate EC2 security groups and associate a security group with each layer that you create. However, you can still manually associate a built-in security group with a layer on creation; custom security groups are required only for those layers that need custom settings.

        For more information, see `Create a New Stack <https://docs.aws.amazon.com/opsworks/latest/userguide/workingstacks-creating.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-useopsworkssecuritygroups
        '''
        result = self._values.get("use_opsworks_security_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPC that the stack is to be launched into.

        The VPC must be in the stack's region. All instances are launched into this VPC. You cannot change the ID later.

        - If your account supports EC2-Classic, the default value is ``no VPC`` .
        - If your account does not support EC2-Classic, the default value is the default VPC for the specified region.

        If the VPC ID corresponds to a default VPC and you have specified either the ``DefaultAvailabilityZone`` or the ``DefaultSubnetId`` parameter only, OpsWorks Stacks infers the value of the other parameter. If you specify neither parameter, OpsWorks Stacks sets these parameters to the first valid Availability Zone for the specified region and the corresponding default VPC subnet ID, respectively.

        If you specify a nondefault VPC ID, note the following:

        - It must belong to a VPC in your account that is in the specified region.
        - You must specify a value for ``DefaultSubnetId`` .

        For more information about how to use OpsWorks Stacks with a VPC, see `Running a Stack in a VPC <https://docs.aws.amazon.com/opsworks/latest/userguide/workingstacks-vpc.html>`_ . For more information about default VPC and EC2-Classic, see `Supported Platforms <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-supported-platforms.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnStackPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html
    :cloudformationResource: AWS::OpsWorks::Stack
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
        
        # custom_json: Any
        
        cfn_stack_props_mixin = opsworks_mixins.CfnStackPropsMixin(opsworks_mixins.CfnStackMixinProps(
            agent_version="agentVersion",
            attributes={
                "attributes_key": "attributes"
            },
            chef_configuration=opsworks_mixins.CfnStackPropsMixin.ChefConfigurationProperty(
                berkshelf_version="berkshelfVersion",
                manage_berkshelf=False
            ),
            clone_app_ids=["cloneAppIds"],
            clone_permissions=False,
            configuration_manager=opsworks_mixins.CfnStackPropsMixin.StackConfigurationManagerProperty(
                name="name",
                version="version"
            ),
            custom_cookbooks_source=opsworks_mixins.CfnStackPropsMixin.SourceProperty(
                password="password",
                revision="revision",
                ssh_key="sshKey",
                type="type",
                url="url",
                username="username"
            ),
            custom_json=custom_json,
            default_availability_zone="defaultAvailabilityZone",
            default_instance_profile_arn="defaultInstanceProfileArn",
            default_os="defaultOs",
            default_root_device_type="defaultRootDeviceType",
            default_ssh_key_name="defaultSshKeyName",
            default_subnet_id="defaultSubnetId",
            ecs_cluster_arn="ecsClusterArn",
            elastic_ips=[opsworks_mixins.CfnStackPropsMixin.ElasticIpProperty(
                ip="ip",
                name="name"
            )],
            hostname_theme="hostnameTheme",
            name="name",
            rds_db_instances=[opsworks_mixins.CfnStackPropsMixin.RdsDbInstanceProperty(
                db_password="dbPassword",
                db_user="dbUser",
                rds_db_instance_arn="rdsDbInstanceArn"
            )],
            service_role_arn="serviceRoleArn",
            source_stack_id="sourceStackId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            use_custom_cookbooks=False,
            use_opsworks_security_groups=False,
            vpc_id="vpcId"
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
        '''Create a mixin to apply properties to ``AWS::OpsWorks::Stack``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa83fd0e2d9f0e58d8d64924c7000d61cad4d1dbf0c15d15d885386f9c6f01a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b22be320d928085e7dd6cdd7670fd7c1575c4700d493406957bc15c12d843790)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a8f116ffe6bf99abaaba2ffb5750975b3a81ac3123a739888bf4568c55705e)
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
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnStackPropsMixin.ChefConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "berkshelf_version": "berkshelfVersion",
            "manage_berkshelf": "manageBerkshelf",
        },
    )
    class ChefConfigurationProperty:
        def __init__(
            self,
            *,
            berkshelf_version: typing.Optional[builtins.str] = None,
            manage_berkshelf: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param berkshelf_version: The Berkshelf version.
            :param manage_berkshelf: Whether to enable Berkshelf.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                chef_configuration_property = opsworks_mixins.CfnStackPropsMixin.ChefConfigurationProperty(
                    berkshelf_version="berkshelfVersion",
                    manage_berkshelf=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0064b9e039f96149bd08b218ff6324642f54b899f4db721401d0cbd4de54e01)
                check_type(argname="argument berkshelf_version", value=berkshelf_version, expected_type=type_hints["berkshelf_version"])
                check_type(argname="argument manage_berkshelf", value=manage_berkshelf, expected_type=type_hints["manage_berkshelf"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if berkshelf_version is not None:
                self._values["berkshelf_version"] = berkshelf_version
            if manage_berkshelf is not None:
                self._values["manage_berkshelf"] = manage_berkshelf

        @builtins.property
        def berkshelf_version(self) -> typing.Optional[builtins.str]:
            '''The Berkshelf version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html#cfn-opsworks-stack-chefconfiguration-berkshelfversion
            '''
            result = self._values.get("berkshelf_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manage_berkshelf(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to enable Berkshelf.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html#cfn-opsworks-stack-chefconfiguration-manageberkshelf
            '''
            result = self._values.get("manage_berkshelf")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChefConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnStackPropsMixin.ElasticIpProperty",
        jsii_struct_bases=[],
        name_mapping={"ip": "ip", "name": "name"},
    )
    class ElasticIpProperty:
        def __init__(
            self,
            *,
            ip: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param ip: The IP address.
            :param name: The name, which can be a maximum of 32 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                elastic_ip_property = opsworks_mixins.CfnStackPropsMixin.ElasticIpProperty(
                    ip="ip",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__005b250f1ca4f108add7c355387f84efd55e6e7c05118f730f76c8992e0166eb)
                check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip is not None:
                self._values["ip"] = ip
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def ip(self) -> typing.Optional[builtins.str]:
            '''The IP address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html#cfn-opsworks-stack-elasticip-ip
            '''
            result = self._values.get("ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name, which can be a maximum of 32 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html#cfn-opsworks-stack-elasticip-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticIpProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnStackPropsMixin.RdsDbInstanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "db_password": "dbPassword",
            "db_user": "dbUser",
            "rds_db_instance_arn": "rdsDbInstanceArn",
        },
    )
    class RdsDbInstanceProperty:
        def __init__(
            self,
            *,
            db_password: typing.Optional[builtins.str] = None,
            db_user: typing.Optional[builtins.str] = None,
            rds_db_instance_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param db_password: OpsWorks Stacks returns ``*****FILTERED*****`` instead of the actual value.
            :param db_user: The master user name.
            :param rds_db_instance_arn: The instance's ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                rds_db_instance_property = opsworks_mixins.CfnStackPropsMixin.RdsDbInstanceProperty(
                    db_password="dbPassword",
                    db_user="dbUser",
                    rds_db_instance_arn="rdsDbInstanceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__651d164d1d14a2cd83d19503e0a7f5dcf73a4928c26e77744cad919d5d031ecc)
                check_type(argname="argument db_password", value=db_password, expected_type=type_hints["db_password"])
                check_type(argname="argument db_user", value=db_user, expected_type=type_hints["db_user"])
                check_type(argname="argument rds_db_instance_arn", value=rds_db_instance_arn, expected_type=type_hints["rds_db_instance_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if db_password is not None:
                self._values["db_password"] = db_password
            if db_user is not None:
                self._values["db_user"] = db_user
            if rds_db_instance_arn is not None:
                self._values["rds_db_instance_arn"] = rds_db_instance_arn

        @builtins.property
        def db_password(self) -> typing.Optional[builtins.str]:
            '''OpsWorks Stacks returns ``*****FILTERED*****`` instead of the actual value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-dbpassword
            '''
            result = self._values.get("db_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def db_user(self) -> typing.Optional[builtins.str]:
            '''The master user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-dbuser
            '''
            result = self._values.get("db_user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rds_db_instance_arn(self) -> typing.Optional[builtins.str]:
            '''The instance's ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-rdsdbinstancearn
            '''
            result = self._values.get("rds_db_instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RdsDbInstanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnStackPropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "revision": "revision",
            "ssh_key": "sshKey",
            "type": "type",
            "url": "url",
            "username": "username",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            revision: typing.Optional[builtins.str] = None,
            ssh_key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param password: When included in a request, the parameter depends on the repository type. - For Amazon S3 bundles, set ``Password`` to the appropriate IAM secret access key. - For HTTP bundles and Subversion repositories, set ``Password`` to the password. For more information on how to safely handle IAM credentials, see ` <https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html>`_ . In responses, OpsWorks Stacks returns ``*****FILTERED*****`` instead of the actual value.
            :param revision: The application's version. OpsWorks Stacks enables you to easily deploy new versions of an application. One of the simplest approaches is to have branches or revisions in your repository that represent different versions that can potentially be deployed.
            :param ssh_key: The repository's SSH key. For more information, see `Using Git Repository SSH Keys <https://docs.aws.amazon.com/opsworks/latest/userguide/workingapps-deploykeys.html>`_ in the *OpsWorks User Guide* . To pass in an SSH key as a parameter, see the following example: ``"Parameters" : { "GitSSHKey" : { "Description" : "Change SSH key newlines to commas.", "Type" : "CommaDelimitedList", "NoEcho" : "true" }, ... "CustomCookbooksSource": { "Revision" : { "Ref": "GitRevision"}, "SshKey" : { "Fn::Join" : [ "\\n", { "Ref": "GitSSHKey"} ] }, "Type": "git", "Url": { "Ref": "GitURL"} } ...``
            :param type: The repository type.
            :param url: The source URL. The following is an example of an Amazon S3 source URL: ``https://s3.amazonaws.com/opsworks-demo-bucket/opsworks_cookbook_demo.tar.gz`` .
            :param username: This parameter depends on the repository type. - For Amazon S3 bundles, set ``Username`` to the appropriate IAM access key ID. - For HTTP bundles, Git repositories, and Subversion repositories, set ``Username`` to the user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                source_property = opsworks_mixins.CfnStackPropsMixin.SourceProperty(
                    password="password",
                    revision="revision",
                    ssh_key="sshKey",
                    type="type",
                    url="url",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85c5596ecaeb7b1534e4a348367ce64ebd065c5b610c4b2e3cb72237423e8610)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
                check_type(argname="argument ssh_key", value=ssh_key, expected_type=type_hints["ssh_key"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if revision is not None:
                self._values["revision"] = revision
            if ssh_key is not None:
                self._values["ssh_key"] = ssh_key
            if type is not None:
                self._values["type"] = type
            if url is not None:
                self._values["url"] = url
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''When included in a request, the parameter depends on the repository type.

            - For Amazon S3 bundles, set ``Password`` to the appropriate IAM secret access key.
            - For HTTP bundles and Subversion repositories, set ``Password`` to the password.

            For more information on how to safely handle IAM credentials, see ` <https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html>`_ .

            In responses, OpsWorks Stacks returns ``*****FILTERED*****`` instead of the actual value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-stack-source-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def revision(self) -> typing.Optional[builtins.str]:
            '''The application's version.

            OpsWorks Stacks enables you to easily deploy new versions of an application. One of the simplest approaches is to have branches or revisions in your repository that represent different versions that can potentially be deployed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-stack-source-revision
            '''
            result = self._values.get("revision")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssh_key(self) -> typing.Optional[builtins.str]:
            '''The repository's SSH key.

            For more information, see `Using Git Repository SSH Keys <https://docs.aws.amazon.com/opsworks/latest/userguide/workingapps-deploykeys.html>`_ in the *OpsWorks User Guide* . To pass in an SSH key as a parameter, see the following example:

            ``"Parameters" : { "GitSSHKey" : { "Description" : "Change SSH key newlines to commas.", "Type" : "CommaDelimitedList", "NoEcho" : "true" }, ... "CustomCookbooksSource": { "Revision" : { "Ref": "GitRevision"}, "SshKey" : { "Fn::Join" : [ "\\n", { "Ref": "GitSSHKey"} ] }, "Type": "git", "Url": { "Ref": "GitURL"} } ...``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-stack-source-sshkey
            '''
            result = self._values.get("ssh_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The repository type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-stack-source-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The source URL.

            The following is an example of an Amazon S3 source URL: ``https://s3.amazonaws.com/opsworks-demo-bucket/opsworks_cookbook_demo.tar.gz`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-stack-source-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''This parameter depends on the repository type.

            - For Amazon S3 bundles, set ``Username`` to the appropriate IAM access key ID.
            - For HTTP bundles, Git repositories, and Subversion repositories, set ``Username`` to the user name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-stack-source-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnStackPropsMixin.StackConfigurationManagerProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class StackConfigurationManagerProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: The name. This parameter must be set to ``Chef`` .
            :param version: The Chef version. This parameter must be set to 12, 11.10, or 11.4 for Linux stacks, and to 12.2 for Windows stacks. The default value for Linux stacks is 12.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigurationmanager.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
                
                stack_configuration_manager_property = opsworks_mixins.CfnStackPropsMixin.StackConfigurationManagerProperty(
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f7eb3c4c1008c70c3036c85fe97215325031d31ac2e9747cff8a540f26beaeb)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name.

            This parameter must be set to ``Chef`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigurationmanager.html#cfn-opsworks-stack-stackconfigurationmanager-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The Chef version.

            This parameter must be set to 12, 11.10, or 11.4 for Linux stacks, and to 12.2 for Windows stacks. The default value for Linux stacks is 12.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigurationmanager.html#cfn-opsworks-stack-stackconfigurationmanager-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackConfigurationManagerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnUserProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_self_management": "allowSelfManagement",
        "iam_user_arn": "iamUserArn",
        "ssh_public_key": "sshPublicKey",
        "ssh_username": "sshUsername",
    },
)
class CfnUserProfileMixinProps:
    def __init__(
        self,
        *,
        allow_self_management: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        iam_user_arn: typing.Optional[builtins.str] = None,
        ssh_public_key: typing.Optional[builtins.str] = None,
        ssh_username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserProfilePropsMixin.

        :param allow_self_management: Whether users can specify their own SSH public key through the My Settings page. For more information, see `Managing User Permissions <https://docs.aws.amazon.com/opsworks/latest/userguide/security-settingsshkey.html>`_ .
        :param iam_user_arn: The user's IAM ARN.
        :param ssh_public_key: The user's SSH public key.
        :param ssh_username: The user's SSH user name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
            
            cfn_user_profile_mixin_props = opsworks_mixins.CfnUserProfileMixinProps(
                allow_self_management=False,
                iam_user_arn="iamUserArn",
                ssh_public_key="sshPublicKey",
                ssh_username="sshUsername"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05b0a190b440b3f7931864139ac58692277818872fdb0b0de259d27366e95b4)
            check_type(argname="argument allow_self_management", value=allow_self_management, expected_type=type_hints["allow_self_management"])
            check_type(argname="argument iam_user_arn", value=iam_user_arn, expected_type=type_hints["iam_user_arn"])
            check_type(argname="argument ssh_public_key", value=ssh_public_key, expected_type=type_hints["ssh_public_key"])
            check_type(argname="argument ssh_username", value=ssh_username, expected_type=type_hints["ssh_username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_self_management is not None:
            self._values["allow_self_management"] = allow_self_management
        if iam_user_arn is not None:
            self._values["iam_user_arn"] = iam_user_arn
        if ssh_public_key is not None:
            self._values["ssh_public_key"] = ssh_public_key
        if ssh_username is not None:
            self._values["ssh_username"] = ssh_username

    @builtins.property
    def allow_self_management(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether users can specify their own SSH public key through the My Settings page.

        For more information, see `Managing User Permissions <https://docs.aws.amazon.com/opsworks/latest/userguide/security-settingsshkey.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-allowselfmanagement
        '''
        result = self._values.get("allow_self_management")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def iam_user_arn(self) -> typing.Optional[builtins.str]:
        '''The user's IAM ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-iamuserarn
        '''
        result = self._values.get("iam_user_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_public_key(self) -> typing.Optional[builtins.str]:
        '''The user's SSH public key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshpublickey
        '''
        result = self._values.get("ssh_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_username(self) -> typing.Optional[builtins.str]:
        '''The user's SSH user name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshusername
        '''
        result = self._values.get("ssh_username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnUserProfilePropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html
    :cloudformationResource: AWS::OpsWorks::UserProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
        
        cfn_user_profile_props_mixin = opsworks_mixins.CfnUserProfilePropsMixin(opsworks_mixins.CfnUserProfileMixinProps(
            allow_self_management=False,
            iam_user_arn="iamUserArn",
            ssh_public_key="sshPublicKey",
            ssh_username="sshUsername"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpsWorks::UserProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfb362836c55ed80e936913fec07a3093ad3fc496bcdf7ed3f25ab2e9fbcced1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dad16673274770617a9bc0f45e63477dc98071cc82712249682595838f6c8608)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad6fe4b137e01df219ce05d673314ac5dfb1ae0d4b7da5cefdb82bc8ebcf33d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserProfileMixinProps:
        return typing.cast(CfnUserProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnVolumeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ec2_volume_id": "ec2VolumeId",
        "mount_point": "mountPoint",
        "name": "name",
        "stack_id": "stackId",
    },
)
class CfnVolumeMixinProps:
    def __init__(
        self,
        *,
        ec2_volume_id: typing.Optional[builtins.str] = None,
        mount_point: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        stack_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVolumePropsMixin.

        :param ec2_volume_id: The Amazon EC2 volume ID.
        :param mount_point: The volume mount point. For example, "/mnt/disk1".
        :param name: The volume name. Volume names are a maximum of 128 characters.
        :param stack_id: The stack ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
            
            cfn_volume_mixin_props = opsworks_mixins.CfnVolumeMixinProps(
                ec2_volume_id="ec2VolumeId",
                mount_point="mountPoint",
                name="name",
                stack_id="stackId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a360bea7fcc3914f280b7c8f76920b832bdfd2a407486185825deeb319fe1760)
            check_type(argname="argument ec2_volume_id", value=ec2_volume_id, expected_type=type_hints["ec2_volume_id"])
            check_type(argname="argument mount_point", value=mount_point, expected_type=type_hints["mount_point"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ec2_volume_id is not None:
            self._values["ec2_volume_id"] = ec2_volume_id
        if mount_point is not None:
            self._values["mount_point"] = mount_point
        if name is not None:
            self._values["name"] = name
        if stack_id is not None:
            self._values["stack_id"] = stack_id

    @builtins.property
    def ec2_volume_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 volume ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-ec2volumeid
        '''
        result = self._values.get("ec2_volume_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mount_point(self) -> typing.Optional[builtins.str]:
        '''The volume mount point.

        For example, "/mnt/disk1".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-mountpoint
        '''
        result = self._values.get("mount_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The volume name.

        Volume names are a maximum of 128 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_id(self) -> typing.Optional[builtins.str]:
        '''The stack ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-stackid
        '''
        result = self._values.get("stack_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVolumeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVolumePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_opsworks.mixins.CfnVolumePropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html
    :cloudformationResource: AWS::OpsWorks::Volume
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_opsworks import mixins as opsworks_mixins
        
        cfn_volume_props_mixin = opsworks_mixins.CfnVolumePropsMixin(opsworks_mixins.CfnVolumeMixinProps(
            ec2_volume_id="ec2VolumeId",
            mount_point="mountPoint",
            name="name",
            stack_id="stackId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVolumeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::OpsWorks::Volume``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4cdc40edf0f4bab7e55a1365bc4acb10217a32ff0f6efe0a7eb6143a568acd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4ed0ecb5b0844cc31650096d9060a373858beb47105be2c837755e49e4d254b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf70aea28c8c06a870b003fbba0426a127d90eac355f5ad6fb466b203c4314e8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVolumeMixinProps:
        return typing.cast(CfnVolumeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAppMixinProps",
    "CfnAppPropsMixin",
    "CfnElasticLoadBalancerAttachmentMixinProps",
    "CfnElasticLoadBalancerAttachmentPropsMixin",
    "CfnInstanceMixinProps",
    "CfnInstancePropsMixin",
    "CfnLayerMixinProps",
    "CfnLayerPropsMixin",
    "CfnStackMixinProps",
    "CfnStackPropsMixin",
    "CfnUserProfileMixinProps",
    "CfnUserProfilePropsMixin",
    "CfnVolumeMixinProps",
    "CfnVolumePropsMixin",
]

publication.publish()

def _typecheckingstub__56a0e54bad443e9f37f3d08e982af92e4c0d4050f84813c7d8b0fa602bb082e0(
    *,
    app_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    data_sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.DataSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_ssl: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    shortname: typing.Optional[builtins.str] = None,
    ssl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.SslConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stack_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef527aeec828773bf2844eb14201792c89b00d89543dffca0c8f1acf54e9e50d(
    props: typing.Union[CfnAppMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0f1adf73b36a3c5127876169face74ec978842575ec94ce6ec9f1d1989c9b4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb002427b5e037fdaec6e2579d27e091e3b5fa8ff66a6433e10e8a88141976d3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e5935aff8c920a1158ccba84220c90337b91c6f789cfb7c171eae4dac5ec47(
    *,
    arn: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ff39d76264be19370d9eb098819836270ad4aaa3fbecc859a952b16894dae0(
    *,
    key: typing.Optional[builtins.str] = None,
    secure: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1196cf9927815a8c26734d83cadcd752571097a31346dbad2f0ad146ddb41e7e(
    *,
    password: typing.Optional[builtins.str] = None,
    revision: typing.Optional[builtins.str] = None,
    ssh_key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211a775322b0e21cbdfc24be0aad50b503466c9c50ab97ab292d310c6334d360(
    *,
    certificate: typing.Optional[builtins.str] = None,
    chain: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e188ad118bf61c05eb87cecf79cd3fe0a7d31ccf5f5ee90cab14554732a17bc(
    *,
    elastic_load_balancer_name: typing.Optional[builtins.str] = None,
    layer_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa5e71c391d8e35dac5e90f70aa3fddf53f77e55ef8f4b38010fa6d1d04ff3a(
    props: typing.Union[CfnElasticLoadBalancerAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc88a7e350838912534a914f1c8c336096e15f25ee8ab83c3ee1c740a33d71e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__561356eea75fcb54a9ec66ae5ff6a5ec55325ebd149f0d903e7fab97218f08b1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a24386e63afbcac332e48fea6ab9d26700a5057ab8ec49cdec0a11b14af693(
    *,
    agent_version: typing.Optional[builtins.str] = None,
    ami_id: typing.Optional[builtins.str] = None,
    architecture: typing.Optional[builtins.str] = None,
    auto_scaling_type: typing.Optional[builtins.str] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    elastic_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    hostname: typing.Optional[builtins.str] = None,
    install_updates_on_boot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    layer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    os: typing.Optional[builtins.str] = None,
    root_device_type: typing.Optional[builtins.str] = None,
    ssh_key_name: typing.Optional[builtins.str] = None,
    stack_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tenancy: typing.Optional[builtins.str] = None,
    time_based_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.TimeBasedAutoScalingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtualization_type: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647b45ee490b1a37f9f9ce98867161533c5dfe2afe10730970d653004d18674a(
    props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c629249eca5a64a8cc473128268d460a7ad55b1c410417785be6b5ada2ff84b8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8c689083be869abc5ffddc3fc42bc57926f98cce9b42972a92748533ed8304(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba80c5e650f27c22f883eed40dcd1d5c0c9b9f3f95b07cf5554645570bcaa76(
    *,
    device_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.EbsBlockDeviceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    no_device: typing.Optional[builtins.str] = None,
    virtual_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dedd2b0679b62402c70a92193ed6fcfb66c6d9a5c01810141b46495a30222dd0(
    *,
    delete_on_termination: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7d2e8fbea71f6d83f9f4f65613a74f9b181967268619b8f0b1943ea36db860(
    *,
    friday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    monday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    saturday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    sunday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    thursday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    tuesday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    wednesday: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ccb68cbc18c6d96b0eb5c724b8dfe1899bd2d85edc58bb113e20042a026376(
    *,
    attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    auto_assign_elastic_ips: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    auto_assign_public_ips: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    custom_instance_profile_arn: typing.Optional[builtins.str] = None,
    custom_json: typing.Any = None,
    custom_recipes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLayerPropsMixin.RecipesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_auto_healing: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    install_updates_on_boot: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    lifecycle_event_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLayerPropsMixin.LifecycleEventConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    load_based_auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLayerPropsMixin.LoadBasedAutoScalingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    shortname: typing.Optional[builtins.str] = None,
    stack_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    use_ebs_optimized_instances: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    volume_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLayerPropsMixin.VolumeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b47bb06b9c94b588cedfb15607b5a1fa1f7d11cc0e5a833689a4f9b51b84a01(
    props: typing.Union[CfnLayerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb5f98f7ca330e67fb08d0b3f7fad9c0a015428594984dc8f0112fb959ede69(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27197eba6098d3b0ec0aa8d7178e026a2f810f6af5a67aa20aba2ee9b73a13e2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd88cdea05e245498039c4c732d99833d01e6109a5148f88b6fde11262f13062(
    *,
    cpu_threshold: typing.Optional[jsii.Number] = None,
    ignore_metrics_time: typing.Optional[jsii.Number] = None,
    instance_count: typing.Optional[jsii.Number] = None,
    load_threshold: typing.Optional[jsii.Number] = None,
    memory_threshold: typing.Optional[jsii.Number] = None,
    thresholds_wait_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7ed848eefb0c31a672f49417ab69d3b6989ec755ee3da7a82d1bdf498edeb1(
    *,
    shutdown_event_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLayerPropsMixin.ShutdownEventConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17d7a5a4f09b6289b36517c635b24b470c0cded1bd85885193f38b6431fece38(
    *,
    down_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLayerPropsMixin.AutoScalingThresholdsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    up_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLayerPropsMixin.AutoScalingThresholdsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9634cc89c8c23d46cc2a888071e72c14db74d1a3b6386148e45de2ff00dd62be(
    *,
    configure: typing.Optional[typing.Sequence[builtins.str]] = None,
    deploy: typing.Optional[typing.Sequence[builtins.str]] = None,
    setup: typing.Optional[typing.Sequence[builtins.str]] = None,
    shutdown: typing.Optional[typing.Sequence[builtins.str]] = None,
    undeploy: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8deb4c7236b02983da71b425282ab6fc7f6199b9c923882eeb79987c4b4e2048(
    *,
    delay_until_elb_connections_drained: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    execution_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e5503fb9c874df155881fa7cba7b3f015ec8d13754b5f1cabcf946f494d4f6(
    *,
    encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    mount_point: typing.Optional[builtins.str] = None,
    number_of_disks: typing.Optional[jsii.Number] = None,
    raid_level: typing.Optional[jsii.Number] = None,
    size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb933e262de7f5a6952452c03824f857a66d934abbefd71aee720603ebd361ce(
    *,
    agent_version: typing.Optional[builtins.str] = None,
    attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    chef_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.ChefConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    clone_app_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    clone_permissions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    configuration_manager: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.StackConfigurationManagerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_cookbooks_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_json: typing.Any = None,
    default_availability_zone: typing.Optional[builtins.str] = None,
    default_instance_profile_arn: typing.Optional[builtins.str] = None,
    default_os: typing.Optional[builtins.str] = None,
    default_root_device_type: typing.Optional[builtins.str] = None,
    default_ssh_key_name: typing.Optional[builtins.str] = None,
    default_subnet_id: typing.Optional[builtins.str] = None,
    ecs_cluster_arn: typing.Optional[builtins.str] = None,
    elastic_ips: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.ElasticIpProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    hostname_theme: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rds_db_instances: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackPropsMixin.RdsDbInstanceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
    source_stack_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_custom_cookbooks: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_opsworks_security_groups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa83fd0e2d9f0e58d8d64924c7000d61cad4d1dbf0c15d15d885386f9c6f01a0(
    props: typing.Union[CfnStackMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22be320d928085e7dd6cdd7670fd7c1575c4700d493406957bc15c12d843790(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a8f116ffe6bf99abaaba2ffb5750975b3a81ac3123a739888bf4568c55705e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0064b9e039f96149bd08b218ff6324642f54b899f4db721401d0cbd4de54e01(
    *,
    berkshelf_version: typing.Optional[builtins.str] = None,
    manage_berkshelf: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005b250f1ca4f108add7c355387f84efd55e6e7c05118f730f76c8992e0166eb(
    *,
    ip: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651d164d1d14a2cd83d19503e0a7f5dcf73a4928c26e77744cad919d5d031ecc(
    *,
    db_password: typing.Optional[builtins.str] = None,
    db_user: typing.Optional[builtins.str] = None,
    rds_db_instance_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85c5596ecaeb7b1534e4a348367ce64ebd065c5b610c4b2e3cb72237423e8610(
    *,
    password: typing.Optional[builtins.str] = None,
    revision: typing.Optional[builtins.str] = None,
    ssh_key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7eb3c4c1008c70c3036c85fe97215325031d31ac2e9747cff8a540f26beaeb(
    *,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05b0a190b440b3f7931864139ac58692277818872fdb0b0de259d27366e95b4(
    *,
    allow_self_management: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iam_user_arn: typing.Optional[builtins.str] = None,
    ssh_public_key: typing.Optional[builtins.str] = None,
    ssh_username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb362836c55ed80e936913fec07a3093ad3fc496bcdf7ed3f25ab2e9fbcced1(
    props: typing.Union[CfnUserProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad16673274770617a9bc0f45e63477dc98071cc82712249682595838f6c8608(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad6fe4b137e01df219ce05d673314ac5dfb1ae0d4b7da5cefdb82bc8ebcf33d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a360bea7fcc3914f280b7c8f76920b832bdfd2a407486185825deeb319fe1760(
    *,
    ec2_volume_id: typing.Optional[builtins.str] = None,
    mount_point: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    stack_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4cdc40edf0f4bab7e55a1365bc4acb10217a32ff0f6efe0a7eb6143a568acd(
    props: typing.Union[CfnVolumeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ed0ecb5b0844cc31650096d9060a373858beb47105be2c837755e49e4d254b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf70aea28c8c06a870b003fbba0426a127d90eac355f5ad6fb466b203c4314e8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
