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
    jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "description": "description",
        "resource_lifecycle_config": "resourceLifecycleConfig",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        resource_lifecycle_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationResourceLifecycleConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param application_name: A name for the Elastic Beanstalk application. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param description: Your description of the application.
        :param resource_lifecycle_config: Specifies an application resource lifecycle configuration to prevent your application from accumulating too many versions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
            
            cfn_application_mixin_props = elasticbeanstalk_mixins.CfnApplicationMixinProps(
                application_name="applicationName",
                description="description",
                resource_lifecycle_config=elasticbeanstalk_mixins.CfnApplicationPropsMixin.ApplicationResourceLifecycleConfigProperty(
                    service_role="serviceRole",
                    version_lifecycle_config=elasticbeanstalk_mixins.CfnApplicationPropsMixin.ApplicationVersionLifecycleConfigProperty(
                        max_age_rule=elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxAgeRuleProperty(
                            delete_source_from_s3=False,
                            enabled=False,
                            max_age_in_days=123
                        ),
                        max_count_rule=elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxCountRuleProperty(
                            delete_source_from_s3=False,
                            enabled=False,
                            max_count=123
                        )
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144d9037afc3bec5fe1f04e6b86efdcb8f9a410cc8c1753c5cbd3f506c602ee4)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument resource_lifecycle_config", value=resource_lifecycle_config, expected_type=type_hints["resource_lifecycle_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if description is not None:
            self._values["description"] = description
        if resource_lifecycle_config is not None:
            self._values["resource_lifecycle_config"] = resource_lifecycle_config

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''A name for the Elastic Beanstalk application.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html#cfn-elasticbeanstalk-application-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Your description of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html#cfn-elasticbeanstalk-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_lifecycle_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationResourceLifecycleConfigProperty"]]:
        '''Specifies an application resource lifecycle configuration to prevent your application from accumulating too many versions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html#cfn-elasticbeanstalk-application-resourcelifecycleconfig
        '''
        result = self._values.get("resource_lifecycle_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationResourceLifecycleConfigProperty"]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnApplicationPropsMixin",
):
    '''Specify an AWS Elastic Beanstalk application by using the AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

    The AWS::ElasticBeanstalk::Application resource is an AWS Elastic Beanstalk Beanstalk resource type that specifies an Elastic Beanstalk application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html
    :cloudformationResource: AWS::ElasticBeanstalk::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
        
        cfn_application_props_mixin = elasticbeanstalk_mixins.CfnApplicationPropsMixin(elasticbeanstalk_mixins.CfnApplicationMixinProps(
            application_name="applicationName",
            description="description",
            resource_lifecycle_config=elasticbeanstalk_mixins.CfnApplicationPropsMixin.ApplicationResourceLifecycleConfigProperty(
                service_role="serviceRole",
                version_lifecycle_config=elasticbeanstalk_mixins.CfnApplicationPropsMixin.ApplicationVersionLifecycleConfigProperty(
                    max_age_rule=elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxAgeRuleProperty(
                        delete_source_from_s3=False,
                        enabled=False,
                        max_age_in_days=123
                    ),
                    max_count_rule=elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxCountRuleProperty(
                        delete_source_from_s3=False,
                        enabled=False,
                        max_count=123
                    )
                )
            )
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
        '''Create a mixin to apply properties to ``AWS::ElasticBeanstalk::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd405a1febef9decf4409c3edf11e92f143b8ec7aa53e6556bbd33baa423acb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58140f6ba35acaaf2259bc7814d195f4e5a6e4682d2914b4d99d5caad758bf58)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e61c3aebf2ab4946590131d80c80f41fc26e0c118306857a8499f63a3c628d8)
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
        jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnApplicationPropsMixin.ApplicationResourceLifecycleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "service_role": "serviceRole",
            "version_lifecycle_config": "versionLifecycleConfig",
        },
    )
    class ApplicationResourceLifecycleConfigProperty:
        def __init__(
            self,
            *,
            service_role: typing.Optional[builtins.str] = None,
            version_lifecycle_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ApplicationVersionLifecycleConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Use the ``ApplicationResourceLifecycleConfig`` property type to specify lifecycle settings for resources that belong to an AWS Elastic Beanstalk application when defining an AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

            The resource lifecycle configuration for an application. Defines lifecycle settings for resources that belong to the application, and the service role that Elastic Beanstalk assumes in order to apply lifecycle settings. The version lifecycle configuration defines lifecycle settings for application versions.

            ``ApplicationResourceLifecycleConfig`` is a property of the `AWS::ElasticBeanstalk::Application <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html>`_ resource.

            :param service_role: The ARN of an IAM service role that Elastic Beanstalk has permission to assume. The ``ServiceRole`` property is required the first time that you provide a ``ResourceLifecycleConfig`` for the application. After you provide it once, Elastic Beanstalk persists the Service Role with the application, and you don't need to specify it again. You can, however, specify it in subsequent updates to change the Service Role to another value.
            :param version_lifecycle_config: Defines lifecycle settings for application versions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
                
                application_resource_lifecycle_config_property = elasticbeanstalk_mixins.CfnApplicationPropsMixin.ApplicationResourceLifecycleConfigProperty(
                    service_role="serviceRole",
                    version_lifecycle_config=elasticbeanstalk_mixins.CfnApplicationPropsMixin.ApplicationVersionLifecycleConfigProperty(
                        max_age_rule=elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxAgeRuleProperty(
                            delete_source_from_s3=False,
                            enabled=False,
                            max_age_in_days=123
                        ),
                        max_count_rule=elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxCountRuleProperty(
                            delete_source_from_s3=False,
                            enabled=False,
                            max_count=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef1291b13f5bb927e819495f02f12bd4c873926de97aec8a314dacc34551d59b)
                check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
                check_type(argname="argument version_lifecycle_config", value=version_lifecycle_config, expected_type=type_hints["version_lifecycle_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if service_role is not None:
                self._values["service_role"] = service_role
            if version_lifecycle_config is not None:
                self._values["version_lifecycle_config"] = version_lifecycle_config

        @builtins.property
        def service_role(self) -> typing.Optional[builtins.str]:
            '''The ARN of an IAM service role that Elastic Beanstalk has permission to assume.

            The ``ServiceRole`` property is required the first time that you provide a ``ResourceLifecycleConfig`` for the application. After you provide it once, Elastic Beanstalk persists the Service Role with the application, and you don't need to specify it again. You can, however, specify it in subsequent updates to change the Service Role to another value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html#cfn-elasticbeanstalk-application-applicationresourcelifecycleconfig-servicerole
            '''
            result = self._values.get("service_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version_lifecycle_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationVersionLifecycleConfigProperty"]]:
            '''Defines lifecycle settings for application versions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html#cfn-elasticbeanstalk-application-applicationresourcelifecycleconfig-versionlifecycleconfig
            '''
            result = self._values.get("version_lifecycle_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ApplicationVersionLifecycleConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationResourceLifecycleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnApplicationPropsMixin.ApplicationVersionLifecycleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"max_age_rule": "maxAgeRule", "max_count_rule": "maxCountRule"},
    )
    class ApplicationVersionLifecycleConfigProperty:
        def __init__(
            self,
            *,
            max_age_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.MaxAgeRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            max_count_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.MaxCountRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Use the ``ApplicationVersionLifecycleConfig`` property type to specify application version lifecycle settings for an AWS Elastic Beanstalk application when defining an AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

            The application version lifecycle settings for an application. Defines the rules that Elastic Beanstalk applies to an application's versions in order to avoid hitting the per-region limit for application versions.

            When Elastic Beanstalk deletes an application version from its database, you can no longer deploy that version to an environment. The source bundle remains in S3 unless you configure the rule to delete it.

            ``ApplicationVersionLifecycleConfig`` is a property of the `ApplicationResourceLifecycleConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html>`_ property type.

            :param max_age_rule: Specify a max age rule to restrict the length of time that application versions are retained for an application.
            :param max_count_rule: Specify a max count rule to restrict the number of application versions that are retained for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
                
                application_version_lifecycle_config_property = elasticbeanstalk_mixins.CfnApplicationPropsMixin.ApplicationVersionLifecycleConfigProperty(
                    max_age_rule=elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxAgeRuleProperty(
                        delete_source_from_s3=False,
                        enabled=False,
                        max_age_in_days=123
                    ),
                    max_count_rule=elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxCountRuleProperty(
                        delete_source_from_s3=False,
                        enabled=False,
                        max_count=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19467cad0e422a8f524d5cd3f8fcdc0145842f46b61e0e6590b0bab6fbb509e8)
                check_type(argname="argument max_age_rule", value=max_age_rule, expected_type=type_hints["max_age_rule"])
                check_type(argname="argument max_count_rule", value=max_count_rule, expected_type=type_hints["max_count_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_age_rule is not None:
                self._values["max_age_rule"] = max_age_rule
            if max_count_rule is not None:
                self._values["max_count_rule"] = max_count_rule

        @builtins.property
        def max_age_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MaxAgeRuleProperty"]]:
            '''Specify a max age rule to restrict the length of time that application versions are retained for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html#cfn-elasticbeanstalk-application-applicationversionlifecycleconfig-maxagerule
            '''
            result = self._values.get("max_age_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MaxAgeRuleProperty"]], result)

        @builtins.property
        def max_count_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MaxCountRuleProperty"]]:
            '''Specify a max count rule to restrict the number of application versions that are retained for an application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html#cfn-elasticbeanstalk-application-applicationversionlifecycleconfig-maxcountrule
            '''
            result = self._values.get("max_count_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MaxCountRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationVersionLifecycleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnApplicationPropsMixin.MaxAgeRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_source_from_s3": "deleteSourceFromS3",
            "enabled": "enabled",
            "max_age_in_days": "maxAgeInDays",
        },
    )
    class MaxAgeRuleProperty:
        def __init__(
            self,
            *,
            delete_source_from_s3: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_age_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Use the ``MaxAgeRule`` property type to specify a max age rule to restrict the length of time that application versions are retained for an AWS Elastic Beanstalk application when defining an AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

            A lifecycle rule that deletes application versions after the specified number of days.

            ``MaxAgeRule`` is a property of the `ApplicationVersionLifecycleConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html>`_ property type.

            :param delete_source_from_s3: Set to ``true`` to delete a version's source bundle from Amazon S3 when Elastic Beanstalk deletes the application version.
            :param enabled: Specify ``true`` to apply the rule, or ``false`` to disable it.
            :param max_age_in_days: Specify the number of days to retain an application versions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
                
                max_age_rule_property = elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxAgeRuleProperty(
                    delete_source_from_s3=False,
                    enabled=False,
                    max_age_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__342b4a31c8578eb19392cb0bf8da5db261be2f3aaa2657b2ac4fbdde6b1fc81f)
                check_type(argname="argument delete_source_from_s3", value=delete_source_from_s3, expected_type=type_hints["delete_source_from_s3"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument max_age_in_days", value=max_age_in_days, expected_type=type_hints["max_age_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_source_from_s3 is not None:
                self._values["delete_source_from_s3"] = delete_source_from_s3
            if enabled is not None:
                self._values["enabled"] = enabled
            if max_age_in_days is not None:
                self._values["max_age_in_days"] = max_age_in_days

        @builtins.property
        def delete_source_from_s3(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to ``true`` to delete a version's source bundle from Amazon S3 when Elastic Beanstalk deletes the application version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-deletesourcefroms3
            '''
            result = self._values.get("delete_source_from_s3")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify ``true`` to apply the rule, or ``false`` to disable it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_age_in_days(self) -> typing.Optional[jsii.Number]:
            '''Specify the number of days to retain an application versions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-maxageindays
            '''
            result = self._values.get("max_age_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaxAgeRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnApplicationPropsMixin.MaxCountRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_source_from_s3": "deleteSourceFromS3",
            "enabled": "enabled",
            "max_count": "maxCount",
        },
    )
    class MaxCountRuleProperty:
        def __init__(
            self,
            *,
            delete_source_from_s3: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Use the ``MaxAgeRule`` property type to specify a max count rule to restrict the number of application versions that are retained for an AWS Elastic Beanstalk application when defining an AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

            A lifecycle rule that deletes the oldest application version when the maximum count is exceeded.

            ``MaxCountRule`` is a property of the `ApplicationVersionLifecycleConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html>`_ property type.

            :param delete_source_from_s3: Set to ``true`` to delete a version's source bundle from Amazon S3 when Elastic Beanstalk deletes the application version.
            :param enabled: Specify ``true`` to apply the rule, or ``false`` to disable it.
            :param max_count: Specify the maximum number of application versions to retain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
                
                max_count_rule_property = elasticbeanstalk_mixins.CfnApplicationPropsMixin.MaxCountRuleProperty(
                    delete_source_from_s3=False,
                    enabled=False,
                    max_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f084097d6e3d2cce0454c7f73b4b5c3110b14611d9c4b0c516c8000743178b95)
                check_type(argname="argument delete_source_from_s3", value=delete_source_from_s3, expected_type=type_hints["delete_source_from_s3"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_source_from_s3 is not None:
                self._values["delete_source_from_s3"] = delete_source_from_s3
            if enabled is not None:
                self._values["enabled"] = enabled
            if max_count is not None:
                self._values["max_count"] = max_count

        @builtins.property
        def delete_source_from_s3(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set to ``true`` to delete a version's source bundle from Amazon S3 when Elastic Beanstalk deletes the application version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-deletesourcefroms3
            '''
            result = self._values.get("delete_source_from_s3")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify ``true`` to apply the rule, or ``false`` to disable it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_count(self) -> typing.Optional[jsii.Number]:
            '''Specify the maximum number of application versions to retain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-maxcount
            '''
            result = self._values.get("max_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaxCountRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnApplicationVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "description": "description",
        "source_bundle": "sourceBundle",
    },
)
class CfnApplicationVersionMixinProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        source_bundle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationVersionPropsMixin.SourceBundleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationVersionPropsMixin.

        :param application_name: The name of the Elastic Beanstalk application that is associated with this application version.
        :param description: A description of this application version.
        :param source_bundle: The Amazon S3 bucket and key that identify the location of the source bundle for this version. .. epigraph:: The Amazon S3 bucket must be in the same region as the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
            
            cfn_application_version_mixin_props = elasticbeanstalk_mixins.CfnApplicationVersionMixinProps(
                application_name="applicationName",
                description="description",
                source_bundle=elasticbeanstalk_mixins.CfnApplicationVersionPropsMixin.SourceBundleProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56bff1ff17c78b1a603cefdcdedd382116de4a4e2eeac225bebf6940dbf7d52)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument source_bundle", value=source_bundle, expected_type=type_hints["source_bundle"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if description is not None:
            self._values["description"] = description
        if source_bundle is not None:
            self._values["source_bundle"] = source_bundle

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Elastic Beanstalk application that is associated with this application version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html#cfn-elasticbeanstalk-applicationversion-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this application version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html#cfn-elasticbeanstalk-applicationversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_bundle(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationVersionPropsMixin.SourceBundleProperty"]]:
        '''The Amazon S3 bucket and key that identify the location of the source bundle for this version.

        .. epigraph::

           The Amazon S3 bucket must be in the same region as the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html#cfn-elasticbeanstalk-applicationversion-sourcebundle
        '''
        result = self._values.get("source_bundle")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationVersionPropsMixin.SourceBundleProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnApplicationVersionPropsMixin",
):
    '''Specify an AWS Elastic Beanstalk application version by using the AWS::ElasticBeanstalk::ApplicationVersion resource in an AWS CloudFormation template.

    The AWS::ElasticBeanstalk::ApplicationVersion resource is an AWS Elastic Beanstalk resource type that specifies an application version, an iteration of deployable code, for an Elastic Beanstalk application.
    .. epigraph::

       After you create an application version with a specified Amazon S3 bucket and key location, you can't change that Amazon S3 location. If you change the Amazon S3 location, an attempt to launch an environment from the application version will fail.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html
    :cloudformationResource: AWS::ElasticBeanstalk::ApplicationVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
        
        cfn_application_version_props_mixin = elasticbeanstalk_mixins.CfnApplicationVersionPropsMixin(elasticbeanstalk_mixins.CfnApplicationVersionMixinProps(
            application_name="applicationName",
            description="description",
            source_bundle=elasticbeanstalk_mixins.CfnApplicationVersionPropsMixin.SourceBundleProperty(
                s3_bucket="s3Bucket",
                s3_key="s3Key"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElasticBeanstalk::ApplicationVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6eb15715f07f81a3717c64d94590f61d8cf91bbb4f1358d1b477ecf141d81b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d9ea4f7b5831258e88f80799bac835fce9defc9f2f369e5dff83283fa518999)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d152289d2b2ea88b5c3853dd46b10318df8421e3064d0b32d61e2ffc63c0c4fb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationVersionMixinProps:
        return typing.cast(CfnApplicationVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnApplicationVersionPropsMixin.SourceBundleProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_key": "s3Key"},
    )
    class SourceBundleProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``SourceBundle`` property type to specify the Amazon S3 location of the source bundle for an AWS Elastic Beanstalk application version when defining an AWS::ElasticBeanstalk::ApplicationVersion resource in an AWS CloudFormation template.

            The ``SourceBundle`` property is an embedded property of the `AWS::ElasticBeanstalk::ApplicationVersion <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-sourcebundle.html>`_ resource. It specifies the Amazon S3 location of the source bundle for an AWS Elastic Beanstalk application version.

            :param s3_bucket: The Amazon S3 bucket where the data is located.
            :param s3_key: The Amazon S3 key where the data is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-applicationversion-sourcebundle.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
                
                source_bundle_property = elasticbeanstalk_mixins.CfnApplicationVersionPropsMixin.SourceBundleProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3cba9b0738d0637eae4c1ec38f9bc3fa8c7aa5d87bcab15b64560b43176c4a8)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket where the data is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-applicationversion-sourcebundle.html#cfn-elasticbeanstalk-applicationversion-sourcebundle-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 key where the data is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-applicationversion-sourcebundle.html#cfn-elasticbeanstalk-applicationversion-sourcebundle-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceBundleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnConfigurationTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "description": "description",
        "environment_id": "environmentId",
        "option_settings": "optionSettings",
        "platform_arn": "platformArn",
        "solution_stack_name": "solutionStackName",
        "source_configuration": "sourceConfiguration",
    },
)
class CfnConfigurationTemplateMixinProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        environment_id: typing.Optional[builtins.str] = None,
        option_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationTemplatePropsMixin.ConfigurationOptionSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        platform_arn: typing.Optional[builtins.str] = None,
        solution_stack_name: typing.Optional[builtins.str] = None,
        source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationTemplatePropsMixin.SourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConfigurationTemplatePropsMixin.

        :param application_name: The name of the Elastic Beanstalk application to associate with this configuration template.
        :param description: An optional description for this configuration.
        :param environment_id: The ID of an environment whose settings you want to use to create the configuration template. You must specify ``EnvironmentId`` if you don't specify ``PlatformArn`` , ``SolutionStackName`` , or ``SourceConfiguration`` .
        :param option_settings: Option values for the Elastic Beanstalk configuration, such as the instance type. If specified, these values override the values obtained from the solution stack or the source configuration template. For a complete list of Elastic Beanstalk configuration options, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
        :param platform_arn: The Amazon Resource Name (ARN) of the custom platform. For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . .. epigraph:: If you specify ``PlatformArn`` , then don't specify ``SolutionStackName`` .
        :param solution_stack_name: The name of an Elastic Beanstalk solution stack (platform version) that this configuration uses. For example, ``64bit Amazon Linux 2013.09 running Tomcat 7 Java 7`` . A solution stack specifies the operating system, runtime, and application server for a configuration template. It also determines the set of configuration options as well as the possible and default values. For more information, see `Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . You must specify ``SolutionStackName`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SourceConfiguration`` . Use the ```ListAvailableSolutionStacks`` <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_ListAvailableSolutionStacks.html>`_ API to obtain a list of available solution stacks.
        :param source_configuration: An Elastic Beanstalk configuration template to base this one on. If specified, Elastic Beanstalk uses the configuration values from the specified configuration template to create a new configuration. Values specified in ``OptionSettings`` override any values obtained from the ``SourceConfiguration`` . You must specify ``SourceConfiguration`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SolutionStackName`` . Constraint: If both solution stack name and source configuration are specified, the solution stack of the source configuration template must match the specified solution stack name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
            
            cfn_configuration_template_mixin_props = elasticbeanstalk_mixins.CfnConfigurationTemplateMixinProps(
                application_name="applicationName",
                description="description",
                environment_id="environmentId",
                option_settings=[elasticbeanstalk_mixins.CfnConfigurationTemplatePropsMixin.ConfigurationOptionSettingProperty(
                    namespace="namespace",
                    option_name="optionName",
                    resource_name="resourceName",
                    value="value"
                )],
                platform_arn="platformArn",
                solution_stack_name="solutionStackName",
                source_configuration=elasticbeanstalk_mixins.CfnConfigurationTemplatePropsMixin.SourceConfigurationProperty(
                    application_name="applicationName",
                    template_name="templateName"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58cc15e2735b4c3d918c7fe863b52d75389b4dc9eaa3ad7a6f25f1299c304d99)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_id", value=environment_id, expected_type=type_hints["environment_id"])
            check_type(argname="argument option_settings", value=option_settings, expected_type=type_hints["option_settings"])
            check_type(argname="argument platform_arn", value=platform_arn, expected_type=type_hints["platform_arn"])
            check_type(argname="argument solution_stack_name", value=solution_stack_name, expected_type=type_hints["solution_stack_name"])
            check_type(argname="argument source_configuration", value=source_configuration, expected_type=type_hints["source_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if description is not None:
            self._values["description"] = description
        if environment_id is not None:
            self._values["environment_id"] = environment_id
        if option_settings is not None:
            self._values["option_settings"] = option_settings
        if platform_arn is not None:
            self._values["platform_arn"] = platform_arn
        if solution_stack_name is not None:
            self._values["solution_stack_name"] = solution_stack_name
        if source_configuration is not None:
            self._values["source_configuration"] = source_configuration

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Elastic Beanstalk application to associate with this configuration template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an environment whose settings you want to use to create the configuration template.

        You must specify ``EnvironmentId`` if you don't specify ``PlatformArn`` , ``SolutionStackName`` , or ``SourceConfiguration`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-environmentid
        '''
        result = self._values.get("environment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationTemplatePropsMixin.ConfigurationOptionSettingProperty"]]]]:
        '''Option values for the Elastic Beanstalk configuration, such as the instance type.

        If specified, these values override the values obtained from the solution stack or the source configuration template. For a complete list of Elastic Beanstalk configuration options, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-optionsettings
        '''
        result = self._values.get("option_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationTemplatePropsMixin.ConfigurationOptionSettingProperty"]]]], result)

    @builtins.property
    def platform_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the custom platform.

        For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
        .. epigraph::

           If you specify ``PlatformArn`` , then don't specify ``SolutionStackName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-platformarn
        '''
        result = self._values.get("platform_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def solution_stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of an Elastic Beanstalk solution stack (platform version) that this configuration uses.

        For example, ``64bit Amazon Linux 2013.09 running Tomcat 7 Java 7`` . A solution stack specifies the operating system, runtime, and application server for a configuration template. It also determines the set of configuration options as well as the possible and default values. For more information, see `Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

        You must specify ``SolutionStackName`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SourceConfiguration`` .

        Use the ```ListAvailableSolutionStacks`` <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_ListAvailableSolutionStacks.html>`_ API to obtain a list of available solution stacks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-solutionstackname
        '''
        result = self._values.get("solution_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationTemplatePropsMixin.SourceConfigurationProperty"]]:
        '''An Elastic Beanstalk configuration template to base this one on.

        If specified, Elastic Beanstalk uses the configuration values from the specified configuration template to create a new configuration.

        Values specified in ``OptionSettings`` override any values obtained from the ``SourceConfiguration`` .

        You must specify ``SourceConfiguration`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SolutionStackName`` .

        Constraint: If both solution stack name and source configuration are specified, the solution stack of the source configuration template must match the specified solution stack name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration
        '''
        result = self._values.get("source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationTemplatePropsMixin.SourceConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConfigurationTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnConfigurationTemplatePropsMixin",
):
    '''Specify an AWS Elastic Beanstalk configuration template by using the AWS::ElasticBeanstalk::ConfigurationTemplate resource in an AWS CloudFormation template.

    The AWS::ElasticBeanstalk::ConfigurationTemplate resource is an AWS Elastic Beanstalk resource type that specifies an Elastic Beanstalk configuration template, associated with a specific Elastic Beanstalk application. You define application configuration settings in a configuration template. You can then use the configuration template to deploy different versions of the application with the same configuration settings.
    .. epigraph::

       The Elastic Beanstalk console and documentation often refer to configuration templates as *saved configurations* . When you set configuration options in a saved configuration (configuration template), Elastic Beanstalk applies them with a particular precedence as part of applying options from multiple sources. For more information, see `Configuration Options <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html
    :cloudformationResource: AWS::ElasticBeanstalk::ConfigurationTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
        
        cfn_configuration_template_props_mixin = elasticbeanstalk_mixins.CfnConfigurationTemplatePropsMixin(elasticbeanstalk_mixins.CfnConfigurationTemplateMixinProps(
            application_name="applicationName",
            description="description",
            environment_id="environmentId",
            option_settings=[elasticbeanstalk_mixins.CfnConfigurationTemplatePropsMixin.ConfigurationOptionSettingProperty(
                namespace="namespace",
                option_name="optionName",
                resource_name="resourceName",
                value="value"
            )],
            platform_arn="platformArn",
            solution_stack_name="solutionStackName",
            source_configuration=elasticbeanstalk_mixins.CfnConfigurationTemplatePropsMixin.SourceConfigurationProperty(
                application_name="applicationName",
                template_name="templateName"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConfigurationTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElasticBeanstalk::ConfigurationTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba38b30bdb9afd65db334753f0d856ff44b19412390cc999f77bc9e9522fb3ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5673a74dda0c3f4f14c8713fab60a7357dcfa220f84a1064929db50d81f2df84)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6918f04e24722c62e8ed3bdbc5593b2355eb1aa9bdab8a6187831d60d19e33d2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConfigurationTemplateMixinProps:
        return typing.cast(CfnConfigurationTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnConfigurationTemplatePropsMixin.ConfigurationOptionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "namespace": "namespace",
            "option_name": "optionName",
            "resource_name": "resourceName",
            "value": "value",
        },
    )
    class ConfigurationOptionSettingProperty:
        def __init__(
            self,
            *,
            namespace: typing.Optional[builtins.str] = None,
            option_name: typing.Optional[builtins.str] = None,
            resource_name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``ConfigurationOptionSetting`` property type to specify an option for an AWS Elastic Beanstalk configuration template when defining an AWS::ElasticBeanstalk::ConfigurationTemplate resource in an AWS CloudFormation template.

            The ``ConfigurationOptionSetting`` property type specifies an option for an AWS Elastic Beanstalk configuration template.

            The ``OptionSettings`` property of the `AWS::ElasticBeanstalk::ConfigurationTemplate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ resource contains a list of ``ConfigurationOptionSetting`` property types.

            For a list of possible namespaces and option values, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

            :param namespace: A unique namespace that identifies the option's associated AWS resource.
            :param option_name: The name of the configuration option.
            :param resource_name: A unique resource name for the option setting. Use it for a time–based scaling configuration option.
            :param value: The current value for the configuration option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
                
                configuration_option_setting_property = elasticbeanstalk_mixins.CfnConfigurationTemplatePropsMixin.ConfigurationOptionSettingProperty(
                    namespace="namespace",
                    option_name="optionName",
                    resource_name="resourceName",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af9581a28a57063245aa9444d5b41883880a2845a06bab7175789bd303017a39)
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument option_name", value=option_name, expected_type=type_hints["option_name"])
                check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if namespace is not None:
                self._values["namespace"] = namespace
            if option_name is not None:
                self._values["option_name"] = option_name
            if resource_name is not None:
                self._values["resource_name"] = resource_name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''A unique namespace that identifies the option's associated AWS resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def option_name(self) -> typing.Optional[builtins.str]:
            '''The name of the configuration option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-optionname
            '''
            result = self._values.get("option_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_name(self) -> typing.Optional[builtins.str]:
            '''A unique resource name for the option setting.

            Use it for a time–based scaling configuration option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-resourcename
            '''
            result = self._values.get("resource_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The current value for the configuration option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationOptionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnConfigurationTemplatePropsMixin.SourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_name": "applicationName",
            "template_name": "templateName",
        },
    )
    class SourceConfigurationProperty:
        def __init__(
            self,
            *,
            application_name: typing.Optional[builtins.str] = None,
            template_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``SourceConfiguration`` property type to specify another AWS Elastic Beanstalk configuration template as the base to creating a new AWS::ElasticBeanstalk::ConfigurationTemplate resource in an AWS CloudFormation template.

            An AWS Elastic Beanstalk configuration template to base a new one on. You can use it to define a `AWS::ElasticBeanstalk::ConfigurationTemplate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ resource.

            :param application_name: The name of the application associated with the configuration.
            :param template_name: The name of the configuration template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
                
                source_configuration_property = elasticbeanstalk_mixins.CfnConfigurationTemplatePropsMixin.SourceConfigurationProperty(
                    application_name="applicationName",
                    template_name="templateName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__702903fcc6ed26e9de085e2ac88fc933cb067930a109602bfcd70381d7d0871c)
                check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
                check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_name is not None:
                self._values["application_name"] = application_name
            if template_name is not None:
                self._values["template_name"] = template_name

        @builtins.property
        def application_name(self) -> typing.Optional[builtins.str]:
            '''The name of the application associated with the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration-applicationname
            '''
            result = self._values.get("application_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def template_name(self) -> typing.Optional[builtins.str]:
            '''The name of the configuration template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration-templatename
            '''
            result = self._values.get("template_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "cname_prefix": "cnamePrefix",
        "description": "description",
        "environment_name": "environmentName",
        "operations_role": "operationsRole",
        "option_settings": "optionSettings",
        "platform_arn": "platformArn",
        "solution_stack_name": "solutionStackName",
        "tags": "tags",
        "template_name": "templateName",
        "tier": "tier",
        "version_label": "versionLabel",
    },
)
class CfnEnvironmentMixinProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        cname_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        operations_role: typing.Optional[builtins.str] = None,
        option_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.OptionSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        platform_arn: typing.Optional[builtins.str] = None,
        solution_stack_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        template_name: typing.Optional[builtins.str] = None,
        tier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.TierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        version_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEnvironmentPropsMixin.

        :param application_name: The name of the application that is associated with this environment.
        :param cname_prefix: If specified, the environment attempts to use this value as the prefix for the CNAME in your Elastic Beanstalk environment URL. If not specified, the CNAME is generated automatically by appending a random alphanumeric string to the environment name.
        :param description: Your description for this environment.
        :param environment_name: A unique name for the environment. Constraint: Must be from 4 to 40 characters in length. The name can contain only letters, numbers, and hyphens. It can't start or end with a hyphen. This name must be unique within a region in your account. If you don't specify the ``CNAMEPrefix`` parameter, the environment name becomes part of the CNAME, and therefore part of the visible URL for your application. If you don't specify an environment name, AWS CloudFormation generates a unique physical ID and uses that ID for the environment name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param operations_role: .. epigraph:: The operations role feature of AWS Elastic Beanstalk is in beta release and is subject to change. The Amazon Resource Name (ARN) of an existing IAM role to be used as the environment's operations role. If specified, Elastic Beanstalk uses the operations role for permissions to downstream services during this call and during subsequent calls acting on this environment. To specify an operations role, you must have the ``iam:PassRole`` permission for the role.
        :param option_settings: Key-value pairs defining configuration options for this environment, such as the instance type. These options override the values that are defined in the solution stack or the `configuration template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ . If you remove any options during a stack update, the removed options retain their current values.
        :param platform_arn: The Amazon Resource Name (ARN) of the custom platform to use with the environment. For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . .. epigraph:: If you specify ``PlatformArn`` , don't specify ``SolutionStackName`` .
        :param solution_stack_name: The name of an Elastic Beanstalk solution stack (platform version) to use with the environment. If specified, Elastic Beanstalk sets the configuration values to the default values associated with the specified solution stack. For a list of current solution stacks, see `Elastic Beanstalk Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html>`_ in the *AWS Elastic Beanstalk Platforms* guide. .. epigraph:: If you specify ``SolutionStackName`` , don't specify ``PlatformArn`` or ``TemplateName`` .
        :param tags: Specifies the tags applied to resources in the environment.
        :param template_name: The name of the Elastic Beanstalk configuration template to use with the environment. .. epigraph:: If you specify ``TemplateName`` , then don't specify ``SolutionStackName`` .
        :param tier: Specifies the tier to use in creating this environment. The environment tier that you choose determines whether Elastic Beanstalk provisions resources to support a web application that handles HTTP(S) requests or a web application that handles background-processing tasks.
        :param version_label: The name of the application version to deploy. Default: If not specified, Elastic Beanstalk attempts to deploy the sample application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
            
            cfn_environment_mixin_props = elasticbeanstalk_mixins.CfnEnvironmentMixinProps(
                application_name="applicationName",
                cname_prefix="cnamePrefix",
                description="description",
                environment_name="environmentName",
                operations_role="operationsRole",
                option_settings=[elasticbeanstalk_mixins.CfnEnvironmentPropsMixin.OptionSettingProperty(
                    namespace="namespace",
                    option_name="optionName",
                    resource_name="resourceName",
                    value="value"
                )],
                platform_arn="platformArn",
                solution_stack_name="solutionStackName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                template_name="templateName",
                tier=elasticbeanstalk_mixins.CfnEnvironmentPropsMixin.TierProperty(
                    name="name",
                    type="type",
                    version="version"
                ),
                version_label="versionLabel"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99bb076a69a087531fae9841195cff1dcba2bbeb43b848830c299797378adc7e)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument cname_prefix", value=cname_prefix, expected_type=type_hints["cname_prefix"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument operations_role", value=operations_role, expected_type=type_hints["operations_role"])
            check_type(argname="argument option_settings", value=option_settings, expected_type=type_hints["option_settings"])
            check_type(argname="argument platform_arn", value=platform_arn, expected_type=type_hints["platform_arn"])
            check_type(argname="argument solution_stack_name", value=solution_stack_name, expected_type=type_hints["solution_stack_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument version_label", value=version_label, expected_type=type_hints["version_label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if cname_prefix is not None:
            self._values["cname_prefix"] = cname_prefix
        if description is not None:
            self._values["description"] = description
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if operations_role is not None:
            self._values["operations_role"] = operations_role
        if option_settings is not None:
            self._values["option_settings"] = option_settings
        if platform_arn is not None:
            self._values["platform_arn"] = platform_arn
        if solution_stack_name is not None:
            self._values["solution_stack_name"] = solution_stack_name
        if tags is not None:
            self._values["tags"] = tags
        if template_name is not None:
            self._values["template_name"] = template_name
        if tier is not None:
            self._values["tier"] = tier
        if version_label is not None:
            self._values["version_label"] = version_label

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The name of the application that is associated with this environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cname_prefix(self) -> typing.Optional[builtins.str]:
        '''If specified, the environment attempts to use this value as the prefix for the CNAME in your Elastic Beanstalk environment URL.

        If not specified, the CNAME is generated automatically by appending a random alphanumeric string to the environment name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-cnameprefix
        '''
        result = self._values.get("cname_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Your description for this environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the environment.

        Constraint: Must be from 4 to 40 characters in length. The name can contain only letters, numbers, and hyphens. It can't start or end with a hyphen. This name must be unique within a region in your account.

        If you don't specify the ``CNAMEPrefix`` parameter, the environment name becomes part of the CNAME, and therefore part of the visible URL for your application.

        If you don't specify an environment name, AWS CloudFormation generates a unique physical ID and uses that ID for the environment name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-environmentname
        '''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operations_role(self) -> typing.Optional[builtins.str]:
        '''.. epigraph::

   The operations role feature of AWS Elastic Beanstalk is in beta release and is subject to change.

        The Amazon Resource Name (ARN) of an existing IAM role to be used as the environment's operations role. If specified, Elastic Beanstalk uses the operations role for permissions to downstream services during this call and during subsequent calls acting on this environment. To specify an operations role, you must have the ``iam:PassRole`` permission for the role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-operationsrole
        '''
        result = self._values.get("operations_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.OptionSettingProperty"]]]]:
        '''Key-value pairs defining configuration options for this environment, such as the instance type.

        These options override the values that are defined in the solution stack or the `configuration template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ . If you remove any options during a stack update, the removed options retain their current values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-optionsettings
        '''
        result = self._values.get("option_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.OptionSettingProperty"]]]], result)

    @builtins.property
    def platform_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the custom platform to use with the environment.

        For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
        .. epigraph::

           If you specify ``PlatformArn`` , don't specify ``SolutionStackName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-platformarn
        '''
        result = self._values.get("platform_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def solution_stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of an Elastic Beanstalk solution stack (platform version) to use with the environment.

        If specified, Elastic Beanstalk sets the configuration values to the default values associated with the specified solution stack. For a list of current solution stacks, see `Elastic Beanstalk Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html>`_ in the *AWS Elastic Beanstalk Platforms* guide.
        .. epigraph::

           If you specify ``SolutionStackName`` , don't specify ``PlatformArn`` or ``TemplateName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-solutionstackname
        '''
        result = self._values.get("solution_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies the tags applied to resources in the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Elastic Beanstalk configuration template to use with the environment.

        .. epigraph::

           If you specify ``TemplateName`` , then don't specify ``SolutionStackName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-templatename
        '''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tier(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.TierProperty"]]:
        '''Specifies the tier to use in creating this environment.

        The environment tier that you choose determines whether Elastic Beanstalk provisions resources to support a web application that handles HTTP(S) requests or a web application that handles background-processing tasks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-tier
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.TierProperty"]], result)

    @builtins.property
    def version_label(self) -> typing.Optional[builtins.str]:
        '''The name of the application version to deploy.

        Default: If not specified, Elastic Beanstalk attempts to deploy the sample application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-versionlabel
        '''
        result = self._values.get("version_label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnEnvironmentPropsMixin",
):
    '''Specify an AWS Elastic Beanstalk environment by using the AWS::ElasticBeanstalk::Environment resource in an AWS CloudFormation template.

    The AWS::ElasticBeanstalk::Environment resource is an AWS Elastic Beanstalk resource type that specifies an Elastic Beanstalk environment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html
    :cloudformationResource: AWS::ElasticBeanstalk::Environment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
        
        cfn_environment_props_mixin = elasticbeanstalk_mixins.CfnEnvironmentPropsMixin(elasticbeanstalk_mixins.CfnEnvironmentMixinProps(
            application_name="applicationName",
            cname_prefix="cnamePrefix",
            description="description",
            environment_name="environmentName",
            operations_role="operationsRole",
            option_settings=[elasticbeanstalk_mixins.CfnEnvironmentPropsMixin.OptionSettingProperty(
                namespace="namespace",
                option_name="optionName",
                resource_name="resourceName",
                value="value"
            )],
            platform_arn="platformArn",
            solution_stack_name="solutionStackName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            template_name="templateName",
            tier=elasticbeanstalk_mixins.CfnEnvironmentPropsMixin.TierProperty(
                name="name",
                type="type",
                version="version"
            ),
            version_label="versionLabel"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElasticBeanstalk::Environment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e52ea4f16c9ada474c45cf93ee9bb2170a410aba91c3573e2981dab1c13f5f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__738fe9265a4608cfba868f6d4bde09eb6fc24b0c7d7da03a57e22c9cf2615744)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420af3dff7f857a951e500bbaa8d9809137d5c18623b05de2844542bc14daca7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentMixinProps:
        return typing.cast(CfnEnvironmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnEnvironmentPropsMixin.OptionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "namespace": "namespace",
            "option_name": "optionName",
            "resource_name": "resourceName",
            "value": "value",
        },
    )
    class OptionSettingProperty:
        def __init__(
            self,
            *,
            namespace: typing.Optional[builtins.str] = None,
            option_name: typing.Optional[builtins.str] = None,
            resource_name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``OptionSetting`` property type to specify an option for an AWS Elastic Beanstalk environment when defining an AWS::ElasticBeanstalk::Environment resource in an AWS CloudFormation template.

            The ``OptionSetting`` property type specifies an option for an AWS Elastic Beanstalk environment.

            The ``OptionSettings`` property of the `AWS::ElasticBeanstalk::Environment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html>`_ resource contains a list of ``OptionSetting`` property types.

            For a list of possible namespaces and option values, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

            :param namespace: A unique namespace that identifies the option's associated AWS resource.
            :param option_name: The name of the configuration option.
            :param resource_name: A unique resource name for the option setting. Use it for a time–based scaling configuration option.
            :param value: The current value for the configuration option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
                
                option_setting_property = elasticbeanstalk_mixins.CfnEnvironmentPropsMixin.OptionSettingProperty(
                    namespace="namespace",
                    option_name="optionName",
                    resource_name="resourceName",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4066a4f7fe13cf3503d7d78889e0bd7f59a0582bc1b7c56fa65d962cf7f2d3f2)
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument option_name", value=option_name, expected_type=type_hints["option_name"])
                check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if namespace is not None:
                self._values["namespace"] = namespace
            if option_name is not None:
                self._values["option_name"] = option_name
            if resource_name is not None:
                self._values["resource_name"] = resource_name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''A unique namespace that identifies the option's associated AWS resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html#cfn-elasticbeanstalk-environment-optionsetting-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def option_name(self) -> typing.Optional[builtins.str]:
            '''The name of the configuration option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html#cfn-elasticbeanstalk-environment-optionsetting-optionname
            '''
            result = self._values.get("option_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_name(self) -> typing.Optional[builtins.str]:
            '''A unique resource name for the option setting.

            Use it for a time–based scaling configuration option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html#cfn-elasticbeanstalk-environment-optionsetting-resourcename
            '''
            result = self._values.get("resource_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The current value for the configuration option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html#cfn-elasticbeanstalk-environment-optionsetting-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticbeanstalk.mixins.CfnEnvironmentPropsMixin.TierProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type", "version": "version"},
    )
    class TierProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``Tier`` property type to specify the environment tier for an AWS Elastic Beanstalk environment when defining an AWS::ElasticBeanstalk::Environment resource in an AWS CloudFormation template.

            Describes the environment tier for an `AWS::ElasticBeanstalk::Environment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html>`_ resource. For more information, see `Environment Tiers <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features-managing-env-tiers.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

            :param name: The name of this environment tier. Valid values: - For *Web server tier* – ``WebServer`` - For *Worker tier* – ``Worker``
            :param type: The type of this environment tier. Valid values: - For *Web server tier* – ``Standard`` - For *Worker tier* – ``SQS/HTTP``
            :param version: The version of this environment tier. When you don't set a value to it, Elastic Beanstalk uses the latest compatible worker tier version. .. epigraph:: This member is deprecated. Any specific version that you set may become out of date. We recommend leaving it unspecified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-tier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticbeanstalk import mixins as elasticbeanstalk_mixins
                
                tier_property = elasticbeanstalk_mixins.CfnEnvironmentPropsMixin.TierProperty(
                    name="name",
                    type="type",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__68e858cf936d4ecd97c7a9a9cc4fb78b4a56fca26dcdca18bc4ebf027e2c5ba7)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of this environment tier.

            Valid values:

            - For *Web server tier* – ``WebServer``
            - For *Worker tier* – ``Worker``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-tier.html#cfn-elasticbeanstalk-environment-tier-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of this environment tier.

            Valid values:

            - For *Web server tier* – ``Standard``
            - For *Worker tier* – ``SQS/HTTP``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-tier.html#cfn-elasticbeanstalk-environment-tier-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of this environment tier.

            When you don't set a value to it, Elastic Beanstalk uses the latest compatible worker tier version.
            .. epigraph::

               This member is deprecated. Any specific version that you set may become out of date. We recommend leaving it unspecified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-tier.html#cfn-elasticbeanstalk-environment-tier-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnApplicationVersionMixinProps",
    "CfnApplicationVersionPropsMixin",
    "CfnConfigurationTemplateMixinProps",
    "CfnConfigurationTemplatePropsMixin",
    "CfnEnvironmentMixinProps",
    "CfnEnvironmentPropsMixin",
]

publication.publish()

def _typecheckingstub__144d9037afc3bec5fe1f04e6b86efdcb8f9a410cc8c1753c5cbd3f506c602ee4(
    *,
    application_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    resource_lifecycle_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationResourceLifecycleConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd405a1febef9decf4409c3edf11e92f143b8ec7aa53e6556bbd33baa423acb(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58140f6ba35acaaf2259bc7814d195f4e5a6e4682d2914b4d99d5caad758bf58(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e61c3aebf2ab4946590131d80c80f41fc26e0c118306857a8499f63a3c628d8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1291b13f5bb927e819495f02f12bd4c873926de97aec8a314dacc34551d59b(
    *,
    service_role: typing.Optional[builtins.str] = None,
    version_lifecycle_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ApplicationVersionLifecycleConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19467cad0e422a8f524d5cd3f8fcdc0145842f46b61e0e6590b0bab6fbb509e8(
    *,
    max_age_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.MaxAgeRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_count_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.MaxCountRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342b4a31c8578eb19392cb0bf8da5db261be2f3aaa2657b2ac4fbdde6b1fc81f(
    *,
    delete_source_from_s3: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_age_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f084097d6e3d2cce0454c7f73b4b5c3110b14611d9c4b0c516c8000743178b95(
    *,
    delete_source_from_s3: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56bff1ff17c78b1a603cefdcdedd382116de4a4e2eeac225bebf6940dbf7d52(
    *,
    application_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    source_bundle: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationVersionPropsMixin.SourceBundleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6eb15715f07f81a3717c64d94590f61d8cf91bbb4f1358d1b477ecf141d81b5(
    props: typing.Union[CfnApplicationVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9ea4f7b5831258e88f80799bac835fce9defc9f2f369e5dff83283fa518999(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d152289d2b2ea88b5c3853dd46b10318df8421e3064d0b32d61e2ffc63c0c4fb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3cba9b0738d0637eae4c1ec38f9bc3fa8c7aa5d87bcab15b64560b43176c4a8(
    *,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58cc15e2735b4c3d918c7fe863b52d75389b4dc9eaa3ad7a6f25f1299c304d99(
    *,
    application_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    environment_id: typing.Optional[builtins.str] = None,
    option_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationTemplatePropsMixin.ConfigurationOptionSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    platform_arn: typing.Optional[builtins.str] = None,
    solution_stack_name: typing.Optional[builtins.str] = None,
    source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationTemplatePropsMixin.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba38b30bdb9afd65db334753f0d856ff44b19412390cc999f77bc9e9522fb3ff(
    props: typing.Union[CfnConfigurationTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5673a74dda0c3f4f14c8713fab60a7357dcfa220f84a1064929db50d81f2df84(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6918f04e24722c62e8ed3bdbc5593b2355eb1aa9bdab8a6187831d60d19e33d2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9581a28a57063245aa9444d5b41883880a2845a06bab7175789bd303017a39(
    *,
    namespace: typing.Optional[builtins.str] = None,
    option_name: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702903fcc6ed26e9de085e2ac88fc933cb067930a109602bfcd70381d7d0871c(
    *,
    application_name: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bb076a69a087531fae9841195cff1dcba2bbeb43b848830c299797378adc7e(
    *,
    application_name: typing.Optional[builtins.str] = None,
    cname_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    operations_role: typing.Optional[builtins.str] = None,
    option_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.OptionSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    platform_arn: typing.Optional[builtins.str] = None,
    solution_stack_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_name: typing.Optional[builtins.str] = None,
    tier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.TierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    version_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e52ea4f16c9ada474c45cf93ee9bb2170a410aba91c3573e2981dab1c13f5f3(
    props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738fe9265a4608cfba868f6d4bde09eb6fc24b0c7d7da03a57e22c9cf2615744(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420af3dff7f857a951e500bbaa8d9809137d5c18623b05de2844542bc14daca7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4066a4f7fe13cf3503d7d78889e0bd7f59a0582bc1b7c56fa65d962cf7f2d3f2(
    *,
    namespace: typing.Optional[builtins.str] = None,
    option_name: typing.Optional[builtins.str] = None,
    resource_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e858cf936d4ecd97c7a9a9cc4fb78b4a56fca26dcdca18bc4ebf027e2c5ba7(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
