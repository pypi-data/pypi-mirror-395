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
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnCustomResourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "service_timeout": "serviceTimeout",
        "service_token": "serviceToken",
    },
)
class CfnCustomResourceMixinProps:
    def __init__(
        self,
        *,
        service_timeout: typing.Optional[jsii.Number] = None,
        service_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCustomResourcePropsMixin.

        :param service_timeout: The maximum time, in seconds, that can elapse before a custom resource operation times out. The value must be an integer from 1 to 3600. The default value is 3600 seconds (1 hour).
        :param service_token: The service token, such as an Amazon topic ARN or Lambda function ARN. The service token must be from the same Region as the stack. Updates aren't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-customresource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_custom_resource_mixin_props = cloudformation_mixins.CfnCustomResourceMixinProps(
                service_timeout=123,
                service_token="serviceToken"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2bc211907550ae2cbe1295611d8d47a48cd8ac71f7cee09f9f5f8cfdbfb3526)
            check_type(argname="argument service_timeout", value=service_timeout, expected_type=type_hints["service_timeout"])
            check_type(argname="argument service_token", value=service_token, expected_type=type_hints["service_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_timeout is not None:
            self._values["service_timeout"] = service_timeout
        if service_token is not None:
            self._values["service_token"] = service_token

    @builtins.property
    def service_timeout(self) -> typing.Optional[jsii.Number]:
        '''The maximum time, in seconds, that can elapse before a custom resource operation times out.

        The value must be an integer from 1 to 3600. The default value is 3600 seconds (1 hour).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-customresource.html#cfn-cloudformation-customresource-servicetimeout
        '''
        result = self._values.get("service_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_token(self) -> typing.Optional[builtins.str]:
        '''The service token, such as an Amazon  topic ARN or Lambda function ARN.

        The service token must be from the same Region as the stack.

        Updates aren't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-customresource.html#cfn-cloudformation-customresource-servicetoken
        '''
        result = self._values.get("service_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomResourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCustomResourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnCustomResourcePropsMixin",
):
    '''The ``AWS::CloudFormation::CustomResource`` resource creates a custom resource.

    Custom resources provide a way for you to write custom provisioning logic into your CloudFormation templates and have CloudFormation run it anytime you create, update (if you changed the custom resource), or delete a stack.

    For more information, see `Create custom provisioning logic with custom resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html>`_ in the *CloudFormation User Guide* .
    .. epigraph::

       If you use AWS PrivateLink , custom resources in the VPC must have access to CloudFormation -specific Amazon S3 buckets. Custom resources must send responses to a presigned Amazon S3 URL. If they can't send responses to Amazon S3 , CloudFormation won't receive a response and the stack operation fails. For more information, see `Access CloudFormation using an interface endpoint ( AWS PrivateLink ) <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/vpc-interface-endpoints.html>`_ in the *CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-customresource.html
    :cloudformationResource: AWS::CloudFormation::CustomResource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_custom_resource_props_mixin = cloudformation_mixins.CfnCustomResourcePropsMixin(cloudformation_mixins.CfnCustomResourceMixinProps(
            service_timeout=123,
            service_token="serviceToken"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCustomResourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::CustomResource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc671c65f20d38959c3c95dac6907a019841cfe71a2b699f9f4e5e79bc60c57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2088255e09043e85440b492721425214c9211a6ad05e5193cac64856e724dc3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fce90ef2e732a96bb0495fe0d5c7b080fa8f356f62d0c73743c9a2a2b3eb808)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCustomResourceMixinProps:
        return typing.cast(CfnCustomResourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnGuardHookMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "execution_role": "executionRole",
        "failure_mode": "failureMode",
        "hook_status": "hookStatus",
        "log_bucket": "logBucket",
        "options": "options",
        "rule_location": "ruleLocation",
        "stack_filters": "stackFilters",
        "target_filters": "targetFilters",
        "target_operations": "targetOperations",
    },
)
class CfnGuardHookMixinProps:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        execution_role: typing.Optional[builtins.str] = None,
        failure_mode: typing.Optional[builtins.str] = None,
        hook_status: typing.Optional[builtins.str] = None,
        log_bucket: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGuardHookPropsMixin.OptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rule_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGuardHookPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stack_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGuardHookPropsMixin.StackFiltersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGuardHookPropsMixin.TargetFiltersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnGuardHookPropsMixin.

        :param alias: The type name alias for the Hook. This alias must be unique per account and Region. The alias must be in the form ``Name1::Name2::Name3`` and must not begin with ``AWS`` . For example, ``Private::Guard::MyTestHook`` .
        :param execution_role: The IAM role that the Hook assumes to retrieve your Guard rules from S3 and optionally write a detailed Guard output report back.
        :param failure_mode: Specifies how the Hook responds when rules fail their evaluation. - ``FAIL`` : Prevents the action from proceeding. This is helpful for enforcing strict compliance or security policies. - ``WARN`` : Issues warnings to users but allows actions to continue. This is useful for non-critical validations or informational checks. Default: - "WARN"
        :param hook_status: Specifies if the Hook is ``ENABLED`` or ``DISABLED`` . Default: - "DISABLED"
        :param log_bucket: Specifies the name of an S3 bucket to store the Guard output report. This report contains the results of your Guard rule validations.
        :param options: Specifies the S3 location of your input parameters.
        :param rule_location: Specifies the S3 location of your Guard rules.
        :param stack_filters: Specifies the stack level filters for the Hook. Example stack level filter in JSON: ``"StackFilters": {"FilteringCriteria": "ALL", "StackNames": {"Exclude": [ "stack-1", "stack-2"]}}`` Example stack level filter in YAML: ``StackFilters: FilteringCriteria: ALL StackNames: Exclude: - stack-1 - stack-2``
        :param target_filters: Specifies the target filters for the Hook. Example target filter in JSON: ``"TargetFilters": {"Actions": [ "CREATE", "UPDATE", "DELETE" ]}`` Example target filter in YAML: ``TargetFilters: Actions: - CREATE - UPDATE - DELETE``
        :param target_operations: Specifies the list of operations the Hook is run against. For more information, see `Hook targets <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-concepts.html#hook-terms-hook-target>`_ in the *CloudFormation Hooks User Guide* . Valid values: ``STACK`` | ``RESOURCE`` | ``CHANGE_SET`` | ``CLOUD_CONTROL``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_guard_hook_mixin_props = cloudformation_mixins.CfnGuardHookMixinProps(
                alias="alias",
                execution_role="executionRole",
                failure_mode="failureMode",
                hook_status="hookStatus",
                log_bucket="logBucket",
                options=cloudformation_mixins.CfnGuardHookPropsMixin.OptionsProperty(
                    input_params=cloudformation_mixins.CfnGuardHookPropsMixin.S3LocationProperty(
                        uri="uri",
                        version_id="versionId"
                    )
                ),
                rule_location=cloudformation_mixins.CfnGuardHookPropsMixin.S3LocationProperty(
                    uri="uri",
                    version_id="versionId"
                ),
                stack_filters=cloudformation_mixins.CfnGuardHookPropsMixin.StackFiltersProperty(
                    filtering_criteria="filteringCriteria",
                    stack_names=cloudformation_mixins.CfnGuardHookPropsMixin.StackNamesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    ),
                    stack_roles=cloudformation_mixins.CfnGuardHookPropsMixin.StackRolesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    )
                ),
                target_filters=cloudformation_mixins.CfnGuardHookPropsMixin.TargetFiltersProperty(
                    actions=["actions"],
                    invocation_points=["invocationPoints"],
                    target_names=["targetNames"],
                    targets=[cloudformation_mixins.CfnGuardHookPropsMixin.HookTargetProperty(
                        action="action",
                        invocation_point="invocationPoint",
                        target_name="targetName"
                    )]
                ),
                target_operations=["targetOperations"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f2785017f90af2b6ba3b2a992462488b80c9036a8eb7187c9f2715c308dd4e)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument failure_mode", value=failure_mode, expected_type=type_hints["failure_mode"])
            check_type(argname="argument hook_status", value=hook_status, expected_type=type_hints["hook_status"])
            check_type(argname="argument log_bucket", value=log_bucket, expected_type=type_hints["log_bucket"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument rule_location", value=rule_location, expected_type=type_hints["rule_location"])
            check_type(argname="argument stack_filters", value=stack_filters, expected_type=type_hints["stack_filters"])
            check_type(argname="argument target_filters", value=target_filters, expected_type=type_hints["target_filters"])
            check_type(argname="argument target_operations", value=target_operations, expected_type=type_hints["target_operations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if failure_mode is not None:
            self._values["failure_mode"] = failure_mode
        if hook_status is not None:
            self._values["hook_status"] = hook_status
        if log_bucket is not None:
            self._values["log_bucket"] = log_bucket
        if options is not None:
            self._values["options"] = options
        if rule_location is not None:
            self._values["rule_location"] = rule_location
        if stack_filters is not None:
            self._values["stack_filters"] = stack_filters
        if target_filters is not None:
            self._values["target_filters"] = target_filters
        if target_operations is not None:
            self._values["target_operations"] = target_operations

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''The type name alias for the Hook. This alias must be unique per account and Region.

        The alias must be in the form ``Name1::Name2::Name3`` and must not begin with ``AWS`` . For example, ``Private::Guard::MyTestHook`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-alias
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[builtins.str]:
        '''The IAM role that the Hook assumes to retrieve your Guard rules from S3 and optionally write a detailed Guard output report back.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-executionrole
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies how the Hook responds when rules fail their evaluation.

        - ``FAIL`` : Prevents the action from proceeding. This is helpful for enforcing strict compliance or security policies.
        - ``WARN`` : Issues warnings to users but allows actions to continue. This is useful for non-critical validations or informational checks.

        :default: - "WARN"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-failuremode
        '''
        result = self._values.get("failure_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hook_status(self) -> typing.Optional[builtins.str]:
        '''Specifies if the Hook is ``ENABLED`` or ``DISABLED`` .

        :default: - "DISABLED"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-hookstatus
        '''
        result = self._values.get("hook_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_bucket(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of an S3 bucket to store the Guard output report.

        This report contains the results of your Guard rule validations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-logbucket
        '''
        result = self._values.get("log_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.OptionsProperty"]]:
        '''Specifies the S3 location of your input parameters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.OptionsProperty"]], result)

    @builtins.property
    def rule_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.S3LocationProperty"]]:
        '''Specifies the S3 location of your Guard rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-rulelocation
        '''
        result = self._values.get("rule_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def stack_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.StackFiltersProperty"]]:
        '''Specifies the stack level filters for the Hook.

        Example stack level filter in JSON:

        ``"StackFilters": {"FilteringCriteria": "ALL", "StackNames": {"Exclude": [ "stack-1", "stack-2"]}}``

        Example stack level filter in YAML:

        ``StackFilters: FilteringCriteria: ALL StackNames: Exclude: - stack-1 - stack-2``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-stackfilters
        '''
        result = self._values.get("stack_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.StackFiltersProperty"]], result)

    @builtins.property
    def target_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.TargetFiltersProperty"]]:
        '''Specifies the target filters for the Hook.

        Example target filter in JSON:

        ``"TargetFilters": {"Actions": [ "CREATE", "UPDATE", "DELETE" ]}``

        Example target filter in YAML:

        ``TargetFilters: Actions: - CREATE - UPDATE - DELETE``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-targetfilters
        '''
        result = self._values.get("target_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.TargetFiltersProperty"]], result)

    @builtins.property
    def target_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of operations the Hook is run against.

        For more information, see `Hook targets <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-concepts.html#hook-terms-hook-target>`_ in the *CloudFormation Hooks User Guide* .

        Valid values: ``STACK`` | ``RESOURCE`` | ``CHANGE_SET`` | ``CLOUD_CONTROL``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html#cfn-cloudformation-guardhook-targetoperations
        '''
        result = self._values.get("target_operations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGuardHookMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGuardHookPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnGuardHookPropsMixin",
):
    '''The ``AWS::CloudFormation::GuardHook`` resource creates and activates a Guard Hook.

    Using the Guard domain specific language (DSL), you can author Guard Hooks to evaluate your resources before allowing stack operations.

    For more information, see `Guard Hooks <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/guard-hooks.html>`_ in the *CloudFormation Hooks User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-guardhook.html
    :cloudformationResource: AWS::CloudFormation::GuardHook
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_guard_hook_props_mixin = cloudformation_mixins.CfnGuardHookPropsMixin(cloudformation_mixins.CfnGuardHookMixinProps(
            alias="alias",
            execution_role="executionRole",
            failure_mode="failureMode",
            hook_status="hookStatus",
            log_bucket="logBucket",
            options=cloudformation_mixins.CfnGuardHookPropsMixin.OptionsProperty(
                input_params=cloudformation_mixins.CfnGuardHookPropsMixin.S3LocationProperty(
                    uri="uri",
                    version_id="versionId"
                )
            ),
            rule_location=cloudformation_mixins.CfnGuardHookPropsMixin.S3LocationProperty(
                uri="uri",
                version_id="versionId"
            ),
            stack_filters=cloudformation_mixins.CfnGuardHookPropsMixin.StackFiltersProperty(
                filtering_criteria="filteringCriteria",
                stack_names=cloudformation_mixins.CfnGuardHookPropsMixin.StackNamesProperty(
                    exclude=["exclude"],
                    include=["include"]
                ),
                stack_roles=cloudformation_mixins.CfnGuardHookPropsMixin.StackRolesProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            ),
            target_filters=cloudformation_mixins.CfnGuardHookPropsMixin.TargetFiltersProperty(
                actions=["actions"],
                invocation_points=["invocationPoints"],
                target_names=["targetNames"],
                targets=[cloudformation_mixins.CfnGuardHookPropsMixin.HookTargetProperty(
                    action="action",
                    invocation_point="invocationPoint",
                    target_name="targetName"
                )]
            ),
            target_operations=["targetOperations"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGuardHookMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::GuardHook``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacbde3b2a5fc9f73e57ad2aa241d17d5fcb9d5efb203b0cb2e101be22e43d0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ce25bd47c17d2f87d3531d01e6e8e72fc758d6c7e89fa383c5755a53af990bd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05cda488fc33650c0335c898b01db2b1ce64995329eccc5fae112b21bbee7d7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGuardHookMixinProps:
        return typing.cast(CfnGuardHookMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnGuardHookPropsMixin.HookTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "invocation_point": "invocationPoint",
            "target_name": "targetName",
        },
    )
    class HookTargetProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            invocation_point: typing.Optional[builtins.str] = None,
            target_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Hook targets are the destination where hooks will be invoked against.

            :param action: Target actions are the type of operation hooks will be executed at.
            :param invocation_point: Invocation points are the point in provisioning workflow where hooks will be executed.
            :param target_name: Type name of hook target. Hook targets are the destination where hooks will be invoked against.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-hooktarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                hook_target_property = cloudformation_mixins.CfnGuardHookPropsMixin.HookTargetProperty(
                    action="action",
                    invocation_point="invocationPoint",
                    target_name="targetName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__105efa52488deb50e130fbccf1fa3a7b53bb0557a1bce49acbea112f8310c9dc)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument invocation_point", value=invocation_point, expected_type=type_hints["invocation_point"])
                check_type(argname="argument target_name", value=target_name, expected_type=type_hints["target_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if invocation_point is not None:
                self._values["invocation_point"] = invocation_point
            if target_name is not None:
                self._values["target_name"] = target_name

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''Target actions are the type of operation hooks will be executed at.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-hooktarget.html#cfn-cloudformation-guardhook-hooktarget-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def invocation_point(self) -> typing.Optional[builtins.str]:
            '''Invocation points are the point in provisioning workflow where hooks will be executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-hooktarget.html#cfn-cloudformation-guardhook-hooktarget-invocationpoint
            '''
            result = self._values.get("invocation_point")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_name(self) -> typing.Optional[builtins.str]:
            '''Type name of hook target.

            Hook targets are the destination where hooks will be invoked against.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-hooktarget.html#cfn-cloudformation-guardhook-hooktarget-targetname
            '''
            result = self._values.get("target_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HookTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnGuardHookPropsMixin.OptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"input_params": "inputParams"},
    )
    class OptionsProperty:
        def __init__(
            self,
            *,
            input_params: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGuardHookPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the input parameters for a Guard Hook.

            :param input_params: Specifies the S3 location where your input parameters are located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-options.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                options_property = cloudformation_mixins.CfnGuardHookPropsMixin.OptionsProperty(
                    input_params=cloudformation_mixins.CfnGuardHookPropsMixin.S3LocationProperty(
                        uri="uri",
                        version_id="versionId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b35d4fd4d5399176b0f3dc44a5b0ed7be51156e6ca54ae9ea0fd4f469fcd88d7)
                check_type(argname="argument input_params", value=input_params, expected_type=type_hints["input_params"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_params is not None:
                self._values["input_params"] = input_params

        @builtins.property
        def input_params(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.S3LocationProperty"]]:
            '''Specifies the S3 location where your input parameters are located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-options.html#cfn-cloudformation-guardhook-options-inputparams
            '''
            result = self._values.get("input_params")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnGuardHookPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"uri": "uri", "version_id": "versionId"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            uri: typing.Optional[builtins.str] = None,
            version_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the S3 location where your Guard rules or input parameters are located.

            :param uri: Specifies the S3 path to the file that contains your Guard rules or input parameters (in the form ``s3://<bucket name>/<file name>`` ). For Guard rules, the object stored in S3 must have one of the following file extensions: ``.guard`` , ``.zip`` , or ``.tar.gz`` . For input parameters, the object stored in S3 must have one of the following file extensions: ``.yaml`` , ``.json`` , ``.zip`` , or ``.tar.gz`` .
            :param version_id: For S3 buckets with versioning enabled, specifies the unique ID of the S3 object version to download your Guard rules or input parameters from. The Guard Hook downloads files from S3 every time the Hook is invoked. To prevent accidental changes or deletions, we recommend using a version when configuring your Guard Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                s3_location_property = cloudformation_mixins.CfnGuardHookPropsMixin.S3LocationProperty(
                    uri="uri",
                    version_id="versionId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3859d18635353f751a50fcc26c4c59378dd4b3764f10350e08e8092f36017dd6)
                check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
                check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if uri is not None:
                self._values["uri"] = uri
            if version_id is not None:
                self._values["version_id"] = version_id

        @builtins.property
        def uri(self) -> typing.Optional[builtins.str]:
            '''Specifies the S3 path to the file that contains your Guard rules or input parameters (in the form ``s3://<bucket name>/<file name>`` ).

            For Guard rules, the object stored in S3 must have one of the following file extensions: ``.guard`` , ``.zip`` , or ``.tar.gz`` .

            For input parameters, the object stored in S3 must have one of the following file extensions: ``.yaml`` , ``.json`` , ``.zip`` , or ``.tar.gz`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-s3location.html#cfn-cloudformation-guardhook-s3location-uri
            '''
            result = self._values.get("uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version_id(self) -> typing.Optional[builtins.str]:
            '''For S3 buckets with versioning enabled, specifies the unique ID of the S3 object version to download your Guard rules or input parameters from.

            The Guard Hook downloads files from S3 every time the Hook is invoked. To prevent accidental changes or deletions, we recommend using a version when configuring your Guard Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-s3location.html#cfn-cloudformation-guardhook-s3location-versionid
            '''
            result = self._values.get("version_id")
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
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnGuardHookPropsMixin.StackFiltersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "filtering_criteria": "filteringCriteria",
            "stack_names": "stackNames",
            "stack_roles": "stackRoles",
        },
    )
    class StackFiltersProperty:
        def __init__(
            self,
            *,
            filtering_criteria: typing.Optional[builtins.str] = None,
            stack_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGuardHookPropsMixin.StackNamesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stack_roles: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGuardHookPropsMixin.StackRolesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``StackFilters`` property type specifies stack level filters for a Hook.

            The ``StackNames`` or ``StackRoles`` properties are optional. However, you must specify at least one of these properties.

            For more information, see `CloudFormation Hooks stack level filters <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-stack-level-filtering.html>`_ .

            :param filtering_criteria: The filtering criteria. - All stack names and stack roles ( ``All`` ): The Hook will only be invoked when all specified filters match. - Any stack names and stack roles ( ``Any`` ): The Hook will be invoked if at least one of the specified filters match. Default: - "ALL"
            :param stack_names: Includes or excludes specific stacks from Hook invocations.
            :param stack_roles: Includes or excludes specific stacks from Hook invocations based on their associated IAM roles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stackfilters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                stack_filters_property = cloudformation_mixins.CfnGuardHookPropsMixin.StackFiltersProperty(
                    filtering_criteria="filteringCriteria",
                    stack_names=cloudformation_mixins.CfnGuardHookPropsMixin.StackNamesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    ),
                    stack_roles=cloudformation_mixins.CfnGuardHookPropsMixin.StackRolesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e46394e8691f5fd9c0e36c979f212b4d865d2ef2daf02f66f1603892c6f6947)
                check_type(argname="argument filtering_criteria", value=filtering_criteria, expected_type=type_hints["filtering_criteria"])
                check_type(argname="argument stack_names", value=stack_names, expected_type=type_hints["stack_names"])
                check_type(argname="argument stack_roles", value=stack_roles, expected_type=type_hints["stack_roles"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filtering_criteria is not None:
                self._values["filtering_criteria"] = filtering_criteria
            if stack_names is not None:
                self._values["stack_names"] = stack_names
            if stack_roles is not None:
                self._values["stack_roles"] = stack_roles

        @builtins.property
        def filtering_criteria(self) -> typing.Optional[builtins.str]:
            '''The filtering criteria.

            - All stack names and stack roles ( ``All`` ): The Hook will only be invoked when all specified filters match.
            - Any stack names and stack roles ( ``Any`` ): The Hook will be invoked if at least one of the specified filters match.

            :default: - "ALL"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stackfilters.html#cfn-cloudformation-guardhook-stackfilters-filteringcriteria
            '''
            result = self._values.get("filtering_criteria")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stack_names(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.StackNamesProperty"]]:
            '''Includes or excludes specific stacks from Hook invocations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stackfilters.html#cfn-cloudformation-guardhook-stackfilters-stacknames
            '''
            result = self._values.get("stack_names")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.StackNamesProperty"]], result)

        @builtins.property
        def stack_roles(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.StackRolesProperty"]]:
            '''Includes or excludes specific stacks from Hook invocations based on their associated IAM roles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stackfilters.html#cfn-cloudformation-guardhook-stackfilters-stackroles
            '''
            result = self._values.get("stack_roles")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.StackRolesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackFiltersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnGuardHookPropsMixin.StackNamesProperty",
        jsii_struct_bases=[],
        name_mapping={"exclude": "exclude", "include": "include"},
    )
    class StackNamesProperty:
        def __init__(
            self,
            *,
            exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            include: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the stack names for the ``StackFilters`` property type to include or exclude specific stacks from Hook invocations.

            For more information, see `CloudFormation Hooks stack level filters <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-stack-level-filtering.html>`_ .

            :param exclude: The stack names to exclude. All stacks except those listed here will invoke the Hook.
            :param include: The stack names to include. Only the stacks specified in this list will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stacknames.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                stack_names_property = cloudformation_mixins.CfnGuardHookPropsMixin.StackNamesProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6f7079a4dcc1b5b824fa1bbd03671703db5e70cd45ea18312f68e6e24ef1267)
                check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude is not None:
                self._values["exclude"] = exclude
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The stack names to exclude.

            All stacks except those listed here will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stacknames.html#cfn-cloudformation-guardhook-stacknames-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The stack names to include.

            Only the stacks specified in this list will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stacknames.html#cfn-cloudformation-guardhook-stacknames-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackNamesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnGuardHookPropsMixin.StackRolesProperty",
        jsii_struct_bases=[],
        name_mapping={"exclude": "exclude", "include": "include"},
    )
    class StackRolesProperty:
        def __init__(
            self,
            *,
            exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            include: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the stack roles for the ``StackFilters`` property type to include or exclude specific stacks from Hook invocations based on their associated IAM roles.

            For more information, see `CloudFormation Hooks stack level filters <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-stack-level-filtering.html>`_ .

            :param exclude: The IAM role ARNs for stacks you want to exclude. The Hook will be invoked on all stacks except those initiated by the specified roles.
            :param include: The IAM role ARNs to target stacks associated with these roles. Only stack operations initiated by these roles will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stackroles.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                stack_roles_property = cloudformation_mixins.CfnGuardHookPropsMixin.StackRolesProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__226e629068c06e4a33bab8a41e098a9f868ca4578a6763b5f48e1fb80aada585)
                check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude is not None:
                self._values["exclude"] = exclude
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IAM role ARNs for stacks you want to exclude.

            The Hook will be invoked on all stacks except those initiated by the specified roles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stackroles.html#cfn-cloudformation-guardhook-stackroles-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IAM role ARNs to target stacks associated with these roles.

            Only stack operations initiated by these roles will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-stackroles.html#cfn-cloudformation-guardhook-stackroles-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackRolesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnGuardHookPropsMixin.TargetFiltersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "invocation_points": "invocationPoints",
            "target_names": "targetNames",
            "targets": "targets",
        },
    )
    class TargetFiltersProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            invocation_points: typing.Optional[typing.Sequence[builtins.str]] = None,
            target_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGuardHookPropsMixin.HookTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``TargetFilters`` property type specifies the target filters for the Hook.

            For more information, see `CloudFormation Hook target filters <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-target-filtering.html>`_ .

            :param actions: List of actions that the hook is going to target.
            :param invocation_points: List of invocation points that the hook is going to target.
            :param target_names: List of type names that the hook is going to target.
            :param targets: List of hook targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-targetfilters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                target_filters_property = cloudformation_mixins.CfnGuardHookPropsMixin.TargetFiltersProperty(
                    actions=["actions"],
                    invocation_points=["invocationPoints"],
                    target_names=["targetNames"],
                    targets=[cloudformation_mixins.CfnGuardHookPropsMixin.HookTargetProperty(
                        action="action",
                        invocation_point="invocationPoint",
                        target_name="targetName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a5ccf579ee6a5bb653c147558f98d4001d5e8e70f1602143345e03c2f371f6f)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument invocation_points", value=invocation_points, expected_type=type_hints["invocation_points"])
                check_type(argname="argument target_names", value=target_names, expected_type=type_hints["target_names"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if invocation_points is not None:
                self._values["invocation_points"] = invocation_points
            if target_names is not None:
                self._values["target_names"] = target_names
            if targets is not None:
                self._values["targets"] = targets

        @builtins.property
        def actions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of actions that the hook is going to target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-targetfilters.html#cfn-cloudformation-guardhook-targetfilters-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def invocation_points(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of invocation points that the hook is going to target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-targetfilters.html#cfn-cloudformation-guardhook-targetfilters-invocationpoints
            '''
            result = self._values.get("invocation_points")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def target_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of type names that the hook is going to target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-targetfilters.html#cfn-cloudformation-guardhook-targetfilters-targetnames
            '''
            result = self._values.get("target_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.HookTargetProperty"]]]]:
            '''List of hook targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-guardhook-targetfilters.html#cfn-cloudformation-guardhook-targetfilters-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGuardHookPropsMixin.HookTargetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetFiltersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnHookDefaultVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "type_name": "typeName",
        "type_version_arn": "typeVersionArn",
        "version_id": "versionId",
    },
)
class CfnHookDefaultVersionMixinProps:
    def __init__(
        self,
        *,
        type_name: typing.Optional[builtins.str] = None,
        type_version_arn: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnHookDefaultVersionPropsMixin.

        :param type_name: The name of the Hook. You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param type_version_arn: The version ID of the type configuration. You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param version_id: The version ID of the type specified. You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_hook_default_version_mixin_props = cloudformation_mixins.CfnHookDefaultVersionMixinProps(
                type_name="typeName",
                type_version_arn="typeVersionArn",
                version_id="versionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ee3982c76a548518fcb400f607e6fdf87c5199a8fafd430948199cd9c63b39)
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument type_version_arn", value=type_version_arn, expected_type=type_hints["type_version_arn"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type_name is not None:
            self._values["type_name"] = type_name
        if type_version_arn is not None:
            self._values["type_version_arn"] = type_version_arn
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Hook.

        You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html#cfn-cloudformation-hookdefaultversion-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_version_arn(self) -> typing.Optional[builtins.str]:
        '''The version ID of the type configuration.

        You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html#cfn-cloudformation-hookdefaultversion-typeversionarn
        '''
        result = self._values.get("type_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''The version ID of the type specified.

        You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html#cfn-cloudformation-hookdefaultversion-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHookDefaultVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHookDefaultVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnHookDefaultVersionPropsMixin",
):
    '''The ``AWS::CloudFormation::HookDefaultVersion`` resource specifies the default version of a Hook.

    The default version of the Hook is used in CloudFormation operations for this AWS account and AWS Region .

    For information about the CloudFormation registry, see `Managing extensions with the CloudFormation registry <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html>`_ in the *CloudFormation User Guide* .

    This resource type is not compatible with Guard and Lambda Hooks.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookdefaultversion.html
    :cloudformationResource: AWS::CloudFormation::HookDefaultVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_hook_default_version_props_mixin = cloudformation_mixins.CfnHookDefaultVersionPropsMixin(cloudformation_mixins.CfnHookDefaultVersionMixinProps(
            type_name="typeName",
            type_version_arn="typeVersionArn",
            version_id="versionId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnHookDefaultVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::HookDefaultVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1246c39dba98b649df85eb7e7db20e5c2e1d5f1a12863e5a4a0360af3cdfec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac5ea19c9dff1f7a0752d25f24e044b425ca4897578f66dd03cb76d87a78c73f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32fffd003a829e0c3420a3e887768025c4bf32294372297521f6d629401b9587)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHookDefaultVersionMixinProps:
        return typing.cast(CfnHookDefaultVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnHookTypeConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "configuration_alias": "configurationAlias",
        "type_arn": "typeArn",
        "type_name": "typeName",
    },
)
class CfnHookTypeConfigMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[builtins.str] = None,
        configuration_alias: typing.Optional[builtins.str] = None,
        type_arn: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnHookTypeConfigPropsMixin.

        :param configuration: Specifies the activated Hook type configuration, in this AWS account and AWS Region . You must specify either ``TypeName`` and ``Configuration`` or ``TypeArn`` and ``Configuration`` .
        :param configuration_alias: An alias by which to refer to this configuration data. Defaults to ``default`` alias. Hook types currently support default configuration alias. Default: - "default"
        :param type_arn: The Amazon Resource Number (ARN) for the Hook to set ``Configuration`` for. You must specify either ``TypeName`` and ``Configuration`` or ``TypeArn`` and ``Configuration`` .
        :param type_name: The unique name for your Hook. Specifies a three-part namespace for your Hook, with a recommended pattern of ``Organization::Service::Hook`` . You must specify either ``TypeName`` and ``Configuration`` or ``TypeArn`` and ``Configuration`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_hook_type_config_mixin_props = cloudformation_mixins.CfnHookTypeConfigMixinProps(
                configuration="configuration",
                configuration_alias="configurationAlias",
                type_arn="typeArn",
                type_name="typeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f177c4ff8303b775fc7629d2c3746a21e904a011d2caf48500e389607046236)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument configuration_alias", value=configuration_alias, expected_type=type_hints["configuration_alias"])
            check_type(argname="argument type_arn", value=type_arn, expected_type=type_hints["type_arn"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if configuration_alias is not None:
            self._values["configuration_alias"] = configuration_alias
        if type_arn is not None:
            self._values["type_arn"] = type_arn
        if type_name is not None:
            self._values["type_name"] = type_name

    @builtins.property
    def configuration(self) -> typing.Optional[builtins.str]:
        '''Specifies the activated Hook type configuration, in this AWS account and AWS Region .

        You must specify either ``TypeName`` and ``Configuration`` or ``TypeArn`` and ``Configuration`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_alias(self) -> typing.Optional[builtins.str]:
        '''An alias by which to refer to this configuration data.

        Defaults to ``default`` alias. Hook types currently support default configuration alias.

        :default: - "default"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-configurationalias
        '''
        result = self._values.get("configuration_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) for the Hook to set ``Configuration`` for.

        You must specify either ``TypeName`` and ``Configuration`` or ``TypeArn`` and ``Configuration`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-typearn
        '''
        result = self._values.get("type_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The unique name for your Hook.

        Specifies a three-part namespace for your Hook, with a recommended pattern of ``Organization::Service::Hook`` .

        You must specify either ``TypeName`` and ``Configuration`` or ``TypeArn`` and ``Configuration`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html#cfn-cloudformation-hooktypeconfig-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHookTypeConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHookTypeConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnHookTypeConfigPropsMixin",
):
    '''The ``AWS::CloudFormation::HookTypeConfig`` resource specifies the configuration of an activated Hook.

    For information about the CloudFormation registry, see `Managing extensions with the CloudFormation registry <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html>`_ in the *CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hooktypeconfig.html
    :cloudformationResource: AWS::CloudFormation::HookTypeConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_hook_type_config_props_mixin = cloudformation_mixins.CfnHookTypeConfigPropsMixin(cloudformation_mixins.CfnHookTypeConfigMixinProps(
            configuration="configuration",
            configuration_alias="configurationAlias",
            type_arn="typeArn",
            type_name="typeName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnHookTypeConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::HookTypeConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21bfbe90b8c6c27cfe7c696c02a55138ab4782feb2b1cdd0b52b32bb12e825c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e6e87c8c5586ab513d04dc0fb3331db7e719a00b3024dfd092e1fcbfcc99896)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac48ae7ff7cca726350aec55fa19ec05224f87e39e88cc2249d33b6fb200484c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHookTypeConfigMixinProps:
        return typing.cast(CfnHookTypeConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnHookVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role_arn": "executionRoleArn",
        "logging_config": "loggingConfig",
        "schema_handler_package": "schemaHandlerPackage",
        "type_name": "typeName",
    },
)
class CfnHookVersionMixinProps:
    def __init__(
        self,
        *,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHookVersionPropsMixin.LoggingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schema_handler_package: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnHookVersionPropsMixin.

        :param execution_role_arn: The Amazon Resource Name (ARN) of the task execution role that grants the Hook permission.
        :param logging_config: Contains logging configuration information for an extension.
        :param schema_handler_package: A URL to the Amazon S3 bucket for the Hook project package that contains the necessary files for the Hook you want to register. For information on generating a schema handler package, see `Modeling custom CloudFormation Hooks <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-model.html>`_ in the *CloudFormation Hooks User Guide* . .. epigraph:: To register the Hook, you must have ``s3:GetObject`` permissions to access the S3 objects.
        :param type_name: The unique name for your Hook. Specifies a three-part namespace for your Hook, with a recommended pattern of ``Organization::Service::Hook`` . .. epigraph:: The following organization namespaces are reserved and can't be used in your Hook type names: - ``Alexa`` - ``AMZN`` - ``Amazon`` - ``ASK`` - ``AWS`` - ``Custom`` - ``Dev``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_hook_version_mixin_props = cloudformation_mixins.CfnHookVersionMixinProps(
                execution_role_arn="executionRoleArn",
                logging_config=cloudformation_mixins.CfnHookVersionPropsMixin.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                ),
                schema_handler_package="schemaHandlerPackage",
                type_name="typeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2e7d068847c0c435dd51b41d1056aef91fc94dcd1c231432d39d0b2c4cea3d)
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument schema_handler_package", value=schema_handler_package, expected_type=type_hints["schema_handler_package"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if schema_handler_package is not None:
            self._values["schema_handler_package"] = schema_handler_package
        if type_name is not None:
            self._values["type_name"] = type_name

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the task execution role that grants the Hook permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHookVersionPropsMixin.LoggingConfigProperty"]]:
        '''Contains logging configuration information for an extension.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-loggingconfig
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHookVersionPropsMixin.LoggingConfigProperty"]], result)

    @builtins.property
    def schema_handler_package(self) -> typing.Optional[builtins.str]:
        '''A URL to the Amazon S3 bucket for the Hook project package that contains the necessary files for the Hook you want to register.

        For information on generating a schema handler package, see `Modeling custom CloudFormation Hooks <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-model.html>`_ in the *CloudFormation Hooks User Guide* .
        .. epigraph::

           To register the Hook, you must have ``s3:GetObject`` permissions to access the S3 objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-schemahandlerpackage
        '''
        result = self._values.get("schema_handler_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The unique name for your Hook.

        Specifies a three-part namespace for your Hook, with a recommended pattern of ``Organization::Service::Hook`` .
        .. epigraph::

           The following organization namespaces are reserved and can't be used in your Hook type names:

           - ``Alexa``
           - ``AMZN``
           - ``Amazon``
           - ``ASK``
           - ``AWS``
           - ``Custom``
           - ``Dev``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html#cfn-cloudformation-hookversion-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHookVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHookVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnHookVersionPropsMixin",
):
    '''The ``AWS::CloudFormation::HookVersion`` resource publishes new or first version of a Hook to the CloudFormation registry.

    For information about the CloudFormation registry, see `Managing extensions with the CloudFormation registry <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html>`_ in the *CloudFormation User Guide* .

    This resource type is not compatible with Guard and Lambda Hooks.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-hookversion.html
    :cloudformationResource: AWS::CloudFormation::HookVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_hook_version_props_mixin = cloudformation_mixins.CfnHookVersionPropsMixin(cloudformation_mixins.CfnHookVersionMixinProps(
            execution_role_arn="executionRoleArn",
            logging_config=cloudformation_mixins.CfnHookVersionPropsMixin.LoggingConfigProperty(
                log_group_name="logGroupName",
                log_role_arn="logRoleArn"
            ),
            schema_handler_package="schemaHandlerPackage",
            type_name="typeName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnHookVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::HookVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d88066c1e7a09e7516497c71ba292a91ad264028f98a39c99408e9d57d7e85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ef07c16b65ed4d51fd7b16dc24e1b207ff7d96da7fd6fdba7b3a801fc6edde9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ffb85180794faabb01c643edb3c148fdafe7477ec66c3a4513c75e63abbc77)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHookVersionMixinProps:
        return typing.cast(CfnHookVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnHookVersionPropsMixin.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName", "log_role_arn": "logRoleArn"},
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
            log_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LoggingConfig`` property type specifies logging configuration information for an extension.

            :param log_group_name: The Amazon CloudWatch Logs group to which CloudFormation sends error logging information when invoking the extension's handlers.
            :param log_role_arn: The Amazon Resource Name (ARN) of the role that CloudFormation should assume when sending log entries to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-hookversion-loggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                logging_config_property = cloudformation_mixins.CfnHookVersionPropsMixin.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a41edbb56e29c29806e6fe87fae8d7e3ab2cc9df865980197388f9980c982e2b)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument log_role_arn", value=log_role_arn, expected_type=type_hints["log_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_role_arn is not None:
                self._values["log_role_arn"] = log_role_arn

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon CloudWatch Logs group to which CloudFormation sends error logging information when invoking the extension's handlers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-hookversion-loggingconfig.html#cfn-cloudformation-hookversion-loggingconfig-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role that CloudFormation should assume when sending log entries to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-hookversion-loggingconfig.html#cfn-cloudformation-hookversion-loggingconfig-logrolearn
            '''
            result = self._values.get("log_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnLambdaHookMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "execution_role": "executionRole",
        "failure_mode": "failureMode",
        "hook_status": "hookStatus",
        "lambda_function": "lambdaFunction",
        "stack_filters": "stackFilters",
        "target_filters": "targetFilters",
        "target_operations": "targetOperations",
    },
)
class CfnLambdaHookMixinProps:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        execution_role: typing.Optional[builtins.str] = None,
        failure_mode: typing.Optional[builtins.str] = None,
        hook_status: typing.Optional[builtins.str] = None,
        lambda_function: typing.Optional[builtins.str] = None,
        stack_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLambdaHookPropsMixin.StackFiltersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLambdaHookPropsMixin.TargetFiltersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        target_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnLambdaHookPropsMixin.

        :param alias: The type name alias for the Hook. This alias must be unique per account and Region. The alias must be in the form ``Name1::Name2::Name3`` and must not begin with ``AWS`` . For example, ``Private::Lambda::MyTestHook`` .
        :param execution_role: The IAM role that the Hook assumes to invoke your Lambda function.
        :param failure_mode: Specifies how the Hook responds when the Lambda function invoked by the Hook returns a ``FAILED`` response. - ``FAIL`` : Prevents the action from proceeding. This is helpful for enforcing strict compliance or security policies. - ``WARN`` : Issues warnings to users but allows actions to continue. This is useful for non-critical validations or informational checks.
        :param hook_status: Specifies if the Hook is ``ENABLED`` or ``DISABLED`` . Default: - "ENABLED"
        :param lambda_function: Specifies the Lambda function for the Hook. You can use:. - The full Amazon Resource Name (ARN) without a suffix. - A qualified ARN with a version or alias suffix.
        :param stack_filters: Specifies the stack level filters for the Hook. Example stack level filter in JSON: ``"StackFilters": {"FilteringCriteria": "ALL", "StackNames": {"Exclude": [ "stack-1", "stack-2"]}}`` Example stack level filter in YAML: ``StackFilters: FilteringCriteria: ALL StackNames: Exclude: - stack-1 - stack-2``
        :param target_filters: Specifies the target filters for the Hook. Example target filter in JSON: ``"TargetFilters": {"Actions": [ "CREATE", "UPDATE", "DELETE" ]}`` Example target filter in YAML: ``TargetFilters: Actions: - CREATE - UPDATE - DELETE``
        :param target_operations: Specifies the list of operations the Hook is run against. For more information, see `Hook targets <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-concepts.html#hook-terms-hook-target>`_ in the *CloudFormation Hooks User Guide* . Valid values: ``STACK`` | ``RESOURCE`` | ``CHANGE_SET`` | ``CLOUD_CONTROL``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_lambda_hook_mixin_props = cloudformation_mixins.CfnLambdaHookMixinProps(
                alias="alias",
                execution_role="executionRole",
                failure_mode="failureMode",
                hook_status="hookStatus",
                lambda_function="lambdaFunction",
                stack_filters=cloudformation_mixins.CfnLambdaHookPropsMixin.StackFiltersProperty(
                    filtering_criteria="filteringCriteria",
                    stack_names=cloudformation_mixins.CfnLambdaHookPropsMixin.StackNamesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    ),
                    stack_roles=cloudformation_mixins.CfnLambdaHookPropsMixin.StackRolesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    )
                ),
                target_filters=cloudformation_mixins.CfnLambdaHookPropsMixin.TargetFiltersProperty(
                    actions=["actions"],
                    invocation_points=["invocationPoints"],
                    target_names=["targetNames"],
                    targets=[cloudformation_mixins.CfnLambdaHookPropsMixin.HookTargetProperty(
                        action="action",
                        invocation_point="invocationPoint",
                        target_name="targetName"
                    )]
                ),
                target_operations=["targetOperations"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c06249b15b252ffff22cea2e223c0fb1e80dc74302380a717168372e0e17487)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument failure_mode", value=failure_mode, expected_type=type_hints["failure_mode"])
            check_type(argname="argument hook_status", value=hook_status, expected_type=type_hints["hook_status"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
            check_type(argname="argument stack_filters", value=stack_filters, expected_type=type_hints["stack_filters"])
            check_type(argname="argument target_filters", value=target_filters, expected_type=type_hints["target_filters"])
            check_type(argname="argument target_operations", value=target_operations, expected_type=type_hints["target_operations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if failure_mode is not None:
            self._values["failure_mode"] = failure_mode
        if hook_status is not None:
            self._values["hook_status"] = hook_status
        if lambda_function is not None:
            self._values["lambda_function"] = lambda_function
        if stack_filters is not None:
            self._values["stack_filters"] = stack_filters
        if target_filters is not None:
            self._values["target_filters"] = target_filters
        if target_operations is not None:
            self._values["target_operations"] = target_operations

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''The type name alias for the Hook. This alias must be unique per account and Region.

        The alias must be in the form ``Name1::Name2::Name3`` and must not begin with ``AWS`` . For example, ``Private::Lambda::MyTestHook`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html#cfn-cloudformation-lambdahook-alias
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[builtins.str]:
        '''The IAM role that the Hook assumes to invoke your Lambda function.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html#cfn-cloudformation-lambdahook-executionrole
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies how the Hook responds when the Lambda function invoked by the Hook returns a ``FAILED`` response.

        - ``FAIL`` : Prevents the action from proceeding. This is helpful for enforcing strict compliance or security policies.
        - ``WARN`` : Issues warnings to users but allows actions to continue. This is useful for non-critical validations or informational checks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html#cfn-cloudformation-lambdahook-failuremode
        '''
        result = self._values.get("failure_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hook_status(self) -> typing.Optional[builtins.str]:
        '''Specifies if the Hook is ``ENABLED`` or ``DISABLED`` .

        :default: - "ENABLED"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html#cfn-cloudformation-lambdahook-hookstatus
        '''
        result = self._values.get("hook_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_function(self) -> typing.Optional[builtins.str]:
        '''Specifies the Lambda function for the Hook. You can use:.

        - The full Amazon Resource Name (ARN) without a suffix.
        - A qualified ARN with a version or alias suffix.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html#cfn-cloudformation-lambdahook-lambdafunction
        '''
        result = self._values.get("lambda_function")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.StackFiltersProperty"]]:
        '''Specifies the stack level filters for the Hook.

        Example stack level filter in JSON:

        ``"StackFilters": {"FilteringCriteria": "ALL", "StackNames": {"Exclude": [ "stack-1", "stack-2"]}}``

        Example stack level filter in YAML:

        ``StackFilters: FilteringCriteria: ALL StackNames: Exclude: - stack-1 - stack-2``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html#cfn-cloudformation-lambdahook-stackfilters
        '''
        result = self._values.get("stack_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.StackFiltersProperty"]], result)

    @builtins.property
    def target_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.TargetFiltersProperty"]]:
        '''Specifies the target filters for the Hook.

        Example target filter in JSON:

        ``"TargetFilters": {"Actions": [ "CREATE", "UPDATE", "DELETE" ]}``

        Example target filter in YAML:

        ``TargetFilters: Actions: - CREATE - UPDATE - DELETE``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html#cfn-cloudformation-lambdahook-targetfilters
        '''
        result = self._values.get("target_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.TargetFiltersProperty"]], result)

    @builtins.property
    def target_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of operations the Hook is run against.

        For more information, see `Hook targets <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-concepts.html#hook-terms-hook-target>`_ in the *CloudFormation Hooks User Guide* .

        Valid values: ``STACK`` | ``RESOURCE`` | ``CHANGE_SET`` | ``CLOUD_CONTROL``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html#cfn-cloudformation-lambdahook-targetoperations
        '''
        result = self._values.get("target_operations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLambdaHookMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLambdaHookPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnLambdaHookPropsMixin",
):
    '''The ``AWS::CloudFormation::LambdaHook`` resource creates and activates a Lambda Hook.

    You can use a Lambda Hook to evaluate your resources before allowing stack operations. This resource forwards requests for resource evaluation to a Lambda function.

    For more information, see `Lambda Hooks <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/lambda-hooks.html>`_ in the *CloudFormation Hooks User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-lambdahook.html
    :cloudformationResource: AWS::CloudFormation::LambdaHook
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_lambda_hook_props_mixin = cloudformation_mixins.CfnLambdaHookPropsMixin(cloudformation_mixins.CfnLambdaHookMixinProps(
            alias="alias",
            execution_role="executionRole",
            failure_mode="failureMode",
            hook_status="hookStatus",
            lambda_function="lambdaFunction",
            stack_filters=cloudformation_mixins.CfnLambdaHookPropsMixin.StackFiltersProperty(
                filtering_criteria="filteringCriteria",
                stack_names=cloudformation_mixins.CfnLambdaHookPropsMixin.StackNamesProperty(
                    exclude=["exclude"],
                    include=["include"]
                ),
                stack_roles=cloudformation_mixins.CfnLambdaHookPropsMixin.StackRolesProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            ),
            target_filters=cloudformation_mixins.CfnLambdaHookPropsMixin.TargetFiltersProperty(
                actions=["actions"],
                invocation_points=["invocationPoints"],
                target_names=["targetNames"],
                targets=[cloudformation_mixins.CfnLambdaHookPropsMixin.HookTargetProperty(
                    action="action",
                    invocation_point="invocationPoint",
                    target_name="targetName"
                )]
            ),
            target_operations=["targetOperations"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLambdaHookMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::LambdaHook``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f9a4f0c826a6fc3aa5cc8692725811cb0d77dd00e17e314c8fc12e63e0d76d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc2bc97581c6861ade19e87a51626f749e4a4ec1877b77c45738b49beb292d40)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3182411f26a8435a56e1b0f927dcfd26a672c1a34825ec6f4326b58a347ea6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLambdaHookMixinProps:
        return typing.cast(CfnLambdaHookMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnLambdaHookPropsMixin.HookTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "invocation_point": "invocationPoint",
            "target_name": "targetName",
        },
    )
    class HookTargetProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            invocation_point: typing.Optional[builtins.str] = None,
            target_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Hook targets are the destination where hooks will be invoked against.

            :param action: Target actions are the type of operation hooks will be executed at.
            :param invocation_point: Invocation points are the point in provisioning workflow where hooks will be executed.
            :param target_name: Type name of hook target. Hook targets are the destination where hooks will be invoked against.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-hooktarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                hook_target_property = cloudformation_mixins.CfnLambdaHookPropsMixin.HookTargetProperty(
                    action="action",
                    invocation_point="invocationPoint",
                    target_name="targetName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1bf38b9644c9bbfef34b8031ec03393ce0d68694b7e3a8cd3902bd5fa72878d)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument invocation_point", value=invocation_point, expected_type=type_hints["invocation_point"])
                check_type(argname="argument target_name", value=target_name, expected_type=type_hints["target_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if invocation_point is not None:
                self._values["invocation_point"] = invocation_point
            if target_name is not None:
                self._values["target_name"] = target_name

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''Target actions are the type of operation hooks will be executed at.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-hooktarget.html#cfn-cloudformation-lambdahook-hooktarget-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def invocation_point(self) -> typing.Optional[builtins.str]:
            '''Invocation points are the point in provisioning workflow where hooks will be executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-hooktarget.html#cfn-cloudformation-lambdahook-hooktarget-invocationpoint
            '''
            result = self._values.get("invocation_point")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_name(self) -> typing.Optional[builtins.str]:
            '''Type name of hook target.

            Hook targets are the destination where hooks will be invoked against.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-hooktarget.html#cfn-cloudformation-lambdahook-hooktarget-targetname
            '''
            result = self._values.get("target_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HookTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnLambdaHookPropsMixin.StackFiltersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "filtering_criteria": "filteringCriteria",
            "stack_names": "stackNames",
            "stack_roles": "stackRoles",
        },
    )
    class StackFiltersProperty:
        def __init__(
            self,
            *,
            filtering_criteria: typing.Optional[builtins.str] = None,
            stack_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLambdaHookPropsMixin.StackNamesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stack_roles: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLambdaHookPropsMixin.StackRolesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``StackFilters`` property type specifies stack level filters for a Hook.

            The ``StackNames`` or ``StackRoles`` properties are optional. However, you must specify at least one of these properties.

            For more information, see `CloudFormation Hooks stack level filters <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-stack-level-filtering.html>`_ .

            :param filtering_criteria: The filtering criteria. - All stack names and stack roles ( ``All`` ): The Hook will only be invoked when all specified filters match. - Any stack names and stack roles ( ``Any`` ): The Hook will be invoked if at least one of the specified filters match. Default: - "ALL"
            :param stack_names: Includes or excludes specific stacks from Hook invocations.
            :param stack_roles: Includes or excludes specific stacks from Hook invocations based on their associated IAM roles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stackfilters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                stack_filters_property = cloudformation_mixins.CfnLambdaHookPropsMixin.StackFiltersProperty(
                    filtering_criteria="filteringCriteria",
                    stack_names=cloudformation_mixins.CfnLambdaHookPropsMixin.StackNamesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    ),
                    stack_roles=cloudformation_mixins.CfnLambdaHookPropsMixin.StackRolesProperty(
                        exclude=["exclude"],
                        include=["include"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22ed93446cda2e9b78329fd0c50d7d750c07913cbafa40b29ff8fa1b5151a19b)
                check_type(argname="argument filtering_criteria", value=filtering_criteria, expected_type=type_hints["filtering_criteria"])
                check_type(argname="argument stack_names", value=stack_names, expected_type=type_hints["stack_names"])
                check_type(argname="argument stack_roles", value=stack_roles, expected_type=type_hints["stack_roles"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filtering_criteria is not None:
                self._values["filtering_criteria"] = filtering_criteria
            if stack_names is not None:
                self._values["stack_names"] = stack_names
            if stack_roles is not None:
                self._values["stack_roles"] = stack_roles

        @builtins.property
        def filtering_criteria(self) -> typing.Optional[builtins.str]:
            '''The filtering criteria.

            - All stack names and stack roles ( ``All`` ): The Hook will only be invoked when all specified filters match.
            - Any stack names and stack roles ( ``Any`` ): The Hook will be invoked if at least one of the specified filters match.

            :default: - "ALL"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stackfilters.html#cfn-cloudformation-lambdahook-stackfilters-filteringcriteria
            '''
            result = self._values.get("filtering_criteria")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stack_names(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.StackNamesProperty"]]:
            '''Includes or excludes specific stacks from Hook invocations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stackfilters.html#cfn-cloudformation-lambdahook-stackfilters-stacknames
            '''
            result = self._values.get("stack_names")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.StackNamesProperty"]], result)

        @builtins.property
        def stack_roles(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.StackRolesProperty"]]:
            '''Includes or excludes specific stacks from Hook invocations based on their associated IAM roles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stackfilters.html#cfn-cloudformation-lambdahook-stackfilters-stackroles
            '''
            result = self._values.get("stack_roles")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.StackRolesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackFiltersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnLambdaHookPropsMixin.StackNamesProperty",
        jsii_struct_bases=[],
        name_mapping={"exclude": "exclude", "include": "include"},
    )
    class StackNamesProperty:
        def __init__(
            self,
            *,
            exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            include: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the stack names for the ``StackFilters`` property type to include or exclude specific stacks from Hook invocations.

            For more information, see `CloudFormation Hooks stack level filters <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-stack-level-filtering.html>`_ .

            :param exclude: The stack names to exclude. All stacks except those listed here will invoke the Hook.
            :param include: The stack names to include. Only the stacks specified in this list will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stacknames.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                stack_names_property = cloudformation_mixins.CfnLambdaHookPropsMixin.StackNamesProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e7c46b4a8126adea9a69a069264eb2c473e2a7160c09cf599cd9f6013cef55d)
                check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude is not None:
                self._values["exclude"] = exclude
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The stack names to exclude.

            All stacks except those listed here will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stacknames.html#cfn-cloudformation-lambdahook-stacknames-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The stack names to include.

            Only the stacks specified in this list will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stacknames.html#cfn-cloudformation-lambdahook-stacknames-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackNamesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnLambdaHookPropsMixin.StackRolesProperty",
        jsii_struct_bases=[],
        name_mapping={"exclude": "exclude", "include": "include"},
    )
    class StackRolesProperty:
        def __init__(
            self,
            *,
            exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            include: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the stack roles for the ``StackFilters`` property type to include or exclude specific stacks from Hook invocations based on their associated IAM roles.

            For more information, see `CloudFormation Hooks stack level filters <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-stack-level-filtering.html>`_ .

            :param exclude: The IAM role ARNs for stacks you want to exclude. The Hook will be invoked on all stacks except those initiated by the specified roles.
            :param include: The IAM role ARNs to target stacks associated with these roles. Only stack operations initiated by these roles will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stackroles.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                stack_roles_property = cloudformation_mixins.CfnLambdaHookPropsMixin.StackRolesProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__525c022dbe8fd435bf17946d02b75bf2eaa7b3f2ca41294586ae21de41472733)
                check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude is not None:
                self._values["exclude"] = exclude
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IAM role ARNs for stacks you want to exclude.

            The Hook will be invoked on all stacks except those initiated by the specified roles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stackroles.html#cfn-cloudformation-lambdahook-stackroles-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IAM role ARNs to target stacks associated with these roles.

            Only stack operations initiated by these roles will invoke the Hook.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-stackroles.html#cfn-cloudformation-lambdahook-stackroles-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackRolesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnLambdaHookPropsMixin.TargetFiltersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "invocation_points": "invocationPoints",
            "target_names": "targetNames",
            "targets": "targets",
        },
    )
    class TargetFiltersProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            invocation_points: typing.Optional[typing.Sequence[builtins.str]] = None,
            target_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLambdaHookPropsMixin.HookTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``TargetFilters`` property type specifies the target filters for the Hook.

            For more information, see `CloudFormation Hook target filters <https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/hooks-target-filtering.html>`_ .

            :param actions: List of actions that the hook is going to target.
            :param invocation_points: List of invocation points that the hook is going to target.
            :param target_names: List of type names that the hook is going to target.
            :param targets: List of hook targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-targetfilters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                target_filters_property = cloudformation_mixins.CfnLambdaHookPropsMixin.TargetFiltersProperty(
                    actions=["actions"],
                    invocation_points=["invocationPoints"],
                    target_names=["targetNames"],
                    targets=[cloudformation_mixins.CfnLambdaHookPropsMixin.HookTargetProperty(
                        action="action",
                        invocation_point="invocationPoint",
                        target_name="targetName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1de3eb2074d0dab8c945e1c42f3149069d0f19d1a6bb5c6cf399ae90fe43f4c5)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument invocation_points", value=invocation_points, expected_type=type_hints["invocation_points"])
                check_type(argname="argument target_names", value=target_names, expected_type=type_hints["target_names"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if invocation_points is not None:
                self._values["invocation_points"] = invocation_points
            if target_names is not None:
                self._values["target_names"] = target_names
            if targets is not None:
                self._values["targets"] = targets

        @builtins.property
        def actions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of actions that the hook is going to target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-targetfilters.html#cfn-cloudformation-lambdahook-targetfilters-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def invocation_points(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of invocation points that the hook is going to target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-targetfilters.html#cfn-cloudformation-lambdahook-targetfilters-invocationpoints
            '''
            result = self._values.get("invocation_points")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def target_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of type names that the hook is going to target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-targetfilters.html#cfn-cloudformation-lambdahook-targetfilters-targetnames
            '''
            result = self._values.get("target_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.HookTargetProperty"]]]]:
            '''List of hook targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-lambdahook-targetfilters.html#cfn-cloudformation-lambdahook-targetfilters-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLambdaHookPropsMixin.HookTargetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetFiltersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnMacroMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "function_name": "functionName",
        "log_group_name": "logGroupName",
        "log_role_arn": "logRoleArn",
        "name": "name",
    },
)
class CfnMacroMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        function_name: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_role_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMacroPropsMixin.

        :param description: A description of the macro.
        :param function_name: The Amazon Resource Name (ARN) of the underlying Lambda function that you want CloudFormation to invoke when the macro is run.
        :param log_group_name: The CloudWatch Logs group to which CloudFormation sends error logging information when invoking the macro's underlying Lambda function. This will be an existing CloudWatch Logs LogGroup. Neither CloudFormation or Lambda will create the group.
        :param log_role_arn: The ARN of the role CloudFormation should assume when sending log entries to CloudWatch Logs .
        :param name: The name of the macro. The name of the macro must be unique across all macros in the account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_macro_mixin_props = cloudformation_mixins.CfnMacroMixinProps(
                description="description",
                function_name="functionName",
                log_group_name="logGroupName",
                log_role_arn="logRoleArn",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70995a79d21f9cb0016a3cc418bf8c38e6a5a6ec8f3f5b816c1844503ad9574)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_role_arn", value=log_role_arn, expected_type=type_hints["log_role_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if function_name is not None:
            self._values["function_name"] = function_name
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_role_arn is not None:
            self._values["log_role_arn"] = log_role_arn
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the macro.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the underlying Lambda function that you want CloudFormation to invoke when the macro is run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-functionname
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The CloudWatch Logs group to which CloudFormation sends error logging information when invoking the macro's underlying Lambda function.

        This will be an existing CloudWatch Logs LogGroup. Neither CloudFormation or Lambda will create the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the role CloudFormation should assume when sending log entries to CloudWatch Logs .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-logrolearn
        '''
        result = self._values.get("log_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the macro.

        The name of the macro must be unique across all macros in the account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html#cfn-cloudformation-macro-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMacroMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMacroPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnMacroPropsMixin",
):
    '''The ``AWS::CloudFormation::Macro`` resource is a CloudFormation resource type that creates a CloudFormation macro to perform custom processing on CloudFormation templates.

    For more information, see `Perform custom processing on CloudFormation templates with template macros <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html>`_ in the *CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-macro.html
    :cloudformationResource: AWS::CloudFormation::Macro
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_macro_props_mixin = cloudformation_mixins.CfnMacroPropsMixin(cloudformation_mixins.CfnMacroMixinProps(
            description="description",
            function_name="functionName",
            log_group_name="logGroupName",
            log_role_arn="logRoleArn",
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMacroMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::Macro``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0092f3cb79b7804c3af6db1deec32acf1d389fae7a50419ba65125d58fe74b8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd9d5433926429f8662589ff067205229ceee6429a7e0766a2c65cd7dfe24146)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cd2087f2a9fe6d407686060c7e7fc0404ec65306142db17565ac75a4b95060)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMacroMixinProps:
        return typing.cast(CfnMacroMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnModuleDefaultVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "module_name": "moduleName",
        "version_id": "versionId",
    },
)
class CfnModuleDefaultVersionMixinProps:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        module_name: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnModuleDefaultVersionPropsMixin.

        :param arn: The Amazon Resource Name (ARN) of the module version to set as the default version. Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .
        :param module_name: The name of the module. Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .
        :param version_id: The ID for the specific version of the module. Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_module_default_version_mixin_props = cloudformation_mixins.CfnModuleDefaultVersionMixinProps(
                arn="arn",
                module_name="moduleName",
                version_id="versionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5944749315c89043c68e202f37035cd4f6694c2fbec03a26263349eb37bd4b3)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if module_name is not None:
            self._values["module_name"] = module_name
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the module version to set as the default version.

        Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def module_name(self) -> typing.Optional[builtins.str]:
        '''The name of the module.

        Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-modulename
        '''
        result = self._values.get("module_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''The ID for the specific version of the module.

        Conditional: You must specify either ``Arn`` , or ``ModuleName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html#cfn-cloudformation-moduledefaultversion-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModuleDefaultVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnModuleDefaultVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnModuleDefaultVersionPropsMixin",
):
    '''Specifies the default version of a module.

    The default version of the module will be used in CloudFormation operations for this account and Region.

    For more information, see `Create reusable resource configurations that can be included across templates with CloudFormation modules <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/modules.html>`_ in the *CloudFormation User Guide* .

    For information about the CloudFormation registry, see `Managing extensions with the CloudFormation registry <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html>`_ in the *CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduledefaultversion.html
    :cloudformationResource: AWS::CloudFormation::ModuleDefaultVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_module_default_version_props_mixin = cloudformation_mixins.CfnModuleDefaultVersionPropsMixin(cloudformation_mixins.CfnModuleDefaultVersionMixinProps(
            arn="arn",
            module_name="moduleName",
            version_id="versionId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnModuleDefaultVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::ModuleDefaultVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a7d727641781ce41c14f41d95084b62c9f33d46b2a38e0970d1ddbcc202c79b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ba28c1885328e89802e770a89221f9c7f20b235df66549633b8895c5d8be5df)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b91e29c9b6689fbe1f053086239983d632a09e2afa8bcdbfd241e783178844)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnModuleDefaultVersionMixinProps:
        return typing.cast(CfnModuleDefaultVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnModuleVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"module_name": "moduleName", "module_package": "modulePackage"},
)
class CfnModuleVersionMixinProps:
    def __init__(
        self,
        *,
        module_name: typing.Optional[builtins.str] = None,
        module_package: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnModuleVersionPropsMixin.

        :param module_name: The name of the module being registered.
        :param module_package: A URL to the S3 bucket for the package that contains the template fragment and schema files for the module version to register. For more information, see `Module structure and requirements <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/modules-structure.html>`_ in the *CloudFormation Command Line Interface (CLI) User Guide* . .. epigraph:: To register the module version, you must have ``s3:GetObject`` permissions to access the S3 objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_module_version_mixin_props = cloudformation_mixins.CfnModuleVersionMixinProps(
                module_name="moduleName",
                module_package="modulePackage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde2a44021c4ab4489723db6a6c4af717aca8f520ec7e266f8b5c720b2c4e37b)
            check_type(argname="argument module_name", value=module_name, expected_type=type_hints["module_name"])
            check_type(argname="argument module_package", value=module_package, expected_type=type_hints["module_package"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if module_name is not None:
            self._values["module_name"] = module_name
        if module_package is not None:
            self._values["module_package"] = module_package

    @builtins.property
    def module_name(self) -> typing.Optional[builtins.str]:
        '''The name of the module being registered.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulename
        '''
        result = self._values.get("module_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def module_package(self) -> typing.Optional[builtins.str]:
        '''A URL to the S3 bucket for the package that contains the template fragment and schema files for the module version to register.

        For more information, see `Module structure and requirements <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/modules-structure.html>`_ in the *CloudFormation Command Line Interface (CLI) User Guide* .
        .. epigraph::

           To register the module version, you must have ``s3:GetObject`` permissions to access the S3 objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html#cfn-cloudformation-moduleversion-modulepackage
        '''
        result = self._values.get("module_package")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnModuleVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnModuleVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnModuleVersionPropsMixin",
):
    '''The ``AWS::CloudFormation::ModuleVersion`` resource registers the specified version of the module with the CloudFormation registry.

    Registering a module makes it available for use in CloudFormation templates in your AWS account and Region.

    For more information, see `Create reusable resource configurations that can be included across templates with CloudFormation modules <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/modules.html>`_ in the *CloudFormation User Guide* .

    For information about the CloudFormation registry, see `Managing extensions with the CloudFormation registry <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html>`_ in the *CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-moduleversion.html
    :cloudformationResource: AWS::CloudFormation::ModuleVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_module_version_props_mixin = cloudformation_mixins.CfnModuleVersionPropsMixin(cloudformation_mixins.CfnModuleVersionMixinProps(
            module_name="moduleName",
            module_package="modulePackage"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnModuleVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::ModuleVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632e9388780ed9b70879996eca8d96c461ca4552fa51e603ddfc6008ee7a2675)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f34f47bfa50cafff6121a81c811fb303d4065e96bd36ccda670faaedfa2d5c0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b4c9f2d1e1263ef172ce0536d953310a3d1087e4e9838b2ba9763ce21d4c302)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnModuleVersionMixinProps:
        return typing.cast(CfnModuleVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnPublicTypeVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "log_delivery_bucket": "logDeliveryBucket",
        "public_version_number": "publicVersionNumber",
        "type": "type",
        "type_name": "typeName",
    },
)
class CfnPublicTypeVersionMixinProps:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        log_delivery_bucket: typing.Optional[builtins.str] = None,
        public_version_number: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPublicTypeVersionPropsMixin.

        :param arn: The Amazon Resource Number (ARN) of the extension. Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .
        :param log_delivery_bucket: The S3 bucket to which CloudFormation delivers the contract test execution logs. CloudFormation delivers the logs by the time contract testing has completed and the extension has been assigned a test type status of ``PASSED`` or ``FAILED`` . The user initiating the stack operation must be able to access items in the specified S3 bucket. Specifically, the user needs the following permissions: - s3:GetObject - s3:PutObject
        :param public_version_number: The version number to assign to this version of the extension. Use the following format, and adhere to semantic versioning when assigning a version number to your extension: ``MAJOR.MINOR.PATCH`` For more information, see `Semantic Versioning 2.0.0 <https://docs.aws.amazon.com/https://semver.org/>`_ . If you don't specify a version number, CloudFormation increments the version number by one minor version release. You cannot specify a version number the first time you publish a type. CloudFormation automatically sets the first version number to be ``1.0.0`` .
        :param type: The type of the extension to test. Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .
        :param type_name: The name of the extension to test. Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_public_type_version_mixin_props = cloudformation_mixins.CfnPublicTypeVersionMixinProps(
                arn="arn",
                log_delivery_bucket="logDeliveryBucket",
                public_version_number="publicVersionNumber",
                type="type",
                type_name="typeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2eb8092c3a922c1b941501013d3616d0c15819ef89cef4be65b5a4f8b37ee6)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument log_delivery_bucket", value=log_delivery_bucket, expected_type=type_hints["log_delivery_bucket"])
            check_type(argname="argument public_version_number", value=public_version_number, expected_type=type_hints["public_version_number"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if log_delivery_bucket is not None:
            self._values["log_delivery_bucket"] = log_delivery_bucket
        if public_version_number is not None:
            self._values["public_version_number"] = public_version_number
        if type is not None:
            self._values["type"] = type
        if type_name is not None:
            self._values["type_name"] = type_name

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the extension.

        Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-arn
        '''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery_bucket(self) -> typing.Optional[builtins.str]:
        '''The S3 bucket to which CloudFormation delivers the contract test execution logs.

        CloudFormation delivers the logs by the time contract testing has completed and the extension has been assigned a test type status of ``PASSED`` or ``FAILED`` .

        The user initiating the stack operation must be able to access items in the specified S3 bucket. Specifically, the user needs the following permissions:

        - s3:GetObject
        - s3:PutObject

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-logdeliverybucket
        '''
        result = self._values.get("log_delivery_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_version_number(self) -> typing.Optional[builtins.str]:
        '''The version number to assign to this version of the extension.

        Use the following format, and adhere to semantic versioning when assigning a version number to your extension:

        ``MAJOR.MINOR.PATCH``

        For more information, see `Semantic Versioning 2.0.0 <https://docs.aws.amazon.com/https://semver.org/>`_ .

        If you don't specify a version number, CloudFormation increments the version number by one minor version release.

        You cannot specify a version number the first time you publish a type. CloudFormation automatically sets the first version number to be ``1.0.0`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-publicversionnumber
        '''
        result = self._values.get("public_version_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the extension to test.

        Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the extension to test.

        Conditional: You must specify ``Arn`` , or ``TypeName`` and ``Type`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html#cfn-cloudformation-publictypeversion-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublicTypeVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPublicTypeVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnPublicTypeVersionPropsMixin",
):
    '''The ``AWS::CloudFormation::PublicTypeVersion`` resource tests and publishes a registered extension as a public, third-party extension.

    CloudFormation first tests the extension to make sure it meets all necessary requirements for being published in the CloudFormation registry. If it does, CloudFormation then publishes it to the registry as a public third-party extension in this Region. Public extensions are available for use by all CloudFormation users.

    - For resource types, testing includes passing all contracts tests defined for the type.
    - For modules, testing includes determining if the module's model meets all necessary requirements.

    For more information, see `Testing your public extension prior to publishing <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html#publish-extension-testing>`_ in the *CloudFormation Command Line Interface (CLI) User Guide* .

    If you don't specify a version, CloudFormation uses the default version of the extension in your account and Region for testing.

    To perform testing, CloudFormation assumes the execution role specified when the type was registered.

    An extension must have a test status of ``PASSED`` before it can be published. For more information, see `Publishing extensions to make them available for public use <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html>`_ in the *CloudFormation Command Line Interface (CLI) User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publictypeversion.html
    :cloudformationResource: AWS::CloudFormation::PublicTypeVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_public_type_version_props_mixin = cloudformation_mixins.CfnPublicTypeVersionPropsMixin(cloudformation_mixins.CfnPublicTypeVersionMixinProps(
            arn="arn",
            log_delivery_bucket="logDeliveryBucket",
            public_version_number="publicVersionNumber",
            type="type",
            type_name="typeName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPublicTypeVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::PublicTypeVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8a5239fb158d4330d99d26b344da738c8c32db8dc54203a9747a6ea5e89f5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcc72cf2d18996a0e4bb573e077121c0a8e134744f656c4de62ac056b9559e63)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859b5e82cbf2d6fa0fc62d451cfd3ed90d894f71003dbd386640b202a13a07e0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPublicTypeVersionMixinProps:
        return typing.cast(CfnPublicTypeVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnPublisherMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_terms_and_conditions": "acceptTermsAndConditions",
        "connection_arn": "connectionArn",
    },
)
class CfnPublisherMixinProps:
    def __init__(
        self,
        *,
        accept_terms_and_conditions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        connection_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPublisherPropsMixin.

        :param accept_terms_and_conditions: Whether you accept the `Terms and Conditions <https://docs.aws.amazon.com/https://cloudformation-registry-documents.s3.amazonaws.com/Terms_and_Conditions_for_AWS_CloudFormation_Registry_Publishers.pdf>`_ for publishing extensions in the CloudFormation registry. You must accept the terms and conditions in order to register to publish public extensions to the CloudFormation registry. The default is ``false`` .
        :param connection_arn: If you are using a Bitbucket or GitHub account for identity verification, the Amazon Resource Name (ARN) for your connection to that account. For more information, see `Prerequisite: Registering your account to publish CloudFormation extensions <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html#publish-extension-prereqs>`_ in the *AWS CloudFormation Command Line Interface (CLI) User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_publisher_mixin_props = cloudformation_mixins.CfnPublisherMixinProps(
                accept_terms_and_conditions=False,
                connection_arn="connectionArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48d91e0b0e3a64273daffa22c162b0ac6f0e01d16b922c032ed7b37a4481e50)
            check_type(argname="argument accept_terms_and_conditions", value=accept_terms_and_conditions, expected_type=type_hints["accept_terms_and_conditions"])
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_terms_and_conditions is not None:
            self._values["accept_terms_and_conditions"] = accept_terms_and_conditions
        if connection_arn is not None:
            self._values["connection_arn"] = connection_arn

    @builtins.property
    def accept_terms_and_conditions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether you accept the `Terms and Conditions <https://docs.aws.amazon.com/https://cloudformation-registry-documents.s3.amazonaws.com/Terms_and_Conditions_for_AWS_CloudFormation_Registry_Publishers.pdf>`_ for publishing extensions in the CloudFormation registry. You must accept the terms and conditions in order to register to publish public extensions to the CloudFormation registry.

        The default is ``false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html#cfn-cloudformation-publisher-accepttermsandconditions
        '''
        result = self._values.get("accept_terms_and_conditions")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''If you are using a Bitbucket or GitHub account for identity verification, the Amazon Resource Name (ARN) for your connection to that account.

        For more information, see `Prerequisite: Registering your account to publish CloudFormation extensions <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.html#publish-extension-prereqs>`_ in the *AWS CloudFormation Command Line Interface (CLI) User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html#cfn-cloudformation-publisher-connectionarn
        '''
        result = self._values.get("connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublisherMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPublisherPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnPublisherPropsMixin",
):
    '''The ``AWS::CloudFormation::Publisher`` resource registers your account as a publisher of public extensions in the CloudFormation registry.

    Public extensions are available for use by all CloudFormation users.

    For information on requirements for registering as a public extension publisher, see `Publishing extensions to make them available for public use <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/publish-extension.htm>`_ in the *CloudFormation Command Line Interface (CLI) User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-publisher.html
    :cloudformationResource: AWS::CloudFormation::Publisher
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_publisher_props_mixin = cloudformation_mixins.CfnPublisherPropsMixin(cloudformation_mixins.CfnPublisherMixinProps(
            accept_terms_and_conditions=False,
            connection_arn="connectionArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPublisherMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::Publisher``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a69f0c17f518810bfddc338355c92b82f5d57eb2b8e2bace3ce3a83d731f751)
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
            type_hints = typing.get_type_hints(_typecheckingstub__437ce047d8a538f90b5ab464b302e620436034ca12842d0078875615c6b14f57)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d33877b7d8fe013b959c299ec91fe6d830622f72bce5c89a8b8a060a4b90923)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPublisherMixinProps:
        return typing.cast(CfnPublisherMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnResourceDefaultVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "type_name": "typeName",
        "type_version_arn": "typeVersionArn",
        "version_id": "versionId",
    },
)
class CfnResourceDefaultVersionMixinProps:
    def __init__(
        self,
        *,
        type_name: typing.Optional[builtins.str] = None,
        type_version_arn: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourceDefaultVersionPropsMixin.

        :param type_name: The name of the resource. Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param type_version_arn: The Amazon Resource Name (ARN) of the resource version. Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .
        :param version_id: The ID of a specific version of the resource. The version ID is the value at the end of the Amazon Resource Name (ARN) assigned to the resource version when it's registered. Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_resource_default_version_mixin_props = cloudformation_mixins.CfnResourceDefaultVersionMixinProps(
                type_name="typeName",
                type_version_arn="typeVersionArn",
                version_id="versionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82505ab6eb872456580b040b982563c28fa47b856c019dd282064adbb78beefc)
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument type_version_arn", value=type_version_arn, expected_type=type_hints["type_version_arn"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type_name is not None:
            self._values["type_name"] = type_name
        if type_version_arn is not None:
            self._values["type_version_arn"] = type_version_arn
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource.

        Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_version_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resource version.

        Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-typeversionarn
        '''
        result = self._values.get("type_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''The ID of a specific version of the resource.

        The version ID is the value at the end of the Amazon Resource Name (ARN) assigned to the resource version when it's registered.

        Conditional: You must specify either ``TypeVersionArn`` , or ``TypeName`` and ``VersionId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html#cfn-cloudformation-resourcedefaultversion-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceDefaultVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceDefaultVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnResourceDefaultVersionPropsMixin",
):
    '''The ``AWS::CloudFormation::ResourceDefaultVersion`` resource specifies the default version of a resource.

    The default version of a resource will be used in CloudFormation operations.

    For information about the CloudFormation registry, see `Managing extensions with the CloudFormation registry <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html>`_ in the *CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourcedefaultversion.html
    :cloudformationResource: AWS::CloudFormation::ResourceDefaultVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_resource_default_version_props_mixin = cloudformation_mixins.CfnResourceDefaultVersionPropsMixin(cloudformation_mixins.CfnResourceDefaultVersionMixinProps(
            type_name="typeName",
            type_version_arn="typeVersionArn",
            version_id="versionId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceDefaultVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::ResourceDefaultVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9dbc74f4956367064ccea1e371ec9ecff905829be73575efa1f13e95df38e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__718699835598d423e28e2f850da4973658a219b462d9018dbb10ddaf42d30cc8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d88892c6165569eb225916e5dc05f92893172f9ed6935b450c8d9b7dea0dff9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceDefaultVersionMixinProps:
        return typing.cast(CfnResourceDefaultVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnResourceVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role_arn": "executionRoleArn",
        "logging_config": "loggingConfig",
        "schema_handler_package": "schemaHandlerPackage",
        "type_name": "typeName",
    },
)
class CfnResourceVersionMixinProps:
    def __init__(
        self,
        *,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceVersionPropsMixin.LoggingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schema_handler_package: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourceVersionPropsMixin.

        :param execution_role_arn: The Amazon Resource Name (ARN) of the IAM role for CloudFormation to assume when invoking the resource. If your resource calls AWS APIs in any of its handlers, you must create an IAM execution role that includes the necessary permissions to call those AWS APIs, and provision that execution role in your account. When CloudFormation needs to invoke the resource type handler, CloudFormation assumes this execution role to create a temporary session token, which it then passes to the resource type handler, thereby supplying your resource type with the appropriate credentials.
        :param logging_config: Logging configuration information for a resource.
        :param schema_handler_package: A URL to the S3 bucket for the resource project package that contains the necessary files for the resource you want to register. For information on generating a schema handler package, see `Modeling resource types to use with CloudFormation <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-model.html>`_ in the *CloudFormation Command Line Interface (CLI) User Guide* . .. epigraph:: To register the resource version, you must have ``s3:GetObject`` permissions to access the S3 objects.
        :param type_name: The name of the resource being registered. We recommend that resource names adhere to the following pattern: *company_or_organization* :: *service* :: *type* . .. epigraph:: The following organization namespaces are reserved and can't be used in your resource names: - ``Alexa`` - ``AMZN`` - ``Amazon`` - ``AWS`` - ``Custom`` - ``Dev``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_resource_version_mixin_props = cloudformation_mixins.CfnResourceVersionMixinProps(
                execution_role_arn="executionRoleArn",
                logging_config=cloudformation_mixins.CfnResourceVersionPropsMixin.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                ),
                schema_handler_package="schemaHandlerPackage",
                type_name="typeName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453b227b1207da7b32b7a1eea867b29fdc41de631528af43c8e9be6a247840b0)
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument schema_handler_package", value=schema_handler_package, expected_type=type_hints["schema_handler_package"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if schema_handler_package is not None:
            self._values["schema_handler_package"] = schema_handler_package
        if type_name is not None:
            self._values["type_name"] = type_name

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role for CloudFormation to assume when invoking the resource.

        If your resource calls AWS APIs in any of its handlers, you must create an IAM execution role that includes the necessary permissions to call those AWS APIs, and provision that execution role in your account. When CloudFormation needs to invoke the resource type handler, CloudFormation assumes this execution role to create a temporary session token, which it then passes to the resource type handler, thereby supplying your resource type with the appropriate credentials.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceVersionPropsMixin.LoggingConfigProperty"]]:
        '''Logging configuration information for a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-loggingconfig
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceVersionPropsMixin.LoggingConfigProperty"]], result)

    @builtins.property
    def schema_handler_package(self) -> typing.Optional[builtins.str]:
        '''A URL to the S3 bucket for the resource project package that contains the necessary files for the resource you want to register.

        For information on generating a schema handler package, see `Modeling resource types to use with CloudFormation <https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/resource-type-model.html>`_ in the *CloudFormation Command Line Interface (CLI) User Guide* .
        .. epigraph::

           To register the resource version, you must have ``s3:GetObject`` permissions to access the S3 objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-schemahandlerpackage
        '''
        result = self._values.get("schema_handler_package")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource being registered.

        We recommend that resource names adhere to the following pattern: *company_or_organization* :: *service* :: *type* .
        .. epigraph::

           The following organization namespaces are reserved and can't be used in your resource names:

           - ``Alexa``
           - ``AMZN``
           - ``Amazon``
           - ``AWS``
           - ``Custom``
           - ``Dev``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html#cfn-cloudformation-resourceversion-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnResourceVersionPropsMixin",
):
    '''The ``AWS::CloudFormation::ResourceVersion`` resource registers a resource version with the CloudFormation registry.

    Registering a resource version makes it available for use in CloudFormation templates in your AWS account , and includes:

    - Validating the resource schema.
    - Determining which handlers, if any, have been specified for the resource.
    - Making the resource available for use in your account.

    For information about the CloudFormation registry, see `Managing extensions with the CloudFormation registry <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html>`_ in the *CloudFormation User Guide* .

    You can have a maximum of 50 resource versions registered at a time. This maximum is per account and per Region.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-resourceversion.html
    :cloudformationResource: AWS::CloudFormation::ResourceVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_resource_version_props_mixin = cloudformation_mixins.CfnResourceVersionPropsMixin(cloudformation_mixins.CfnResourceVersionMixinProps(
            execution_role_arn="executionRoleArn",
            logging_config=cloudformation_mixins.CfnResourceVersionPropsMixin.LoggingConfigProperty(
                log_group_name="logGroupName",
                log_role_arn="logRoleArn"
            ),
            schema_handler_package="schemaHandlerPackage",
            type_name="typeName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::ResourceVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63efeeeba5e7e18039863e55febc6310943acdcd05fcc0981e5f675df4b2357)
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
            type_hints = typing.get_type_hints(_typecheckingstub__234a37362b89d9f1a633e370944429784ce81a2a35041a8b58c2b88316a10324)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2cb04d5bbabe53c7dad6b59aba0ad42e0f7013b697e40c15c0b2440590abde)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceVersionMixinProps:
        return typing.cast(CfnResourceVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnResourceVersionPropsMixin.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName", "log_role_arn": "logRoleArn"},
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
            log_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Logging configuration information for a resource.

            :param log_group_name: The Amazon CloudWatch logs group to which CloudFormation sends error logging information when invoking the type's handlers.
            :param log_role_arn: The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-resourceversion-loggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                logging_config_property = cloudformation_mixins.CfnResourceVersionPropsMixin.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ad0aec9e2b35f0e22b0017c477f81278bad01322c169006e2f7715fb89a54aa)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument log_role_arn", value=log_role_arn, expected_type=type_hints["log_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_role_arn is not None:
                self._values["log_role_arn"] = log_role_arn

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon CloudWatch logs group to which CloudFormation sends error logging information when invoking the type's handlers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-resourceversion-loggingconfig.html#cfn-cloudformation-resourceversion-loggingconfig-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-resourceversion-loggingconfig.html#cfn-cloudformation-resourceversion-loggingconfig-logrolearn
            '''
            result = self._values.get("log_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "notification_arns": "notificationArns",
        "parameters": "parameters",
        "tags": "tags",
        "template_url": "templateUrl",
        "timeout_in_minutes": "timeoutInMinutes",
    },
)
class CfnStackMixinProps:
    def __init__(
        self,
        *,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        template_url: typing.Optional[builtins.str] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnStackPropsMixin.

        :param notification_arns: The Amazon SNS topic ARNs to publish stack related events. You can find your Amazon SNS topic ARNs using the Amazon SNS console or your Command Line Interface (CLI).
        :param parameters: The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. .. epigraph:: If you use the ``Ref`` function to pass a parameter value to a nested stack, comma-delimited list parameters must be of type ``String`` . In other words, you can't pass values that are of type ``CommaDelimitedList`` to nested stacks. Required if the nested stack requires input parameters. Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.
        :param tags: Key-value pairs to associate with this stack. CloudFormation also propagates these tags to the resources created in the stack. A maximum number of 50 tags can be specified.
        :param template_url: The URL of a file that contains the template body. The URL must point to a template (max size: 1 MB) that's located in an Amazon S3 bucket. The location for an Amazon S3 bucket must start with ``https://`` . Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.
        :param timeout_in_minutes: The length of time, in minutes, that CloudFormation waits for the nested stack to reach the ``CREATE_COMPLETE`` state. The default is no timeout. When CloudFormation detects that the nested stack has reached the ``CREATE_COMPLETE`` state, it marks the nested stack resource as ``CREATE_COMPLETE`` in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches ``CREATE_COMPLETE`` , CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Updates aren't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stack.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_stack_mixin_props = cloudformation_mixins.CfnStackMixinProps(
                notification_arns=["notificationArns"],
                parameters={
                    "parameters_key": "parameters"
                },
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                template_url="templateUrl",
                timeout_in_minutes=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bcf14f1bfab1c8a1503ec1d4d2cda4bc110879e45e2da4f9f0631be1b28d75)
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_url", value=template_url, expected_type=type_hints["template_url"])
            check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags
        if template_url is not None:
            self._values["template_url"] = template_url
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon SNS topic ARNs to publish stack related events.

        You can find your Amazon SNS topic ARNs using the Amazon SNS console or your Command Line Interface (CLI).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stack.html#cfn-cloudformation-stack-notificationarns
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created.

        Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter.
        .. epigraph::

           If you use the ``Ref`` function to pass a parameter value to a nested stack, comma-delimited list parameters must be of type ``String`` . In other words, you can't pass values that are of type ``CommaDelimitedList`` to nested stacks.

        Required if the nested stack requires input parameters.

        Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stack.html#cfn-cloudformation-stack-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs to associate with this stack.

        CloudFormation also propagates these tags to the resources created in the stack. A maximum number of 50 tags can be specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stack.html#cfn-cloudformation-stack-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def template_url(self) -> typing.Optional[builtins.str]:
        '''The URL of a file that contains the template body.

        The URL must point to a template (max size: 1 MB) that's located in an Amazon S3 bucket. The location for an Amazon S3 bucket must start with ``https://`` .

        Whether an update causes interruptions depends on the resources that are being updated. An update never causes a nested stack to be replaced.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stack.html#cfn-cloudformation-stack-templateurl
        '''
        result = self._values.get("template_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''The length of time, in minutes, that CloudFormation waits for the nested stack to reach the ``CREATE_COMPLETE`` state.

        The default is no timeout. When CloudFormation detects that the nested stack has reached the ``CREATE_COMPLETE`` state, it marks the nested stack resource as ``CREATE_COMPLETE`` in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches ``CREATE_COMPLETE`` , CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack.

        Updates aren't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stack.html#cfn-cloudformation-stack-timeoutinminutes
        '''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackPropsMixin",
):
    '''The ``AWS::CloudFormation::Stack`` resource nests a stack as a resource in a top-level template.

    For more information, see `Nested stacks <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html>`_ in the *CloudFormation User Guide* .

    You can add output values from a nested stack within the containing template. You use the `GetAtt <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference-getatt.html>`_ function with the nested stack's logical name and the name of the output value in the nested stack in the format ``Outputs. *NestedStackOutputName*`` .

    We strongly recommend that updates to nested stacks are run from the parent stack.

    When you apply template changes to update a top-level stack, CloudFormation updates the top-level stack and initiates an update to its nested stacks. CloudFormation updates the resources of modified nested stacks, but doesn't update the resources of unmodified nested stacks.

    For stacks that contain IAM resources, you must acknowledge IAM capabilities. Also, make sure that you have cancel update stack permissions, which are required if an update rolls back. For more information about IAM and CloudFormation , see `Controlling access with AWS Identity and Access Management <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/control-access-with-iam.html>`_ in the *CloudFormation User Guide* .
    .. epigraph::

       A subset of ``AWS::CloudFormation::Stack`` resource type properties listed below are available to customers using CloudFormation , AWS CDK , and Cloud Control  to configure.

       - ``NotificationARNs``
       - ``Parameters``
       - ``Tags``
       - ``TemplateURL``
       - ``TimeoutInMinutes``

       These properties can be configured only when using Cloud Control  . This is because the below properties are set by the parent stack, and thus cannot be configured using CloudFormation or AWS CDK but only Cloud Control  .

       - ``Capabilities``
       - ``Description``
       - ``DisableRollback``
       - ``EnableTerminationProtection``
       - ``RoleARN``
       - ``StackName``
       - ``StackPolicyBody``
       - ``StackPolicyURL``
       - ``StackStatusReason``
       - ``TemplateBody``

       Customers that configure ``AWS::CloudFormation::Stack`` using CloudFormation and AWS CDK can do so for nesting a CloudFormation stack as a resource in their top-level template.

       These read-only properties can be accessed only when using Cloud Control  .

       - ``ChangeSetId``
       - ``CreationTime``
       - ``LastUpdateTime``
       - ``Outputs``
       - ``ParentId``
       - ``RootId``
       - ``StackId``
       - ``StackStatus``

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stack.html
    :cloudformationResource: AWS::CloudFormation::Stack
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_stack_props_mixin = cloudformation_mixins.CfnStackPropsMixin(cloudformation_mixins.CfnStackMixinProps(
            notification_arns=["notificationArns"],
            parameters={
                "parameters_key": "parameters"
            },
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            template_url="templateUrl",
            timeout_in_minutes=123
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
        '''Create a mixin to apply properties to ``AWS::CloudFormation::Stack``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c69d4cb942c2c6d0b9543619efc09ac7d5059a1818de88b8a3f540ceb0e31a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cc3edb586ee0d8ff2fb660c0db3a6078c5bf9b7116e0589e365246126873733)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f77d252fad8419571a43da49bf88ce2498fbdee9dc338537b8e391f061bdeeb7)
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
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackPropsMixin.OutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "export_name": "exportName",
            "output_key": "outputKey",
            "output_value": "outputValue",
        },
    )
    class OutputProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            export_name: typing.Optional[builtins.str] = None,
            output_key: typing.Optional[builtins.str] = None,
            output_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Output`` data type.

            :param description: User defined description associated with the output.
            :param export_name: The name of the export associated with the output.
            :param output_key: The key associated with the output.
            :param output_value: The value associated with the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stack-output.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                output_property = cloudformation_mixins.CfnStackPropsMixin.OutputProperty(
                    description="description",
                    export_name="exportName",
                    output_key="outputKey",
                    output_value="outputValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__481dcfcbb5419f66b20654b75fdd0391bbbf4af177d9f893940831c29d285132)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument export_name", value=export_name, expected_type=type_hints["export_name"])
                check_type(argname="argument output_key", value=output_key, expected_type=type_hints["output_key"])
                check_type(argname="argument output_value", value=output_value, expected_type=type_hints["output_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if export_name is not None:
                self._values["export_name"] = export_name
            if output_key is not None:
                self._values["output_key"] = output_key
            if output_value is not None:
                self._values["output_value"] = output_value

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''User defined description associated with the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stack-output.html#cfn-cloudformation-stack-output-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def export_name(self) -> typing.Optional[builtins.str]:
            '''The name of the export associated with the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stack-output.html#cfn-cloudformation-stack-output-exportname
            '''
            result = self._values.get("export_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_key(self) -> typing.Optional[builtins.str]:
            '''The key associated with the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stack-output.html#cfn-cloudformation-stack-output-outputkey
            '''
            result = self._values.get("output_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_value(self) -> typing.Optional[builtins.str]:
            '''The value associated with the output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stack-output.html#cfn-cloudformation-stack-output-outputvalue
            '''
            result = self._values.get("output_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "administration_role_arn": "administrationRoleArn",
        "auto_deployment": "autoDeployment",
        "call_as": "callAs",
        "capabilities": "capabilities",
        "description": "description",
        "execution_role_name": "executionRoleName",
        "managed_execution": "managedExecution",
        "operation_preferences": "operationPreferences",
        "parameters": "parameters",
        "permission_model": "permissionModel",
        "stack_instances_group": "stackInstancesGroup",
        "stack_set_name": "stackSetName",
        "tags": "tags",
        "template_body": "templateBody",
        "template_url": "templateUrl",
    },
)
class CfnStackSetMixinProps:
    def __init__(
        self,
        *,
        administration_role_arn: typing.Optional[builtins.str] = None,
        auto_deployment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackSetPropsMixin.AutoDeploymentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        call_as: typing.Optional[builtins.str] = None,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role_name: typing.Optional[builtins.str] = None,
        managed_execution: typing.Any = None,
        operation_preferences: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackSetPropsMixin.OperationPreferencesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackSetPropsMixin.ParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        permission_model: typing.Optional[builtins.str] = None,
        stack_instances_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackSetPropsMixin.StackInstancesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        stack_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        template_body: typing.Optional[builtins.str] = None,
        template_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStackSetPropsMixin.

        :param administration_role_arn: The Amazon Resource Number (ARN) of the IAM role to use to create this StackSet. Specify an IAM role only if you are using customized administrator roles to control which users or groups can manage specific StackSets within the same administrator account. Use customized administrator roles to control which users or groups can manage specific StackSets within the same administrator account. For more information, see `Grant self-managed permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html>`_ in the *CloudFormation User Guide* . Valid only if the permissions model is ``SELF_MANAGED`` .
        :param auto_deployment: Describes whether StackSets automatically deploys to AWS Organizations accounts that are added to a target organization or organizational unit (OU). For more information, see `Enable or disable automatic deployments for StackSets in AWS Organizations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-manage-auto-deployment.html>`_ in the *CloudFormation User Guide* . Required if the permissions model is ``SERVICE_MANAGED`` . (Not used with self-managed permissions.)
        :param call_as: Specifies whether you are acting as an account administrator in the organization's management account or as a delegated administrator in a member account. By default, ``SELF`` is specified. Use ``SELF`` for StackSets with self-managed permissions. - To create a StackSet with service-managed permissions while signed in to the management account, specify ``SELF`` . - To create a StackSet with service-managed permissions while signed in to a delegated administrator account, specify ``DELEGATED_ADMIN`` . Your AWS account must be registered as a delegated admin in the management account. For more information, see `Register a delegated administrator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-delegated-admin.html>`_ in the *CloudFormation User Guide* . StackSets with service-managed permissions are created in the management account, including StackSets that are created by delegated administrators. Valid only if the permissions model is ``SERVICE_MANAGED`` .
        :param capabilities: The capabilities that are allowed in the StackSet. Some StackSet templates might include resources that can affect permissions in your AWS account —for example, by creating new IAM users. For more information, see `Acknowledging IAM resources in CloudFormation templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/control-access-with-iam.html#using-iam-capabilities>`_ in the *CloudFormation User Guide* .
        :param description: A description of the StackSet.
        :param execution_role_name: The name of the IAM execution role to use to create the StackSet. If you don't specify an execution role, CloudFormation uses the ``AWSCloudFormationStackSetExecutionRole`` role for the StackSet operation. Valid only if the permissions model is ``SELF_MANAGED`` . *Pattern* : ``[a-zA-Z_0-9+=,.@-]+``
        :param managed_execution: Describes whether StackSets performs non-conflicting operations concurrently and queues conflicting operations. When active, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order. .. epigraph:: If there are already running or queued operations, StackSets queues all incoming operations even if they are non-conflicting. You can't modify your StackSet's execution configuration while there are running or queued operations for that StackSet. When inactive (default), StackSets performs one operation at a time in request order.
        :param operation_preferences: The user-specified preferences for how CloudFormation performs a StackSet operation.
        :param parameters: The input parameters for the StackSet template.
        :param permission_model: Describes how the IAM roles required for StackSet operations are created. - With ``SELF_MANAGED`` permissions, you must create the administrator and execution roles required to deploy to target accounts. For more information, see `Grant self-managed permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html>`_ in the *CloudFormation User Guide* . - With ``SERVICE_MANAGED`` permissions, StackSets automatically creates the IAM roles required to deploy to accounts managed by AWS Organizations . For more information, see `Activate trusted access for StackSets with AWS Organizations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-activate-trusted-access.html>`_ in the *CloudFormation User Guide* .
        :param stack_instances_group: A group of stack instances with parameters in some specific accounts and Regions.
        :param stack_set_name: The name to associate with the StackSet. The name must be unique in the Region where you create your StackSet.
        :param tags: Key-value pairs to associate with this stack. CloudFormation also propagates these tags to supported resources in the stack. You can specify a maximum number of 50 tags. If you don't specify this parameter, CloudFormation doesn't modify the stack's tags. If you specify an empty value, CloudFormation removes all associated tags.
        :param template_body: The structure that contains the template body, with a minimum length of 1 byte and a maximum length of 51,200 bytes. You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both. Dynamic references in the ``TemplateBody`` may not work correctly in all cases. It's recommended to pass templates that contain dynamic references through ``TemplateUrl`` instead.
        :param template_url: The URL of a file that contains the template body. The URL must point to a template (max size: 1 MB) that's located in an Amazon S3 bucket or a Systems Manager document. The location for an Amazon S3 bucket must start with ``https://`` . Conditional: You must specify only one of the following parameters: ``TemplateBody`` , ``TemplateURL`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            # managed_execution: Any
            
            cfn_stack_set_mixin_props = cloudformation_mixins.CfnStackSetMixinProps(
                administration_role_arn="administrationRoleArn",
                auto_deployment=cloudformation_mixins.CfnStackSetPropsMixin.AutoDeploymentProperty(
                    depends_on=["dependsOn"],
                    enabled=False,
                    retain_stacks_on_account_removal=False
                ),
                call_as="callAs",
                capabilities=["capabilities"],
                description="description",
                execution_role_name="executionRoleName",
                managed_execution=managed_execution,
                operation_preferences=cloudformation_mixins.CfnStackSetPropsMixin.OperationPreferencesProperty(
                    concurrency_mode="concurrencyMode",
                    failure_tolerance_count=123,
                    failure_tolerance_percentage=123,
                    max_concurrent_count=123,
                    max_concurrent_percentage=123,
                    region_concurrency_type="regionConcurrencyType",
                    region_order=["regionOrder"]
                ),
                parameters=[cloudformation_mixins.CfnStackSetPropsMixin.ParameterProperty(
                    parameter_key="parameterKey",
                    parameter_value="parameterValue"
                )],
                permission_model="permissionModel",
                stack_instances_group=[cloudformation_mixins.CfnStackSetPropsMixin.StackInstancesProperty(
                    deployment_targets=cloudformation_mixins.CfnStackSetPropsMixin.DeploymentTargetsProperty(
                        account_filter_type="accountFilterType",
                        accounts=["accounts"],
                        accounts_url="accountsUrl",
                        organizational_unit_ids=["organizationalUnitIds"]
                    ),
                    parameter_overrides=[cloudformation_mixins.CfnStackSetPropsMixin.ParameterProperty(
                        parameter_key="parameterKey",
                        parameter_value="parameterValue"
                    )],
                    regions=["regions"]
                )],
                stack_set_name="stackSetName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                template_body="templateBody",
                template_url="templateUrl"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d578ce42fb285aff99bff46eac06dcc11f34520ffbebf432240fe6bbe1e8845)
            check_type(argname="argument administration_role_arn", value=administration_role_arn, expected_type=type_hints["administration_role_arn"])
            check_type(argname="argument auto_deployment", value=auto_deployment, expected_type=type_hints["auto_deployment"])
            check_type(argname="argument call_as", value=call_as, expected_type=type_hints["call_as"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role_name", value=execution_role_name, expected_type=type_hints["execution_role_name"])
            check_type(argname="argument managed_execution", value=managed_execution, expected_type=type_hints["managed_execution"])
            check_type(argname="argument operation_preferences", value=operation_preferences, expected_type=type_hints["operation_preferences"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument permission_model", value=permission_model, expected_type=type_hints["permission_model"])
            check_type(argname="argument stack_instances_group", value=stack_instances_group, expected_type=type_hints["stack_instances_group"])
            check_type(argname="argument stack_set_name", value=stack_set_name, expected_type=type_hints["stack_set_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_body", value=template_body, expected_type=type_hints["template_body"])
            check_type(argname="argument template_url", value=template_url, expected_type=type_hints["template_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if administration_role_arn is not None:
            self._values["administration_role_arn"] = administration_role_arn
        if auto_deployment is not None:
            self._values["auto_deployment"] = auto_deployment
        if call_as is not None:
            self._values["call_as"] = call_as
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if description is not None:
            self._values["description"] = description
        if execution_role_name is not None:
            self._values["execution_role_name"] = execution_role_name
        if managed_execution is not None:
            self._values["managed_execution"] = managed_execution
        if operation_preferences is not None:
            self._values["operation_preferences"] = operation_preferences
        if parameters is not None:
            self._values["parameters"] = parameters
        if permission_model is not None:
            self._values["permission_model"] = permission_model
        if stack_instances_group is not None:
            self._values["stack_instances_group"] = stack_instances_group
        if stack_set_name is not None:
            self._values["stack_set_name"] = stack_set_name
        if tags is not None:
            self._values["tags"] = tags
        if template_body is not None:
            self._values["template_body"] = template_body
        if template_url is not None:
            self._values["template_url"] = template_url

    @builtins.property
    def administration_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the IAM role to use to create this StackSet.

        Specify an IAM role only if you are using customized administrator roles to control which users or groups can manage specific StackSets within the same administrator account.

        Use customized administrator roles to control which users or groups can manage specific StackSets within the same administrator account. For more information, see `Grant self-managed permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html>`_ in the *CloudFormation User Guide* .

        Valid only if the permissions model is ``SELF_MANAGED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-administrationrolearn
        '''
        result = self._values.get("administration_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_deployment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.AutoDeploymentProperty"]]:
        '''Describes whether StackSets automatically deploys to AWS Organizations accounts that are added to a target organization or organizational unit (OU).

        For more information, see `Enable or disable automatic deployments for StackSets in AWS Organizations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-manage-auto-deployment.html>`_ in the *CloudFormation User Guide* .

        Required if the permissions model is ``SERVICE_MANAGED`` . (Not used with self-managed permissions.)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-autodeployment
        '''
        result = self._values.get("auto_deployment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.AutoDeploymentProperty"]], result)

    @builtins.property
    def call_as(self) -> typing.Optional[builtins.str]:
        '''Specifies whether you are acting as an account administrator in the organization's management account or as a delegated administrator in a member account.

        By default, ``SELF`` is specified. Use ``SELF`` for StackSets with self-managed permissions.

        - To create a StackSet with service-managed permissions while signed in to the management account, specify ``SELF`` .
        - To create a StackSet with service-managed permissions while signed in to a delegated administrator account, specify ``DELEGATED_ADMIN`` .

        Your AWS account must be registered as a delegated admin in the management account. For more information, see `Register a delegated administrator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-delegated-admin.html>`_ in the *CloudFormation User Guide* .

        StackSets with service-managed permissions are created in the management account, including StackSets that are created by delegated administrators.

        Valid only if the permissions model is ``SERVICE_MANAGED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-callas
        '''
        result = self._values.get("call_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The capabilities that are allowed in the StackSet.

        Some StackSet templates might include resources that can affect permissions in your AWS account —for example, by creating new IAM users. For more information, see `Acknowledging IAM resources in CloudFormation templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/control-access-with-iam.html#using-iam-capabilities>`_ in the *CloudFormation User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-capabilities
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the StackSet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM execution role to use to create the StackSet.

        If you don't specify an execution role, CloudFormation uses the ``AWSCloudFormationStackSetExecutionRole`` role for the StackSet operation.

        Valid only if the permissions model is ``SELF_MANAGED`` .

        *Pattern* : ``[a-zA-Z_0-9+=,.@-]+``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-executionrolename
        '''
        result = self._values.get("execution_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_execution(self) -> typing.Any:
        '''Describes whether StackSets performs non-conflicting operations concurrently and queues conflicting operations.

        When active, StackSets performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, StackSets starts queued operations in request order.
        .. epigraph::

           If there are already running or queued operations, StackSets queues all incoming operations even if they are non-conflicting.

           You can't modify your StackSet's execution configuration while there are running or queued operations for that StackSet.

        When inactive (default), StackSets performs one operation at a time in request order.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-managedexecution
        '''
        result = self._values.get("managed_execution")
        return typing.cast(typing.Any, result)

    @builtins.property
    def operation_preferences(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.OperationPreferencesProperty"]]:
        '''The user-specified preferences for how CloudFormation performs a StackSet operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-operationpreferences
        '''
        result = self._values.get("operation_preferences")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.OperationPreferencesProperty"]], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.ParameterProperty"]]]]:
        '''The input parameters for the StackSet template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.ParameterProperty"]]]], result)

    @builtins.property
    def permission_model(self) -> typing.Optional[builtins.str]:
        '''Describes how the IAM roles required for StackSet operations are created.

        - With ``SELF_MANAGED`` permissions, you must create the administrator and execution roles required to deploy to target accounts. For more information, see `Grant self-managed permissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html>`_ in the *CloudFormation User Guide* .
        - With ``SERVICE_MANAGED`` permissions, StackSets automatically creates the IAM roles required to deploy to accounts managed by AWS Organizations . For more information, see `Activate trusted access for StackSets with AWS Organizations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-activate-trusted-access.html>`_ in the *CloudFormation User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-permissionmodel
        '''
        result = self._values.get("permission_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_instances_group(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.StackInstancesProperty"]]]]:
        '''A group of stack instances with parameters in some specific accounts and Regions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stackinstancesgroup
        '''
        result = self._values.get("stack_instances_group")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.StackInstancesProperty"]]]], result)

    @builtins.property
    def stack_set_name(self) -> typing.Optional[builtins.str]:
        '''The name to associate with the StackSet.

        The name must be unique in the Region where you create your StackSet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-stacksetname
        '''
        result = self._values.get("stack_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs to associate with this stack.

        CloudFormation also propagates these tags to supported resources in the stack. You can specify a maximum number of 50 tags.

        If you don't specify this parameter, CloudFormation doesn't modify the stack's tags. If you specify an empty value, CloudFormation removes all associated tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def template_body(self) -> typing.Optional[builtins.str]:
        '''The structure that contains the template body, with a minimum length of 1 byte and a maximum length of 51,200 bytes.

        You must include either ``TemplateURL`` or ``TemplateBody`` in a StackSet, but you can't use both. Dynamic references in the ``TemplateBody`` may not work correctly in all cases. It's recommended to pass templates that contain dynamic references through ``TemplateUrl`` instead.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templatebody
        '''
        result = self._values.get("template_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_url(self) -> typing.Optional[builtins.str]:
        '''The URL of a file that contains the template body.

        The URL must point to a template (max size: 1 MB) that's located in an Amazon S3 bucket or a Systems Manager document. The location for an Amazon S3 bucket must start with ``https://`` .

        Conditional: You must specify only one of the following parameters: ``TemplateBody`` , ``TemplateURL`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html#cfn-cloudformation-stackset-templateurl
        '''
        result = self._values.get("template_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStackSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackSetPropsMixin",
):
    '''The ``AWS::CloudFormation::StackSet`` resource contains information about a StackSet.

    With StackSets, you can provision stacks across AWS accounts and Regions from a single CloudFormation template. Each stack is based on the same CloudFormation template, but you can customize individual stacks using parameters.
    .. epigraph::

       Run deployments to nested StackSets from the parent stack, not directly through the StackSet API.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-stackset.html
    :cloudformationResource: AWS::CloudFormation::StackSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        # managed_execution: Any
        
        cfn_stack_set_props_mixin = cloudformation_mixins.CfnStackSetPropsMixin(cloudformation_mixins.CfnStackSetMixinProps(
            administration_role_arn="administrationRoleArn",
            auto_deployment=cloudformation_mixins.CfnStackSetPropsMixin.AutoDeploymentProperty(
                depends_on=["dependsOn"],
                enabled=False,
                retain_stacks_on_account_removal=False
            ),
            call_as="callAs",
            capabilities=["capabilities"],
            description="description",
            execution_role_name="executionRoleName",
            managed_execution=managed_execution,
            operation_preferences=cloudformation_mixins.CfnStackSetPropsMixin.OperationPreferencesProperty(
                concurrency_mode="concurrencyMode",
                failure_tolerance_count=123,
                failure_tolerance_percentage=123,
                max_concurrent_count=123,
                max_concurrent_percentage=123,
                region_concurrency_type="regionConcurrencyType",
                region_order=["regionOrder"]
            ),
            parameters=[cloudformation_mixins.CfnStackSetPropsMixin.ParameterProperty(
                parameter_key="parameterKey",
                parameter_value="parameterValue"
            )],
            permission_model="permissionModel",
            stack_instances_group=[cloudformation_mixins.CfnStackSetPropsMixin.StackInstancesProperty(
                deployment_targets=cloudformation_mixins.CfnStackSetPropsMixin.DeploymentTargetsProperty(
                    account_filter_type="accountFilterType",
                    accounts=["accounts"],
                    accounts_url="accountsUrl",
                    organizational_unit_ids=["organizationalUnitIds"]
                ),
                parameter_overrides=[cloudformation_mixins.CfnStackSetPropsMixin.ParameterProperty(
                    parameter_key="parameterKey",
                    parameter_value="parameterValue"
                )],
                regions=["regions"]
            )],
            stack_set_name="stackSetName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            template_body="templateBody",
            template_url="templateUrl"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStackSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::StackSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c49ca082e9333a7e23f97acd9b4c18c88c018a71798365249b9ce98f875c2e8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0590fef52b6029507b8f584cdca297a76d1dd3a7466e9985354223764a97c8c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9ab692a764dbaabafd32ff8881e154f98a08739016c3bd44a3f62ef21c3a8e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStackSetMixinProps:
        return typing.cast(CfnStackSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackSetPropsMixin.AutoDeploymentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "depends_on": "dependsOn",
            "enabled": "enabled",
            "retain_stacks_on_account_removal": "retainStacksOnAccountRemoval",
        },
    )
    class AutoDeploymentProperty:
        def __init__(
            self,
            *,
            depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            retain_stacks_on_account_removal: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes whether StackSets automatically deploys to AWS Organizations accounts that are added to a target organization or organizational unit (OU).

            For more information, see `Enable or disable automatic deployments for StackSets in AWS Organizations <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-manage-auto-deployment.html>`_ in the *CloudFormation User Guide* .

            :param depends_on: A list of StackSet ARNs that this StackSet depends on for auto-deployment operations. When auto-deployment is triggered, operations will be sequenced to ensure all dependencies complete successfully before this StackSet's operation begins.
            :param enabled: If set to ``true`` , StackSets automatically deploys additional stack instances to AWS Organizations accounts that are added to a target organization or organizational unit (OU) in the specified Regions. If an account is removed from a target organization or OU, StackSets deletes stack instances from the account in the specified Regions.
            :param retain_stacks_on_account_removal: If set to ``true`` , stack resources are retained when an account is removed from a target organization or OU. If set to ``false`` , stack resources are deleted. Specify only if ``Enabled`` is set to ``True`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                auto_deployment_property = cloudformation_mixins.CfnStackSetPropsMixin.AutoDeploymentProperty(
                    depends_on=["dependsOn"],
                    enabled=False,
                    retain_stacks_on_account_removal=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__787a979fc4c0da0be9b187805e465f8383a7d6ad2191e22d487faf76f6dc8bff)
                check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument retain_stacks_on_account_removal", value=retain_stacks_on_account_removal, expected_type=type_hints["retain_stacks_on_account_removal"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if depends_on is not None:
                self._values["depends_on"] = depends_on
            if enabled is not None:
                self._values["enabled"] = enabled
            if retain_stacks_on_account_removal is not None:
                self._values["retain_stacks_on_account_removal"] = retain_stacks_on_account_removal

        @builtins.property
        def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of StackSet ARNs that this StackSet depends on for auto-deployment operations.

            When auto-deployment is triggered, operations will be sequenced to ensure all dependencies complete successfully before this StackSet's operation begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html#cfn-cloudformation-stackset-autodeployment-dependson
            '''
            result = self._values.get("depends_on")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to ``true`` , StackSets automatically deploys additional stack instances to AWS Organizations accounts that are added to a target organization or organizational unit (OU) in the specified Regions.

            If an account is removed from a target organization or OU, StackSets deletes stack instances from the account in the specified Regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html#cfn-cloudformation-stackset-autodeployment-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def retain_stacks_on_account_removal(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to ``true`` , stack resources are retained when an account is removed from a target organization or OU.

            If set to ``false`` , stack resources are deleted. Specify only if ``Enabled`` is set to ``True`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-autodeployment.html#cfn-cloudformation-stackset-autodeployment-retainstacksonaccountremoval
            '''
            result = self._values.get("retain_stacks_on_account_removal")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoDeploymentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackSetPropsMixin.DeploymentTargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_filter_type": "accountFilterType",
            "accounts": "accounts",
            "accounts_url": "accountsUrl",
            "organizational_unit_ids": "organizationalUnitIds",
        },
    )
    class DeploymentTargetsProperty:
        def __init__(
            self,
            *,
            account_filter_type: typing.Optional[builtins.str] = None,
            accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            accounts_url: typing.Optional[builtins.str] = None,
            organizational_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The AWS Organizations accounts or AWS accounts to deploy stacks to in the specified Regions.

            When deploying to AWS Organizations accounts with ``SERVICE_MANAGED`` permissions:

            - You must specify the ``OrganizationalUnitIds`` property.
            - If you specify organizational units (OUs) for ``OrganizationalUnitIds`` and use either the ``Accounts`` or ``AccountsUrl`` property, you must also specify the ``AccountFilterType`` property.

            When deploying to AWS accounts with ``SELF_MANAGED`` permissions:

            - You must specify either the ``Accounts`` or ``AccountsUrl`` property, but not both.

            :param account_filter_type: Refines which accounts to deploy stacks to by specifying how to use the ``Accounts`` and ``OrganizationalUnitIds`` properties together. The following values determine how CloudFormation selects target accounts: - ``INTERSECTION`` : StackSet deploys to the accounts specified in the ``Accounts`` property. - ``DIFFERENCE`` : StackSet deploys to the OU, excluding the accounts specified in the ``Accounts`` property. - ``UNION`` : StackSet deploys to the OU, and the accounts specified in the ``Accounts`` property. ``UNION`` is not supported for create operations when using StackSet as a resource or the ``CreateStackInstances`` API.
            :param accounts: The account IDs of the AWS accounts . If you have many account numbers, you can provide those accounts using the ``AccountsUrl`` property instead. *Pattern* : ``^[0-9]{12}$``
            :param accounts_url: The Amazon S3 URL path to a file that contains a list of AWS account IDs. The file format must be either ``.csv`` or ``.txt`` , and the data can be comma-separated or new-line-separated. There is currently a 10MB limit for the data (approximately 800,000 accounts). This property serves the same purpose as ``Accounts`` but allows you to specify a large number of accounts.
            :param organizational_unit_ids: The organization root ID or organizational unit (OU) IDs. *Pattern* : ``^(ou-[a-z0-9]{4,32}-[a-z0-9]{8,32}|r-[a-z0-9]{4,32})$``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                deployment_targets_property = cloudformation_mixins.CfnStackSetPropsMixin.DeploymentTargetsProperty(
                    account_filter_type="accountFilterType",
                    accounts=["accounts"],
                    accounts_url="accountsUrl",
                    organizational_unit_ids=["organizationalUnitIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c78a10d40a3fb403ccc0b880781c797128dbae6de26b6fbd6ca4fc5e268daaf3)
                check_type(argname="argument account_filter_type", value=account_filter_type, expected_type=type_hints["account_filter_type"])
                check_type(argname="argument accounts", value=accounts, expected_type=type_hints["accounts"])
                check_type(argname="argument accounts_url", value=accounts_url, expected_type=type_hints["accounts_url"])
                check_type(argname="argument organizational_unit_ids", value=organizational_unit_ids, expected_type=type_hints["organizational_unit_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_filter_type is not None:
                self._values["account_filter_type"] = account_filter_type
            if accounts is not None:
                self._values["accounts"] = accounts
            if accounts_url is not None:
                self._values["accounts_url"] = accounts_url
            if organizational_unit_ids is not None:
                self._values["organizational_unit_ids"] = organizational_unit_ids

        @builtins.property
        def account_filter_type(self) -> typing.Optional[builtins.str]:
            '''Refines which accounts to deploy stacks to by specifying how to use the ``Accounts`` and ``OrganizationalUnitIds`` properties together.

            The following values determine how CloudFormation selects target accounts:

            - ``INTERSECTION`` : StackSet deploys to the accounts specified in the ``Accounts`` property.
            - ``DIFFERENCE`` : StackSet deploys to the OU, excluding the accounts specified in the ``Accounts`` property.
            - ``UNION`` : StackSet deploys to the OU, and the accounts specified in the ``Accounts`` property. ``UNION`` is not supported for create operations when using StackSet as a resource or the ``CreateStackInstances`` API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-accountfiltertype
            '''
            result = self._values.get("account_filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The account IDs of the AWS accounts .

            If you have many account numbers, you can provide those accounts using the ``AccountsUrl`` property instead.

            *Pattern* : ``^[0-9]{12}$``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-accounts
            '''
            result = self._values.get("accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def accounts_url(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 URL path to a file that contains a list of AWS account IDs.

            The file format must be either ``.csv`` or ``.txt`` , and the data can be comma-separated or new-line-separated. There is currently a 10MB limit for the data (approximately 800,000 accounts).

            This property serves the same purpose as ``Accounts`` but allows you to specify a large number of accounts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-accountsurl
            '''
            result = self._values.get("accounts_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The organization root ID or organizational unit (OU) IDs.

            *Pattern* : ``^(ou-[a-z0-9]{4,32}-[a-z0-9]{8,32}|r-[a-z0-9]{4,32})$``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-deploymenttargets.html#cfn-cloudformation-stackset-deploymenttargets-organizationalunitids
            '''
            result = self._values.get("organizational_unit_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentTargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackSetPropsMixin.ManagedExecutionProperty",
        jsii_struct_bases=[],
        name_mapping={"active": "active"},
    )
    class ManagedExecutionProperty:
        def __init__(
            self,
            *,
            active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes whether StackSets performs non-conflicting operations concurrently and queues conflicting operations.

            :param active: When ``true`` , CloudFormation performs non-conflicting operations concurrently and queues conflicting operations. After conflicting operations finish, CloudFormation starts queued operations in request order. .. epigraph:: If there are already running or queued operations, CloudFormation queues all incoming operations even if they are non-conflicting. You can't modify your StackSet's execution configuration while there are running or queued operations for that StackSet. When ``false`` (default), StackSets performs one operation at a time in request order.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-managedexecution.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                managed_execution_property = cloudformation_mixins.CfnStackSetPropsMixin.ManagedExecutionProperty(
                    active=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9d2fc930e2369a5245b8430a63c173be831c2f06e6ba241a3d88feb17cb9a7e)
                check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active is not None:
                self._values["active"] = active

        @builtins.property
        def active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When ``true`` , CloudFormation performs non-conflicting operations concurrently and queues conflicting operations.

            After conflicting operations finish, CloudFormation starts queued operations in request order.
            .. epigraph::

               If there are already running or queued operations, CloudFormation queues all incoming operations even if they are non-conflicting.

               You can't modify your StackSet's execution configuration while there are running or queued operations for that StackSet.

            When ``false`` (default), StackSets performs one operation at a time in request order.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-managedexecution.html#cfn-cloudformation-stackset-managedexecution-active
            '''
            result = self._values.get("active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedExecutionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackSetPropsMixin.OperationPreferencesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "concurrency_mode": "concurrencyMode",
            "failure_tolerance_count": "failureToleranceCount",
            "failure_tolerance_percentage": "failureTolerancePercentage",
            "max_concurrent_count": "maxConcurrentCount",
            "max_concurrent_percentage": "maxConcurrentPercentage",
            "region_concurrency_type": "regionConcurrencyType",
            "region_order": "regionOrder",
        },
    )
    class OperationPreferencesProperty:
        def __init__(
            self,
            *,
            concurrency_mode: typing.Optional[builtins.str] = None,
            failure_tolerance_count: typing.Optional[jsii.Number] = None,
            failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
            max_concurrent_count: typing.Optional[jsii.Number] = None,
            max_concurrent_percentage: typing.Optional[jsii.Number] = None,
            region_concurrency_type: typing.Optional[builtins.str] = None,
            region_order: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The user-specified preferences for how CloudFormation performs a StackSet operation.

            For more information on maximum concurrent accounts and failure tolerance, see `StackSet operation options <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-concepts.html#stackset-ops-options>`_ in the *CloudFormation User Guide* .

            :param concurrency_mode: Specifies how the concurrency level behaves during the operation execution. - ``STRICT_FAILURE_TOLERANCE`` : This option dynamically lowers the concurrency level to ensure the number of failed accounts never exceeds the value of ``FailureToleranceCount`` +1. The initial actual concurrency is set to the lower of either the value of the ``MaxConcurrentCount`` , or the value of ``FailureToleranceCount`` +1. The actual concurrency is then reduced proportionally by the number of failures. This is the default behavior. If failure tolerance or Maximum concurrent accounts are set to percentages, the behavior is similar. - ``SOFT_FAILURE_TOLERANCE`` : This option decouples ``FailureToleranceCount`` from the actual concurrency. This allows StackSet operations to run at the concurrency level set by the ``MaxConcurrentCount`` value, or ``MaxConcurrentPercentage`` , regardless of the number of failures.
            :param failure_tolerance_count: The number of accounts per Region this operation can fail in before CloudFormation stops the operation in that Region. If the operation is stopped in a Region, CloudFormation doesn't attempt the operation in any subsequent Regions. Conditional: You must specify either ``FailureToleranceCount`` or ``FailureTolerancePercentage`` (but not both).
            :param failure_tolerance_percentage: The percentage of accounts per Region this stack operation can fail in before CloudFormation stops the operation in that Region. If the operation is stopped in a Region, CloudFormation doesn't attempt the operation in any subsequent Regions. When calculating the number of accounts based on the specified percentage, CloudFormation rounds *down* to the next whole number. Conditional: You must specify either ``FailureToleranceCount`` or ``FailureTolerancePercentage`` , but not both.
            :param max_concurrent_count: The maximum number of accounts in which to perform this operation at one time. This is dependent on the value of ``FailureToleranceCount`` . ``MaxConcurrentCount`` is at most one more than the ``FailureToleranceCount`` . Note that this setting lets you specify the *maximum* for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling. Conditional: You must specify either ``MaxConcurrentCount`` or ``MaxConcurrentPercentage`` , but not both.
            :param max_concurrent_percentage: The maximum percentage of accounts in which to perform this operation at one time. When calculating the number of accounts based on the specified percentage, CloudFormation rounds down to the next whole number. This is true except in cases where rounding down would result is zero. In this case, CloudFormation sets the number as one instead. Note that this setting lets you specify the *maximum* for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling. Conditional: You must specify either ``MaxConcurrentCount`` or ``MaxConcurrentPercentage`` , but not both.
            :param region_concurrency_type: The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time.
            :param region_order: The order of the Regions where you want to perform the stack operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                operation_preferences_property = cloudformation_mixins.CfnStackSetPropsMixin.OperationPreferencesProperty(
                    concurrency_mode="concurrencyMode",
                    failure_tolerance_count=123,
                    failure_tolerance_percentage=123,
                    max_concurrent_count=123,
                    max_concurrent_percentage=123,
                    region_concurrency_type="regionConcurrencyType",
                    region_order=["regionOrder"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c29ced7ffb9ee4f5d1a82acfae3e64eefef1f7c3b911be7df1a3206be3c6ef9e)
                check_type(argname="argument concurrency_mode", value=concurrency_mode, expected_type=type_hints["concurrency_mode"])
                check_type(argname="argument failure_tolerance_count", value=failure_tolerance_count, expected_type=type_hints["failure_tolerance_count"])
                check_type(argname="argument failure_tolerance_percentage", value=failure_tolerance_percentage, expected_type=type_hints["failure_tolerance_percentage"])
                check_type(argname="argument max_concurrent_count", value=max_concurrent_count, expected_type=type_hints["max_concurrent_count"])
                check_type(argname="argument max_concurrent_percentage", value=max_concurrent_percentage, expected_type=type_hints["max_concurrent_percentage"])
                check_type(argname="argument region_concurrency_type", value=region_concurrency_type, expected_type=type_hints["region_concurrency_type"])
                check_type(argname="argument region_order", value=region_order, expected_type=type_hints["region_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if concurrency_mode is not None:
                self._values["concurrency_mode"] = concurrency_mode
            if failure_tolerance_count is not None:
                self._values["failure_tolerance_count"] = failure_tolerance_count
            if failure_tolerance_percentage is not None:
                self._values["failure_tolerance_percentage"] = failure_tolerance_percentage
            if max_concurrent_count is not None:
                self._values["max_concurrent_count"] = max_concurrent_count
            if max_concurrent_percentage is not None:
                self._values["max_concurrent_percentage"] = max_concurrent_percentage
            if region_concurrency_type is not None:
                self._values["region_concurrency_type"] = region_concurrency_type
            if region_order is not None:
                self._values["region_order"] = region_order

        @builtins.property
        def concurrency_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies how the concurrency level behaves during the operation execution.

            - ``STRICT_FAILURE_TOLERANCE`` : This option dynamically lowers the concurrency level to ensure the number of failed accounts never exceeds the value of ``FailureToleranceCount`` +1. The initial actual concurrency is set to the lower of either the value of the ``MaxConcurrentCount`` , or the value of ``FailureToleranceCount`` +1. The actual concurrency is then reduced proportionally by the number of failures. This is the default behavior.

            If failure tolerance or Maximum concurrent accounts are set to percentages, the behavior is similar.

            - ``SOFT_FAILURE_TOLERANCE`` : This option decouples ``FailureToleranceCount`` from the actual concurrency. This allows StackSet operations to run at the concurrency level set by the ``MaxConcurrentCount`` value, or ``MaxConcurrentPercentage`` , regardless of the number of failures.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-concurrencymode
            '''
            result = self._values.get("concurrency_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def failure_tolerance_count(self) -> typing.Optional[jsii.Number]:
            '''The number of accounts per Region this operation can fail in before CloudFormation stops the operation in that Region.

            If the operation is stopped in a Region, CloudFormation doesn't attempt the operation in any subsequent Regions.

            Conditional: You must specify either ``FailureToleranceCount`` or ``FailureTolerancePercentage`` (but not both).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-failuretolerancecount
            '''
            result = self._values.get("failure_tolerance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def failure_tolerance_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of accounts per Region this stack operation can fail in before CloudFormation stops the operation in that Region.

            If the operation is stopped in a Region, CloudFormation doesn't attempt the operation in any subsequent Regions.

            When calculating the number of accounts based on the specified percentage, CloudFormation rounds *down* to the next whole number.

            Conditional: You must specify either ``FailureToleranceCount`` or ``FailureTolerancePercentage`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-failuretolerancepercentage
            '''
            result = self._values.get("failure_tolerance_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_concurrent_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of accounts in which to perform this operation at one time.

            This is dependent on the value of ``FailureToleranceCount`` . ``MaxConcurrentCount`` is at most one more than the ``FailureToleranceCount`` .

            Note that this setting lets you specify the *maximum* for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling.

            Conditional: You must specify either ``MaxConcurrentCount`` or ``MaxConcurrentPercentage`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-maxconcurrentcount
            '''
            result = self._values.get("max_concurrent_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_concurrent_percentage(self) -> typing.Optional[jsii.Number]:
            '''The maximum percentage of accounts in which to perform this operation at one time.

            When calculating the number of accounts based on the specified percentage, CloudFormation rounds down to the next whole number. This is true except in cases where rounding down would result is zero. In this case, CloudFormation sets the number as one instead.

            Note that this setting lets you specify the *maximum* for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling.

            Conditional: You must specify either ``MaxConcurrentCount`` or ``MaxConcurrentPercentage`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-maxconcurrentpercentage
            '''
            result = self._values.get("max_concurrent_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def region_concurrency_type(self) -> typing.Optional[builtins.str]:
            '''The concurrency type of deploying StackSets operations in Regions, could be in parallel or one Region at a time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-regionconcurrencytype
            '''
            result = self._values.get("region_concurrency_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region_order(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The order of the Regions where you want to perform the stack operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-operationpreferences.html#cfn-cloudformation-stackset-operationpreferences-regionorder
            '''
            result = self._values.get("region_order")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OperationPreferencesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackSetPropsMixin.ParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_key": "parameterKey",
            "parameter_value": "parameterValue",
        },
    )
    class ParameterProperty:
        def __init__(
            self,
            *,
            parameter_key: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Parameter data type.

            :param parameter_key: The key associated with the parameter. If you don't specify a key and value for a particular parameter, CloudFormation uses the default value that's specified in your template.
            :param parameter_value: The input value associated with the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                parameter_property = cloudformation_mixins.CfnStackSetPropsMixin.ParameterProperty(
                    parameter_key="parameterKey",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__812c4feb6b2568e2f80747cc131dc0b4614545d572f88d756ce0754012bc9bc5)
                check_type(argname="argument parameter_key", value=parameter_key, expected_type=type_hints["parameter_key"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_key is not None:
                self._values["parameter_key"] = parameter_key
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_key(self) -> typing.Optional[builtins.str]:
            '''The key associated with the parameter.

            If you don't specify a key and value for a particular parameter, CloudFormation uses the default value that's specified in your template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html#cfn-cloudformation-stackset-parameter-parameterkey
            '''
            result = self._values.get("parameter_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''The input value associated with the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-parameter.html#cfn-cloudformation-stackset-parameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnStackSetPropsMixin.StackInstancesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_targets": "deploymentTargets",
            "parameter_overrides": "parameterOverrides",
            "regions": "regions",
        },
    )
    class StackInstancesProperty:
        def __init__(
            self,
            *,
            deployment_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackSetPropsMixin.DeploymentTargetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parameter_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStackSetPropsMixin.ParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Stack instances in some specific accounts and Regions.

            :param deployment_targets: The AWS Organizations accounts or AWS accounts to deploy stacks to in the specified Regions.
            :param parameter_overrides: A list of StackSet parameters whose values you want to override in the selected stack instances.
            :param regions: The names of one or more Regions where you want to create stack instances using the specified AWS accounts .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                stack_instances_property = cloudformation_mixins.CfnStackSetPropsMixin.StackInstancesProperty(
                    deployment_targets=cloudformation_mixins.CfnStackSetPropsMixin.DeploymentTargetsProperty(
                        account_filter_type="accountFilterType",
                        accounts=["accounts"],
                        accounts_url="accountsUrl",
                        organizational_unit_ids=["organizationalUnitIds"]
                    ),
                    parameter_overrides=[cloudformation_mixins.CfnStackSetPropsMixin.ParameterProperty(
                        parameter_key="parameterKey",
                        parameter_value="parameterValue"
                    )],
                    regions=["regions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ddfc45d62903ab3cb75abc31c05776b382aa4faeff9cb36364c958b771382efc)
                check_type(argname="argument deployment_targets", value=deployment_targets, expected_type=type_hints["deployment_targets"])
                check_type(argname="argument parameter_overrides", value=parameter_overrides, expected_type=type_hints["parameter_overrides"])
                check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if deployment_targets is not None:
                self._values["deployment_targets"] = deployment_targets
            if parameter_overrides is not None:
                self._values["parameter_overrides"] = parameter_overrides
            if regions is not None:
                self._values["regions"] = regions

        @builtins.property
        def deployment_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.DeploymentTargetsProperty"]]:
            '''The AWS Organizations accounts or AWS accounts to deploy stacks to in the specified Regions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-deploymenttargets
            '''
            result = self._values.get("deployment_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.DeploymentTargetsProperty"]], result)

        @builtins.property
        def parameter_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.ParameterProperty"]]]]:
            '''A list of StackSet parameters whose values you want to override in the selected stack instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-parameteroverrides
            '''
            result = self._values.get("parameter_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStackSetPropsMixin.ParameterProperty"]]]], result)

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of one or more Regions where you want to create stack instances using the specified AWS accounts .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-stackset-stackinstances.html#cfn-cloudformation-stackset-stackinstances-regions
            '''
            result = self._values.get("regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackInstancesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnTypeActivationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_update": "autoUpdate",
        "execution_role_arn": "executionRoleArn",
        "logging_config": "loggingConfig",
        "major_version": "majorVersion",
        "public_type_arn": "publicTypeArn",
        "publisher_id": "publisherId",
        "type": "type",
        "type_name": "typeName",
        "type_name_alias": "typeNameAlias",
        "version_bump": "versionBump",
    },
)
class CfnTypeActivationMixinProps:
    def __init__(
        self,
        *,
        auto_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTypeActivationPropsMixin.LoggingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        major_version: typing.Optional[builtins.str] = None,
        public_type_arn: typing.Optional[builtins.str] = None,
        publisher_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        type_name: typing.Optional[builtins.str] = None,
        type_name_alias: typing.Optional[builtins.str] = None,
        version_bump: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTypeActivationPropsMixin.

        :param auto_update: Whether to automatically update the extension in this account and Region when a new *minor* version is published by the extension publisher. Major versions released by the publisher must be manually updated. The default is ``true`` .
        :param execution_role_arn: The name of the IAM execution role to use to activate the extension.
        :param logging_config: Specifies logging configuration information for an extension.
        :param major_version: The major version of this extension you want to activate, if multiple major versions are available. The default is the latest major version. CloudFormation uses the latest available *minor* version of the major version selected. You can specify ``MajorVersion`` or ``VersionBump`` , but not both.
        :param public_type_arn: The Amazon Resource Number (ARN) of the public extension. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param publisher_id: The ID of the extension publisher. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param type: The extension type. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param type_name: The name of the extension. Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .
        :param type_name_alias: An alias to assign to the public extension in this account and Region. If you specify an alias for the extension, CloudFormation treats the alias as the extension type name within this account and Region. You must use the alias to refer to the extension in your templates, API calls, and CloudFormation console. An extension alias must be unique within a given account and Region. You can activate the same public resource multiple times in the same account and Region, using different type name aliases.
        :param version_bump: Manually updates a previously-activated type to a new major or minor version, if available. You can also use this parameter to update the value of ``AutoUpdate`` . - ``MAJOR`` : CloudFormation updates the extension to the newest major version, if one is available. - ``MINOR`` : CloudFormation updates the extension to the newest minor version, if one is available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_type_activation_mixin_props = cloudformation_mixins.CfnTypeActivationMixinProps(
                auto_update=False,
                execution_role_arn="executionRoleArn",
                logging_config=cloudformation_mixins.CfnTypeActivationPropsMixin.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                ),
                major_version="majorVersion",
                public_type_arn="publicTypeArn",
                publisher_id="publisherId",
                type="type",
                type_name="typeName",
                type_name_alias="typeNameAlias",
                version_bump="versionBump"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3960b65fb4125dfdf964c5512d40d08d691671ab8c9414d2e029c4d4659b7cd2)
            check_type(argname="argument auto_update", value=auto_update, expected_type=type_hints["auto_update"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument major_version", value=major_version, expected_type=type_hints["major_version"])
            check_type(argname="argument public_type_arn", value=public_type_arn, expected_type=type_hints["public_type_arn"])
            check_type(argname="argument publisher_id", value=publisher_id, expected_type=type_hints["publisher_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            check_type(argname="argument type_name_alias", value=type_name_alias, expected_type=type_hints["type_name_alias"])
            check_type(argname="argument version_bump", value=version_bump, expected_type=type_hints["version_bump"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_update is not None:
            self._values["auto_update"] = auto_update
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if major_version is not None:
            self._values["major_version"] = major_version
        if public_type_arn is not None:
            self._values["public_type_arn"] = public_type_arn
        if publisher_id is not None:
            self._values["publisher_id"] = publisher_id
        if type is not None:
            self._values["type"] = type
        if type_name is not None:
            self._values["type_name"] = type_name
        if type_name_alias is not None:
            self._values["type_name_alias"] = type_name_alias
        if version_bump is not None:
            self._values["version_bump"] = version_bump

    @builtins.property
    def auto_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to automatically update the extension in this account and Region when a new *minor* version is published by the extension publisher.

        Major versions released by the publisher must be manually updated.

        The default is ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-autoupdate
        '''
        result = self._values.get("auto_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM execution role to use to activate the extension.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTypeActivationPropsMixin.LoggingConfigProperty"]]:
        '''Specifies logging configuration information for an extension.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-loggingconfig
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTypeActivationPropsMixin.LoggingConfigProperty"]], result)

    @builtins.property
    def major_version(self) -> typing.Optional[builtins.str]:
        '''The major version of this extension you want to activate, if multiple major versions are available.

        The default is the latest major version. CloudFormation uses the latest available *minor* version of the major version selected.

        You can specify ``MajorVersion`` or ``VersionBump`` , but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-majorversion
        '''
        result = self._values.get("major_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_type_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the public extension.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-publictypearn
        '''
        result = self._values.get("public_type_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the extension publisher.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-publisherid
        '''
        result = self._values.get("publisher_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The extension type.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name(self) -> typing.Optional[builtins.str]:
        '''The name of the extension.

        Conditional: You must specify ``PublicTypeArn`` , or ``TypeName`` , ``Type`` , and ``PublisherId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-typename
        '''
        result = self._values.get("type_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type_name_alias(self) -> typing.Optional[builtins.str]:
        '''An alias to assign to the public extension in this account and Region.

        If you specify an alias for the extension, CloudFormation treats the alias as the extension type name within this account and Region. You must use the alias to refer to the extension in your templates, API calls, and CloudFormation console.

        An extension alias must be unique within a given account and Region. You can activate the same public resource multiple times in the same account and Region, using different type name aliases.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-typenamealias
        '''
        result = self._values.get("type_name_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_bump(self) -> typing.Optional[builtins.str]:
        '''Manually updates a previously-activated type to a new major or minor version, if available.

        You can also use this parameter to update the value of ``AutoUpdate`` .

        - ``MAJOR`` : CloudFormation updates the extension to the newest major version, if one is available.
        - ``MINOR`` : CloudFormation updates the extension to the newest minor version, if one is available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html#cfn-cloudformation-typeactivation-versionbump
        '''
        result = self._values.get("version_bump")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTypeActivationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTypeActivationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnTypeActivationPropsMixin",
):
    '''The ``AWS::CloudFormation::TypeActivation`` resource activates a public third-party extension, making it available for use in stack templates.

    For information about the CloudFormation registry, see `Managing extensions with the CloudFormation registry <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html>`_ in the *CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-typeactivation.html
    :cloudformationResource: AWS::CloudFormation::TypeActivation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_type_activation_props_mixin = cloudformation_mixins.CfnTypeActivationPropsMixin(cloudformation_mixins.CfnTypeActivationMixinProps(
            auto_update=False,
            execution_role_arn="executionRoleArn",
            logging_config=cloudformation_mixins.CfnTypeActivationPropsMixin.LoggingConfigProperty(
                log_group_name="logGroupName",
                log_role_arn="logRoleArn"
            ),
            major_version="majorVersion",
            public_type_arn="publicTypeArn",
            publisher_id="publisherId",
            type="type",
            type_name="typeName",
            type_name_alias="typeNameAlias",
            version_bump="versionBump"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTypeActivationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::TypeActivation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4ecea5da507450013c3404e9ba9da7576e936c79fdc8b23aaa5209f67750c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b025c322d6652e13d38734a4584a8a9cbadfb6debc0b19c8845c3db46f684992)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77130afbeb64f52e7da306cfff18b898589b35dfb82f754fc45218170e45d073)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTypeActivationMixinProps:
        return typing.cast(CfnTypeActivationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnTypeActivationPropsMixin.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName", "log_role_arn": "logRoleArn"},
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
            log_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains logging configuration information for an extension.

            :param log_group_name: The Amazon CloudWatch Logs group to which CloudFormation sends error logging information when invoking the extension's handlers.
            :param log_role_arn: The Amazon Resource Name (ARN) of the role that CloudFormation should assume when sending log entries to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-typeactivation-loggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
                
                logging_config_property = cloudformation_mixins.CfnTypeActivationPropsMixin.LoggingConfigProperty(
                    log_group_name="logGroupName",
                    log_role_arn="logRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__495b3cf88961a0ff4061eddf5ab49d4ef2a0e92dc2ebad4a31f36ca9165ecee2)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
                check_type(argname="argument log_role_arn", value=log_role_arn, expected_type=type_hints["log_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_role_arn is not None:
                self._values["log_role_arn"] = log_role_arn

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''The Amazon CloudWatch Logs group to which CloudFormation sends error logging information when invoking the extension's handlers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-typeactivation-loggingconfig.html#cfn-cloudformation-typeactivation-loggingconfig-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the role that CloudFormation should assume when sending log entries to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudformation-typeactivation-loggingconfig.html#cfn-cloudformation-typeactivation-loggingconfig-logrolearn
            '''
            result = self._values.get("log_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnWaitConditionHandleMixinProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class CfnWaitConditionHandleMixinProps:
    def __init__(self) -> None:
        '''Properties for CfnWaitConditionHandlePropsMixin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-waitconditionhandle.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_wait_condition_handle_mixin_props = cloudformation_mixins.CfnWaitConditionHandleMixinProps()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWaitConditionHandleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWaitConditionHandlePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnWaitConditionHandlePropsMixin",
):
    '''The ``AWS::CloudFormation::WaitConditionHandle`` type has no properties.

    When you reference the ``WaitConditionHandle`` resource by using the ``Ref`` function, CloudFormation returns a presigned URL. You pass this URL to applications or scripts that are running on your Amazon EC2 instances to send signals to that URL. An associated ``AWS::CloudFormation::WaitCondition`` resource checks the URL for the required number of success signals or for a failure signal.

    For more information, see `Create wait conditions in a CloudFormation template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-waitcondition.html>`_ in the *CloudFormation User Guide* .

    Anytime you add a ``WaitCondition`` resource during a stack update or update a resource with a wait condition, you must associate the wait condition with a new ``WaitConditionHandle`` resource. Don't reuse an old wait condition handle that has already been defined in the template. If you reuse a wait condition handle, the wait condition might evaluate old signals from a previous create or update stack command.

    Updates aren't supported for this resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-waitconditionhandle.html
    :cloudformationResource: AWS::CloudFormation::WaitConditionHandle
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_wait_condition_handle_props_mixin = cloudformation_mixins.CfnWaitConditionHandlePropsMixin(cloudformation_mixins.CfnWaitConditionHandleMixinProps(),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWaitConditionHandleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::WaitConditionHandle``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e449dd285801b85628f7bff485b9a536f4009ff2731e3e4ab96cc2e47d10717f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf3c239cd869a10919f40043c8d31958d1f3abcdedd0f98cb81084ebce11b138)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca62372c0d0dedd23bb9a0ba1277017367fbcff1f165801fcdfb1b8c26fb6c4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWaitConditionHandleMixinProps:
        return typing.cast(CfnWaitConditionHandleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnWaitConditionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "handle": "handle", "timeout": "timeout"},
)
class CfnWaitConditionMixinProps:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        handle: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWaitConditionPropsMixin.

        :param count: The number of success signals that CloudFormation must receive before it continues the stack creation process. When the wait condition receives the requisite number of success signals, CloudFormation resumes the creation of the stack. If the wait condition doesn't receive the specified number of success signals before the Timeout period expires, CloudFormation assumes that the wait condition has failed and rolls the stack back. Updates aren't supported.
        :param handle: A reference to the wait condition handle used to signal this wait condition. Use the ``Ref`` intrinsic function to specify an `AWS::CloudFormation::WaitConditionHandle <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-cloudformation-waitconditionhandle.html>`_ resource. Anytime you add a ``WaitCondition`` resource during a stack update, you must associate the wait condition with a new WaitConditionHandle resource. Don't reuse an old wait condition handle that has already been defined in the template. If you reuse a wait condition handle, the wait condition might evaluate old signals from a previous create or update stack command. Updates aren't supported.
        :param timeout: The length of time (in seconds) to wait for the number of signals that the ``Count`` property specifies. ``Timeout`` is a minimum-bound property, meaning the timeout occurs no sooner than the time you specify, but can occur shortly thereafter. The maximum time that can be specified for this property is 12 hours (43200 seconds). Updates aren't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-waitcondition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
            
            cfn_wait_condition_mixin_props = cloudformation_mixins.CfnWaitConditionMixinProps(
                count=123,
                handle="handle",
                timeout="timeout"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b561794dc47cfd14c9923bf63c5c74791e3d5bdc4cc49f80f4b42d6c5df2ea64)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument handle", value=handle, expected_type=type_hints["handle"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if handle is not None:
            self._values["handle"] = handle
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''The number of success signals that CloudFormation must receive before it continues the stack creation process.

        When the wait condition receives the requisite number of success signals, CloudFormation resumes the creation of the stack. If the wait condition doesn't receive the specified number of success signals before the Timeout period expires, CloudFormation assumes that the wait condition has failed and rolls the stack back.

        Updates aren't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-waitcondition.html#cfn-cloudformation-waitcondition-count
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def handle(self) -> typing.Optional[builtins.str]:
        '''A reference to the wait condition handle used to signal this wait condition.

        Use the ``Ref`` intrinsic function to specify an `AWS::CloudFormation::WaitConditionHandle <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-cloudformation-waitconditionhandle.html>`_ resource.

        Anytime you add a ``WaitCondition`` resource during a stack update, you must associate the wait condition with a new WaitConditionHandle resource. Don't reuse an old wait condition handle that has already been defined in the template. If you reuse a wait condition handle, the wait condition might evaluate old signals from a previous create or update stack command.

        Updates aren't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-waitcondition.html#cfn-cloudformation-waitcondition-handle
        '''
        result = self._values.get("handle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''The length of time (in seconds) to wait for the number of signals that the ``Count`` property specifies.

        ``Timeout`` is a minimum-bound property, meaning the timeout occurs no sooner than the time you specify, but can occur shortly thereafter. The maximum time that can be specified for this property is 12 hours (43200 seconds).

        Updates aren't supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-waitcondition.html#cfn-cloudformation-waitcondition-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWaitConditionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWaitConditionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudformation.mixins.CfnWaitConditionPropsMixin",
):
    '''The ``AWS::CloudFormation::WaitCondition`` resource provides a way to coordinate stack resource creation with configuration actions that are external to the stack creation or to track the status of a configuration process.

    In these situations, we recommend that you associate a ``CreationPolicy`` attribute with the wait condition instead of using a wait condition handle. For more information and an example, see `CreationPolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-creationpolicy.html>`_ in the *CloudFormation User Guide* . If you use a ``CreationPolicy`` with a wait condition, don't specify any of the wait condition's properties.
    .. epigraph::

       If you use AWS PrivateLink , resources in the VPC that respond to wait conditions must have access to CloudFormation , specific Amazon S3 buckets. Resources must send wait condition responses to a presigned Amazon S3 URL. If they can't send responses to Amazon S3 , CloudFormation won't receive a response and the stack operation fails. For more information, see `Access CloudFormation using an interface endpoint ( AWS PrivateLink ) <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/vpc-interface-endpoints.html>`_ in the *CloudFormation User Guide* . > For Amazon EC2 and Amazon EC2 Auto Scaling resources, we recommend that you use a ``CreationPolicy`` attribute instead of wait conditions. Add a ``CreationPolicy`` attribute to those resources, and use the ``cfn-signal`` helper script to signal when an instance creation process has completed successfully.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudformation-waitcondition.html
    :cloudformationResource: AWS::CloudFormation::WaitCondition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudformation import mixins as cloudformation_mixins
        
        cfn_wait_condition_props_mixin = cloudformation_mixins.CfnWaitConditionPropsMixin(cloudformation_mixins.CfnWaitConditionMixinProps(
            count=123,
            handle="handle",
            timeout="timeout"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWaitConditionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudFormation::WaitCondition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a2a38f557f3ce909f107578d4328d65bf0e415e6a7d6e87a8a3e66983ad546)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3302a2b19976c05ec469d4168268baa7783b4dfcb2cee806b6bdf41925360614)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76417122b39493dece6e006f629d9b390cd659c321f06232bfaa7532a5ce25d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWaitConditionMixinProps:
        return typing.cast(CfnWaitConditionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnCustomResourceMixinProps",
    "CfnCustomResourcePropsMixin",
    "CfnGuardHookMixinProps",
    "CfnGuardHookPropsMixin",
    "CfnHookDefaultVersionMixinProps",
    "CfnHookDefaultVersionPropsMixin",
    "CfnHookTypeConfigMixinProps",
    "CfnHookTypeConfigPropsMixin",
    "CfnHookVersionMixinProps",
    "CfnHookVersionPropsMixin",
    "CfnLambdaHookMixinProps",
    "CfnLambdaHookPropsMixin",
    "CfnMacroMixinProps",
    "CfnMacroPropsMixin",
    "CfnModuleDefaultVersionMixinProps",
    "CfnModuleDefaultVersionPropsMixin",
    "CfnModuleVersionMixinProps",
    "CfnModuleVersionPropsMixin",
    "CfnPublicTypeVersionMixinProps",
    "CfnPublicTypeVersionPropsMixin",
    "CfnPublisherMixinProps",
    "CfnPublisherPropsMixin",
    "CfnResourceDefaultVersionMixinProps",
    "CfnResourceDefaultVersionPropsMixin",
    "CfnResourceVersionMixinProps",
    "CfnResourceVersionPropsMixin",
    "CfnStackMixinProps",
    "CfnStackPropsMixin",
    "CfnStackSetMixinProps",
    "CfnStackSetPropsMixin",
    "CfnTypeActivationMixinProps",
    "CfnTypeActivationPropsMixin",
    "CfnWaitConditionHandleMixinProps",
    "CfnWaitConditionHandlePropsMixin",
    "CfnWaitConditionMixinProps",
    "CfnWaitConditionPropsMixin",
]

publication.publish()

def _typecheckingstub__c2bc211907550ae2cbe1295611d8d47a48cd8ac71f7cee09f9f5f8cfdbfb3526(
    *,
    service_timeout: typing.Optional[jsii.Number] = None,
    service_token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc671c65f20d38959c3c95dac6907a019841cfe71a2b699f9f4e5e79bc60c57(
    props: typing.Union[CfnCustomResourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2088255e09043e85440b492721425214c9211a6ad05e5193cac64856e724dc3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fce90ef2e732a96bb0495fe0d5c7b080fa8f356f62d0c73743c9a2a2b3eb808(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f2785017f90af2b6ba3b2a992462488b80c9036a8eb7187c9f2715c308dd4e(
    *,
    alias: typing.Optional[builtins.str] = None,
    execution_role: typing.Optional[builtins.str] = None,
    failure_mode: typing.Optional[builtins.str] = None,
    hook_status: typing.Optional[builtins.str] = None,
    log_bucket: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGuardHookPropsMixin.OptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGuardHookPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stack_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGuardHookPropsMixin.StackFiltersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGuardHookPropsMixin.TargetFiltersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacbde3b2a5fc9f73e57ad2aa241d17d5fcb9d5efb203b0cb2e101be22e43d0a(
    props: typing.Union[CfnGuardHookMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce25bd47c17d2f87d3531d01e6e8e72fc758d6c7e89fa383c5755a53af990bd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05cda488fc33650c0335c898b01db2b1ce64995329eccc5fae112b21bbee7d7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105efa52488deb50e130fbccf1fa3a7b53bb0557a1bce49acbea112f8310c9dc(
    *,
    action: typing.Optional[builtins.str] = None,
    invocation_point: typing.Optional[builtins.str] = None,
    target_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35d4fd4d5399176b0f3dc44a5b0ed7be51156e6ca54ae9ea0fd4f469fcd88d7(
    *,
    input_params: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGuardHookPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3859d18635353f751a50fcc26c4c59378dd4b3764f10350e08e8092f36017dd6(
    *,
    uri: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e46394e8691f5fd9c0e36c979f212b4d865d2ef2daf02f66f1603892c6f6947(
    *,
    filtering_criteria: typing.Optional[builtins.str] = None,
    stack_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGuardHookPropsMixin.StackNamesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stack_roles: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGuardHookPropsMixin.StackRolesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f7079a4dcc1b5b824fa1bbd03671703db5e70cd45ea18312f68e6e24ef1267(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226e629068c06e4a33bab8a41e098a9f868ca4578a6763b5f48e1fb80aada585(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5ccf579ee6a5bb653c147558f98d4001d5e8e70f1602143345e03c2f371f6f(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    invocation_points: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGuardHookPropsMixin.HookTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ee3982c76a548518fcb400f607e6fdf87c5199a8fafd430948199cd9c63b39(
    *,
    type_name: typing.Optional[builtins.str] = None,
    type_version_arn: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1246c39dba98b649df85eb7e7db20e5c2e1d5f1a12863e5a4a0360af3cdfec(
    props: typing.Union[CfnHookDefaultVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5ea19c9dff1f7a0752d25f24e044b425ca4897578f66dd03cb76d87a78c73f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fffd003a829e0c3420a3e887768025c4bf32294372297521f6d629401b9587(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f177c4ff8303b775fc7629d2c3746a21e904a011d2caf48500e389607046236(
    *,
    configuration: typing.Optional[builtins.str] = None,
    configuration_alias: typing.Optional[builtins.str] = None,
    type_arn: typing.Optional[builtins.str] = None,
    type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21bfbe90b8c6c27cfe7c696c02a55138ab4782feb2b1cdd0b52b32bb12e825c7(
    props: typing.Union[CfnHookTypeConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6e87c8c5586ab513d04dc0fb3331db7e719a00b3024dfd092e1fcbfcc99896(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac48ae7ff7cca726350aec55fa19ec05224f87e39e88cc2249d33b6fb200484c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2e7d068847c0c435dd51b41d1056aef91fc94dcd1c231432d39d0b2c4cea3d(
    *,
    execution_role_arn: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHookVersionPropsMixin.LoggingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_handler_package: typing.Optional[builtins.str] = None,
    type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d88066c1e7a09e7516497c71ba292a91ad264028f98a39c99408e9d57d7e85(
    props: typing.Union[CfnHookVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef07c16b65ed4d51fd7b16dc24e1b207ff7d96da7fd6fdba7b3a801fc6edde9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ffb85180794faabb01c643edb3c148fdafe7477ec66c3a4513c75e63abbc77(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41edbb56e29c29806e6fe87fae8d7e3ab2cc9df865980197388f9980c982e2b(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
    log_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c06249b15b252ffff22cea2e223c0fb1e80dc74302380a717168372e0e17487(
    *,
    alias: typing.Optional[builtins.str] = None,
    execution_role: typing.Optional[builtins.str] = None,
    failure_mode: typing.Optional[builtins.str] = None,
    hook_status: typing.Optional[builtins.str] = None,
    lambda_function: typing.Optional[builtins.str] = None,
    stack_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLambdaHookPropsMixin.StackFiltersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLambdaHookPropsMixin.TargetFiltersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_operations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f9a4f0c826a6fc3aa5cc8692725811cb0d77dd00e17e314c8fc12e63e0d76d(
    props: typing.Union[CfnLambdaHookMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2bc97581c6861ade19e87a51626f749e4a4ec1877b77c45738b49beb292d40(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3182411f26a8435a56e1b0f927dcfd26a672c1a34825ec6f4326b58a347ea6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bf38b9644c9bbfef34b8031ec03393ce0d68694b7e3a8cd3902bd5fa72878d(
    *,
    action: typing.Optional[builtins.str] = None,
    invocation_point: typing.Optional[builtins.str] = None,
    target_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ed93446cda2e9b78329fd0c50d7d750c07913cbafa40b29ff8fa1b5151a19b(
    *,
    filtering_criteria: typing.Optional[builtins.str] = None,
    stack_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLambdaHookPropsMixin.StackNamesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stack_roles: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLambdaHookPropsMixin.StackRolesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7c46b4a8126adea9a69a069264eb2c473e2a7160c09cf599cd9f6013cef55d(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525c022dbe8fd435bf17946d02b75bf2eaa7b3f2ca41294586ae21de41472733(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de3eb2074d0dab8c945e1c42f3149069d0f19d1a6bb5c6cf399ae90fe43f4c5(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    invocation_points: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLambdaHookPropsMixin.HookTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70995a79d21f9cb0016a3cc418bf8c38e6a5a6ec8f3f5b816c1844503ad9574(
    *,
    description: typing.Optional[builtins.str] = None,
    function_name: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_role_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0092f3cb79b7804c3af6db1deec32acf1d389fae7a50419ba65125d58fe74b8e(
    props: typing.Union[CfnMacroMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9d5433926429f8662589ff067205229ceee6429a7e0766a2c65cd7dfe24146(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cd2087f2a9fe6d407686060c7e7fc0404ec65306142db17565ac75a4b95060(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5944749315c89043c68e202f37035cd4f6694c2fbec03a26263349eb37bd4b3(
    *,
    arn: typing.Optional[builtins.str] = None,
    module_name: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7d727641781ce41c14f41d95084b62c9f33d46b2a38e0970d1ddbcc202c79b(
    props: typing.Union[CfnModuleDefaultVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba28c1885328e89802e770a89221f9c7f20b235df66549633b8895c5d8be5df(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b91e29c9b6689fbe1f053086239983d632a09e2afa8bcdbfd241e783178844(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde2a44021c4ab4489723db6a6c4af717aca8f520ec7e266f8b5c720b2c4e37b(
    *,
    module_name: typing.Optional[builtins.str] = None,
    module_package: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632e9388780ed9b70879996eca8d96c461ca4552fa51e603ddfc6008ee7a2675(
    props: typing.Union[CfnModuleVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f34f47bfa50cafff6121a81c811fb303d4065e96bd36ccda670faaedfa2d5c0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4c9f2d1e1263ef172ce0536d953310a3d1087e4e9838b2ba9763ce21d4c302(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2eb8092c3a922c1b941501013d3616d0c15819ef89cef4be65b5a4f8b37ee6(
    *,
    arn: typing.Optional[builtins.str] = None,
    log_delivery_bucket: typing.Optional[builtins.str] = None,
    public_version_number: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8a5239fb158d4330d99d26b344da738c8c32db8dc54203a9747a6ea5e89f5d(
    props: typing.Union[CfnPublicTypeVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc72cf2d18996a0e4bb573e077121c0a8e134744f656c4de62ac056b9559e63(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859b5e82cbf2d6fa0fc62d451cfd3ed90d894f71003dbd386640b202a13a07e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48d91e0b0e3a64273daffa22c162b0ac6f0e01d16b922c032ed7b37a4481e50(
    *,
    accept_terms_and_conditions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    connection_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a69f0c17f518810bfddc338355c92b82f5d57eb2b8e2bace3ce3a83d731f751(
    props: typing.Union[CfnPublisherMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437ce047d8a538f90b5ab464b302e620436034ca12842d0078875615c6b14f57(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d33877b7d8fe013b959c299ec91fe6d830622f72bce5c89a8b8a060a4b90923(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82505ab6eb872456580b040b982563c28fa47b856c019dd282064adbb78beefc(
    *,
    type_name: typing.Optional[builtins.str] = None,
    type_version_arn: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9dbc74f4956367064ccea1e371ec9ecff905829be73575efa1f13e95df38e5(
    props: typing.Union[CfnResourceDefaultVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718699835598d423e28e2f850da4973658a219b462d9018dbb10ddaf42d30cc8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d88892c6165569eb225916e5dc05f92893172f9ed6935b450c8d9b7dea0dff9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453b227b1207da7b32b7a1eea867b29fdc41de631528af43c8e9be6a247840b0(
    *,
    execution_role_arn: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceVersionPropsMixin.LoggingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_handler_package: typing.Optional[builtins.str] = None,
    type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63efeeeba5e7e18039863e55febc6310943acdcd05fcc0981e5f675df4b2357(
    props: typing.Union[CfnResourceVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234a37362b89d9f1a633e370944429784ce81a2a35041a8b58c2b88316a10324(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2cb04d5bbabe53c7dad6b59aba0ad42e0f7013b697e40c15c0b2440590abde(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad0aec9e2b35f0e22b0017c477f81278bad01322c169006e2f7715fb89a54aa(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
    log_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1bcf14f1bfab1c8a1503ec1d4d2cda4bc110879e45e2da4f9f0631be1b28d75(
    *,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_url: typing.Optional[builtins.str] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c69d4cb942c2c6d0b9543619efc09ac7d5059a1818de88b8a3f540ceb0e31a(
    props: typing.Union[CfnStackMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc3edb586ee0d8ff2fb660c0db3a6078c5bf9b7116e0589e365246126873733(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77d252fad8419571a43da49bf88ce2498fbdee9dc338537b8e391f061bdeeb7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481dcfcbb5419f66b20654b75fdd0391bbbf4af177d9f893940831c29d285132(
    *,
    description: typing.Optional[builtins.str] = None,
    export_name: typing.Optional[builtins.str] = None,
    output_key: typing.Optional[builtins.str] = None,
    output_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d578ce42fb285aff99bff46eac06dcc11f34520ffbebf432240fe6bbe1e8845(
    *,
    administration_role_arn: typing.Optional[builtins.str] = None,
    auto_deployment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackSetPropsMixin.AutoDeploymentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    call_as: typing.Optional[builtins.str] = None,
    capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    execution_role_name: typing.Optional[builtins.str] = None,
    managed_execution: typing.Any = None,
    operation_preferences: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackSetPropsMixin.OperationPreferencesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackSetPropsMixin.ParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    permission_model: typing.Optional[builtins.str] = None,
    stack_instances_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackSetPropsMixin.StackInstancesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stack_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_body: typing.Optional[builtins.str] = None,
    template_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49ca082e9333a7e23f97acd9b4c18c88c018a71798365249b9ce98f875c2e8c(
    props: typing.Union[CfnStackSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0590fef52b6029507b8f584cdca297a76d1dd3a7466e9985354223764a97c8c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9ab692a764dbaabafd32ff8881e154f98a08739016c3bd44a3f62ef21c3a8e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787a979fc4c0da0be9b187805e465f8383a7d6ad2191e22d487faf76f6dc8bff(
    *,
    depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    retain_stacks_on_account_removal: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78a10d40a3fb403ccc0b880781c797128dbae6de26b6fbd6ca4fc5e268daaf3(
    *,
    account_filter_type: typing.Optional[builtins.str] = None,
    accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    accounts_url: typing.Optional[builtins.str] = None,
    organizational_unit_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d2fc930e2369a5245b8430a63c173be831c2f06e6ba241a3d88feb17cb9a7e(
    *,
    active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29ced7ffb9ee4f5d1a82acfae3e64eefef1f7c3b911be7df1a3206be3c6ef9e(
    *,
    concurrency_mode: typing.Optional[builtins.str] = None,
    failure_tolerance_count: typing.Optional[jsii.Number] = None,
    failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
    max_concurrent_count: typing.Optional[jsii.Number] = None,
    max_concurrent_percentage: typing.Optional[jsii.Number] = None,
    region_concurrency_type: typing.Optional[builtins.str] = None,
    region_order: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812c4feb6b2568e2f80747cc131dc0b4614545d572f88d756ce0754012bc9bc5(
    *,
    parameter_key: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfc45d62903ab3cb75abc31c05776b382aa4faeff9cb36364c958b771382efc(
    *,
    deployment_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackSetPropsMixin.DeploymentTargetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameter_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStackSetPropsMixin.ParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3960b65fb4125dfdf964c5512d40d08d691671ab8c9414d2e029c4d4659b7cd2(
    *,
    auto_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTypeActivationPropsMixin.LoggingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    major_version: typing.Optional[builtins.str] = None,
    public_type_arn: typing.Optional[builtins.str] = None,
    publisher_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    type_name: typing.Optional[builtins.str] = None,
    type_name_alias: typing.Optional[builtins.str] = None,
    version_bump: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4ecea5da507450013c3404e9ba9da7576e936c79fdc8b23aaa5209f67750c4(
    props: typing.Union[CfnTypeActivationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b025c322d6652e13d38734a4584a8a9cbadfb6debc0b19c8845c3db46f684992(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77130afbeb64f52e7da306cfff18b898589b35dfb82f754fc45218170e45d073(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495b3cf88961a0ff4061eddf5ab49d4ef2a0e92dc2ebad4a31f36ca9165ecee2(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
    log_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e449dd285801b85628f7bff485b9a536f4009ff2731e3e4ab96cc2e47d10717f(
    props: typing.Union[CfnWaitConditionHandleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3c239cd869a10919f40043c8d31958d1f3abcdedd0f98cb81084ebce11b138(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca62372c0d0dedd23bb9a0ba1277017367fbcff1f165801fcdfb1b8c26fb6c4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b561794dc47cfd14c9923bf63c5c74791e3d5bdc4cc49f80f4b42d6c5df2ea64(
    *,
    count: typing.Optional[jsii.Number] = None,
    handle: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a2a38f557f3ce909f107578d4328d65bf0e415e6a7d6e87a8a3e66983ad546(
    props: typing.Union[CfnWaitConditionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3302a2b19976c05ec469d4168268baa7783b4dfcb2cee806b6bdf41925360614(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76417122b39493dece6e006f629d9b390cd659c321f06232bfaa7532a5ce25d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
