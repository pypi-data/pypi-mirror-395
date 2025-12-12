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
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnAccountMixinProps",
    jsii_struct_bases=[],
    name_mapping={"cloud_watch_role_arn": "cloudWatchRoleArn"},
)
class CfnAccountMixinProps:
    def __init__(
        self,
        *,
        cloud_watch_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAccountPropsMixin.

        :param cloud_watch_role_arn: The ARN of an Amazon CloudWatch role for the current Account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-account.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_account_mixin_props = apigateway_mixins.CfnAccountMixinProps(
                cloud_watch_role_arn="cloudWatchRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ae4ef4012c2ddb5f9a2fe2e77835b7caae1e76220f418a13a94808c188f495)
            check_type(argname="argument cloud_watch_role_arn", value=cloud_watch_role_arn, expected_type=type_hints["cloud_watch_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_watch_role_arn is not None:
            self._values["cloud_watch_role_arn"] = cloud_watch_role_arn

    @builtins.property
    def cloud_watch_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an Amazon CloudWatch role for the current Account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-account.html#cfn-apigateway-account-cloudwatchrolearn
        '''
        result = self._values.get("cloud_watch_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccountMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccountPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnAccountPropsMixin",
):
    '''The ``AWS::ApiGateway::Account`` resource specifies the IAM role that Amazon API Gateway uses to write API logs to Amazon CloudWatch Logs.

    To avoid overwriting other roles, you should only have one ``AWS::ApiGateway::Account`` resource per region per account.

    When you delete a stack containing this resource, API Gateway can still assume the provided IAM role to write API logs to CloudWatch Logs. To deny API Gateway access to write API logs to CloudWatch logs, update the permissions policies or change the IAM role to deny access.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-account.html
    :cloudformationResource: AWS::ApiGateway::Account
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_account_props_mixin = apigateway_mixins.CfnAccountPropsMixin(apigateway_mixins.CfnAccountMixinProps(
            cloud_watch_role_arn="cloudWatchRoleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccountMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::Account``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9fb8ed77b3acd1132807e2d8f7501879a148d594bf09869f1263ce388fcf85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd3b5f0743e2fdc1ccaf76cfe0acaf4de41b11c1bae0d9f93ed334fd58c796c2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be175413c0997e42b8eac3aa03a079cdb90043026798c50e491452a9cc0ab4c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccountMixinProps:
        return typing.cast(CfnAccountMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnApiKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "customer_id": "customerId",
        "description": "description",
        "enabled": "enabled",
        "generate_distinct_id": "generateDistinctId",
        "name": "name",
        "stage_keys": "stageKeys",
        "tags": "tags",
        "value": "value",
    },
)
class CfnApiKeyMixinProps:
    def __init__(
        self,
        *,
        customer_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        generate_distinct_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        stage_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApiKeyPropsMixin.StageKeyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnApiKeyPropsMixin.

        :param customer_id: An AWS Marketplace customer identifier, when integrating with the AWS SaaS Marketplace.
        :param description: The description of the ApiKey.
        :param enabled: Specifies whether the ApiKey can be used by callers. Default: - false
        :param generate_distinct_id: Specifies whether ( ``true`` ) or not ( ``false`` ) the key identifier is distinct from the created API key value. This parameter is deprecated and should not be used.
        :param name: A name for the API key. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the API key name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param stage_keys: DEPRECATED FOR USAGE PLANS - Specifies stages associated with the API key.
        :param tags: The key-value map of strings. The valid character set is [a-zA-Z+-=._:/]. The tag key can be up to 128 characters and must not start with ``aws:`` . The tag value can be up to 256 characters.
        :param value: Specifies a value of the API key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_api_key_mixin_props = apigateway_mixins.CfnApiKeyMixinProps(
                customer_id="customerId",
                description="description",
                enabled=False,
                generate_distinct_id=False,
                name="name",
                stage_keys=[apigateway_mixins.CfnApiKeyPropsMixin.StageKeyProperty(
                    rest_api_id="restApiId",
                    stage_name="stageName"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40a9ec618f0dc58c25ffe419ef733f1397d2a97286d49c9af11df9c4728bf7d)
            check_type(argname="argument customer_id", value=customer_id, expected_type=type_hints["customer_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument generate_distinct_id", value=generate_distinct_id, expected_type=type_hints["generate_distinct_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stage_keys", value=stage_keys, expected_type=type_hints["stage_keys"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if customer_id is not None:
            self._values["customer_id"] = customer_id
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if generate_distinct_id is not None:
            self._values["generate_distinct_id"] = generate_distinct_id
        if name is not None:
            self._values["name"] = name
        if stage_keys is not None:
            self._values["stage_keys"] = stage_keys
        if tags is not None:
            self._values["tags"] = tags
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def customer_id(self) -> typing.Optional[builtins.str]:
        '''An AWS Marketplace customer identifier, when integrating with the AWS SaaS Marketplace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-customerid
        '''
        result = self._values.get("customer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the ApiKey.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the ApiKey can be used by callers.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def generate_distinct_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether ( ``true`` ) or not ( ``false`` ) the key identifier is distinct from the created API key value.

        This parameter is deprecated and should not be used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-generatedistinctid
        '''
        result = self._values.get("generate_distinct_id")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the API key.

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the API key name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_keys(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiKeyPropsMixin.StageKeyProperty"]]]]:
        '''DEPRECATED FOR USAGE PLANS - Specifies stages associated with the API key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-stagekeys
        '''
        result = self._values.get("stage_keys")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApiKeyPropsMixin.StageKeyProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The key-value map of strings.

        The valid character set is [a-zA-Z+-=._:/]. The tag key can be up to 128 characters and must not start with ``aws:`` . The tag value can be up to 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Specifies a value of the API key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html#cfn-apigateway-apikey-value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApiKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApiKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnApiKeyPropsMixin",
):
    '''The ``AWS::ApiGateway::ApiKey`` resource creates a unique key that you can distribute to clients who are executing API Gateway ``Method`` resources that require an API key.

    To specify which API key clients must use, map the API key with the ``RestApi`` and ``Stage`` resources that include the methods that require a key.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html
    :cloudformationResource: AWS::ApiGateway::ApiKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_api_key_props_mixin = apigateway_mixins.CfnApiKeyPropsMixin(apigateway_mixins.CfnApiKeyMixinProps(
            customer_id="customerId",
            description="description",
            enabled=False,
            generate_distinct_id=False,
            name="name",
            stage_keys=[apigateway_mixins.CfnApiKeyPropsMixin.StageKeyProperty(
                rest_api_id="restApiId",
                stage_name="stageName"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            value="value"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApiKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::ApiKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c6ef21cefaa9f4ec0caa0dde5abe9948201a3fa0b021587ec530cfac3ff0687)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb108cacc891782cc9bd7cd0a5eb77cec31b2e18719d7f6ab735e075ce81e3c2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b12b197e3c4cf77d867dc3e7ca2776aaf20fb390f89b544230ca4b5220d98f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApiKeyMixinProps:
        return typing.cast(CfnApiKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnApiKeyPropsMixin.StageKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"rest_api_id": "restApiId", "stage_name": "stageName"},
    )
    class StageKeyProperty:
        def __init__(
            self,
            *,
            rest_api_id: typing.Optional[builtins.str] = None,
            stage_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``StageKey`` is a property of the `AWS::ApiGateway::ApiKey <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-apikey.html>`_ resource that specifies the stage to associate with the API key. This association allows only clients with the key to make requests to methods in that stage.

            :param rest_api_id: The string identifier of the associated RestApi.
            :param stage_name: The stage name associated with the stage key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-apikey-stagekey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                stage_key_property = apigateway_mixins.CfnApiKeyPropsMixin.StageKeyProperty(
                    rest_api_id="restApiId",
                    stage_name="stageName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f2d45cf9ba67190fdb0e0847faebb0af535a361baa4a4b4cf016270d7912a22)
                check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
                check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rest_api_id is not None:
                self._values["rest_api_id"] = rest_api_id
            if stage_name is not None:
                self._values["stage_name"] = stage_name

        @builtins.property
        def rest_api_id(self) -> typing.Optional[builtins.str]:
            '''The string identifier of the associated RestApi.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-apikey-stagekey.html#cfn-apigateway-apikey-stagekey-restapiid
            '''
            result = self._values.get("rest_api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage_name(self) -> typing.Optional[builtins.str]:
            '''The stage name associated with the stage key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-apikey-stagekey.html#cfn-apigateway-apikey-stagekey-stagename
            '''
            result = self._values.get("stage_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnAuthorizerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorizer_credentials": "authorizerCredentials",
        "authorizer_result_ttl_in_seconds": "authorizerResultTtlInSeconds",
        "authorizer_uri": "authorizerUri",
        "auth_type": "authType",
        "identity_source": "identitySource",
        "identity_validation_expression": "identityValidationExpression",
        "name": "name",
        "provider_arns": "providerArns",
        "rest_api_id": "restApiId",
        "type": "type",
    },
)
class CfnAuthorizerMixinProps:
    def __init__(
        self,
        *,
        authorizer_credentials: typing.Optional[builtins.str] = None,
        authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
        authorizer_uri: typing.Optional[builtins.str] = None,
        auth_type: typing.Optional[builtins.str] = None,
        identity_source: typing.Optional[builtins.str] = None,
        identity_validation_expression: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        provider_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAuthorizerPropsMixin.

        :param authorizer_credentials: Specifies the required credentials as an IAM role for API Gateway to invoke the authorizer. To specify an IAM role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To use resource-based permissions on the Lambda function, specify null.
        :param authorizer_result_ttl_in_seconds: The TTL in seconds of cached authorizer results. If it equals 0, authorization caching is disabled. If it is greater than 0, API Gateway will cache authorizer responses. If this field is not set, the default value is 300. The maximum value is 3600, or 1 hour.
        :param authorizer_uri: Specifies the authorizer's Uniform Resource Identifier (URI). For ``TOKEN`` or ``REQUEST`` authorizers, this must be a well-formed Lambda function URI, for example, ``arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2:{account_id}:function:{lambda_function_name}/invocations`` . In general, the URI has this form ``arn:aws:apigateway:{region}:lambda:path/{service_api}`` , where ``{region}`` is the same as the region hosting the Lambda function, ``path`` indicates that the remaining substring in the URI should be treated as the path to the resource, including the initial ``/`` . For Lambda functions, this is usually of the form ``/2015-03-31/functions/[FunctionARN]/invocations`` .
        :param auth_type: Optional customer-defined field, used in OpenAPI imports and exports without functional impact.
        :param identity_source: The identity source for which authorization is requested. For a ``TOKEN`` or ``COGNITO_USER_POOLS`` authorizer, this is required and specifies the request header mapping expression for the custom header holding the authorization token submitted by the client. For example, if the token header name is ``Auth`` , the header mapping expression is ``method.request.header.Auth`` . For the ``REQUEST`` authorizer, this is required when authorization caching is enabled. The value is a comma-separated string of one or more mapping expressions of the specified request parameters. For example, if an ``Auth`` header, a ``Name`` query string parameter are defined as identity sources, this value is ``method.request.header.Auth, method.request.querystring.Name`` . These parameters will be used to derive the authorization caching key and to perform runtime validation of the ``REQUEST`` authorizer by verifying all of the identity-related request parameters are present, not null and non-empty. Only when this is true does the authorizer invoke the authorizer Lambda function, otherwise, it returns a 401 Unauthorized response without calling the Lambda function. The valid value is a string of comma-separated mapping expressions of the specified request parameters. When the authorization caching is not enabled, this property is optional.
        :param identity_validation_expression: A validation expression for the incoming identity token. For ``TOKEN`` authorizers, this value is a regular expression. For ``COGNITO_USER_POOLS`` authorizers, API Gateway will match the ``aud`` field of the incoming token from the client against the specified regular expression. It will invoke the authorizer's Lambda function when there is a match. Otherwise, it will return a 401 Unauthorized response without calling the Lambda function. The validation expression does not apply to the ``REQUEST`` authorizer.
        :param name: The name of the authorizer.
        :param provider_arns: A list of the Amazon Cognito user pool ARNs for the ``COGNITO_USER_POOLS`` authorizer. Each element is of this format: ``arn:aws:cognito-idp:{region}:{account_id}:userpool/{user_pool_id}`` . For a ``TOKEN`` or ``REQUEST`` authorizer, this is not defined.
        :param rest_api_id: The string identifier of the associated RestApi.
        :param type: The authorizer type. Valid values are ``TOKEN`` for a Lambda function using a single authorization token submitted in a custom header, ``REQUEST`` for a Lambda function using incoming request parameters, and ``COGNITO_USER_POOLS`` for using an Amazon Cognito user pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_authorizer_mixin_props = apigateway_mixins.CfnAuthorizerMixinProps(
                authorizer_credentials="authorizerCredentials",
                authorizer_result_ttl_in_seconds=123,
                authorizer_uri="authorizerUri",
                auth_type="authType",
                identity_source="identitySource",
                identity_validation_expression="identityValidationExpression",
                name="name",
                provider_arns=["providerArns"],
                rest_api_id="restApiId",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fdb4445b1b4476ab5f691393ec07b0c2248451c55e9ee7ab00ffa018f26328f)
            check_type(argname="argument authorizer_credentials", value=authorizer_credentials, expected_type=type_hints["authorizer_credentials"])
            check_type(argname="argument authorizer_result_ttl_in_seconds", value=authorizer_result_ttl_in_seconds, expected_type=type_hints["authorizer_result_ttl_in_seconds"])
            check_type(argname="argument authorizer_uri", value=authorizer_uri, expected_type=type_hints["authorizer_uri"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument identity_source", value=identity_source, expected_type=type_hints["identity_source"])
            check_type(argname="argument identity_validation_expression", value=identity_validation_expression, expected_type=type_hints["identity_validation_expression"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provider_arns", value=provider_arns, expected_type=type_hints["provider_arns"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorizer_credentials is not None:
            self._values["authorizer_credentials"] = authorizer_credentials
        if authorizer_result_ttl_in_seconds is not None:
            self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
        if authorizer_uri is not None:
            self._values["authorizer_uri"] = authorizer_uri
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if identity_source is not None:
            self._values["identity_source"] = identity_source
        if identity_validation_expression is not None:
            self._values["identity_validation_expression"] = identity_validation_expression
        if name is not None:
            self._values["name"] = name
        if provider_arns is not None:
            self._values["provider_arns"] = provider_arns
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def authorizer_credentials(self) -> typing.Optional[builtins.str]:
        '''Specifies the required credentials as an IAM role for API Gateway to invoke the authorizer.

        To specify an IAM role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To use resource-based permissions on the Lambda function, specify null.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authorizercredentials
        '''
        result = self._values.get("authorizer_credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The TTL in seconds of cached authorizer results.

        If it equals 0, authorization caching is disabled. If it is greater than 0, API Gateway will cache authorizer responses. If this field is not set, the default value is 300. The maximum value is 3600, or 1 hour.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authorizerresultttlinseconds
        '''
        result = self._values.get("authorizer_result_ttl_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def authorizer_uri(self) -> typing.Optional[builtins.str]:
        '''Specifies the authorizer's Uniform Resource Identifier (URI).

        For ``TOKEN`` or ``REQUEST`` authorizers, this must be a well-formed Lambda function URI, for example, ``arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2:{account_id}:function:{lambda_function_name}/invocations`` . In general, the URI has this form ``arn:aws:apigateway:{region}:lambda:path/{service_api}`` , where ``{region}`` is the same as the region hosting the Lambda function, ``path`` indicates that the remaining substring in the URI should be treated as the path to the resource, including the initial ``/`` . For Lambda functions, this is usually of the form ``/2015-03-31/functions/[FunctionARN]/invocations`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authorizeruri
        '''
        result = self._values.get("authorizer_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''Optional customer-defined field, used in OpenAPI imports and exports without functional impact.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-authtype
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_source(self) -> typing.Optional[builtins.str]:
        '''The identity source for which authorization is requested.

        For a ``TOKEN`` or ``COGNITO_USER_POOLS`` authorizer, this is required and specifies the request header mapping expression for the custom header holding the authorization token submitted by the client. For example, if the token header name is ``Auth`` , the header mapping expression is ``method.request.header.Auth`` . For the ``REQUEST`` authorizer, this is required when authorization caching is enabled. The value is a comma-separated string of one or more mapping expressions of the specified request parameters. For example, if an ``Auth`` header, a ``Name`` query string parameter are defined as identity sources, this value is ``method.request.header.Auth, method.request.querystring.Name`` . These parameters will be used to derive the authorization caching key and to perform runtime validation of the ``REQUEST`` authorizer by verifying all of the identity-related request parameters are present, not null and non-empty. Only when this is true does the authorizer invoke the authorizer Lambda function, otherwise, it returns a 401 Unauthorized response without calling the Lambda function. The valid value is a string of comma-separated mapping expressions of the specified request parameters. When the authorization caching is not enabled, this property is optional.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-identitysource
        '''
        result = self._values.get("identity_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_validation_expression(self) -> typing.Optional[builtins.str]:
        '''A validation expression for the incoming identity token.

        For ``TOKEN`` authorizers, this value is a regular expression. For ``COGNITO_USER_POOLS`` authorizers, API Gateway will match the ``aud`` field of the incoming token from the client against the specified regular expression. It will invoke the authorizer's Lambda function when there is a match. Otherwise, it will return a 401 Unauthorized response without calling the Lambda function. The validation expression does not apply to the ``REQUEST`` authorizer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-identityvalidationexpression
        '''
        result = self._values.get("identity_validation_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the authorizer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the Amazon Cognito user pool ARNs for the ``COGNITO_USER_POOLS`` authorizer.

        Each element is of this format: ``arn:aws:cognito-idp:{region}:{account_id}:userpool/{user_pool_id}`` . For a ``TOKEN`` or ``REQUEST`` authorizer, this is not defined.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-providerarns
        '''
        result = self._values.get("provider_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The authorizer type.

        Valid values are ``TOKEN`` for a Lambda function using a single authorization token submitted in a custom header, ``REQUEST`` for a Lambda function using incoming request parameters, and ``COGNITO_USER_POOLS`` for using an Amazon Cognito user pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html#cfn-apigateway-authorizer-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAuthorizerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAuthorizerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnAuthorizerPropsMixin",
):
    '''The ``AWS::ApiGateway::Authorizer`` resource creates an authorization layer that API Gateway activates for methods that have authorization enabled.

    API Gateway activates the authorizer when a client calls those methods.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html
    :cloudformationResource: AWS::ApiGateway::Authorizer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_authorizer_props_mixin = apigateway_mixins.CfnAuthorizerPropsMixin(apigateway_mixins.CfnAuthorizerMixinProps(
            authorizer_credentials="authorizerCredentials",
            authorizer_result_ttl_in_seconds=123,
            authorizer_uri="authorizerUri",
            auth_type="authType",
            identity_source="identitySource",
            identity_validation_expression="identityValidationExpression",
            name="name",
            provider_arns=["providerArns"],
            rest_api_id="restApiId",
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAuthorizerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::Authorizer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45531243a956388e3b26a67298a0cf13d80e0d3f572ada5b5803bdd45c0bcf7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__070b4f9e767e9500a4684f004dfe7ad5acfd1e18ffacd89685614f3b1ec2b50a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0f0d651c2cdfdc1c1e64ad3528a2e67ecac45c2d861666178d0d0c966bd2121)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAuthorizerMixinProps:
        return typing.cast(CfnAuthorizerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnBasePathMappingMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "base_path": "basePath",
        "domain_name": "domainName",
        "id": "id",
        "rest_api_id": "restApiId",
        "stage": "stage",
    },
)
class CfnBasePathMappingMixinProps:
    def __init__(
        self,
        *,
        base_path: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnBasePathMappingPropsMixin.

        :param base_path: The base path name that callers of the API must provide as part of the URL after the domain name.
        :param domain_name: The domain name of the BasePathMapping resource to be described.
        :param id: 
        :param rest_api_id: The string identifier of the associated RestApi.
        :param stage: The name of the associated stage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_base_path_mapping_mixin_props = apigateway_mixins.CfnBasePathMappingMixinProps(
                base_path="basePath",
                domain_name="domainName",
                id="id",
                rest_api_id="restApiId",
                stage="stage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a926e6e716b81ecf2bb5ea32284c02f96c05d2dd22570c8d01ef9f9699a8ae7)
            check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_path is not None:
            self._values["base_path"] = base_path
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if id is not None:
            self._values["id"] = id
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def base_path(self) -> typing.Optional[builtins.str]:
        '''The base path name that callers of the API must provide as part of the URL after the domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-basepath
        '''
        result = self._values.get("base_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name of the BasePathMapping resource to be described.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-id
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''The name of the associated stage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html#cfn-apigateway-basepathmapping-stage
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBasePathMappingMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBasePathMappingPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnBasePathMappingPropsMixin",
):
    '''The ``AWS::ApiGateway::BasePathMapping`` resource creates a base path that clients who call your API must use in the invocation URL.

    Supported only for public custom domain names.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmapping.html
    :cloudformationResource: AWS::ApiGateway::BasePathMapping
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_base_path_mapping_props_mixin = apigateway_mixins.CfnBasePathMappingPropsMixin(apigateway_mixins.CfnBasePathMappingMixinProps(
            base_path="basePath",
            domain_name="domainName",
            id="id",
            rest_api_id="restApiId",
            stage="stage"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBasePathMappingMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::BasePathMapping``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6660880b73afc5fe53e3c92496cd48c035fef36d7ee5674ce2de7df5cce09f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c920cdb15fbfe9b6aa4ba56267ee3ac00757201415b015af28ff66aecbe364d1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c1f6f2970c75b106c2baf86b655cb8ee5007e77cc1bc5f50350d4cc2920991)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBasePathMappingMixinProps:
        return typing.cast(CfnBasePathMappingMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnBasePathMappingV2MixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "base_path": "basePath",
        "domain_name_arn": "domainNameArn",
        "rest_api_id": "restApiId",
        "stage": "stage",
    },
)
class CfnBasePathMappingV2MixinProps:
    def __init__(
        self,
        *,
        base_path: typing.Optional[builtins.str] = None,
        domain_name_arn: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnBasePathMappingV2PropsMixin.

        :param base_path: The base path name that callers of the private API must provide as part of the URL after the domain name.
        :param domain_name_arn: The ARN of the domain name for the BasePathMappingV2 resource to be described.
        :param rest_api_id: The private API's identifier. This identifier is unique across all of your APIs in API Gateway.
        :param stage: Represents a unique identifier for a version of a deployed private RestApi that is callable by users. The Stage must depend on the ``RestApi`` 's stage. To create a dependency, add a DependsOn attribute to the BasePathMappingV2 resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmappingv2.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_base_path_mapping_v2_mixin_props = apigateway_mixins.CfnBasePathMappingV2MixinProps(
                base_path="basePath",
                domain_name_arn="domainNameArn",
                rest_api_id="restApiId",
                stage="stage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7370e2cc9c8202b81c0224d093266038a2a84ab7d18c56f00bbe65259c8f7d54)
            check_type(argname="argument base_path", value=base_path, expected_type=type_hints["base_path"])
            check_type(argname="argument domain_name_arn", value=domain_name_arn, expected_type=type_hints["domain_name_arn"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_path is not None:
            self._values["base_path"] = base_path
        if domain_name_arn is not None:
            self._values["domain_name_arn"] = domain_name_arn
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def base_path(self) -> typing.Optional[builtins.str]:
        '''The base path name that callers of the private API must provide as part of the URL after the domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmappingv2.html#cfn-apigateway-basepathmappingv2-basepath
        '''
        result = self._values.get("base_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the domain name for the BasePathMappingV2 resource to be described.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmappingv2.html#cfn-apigateway-basepathmappingv2-domainnamearn
        '''
        result = self._values.get("domain_name_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The private API's identifier.

        This identifier is unique across all of your APIs in API Gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmappingv2.html#cfn-apigateway-basepathmappingv2-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''Represents a unique identifier for a version of a deployed private RestApi that is callable by users.

        The Stage must depend on the ``RestApi`` 's stage. To create a dependency, add a DependsOn attribute to the BasePathMappingV2 resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmappingv2.html#cfn-apigateway-basepathmappingv2-stage
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBasePathMappingV2MixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBasePathMappingV2PropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnBasePathMappingV2PropsMixin",
):
    '''The ``AWS::ApiGateway::BasePathMappingV2`` resource creates a base path that clients who call your API must use in the invocation URL.

    Supported only for private custom domain names.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-basepathmappingv2.html
    :cloudformationResource: AWS::ApiGateway::BasePathMappingV2
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_base_path_mapping_v2_props_mixin = apigateway_mixins.CfnBasePathMappingV2PropsMixin(apigateway_mixins.CfnBasePathMappingV2MixinProps(
            base_path="basePath",
            domain_name_arn="domainNameArn",
            rest_api_id="restApiId",
            stage="stage"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBasePathMappingV2MixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::BasePathMappingV2``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ddf36f303caa5ea3cc0b031cdd413f247cc7c8877c7b70d50b8cc10879320b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c50c406c28342738fb5130130c0079c611708cf59215b133a273748ff76f189c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1a073de8e1ea064d69b0c3a8b64bc6b85623530310f871e23920e47720022b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBasePathMappingV2MixinProps:
        return typing.cast(CfnBasePathMappingV2MixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnClientCertificateMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "tags": "tags"},
)
class CfnClientCertificateMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnClientCertificatePropsMixin.

        :param description: The description of the client certificate.
        :param tags: The collection of tags. Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_client_certificate_mixin_props = apigateway_mixins.CfnClientCertificateMixinProps(
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b059e4c55be9f108c3ec78bc25760e10928b3009d9ca2484f8e7ba51fd58ec1e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the client certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html#cfn-apigateway-clientcertificate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html#cfn-apigateway-clientcertificate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClientCertificateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClientCertificatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnClientCertificatePropsMixin",
):
    '''The ``AWS::ApiGateway::ClientCertificate`` resource creates a client certificate that API Gateway uses to configure client-side SSL authentication for sending requests to the integration endpoint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-clientcertificate.html
    :cloudformationResource: AWS::ApiGateway::ClientCertificate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_client_certificate_props_mixin = apigateway_mixins.CfnClientCertificatePropsMixin(apigateway_mixins.CfnClientCertificateMixinProps(
            description="description",
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
        props: typing.Union[CfnClientCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::ClientCertificate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fdb55897c60d2e1d6c800f92b39109c9a923a6563b4b1bf03803899d4018eab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5bf6303d6df8a22fe05f06a563ff01895e7e57d3ab87e368020a078f10eb89a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f820793afa30f58ae19ef492f5222845424c18a7d4f8ac96578eebbc6b118af2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClientCertificateMixinProps:
        return typing.cast(CfnClientCertificateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDeploymentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_canary_settings": "deploymentCanarySettings",
        "description": "description",
        "rest_api_id": "restApiId",
        "stage_description": "stageDescription",
        "stage_name": "stageName",
    },
)
class CfnDeploymentMixinProps:
    def __init__(
        self,
        *,
        deployment_canary_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.DeploymentCanarySettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
        stage_description: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.StageDescriptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDeploymentPropsMixin.

        :param deployment_canary_settings: The input configuration for a canary deployment.
        :param description: The description for the Deployment resource to create.
        :param rest_api_id: The string identifier of the associated RestApi.
        :param stage_description: The description of the Stage resource for the Deployment resource to create. To specify a stage description, you must also provide a stage name.
        :param stage_name: The name of the Stage resource for the Deployment resource to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_deployment_mixin_props = apigateway_mixins.CfnDeploymentMixinProps(
                deployment_canary_settings=apigateway_mixins.CfnDeploymentPropsMixin.DeploymentCanarySettingsProperty(
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                ),
                description="description",
                rest_api_id="restApiId",
                stage_description=apigateway_mixins.CfnDeploymentPropsMixin.StageDescriptionProperty(
                    access_log_setting=apigateway_mixins.CfnDeploymentPropsMixin.AccessLogSettingProperty(
                        destination_arn="destinationArn",
                        format="format"
                    ),
                    cache_cluster_enabled=False,
                    cache_cluster_size="cacheClusterSize",
                    cache_data_encrypted=False,
                    cache_ttl_in_seconds=123,
                    caching_enabled=False,
                    canary_setting=apigateway_mixins.CfnDeploymentPropsMixin.CanarySettingProperty(
                        percent_traffic=123,
                        stage_variable_overrides={
                            "stage_variable_overrides_key": "stageVariableOverrides"
                        },
                        use_stage_cache=False
                    ),
                    client_certificate_id="clientCertificateId",
                    data_trace_enabled=False,
                    description="description",
                    documentation_version="documentationVersion",
                    logging_level="loggingLevel",
                    method_settings=[apigateway_mixins.CfnDeploymentPropsMixin.MethodSettingProperty(
                        cache_data_encrypted=False,
                        cache_ttl_in_seconds=123,
                        caching_enabled=False,
                        data_trace_enabled=False,
                        http_method="httpMethod",
                        logging_level="loggingLevel",
                        metrics_enabled=False,
                        resource_path="resourcePath",
                        throttling_burst_limit=123,
                        throttling_rate_limit=123
                    )],
                    metrics_enabled=False,
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    throttling_burst_limit=123,
                    throttling_rate_limit=123,
                    tracing_enabled=False,
                    variables={
                        "variables_key": "variables"
                    }
                ),
                stage_name="stageName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40300f53affc19168065d4dc9971bb6415a54c1aa95737c7e412f224c839827d)
            check_type(argname="argument deployment_canary_settings", value=deployment_canary_settings, expected_type=type_hints["deployment_canary_settings"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            check_type(argname="argument stage_description", value=stage_description, expected_type=type_hints["stage_description"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deployment_canary_settings is not None:
            self._values["deployment_canary_settings"] = deployment_canary_settings
        if description is not None:
            self._values["description"] = description
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id
        if stage_description is not None:
            self._values["stage_description"] = stage_description
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def deployment_canary_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentCanarySettingsProperty"]]:
        '''The input configuration for a canary deployment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-deploymentcanarysettings
        '''
        result = self._values.get("deployment_canary_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.DeploymentCanarySettingsProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the Deployment resource to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_description(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.StageDescriptionProperty"]]:
        '''The description of the Stage resource for the Deployment resource to create.

        To specify a stage description, you must also provide a stage name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-stagedescription
        '''
        result = self._values.get("stage_description")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.StageDescriptionProperty"]], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Stage resource for the Deployment resource to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html#cfn-apigateway-deployment-stagename
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeploymentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDeploymentPropsMixin",
):
    '''The ``AWS::ApiGateway::Deployment`` resource deploys an API Gateway ``RestApi`` resource to a stage so that clients can call the API over the internet.

    The stage acts as an environment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html
    :cloudformationResource: AWS::ApiGateway::Deployment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_deployment_props_mixin = apigateway_mixins.CfnDeploymentPropsMixin(apigateway_mixins.CfnDeploymentMixinProps(
            deployment_canary_settings=apigateway_mixins.CfnDeploymentPropsMixin.DeploymentCanarySettingsProperty(
                percent_traffic=123,
                stage_variable_overrides={
                    "stage_variable_overrides_key": "stageVariableOverrides"
                },
                use_stage_cache=False
            ),
            description="description",
            rest_api_id="restApiId",
            stage_description=apigateway_mixins.CfnDeploymentPropsMixin.StageDescriptionProperty(
                access_log_setting=apigateway_mixins.CfnDeploymentPropsMixin.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                cache_cluster_enabled=False,
                cache_cluster_size="cacheClusterSize",
                cache_data_encrypted=False,
                cache_ttl_in_seconds=123,
                caching_enabled=False,
                canary_setting=apigateway_mixins.CfnDeploymentPropsMixin.CanarySettingProperty(
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                ),
                client_certificate_id="clientCertificateId",
                data_trace_enabled=False,
                description="description",
                documentation_version="documentationVersion",
                logging_level="loggingLevel",
                method_settings=[apigateway_mixins.CfnDeploymentPropsMixin.MethodSettingProperty(
                    cache_data_encrypted=False,
                    cache_ttl_in_seconds=123,
                    caching_enabled=False,
                    data_trace_enabled=False,
                    http_method="httpMethod",
                    logging_level="loggingLevel",
                    metrics_enabled=False,
                    resource_path="resourcePath",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )],
                metrics_enabled=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                throttling_burst_limit=123,
                throttling_rate_limit=123,
                tracing_enabled=False,
                variables={
                    "variables_key": "variables"
                }
            ),
            stage_name="stageName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeploymentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::Deployment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51af28b22596895582ad4923c2d41d70fb0e53c8b5692990d5c0cae639cdaa1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__920b75d7c0eb8831031a8c0d8d1ba3c252656c4ac7615a6436d4134d0e3af47b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5ae7a4e19cc84d11e45fdfea1987eb4a29118e593059ceeddf21af4a027302)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeploymentMixinProps:
        return typing.cast(CfnDeploymentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDeploymentPropsMixin.AccessLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AccessLogSetting`` property type specifies settings for logging access in this stage.

            ``AccessLogSetting`` is a property of the `StageDescription <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html>`_ property type.

            :param destination_arn: The Amazon Resource Name (ARN) of the CloudWatch Logs log group or Kinesis Data Firehose delivery stream to receive access logs. If you specify a Kinesis Data Firehose delivery stream, the stream name must begin with ``amazon-apigateway-`` .
            :param format: A single line format of the access logs of data, as specified by selected $context variables. The format must include at least ``$context.requestId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-accesslogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                access_log_setting_property = apigateway_mixins.CfnDeploymentPropsMixin.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__496421d57fc8f06071cdc43c9e672514902461601c155a85aff2293164248814)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the CloudWatch Logs log group or Kinesis Data Firehose delivery stream to receive access logs.

            If you specify a Kinesis Data Firehose delivery stream, the stream name must begin with ``amazon-apigateway-`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-accesslogsetting.html#cfn-apigateway-deployment-accesslogsetting-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''A single line format of the access logs of data, as specified by selected $context variables.

            The format must include at least ``$context.requestId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-accesslogsetting.html#cfn-apigateway-deployment-accesslogsetting-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDeploymentPropsMixin.CanarySettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "percent_traffic": "percentTraffic",
            "stage_variable_overrides": "stageVariableOverrides",
            "use_stage_cache": "useStageCache",
        },
    )
    class CanarySettingProperty:
        def __init__(
            self,
            *,
            percent_traffic: typing.Optional[jsii.Number] = None,
            stage_variable_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The ``CanarySetting`` property type specifies settings for the canary deployment in this stage.

            ``CanarySetting`` is a property of the `StageDescription <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html>`_ property type.

            :param percent_traffic: The percent (0-100) of traffic diverted to a canary deployment.
            :param stage_variable_overrides: Stage variables overridden for a canary release deployment, including new stage variables introduced in the canary. These stage variables are represented as a string-to-string map between stage variable names and their values.
            :param use_stage_cache: A Boolean flag to indicate whether the canary deployment uses the stage cache or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-canarysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                canary_setting_property = apigateway_mixins.CfnDeploymentPropsMixin.CanarySettingProperty(
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84c43d4983f26e74a685e10d3f546e59ca9aa9a1baa48b07f4e40a8894fd206a)
                check_type(argname="argument percent_traffic", value=percent_traffic, expected_type=type_hints["percent_traffic"])
                check_type(argname="argument stage_variable_overrides", value=stage_variable_overrides, expected_type=type_hints["stage_variable_overrides"])
                check_type(argname="argument use_stage_cache", value=use_stage_cache, expected_type=type_hints["use_stage_cache"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if percent_traffic is not None:
                self._values["percent_traffic"] = percent_traffic
            if stage_variable_overrides is not None:
                self._values["stage_variable_overrides"] = stage_variable_overrides
            if use_stage_cache is not None:
                self._values["use_stage_cache"] = use_stage_cache

        @builtins.property
        def percent_traffic(self) -> typing.Optional[jsii.Number]:
            '''The percent (0-100) of traffic diverted to a canary deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-canarysetting.html#cfn-apigateway-deployment-canarysetting-percenttraffic
            '''
            result = self._values.get("percent_traffic")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stage_variable_overrides(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Stage variables overridden for a canary release deployment, including new stage variables introduced in the canary.

            These stage variables are represented as a string-to-string map between stage variable names and their values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-canarysetting.html#cfn-apigateway-deployment-canarysetting-stagevariableoverrides
            '''
            result = self._values.get("stage_variable_overrides")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_stage_cache(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean flag to indicate whether the canary deployment uses the stage cache or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-canarysetting.html#cfn-apigateway-deployment-canarysetting-usestagecache
            '''
            result = self._values.get("use_stage_cache")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanarySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDeploymentPropsMixin.DeploymentCanarySettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "percent_traffic": "percentTraffic",
            "stage_variable_overrides": "stageVariableOverrides",
            "use_stage_cache": "useStageCache",
        },
    )
    class DeploymentCanarySettingsProperty:
        def __init__(
            self,
            *,
            percent_traffic: typing.Optional[jsii.Number] = None,
            stage_variable_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The ``DeploymentCanarySettings`` property type specifies settings for the canary deployment.

            :param percent_traffic: The percentage (0.0-100.0) of traffic routed to the canary deployment.
            :param stage_variable_overrides: A stage variable overrides used for the canary release deployment. They can override existing stage variables or add new stage variables for the canary release deployment. These stage variables are represented as a string-to-string map between stage variable names and their values.
            :param use_stage_cache: A Boolean flag to indicate whether the canary release deployment uses the stage cache or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-deploymentcanarysettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                deployment_canary_settings_property = apigateway_mixins.CfnDeploymentPropsMixin.DeploymentCanarySettingsProperty(
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d902da8a3d5ca3c7637f3672cceb0a6d03320cb06bb47f4ac78178122ca91adb)
                check_type(argname="argument percent_traffic", value=percent_traffic, expected_type=type_hints["percent_traffic"])
                check_type(argname="argument stage_variable_overrides", value=stage_variable_overrides, expected_type=type_hints["stage_variable_overrides"])
                check_type(argname="argument use_stage_cache", value=use_stage_cache, expected_type=type_hints["use_stage_cache"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if percent_traffic is not None:
                self._values["percent_traffic"] = percent_traffic
            if stage_variable_overrides is not None:
                self._values["stage_variable_overrides"] = stage_variable_overrides
            if use_stage_cache is not None:
                self._values["use_stage_cache"] = use_stage_cache

        @builtins.property
        def percent_traffic(self) -> typing.Optional[jsii.Number]:
            '''The percentage (0.0-100.0) of traffic routed to the canary deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-deploymentcanarysettings.html#cfn-apigateway-deployment-deploymentcanarysettings-percenttraffic
            '''
            result = self._values.get("percent_traffic")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stage_variable_overrides(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A stage variable overrides used for the canary release deployment.

            They can override existing stage variables or add new stage variables for the canary release deployment. These stage variables are represented as a string-to-string map between stage variable names and their values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-deploymentcanarysettings.html#cfn-apigateway-deployment-deploymentcanarysettings-stagevariableoverrides
            '''
            result = self._values.get("stage_variable_overrides")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_stage_cache(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean flag to indicate whether the canary release deployment uses the stage cache or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-deploymentcanarysettings.html#cfn-apigateway-deployment-deploymentcanarysettings-usestagecache
            '''
            result = self._values.get("use_stage_cache")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentCanarySettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDeploymentPropsMixin.MethodSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cache_data_encrypted": "cacheDataEncrypted",
            "cache_ttl_in_seconds": "cacheTtlInSeconds",
            "caching_enabled": "cachingEnabled",
            "data_trace_enabled": "dataTraceEnabled",
            "http_method": "httpMethod",
            "logging_level": "loggingLevel",
            "metrics_enabled": "metricsEnabled",
            "resource_path": "resourcePath",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class MethodSettingProperty:
        def __init__(
            self,
            *,
            cache_data_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            cache_ttl_in_seconds: typing.Optional[jsii.Number] = None,
            caching_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            http_method: typing.Optional[builtins.str] = None,
            logging_level: typing.Optional[builtins.str] = None,
            metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            resource_path: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``MethodSetting`` property type configures settings for all methods in a stage.

            If you modify this property type, you must create a new deployment for your API.

            The ``MethodSettings`` property of the `Amazon API Gateway Deployment StageDescription <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html>`_ property type contains a list of ``MethodSetting`` property types.

            :param cache_data_encrypted: Specifies whether the cached responses are encrypted.
            :param cache_ttl_in_seconds: Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached.
            :param caching_enabled: Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached.
            :param data_trace_enabled: Specifies whether data trace logging is enabled for this method, which affects the log entries pushed to Amazon CloudWatch Logs. This can be useful to troubleshoot APIs, but can result in logging sensitive data. We recommend that you don't enable this option for production APIs.
            :param http_method: The HTTP method.
            :param logging_level: Specifies the logging level for this method, which affects the log entries pushed to Amazon CloudWatch Logs. Valid values are ``OFF`` , ``ERROR`` , and ``INFO`` . Choose ``ERROR`` to write only error-level entries to CloudWatch Logs, or choose ``INFO`` to include all ``ERROR`` events as well as extra informational events.
            :param metrics_enabled: Specifies whether Amazon CloudWatch metrics are enabled for this method.
            :param resource_path: The resource path for this method. Forward slashes ( ``/`` ) are encoded as ``~1`` and the initial slash must include a forward slash. For example, the path value ``/resource/subresource`` must be encoded as ``/~1resource~1subresource`` . To specify the root path, use only a slash ( ``/`` ).
            :param throttling_burst_limit: Specifies the throttling burst limit.
            :param throttling_rate_limit: Specifies the throttling rate limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                method_setting_property = apigateway_mixins.CfnDeploymentPropsMixin.MethodSettingProperty(
                    cache_data_encrypted=False,
                    cache_ttl_in_seconds=123,
                    caching_enabled=False,
                    data_trace_enabled=False,
                    http_method="httpMethod",
                    logging_level="loggingLevel",
                    metrics_enabled=False,
                    resource_path="resourcePath",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc2ea2e1b2071015ea06a81ff242b3f5d323bc1b3e6ee0442d4d8f0af0c06852)
                check_type(argname="argument cache_data_encrypted", value=cache_data_encrypted, expected_type=type_hints["cache_data_encrypted"])
                check_type(argname="argument cache_ttl_in_seconds", value=cache_ttl_in_seconds, expected_type=type_hints["cache_ttl_in_seconds"])
                check_type(argname="argument caching_enabled", value=caching_enabled, expected_type=type_hints["caching_enabled"])
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument metrics_enabled", value=metrics_enabled, expected_type=type_hints["metrics_enabled"])
                check_type(argname="argument resource_path", value=resource_path, expected_type=type_hints["resource_path"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cache_data_encrypted is not None:
                self._values["cache_data_encrypted"] = cache_data_encrypted
            if cache_ttl_in_seconds is not None:
                self._values["cache_ttl_in_seconds"] = cache_ttl_in_seconds
            if caching_enabled is not None:
                self._values["caching_enabled"] = caching_enabled
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if http_method is not None:
                self._values["http_method"] = http_method
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if metrics_enabled is not None:
                self._values["metrics_enabled"] = metrics_enabled
            if resource_path is not None:
                self._values["resource_path"] = resource_path
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def cache_data_encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the cached responses are encrypted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-cachedataencrypted
            '''
            result = self._values.get("cache_data_encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def cache_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Specifies the time to live (TTL), in seconds, for cached responses.

            The higher the TTL, the longer the response will be cached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-cachettlinseconds
            '''
            result = self._values.get("cache_ttl_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def caching_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether responses should be cached and returned for requests.

            A cache cluster must be enabled on the stage for responses to be cached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-cachingenabled
            '''
            result = self._values.get("caching_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether data trace logging is enabled for this method, which affects the log entries pushed to Amazon CloudWatch Logs.

            This can be useful to troubleshoot APIs, but can result in logging sensitive data. We recommend that you don't enable this option for production APIs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def http_method(self) -> typing.Optional[builtins.str]:
            '''The HTTP method.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-httpmethod
            '''
            result = self._values.get("http_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''Specifies the logging level for this method, which affects the log entries pushed to Amazon CloudWatch Logs.

            Valid values are ``OFF`` , ``ERROR`` , and ``INFO`` . Choose ``ERROR`` to write only error-level entries to CloudWatch Logs, or choose ``INFO`` to include all ``ERROR`` events as well as extra informational events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon CloudWatch metrics are enabled for this method.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-metricsenabled
            '''
            result = self._values.get("metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def resource_path(self) -> typing.Optional[builtins.str]:
            '''The resource path for this method.

            Forward slashes ( ``/`` ) are encoded as ``~1`` and the initial slash must include a forward slash. For example, the path value ``/resource/subresource`` must be encoded as ``/~1resource~1subresource`` . To specify the root path, use only a slash ( ``/`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-resourcepath
            '''
            result = self._values.get("resource_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throttling burst limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throttling rate limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-methodsetting.html#cfn-apigateway-deployment-methodsetting-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MethodSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDeploymentPropsMixin.StageDescriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_log_setting": "accessLogSetting",
            "cache_cluster_enabled": "cacheClusterEnabled",
            "cache_cluster_size": "cacheClusterSize",
            "cache_data_encrypted": "cacheDataEncrypted",
            "cache_ttl_in_seconds": "cacheTtlInSeconds",
            "caching_enabled": "cachingEnabled",
            "canary_setting": "canarySetting",
            "client_certificate_id": "clientCertificateId",
            "data_trace_enabled": "dataTraceEnabled",
            "description": "description",
            "documentation_version": "documentationVersion",
            "logging_level": "loggingLevel",
            "method_settings": "methodSettings",
            "metrics_enabled": "metricsEnabled",
            "tags": "tags",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
            "tracing_enabled": "tracingEnabled",
            "variables": "variables",
        },
    )
    class StageDescriptionProperty:
        def __init__(
            self,
            *,
            access_log_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.AccessLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            cache_cluster_size: typing.Optional[builtins.str] = None,
            cache_data_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            cache_ttl_in_seconds: typing.Optional[jsii.Number] = None,
            caching_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            canary_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.CanarySettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            client_certificate_id: typing.Optional[builtins.str] = None,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            description: typing.Optional[builtins.str] = None,
            documentation_version: typing.Optional[builtins.str] = None,
            logging_level: typing.Optional[builtins.str] = None,
            method_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeploymentPropsMixin.MethodSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
            tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''``StageDescription`` is a property of the `AWS::ApiGateway::Deployment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-deployment.html>`_ resource that configures a deployment stage.

            :param access_log_setting: Specifies settings for logging access in this stage.
            :param cache_cluster_enabled: Specifies whether a cache cluster is enabled for the stage. To activate a method-level cache, set ``CachingEnabled`` to ``true`` for a method.
            :param cache_cluster_size: The size of the stage's cache cluster. For more information, see `cacheClusterSize <https://docs.aws.amazon.com/apigateway/latest/api/API_CreateStage.html#apigw-CreateStage-request-cacheClusterSize>`_ in the *API Gateway API Reference* .
            :param cache_data_encrypted: Indicates whether the cached responses are encrypted.
            :param cache_ttl_in_seconds: The time-to-live (TTL) period, in seconds, that specifies how long API Gateway caches responses.
            :param caching_enabled: Indicates whether responses are cached and returned for requests. You must enable a cache cluster on the stage to cache responses. For more information, see `Enable API Gateway Caching in a Stage to Enhance API Performance <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html>`_ in the *API Gateway Developer Guide* .
            :param canary_setting: Specifies settings for the canary deployment in this stage.
            :param client_certificate_id: The identifier of the client certificate that API Gateway uses to call your integration endpoints in the stage.
            :param data_trace_enabled: Indicates whether data trace logging is enabled for methods in the stage. API Gateway pushes these logs to Amazon CloudWatch Logs.
            :param description: A description of the purpose of the stage.
            :param documentation_version: The version identifier of the API documentation snapshot.
            :param logging_level: The logging level for this method. For valid values, see the ``loggingLevel`` property of the `MethodSetting <https://docs.aws.amazon.com/apigateway/latest/api/API_MethodSetting.html>`_ resource in the *Amazon API Gateway API Reference* .
            :param method_settings: Configures settings for all of the stage's methods.
            :param metrics_enabled: Indicates whether Amazon CloudWatch metrics are enabled for methods in the stage.
            :param tags: An array of arbitrary tags (key-value pairs) to associate with the stage.
            :param throttling_burst_limit: The target request burst rate limit. This allows more requests through for a period of time than the target rate limit. For more information, see `Manage API Request Throttling <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html>`_ in the *API Gateway Developer Guide* .
            :param throttling_rate_limit: The target request steady-state rate limit. For more information, see `Manage API Request Throttling <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html>`_ in the *API Gateway Developer Guide* .
            :param tracing_enabled: Specifies whether active tracing with X-ray is enabled for this stage. For more information, see `Trace API Gateway API Execution with AWS X-Ray <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-xray.html>`_ in the *API Gateway Developer Guide* .
            :param variables: A map that defines the stage variables. Variable names must consist of alphanumeric characters, and the values must match the following regular expression: ``[A-Za-z0-9-._~:/?#&=,]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                stage_description_property = apigateway_mixins.CfnDeploymentPropsMixin.StageDescriptionProperty(
                    access_log_setting=apigateway_mixins.CfnDeploymentPropsMixin.AccessLogSettingProperty(
                        destination_arn="destinationArn",
                        format="format"
                    ),
                    cache_cluster_enabled=False,
                    cache_cluster_size="cacheClusterSize",
                    cache_data_encrypted=False,
                    cache_ttl_in_seconds=123,
                    caching_enabled=False,
                    canary_setting=apigateway_mixins.CfnDeploymentPropsMixin.CanarySettingProperty(
                        percent_traffic=123,
                        stage_variable_overrides={
                            "stage_variable_overrides_key": "stageVariableOverrides"
                        },
                        use_stage_cache=False
                    ),
                    client_certificate_id="clientCertificateId",
                    data_trace_enabled=False,
                    description="description",
                    documentation_version="documentationVersion",
                    logging_level="loggingLevel",
                    method_settings=[apigateway_mixins.CfnDeploymentPropsMixin.MethodSettingProperty(
                        cache_data_encrypted=False,
                        cache_ttl_in_seconds=123,
                        caching_enabled=False,
                        data_trace_enabled=False,
                        http_method="httpMethod",
                        logging_level="loggingLevel",
                        metrics_enabled=False,
                        resource_path="resourcePath",
                        throttling_burst_limit=123,
                        throttling_rate_limit=123
                    )],
                    metrics_enabled=False,
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    throttling_burst_limit=123,
                    throttling_rate_limit=123,
                    tracing_enabled=False,
                    variables={
                        "variables_key": "variables"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66cbda9a88b45df1baa3dd06dff29a85e74bd2ace94ff783beac024d9c9c38c7)
                check_type(argname="argument access_log_setting", value=access_log_setting, expected_type=type_hints["access_log_setting"])
                check_type(argname="argument cache_cluster_enabled", value=cache_cluster_enabled, expected_type=type_hints["cache_cluster_enabled"])
                check_type(argname="argument cache_cluster_size", value=cache_cluster_size, expected_type=type_hints["cache_cluster_size"])
                check_type(argname="argument cache_data_encrypted", value=cache_data_encrypted, expected_type=type_hints["cache_data_encrypted"])
                check_type(argname="argument cache_ttl_in_seconds", value=cache_ttl_in_seconds, expected_type=type_hints["cache_ttl_in_seconds"])
                check_type(argname="argument caching_enabled", value=caching_enabled, expected_type=type_hints["caching_enabled"])
                check_type(argname="argument canary_setting", value=canary_setting, expected_type=type_hints["canary_setting"])
                check_type(argname="argument client_certificate_id", value=client_certificate_id, expected_type=type_hints["client_certificate_id"])
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument documentation_version", value=documentation_version, expected_type=type_hints["documentation_version"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument method_settings", value=method_settings, expected_type=type_hints["method_settings"])
                check_type(argname="argument metrics_enabled", value=metrics_enabled, expected_type=type_hints["metrics_enabled"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
                check_type(argname="argument tracing_enabled", value=tracing_enabled, expected_type=type_hints["tracing_enabled"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_log_setting is not None:
                self._values["access_log_setting"] = access_log_setting
            if cache_cluster_enabled is not None:
                self._values["cache_cluster_enabled"] = cache_cluster_enabled
            if cache_cluster_size is not None:
                self._values["cache_cluster_size"] = cache_cluster_size
            if cache_data_encrypted is not None:
                self._values["cache_data_encrypted"] = cache_data_encrypted
            if cache_ttl_in_seconds is not None:
                self._values["cache_ttl_in_seconds"] = cache_ttl_in_seconds
            if caching_enabled is not None:
                self._values["caching_enabled"] = caching_enabled
            if canary_setting is not None:
                self._values["canary_setting"] = canary_setting
            if client_certificate_id is not None:
                self._values["client_certificate_id"] = client_certificate_id
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if description is not None:
                self._values["description"] = description
            if documentation_version is not None:
                self._values["documentation_version"] = documentation_version
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if method_settings is not None:
                self._values["method_settings"] = method_settings
            if metrics_enabled is not None:
                self._values["metrics_enabled"] = metrics_enabled
            if tags is not None:
                self._values["tags"] = tags
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit
            if tracing_enabled is not None:
                self._values["tracing_enabled"] = tracing_enabled
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def access_log_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.AccessLogSettingProperty"]]:
            '''Specifies settings for logging access in this stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-accesslogsetting
            '''
            result = self._values.get("access_log_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.AccessLogSettingProperty"]], result)

        @builtins.property
        def cache_cluster_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether a cache cluster is enabled for the stage.

            To activate a method-level cache, set ``CachingEnabled`` to ``true`` for a method.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cacheclusterenabled
            '''
            result = self._values.get("cache_cluster_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def cache_cluster_size(self) -> typing.Optional[builtins.str]:
            '''The size of the stage's cache cluster.

            For more information, see `cacheClusterSize <https://docs.aws.amazon.com/apigateway/latest/api/API_CreateStage.html#apigw-CreateStage-request-cacheClusterSize>`_ in the *API Gateway API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cacheclustersize
            '''
            result = self._values.get("cache_cluster_size")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cache_data_encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the cached responses are encrypted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cachedataencrypted
            '''
            result = self._values.get("cache_data_encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def cache_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The time-to-live (TTL) period, in seconds, that specifies how long API Gateway caches responses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cachettlinseconds
            '''
            result = self._values.get("cache_ttl_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def caching_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether responses are cached and returned for requests.

            You must enable a cache cluster on the stage to cache responses. For more information, see `Enable API Gateway Caching in a Stage to Enhance API Performance <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html>`_ in the *API Gateway Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-cachingenabled
            '''
            result = self._values.get("caching_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def canary_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.CanarySettingProperty"]]:
            '''Specifies settings for the canary deployment in this stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-canarysetting
            '''
            result = self._values.get("canary_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.CanarySettingProperty"]], result)

        @builtins.property
        def client_certificate_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the client certificate that API Gateway uses to call your integration endpoints in the stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-clientcertificateid
            '''
            result = self._values.get("client_certificate_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether data trace logging is enabled for methods in the stage.

            API Gateway pushes these logs to Amazon CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the purpose of the stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def documentation_version(self) -> typing.Optional[builtins.str]:
            '''The version identifier of the API documentation snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-documentationversion
            '''
            result = self._values.get("documentation_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''The logging level for this method.

            For valid values, see the ``loggingLevel`` property of the `MethodSetting <https://docs.aws.amazon.com/apigateway/latest/api/API_MethodSetting.html>`_ resource in the *Amazon API Gateway API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def method_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.MethodSettingProperty"]]]]:
            '''Configures settings for all of the stage's methods.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-methodsettings
            '''
            result = self._values.get("method_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeploymentPropsMixin.MethodSettingProperty"]]]], result)

        @builtins.property
        def metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Amazon CloudWatch metrics are enabled for methods in the stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-metricsenabled
            '''
            result = self._values.get("metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''An array of arbitrary tags (key-value pairs) to associate with the stage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''The target request burst rate limit.

            This allows more requests through for a period of time than the target rate limit. For more information, see `Manage API Request Throttling <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html>`_ in the *API Gateway Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''The target request steady-state rate limit.

            For more information, see `Manage API Request Throttling <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html>`_ in the *API Gateway Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def tracing_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether active tracing with X-ray is enabled for this stage.

            For more information, see `Trace API Gateway API Execution with AWS X-Ray <https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-xray.html>`_ in the *API Gateway Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-tracingenabled
            '''
            result = self._values.get("tracing_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A map that defines the stage variables.

            Variable names must consist of alphanumeric characters, and the values must match the following regular expression: ``[A-Za-z0-9-._~:/?#&=,]+`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-deployment-stagedescription.html#cfn-apigateway-deployment-stagedescription-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageDescriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDocumentationPartMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "properties": "properties",
        "rest_api_id": "restApiId",
    },
)
class CfnDocumentationPartMixinProps:
    def __init__(
        self,
        *,
        location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDocumentationPartPropsMixin.LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        properties: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDocumentationPartPropsMixin.

        :param location: The location of the targeted API entity of the to-be-created documentation part.
        :param properties: The new documentation content map of the targeted API entity. Enclosed key-value pairs are API-specific, but only OpenAPI-compliant key-value pairs can be exported and, hence, published.
        :param rest_api_id: The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_documentation_part_mixin_props = apigateway_mixins.CfnDocumentationPartMixinProps(
                location=apigateway_mixins.CfnDocumentationPartPropsMixin.LocationProperty(
                    method="method",
                    name="name",
                    path="path",
                    status_code="statusCode",
                    type="type"
                ),
                properties="properties",
                rest_api_id="restApiId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e55be9483b40000c912966094d27feb425e2de71546f848ddf6b82176a5d46c)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if location is not None:
            self._values["location"] = location
        if properties is not None:
            self._values["properties"] = properties
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentationPartPropsMixin.LocationProperty"]]:
        '''The location of the targeted API entity of the to-be-created documentation part.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html#cfn-apigateway-documentationpart-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentationPartPropsMixin.LocationProperty"]], result)

    @builtins.property
    def properties(self) -> typing.Optional[builtins.str]:
        '''The new documentation content map of the targeted API entity.

        Enclosed key-value pairs are API-specific, but only OpenAPI-compliant key-value pairs can be exported and, hence, published.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html#cfn-apigateway-documentationpart-properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html#cfn-apigateway-documentationpart-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDocumentationPartMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDocumentationPartPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDocumentationPartPropsMixin",
):
    '''The ``AWS::ApiGateway::DocumentationPart`` resource creates a documentation part for an API.

    For more information, see `Representation of API Documentation in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-documenting-api-content-representation.html>`_ in the *API Gateway Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html
    :cloudformationResource: AWS::ApiGateway::DocumentationPart
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_documentation_part_props_mixin = apigateway_mixins.CfnDocumentationPartPropsMixin(apigateway_mixins.CfnDocumentationPartMixinProps(
            location=apigateway_mixins.CfnDocumentationPartPropsMixin.LocationProperty(
                method="method",
                name="name",
                path="path",
                status_code="statusCode",
                type="type"
            ),
            properties="properties",
            rest_api_id="restApiId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDocumentationPartMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::DocumentationPart``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1c17ab0ee6c93d516fd8b7ed280589dda26f8502070608c921b17f67bc123c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91883d66e90a5724121d1d425598842ea8911f444b489bd02a04dcb53613c407)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d53839a5b4abe45015c42fc2d6828fede4c48de50d67fab69034444d17cbfd4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDocumentationPartMixinProps:
        return typing.cast(CfnDocumentationPartMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDocumentationPartPropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "method": "method",
            "name": "name",
            "path": "path",
            "status_code": "statusCode",
            "type": "type",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            method: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            status_code: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Location`` property specifies the location of the Amazon API Gateway API entity that the documentation applies to.

            ``Location`` is a property of the `AWS::ApiGateway::DocumentationPart <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationpart.html>`_ resource.
            .. epigraph::

               For more information about each property, including constraints and valid values, see `DocumentationPart <https://docs.aws.amazon.com/apigateway/latest/api/API_DocumentationPartLocation.html>`_ in the *Amazon API Gateway REST API Reference* .

            :param method: The HTTP verb of a method. It is a valid field for the API entity types of ``METHOD`` , ``PATH_PARAMETER`` , ``QUERY_PARAMETER`` , ``REQUEST_HEADER`` , ``REQUEST_BODY`` , ``RESPONSE`` , ``RESPONSE_HEADER`` , and ``RESPONSE_BODY`` . The default value is ``*`` for any method. When an applicable child entity inherits the content of an entity of the same type with more general specifications of the other ``location`` attributes, the child entity's ``method`` attribute must match that of the parent entity exactly.
            :param name: The name of the targeted API entity. It is a valid and required field for the API entity types of ``AUTHORIZER`` , ``MODEL`` , ``PATH_PARAMETER`` , ``QUERY_PARAMETER`` , ``REQUEST_HEADER`` , ``REQUEST_BODY`` and ``RESPONSE_HEADER`` . It is an invalid field for any other entity type.
            :param path: The URL path of the target. It is a valid field for the API entity types of ``RESOURCE`` , ``METHOD`` , ``PATH_PARAMETER`` , ``QUERY_PARAMETER`` , ``REQUEST_HEADER`` , ``REQUEST_BODY`` , ``RESPONSE`` , ``RESPONSE_HEADER`` , and ``RESPONSE_BODY`` . The default value is ``/`` for the root resource. When an applicable child entity inherits the content of another entity of the same type with more general specifications of the other ``location`` attributes, the child entity's ``path`` attribute must match that of the parent entity as a prefix.
            :param status_code: The HTTP status code of a response. It is a valid field for the API entity types of ``RESPONSE`` , ``RESPONSE_HEADER`` , and ``RESPONSE_BODY`` . The default value is ``*`` for any status code. When an applicable child entity inherits the content of an entity of the same type with more general specifications of the other ``location`` attributes, the child entity's ``statusCode`` attribute must match that of the parent entity exactly.
            :param type: The type of API entity to which the documentation content applies. Valid values are ``API`` , ``AUTHORIZER`` , ``MODEL`` , ``RESOURCE`` , ``METHOD`` , ``PATH_PARAMETER`` , ``QUERY_PARAMETER`` , ``REQUEST_HEADER`` , ``REQUEST_BODY`` , ``RESPONSE`` , ``RESPONSE_HEADER`` , and ``RESPONSE_BODY`` . Content inheritance does not apply to any entity of the ``API`` , ``AUTHORIZER`` , ``METHOD`` , ``MODEL`` , ``REQUEST_BODY`` , or ``RESOURCE`` type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                location_property = apigateway_mixins.CfnDocumentationPartPropsMixin.LocationProperty(
                    method="method",
                    name="name",
                    path="path",
                    status_code="statusCode",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3dd543544b8508f381cc03617be28a09acaea00d0ba05834fd62f5663bf97652)
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if method is not None:
                self._values["method"] = method
            if name is not None:
                self._values["name"] = name
            if path is not None:
                self._values["path"] = path
            if status_code is not None:
                self._values["status_code"] = status_code
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''The HTTP verb of a method.

            It is a valid field for the API entity types of ``METHOD`` , ``PATH_PARAMETER`` , ``QUERY_PARAMETER`` , ``REQUEST_HEADER`` , ``REQUEST_BODY`` , ``RESPONSE`` , ``RESPONSE_HEADER`` , and ``RESPONSE_BODY`` . The default value is ``*`` for any method. When an applicable child entity inherits the content of an entity of the same type with more general specifications of the other ``location`` attributes, the child entity's ``method`` attribute must match that of the parent entity exactly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the targeted API entity.

            It is a valid and required field for the API entity types of ``AUTHORIZER`` , ``MODEL`` , ``PATH_PARAMETER`` , ``QUERY_PARAMETER`` , ``REQUEST_HEADER`` , ``REQUEST_BODY`` and ``RESPONSE_HEADER`` . It is an invalid field for any other entity type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The URL path of the target.

            It is a valid field for the API entity types of ``RESOURCE`` , ``METHOD`` , ``PATH_PARAMETER`` , ``QUERY_PARAMETER`` , ``REQUEST_HEADER`` , ``REQUEST_BODY`` , ``RESPONSE`` , ``RESPONSE_HEADER`` , and ``RESPONSE_BODY`` . The default value is ``/`` for the root resource. When an applicable child entity inherits the content of another entity of the same type with more general specifications of the other ``location`` attributes, the child entity's ``path`` attribute must match that of the parent entity as a prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_code(self) -> typing.Optional[builtins.str]:
            '''The HTTP status code of a response.

            It is a valid field for the API entity types of ``RESPONSE`` , ``RESPONSE_HEADER`` , and ``RESPONSE_BODY`` . The default value is ``*`` for any status code. When an applicable child entity inherits the content of an entity of the same type with more general specifications of the other ``location`` attributes, the child entity's ``statusCode`` attribute must match that of the parent entity exactly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of API entity to which the documentation content applies.

            Valid values are ``API`` , ``AUTHORIZER`` , ``MODEL`` , ``RESOURCE`` , ``METHOD`` , ``PATH_PARAMETER`` , ``QUERY_PARAMETER`` , ``REQUEST_HEADER`` , ``REQUEST_BODY`` , ``RESPONSE`` , ``RESPONSE_HEADER`` , and ``RESPONSE_BODY`` . Content inheritance does not apply to any entity of the ``API`` , ``AUTHORIZER`` , ``METHOD`` , ``MODEL`` , ``REQUEST_BODY`` , or ``RESOURCE`` type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-documentationpart-location.html#cfn-apigateway-documentationpart-location-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDocumentationVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "documentation_version": "documentationVersion",
        "rest_api_id": "restApiId",
    },
)
class CfnDocumentationVersionMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        documentation_version: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDocumentationVersionPropsMixin.

        :param description: A description about the new documentation snapshot.
        :param documentation_version: The version identifier of the to-be-updated documentation version.
        :param rest_api_id: The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_documentation_version_mixin_props = apigateway_mixins.CfnDocumentationVersionMixinProps(
                description="description",
                documentation_version="documentationVersion",
                rest_api_id="restApiId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aabf58a4e4d3cd0239f40bbf556bdfd20178236721da99ec4116c0778a7e3017)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation_version", value=documentation_version, expected_type=type_hints["documentation_version"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if documentation_version is not None:
            self._values["documentation_version"] = documentation_version
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description about the new documentation snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html#cfn-apigateway-documentationversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation_version(self) -> typing.Optional[builtins.str]:
        '''The version identifier of the to-be-updated documentation version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html#cfn-apigateway-documentationversion-documentationversion
        '''
        result = self._values.get("documentation_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html#cfn-apigateway-documentationversion-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDocumentationVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDocumentationVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDocumentationVersionPropsMixin",
):
    '''The ``AWS::ApiGateway::DocumentationVersion`` resource creates a snapshot of the documentation for an API.

    For more information, see `Representation of API Documentation in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-documenting-api-content-representation.html>`_ in the *API Gateway Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-documentationversion.html
    :cloudformationResource: AWS::ApiGateway::DocumentationVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_documentation_version_props_mixin = apigateway_mixins.CfnDocumentationVersionPropsMixin(apigateway_mixins.CfnDocumentationVersionMixinProps(
            description="description",
            documentation_version="documentationVersion",
            rest_api_id="restApiId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDocumentationVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::DocumentationVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7c346227a432924cc28c6727669a4f81e1c106774d3b517d894930fe0f0d19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9d4d88081854fb9d1a6e55c8bd43255beced8ae06a41401b294c9f9aeb66db9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ff6c8a4245c2026de743ac8d4674475dd26d63c109e98ff513b8964302998b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDocumentationVersionMixinProps:
        return typing.cast(CfnDocumentationVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDomainNameAccessAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_association_source": "accessAssociationSource",
        "access_association_source_type": "accessAssociationSourceType",
        "domain_name_arn": "domainNameArn",
        "tags": "tags",
    },
)
class CfnDomainNameAccessAssociationMixinProps:
    def __init__(
        self,
        *,
        access_association_source: typing.Optional[builtins.str] = None,
        access_association_source_type: typing.Optional[builtins.str] = None,
        domain_name_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainNameAccessAssociationPropsMixin.

        :param access_association_source: The identifier of the domain name access association source. For a ``VPCE`` , the value is the VPC endpoint ID.
        :param access_association_source_type: The type of the domain name access association source. Only ``VPCE`` is currently supported.
        :param domain_name_arn: The ARN of the domain name.
        :param tags: The collection of tags. Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnameaccessassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_domain_name_access_association_mixin_props = apigateway_mixins.CfnDomainNameAccessAssociationMixinProps(
                access_association_source="accessAssociationSource",
                access_association_source_type="accessAssociationSourceType",
                domain_name_arn="domainNameArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f3e2917c3578379dd19d3dc95a3db1954a3f54aa50c28387b26b8f987b7c4a)
            check_type(argname="argument access_association_source", value=access_association_source, expected_type=type_hints["access_association_source"])
            check_type(argname="argument access_association_source_type", value=access_association_source_type, expected_type=type_hints["access_association_source_type"])
            check_type(argname="argument domain_name_arn", value=domain_name_arn, expected_type=type_hints["domain_name_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_association_source is not None:
            self._values["access_association_source"] = access_association_source
        if access_association_source_type is not None:
            self._values["access_association_source_type"] = access_association_source_type
        if domain_name_arn is not None:
            self._values["domain_name_arn"] = domain_name_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_association_source(self) -> typing.Optional[builtins.str]:
        '''The identifier of the domain name access association source.

        For a ``VPCE`` , the value is the VPC endpoint ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnameaccessassociation.html#cfn-apigateway-domainnameaccessassociation-accessassociationsource
        '''
        result = self._values.get("access_association_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_association_source_type(self) -> typing.Optional[builtins.str]:
        '''The type of the domain name access association source.

        Only ``VPCE`` is currently supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnameaccessassociation.html#cfn-apigateway-domainnameaccessassociation-accessassociationsourcetype
        '''
        result = self._values.get("access_association_source_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnameaccessassociation.html#cfn-apigateway-domainnameaccessassociation-domainnamearn
        '''
        result = self._values.get("domain_name_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnameaccessassociation.html#cfn-apigateway-domainnameaccessassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainNameAccessAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainNameAccessAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDomainNameAccessAssociationPropsMixin",
):
    '''The ``AWS::ApiGateway::DomainNameAccessAssociation`` resource creates a domain name access association between an access association source and a private custom domain name.

    Use a domain name access association to invoke a private custom domain name while isolated from the public internet.

    You can only create or delete a DomainNameAccessAssociation using CloudFormation. To reject a domain name access association, use the AWS CLI.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnameaccessassociation.html
    :cloudformationResource: AWS::ApiGateway::DomainNameAccessAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_domain_name_access_association_props_mixin = apigateway_mixins.CfnDomainNameAccessAssociationPropsMixin(apigateway_mixins.CfnDomainNameAccessAssociationMixinProps(
            access_association_source="accessAssociationSource",
            access_association_source_type="accessAssociationSourceType",
            domain_name_arn="domainNameArn",
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
        props: typing.Union[CfnDomainNameAccessAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::DomainNameAccessAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66861aaab7f378b3dd8f052a02296b8a588acc119f4a8bf69536ed07e345b26b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2678ba7c3d723310c24fee73d803bafe70ebeaad983d293ec9586c9d902a474e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b92b8cfd5767205370f7002e75919dc5df0393bcf429ae7e721c06a4d4fb1cb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainNameAccessAssociationMixinProps:
        return typing.cast(CfnDomainNameAccessAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDomainNameMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_arn": "certificateArn",
        "domain_name": "domainName",
        "endpoint_access_mode": "endpointAccessMode",
        "endpoint_configuration": "endpointConfiguration",
        "mutual_tls_authentication": "mutualTlsAuthentication",
        "ownership_verification_certificate_arn": "ownershipVerificationCertificateArn",
        "regional_certificate_arn": "regionalCertificateArn",
        "routing_mode": "routingMode",
        "security_policy": "securityPolicy",
        "tags": "tags",
    },
)
class CfnDomainNameMixinProps:
    def __init__(
        self,
        *,
        certificate_arn: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        endpoint_access_mode: typing.Optional[builtins.str] = None,
        endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainNamePropsMixin.EndpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainNamePropsMixin.MutualTlsAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ownership_verification_certificate_arn: typing.Optional[builtins.str] = None,
        regional_certificate_arn: typing.Optional[builtins.str] = None,
        routing_mode: typing.Optional[builtins.str] = None,
        security_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainNamePropsMixin.

        :param certificate_arn: The reference to an AWS -managed certificate that will be used by edge-optimized endpoint or private endpoint for this domain name. Certificate Manager is the only supported source.
        :param domain_name: The custom domain name as an API host name, for example, ``my-api.example.com`` .
        :param endpoint_access_mode: The endpoint access mode for your DomainName.
        :param endpoint_configuration: The endpoint configuration of this DomainName showing the endpoint types and IP address types of the domain name.
        :param mutual_tls_authentication: The mutual TLS authentication configuration for a custom domain name. If specified, API Gateway performs two-way authentication between the client and the server. Clients must present a trusted certificate to access your API.
        :param ownership_verification_certificate_arn: The ARN of the public certificate issued by ACM to validate ownership of your custom domain. Only required when configuring mutual TLS and using an ACM imported or private CA certificate ARN as the RegionalCertificateArn.
        :param regional_certificate_arn: The reference to an AWS -managed certificate that will be used for validating the regional domain name. Certificate Manager is the only supported source.
        :param routing_mode: The routing mode for this domain name. The routing mode determines how API Gateway sends traffic from your custom domain name to your public APIs. Default: - "BASE_PATH_MAPPING_ONLY"
        :param security_policy: The Transport Layer Security (TLS) version + cipher suite for this DomainName.
        :param tags: The collection of tags. Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_domain_name_mixin_props = apigateway_mixins.CfnDomainNameMixinProps(
                certificate_arn="certificateArn",
                domain_name="domainName",
                endpoint_access_mode="endpointAccessMode",
                endpoint_configuration=apigateway_mixins.CfnDomainNamePropsMixin.EndpointConfigurationProperty(
                    ip_address_type="ipAddressType",
                    types=["types"]
                ),
                mutual_tls_authentication=apigateway_mixins.CfnDomainNamePropsMixin.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                ),
                ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
                regional_certificate_arn="regionalCertificateArn",
                routing_mode="routingMode",
                security_policy="securityPolicy",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7bb0fccbf95b817b115d90337197d9438040235b4882a32d824ed6e5424f6e8)
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument endpoint_access_mode", value=endpoint_access_mode, expected_type=type_hints["endpoint_access_mode"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument mutual_tls_authentication", value=mutual_tls_authentication, expected_type=type_hints["mutual_tls_authentication"])
            check_type(argname="argument ownership_verification_certificate_arn", value=ownership_verification_certificate_arn, expected_type=type_hints["ownership_verification_certificate_arn"])
            check_type(argname="argument regional_certificate_arn", value=regional_certificate_arn, expected_type=type_hints["regional_certificate_arn"])
            check_type(argname="argument routing_mode", value=routing_mode, expected_type=type_hints["routing_mode"])
            check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if endpoint_access_mode is not None:
            self._values["endpoint_access_mode"] = endpoint_access_mode
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if mutual_tls_authentication is not None:
            self._values["mutual_tls_authentication"] = mutual_tls_authentication
        if ownership_verification_certificate_arn is not None:
            self._values["ownership_verification_certificate_arn"] = ownership_verification_certificate_arn
        if regional_certificate_arn is not None:
            self._values["regional_certificate_arn"] = regional_certificate_arn
        if routing_mode is not None:
            self._values["routing_mode"] = routing_mode
        if security_policy is not None:
            self._values["security_policy"] = security_policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''The reference to an AWS -managed certificate that will be used by edge-optimized endpoint or private endpoint for this domain name.

        Certificate Manager is the only supported source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-certificatearn
        '''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The custom domain name as an API host name, for example, ``my-api.example.com`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_access_mode(self) -> typing.Optional[builtins.str]:
        '''The endpoint access mode for your DomainName.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-endpointaccessmode
        '''
        result = self._values.get("endpoint_access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainNamePropsMixin.EndpointConfigurationProperty"]]:
        '''The endpoint configuration of this DomainName showing the endpoint types and IP address types of the domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-endpointconfiguration
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainNamePropsMixin.EndpointConfigurationProperty"]], result)

    @builtins.property
    def mutual_tls_authentication(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainNamePropsMixin.MutualTlsAuthenticationProperty"]]:
        '''The mutual TLS authentication configuration for a custom domain name.

        If specified, API Gateway performs two-way authentication between the client and the server. Clients must present a trusted certificate to access your API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-mutualtlsauthentication
        '''
        result = self._values.get("mutual_tls_authentication")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainNamePropsMixin.MutualTlsAuthenticationProperty"]], result)

    @builtins.property
    def ownership_verification_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the public certificate issued by ACM to validate ownership of your custom domain.

        Only required when configuring mutual TLS and using an ACM imported or private CA certificate ARN as the RegionalCertificateArn.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-ownershipverificationcertificatearn
        '''
        result = self._values.get("ownership_verification_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regional_certificate_arn(self) -> typing.Optional[builtins.str]:
        '''The reference to an AWS -managed certificate that will be used for validating the regional domain name.

        Certificate Manager is the only supported source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-regionalcertificatearn
        '''
        result = self._values.get("regional_certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_mode(self) -> typing.Optional[builtins.str]:
        '''The routing mode for this domain name.

        The routing mode determines how API Gateway sends traffic from your custom domain name to your public APIs.

        :default: - "BASE_PATH_MAPPING_ONLY"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-routingmode
        '''
        result = self._values.get("routing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_policy(self) -> typing.Optional[builtins.str]:
        '''The Transport Layer Security (TLS) version + cipher suite for this DomainName.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-securitypolicy
        '''
        result = self._values.get("security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html#cfn-apigateway-domainname-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainNameMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainNamePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDomainNamePropsMixin",
):
    '''The ``AWS::ApiGateway::DomainName`` resource specifies a public custom domain name for your API in API Gateway.

    To create a custom domain name for private APIs, use `AWS::ApiGateway::DomainNameV2 <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html>`_ .

    You can use a custom domain name to provide a URL that's more intuitive and easier to recall. For more information about using custom domain names, see `Set up Custom Domain Name for an API in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-custom-domains.html>`_ in the *API Gateway Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html
    :cloudformationResource: AWS::ApiGateway::DomainName
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_domain_name_props_mixin = apigateway_mixins.CfnDomainNamePropsMixin(apigateway_mixins.CfnDomainNameMixinProps(
            certificate_arn="certificateArn",
            domain_name="domainName",
            endpoint_access_mode="endpointAccessMode",
            endpoint_configuration=apigateway_mixins.CfnDomainNamePropsMixin.EndpointConfigurationProperty(
                ip_address_type="ipAddressType",
                types=["types"]
            ),
            mutual_tls_authentication=apigateway_mixins.CfnDomainNamePropsMixin.MutualTlsAuthenticationProperty(
                truststore_uri="truststoreUri",
                truststore_version="truststoreVersion"
            ),
            ownership_verification_certificate_arn="ownershipVerificationCertificateArn",
            regional_certificate_arn="regionalCertificateArn",
            routing_mode="routingMode",
            security_policy="securityPolicy",
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
        props: typing.Union[CfnDomainNameMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::DomainName``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee4cf63c82056427f389ac42dab61000f425b3c55b3f2dbf6415079fc0fb606)
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
            type_hints = typing.get_type_hints(_typecheckingstub__214e89db1eb09b671d494a032a7e77d75acb708e3677043dbb34fa5173bdda1a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050d8c6dc260cfce08a458cc6c5a200aa61ebe7527a36bbd07d6393bb99ae0db)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainNameMixinProps:
        return typing.cast(CfnDomainNameMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDomainNamePropsMixin.EndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_address_type": "ipAddressType", "types": "types"},
    )
    class EndpointConfigurationProperty:
        def __init__(
            self,
            *,
            ip_address_type: typing.Optional[builtins.str] = None,
            types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``EndpointConfiguration`` property type specifies the endpoint types and IP address types of an Amazon API Gateway domain name.

            ``EndpointConfiguration`` is a property of the `AWS::ApiGateway::DomainName <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainname.html>`_ resource.

            :param ip_address_type: The IP address types that can invoke this DomainName. Use ``ipv4`` to allow only IPv4 addresses to invoke this DomainName, or use ``dualstack`` to allow both IPv4 and IPv6 addresses to invoke this DomainName. For the ``PRIVATE`` endpoint type, only ``dualstack`` is supported.
            :param types: A list of endpoint types of an API (RestApi) or its custom domain name (DomainName). For an edge-optimized API and its custom domain name, the endpoint type is ``"EDGE"`` . For a regional API and its custom domain name, the endpoint type is ``REGIONAL`` . For a private API, the endpoint type is ``PRIVATE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-endpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                endpoint_configuration_property = apigateway_mixins.CfnDomainNamePropsMixin.EndpointConfigurationProperty(
                    ip_address_type="ipAddressType",
                    types=["types"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c9c01fe4f1c283b79119437879da37793d59f0be38021baa86fd0f1f023aae7)
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
                check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type
            if types is not None:
                self._values["types"] = types

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''The IP address types that can invoke this DomainName.

            Use ``ipv4`` to allow only IPv4 addresses to invoke this DomainName, or use ``dualstack`` to allow both IPv4 and IPv6 addresses to invoke this DomainName. For the ``PRIVATE`` endpoint type, only ``dualstack`` is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-endpointconfiguration.html#cfn-apigateway-domainname-endpointconfiguration-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of endpoint types of an API (RestApi) or its custom domain name (DomainName).

            For an edge-optimized API and its custom domain name, the endpoint type is ``"EDGE"`` . For a regional API and its custom domain name, the endpoint type is ``REGIONAL`` . For a private API, the endpoint type is ``PRIVATE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-endpointconfiguration.html#cfn-apigateway-domainname-endpointconfiguration-types
            '''
            result = self._values.get("types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDomainNamePropsMixin.MutualTlsAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "truststore_uri": "truststoreUri",
            "truststore_version": "truststoreVersion",
        },
    )
    class MutualTlsAuthenticationProperty:
        def __init__(
            self,
            *,
            truststore_uri: typing.Optional[builtins.str] = None,
            truststore_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The mutual TLS authentication configuration for a custom domain name.

            If specified, API Gateway performs two-way authentication between the client and the server. Clients must present a trusted certificate to access your API.

            :param truststore_uri: An Amazon S3 URL that specifies the truststore for mutual TLS authentication, for example ``s3://bucket-name/key-name`` . The truststore can contain certificates from public or private certificate authorities. To update the truststore, upload a new version to S3, and then update your custom domain name to use the new version. To update the truststore, you must have permissions to access the S3 object.
            :param truststore_version: The version of the S3 object that contains your truststore. To specify a version, you must have versioning enabled for the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-mutualtlsauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                mutual_tls_authentication_property = apigateway_mixins.CfnDomainNamePropsMixin.MutualTlsAuthenticationProperty(
                    truststore_uri="truststoreUri",
                    truststore_version="truststoreVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03ed436d1bb283806e756ce50177b9863c4b0c980cf4abb49c6f18db8a22499d)
                check_type(argname="argument truststore_uri", value=truststore_uri, expected_type=type_hints["truststore_uri"])
                check_type(argname="argument truststore_version", value=truststore_version, expected_type=type_hints["truststore_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if truststore_uri is not None:
                self._values["truststore_uri"] = truststore_uri
            if truststore_version is not None:
                self._values["truststore_version"] = truststore_version

        @builtins.property
        def truststore_uri(self) -> typing.Optional[builtins.str]:
            '''An Amazon S3 URL that specifies the truststore for mutual TLS authentication, for example ``s3://bucket-name/key-name`` .

            The truststore can contain certificates from public or private certificate authorities. To update the truststore, upload a new version to S3, and then update your custom domain name to use the new version. To update the truststore, you must have permissions to access the S3 object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-mutualtlsauthentication.html#cfn-apigateway-domainname-mutualtlsauthentication-truststoreuri
            '''
            result = self._values.get("truststore_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def truststore_version(self) -> typing.Optional[builtins.str]:
            '''The version of the S3 object that contains your truststore.

            To specify a version, you must have versioning enabled for the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainname-mutualtlsauthentication.html#cfn-apigateway-domainname-mutualtlsauthentication-truststoreversion
            '''
            result = self._values.get("truststore_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualTlsAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDomainNameV2MixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_arn": "certificateArn",
        "domain_name": "domainName",
        "endpoint_access_mode": "endpointAccessMode",
        "endpoint_configuration": "endpointConfiguration",
        "policy": "policy",
        "routing_mode": "routingMode",
        "security_policy": "securityPolicy",
        "tags": "tags",
    },
)
class CfnDomainNameV2MixinProps:
    def __init__(
        self,
        *,
        certificate_arn: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        endpoint_access_mode: typing.Optional[builtins.str] = None,
        endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainNameV2PropsMixin.EndpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        policy: typing.Any = None,
        routing_mode: typing.Optional[builtins.str] = None,
        security_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainNameV2PropsMixin.

        :param certificate_arn: The reference to an AWS -managed certificate that will be used by the private endpoint for this domain name. AWS Certificate Manager is the only supported source.
        :param domain_name: Represents a custom domain name as a user-friendly host name of an API (RestApi).
        :param endpoint_access_mode: The endpoint access mode for your DomainName.
        :param endpoint_configuration: The endpoint configuration to indicate the types of endpoints an API (RestApi) or its custom domain name (DomainName) has and the IP address types that can invoke it.
        :param policy: A stringified JSON policy document that applies to the ``execute-api`` service for this DomainName regardless of the caller and Method configuration. You can use ``Fn::ToJsonString`` to enter your ``policy`` . For more information, see `Fn::ToJsonString <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ToJsonString.html>`_ .
        :param routing_mode: The routing mode for this domain name. The routing mode determines how API Gateway sends traffic from your custom domain name to your private APIs. Default: - "BASE_PATH_MAPPING_ONLY"
        :param security_policy: The Transport Layer Security (TLS) version + cipher suite for this DomainName.
        :param tags: The collection of tags. Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            # policy: Any
            
            cfn_domain_name_v2_mixin_props = apigateway_mixins.CfnDomainNameV2MixinProps(
                certificate_arn="certificateArn",
                domain_name="domainName",
                endpoint_access_mode="endpointAccessMode",
                endpoint_configuration=apigateway_mixins.CfnDomainNameV2PropsMixin.EndpointConfigurationProperty(
                    ip_address_type="ipAddressType",
                    types=["types"]
                ),
                policy=policy,
                routing_mode="routingMode",
                security_policy="securityPolicy",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fcc8c30491d071c0648d0b8a6856d37a541072560d8e69e28be59affe2cf24)
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument endpoint_access_mode", value=endpoint_access_mode, expected_type=type_hints["endpoint_access_mode"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument routing_mode", value=routing_mode, expected_type=type_hints["routing_mode"])
            check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if endpoint_access_mode is not None:
            self._values["endpoint_access_mode"] = endpoint_access_mode
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if policy is not None:
            self._values["policy"] = policy
        if routing_mode is not None:
            self._values["routing_mode"] = routing_mode
        if security_policy is not None:
            self._values["security_policy"] = security_policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''The reference to an AWS -managed certificate that will be used by the private endpoint for this domain name.

        AWS Certificate Manager is the only supported source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html#cfn-apigateway-domainnamev2-certificatearn
        '''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''Represents a custom domain name as a user-friendly host name of an API (RestApi).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html#cfn-apigateway-domainnamev2-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_access_mode(self) -> typing.Optional[builtins.str]:
        '''The endpoint access mode for your DomainName.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html#cfn-apigateway-domainnamev2-endpointaccessmode
        '''
        result = self._values.get("endpoint_access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainNameV2PropsMixin.EndpointConfigurationProperty"]]:
        '''The endpoint configuration to indicate the types of endpoints an API (RestApi) or its custom domain name (DomainName) has and the IP address types that can invoke it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html#cfn-apigateway-domainnamev2-endpointconfiguration
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainNameV2PropsMixin.EndpointConfigurationProperty"]], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''A stringified JSON policy document that applies to the ``execute-api`` service for this DomainName regardless of the caller and Method configuration.

        You can use ``Fn::ToJsonString`` to enter your ``policy`` . For more information, see `Fn::ToJsonString <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ToJsonString.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html#cfn-apigateway-domainnamev2-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def routing_mode(self) -> typing.Optional[builtins.str]:
        '''The routing mode for this domain name.

        The routing mode determines how API Gateway sends traffic from your custom domain name to your private APIs.

        :default: - "BASE_PATH_MAPPING_ONLY"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html#cfn-apigateway-domainnamev2-routingmode
        '''
        result = self._values.get("routing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_policy(self) -> typing.Optional[builtins.str]:
        '''The Transport Layer Security (TLS) version + cipher suite for this DomainName.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html#cfn-apigateway-domainnamev2-securitypolicy
        '''
        result = self._values.get("security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html#cfn-apigateway-domainnamev2-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainNameV2MixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainNameV2PropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDomainNameV2PropsMixin",
):
    '''The ``AWS::ApiGateway::DomainNameV2`` resource specifies a custom domain name for your private APIs in API Gateway.

    You can use a private custom domain name to provide a URL for your private API that's more intuitive and easier to recall.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-domainnamev2.html
    :cloudformationResource: AWS::ApiGateway::DomainNameV2
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        # policy: Any
        
        cfn_domain_name_v2_props_mixin = apigateway_mixins.CfnDomainNameV2PropsMixin(apigateway_mixins.CfnDomainNameV2MixinProps(
            certificate_arn="certificateArn",
            domain_name="domainName",
            endpoint_access_mode="endpointAccessMode",
            endpoint_configuration=apigateway_mixins.CfnDomainNameV2PropsMixin.EndpointConfigurationProperty(
                ip_address_type="ipAddressType",
                types=["types"]
            ),
            policy=policy,
            routing_mode="routingMode",
            security_policy="securityPolicy",
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
        props: typing.Union[CfnDomainNameV2MixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::DomainNameV2``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5597eeaa9adc8227c741252aaf782e74c3a36d7eb77a648cccdc3230ed32deb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b823e4d10b7d7500636cbf39af222f81859086c2671aebcb7ab01453e96a0ab8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d2f85850115a134094271f211aa4e4a343ef4e170078a1b947c96f3a4578b9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainNameV2MixinProps:
        return typing.cast(CfnDomainNameV2MixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnDomainNameV2PropsMixin.EndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_address_type": "ipAddressType", "types": "types"},
    )
    class EndpointConfigurationProperty:
        def __init__(
            self,
            *,
            ip_address_type: typing.Optional[builtins.str] = None,
            types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The endpoint configuration to indicate the types of endpoints an API (RestApi) or its custom domain name (DomainName) has and the IP address types that can invoke it.

            :param ip_address_type: The IP address types that can invoke an API (RestApi) or a DomainName. Use ``ipv4`` to allow only IPv4 addresses to invoke an API or DomainName, or use ``dualstack`` to allow both IPv4 and IPv6 addresses to invoke an API or a DomainName. For the ``PRIVATE`` endpoint type, only ``dualstack`` is supported.
            :param types: A list of endpoint types of an API (RestApi) or its custom domain name (DomainName). For an edge-optimized API and its custom domain name, the endpoint type is ``"EDGE"`` . For a regional API and its custom domain name, the endpoint type is ``REGIONAL`` . For a private API, the endpoint type is ``PRIVATE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainnamev2-endpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                endpoint_configuration_property = apigateway_mixins.CfnDomainNameV2PropsMixin.EndpointConfigurationProperty(
                    ip_address_type="ipAddressType",
                    types=["types"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a443153dc5beac1dbbe289f571f5d128868a5ad78b6f382b356c2ad29af97d53)
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
                check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type
            if types is not None:
                self._values["types"] = types

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''The IP address types that can invoke an API (RestApi) or a DomainName.

            Use ``ipv4`` to allow only IPv4 addresses to invoke an API or DomainName, or use ``dualstack`` to allow both IPv4 and IPv6 addresses to invoke an API or a DomainName. For the ``PRIVATE`` endpoint type, only ``dualstack`` is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainnamev2-endpointconfiguration.html#cfn-apigateway-domainnamev2-endpointconfiguration-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of endpoint types of an API (RestApi) or its custom domain name (DomainName).

            For an edge-optimized API and its custom domain name, the endpoint type is ``"EDGE"`` . For a regional API and its custom domain name, the endpoint type is ``REGIONAL`` . For a private API, the endpoint type is ``PRIVATE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-domainnamev2-endpointconfiguration.html#cfn-apigateway-domainnamev2-endpointconfiguration-types
            '''
            result = self._values.get("types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnGatewayResponseMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "response_parameters": "responseParameters",
        "response_templates": "responseTemplates",
        "response_type": "responseType",
        "rest_api_id": "restApiId",
        "status_code": "statusCode",
    },
)
class CfnGatewayResponseMixinProps:
    def __init__(
        self,
        *,
        response_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        response_templates: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        response_type: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGatewayResponsePropsMixin.

        :param response_parameters: Response parameters (paths, query strings and headers) of the GatewayResponse as a string-to-string map of key-value pairs.
        :param response_templates: Response templates of the GatewayResponse as a string-to-string map of key-value pairs.
        :param response_type: The response type of the associated GatewayResponse.
        :param rest_api_id: The string identifier of the associated RestApi.
        :param status_code: The HTTP status code for this GatewayResponse.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_gateway_response_mixin_props = apigateway_mixins.CfnGatewayResponseMixinProps(
                response_parameters={
                    "response_parameters_key": "responseParameters"
                },
                response_templates={
                    "response_templates_key": "responseTemplates"
                },
                response_type="responseType",
                rest_api_id="restApiId",
                status_code="statusCode"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b141a9b9541da979214c570ff0dae3750c5ad3c3abcdab2283fc98a89b9837d7)
            check_type(argname="argument response_parameters", value=response_parameters, expected_type=type_hints["response_parameters"])
            check_type(argname="argument response_templates", value=response_templates, expected_type=type_hints["response_templates"])
            check_type(argname="argument response_type", value=response_type, expected_type=type_hints["response_type"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if response_parameters is not None:
            self._values["response_parameters"] = response_parameters
        if response_templates is not None:
            self._values["response_templates"] = response_templates
        if response_type is not None:
            self._values["response_type"] = response_type
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def response_parameters(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''Response parameters (paths, query strings and headers) of the GatewayResponse as a string-to-string map of key-value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-responseparameters
        '''
        result = self._values.get("response_parameters")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def response_templates(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''Response templates of the GatewayResponse as a string-to-string map of key-value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-responsetemplates
        '''
        result = self._values.get("response_templates")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def response_type(self) -> typing.Optional[builtins.str]:
        '''The response type of the associated GatewayResponse.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-responsetype
        '''
        result = self._values.get("response_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_code(self) -> typing.Optional[builtins.str]:
        '''The HTTP status code for this GatewayResponse.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html#cfn-apigateway-gatewayresponse-statuscode
        '''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGatewayResponseMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGatewayResponsePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnGatewayResponsePropsMixin",
):
    '''The ``AWS::ApiGateway::GatewayResponse`` resource creates a gateway response for your API.

    When you delete a stack containing this resource, your custom gateway responses are reset. For more information, see `API Gateway Responses <https://docs.aws.amazon.com/apigateway/latest/developerguide/customize-gateway-responses.html#api-gateway-gatewayResponse-definition>`_ in the *API Gateway Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-gatewayresponse.html
    :cloudformationResource: AWS::ApiGateway::GatewayResponse
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_gateway_response_props_mixin = apigateway_mixins.CfnGatewayResponsePropsMixin(apigateway_mixins.CfnGatewayResponseMixinProps(
            response_parameters={
                "response_parameters_key": "responseParameters"
            },
            response_templates={
                "response_templates_key": "responseTemplates"
            },
            response_type="responseType",
            rest_api_id="restApiId",
            status_code="statusCode"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGatewayResponseMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::GatewayResponse``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea5bcb52aea73eded98b6771a2769f0cfd14f2392553e5d54f9a7db19075e91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4821cb5fa4937e6b2d3886d09ebccf1aff057393aa7af585a0f3d0656d0097e7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89342ef20c4e5d8adb5dfd84d2c84a9ca853c7688eaa4baa11e6c1f09bc3273d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGatewayResponseMixinProps:
        return typing.cast(CfnGatewayResponseMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnMethodMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key_required": "apiKeyRequired",
        "authorization_scopes": "authorizationScopes",
        "authorization_type": "authorizationType",
        "authorizer_id": "authorizerId",
        "http_method": "httpMethod",
        "integration": "integration",
        "method_responses": "methodResponses",
        "operation_name": "operationName",
        "request_models": "requestModels",
        "request_parameters": "requestParameters",
        "request_validator_id": "requestValidatorId",
        "resource_id": "resourceId",
        "rest_api_id": "restApiId",
    },
)
class CfnMethodMixinProps:
    def __init__(
        self,
        *,
        api_key_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        authorization_type: typing.Optional[builtins.str] = None,
        authorizer_id: typing.Optional[builtins.str] = None,
        http_method: typing.Optional[builtins.str] = None,
        integration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMethodPropsMixin.IntegrationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        method_responses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMethodPropsMixin.MethodResponseProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        operation_name: typing.Optional[builtins.str] = None,
        request_models: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        request_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]]] = None,
        request_validator_id: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMethodPropsMixin.

        :param api_key_required: A boolean flag specifying whether a valid ApiKey is required to invoke this method.
        :param authorization_scopes: A list of authorization scopes configured on the method. The scopes are used with a ``COGNITO_USER_POOLS`` authorizer to authorize the method invocation. The authorization works by matching the method scopes against the scopes parsed from the access token in the incoming request. The method invocation is authorized if any method scopes matches a claimed scope in the access token. Otherwise, the invocation is not authorized. When the method scope is configured, the client must provide an access token instead of an identity token for authorization purposes.
        :param authorization_type: The method's authorization type. This parameter is required. For valid values, see `Method <https://docs.aws.amazon.com/apigateway/latest/api/API_Method.html>`_ in the *API Gateway API Reference* . .. epigraph:: If you specify the ``AuthorizerId`` property, specify ``CUSTOM`` or ``COGNITO_USER_POOLS`` for this property.
        :param authorizer_id: The identifier of an authorizer to use on this method. The method's authorization type must be ``CUSTOM`` or ``COGNITO_USER_POOLS`` .
        :param http_method: The method's HTTP verb.
        :param integration: Represents an ``HTTP`` , ``HTTP_PROXY`` , ``AWS`` , ``AWS_PROXY`` , or Mock integration.
        :param method_responses: Gets a method response associated with a given HTTP status code.
        :param operation_name: A human-friendly operation identifier for the method. For example, you can assign the ``operationName`` of ``ListPets`` for the ``GET /pets`` method in the ``PetStore`` example.
        :param request_models: A key-value map specifying data schemas, represented by Model resources, (as the mapped value) of the request payloads of given content types (as the mapping key).
        :param request_parameters: A key-value map defining required or optional method request parameters that can be accepted by API Gateway. A key is a method request parameter name matching the pattern of ``method.request.{location}.{name}`` , where ``location`` is ``querystring`` , ``path`` , or ``header`` and ``name`` is a valid and unique parameter name. The value associated with the key is a Boolean flag indicating whether the parameter is required ( ``true`` ) or optional ( ``false`` ). The method request parameter names defined here are available in Integration to be mapped to integration request parameters or templates.
        :param request_validator_id: The identifier of a RequestValidator for request validation.
        :param resource_id: The Resource identifier for the MethodResponse resource.
        :param rest_api_id: The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_method_mixin_props = apigateway_mixins.CfnMethodMixinProps(
                api_key_required=False,
                authorization_scopes=["authorizationScopes"],
                authorization_type="authorizationType",
                authorizer_id="authorizerId",
                http_method="httpMethod",
                integration=apigateway_mixins.CfnMethodPropsMixin.IntegrationProperty(
                    cache_key_parameters=["cacheKeyParameters"],
                    cache_namespace="cacheNamespace",
                    connection_id="connectionId",
                    connection_type="connectionType",
                    content_handling="contentHandling",
                    credentials="credentials",
                    integration_http_method="integrationHttpMethod",
                    integration_responses=[apigateway_mixins.CfnMethodPropsMixin.IntegrationResponseProperty(
                        content_handling="contentHandling",
                        response_parameters={
                            "response_parameters_key": "responseParameters"
                        },
                        response_templates={
                            "response_templates_key": "responseTemplates"
                        },
                        selection_pattern="selectionPattern",
                        status_code="statusCode"
                    )],
                    integration_target="integrationTarget",
                    passthrough_behavior="passthroughBehavior",
                    request_parameters={
                        "request_parameters_key": "requestParameters"
                    },
                    request_templates={
                        "request_templates_key": "requestTemplates"
                    },
                    response_transfer_mode="responseTransferMode",
                    timeout_in_millis=123,
                    type="type",
                    uri="uri"
                ),
                method_responses=[apigateway_mixins.CfnMethodPropsMixin.MethodResponseProperty(
                    response_models={
                        "response_models_key": "responseModels"
                    },
                    response_parameters={
                        "response_parameters_key": False
                    },
                    status_code="statusCode"
                )],
                operation_name="operationName",
                request_models={
                    "request_models_key": "requestModels"
                },
                request_parameters={
                    "request_parameters_key": False
                },
                request_validator_id="requestValidatorId",
                resource_id="resourceId",
                rest_api_id="restApiId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e21fc26281183856b2328a79523d6206593249c46a47e879ff1f0a1ccca9af2)
            check_type(argname="argument api_key_required", value=api_key_required, expected_type=type_hints["api_key_required"])
            check_type(argname="argument authorization_scopes", value=authorization_scopes, expected_type=type_hints["authorization_scopes"])
            check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
            check_type(argname="argument authorizer_id", value=authorizer_id, expected_type=type_hints["authorizer_id"])
            check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
            check_type(argname="argument integration", value=integration, expected_type=type_hints["integration"])
            check_type(argname="argument method_responses", value=method_responses, expected_type=type_hints["method_responses"])
            check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
            check_type(argname="argument request_models", value=request_models, expected_type=type_hints["request_models"])
            check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
            check_type(argname="argument request_validator_id", value=request_validator_id, expected_type=type_hints["request_validator_id"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_key_required is not None:
            self._values["api_key_required"] = api_key_required
        if authorization_scopes is not None:
            self._values["authorization_scopes"] = authorization_scopes
        if authorization_type is not None:
            self._values["authorization_type"] = authorization_type
        if authorizer_id is not None:
            self._values["authorizer_id"] = authorizer_id
        if http_method is not None:
            self._values["http_method"] = http_method
        if integration is not None:
            self._values["integration"] = integration
        if method_responses is not None:
            self._values["method_responses"] = method_responses
        if operation_name is not None:
            self._values["operation_name"] = operation_name
        if request_models is not None:
            self._values["request_models"] = request_models
        if request_parameters is not None:
            self._values["request_parameters"] = request_parameters
        if request_validator_id is not None:
            self._values["request_validator_id"] = request_validator_id
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id

    @builtins.property
    def api_key_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean flag specifying whether a valid ApiKey is required to invoke this method.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-apikeyrequired
        '''
        result = self._values.get("api_key_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of authorization scopes configured on the method.

        The scopes are used with a ``COGNITO_USER_POOLS`` authorizer to authorize the method invocation. The authorization works by matching the method scopes against the scopes parsed from the access token in the incoming request. The method invocation is authorized if any method scopes matches a claimed scope in the access token. Otherwise, the invocation is not authorized. When the method scope is configured, the client must provide an access token instead of an identity token for authorization purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-authorizationscopes
        '''
        result = self._values.get("authorization_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def authorization_type(self) -> typing.Optional[builtins.str]:
        '''The method's authorization type.

        This parameter is required. For valid values, see `Method <https://docs.aws.amazon.com/apigateway/latest/api/API_Method.html>`_ in the *API Gateway API Reference* .
        .. epigraph::

           If you specify the ``AuthorizerId`` property, specify ``CUSTOM`` or ``COGNITO_USER_POOLS`` for this property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-authorizationtype
        '''
        result = self._values.get("authorization_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authorizer_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of an authorizer to use on this method.

        The method's authorization type must be ``CUSTOM`` or ``COGNITO_USER_POOLS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-authorizerid
        '''
        result = self._values.get("authorizer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_method(self) -> typing.Optional[builtins.str]:
        '''The method's HTTP verb.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-httpmethod
        '''
        result = self._values.get("http_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMethodPropsMixin.IntegrationProperty"]]:
        '''Represents an ``HTTP`` , ``HTTP_PROXY`` , ``AWS`` , ``AWS_PROXY`` , or Mock integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-integration
        '''
        result = self._values.get("integration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMethodPropsMixin.IntegrationProperty"]], result)

    @builtins.property
    def method_responses(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMethodPropsMixin.MethodResponseProperty"]]]]:
        '''Gets a method response associated with a given HTTP status code.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-methodresponses
        '''
        result = self._values.get("method_responses")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMethodPropsMixin.MethodResponseProperty"]]]], result)

    @builtins.property
    def operation_name(self) -> typing.Optional[builtins.str]:
        '''A human-friendly operation identifier for the method.

        For example, you can assign the ``operationName`` of ``ListPets`` for the ``GET /pets`` method in the ``PetStore`` example.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-operationname
        '''
        result = self._values.get("operation_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_models(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''A key-value map specifying data schemas, represented by Model resources, (as the mapped value) of the request payloads of given content types (as the mapping key).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-requestmodels
        '''
        result = self._values.get("request_models")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def request_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]]]:
        '''A key-value map defining required or optional method request parameters that can be accepted by API Gateway.

        A key is a method request parameter name matching the pattern of ``method.request.{location}.{name}`` , where ``location`` is ``querystring`` , ``path`` , or ``header`` and ``name`` is a valid and unique parameter name. The value associated with the key is a Boolean flag indicating whether the parameter is required ( ``true`` ) or optional ( ``false`` ). The method request parameter names defined here are available in Integration to be mapped to integration request parameters or templates.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-requestparameters
        '''
        result = self._values.get("request_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]]], result)

    @builtins.property
    def request_validator_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a RequestValidator for request validation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-requestvalidatorid
        '''
        result = self._values.get("request_validator_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The Resource identifier for the MethodResponse resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html#cfn-apigateway-method-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMethodMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMethodPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnMethodPropsMixin",
):
    '''The ``AWS::ApiGateway::Method`` resource creates API Gateway methods that define the parameters and body that clients must send in their requests.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html
    :cloudformationResource: AWS::ApiGateway::Method
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_method_props_mixin = apigateway_mixins.CfnMethodPropsMixin(apigateway_mixins.CfnMethodMixinProps(
            api_key_required=False,
            authorization_scopes=["authorizationScopes"],
            authorization_type="authorizationType",
            authorizer_id="authorizerId",
            http_method="httpMethod",
            integration=apigateway_mixins.CfnMethodPropsMixin.IntegrationProperty(
                cache_key_parameters=["cacheKeyParameters"],
                cache_namespace="cacheNamespace",
                connection_id="connectionId",
                connection_type="connectionType",
                content_handling="contentHandling",
                credentials="credentials",
                integration_http_method="integrationHttpMethod",
                integration_responses=[apigateway_mixins.CfnMethodPropsMixin.IntegrationResponseProperty(
                    content_handling="contentHandling",
                    response_parameters={
                        "response_parameters_key": "responseParameters"
                    },
                    response_templates={
                        "response_templates_key": "responseTemplates"
                    },
                    selection_pattern="selectionPattern",
                    status_code="statusCode"
                )],
                integration_target="integrationTarget",
                passthrough_behavior="passthroughBehavior",
                request_parameters={
                    "request_parameters_key": "requestParameters"
                },
                request_templates={
                    "request_templates_key": "requestTemplates"
                },
                response_transfer_mode="responseTransferMode",
                timeout_in_millis=123,
                type="type",
                uri="uri"
            ),
            method_responses=[apigateway_mixins.CfnMethodPropsMixin.MethodResponseProperty(
                response_models={
                    "response_models_key": "responseModels"
                },
                response_parameters={
                    "response_parameters_key": False
                },
                status_code="statusCode"
            )],
            operation_name="operationName",
            request_models={
                "request_models_key": "requestModels"
            },
            request_parameters={
                "request_parameters_key": False
            },
            request_validator_id="requestValidatorId",
            resource_id="resourceId",
            rest_api_id="restApiId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMethodMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::Method``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045cca9c6a73a97d0f4b5203f34b52067bd4be43ee2cb6c68efe885120d69c1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43030e793aded1f77f1a6a1886e2657d6e2c11bca001338a7de9805a1970ff7f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23e139a017586ac5c63ea581c6b3c1119e5675e478012f3104513b95c5d0ef1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMethodMixinProps:
        return typing.cast(CfnMethodMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnMethodPropsMixin.IntegrationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cache_key_parameters": "cacheKeyParameters",
            "cache_namespace": "cacheNamespace",
            "connection_id": "connectionId",
            "connection_type": "connectionType",
            "content_handling": "contentHandling",
            "credentials": "credentials",
            "integration_http_method": "integrationHttpMethod",
            "integration_responses": "integrationResponses",
            "integration_target": "integrationTarget",
            "passthrough_behavior": "passthroughBehavior",
            "request_parameters": "requestParameters",
            "request_templates": "requestTemplates",
            "response_transfer_mode": "responseTransferMode",
            "timeout_in_millis": "timeoutInMillis",
            "type": "type",
            "uri": "uri",
        },
    )
    class IntegrationProperty:
        def __init__(
            self,
            *,
            cache_key_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
            cache_namespace: typing.Optional[builtins.str] = None,
            connection_id: typing.Optional[builtins.str] = None,
            connection_type: typing.Optional[builtins.str] = None,
            content_handling: typing.Optional[builtins.str] = None,
            credentials: typing.Optional[builtins.str] = None,
            integration_http_method: typing.Optional[builtins.str] = None,
            integration_responses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMethodPropsMixin.IntegrationResponseProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            integration_target: typing.Optional[builtins.str] = None,
            passthrough_behavior: typing.Optional[builtins.str] = None,
            request_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            request_templates: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            response_transfer_mode: typing.Optional[builtins.str] = None,
            timeout_in_millis: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
            uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Integration`` is a property of the `AWS::ApiGateway::Method <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html>`_ resource that specifies information about the target backend that a method calls.

            :param cache_key_parameters: A list of request parameters whose values API Gateway caches. To be valid values for ``cacheKeyParameters`` , these parameters must also be specified for Method ``requestParameters`` .
            :param cache_namespace: Specifies a group of related cached parameters. By default, API Gateway uses the resource ID as the ``cacheNamespace`` . You can specify the same ``cacheNamespace`` across resources to return the same cached data for requests to different resources.
            :param connection_id: The ID of the VpcLink used for the integration when ``connectionType=VPC_LINK`` and undefined, otherwise.
            :param connection_type: The type of the network connection to the integration endpoint. The valid value is ``INTERNET`` for connections through the public routable internet or ``VPC_LINK`` for private connections between API Gateway and a network load balancer in a VPC. The default value is ``INTERNET`` .
            :param content_handling: Specifies how to handle request payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors: If this property is not defined, the request payload will be passed through from the method request to integration request without modification, provided that the ``passthroughBehavior`` is configured to support payload pass-through.
            :param credentials: Specifies the credentials required for the integration, if any. For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string ``arn:aws:iam::\\*:user/\\*`` . To use resource-based permissions on supported AWS services, specify null.
            :param integration_http_method: Specifies the integration's HTTP method type. For the Type property, if you specify ``MOCK`` , this property is optional. For Lambda integrations, you must set the integration method to ``POST`` . For all other types, you must specify this property.
            :param integration_responses: Specifies the integration's responses.
            :param integration_target: The ALB or NLB listener to send the request to. Only supported for private integrations that use VPC links V2.
            :param passthrough_behavior: Specifies how the method request body of an unmapped content type will be passed through the integration request to the back end without transformation. A content type is unmapped if no mapping template is defined in the integration or the content type does not match any of the mapped content types, as specified in ``requestTemplates`` . The valid value is one of the following: ``WHEN_NO_MATCH`` : passes the method request body through the integration request to the back end without transformation when the method request content type does not match any content type associated with the mapping templates defined in the integration request. ``WHEN_NO_TEMPLATES`` : passes the method request body through the integration request to the back end without transformation when no mapping template is defined in the integration request. If a template is defined when this option is selected, the method request of an unmapped content-type will be rejected with an HTTP 415 Unsupported Media Type response. ``NEVER`` : rejects the method request with an HTTP 415 Unsupported Media Type response when either the method request content type does not match any content type associated with the mapping templates defined in the integration request or no mapping template is defined in the integration request.
            :param request_parameters: A key-value map specifying request parameters that are passed from the method request to the back end. The key is an integration request parameter name and the associated value is a method request parameter value or static value that must be enclosed within single quotes and pre-encoded as required by the back end. The method request parameter value must match the pattern of ``method.request.{location}.{name}`` , where ``location`` is ``querystring`` , ``path`` , or ``header`` and ``name`` must be a valid and unique method request parameter name.
            :param request_templates: Represents a map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client. The content type value is the key in this map, and the template (as a String) is the value.
            :param response_transfer_mode: The response transfer mode of the integration. Use ``STREAM`` to have API Gateway stream response your back to you or use ``BUFFERED`` to have API Gateway wait to receive the complete response before beginning transmission. Default: - "BUFFERED"
            :param timeout_in_millis: Custom timeout between 50 and 29,000 milliseconds. The default value is 29,000 milliseconds or 29 seconds. You can increase the default value to longer than 29 seconds for Regional or private APIs only.
            :param type: Specifies an API method integration type. The valid value is one of the following:. For the HTTP and HTTP proxy integrations, each integration can specify a protocol ( ``http/https`` ), port and path. Standard 80 and 443 ports are supported as well as custom ports above 1024. An HTTP or HTTP proxy integration with a ``connectionType`` of ``VPC_LINK`` is referred to as a private integration and uses a VpcLink to connect API Gateway to a network load balancer of a VPC.
            :param uri: Specifies Uniform Resource Identifier (URI) of the integration endpoint. For ``HTTP`` or ``HTTP_PROXY`` integrations, the URI must be a fully formed, encoded HTTP(S) URL according to the RFC-3986 specification for standard integrations. If ``connectionType`` is ``VPC_LINK`` specify the Network Load Balancer DNS name. For ``AWS`` or ``AWS_PROXY`` integrations, the URI is of the form ``arn:aws:apigateway:{region}:{subdomain.service|service}:path|action/{service_api}`` . Here, {Region} is the API Gateway region (e.g., us-east-1); {service} is the name of the integrated AWS service (e.g., s3); and {subdomain} is a designated subdomain supported by certain AWS service for fast host-name lookup. action can be used for an AWS service action-based API, using an Action={name}&{p1}={v1}&p2={v2}... query string. The ensuing {service_api} refers to a supported action {name} plus any required input parameters. Alternatively, path can be used for an AWS service path-based API. The ensuing service_api refers to the path to an AWS service resource, including the region of the integrated AWS service, if applicable. For example, for integration with the S3 API of GetObject, the uri can be either ``arn:aws:apigateway:us-west-2:s3:action/GetObject&Bucket={bucket}&Key={key}`` or ``arn:aws:apigateway:us-west-2:s3:path/{bucket}/{key}``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                integration_property = apigateway_mixins.CfnMethodPropsMixin.IntegrationProperty(
                    cache_key_parameters=["cacheKeyParameters"],
                    cache_namespace="cacheNamespace",
                    connection_id="connectionId",
                    connection_type="connectionType",
                    content_handling="contentHandling",
                    credentials="credentials",
                    integration_http_method="integrationHttpMethod",
                    integration_responses=[apigateway_mixins.CfnMethodPropsMixin.IntegrationResponseProperty(
                        content_handling="contentHandling",
                        response_parameters={
                            "response_parameters_key": "responseParameters"
                        },
                        response_templates={
                            "response_templates_key": "responseTemplates"
                        },
                        selection_pattern="selectionPattern",
                        status_code="statusCode"
                    )],
                    integration_target="integrationTarget",
                    passthrough_behavior="passthroughBehavior",
                    request_parameters={
                        "request_parameters_key": "requestParameters"
                    },
                    request_templates={
                        "request_templates_key": "requestTemplates"
                    },
                    response_transfer_mode="responseTransferMode",
                    timeout_in_millis=123,
                    type="type",
                    uri="uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36a8f4a5f2386af3ce6bc9839c701ff9b13e41d1891c7ef699d7f9d60c04a42f)
                check_type(argname="argument cache_key_parameters", value=cache_key_parameters, expected_type=type_hints["cache_key_parameters"])
                check_type(argname="argument cache_namespace", value=cache_namespace, expected_type=type_hints["cache_namespace"])
                check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
                check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
                check_type(argname="argument content_handling", value=content_handling, expected_type=type_hints["content_handling"])
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
                check_type(argname="argument integration_http_method", value=integration_http_method, expected_type=type_hints["integration_http_method"])
                check_type(argname="argument integration_responses", value=integration_responses, expected_type=type_hints["integration_responses"])
                check_type(argname="argument integration_target", value=integration_target, expected_type=type_hints["integration_target"])
                check_type(argname="argument passthrough_behavior", value=passthrough_behavior, expected_type=type_hints["passthrough_behavior"])
                check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
                check_type(argname="argument request_templates", value=request_templates, expected_type=type_hints["request_templates"])
                check_type(argname="argument response_transfer_mode", value=response_transfer_mode, expected_type=type_hints["response_transfer_mode"])
                check_type(argname="argument timeout_in_millis", value=timeout_in_millis, expected_type=type_hints["timeout_in_millis"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cache_key_parameters is not None:
                self._values["cache_key_parameters"] = cache_key_parameters
            if cache_namespace is not None:
                self._values["cache_namespace"] = cache_namespace
            if connection_id is not None:
                self._values["connection_id"] = connection_id
            if connection_type is not None:
                self._values["connection_type"] = connection_type
            if content_handling is not None:
                self._values["content_handling"] = content_handling
            if credentials is not None:
                self._values["credentials"] = credentials
            if integration_http_method is not None:
                self._values["integration_http_method"] = integration_http_method
            if integration_responses is not None:
                self._values["integration_responses"] = integration_responses
            if integration_target is not None:
                self._values["integration_target"] = integration_target
            if passthrough_behavior is not None:
                self._values["passthrough_behavior"] = passthrough_behavior
            if request_parameters is not None:
                self._values["request_parameters"] = request_parameters
            if request_templates is not None:
                self._values["request_templates"] = request_templates
            if response_transfer_mode is not None:
                self._values["response_transfer_mode"] = response_transfer_mode
            if timeout_in_millis is not None:
                self._values["timeout_in_millis"] = timeout_in_millis
            if type is not None:
                self._values["type"] = type
            if uri is not None:
                self._values["uri"] = uri

        @builtins.property
        def cache_key_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of request parameters whose values API Gateway caches.

            To be valid values for ``cacheKeyParameters`` , these parameters must also be specified for Method ``requestParameters`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-cachekeyparameters
            '''
            result = self._values.get("cache_key_parameters")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def cache_namespace(self) -> typing.Optional[builtins.str]:
            '''Specifies a group of related cached parameters.

            By default, API Gateway uses the resource ID as the ``cacheNamespace`` . You can specify the same ``cacheNamespace`` across resources to return the same cached data for requests to different resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-cachenamespace
            '''
            result = self._values.get("cache_namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connection_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the VpcLink used for the integration when ``connectionType=VPC_LINK`` and undefined, otherwise.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-connectionid
            '''
            result = self._values.get("connection_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connection_type(self) -> typing.Optional[builtins.str]:
            '''The type of the network connection to the integration endpoint.

            The valid value is ``INTERNET`` for connections through the public routable internet or ``VPC_LINK`` for private connections between API Gateway and a network load balancer in a VPC. The default value is ``INTERNET`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-connectiontype
            '''
            result = self._values.get("connection_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def content_handling(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle request payload content type conversions.

            Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors:

            If this property is not defined, the request payload will be passed through from the method request to integration request without modification, provided that the ``passthroughBehavior`` is configured to support payload pass-through.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-contenthandling
            '''
            result = self._values.get("content_handling")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def credentials(self) -> typing.Optional[builtins.str]:
            '''Specifies the credentials required for the integration, if any.

            For AWS integrations, three options are available. To specify an IAM Role for API Gateway to assume, use the role's Amazon Resource Name (ARN). To require that the caller's identity be passed through from the request, specify the string ``arn:aws:iam::\\*:user/\\*`` . To use resource-based permissions on supported AWS services, specify null.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-credentials
            '''
            result = self._values.get("credentials")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integration_http_method(self) -> typing.Optional[builtins.str]:
            '''Specifies the integration's HTTP method type.

            For the Type property, if you specify ``MOCK`` , this property is optional. For Lambda integrations, you must set the integration method to ``POST`` . For all other types, you must specify this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-integrationhttpmethod
            '''
            result = self._values.get("integration_http_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integration_responses(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMethodPropsMixin.IntegrationResponseProperty"]]]]:
            '''Specifies the integration's responses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-integrationresponses
            '''
            result = self._values.get("integration_responses")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMethodPropsMixin.IntegrationResponseProperty"]]]], result)

        @builtins.property
        def integration_target(self) -> typing.Optional[builtins.str]:
            '''The ALB or NLB listener to send the request to.

            Only supported for private integrations that use VPC links V2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-integrationtarget
            '''
            result = self._values.get("integration_target")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def passthrough_behavior(self) -> typing.Optional[builtins.str]:
            '''Specifies how the method request body of an unmapped content type will be passed through the integration request to the back end without transformation.

            A content type is unmapped if no mapping template is defined in the integration or the content type does not match any of the mapped content types, as specified in ``requestTemplates`` . The valid value is one of the following: ``WHEN_NO_MATCH`` : passes the method request body through the integration request to the back end without transformation when the method request content type does not match any content type associated with the mapping templates defined in the integration request. ``WHEN_NO_TEMPLATES`` : passes the method request body through the integration request to the back end without transformation when no mapping template is defined in the integration request. If a template is defined when this option is selected, the method request of an unmapped content-type will be rejected with an HTTP 415 Unsupported Media Type response. ``NEVER`` : rejects the method request with an HTTP 415 Unsupported Media Type response when either the method request content type does not match any content type associated with the mapping templates defined in the integration request or no mapping template is defined in the integration request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-passthroughbehavior
            '''
            result = self._values.get("passthrough_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def request_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A key-value map specifying request parameters that are passed from the method request to the back end.

            The key is an integration request parameter name and the associated value is a method request parameter value or static value that must be enclosed within single quotes and pre-encoded as required by the back end. The method request parameter value must match the pattern of ``method.request.{location}.{name}`` , where ``location`` is ``querystring`` , ``path`` , or ``header`` and ``name`` must be a valid and unique method request parameter name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-requestparameters
            '''
            result = self._values.get("request_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def request_templates(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Represents a map of Velocity templates that are applied on the request payload based on the value of the Content-Type header sent by the client.

            The content type value is the key in this map, and the template (as a String) is the value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-requesttemplates
            '''
            result = self._values.get("request_templates")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def response_transfer_mode(self) -> typing.Optional[builtins.str]:
            '''The response transfer mode of the integration.

            Use ``STREAM`` to have API Gateway stream response your back to you or use ``BUFFERED`` to have API Gateway wait to receive the complete response before beginning transmission.

            :default: - "BUFFERED"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-responsetransfermode
            '''
            result = self._values.get("response_transfer_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
            '''Custom timeout between 50 and 29,000 milliseconds.

            The default value is 29,000 milliseconds or 29 seconds. You can increase the default value to longer than 29 seconds for Regional or private APIs only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-timeoutinmillis
            '''
            result = self._values.get("timeout_in_millis")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies an API method integration type. The valid value is one of the following:.

            For the HTTP and HTTP proxy integrations, each integration can specify a protocol ( ``http/https`` ), port and path. Standard 80 and 443 ports are supported as well as custom ports above 1024. An HTTP or HTTP proxy integration with a ``connectionType`` of ``VPC_LINK`` is referred to as a private integration and uses a VpcLink to connect API Gateway to a network load balancer of a VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uri(self) -> typing.Optional[builtins.str]:
            '''Specifies Uniform Resource Identifier (URI) of the integration endpoint.

            For ``HTTP`` or ``HTTP_PROXY`` integrations, the URI must be a fully formed, encoded HTTP(S) URL according to the RFC-3986 specification for standard integrations. If ``connectionType`` is ``VPC_LINK`` specify the Network Load Balancer DNS name. For ``AWS`` or ``AWS_PROXY`` integrations, the URI is of the form ``arn:aws:apigateway:{region}:{subdomain.service|service}:path|action/{service_api}`` . Here, {Region} is the API Gateway region (e.g., us-east-1); {service} is the name of the integrated AWS service (e.g., s3); and {subdomain} is a designated subdomain supported by certain AWS service for fast host-name lookup. action can be used for an AWS service action-based API, using an Action={name}&{p1}={v1}&p2={v2}... query string. The ensuing {service_api} refers to a supported action {name} plus any required input parameters. Alternatively, path can be used for an AWS service path-based API. The ensuing service_api refers to the path to an AWS service resource, including the region of the integrated AWS service, if applicable. For example, for integration with the S3 API of GetObject, the uri can be either ``arn:aws:apigateway:us-west-2:s3:action/GetObject&Bucket={bucket}&Key={key}`` or ``arn:aws:apigateway:us-west-2:s3:path/{bucket}/{key}``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integration.html#cfn-apigateway-method-integration-uri
            '''
            result = self._values.get("uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntegrationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnMethodPropsMixin.IntegrationResponseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content_handling": "contentHandling",
            "response_parameters": "responseParameters",
            "response_templates": "responseTemplates",
            "selection_pattern": "selectionPattern",
            "status_code": "statusCode",
        },
    )
    class IntegrationResponseProperty:
        def __init__(
            self,
            *,
            content_handling: typing.Optional[builtins.str] = None,
            response_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            response_templates: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            selection_pattern: typing.Optional[builtins.str] = None,
            status_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``IntegrationResponse`` is a property of the `Amazon API Gateway Method Integration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apitgateway-method-integration.html>`_ property type that specifies the response that API Gateway sends after a method's backend finishes processing a request.

            :param content_handling: Specifies how to handle response payload content type conversions. Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors: If this property is not defined, the response payload will be passed through from the integration response to the method response without modification.
            :param response_parameters: A key-value map specifying response parameters that are passed to the method response from the back end. The key is a method response header parameter name and the mapped value is an integration response header value, a static value enclosed within a pair of single quotes, or a JSON expression from the integration response body. The mapping key must match the pattern of ``method.response.header.{name}`` , where ``name`` is a valid and unique header name. The mapped non-static value must match the pattern of ``integration.response.header.{name}`` or ``integration.response.body.{JSON-expression}`` , where ``name`` is a valid and unique response header name and ``JSON-expression`` is a valid JSON expression without the ``$`` prefix.
            :param response_templates: Specifies the templates used to transform the integration response body. Response templates are represented as a key/value map, with a content-type as the key and a template as the value.
            :param selection_pattern: Specifies the regular expression (regex) pattern used to choose an integration response based on the response from the back end. For example, if the success response returns nothing and the error response returns some string, you could use the ``.+`` regex to match error response. However, make sure that the error response does not contain any newline ( ``\\n`` ) character in such cases. If the back end is an AWS Lambda function, the AWS Lambda function error header is matched. For all other HTTP and AWS back ends, the HTTP status code is matched.
            :param status_code: Specifies the status code that is used to map the integration response to an existing MethodResponse.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integrationresponse.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                integration_response_property = apigateway_mixins.CfnMethodPropsMixin.IntegrationResponseProperty(
                    content_handling="contentHandling",
                    response_parameters={
                        "response_parameters_key": "responseParameters"
                    },
                    response_templates={
                        "response_templates_key": "responseTemplates"
                    },
                    selection_pattern="selectionPattern",
                    status_code="statusCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b754110af3c6f3f5c00e605716b0ddd545dd1c050eacdb95bb6e2f379dee3b5)
                check_type(argname="argument content_handling", value=content_handling, expected_type=type_hints["content_handling"])
                check_type(argname="argument response_parameters", value=response_parameters, expected_type=type_hints["response_parameters"])
                check_type(argname="argument response_templates", value=response_templates, expected_type=type_hints["response_templates"])
                check_type(argname="argument selection_pattern", value=selection_pattern, expected_type=type_hints["selection_pattern"])
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content_handling is not None:
                self._values["content_handling"] = content_handling
            if response_parameters is not None:
                self._values["response_parameters"] = response_parameters
            if response_templates is not None:
                self._values["response_templates"] = response_templates
            if selection_pattern is not None:
                self._values["selection_pattern"] = selection_pattern
            if status_code is not None:
                self._values["status_code"] = status_code

        @builtins.property
        def content_handling(self) -> typing.Optional[builtins.str]:
            '''Specifies how to handle response payload content type conversions.

            Supported values are ``CONVERT_TO_BINARY`` and ``CONVERT_TO_TEXT`` , with the following behaviors:

            If this property is not defined, the response payload will be passed through from the integration response to the method response without modification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integrationresponse.html#cfn-apigateway-method-integrationresponse-contenthandling
            '''
            result = self._values.get("content_handling")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def response_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A key-value map specifying response parameters that are passed to the method response from the back end.

            The key is a method response header parameter name and the mapped value is an integration response header value, a static value enclosed within a pair of single quotes, or a JSON expression from the integration response body. The mapping key must match the pattern of ``method.response.header.{name}`` , where ``name`` is a valid and unique header name. The mapped non-static value must match the pattern of ``integration.response.header.{name}`` or ``integration.response.body.{JSON-expression}`` , where ``name`` is a valid and unique response header name and ``JSON-expression`` is a valid JSON expression without the ``$`` prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integrationresponse.html#cfn-apigateway-method-integrationresponse-responseparameters
            '''
            result = self._values.get("response_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def response_templates(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies the templates used to transform the integration response body.

            Response templates are represented as a key/value map, with a content-type as the key and a template as the value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integrationresponse.html#cfn-apigateway-method-integrationresponse-responsetemplates
            '''
            result = self._values.get("response_templates")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def selection_pattern(self) -> typing.Optional[builtins.str]:
            '''Specifies the regular expression (regex) pattern used to choose an integration response based on the response from the back end.

            For example, if the success response returns nothing and the error response returns some string, you could use the ``.+`` regex to match error response. However, make sure that the error response does not contain any newline ( ``\\n`` ) character in such cases. If the back end is an AWS Lambda function, the AWS Lambda function error header is matched. For all other HTTP and AWS back ends, the HTTP status code is matched.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integrationresponse.html#cfn-apigateway-method-integrationresponse-selectionpattern
            '''
            result = self._values.get("selection_pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_code(self) -> typing.Optional[builtins.str]:
            '''Specifies the status code that is used to map the integration response to an existing MethodResponse.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-integrationresponse.html#cfn-apigateway-method-integrationresponse-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntegrationResponseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnMethodPropsMixin.MethodResponseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "response_models": "responseModels",
            "response_parameters": "responseParameters",
            "status_code": "statusCode",
        },
    )
    class MethodResponseProperty:
        def __init__(
            self,
            *,
            response_models: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            response_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]]] = None,
            status_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a method response of a given HTTP status code returned to the client.

            The method response is passed from the back end through the associated integration response that can be transformed using a mapping template.

            :param response_models: Specifies the Model resources used for the response's content-type. Response models are represented as a key/value map, with a content-type as the key and a Model name as the value.
            :param response_parameters: A key-value map specifying required or optional response parameters that API Gateway can send back to the caller. A key defines a method response header and the value specifies whether the associated method response header is required or not. The expression of the key must match the pattern ``method.response.header.{name}`` , where ``name`` is a valid and unique header name. API Gateway passes certain integration response data to the method response headers specified here according to the mapping you prescribe in the API's IntegrationResponse. The integration response data that can be mapped include an integration response header expressed in ``integration.response.header.{name}`` , a static value enclosed within a pair of single quotes (e.g., ``'application/json'`` ), or a JSON expression from the back-end response payload in the form of ``integration.response.body.{JSON-expression}`` , where ``JSON-expression`` is a valid JSON expression without the ``$`` prefix.)
            :param status_code: The method response's status code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-methodresponse.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                method_response_property = apigateway_mixins.CfnMethodPropsMixin.MethodResponseProperty(
                    response_models={
                        "response_models_key": "responseModels"
                    },
                    response_parameters={
                        "response_parameters_key": False
                    },
                    status_code="statusCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d14dad9f7c8d3e9e0e26370af2b281d6f75c9f3baa50eb4476bd2c884f513c22)
                check_type(argname="argument response_models", value=response_models, expected_type=type_hints["response_models"])
                check_type(argname="argument response_parameters", value=response_parameters, expected_type=type_hints["response_parameters"])
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if response_models is not None:
                self._values["response_models"] = response_models
            if response_parameters is not None:
                self._values["response_parameters"] = response_parameters
            if status_code is not None:
                self._values["status_code"] = status_code

        @builtins.property
        def response_models(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies the Model resources used for the response's content-type.

            Response models are represented as a key/value map, with a content-type as the key and a Model name as the value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-methodresponse.html#cfn-apigateway-method-methodresponse-responsemodels
            '''
            result = self._values.get("response_models")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def response_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]]]:
            '''A key-value map specifying required or optional response parameters that API Gateway can send back to the caller.

            A key defines a method response header and the value specifies whether the associated method response header is required or not. The expression of the key must match the pattern ``method.response.header.{name}`` , where ``name`` is a valid and unique header name. API Gateway passes certain integration response data to the method response headers specified here according to the mapping you prescribe in the API's IntegrationResponse. The integration response data that can be mapped include an integration response header expressed in ``integration.response.header.{name}`` , a static value enclosed within a pair of single quotes (e.g., ``'application/json'`` ), or a JSON expression from the back-end response payload in the form of ``integration.response.body.{JSON-expression}`` , where ``JSON-expression`` is a valid JSON expression without the ``$`` prefix.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-methodresponse.html#cfn-apigateway-method-methodresponse-responseparameters
            '''
            result = self._values.get("response_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]]], result)

        @builtins.property
        def status_code(self) -> typing.Optional[builtins.str]:
            '''The method response's status code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-method-methodresponse.html#cfn-apigateway-method-methodresponse-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MethodResponseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnModelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_type": "contentType",
        "description": "description",
        "name": "name",
        "rest_api_id": "restApiId",
        "schema": "schema",
    },
)
class CfnModelMixinProps:
    def __init__(
        self,
        *,
        content_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
        schema: typing.Any = None,
    ) -> None:
        '''Properties for CfnModelPropsMixin.

        :param content_type: The content-type for the model.
        :param description: The description of the model.
        :param name: A name for the model. If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the model name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param rest_api_id: The string identifier of the associated RestApi.
        :param schema: The schema for the model. For ``application/json`` models, this should be JSON schema draft 4 model. Do not include "* /" characters in the description of any properties because such "* /" characters may be interpreted as the closing marker for comments in some languages, such as Java or JavaScript, causing the installation of your API's SDK generated by API Gateway to fail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            # schema: Any
            
            cfn_model_mixin_props = apigateway_mixins.CfnModelMixinProps(
                content_type="contentType",
                description="description",
                name="name",
                rest_api_id="restApiId",
                schema=schema
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad1149641ec406ba336580f3ea73b75dc32971c51fbaec356afd135a73f1963)
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_type is not None:
            self._values["content_type"] = content_type
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''The content-type for the model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-contenttype
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the model.

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the model name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Any:
        '''The schema for the model.

        For ``application/json`` models, this should be JSON schema draft 4 model. Do not include "* /" characters in the description of any properties because such "* /" characters may be interpreted as the closing marker for comments in some languages, such as Java or JavaScript, causing the installation of your API's SDK generated by API Gateway to fail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html#cfn-apigateway-model-schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnModelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnModelPropsMixin",
):
    '''The ``AWS::ApiGateway::Model`` resource defines the structure of a request or response payload for an API method.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-model.html
    :cloudformationResource: AWS::ApiGateway::Model
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        # schema: Any
        
        cfn_model_props_mixin = apigateway_mixins.CfnModelPropsMixin(apigateway_mixins.CfnModelMixinProps(
            content_type="contentType",
            description="description",
            name="name",
            rest_api_id="restApiId",
            schema=schema
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnModelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::Model``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f63e16db1759dc264ea682e1d837601dafb5359751b5dba8114cfda4e395f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0e71f4b0c577341fde41d5bd8ce552598fde138dd73c568226fd3b6e90e997f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2b6c1cc250eaf539405c23e00f684406117f1280de535cde7b6b051eb2de05)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnModelMixinProps:
        return typing.cast(CfnModelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnRequestValidatorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "rest_api_id": "restApiId",
        "validate_request_body": "validateRequestBody",
        "validate_request_parameters": "validateRequestParameters",
    },
)
class CfnRequestValidatorMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
        validate_request_body: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        validate_request_parameters: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnRequestValidatorPropsMixin.

        :param name: The name of this RequestValidator.
        :param rest_api_id: The string identifier of the associated RestApi.
        :param validate_request_body: A Boolean flag to indicate whether to validate a request body according to the configured Model schema.
        :param validate_request_parameters: A Boolean flag to indicate whether to validate request parameters ( ``true`` ) or not ( ``false`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_request_validator_mixin_props = apigateway_mixins.CfnRequestValidatorMixinProps(
                name="name",
                rest_api_id="restApiId",
                validate_request_body=False,
                validate_request_parameters=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3ffe6ce422e7bbe86ff702290bb0bc96460f98fd5c9bab01e98ea373d25a44)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            check_type(argname="argument validate_request_body", value=validate_request_body, expected_type=type_hints["validate_request_body"])
            check_type(argname="argument validate_request_parameters", value=validate_request_parameters, expected_type=type_hints["validate_request_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id
        if validate_request_body is not None:
            self._values["validate_request_body"] = validate_request_body
        if validate_request_parameters is not None:
            self._values["validate_request_parameters"] = validate_request_parameters

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this RequestValidator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_request_body(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean flag to indicate whether to validate a request body according to the configured Model schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-validaterequestbody
        '''
        result = self._values.get("validate_request_body")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def validate_request_parameters(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean flag to indicate whether to validate request parameters ( ``true`` ) or not ( ``false`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html#cfn-apigateway-requestvalidator-validaterequestparameters
        '''
        result = self._values.get("validate_request_parameters")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRequestValidatorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRequestValidatorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnRequestValidatorPropsMixin",
):
    '''The ``AWS::ApiGateway::RequestValidator`` resource sets up basic validation rules for incoming requests to your API.

    For more information, see `Enable Basic Request Validation for an API in API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-request-validation.html>`_ in the *API Gateway Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-requestvalidator.html
    :cloudformationResource: AWS::ApiGateway::RequestValidator
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_request_validator_props_mixin = apigateway_mixins.CfnRequestValidatorPropsMixin(apigateway_mixins.CfnRequestValidatorMixinProps(
            name="name",
            rest_api_id="restApiId",
            validate_request_body=False,
            validate_request_parameters=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRequestValidatorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::RequestValidator``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc80f0de96075e38efffcc99be5c82d5dc5bbf2c2fe588eace990fdf7ebc8c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f62c1d537d628ae2c073ff8501ab402d814c1bde8cedbcfd457c193de49eb4c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adae5ca91332c20cbb9baaf3dd993855f42258b12f873b9213542eba30715509)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRequestValidatorMixinProps:
        return typing.cast(CfnRequestValidatorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnResourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "parent_id": "parentId",
        "path_part": "pathPart",
        "rest_api_id": "restApiId",
    },
)
class CfnResourceMixinProps:
    def __init__(
        self,
        *,
        parent_id: typing.Optional[builtins.str] = None,
        path_part: typing.Optional[builtins.str] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourcePropsMixin.

        :param parent_id: The parent resource's identifier.
        :param path_part: The last path segment for this resource.
        :param rest_api_id: The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_resource_mixin_props = apigateway_mixins.CfnResourceMixinProps(
                parent_id="parentId",
                path_part="pathPart",
                rest_api_id="restApiId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16e4f5ad32bcf9a1df350143f97eb1bde9339877f5daac8d8d48c1302d51c6f)
            check_type(argname="argument parent_id", value=parent_id, expected_type=type_hints["parent_id"])
            check_type(argname="argument path_part", value=path_part, expected_type=type_hints["path_part"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parent_id is not None:
            self._values["parent_id"] = parent_id
        if path_part is not None:
            self._values["path_part"] = path_part
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id

    @builtins.property
    def parent_id(self) -> typing.Optional[builtins.str]:
        '''The parent resource's identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html#cfn-apigateway-resource-parentid
        '''
        result = self._values.get("parent_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_part(self) -> typing.Optional[builtins.str]:
        '''The last path segment for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html#cfn-apigateway-resource-pathpart
        '''
        result = self._values.get("path_part")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html#cfn-apigateway-resource-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnResourcePropsMixin",
):
    '''The ``AWS::ApiGateway::Resource`` resource creates a resource in an API.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html
    :cloudformationResource: AWS::ApiGateway::Resource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_resource_props_mixin = apigateway_mixins.CfnResourcePropsMixin(apigateway_mixins.CfnResourceMixinProps(
            parent_id="parentId",
            path_part="pathPart",
            rest_api_id="restApiId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::Resource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__862169161dbb247481122ac401878fe77e8beb3b63f4eac0d8547c58ee013d40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a91f26050d12f341624025a5e34885ec71c496c3b386209f3e44054503eeb1c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc02974fa705d3310e4bb2e3705c248d8258bc7a150240e8c763e76c13fbe9eb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceMixinProps:
        return typing.cast(CfnResourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnRestApiMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_key_source_type": "apiKeySourceType",
        "binary_media_types": "binaryMediaTypes",
        "body": "body",
        "body_s3_location": "bodyS3Location",
        "clone_from": "cloneFrom",
        "description": "description",
        "disable_execute_api_endpoint": "disableExecuteApiEndpoint",
        "endpoint_access_mode": "endpointAccessMode",
        "endpoint_configuration": "endpointConfiguration",
        "fail_on_warnings": "failOnWarnings",
        "minimum_compression_size": "minimumCompressionSize",
        "mode": "mode",
        "name": "name",
        "parameters": "parameters",
        "policy": "policy",
        "security_policy": "securityPolicy",
        "tags": "tags",
    },
)
class CfnRestApiMixinProps:
    def __init__(
        self,
        *,
        api_key_source_type: typing.Optional[builtins.str] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        body: typing.Any = None,
        body_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRestApiPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        clone_from: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        endpoint_access_mode: typing.Optional[builtins.str] = None,
        endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRestApiPropsMixin.EndpointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
        mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        policy: typing.Any = None,
        security_policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRestApiPropsMixin.

        :param api_key_source_type: The source of the API key for metering requests according to a usage plan. Valid values are: ``HEADER`` to read the API key from the ``X-API-Key`` header of a request. ``AUTHORIZER`` to read the API key from the ``UsageIdentifierKey`` from a custom authorizer.
        :param binary_media_types: The list of binary media types supported by the RestApi. By default, the RestApi supports only UTF-8-encoded text payloads.
        :param body: An OpenAPI specification that defines a set of RESTful APIs in JSON format. For YAML templates, you can also provide the specification in YAML format.
        :param body_s3_location: The Amazon Simple Storage Service (Amazon S3) location that points to an OpenAPI file, which defines a set of RESTful APIs in JSON or YAML format.
        :param clone_from: The ID of the RestApi that you want to clone from.
        :param description: The description of the RestApi.
        :param disable_execute_api_endpoint: Specifies whether clients can invoke your API by using the default ``execute-api`` endpoint. By default, clients can invoke your API with the default ``https://{api_id}.execute-api.{region}.amazonaws.com`` endpoint. To require that clients use a custom domain name to invoke your API, disable the default endpoint
        :param endpoint_access_mode: The endpoint access mode for your RestApi.
        :param endpoint_configuration: A list of the endpoint types and IP address types of the API. Use this property when creating an API. When importing an existing API, specify the endpoint configuration types using the ``Parameters`` property.
        :param fail_on_warnings: A query parameter to indicate whether to rollback the API update ( ``true`` ) or not ( ``false`` ) when a warning is encountered. The default value is ``false`` .
        :param minimum_compression_size: A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (with a null value) on an API. When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size.
        :param mode: This property applies only when you use OpenAPI to define your REST API. The ``Mode`` determines how API Gateway handles resource updates. Valid values are ``overwrite`` or ``merge`` . For ``overwrite`` , the new API definition replaces the existing one. The existing API identifier remains unchanged. For ``merge`` , the new API definition is merged with the existing API. If you don't specify this property, a default value is chosen. For REST APIs created before March 29, 2021, the default is ``overwrite`` . For REST APIs created after March 29, 2021, the new API definition takes precedence, but any container types such as endpoint configurations and binary media types are merged with the existing API. Use the default mode to define top-level ``RestApi`` properties in addition to using OpenAPI. Generally, it's preferred to use API Gateway's OpenAPI extensions to model these properties.
        :param name: The name of the RestApi. A name is required if the REST API is not based on an OpenAPI specification.
        :param parameters: Custom header parameters as part of the request. For example, to exclude DocumentationParts from an imported API, set ``ignore=documentation`` as a ``parameters`` value, as in the AWS CLI command of ``aws apigateway import-rest-api --parameters ignore=documentation --body 'file:///path/to/imported-api-body.json'`` .
        :param policy: A policy document that contains the permissions for the ``RestApi`` resource. To set the ARN for the policy, use the ``!Join`` intrinsic function with ``""`` as delimiter and values of ``"execute-api:/"`` and ``"*"`` .
        :param security_policy: The Transport Layer Security (TLS) version + cipher suite for this RestApi.
        :param tags: The key-value map of strings. The valid character set is [a-zA-Z+-=._:/]. The tag key can be up to 128 characters and must not start with ``aws:`` . The tag value can be up to 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            # body: Any
            # policy: Any
            
            cfn_rest_api_mixin_props = apigateway_mixins.CfnRestApiMixinProps(
                api_key_source_type="apiKeySourceType",
                binary_media_types=["binaryMediaTypes"],
                body=body,
                body_s3_location=apigateway_mixins.CfnRestApiPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    e_tag="eTag",
                    key="key",
                    version="version"
                ),
                clone_from="cloneFrom",
                description="description",
                disable_execute_api_endpoint=False,
                endpoint_access_mode="endpointAccessMode",
                endpoint_configuration=apigateway_mixins.CfnRestApiPropsMixin.EndpointConfigurationProperty(
                    ip_address_type="ipAddressType",
                    types=["types"],
                    vpc_endpoint_ids=["vpcEndpointIds"]
                ),
                fail_on_warnings=False,
                minimum_compression_size=123,
                mode="mode",
                name="name",
                parameters={
                    "parameters_key": "parameters"
                },
                policy=policy,
                security_policy="securityPolicy",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8a816e2ec061957e5dbd71db985e8ebbce0748cade85ce82084c32eceb8f70)
            check_type(argname="argument api_key_source_type", value=api_key_source_type, expected_type=type_hints["api_key_source_type"])
            check_type(argname="argument binary_media_types", value=binary_media_types, expected_type=type_hints["binary_media_types"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument body_s3_location", value=body_s3_location, expected_type=type_hints["body_s3_location"])
            check_type(argname="argument clone_from", value=clone_from, expected_type=type_hints["clone_from"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_execute_api_endpoint", value=disable_execute_api_endpoint, expected_type=type_hints["disable_execute_api_endpoint"])
            check_type(argname="argument endpoint_access_mode", value=endpoint_access_mode, expected_type=type_hints["endpoint_access_mode"])
            check_type(argname="argument endpoint_configuration", value=endpoint_configuration, expected_type=type_hints["endpoint_configuration"])
            check_type(argname="argument fail_on_warnings", value=fail_on_warnings, expected_type=type_hints["fail_on_warnings"])
            check_type(argname="argument minimum_compression_size", value=minimum_compression_size, expected_type=type_hints["minimum_compression_size"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument security_policy", value=security_policy, expected_type=type_hints["security_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_key_source_type is not None:
            self._values["api_key_source_type"] = api_key_source_type
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if body is not None:
            self._values["body"] = body
        if body_s3_location is not None:
            self._values["body_s3_location"] = body_s3_location
        if clone_from is not None:
            self._values["clone_from"] = clone_from
        if description is not None:
            self._values["description"] = description
        if disable_execute_api_endpoint is not None:
            self._values["disable_execute_api_endpoint"] = disable_execute_api_endpoint
        if endpoint_access_mode is not None:
            self._values["endpoint_access_mode"] = endpoint_access_mode
        if endpoint_configuration is not None:
            self._values["endpoint_configuration"] = endpoint_configuration
        if fail_on_warnings is not None:
            self._values["fail_on_warnings"] = fail_on_warnings
        if minimum_compression_size is not None:
            self._values["minimum_compression_size"] = minimum_compression_size
        if mode is not None:
            self._values["mode"] = mode
        if name is not None:
            self._values["name"] = name
        if parameters is not None:
            self._values["parameters"] = parameters
        if policy is not None:
            self._values["policy"] = policy
        if security_policy is not None:
            self._values["security_policy"] = security_policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def api_key_source_type(self) -> typing.Optional[builtins.str]:
        '''The source of the API key for metering requests according to a usage plan.

        Valid values are: ``HEADER`` to read the API key from the ``X-API-Key`` header of a request. ``AUTHORIZER`` to read the API key from the ``UsageIdentifierKey`` from a custom authorizer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-apikeysourcetype
        '''
        result = self._values.get("api_key_source_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of binary media types supported by the RestApi.

        By default, the RestApi supports only UTF-8-encoded text payloads.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-binarymediatypes
        '''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def body(self) -> typing.Any:
        '''An OpenAPI specification that defines a set of RESTful APIs in JSON format.

        For YAML templates, you can also provide the specification in YAML format.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-body
        '''
        result = self._values.get("body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def body_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestApiPropsMixin.S3LocationProperty"]]:
        '''The Amazon Simple Storage Service (Amazon S3) location that points to an OpenAPI file, which defines a set of RESTful APIs in JSON or YAML format.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-bodys3location
        '''
        result = self._values.get("body_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestApiPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def clone_from(self) -> typing.Optional[builtins.str]:
        '''The ID of the RestApi that you want to clone from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-clonefrom
        '''
        result = self._values.get("clone_from")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_execute_api_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether clients can invoke your API by using the default ``execute-api`` endpoint.

        By default, clients can invoke your API with the default ``https://{api_id}.execute-api.{region}.amazonaws.com`` endpoint. To require that clients use a custom domain name to invoke your API, disable the default endpoint

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-disableexecuteapiendpoint
        '''
        result = self._values.get("disable_execute_api_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def endpoint_access_mode(self) -> typing.Optional[builtins.str]:
        '''The endpoint access mode for your RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-endpointaccessmode
        '''
        result = self._values.get("endpoint_access_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestApiPropsMixin.EndpointConfigurationProperty"]]:
        '''A list of the endpoint types and IP address types of the API.

        Use this property when creating an API. When importing an existing API, specify the endpoint configuration types using the ``Parameters`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-endpointconfiguration
        '''
        result = self._values.get("endpoint_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRestApiPropsMixin.EndpointConfigurationProperty"]], result)

    @builtins.property
    def fail_on_warnings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A query parameter to indicate whether to rollback the API update ( ``true`` ) or not ( ``false`` ) when a warning is encountered.

        The default value is ``false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-failonwarnings
        '''
        result = self._values.get("fail_on_warnings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''A nullable integer that is used to enable compression (with non-negative between 0 and 10485760 (10M) bytes, inclusive) or disable compression (with a null value) on an API.

        When compression is enabled, compression or decompression is not applied on the payload if the payload size is smaller than this value. Setting it to zero allows compression for any payload size.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-minimumcompressionsize
        '''
        result = self._values.get("minimum_compression_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''This property applies only when you use OpenAPI to define your REST API.

        The ``Mode`` determines how API Gateway handles resource updates.

        Valid values are ``overwrite`` or ``merge`` .

        For ``overwrite`` , the new API definition replaces the existing one. The existing API identifier remains unchanged.

        For ``merge`` , the new API definition is merged with the existing API.

        If you don't specify this property, a default value is chosen. For REST APIs created before March 29, 2021, the default is ``overwrite`` . For REST APIs created after March 29, 2021, the new API definition takes precedence, but any container types such as endpoint configurations and binary media types are merged with the existing API.

        Use the default mode to define top-level ``RestApi`` properties in addition to using OpenAPI. Generally, it's preferred to use API Gateway's OpenAPI extensions to model these properties.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-mode
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the RestApi.

        A name is required if the REST API is not based on an OpenAPI specification.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''Custom header parameters as part of the request.

        For example, to exclude DocumentationParts from an imported API, set ``ignore=documentation`` as a ``parameters`` value, as in the AWS CLI command of ``aws apigateway import-rest-api --parameters ignore=documentation --body 'file:///path/to/imported-api-body.json'`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''A policy document that contains the permissions for the ``RestApi`` resource.

        To set the ARN for the policy, use the ``!Join`` intrinsic function with ``""`` as delimiter and values of ``"execute-api:/"`` and ``"*"`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def security_policy(self) -> typing.Optional[builtins.str]:
        '''The Transport Layer Security (TLS) version + cipher suite for this RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-securitypolicy
        '''
        result = self._values.get("security_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The key-value map of strings.

        The valid character set is [a-zA-Z+-=._:/]. The tag key can be up to 128 characters and must not start with ``aws:`` . The tag value can be up to 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html#cfn-apigateway-restapi-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRestApiMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRestApiPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnRestApiPropsMixin",
):
    '''The ``AWS::ApiGateway::RestApi`` resource creates a REST API.

    For more information, see `restapi:create <https://docs.aws.amazon.com/apigateway/latest/api/API_CreateRestApi.html>`_ in the *Amazon API Gateway REST API Reference* .
    .. epigraph::

       On January 1, 2016, the Swagger Specification was donated to the `OpenAPI initiative <https://docs.aws.amazon.com/https://www.openapis.org/>`_ , becoming the foundation of the OpenAPI Specification.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html
    :cloudformationResource: AWS::ApiGateway::RestApi
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        # body: Any
        # policy: Any
        
        cfn_rest_api_props_mixin = apigateway_mixins.CfnRestApiPropsMixin(apigateway_mixins.CfnRestApiMixinProps(
            api_key_source_type="apiKeySourceType",
            binary_media_types=["binaryMediaTypes"],
            body=body,
            body_s3_location=apigateway_mixins.CfnRestApiPropsMixin.S3LocationProperty(
                bucket="bucket",
                e_tag="eTag",
                key="key",
                version="version"
            ),
            clone_from="cloneFrom",
            description="description",
            disable_execute_api_endpoint=False,
            endpoint_access_mode="endpointAccessMode",
            endpoint_configuration=apigateway_mixins.CfnRestApiPropsMixin.EndpointConfigurationProperty(
                ip_address_type="ipAddressType",
                types=["types"],
                vpc_endpoint_ids=["vpcEndpointIds"]
            ),
            fail_on_warnings=False,
            minimum_compression_size=123,
            mode="mode",
            name="name",
            parameters={
                "parameters_key": "parameters"
            },
            policy=policy,
            security_policy="securityPolicy",
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
        props: typing.Union[CfnRestApiMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::RestApi``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bea9ffd65f10bb5e5d464cc0ef3c9a6615cb1b87fe76a482190387213185de8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__891d31aed5db6fb33d8a7779fdc6ecbd57a623944a42ecdded94e46ff354e697)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f8498864ed92185801af8181654f388103ef8db954f9e5b2cd993e32fb50e7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRestApiMixinProps:
        return typing.cast(CfnRestApiMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnRestApiPropsMixin.EndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ip_address_type": "ipAddressType",
            "types": "types",
            "vpc_endpoint_ids": "vpcEndpointIds",
        },
    )
    class EndpointConfigurationProperty:
        def __init__(
            self,
            *,
            ip_address_type: typing.Optional[builtins.str] = None,
            types: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``EndpointConfiguration`` property type specifies the endpoint types and IP address types of a REST API.

            ``EndpointConfiguration`` is a property of the `AWS::ApiGateway::RestApi <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html>`_ resource.

            :param ip_address_type: The IP address types that can invoke an API (RestApi). Use ``ipv4`` to allow only IPv4 addresses to invoke an API, or use ``dualstack`` to allow both IPv4 and IPv6 addresses to invoke an API. For the ``PRIVATE`` endpoint type, only ``dualstack`` is supported.
            :param types: A list of endpoint types of an API (RestApi) or its custom domain name (DomainName). For an edge-optimized API and its custom domain name, the endpoint type is ``"EDGE"`` . For a regional API and its custom domain name, the endpoint type is ``REGIONAL`` . For a private API, the endpoint type is ``PRIVATE`` .
            :param vpc_endpoint_ids: A list of VpcEndpointIds of an API (RestApi) against which to create Route53 ALIASes. It is only supported for ``PRIVATE`` endpoint type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-endpointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                endpoint_configuration_property = apigateway_mixins.CfnRestApiPropsMixin.EndpointConfigurationProperty(
                    ip_address_type="ipAddressType",
                    types=["types"],
                    vpc_endpoint_ids=["vpcEndpointIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd5efd4b22800c3e4c628f3fd78cb97ee43dca98db8889439f8ab84de9f6c0f7)
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
                check_type(argname="argument types", value=types, expected_type=type_hints["types"])
                check_type(argname="argument vpc_endpoint_ids", value=vpc_endpoint_ids, expected_type=type_hints["vpc_endpoint_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type
            if types is not None:
                self._values["types"] = types
            if vpc_endpoint_ids is not None:
                self._values["vpc_endpoint_ids"] = vpc_endpoint_ids

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''The IP address types that can invoke an API (RestApi).

            Use ``ipv4`` to allow only IPv4 addresses to invoke an API, or use ``dualstack`` to allow both IPv4 and IPv6 addresses to invoke an API. For the ``PRIVATE`` endpoint type, only ``dualstack`` is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-endpointconfiguration.html#cfn-apigateway-restapi-endpointconfiguration-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of endpoint types of an API (RestApi) or its custom domain name (DomainName).

            For an edge-optimized API and its custom domain name, the endpoint type is ``"EDGE"`` . For a regional API and its custom domain name, the endpoint type is ``REGIONAL`` . For a private API, the endpoint type is ``PRIVATE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-endpointconfiguration.html#cfn-apigateway-restapi-endpointconfiguration-types
            '''
            result = self._values.get("types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_endpoint_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of VpcEndpointIds of an API (RestApi) against which to create Route53 ALIASes.

            It is only supported for ``PRIVATE`` endpoint type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-endpointconfiguration.html#cfn-apigateway-restapi-endpointconfiguration-vpcendpointids
            '''
            result = self._values.get("vpc_endpoint_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnRestApiPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "e_tag": "eTag",
            "key": "key",
            "version": "version",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            e_tag: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``S3Location`` is a property of the `AWS::ApiGateway::RestApi <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html>`_ resource that specifies the Amazon S3 location of a OpenAPI (formerly Swagger) file that defines a set of RESTful APIs in JSON or YAML.

            .. epigraph::

               On January 1, 2016, the Swagger Specification was donated to the `OpenAPI initiative <https://docs.aws.amazon.com/https://www.openapis.org/>`_ , becoming the foundation of the OpenAPI Specification.

            :param bucket: The name of the S3 bucket where the OpenAPI file is stored.
            :param e_tag: The Amazon S3 ETag (a file checksum) of the OpenAPI file. If you don't specify a value, API Gateway skips ETag validation of your OpenAPI file.
            :param key: The file name of the OpenAPI file (Amazon S3 object name).
            :param version: For versioning-enabled buckets, a specific version of the OpenAPI file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                s3_location_property = apigateway_mixins.CfnRestApiPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    e_tag="eTag",
                    key="key",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27b052841bf93abaaa6255df441da7c9bcab374027fdf02402199e6f5dc0e90f)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument e_tag", value=e_tag, expected_type=type_hints["e_tag"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if e_tag is not None:
                self._values["e_tag"] = e_tag
            if key is not None:
                self._values["key"] = key
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket where the OpenAPI file is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html#cfn-apigateway-restapi-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def e_tag(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 ETag (a file checksum) of the OpenAPI file.

            If you don't specify a value, API Gateway skips ETag validation of your OpenAPI file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html#cfn-apigateway-restapi-s3location-etag
            '''
            result = self._values.get("e_tag")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The file name of the OpenAPI file (Amazon S3 object name).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html#cfn-apigateway-restapi-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''For versioning-enabled buckets, a specific version of the OpenAPI file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-restapi-s3location.html#cfn-apigateway-restapi-s3location-version
            '''
            result = self._values.get("version")
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
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnStageMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_log_setting": "accessLogSetting",
        "cache_cluster_enabled": "cacheClusterEnabled",
        "cache_cluster_size": "cacheClusterSize",
        "canary_setting": "canarySetting",
        "client_certificate_id": "clientCertificateId",
        "deployment_id": "deploymentId",
        "description": "description",
        "documentation_version": "documentationVersion",
        "method_settings": "methodSettings",
        "rest_api_id": "restApiId",
        "stage_name": "stageName",
        "tags": "tags",
        "tracing_enabled": "tracingEnabled",
        "variables": "variables",
    },
)
class CfnStageMixinProps:
    def __init__(
        self,
        *,
        access_log_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStagePropsMixin.AccessLogSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cache_cluster_size: typing.Optional[builtins.str] = None,
        canary_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStagePropsMixin.CanarySettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        client_certificate_id: typing.Optional[builtins.str] = None,
        deployment_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        documentation_version: typing.Optional[builtins.str] = None,
        method_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStagePropsMixin.MethodSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        rest_api_id: typing.Optional[builtins.str] = None,
        stage_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnStagePropsMixin.

        :param access_log_setting: Access log settings, including the access log format and access log destination ARN.
        :param cache_cluster_enabled: Specifies whether a cache cluster is enabled for the stage. To activate a method-level cache, set ``CachingEnabled`` to ``true`` for a method.
        :param cache_cluster_size: The stage's cache capacity in GB. For more information about choosing a cache size, see `Enabling API caching to enhance responsiveness <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html>`_ .
        :param canary_setting: Settings for the canary deployment in this stage.
        :param client_certificate_id: The identifier of a client certificate for an API stage.
        :param deployment_id: The identifier of the Deployment that the stage points to.
        :param description: The stage's description.
        :param documentation_version: The version of the associated API documentation.
        :param method_settings: A map that defines the method settings for a Stage resource. Keys (designated as ``/{method_setting_key`` below) are method paths defined as ``{resource_path}/{http_method}`` for an individual method override, or ``/\\* /\\*`` for overriding all methods in the stage.
        :param rest_api_id: The string identifier of the associated RestApi.
        :param stage_name: The name of the stage is the first path segment in the Uniform Resource Identifier (URI) of a call to API Gateway. Stage names can only contain alphanumeric characters, hyphens, and underscores. Maximum length is 128 characters.
        :param tags: The collection of tags. Each tag element is associated with a given resource.
        :param tracing_enabled: Specifies whether active tracing with X-ray is enabled for the Stage.
        :param variables: A map (string-to-string map) that defines the stage variables, where the variable name is the key and the variable value is the value. Variable names are limited to alphanumeric characters. Values must match the following regular expression: ``[A-Za-z0-9-._~:/?#&=,]+`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_stage_mixin_props = apigateway_mixins.CfnStageMixinProps(
                access_log_setting=apigateway_mixins.CfnStagePropsMixin.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                ),
                cache_cluster_enabled=False,
                cache_cluster_size="cacheClusterSize",
                canary_setting=apigateway_mixins.CfnStagePropsMixin.CanarySettingProperty(
                    deployment_id="deploymentId",
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                ),
                client_certificate_id="clientCertificateId",
                deployment_id="deploymentId",
                description="description",
                documentation_version="documentationVersion",
                method_settings=[apigateway_mixins.CfnStagePropsMixin.MethodSettingProperty(
                    cache_data_encrypted=False,
                    cache_ttl_in_seconds=123,
                    caching_enabled=False,
                    data_trace_enabled=False,
                    http_method="httpMethod",
                    logging_level="loggingLevel",
                    metrics_enabled=False,
                    resource_path="resourcePath",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )],
                rest_api_id="restApiId",
                stage_name="stageName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tracing_enabled=False,
                variables={
                    "variables_key": "variables"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a1cd67fe1c2e89478e7bd4012125c7cfe9c59c68ad78bef4655ac433a701bc)
            check_type(argname="argument access_log_setting", value=access_log_setting, expected_type=type_hints["access_log_setting"])
            check_type(argname="argument cache_cluster_enabled", value=cache_cluster_enabled, expected_type=type_hints["cache_cluster_enabled"])
            check_type(argname="argument cache_cluster_size", value=cache_cluster_size, expected_type=type_hints["cache_cluster_size"])
            check_type(argname="argument canary_setting", value=canary_setting, expected_type=type_hints["canary_setting"])
            check_type(argname="argument client_certificate_id", value=client_certificate_id, expected_type=type_hints["client_certificate_id"])
            check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation_version", value=documentation_version, expected_type=type_hints["documentation_version"])
            check_type(argname="argument method_settings", value=method_settings, expected_type=type_hints["method_settings"])
            check_type(argname="argument rest_api_id", value=rest_api_id, expected_type=type_hints["rest_api_id"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracing_enabled", value=tracing_enabled, expected_type=type_hints["tracing_enabled"])
            check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_log_setting is not None:
            self._values["access_log_setting"] = access_log_setting
        if cache_cluster_enabled is not None:
            self._values["cache_cluster_enabled"] = cache_cluster_enabled
        if cache_cluster_size is not None:
            self._values["cache_cluster_size"] = cache_cluster_size
        if canary_setting is not None:
            self._values["canary_setting"] = canary_setting
        if client_certificate_id is not None:
            self._values["client_certificate_id"] = client_certificate_id
        if deployment_id is not None:
            self._values["deployment_id"] = deployment_id
        if description is not None:
            self._values["description"] = description
        if documentation_version is not None:
            self._values["documentation_version"] = documentation_version
        if method_settings is not None:
            self._values["method_settings"] = method_settings
        if rest_api_id is not None:
            self._values["rest_api_id"] = rest_api_id
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if tags is not None:
            self._values["tags"] = tags
        if tracing_enabled is not None:
            self._values["tracing_enabled"] = tracing_enabled
        if variables is not None:
            self._values["variables"] = variables

    @builtins.property
    def access_log_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.AccessLogSettingProperty"]]:
        '''Access log settings, including the access log format and access log destination ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-accesslogsetting
        '''
        result = self._values.get("access_log_setting")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.AccessLogSettingProperty"]], result)

    @builtins.property
    def cache_cluster_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether a cache cluster is enabled for the stage.

        To activate a method-level cache, set ``CachingEnabled`` to ``true`` for a method.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-cacheclusterenabled
        '''
        result = self._values.get("cache_cluster_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cache_cluster_size(self) -> typing.Optional[builtins.str]:
        '''The stage's cache capacity in GB.

        For more information about choosing a cache size, see `Enabling API caching to enhance responsiveness <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-cacheclustersize
        '''
        result = self._values.get("cache_cluster_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def canary_setting(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.CanarySettingProperty"]]:
        '''Settings for the canary deployment in this stage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-canarysetting
        '''
        result = self._values.get("canary_setting")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.CanarySettingProperty"]], result)

    @builtins.property
    def client_certificate_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a client certificate for an API stage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-clientcertificateid
        '''
        result = self._values.get("client_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Deployment that the stage points to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-deploymentid
        '''
        result = self._values.get("deployment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The stage's description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation_version(self) -> typing.Optional[builtins.str]:
        '''The version of the associated API documentation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-documentationversion
        '''
        result = self._values.get("documentation_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def method_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.MethodSettingProperty"]]]]:
        '''A map that defines the method settings for a Stage resource.

        Keys (designated as ``/{method_setting_key`` below) are method paths defined as ``{resource_path}/{http_method}`` for an individual method override, or ``/\\* /\\*`` for overriding all methods in the stage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-methodsettings
        '''
        result = self._values.get("method_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStagePropsMixin.MethodSettingProperty"]]]], result)

    @builtins.property
    def rest_api_id(self) -> typing.Optional[builtins.str]:
        '''The string identifier of the associated RestApi.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-restapiid
        '''
        result = self._values.get("rest_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''The name of the stage is the first path segment in the Uniform Resource Identifier (URI) of a call to API Gateway.

        Stage names can only contain alphanumeric characters, hyphens, and underscores. Maximum length is 128 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-stagename
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tracing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether active tracing with X-ray is enabled for the Stage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-tracingenabled
        '''
        result = self._values.get("tracing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def variables(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''A map (string-to-string map) that defines the stage variables, where the variable name is the key and the variable value is the value.

        Variable names are limited to alphanumeric characters. Values must match the following regular expression: ``[A-Za-z0-9-._~:/?#&=,]+`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html#cfn-apigateway-stage-variables
        '''
        result = self._values.get("variables")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStageMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStagePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnStagePropsMixin",
):
    '''The ``AWS::ApiGateway::Stage`` resource creates a stage for a deployment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html
    :cloudformationResource: AWS::ApiGateway::Stage
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_stage_props_mixin = apigateway_mixins.CfnStagePropsMixin(apigateway_mixins.CfnStageMixinProps(
            access_log_setting=apigateway_mixins.CfnStagePropsMixin.AccessLogSettingProperty(
                destination_arn="destinationArn",
                format="format"
            ),
            cache_cluster_enabled=False,
            cache_cluster_size="cacheClusterSize",
            canary_setting=apigateway_mixins.CfnStagePropsMixin.CanarySettingProperty(
                deployment_id="deploymentId",
                percent_traffic=123,
                stage_variable_overrides={
                    "stage_variable_overrides_key": "stageVariableOverrides"
                },
                use_stage_cache=False
            ),
            client_certificate_id="clientCertificateId",
            deployment_id="deploymentId",
            description="description",
            documentation_version="documentationVersion",
            method_settings=[apigateway_mixins.CfnStagePropsMixin.MethodSettingProperty(
                cache_data_encrypted=False,
                cache_ttl_in_seconds=123,
                caching_enabled=False,
                data_trace_enabled=False,
                http_method="httpMethod",
                logging_level="loggingLevel",
                metrics_enabled=False,
                resource_path="resourcePath",
                throttling_burst_limit=123,
                throttling_rate_limit=123
            )],
            rest_api_id="restApiId",
            stage_name="stageName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tracing_enabled=False,
            variables={
                "variables_key": "variables"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStageMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::Stage``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322d5ab2f1e0f903b548f60aa6fa7470bbf188c79c7309003c9a2e0ff0b7c94b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1306a221b4170bf3674c5b3455a17be3bf8688cdace208e574fbe4fb7d5513fd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9960ed1ce38cb796160c2628bd38e4caa880ff27c5385f35bb9a849e38a20e66)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStageMixinProps:
        return typing.cast(CfnStageMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnStagePropsMixin.AccessLogSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn", "format": "format"},
    )
    class AccessLogSettingProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AccessLogSetting`` property type specifies settings for logging access in this stage.

            ``AccessLogSetting`` is a property of the `AWS::ApiGateway::Stage <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-stage.html>`_ resource.

            :param destination_arn: The Amazon Resource Name (ARN) of the CloudWatch Logs log group or Kinesis Data Firehose delivery stream to receive access logs. If you specify a Kinesis Data Firehose delivery stream, the stream name must begin with ``amazon-apigateway-`` . This parameter is required to enable access logging.
            :param format: A single line format of the access logs of data, as specified by selected `$context variables <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html#context-variable-reference>`_ . The format must include at least ``$context.requestId`` . This parameter is required to enable access logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                access_log_setting_property = apigateway_mixins.CfnStagePropsMixin.AccessLogSettingProperty(
                    destination_arn="destinationArn",
                    format="format"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__639106ac8b14a88156048b746f2b53f96ab33659aad4a97b36ff72724215d0e4)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if format is not None:
                self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the CloudWatch Logs log group or Kinesis Data Firehose delivery stream to receive access logs.

            If you specify a Kinesis Data Firehose delivery stream, the stream name must begin with ``amazon-apigateway-`` . This parameter is required to enable access logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''A single line format of the access logs of data, as specified by selected `$context variables <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html#context-variable-reference>`_ . The format must include at least ``$context.requestId`` . This parameter is required to enable access logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-accesslogsetting.html#cfn-apigateway-stage-accesslogsetting-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessLogSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnStagePropsMixin.CanarySettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_id": "deploymentId",
            "percent_traffic": "percentTraffic",
            "stage_variable_overrides": "stageVariableOverrides",
            "use_stage_cache": "useStageCache",
        },
    )
    class CanarySettingProperty:
        def __init__(
            self,
            *,
            deployment_id: typing.Optional[builtins.str] = None,
            percent_traffic: typing.Optional[jsii.Number] = None,
            stage_variable_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Configuration settings of a canary deployment.

            :param deployment_id: The ID of the canary deployment.
            :param percent_traffic: The percent (0-100) of traffic diverted to a canary deployment.
            :param stage_variable_overrides: Stage variables overridden for a canary release deployment, including new stage variables introduced in the canary. These stage variables are represented as a string-to-string map between stage variable names and their values.
            :param use_stage_cache: A Boolean flag to indicate whether the canary deployment uses the stage cache or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                canary_setting_property = apigateway_mixins.CfnStagePropsMixin.CanarySettingProperty(
                    deployment_id="deploymentId",
                    percent_traffic=123,
                    stage_variable_overrides={
                        "stage_variable_overrides_key": "stageVariableOverrides"
                    },
                    use_stage_cache=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__20dec0919adf6f5553320e8efb923e8d9209a13becfe88d1e176a0896848aa5c)
                check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
                check_type(argname="argument percent_traffic", value=percent_traffic, expected_type=type_hints["percent_traffic"])
                check_type(argname="argument stage_variable_overrides", value=stage_variable_overrides, expected_type=type_hints["stage_variable_overrides"])
                check_type(argname="argument use_stage_cache", value=use_stage_cache, expected_type=type_hints["use_stage_cache"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_id is not None:
                self._values["deployment_id"] = deployment_id
            if percent_traffic is not None:
                self._values["percent_traffic"] = percent_traffic
            if stage_variable_overrides is not None:
                self._values["stage_variable_overrides"] = stage_variable_overrides
            if use_stage_cache is not None:
                self._values["use_stage_cache"] = use_stage_cache

        @builtins.property
        def deployment_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the canary deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-deploymentid
            '''
            result = self._values.get("deployment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def percent_traffic(self) -> typing.Optional[jsii.Number]:
            '''The percent (0-100) of traffic diverted to a canary deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-percenttraffic
            '''
            result = self._values.get("percent_traffic")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stage_variable_overrides(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Stage variables overridden for a canary release deployment, including new stage variables introduced in the canary.

            These stage variables are represented as a string-to-string map between stage variable names and their values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-stagevariableoverrides
            '''
            result = self._values.get("stage_variable_overrides")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_stage_cache(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean flag to indicate whether the canary deployment uses the stage cache or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-canarysetting.html#cfn-apigateway-stage-canarysetting-usestagecache
            '''
            result = self._values.get("use_stage_cache")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CanarySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnStagePropsMixin.MethodSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cache_data_encrypted": "cacheDataEncrypted",
            "cache_ttl_in_seconds": "cacheTtlInSeconds",
            "caching_enabled": "cachingEnabled",
            "data_trace_enabled": "dataTraceEnabled",
            "http_method": "httpMethod",
            "logging_level": "loggingLevel",
            "metrics_enabled": "metricsEnabled",
            "resource_path": "resourcePath",
            "throttling_burst_limit": "throttlingBurstLimit",
            "throttling_rate_limit": "throttlingRateLimit",
        },
    )
    class MethodSettingProperty:
        def __init__(
            self,
            *,
            cache_data_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            cache_ttl_in_seconds: typing.Optional[jsii.Number] = None,
            caching_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            http_method: typing.Optional[builtins.str] = None,
            logging_level: typing.Optional[builtins.str] = None,
            metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            resource_path: typing.Optional[builtins.str] = None,
            throttling_burst_limit: typing.Optional[jsii.Number] = None,
            throttling_rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``MethodSetting`` property type configures settings for all methods in a stage.

            The ``MethodSettings`` property of the ``AWS::ApiGateway::Stage`` resource contains a list of ``MethodSetting`` property types.

            :param cache_data_encrypted: Specifies whether the cached responses are encrypted.
            :param cache_ttl_in_seconds: Specifies the time to live (TTL), in seconds, for cached responses. The higher the TTL, the longer the response will be cached.
            :param caching_enabled: Specifies whether responses should be cached and returned for requests. A cache cluster must be enabled on the stage for responses to be cached.
            :param data_trace_enabled: Specifies whether data trace logging is enabled for this method, which affects the log entries pushed to Amazon CloudWatch Logs. This can be useful to troubleshoot APIs, but can result in logging sensitive data. We recommend that you don't enable this option for production APIs.
            :param http_method: The HTTP method. To apply settings to multiple resources and methods, specify an asterisk ( ``*`` ) for the ``HttpMethod`` and ``/*`` for the ``ResourcePath`` . This parameter is required when you specify a ``MethodSetting`` .
            :param logging_level: Specifies the logging level for this method, which affects the log entries pushed to Amazon CloudWatch Logs. Valid values are ``OFF`` , ``ERROR`` , and ``INFO`` . Choose ``ERROR`` to write only error-level entries to CloudWatch Logs, or choose ``INFO`` to include all ``ERROR`` events as well as extra informational events.
            :param metrics_enabled: Specifies whether Amazon CloudWatch metrics are enabled for this method.
            :param resource_path: The resource path for this method. Forward slashes ( ``/`` ) are encoded as ``~1`` and the initial slash must include a forward slash. For example, the path value ``/resource/subresource`` must be encoded as ``/~1resource~1subresource`` . To specify the root path, use only a slash ( ``/`` ). To apply settings to multiple resources and methods, specify an asterisk ( ``*`` ) for the ``HttpMethod`` and ``/*`` for the ``ResourcePath`` . This parameter is required when you specify a ``MethodSetting`` .
            :param throttling_burst_limit: Specifies the throttling burst limit.
            :param throttling_rate_limit: Specifies the throttling rate limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                method_setting_property = apigateway_mixins.CfnStagePropsMixin.MethodSettingProperty(
                    cache_data_encrypted=False,
                    cache_ttl_in_seconds=123,
                    caching_enabled=False,
                    data_trace_enabled=False,
                    http_method="httpMethod",
                    logging_level="loggingLevel",
                    metrics_enabled=False,
                    resource_path="resourcePath",
                    throttling_burst_limit=123,
                    throttling_rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3538fdeefb625465256cfe520c8895344951533806f12c21c168a0c275c23c53)
                check_type(argname="argument cache_data_encrypted", value=cache_data_encrypted, expected_type=type_hints["cache_data_encrypted"])
                check_type(argname="argument cache_ttl_in_seconds", value=cache_ttl_in_seconds, expected_type=type_hints["cache_ttl_in_seconds"])
                check_type(argname="argument caching_enabled", value=caching_enabled, expected_type=type_hints["caching_enabled"])
                check_type(argname="argument data_trace_enabled", value=data_trace_enabled, expected_type=type_hints["data_trace_enabled"])
                check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
                check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
                check_type(argname="argument metrics_enabled", value=metrics_enabled, expected_type=type_hints["metrics_enabled"])
                check_type(argname="argument resource_path", value=resource_path, expected_type=type_hints["resource_path"])
                check_type(argname="argument throttling_burst_limit", value=throttling_burst_limit, expected_type=type_hints["throttling_burst_limit"])
                check_type(argname="argument throttling_rate_limit", value=throttling_rate_limit, expected_type=type_hints["throttling_rate_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cache_data_encrypted is not None:
                self._values["cache_data_encrypted"] = cache_data_encrypted
            if cache_ttl_in_seconds is not None:
                self._values["cache_ttl_in_seconds"] = cache_ttl_in_seconds
            if caching_enabled is not None:
                self._values["caching_enabled"] = caching_enabled
            if data_trace_enabled is not None:
                self._values["data_trace_enabled"] = data_trace_enabled
            if http_method is not None:
                self._values["http_method"] = http_method
            if logging_level is not None:
                self._values["logging_level"] = logging_level
            if metrics_enabled is not None:
                self._values["metrics_enabled"] = metrics_enabled
            if resource_path is not None:
                self._values["resource_path"] = resource_path
            if throttling_burst_limit is not None:
                self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None:
                self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def cache_data_encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the cached responses are encrypted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-cachedataencrypted
            '''
            result = self._values.get("cache_data_encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def cache_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Specifies the time to live (TTL), in seconds, for cached responses.

            The higher the TTL, the longer the response will be cached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-cachettlinseconds
            '''
            result = self._values.get("cache_ttl_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def caching_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether responses should be cached and returned for requests.

            A cache cluster must be enabled on the stage for responses to be cached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-cachingenabled
            '''
            result = self._values.get("caching_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def data_trace_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether data trace logging is enabled for this method, which affects the log entries pushed to Amazon CloudWatch Logs.

            This can be useful to troubleshoot APIs, but can result in logging sensitive data. We recommend that you don't enable this option for production APIs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-datatraceenabled
            '''
            result = self._values.get("data_trace_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def http_method(self) -> typing.Optional[builtins.str]:
            '''The HTTP method.

            To apply settings to multiple resources and methods, specify an asterisk ( ``*`` ) for the ``HttpMethod`` and ``/*`` for the ``ResourcePath`` . This parameter is required when you specify a ``MethodSetting`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-httpmethod
            '''
            result = self._values.get("http_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logging_level(self) -> typing.Optional[builtins.str]:
            '''Specifies the logging level for this method, which affects the log entries pushed to Amazon CloudWatch Logs.

            Valid values are ``OFF`` , ``ERROR`` , and ``INFO`` . Choose ``ERROR`` to write only error-level entries to CloudWatch Logs, or choose ``INFO`` to include all ``ERROR`` events as well as extra informational events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-logginglevel
            '''
            result = self._values.get("logging_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon CloudWatch metrics are enabled for this method.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-metricsenabled
            '''
            result = self._values.get("metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def resource_path(self) -> typing.Optional[builtins.str]:
            '''The resource path for this method.

            Forward slashes ( ``/`` ) are encoded as ``~1`` and the initial slash must include a forward slash. For example, the path value ``/resource/subresource`` must be encoded as ``/~1resource~1subresource`` . To specify the root path, use only a slash ( ``/`` ). To apply settings to multiple resources and methods, specify an asterisk ( ``*`` ) for the ``HttpMethod`` and ``/*`` for the ``ResourcePath`` . This parameter is required when you specify a ``MethodSetting`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-resourcepath
            '''
            result = self._values.get("resource_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throttling burst limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-throttlingburstlimit
            '''
            result = self._values.get("throttling_burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throttling rate limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-stage-methodsetting.html#cfn-apigateway-stage-methodsetting-throttlingratelimit
            '''
            result = self._values.get("throttling_rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MethodSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnUsagePlanKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_id": "keyId",
        "key_type": "keyType",
        "usage_plan_id": "usagePlanId",
    },
)
class CfnUsagePlanKeyMixinProps:
    def __init__(
        self,
        *,
        key_id: typing.Optional[builtins.str] = None,
        key_type: typing.Optional[builtins.str] = None,
        usage_plan_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUsagePlanKeyPropsMixin.

        :param key_id: The Id of the UsagePlanKey resource.
        :param key_type: The type of a UsagePlanKey resource for a plan customer.
        :param usage_plan_id: The Id of the UsagePlan resource representing the usage plan containing the UsagePlanKey resource representing a plan customer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_usage_plan_key_mixin_props = apigateway_mixins.CfnUsagePlanKeyMixinProps(
                key_id="keyId",
                key_type="keyType",
                usage_plan_id="usagePlanId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2c5946ed0ae4a5987053d3cece036051faee46d2e1044a50a376bc5a127820)
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            check_type(argname="argument usage_plan_id", value=usage_plan_id, expected_type=type_hints["usage_plan_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key_id is not None:
            self._values["key_id"] = key_id
        if key_type is not None:
            self._values["key_type"] = key_type
        if usage_plan_id is not None:
            self._values["usage_plan_id"] = usage_plan_id

    @builtins.property
    def key_id(self) -> typing.Optional[builtins.str]:
        '''The Id of the UsagePlanKey resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html#cfn-apigateway-usageplankey-keyid
        '''
        result = self._values.get("key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_type(self) -> typing.Optional[builtins.str]:
        '''The type of a UsagePlanKey resource for a plan customer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html#cfn-apigateway-usageplankey-keytype
        '''
        result = self._values.get("key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def usage_plan_id(self) -> typing.Optional[builtins.str]:
        '''The Id of the UsagePlan resource representing the usage plan containing the UsagePlanKey resource representing a plan customer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html#cfn-apigateway-usageplankey-usageplanid
        '''
        result = self._values.get("usage_plan_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUsagePlanKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUsagePlanKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnUsagePlanKeyPropsMixin",
):
    '''The ``AWS::ApiGateway::UsagePlanKey`` resource associates an API key with a usage plan.

    This association determines which users the usage plan is applied to.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplankey.html
    :cloudformationResource: AWS::ApiGateway::UsagePlanKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_usage_plan_key_props_mixin = apigateway_mixins.CfnUsagePlanKeyPropsMixin(apigateway_mixins.CfnUsagePlanKeyMixinProps(
            key_id="keyId",
            key_type="keyType",
            usage_plan_id="usagePlanId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUsagePlanKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::UsagePlanKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e027ae854c79ab93cd800743e15e9e55e0873e8a86d1ab32039a85a52ce124)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad561feafcd20da115e4f0815a857c11a4e04c08f59ce70f955de31a846f9069)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f9bb2c58c0c0151667327893e827c903043668b65e60866f26ed1309109f34)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUsagePlanKeyMixinProps:
        return typing.cast(CfnUsagePlanKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnUsagePlanMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_stages": "apiStages",
        "description": "description",
        "quota": "quota",
        "tags": "tags",
        "throttle": "throttle",
        "usage_plan_name": "usagePlanName",
    },
)
class CfnUsagePlanMixinProps:
    def __init__(
        self,
        *,
        api_stages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUsagePlanPropsMixin.ApiStageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        quota: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUsagePlanPropsMixin.QuotaSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        throttle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUsagePlanPropsMixin.ThrottleSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        usage_plan_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUsagePlanPropsMixin.

        :param api_stages: The associated API stages of a usage plan.
        :param description: The description of a usage plan.
        :param quota: The target maximum number of permitted requests per a given unit time interval.
        :param tags: The collection of tags. Each tag element is associated with a given resource.
        :param throttle: A map containing method level throttling information for API stage in a usage plan.
        :param usage_plan_name: The name of a usage plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_usage_plan_mixin_props = apigateway_mixins.CfnUsagePlanMixinProps(
                api_stages=[apigateway_mixins.CfnUsagePlanPropsMixin.ApiStageProperty(
                    api_id="apiId",
                    stage="stage",
                    throttle={
                        "throttle_key": apigateway_mixins.CfnUsagePlanPropsMixin.ThrottleSettingsProperty(
                            burst_limit=123,
                            rate_limit=123
                        )
                    }
                )],
                description="description",
                quota=apigateway_mixins.CfnUsagePlanPropsMixin.QuotaSettingsProperty(
                    limit=123,
                    offset=123,
                    period="period"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                throttle=apigateway_mixins.CfnUsagePlanPropsMixin.ThrottleSettingsProperty(
                    burst_limit=123,
                    rate_limit=123
                ),
                usage_plan_name="usagePlanName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77782202334b4be40ae74478793c34108ea98be921caf4b1923a560b65e4e24b)
            check_type(argname="argument api_stages", value=api_stages, expected_type=type_hints["api_stages"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument quota", value=quota, expected_type=type_hints["quota"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument throttle", value=throttle, expected_type=type_hints["throttle"])
            check_type(argname="argument usage_plan_name", value=usage_plan_name, expected_type=type_hints["usage_plan_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_stages is not None:
            self._values["api_stages"] = api_stages
        if description is not None:
            self._values["description"] = description
        if quota is not None:
            self._values["quota"] = quota
        if tags is not None:
            self._values["tags"] = tags
        if throttle is not None:
            self._values["throttle"] = throttle
        if usage_plan_name is not None:
            self._values["usage_plan_name"] = usage_plan_name

    @builtins.property
    def api_stages(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsagePlanPropsMixin.ApiStageProperty"]]]]:
        '''The associated API stages of a usage plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-apistages
        '''
        result = self._values.get("api_stages")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsagePlanPropsMixin.ApiStageProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of a usage plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quota(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsagePlanPropsMixin.QuotaSettingsProperty"]]:
        '''The target maximum number of permitted requests per a given unit time interval.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-quota
        '''
        result = self._values.get("quota")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsagePlanPropsMixin.QuotaSettingsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The collection of tags.

        Each tag element is associated with a given resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def throttle(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsagePlanPropsMixin.ThrottleSettingsProperty"]]:
        '''A map containing method level throttling information for API stage in a usage plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-throttle
        '''
        result = self._values.get("throttle")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsagePlanPropsMixin.ThrottleSettingsProperty"]], result)

    @builtins.property
    def usage_plan_name(self) -> typing.Optional[builtins.str]:
        '''The name of a usage plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html#cfn-apigateway-usageplan-usageplanname
        '''
        result = self._values.get("usage_plan_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUsagePlanMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUsagePlanPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnUsagePlanPropsMixin",
):
    '''The ``AWS::ApiGateway::UsagePlan`` resource creates a usage plan for deployed APIs.

    A usage plan sets a target for the throttling and quota limits on individual client API keys. For more information, see `Creating and Using API Usage Plans in Amazon API Gateway <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html>`_ in the *API Gateway Developer Guide* .

    In some cases clients can exceed the targets that you set. Don’t rely on usage plans to control costs. Consider using `AWS Budgets <https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html>`_ to monitor costs and `AWS WAF <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ to manage API requests.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html
    :cloudformationResource: AWS::ApiGateway::UsagePlan
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_usage_plan_props_mixin = apigateway_mixins.CfnUsagePlanPropsMixin(apigateway_mixins.CfnUsagePlanMixinProps(
            api_stages=[apigateway_mixins.CfnUsagePlanPropsMixin.ApiStageProperty(
                api_id="apiId",
                stage="stage",
                throttle={
                    "throttle_key": apigateway_mixins.CfnUsagePlanPropsMixin.ThrottleSettingsProperty(
                        burst_limit=123,
                        rate_limit=123
                    )
                }
            )],
            description="description",
            quota=apigateway_mixins.CfnUsagePlanPropsMixin.QuotaSettingsProperty(
                limit=123,
                offset=123,
                period="period"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            throttle=apigateway_mixins.CfnUsagePlanPropsMixin.ThrottleSettingsProperty(
                burst_limit=123,
                rate_limit=123
            ),
            usage_plan_name="usagePlanName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUsagePlanMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::UsagePlan``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__173c5b60ac2817f3e2501ed6d32c5452805246c484723d4e265d0476f95b5e2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26c74bdedf0bf98448490fa63b0f59e25dc98755726dae34508e9f9d091e690a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0edf0a14e340905f4c0841624c79f181762d462dbee2814558ca5ac0b1fd0d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUsagePlanMixinProps:
        return typing.cast(CfnUsagePlanMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnUsagePlanPropsMixin.ApiStageProperty",
        jsii_struct_bases=[],
        name_mapping={"api_id": "apiId", "stage": "stage", "throttle": "throttle"},
    )
    class ApiStageProperty:
        def __init__(
            self,
            *,
            api_id: typing.Optional[builtins.str] = None,
            stage: typing.Optional[builtins.str] = None,
            throttle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUsagePlanPropsMixin.ThrottleSettingsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''API stage name of the associated API stage in a usage plan.

            :param api_id: API Id of the associated API stage in a usage plan.
            :param stage: API stage name of the associated API stage in a usage plan.
            :param throttle: Map containing method level throttling information for API stage in a usage plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-apistage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                api_stage_property = apigateway_mixins.CfnUsagePlanPropsMixin.ApiStageProperty(
                    api_id="apiId",
                    stage="stage",
                    throttle={
                        "throttle_key": apigateway_mixins.CfnUsagePlanPropsMixin.ThrottleSettingsProperty(
                            burst_limit=123,
                            rate_limit=123
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee71e86ca140052a461f7a023e5f4ecd052afc3e54135961f440bdb78ee4518d)
                check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
                check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
                check_type(argname="argument throttle", value=throttle, expected_type=type_hints["throttle"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if api_id is not None:
                self._values["api_id"] = api_id
            if stage is not None:
                self._values["stage"] = stage
            if throttle is not None:
                self._values["throttle"] = throttle

        @builtins.property
        def api_id(self) -> typing.Optional[builtins.str]:
            '''API Id of the associated API stage in a usage plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-apistage.html#cfn-apigateway-usageplan-apistage-apiid
            '''
            result = self._values.get("api_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage(self) -> typing.Optional[builtins.str]:
            '''API stage name of the associated API stage in a usage plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-apistage.html#cfn-apigateway-usageplan-apistage-stage
            '''
            result = self._values.get("stage")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throttle(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsagePlanPropsMixin.ThrottleSettingsProperty"]]]]:
            '''Map containing method level throttling information for API stage in a usage plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-apistage.html#cfn-apigateway-usageplan-apistage-throttle
            '''
            result = self._values.get("throttle")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsagePlanPropsMixin.ThrottleSettingsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiStageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnUsagePlanPropsMixin.QuotaSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"limit": "limit", "offset": "offset", "period": "period"},
    )
    class QuotaSettingsProperty:
        def __init__(
            self,
            *,
            limit: typing.Optional[jsii.Number] = None,
            offset: typing.Optional[jsii.Number] = None,
            period: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``QuotaSettings`` is a property of the `AWS::ApiGateway::UsagePlan <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html>`_ resource that specifies a target for the maximum number of requests users can make to your REST APIs.

            In some cases clients can exceed the targets that you set. Don’t rely on usage plans to control costs. Consider using `AWS Budgets <https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html>`_ to monitor costs and `AWS WAF <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ to manage API requests.

            :param limit: The target maximum number of requests that can be made in a given time period.
            :param offset: The number of requests subtracted from the given limit in the initial time period.
            :param period: The time period in which the limit applies. Valid values are "DAY", "WEEK" or "MONTH".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-quotasettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                quota_settings_property = apigateway_mixins.CfnUsagePlanPropsMixin.QuotaSettingsProperty(
                    limit=123,
                    offset=123,
                    period="period"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4c52106c7dae4459823c31a0f8f044a15663c55a7bc92f6dee62a6832ee5a7a)
                check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
                check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if limit is not None:
                self._values["limit"] = limit
            if offset is not None:
                self._values["offset"] = offset
            if period is not None:
                self._values["period"] = period

        @builtins.property
        def limit(self) -> typing.Optional[jsii.Number]:
            '''The target maximum number of requests that can be made in a given time period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-quotasettings.html#cfn-apigateway-usageplan-quotasettings-limit
            '''
            result = self._values.get("limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def offset(self) -> typing.Optional[jsii.Number]:
            '''The number of requests subtracted from the given limit in the initial time period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-quotasettings.html#cfn-apigateway-usageplan-quotasettings-offset
            '''
            result = self._values.get("offset")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def period(self) -> typing.Optional[builtins.str]:
            '''The time period in which the limit applies.

            Valid values are "DAY", "WEEK" or "MONTH".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-quotasettings.html#cfn-apigateway-usageplan-quotasettings-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuotaSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnUsagePlanPropsMixin.ThrottleSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"burst_limit": "burstLimit", "rate_limit": "rateLimit"},
    )
    class ThrottleSettingsProperty:
        def __init__(
            self,
            *,
            burst_limit: typing.Optional[jsii.Number] = None,
            rate_limit: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``ThrottleSettings`` is a property of the `AWS::ApiGateway::UsagePlan <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-usageplan.html>`_ resource that specifies the overall request rate (average requests per second) and burst capacity when users call your REST APIs.

            :param burst_limit: The API target request burst rate limit. This allows more requests through for a period of time than the target rate limit.
            :param rate_limit: The API target request rate limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-throttlesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
                
                throttle_settings_property = apigateway_mixins.CfnUsagePlanPropsMixin.ThrottleSettingsProperty(
                    burst_limit=123,
                    rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__233fcec2a67170169c2308d0d9eced04ec391196d775c5dc9ec837f355b0591c)
                check_type(argname="argument burst_limit", value=burst_limit, expected_type=type_hints["burst_limit"])
                check_type(argname="argument rate_limit", value=rate_limit, expected_type=type_hints["rate_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if burst_limit is not None:
                self._values["burst_limit"] = burst_limit
            if rate_limit is not None:
                self._values["rate_limit"] = rate_limit

        @builtins.property
        def burst_limit(self) -> typing.Optional[jsii.Number]:
            '''The API target request burst rate limit.

            This allows more requests through for a period of time than the target rate limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-throttlesettings.html#cfn-apigateway-usageplan-throttlesettings-burstlimit
            '''
            result = self._values.get("burst_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rate_limit(self) -> typing.Optional[jsii.Number]:
            '''The API target request rate limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigateway-usageplan-throttlesettings.html#cfn-apigateway-usageplan-throttlesettings-ratelimit
            '''
            result = self._values.get("rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThrottleSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnVpcLinkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "tags": "tags",
        "target_arns": "targetArns",
    },
)
class CfnVpcLinkMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnVpcLinkPropsMixin.

        :param description: The description of the VPC link.
        :param name: The name used to label and identify the VPC link.
        :param tags: An array of arbitrary tags (key-value pairs) to associate with the VPC link.
        :param target_arns: The ARN of the network load balancer of the VPC targeted by the VPC link. The network load balancer must be owned by the same AWS account of the API owner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
            
            cfn_vpc_link_mixin_props = apigateway_mixins.CfnVpcLinkMixinProps(
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_arns=["targetArns"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0a4d90ddbd07e779440fc3e049348fb1525de4d2707be74f9a5eb6b21297ea4)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_arns", value=target_arns, expected_type=type_hints["target_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if target_arns is not None:
            self._values["target_arns"] = target_arns

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the VPC link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name used to label and identify the VPC link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of arbitrary tags (key-value pairs) to associate with the VPC link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARN of the network load balancer of the VPC targeted by the VPC link.

        The network load balancer must be owned by the same AWS account of the API owner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html#cfn-apigateway-vpclink-targetarns
        '''
        result = self._values.get("target_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcLinkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVpcLinkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_apigateway.mixins.CfnVpcLinkPropsMixin",
):
    '''The ``AWS::ApiGateway::VpcLink`` resource creates an API Gateway VPC link for a REST API to access resources in an Amazon Virtual Private Cloud (VPC).

    For more information, see `vpclink:create <https://docs.aws.amazon.com/apigateway/latest/api/API_CreateVpcLink.html>`_ in the ``Amazon API Gateway REST API Reference`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-vpclink.html
    :cloudformationResource: AWS::ApiGateway::VpcLink
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_apigateway import mixins as apigateway_mixins
        
        cfn_vpc_link_props_mixin = apigateway_mixins.CfnVpcLinkPropsMixin(apigateway_mixins.CfnVpcLinkMixinProps(
            description="description",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_arns=["targetArns"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVpcLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApiGateway::VpcLink``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca0ef85207e8db9c3bf77b940bb160436805f513982430622100b01940abb46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ced072caaf7388156bb541709c7b08d083644070b78ed96d5cee6c0aadbbaf4e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d7abe8f009dd64f1a31f8935a043d9c570cf8aa98e1e8bab1d8c903135ff18)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVpcLinkMixinProps:
        return typing.cast(CfnVpcLinkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAccountMixinProps",
    "CfnAccountPropsMixin",
    "CfnApiKeyMixinProps",
    "CfnApiKeyPropsMixin",
    "CfnAuthorizerMixinProps",
    "CfnAuthorizerPropsMixin",
    "CfnBasePathMappingMixinProps",
    "CfnBasePathMappingPropsMixin",
    "CfnBasePathMappingV2MixinProps",
    "CfnBasePathMappingV2PropsMixin",
    "CfnClientCertificateMixinProps",
    "CfnClientCertificatePropsMixin",
    "CfnDeploymentMixinProps",
    "CfnDeploymentPropsMixin",
    "CfnDocumentationPartMixinProps",
    "CfnDocumentationPartPropsMixin",
    "CfnDocumentationVersionMixinProps",
    "CfnDocumentationVersionPropsMixin",
    "CfnDomainNameAccessAssociationMixinProps",
    "CfnDomainNameAccessAssociationPropsMixin",
    "CfnDomainNameMixinProps",
    "CfnDomainNamePropsMixin",
    "CfnDomainNameV2MixinProps",
    "CfnDomainNameV2PropsMixin",
    "CfnGatewayResponseMixinProps",
    "CfnGatewayResponsePropsMixin",
    "CfnMethodMixinProps",
    "CfnMethodPropsMixin",
    "CfnModelMixinProps",
    "CfnModelPropsMixin",
    "CfnRequestValidatorMixinProps",
    "CfnRequestValidatorPropsMixin",
    "CfnResourceMixinProps",
    "CfnResourcePropsMixin",
    "CfnRestApiMixinProps",
    "CfnRestApiPropsMixin",
    "CfnStageMixinProps",
    "CfnStagePropsMixin",
    "CfnUsagePlanKeyMixinProps",
    "CfnUsagePlanKeyPropsMixin",
    "CfnUsagePlanMixinProps",
    "CfnUsagePlanPropsMixin",
    "CfnVpcLinkMixinProps",
    "CfnVpcLinkPropsMixin",
]

publication.publish()

def _typecheckingstub__b4ae4ef4012c2ddb5f9a2fe2e77835b7caae1e76220f418a13a94808c188f495(
    *,
    cloud_watch_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9fb8ed77b3acd1132807e2d8f7501879a148d594bf09869f1263ce388fcf85(
    props: typing.Union[CfnAccountMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3b5f0743e2fdc1ccaf76cfe0acaf4de41b11c1bae0d9f93ed334fd58c796c2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be175413c0997e42b8eac3aa03a079cdb90043026798c50e491452a9cc0ab4c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40a9ec618f0dc58c25ffe419ef733f1397d2a97286d49c9af11df9c4728bf7d(
    *,
    customer_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    generate_distinct_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    stage_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApiKeyPropsMixin.StageKeyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6ef21cefaa9f4ec0caa0dde5abe9948201a3fa0b021587ec530cfac3ff0687(
    props: typing.Union[CfnApiKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb108cacc891782cc9bd7cd0a5eb77cec31b2e18719d7f6ab735e075ce81e3c2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b12b197e3c4cf77d867dc3e7ca2776aaf20fb390f89b544230ca4b5220d98f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2d45cf9ba67190fdb0e0847faebb0af535a361baa4a4b4cf016270d7912a22(
    *,
    rest_api_id: typing.Optional[builtins.str] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fdb4445b1b4476ab5f691393ec07b0c2248451c55e9ee7ab00ffa018f26328f(
    *,
    authorizer_credentials: typing.Optional[builtins.str] = None,
    authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    authorizer_uri: typing.Optional[builtins.str] = None,
    auth_type: typing.Optional[builtins.str] = None,
    identity_source: typing.Optional[builtins.str] = None,
    identity_validation_expression: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    provider_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45531243a956388e3b26a67298a0cf13d80e0d3f572ada5b5803bdd45c0bcf7d(
    props: typing.Union[CfnAuthorizerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070b4f9e767e9500a4684f004dfe7ad5acfd1e18ffacd89685614f3b1ec2b50a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f0d651c2cdfdc1c1e64ad3528a2e67ecac45c2d861666178d0d0c966bd2121(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a926e6e716b81ecf2bb5ea32284c02f96c05d2dd22570c8d01ef9f9699a8ae7(
    *,
    base_path: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6660880b73afc5fe53e3c92496cd48c035fef36d7ee5674ce2de7df5cce09f(
    props: typing.Union[CfnBasePathMappingMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c920cdb15fbfe9b6aa4ba56267ee3ac00757201415b015af28ff66aecbe364d1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c1f6f2970c75b106c2baf86b655cb8ee5007e77cc1bc5f50350d4cc2920991(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7370e2cc9c8202b81c0224d093266038a2a84ab7d18c56f00bbe65259c8f7d54(
    *,
    base_path: typing.Optional[builtins.str] = None,
    domain_name_arn: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ddf36f303caa5ea3cc0b031cdd413f247cc7c8877c7b70d50b8cc10879320b(
    props: typing.Union[CfnBasePathMappingV2MixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c50c406c28342738fb5130130c0079c611708cf59215b133a273748ff76f189c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1a073de8e1ea064d69b0c3a8b64bc6b85623530310f871e23920e47720022b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b059e4c55be9f108c3ec78bc25760e10928b3009d9ca2484f8e7ba51fd58ec1e(
    *,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdb55897c60d2e1d6c800f92b39109c9a923a6563b4b1bf03803899d4018eab(
    props: typing.Union[CfnClientCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bf6303d6df8a22fe05f06a563ff01895e7e57d3ab87e368020a078f10eb89a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f820793afa30f58ae19ef492f5222845424c18a7d4f8ac96578eebbc6b118af2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40300f53affc19168065d4dc9971bb6415a54c1aa95737c7e412f224c839827d(
    *,
    deployment_canary_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.DeploymentCanarySettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
    stage_description: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.StageDescriptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51af28b22596895582ad4923c2d41d70fb0e53c8b5692990d5c0cae639cdaa1f(
    props: typing.Union[CfnDeploymentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920b75d7c0eb8831031a8c0d8d1ba3c252656c4ac7615a6436d4134d0e3af47b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5ae7a4e19cc84d11e45fdfea1987eb4a29118e593059ceeddf21af4a027302(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496421d57fc8f06071cdc43c9e672514902461601c155a85aff2293164248814(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c43d4983f26e74a685e10d3f546e59ca9aa9a1baa48b07f4e40a8894fd206a(
    *,
    percent_traffic: typing.Optional[jsii.Number] = None,
    stage_variable_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d902da8a3d5ca3c7637f3672cceb0a6d03320cb06bb47f4ac78178122ca91adb(
    *,
    percent_traffic: typing.Optional[jsii.Number] = None,
    stage_variable_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2ea2e1b2071015ea06a81ff242b3f5d323bc1b3e6ee0442d4d8f0af0c06852(
    *,
    cache_data_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cache_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    caching_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    http_method: typing.Optional[builtins.str] = None,
    logging_level: typing.Optional[builtins.str] = None,
    metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_path: typing.Optional[builtins.str] = None,
    throttling_burst_limit: typing.Optional[jsii.Number] = None,
    throttling_rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cbda9a88b45df1baa3dd06dff29a85e74bd2ace94ff783beac024d9c9c38c7(
    *,
    access_log_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cache_cluster_size: typing.Optional[builtins.str] = None,
    cache_data_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cache_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    caching_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    canary_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.CanarySettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    client_certificate_id: typing.Optional[builtins.str] = None,
    data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation_version: typing.Optional[builtins.str] = None,
    logging_level: typing.Optional[builtins.str] = None,
    method_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeploymentPropsMixin.MethodSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    throttling_burst_limit: typing.Optional[jsii.Number] = None,
    throttling_rate_limit: typing.Optional[jsii.Number] = None,
    tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e55be9483b40000c912966094d27feb425e2de71546f848ddf6b82176a5d46c(
    *,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDocumentationPartPropsMixin.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    properties: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1c17ab0ee6c93d516fd8b7ed280589dda26f8502070608c921b17f67bc123c(
    props: typing.Union[CfnDocumentationPartMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91883d66e90a5724121d1d425598842ea8911f444b489bd02a04dcb53613c407(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d53839a5b4abe45015c42fc2d6828fede4c48de50d67fab69034444d17cbfd4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd543544b8508f381cc03617be28a09acaea00d0ba05834fd62f5663bf97652(
    *,
    method: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabf58a4e4d3cd0239f40bbf556bdfd20178236721da99ec4116c0778a7e3017(
    *,
    description: typing.Optional[builtins.str] = None,
    documentation_version: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7c346227a432924cc28c6727669a4f81e1c106774d3b517d894930fe0f0d19(
    props: typing.Union[CfnDocumentationVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d4d88081854fb9d1a6e55c8bd43255beced8ae06a41401b294c9f9aeb66db9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ff6c8a4245c2026de743ac8d4674475dd26d63c109e98ff513b8964302998b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f3e2917c3578379dd19d3dc95a3db1954a3f54aa50c28387b26b8f987b7c4a(
    *,
    access_association_source: typing.Optional[builtins.str] = None,
    access_association_source_type: typing.Optional[builtins.str] = None,
    domain_name_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66861aaab7f378b3dd8f052a02296b8a588acc119f4a8bf69536ed07e345b26b(
    props: typing.Union[CfnDomainNameAccessAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2678ba7c3d723310c24fee73d803bafe70ebeaad983d293ec9586c9d902a474e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b92b8cfd5767205370f7002e75919dc5df0393bcf429ae7e721c06a4d4fb1cb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7bb0fccbf95b817b115d90337197d9438040235b4882a32d824ed6e5424f6e8(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    endpoint_access_mode: typing.Optional[builtins.str] = None,
    endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainNamePropsMixin.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mutual_tls_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainNamePropsMixin.MutualTlsAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ownership_verification_certificate_arn: typing.Optional[builtins.str] = None,
    regional_certificate_arn: typing.Optional[builtins.str] = None,
    routing_mode: typing.Optional[builtins.str] = None,
    security_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee4cf63c82056427f389ac42dab61000f425b3c55b3f2dbf6415079fc0fb606(
    props: typing.Union[CfnDomainNameMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214e89db1eb09b671d494a032a7e77d75acb708e3677043dbb34fa5173bdda1a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050d8c6dc260cfce08a458cc6c5a200aa61ebe7527a36bbd07d6393bb99ae0db(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9c01fe4f1c283b79119437879da37793d59f0be38021baa86fd0f1f023aae7(
    *,
    ip_address_type: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ed436d1bb283806e756ce50177b9863c4b0c980cf4abb49c6f18db8a22499d(
    *,
    truststore_uri: typing.Optional[builtins.str] = None,
    truststore_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fcc8c30491d071c0648d0b8a6856d37a541072560d8e69e28be59affe2cf24(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    endpoint_access_mode: typing.Optional[builtins.str] = None,
    endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainNameV2PropsMixin.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy: typing.Any = None,
    routing_mode: typing.Optional[builtins.str] = None,
    security_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5597eeaa9adc8227c741252aaf782e74c3a36d7eb77a648cccdc3230ed32deb3(
    props: typing.Union[CfnDomainNameV2MixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b823e4d10b7d7500636cbf39af222f81859086c2671aebcb7ab01453e96a0ab8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d2f85850115a134094271f211aa4e4a343ef4e170078a1b947c96f3a4578b9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a443153dc5beac1dbbe289f571f5d128868a5ad78b6f382b356c2ad29af97d53(
    *,
    ip_address_type: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b141a9b9541da979214c570ff0dae3750c5ad3c3abcdab2283fc98a89b9837d7(
    *,
    response_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    response_templates: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    response_type: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea5bcb52aea73eded98b6771a2769f0cfd14f2392553e5d54f9a7db19075e91(
    props: typing.Union[CfnGatewayResponseMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4821cb5fa4937e6b2d3886d09ebccf1aff057393aa7af585a0f3d0656d0097e7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89342ef20c4e5d8adb5dfd84d2c84a9ca853c7688eaa4baa11e6c1f09bc3273d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e21fc26281183856b2328a79523d6206593249c46a47e879ff1f0a1ccca9af2(
    *,
    api_key_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    authorization_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    authorization_type: typing.Optional[builtins.str] = None,
    authorizer_id: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[builtins.str] = None,
    integration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMethodPropsMixin.IntegrationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    method_responses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMethodPropsMixin.MethodResponseProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    operation_name: typing.Optional[builtins.str] = None,
    request_models: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    request_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]]] = None,
    request_validator_id: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045cca9c6a73a97d0f4b5203f34b52067bd4be43ee2cb6c68efe885120d69c1a(
    props: typing.Union[CfnMethodMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43030e793aded1f77f1a6a1886e2657d6e2c11bca001338a7de9805a1970ff7f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23e139a017586ac5c63ea581c6b3c1119e5675e478012f3104513b95c5d0ef1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a8f4a5f2386af3ce6bc9839c701ff9b13e41d1891c7ef699d7f9d60c04a42f(
    *,
    cache_key_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_namespace: typing.Optional[builtins.str] = None,
    connection_id: typing.Optional[builtins.str] = None,
    connection_type: typing.Optional[builtins.str] = None,
    content_handling: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[builtins.str] = None,
    integration_http_method: typing.Optional[builtins.str] = None,
    integration_responses: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMethodPropsMixin.IntegrationResponseProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    integration_target: typing.Optional[builtins.str] = None,
    passthrough_behavior: typing.Optional[builtins.str] = None,
    request_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    request_templates: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    response_transfer_mode: typing.Optional[builtins.str] = None,
    timeout_in_millis: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b754110af3c6f3f5c00e605716b0ddd545dd1c050eacdb95bb6e2f379dee3b5(
    *,
    content_handling: typing.Optional[builtins.str] = None,
    response_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    response_templates: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    selection_pattern: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14dad9f7c8d3e9e0e26370af2b281d6f75c9f3baa50eb4476bd2c884f513c22(
    *,
    response_models: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    response_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]]] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad1149641ec406ba336580f3ea73b75dc32971c51fbaec356afd135a73f1963(
    *,
    content_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
    schema: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f63e16db1759dc264ea682e1d837601dafb5359751b5dba8114cfda4e395f4(
    props: typing.Union[CfnModelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e71f4b0c577341fde41d5bd8ce552598fde138dd73c568226fd3b6e90e997f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2b6c1cc250eaf539405c23e00f684406117f1280de535cde7b6b051eb2de05(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3ffe6ce422e7bbe86ff702290bb0bc96460f98fd5c9bab01e98ea373d25a44(
    *,
    name: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
    validate_request_body: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    validate_request_parameters: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc80f0de96075e38efffcc99be5c82d5dc5bbf2c2fe588eace990fdf7ebc8c1(
    props: typing.Union[CfnRequestValidatorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f62c1d537d628ae2c073ff8501ab402d814c1bde8cedbcfd457c193de49eb4c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adae5ca91332c20cbb9baaf3dd993855f42258b12f873b9213542eba30715509(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16e4f5ad32bcf9a1df350143f97eb1bde9339877f5daac8d8d48c1302d51c6f(
    *,
    parent_id: typing.Optional[builtins.str] = None,
    path_part: typing.Optional[builtins.str] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__862169161dbb247481122ac401878fe77e8beb3b63f4eac0d8547c58ee013d40(
    props: typing.Union[CfnResourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a91f26050d12f341624025a5e34885ec71c496c3b386209f3e44054503eeb1c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc02974fa705d3310e4bb2e3705c248d8258bc7a150240e8c763e76c13fbe9eb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8a816e2ec061957e5dbd71db985e8ebbce0748cade85ce82084c32eceb8f70(
    *,
    api_key_source_type: typing.Optional[builtins.str] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    body: typing.Any = None,
    body_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRestApiPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    clone_from: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    disable_execute_api_endpoint: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    endpoint_access_mode: typing.Optional[builtins.str] = None,
    endpoint_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRestApiPropsMixin.EndpointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fail_on_warnings: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    policy: typing.Any = None,
    security_policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bea9ffd65f10bb5e5d464cc0ef3c9a6615cb1b87fe76a482190387213185de8(
    props: typing.Union[CfnRestApiMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891d31aed5db6fb33d8a7779fdc6ecbd57a623944a42ecdded94e46ff354e697(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f8498864ed92185801af8181654f388103ef8db954f9e5b2cd993e32fb50e7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5efd4b22800c3e4c628f3fd78cb97ee43dca98db8889439f8ab84de9f6c0f7(
    *,
    ip_address_type: typing.Optional[builtins.str] = None,
    types: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_endpoint_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b052841bf93abaaa6255df441da7c9bcab374027fdf02402199e6f5dc0e90f(
    *,
    bucket: typing.Optional[builtins.str] = None,
    e_tag: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a1cd67fe1c2e89478e7bd4012125c7cfe9c59c68ad78bef4655ac433a701bc(
    *,
    access_log_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStagePropsMixin.AccessLogSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cache_cluster_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cache_cluster_size: typing.Optional[builtins.str] = None,
    canary_setting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStagePropsMixin.CanarySettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    client_certificate_id: typing.Optional[builtins.str] = None,
    deployment_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    documentation_version: typing.Optional[builtins.str] = None,
    method_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStagePropsMixin.MethodSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    rest_api_id: typing.Optional[builtins.str] = None,
    stage_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tracing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    variables: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322d5ab2f1e0f903b548f60aa6fa7470bbf188c79c7309003c9a2e0ff0b7c94b(
    props: typing.Union[CfnStageMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1306a221b4170bf3674c5b3455a17be3bf8688cdace208e574fbe4fb7d5513fd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9960ed1ce38cb796160c2628bd38e4caa880ff27c5385f35bb9a849e38a20e66(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639106ac8b14a88156048b746f2b53f96ab33659aad4a97b36ff72724215d0e4(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20dec0919adf6f5553320e8efb923e8d9209a13becfe88d1e176a0896848aa5c(
    *,
    deployment_id: typing.Optional[builtins.str] = None,
    percent_traffic: typing.Optional[jsii.Number] = None,
    stage_variable_overrides: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    use_stage_cache: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3538fdeefb625465256cfe520c8895344951533806f12c21c168a0c275c23c53(
    *,
    cache_data_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cache_ttl_in_seconds: typing.Optional[jsii.Number] = None,
    caching_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    data_trace_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    http_method: typing.Optional[builtins.str] = None,
    logging_level: typing.Optional[builtins.str] = None,
    metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_path: typing.Optional[builtins.str] = None,
    throttling_burst_limit: typing.Optional[jsii.Number] = None,
    throttling_rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2c5946ed0ae4a5987053d3cece036051faee46d2e1044a50a376bc5a127820(
    *,
    key_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    usage_plan_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e027ae854c79ab93cd800743e15e9e55e0873e8a86d1ab32039a85a52ce124(
    props: typing.Union[CfnUsagePlanKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad561feafcd20da115e4f0815a857c11a4e04c08f59ce70f955de31a846f9069(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f9bb2c58c0c0151667327893e827c903043668b65e60866f26ed1309109f34(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77782202334b4be40ae74478793c34108ea98be921caf4b1923a560b65e4e24b(
    *,
    api_stages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUsagePlanPropsMixin.ApiStageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    quota: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUsagePlanPropsMixin.QuotaSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    throttle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUsagePlanPropsMixin.ThrottleSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    usage_plan_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__173c5b60ac2817f3e2501ed6d32c5452805246c484723d4e265d0476f95b5e2e(
    props: typing.Union[CfnUsagePlanMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c74bdedf0bf98448490fa63b0f59e25dc98755726dae34508e9f9d091e690a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0edf0a14e340905f4c0841624c79f181762d462dbee2814558ca5ac0b1fd0d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee71e86ca140052a461f7a023e5f4ecd052afc3e54135961f440bdb78ee4518d(
    *,
    api_id: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    throttle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUsagePlanPropsMixin.ThrottleSettingsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c52106c7dae4459823c31a0f8f044a15663c55a7bc92f6dee62a6832ee5a7a(
    *,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
    period: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233fcec2a67170169c2308d0d9eced04ec391196d775c5dc9ec837f355b0591c(
    *,
    burst_limit: typing.Optional[jsii.Number] = None,
    rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a4d90ddbd07e779440fc3e049348fb1525de4d2707be74f9a5eb6b21297ea4(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca0ef85207e8db9c3bf77b940bb160436805f513982430622100b01940abb46(
    props: typing.Union[CfnVpcLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced072caaf7388156bb541709c7b08d083644070b78ed96d5cee6c0aadbbaf4e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d7abe8f009dd64f1a31f8935a043d9c570cf8aa98e1e8bab1d8c903135ff18(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
