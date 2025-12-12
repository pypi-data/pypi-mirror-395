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
    jsii_type="@aws-cdk/mixins-preview.aws_s3objectlambda.mixins.CfnAccessPointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "object_lambda_configuration": "objectLambdaConfiguration",
    },
)
class CfnAccessPointMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        object_lambda_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPointPropsMixin.ObjectLambdaConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessPointPropsMixin.

        :param name: The name of this access point.
        :param object_lambda_configuration: A configuration used when creating an Object Lambda Access Point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3objectlambda import mixins as s3objectlambda_mixins
            
            # content_transformation: Any
            
            cfn_access_point_mixin_props = s3objectlambda_mixins.CfnAccessPointMixinProps(
                name="name",
                object_lambda_configuration=s3objectlambda_mixins.CfnAccessPointPropsMixin.ObjectLambdaConfigurationProperty(
                    allowed_features=["allowedFeatures"],
                    cloud_watch_metrics_enabled=False,
                    supporting_access_point="supportingAccessPoint",
                    transformation_configurations=[s3objectlambda_mixins.CfnAccessPointPropsMixin.TransformationConfigurationProperty(
                        actions=["actions"],
                        content_transformation=content_transformation
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d12fc88639a02f4b99d16005bb9647cb776dec48470480f0b22723a73ac7b0e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument object_lambda_configuration", value=object_lambda_configuration, expected_type=type_hints["object_lambda_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if object_lambda_configuration is not None:
            self._values["object_lambda_configuration"] = object_lambda_configuration

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html#cfn-s3objectlambda-accesspoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_lambda_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.ObjectLambdaConfigurationProperty"]]:
        '''A configuration used when creating an Object Lambda Access Point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration
        '''
        result = self._values.get("object_lambda_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.ObjectLambdaConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3objectlambda.mixins.CfnAccessPointPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "object_lambda_access_point": "objectLambdaAccessPoint",
        "policy_document": "policyDocument",
    },
)
class CfnAccessPointPolicyMixinProps:
    def __init__(
        self,
        *,
        object_lambda_access_point: typing.Optional[builtins.str] = None,
        policy_document: typing.Any = None,
    ) -> None:
        '''Properties for CfnAccessPointPolicyPropsMixin.

        :param object_lambda_access_point: An access point with an attached AWS Lambda function used to access transformed data from an Amazon S3 bucket.
        :param policy_document: Object Lambda Access Point resource policy document.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3objectlambda import mixins as s3objectlambda_mixins
            
            # policy_document: Any
            
            cfn_access_point_policy_mixin_props = s3objectlambda_mixins.CfnAccessPointPolicyMixinProps(
                object_lambda_access_point="objectLambdaAccessPoint",
                policy_document=policy_document
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6604ef720099cc441b98711cd4c9820d0317c57f2bce60bc6b116192df0d14ca)
            check_type(argname="argument object_lambda_access_point", value=object_lambda_access_point, expected_type=type_hints["object_lambda_access_point"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if object_lambda_access_point is not None:
            self._values["object_lambda_access_point"] = object_lambda_access_point
        if policy_document is not None:
            self._values["policy_document"] = policy_document

    @builtins.property
    def object_lambda_access_point(self) -> typing.Optional[builtins.str]:
        '''An access point with an attached AWS Lambda function used to access transformed data from an Amazon S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html#cfn-s3objectlambda-accesspointpolicy-objectlambdaaccesspoint
        '''
        result = self._values.get("object_lambda_access_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''Object Lambda Access Point resource policy document.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html#cfn-s3objectlambda-accesspointpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessPointPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3objectlambda.mixins.CfnAccessPointPolicyPropsMixin",
):
    '''The ``AWS::S3ObjectLambda::AccessPointPolicy`` resource specifies the Object Lambda Access Point resource policy document.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html
    :cloudformationResource: AWS::S3ObjectLambda::AccessPointPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3objectlambda import mixins as s3objectlambda_mixins
        
        # policy_document: Any
        
        cfn_access_point_policy_props_mixin = s3objectlambda_mixins.CfnAccessPointPolicyPropsMixin(s3objectlambda_mixins.CfnAccessPointPolicyMixinProps(
            object_lambda_access_point="objectLambdaAccessPoint",
            policy_document=policy_document
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccessPointPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3ObjectLambda::AccessPointPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ad71efe82045c67cf0afb31f6076567d828ca0ed863a1d5687b9b0c028ea3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c21f6b3c86f818d1e5f9690e8517b533e83ef1e96b3478f70e9fbbafb0e7bc0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769af0ac5681ee4a69df7dd2a4ae494f89d897e645bcd9943a4b52cd5689afc7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessPointPolicyMixinProps:
        return typing.cast(CfnAccessPointPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnAccessPointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3objectlambda.mixins.CfnAccessPointPropsMixin",
):
    '''The ``AWS::S3ObjectLambda::AccessPoint`` resource specifies an Object Lambda Access Point used to access a bucket.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html
    :cloudformationResource: AWS::S3ObjectLambda::AccessPoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3objectlambda import mixins as s3objectlambda_mixins
        
        # content_transformation: Any
        
        cfn_access_point_props_mixin = s3objectlambda_mixins.CfnAccessPointPropsMixin(s3objectlambda_mixins.CfnAccessPointMixinProps(
            name="name",
            object_lambda_configuration=s3objectlambda_mixins.CfnAccessPointPropsMixin.ObjectLambdaConfigurationProperty(
                allowed_features=["allowedFeatures"],
                cloud_watch_metrics_enabled=False,
                supporting_access_point="supportingAccessPoint",
                transformation_configurations=[s3objectlambda_mixins.CfnAccessPointPropsMixin.TransformationConfigurationProperty(
                    actions=["actions"],
                    content_transformation=content_transformation
                )]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccessPointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3ObjectLambda::AccessPoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b1f3b492cbd7bb691ebf7083619c9dbf58702de604f93ae4133d223870874e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a32f28332e2df7c03e026a90b8c4a8323d8cb2859ae09c9096eee2b86f698eab)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c661eddda7aa178a4caf4ab950123f61467634ddd8c1124301848d58d7ab303a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessPointMixinProps:
        return typing.cast(CfnAccessPointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3objectlambda.mixins.CfnAccessPointPropsMixin.AliasProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status", "value": "value"},
    )
    class AliasProperty:
        def __init__(
            self,
            *,
            status: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The alias of an Object Lambda Access Point.

            For more information, see `How to use a bucket-style alias for your S3 bucket Object Lambda Access Point <https://docs.aws.amazon.com/AmazonS3/latest/userguide/olap-use.html#ol-access-points-alias>`_ .

            :param status: The status of the Object Lambda Access Point alias. If the status is ``PROVISIONING`` , the Object Lambda Access Point is provisioning the alias and the alias is not ready for use yet. If the status is ``READY`` , the Object Lambda Access Point alias is successfully provisioned and ready for use.
            :param value: The alias value of the Object Lambda Access Point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-alias.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3objectlambda import mixins as s3objectlambda_mixins
                
                alias_property = s3objectlambda_mixins.CfnAccessPointPropsMixin.AliasProperty(
                    status="status",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27cf740286ddb648c985061aadaf777da73f1f5f9152f3ced4d41e6a7e4da417)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the Object Lambda Access Point alias.

            If the status is ``PROVISIONING`` , the Object Lambda Access Point is provisioning the alias and the alias is not ready for use yet. If the status is ``READY`` , the Object Lambda Access Point alias is successfully provisioned and ready for use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-alias.html#cfn-s3objectlambda-accesspoint-alias-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The alias value of the Object Lambda Access Point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-alias.html#cfn-s3objectlambda-accesspoint-alias-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AliasProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3objectlambda.mixins.CfnAccessPointPropsMixin.ObjectLambdaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_features": "allowedFeatures",
            "cloud_watch_metrics_enabled": "cloudWatchMetricsEnabled",
            "supporting_access_point": "supportingAccessPoint",
            "transformation_configurations": "transformationConfigurations",
        },
    )
    class ObjectLambdaConfigurationProperty:
        def __init__(
            self,
            *,
            allowed_features: typing.Optional[typing.Sequence[builtins.str]] = None,
            cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            supporting_access_point: typing.Optional[builtins.str] = None,
            transformation_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPointPropsMixin.TransformationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A configuration used when creating an Object Lambda Access Point.

            :param allowed_features: A container for allowed features. Valid inputs are ``GetObject-Range`` , ``GetObject-PartNumber`` , ``HeadObject-Range`` , and ``HeadObject-PartNumber`` .
            :param cloud_watch_metrics_enabled: A container for whether the CloudWatch metrics configuration is enabled.
            :param supporting_access_point: Standard access point associated with the Object Lambda Access Point.
            :param transformation_configurations: A container for transformation configurations for an Object Lambda Access Point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3objectlambda import mixins as s3objectlambda_mixins
                
                # content_transformation: Any
                
                object_lambda_configuration_property = s3objectlambda_mixins.CfnAccessPointPropsMixin.ObjectLambdaConfigurationProperty(
                    allowed_features=["allowedFeatures"],
                    cloud_watch_metrics_enabled=False,
                    supporting_access_point="supportingAccessPoint",
                    transformation_configurations=[s3objectlambda_mixins.CfnAccessPointPropsMixin.TransformationConfigurationProperty(
                        actions=["actions"],
                        content_transformation=content_transformation
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77df052814f96237855dbe7fc7a0dc13e7e8d4f8801a0b47573828acd52852ce)
                check_type(argname="argument allowed_features", value=allowed_features, expected_type=type_hints["allowed_features"])
                check_type(argname="argument cloud_watch_metrics_enabled", value=cloud_watch_metrics_enabled, expected_type=type_hints["cloud_watch_metrics_enabled"])
                check_type(argname="argument supporting_access_point", value=supporting_access_point, expected_type=type_hints["supporting_access_point"])
                check_type(argname="argument transformation_configurations", value=transformation_configurations, expected_type=type_hints["transformation_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_features is not None:
                self._values["allowed_features"] = allowed_features
            if cloud_watch_metrics_enabled is not None:
                self._values["cloud_watch_metrics_enabled"] = cloud_watch_metrics_enabled
            if supporting_access_point is not None:
                self._values["supporting_access_point"] = supporting_access_point
            if transformation_configurations is not None:
                self._values["transformation_configurations"] = transformation_configurations

        @builtins.property
        def allowed_features(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A container for allowed features.

            Valid inputs are ``GetObject-Range`` , ``GetObject-PartNumber`` , ``HeadObject-Range`` , and ``HeadObject-PartNumber`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration-allowedfeatures
            '''
            result = self._values.get("allowed_features")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def cloud_watch_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A container for whether the CloudWatch metrics configuration is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration-cloudwatchmetricsenabled
            '''
            result = self._values.get("cloud_watch_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def supporting_access_point(self) -> typing.Optional[builtins.str]:
            '''Standard access point associated with the Object Lambda Access Point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration-supportingaccesspoint
            '''
            result = self._values.get("supporting_access_point")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transformation_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.TransformationConfigurationProperty"]]]]:
            '''A container for transformation configurations for an Object Lambda Access Point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration-transformationconfigurations
            '''
            result = self._values.get("transformation_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.TransformationConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectLambdaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3objectlambda.mixins.CfnAccessPointPropsMixin.PolicyStatusProperty",
        jsii_struct_bases=[],
        name_mapping={"is_public": "isPublic"},
    )
    class PolicyStatusProperty:
        def __init__(
            self,
            *,
            is_public: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param is_public: Specifies whether the Object lambda Access Point Policy is Public or not. Object lambda Access Points are private by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-policystatus.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3objectlambda import mixins as s3objectlambda_mixins
                
                policy_status_property = s3objectlambda_mixins.CfnAccessPointPropsMixin.PolicyStatusProperty(
                    is_public=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2bda2c18b1ce79a913e296fcf1c7525448e724b6adca4668a983f52fabe1d216)
                check_type(argname="argument is_public", value=is_public, expected_type=type_hints["is_public"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_public is not None:
                self._values["is_public"] = is_public

        @builtins.property
        def is_public(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the Object lambda Access Point Policy is Public or not.

            Object lambda Access Points are private by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-policystatus.html#cfn-s3objectlambda-accesspoint-policystatus-ispublic
            '''
            result = self._values.get("is_public")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyStatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3objectlambda.mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_public_acls": "blockPublicAcls",
            "block_public_policy": "blockPublicPolicy",
            "ignore_public_acls": "ignorePublicAcls",
            "restrict_public_buckets": "restrictPublicBuckets",
        },
    )
    class PublicAccessBlockConfigurationProperty:
        def __init__(
            self,
            *,
            block_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            block_public_policy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The ``PublicAccessBlock`` configuration that you want to apply to this Amazon S3 account.

            You can enable the configuration options in any combination. For more information about when Amazon S3 considers a bucket or object public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .

            This data type is not supported for Amazon S3 on Outposts.

            :param block_public_acls: Specifies whether Amazon S3 should block public access control lists (ACLs) for buckets in this account. Setting this element to ``TRUE`` causes the following behavior: - ``PutBucketAcl`` and ``PutObjectAcl`` calls fail if the specified ACL is public. - PUT Object calls fail if the request includes a public ACL. - PUT Bucket calls fail if the request includes a public ACL. Enabling this setting doesn't affect existing policies or ACLs. This property is not supported for Amazon S3 on Outposts.
            :param block_public_policy: Specifies whether Amazon S3 should block public bucket policies for buckets in this account. Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access. Enabling this setting doesn't affect existing bucket policies. This property is not supported for Amazon S3 on Outposts.
            :param ignore_public_acls: Specifies whether Amazon S3 should ignore public ACLs for buckets in this account. Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on buckets in this account and any objects that they contain. Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set. This property is not supported for Amazon S3 on Outposts.
            :param restrict_public_buckets: Specifies whether Amazon S3 should restrict public bucket policies for buckets in this account. Setting this element to ``TRUE`` restricts access to buckets with public policies to only AWS service principals and authorized users within this account. Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked. This property is not supported for Amazon S3 on Outposts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3objectlambda import mixins as s3objectlambda_mixins
                
                public_access_block_configuration_property = s3objectlambda_mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbca66c5f9778d7114c564bba8aa1dacda7a662e202d530b0fb864099a726760)
                check_type(argname="argument block_public_acls", value=block_public_acls, expected_type=type_hints["block_public_acls"])
                check_type(argname="argument block_public_policy", value=block_public_policy, expected_type=type_hints["block_public_policy"])
                check_type(argname="argument ignore_public_acls", value=ignore_public_acls, expected_type=type_hints["ignore_public_acls"])
                check_type(argname="argument restrict_public_buckets", value=restrict_public_buckets, expected_type=type_hints["restrict_public_buckets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block_public_acls is not None:
                self._values["block_public_acls"] = block_public_acls
            if block_public_policy is not None:
                self._values["block_public_policy"] = block_public_policy
            if ignore_public_acls is not None:
                self._values["ignore_public_acls"] = ignore_public_acls
            if restrict_public_buckets is not None:
                self._values["restrict_public_buckets"] = restrict_public_buckets

        @builtins.property
        def block_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should block public access control lists (ACLs) for buckets in this account.

            Setting this element to ``TRUE`` causes the following behavior:

            - ``PutBucketAcl`` and ``PutObjectAcl`` calls fail if the specified ACL is public.
            - PUT Object calls fail if the request includes a public ACL.
            - PUT Bucket calls fail if the request includes a public ACL.

            Enabling this setting doesn't affect existing policies or ACLs.

            This property is not supported for Amazon S3 on Outposts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html#cfn-s3objectlambda-accesspoint-publicaccessblockconfiguration-blockpublicacls
            '''
            result = self._values.get("block_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def block_public_policy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should block public bucket policies for buckets in this account.

            Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access.

            Enabling this setting doesn't affect existing bucket policies.

            This property is not supported for Amazon S3 on Outposts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html#cfn-s3objectlambda-accesspoint-publicaccessblockconfiguration-blockpublicpolicy
            '''
            result = self._values.get("block_public_policy")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ignore_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should ignore public ACLs for buckets in this account.

            Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on buckets in this account and any objects that they contain.

            Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.

            This property is not supported for Amazon S3 on Outposts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html#cfn-s3objectlambda-accesspoint-publicaccessblockconfiguration-ignorepublicacls
            '''
            result = self._values.get("ignore_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def restrict_public_buckets(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should restrict public bucket policies for buckets in this account.

            Setting this element to ``TRUE`` restricts access to buckets with public policies to only AWS service principals and authorized users within this account.

            Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            This property is not supported for Amazon S3 on Outposts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html#cfn-s3objectlambda-accesspoint-publicaccessblockconfiguration-restrictpublicbuckets
            '''
            result = self._values.get("restrict_public_buckets")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicAccessBlockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3objectlambda.mixins.CfnAccessPointPropsMixin.TransformationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "content_transformation": "contentTransformation",
        },
    )
    class TransformationConfigurationProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            content_transformation: typing.Any = None,
        ) -> None:
            '''A configuration used when creating an Object Lambda Access Point transformation.

            :param actions: A container for the action of an Object Lambda Access Point configuration. Valid inputs are ``GetObject`` , ``HeadObject`` , ``ListObject`` , and ``ListObjectV2`` .
            :param content_transformation: A container for the content transformation of an Object Lambda Access Point configuration. Can include the FunctionArn and FunctionPayload. For more information, see `AwsLambdaTransformation <https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_AwsLambdaTransformation.html>`_ in the *Amazon S3 API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-transformationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3objectlambda import mixins as s3objectlambda_mixins
                
                # content_transformation: Any
                
                transformation_configuration_property = s3objectlambda_mixins.CfnAccessPointPropsMixin.TransformationConfigurationProperty(
                    actions=["actions"],
                    content_transformation=content_transformation
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3bd83e8c8e6186bdf579f03ea358836d643f011e9240eaf405febf3bf762a8f1)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument content_transformation", value=content_transformation, expected_type=type_hints["content_transformation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if content_transformation is not None:
                self._values["content_transformation"] = content_transformation

        @builtins.property
        def actions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A container for the action of an Object Lambda Access Point configuration.

            Valid inputs are ``GetObject`` , ``HeadObject`` , ``ListObject`` , and ``ListObjectV2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-transformationconfiguration.html#cfn-s3objectlambda-accesspoint-transformationconfiguration-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def content_transformation(self) -> typing.Any:
            '''A container for the content transformation of an Object Lambda Access Point configuration.

            Can include the FunctionArn and FunctionPayload. For more information, see `AwsLambdaTransformation <https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_AwsLambdaTransformation.html>`_ in the *Amazon S3 API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-transformationconfiguration.html#cfn-s3objectlambda-accesspoint-transformationconfiguration-contenttransformation
            '''
            result = self._values.get("content_transformation")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransformationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAccessPointMixinProps",
    "CfnAccessPointPolicyMixinProps",
    "CfnAccessPointPolicyPropsMixin",
    "CfnAccessPointPropsMixin",
]

publication.publish()

def _typecheckingstub__4d12fc88639a02f4b99d16005bb9647cb776dec48470480f0b22723a73ac7b0e(
    *,
    name: typing.Optional[builtins.str] = None,
    object_lambda_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPointPropsMixin.ObjectLambdaConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6604ef720099cc441b98711cd4c9820d0317c57f2bce60bc6b116192df0d14ca(
    *,
    object_lambda_access_point: typing.Optional[builtins.str] = None,
    policy_document: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ad71efe82045c67cf0afb31f6076567d828ca0ed863a1d5687b9b0c028ea3f(
    props: typing.Union[CfnAccessPointPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c21f6b3c86f818d1e5f9690e8517b533e83ef1e96b3478f70e9fbbafb0e7bc0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769af0ac5681ee4a69df7dd2a4ae494f89d897e645bcd9943a4b52cd5689afc7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b1f3b492cbd7bb691ebf7083619c9dbf58702de604f93ae4133d223870874e(
    props: typing.Union[CfnAccessPointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32f28332e2df7c03e026a90b8c4a8323d8cb2859ae09c9096eee2b86f698eab(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c661eddda7aa178a4caf4ab950123f61467634ddd8c1124301848d58d7ab303a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cf740286ddb648c985061aadaf777da73f1f5f9152f3ced4d41e6a7e4da417(
    *,
    status: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77df052814f96237855dbe7fc7a0dc13e7e8d4f8801a0b47573828acd52852ce(
    *,
    allowed_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    supporting_access_point: typing.Optional[builtins.str] = None,
    transformation_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPointPropsMixin.TransformationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bda2c18b1ce79a913e296fcf1c7525448e724b6adca4668a983f52fabe1d216(
    *,
    is_public: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbca66c5f9778d7114c564bba8aa1dacda7a662e202d530b0fb864099a726760(
    *,
    block_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    block_public_policy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd83e8c8e6186bdf579f03ea358836d643f011e9240eaf405febf3bf762a8f1(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    content_transformation: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
