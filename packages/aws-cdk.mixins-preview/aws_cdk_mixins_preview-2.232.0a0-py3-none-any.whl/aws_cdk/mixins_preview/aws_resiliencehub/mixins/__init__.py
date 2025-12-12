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
    jsii_type="@aws-cdk/mixins-preview.aws_resiliencehub.mixins.CfnAppMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_assessment_schedule": "appAssessmentSchedule",
        "app_template_body": "appTemplateBody",
        "description": "description",
        "event_subscriptions": "eventSubscriptions",
        "name": "name",
        "permission_model": "permissionModel",
        "resiliency_policy_arn": "resiliencyPolicyArn",
        "resource_mappings": "resourceMappings",
        "tags": "tags",
    },
)
class CfnAppMixinProps:
    def __init__(
        self,
        *,
        app_assessment_schedule: typing.Optional[builtins.str] = None,
        app_template_body: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_subscriptions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.EventSubscriptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        permission_model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.PermissionModelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resiliency_policy_arn: typing.Optional[builtins.str] = None,
        resource_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.ResourceMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnAppPropsMixin.

        :param app_assessment_schedule: Assessment execution schedule with 'Daily' or 'Disabled' values.
        :param app_template_body: A JSON string that provides information about your application structure. To learn more about the ``appTemplateBody`` template, see the sample template in `Sample appTemplateBody template <https://docs.aws.amazon.com//resilience-hub/latest/APIReference/API_PutDraftAppVersionTemplate.html#API_PutDraftAppVersionTemplate_Examples>`_ . The ``appTemplateBody`` JSON string has the following structure: - *``resources``* The list of logical resources that needs to be included in the AWS Resilience Hub application. Type: Array .. epigraph:: Don't add the resources that you want to exclude. Each ``resources`` array item includes the following fields: - *``logicalResourceId``* The logical identifier of the resource. Type: Object Each ``logicalResourceId`` object includes the following fields: - ``identifier`` Identifier of the resource. Type: String - ``logicalStackName`` Name of the AWS CloudFormation stack this resource belongs to. Type: String - ``resourceGroupName`` Name of the resource group this resource belongs to. Type: String - ``terraformSourceName`` Name of the Terraform S3 state file this resource belongs to. Type: String - ``eksSourceName`` Name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to. .. epigraph:: This parameter accepts values in "eks-cluster/namespace" format. Type: String - *``type``* The type of resource. Type: string - *``name``* Name of the resource. Type: String - ``additionalInfo`` Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ . .. epigraph:: Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account. Key: ``"failover-regions"`` Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"`` - *``appComponents``* The list of Application Components (AppComponent) that this resource belongs to. If an AppComponent is not part of the AWS Resilience Hub application, it will be added. Type: Array Each ``appComponents`` array item includes the following fields: - ``name`` Name of the AppComponent. Type: String - ``type`` The type of AppComponent. For more information about the types of AppComponent, see `Grouping resources in an AppComponent <https://docs.aws.amazon.com/resilience-hub/latest/userguide/AppComponent.grouping.html>`_ . Type: String - ``resourceNames`` The list of included resources that are assigned to the AppComponent. Type: Array of strings - ``additionalInfo`` Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ . .. epigraph:: Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account. Key: ``"failover-regions"`` Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"`` - *``excludedResources``* The list of logical resource identifiers to be excluded from the application. Type: Array .. epigraph:: Don't add the resources that you want to include. Each ``excludedResources`` array item includes the following fields: - *``logicalResourceIds``* The logical identifier of the resource. Type: Object .. epigraph:: You can configure only one of the following fields: - ``logicalStackName`` - ``resourceGroupName`` - ``terraformSourceName`` - ``eksSourceName`` Each ``logicalResourceIds`` object includes the following fields: - ``identifier`` The identifier of the resource. Type: String - ``logicalStackName`` Name of the AWS CloudFormation stack this resource belongs to. Type: String - ``resourceGroupName`` Name of the resource group this resource belongs to. Type: String - ``terraformSourceName`` Name of the Terraform S3 state file this resource belongs to. Type: String - ``eksSourceName`` Name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to. .. epigraph:: This parameter accepts values in "eks-cluster/namespace" format. Type: String - *``version``* The AWS Resilience Hub application version. - ``additionalInfo`` Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ . .. epigraph:: Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account. Key: ``"failover-regions"`` Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``
        :param description: Optional description for an application.
        :param event_subscriptions: The list of events you would like to subscribe and get notification for. Currently, AWS Resilience Hub supports notifications only for *Drift detected* and *Scheduled assessment failure* events.
        :param name: Name for the application.
        :param permission_model: Defines the roles and credentials that AWS Resilience Hub would use while creating the application, importing its resources, and running an assessment.
        :param resiliency_policy_arn: The Amazon Resource Name (ARN) of the resiliency policy.
        :param resource_mappings: An array of ``ResourceMapping`` objects.
        :param tags: Tags assigned to the resource. A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_resiliencehub import mixins as resiliencehub_mixins
            
            cfn_app_mixin_props = resiliencehub_mixins.CfnAppMixinProps(
                app_assessment_schedule="appAssessmentSchedule",
                app_template_body="appTemplateBody",
                description="description",
                event_subscriptions=[resiliencehub_mixins.CfnAppPropsMixin.EventSubscriptionProperty(
                    event_type="eventType",
                    name="name",
                    sns_topic_arn="snsTopicArn"
                )],
                name="name",
                permission_model=resiliencehub_mixins.CfnAppPropsMixin.PermissionModelProperty(
                    cross_account_role_arns=["crossAccountRoleArns"],
                    invoker_role_name="invokerRoleName",
                    type="type"
                ),
                resiliency_policy_arn="resiliencyPolicyArn",
                resource_mappings=[resiliencehub_mixins.CfnAppPropsMixin.ResourceMappingProperty(
                    eks_source_name="eksSourceName",
                    logical_stack_name="logicalStackName",
                    mapping_type="mappingType",
                    physical_resource_id=resiliencehub_mixins.CfnAppPropsMixin.PhysicalResourceIdProperty(
                        aws_account_id="awsAccountId",
                        aws_region="awsRegion",
                        identifier="identifier",
                        type="type"
                    ),
                    resource_name="resourceName",
                    terraform_source_name="terraformSourceName"
                )],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbd408c2d6823f89a5c83f78f3fa70c73570f9df10d4db0049f88586fffa9c0)
            check_type(argname="argument app_assessment_schedule", value=app_assessment_schedule, expected_type=type_hints["app_assessment_schedule"])
            check_type(argname="argument app_template_body", value=app_template_body, expected_type=type_hints["app_template_body"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_subscriptions", value=event_subscriptions, expected_type=type_hints["event_subscriptions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permission_model", value=permission_model, expected_type=type_hints["permission_model"])
            check_type(argname="argument resiliency_policy_arn", value=resiliency_policy_arn, expected_type=type_hints["resiliency_policy_arn"])
            check_type(argname="argument resource_mappings", value=resource_mappings, expected_type=type_hints["resource_mappings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_assessment_schedule is not None:
            self._values["app_assessment_schedule"] = app_assessment_schedule
        if app_template_body is not None:
            self._values["app_template_body"] = app_template_body
        if description is not None:
            self._values["description"] = description
        if event_subscriptions is not None:
            self._values["event_subscriptions"] = event_subscriptions
        if name is not None:
            self._values["name"] = name
        if permission_model is not None:
            self._values["permission_model"] = permission_model
        if resiliency_policy_arn is not None:
            self._values["resiliency_policy_arn"] = resiliency_policy_arn
        if resource_mappings is not None:
            self._values["resource_mappings"] = resource_mappings
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_assessment_schedule(self) -> typing.Optional[builtins.str]:
        '''Assessment execution schedule with 'Daily' or 'Disabled' values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-appassessmentschedule
        '''
        result = self._values.get("app_assessment_schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_template_body(self) -> typing.Optional[builtins.str]:
        '''A JSON string that provides information about your application structure.

        To learn more about the ``appTemplateBody`` template, see the sample template in `Sample appTemplateBody template <https://docs.aws.amazon.com//resilience-hub/latest/APIReference/API_PutDraftAppVersionTemplate.html#API_PutDraftAppVersionTemplate_Examples>`_ .

        The ``appTemplateBody`` JSON string has the following structure:

        - *``resources``*

        The list of logical resources that needs to be included in the AWS Resilience Hub application.

        Type: Array
        .. epigraph::

           Don't add the resources that you want to exclude.

        Each ``resources`` array item includes the following fields:

        - *``logicalResourceId``*

        The logical identifier of the resource.

        Type: Object

        Each ``logicalResourceId`` object includes the following fields:

        - ``identifier``

        Identifier of the resource.

        Type: String

        - ``logicalStackName``

        Name of the AWS CloudFormation stack this resource belongs to.

        Type: String

        - ``resourceGroupName``

        Name of the resource group this resource belongs to.

        Type: String

        - ``terraformSourceName``

        Name of the Terraform S3 state file this resource belongs to.

        Type: String

        - ``eksSourceName``

        Name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to.
        .. epigraph::

           This parameter accepts values in "eks-cluster/namespace" format.

        Type: String

        - *``type``*

        The type of resource.

        Type: string

        - *``name``*

        Name of the resource.

        Type: String

        - ``additionalInfo``

        Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ .
        .. epigraph::

           Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account.

           Key: ``"failover-regions"``

           Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``

        - *``appComponents``*

        The list of Application Components (AppComponent) that this resource belongs to. If an AppComponent is not part of the AWS Resilience Hub application, it will be added.

        Type: Array

        Each ``appComponents`` array item includes the following fields:

        - ``name``

        Name of the AppComponent.

        Type: String

        - ``type``

        The type of AppComponent. For more information about the types of AppComponent, see `Grouping resources in an AppComponent <https://docs.aws.amazon.com/resilience-hub/latest/userguide/AppComponent.grouping.html>`_ .

        Type: String

        - ``resourceNames``

        The list of included resources that are assigned to the AppComponent.

        Type: Array of strings

        - ``additionalInfo``

        Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ .
        .. epigraph::

           Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account.

           Key: ``"failover-regions"``

           Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``

        - *``excludedResources``*

        The list of logical resource identifiers to be excluded from the application.

        Type: Array
        .. epigraph::

           Don't add the resources that you want to include.

        Each ``excludedResources`` array item includes the following fields:

        - *``logicalResourceIds``*

        The logical identifier of the resource.

        Type: Object
        .. epigraph::

           You can configure only one of the following fields:

           - ``logicalStackName``
           - ``resourceGroupName``
           - ``terraformSourceName``
           - ``eksSourceName``

        Each ``logicalResourceIds`` object includes the following fields:

        - ``identifier``

        The identifier of the resource.

        Type: String

        - ``logicalStackName``

        Name of the AWS CloudFormation stack this resource belongs to.

        Type: String

        - ``resourceGroupName``

        Name of the resource group this resource belongs to.

        Type: String

        - ``terraformSourceName``

        Name of the Terraform S3 state file this resource belongs to.

        Type: String

        - ``eksSourceName``

        Name of the Amazon Elastic Kubernetes Service cluster and namespace this resource belongs to.
        .. epigraph::

           This parameter accepts values in "eks-cluster/namespace" format.

        Type: String

        - *``version``*

        The AWS Resilience Hub application version.

        - ``additionalInfo``

        Additional configuration parameters for an AWS Resilience Hub application. If you want to implement ``additionalInfo`` through the AWS Resilience Hub console rather than using an API call, see `Configure the application configuration parameters <https://docs.aws.amazon.com//resilience-hub/latest/userguide/app-config-param.html>`_ .
        .. epigraph::

           Currently, this parameter accepts a key-value mapping (in a string format) of only one failover region and one associated account.

           Key: ``"failover-regions"``

           Value: ``"[{"region":"<REGION>", "accounts":[{"id":"<ACCOUNT_ID>"}]}]"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-apptemplatebody
        '''
        result = self._values.get("app_template_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional description for an application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_subscriptions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.EventSubscriptionProperty"]]]]:
        '''The list of events you would like to subscribe and get notification for.

        Currently, AWS Resilience Hub supports notifications only for *Drift detected* and *Scheduled assessment failure* events.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-eventsubscriptions
        '''
        result = self._values.get("event_subscriptions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.EventSubscriptionProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name for the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission_model(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.PermissionModelProperty"]]:
        '''Defines the roles and credentials that AWS Resilience Hub would use while creating the application, importing its resources, and running an assessment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-permissionmodel
        '''
        result = self._values.get("permission_model")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.PermissionModelProperty"]], result)

    @builtins.property
    def resiliency_policy_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resiliency policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resiliencypolicyarn
        '''
        result = self._values.get("resiliency_policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.ResourceMappingProperty"]]]]:
        '''An array of ``ResourceMapping`` objects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-resourcemappings
        '''
        result = self._values.get("resource_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.ResourceMappingProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags assigned to the resource.

        A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html#cfn-resiliencehub-app-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_resiliencehub.mixins.CfnAppPropsMixin",
):
    '''Creates an AWS Resilience Hub application.

    An AWS Resilience Hub application is a collection of AWS resources structured to prevent and recover AWS application disruptions. To describe a AWS Resilience Hub application, you provide an application name, resources from one or more AWS CloudFormation stacks, AWS Resource Groups , Terraform state files, AppRegistry applications, and an appropriate resiliency policy. In addition, you can also add resources that are located on Amazon Elastic Kubernetes Service (Amazon EKS) clusters as optional resources. For more information about the number of resources supported per application, see `Service quotas <https://docs.aws.amazon.com/general/latest/gr/resiliencehub.html#limits_resiliencehub>`_ .

    After you create an AWS Resilience Hub application, you publish it so that you can run a resiliency assessment on it. You can then use recommendations from the assessment to improve resiliency by running another assessment, comparing results, and then iterating the process until you achieve your goals for recovery time objective (RTO) and recovery point objective (RPO).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-app.html
    :cloudformationResource: AWS::ResilienceHub::App
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_resiliencehub import mixins as resiliencehub_mixins
        
        cfn_app_props_mixin = resiliencehub_mixins.CfnAppPropsMixin(resiliencehub_mixins.CfnAppMixinProps(
            app_assessment_schedule="appAssessmentSchedule",
            app_template_body="appTemplateBody",
            description="description",
            event_subscriptions=[resiliencehub_mixins.CfnAppPropsMixin.EventSubscriptionProperty(
                event_type="eventType",
                name="name",
                sns_topic_arn="snsTopicArn"
            )],
            name="name",
            permission_model=resiliencehub_mixins.CfnAppPropsMixin.PermissionModelProperty(
                cross_account_role_arns=["crossAccountRoleArns"],
                invoker_role_name="invokerRoleName",
                type="type"
            ),
            resiliency_policy_arn="resiliencyPolicyArn",
            resource_mappings=[resiliencehub_mixins.CfnAppPropsMixin.ResourceMappingProperty(
                eks_source_name="eksSourceName",
                logical_stack_name="logicalStackName",
                mapping_type="mappingType",
                physical_resource_id=resiliencehub_mixins.CfnAppPropsMixin.PhysicalResourceIdProperty(
                    aws_account_id="awsAccountId",
                    aws_region="awsRegion",
                    identifier="identifier",
                    type="type"
                ),
                resource_name="resourceName",
                terraform_source_name="terraformSourceName"
            )],
            tags={
                "tags_key": "tags"
            }
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
        '''Create a mixin to apply properties to ``AWS::ResilienceHub::App``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641d7f5fdb9f05d6e0b11ebc0cbb09cf41e67d67d2e0e38d518f04839fa7e0d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffcd4e8cc96799c943bf6a486a93b1e189571816a8d020728a24400236c53cdf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb78b95c60f0bf7463d22e1cfdc728bce8283189e78de2aefaed136ac989eaf)
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
        jsii_type="@aws-cdk/mixins-preview.aws_resiliencehub.mixins.CfnAppPropsMixin.EventSubscriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_type": "eventType",
            "name": "name",
            "sns_topic_arn": "snsTopicArn",
        },
    )
    class EventSubscriptionProperty:
        def __init__(
            self,
            *,
            event_type: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            sns_topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Indicates an event you would like to subscribe and get notification for.

            Currently, AWS Resilience Hub supports notifications only for *Drift detected* and *Scheduled assessment failure* events.

            :param event_type: The type of event you would like to subscribe and get notification for. Currently, AWS Resilience Hub supports notifications only for *Drift detected* ( ``DriftDetected`` ) and *Scheduled assessment failure* ( ``ScheduledAssessmentFailure`` ) events.
            :param name: Unique name to identify an event subscription.
            :param sns_topic_arn: Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic. The format for this ARN is: ``arn:partition:sns:region:account:topic-name`` . For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-eventsubscription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resiliencehub import mixins as resiliencehub_mixins
                
                event_subscription_property = resiliencehub_mixins.CfnAppPropsMixin.EventSubscriptionProperty(
                    event_type="eventType",
                    name="name",
                    sns_topic_arn="snsTopicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ab8916bcae7d87ada1bac38ee4c0025181fbec23f790c8baf35ade2f156f70c)
                check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_type is not None:
                self._values["event_type"] = event_type
            if name is not None:
                self._values["name"] = name
            if sns_topic_arn is not None:
                self._values["sns_topic_arn"] = sns_topic_arn

        @builtins.property
        def event_type(self) -> typing.Optional[builtins.str]:
            '''The type of event you would like to subscribe and get notification for.

            Currently, AWS Resilience Hub supports notifications only for *Drift detected* ( ``DriftDetected`` ) and *Scheduled assessment failure* ( ``ScheduledAssessmentFailure`` ) events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-eventsubscription.html#cfn-resiliencehub-app-eventsubscription-eventtype
            '''
            result = self._values.get("event_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Unique name to identify an event subscription.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-eventsubscription.html#cfn-resiliencehub-app-eventsubscription-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sns_topic_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) of the Amazon Simple Notification Service topic.

            The format for this ARN is: ``arn:partition:sns:region:account:topic-name`` . For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-eventsubscription.html#cfn-resiliencehub-app-eventsubscription-snstopicarn
            '''
            result = self._values.get("sns_topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSubscriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resiliencehub.mixins.CfnAppPropsMixin.PermissionModelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cross_account_role_arns": "crossAccountRoleArns",
            "invoker_role_name": "invokerRoleName",
            "type": "type",
        },
    )
    class PermissionModelProperty:
        def __init__(
            self,
            *,
            cross_account_role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            invoker_role_name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the roles and credentials that AWS Resilience Hub would use while creating the application, importing its resources, and running an assessment.

            :param cross_account_role_arns: Defines a list of role Amazon Resource Names (ARNs) to be used in other accounts. These ARNs are used for querying purposes while importing resources and assessing your application. .. epigraph:: - These ARNs are required only when your resources are in other accounts and you have different role name in these accounts. Else, the invoker role name will be used in the other accounts. - These roles must have a trust policy with ``iam:AssumeRole`` permission to the invoker role in the primary account.
            :param invoker_role_name: Existing AWS IAM role name in the primary AWS account that will be assumed by AWS Resilience Hub Service Principle to obtain a read-only access to your application resources while running an assessment. If your IAM role includes a path, you must include the path in the ``invokerRoleName`` parameter. For example, if your IAM role's ARN is ``arn:aws:iam:123456789012:role/my-path/role-name`` , you should pass ``my-path/role-name`` . .. epigraph:: - You must have ``iam:passRole`` permission for this role while creating or updating the application. - Currently, ``invokerRoleName`` accepts only ``[A-Za-z0-9_+=,.@-]`` characters.
            :param type: Defines how AWS Resilience Hub scans your resources. It can scan for the resources by using a pre-existing role in your AWS account, or by using the credentials of the current IAM user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-permissionmodel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resiliencehub import mixins as resiliencehub_mixins
                
                permission_model_property = resiliencehub_mixins.CfnAppPropsMixin.PermissionModelProperty(
                    cross_account_role_arns=["crossAccountRoleArns"],
                    invoker_role_name="invokerRoleName",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d511dc5b39fa6a30d7318bee7e987c58a8a7395e99b0505103bb85293e6f6865)
                check_type(argname="argument cross_account_role_arns", value=cross_account_role_arns, expected_type=type_hints["cross_account_role_arns"])
                check_type(argname="argument invoker_role_name", value=invoker_role_name, expected_type=type_hints["invoker_role_name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cross_account_role_arns is not None:
                self._values["cross_account_role_arns"] = cross_account_role_arns
            if invoker_role_name is not None:
                self._values["invoker_role_name"] = invoker_role_name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def cross_account_role_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Defines a list of role Amazon Resource Names (ARNs) to be used in other accounts.

            These ARNs are used for querying purposes while importing resources and assessing your application.
            .. epigraph::

               - These ARNs are required only when your resources are in other accounts and you have different role name in these accounts. Else, the invoker role name will be used in the other accounts.
               - These roles must have a trust policy with ``iam:AssumeRole`` permission to the invoker role in the primary account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-permissionmodel.html#cfn-resiliencehub-app-permissionmodel-crossaccountrolearns
            '''
            result = self._values.get("cross_account_role_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def invoker_role_name(self) -> typing.Optional[builtins.str]:
            '''Existing AWS IAM role name in the primary AWS account that will be assumed by AWS Resilience Hub Service Principle to obtain a read-only access to your application resources while running an assessment.

            If your IAM role includes a path, you must include the path in the ``invokerRoleName`` parameter. For example, if your IAM role's ARN is ``arn:aws:iam:123456789012:role/my-path/role-name`` , you should pass ``my-path/role-name`` .
            .. epigraph::

               - You must have ``iam:passRole`` permission for this role while creating or updating the application.
               - Currently, ``invokerRoleName`` accepts only ``[A-Za-z0-9_+=,.@-]`` characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-permissionmodel.html#cfn-resiliencehub-app-permissionmodel-invokerrolename
            '''
            result = self._values.get("invoker_role_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Defines how AWS Resilience Hub scans your resources.

            It can scan for the resources by using a pre-existing role in your AWS account, or by using the credentials of the current IAM user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-permissionmodel.html#cfn-resiliencehub-app-permissionmodel-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PermissionModelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resiliencehub.mixins.CfnAppPropsMixin.PhysicalResourceIdProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_account_id": "awsAccountId",
            "aws_region": "awsRegion",
            "identifier": "identifier",
            "type": "type",
        },
    )
    class PhysicalResourceIdProperty:
        def __init__(
            self,
            *,
            aws_account_id: typing.Optional[builtins.str] = None,
            aws_region: typing.Optional[builtins.str] = None,
            identifier: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a physical resource identifier.

            :param aws_account_id: The AWS account that owns the physical resource.
            :param aws_region: The AWS Region that the physical resource is located in.
            :param identifier: Identifier of the physical resource.
            :param type: Specifies the type of physical resource identifier. - **Arn** - The resource identifier is an Amazon Resource Name (ARN) and it can identify the following list of resources: - ``AWS::ECS::Service`` - ``AWS::EFS::FileSystem`` - ``AWS::ElasticLoadBalancingV2::LoadBalancer`` - ``AWS::Lambda::Function`` - ``AWS::SNS::Topic`` - **Native** - The resource identifier is an AWS Resilience Hub -native identifier and it can identify the following list of resources: - ``AWS::ApiGateway::RestApi`` - ``AWS::ApiGatewayV2::Api`` - ``AWS::AutoScaling::AutoScalingGroup`` - ``AWS::DocDB::DBCluster`` - ``AWS::DocDB::DBGlobalCluster`` - ``AWS::DocDB::DBInstance`` - ``AWS::DynamoDB::GlobalTable`` - ``AWS::DynamoDB::Table`` - ``AWS::EC2::EC2Fleet`` - ``AWS::EC2::Instance`` - ``AWS::EC2::NatGateway`` - ``AWS::EC2::Volume`` - ``AWS::ElasticLoadBalancing::LoadBalancer`` - ``AWS::RDS::DBCluster`` - ``AWS::RDS::DBInstance`` - ``AWS::RDS::GlobalCluster`` - ``AWS::Route53::RecordSet`` - ``AWS::S3::Bucket`` - ``AWS::SQS::Queue``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resiliencehub import mixins as resiliencehub_mixins
                
                physical_resource_id_property = resiliencehub_mixins.CfnAppPropsMixin.PhysicalResourceIdProperty(
                    aws_account_id="awsAccountId",
                    aws_region="awsRegion",
                    identifier="identifier",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__176e772aff67048e3f5b1a7cd08de069ede5c9b820b757a5f8a29f0dc5501961)
                check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
                check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_account_id is not None:
                self._values["aws_account_id"] = aws_account_id
            if aws_region is not None:
                self._values["aws_region"] = aws_region
            if identifier is not None:
                self._values["identifier"] = identifier
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def aws_account_id(self) -> typing.Optional[builtins.str]:
            '''The AWS account that owns the physical resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-awsaccountid
            '''
            result = self._values.get("aws_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aws_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region that the physical resource is located in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-awsregion
            '''
            result = self._values.get("aws_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identifier(self) -> typing.Optional[builtins.str]:
            '''Identifier of the physical resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-identifier
            '''
            result = self._values.get("identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of physical resource identifier.

            - **Arn** - The resource identifier is an Amazon Resource Name (ARN) and it can identify the following list of resources:
            - ``AWS::ECS::Service``
            - ``AWS::EFS::FileSystem``
            - ``AWS::ElasticLoadBalancingV2::LoadBalancer``
            - ``AWS::Lambda::Function``
            - ``AWS::SNS::Topic``
            - **Native** - The resource identifier is an AWS Resilience Hub -native identifier and it can identify the following list of resources:
            - ``AWS::ApiGateway::RestApi``
            - ``AWS::ApiGatewayV2::Api``
            - ``AWS::AutoScaling::AutoScalingGroup``
            - ``AWS::DocDB::DBCluster``
            - ``AWS::DocDB::DBGlobalCluster``
            - ``AWS::DocDB::DBInstance``
            - ``AWS::DynamoDB::GlobalTable``
            - ``AWS::DynamoDB::Table``
            - ``AWS::EC2::EC2Fleet``
            - ``AWS::EC2::Instance``
            - ``AWS::EC2::NatGateway``
            - ``AWS::EC2::Volume``
            - ``AWS::ElasticLoadBalancing::LoadBalancer``
            - ``AWS::RDS::DBCluster``
            - ``AWS::RDS::DBInstance``
            - ``AWS::RDS::GlobalCluster``
            - ``AWS::Route53::RecordSet``
            - ``AWS::S3::Bucket``
            - ``AWS::SQS::Queue``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-physicalresourceid.html#cfn-resiliencehub-app-physicalresourceid-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PhysicalResourceIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resiliencehub.mixins.CfnAppPropsMixin.ResourceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "eks_source_name": "eksSourceName",
            "logical_stack_name": "logicalStackName",
            "mapping_type": "mappingType",
            "physical_resource_id": "physicalResourceId",
            "resource_name": "resourceName",
            "terraform_source_name": "terraformSourceName",
        },
    )
    class ResourceMappingProperty:
        def __init__(
            self,
            *,
            eks_source_name: typing.Optional[builtins.str] = None,
            logical_stack_name: typing.Optional[builtins.str] = None,
            mapping_type: typing.Optional[builtins.str] = None,
            physical_resource_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.PhysicalResourceIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_name: typing.Optional[builtins.str] = None,
            terraform_source_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a resource mapping.

            :param eks_source_name: Name of the Amazon Elastic Kubernetes Service cluster and namespace that this resource is mapped to when the ``mappingType`` is ``EKS`` . .. epigraph:: This parameter accepts values in "eks-cluster/namespace" format.
            :param logical_stack_name: Name of the CloudFormation stack this resource is mapped to when the ``mappingType`` is ``CfnStack`` .
            :param mapping_type: Specifies the type of resource mapping.
            :param physical_resource_id: Identifier of the physical resource.
            :param resource_name: Name of the resource that this resource is mapped to when the ``mappingType`` is ``Resource`` .
            :param terraform_source_name: Name of the Terraform source that this resource is mapped to when the ``mappingType`` is ``Terraform`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resiliencehub import mixins as resiliencehub_mixins
                
                resource_mapping_property = resiliencehub_mixins.CfnAppPropsMixin.ResourceMappingProperty(
                    eks_source_name="eksSourceName",
                    logical_stack_name="logicalStackName",
                    mapping_type="mappingType",
                    physical_resource_id=resiliencehub_mixins.CfnAppPropsMixin.PhysicalResourceIdProperty(
                        aws_account_id="awsAccountId",
                        aws_region="awsRegion",
                        identifier="identifier",
                        type="type"
                    ),
                    resource_name="resourceName",
                    terraform_source_name="terraformSourceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7718316e8048207f18e2783733968c90fa3f9d14c70450b23909bedc1e156f34)
                check_type(argname="argument eks_source_name", value=eks_source_name, expected_type=type_hints["eks_source_name"])
                check_type(argname="argument logical_stack_name", value=logical_stack_name, expected_type=type_hints["logical_stack_name"])
                check_type(argname="argument mapping_type", value=mapping_type, expected_type=type_hints["mapping_type"])
                check_type(argname="argument physical_resource_id", value=physical_resource_id, expected_type=type_hints["physical_resource_id"])
                check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
                check_type(argname="argument terraform_source_name", value=terraform_source_name, expected_type=type_hints["terraform_source_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if eks_source_name is not None:
                self._values["eks_source_name"] = eks_source_name
            if logical_stack_name is not None:
                self._values["logical_stack_name"] = logical_stack_name
            if mapping_type is not None:
                self._values["mapping_type"] = mapping_type
            if physical_resource_id is not None:
                self._values["physical_resource_id"] = physical_resource_id
            if resource_name is not None:
                self._values["resource_name"] = resource_name
            if terraform_source_name is not None:
                self._values["terraform_source_name"] = terraform_source_name

        @builtins.property
        def eks_source_name(self) -> typing.Optional[builtins.str]:
            '''Name of the Amazon Elastic Kubernetes Service cluster and namespace that this resource is mapped to when the ``mappingType`` is ``EKS`` .

            .. epigraph::

               This parameter accepts values in "eks-cluster/namespace" format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-ekssourcename
            '''
            result = self._values.get("eks_source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logical_stack_name(self) -> typing.Optional[builtins.str]:
            '''Name of the CloudFormation stack this resource is mapped to when the ``mappingType`` is ``CfnStack`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-logicalstackname
            '''
            result = self._values.get("logical_stack_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mapping_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of resource mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-mappingtype
            '''
            result = self._values.get("mapping_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def physical_resource_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.PhysicalResourceIdProperty"]]:
            '''Identifier of the physical resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-physicalresourceid
            '''
            result = self._values.get("physical_resource_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.PhysicalResourceIdProperty"]], result)

        @builtins.property
        def resource_name(self) -> typing.Optional[builtins.str]:
            '''Name of the resource that this resource is mapped to when the ``mappingType`` is ``Resource`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-resourcename
            '''
            result = self._values.get("resource_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def terraform_source_name(self) -> typing.Optional[builtins.str]:
            '''Name of the Terraform source that this resource is mapped to when the ``mappingType`` is ``Terraform`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-app-resourcemapping.html#cfn-resiliencehub-app-resourcemapping-terraformsourcename
            '''
            result = self._values.get("terraform_source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_resiliencehub.mixins.CfnResiliencyPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_location_constraint": "dataLocationConstraint",
        "policy": "policy",
        "policy_description": "policyDescription",
        "policy_name": "policyName",
        "tags": "tags",
        "tier": "tier",
    },
)
class CfnResiliencyPolicyMixinProps:
    def __init__(
        self,
        *,
        data_location_constraint: typing.Optional[builtins.str] = None,
        policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResiliencyPolicyPropsMixin.FailurePolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        policy_description: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResiliencyPolicyPropsMixin.

        :param data_location_constraint: Specifies a high-level geographical location constraint for where your resilience policy data can be stored.
        :param policy: The resiliency policy.
        :param policy_description: Description of the resiliency policy.
        :param policy_name: The name of the policy.
        :param tags: Tags assigned to the resource. A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.
        :param tier: The tier for this resiliency policy, ranging from the highest severity ( ``MissionCritical`` ) to lowest ( ``NonCritical`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_resiliencehub import mixins as resiliencehub_mixins
            
            cfn_resiliency_policy_mixin_props = resiliencehub_mixins.CfnResiliencyPolicyMixinProps(
                data_location_constraint="dataLocationConstraint",
                policy={
                    "policy_key": resiliencehub_mixins.CfnResiliencyPolicyPropsMixin.FailurePolicyProperty(
                        rpo_in_secs=123,
                        rto_in_secs=123
                    )
                },
                policy_description="policyDescription",
                policy_name="policyName",
                tags={
                    "tags_key": "tags"
                },
                tier="tier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f35b7e4a8655867e1ee2a09cb15de73e333dc13ff84e4022d1a96d4b8e2da63a)
            check_type(argname="argument data_location_constraint", value=data_location_constraint, expected_type=type_hints["data_location_constraint"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument policy_description", value=policy_description, expected_type=type_hints["policy_description"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_location_constraint is not None:
            self._values["data_location_constraint"] = data_location_constraint
        if policy is not None:
            self._values["policy"] = policy
        if policy_description is not None:
            self._values["policy_description"] = policy_description
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if tags is not None:
            self._values["tags"] = tags
        if tier is not None:
            self._values["tier"] = tier

    @builtins.property
    def data_location_constraint(self) -> typing.Optional[builtins.str]:
        '''Specifies a high-level geographical location constraint for where your resilience policy data can be stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-datalocationconstraint
        '''
        result = self._values.get("data_location_constraint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResiliencyPolicyPropsMixin.FailurePolicyProperty"]]]]:
        '''The resiliency policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResiliencyPolicyPropsMixin.FailurePolicyProperty"]]]], result)

    @builtins.property
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''Description of the resiliency policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policydescription
        '''
        result = self._values.get("policy_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags assigned to the resource.

        A tag is a label that you assign to an AWS resource. Each tag consists of a key/value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The tier for this resiliency policy, ranging from the highest severity ( ``MissionCritical`` ) to lowest ( ``NonCritical`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html#cfn-resiliencehub-resiliencypolicy-tier
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResiliencyPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResiliencyPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_resiliencehub.mixins.CfnResiliencyPolicyPropsMixin",
):
    '''Defines a resiliency policy.

    .. epigraph::

       AWS Resilience Hub allows you to provide a value of zero for ``rtoInSecs`` and ``rpoInSecs`` of your resiliency policy. But, while assessing your application, the lowest possible assessment result is near zero. Hence, if you provide value zero for ``rtoInSecs`` and ``rpoInSecs`` , the estimated workload RTO and estimated workload RPO result will be near zero and the *Compliance status* for your application will be set to *Policy breached* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resiliencehub-resiliencypolicy.html
    :cloudformationResource: AWS::ResilienceHub::ResiliencyPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_resiliencehub import mixins as resiliencehub_mixins
        
        cfn_resiliency_policy_props_mixin = resiliencehub_mixins.CfnResiliencyPolicyPropsMixin(resiliencehub_mixins.CfnResiliencyPolicyMixinProps(
            data_location_constraint="dataLocationConstraint",
            policy={
                "policy_key": resiliencehub_mixins.CfnResiliencyPolicyPropsMixin.FailurePolicyProperty(
                    rpo_in_secs=123,
                    rto_in_secs=123
                )
            },
            policy_description="policyDescription",
            policy_name="policyName",
            tags={
                "tags_key": "tags"
            },
            tier="tier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResiliencyPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ResilienceHub::ResiliencyPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ba2f179e164ee7cb45a11faacc1fc08eee37d82bea1a7e8276cdd30037a941)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b07ef32db1ad205ba2da683b78ddf449b441b2fd0cfaa0bba28547da3711b696)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852031bc7c0a2c6f919e9f82b81142fa60e189445c8075f913c78ab8f67819f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResiliencyPolicyMixinProps:
        return typing.cast(CfnResiliencyPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_resiliencehub.mixins.CfnResiliencyPolicyPropsMixin.FailurePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"rpo_in_secs": "rpoInSecs", "rto_in_secs": "rtoInSecs"},
    )
    class FailurePolicyProperty:
        def __init__(
            self,
            *,
            rpo_in_secs: typing.Optional[jsii.Number] = None,
            rto_in_secs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines a failure policy.

            :param rpo_in_secs: Recovery Point Objective (RPO) in seconds.
            :param rto_in_secs: Recovery Time Objective (RTO) in seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-resiliencypolicy-failurepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_resiliencehub import mixins as resiliencehub_mixins
                
                failure_policy_property = resiliencehub_mixins.CfnResiliencyPolicyPropsMixin.FailurePolicyProperty(
                    rpo_in_secs=123,
                    rto_in_secs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65cfe873bae5f7fa1a18af3d32608d3f88dc29ebc71fad9537ebcf5c6c816b8d)
                check_type(argname="argument rpo_in_secs", value=rpo_in_secs, expected_type=type_hints["rpo_in_secs"])
                check_type(argname="argument rto_in_secs", value=rto_in_secs, expected_type=type_hints["rto_in_secs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rpo_in_secs is not None:
                self._values["rpo_in_secs"] = rpo_in_secs
            if rto_in_secs is not None:
                self._values["rto_in_secs"] = rto_in_secs

        @builtins.property
        def rpo_in_secs(self) -> typing.Optional[jsii.Number]:
            '''Recovery Point Objective (RPO) in seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-resiliencypolicy-failurepolicy.html#cfn-resiliencehub-resiliencypolicy-failurepolicy-rpoinsecs
            '''
            result = self._values.get("rpo_in_secs")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rto_in_secs(self) -> typing.Optional[jsii.Number]:
            '''Recovery Time Objective (RTO) in seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resiliencehub-resiliencypolicy-failurepolicy.html#cfn-resiliencehub-resiliencypolicy-failurepolicy-rtoinsecs
            '''
            result = self._values.get("rto_in_secs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailurePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAppMixinProps",
    "CfnAppPropsMixin",
    "CfnResiliencyPolicyMixinProps",
    "CfnResiliencyPolicyPropsMixin",
]

publication.publish()

def _typecheckingstub__dcbd408c2d6823f89a5c83f78f3fa70c73570f9df10d4db0049f88586fffa9c0(
    *,
    app_assessment_schedule: typing.Optional[builtins.str] = None,
    app_template_body: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    event_subscriptions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.EventSubscriptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    permission_model: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.PermissionModelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resiliency_policy_arn: typing.Optional[builtins.str] = None,
    resource_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.ResourceMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641d7f5fdb9f05d6e0b11ebc0cbb09cf41e67d67d2e0e38d518f04839fa7e0d3(
    props: typing.Union[CfnAppMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffcd4e8cc96799c943bf6a486a93b1e189571816a8d020728a24400236c53cdf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb78b95c60f0bf7463d22e1cfdc728bce8283189e78de2aefaed136ac989eaf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab8916bcae7d87ada1bac38ee4c0025181fbec23f790c8baf35ade2f156f70c(
    *,
    event_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d511dc5b39fa6a30d7318bee7e987c58a8a7395e99b0505103bb85293e6f6865(
    *,
    cross_account_role_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    invoker_role_name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176e772aff67048e3f5b1a7cd08de069ede5c9b820b757a5f8a29f0dc5501961(
    *,
    aws_account_id: typing.Optional[builtins.str] = None,
    aws_region: typing.Optional[builtins.str] = None,
    identifier: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7718316e8048207f18e2783733968c90fa3f9d14c70450b23909bedc1e156f34(
    *,
    eks_source_name: typing.Optional[builtins.str] = None,
    logical_stack_name: typing.Optional[builtins.str] = None,
    mapping_type: typing.Optional[builtins.str] = None,
    physical_resource_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.PhysicalResourceIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_name: typing.Optional[builtins.str] = None,
    terraform_source_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f35b7e4a8655867e1ee2a09cb15de73e333dc13ff84e4022d1a96d4b8e2da63a(
    *,
    data_location_constraint: typing.Optional[builtins.str] = None,
    policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResiliencyPolicyPropsMixin.FailurePolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    policy_description: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ba2f179e164ee7cb45a11faacc1fc08eee37d82bea1a7e8276cdd30037a941(
    props: typing.Union[CfnResiliencyPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07ef32db1ad205ba2da683b78ddf449b441b2fd0cfaa0bba28547da3711b696(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852031bc7c0a2c6f919e9f82b81142fa60e189445c8075f913c78ab8f67819f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cfe873bae5f7fa1a18af3d32608d3f88dc29ebc71fad9537ebcf5c6c816b8d(
    *,
    rpo_in_secs: typing.Optional[jsii.Number] = None,
    rto_in_secs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
