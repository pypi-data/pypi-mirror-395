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
    jsii_type="@aws-cdk/mixins-preview.aws_mediastore.mixins.CfnContainerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_logging_enabled": "accessLoggingEnabled",
        "container_name": "containerName",
        "cors_policy": "corsPolicy",
        "lifecycle_policy": "lifecyclePolicy",
        "metric_policy": "metricPolicy",
        "policy": "policy",
        "tags": "tags",
    },
)
class CfnContainerMixinProps:
    def __init__(
        self,
        *,
        access_logging_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        container_name: typing.Optional[builtins.str] = None,
        cors_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.CorsRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        lifecycle_policy: typing.Optional[builtins.str] = None,
        metric_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.MetricPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        policy: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnContainerPropsMixin.

        :param access_logging_enabled: The state of access logging on the container. This value is ``false`` by default, indicating that AWS Elemental MediaStore does not send access logs to Amazon CloudWatch Logs. When you enable access logging on the container, MediaStore changes this value to ``true`` , indicating that the service delivers access logs for objects stored in that container to CloudWatch Logs.
        :param container_name: The name for the container. The name must be from 1 to 255 characters. Container names must be unique to your AWS account within a specific region. As an example, you could create a container named ``movies`` in every region, as long as you don’t have an existing container with that name.
        :param cors_policy: .. epigraph:: End of support notice: On November 13, 2025, AWS will discontinue support for AWS Elemental MediaStore. After November 13, 2025, you will no longer be able to access the AWS Elemental MediaStore console or AWS Elemental MediaStore resources. For more information, visit this `blog post <https://docs.aws.amazon.com/media/support-for-aws-elemental-mediastore-ending-soon/>`_ . Sets the cross-origin resource sharing (CORS) configuration on a container so that the container can service cross-origin requests. For example, you might want to enable a request whose origin is http://www.example.com to access your AWS Elemental MediaStore container at my.example.container.com by using the browser's XMLHttpRequest capability. To enable CORS on a container, you attach a CORS policy to the container. In the CORS policy, you configure rules that identify origins and the HTTP methods that can be executed on your container. The policy can contain up to 398,000 characters. You can add up to 100 rules to a CORS policy. If more than one rule applies, the service uses the first applicable rule listed. To learn more about CORS, see `Cross-Origin Resource Sharing (CORS) in AWS Elemental MediaStore <https://docs.aws.amazon.com/mediastore/latest/ug/cors-policy.html>`_ .
        :param lifecycle_policy: .. epigraph:: End of support notice: On November 13, 2025, AWS will discontinue support for AWS Elemental MediaStore. After November 13, 2025, you will no longer be able to access the AWS Elemental MediaStore console or AWS Elemental MediaStore resources. For more information, visit this `blog post <https://docs.aws.amazon.com/media/support-for-aws-elemental-mediastore-ending-soon/>`_ . Writes an object lifecycle policy to a container. If the container already has an object lifecycle policy, the service replaces the existing policy with the new policy. It takes up to 20 minutes for the change to take effect. For information about how to construct an object lifecycle policy, see `Components of an Object Lifecycle Policy <https://docs.aws.amazon.com/mediastore/latest/ug/policies-object-lifecycle-components.html>`_ .
        :param metric_policy: The metric policy that is associated with the container. A metric policy allows AWS Elemental MediaStore to send metrics to Amazon CloudWatch. In the policy, you must indicate whether you want MediaStore to send container-level metrics. You can also include rules to define groups of objects that you want MediaStore to send object-level metrics for. To view examples of how to construct a metric policy for your use case, see `Example Metric Policies <https://docs.aws.amazon.com/mediastore/latest/ug/policies-metric-examples.html>`_ .
        :param policy: Creates an access policy for the specified container to restrict the users and clients that can access it. For information about the data that is included in an access policy, see the `AWS Identity and Access Management User Guide <https://docs.aws.amazon.com/iam/>`_ . For this release of the REST API, you can create only one policy for a container. If you enter ``PutContainerPolicy`` twice, the second command modifies the existing policy.
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mediastore import mixins as mediastore_mixins
            
            cfn_container_mixin_props = mediastore_mixins.CfnContainerMixinProps(
                access_logging_enabled=False,
                container_name="containerName",
                cors_policy=[mediastore_mixins.CfnContainerPropsMixin.CorsRuleProperty(
                    allowed_headers=["allowedHeaders"],
                    allowed_methods=["allowedMethods"],
                    allowed_origins=["allowedOrigins"],
                    expose_headers=["exposeHeaders"],
                    max_age_seconds=123
                )],
                lifecycle_policy="lifecyclePolicy",
                metric_policy=mediastore_mixins.CfnContainerPropsMixin.MetricPolicyProperty(
                    container_level_metrics="containerLevelMetrics",
                    metric_policy_rules=[mediastore_mixins.CfnContainerPropsMixin.MetricPolicyRuleProperty(
                        object_group="objectGroup",
                        object_group_name="objectGroupName"
                    )]
                ),
                policy="policy",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af819abb7235bdf1f60881b435314bcb921cc6581a51611b3ef880e2e24a97de)
            check_type(argname="argument access_logging_enabled", value=access_logging_enabled, expected_type=type_hints["access_logging_enabled"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument cors_policy", value=cors_policy, expected_type=type_hints["cors_policy"])
            check_type(argname="argument lifecycle_policy", value=lifecycle_policy, expected_type=type_hints["lifecycle_policy"])
            check_type(argname="argument metric_policy", value=metric_policy, expected_type=type_hints["metric_policy"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_logging_enabled is not None:
            self._values["access_logging_enabled"] = access_logging_enabled
        if container_name is not None:
            self._values["container_name"] = container_name
        if cors_policy is not None:
            self._values["cors_policy"] = cors_policy
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if metric_policy is not None:
            self._values["metric_policy"] = metric_policy
        if policy is not None:
            self._values["policy"] = policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The state of access logging on the container.

        This value is ``false`` by default, indicating that AWS Elemental MediaStore does not send access logs to Amazon CloudWatch Logs. When you enable access logging on the container, MediaStore changes this value to ``true`` , indicating that the service delivers access logs for objects stored in that container to CloudWatch Logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-accessloggingenabled
        '''
        result = self._values.get("access_logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''The name for the container.

        The name must be from 1 to 255 characters. Container names must be unique to your AWS account within a specific region. As an example, you could create a container named ``movies`` in every region, as long as you don’t have an existing container with that name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-containername
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.CorsRuleProperty"]]]]:
        '''.. epigraph::

   End of support notice: On November 13, 2025, AWS will discontinue support for AWS Elemental MediaStore.

        After November 13, 2025, you will no longer be able to access the AWS Elemental MediaStore console or AWS Elemental MediaStore resources. For more information, visit this `blog post <https://docs.aws.amazon.com/media/support-for-aws-elemental-mediastore-ending-soon/>`_ .

        Sets the cross-origin resource sharing (CORS) configuration on a container so that the container can service cross-origin requests. For example, you might want to enable a request whose origin is http://www.example.com to access your AWS Elemental MediaStore container at my.example.container.com by using the browser's XMLHttpRequest capability.

        To enable CORS on a container, you attach a CORS policy to the container. In the CORS policy, you configure rules that identify origins and the HTTP methods that can be executed on your container. The policy can contain up to 398,000 characters. You can add up to 100 rules to a CORS policy. If more than one rule applies, the service uses the first applicable rule listed.

        To learn more about CORS, see `Cross-Origin Resource Sharing (CORS) in AWS Elemental MediaStore <https://docs.aws.amazon.com/mediastore/latest/ug/cors-policy.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-corspolicy
        '''
        result = self._values.get("cors_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.CorsRuleProperty"]]]], result)

    @builtins.property
    def lifecycle_policy(self) -> typing.Optional[builtins.str]:
        '''.. epigraph::

   End of support notice: On November 13, 2025, AWS will discontinue support for AWS Elemental MediaStore.

        After November 13, 2025, you will no longer be able to access the AWS Elemental MediaStore console or AWS Elemental MediaStore resources. For more information, visit this `blog post <https://docs.aws.amazon.com/media/support-for-aws-elemental-mediastore-ending-soon/>`_ .

        Writes an object lifecycle policy to a container. If the container already has an object lifecycle policy, the service replaces the existing policy with the new policy. It takes up to 20 minutes for the change to take effect.

        For information about how to construct an object lifecycle policy, see `Components of an Object Lifecycle Policy <https://docs.aws.amazon.com/mediastore/latest/ug/policies-object-lifecycle-components.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-lifecyclepolicy
        '''
        result = self._values.get("lifecycle_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.MetricPolicyProperty"]]:
        '''The metric policy that is associated with the container.

        A metric policy allows AWS Elemental MediaStore to send metrics to Amazon CloudWatch. In the policy, you must indicate whether you want MediaStore to send container-level metrics. You can also include rules to define groups of objects that you want MediaStore to send object-level metrics for.

        To view examples of how to construct a metric policy for your use case, see `Example Metric Policies <https://docs.aws.amazon.com/mediastore/latest/ug/policies-metric-examples.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-metricpolicy
        '''
        result = self._values.get("metric_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.MetricPolicyProperty"]], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''Creates an access policy for the specified container to restrict the users and clients that can access it.

        For information about the data that is included in an access policy, see the `AWS Identity and Access Management User Guide <https://docs.aws.amazon.com/iam/>`_ .

        For this release of the REST API, you can create only one policy for a container. If you enter ``PutContainerPolicy`` twice, the second command modifies the existing policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContainerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContainerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mediastore.mixins.CfnContainerPropsMixin",
):
    '''The AWS::MediaStore::Container resource specifies a storage container to hold objects.

    A container is similar to a bucket in Amazon S3.

    When you create a container using CloudFormation , the template manages data for five API actions: creating a container, setting access logging, updating the default container policy, adding a cross-origin resource sharing (CORS) policy, and adding an object lifecycle policy.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html
    :cloudformationResource: AWS::MediaStore::Container
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mediastore import mixins as mediastore_mixins
        
        cfn_container_props_mixin = mediastore_mixins.CfnContainerPropsMixin(mediastore_mixins.CfnContainerMixinProps(
            access_logging_enabled=False,
            container_name="containerName",
            cors_policy=[mediastore_mixins.CfnContainerPropsMixin.CorsRuleProperty(
                allowed_headers=["allowedHeaders"],
                allowed_methods=["allowedMethods"],
                allowed_origins=["allowedOrigins"],
                expose_headers=["exposeHeaders"],
                max_age_seconds=123
            )],
            lifecycle_policy="lifecyclePolicy",
            metric_policy=mediastore_mixins.CfnContainerPropsMixin.MetricPolicyProperty(
                container_level_metrics="containerLevelMetrics",
                metric_policy_rules=[mediastore_mixins.CfnContainerPropsMixin.MetricPolicyRuleProperty(
                    object_group="objectGroup",
                    object_group_name="objectGroupName"
                )]
            ),
            policy="policy",
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
        props: typing.Union[CfnContainerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MediaStore::Container``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924bcc5cd0dc969cda2b2611cdde22e9b2e2adba18c29cf23828659c997469fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7432ca495365861e690fdde66241ca49641f675f3f3b07b7badb26b3717b640e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05c76c985ca1dc826c9b8f253fc5dcdbccb3a9c7ffae5c3a3e6aa1f7bb26603)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContainerMixinProps:
        return typing.cast(CfnContainerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediastore.mixins.CfnContainerPropsMixin.CorsRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_headers": "allowedHeaders",
            "allowed_methods": "allowedMethods",
            "allowed_origins": "allowedOrigins",
            "expose_headers": "exposeHeaders",
            "max_age_seconds": "maxAgeSeconds",
        },
    )
    class CorsRuleProperty:
        def __init__(
            self,
            *,
            allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
            expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_age_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A rule for a CORS policy.

            You can add up to 100 rules to a CORS policy. If more than one rule applies, the service uses the first applicable rule listed.

            :param allowed_headers: Specifies which headers are allowed in a preflight ``OPTIONS`` request through the ``Access-Control-Request-Headers`` header. Each header name that is specified in ``Access-Control-Request-Headers`` must have a corresponding entry in the rule. Only the headers that were requested are sent back. This element can contain only one wildcard character (*).
            :param allowed_methods: Identifies an HTTP method that the origin that is specified in the rule is allowed to execute. Each CORS rule must contain at least one ``AllowedMethods`` and one ``AllowedOrigins`` element.
            :param allowed_origins: One or more response headers that you want users to be able to access from their applications (for example, from a JavaScript ``XMLHttpRequest`` object). Each CORS rule must have at least one ``AllowedOrigins`` element. The string value can include only one wildcard character (*), for example, http://*.example.com. Additionally, you can specify only one wildcard character to allow cross-origin access for all origins.
            :param expose_headers: One or more headers in the response that you want users to be able to access from their applications (for example, from a JavaScript ``XMLHttpRequest`` object). This element is optional for each rule.
            :param max_age_seconds: The time in seconds that your browser caches the preflight response for the specified resource. A CORS rule can have only one ``MaxAgeSeconds`` element.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediastore import mixins as mediastore_mixins
                
                cors_rule_property = mediastore_mixins.CfnContainerPropsMixin.CorsRuleProperty(
                    allowed_headers=["allowedHeaders"],
                    allowed_methods=["allowedMethods"],
                    allowed_origins=["allowedOrigins"],
                    expose_headers=["exposeHeaders"],
                    max_age_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ffe8a3cf99cb31e6d036adaf1b7b17eabfdbcd36769777a3fd7a92f07d9f463f)
                check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
                check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
                check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
                check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
                check_type(argname="argument max_age_seconds", value=max_age_seconds, expected_type=type_hints["max_age_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_headers is not None:
                self._values["allowed_headers"] = allowed_headers
            if allowed_methods is not None:
                self._values["allowed_methods"] = allowed_methods
            if allowed_origins is not None:
                self._values["allowed_origins"] = allowed_origins
            if expose_headers is not None:
                self._values["expose_headers"] = expose_headers
            if max_age_seconds is not None:
                self._values["max_age_seconds"] = max_age_seconds

        @builtins.property
        def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies which headers are allowed in a preflight ``OPTIONS`` request through the ``Access-Control-Request-Headers`` header.

            Each header name that is specified in ``Access-Control-Request-Headers`` must have a corresponding entry in the rule. Only the headers that were requested are sent back.

            This element can contain only one wildcard character (*).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-allowedheaders
            '''
            result = self._values.get("allowed_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Identifies an HTTP method that the origin that is specified in the rule is allowed to execute.

            Each CORS rule must contain at least one ``AllowedMethods`` and one ``AllowedOrigins`` element.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-allowedmethods
            '''
            result = self._values.get("allowed_methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more response headers that you want users to be able to access from their applications (for example, from a JavaScript ``XMLHttpRequest`` object).

            Each CORS rule must have at least one ``AllowedOrigins`` element. The string value can include only one wildcard character (*), for example, http://*.example.com. Additionally, you can specify only one wildcard character to allow cross-origin access for all origins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-allowedorigins
            '''
            result = self._values.get("allowed_origins")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more headers in the response that you want users to be able to access from their applications (for example, from a JavaScript ``XMLHttpRequest`` object).

            This element is optional for each rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-exposeheaders
            '''
            result = self._values.get("expose_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_age_seconds(self) -> typing.Optional[jsii.Number]:
            '''The time in seconds that your browser caches the preflight response for the specified resource.

            A CORS rule can have only one ``MaxAgeSeconds`` element.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-maxageseconds
            '''
            result = self._values.get("max_age_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediastore.mixins.CfnContainerPropsMixin.MetricPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_level_metrics": "containerLevelMetrics",
            "metric_policy_rules": "metricPolicyRules",
        },
    )
    class MetricPolicyProperty:
        def __init__(
            self,
            *,
            container_level_metrics: typing.Optional[builtins.str] = None,
            metric_policy_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.MetricPolicyRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The metric policy that is associated with the container.

            A metric policy allows AWS Elemental MediaStore to send metrics to Amazon CloudWatch. In the policy, you must indicate whether you want MediaStore to send container-level metrics. You can also include rules to define groups of objects that you want MediaStore to send object-level metrics for.

            To view examples of how to construct a metric policy for your use case, see `Example Metric Policies <https://docs.aws.amazon.com/mediastore/latest/ug/policies-metric-examples.html>`_ .

            :param container_level_metrics: A setting to enable or disable metrics at the container level.
            :param metric_policy_rules: A parameter that holds an array of rules that enable metrics at the object level. This parameter is optional, but if you choose to include it, you must also include at least one rule. By default, you can include up to five rules. You can also `request a quota increase <https://docs.aws.amazon.com/servicequotas/home?region=us-east-1#!/services/mediastore/quotas>`_ to allow up to 300 rules per policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediastore import mixins as mediastore_mixins
                
                metric_policy_property = mediastore_mixins.CfnContainerPropsMixin.MetricPolicyProperty(
                    container_level_metrics="containerLevelMetrics",
                    metric_policy_rules=[mediastore_mixins.CfnContainerPropsMixin.MetricPolicyRuleProperty(
                        object_group="objectGroup",
                        object_group_name="objectGroupName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc1629c11d7c3b5f1819660d350a22950a310bdf7c345b7392dbef6f8561cd7c)
                check_type(argname="argument container_level_metrics", value=container_level_metrics, expected_type=type_hints["container_level_metrics"])
                check_type(argname="argument metric_policy_rules", value=metric_policy_rules, expected_type=type_hints["metric_policy_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_level_metrics is not None:
                self._values["container_level_metrics"] = container_level_metrics
            if metric_policy_rules is not None:
                self._values["metric_policy_rules"] = metric_policy_rules

        @builtins.property
        def container_level_metrics(self) -> typing.Optional[builtins.str]:
            '''A setting to enable or disable metrics at the container level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicy.html#cfn-mediastore-container-metricpolicy-containerlevelmetrics
            '''
            result = self._values.get("container_level_metrics")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_policy_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.MetricPolicyRuleProperty"]]]]:
            '''A parameter that holds an array of rules that enable metrics at the object level.

            This parameter is optional, but if you choose to include it, you must also include at least one rule. By default, you can include up to five rules. You can also `request a quota increase <https://docs.aws.amazon.com/servicequotas/home?region=us-east-1#!/services/mediastore/quotas>`_ to allow up to 300 rules per policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicy.html#cfn-mediastore-container-metricpolicy-metricpolicyrules
            '''
            result = self._values.get("metric_policy_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.MetricPolicyRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mediastore.mixins.CfnContainerPropsMixin.MetricPolicyRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object_group": "objectGroup",
            "object_group_name": "objectGroupName",
        },
    )
    class MetricPolicyRuleProperty:
        def __init__(
            self,
            *,
            object_group: typing.Optional[builtins.str] = None,
            object_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A setting that enables metrics at the object level.

            Each rule contains an object group and an object group name. If the policy includes the MetricPolicyRules parameter, you must include at least one rule. Each metric policy can include up to five rules by default. You can also `request a quota increase <https://docs.aws.amazon.com/servicequotas/home?region=us-east-1#!/services/mediastore/quotas>`_ to allow up to 300 rules per policy.

            :param object_group: A path or file name that defines which objects to include in the group. Wildcards (*) are acceptable.
            :param object_group_name: A name that allows you to refer to the object group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicyrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mediastore import mixins as mediastore_mixins
                
                metric_policy_rule_property = mediastore_mixins.CfnContainerPropsMixin.MetricPolicyRuleProperty(
                    object_group="objectGroup",
                    object_group_name="objectGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__721b6b17c266cb8a752bdc166f74534be65025410089c8cb84a7963fbb265f74)
                check_type(argname="argument object_group", value=object_group, expected_type=type_hints["object_group"])
                check_type(argname="argument object_group_name", value=object_group_name, expected_type=type_hints["object_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object_group is not None:
                self._values["object_group"] = object_group
            if object_group_name is not None:
                self._values["object_group_name"] = object_group_name

        @builtins.property
        def object_group(self) -> typing.Optional[builtins.str]:
            '''A path or file name that defines which objects to include in the group.

            Wildcards (*) are acceptable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicyrule.html#cfn-mediastore-container-metricpolicyrule-objectgroup
            '''
            result = self._values.get("object_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_group_name(self) -> typing.Optional[builtins.str]:
            '''A name that allows you to refer to the object group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicyrule.html#cfn-mediastore-container-metricpolicyrule-objectgroupname
            '''
            result = self._values.get("object_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricPolicyRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnContainerMixinProps",
    "CfnContainerPropsMixin",
]

publication.publish()

def _typecheckingstub__af819abb7235bdf1f60881b435314bcb921cc6581a51611b3ef880e2e24a97de(
    *,
    access_logging_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    container_name: typing.Optional[builtins.str] = None,
    cors_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.CorsRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lifecycle_policy: typing.Optional[builtins.str] = None,
    metric_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.MetricPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924bcc5cd0dc969cda2b2611cdde22e9b2e2adba18c29cf23828659c997469fe(
    props: typing.Union[CfnContainerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7432ca495365861e690fdde66241ca49641f675f3f3b07b7badb26b3717b640e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05c76c985ca1dc826c9b8f253fc5dcdbccb3a9c7ffae5c3a3e6aa1f7bb26603(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe8a3cf99cb31e6d036adaf1b7b17eabfdbcd36769777a3fd7a92f07d9f463f(
    *,
    allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1629c11d7c3b5f1819660d350a22950a310bdf7c345b7392dbef6f8561cd7c(
    *,
    container_level_metrics: typing.Optional[builtins.str] = None,
    metric_policy_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.MetricPolicyRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721b6b17c266cb8a752bdc166f74534be65025410089c8cb84a7963fbb265f74(
    *,
    object_group: typing.Optional[builtins.str] = None,
    object_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
