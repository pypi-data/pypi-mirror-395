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
    jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "block_public_policy": "blockPublicPolicy",
        "resource_policy": "resourcePolicy",
        "secret_id": "secretId",
    },
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        block_public_policy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        resource_policy: typing.Any = None,
        secret_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param block_public_policy: Specifies whether to block resource-based policies that allow broad access to the secret. By default, Secrets Manager blocks policies that allow broad access, for example those that use a wildcard for the principal.
        :param resource_policy: A JSON-formatted string for an AWS resource-based policy. For example policies, see `Permissions policy examples <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html>`_ .
        :param secret_id: The ARN or name of the secret to attach the resource-based policy. For an ARN, we recommend that you specify a complete ARN rather than a partial ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
            
            # resource_policy: Any
            
            cfn_resource_policy_mixin_props = secretsmanager_mixins.CfnResourcePolicyMixinProps(
                block_public_policy=False,
                resource_policy=resource_policy,
                secret_id="secretId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018dd948e2299c43af2943c3ae8ae346b7d70c84aab707c7dea96a6c18b41f1c)
            check_type(argname="argument block_public_policy", value=block_public_policy, expected_type=type_hints["block_public_policy"])
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if block_public_policy is not None:
            self._values["block_public_policy"] = block_public_policy
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy
        if secret_id is not None:
            self._values["secret_id"] = secret_id

    @builtins.property
    def block_public_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether to block resource-based policies that allow broad access to the secret.

        By default, Secrets Manager blocks policies that allow broad access, for example those that use a wildcard for the principal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-blockpublicpolicy
        '''
        result = self._values.get("block_public_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def resource_policy(self) -> typing.Any:
        '''A JSON-formatted string for an AWS resource-based policy.

        For example policies, see `Permissions policy examples <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-resourcepolicy
        '''
        result = self._values.get("resource_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def secret_id(self) -> typing.Optional[builtins.str]:
        '''The ARN or name of the secret to attach the resource-based policy.

        For an ARN, we recommend that you specify a complete ARN rather than a partial ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html#cfn-secretsmanager-resourcepolicy-secretid
        '''
        result = self._values.get("secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourcePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnResourcePolicyPropsMixin",
):
    '''Attaches a resource-based permission policy to a secret.

    A resource-based policy is optional. If a secret already has a resource policy attached, you must first remove it before attaching a new policy using this CloudFormation resource. You can remove the policy using the `console <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_resource-policies.html>`_ , `CLI <https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/delete-resource-policy.html>`_ , or `API <https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_DeleteResourcePolicy.html>`_ . For more information, see `Authentication and access control for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html>`_ .

    *Required permissions:* ``secretsmanager:PutResourcePolicy`` , ``secretsmanager:GetResourcePolicy`` . For more information, see `IAM policy actions for Secrets Manager <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssecretsmanager.html#awssecretsmanager-actions-as-permissions>`_ and `Authentication and access control in Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-resourcepolicy.html
    :cloudformationResource: AWS::SecretsManager::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
        
        # resource_policy: Any
        
        cfn_resource_policy_props_mixin = secretsmanager_mixins.CfnResourcePolicyPropsMixin(secretsmanager_mixins.CfnResourcePolicyMixinProps(
            block_public_policy=False,
            resource_policy=resource_policy,
            secret_id="secretId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecretsManager::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a8c36f7c6e67d027b26742d240c9ecf3947283dd538aba4b321d71d581d651)
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
            type_hints = typing.get_type_hints(_typecheckingstub__871d472dcacd8c19d9fe154b24d10bb75323a43acf26f9ba7d484ee5dc7346ff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504bfb77c7cfb6a43dc53f5d362c7b5718d306ea3f8d0141ccbeb94f43f825b6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourcePolicyMixinProps:
        return typing.cast(CfnResourcePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnRotationScheduleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "external_secret_rotation_metadata": "externalSecretRotationMetadata",
        "external_secret_rotation_role_arn": "externalSecretRotationRoleArn",
        "hosted_rotation_lambda": "hostedRotationLambda",
        "rotate_immediately_on_update": "rotateImmediatelyOnUpdate",
        "rotation_lambda_arn": "rotationLambdaArn",
        "rotation_rules": "rotationRules",
        "secret_id": "secretId",
    },
)
class CfnRotationScheduleMixinProps:
    def __init__(
        self,
        *,
        external_secret_rotation_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRotationSchedulePropsMixin.ExternalSecretRotationMetadataItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        external_secret_rotation_role_arn: typing.Optional[builtins.str] = None,
        hosted_rotation_lambda: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRotationSchedulePropsMixin.HostedRotationLambdaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rotate_immediately_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        rotation_lambda_arn: typing.Optional[builtins.str] = None,
        rotation_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRotationSchedulePropsMixin.RotationRulesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        secret_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRotationSchedulePropsMixin.

        :param external_secret_rotation_metadata: The list of metadata needed to successfully rotate a managed external secret.
        :param external_secret_rotation_role_arn: The ARN of the IAM role that is used by Secrets Manager to rotate a managed external secret.
        :param hosted_rotation_lambda: Creates a new Lambda rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ . To use a rotation function that already exists, specify ``RotationLambdaARN`` instead. You must specify ``Transform: AWS::SecretsManager-2024-09-16`` at the beginning of the CloudFormation template. Transforms are macros hosted by AWS CloudFormation that help you create and manage complex infrastructure. The ``Transform: AWS::SecretsManager-2024-09-16`` transform automatically extends the CloudFormation stack to include a nested stack (of type ``AWS::CloudFormation::Stack`` ), which then creates and updates on your behalf during subsequent stack operations, the appropriate rotation Lambda function for your database or service. For general information on transforms, see the `AWS CloudFormation documentation. <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-reference.html>`_ For Amazon RDS master user credentials, see `AWS::RDS::DBCluster MasterUserSecret <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html>`_ . For Amazon Redshift admin user credentials, see `AWS::Redshift::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html>`_ .
        :param rotate_immediately_on_update: Determines whether to rotate the secret immediately or wait until the next scheduled rotation window when the rotation schedule is updated. The rotation schedule is defined in ``RotationRules`` . The default for ``RotateImmediatelyOnUpdate`` is ``true`` . If you don't specify this value, Secrets Manager rotates the secret immediately. If you set ``RotateImmediatelyOnUpdate`` to ``false`` , Secrets Manager tests the rotation configuration by running the ```testSecret`` step <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ of the Lambda rotation function. This test creates an ``AWSPENDING`` version of the secret and then removes it. .. epigraph:: When changing an existing rotation schedule and setting ``RotateImmediatelyOnUpdate`` to ``false`` : - If using ``AutomaticallyAfterDays`` or a ``ScheduleExpression`` with ``rate()`` , the previously scheduled rotation might still occur. - To prevent unintended rotations, use a ``ScheduleExpression`` with ``cron()`` for granular control over rotation windows. Rotation is an asynchronous process. For more information, see `How rotation works <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ .
        :param rotation_lambda_arn: The ARN of an existing Lambda rotation function. To specify a rotation function that is also defined in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function. For Amazon RDS master user credentials, see `AWS::RDS::DBCluster MasterUserSecret <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html>`_ . For Amazon Redshift admin user credentials, see `AWS::Redshift::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html>`_ . To create a new rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ , specify ``HostedRotationLambda`` instead.
        :param rotation_rules: A structure that defines the rotation configuration for this secret.
        :param secret_id: The ARN or name of the secret to rotate. This is unique for each rotation schedule definition. To reference a secret also created in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
            
            cfn_rotation_schedule_mixin_props = secretsmanager_mixins.CfnRotationScheduleMixinProps(
                external_secret_rotation_metadata=[secretsmanager_mixins.CfnRotationSchedulePropsMixin.ExternalSecretRotationMetadataItemProperty(
                    key="key",
                    value="value"
                )],
                external_secret_rotation_role_arn="externalSecretRotationRoleArn",
                hosted_rotation_lambda=secretsmanager_mixins.CfnRotationSchedulePropsMixin.HostedRotationLambdaProperty(
                    exclude_characters="excludeCharacters",
                    kms_key_arn="kmsKeyArn",
                    master_secret_arn="masterSecretArn",
                    master_secret_kms_key_arn="masterSecretKmsKeyArn",
                    rotation_lambda_name="rotationLambdaName",
                    rotation_type="rotationType",
                    runtime="runtime",
                    superuser_secret_arn="superuserSecretArn",
                    superuser_secret_kms_key_arn="superuserSecretKmsKeyArn",
                    vpc_security_group_ids="vpcSecurityGroupIds",
                    vpc_subnet_ids="vpcSubnetIds"
                ),
                rotate_immediately_on_update=False,
                rotation_lambda_arn="rotationLambdaArn",
                rotation_rules=secretsmanager_mixins.CfnRotationSchedulePropsMixin.RotationRulesProperty(
                    automatically_after_days=123,
                    duration="duration",
                    schedule_expression="scheduleExpression"
                ),
                secret_id="secretId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dcba8a53bd95719a1b276b48aea21c780d15255d2268cff375d8b0d6d565695)
            check_type(argname="argument external_secret_rotation_metadata", value=external_secret_rotation_metadata, expected_type=type_hints["external_secret_rotation_metadata"])
            check_type(argname="argument external_secret_rotation_role_arn", value=external_secret_rotation_role_arn, expected_type=type_hints["external_secret_rotation_role_arn"])
            check_type(argname="argument hosted_rotation_lambda", value=hosted_rotation_lambda, expected_type=type_hints["hosted_rotation_lambda"])
            check_type(argname="argument rotate_immediately_on_update", value=rotate_immediately_on_update, expected_type=type_hints["rotate_immediately_on_update"])
            check_type(argname="argument rotation_lambda_arn", value=rotation_lambda_arn, expected_type=type_hints["rotation_lambda_arn"])
            check_type(argname="argument rotation_rules", value=rotation_rules, expected_type=type_hints["rotation_rules"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_secret_rotation_metadata is not None:
            self._values["external_secret_rotation_metadata"] = external_secret_rotation_metadata
        if external_secret_rotation_role_arn is not None:
            self._values["external_secret_rotation_role_arn"] = external_secret_rotation_role_arn
        if hosted_rotation_lambda is not None:
            self._values["hosted_rotation_lambda"] = hosted_rotation_lambda
        if rotate_immediately_on_update is not None:
            self._values["rotate_immediately_on_update"] = rotate_immediately_on_update
        if rotation_lambda_arn is not None:
            self._values["rotation_lambda_arn"] = rotation_lambda_arn
        if rotation_rules is not None:
            self._values["rotation_rules"] = rotation_rules
        if secret_id is not None:
            self._values["secret_id"] = secret_id

    @builtins.property
    def external_secret_rotation_metadata(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationSchedulePropsMixin.ExternalSecretRotationMetadataItemProperty"]]]]:
        '''The list of metadata needed to successfully rotate a managed external secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-externalsecretrotationmetadata
        '''
        result = self._values.get("external_secret_rotation_metadata")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationSchedulePropsMixin.ExternalSecretRotationMetadataItemProperty"]]]], result)

    @builtins.property
    def external_secret_rotation_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that is used by Secrets Manager to rotate a managed external secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-externalsecretrotationrolearn
        '''
        result = self._values.get("external_secret_rotation_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosted_rotation_lambda(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationSchedulePropsMixin.HostedRotationLambdaProperty"]]:
        '''Creates a new Lambda rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ . To use a rotation function that already exists, specify ``RotationLambdaARN`` instead.

        You must specify ``Transform: AWS::SecretsManager-2024-09-16`` at the beginning of the CloudFormation template. Transforms are macros hosted by AWS CloudFormation that help you create and manage complex infrastructure. The ``Transform: AWS::SecretsManager-2024-09-16`` transform automatically extends the CloudFormation stack to include a nested stack (of type ``AWS::CloudFormation::Stack`` ), which then creates and updates on your behalf during subsequent stack operations, the appropriate rotation Lambda function for your database or service. For general information on transforms, see the `AWS CloudFormation documentation. <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-reference.html>`_

        For Amazon RDS master user credentials, see `AWS::RDS::DBCluster MasterUserSecret <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html>`_ .

        For Amazon Redshift admin user credentials, see `AWS::Redshift::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda
        '''
        result = self._values.get("hosted_rotation_lambda")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationSchedulePropsMixin.HostedRotationLambdaProperty"]], result)

    @builtins.property
    def rotate_immediately_on_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Determines whether to rotate the secret immediately or wait until the next scheduled rotation window when the rotation schedule is updated.

        The rotation schedule is defined in ``RotationRules`` .

        The default for ``RotateImmediatelyOnUpdate`` is ``true`` . If you don't specify this value, Secrets Manager rotates the secret immediately.

        If you set ``RotateImmediatelyOnUpdate`` to ``false`` , Secrets Manager tests the rotation configuration by running the ```testSecret`` step <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ of the Lambda rotation function. This test creates an ``AWSPENDING`` version of the secret and then removes it.
        .. epigraph::

           When changing an existing rotation schedule and setting ``RotateImmediatelyOnUpdate`` to ``false`` :

           - If using ``AutomaticallyAfterDays`` or a ``ScheduleExpression`` with ``rate()`` , the previously scheduled rotation might still occur.
           - To prevent unintended rotations, use a ``ScheduleExpression`` with ``cron()`` for granular control over rotation windows.

        Rotation is an asynchronous process. For more information, see `How rotation works <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotateimmediatelyonupdate
        '''
        result = self._values.get("rotate_immediately_on_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def rotation_lambda_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an existing Lambda rotation function.

        To specify a rotation function that is also defined in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function.

        For Amazon RDS master user credentials, see `AWS::RDS::DBCluster MasterUserSecret <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html>`_ .

        For Amazon Redshift admin user credentials, see `AWS::Redshift::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html>`_ .

        To create a new rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ , specify ``HostedRotationLambda`` instead.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationlambdaarn
        '''
        result = self._values.get("rotation_lambda_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationSchedulePropsMixin.RotationRulesProperty"]]:
        '''A structure that defines the rotation configuration for this secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-rotationrules
        '''
        result = self._values.get("rotation_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationSchedulePropsMixin.RotationRulesProperty"]], result)

    @builtins.property
    def secret_id(self) -> typing.Optional[builtins.str]:
        '''The ARN or name of the secret to rotate. This is unique for each rotation schedule definition.

        To reference a secret also created in this template, use the `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html#cfn-secretsmanager-rotationschedule-secretid
        '''
        result = self._values.get("secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRotationScheduleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRotationSchedulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnRotationSchedulePropsMixin",
):
    '''Configure the rotation schedule and Lambda rotation function for a secret. For more information, see `How rotation works <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_how.html>`_ .

    For database credentials, refer to the following resources:

    - Amazon RDS master user credentials: `AWS::RDS::DBCluster MasterUserSecret <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html>`_
    - Amazon Redshift admin user credentials: `AWS::Redshift::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html>`_

    Choose one of the following options for the rotation function:

    - Create a new rotation function using ``HostedRotationLambda`` based on a `Secrets Manager rotation function template <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ .
    - Use an existing rotation function by specifying its ARN with ``RotationLambdaARN`` .

    .. epigraph::

       For database secrets defined in the same CloudFormation template as the database or service:

       - Use the `AWS::SecretsManager::SecretTargetAttachment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html>`_ resource to populate the secret with connection details.
       - Add a ``DependsOn`` attribute to the ``RotationSchedule`` resource that uses a ``SecretTargetAttachment`` . This ensures the rotation is configured after the secret is populated with connection details. > You can define only one rotation schedule per secret.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-rotationschedule.html
    :cloudformationResource: AWS::SecretsManager::RotationSchedule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
        
        cfn_rotation_schedule_props_mixin = secretsmanager_mixins.CfnRotationSchedulePropsMixin(secretsmanager_mixins.CfnRotationScheduleMixinProps(
            external_secret_rotation_metadata=[secretsmanager_mixins.CfnRotationSchedulePropsMixin.ExternalSecretRotationMetadataItemProperty(
                key="key",
                value="value"
            )],
            external_secret_rotation_role_arn="externalSecretRotationRoleArn",
            hosted_rotation_lambda=secretsmanager_mixins.CfnRotationSchedulePropsMixin.HostedRotationLambdaProperty(
                exclude_characters="excludeCharacters",
                kms_key_arn="kmsKeyArn",
                master_secret_arn="masterSecretArn",
                master_secret_kms_key_arn="masterSecretKmsKeyArn",
                rotation_lambda_name="rotationLambdaName",
                rotation_type="rotationType",
                runtime="runtime",
                superuser_secret_arn="superuserSecretArn",
                superuser_secret_kms_key_arn="superuserSecretKmsKeyArn",
                vpc_security_group_ids="vpcSecurityGroupIds",
                vpc_subnet_ids="vpcSubnetIds"
            ),
            rotate_immediately_on_update=False,
            rotation_lambda_arn="rotationLambdaArn",
            rotation_rules=secretsmanager_mixins.CfnRotationSchedulePropsMixin.RotationRulesProperty(
                automatically_after_days=123,
                duration="duration",
                schedule_expression="scheduleExpression"
            ),
            secret_id="secretId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRotationScheduleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecretsManager::RotationSchedule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3862fd394e20642f87c5b4c70fbb7d3738395920fa3f1f6977c090a22c12cc04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d96679c13692ef1ecde803204860b3015eb7a96d6f64a0354f3ee3c676664f98)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48e5c0c7c77733230cc5120c624fddeccf537ec660b930c5d04d95460d3f0f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRotationScheduleMixinProps:
        return typing.cast(CfnRotationScheduleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnRotationSchedulePropsMixin.ExternalSecretRotationMetadataItemProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ExternalSecretRotationMetadataItemProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The metadata needed to successfully rotate a managed external secret.

            A list of key value pairs in JSON format specified by the partner. For more information, see `Managed external secret partners <https://docs.aws.amazon.com/secretsmanager/latest/userguide/mes-partners.html>`_ .

            :param key: The key that identifies the item.
            :param value: The value of the specified item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-externalsecretrotationmetadataitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
                
                external_secret_rotation_metadata_item_property = secretsmanager_mixins.CfnRotationSchedulePropsMixin.ExternalSecretRotationMetadataItemProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a99ce69fcfd0a8d8fae6a9228490dec205c7afa960a214e4648b2ee55ed685e8)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key that identifies the item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-externalsecretrotationmetadataitem.html#cfn-secretsmanager-rotationschedule-externalsecretrotationmetadataitem-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the specified item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-externalsecretrotationmetadataitem.html#cfn-secretsmanager-rotationschedule-externalsecretrotationmetadataitem-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExternalSecretRotationMetadataItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnRotationSchedulePropsMixin.HostedRotationLambdaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_characters": "excludeCharacters",
            "kms_key_arn": "kmsKeyArn",
            "master_secret_arn": "masterSecretArn",
            "master_secret_kms_key_arn": "masterSecretKmsKeyArn",
            "rotation_lambda_name": "rotationLambdaName",
            "rotation_type": "rotationType",
            "runtime": "runtime",
            "superuser_secret_arn": "superuserSecretArn",
            "superuser_secret_kms_key_arn": "superuserSecretKmsKeyArn",
            "vpc_security_group_ids": "vpcSecurityGroupIds",
            "vpc_subnet_ids": "vpcSubnetIds",
        },
    )
    class HostedRotationLambdaProperty:
        def __init__(
            self,
            *,
            exclude_characters: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
            master_secret_arn: typing.Optional[builtins.str] = None,
            master_secret_kms_key_arn: typing.Optional[builtins.str] = None,
            rotation_lambda_name: typing.Optional[builtins.str] = None,
            rotation_type: typing.Optional[builtins.str] = None,
            runtime: typing.Optional[builtins.str] = None,
            superuser_secret_arn: typing.Optional[builtins.str] = None,
            superuser_secret_kms_key_arn: typing.Optional[builtins.str] = None,
            vpc_security_group_ids: typing.Optional[builtins.str] = None,
            vpc_subnet_ids: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Creates a new Lambda rotation function based on one of the `Secrets Manager rotation function templates <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html>`_ .

            You must specify ``Transform: AWS::SecretsManager-2024-09-16`` at the beginning of the CloudFormation template.

            For Amazon RDS master user credentials, see `AWS::RDS::DBCluster MasterUserSecret <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html>`_ .

            For Amazon Redshift admin user credentials, see `AWS::Redshift::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html>`_ .

            :param exclude_characters: A string of the characters that you don't want in the password.
            :param kms_key_arn: The ARN of the KMS key that Secrets Manager uses to encrypt the secret. If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If ``aws/secretsmanager`` doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value.
            :param master_secret_arn: The ARN of the secret that contains superuser credentials, if you use the `Alternating users rotation strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . CloudFormation grants the execution role for the Lambda rotation function ``GetSecretValue`` permission to the secret in this property. For more information, see `Lambda rotation function execution role permissions for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions-function.html>`_ . You must create the superuser secret before you can set this property. You must also include the superuser secret ARN as a key in the JSON of the rotating secret so that the Lambda rotation function can find it. CloudFormation does not hardcode secret ARNs in the Lambda rotation function, so you can use the function to rotate multiple secrets. For more information, see `JSON structure of Secrets Manager secrets <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_secret_json_structure.html>`_ . You can specify ``MasterSecretArn`` or ``SuperuserSecretArn`` but not both. They represent the same superuser secret.
            :param master_secret_kms_key_arn: The ARN of the KMS key that Secrets Manager used to encrypt the superuser secret, if you use the `alternating users strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ and the superuser secret is encrypted with a customer managed key. You don't need to specify this property if the superuser secret is encrypted using the key ``aws/secretsmanager`` . CloudFormation grants the execution role for the Lambda rotation function ``Decrypt`` , ``DescribeKey`` , and ``GenerateDataKey`` permission to the key in this property. For more information, see `Lambda rotation function execution role permissions for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions-function.html>`_ . You can specify ``MasterSecretKmsKeyArn`` or ``SuperuserSecretKmsKeyArn`` but not both. They represent the same superuser secret KMS key .
            :param rotation_lambda_name: The name of the Lambda rotation function.
            :param rotation_type: The rotation template to base the rotation function on, one of the following:. - ``Db2SingleUser`` to use the template `SecretsManagerRDSDb2RotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-db2-singleuser>`_ . - ``Db2MultiUser`` to use the template `SecretsManagerRDSDb2RotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-db2-multiuser>`_ . - ``MySQLSingleUser`` to use the template `SecretsManagerRDSMySQLRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mysql-singleuser>`_ . - ``MySQLMultiUser`` to use the template `SecretsManagerRDSMySQLRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mysql-multiuser>`_ . - ``PostgreSQLSingleUser`` to use the template `SecretsManagerRDSPostgreSQLRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-postgre-singleuser>`_ - ``PostgreSQLMultiUser`` to use the template `SecretsManagerRDSPostgreSQLRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-postgre-multiuser>`_ . - ``OracleSingleUser`` to use the template `SecretsManagerRDSOracleRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-oracle-singleuser>`_ . - ``OracleMultiUser`` to use the template `SecretsManagerRDSOracleRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-oracle-multiuser>`_ . - ``MariaDBSingleUser`` to use the template `SecretsManagerRDSMariaDBRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mariadb-singleuser>`_ . - ``MariaDBMultiUser`` to use the template `SecretsManagerRDSMariaDBRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mariadb-multiuser>`_ . - ``SQLServerSingleUser`` to use the template `SecretsManagerRDSSQLServerRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-sqlserver-singleuser>`_ . - ``SQLServerMultiUser`` to use the template `SecretsManagerRDSSQLServerRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-sqlserver-multiuser>`_ . - ``RedshiftSingleUser`` to use the template `SecretsManagerRedshiftRotationSingleUsr <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-redshift-singleuser>`_ . - ``RedshiftMultiUser`` to use the template `SecretsManagerRedshiftRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-redshift-multiuser>`_ . - ``MongoDBSingleUser`` to use the template `SecretsManagerMongoDBRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mongodb-singleuser>`_ . - ``MongoDBMultiUser`` to use the template `SecretsManagerMongoDBRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mongodb-multiuser>`_ .
            :param runtime: .. epigraph:: Do not set this value if you are using ``Transform: AWS::SecretsManager-2024-09-16`` . Over time, the updated rotation lambda artifacts vended by AWS may not be compatible with the code or shared object files defined in the rotation function deployment package. .. epigraph:: Only define the ``Runtime`` key if: - You are using ``Transform: AWS::SecretsManager-2020-07-23`` . - The code or shared object files defined in the rotation function deployment package are incompatible with Python 3.10. The Python Runtime version for with the rotation function. By default, CloudFormation deploys Python 3.10 binaries for the rotation function. To use a different version of Python, you must do the following two steps: - Deploy the matching version Python binaries with your rotation function. - Set the version number in this field. For example, for Python 3.10, enter *python3.10* . If you only do one of the steps, your rotation function will be incompatible with the binaries. For more information, see `Why did my Lambda rotation function fail with a "pg module not found" error <https://docs.aws.amazon.com/https://repost.aws/knowledge-center/secrets-manager-lambda-rotation>`_ .
            :param superuser_secret_arn: The ARN of the secret that contains superuser credentials, if you use the `Alternating users rotation strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . CloudFormation grants the execution role for the Lambda rotation function ``GetSecretValue`` permission to the secret in this property. For more information, see `Lambda rotation function execution role permissions for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions-function.html>`_ . You must create the superuser secret before you can set this property. You must also include the superuser secret ARN as a key in the JSON of the rotating secret so that the Lambda rotation function can find it. CloudFormation does not hardcode secret ARNs in the Lambda rotation function, so you can use the function to rotate multiple secrets. For more information, see `JSON structure of Secrets Manager secrets <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_secret_json_structure.html>`_ . You can specify ``MasterSecretArn`` or ``SuperuserSecretArn`` but not both. They represent the same superuser secret.
            :param superuser_secret_kms_key_arn: The ARN of the KMS key that Secrets Manager used to encrypt the superuser secret, if you use the `alternating users strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ and the superuser secret is encrypted with a customer managed key. You don't need to specify this property if the superuser secret is encrypted using the key ``aws/secretsmanager`` . CloudFormation grants the execution role for the Lambda rotation function ``Decrypt`` , ``DescribeKey`` , and ``GenerateDataKey`` permission to the key in this property. For more information, see `Lambda rotation function execution role permissions for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions-function.html>`_ . You can specify ``MasterSecretKmsKeyArn`` or ``SuperuserSecretKmsKeyArn`` but not both. They represent the same superuser secret KMS key .
            :param vpc_security_group_ids: A comma-separated list of security group IDs applied to the target database. The template applies the same security groups as on the Lambda rotation function that is created as part of this stack.
            :param vpc_subnet_ids: A comma separated list of VPC subnet IDs of the target database network. The Lambda rotation function is in the same subnet group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
                
                hosted_rotation_lambda_property = secretsmanager_mixins.CfnRotationSchedulePropsMixin.HostedRotationLambdaProperty(
                    exclude_characters="excludeCharacters",
                    kms_key_arn="kmsKeyArn",
                    master_secret_arn="masterSecretArn",
                    master_secret_kms_key_arn="masterSecretKmsKeyArn",
                    rotation_lambda_name="rotationLambdaName",
                    rotation_type="rotationType",
                    runtime="runtime",
                    superuser_secret_arn="superuserSecretArn",
                    superuser_secret_kms_key_arn="superuserSecretKmsKeyArn",
                    vpc_security_group_ids="vpcSecurityGroupIds",
                    vpc_subnet_ids="vpcSubnetIds"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65b8c5869cfb6955fc8ed74decc08e240203fb90462c91d9ca6a25d13b05509e)
                check_type(argname="argument exclude_characters", value=exclude_characters, expected_type=type_hints["exclude_characters"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument master_secret_arn", value=master_secret_arn, expected_type=type_hints["master_secret_arn"])
                check_type(argname="argument master_secret_kms_key_arn", value=master_secret_kms_key_arn, expected_type=type_hints["master_secret_kms_key_arn"])
                check_type(argname="argument rotation_lambda_name", value=rotation_lambda_name, expected_type=type_hints["rotation_lambda_name"])
                check_type(argname="argument rotation_type", value=rotation_type, expected_type=type_hints["rotation_type"])
                check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
                check_type(argname="argument superuser_secret_arn", value=superuser_secret_arn, expected_type=type_hints["superuser_secret_arn"])
                check_type(argname="argument superuser_secret_kms_key_arn", value=superuser_secret_kms_key_arn, expected_type=type_hints["superuser_secret_kms_key_arn"])
                check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
                check_type(argname="argument vpc_subnet_ids", value=vpc_subnet_ids, expected_type=type_hints["vpc_subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_characters is not None:
                self._values["exclude_characters"] = exclude_characters
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if master_secret_arn is not None:
                self._values["master_secret_arn"] = master_secret_arn
            if master_secret_kms_key_arn is not None:
                self._values["master_secret_kms_key_arn"] = master_secret_kms_key_arn
            if rotation_lambda_name is not None:
                self._values["rotation_lambda_name"] = rotation_lambda_name
            if rotation_type is not None:
                self._values["rotation_type"] = rotation_type
            if runtime is not None:
                self._values["runtime"] = runtime
            if superuser_secret_arn is not None:
                self._values["superuser_secret_arn"] = superuser_secret_arn
            if superuser_secret_kms_key_arn is not None:
                self._values["superuser_secret_kms_key_arn"] = superuser_secret_kms_key_arn
            if vpc_security_group_ids is not None:
                self._values["vpc_security_group_ids"] = vpc_security_group_ids
            if vpc_subnet_ids is not None:
                self._values["vpc_subnet_ids"] = vpc_subnet_ids

        @builtins.property
        def exclude_characters(self) -> typing.Optional[builtins.str]:
            '''A string of the characters that you don't want in the password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-excludecharacters
            '''
            result = self._values.get("exclude_characters")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key that Secrets Manager uses to encrypt the secret.

            If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If ``aws/secretsmanager`` doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that contains superuser credentials, if you use the `Alternating users rotation strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . CloudFormation grants the execution role for the Lambda rotation function ``GetSecretValue`` permission to the secret in this property. For more information, see `Lambda rotation function execution role permissions for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions-function.html>`_ .

            You must create the superuser secret before you can set this property.

            You must also include the superuser secret ARN as a key in the JSON of the rotating secret so that the Lambda rotation function can find it. CloudFormation does not hardcode secret ARNs in the Lambda rotation function, so you can use the function to rotate multiple secrets. For more information, see `JSON structure of Secrets Manager secrets <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_secret_json_structure.html>`_ .

            You can specify ``MasterSecretArn`` or ``SuperuserSecretArn`` but not both. They represent the same superuser secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-mastersecretarn
            '''
            result = self._values.get("master_secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_secret_kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key that Secrets Manager used to encrypt the superuser secret, if you use the `alternating users strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ and the superuser secret is encrypted with a customer managed key. You don't need to specify this property if the superuser secret is encrypted using the key ``aws/secretsmanager`` . CloudFormation grants the execution role for the Lambda rotation function ``Decrypt`` , ``DescribeKey`` , and ``GenerateDataKey`` permission to the key in this property. For more information, see `Lambda rotation function execution role permissions for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions-function.html>`_ .

            You can specify ``MasterSecretKmsKeyArn`` or ``SuperuserSecretKmsKeyArn`` but not both. They represent the same superuser secret KMS key .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-mastersecretkmskeyarn
            '''
            result = self._values.get("master_secret_kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rotation_lambda_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Lambda rotation function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-rotationlambdaname
            '''
            result = self._values.get("rotation_lambda_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rotation_type(self) -> typing.Optional[builtins.str]:
            '''The rotation template to base the rotation function on, one of the following:.

            - ``Db2SingleUser`` to use the template `SecretsManagerRDSDb2RotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-db2-singleuser>`_ .
            - ``Db2MultiUser`` to use the template `SecretsManagerRDSDb2RotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-db2-multiuser>`_ .
            - ``MySQLSingleUser`` to use the template `SecretsManagerRDSMySQLRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mysql-singleuser>`_ .
            - ``MySQLMultiUser`` to use the template `SecretsManagerRDSMySQLRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mysql-multiuser>`_ .
            - ``PostgreSQLSingleUser`` to use the template `SecretsManagerRDSPostgreSQLRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-postgre-singleuser>`_
            - ``PostgreSQLMultiUser`` to use the template `SecretsManagerRDSPostgreSQLRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-postgre-multiuser>`_ .
            - ``OracleSingleUser`` to use the template `SecretsManagerRDSOracleRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-oracle-singleuser>`_ .
            - ``OracleMultiUser`` to use the template `SecretsManagerRDSOracleRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-oracle-multiuser>`_ .
            - ``MariaDBSingleUser`` to use the template `SecretsManagerRDSMariaDBRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mariadb-singleuser>`_ .
            - ``MariaDBMultiUser`` to use the template `SecretsManagerRDSMariaDBRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mariadb-multiuser>`_ .
            - ``SQLServerSingleUser`` to use the template `SecretsManagerRDSSQLServerRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-sqlserver-singleuser>`_ .
            - ``SQLServerMultiUser`` to use the template `SecretsManagerRDSSQLServerRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-sqlserver-multiuser>`_ .
            - ``RedshiftSingleUser`` to use the template `SecretsManagerRedshiftRotationSingleUsr <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-redshift-singleuser>`_ .
            - ``RedshiftMultiUser`` to use the template `SecretsManagerRedshiftRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-redshift-multiuser>`_ .
            - ``MongoDBSingleUser`` to use the template `SecretsManagerMongoDBRotationSingleUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mongodb-singleuser>`_ .
            - ``MongoDBMultiUser`` to use the template `SecretsManagerMongoDBRotationMultiUser <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#sar-template-mongodb-multiuser>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-rotationtype
            '''
            result = self._values.get("rotation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime(self) -> typing.Optional[builtins.str]:
            '''.. epigraph::

   Do not set this value if you are using ``Transform: AWS::SecretsManager-2024-09-16`` .

            Over time, the updated rotation lambda artifacts vended by AWS may not be compatible with the code or shared object files defined in the rotation function deployment package.
            .. epigraph::

               Only define the ``Runtime`` key if:

               - You are using ``Transform: AWS::SecretsManager-2020-07-23`` .
               - The code or shared object files defined in the rotation function deployment package are incompatible with Python 3.10.

            The Python Runtime version for with the rotation function. By default, CloudFormation deploys Python 3.10 binaries for the rotation function. To use a different version of Python, you must do the following two steps:

            - Deploy the matching version Python binaries with your rotation function.
            - Set the version number in this field. For example, for Python 3.10, enter *python3.10* .

            If you only do one of the steps, your rotation function will be incompatible with the binaries. For more information, see `Why did my Lambda rotation function fail with a "pg module not found" error <https://docs.aws.amazon.com/https://repost.aws/knowledge-center/secrets-manager-lambda-rotation>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-runtime
            '''
            result = self._values.get("runtime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def superuser_secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that contains superuser credentials, if you use the `Alternating users rotation strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ . CloudFormation grants the execution role for the Lambda rotation function ``GetSecretValue`` permission to the secret in this property. For more information, see `Lambda rotation function execution role permissions for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions-function.html>`_ .

            You must create the superuser secret before you can set this property.

            You must also include the superuser secret ARN as a key in the JSON of the rotating secret so that the Lambda rotation function can find it. CloudFormation does not hardcode secret ARNs in the Lambda rotation function, so you can use the function to rotate multiple secrets. For more information, see `JSON structure of Secrets Manager secrets <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_secret_json_structure.html>`_ .

            You can specify ``MasterSecretArn`` or ``SuperuserSecretArn`` but not both. They represent the same superuser secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-superusersecretarn
            '''
            result = self._values.get("superuser_secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def superuser_secret_kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key that Secrets Manager used to encrypt the superuser secret, if you use the `alternating users strategy <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets_strategies.html#rotating-secrets-two-users>`_ and the superuser secret is encrypted with a customer managed key. You don't need to specify this property if the superuser secret is encrypted using the key ``aws/secretsmanager`` . CloudFormation grants the execution role for the Lambda rotation function ``Decrypt`` , ``DescribeKey`` , and ``GenerateDataKey`` permission to the key in this property. For more information, see `Lambda rotation function execution role permissions for Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions-function.html>`_ .

            You can specify ``MasterSecretKmsKeyArn`` or ``SuperuserSecretKmsKeyArn`` but not both. They represent the same superuser secret KMS key .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-superusersecretkmskeyarn
            '''
            result = self._values.get("superuser_secret_kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_security_group_ids(self) -> typing.Optional[builtins.str]:
            '''A comma-separated list of security group IDs applied to the target database.

            The template applies the same security groups as on the Lambda rotation function that is created as part of this stack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-vpcsecuritygroupids
            '''
            result = self._values.get("vpc_security_group_ids")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_subnet_ids(self) -> typing.Optional[builtins.str]:
            '''A comma separated list of VPC subnet IDs of the target database network.

            The Lambda rotation function is in the same subnet group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-hostedrotationlambda.html#cfn-secretsmanager-rotationschedule-hostedrotationlambda-vpcsubnetids
            '''
            result = self._values.get("vpc_subnet_ids")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostedRotationLambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnRotationSchedulePropsMixin.RotationRulesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automatically_after_days": "automaticallyAfterDays",
            "duration": "duration",
            "schedule_expression": "scheduleExpression",
        },
    )
    class RotationRulesProperty:
        def __init__(
            self,
            *,
            automatically_after_days: typing.Optional[jsii.Number] = None,
            duration: typing.Optional[builtins.str] = None,
            schedule_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The rotation schedule and window.

            We recommend you use ``ScheduleExpression`` to set a cron or rate expression for the schedule and ``Duration`` to set the length of the rotation window.
            .. epigraph::

               When changing an existing rotation schedule and setting ``RotateImmediatelyOnUpdate`` to ``false`` :

               - If using ``AutomaticallyAfterDays`` or a ``ScheduleExpression`` with ``rate()`` , the previously scheduled rotation might still occur.
               - To prevent unintended rotations, use a ``ScheduleExpression`` with ``cron()`` for granular control over rotation windows.

            :param automatically_after_days: The number of days between automatic scheduled rotations of the secret. You can use this value to check that your secret meets your compliance guidelines for how often secrets must be rotated. In ``DescribeSecret`` and ``ListSecrets`` , this value is calculated from the rotation schedule after every successful rotation. In ``RotateSecret`` , you can set the rotation schedule in ``RotationRules`` with ``AutomaticallyAfterDays`` or ``ScheduleExpression`` , but not both.
            :param duration: The length of the rotation window in hours, for example ``3h`` for a three hour window. Secrets Manager rotates your secret at any time during this window. The window must not extend into the next rotation window or the next UTC day. The window starts according to the ``ScheduleExpression`` . If you don't specify a ``Duration`` , for a ``ScheduleExpression`` in hours, the window automatically closes after one hour. For a ``ScheduleExpression`` in days, the window automatically closes at the end of the UTC day. For more information, including examples, see `Schedule expressions in Secrets Manager rotation <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_schedule.html>`_ in the *Secrets Manager Users Guide* .
            :param schedule_expression: A ``cron()`` or ``rate()`` expression that defines the schedule for rotating your secret. Secrets Manager rotation schedules use UTC time zone. Secrets Manager rotates your secret any time during a rotation window. Secrets Manager ``rate()`` expressions represent the interval in hours or days that you want to rotate your secret, for example ``rate(12 hours)`` or ``rate(10 days)`` . You can rotate a secret as often as every four hours. If you use a ``rate()`` expression, the rotation window starts at midnight. For a rate in hours, the default rotation window closes after one hour. For a rate in days, the default rotation window closes at the end of the day. You can set the ``Duration`` to change the rotation window. The rotation window must not extend into the next UTC day or into the next rotation window. You can use a ``cron()`` expression to create a rotation schedule that is more detailed than a rotation interval. For more information, including examples, see `Schedule expressions in Secrets Manager rotation <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_schedule.html>`_ in the *Secrets Manager Users Guide* . For a cron expression that represents a schedule in hours, the default rotation window closes after one hour. For a cron expression that represents a schedule in days, the default rotation window closes at the end of the day. You can set the ``Duration`` to change the rotation window. The rotation window must not extend into the next UTC day or into the next rotation window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
                
                rotation_rules_property = secretsmanager_mixins.CfnRotationSchedulePropsMixin.RotationRulesProperty(
                    automatically_after_days=123,
                    duration="duration",
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__282765dfedf88ca1ac2693c1846247d742a4a1096e350f76ae0157ff23f886c9)
                check_type(argname="argument automatically_after_days", value=automatically_after_days, expected_type=type_hints["automatically_after_days"])
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatically_after_days is not None:
                self._values["automatically_after_days"] = automatically_after_days
            if duration is not None:
                self._values["duration"] = duration
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression

        @builtins.property
        def automatically_after_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days between automatic scheduled rotations of the secret.

            You can use this value to check that your secret meets your compliance guidelines for how often secrets must be rotated.

            In ``DescribeSecret`` and ``ListSecrets`` , this value is calculated from the rotation schedule after every successful rotation. In ``RotateSecret`` , you can set the rotation schedule in ``RotationRules`` with ``AutomaticallyAfterDays`` or ``ScheduleExpression`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-automaticallyafterdays
            '''
            result = self._values.get("automatically_after_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def duration(self) -> typing.Optional[builtins.str]:
            '''The length of the rotation window in hours, for example ``3h`` for a three hour window.

            Secrets Manager rotates your secret at any time during this window. The window must not extend into the next rotation window or the next UTC day. The window starts according to the ``ScheduleExpression`` . If you don't specify a ``Duration`` , for a ``ScheduleExpression`` in hours, the window automatically closes after one hour. For a ``ScheduleExpression`` in days, the window automatically closes at the end of the UTC day. For more information, including examples, see `Schedule expressions in Secrets Manager rotation <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_schedule.html>`_ in the *Secrets Manager Users Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-duration
            '''
            result = self._values.get("duration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''A ``cron()`` or ``rate()`` expression that defines the schedule for rotating your secret.

            Secrets Manager rotation schedules use UTC time zone. Secrets Manager rotates your secret any time during a rotation window.

            Secrets Manager ``rate()`` expressions represent the interval in hours or days that you want to rotate your secret, for example ``rate(12 hours)`` or ``rate(10 days)`` . You can rotate a secret as often as every four hours. If you use a ``rate()`` expression, the rotation window starts at midnight. For a rate in hours, the default rotation window closes after one hour. For a rate in days, the default rotation window closes at the end of the day. You can set the ``Duration`` to change the rotation window. The rotation window must not extend into the next UTC day or into the next rotation window.

            You can use a ``cron()`` expression to create a rotation schedule that is more detailed than a rotation interval. For more information, including examples, see `Schedule expressions in Secrets Manager rotation <https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_schedule.html>`_ in the *Secrets Manager Users Guide* . For a cron expression that represents a schedule in hours, the default rotation window closes after one hour. For a cron expression that represents a schedule in days, the default rotation window closes at the end of the day. You can set the ``Duration`` to change the rotation window. The rotation window must not extend into the next UTC day or into the next rotation window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-rotationschedule-rotationrules.html#cfn-secretsmanager-rotationschedule-rotationrules-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RotationRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnSecretMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "generate_secret_string": "generateSecretString",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "replica_regions": "replicaRegions",
        "secret_string": "secretString",
        "tags": "tags",
        "type": "type",
    },
)
class CfnSecretMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        generate_secret_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecretPropsMixin.GenerateSecretStringProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        replica_regions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecretPropsMixin.ReplicaRegionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        secret_string: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSecretPropsMixin.

        :param description: The description of the secret.
        :param generate_secret_string: A structure that specifies how to generate a password to encrypt and store in the secret. To include a specific string in the secret, use ``SecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret. When you make a change to this property, a new secret version is created. We recommend that you specify the maximum length and include every character type that the system you are generating a password for can support.
        :param kms_key_id: The ARN, key ID, or alias of the AWS key that Secrets Manager uses to encrypt the secret value in the secret. An alias is always prefixed by ``alias/`` , for example ``alias/aws/secretsmanager`` . For more information, see `About aliases <https://docs.aws.amazon.com/kms/latest/developerguide/alias-about.html>`_ . To use a AWS key in a different account, use the key ARN or the alias ARN. If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If that key doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value. If the secret is in a different AWS account from the credentials calling the API, then you can't use ``aws/secretsmanager`` to encrypt the secret, and you must create and use a customer managed AWS key.
        :param name: The name of the new secret. The secret name can contain ASCII letters, numbers, and the following characters: /_+=.@- Do not end your secret name with a hyphen followed by six characters. If you do so, you risk confusion and unexpected results when searching for a secret by partial ARN. Secrets Manager automatically adds a hyphen and six random characters after the secret name at the end of the ARN.
        :param replica_regions: A custom type that specifies a ``Region`` and the ``KmsKeyId`` for a replica secret.
        :param secret_string: The text to encrypt and store in the secret. We recommend you use a JSON structure of key/value pairs for your secret value. To generate a random password, use ``GenerateSecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret. When you make a change to this property, a new secret version is created.
        :param tags: A list of tags to attach to the secret. Each tag is a key and value pair of strings in a JSON text string, for example: ``[{"Key":"CostCenter","Value":"12345"},{"Key":"environment","Value":"production"}]`` Secrets Manager tag key names are case sensitive. A tag with the key "ABC" is a different tag from one with key "abc". Stack-level tags, tags you apply to the CloudFormation stack, are also attached to the secret. If you check tags in permissions policies as part of your security strategy, then adding or removing a tag can change permissions. If the completion of this operation would result in you losing your permissions for this secret, then Secrets Manager blocks the operation and returns an ``Access Denied`` error. For more information, see `Control access to secrets using tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#tag-secrets-abac>`_ and `Limit access to identities with tags that match secrets' tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#auth-and-access_tags2>`_ . For information about how to format a JSON parameter for the various command line tool environments, see `Using JSON for Parameters <https://docs.aws.amazon.com/cli/latest/userguide/cli-using-param.html#cli-using-param-json>`_ . If your command-line tool or SDK requires quotation marks around the parameter, you should use single quotes to avoid confusion with the double quotes required in the JSON text. The following restrictions apply to tags: - Maximum number of tags per secret: 50 - Maximum key length: 127 Unicode characters in UTF-8 - Maximum value length: 255 Unicode characters in UTF-8 - Tag keys and values are case sensitive. - Do not use the ``aws:`` prefix in your tag names or values because AWS reserves it for AWS use. You can't edit or delete tag names or values with this prefix. Tags with this prefix do not count against your tags per secret limit. - If you use your tagging schema across multiple services and resources, other services might have restrictions on allowed characters. Generally allowed characters: letters, spaces, and numbers representable in UTF-8, plus the following special characters: + - = . _ : /
        :param type: The exact string that identifies the third-party partner that holds the external secret. For more information, see `Managed external secret partners <https://docs.aws.amazon.com/secretsmanager/latest/userguide/mes-partners.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
            
            cfn_secret_mixin_props = secretsmanager_mixins.CfnSecretMixinProps(
                description="description",
                generate_secret_string=secretsmanager_mixins.CfnSecretPropsMixin.GenerateSecretStringProperty(
                    exclude_characters="excludeCharacters",
                    exclude_lowercase=False,
                    exclude_numbers=False,
                    exclude_punctuation=False,
                    exclude_uppercase=False,
                    generate_string_key="generateStringKey",
                    include_space=False,
                    password_length=123,
                    require_each_included_type=False,
                    secret_string_template="secretStringTemplate"
                ),
                kms_key_id="kmsKeyId",
                name="name",
                replica_regions=[secretsmanager_mixins.CfnSecretPropsMixin.ReplicaRegionProperty(
                    kms_key_id="kmsKeyId",
                    region="region"
                )],
                secret_string="secretString",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573810b816d185c64a484569de1d2e9249a5c1527e2dd3e789424f1c5bec8141)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument generate_secret_string", value=generate_secret_string, expected_type=type_hints["generate_secret_string"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replica_regions", value=replica_regions, expected_type=type_hints["replica_regions"])
            check_type(argname="argument secret_string", value=secret_string, expected_type=type_hints["secret_string"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if generate_secret_string is not None:
            self._values["generate_secret_string"] = generate_secret_string
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if replica_regions is not None:
            self._values["replica_regions"] = replica_regions
        if secret_string is not None:
            self._values["secret_string"] = secret_string
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def generate_secret_string(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecretPropsMixin.GenerateSecretStringProperty"]]:
        '''A structure that specifies how to generate a password to encrypt and store in the secret.

        To include a specific string in the secret, use ``SecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret. When you make a change to this property, a new secret version is created.

        We recommend that you specify the maximum length and include every character type that the system you are generating a password for can support.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-generatesecretstring
        '''
        result = self._values.get("generate_secret_string")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecretPropsMixin.GenerateSecretStringProperty"]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ARN, key ID, or alias of the AWS  key that Secrets Manager uses to encrypt the secret value in the secret.

        An alias is always prefixed by ``alias/`` , for example ``alias/aws/secretsmanager`` . For more information, see `About aliases <https://docs.aws.amazon.com/kms/latest/developerguide/alias-about.html>`_ .

        To use a AWS  key in a different account, use the key ARN or the alias ARN.

        If you don't specify this value, then Secrets Manager uses the key ``aws/secretsmanager`` . If that key doesn't yet exist, then Secrets Manager creates it for you automatically the first time it encrypts the secret value.

        If the secret is in a different AWS account from the credentials calling the API, then you can't use ``aws/secretsmanager`` to encrypt the secret, and you must create and use a customer managed AWS  key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the new secret.

        The secret name can contain ASCII letters, numbers, and the following characters: /_+=.@-

        Do not end your secret name with a hyphen followed by six characters. If you do so, you risk confusion and unexpected results when searching for a secret by partial ARN. Secrets Manager automatically adds a hyphen and six random characters after the secret name at the end of the ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replica_regions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecretPropsMixin.ReplicaRegionProperty"]]]]:
        '''A custom type that specifies a ``Region`` and the ``KmsKeyId`` for a replica secret.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-replicaregions
        '''
        result = self._values.get("replica_regions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecretPropsMixin.ReplicaRegionProperty"]]]], result)

    @builtins.property
    def secret_string(self) -> typing.Optional[builtins.str]:
        '''The text to encrypt and store in the secret.

        We recommend you use a JSON structure of key/value pairs for your secret value. To generate a random password, use ``GenerateSecretString`` instead. If you omit both ``GenerateSecretString`` and ``SecretString`` , you create an empty secret. When you make a change to this property, a new secret version is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-secretstring
        '''
        result = self._values.get("secret_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags to attach to the secret.

        Each tag is a key and value pair of strings in a JSON text string, for example:

        ``[{"Key":"CostCenter","Value":"12345"},{"Key":"environment","Value":"production"}]``

        Secrets Manager tag key names are case sensitive. A tag with the key "ABC" is a different tag from one with key "abc".

        Stack-level tags, tags you apply to the CloudFormation stack, are also attached to the secret.

        If you check tags in permissions policies as part of your security strategy, then adding or removing a tag can change permissions. If the completion of this operation would result in you losing your permissions for this secret, then Secrets Manager blocks the operation and returns an ``Access Denied`` error. For more information, see `Control access to secrets using tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#tag-secrets-abac>`_ and `Limit access to identities with tags that match secrets' tags <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples.html#auth-and-access_tags2>`_ .

        For information about how to format a JSON parameter for the various command line tool environments, see `Using JSON for Parameters <https://docs.aws.amazon.com/cli/latest/userguide/cli-using-param.html#cli-using-param-json>`_ . If your command-line tool or SDK requires quotation marks around the parameter, you should use single quotes to avoid confusion with the double quotes required in the JSON text.

        The following restrictions apply to tags:

        - Maximum number of tags per secret: 50
        - Maximum key length: 127 Unicode characters in UTF-8
        - Maximum value length: 255 Unicode characters in UTF-8
        - Tag keys and values are case sensitive.
        - Do not use the ``aws:`` prefix in your tag names or values because AWS reserves it for AWS use. You can't edit or delete tag names or values with this prefix. Tags with this prefix do not count against your tags per secret limit.
        - If you use your tagging schema across multiple services and resources, other services might have restrictions on allowed characters. Generally allowed characters: letters, spaces, and numbers representable in UTF-8, plus the following special characters: + - = . _ : /

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-tags
        :: .
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The exact string that identifies the third-party partner that holds the external secret.

        For more information, see `Managed external secret partners <https://docs.aws.amazon.com/secretsmanager/latest/userguide/mes-partners.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html#cfn-secretsmanager-secret-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecretMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecretPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnSecretPropsMixin",
):
    '''Creates a new secret.

    A *secret* can be a password, a set of credentials such as a user name and password, an OAuth token, or other secret information that you store in an encrypted form in Secrets Manager.

    For Amazon RDS master user credentials, see `AWS::RDS::DBCluster MasterUserSecret <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html>`_ .

    For Amazon Redshift admin user credentials, see `AWS::Redshift::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html>`_ .

    To retrieve a secret in a CloudFormation template, use a *dynamic reference* . For more information, see `Retrieve a secret in an CloudFormation resource <https://docs.aws.amazon.com/secretsmanager/latest/userguide/cfn-example_reference-secret.html>`_ .

    For information about creating a secret in the console, see `Create a secret <https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_create-basic-secret.html>`_ . For information about creating a secret using the CLI or SDK, see `CreateSecret <https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_CreateSecret.html>`_ .

    For information about retrieving a secret in code, see `Retrieve secrets from Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html
    :cloudformationResource: AWS::SecretsManager::Secret
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
        
        cfn_secret_props_mixin = secretsmanager_mixins.CfnSecretPropsMixin(secretsmanager_mixins.CfnSecretMixinProps(
            description="description",
            generate_secret_string=secretsmanager_mixins.CfnSecretPropsMixin.GenerateSecretStringProperty(
                exclude_characters="excludeCharacters",
                exclude_lowercase=False,
                exclude_numbers=False,
                exclude_punctuation=False,
                exclude_uppercase=False,
                generate_string_key="generateStringKey",
                include_space=False,
                password_length=123,
                require_each_included_type=False,
                secret_string_template="secretStringTemplate"
            ),
            kms_key_id="kmsKeyId",
            name="name",
            replica_regions=[secretsmanager_mixins.CfnSecretPropsMixin.ReplicaRegionProperty(
                kms_key_id="kmsKeyId",
                region="region"
            )],
            secret_string="secretString",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSecretMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecretsManager::Secret``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa4357495cdceb7b9a5f99a172f88cea12f38c3046522e232e586f24b6f116c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88e6be09d2ab03de3e8772bcf1bf812a2b5fc4b482ffbdef8b7ab9a139b0ac83)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebced1f8c224111b8cc6f18fd4c8e4f34993453e308ac3d10359f07d1c59878)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecretMixinProps:
        return typing.cast(CfnSecretMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnSecretPropsMixin.GenerateSecretStringProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_characters": "excludeCharacters",
            "exclude_lowercase": "excludeLowercase",
            "exclude_numbers": "excludeNumbers",
            "exclude_punctuation": "excludePunctuation",
            "exclude_uppercase": "excludeUppercase",
            "generate_string_key": "generateStringKey",
            "include_space": "includeSpace",
            "password_length": "passwordLength",
            "require_each_included_type": "requireEachIncludedType",
            "secret_string_template": "secretStringTemplate",
        },
    )
    class GenerateSecretStringProperty:
        def __init__(
            self,
            *,
            exclude_characters: typing.Optional[builtins.str] = None,
            exclude_lowercase: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclude_numbers: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclude_punctuation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclude_uppercase: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            generate_string_key: typing.Optional[builtins.str] = None,
            include_space: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            password_length: typing.Optional[jsii.Number] = None,
            require_each_included_type: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            secret_string_template: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Generates a random password.

            We recommend that you specify the maximum length and include every character type that the system you are generating a password for can support.

            *Required permissions:* ``secretsmanager:GetRandomPassword`` . For more information, see `IAM policy actions for Secrets Manager <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssecretsmanager.html#awssecretsmanager-actions-as-permissions>`_ and `Authentication and access control in Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access.html>`_ .

            :param exclude_characters: A string of the characters that you don't want in the password.
            :param exclude_lowercase: Specifies whether to exclude lowercase letters from the password. If you don't include this switch, the password can contain lowercase letters.
            :param exclude_numbers: Specifies whether to exclude numbers from the password. If you don't include this switch, the password can contain numbers.
            :param exclude_punctuation: Specifies whether to exclude the following punctuation characters from the password: `! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ `` { | } ~`` . If you don't include this switch, the password can contain punctuation.
            :param exclude_uppercase: Specifies whether to exclude uppercase letters from the password. If you don't include this switch, the password can contain uppercase letters.
            :param generate_string_key: The JSON key name for the key/value pair, where the value is the generated password. This pair is added to the JSON structure specified by the ``SecretStringTemplate`` parameter. If you specify this parameter, then you must also specify ``SecretStringTemplate`` .
            :param include_space: Specifies whether to include the space character. If you include this switch, the password can contain space characters.
            :param password_length: The length of the password. If you don't include this parameter, the default length is 32 characters.
            :param require_each_included_type: Specifies whether to include at least one upper and lowercase letter, one number, and one punctuation. If you don't include this switch, the password contains at least one of every character type.
            :param secret_string_template: A template that the generated string must match. When you make a change to this property, a new secret version is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
                
                generate_secret_string_property = secretsmanager_mixins.CfnSecretPropsMixin.GenerateSecretStringProperty(
                    exclude_characters="excludeCharacters",
                    exclude_lowercase=False,
                    exclude_numbers=False,
                    exclude_punctuation=False,
                    exclude_uppercase=False,
                    generate_string_key="generateStringKey",
                    include_space=False,
                    password_length=123,
                    require_each_included_type=False,
                    secret_string_template="secretStringTemplate"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8288c83d73617054f93450bd7eb28d1e55b3bf931c155d2f1a64c9d16dcd5c6)
                check_type(argname="argument exclude_characters", value=exclude_characters, expected_type=type_hints["exclude_characters"])
                check_type(argname="argument exclude_lowercase", value=exclude_lowercase, expected_type=type_hints["exclude_lowercase"])
                check_type(argname="argument exclude_numbers", value=exclude_numbers, expected_type=type_hints["exclude_numbers"])
                check_type(argname="argument exclude_punctuation", value=exclude_punctuation, expected_type=type_hints["exclude_punctuation"])
                check_type(argname="argument exclude_uppercase", value=exclude_uppercase, expected_type=type_hints["exclude_uppercase"])
                check_type(argname="argument generate_string_key", value=generate_string_key, expected_type=type_hints["generate_string_key"])
                check_type(argname="argument include_space", value=include_space, expected_type=type_hints["include_space"])
                check_type(argname="argument password_length", value=password_length, expected_type=type_hints["password_length"])
                check_type(argname="argument require_each_included_type", value=require_each_included_type, expected_type=type_hints["require_each_included_type"])
                check_type(argname="argument secret_string_template", value=secret_string_template, expected_type=type_hints["secret_string_template"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_characters is not None:
                self._values["exclude_characters"] = exclude_characters
            if exclude_lowercase is not None:
                self._values["exclude_lowercase"] = exclude_lowercase
            if exclude_numbers is not None:
                self._values["exclude_numbers"] = exclude_numbers
            if exclude_punctuation is not None:
                self._values["exclude_punctuation"] = exclude_punctuation
            if exclude_uppercase is not None:
                self._values["exclude_uppercase"] = exclude_uppercase
            if generate_string_key is not None:
                self._values["generate_string_key"] = generate_string_key
            if include_space is not None:
                self._values["include_space"] = include_space
            if password_length is not None:
                self._values["password_length"] = password_length
            if require_each_included_type is not None:
                self._values["require_each_included_type"] = require_each_included_type
            if secret_string_template is not None:
                self._values["secret_string_template"] = secret_string_template

        @builtins.property
        def exclude_characters(self) -> typing.Optional[builtins.str]:
            '''A string of the characters that you don't want in the password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludecharacters
            '''
            result = self._values.get("exclude_characters")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_lowercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to exclude lowercase letters from the password.

            If you don't include this switch, the password can contain lowercase letters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludelowercase
            '''
            result = self._values.get("exclude_lowercase")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclude_numbers(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to exclude numbers from the password.

            If you don't include this switch, the password can contain numbers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludenumbers
            '''
            result = self._values.get("exclude_numbers")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclude_punctuation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to exclude the following punctuation characters from the password: `!

            " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \\ ] ^ _ `` { | } ~`` . If you don't include this switch, the password can contain punctuation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludepunctuation
            '''
            result = self._values.get("exclude_punctuation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclude_uppercase(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to exclude uppercase letters from the password.

            If you don't include this switch, the password can contain uppercase letters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-excludeuppercase
            '''
            result = self._values.get("exclude_uppercase")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def generate_string_key(self) -> typing.Optional[builtins.str]:
            '''The JSON key name for the key/value pair, where the value is the generated password.

            This pair is added to the JSON structure specified by the ``SecretStringTemplate`` parameter. If you specify this parameter, then you must also specify ``SecretStringTemplate`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-generatestringkey
            '''
            result = self._values.get("generate_string_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_space(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to include the space character.

            If you include this switch, the password can contain space characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-includespace
            '''
            result = self._values.get("include_space")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def password_length(self) -> typing.Optional[jsii.Number]:
            '''The length of the password.

            If you don't include this parameter, the default length is 32 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-passwordlength
            '''
            result = self._values.get("password_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def require_each_included_type(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to include at least one upper and lowercase letter, one number, and one punctuation.

            If you don't include this switch, the password contains at least one of every character type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-requireeachincludedtype
            '''
            result = self._values.get("require_each_included_type")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def secret_string_template(self) -> typing.Optional[builtins.str]:
            '''A template that the generated string must match.

            When you make a change to this property, a new secret version is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-generatesecretstring.html#cfn-secretsmanager-secret-generatesecretstring-secretstringtemplate
            '''
            result = self._values.get("secret_string_template")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GenerateSecretStringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnSecretPropsMixin.ReplicaRegionProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId", "region": "region"},
    )
    class ReplicaRegionProperty:
        def __init__(
            self,
            *,
            kms_key_id: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a ``Region`` and the ``KmsKeyId`` for a replica secret.

            :param kms_key_id: The ARN, key ID, or alias of the KMS key to encrypt the secret. If you don't include this field, Secrets Manager uses ``aws/secretsmanager`` .
            :param region: A string that represents a ``Region`` , for example "us-east-1".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-replicaregion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
                
                replica_region_property = secretsmanager_mixins.CfnSecretPropsMixin.ReplicaRegionProperty(
                    kms_key_id="kmsKeyId",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f351446b5f9b15e0bbdc7114ad1b689eebeccfacd726f417196e474c5031946)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ARN, key ID, or alias of the KMS key to encrypt the secret.

            If you don't include this field, Secrets Manager uses ``aws/secretsmanager`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-replicaregion.html#cfn-secretsmanager-secret-replicaregion-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''A string that represents a ``Region`` , for example "us-east-1".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-secretsmanager-secret-replicaregion.html#cfn-secretsmanager-secret-replicaregion-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaRegionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnSecretTargetAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "target_id": "targetId",
        "target_type": "targetType",
    },
)
class CfnSecretTargetAttachmentMixinProps:
    def __init__(
        self,
        *,
        secret_id: typing.Optional[builtins.str] = None,
        target_id: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSecretTargetAttachmentPropsMixin.

        :param secret_id: The ARN or name of the secret. To reference a secret also created in this template, use the see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID. This field is unique for each target attachment definition.
        :param target_id: The ID of the database or cluster.
        :param target_type: A string that defines the type of service or database associated with the secret. This value instructs Secrets Manager how to update the secret with the details of the service or database. This value must be one of the following: - AWS::RDS::DBInstance - AWS::RDS::DBCluster - AWS::Redshift::Cluster - AWS::RedshiftServerless::Namespace - AWS::DocDB::DBInstance - AWS::DocDB::DBCluster - AWS::DocDBElastic::Cluster

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
            
            cfn_secret_target_attachment_mixin_props = secretsmanager_mixins.CfnSecretTargetAttachmentMixinProps(
                secret_id="secretId",
                target_id="targetId",
                target_type="targetType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9320232e44b10cb269996cb8323b037b8cdafcbca6055059ef1b2e573871088e)
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret_id is not None:
            self._values["secret_id"] = secret_id
        if target_id is not None:
            self._values["target_id"] = target_id
        if target_type is not None:
            self._values["target_type"] = target_type

    @builtins.property
    def secret_id(self) -> typing.Optional[builtins.str]:
        '''The ARN or name of the secret.

        To reference a secret also created in this template, use the see `Ref <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html>`_ function with the secret's logical ID. This field is unique for each target attachment definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-secretid
        '''
        result = self._values.get("secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the database or cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targetid
        '''
        result = self._values.get("target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_type(self) -> typing.Optional[builtins.str]:
        '''A string that defines the type of service or database associated with the secret.

        This value instructs Secrets Manager how to update the secret with the details of the service or database. This value must be one of the following:

        - AWS::RDS::DBInstance
        - AWS::RDS::DBCluster
        - AWS::Redshift::Cluster
        - AWS::RedshiftServerless::Namespace
        - AWS::DocDB::DBInstance
        - AWS::DocDB::DBCluster
        - AWS::DocDBElastic::Cluster

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html#cfn-secretsmanager-secrettargetattachment-targettype
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecretTargetAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecretTargetAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_secretsmanager.mixins.CfnSecretTargetAttachmentPropsMixin",
):
    '''The ``AWS::SecretsManager::SecretTargetAttachment`` resource completes the final link between a Secrets Manager secret and the associated database by adding the database connection information to the secret JSON.

    If you want to turn on automatic rotation for a database credential secret, the secret must contain the database connection information. For more information, see `JSON structure of Secrets Manager database credential secrets <https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_secret_json_structure.html>`_ .

    A single secret resource can only have one target attached to it.

    When you remove a ``SecretTargetAttachment`` from a stack, Secrets Manager removes the database connection information from the secret with a ``PutSecretValue`` call.

    For Amazon RDS master user credentials, see `AWS::RDS::DBCluster MasterUserSecret <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-masterusersecret.html>`_ .

    For Amazon Redshift admin user credentials, see `AWS::Redshift::Cluster <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
    :cloudformationResource: AWS::SecretsManager::SecretTargetAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_secretsmanager import mixins as secretsmanager_mixins
        
        cfn_secret_target_attachment_props_mixin = secretsmanager_mixins.CfnSecretTargetAttachmentPropsMixin(secretsmanager_mixins.CfnSecretTargetAttachmentMixinProps(
            secret_id="secretId",
            target_id="targetId",
            target_type="targetType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSecretTargetAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SecretsManager::SecretTargetAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7451c405806205e49a9d4c9491120387400acad2b41d6cdfeb8402be996d765)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb3b88b17c5e34991f506e5ac62a589f91db24fa8f246b05d66c26873414dc73)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9c1f59e4ad220ee492d83b52dfab5468bf85be3f6fdc0de6da0c077734676d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecretTargetAttachmentMixinProps:
        return typing.cast(CfnSecretTargetAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
    "CfnRotationScheduleMixinProps",
    "CfnRotationSchedulePropsMixin",
    "CfnSecretMixinProps",
    "CfnSecretPropsMixin",
    "CfnSecretTargetAttachmentMixinProps",
    "CfnSecretTargetAttachmentPropsMixin",
]

publication.publish()

def _typecheckingstub__018dd948e2299c43af2943c3ae8ae346b7d70c84aab707c7dea96a6c18b41f1c(
    *,
    block_public_policy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_policy: typing.Any = None,
    secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a8c36f7c6e67d027b26742d240c9ecf3947283dd538aba4b321d71d581d651(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871d472dcacd8c19d9fe154b24d10bb75323a43acf26f9ba7d484ee5dc7346ff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504bfb77c7cfb6a43dc53f5d362c7b5718d306ea3f8d0141ccbeb94f43f825b6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dcba8a53bd95719a1b276b48aea21c780d15255d2268cff375d8b0d6d565695(
    *,
    external_secret_rotation_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRotationSchedulePropsMixin.ExternalSecretRotationMetadataItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    external_secret_rotation_role_arn: typing.Optional[builtins.str] = None,
    hosted_rotation_lambda: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRotationSchedulePropsMixin.HostedRotationLambdaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rotate_immediately_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    rotation_lambda_arn: typing.Optional[builtins.str] = None,
    rotation_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRotationSchedulePropsMixin.RotationRulesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3862fd394e20642f87c5b4c70fbb7d3738395920fa3f1f6977c090a22c12cc04(
    props: typing.Union[CfnRotationScheduleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96679c13692ef1ecde803204860b3015eb7a96d6f64a0354f3ee3c676664f98(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48e5c0c7c77733230cc5120c624fddeccf537ec660b930c5d04d95460d3f0f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99ce69fcfd0a8d8fae6a9228490dec205c7afa960a214e4648b2ee55ed685e8(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b8c5869cfb6955fc8ed74decc08e240203fb90462c91d9ca6a25d13b05509e(
    *,
    exclude_characters: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    master_secret_arn: typing.Optional[builtins.str] = None,
    master_secret_kms_key_arn: typing.Optional[builtins.str] = None,
    rotation_lambda_name: typing.Optional[builtins.str] = None,
    rotation_type: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    superuser_secret_arn: typing.Optional[builtins.str] = None,
    superuser_secret_kms_key_arn: typing.Optional[builtins.str] = None,
    vpc_security_group_ids: typing.Optional[builtins.str] = None,
    vpc_subnet_ids: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282765dfedf88ca1ac2693c1846247d742a4a1096e350f76ae0157ff23f886c9(
    *,
    automatically_after_days: typing.Optional[jsii.Number] = None,
    duration: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573810b816d185c64a484569de1d2e9249a5c1527e2dd3e789424f1c5bec8141(
    *,
    description: typing.Optional[builtins.str] = None,
    generate_secret_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecretPropsMixin.GenerateSecretStringProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    replica_regions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecretPropsMixin.ReplicaRegionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    secret_string: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa4357495cdceb7b9a5f99a172f88cea12f38c3046522e232e586f24b6f116c(
    props: typing.Union[CfnSecretMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e6be09d2ab03de3e8772bcf1bf812a2b5fc4b482ffbdef8b7ab9a139b0ac83(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebced1f8c224111b8cc6f18fd4c8e4f34993453e308ac3d10359f07d1c59878(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8288c83d73617054f93450bd7eb28d1e55b3bf931c155d2f1a64c9d16dcd5c6(
    *,
    exclude_characters: typing.Optional[builtins.str] = None,
    exclude_lowercase: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclude_numbers: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclude_punctuation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclude_uppercase: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    generate_string_key: typing.Optional[builtins.str] = None,
    include_space: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    password_length: typing.Optional[jsii.Number] = None,
    require_each_included_type: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    secret_string_template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f351446b5f9b15e0bbdc7114ad1b689eebeccfacd726f417196e474c5031946(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9320232e44b10cb269996cb8323b037b8cdafcbca6055059ef1b2e573871088e(
    *,
    secret_id: typing.Optional[builtins.str] = None,
    target_id: typing.Optional[builtins.str] = None,
    target_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7451c405806205e49a9d4c9491120387400acad2b41d6cdfeb8402be996d765(
    props: typing.Union[CfnSecretTargetAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3b88b17c5e34991f506e5ac62a589f91db24fa8f246b05d66c26873414dc73(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9c1f59e4ad220ee492d83b52dfab5468bf85be3f6fdc0de6da0c077734676d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
