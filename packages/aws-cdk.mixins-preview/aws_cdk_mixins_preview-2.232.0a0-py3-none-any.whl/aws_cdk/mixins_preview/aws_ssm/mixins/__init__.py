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
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "apply_only_at_cron_interval": "applyOnlyAtCronInterval",
        "association_name": "associationName",
        "automation_target_parameter_name": "automationTargetParameterName",
        "calendar_names": "calendarNames",
        "compliance_severity": "complianceSeverity",
        "document_version": "documentVersion",
        "instance_id": "instanceId",
        "max_concurrency": "maxConcurrency",
        "max_errors": "maxErrors",
        "name": "name",
        "output_location": "outputLocation",
        "parameters": "parameters",
        "schedule_expression": "scheduleExpression",
        "schedule_offset": "scheduleOffset",
        "sync_compliance": "syncCompliance",
        "targets": "targets",
        "wait_for_success_timeout_seconds": "waitForSuccessTimeoutSeconds",
    },
)
class CfnAssociationMixinProps:
    def __init__(
        self,
        *,
        apply_only_at_cron_interval: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        association_name: typing.Optional[builtins.str] = None,
        automation_target_parameter_name: typing.Optional[builtins.str] = None,
        calendar_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        compliance_severity: typing.Optional[builtins.str] = None,
        document_version: typing.Optional[builtins.str] = None,
        instance_id: typing.Optional[builtins.str] = None,
        max_concurrency: typing.Optional[builtins.str] = None,
        max_errors: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        output_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.InstanceAssociationOutputLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        parameters: typing.Any = None,
        schedule_expression: typing.Optional[builtins.str] = None,
        schedule_offset: typing.Optional[jsii.Number] = None,
        sync_compliance: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.TargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        wait_for_success_timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnAssociationPropsMixin.

        :param apply_only_at_cron_interval: By default, when you create a new association, the system runs it immediately after it is created and then according to the schedule you specified. Specify this option if you don't want an association to run immediately after you create it. This parameter is not supported for rate expressions.
        :param association_name: Specify a descriptive name for the association.
        :param automation_target_parameter_name: Choose the parameter that will define how your automation will branch out. This target is required for associations that use an Automation runbook and target resources by using rate controls. Automation is a tool in AWS Systems Manager .
        :param calendar_names: The names or Amazon Resource Names (ARNs) of the Change Calendar type documents your associations are gated under. The associations only run when that Change Calendar is open. For more information, see `AWS Systems Manager Change Calendar <https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-change-calendar>`_ in the *AWS Systems Manager User Guide* .
        :param compliance_severity: The severity level that is assigned to the association.
        :param document_version: The version of the SSM document to associate with the target. .. epigraph:: Note the following important information. - State Manager doesn't support running associations that use a new version of a document if that document is shared from another account. State Manager always runs the ``default`` version of a document if shared from another account, even though the Systems Manager console shows that a new version was processed. If you want to run an association using a new version of a document shared form another account, you must set the document version to ``default`` . - ``DocumentVersion`` is not valid for documents owned by AWS , such as ``AWS-RunPatchBaseline`` or ``AWS-UpdateSSMAgent`` . If you specify ``DocumentVersion`` for an AWS document, the system returns the following error: "Error occurred during operation 'CreateAssociation'." (RequestToken: , HandlerErrorCode: GeneralServiceException).
        :param instance_id: .. epigraph:: ``InstanceId`` has been deprecated. To specify an instance ID for an association, use the ``Targets`` parameter. If you use the parameter ``InstanceId`` , you cannot use the parameters ``AssociationName`` , ``DocumentVersion`` , ``MaxErrors`` , ``MaxConcurrency`` , ``OutputLocation`` , or ``ScheduleExpression`` . To use these parameters, you must use the ``Targets`` parameter. .. epigraph:: Note that in some examples later in this page, ``InstanceIds`` is used as the tag-key name in a ``Targets`` filter. ``InstanceId`` is not used as a parameter. The ID of the instance that the SSM document is associated with. You must specify the ``InstanceId`` or ``Targets`` property.
        :param max_concurrency: The maximum number of targets allowed to run the association at the same time. You can specify a number, for example 10, or a percentage of the target set, for example 10%. The default value is 100%, which means all targets run the association at the same time. If a new managed node starts and attempts to run an association while Systems Manager is running ``MaxConcurrency`` associations, the association is allowed to run. During the next association interval, the new managed node will process its association within the limit specified for ``MaxConcurrency`` .
        :param max_errors: The number of errors that are allowed before the system stops sending requests to run the association on additional targets. You can specify either an absolute number of errors, for example 10, or a percentage of the target set, for example 10%. If you specify 3, for example, the system stops sending requests when the fourth error is received. If you specify 0, then the system stops sending requests after the first error is returned. If you run an association on 50 managed nodes and set ``MaxError`` to 10%, then the system stops sending the request when the sixth error is received. Executions that are already running an association when ``MaxErrors`` is reached are allowed to complete, but some of these executions may fail as well. If you need to ensure that there won't be more than max-errors failed executions, set ``MaxConcurrency`` to 1 so that executions proceed one at a time.
        :param name: The name of the SSM document that contains the configuration information for the instance. You can specify ``Command`` or ``Automation`` documents. The documents can be AWS -predefined documents, documents you created, or a document that is shared with you from another account. For SSM documents that are shared with you from other AWS accounts , you must specify the complete SSM document ARN, in the following format: ``arn:partition:ssm:region:account-id:document/document-name`` For example: ``arn:aws:ssm:us-east-2:12345678912:document/My-Shared-Document`` For AWS -predefined documents and SSM documents you created in your account, you only need to specify the document name. For example, ``AWS -ApplyPatchBaseline`` or ``My-Document`` .
        :param output_location: An Amazon Simple Storage Service (Amazon S3) bucket where you want to store the output details of the request.
        :param parameters: The parameters for the runtime configuration of the document.
        :param schedule_expression: A cron expression that specifies a schedule when the association runs. The schedule runs in Coordinated Universal Time (UTC).
        :param schedule_offset: Number of days to wait after the scheduled day to run an association.
        :param sync_compliance: The mode for generating association compliance. You can specify ``AUTO`` or ``MANUAL`` . In ``AUTO`` mode, the system uses the status of the association execution to determine the compliance status. If the association execution runs successfully, then the association is ``COMPLIANT`` . If the association execution doesn't run successfully, the association is ``NON-COMPLIANT`` . In ``MANUAL`` mode, you must specify the ``AssociationId`` as a parameter for the ``PutComplianceItems`` API action. In this case, compliance data is not managed by State Manager. It is managed by your direct call to the ``PutComplianceItems`` API action. By default, all associations use ``AUTO`` mode.
        :param targets: The targets for the association. You must specify the ``InstanceId`` or ``Targets`` property. You can target all instances in an AWS account by specifying t he ``InstanceIds`` key with a value of ``*`` . Supported formats include the following. - ``Key=InstanceIds,Values=<instance-id-1>,<instance-id-2>,<instance-id-3>`` - ``Key=tag-key,Values=<my-tag-key-1>,<my-tag-key-2>`` To view a JSON and a YAML example that targets all instances, see "Create an association for all managed instances in an AWS account " on the Examples page.
        :param wait_for_success_timeout_seconds: The number of seconds the service should wait for the association status to show "Success" before proceeding with the stack execution. If the association status doesn't show "Success" after the specified number of seconds, then stack creation fails. .. epigraph:: When you specify a value for the ``WaitForSuccessTimeoutSeconds`` , `drift detection <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html>`_ for your CloudFormation stack’s configuration might yield inaccurate results. If drift detection is important in your scenario, we recommend that you don’t include ``WaitForSuccessTimeoutSeconds`` in your template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
            
            # parameters: Any
            
            cfn_association_mixin_props = ssm_mixins.CfnAssociationMixinProps(
                apply_only_at_cron_interval=False,
                association_name="associationName",
                automation_target_parameter_name="automationTargetParameterName",
                calendar_names=["calendarNames"],
                compliance_severity="complianceSeverity",
                document_version="documentVersion",
                instance_id="instanceId",
                max_concurrency="maxConcurrency",
                max_errors="maxErrors",
                name="name",
                output_location=ssm_mixins.CfnAssociationPropsMixin.InstanceAssociationOutputLocationProperty(
                    s3_location=ssm_mixins.CfnAssociationPropsMixin.S3OutputLocationProperty(
                        output_s3_bucket_name="outputS3BucketName",
                        output_s3_key_prefix="outputS3KeyPrefix",
                        output_s3_region="outputS3Region"
                    )
                ),
                parameters=parameters,
                schedule_expression="scheduleExpression",
                schedule_offset=123,
                sync_compliance="syncCompliance",
                targets=[ssm_mixins.CfnAssociationPropsMixin.TargetProperty(
                    key="key",
                    values=["values"]
                )],
                wait_for_success_timeout_seconds=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237e10943445760b75f55cdb0541f55052f71657b70d772dd866a04ab57513cf)
            check_type(argname="argument apply_only_at_cron_interval", value=apply_only_at_cron_interval, expected_type=type_hints["apply_only_at_cron_interval"])
            check_type(argname="argument association_name", value=association_name, expected_type=type_hints["association_name"])
            check_type(argname="argument automation_target_parameter_name", value=automation_target_parameter_name, expected_type=type_hints["automation_target_parameter_name"])
            check_type(argname="argument calendar_names", value=calendar_names, expected_type=type_hints["calendar_names"])
            check_type(argname="argument compliance_severity", value=compliance_severity, expected_type=type_hints["compliance_severity"])
            check_type(argname="argument document_version", value=document_version, expected_type=type_hints["document_version"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument max_errors", value=max_errors, expected_type=type_hints["max_errors"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            check_type(argname="argument schedule_offset", value=schedule_offset, expected_type=type_hints["schedule_offset"])
            check_type(argname="argument sync_compliance", value=sync_compliance, expected_type=type_hints["sync_compliance"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument wait_for_success_timeout_seconds", value=wait_for_success_timeout_seconds, expected_type=type_hints["wait_for_success_timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apply_only_at_cron_interval is not None:
            self._values["apply_only_at_cron_interval"] = apply_only_at_cron_interval
        if association_name is not None:
            self._values["association_name"] = association_name
        if automation_target_parameter_name is not None:
            self._values["automation_target_parameter_name"] = automation_target_parameter_name
        if calendar_names is not None:
            self._values["calendar_names"] = calendar_names
        if compliance_severity is not None:
            self._values["compliance_severity"] = compliance_severity
        if document_version is not None:
            self._values["document_version"] = document_version
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if max_concurrency is not None:
            self._values["max_concurrency"] = max_concurrency
        if max_errors is not None:
            self._values["max_errors"] = max_errors
        if name is not None:
            self._values["name"] = name
        if output_location is not None:
            self._values["output_location"] = output_location
        if parameters is not None:
            self._values["parameters"] = parameters
        if schedule_expression is not None:
            self._values["schedule_expression"] = schedule_expression
        if schedule_offset is not None:
            self._values["schedule_offset"] = schedule_offset
        if sync_compliance is not None:
            self._values["sync_compliance"] = sync_compliance
        if targets is not None:
            self._values["targets"] = targets
        if wait_for_success_timeout_seconds is not None:
            self._values["wait_for_success_timeout_seconds"] = wait_for_success_timeout_seconds

    @builtins.property
    def apply_only_at_cron_interval(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''By default, when you create a new association, the system runs it immediately after it is created and then according to the schedule you specified.

        Specify this option if you don't want an association to run immediately after you create it. This parameter is not supported for rate expressions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-applyonlyatcroninterval
        '''
        result = self._values.get("apply_only_at_cron_interval")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def association_name(self) -> typing.Optional[builtins.str]:
        '''Specify a descriptive name for the association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-associationname
        '''
        result = self._values.get("association_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automation_target_parameter_name(self) -> typing.Optional[builtins.str]:
        '''Choose the parameter that will define how your automation will branch out.

        This target is required for associations that use an Automation runbook and target resources by using rate controls. Automation is a tool in AWS Systems Manager .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-automationtargetparametername
        '''
        result = self._values.get("automation_target_parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def calendar_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The names or Amazon Resource Names (ARNs) of the Change Calendar type documents your associations are gated under.

        The associations only run when that Change Calendar is open. For more information, see `AWS Systems Manager Change Calendar <https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-change-calendar>`_ in the *AWS Systems Manager User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-calendarnames
        '''
        result = self._values.get("calendar_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def compliance_severity(self) -> typing.Optional[builtins.str]:
        '''The severity level that is assigned to the association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-complianceseverity
        '''
        result = self._values.get("compliance_severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_version(self) -> typing.Optional[builtins.str]:
        '''The version of the SSM document to associate with the target.

        .. epigraph::

           Note the following important information.

           - State Manager doesn't support running associations that use a new version of a document if that document is shared from another account. State Manager always runs the ``default`` version of a document if shared from another account, even though the Systems Manager console shows that a new version was processed. If you want to run an association using a new version of a document shared form another account, you must set the document version to ``default`` .
           - ``DocumentVersion`` is not valid for documents owned by AWS , such as ``AWS-RunPatchBaseline`` or ``AWS-UpdateSSMAgent`` . If you specify ``DocumentVersion`` for an AWS document, the system returns the following error: "Error occurred during operation 'CreateAssociation'." (RequestToken: , HandlerErrorCode: GeneralServiceException).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-documentversion
        '''
        result = self._values.get("document_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''.. epigraph::

   ``InstanceId`` has been deprecated.

        To specify an instance ID for an association, use the ``Targets`` parameter. If you use the parameter ``InstanceId`` , you cannot use the parameters ``AssociationName`` , ``DocumentVersion`` , ``MaxErrors`` , ``MaxConcurrency`` , ``OutputLocation`` , or ``ScheduleExpression`` . To use these parameters, you must use the ``Targets`` parameter.
        .. epigraph::

           Note that in some examples later in this page, ``InstanceIds`` is used as the tag-key name in a ``Targets`` filter. ``InstanceId`` is not used as a parameter.

        The ID of the instance that the SSM document is associated with. You must specify the ``InstanceId`` or ``Targets`` property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-instanceid
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrency(self) -> typing.Optional[builtins.str]:
        '''The maximum number of targets allowed to run the association at the same time.

        You can specify a number, for example 10, or a percentage of the target set, for example 10%. The default value is 100%, which means all targets run the association at the same time.

        If a new managed node starts and attempts to run an association while Systems Manager is running ``MaxConcurrency`` associations, the association is allowed to run. During the next association interval, the new managed node will process its association within the limit specified for ``MaxConcurrency`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-maxconcurrency
        '''
        result = self._values.get("max_concurrency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_errors(self) -> typing.Optional[builtins.str]:
        '''The number of errors that are allowed before the system stops sending requests to run the association on additional targets.

        You can specify either an absolute number of errors, for example 10, or a percentage of the target set, for example 10%. If you specify 3, for example, the system stops sending requests when the fourth error is received. If you specify 0, then the system stops sending requests after the first error is returned. If you run an association on 50 managed nodes and set ``MaxError`` to 10%, then the system stops sending the request when the sixth error is received.

        Executions that are already running an association when ``MaxErrors`` is reached are allowed to complete, but some of these executions may fail as well. If you need to ensure that there won't be more than max-errors failed executions, set ``MaxConcurrency`` to 1 so that executions proceed one at a time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-maxerrors
        '''
        result = self._values.get("max_errors")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the SSM document that contains the configuration information for the instance.

        You can specify ``Command`` or ``Automation`` documents. The documents can be AWS -predefined documents, documents you created, or a document that is shared with you from another account. For SSM documents that are shared with you from other AWS accounts , you must specify the complete SSM document ARN, in the following format:

        ``arn:partition:ssm:region:account-id:document/document-name``

        For example: ``arn:aws:ssm:us-east-2:12345678912:document/My-Shared-Document``

        For AWS -predefined documents and SSM documents you created in your account, you only need to specify the document name. For example, ``AWS -ApplyPatchBaseline`` or ``My-Document`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.InstanceAssociationOutputLocationProperty"]]:
        '''An Amazon Simple Storage Service (Amazon S3) bucket where you want to store the output details of the request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-outputlocation
        '''
        result = self._values.get("output_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.InstanceAssociationOutputLocationProperty"]], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''The parameters for the runtime configuration of the document.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        '''A cron expression that specifies a schedule when the association runs.

        The schedule runs in Coordinated Universal Time (UTC).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-scheduleexpression
        '''
        result = self._values.get("schedule_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_offset(self) -> typing.Optional[jsii.Number]:
        '''Number of days to wait after the scheduled day to run an association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-scheduleoffset
        '''
        result = self._values.get("schedule_offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sync_compliance(self) -> typing.Optional[builtins.str]:
        '''The mode for generating association compliance.

        You can specify ``AUTO`` or ``MANUAL`` . In ``AUTO`` mode, the system uses the status of the association execution to determine the compliance status. If the association execution runs successfully, then the association is ``COMPLIANT`` . If the association execution doesn't run successfully, the association is ``NON-COMPLIANT`` .

        In ``MANUAL`` mode, you must specify the ``AssociationId`` as a parameter for the ``PutComplianceItems`` API action. In this case, compliance data is not managed by State Manager. It is managed by your direct call to the ``PutComplianceItems`` API action.

        By default, all associations use ``AUTO`` mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-synccompliance
        '''
        result = self._values.get("sync_compliance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.TargetProperty"]]]]:
        '''The targets for the association.

        You must specify the ``InstanceId`` or ``Targets`` property. You can target all instances in an AWS account by specifying t he ``InstanceIds`` key with a value of ``*`` .

        Supported formats include the following.

        - ``Key=InstanceIds,Values=<instance-id-1>,<instance-id-2>,<instance-id-3>``
        - ``Key=tag-key,Values=<my-tag-key-1>,<my-tag-key-2>``

        To view a JSON and a YAML example that targets all instances, see "Create an association for all managed instances in an AWS account " on the Examples page.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.TargetProperty"]]]], result)

    @builtins.property
    def wait_for_success_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds the service should wait for the association status to show "Success" before proceeding with the stack execution.

        If the association status doesn't show "Success" after the specified number of seconds, then stack creation fails.
        .. epigraph::

           When you specify a value for the ``WaitForSuccessTimeoutSeconds`` , `drift detection <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html>`_ for your CloudFormation stack’s configuration might yield inaccurate results. If drift detection is important in your scenario, we recommend that you don’t include ``WaitForSuccessTimeoutSeconds`` in your template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html#cfn-ssm-association-waitforsuccesstimeoutseconds
        '''
        result = self._values.get("wait_for_success_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnAssociationPropsMixin",
):
    '''The ``AWS::SSM::Association`` resource creates a State Manager association for your managed instances.

    A State Manager association defines the state that you want to maintain on your instances. For example, an association can specify that anti-virus software must be installed and running on your instances, or that certain ports must be closed. For static targets, the association specifies a schedule for when the configuration is reapplied. For dynamic targets, such as an AWS Resource Groups or an AWS Auto Scaling Group, State Manager applies the configuration when new instances are added to the group. The association also specifies actions to take when applying the configuration. For example, an association for anti-virus software might run once a day. If the software is not installed, then State Manager installs it. If the software is installed, but the service is not running, then the association might instruct State Manager to start the service.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html
    :cloudformationResource: AWS::SSM::Association
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
        
        # parameters: Any
        
        cfn_association_props_mixin = ssm_mixins.CfnAssociationPropsMixin(ssm_mixins.CfnAssociationMixinProps(
            apply_only_at_cron_interval=False,
            association_name="associationName",
            automation_target_parameter_name="automationTargetParameterName",
            calendar_names=["calendarNames"],
            compliance_severity="complianceSeverity",
            document_version="documentVersion",
            instance_id="instanceId",
            max_concurrency="maxConcurrency",
            max_errors="maxErrors",
            name="name",
            output_location=ssm_mixins.CfnAssociationPropsMixin.InstanceAssociationOutputLocationProperty(
                s3_location=ssm_mixins.CfnAssociationPropsMixin.S3OutputLocationProperty(
                    output_s3_bucket_name="outputS3BucketName",
                    output_s3_key_prefix="outputS3KeyPrefix",
                    output_s3_region="outputS3Region"
                )
            ),
            parameters=parameters,
            schedule_expression="scheduleExpression",
            schedule_offset=123,
            sync_compliance="syncCompliance",
            targets=[ssm_mixins.CfnAssociationPropsMixin.TargetProperty(
                key="key",
                values=["values"]
            )],
            wait_for_success_timeout_seconds=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSM::Association``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eef7239a34cf2c04cdc979bf72d3aefc65b2032a4513efa4828a4c016c34f3f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21e1200633f9c85b8f82c01cee343d0b5add4d3539536c518f80cc581cdaf4e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc5aa56aab0de65e2006b16c18b20216f36afa43f831e4101ebba0209a70edde)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssociationMixinProps:
        return typing.cast(CfnAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnAssociationPropsMixin.InstanceAssociationOutputLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_location": "s3Location"},
    )
    class InstanceAssociationOutputLocationProperty:
        def __init__(
            self,
            *,
            s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssociationPropsMixin.S3OutputLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``InstanceAssociationOutputLocation`` is a property of the `AWS::SSM::Association <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html>`_ resource that specifies an Amazon S3 bucket where you want to store the results of this association request.

            For the minimal permissions required to enable Amazon S3 output for an association, see `Creating associations <https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-state-assoc.html>`_ in the *Systems Manager User Guide* .

            :param s3_location: ``S3OutputLocation`` is a property of the `InstanceAssociationOutputLocation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-instanceassociationoutputlocation.html>`_ property that specifies an Amazon S3 bucket where you want to store the results of this request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-instanceassociationoutputlocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                instance_association_output_location_property = ssm_mixins.CfnAssociationPropsMixin.InstanceAssociationOutputLocationProperty(
                    s3_location=ssm_mixins.CfnAssociationPropsMixin.S3OutputLocationProperty(
                        output_s3_bucket_name="outputS3BucketName",
                        output_s3_key_prefix="outputS3KeyPrefix",
                        output_s3_region="outputS3Region"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f022ac6e7db47f2a2087a86176a91aa8105cc9ad9c47a3d1a4d187ab367b4bcb)
                check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_location is not None:
                self._values["s3_location"] = s3_location

        @builtins.property
        def s3_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.S3OutputLocationProperty"]]:
            '''``S3OutputLocation`` is a property of the `InstanceAssociationOutputLocation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-instanceassociationoutputlocation.html>`_ property that specifies an Amazon S3 bucket where you want to store the results of this request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-instanceassociationoutputlocation.html#cfn-ssm-association-instanceassociationoutputlocation-s3location
            '''
            result = self._values.get("s3_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssociationPropsMixin.S3OutputLocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceAssociationOutputLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnAssociationPropsMixin.S3OutputLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "output_s3_bucket_name": "outputS3BucketName",
            "output_s3_key_prefix": "outputS3KeyPrefix",
            "output_s3_region": "outputS3Region",
        },
    )
    class S3OutputLocationProperty:
        def __init__(
            self,
            *,
            output_s3_bucket_name: typing.Optional[builtins.str] = None,
            output_s3_key_prefix: typing.Optional[builtins.str] = None,
            output_s3_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``S3OutputLocation`` is a property of the `AWS::SSM::Association <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html>`_ resource that specifies an Amazon S3 bucket where you want to store the results of this association request.

            :param output_s3_bucket_name: The name of the S3 bucket.
            :param output_s3_key_prefix: The S3 bucket subfolder.
            :param output_s3_region: The AWS Region of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-s3outputlocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                s3_output_location_property = ssm_mixins.CfnAssociationPropsMixin.S3OutputLocationProperty(
                    output_s3_bucket_name="outputS3BucketName",
                    output_s3_key_prefix="outputS3KeyPrefix",
                    output_s3_region="outputS3Region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b2de6ab18cc5ae748fb31dc82400281ee33905140bf309eb7138746716f78b9)
                check_type(argname="argument output_s3_bucket_name", value=output_s3_bucket_name, expected_type=type_hints["output_s3_bucket_name"])
                check_type(argname="argument output_s3_key_prefix", value=output_s3_key_prefix, expected_type=type_hints["output_s3_key_prefix"])
                check_type(argname="argument output_s3_region", value=output_s3_region, expected_type=type_hints["output_s3_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if output_s3_bucket_name is not None:
                self._values["output_s3_bucket_name"] = output_s3_bucket_name
            if output_s3_key_prefix is not None:
                self._values["output_s3_key_prefix"] = output_s3_key_prefix
            if output_s3_region is not None:
                self._values["output_s3_region"] = output_s3_region

        @builtins.property
        def output_s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-s3outputlocation.html#cfn-ssm-association-s3outputlocation-outputs3bucketname
            '''
            result = self._values.get("output_s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_s3_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket subfolder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-s3outputlocation.html#cfn-ssm-association-s3outputlocation-outputs3keyprefix
            '''
            result = self._values.get("output_s3_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_s3_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-s3outputlocation.html#cfn-ssm-association-s3outputlocation-outputs3region
            '''
            result = self._values.get("output_s3_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OutputLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnAssociationPropsMixin.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''``Target`` is a property of the `AWS::SSM::Association <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-association.html>`_ resource that specifies the targets for an SSM document in Systems Manager . You can target all instances in an AWS account by specifying the ``InstanceIds`` key with a value of ``*`` . To view a JSON and a YAML example that targets all instances, see the example "Create an association for all managed instances in an AWS account " later in this page.

            :param key: User-defined criteria for sending commands that target managed nodes that meet the criteria.
            :param values: User-defined criteria that maps to ``Key`` . For example, if you specified ``tag:ServerRole`` , you could specify ``value:WebServer`` to run a command on instances that include EC2 tags of ``ServerRole,WebServer`` . Depending on the type of target, the maximum number of values for a key might be lower than the global maximum of 50.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                target_property = ssm_mixins.CfnAssociationPropsMixin.TargetProperty(
                    key="key",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6c839f6fd4381378868d2885eea7f45688dd0b110bbfbd7911e03354086737f)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''User-defined criteria for sending commands that target managed nodes that meet the criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-target.html#cfn-ssm-association-target-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''User-defined criteria that maps to ``Key`` .

            For example, if you specified ``tag:ServerRole`` , you could specify ``value:WebServer`` to run a command on instances that include EC2 tags of ``ServerRole,WebServer`` .

            Depending on the type of target, the maximum number of values for a key might be lower than the global maximum of 50.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-association-target.html#cfn-ssm-association-target-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnDocumentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attachments": "attachments",
        "content": "content",
        "document_format": "documentFormat",
        "document_type": "documentType",
        "name": "name",
        "requires": "requires",
        "tags": "tags",
        "target_type": "targetType",
        "update_method": "updateMethod",
        "version_name": "versionName",
    },
)
class CfnDocumentMixinProps:
    def __init__(
        self,
        *,
        attachments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDocumentPropsMixin.AttachmentsSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        content: typing.Any = None,
        document_format: typing.Optional[builtins.str] = None,
        document_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        requires: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDocumentPropsMixin.DocumentRequiresProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_type: typing.Optional[builtins.str] = None,
        update_method: typing.Optional[builtins.str] = None,
        version_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDocumentPropsMixin.

        :param attachments: A list of key-value pairs that describe attachments to a version of a document.
        :param content: The content for the new SSM document in JSON or YAML. For more information about the schemas for SSM document content, see `SSM document schema features and examples <https://docs.aws.amazon.com/systems-manager/latest/userguide/document-schemas-features.html>`_ in the *AWS Systems Manager User Guide* . .. epigraph:: This parameter also supports ``String`` data types.
        :param document_format: Specify the document format for the request. ``JSON`` is the default format. Default: - "JSON"
        :param document_type: The type of document to create.
        :param name: A name for the SSM document. .. epigraph:: You can't use the following strings as document name prefixes. These are reserved by AWS for use as document name prefixes: - ``aws`` - ``amazon`` - ``amzn`` - ``AWSEC2`` - ``AWSConfigRemediation`` - ``AWSSupport``
        :param requires: A list of SSM documents required by a document. This parameter is used exclusively by AWS AppConfig . When a user creates an AWS AppConfig configuration in an SSM document, the user must also specify a required document for validation purposes. In this case, an ``ApplicationConfiguration`` document requires an ``ApplicationConfigurationSchema`` document for validation purposes. For more information, see `What is AWS AppConfig ? <https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html>`_ in the *AWS AppConfig User Guide* .
        :param tags: AWS CloudFormation resource tags to apply to the document. Use tags to help you identify and categorize resources.
        :param target_type: Specify a target type to define the kinds of resources the document can run on. For example, to run a document on EC2 instances, specify the following value: ``/AWS::EC2::Instance`` . If you specify a value of '/' the document can run on all types of resources. If you don't specify a value, the document can't run on any resources. For a list of valid resource types, see `AWS resource and property types reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_ in the *AWS CloudFormation User Guide* .
        :param update_method: If the document resource you specify in your template already exists, this parameter determines whether a new version of the existing document is created, or the existing document is replaced. ``Replace`` is the default method. If you specify ``NewVersion`` for the ``UpdateMethod`` parameter, and the ``Name`` of the document does not match an existing resource, a new document is created. When you specify ``NewVersion`` , the default version of the document is changed to the newly created version. Default: - "Replace"
        :param version_name: An optional field specifying the version of the artifact you are creating with the document. For example, ``Release12.1`` . This value is unique across all versions of a document, and can't be changed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
            
            # content: Any
            
            cfn_document_mixin_props = ssm_mixins.CfnDocumentMixinProps(
                attachments=[ssm_mixins.CfnDocumentPropsMixin.AttachmentsSourceProperty(
                    key="key",
                    name="name",
                    values=["values"]
                )],
                content=content,
                document_format="documentFormat",
                document_type="documentType",
                name="name",
                requires=[ssm_mixins.CfnDocumentPropsMixin.DocumentRequiresProperty(
                    name="name",
                    version="version"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_type="targetType",
                update_method="updateMethod",
                version_name="versionName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b3156f6822f24d51787d10f3b2a4be3cc8c9db409872be40ce5330d060eb55)
            check_type(argname="argument attachments", value=attachments, expected_type=type_hints["attachments"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument document_format", value=document_format, expected_type=type_hints["document_format"])
            check_type(argname="argument document_type", value=document_type, expected_type=type_hints["document_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument requires", value=requires, expected_type=type_hints["requires"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
            check_type(argname="argument update_method", value=update_method, expected_type=type_hints["update_method"])
            check_type(argname="argument version_name", value=version_name, expected_type=type_hints["version_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attachments is not None:
            self._values["attachments"] = attachments
        if content is not None:
            self._values["content"] = content
        if document_format is not None:
            self._values["document_format"] = document_format
        if document_type is not None:
            self._values["document_type"] = document_type
        if name is not None:
            self._values["name"] = name
        if requires is not None:
            self._values["requires"] = requires
        if tags is not None:
            self._values["tags"] = tags
        if target_type is not None:
            self._values["target_type"] = target_type
        if update_method is not None:
            self._values["update_method"] = update_method
        if version_name is not None:
            self._values["version_name"] = version_name

    @builtins.property
    def attachments(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentPropsMixin.AttachmentsSourceProperty"]]]]:
        '''A list of key-value pairs that describe attachments to a version of a document.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-attachments
        '''
        result = self._values.get("attachments")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentPropsMixin.AttachmentsSourceProperty"]]]], result)

    @builtins.property
    def content(self) -> typing.Any:
        '''The content for the new SSM document in JSON or YAML.

        For more information about the schemas for SSM document content, see `SSM document schema features and examples <https://docs.aws.amazon.com/systems-manager/latest/userguide/document-schemas-features.html>`_ in the *AWS Systems Manager User Guide* .
        .. epigraph::

           This parameter also supports ``String`` data types.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Any, result)

    @builtins.property
    def document_format(self) -> typing.Optional[builtins.str]:
        '''Specify the document format for the request.

        ``JSON`` is the default format.

        :default: - "JSON"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-documentformat
        '''
        result = self._values.get("document_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_type(self) -> typing.Optional[builtins.str]:
        '''The type of document to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-documenttype
        '''
        result = self._values.get("document_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the SSM document.

        .. epigraph::

           You can't use the following strings as document name prefixes. These are reserved by AWS for use as document name prefixes:

           - ``aws``
           - ``amazon``
           - ``amzn``
           - ``AWSEC2``
           - ``AWSConfigRemediation``
           - ``AWSSupport``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requires(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentPropsMixin.DocumentRequiresProperty"]]]]:
        '''A list of SSM documents required by a document.

        This parameter is used exclusively by AWS AppConfig . When a user creates an AWS AppConfig configuration in an SSM document, the user must also specify a required document for validation purposes. In this case, an ``ApplicationConfiguration`` document requires an ``ApplicationConfigurationSchema`` document for validation purposes. For more information, see `What is AWS AppConfig ? <https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html>`_ in the *AWS AppConfig User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-requires
        '''
        result = self._values.get("requires")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDocumentPropsMixin.DocumentRequiresProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''AWS CloudFormation resource tags to apply to the document.

        Use tags to help you identify and categorize resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_type(self) -> typing.Optional[builtins.str]:
        '''Specify a target type to define the kinds of resources the document can run on.

        For example, to run a document on EC2 instances, specify the following value: ``/AWS::EC2::Instance`` . If you specify a value of '/' the document can run on all types of resources. If you don't specify a value, the document can't run on any resources. For a list of valid resource types, see `AWS resource and property types reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_ in the *AWS CloudFormation User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-targettype
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_method(self) -> typing.Optional[builtins.str]:
        '''If the document resource you specify in your template already exists, this parameter determines whether a new version of the existing document is created, or the existing document is replaced.

        ``Replace`` is the default method. If you specify ``NewVersion`` for the ``UpdateMethod`` parameter, and the ``Name`` of the document does not match an existing resource, a new document is created. When you specify ``NewVersion`` , the default version of the document is changed to the newly created version.

        :default: - "Replace"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-updatemethod
        '''
        result = self._values.get("update_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_name(self) -> typing.Optional[builtins.str]:
        '''An optional field specifying the version of the artifact you are creating with the document.

        For example, ``Release12.1`` . This value is unique across all versions of a document, and can't be changed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html#cfn-ssm-document-versionname
        '''
        result = self._values.get("version_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDocumentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDocumentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnDocumentPropsMixin",
):
    '''The ``AWS::SSM::Document`` resource creates a Systems Manager (SSM) document in AWS Systems Manager .

    This document defines the actions that Systems Manager performs on your AWS resources.
    .. epigraph::

       This resource does not support CloudFormation drift detection.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-document.html
    :cloudformationResource: AWS::SSM::Document
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
        
        # content: Any
        
        cfn_document_props_mixin = ssm_mixins.CfnDocumentPropsMixin(ssm_mixins.CfnDocumentMixinProps(
            attachments=[ssm_mixins.CfnDocumentPropsMixin.AttachmentsSourceProperty(
                key="key",
                name="name",
                values=["values"]
            )],
            content=content,
            document_format="documentFormat",
            document_type="documentType",
            name="name",
            requires=[ssm_mixins.CfnDocumentPropsMixin.DocumentRequiresProperty(
                name="name",
                version="version"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_type="targetType",
            update_method="updateMethod",
            version_name="versionName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDocumentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSM::Document``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328d0637df58f5d44d6a1d8ffa5ed10890456ce95a38ae4980b3b5778d492805)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3a6a0f764ee7002c98fb8289b6fd2320b122ea51d9dd5d75db7100fb29dc45e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6edb37bdd487b2b1fad069c510dab4731285e14c8a4c93a212a4de4c264c492)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDocumentMixinProps:
        return typing.cast(CfnDocumentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnDocumentPropsMixin.AttachmentsSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "name": "name", "values": "values"},
    )
    class AttachmentsSourceProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Identifying information about a document attachment, including the file name and a key-value pair that identifies the location of an attachment to a document.

            :param key: The key of a key-value pair that identifies the location of an attachment to a document.
            :param name: The name of the document attachment file.
            :param values: The value of a key-value pair that identifies the location of an attachment to a document. The format for *Value* depends on the type of key you specify. - For the key *SourceUrl* , the value is an S3 bucket location. For example: ``"Values": [ "s3://amzn-s3-demo-bucket/my-prefix" ]`` - For the key *S3FileUrl* , the value is a file in an S3 bucket. For example: ``"Values": [ "s3://amzn-s3-demo-bucket/my-prefix/my-file.py" ]`` - For the key *AttachmentReference* , the value is constructed from the name of another SSM document in your account, a version number of that document, and a file attached to that document version that you want to reuse. For example: ``"Values": [ "MyOtherDocument/3/my-other-file.py" ]`` However, if the SSM document is shared with you from another account, the full SSM document ARN must be specified instead of the document name only. For example: ``"Values": [ "arn:aws:ssm:us-east-2:111122223333:document/OtherAccountDocument/3/their-file.py" ]``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-document-attachmentssource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                attachments_source_property = ssm_mixins.CfnDocumentPropsMixin.AttachmentsSourceProperty(
                    key="key",
                    name="name",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__09a2953f7a288bd92d78b3535a6aacbd4beb84c23cef557d1b57b959f558ff63)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if name is not None:
                self._values["name"] = name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of a key-value pair that identifies the location of an attachment to a document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-document-attachmentssource.html#cfn-ssm-document-attachmentssource-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the document attachment file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-document-attachmentssource.html#cfn-ssm-document-attachmentssource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The value of a key-value pair that identifies the location of an attachment to a document.

            The format for *Value* depends on the type of key you specify.

            - For the key *SourceUrl* , the value is an S3 bucket location. For example:

            ``"Values": [ "s3://amzn-s3-demo-bucket/my-prefix" ]``

            - For the key *S3FileUrl* , the value is a file in an S3 bucket. For example:

            ``"Values": [ "s3://amzn-s3-demo-bucket/my-prefix/my-file.py" ]``

            - For the key *AttachmentReference* , the value is constructed from the name of another SSM document in your account, a version number of that document, and a file attached to that document version that you want to reuse. For example:

            ``"Values": [ "MyOtherDocument/3/my-other-file.py" ]``

            However, if the SSM document is shared with you from another account, the full SSM document ARN must be specified instead of the document name only. For example:

            ``"Values": [ "arn:aws:ssm:us-east-2:111122223333:document/OtherAccountDocument/3/their-file.py" ]``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-document-attachmentssource.html#cfn-ssm-document-attachmentssource-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttachmentsSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnDocumentPropsMixin.DocumentRequiresProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class DocumentRequiresProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An SSM document required by the current document.

            :param name: The name of the required SSM document. The name can be an Amazon Resource Name (ARN).
            :param version: The document version required by the current document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-document-documentrequires.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                document_requires_property = ssm_mixins.CfnDocumentPropsMixin.DocumentRequiresProperty(
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83dddb128ea59994df081c4a9f3bc414748bf47341a3564f06486c99d6131b60)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the required SSM document.

            The name can be an Amazon Resource Name (ARN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-document-documentrequires.html#cfn-ssm-document-documentrequires-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The document version required by the current document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-document-documentrequires.html#cfn-ssm-document-documentrequires-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentRequiresProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_unassociated_targets": "allowUnassociatedTargets",
        "cutoff": "cutoff",
        "description": "description",
        "duration": "duration",
        "end_date": "endDate",
        "name": "name",
        "schedule": "schedule",
        "schedule_offset": "scheduleOffset",
        "schedule_timezone": "scheduleTimezone",
        "start_date": "startDate",
        "tags": "tags",
    },
)
class CfnMaintenanceWindowMixinProps:
    def __init__(
        self,
        *,
        allow_unassociated_targets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        cutoff: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        duration: typing.Optional[jsii.Number] = None,
        end_date: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        schedule_offset: typing.Optional[jsii.Number] = None,
        schedule_timezone: typing.Optional[builtins.str] = None,
        start_date: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMaintenanceWindowPropsMixin.

        :param allow_unassociated_targets: Enables a maintenance window task to run on managed instances, even if you have not registered those instances as targets. If enabled, then you must specify the unregistered instances (by instance ID) when you register a task with the maintenance window.
        :param cutoff: The number of hours before the end of the maintenance window that AWS Systems Manager stops scheduling new tasks for execution.
        :param description: A description of the maintenance window.
        :param duration: The duration of the maintenance window in hours.
        :param end_date: The date and time, in ISO-8601 Extended format, for when the maintenance window is scheduled to become inactive.
        :param name: The name of the maintenance window.
        :param schedule: The schedule of the maintenance window in the form of a cron or rate expression.
        :param schedule_offset: The number of days to wait to run a maintenance window after the scheduled cron expression date and time.
        :param schedule_timezone: The time zone that the scheduled maintenance window executions are based on, in Internet Assigned Numbers Authority (IANA) format.
        :param start_date: The date and time, in ISO-8601 Extended format, for when the maintenance window is scheduled to become active. ``StartDate`` allows you to delay activation of the maintenance window until the specified future date.
        :param tags: Optional metadata that you assign to a resource in the form of an arbitrary set of tags (key-value pairs). Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a maintenance window to identify the type of tasks it will run, the types of targets, and the environment it will run in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
            
            cfn_maintenance_window_mixin_props = ssm_mixins.CfnMaintenanceWindowMixinProps(
                allow_unassociated_targets=False,
                cutoff=123,
                description="description",
                duration=123,
                end_date="endDate",
                name="name",
                schedule="schedule",
                schedule_offset=123,
                schedule_timezone="scheduleTimezone",
                start_date="startDate",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb00a90bb49285cb6cda21fa7f42015d755a7022319000416f09d2cbbb36229)
            check_type(argname="argument allow_unassociated_targets", value=allow_unassociated_targets, expected_type=type_hints["allow_unassociated_targets"])
            check_type(argname="argument cutoff", value=cutoff, expected_type=type_hints["cutoff"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument schedule_offset", value=schedule_offset, expected_type=type_hints["schedule_offset"])
            check_type(argname="argument schedule_timezone", value=schedule_timezone, expected_type=type_hints["schedule_timezone"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_unassociated_targets is not None:
            self._values["allow_unassociated_targets"] = allow_unassociated_targets
        if cutoff is not None:
            self._values["cutoff"] = cutoff
        if description is not None:
            self._values["description"] = description
        if duration is not None:
            self._values["duration"] = duration
        if end_date is not None:
            self._values["end_date"] = end_date
        if name is not None:
            self._values["name"] = name
        if schedule is not None:
            self._values["schedule"] = schedule
        if schedule_offset is not None:
            self._values["schedule_offset"] = schedule_offset
        if schedule_timezone is not None:
            self._values["schedule_timezone"] = schedule_timezone
        if start_date is not None:
            self._values["start_date"] = start_date
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allow_unassociated_targets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables a maintenance window task to run on managed instances, even if you have not registered those instances as targets.

        If enabled, then you must specify the unregistered instances (by instance ID) when you register a task with the maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-allowunassociatedtargets
        '''
        result = self._values.get("allow_unassociated_targets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def cutoff(self) -> typing.Optional[jsii.Number]:
        '''The number of hours before the end of the maintenance window that AWS Systems Manager stops scheduling new tasks for execution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-cutoff
        '''
        result = self._values.get("cutoff")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def duration(self) -> typing.Optional[jsii.Number]:
        '''The duration of the maintenance window in hours.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-duration
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end_date(self) -> typing.Optional[builtins.str]:
        '''The date and time, in ISO-8601 Extended format, for when the maintenance window is scheduled to become inactive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-enddate
        '''
        result = self._values.get("end_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''The schedule of the maintenance window in the form of a cron or rate expression.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_offset(self) -> typing.Optional[jsii.Number]:
        '''The number of days to wait to run a maintenance window after the scheduled cron expression date and time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-scheduleoffset
        '''
        result = self._values.get("schedule_offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule_timezone(self) -> typing.Optional[builtins.str]:
        '''The time zone that the scheduled maintenance window executions are based on, in Internet Assigned Numbers Authority (IANA) format.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-scheduletimezone
        '''
        result = self._values.get("schedule_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_date(self) -> typing.Optional[builtins.str]:
        '''The date and time, in ISO-8601 Extended format, for when the maintenance window is scheduled to become active.

        ``StartDate`` allows you to delay activation of the maintenance window until the specified future date.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-startdate
        '''
        result = self._values.get("start_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata that you assign to a resource in the form of an arbitrary set of tags (key-value pairs).

        Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a maintenance window to identify the type of tasks it will run, the types of targets, and the environment it will run in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html#cfn-ssm-maintenancewindow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMaintenanceWindowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMaintenanceWindowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowPropsMixin",
):
    '''The ``AWS::SSM::MaintenanceWindow`` resource represents general information about a maintenance window for AWS Systems Manager .

    Maintenance windows let you define a schedule for when to perform potentially disruptive actions on your instances, such as patching an operating system (OS), updating drivers, or installing software. Each maintenance window has a schedule, a duration, a set of registered targets, and a set of registered tasks.

    For more information, see `Systems Manager Maintenance Windows <https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-maintenance.html>`_ in the *AWS Systems Manager User Guide* and `CreateMaintenanceWindow <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_CreateMaintenanceWindow.html>`_ in the *AWS Systems Manager API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindow.html
    :cloudformationResource: AWS::SSM::MaintenanceWindow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
        
        cfn_maintenance_window_props_mixin = ssm_mixins.CfnMaintenanceWindowPropsMixin(ssm_mixins.CfnMaintenanceWindowMixinProps(
            allow_unassociated_targets=False,
            cutoff=123,
            description="description",
            duration=123,
            end_date="endDate",
            name="name",
            schedule="schedule",
            schedule_offset=123,
            schedule_timezone="scheduleTimezone",
            start_date="startDate",
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
        props: typing.Union[CfnMaintenanceWindowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSM::MaintenanceWindow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b878a6571d4bd09f090a8296169df5fcfa3c825c69d08d71e06e155e92e1237)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a81fa8c91cb74a1aba3c05a739ebb96e162072d3ff2bce9afb8c7bf5c3f9be93)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74269da83810d1a884979ab661d35b1710cf578f6f531cc8c0c0de540917d33b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMaintenanceWindowMixinProps:
        return typing.cast(CfnMaintenanceWindowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTargetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "owner_information": "ownerInformation",
        "resource_type": "resourceType",
        "targets": "targets",
        "window_id": "windowId",
    },
)
class CfnMaintenanceWindowTargetMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner_information: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTargetPropsMixin.TargetsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        window_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMaintenanceWindowTargetPropsMixin.

        :param description: A description for the target.
        :param name: The name for the maintenance window target.
        :param owner_information: A user-provided value that will be included in any Amazon CloudWatch Events events that are raised while running tasks for these targets in this maintenance window.
        :param resource_type: The type of target that is being registered with the maintenance window.
        :param targets: The targets to register with the maintenance window. In other words, the instances to run commands on when the maintenance window runs. You must specify targets by using the ``WindowTargetIds`` parameter.
        :param window_id: The ID of the maintenance window to register the target with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
            
            cfn_maintenance_window_target_mixin_props = ssm_mixins.CfnMaintenanceWindowTargetMixinProps(
                description="description",
                name="name",
                owner_information="ownerInformation",
                resource_type="resourceType",
                targets=[ssm_mixins.CfnMaintenanceWindowTargetPropsMixin.TargetsProperty(
                    key="key",
                    values=["values"]
                )],
                window_id="windowId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3bad47b3d001408f796cabaf23f89432c7922ade7eafedf8217cc812bdcddec)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner_information", value=owner_information, expected_type=type_hints["owner_information"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument window_id", value=window_id, expected_type=type_hints["window_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if owner_information is not None:
            self._values["owner_information"] = owner_information
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if targets is not None:
            self._values["targets"] = targets
        if window_id is not None:
            self._values["window_id"] = window_id

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the maintenance window target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_information(self) -> typing.Optional[builtins.str]:
        '''A user-provided value that will be included in any Amazon CloudWatch Events events that are raised while running tasks for these targets in this maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-ownerinformation
        '''
        result = self._values.get("owner_information")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The type of target that is being registered with the maintenance window.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTargetPropsMixin.TargetsProperty"]]]]:
        '''The targets to register with the maintenance window.

        In other words, the instances to run commands on when the maintenance window runs.

        You must specify targets by using the ``WindowTargetIds`` parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTargetPropsMixin.TargetsProperty"]]]], result)

    @builtins.property
    def window_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the maintenance window to register the target with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html#cfn-ssm-maintenancewindowtarget-windowid
        '''
        result = self._values.get("window_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMaintenanceWindowTargetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMaintenanceWindowTargetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTargetPropsMixin",
):
    '''The ``AWS::SSM::MaintenanceWindowTarget`` resource registers a target with a maintenance window for AWS Systems Manager .

    For more information, see `RegisterTargetWithMaintenanceWindow <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_RegisterTargetWithMaintenanceWindow.html>`_ in the *AWS Systems Manager API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html
    :cloudformationResource: AWS::SSM::MaintenanceWindowTarget
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
        
        cfn_maintenance_window_target_props_mixin = ssm_mixins.CfnMaintenanceWindowTargetPropsMixin(ssm_mixins.CfnMaintenanceWindowTargetMixinProps(
            description="description",
            name="name",
            owner_information="ownerInformation",
            resource_type="resourceType",
            targets=[ssm_mixins.CfnMaintenanceWindowTargetPropsMixin.TargetsProperty(
                key="key",
                values=["values"]
            )],
            window_id="windowId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMaintenanceWindowTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSM::MaintenanceWindowTarget``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e2d7e04e8085178df58e178e0af0f23afbdcb4b824a7f504898fc76572c4cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb9bbd4b6162bcdaab7436c660142881e6caead051024d3c8d8a1202594df9a7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94af1a6ee85b44c849e4202248da6b0be02916cb3132ba911a53f88d5f701f02)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMaintenanceWindowTargetMixinProps:
        return typing.cast(CfnMaintenanceWindowTargetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTargetPropsMixin.TargetsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class TargetsProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``Targets`` property type specifies adding a target to a maintenance window target in AWS Systems Manager .

            ``Targets`` is a property of the `AWS::SSM::MaintenanceWindowTarget <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtarget.html>`_ resource.

            :param key: User-defined criteria for sending commands that target managed nodes that meet the criteria.
            :param values: User-defined criteria that maps to ``Key`` . For example, if you specified ``tag:ServerRole`` , you could specify ``value:WebServer`` to run a command on instances that include EC2 tags of ``ServerRole,WebServer`` . Depending on the type of target, the maximum number of values for a key might be lower than the global maximum of 50.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtarget-targets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                targets_property = ssm_mixins.CfnMaintenanceWindowTargetPropsMixin.TargetsProperty(
                    key="key",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34aedd0978f76f8ba5595844e354384d81f6adf737b8d48e28b8ae7f06b258b8)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''User-defined criteria for sending commands that target managed nodes that meet the criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtarget-targets.html#cfn-ssm-maintenancewindowtarget-targets-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''User-defined criteria that maps to ``Key`` .

            For example, if you specified ``tag:ServerRole`` , you could specify ``value:WebServer`` to run a command on instances that include EC2 tags of ``ServerRole,WebServer`` .

            Depending on the type of target, the maximum number of values for a key might be lower than the global maximum of 50.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtarget-targets.html#cfn-ssm-maintenancewindowtarget-targets-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cutoff_behavior": "cutoffBehavior",
        "description": "description",
        "logging_info": "loggingInfo",
        "max_concurrency": "maxConcurrency",
        "max_errors": "maxErrors",
        "name": "name",
        "priority": "priority",
        "service_role_arn": "serviceRoleArn",
        "targets": "targets",
        "task_arn": "taskArn",
        "task_invocation_parameters": "taskInvocationParameters",
        "task_parameters": "taskParameters",
        "task_type": "taskType",
        "window_id": "windowId",
    },
)
class CfnMaintenanceWindowTaskMixinProps:
    def __init__(
        self,
        *,
        cutoff_behavior: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        logging_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTaskPropsMixin.LoggingInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        max_concurrency: typing.Optional[builtins.str] = None,
        max_errors: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTaskPropsMixin.TargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        task_arn: typing.Optional[builtins.str] = None,
        task_invocation_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTaskPropsMixin.TaskInvocationParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        task_parameters: typing.Any = None,
        task_type: typing.Optional[builtins.str] = None,
        window_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMaintenanceWindowTaskPropsMixin.

        :param cutoff_behavior: The specification for whether tasks should continue to run after the cutoff time specified in the maintenance windows is reached.
        :param description: A description of the task.
        :param logging_info: .. epigraph:: ``LoggingInfo`` has been deprecated. To specify an Amazon S3 bucket to contain logs for Run Command tasks, instead use the ``OutputS3BucketName`` and ``OutputS3KeyPrefix`` options in the ``TaskInvocationParameters`` structure. For information about how Systems Manager handles these options for the supported maintenance window task types, see `AWS ::SSM::MaintenanceWindowTask MaintenanceWindowRunCommandParameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html>`_ . Information about an Amazon S3 bucket to write Run Command task-level logs to.
        :param max_concurrency: The maximum number of targets this task can be run for, in parallel. .. epigraph:: Although this element is listed as "Required: No", a value can be omitted only when you are registering or updating a `targetless task <https://docs.aws.amazon.com/systems-manager/latest/userguide/maintenance-windows-targetless-tasks.html>`_ You must provide a value in all other cases. For maintenance window tasks without a target specified, you can't supply a value for this option. Instead, the system inserts a placeholder value of ``1`` . This value doesn't affect the running of your task.
        :param max_errors: The maximum number of errors allowed before this task stops being scheduled. .. epigraph:: Although this element is listed as "Required: No", a value can be omitted only when you are registering or updating a `targetless task <https://docs.aws.amazon.com/systems-manager/latest/userguide/maintenance-windows-targetless-tasks.html>`_ You must provide a value in all other cases. For maintenance window tasks without a target specified, you can't supply a value for this option. Instead, the system inserts a placeholder value of ``1`` . This value doesn't affect the running of your task.
        :param name: The task name.
        :param priority: The priority of the task in the maintenance window. The lower the number, the higher the priority. Tasks that have the same priority are scheduled in parallel.
        :param service_role_arn: The Amazon Resource Name (ARN) of the IAM service role for AWS Systems Manager to assume when running a maintenance window task. If you do not specify a service role ARN, Systems Manager uses a service-linked role in your account. If no appropriate service-linked role for Systems Manager exists in your account, it is created when you run ``RegisterTaskWithMaintenanceWindow`` . However, for an improved security posture, we strongly recommend creating a custom policy and custom service role for running your maintenance window tasks. The policy can be crafted to provide only the permissions needed for your particular maintenance window tasks. For more information, see `Setting up Maintenance Windows <https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-maintenance-permissions.html>`_ in the in the *AWS Systems Manager User Guide* .
        :param targets: The targets, either instances or window target IDs. - Specify instances using ``Key=InstanceIds,Values= *instanceid1* , *instanceid2*`` . - Specify window target IDs using ``Key=WindowTargetIds,Values= *window-target-id-1* , *window-target-id-2*`` .
        :param task_arn: The resource that the task uses during execution. For ``RUN_COMMAND`` and ``AUTOMATION`` task types, ``TaskArn`` is the SSM document name or Amazon Resource Name (ARN). For ``LAMBDA`` tasks, ``TaskArn`` is the function name or ARN. For ``STEP_FUNCTIONS`` tasks, ``TaskArn`` is the state machine ARN.
        :param task_invocation_parameters: The parameters to pass to the task when it runs. Populate only the fields that match the task type. All other fields should be empty. .. epigraph:: When you update a maintenance window task that has options specified in ``TaskInvocationParameters`` , you must provide again all the ``TaskInvocationParameters`` values that you want to retain. The values you do not specify again are removed. For example, suppose that when you registered a Run Command task, you specified ``TaskInvocationParameters`` values for ``Comment`` , ``NotificationConfig`` , and ``OutputS3BucketName`` . If you update the maintenance window task and specify only a different ``OutputS3BucketName`` value, the values for ``Comment`` and ``NotificationConfig`` are removed.
        :param task_parameters: .. epigraph:: ``TaskParameters`` has been deprecated. To specify parameters to pass to a task when it runs, instead use the ``Parameters`` option in the ``TaskInvocationParameters`` structure. For information about how Systems Manager handles these options for the supported maintenance window task types, see `MaintenanceWindowTaskInvocationParameters <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_MaintenanceWindowTaskInvocationParameters.html>`_ . The parameters to pass to the task when it runs.
        :param task_type: The type of task. Valid values: ``RUN_COMMAND`` , ``AUTOMATION`` , ``LAMBDA`` , ``STEP_FUNCTIONS`` .
        :param window_id: The ID of the maintenance window where the task is registered.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
            
            # parameters: Any
            # task_parameters: Any
            
            cfn_maintenance_window_task_mixin_props = ssm_mixins.CfnMaintenanceWindowTaskMixinProps(
                cutoff_behavior="cutoffBehavior",
                description="description",
                logging_info=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.LoggingInfoProperty(
                    region="region",
                    s3_bucket="s3Bucket",
                    s3_prefix="s3Prefix"
                ),
                max_concurrency="maxConcurrency",
                max_errors="maxErrors",
                name="name",
                priority=123,
                service_role_arn="serviceRoleArn",
                targets=[ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.TargetProperty(
                    key="key",
                    values=["values"]
                )],
                task_arn="taskArn",
                task_invocation_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.TaskInvocationParametersProperty(
                    maintenance_window_automation_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowAutomationParametersProperty(
                        document_version="documentVersion",
                        parameters=parameters
                    ),
                    maintenance_window_lambda_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowLambdaParametersProperty(
                        client_context="clientContext",
                        payload="payload",
                        qualifier="qualifier"
                    ),
                    maintenance_window_run_command_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowRunCommandParametersProperty(
                        cloud_watch_output_config=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty(
                            cloud_watch_log_group_name="cloudWatchLogGroupName",
                            cloud_watch_output_enabled=False
                        ),
                        comment="comment",
                        document_hash="documentHash",
                        document_hash_type="documentHashType",
                        document_version="documentVersion",
                        notification_config=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty(
                            notification_arn="notificationArn",
                            notification_events=["notificationEvents"],
                            notification_type="notificationType"
                        ),
                        output_s3_bucket_name="outputS3BucketName",
                        output_s3_key_prefix="outputS3KeyPrefix",
                        parameters=parameters,
                        service_role_arn="serviceRoleArn",
                        timeout_seconds=123
                    ),
                    maintenance_window_step_functions_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowStepFunctionsParametersProperty(
                        input="input",
                        name="name"
                    )
                ),
                task_parameters=task_parameters,
                task_type="taskType",
                window_id="windowId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a02d9ae989a99922d8c20aa70332bbca5a3b6bae8fcbd4e51bb00ad049d6c91)
            check_type(argname="argument cutoff_behavior", value=cutoff_behavior, expected_type=type_hints["cutoff_behavior"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument logging_info", value=logging_info, expected_type=type_hints["logging_info"])
            check_type(argname="argument max_concurrency", value=max_concurrency, expected_type=type_hints["max_concurrency"])
            check_type(argname="argument max_errors", value=max_errors, expected_type=type_hints["max_errors"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument task_arn", value=task_arn, expected_type=type_hints["task_arn"])
            check_type(argname="argument task_invocation_parameters", value=task_invocation_parameters, expected_type=type_hints["task_invocation_parameters"])
            check_type(argname="argument task_parameters", value=task_parameters, expected_type=type_hints["task_parameters"])
            check_type(argname="argument task_type", value=task_type, expected_type=type_hints["task_type"])
            check_type(argname="argument window_id", value=window_id, expected_type=type_hints["window_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cutoff_behavior is not None:
            self._values["cutoff_behavior"] = cutoff_behavior
        if description is not None:
            self._values["description"] = description
        if logging_info is not None:
            self._values["logging_info"] = logging_info
        if max_concurrency is not None:
            self._values["max_concurrency"] = max_concurrency
        if max_errors is not None:
            self._values["max_errors"] = max_errors
        if name is not None:
            self._values["name"] = name
        if priority is not None:
            self._values["priority"] = priority
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn
        if targets is not None:
            self._values["targets"] = targets
        if task_arn is not None:
            self._values["task_arn"] = task_arn
        if task_invocation_parameters is not None:
            self._values["task_invocation_parameters"] = task_invocation_parameters
        if task_parameters is not None:
            self._values["task_parameters"] = task_parameters
        if task_type is not None:
            self._values["task_type"] = task_type
        if window_id is not None:
            self._values["window_id"] = window_id

    @builtins.property
    def cutoff_behavior(self) -> typing.Optional[builtins.str]:
        '''The specification for whether tasks should continue to run after the cutoff time specified in the maintenance windows is reached.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-cutoffbehavior
        '''
        result = self._values.get("cutoff_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.LoggingInfoProperty"]]:
        '''.. epigraph::

   ``LoggingInfo`` has been deprecated.

        To specify an Amazon S3 bucket to contain logs for Run Command tasks, instead use the ``OutputS3BucketName`` and ``OutputS3KeyPrefix`` options in the ``TaskInvocationParameters`` structure. For information about how Systems Manager handles these options for the supported maintenance window task types, see `AWS ::SSM::MaintenanceWindowTask MaintenanceWindowRunCommandParameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html>`_ .

        Information about an Amazon S3 bucket to write Run Command task-level logs to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-logginginfo
        '''
        result = self._values.get("logging_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.LoggingInfoProperty"]], result)

    @builtins.property
    def max_concurrency(self) -> typing.Optional[builtins.str]:
        '''The maximum number of targets this task can be run for, in parallel.

        .. epigraph::

           Although this element is listed as "Required: No", a value can be omitted only when you are registering or updating a `targetless task <https://docs.aws.amazon.com/systems-manager/latest/userguide/maintenance-windows-targetless-tasks.html>`_ You must provide a value in all other cases.

           For maintenance window tasks without a target specified, you can't supply a value for this option. Instead, the system inserts a placeholder value of ``1`` . This value doesn't affect the running of your task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-maxconcurrency
        '''
        result = self._values.get("max_concurrency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_errors(self) -> typing.Optional[builtins.str]:
        '''The maximum number of errors allowed before this task stops being scheduled.

        .. epigraph::

           Although this element is listed as "Required: No", a value can be omitted only when you are registering or updating a `targetless task <https://docs.aws.amazon.com/systems-manager/latest/userguide/maintenance-windows-targetless-tasks.html>`_ You must provide a value in all other cases.

           For maintenance window tasks without a target specified, you can't supply a value for this option. Instead, the system inserts a placeholder value of ``1`` . This value doesn't affect the running of your task.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-maxerrors
        '''
        result = self._values.get("max_errors")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The task name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of the task in the maintenance window.

        The lower the number, the higher the priority. Tasks that have the same priority are scheduled in parallel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM service role for AWS Systems Manager to assume when running a maintenance window task.

        If you do not specify a service role ARN, Systems Manager uses a service-linked role in your account. If no appropriate service-linked role for Systems Manager exists in your account, it is created when you run ``RegisterTaskWithMaintenanceWindow`` .

        However, for an improved security posture, we strongly recommend creating a custom policy and custom service role for running your maintenance window tasks. The policy can be crafted to provide only the permissions needed for your particular maintenance window tasks. For more information, see `Setting up Maintenance Windows <https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-maintenance-permissions.html>`_ in the in the *AWS Systems Manager User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-servicerolearn
        '''
        result = self._values.get("service_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.TargetProperty"]]]]:
        '''The targets, either instances or window target IDs.

        - Specify instances using ``Key=InstanceIds,Values= *instanceid1* , *instanceid2*`` .
        - Specify window target IDs using ``Key=WindowTargetIds,Values= *window-target-id-1* , *window-target-id-2*`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.TargetProperty"]]]], result)

    @builtins.property
    def task_arn(self) -> typing.Optional[builtins.str]:
        '''The resource that the task uses during execution.

        For ``RUN_COMMAND`` and ``AUTOMATION`` task types, ``TaskArn`` is the SSM document name or Amazon Resource Name (ARN).

        For ``LAMBDA`` tasks, ``TaskArn`` is the function name or ARN.

        For ``STEP_FUNCTIONS`` tasks, ``TaskArn`` is the state machine ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-taskarn
        '''
        result = self._values.get("task_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_invocation_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.TaskInvocationParametersProperty"]]:
        '''The parameters to pass to the task when it runs.

        Populate only the fields that match the task type. All other fields should be empty.
        .. epigraph::

           When you update a maintenance window task that has options specified in ``TaskInvocationParameters`` , you must provide again all the ``TaskInvocationParameters`` values that you want to retain. The values you do not specify again are removed. For example, suppose that when you registered a Run Command task, you specified ``TaskInvocationParameters`` values for ``Comment`` , ``NotificationConfig`` , and ``OutputS3BucketName`` . If you update the maintenance window task and specify only a different ``OutputS3BucketName`` value, the values for ``Comment`` and ``NotificationConfig`` are removed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters
        '''
        result = self._values.get("task_invocation_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.TaskInvocationParametersProperty"]], result)

    @builtins.property
    def task_parameters(self) -> typing.Any:
        '''.. epigraph::

   ``TaskParameters`` has been deprecated.

        To specify parameters to pass to a task when it runs, instead use the ``Parameters`` option in the ``TaskInvocationParameters`` structure. For information about how Systems Manager handles these options for the supported maintenance window task types, see `MaintenanceWindowTaskInvocationParameters <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_MaintenanceWindowTaskInvocationParameters.html>`_ .

        The parameters to pass to the task when it runs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-taskparameters
        '''
        result = self._values.get("task_parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def task_type(self) -> typing.Optional[builtins.str]:
        '''The type of task.

        Valid values: ``RUN_COMMAND`` , ``AUTOMATION`` , ``LAMBDA`` , ``STEP_FUNCTIONS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-tasktype
        '''
        result = self._values.get("task_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def window_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the maintenance window where the task is registered.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#cfn-ssm-maintenancewindowtask-windowid
        '''
        result = self._values.get("window_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMaintenanceWindowTaskMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMaintenanceWindowTaskPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin",
):
    '''The ``AWS::SSM::MaintenanceWindowTask`` resource defines information about a task for an AWS Systems Manager maintenance window.

    For more information, see `RegisterTaskWithMaintenanceWindow <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_RegisterTaskWithMaintenanceWindow.html>`_ in the *AWS Systems Manager API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html
    :cloudformationResource: AWS::SSM::MaintenanceWindowTask
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
        
        # parameters: Any
        # task_parameters: Any
        
        cfn_maintenance_window_task_props_mixin = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin(ssm_mixins.CfnMaintenanceWindowTaskMixinProps(
            cutoff_behavior="cutoffBehavior",
            description="description",
            logging_info=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.LoggingInfoProperty(
                region="region",
                s3_bucket="s3Bucket",
                s3_prefix="s3Prefix"
            ),
            max_concurrency="maxConcurrency",
            max_errors="maxErrors",
            name="name",
            priority=123,
            service_role_arn="serviceRoleArn",
            targets=[ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.TargetProperty(
                key="key",
                values=["values"]
            )],
            task_arn="taskArn",
            task_invocation_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.TaskInvocationParametersProperty(
                maintenance_window_automation_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowAutomationParametersProperty(
                    document_version="documentVersion",
                    parameters=parameters
                ),
                maintenance_window_lambda_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowLambdaParametersProperty(
                    client_context="clientContext",
                    payload="payload",
                    qualifier="qualifier"
                ),
                maintenance_window_run_command_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowRunCommandParametersProperty(
                    cloud_watch_output_config=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty(
                        cloud_watch_log_group_name="cloudWatchLogGroupName",
                        cloud_watch_output_enabled=False
                    ),
                    comment="comment",
                    document_hash="documentHash",
                    document_hash_type="documentHashType",
                    document_version="documentVersion",
                    notification_config=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty(
                        notification_arn="notificationArn",
                        notification_events=["notificationEvents"],
                        notification_type="notificationType"
                    ),
                    output_s3_bucket_name="outputS3BucketName",
                    output_s3_key_prefix="outputS3KeyPrefix",
                    parameters=parameters,
                    service_role_arn="serviceRoleArn",
                    timeout_seconds=123
                ),
                maintenance_window_step_functions_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowStepFunctionsParametersProperty(
                    input="input",
                    name="name"
                )
            ),
            task_parameters=task_parameters,
            task_type="taskType",
            window_id="windowId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMaintenanceWindowTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSM::MaintenanceWindowTask``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ddcb054f72d1febc2d453c908c26ba0846b9857386d8e1586accedb12455033)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f9024c9bbb127b6f07670ea32fa31988cfd9b8a6c40525e994b0e33cd89598d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08862be412f7046aea50da93885dd2df69cd4d1139484a3f2720edaf823b56b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMaintenanceWindowTaskMixinProps:
        return typing.cast(CfnMaintenanceWindowTaskMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_log_group_name": "cloudWatchLogGroupName",
            "cloud_watch_output_enabled": "cloudWatchOutputEnabled",
        },
    )
    class CloudWatchOutputConfigProperty:
        def __init__(
            self,
            *,
            cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
            cloud_watch_output_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Configuration options for sending command output to Amazon CloudWatch Logs.

            :param cloud_watch_log_group_name: The name of the CloudWatch Logs log group where you want to send command output. If you don't specify a group name, AWS Systems Manager automatically creates a log group for you. The log group uses the following naming format: ``aws/ssm/ *SystemsManagerDocumentName*``
            :param cloud_watch_output_enabled: Enables Systems Manager to send command output to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-cloudwatchoutputconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                cloud_watch_output_config_property = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty(
                    cloud_watch_log_group_name="cloudWatchLogGroupName",
                    cloud_watch_output_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__deb9f5882685186ebc9c2608126233a577b2ff3c64db1c2a063d9e612f4583d4)
                check_type(argname="argument cloud_watch_log_group_name", value=cloud_watch_log_group_name, expected_type=type_hints["cloud_watch_log_group_name"])
                check_type(argname="argument cloud_watch_output_enabled", value=cloud_watch_output_enabled, expected_type=type_hints["cloud_watch_output_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_log_group_name is not None:
                self._values["cloud_watch_log_group_name"] = cloud_watch_log_group_name
            if cloud_watch_output_enabled is not None:
                self._values["cloud_watch_output_enabled"] = cloud_watch_output_enabled

        @builtins.property
        def cloud_watch_log_group_name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch Logs log group where you want to send command output.

            If you don't specify a group name, AWS Systems Manager automatically creates a log group for you. The log group uses the following naming format:

            ``aws/ssm/ *SystemsManagerDocumentName*``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-cloudwatchoutputconfig.html#cfn-ssm-maintenancewindowtask-cloudwatchoutputconfig-cloudwatchloggroupname
            '''
            result = self._values.get("cloud_watch_log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cloud_watch_output_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables Systems Manager to send command output to CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-cloudwatchoutputconfig.html#cfn-ssm-maintenancewindowtask-cloudwatchoutputconfig-cloudwatchoutputenabled
            '''
            result = self._values.get("cloud_watch_output_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchOutputConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin.LoggingInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "region": "region",
            "s3_bucket": "s3Bucket",
            "s3_prefix": "s3Prefix",
        },
    )
    class LoggingInfoProperty:
        def __init__(
            self,
            *,
            region: typing.Optional[builtins.str] = None,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   ``LoggingInfo`` has been deprecated.

            To specify an Amazon S3 bucket to contain logs, instead use the ``OutputS3BucketName`` and ``OutputS3KeyPrefix`` options in the ``TaskInvocationParameters`` structure. For information about how Systems Manager handles these options for the supported maintenance window task types, see `AWS ::SSM::MaintenanceWindowTask MaintenanceWindowRunCommandParameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html>`_ .

            The ``LoggingInfo`` property type specifies information about the Amazon S3 bucket to write instance-level logs to.

            ``LoggingInfo`` is a property of the `AWS::SSM::MaintenanceWindowTask <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html>`_ resource.

            :param region: The AWS Region where the S3 bucket is located.
            :param s3_bucket: The name of an S3 bucket where execution logs are stored.
            :param s3_prefix: The Amazon S3 bucket subfolder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-logginginfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                logging_info_property = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.LoggingInfoProperty(
                    region="region",
                    s3_bucket="s3Bucket",
                    s3_prefix="s3Prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce31eccd03df75ed4002dcc39662ab329ff3888e9154f1ce73263a7736e91ce1)
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if region is not None:
                self._values["region"] = region
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_prefix is not None:
                self._values["s3_prefix"] = s3_prefix

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region where the S3 bucket is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-logginginfo.html#cfn-ssm-maintenancewindowtask-logginginfo-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The name of an S3 bucket where execution logs are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-logginginfo.html#cfn-ssm-maintenancewindowtask-logginginfo-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_prefix(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket subfolder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-logginginfo.html#cfn-ssm-maintenancewindowtask-logginginfo-s3prefix
            '''
            result = self._values.get("s3_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowAutomationParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_version": "documentVersion",
            "parameters": "parameters",
        },
    )
    class MaintenanceWindowAutomationParametersProperty:
        def __init__(
            self,
            *,
            document_version: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
        ) -> None:
            '''The ``MaintenanceWindowAutomationParameters`` property type specifies the parameters for an ``AUTOMATION`` task type for a maintenance window task in AWS Systems Manager .

            ``MaintenanceWindowAutomationParameters`` is a property of the `TaskInvocationParameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html>`_ property type.

            For information about available parameters in Automation runbooks, you can view the content of the runbook itself in the Systems Manager console. For information, see `View runbook content <https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-documents-reference-details.html#view-automation-json>`_ in the *AWS Systems Manager User Guide* .

            :param document_version: The version of an Automation runbook to use during task execution.
            :param parameters: The parameters for the ``AUTOMATION`` type task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowautomationparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                # parameters: Any
                
                maintenance_window_automation_parameters_property = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowAutomationParametersProperty(
                    document_version="documentVersion",
                    parameters=parameters
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95ce5abb429327c99b22c0ea934b12796ab62f9c8f3dd7b5dad9286053fbbfa3)
                check_type(argname="argument document_version", value=document_version, expected_type=type_hints["document_version"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_version is not None:
                self._values["document_version"] = document_version
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def document_version(self) -> typing.Optional[builtins.str]:
            '''The version of an Automation runbook to use during task execution.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowautomationparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowautomationparameters-documentversion
            '''
            result = self._values.get("document_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''The parameters for the ``AUTOMATION`` type task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowautomationparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowautomationparameters-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowAutomationParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowLambdaParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_context": "clientContext",
            "payload": "payload",
            "qualifier": "qualifier",
        },
    )
    class MaintenanceWindowLambdaParametersProperty:
        def __init__(
            self,
            *,
            client_context: typing.Optional[builtins.str] = None,
            payload: typing.Optional[builtins.str] = None,
            qualifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``MaintenanceWindowLambdaParameters`` property type specifies the parameters for a ``LAMBDA`` task type for a maintenance window task in AWS Systems Manager .

            ``MaintenanceWindowLambdaParameters`` is a property of the `TaskInvocationParameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html>`_ property type.

            :param client_context: Client-specific information to pass to the AWS Lambda function that you're invoking. You can then use the ``context`` variable to process the client information in your AWS Lambda function.
            :param payload: JSON to provide to your AWS Lambda function as input. .. epigraph:: Although ``Type`` is listed as "String" for this property, the payload content must be formatted as a Base64-encoded binary data object. *Length Constraint:* 4096
            :param qualifier: An AWS Lambda function version or alias name. If you specify a function version, the action uses the qualified function Amazon Resource Name (ARN) to invoke a specific Lambda function. If you specify an alias name, the action uses the alias ARN to invoke the Lambda function version that the alias points to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowlambdaparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                maintenance_window_lambda_parameters_property = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowLambdaParametersProperty(
                    client_context="clientContext",
                    payload="payload",
                    qualifier="qualifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a2cca521862d2c2ff42dcf494a3a5f795a9347ca061cc8b9fcb98b02912b572)
                check_type(argname="argument client_context", value=client_context, expected_type=type_hints["client_context"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_context is not None:
                self._values["client_context"] = client_context
            if payload is not None:
                self._values["payload"] = payload
            if qualifier is not None:
                self._values["qualifier"] = qualifier

        @builtins.property
        def client_context(self) -> typing.Optional[builtins.str]:
            '''Client-specific information to pass to the AWS Lambda function that you're invoking.

            You can then use the ``context`` variable to process the client information in your AWS Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowlambdaparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowlambdaparameters-clientcontext
            '''
            result = self._values.get("client_context")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(self) -> typing.Optional[builtins.str]:
            '''JSON to provide to your AWS Lambda function as input.

            .. epigraph::

               Although ``Type`` is listed as "String" for this property, the payload content must be formatted as a Base64-encoded binary data object.

            *Length Constraint:* 4096

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowlambdaparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowlambdaparameters-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def qualifier(self) -> typing.Optional[builtins.str]:
            '''An AWS Lambda function version or alias name.

            If you specify a function version, the action uses the qualified function Amazon Resource Name (ARN) to invoke a specific Lambda function. If you specify an alias name, the action uses the alias ARN to invoke the Lambda function version that the alias points to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowlambdaparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowlambdaparameters-qualifier
            '''
            result = self._values.get("qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowLambdaParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowRunCommandParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_output_config": "cloudWatchOutputConfig",
            "comment": "comment",
            "document_hash": "documentHash",
            "document_hash_type": "documentHashType",
            "document_version": "documentVersion",
            "notification_config": "notificationConfig",
            "output_s3_bucket_name": "outputS3BucketName",
            "output_s3_key_prefix": "outputS3KeyPrefix",
            "parameters": "parameters",
            "service_role_arn": "serviceRoleArn",
            "timeout_seconds": "timeoutSeconds",
        },
    )
    class MaintenanceWindowRunCommandParametersProperty:
        def __init__(
            self,
            *,
            cloud_watch_output_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            comment: typing.Optional[builtins.str] = None,
            document_hash: typing.Optional[builtins.str] = None,
            document_hash_type: typing.Optional[builtins.str] = None,
            document_version: typing.Optional[builtins.str] = None,
            notification_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            output_s3_bucket_name: typing.Optional[builtins.str] = None,
            output_s3_key_prefix: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
            service_role_arn: typing.Optional[builtins.str] = None,
            timeout_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ``MaintenanceWindowRunCommandParameters`` property type specifies the parameters for a ``RUN_COMMAND`` task type for a maintenance window task in AWS Systems Manager .

            This means that these parameters are the same as those for the ``SendCommand`` API call. For more information about ``SendCommand`` parameters, see `SendCommand <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_SendCommand.html>`_ in the *AWS Systems Manager API Reference* .

            For information about available parameters in SSM Command documents, you can view the content of the document itself in the Systems Manager console. For information, see `Viewing SSM command document content <https://docs.aws.amazon.com/systems-manager/latest/userguide/viewing-ssm-document-content.html>`_ in the *AWS Systems Manager User Guide* .

            ``MaintenanceWindowRunCommandParameters`` is a property of the `TaskInvocationParameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html>`_ property type.

            :param cloud_watch_output_config: Configuration options for sending command output to Amazon CloudWatch Logs.
            :param comment: Information about the command or commands to run.
            :param document_hash: The SHA-256 or SHA-1 hash created by the system when the document was created. SHA-1 hashes have been deprecated.
            :param document_hash_type: The SHA-256 or SHA-1 hash type. SHA-1 hashes are deprecated.
            :param document_version: The AWS Systems Manager document (SSM document) version to use in the request. You can specify ``$DEFAULT`` , ``$LATEST`` , or a specific version number. If you run commands by using the AWS CLI, then you must escape the first two options by using a backslash. If you specify a version number, then you don't need to use the backslash. For example: ``--document-version "\\$DEFAULT"`` ``--document-version "\\$LATEST"`` ``--document-version "3"``
            :param notification_config: Configurations for sending notifications about command status changes on a per-managed node basis.
            :param output_s3_bucket_name: The name of the Amazon Simple Storage Service (Amazon S3) bucket.
            :param output_s3_key_prefix: The S3 bucket subfolder.
            :param parameters: The parameters for the ``RUN_COMMAND`` task execution. The supported parameters are the same as those for the ``SendCommand`` API call. For more information, see `SendCommand <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_SendCommand.html>`_ in the *AWS Systems Manager API Reference* .
            :param service_role_arn: The Amazon Resource Name (ARN) of the IAM service role for AWS Systems Manager to assume when running a maintenance window task. If you do not specify a service role ARN, Systems Manager uses a service-linked role in your account. If no appropriate service-linked role for Systems Manager exists in your account, it is created when you run ``RegisterTaskWithMaintenanceWindow`` . However, for an improved security posture, we strongly recommend creating a custom policy and custom service role for running your maintenance window tasks. The policy can be crafted to provide only the permissions needed for your particular maintenance window tasks. For more information, see `Setting up Maintenance Windows <https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-maintenance-permissions.html>`_ in the in the *AWS Systems Manager User Guide* .
            :param timeout_seconds: If this time is reached and the command hasn't already started running, it doesn't run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                # parameters: Any
                
                maintenance_window_run_command_parameters_property = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowRunCommandParametersProperty(
                    cloud_watch_output_config=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty(
                        cloud_watch_log_group_name="cloudWatchLogGroupName",
                        cloud_watch_output_enabled=False
                    ),
                    comment="comment",
                    document_hash="documentHash",
                    document_hash_type="documentHashType",
                    document_version="documentVersion",
                    notification_config=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty(
                        notification_arn="notificationArn",
                        notification_events=["notificationEvents"],
                        notification_type="notificationType"
                    ),
                    output_s3_bucket_name="outputS3BucketName",
                    output_s3_key_prefix="outputS3KeyPrefix",
                    parameters=parameters,
                    service_role_arn="serviceRoleArn",
                    timeout_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95cf7ce26230c6225059e32b81aaa0a600c0f84124bff555b3b1b7ae4b3e3ed8)
                check_type(argname="argument cloud_watch_output_config", value=cloud_watch_output_config, expected_type=type_hints["cloud_watch_output_config"])
                check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
                check_type(argname="argument document_hash", value=document_hash, expected_type=type_hints["document_hash"])
                check_type(argname="argument document_hash_type", value=document_hash_type, expected_type=type_hints["document_hash_type"])
                check_type(argname="argument document_version", value=document_version, expected_type=type_hints["document_version"])
                check_type(argname="argument notification_config", value=notification_config, expected_type=type_hints["notification_config"])
                check_type(argname="argument output_s3_bucket_name", value=output_s3_bucket_name, expected_type=type_hints["output_s3_bucket_name"])
                check_type(argname="argument output_s3_key_prefix", value=output_s3_key_prefix, expected_type=type_hints["output_s3_key_prefix"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
                check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_output_config is not None:
                self._values["cloud_watch_output_config"] = cloud_watch_output_config
            if comment is not None:
                self._values["comment"] = comment
            if document_hash is not None:
                self._values["document_hash"] = document_hash
            if document_hash_type is not None:
                self._values["document_hash_type"] = document_hash_type
            if document_version is not None:
                self._values["document_version"] = document_version
            if notification_config is not None:
                self._values["notification_config"] = notification_config
            if output_s3_bucket_name is not None:
                self._values["output_s3_bucket_name"] = output_s3_bucket_name
            if output_s3_key_prefix is not None:
                self._values["output_s3_key_prefix"] = output_s3_key_prefix
            if parameters is not None:
                self._values["parameters"] = parameters
            if service_role_arn is not None:
                self._values["service_role_arn"] = service_role_arn
            if timeout_seconds is not None:
                self._values["timeout_seconds"] = timeout_seconds

        @builtins.property
        def cloud_watch_output_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty"]]:
            '''Configuration options for sending command output to Amazon CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-cloudwatchoutputconfig
            '''
            result = self._values.get("cloud_watch_output_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty"]], result)

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            '''Information about the command or commands to run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-comment
            '''
            result = self._values.get("comment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_hash(self) -> typing.Optional[builtins.str]:
            '''The SHA-256 or SHA-1 hash created by the system when the document was created.

            SHA-1 hashes have been deprecated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-documenthash
            '''
            result = self._values.get("document_hash")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_hash_type(self) -> typing.Optional[builtins.str]:
            '''The SHA-256 or SHA-1 hash type.

            SHA-1 hashes are deprecated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-documenthashtype
            '''
            result = self._values.get("document_hash_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_version(self) -> typing.Optional[builtins.str]:
            '''The AWS Systems Manager document (SSM document) version to use in the request.

            You can specify ``$DEFAULT`` , ``$LATEST`` , or a specific version number. If you run commands by using the AWS CLI, then you must escape the first two options by using a backslash. If you specify a version number, then you don't need to use the backslash. For example:

            ``--document-version "\\$DEFAULT"``

            ``--document-version "\\$LATEST"``

            ``--document-version "3"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-documentversion
            '''
            result = self._values.get("document_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty"]]:
            '''Configurations for sending notifications about command status changes on a per-managed node basis.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-notificationconfig
            '''
            result = self._values.get("notification_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty"]], result)

        @builtins.property
        def output_s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon Simple Storage Service (Amazon S3) bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-outputs3bucketname
            '''
            result = self._values.get("output_s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_s3_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket subfolder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-outputs3keyprefix
            '''
            result = self._values.get("output_s3_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''The parameters for the ``RUN_COMMAND`` task execution.

            The supported parameters are the same as those for the ``SendCommand`` API call. For more information, see `SendCommand <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_SendCommand.html>`_ in the *AWS Systems Manager API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def service_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM service role for AWS Systems Manager to assume when running a maintenance window task.

            If you do not specify a service role ARN, Systems Manager uses a service-linked role in your account. If no appropriate service-linked role for Systems Manager exists in your account, it is created when you run ``RegisterTaskWithMaintenanceWindow`` .

            However, for an improved security posture, we strongly recommend creating a custom policy and custom service role for running your maintenance window tasks. The policy can be crafted to provide only the permissions needed for your particular maintenance window tasks. For more information, see `Setting up Maintenance Windows <https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-maintenance-permissions.html>`_ in the in the *AWS Systems Manager User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-servicerolearn
            '''
            result = self._values.get("service_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_seconds(self) -> typing.Optional[jsii.Number]:
            '''If this time is reached and the command hasn't already started running, it doesn't run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowruncommandparameters-timeoutseconds
            '''
            result = self._values.get("timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowRunCommandParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowStepFunctionsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"input": "input", "name": "name"},
    )
    class MaintenanceWindowStepFunctionsParametersProperty:
        def __init__(
            self,
            *,
            input: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``MaintenanceWindowStepFunctionsParameters`` property type specifies the parameters for the execution of a ``STEP_FUNCTIONS`` task in a Systems Manager maintenance window.

            ``MaintenanceWindowStepFunctionsParameters`` is a property of the `TaskInvocationParameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html>`_ property type.

            :param input: The inputs for the ``STEP_FUNCTIONS`` task.
            :param name: The name of the ``STEP_FUNCTIONS`` task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                maintenance_window_step_functions_parameters_property = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowStepFunctionsParametersProperty(
                    input="input",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5635767fb55f0832bc70b49f1ed74758e33802a63fa33dc8b7fbb9ed31996e8b)
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input is not None:
                self._values["input"] = input
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''The inputs for the ``STEP_FUNCTIONS`` task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the ``STEP_FUNCTIONS`` task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters.html#cfn-ssm-maintenancewindowtask-maintenancewindowstepfunctionsparameters-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaintenanceWindowStepFunctionsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "notification_arn": "notificationArn",
            "notification_events": "notificationEvents",
            "notification_type": "notificationType",
        },
    )
    class NotificationConfigProperty:
        def __init__(
            self,
            *,
            notification_arn: typing.Optional[builtins.str] = None,
            notification_events: typing.Optional[typing.Sequence[builtins.str]] = None,
            notification_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``NotificationConfig`` property type specifies configurations for sending notifications for a maintenance window task in AWS Systems Manager .

            ``NotificationConfig`` is a property of the `MaintenanceWindowRunCommandParameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-maintenancewindowruncommandparameters.html>`_ property type.

            :param notification_arn: An Amazon Resource Name (ARN) for an Amazon Simple Notification Service (Amazon SNS) topic. Run Command pushes notifications about command status changes to this topic.
            :param notification_events: The different events that you can receive notifications for. These events include the following: ``All`` (events), ``InProgress`` , ``Success`` , ``TimedOut`` , ``Cancelled`` , ``Failed`` . To learn more about these events, see `Configuring Amazon SNS Notifications for AWS Systems Manager <https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-sns-notifications.html>`_ in the *AWS Systems Manager User Guide* .
            :param notification_type: The notification type. - ``Command`` : Receive notification when the status of a command changes. - ``Invocation`` : For commands sent to multiple instances, receive notification on a per-instance basis when the status of a command changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-notificationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                notification_config_property = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty(
                    notification_arn="notificationArn",
                    notification_events=["notificationEvents"],
                    notification_type="notificationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3bfa1c003d4c01e5180d8b406d458ae04d7397cac92bb91ba18e6e953dbcb253)
                check_type(argname="argument notification_arn", value=notification_arn, expected_type=type_hints["notification_arn"])
                check_type(argname="argument notification_events", value=notification_events, expected_type=type_hints["notification_events"])
                check_type(argname="argument notification_type", value=notification_type, expected_type=type_hints["notification_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if notification_arn is not None:
                self._values["notification_arn"] = notification_arn
            if notification_events is not None:
                self._values["notification_events"] = notification_events
            if notification_type is not None:
                self._values["notification_type"] = notification_type

        @builtins.property
        def notification_arn(self) -> typing.Optional[builtins.str]:
            '''An Amazon Resource Name (ARN) for an Amazon Simple Notification Service (Amazon SNS) topic.

            Run Command pushes notifications about command status changes to this topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-notificationconfig.html#cfn-ssm-maintenancewindowtask-notificationconfig-notificationarn
            '''
            result = self._values.get("notification_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The different events that you can receive notifications for.

            These events include the following: ``All`` (events), ``InProgress`` , ``Success`` , ``TimedOut`` , ``Cancelled`` , ``Failed`` . To learn more about these events, see `Configuring Amazon SNS Notifications for AWS Systems Manager <https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-sns-notifications.html>`_ in the *AWS Systems Manager User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-notificationconfig.html#cfn-ssm-maintenancewindowtask-notificationconfig-notificationevents
            '''
            result = self._values.get("notification_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def notification_type(self) -> typing.Optional[builtins.str]:
            '''The notification type.

            - ``Command`` : Receive notification when the status of a command changes.
            - ``Invocation`` : For commands sent to multiple instances, receive notification on a per-instance basis when the status of a command changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-notificationconfig.html#cfn-ssm-maintenancewindowtask-notificationconfig-notificationtype
            '''
            result = self._values.get("notification_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``Target`` property type specifies targets (either instances or window target IDs).

            You specify instances by using ``Key=InstanceIds,Values=< *instanceid1* >,< *instanceid2* >`` . You specify window target IDs using ``Key=WindowTargetIds,Values=< *window-target-id-1* >,< *window-target-id-2* >`` for a maintenance window task in AWS Systems Manager .

            ``Target`` is a property of the `AWS::SSM::MaintenanceWindowTask <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html>`_ property type.
            .. epigraph::

               To use ``resource-groups:Name`` as the key for a maintenance window target, specify the resource group as a ``AWS::SSM::MaintenanceWindowTarget`` type, and use the ``Ref`` function to specify the target for ``AWS::SSM::MaintenanceWindowTask`` . For an example, see *Create a Run Command task that targets instances using a resource group name* in `AWS::SSM::MaintenanceWindowTask Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html#aws-resource-ssm-maintenancewindowtask--examples>`_ .

            :param key: User-defined criteria for sending commands that target instances that meet the criteria. ``Key`` can be ``InstanceIds`` or ``WindowTargetIds`` . For more information about how to target instances within a maintenance window task, see `About 'register-task-with-maintenance-window' Options and Values <https://docs.aws.amazon.com/systems-manager/latest/userguide/register-tasks-options.html>`_ in the *AWS Systems Manager User Guide* .
            :param values: User-defined criteria that maps to ``Key`` . For example, if you specify ``InstanceIds`` , you can specify ``i-1234567890abcdef0,i-9876543210abcdef0`` to run a command on two EC2 instances. For more information about how to target instances within a maintenance window task, see `About 'register-task-with-maintenance-window' Options and Values <https://docs.aws.amazon.com/systems-manager/latest/userguide/register-tasks-options.html>`_ in the *AWS Systems Manager User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                target_property = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.TargetProperty(
                    key="key",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb11e06c6e5faca943765f6bb2e5c3e1ce01190dc467e752e8f91028c9867876)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''User-defined criteria for sending commands that target instances that meet the criteria.

            ``Key`` can be ``InstanceIds`` or ``WindowTargetIds`` . For more information about how to target instances within a maintenance window task, see `About 'register-task-with-maintenance-window' Options and Values <https://docs.aws.amazon.com/systems-manager/latest/userguide/register-tasks-options.html>`_ in the *AWS Systems Manager User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-target.html#cfn-ssm-maintenancewindowtask-target-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''User-defined criteria that maps to ``Key`` .

            For example, if you specify ``InstanceIds`` , you can specify ``i-1234567890abcdef0,i-9876543210abcdef0`` to run a command on two EC2 instances. For more information about how to target instances within a maintenance window task, see `About 'register-task-with-maintenance-window' Options and Values <https://docs.aws.amazon.com/systems-manager/latest/userguide/register-tasks-options.html>`_ in the *AWS Systems Manager User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-target.html#cfn-ssm-maintenancewindowtask-target-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnMaintenanceWindowTaskPropsMixin.TaskInvocationParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maintenance_window_automation_parameters": "maintenanceWindowAutomationParameters",
            "maintenance_window_lambda_parameters": "maintenanceWindowLambdaParameters",
            "maintenance_window_run_command_parameters": "maintenanceWindowRunCommandParameters",
            "maintenance_window_step_functions_parameters": "maintenanceWindowStepFunctionsParameters",
        },
    )
    class TaskInvocationParametersProperty:
        def __init__(
            self,
            *,
            maintenance_window_automation_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowAutomationParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maintenance_window_lambda_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowLambdaParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maintenance_window_run_command_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowRunCommandParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maintenance_window_step_functions_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowStepFunctionsParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``TaskInvocationParameters`` property type specifies the task execution parameters for a maintenance window task in AWS Systems Manager .

            ``TaskInvocationParameters`` is a property of the `AWS::SSM::MaintenanceWindowTask <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-maintenancewindowtask.html>`_ property type.

            :param maintenance_window_automation_parameters: The parameters for an ``AUTOMATION`` task type.
            :param maintenance_window_lambda_parameters: The parameters for a ``LAMBDA`` task type.
            :param maintenance_window_run_command_parameters: The parameters for a ``RUN_COMMAND`` task type.
            :param maintenance_window_step_functions_parameters: The parameters for a ``STEP_FUNCTIONS`` task type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                # parameters: Any
                
                task_invocation_parameters_property = ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.TaskInvocationParametersProperty(
                    maintenance_window_automation_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowAutomationParametersProperty(
                        document_version="documentVersion",
                        parameters=parameters
                    ),
                    maintenance_window_lambda_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowLambdaParametersProperty(
                        client_context="clientContext",
                        payload="payload",
                        qualifier="qualifier"
                    ),
                    maintenance_window_run_command_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowRunCommandParametersProperty(
                        cloud_watch_output_config=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty(
                            cloud_watch_log_group_name="cloudWatchLogGroupName",
                            cloud_watch_output_enabled=False
                        ),
                        comment="comment",
                        document_hash="documentHash",
                        document_hash_type="documentHashType",
                        document_version="documentVersion",
                        notification_config=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty(
                            notification_arn="notificationArn",
                            notification_events=["notificationEvents"],
                            notification_type="notificationType"
                        ),
                        output_s3_bucket_name="outputS3BucketName",
                        output_s3_key_prefix="outputS3KeyPrefix",
                        parameters=parameters,
                        service_role_arn="serviceRoleArn",
                        timeout_seconds=123
                    ),
                    maintenance_window_step_functions_parameters=ssm_mixins.CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowStepFunctionsParametersProperty(
                        input="input",
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da427e718906b6a7041417cdc4a65ddd9bb12d6bef75266389c644d547e80d1b)
                check_type(argname="argument maintenance_window_automation_parameters", value=maintenance_window_automation_parameters, expected_type=type_hints["maintenance_window_automation_parameters"])
                check_type(argname="argument maintenance_window_lambda_parameters", value=maintenance_window_lambda_parameters, expected_type=type_hints["maintenance_window_lambda_parameters"])
                check_type(argname="argument maintenance_window_run_command_parameters", value=maintenance_window_run_command_parameters, expected_type=type_hints["maintenance_window_run_command_parameters"])
                check_type(argname="argument maintenance_window_step_functions_parameters", value=maintenance_window_step_functions_parameters, expected_type=type_hints["maintenance_window_step_functions_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maintenance_window_automation_parameters is not None:
                self._values["maintenance_window_automation_parameters"] = maintenance_window_automation_parameters
            if maintenance_window_lambda_parameters is not None:
                self._values["maintenance_window_lambda_parameters"] = maintenance_window_lambda_parameters
            if maintenance_window_run_command_parameters is not None:
                self._values["maintenance_window_run_command_parameters"] = maintenance_window_run_command_parameters
            if maintenance_window_step_functions_parameters is not None:
                self._values["maintenance_window_step_functions_parameters"] = maintenance_window_step_functions_parameters

        @builtins.property
        def maintenance_window_automation_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowAutomationParametersProperty"]]:
            '''The parameters for an ``AUTOMATION`` task type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters-maintenancewindowautomationparameters
            '''
            result = self._values.get("maintenance_window_automation_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowAutomationParametersProperty"]], result)

        @builtins.property
        def maintenance_window_lambda_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowLambdaParametersProperty"]]:
            '''The parameters for a ``LAMBDA`` task type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters-maintenancewindowlambdaparameters
            '''
            result = self._values.get("maintenance_window_lambda_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowLambdaParametersProperty"]], result)

        @builtins.property
        def maintenance_window_run_command_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowRunCommandParametersProperty"]]:
            '''The parameters for a ``RUN_COMMAND`` task type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters-maintenancewindowruncommandparameters
            '''
            result = self._values.get("maintenance_window_run_command_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowRunCommandParametersProperty"]], result)

        @builtins.property
        def maintenance_window_step_functions_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowStepFunctionsParametersProperty"]]:
            '''The parameters for a ``STEP_FUNCTIONS`` task type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-maintenancewindowtask-taskinvocationparameters.html#cfn-ssm-maintenancewindowtask-taskinvocationparameters-maintenancewindowstepfunctionsparameters
            '''
            result = self._values.get("maintenance_window_step_functions_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowStepFunctionsParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskInvocationParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnParameterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_pattern": "allowedPattern",
        "data_type": "dataType",
        "description": "description",
        "name": "name",
        "policies": "policies",
        "tags": "tags",
        "tier": "tier",
        "type": "type",
        "value": "value",
    },
)
class CfnParameterMixinProps:
    def __init__(
        self,
        *,
        allowed_pattern: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tier: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnParameterPropsMixin.

        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for ``String`` types with values restricted to numbers, you can specify the following: ``AllowedPattern=^\\d+$``
        :param data_type: The data type of the parameter, such as ``text`` or ``aws:ec2:image`` . The default is ``text`` .
        :param description: Information about the parameter.
        :param name: The name of the parameter. .. epigraph:: The reported maximum length of 2048 characters for a parameter name includes 1037 characters that are reserved for internal use by Systems Manager . The maximum length for a parameter name that you specify is 1011 characters. This count of 1011 characters includes the characters in the ARN that precede the name you specify. This ARN length will vary depending on your partition and Region. For example, the following 45 characters count toward the 1011 character maximum for a parameter created in the US East (Ohio) Region: ``arn:aws:ssm:us-east-2:111122223333:parameter/`` .
        :param policies: Information about the policies assigned to a parameter. `Assigning parameter policies <https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-policies.html>`_ in the *AWS Systems Manager User Guide* .
        :param tags: Optional metadata that you assign to a resource in the form of an arbitrary set of tags (key-value pairs). Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a Systems Manager parameter to identify the type of resource to which it applies, the environment, or the type of configuration data referenced by the parameter.
        :param tier: The parameter tier.
        :param type: The type of parameter. .. epigraph:: Parameters of type ``SecureString`` are not supported by AWS CloudFormation .
        :param value: The parameter value. .. epigraph:: If type is ``StringList`` , the system returns a comma-separated string with no spaces between commas in the ``Value`` field.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
            
            cfn_parameter_mixin_props = ssm_mixins.CfnParameterMixinProps(
                allowed_pattern="allowedPattern",
                data_type="dataType",
                description="description",
                name="name",
                policies="policies",
                tags={
                    "tags_key": "tags"
                },
                tier="tier",
                type="type",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3200d2546f786b8279189677af1b9b028c21a94fc18ff28e03e79a12cddfe5)
            check_type(argname="argument allowed_pattern", value=allowed_pattern, expected_type=type_hints["allowed_pattern"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_pattern is not None:
            self._values["allowed_pattern"] = allowed_pattern
        if data_type is not None:
            self._values["data_type"] = data_type
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if policies is not None:
            self._values["policies"] = policies
        if tags is not None:
            self._values["tags"] = tags
        if tier is not None:
            self._values["tier"] = tier
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[builtins.str]:
        '''A regular expression used to validate the parameter value.

        For example, for ``String`` types with values restricted to numbers, you can specify the following: ``AllowedPattern=^\\d+$``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-allowedpattern
        '''
        result = self._values.get("allowed_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The data type of the parameter, such as ``text`` or ``aws:ec2:image`` .

        The default is ``text`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-datatype
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Information about the parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter.

        .. epigraph::

           The reported maximum length of 2048 characters for a parameter name includes 1037 characters that are reserved for internal use by Systems Manager . The maximum length for a parameter name that you specify is 1011 characters.

           This count of 1011 characters includes the characters in the ARN that precede the name you specify. This ARN length will vary depending on your partition and Region. For example, the following 45 characters count toward the 1011 character maximum for a parameter created in the US East (Ohio) Region: ``arn:aws:ssm:us-east-2:111122223333:parameter/`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(self) -> typing.Optional[builtins.str]:
        '''Information about the policies assigned to a parameter.

        `Assigning parameter policies <https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-policies.html>`_ in the *AWS Systems Manager User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional metadata that you assign to a resource in the form of an arbitrary set of tags (key-value pairs).

        Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a Systems Manager parameter to identify the type of resource to which it applies, the environment, or the type of configuration data referenced by the parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tier(self) -> typing.Optional[builtins.str]:
        '''The parameter tier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-tier
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of parameter.

        .. epigraph::

           Parameters of type ``SecureString`` are not supported by AWS CloudFormation .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The parameter value.

        .. epigraph::

           If type is ``StringList`` , the system returns a comma-separated string with no spaces between commas in the ``Value`` field.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParameterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnParameterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnParameterPropsMixin",
):
    '''The ``AWS::SSM::Parameter`` resource creates an SSM parameter in AWS Systems Manager Parameter Store.

    .. epigraph::

       To create an SSM parameter, you must have the AWS Identity and Access Management ( IAM ) permissions ``ssm:PutParameter`` and ``ssm:AddTagsToResource`` . On stack creation, AWS CloudFormation adds the following three tags to the parameter: ``aws:cloudformation:stack-name`` , ``aws:cloudformation:logical-id`` , and ``aws:cloudformation:stack-id`` , in addition to any custom tags you specify.

       To add, update, or remove tags during stack update, you must have IAM permissions for both ``ssm:AddTagsToResource`` and ``ssm:RemoveTagsFromResource`` . For more information, see `Managing access using policies <https://docs.aws.amazon.com/systems-manager/latest/userguide/security-iam.html#security_iam_access-manage>`_ in the *AWS Systems Manager User Guide* .

    For information about valid values for parameters, see `About requirements and constraints for parameter names <https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-su-create.html#sysman-parameter-name-constraints>`_ in the *AWS Systems Manager User Guide* and `PutParameter <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PutParameter.html>`_ in the *AWS Systems Manager API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html
    :cloudformationResource: AWS::SSM::Parameter
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
        
        cfn_parameter_props_mixin = ssm_mixins.CfnParameterPropsMixin(ssm_mixins.CfnParameterMixinProps(
            allowed_pattern="allowedPattern",
            data_type="dataType",
            description="description",
            name="name",
            policies="policies",
            tags={
                "tags_key": "tags"
            },
            tier="tier",
            type="type",
            value="value"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnParameterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSM::Parameter``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449a24370b660ac8c714a3cd1177e6ea5891369c619578b02f87bc131125825d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2798d459a3a0bfd521995b390921aa4756015386a25f986cc969f8be9e850388)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed17a0f9995ef4b5920ba9e67f3aeb77de97df3852d4ad8aab59444290391fe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnParameterMixinProps:
        return typing.cast(CfnParameterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnPatchBaselineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "approval_rules": "approvalRules",
        "approved_patches": "approvedPatches",
        "approved_patches_compliance_level": "approvedPatchesComplianceLevel",
        "approved_patches_enable_non_security": "approvedPatchesEnableNonSecurity",
        "available_security_updates_compliance_status": "availableSecurityUpdatesComplianceStatus",
        "default_baseline": "defaultBaseline",
        "description": "description",
        "global_filters": "globalFilters",
        "name": "name",
        "operating_system": "operatingSystem",
        "patch_groups": "patchGroups",
        "rejected_patches": "rejectedPatches",
        "rejected_patches_action": "rejectedPatchesAction",
        "sources": "sources",
        "tags": "tags",
    },
)
class CfnPatchBaselineMixinProps:
    def __init__(
        self,
        *,
        approval_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPatchBaselinePropsMixin.RuleGroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        approved_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
        approved_patches_compliance_level: typing.Optional[builtins.str] = None,
        approved_patches_enable_non_security: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        available_security_updates_compliance_status: typing.Optional[builtins.str] = None,
        default_baseline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        global_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPatchBaselinePropsMixin.PatchFilterGroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        operating_system: typing.Optional[builtins.str] = None,
        patch_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        rejected_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
        rejected_patches_action: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPatchBaselinePropsMixin.PatchSourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPatchBaselinePropsMixin.

        :param approval_rules: A set of rules used to include patches in the baseline.
        :param approved_patches: A list of explicitly approved patches for the baseline. For information about accepted formats for lists of approved patches and rejected patches, see `Package name formats for approved and rejected patch lists <https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-approved-rejected-package-name-formats.html>`_ in the *AWS Systems Manager User Guide* .
        :param approved_patches_compliance_level: Defines the compliance level for approved patches. When an approved patch is reported as missing, this value describes the severity of the compliance violation. The default value is ``UNSPECIFIED`` . Default: - "UNSPECIFIED"
        :param approved_patches_enable_non_security: Indicates whether the list of approved patches includes non-security updates that should be applied to the managed nodes. The default value is ``false`` . Applies to Linux managed nodes only. Default: - false
        :param available_security_updates_compliance_status: Indicates the status you want to assign to security patches that are available but not approved because they don't meet the installation criteria specified in the patch baseline. Example scenario: Security patches that you might want installed can be skipped if you have specified a long period to wait after a patch is released before installation. If an update to the patch is released during your specified waiting period, the waiting period for installing the patch starts over. If the waiting period is too long, multiple versions of the patch could be released but never installed. Supported for Windows Server managed nodes only.
        :param default_baseline: Indicates whether this is the default baseline. AWS Systems Manager supports creating multiple default patch baselines. For example, you can create a default patch baseline for each operating system. Default: - false
        :param description: A description of the patch baseline.
        :param global_filters: A set of global filters used to include patches in the baseline. .. epigraph:: The ``GlobalFilters`` parameter can be configured only by using the AWS CLI or an AWS SDK. It can't be configured from the Patch Manager console, and its value isn't displayed in the console.
        :param name: The name of the patch baseline.
        :param operating_system: Defines the operating system the patch baseline applies to. The default value is ``WINDOWS`` . Default: - "WINDOWS"
        :param patch_groups: The name of the patch group to be registered with the patch baseline.
        :param rejected_patches: A list of explicitly rejected patches for the baseline. For information about accepted formats for lists of approved patches and rejected patches, see `Package name formats for approved and rejected patch lists <https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-approved-rejected-package-name-formats.html>`_ in the *AWS Systems Manager User Guide* .
        :param rejected_patches_action: The action for Patch Manager to take on patches included in the ``RejectedPackages`` list. - **ALLOW_AS_DEPENDENCY** - *Linux and macOS* : A package in the rejected patches list is installed only if it is a dependency of another package. It is considered compliant with the patch baseline, and its status is reported as ``INSTALLED_OTHER`` . This is the default action if no option is specified. *Windows Server* : Windows Server doesn't support the concept of package dependencies. If a package in the rejected patches list and already installed on the node, its status is reported as ``INSTALLED_OTHER`` . Any package not already installed on the node is skipped. This is the default action if no option is specified. - **BLOCK** - *All OSs* : Packages in the rejected patches list, and packages that include them as dependencies, aren't installed by Patch Manager under any circumstances. State value assignment for patch compliance: - If a package was installed before it was added to the rejected patches list, or is installed outside of Patch Manager afterward, it's considered noncompliant with the patch baseline and its status is reported as ``INSTALLED_REJECTED`` . - If an update attempts to install a dependency package that is now rejected by the baseline, when previous versions of the package were not rejected, the package being updated is reported as ``MISSING`` for ``SCAN`` operations and as ``FAILED`` for ``INSTALL`` operations. Default: - "ALLOW_AS_DEPENDENCY"
        :param sources: Information about the patches to use to update the managed nodes, including target operating systems and source repositories. Applies to Linux managed nodes only.
        :param tags: Optional metadata that you assign to a resource. Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a patch baseline to identify the severity level of patches it specifies and the operating system family it applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
            
            cfn_patch_baseline_mixin_props = ssm_mixins.CfnPatchBaselineMixinProps(
                approval_rules=ssm_mixins.CfnPatchBaselinePropsMixin.RuleGroupProperty(
                    patch_rules=[ssm_mixins.CfnPatchBaselinePropsMixin.RuleProperty(
                        approve_after_days=123,
                        approve_until_date="approveUntilDate",
                        compliance_level="complianceLevel",
                        enable_non_security=False,
                        patch_filter_group=ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterGroupProperty(
                            patch_filters=[ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterProperty(
                                key="key",
                                values=["values"]
                            )]
                        )
                    )]
                ),
                approved_patches=["approvedPatches"],
                approved_patches_compliance_level="approvedPatchesComplianceLevel",
                approved_patches_enable_non_security=False,
                available_security_updates_compliance_status="availableSecurityUpdatesComplianceStatus",
                default_baseline=False,
                description="description",
                global_filters=ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterGroupProperty(
                    patch_filters=[ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterProperty(
                        key="key",
                        values=["values"]
                    )]
                ),
                name="name",
                operating_system="operatingSystem",
                patch_groups=["patchGroups"],
                rejected_patches=["rejectedPatches"],
                rejected_patches_action="rejectedPatchesAction",
                sources=[ssm_mixins.CfnPatchBaselinePropsMixin.PatchSourceProperty(
                    configuration="configuration",
                    name="name",
                    products=["products"]
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966a6783d92096bb4b3f576bc68e3ff3211ba3ef759c338392ded72d30ffb6df)
            check_type(argname="argument approval_rules", value=approval_rules, expected_type=type_hints["approval_rules"])
            check_type(argname="argument approved_patches", value=approved_patches, expected_type=type_hints["approved_patches"])
            check_type(argname="argument approved_patches_compliance_level", value=approved_patches_compliance_level, expected_type=type_hints["approved_patches_compliance_level"])
            check_type(argname="argument approved_patches_enable_non_security", value=approved_patches_enable_non_security, expected_type=type_hints["approved_patches_enable_non_security"])
            check_type(argname="argument available_security_updates_compliance_status", value=available_security_updates_compliance_status, expected_type=type_hints["available_security_updates_compliance_status"])
            check_type(argname="argument default_baseline", value=default_baseline, expected_type=type_hints["default_baseline"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument global_filters", value=global_filters, expected_type=type_hints["global_filters"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
            check_type(argname="argument patch_groups", value=patch_groups, expected_type=type_hints["patch_groups"])
            check_type(argname="argument rejected_patches", value=rejected_patches, expected_type=type_hints["rejected_patches"])
            check_type(argname="argument rejected_patches_action", value=rejected_patches_action, expected_type=type_hints["rejected_patches_action"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if approval_rules is not None:
            self._values["approval_rules"] = approval_rules
        if approved_patches is not None:
            self._values["approved_patches"] = approved_patches
        if approved_patches_compliance_level is not None:
            self._values["approved_patches_compliance_level"] = approved_patches_compliance_level
        if approved_patches_enable_non_security is not None:
            self._values["approved_patches_enable_non_security"] = approved_patches_enable_non_security
        if available_security_updates_compliance_status is not None:
            self._values["available_security_updates_compliance_status"] = available_security_updates_compliance_status
        if default_baseline is not None:
            self._values["default_baseline"] = default_baseline
        if description is not None:
            self._values["description"] = description
        if global_filters is not None:
            self._values["global_filters"] = global_filters
        if name is not None:
            self._values["name"] = name
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if patch_groups is not None:
            self._values["patch_groups"] = patch_groups
        if rejected_patches is not None:
            self._values["rejected_patches"] = rejected_patches
        if rejected_patches_action is not None:
            self._values["rejected_patches_action"] = rejected_patches_action
        if sources is not None:
            self._values["sources"] = sources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def approval_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.RuleGroupProperty"]]:
        '''A set of rules used to include patches in the baseline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvalrules
        '''
        result = self._values.get("approval_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.RuleGroupProperty"]], result)

    @builtins.property
    def approved_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of explicitly approved patches for the baseline.

        For information about accepted formats for lists of approved patches and rejected patches, see `Package name formats for approved and rejected patch lists <https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-approved-rejected-package-name-formats.html>`_ in the *AWS Systems Manager User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvedpatches
        '''
        result = self._values.get("approved_patches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def approved_patches_compliance_level(self) -> typing.Optional[builtins.str]:
        '''Defines the compliance level for approved patches.

        When an approved patch is reported as missing, this value describes the severity of the compliance violation. The default value is ``UNSPECIFIED`` .

        :default: - "UNSPECIFIED"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvedpatchescompliancelevel
        '''
        result = self._values.get("approved_patches_compliance_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def approved_patches_enable_non_security(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the list of approved patches includes non-security updates that should be applied to the managed nodes.

        The default value is ``false`` . Applies to Linux managed nodes only.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-approvedpatchesenablenonsecurity
        '''
        result = self._values.get("approved_patches_enable_non_security")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def available_security_updates_compliance_status(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Indicates the status you want to assign to security patches that are available but not approved because they don't meet the installation criteria specified in the patch baseline.

        Example scenario: Security patches that you might want installed can be skipped if you have specified a long period to wait after a patch is released before installation. If an update to the patch is released during your specified waiting period, the waiting period for installing the patch starts over. If the waiting period is too long, multiple versions of the patch could be released but never installed.

        Supported for Windows Server managed nodes only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-availablesecurityupdatescompliancestatus
        '''
        result = self._values.get("available_security_updates_compliance_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_baseline(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether this is the default baseline.

        AWS Systems Manager supports creating multiple default patch baselines. For example, you can create a default patch baseline for each operating system.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-defaultbaseline
        '''
        result = self._values.get("default_baseline")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the patch baseline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.PatchFilterGroupProperty"]]:
        '''A set of global filters used to include patches in the baseline.

        .. epigraph::

           The ``GlobalFilters`` parameter can be configured only by using the AWS CLI or an AWS SDK. It can't be configured from the Patch Manager console, and its value isn't displayed in the console.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-globalfilters
        '''
        result = self._values.get("global_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.PatchFilterGroupProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the patch baseline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Defines the operating system the patch baseline applies to.

        The default value is ``WINDOWS`` .

        :default: - "WINDOWS"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-operatingsystem
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def patch_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the patch group to be registered with the patch baseline.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-patchgroups
        '''
        result = self._values.get("patch_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rejected_patches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of explicitly rejected patches for the baseline.

        For information about accepted formats for lists of approved patches and rejected patches, see `Package name formats for approved and rejected patch lists <https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-approved-rejected-package-name-formats.html>`_ in the *AWS Systems Manager User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-rejectedpatches
        '''
        result = self._values.get("rejected_patches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rejected_patches_action(self) -> typing.Optional[builtins.str]:
        '''The action for Patch Manager to take on patches included in the ``RejectedPackages`` list.

        - **ALLOW_AS_DEPENDENCY** - *Linux and macOS* : A package in the rejected patches list is installed only if it is a dependency of another package. It is considered compliant with the patch baseline, and its status is reported as ``INSTALLED_OTHER`` . This is the default action if no option is specified.

        *Windows Server* : Windows Server doesn't support the concept of package dependencies. If a package in the rejected patches list and already installed on the node, its status is reported as ``INSTALLED_OTHER`` . Any package not already installed on the node is skipped. This is the default action if no option is specified.

        - **BLOCK** - *All OSs* : Packages in the rejected patches list, and packages that include them as dependencies, aren't installed by Patch Manager under any circumstances.

        State value assignment for patch compliance:

        - If a package was installed before it was added to the rejected patches list, or is installed outside of Patch Manager afterward, it's considered noncompliant with the patch baseline and its status is reported as ``INSTALLED_REJECTED`` .
        - If an update attempts to install a dependency package that is now rejected by the baseline, when previous versions of the package were not rejected, the package being updated is reported as ``MISSING`` for ``SCAN`` operations and as ``FAILED`` for ``INSTALL`` operations.

        :default: - "ALLOW_AS_DEPENDENCY"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-rejectedpatchesaction
        '''
        result = self._values.get("rejected_patches_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.PatchSourceProperty"]]]]:
        '''Information about the patches to use to update the managed nodes, including target operating systems and source repositories.

        Applies to Linux managed nodes only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-sources
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.PatchSourceProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata that you assign to a resource.

        Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For example, you might want to tag a patch baseline to identify the severity level of patches it specifies and the operating system family it applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html#cfn-ssm-patchbaseline-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPatchBaselineMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPatchBaselinePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnPatchBaselinePropsMixin",
):
    '''The ``AWS::SSM::PatchBaseline`` resource defines the basic information for an AWS Systems Manager patch baseline.

    A patch baseline defines which patches are approved for installation on your instances.

    For more information, see `CreatePatchBaseline <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_CreatePatchBaseline.html>`_ in the *AWS Systems Manager API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html
    :cloudformationResource: AWS::SSM::PatchBaseline
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
        
        cfn_patch_baseline_props_mixin = ssm_mixins.CfnPatchBaselinePropsMixin(ssm_mixins.CfnPatchBaselineMixinProps(
            approval_rules=ssm_mixins.CfnPatchBaselinePropsMixin.RuleGroupProperty(
                patch_rules=[ssm_mixins.CfnPatchBaselinePropsMixin.RuleProperty(
                    approve_after_days=123,
                    approve_until_date="approveUntilDate",
                    compliance_level="complianceLevel",
                    enable_non_security=False,
                    patch_filter_group=ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterGroupProperty(
                        patch_filters=[ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterProperty(
                            key="key",
                            values=["values"]
                        )]
                    )
                )]
            ),
            approved_patches=["approvedPatches"],
            approved_patches_compliance_level="approvedPatchesComplianceLevel",
            approved_patches_enable_non_security=False,
            available_security_updates_compliance_status="availableSecurityUpdatesComplianceStatus",
            default_baseline=False,
            description="description",
            global_filters=ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterGroupProperty(
                patch_filters=[ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterProperty(
                    key="key",
                    values=["values"]
                )]
            ),
            name="name",
            operating_system="operatingSystem",
            patch_groups=["patchGroups"],
            rejected_patches=["rejectedPatches"],
            rejected_patches_action="rejectedPatchesAction",
            sources=[ssm_mixins.CfnPatchBaselinePropsMixin.PatchSourceProperty(
                configuration="configuration",
                name="name",
                products=["products"]
            )],
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
        props: typing.Union[CfnPatchBaselineMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSM::PatchBaseline``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf2a2324ac64be0d38fa6a05fdd473bf1c6ff4acf8f5e9b3b7977a432c4d085a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd5a6eebf31980a352d94ca8cd8ea5895e71ea2970919423c0a142616f6caf04)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cda3936807b9e9080f40f697d2a404802db4658f16fa50f6a508a8790e43d51)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPatchBaselineMixinProps:
        return typing.cast(CfnPatchBaselineMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnPatchBaselinePropsMixin.PatchFilterGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"patch_filters": "patchFilters"},
    )
    class PatchFilterGroupProperty:
        def __init__(
            self,
            *,
            patch_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPatchBaselinePropsMixin.PatchFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``PatchFilterGroup`` property type specifies a set of patch filters for an AWS Systems Manager patch baseline, typically used for approval rules for a Systems Manager patch baseline.

            ``PatchFilterGroup`` is the property type for the ``GlobalFilters`` property of the `AWS::SSM::PatchBaseline <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html>`_ resource and the ``PatchFilterGroup`` property of the `Rule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html>`_ property type.

            :param patch_filters: The set of patch filters that make up the group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfiltergroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                patch_filter_group_property = ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterGroupProperty(
                    patch_filters=[ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterProperty(
                        key="key",
                        values=["values"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a623dcc484fa5af0b2adfd92911cfc120fddfd8aee73e7cd620bcbf26b8774a9)
                check_type(argname="argument patch_filters", value=patch_filters, expected_type=type_hints["patch_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if patch_filters is not None:
                self._values["patch_filters"] = patch_filters

        @builtins.property
        def patch_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.PatchFilterProperty"]]]]:
            '''The set of patch filters that make up the group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfiltergroup.html#cfn-ssm-patchbaseline-patchfiltergroup-patchfilters
            '''
            result = self._values.get("patch_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.PatchFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PatchFilterGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnPatchBaselinePropsMixin.PatchFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class PatchFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The ``PatchFilter`` property type defines a patch filter for an AWS Systems Manager patch baseline.

            The ``PatchFilters`` property of the `PatchFilterGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfiltergroup.html>`_ property type contains a list of ``PatchFilter`` property types.

            You can view lists of valid values for the patch properties by running the ``DescribePatchProperties`` command. For more information, see `DescribePatchProperties <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_DescribePatchProperties.html>`_ in the *AWS Systems Manager API Reference* .

            :param key: The key for the filter. For information about valid keys, see `PatchFilter <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PatchFilter.html>`_ in the *AWS Systems Manager API Reference* .
            :param values: The value for the filter key. For information about valid values for each key based on operating system type, see `PatchFilter <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PatchFilter.html>`_ in the *AWS Systems Manager API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                patch_filter_property = ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterProperty(
                    key="key",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6e1c5fcef15226e878845215765bb25c876a8b353c1b4699bdd8200b0168b63)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key for the filter.

            For information about valid keys, see `PatchFilter <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PatchFilter.html>`_ in the *AWS Systems Manager API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfilter.html#cfn-ssm-patchbaseline-patchfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The value for the filter key.

            For information about valid values for each key based on operating system type, see `PatchFilter <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PatchFilter.html>`_ in the *AWS Systems Manager API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchfilter.html#cfn-ssm-patchbaseline-patchfilter-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PatchFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnPatchBaselinePropsMixin.PatchSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration": "configuration",
            "name": "name",
            "products": "products",
        },
    )
    class PatchSourceProperty:
        def __init__(
            self,
            *,
            configuration: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            products: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''``PatchSource`` is the property type for the ``Sources`` resource of the `AWS::SSM::PatchBaseline <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html>`_ resource.

            The AWS CloudFormation ``AWS::SSM::PatchSource`` resource is used to provide information about the patches to use to update target instances, including target operating systems and source repository. Applies to Linux managed nodes only.

            :param configuration: The value of the repo configuration. *Example for yum repositories* ``[main]`` ``name=MyCustomRepository`` ``baseurl=https://my-custom-repository`` ``enabled=1`` For information about other options available for your yum repository configuration, see `dnf.conf(5) <https://docs.aws.amazon.com/https://man7.org/linux/man-pages/man5/dnf.conf.5.html>`_ on the *man7.org* website. *Examples for Ubuntu Server and Debian Server* ``deb http://security.ubuntu.com/ubuntu jammy main`` ``deb https://site.example.com/debian distribution component1 component2 component3`` Repo information for Ubuntu Server repositories must be specifed in a single line. For more examples and information, see `jammy (5) sources.list.5.gz <https://docs.aws.amazon.com/https://manpages.ubuntu.com/manpages/jammy/man5/sources.list.5.html>`_ on the *Ubuntu Server Manuals* website and `sources.list format <https://docs.aws.amazon.com/https://wiki.debian.org/SourcesList#sources.list_format>`_ on the *Debian Wiki* .
            :param name: The name specified to identify the patch source.
            :param products: The specific operating system versions a patch repository applies to, such as "Ubuntu16.04", "RedhatEnterpriseLinux7.2" or "Suse12.7". For lists of supported product values, see `PatchFilter <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PatchFilter.html>`_ in the *AWS Systems Manager API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                patch_source_property = ssm_mixins.CfnPatchBaselinePropsMixin.PatchSourceProperty(
                    configuration="configuration",
                    name="name",
                    products=["products"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__869ea368f29938b8034592b9bcf91f7555a5903059ceea893ee631183fbb4cfe)
                check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument products", value=products, expected_type=type_hints["products"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration is not None:
                self._values["configuration"] = configuration
            if name is not None:
                self._values["name"] = name
            if products is not None:
                self._values["products"] = products

        @builtins.property
        def configuration(self) -> typing.Optional[builtins.str]:
            '''The value of the repo configuration.

            *Example for yum repositories*

            ``[main]``

            ``name=MyCustomRepository``

            ``baseurl=https://my-custom-repository``

            ``enabled=1``

            For information about other options available for your yum repository configuration, see `dnf.conf(5) <https://docs.aws.amazon.com/https://man7.org/linux/man-pages/man5/dnf.conf.5.html>`_ on the *man7.org* website.

            *Examples for Ubuntu Server and Debian Server*

            ``deb http://security.ubuntu.com/ubuntu jammy main``

            ``deb https://site.example.com/debian distribution component1 component2 component3``

            Repo information for Ubuntu Server repositories must be specifed in a single line. For more examples and information, see `jammy (5) sources.list.5.gz <https://docs.aws.amazon.com/https://manpages.ubuntu.com/manpages/jammy/man5/sources.list.5.html>`_ on the *Ubuntu Server Manuals* website and `sources.list format <https://docs.aws.amazon.com/https://wiki.debian.org/SourcesList#sources.list_format>`_ on the *Debian Wiki* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchsource.html#cfn-ssm-patchbaseline-patchsource-configuration
            '''
            result = self._values.get("configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name specified to identify the patch source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchsource.html#cfn-ssm-patchbaseline-patchsource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def products(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The specific operating system versions a patch repository applies to, such as "Ubuntu16.04", "RedhatEnterpriseLinux7.2" or "Suse12.7". For lists of supported product values, see `PatchFilter <https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PatchFilter.html>`_ in the *AWS Systems Manager API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-patchsource.html#cfn-ssm-patchbaseline-patchsource-products
            '''
            result = self._values.get("products")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PatchSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnPatchBaselinePropsMixin.RuleGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"patch_rules": "patchRules"},
    )
    class RuleGroupProperty:
        def __init__(
            self,
            *,
            patch_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPatchBaselinePropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``RuleGroup`` property type specifies a set of rules that define the approval rules for an AWS Systems Manager patch baseline.

            ``RuleGroup`` is the property type for the ``ApprovalRules`` property of the `AWS::SSM::PatchBaseline <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-patchbaseline.html>`_ resource.

            :param patch_rules: The rules that make up the rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rulegroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                rule_group_property = ssm_mixins.CfnPatchBaselinePropsMixin.RuleGroupProperty(
                    patch_rules=[ssm_mixins.CfnPatchBaselinePropsMixin.RuleProperty(
                        approve_after_days=123,
                        approve_until_date="approveUntilDate",
                        compliance_level="complianceLevel",
                        enable_non_security=False,
                        patch_filter_group=ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterGroupProperty(
                            patch_filters=[ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterProperty(
                                key="key",
                                values=["values"]
                            )]
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a83f81319b0664e874ee904bdd73e4447949b65e14bc4cb88fcd35cd1d43f01)
                check_type(argname="argument patch_rules", value=patch_rules, expected_type=type_hints["patch_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if patch_rules is not None:
                self._values["patch_rules"] = patch_rules

        @builtins.property
        def patch_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.RuleProperty"]]]]:
            '''The rules that make up the rule group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rulegroup.html#cfn-ssm-patchbaseline-rulegroup-patchrules
            '''
            result = self._values.get("patch_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.RuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnPatchBaselinePropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "approve_after_days": "approveAfterDays",
            "approve_until_date": "approveUntilDate",
            "compliance_level": "complianceLevel",
            "enable_non_security": "enableNonSecurity",
            "patch_filter_group": "patchFilterGroup",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            approve_after_days: typing.Optional[jsii.Number] = None,
            approve_until_date: typing.Optional[builtins.str] = None,
            compliance_level: typing.Optional[builtins.str] = None,
            enable_non_security: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            patch_filter_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPatchBaselinePropsMixin.PatchFilterGroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ``Rule`` property type specifies an approval rule for a Systems Manager patch baseline.

            The ``PatchRules`` property of the `RuleGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rulegroup.html>`_ property type contains a list of ``Rule`` property types.

            :param approve_after_days: The number of days after the release date of each patch matched by the rule that the patch is marked as approved in the patch baseline. For example, a value of ``7`` means that patches are approved seven days after they are released. Patch Manager evaluates patch release dates using Coordinated Universal Time (UTC). If the day represented by ``7`` is ``2025-11-16`` , patches released between ``2025-11-16T00:00:00Z`` and ``2025-11-16T23:59:59Z`` will be included in the approval. This parameter is marked as ``Required: No`` , but your request must include a value for either ``ApproveAfterDays`` or ``ApproveUntilDate`` . Not supported for Debian Server or Ubuntu Server. .. epigraph:: Use caution when setting this value for Windows Server patch baselines. Because patch updates that are replaced by later updates are removed, setting too broad a value for this parameter can result in crucial patches not being installed. For more information, see the *Windows Server* tab in the topic `How security patches are selected <https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-selecting-patches.html>`_ in the *AWS Systems Manager User Guide* .
            :param approve_until_date: The cutoff date for auto approval of released patches. Any patches released on or before this date are installed automatically. Enter dates in the format ``YYYY-MM-DD`` . For example, ``2025-11-16`` . Patch Manager evaluates patch release dates using Coordinated Universal Time (UTC). If you enter the date ``2025-11-16`` , patches released between ``2025-11-16T00:00:00Z`` and ``2025-11-16T23:59:59Z`` will be included in the approval. This parameter is marked as ``Required: No`` , but your request must include a value for either ``ApproveUntilDate`` or ``ApproveAfterDays`` . Not supported for Debian Server or Ubuntu Server. .. epigraph:: Use caution when setting this value for Windows Server patch baselines. Because patch updates that are replaced by later updates are removed, setting too broad a value for this parameter can result in crucial patches not being installed. For more information, see the *Windows Server* tab in the topic `How security patches are selected <https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-selecting-patches.html>`_ in the *AWS Systems Manager User Guide* .
            :param compliance_level: A compliance severity level for all approved patches in a patch baseline. Valid compliance severity levels include the following: ``UNSPECIFIED`` , ``CRITICAL`` , ``HIGH`` , ``MEDIUM`` , ``LOW`` , and ``INFORMATIONAL`` .
            :param enable_non_security: For managed nodes identified by the approval rule filters, enables a patch baseline to apply non-security updates available in the specified repository. The default value is ``false`` . Applies to Linux managed nodes only. Default: - false
            :param patch_filter_group: The patch filter group that defines the criteria for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                rule_property = ssm_mixins.CfnPatchBaselinePropsMixin.RuleProperty(
                    approve_after_days=123,
                    approve_until_date="approveUntilDate",
                    compliance_level="complianceLevel",
                    enable_non_security=False,
                    patch_filter_group=ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterGroupProperty(
                        patch_filters=[ssm_mixins.CfnPatchBaselinePropsMixin.PatchFilterProperty(
                            key="key",
                            values=["values"]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1a5d6ff43db6455f5f654f90ad1947cee6cb76c6908b8442f3fbdd8940add40)
                check_type(argname="argument approve_after_days", value=approve_after_days, expected_type=type_hints["approve_after_days"])
                check_type(argname="argument approve_until_date", value=approve_until_date, expected_type=type_hints["approve_until_date"])
                check_type(argname="argument compliance_level", value=compliance_level, expected_type=type_hints["compliance_level"])
                check_type(argname="argument enable_non_security", value=enable_non_security, expected_type=type_hints["enable_non_security"])
                check_type(argname="argument patch_filter_group", value=patch_filter_group, expected_type=type_hints["patch_filter_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approve_after_days is not None:
                self._values["approve_after_days"] = approve_after_days
            if approve_until_date is not None:
                self._values["approve_until_date"] = approve_until_date
            if compliance_level is not None:
                self._values["compliance_level"] = compliance_level
            if enable_non_security is not None:
                self._values["enable_non_security"] = enable_non_security
            if patch_filter_group is not None:
                self._values["patch_filter_group"] = patch_filter_group

        @builtins.property
        def approve_after_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days after the release date of each patch matched by the rule that the patch is marked as approved in the patch baseline.

            For example, a value of ``7`` means that patches are approved seven days after they are released.

            Patch Manager evaluates patch release dates using Coordinated Universal Time (UTC). If the day represented by ``7`` is ``2025-11-16`` , patches released between ``2025-11-16T00:00:00Z`` and ``2025-11-16T23:59:59Z`` will be included in the approval.

            This parameter is marked as ``Required: No`` , but your request must include a value for either ``ApproveAfterDays`` or ``ApproveUntilDate`` .

            Not supported for Debian Server or Ubuntu Server.
            .. epigraph::

               Use caution when setting this value for Windows Server patch baselines. Because patch updates that are replaced by later updates are removed, setting too broad a value for this parameter can result in crucial patches not being installed. For more information, see the *Windows Server* tab in the topic `How security patches are selected <https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-selecting-patches.html>`_ in the *AWS Systems Manager User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-approveafterdays
            '''
            result = self._values.get("approve_after_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def approve_until_date(self) -> typing.Optional[builtins.str]:
            '''The cutoff date for auto approval of released patches.

            Any patches released on or before this date are installed automatically.

            Enter dates in the format ``YYYY-MM-DD`` . For example, ``2025-11-16`` .

            Patch Manager evaluates patch release dates using Coordinated Universal Time (UTC). If you enter the date ``2025-11-16`` , patches released between ``2025-11-16T00:00:00Z`` and ``2025-11-16T23:59:59Z`` will be included in the approval.

            This parameter is marked as ``Required: No`` , but your request must include a value for either ``ApproveUntilDate`` or ``ApproveAfterDays`` .

            Not supported for Debian Server or Ubuntu Server.
            .. epigraph::

               Use caution when setting this value for Windows Server patch baselines. Because patch updates that are replaced by later updates are removed, setting too broad a value for this parameter can result in crucial patches not being installed. For more information, see the *Windows Server* tab in the topic `How security patches are selected <https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-selecting-patches.html>`_ in the *AWS Systems Manager User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-approveuntildate
            '''
            result = self._values.get("approve_until_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def compliance_level(self) -> typing.Optional[builtins.str]:
            '''A compliance severity level for all approved patches in a patch baseline.

            Valid compliance severity levels include the following: ``UNSPECIFIED`` , ``CRITICAL`` , ``HIGH`` , ``MEDIUM`` , ``LOW`` , and ``INFORMATIONAL`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-compliancelevel
            '''
            result = self._values.get("compliance_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_non_security(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''For managed nodes identified by the approval rule filters, enables a patch baseline to apply non-security updates available in the specified repository.

            The default value is ``false`` . Applies to Linux managed nodes only.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-enablenonsecurity
            '''
            result = self._values.get("enable_non_security")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def patch_filter_group(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.PatchFilterGroupProperty"]]:
            '''The patch filter group that defines the criteria for the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-patchbaseline-rule.html#cfn-ssm-patchbaseline-rule-patchfiltergroup
            '''
            result = self._values.get("patch_filter_group")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPatchBaselinePropsMixin.PatchFilterGroupProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnResourceDataSyncMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "bucket_prefix": "bucketPrefix",
        "bucket_region": "bucketRegion",
        "kms_key_arn": "kmsKeyArn",
        "s3_destination": "s3Destination",
        "sync_format": "syncFormat",
        "sync_name": "syncName",
        "sync_source": "syncSource",
        "sync_type": "syncType",
    },
)
class CfnResourceDataSyncMixinProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_prefix: typing.Optional[builtins.str] = None,
        bucket_region: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        s3_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDataSyncPropsMixin.S3DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sync_format: typing.Optional[builtins.str] = None,
        sync_name: typing.Optional[builtins.str] = None,
        sync_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDataSyncPropsMixin.SyncSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sync_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourceDataSyncPropsMixin.

        :param bucket_name: The name of the S3 bucket where the aggregated data is stored.
        :param bucket_prefix: An Amazon S3 prefix for the bucket.
        :param bucket_region: The AWS Region with the S3 bucket targeted by the resource data sync.
        :param kms_key_arn: The Amazon Resource Name (ARN) of an encryption key for a destination in Amazon S3 . You can use a KMS key to encrypt inventory data in Amazon S3 . You must specify a key that exist in the same AWS Region as the destination Amazon S3 bucket.
        :param s3_destination: Configuration information for the target S3 bucket.
        :param sync_format: A supported sync format. The following format is currently supported: JsonSerDe
        :param sync_name: A name for the resource data sync.
        :param sync_source: Information about the source where the data was synchronized.
        :param sync_type: The type of resource data sync. If ``SyncType`` is ``SyncToDestination`` , then the resource data sync synchronizes data to an S3 bucket. If the ``SyncType`` is ``SyncFromSource`` then the resource data sync synchronizes data from AWS Organizations or from multiple AWS Regions .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
            
            cfn_resource_data_sync_mixin_props = ssm_mixins.CfnResourceDataSyncMixinProps(
                bucket_name="bucketName",
                bucket_prefix="bucketPrefix",
                bucket_region="bucketRegion",
                kms_key_arn="kmsKeyArn",
                s3_destination=ssm_mixins.CfnResourceDataSyncPropsMixin.S3DestinationProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    bucket_region="bucketRegion",
                    kms_key_arn="kmsKeyArn",
                    sync_format="syncFormat"
                ),
                sync_format="syncFormat",
                sync_name="syncName",
                sync_source=ssm_mixins.CfnResourceDataSyncPropsMixin.SyncSourceProperty(
                    aws_organizations_source=ssm_mixins.CfnResourceDataSyncPropsMixin.AwsOrganizationsSourceProperty(
                        organizational_units=["organizationalUnits"],
                        organization_source_type="organizationSourceType"
                    ),
                    include_future_regions=False,
                    source_regions=["sourceRegions"],
                    source_type="sourceType"
                ),
                sync_type="syncType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a736424ee96a2735d58cb4a4cb1dd523bccad28c3b82ca96b047602144a4905)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
            check_type(argname="argument bucket_region", value=bucket_region, expected_type=type_hints["bucket_region"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument s3_destination", value=s3_destination, expected_type=type_hints["s3_destination"])
            check_type(argname="argument sync_format", value=sync_format, expected_type=type_hints["sync_format"])
            check_type(argname="argument sync_name", value=sync_name, expected_type=type_hints["sync_name"])
            check_type(argname="argument sync_source", value=sync_source, expected_type=type_hints["sync_source"])
            check_type(argname="argument sync_type", value=sync_type, expected_type=type_hints["sync_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_prefix is not None:
            self._values["bucket_prefix"] = bucket_prefix
        if bucket_region is not None:
            self._values["bucket_region"] = bucket_region
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if s3_destination is not None:
            self._values["s3_destination"] = s3_destination
        if sync_format is not None:
            self._values["sync_format"] = sync_format
        if sync_name is not None:
            self._values["sync_name"] = sync_name
        if sync_source is not None:
            self._values["sync_source"] = sync_source
        if sync_type is not None:
            self._values["sync_type"] = sync_type

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the S3 bucket where the aggregated data is stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-bucketname
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_prefix(self) -> typing.Optional[builtins.str]:
        '''An Amazon S3 prefix for the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-bucketprefix
        '''
        result = self._values.get("bucket_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_region(self) -> typing.Optional[builtins.str]:
        '''The AWS Region with the S3 bucket targeted by the resource data sync.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-bucketregion
        '''
        result = self._values.get("bucket_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an encryption key for a destination in Amazon S3 .

        You can use a KMS key to encrypt inventory data in Amazon S3 . You must specify a key that exist in the same AWS Region as the destination Amazon S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_destination(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDataSyncPropsMixin.S3DestinationProperty"]]:
        '''Configuration information for the target S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-s3destination
        '''
        result = self._values.get("s3_destination")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDataSyncPropsMixin.S3DestinationProperty"]], result)

    @builtins.property
    def sync_format(self) -> typing.Optional[builtins.str]:
        '''A supported sync format.

        The following format is currently supported: JsonSerDe

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-syncformat
        '''
        result = self._values.get("sync_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_name(self) -> typing.Optional[builtins.str]:
        '''A name for the resource data sync.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-syncname
        '''
        result = self._values.get("sync_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDataSyncPropsMixin.SyncSourceProperty"]]:
        '''Information about the source where the data was synchronized.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-syncsource
        '''
        result = self._values.get("sync_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDataSyncPropsMixin.SyncSourceProperty"]], result)

    @builtins.property
    def sync_type(self) -> typing.Optional[builtins.str]:
        '''The type of resource data sync.

        If ``SyncType`` is ``SyncToDestination`` , then the resource data sync synchronizes data to an S3 bucket. If the ``SyncType`` is ``SyncFromSource`` then the resource data sync synchronizes data from AWS Organizations or from multiple AWS Regions .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html#cfn-ssm-resourcedatasync-synctype
        '''
        result = self._values.get("sync_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceDataSyncMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceDataSyncPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnResourceDataSyncPropsMixin",
):
    '''The ``AWS::SSM::ResourceDataSync`` resource creates, updates, or deletes a resource data sync for AWS Systems Manager .

    A resource data sync helps you view data from multiple sources in a single location. Systems Manager offers two types of resource data sync: ``SyncToDestination`` and ``SyncFromSource`` .

    You can configure Systems Manager Inventory to use the ``SyncToDestination`` type to synchronize Inventory data from multiple AWS Regions to a single Amazon S3 bucket.

    You can configure Systems Manager Explorer to use the ``SyncFromSource`` type to synchronize operational work items (OpsItems) and operational data (OpsData) from multiple AWS Regions . This type can synchronize OpsItems and OpsData from multiple AWS accounts and Regions or from an ``EntireOrganization`` by using AWS Organizations .

    A resource data sync is an asynchronous operation that returns immediately. After a successful initial sync is completed, the system continuously syncs data.

    By default, data is not encrypted in Amazon S3 . We strongly recommend that you enable encryption in Amazon S3 to ensure secure data storage. We also recommend that you secure access to the Amazon S3 bucket by creating a restrictive bucket policy.

    For more information, see `Configuring Inventory Collection <https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-inventory-configuring.html#sysman-inventory-datasync>`_ and `Setting Up Systems Manager Explorer to Display Data from Multiple Accounts and Regions <https://docs.aws.amazon.com/systems-manager/latest/userguide/Explorer-resource-data-sync.html>`_ in the *AWS Systems Manager User Guide* .
    .. epigraph::

       The following *Syntax* section shows all fields that are supported for a resource data sync. The *Examples* section below shows the recommended way to specify configurations for each sync type. Refer to the *Examples* section when you create your resource data sync.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcedatasync.html
    :cloudformationResource: AWS::SSM::ResourceDataSync
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
        
        cfn_resource_data_sync_props_mixin = ssm_mixins.CfnResourceDataSyncPropsMixin(ssm_mixins.CfnResourceDataSyncMixinProps(
            bucket_name="bucketName",
            bucket_prefix="bucketPrefix",
            bucket_region="bucketRegion",
            kms_key_arn="kmsKeyArn",
            s3_destination=ssm_mixins.CfnResourceDataSyncPropsMixin.S3DestinationProperty(
                bucket_name="bucketName",
                bucket_prefix="bucketPrefix",
                bucket_region="bucketRegion",
                kms_key_arn="kmsKeyArn",
                sync_format="syncFormat"
            ),
            sync_format="syncFormat",
            sync_name="syncName",
            sync_source=ssm_mixins.CfnResourceDataSyncPropsMixin.SyncSourceProperty(
                aws_organizations_source=ssm_mixins.CfnResourceDataSyncPropsMixin.AwsOrganizationsSourceProperty(
                    organizational_units=["organizationalUnits"],
                    organization_source_type="organizationSourceType"
                ),
                include_future_regions=False,
                source_regions=["sourceRegions"],
                source_type="sourceType"
            ),
            sync_type="syncType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceDataSyncMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSM::ResourceDataSync``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5abc563b92671b1c760dc2a666f004a52463b57c7fe1f70f41de3909b2ff05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__142561541e3f4fb02aa2e58d9f7eb9cbe2d251b72f9a4e66e1b40df58bd9593b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c1c5d1af9138ea1b525e658e517b25904ac29693bff39de112bedf6798f7ae)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceDataSyncMixinProps:
        return typing.cast(CfnResourceDataSyncMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnResourceDataSyncPropsMixin.AwsOrganizationsSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "organizational_units": "organizationalUnits",
            "organization_source_type": "organizationSourceType",
        },
    )
    class AwsOrganizationsSourceProperty:
        def __init__(
            self,
            *,
            organizational_units: typing.Optional[typing.Sequence[builtins.str]] = None,
            organization_source_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the ``AwsOrganizationsSource`` resource data sync source.

            A sync source of this type can synchronize data from AWS Organizations or, if an AWS organization isn't present, from multiple AWS Regions .

            :param organizational_units: The AWS Organizations organization units included in the sync.
            :param organization_source_type: If an AWS organization is present, this is either ``OrganizationalUnits`` or ``EntireOrganization`` . For ``OrganizationalUnits`` , the data is aggregated from a set of organization units. For ``EntireOrganization`` , the data is aggregated from the entire AWS organization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-awsorganizationssource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                aws_organizations_source_property = ssm_mixins.CfnResourceDataSyncPropsMixin.AwsOrganizationsSourceProperty(
                    organizational_units=["organizationalUnits"],
                    organization_source_type="organizationSourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9a9f496c8d7a0e1bf9d7c176ea82ac1fff0091db0e62240cb61aeec09dcb4cf)
                check_type(argname="argument organizational_units", value=organizational_units, expected_type=type_hints["organizational_units"])
                check_type(argname="argument organization_source_type", value=organization_source_type, expected_type=type_hints["organization_source_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if organizational_units is not None:
                self._values["organizational_units"] = organizational_units
            if organization_source_type is not None:
                self._values["organization_source_type"] = organization_source_type

        @builtins.property
        def organizational_units(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The AWS Organizations organization units included in the sync.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-awsorganizationssource.html#cfn-ssm-resourcedatasync-awsorganizationssource-organizationalunits
            '''
            result = self._values.get("organizational_units")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def organization_source_type(self) -> typing.Optional[builtins.str]:
            '''If an AWS organization is present, this is either ``OrganizationalUnits`` or ``EntireOrganization`` .

            For ``OrganizationalUnits`` , the data is aggregated from a set of organization units. For ``EntireOrganization`` , the data is aggregated from the entire AWS organization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-awsorganizationssource.html#cfn-ssm-resourcedatasync-awsorganizationssource-organizationsourcetype
            '''
            result = self._values.get("organization_source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsOrganizationsSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnResourceDataSyncPropsMixin.S3DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "bucket_region": "bucketRegion",
            "kms_key_arn": "kmsKeyArn",
            "sync_format": "syncFormat",
        },
    )
    class S3DestinationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            bucket_region: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
            sync_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the target S3 bucket for the resource data sync.

            :param bucket_name: The name of the S3 bucket where the aggregated data is stored.
            :param bucket_prefix: An Amazon S3 prefix for the bucket.
            :param bucket_region: The AWS Region with the S3 bucket targeted by the resource data sync.
            :param kms_key_arn: The ARN of an encryption key for a destination in Amazon S3. Must belong to the same Region as the destination S3 bucket.
            :param sync_format: A supported sync format. The following format is currently supported: JsonSerDe

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                s3_destination_property = ssm_mixins.CfnResourceDataSyncPropsMixin.S3DestinationProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    bucket_region="bucketRegion",
                    kms_key_arn="kmsKeyArn",
                    sync_format="syncFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bde99a29e26cc2a2d55a061067aca5086c035c2052ebb833391fd22df69b4c76)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument bucket_region", value=bucket_region, expected_type=type_hints["bucket_region"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument sync_format", value=sync_format, expected_type=type_hints["sync_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if bucket_region is not None:
                self._values["bucket_region"] = bucket_region
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if sync_format is not None:
                self._values["sync_format"] = sync_format

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket where the aggregated data is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''An Amazon S3 prefix for the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region with the S3 bucket targeted by the resource data sync.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-bucketregion
            '''
            result = self._values.get("bucket_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an encryption key for a destination in Amazon S3.

            Must belong to the same Region as the destination S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sync_format(self) -> typing.Optional[builtins.str]:
            '''A supported sync format.

            The following format is currently supported: JsonSerDe

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-s3destination.html#cfn-ssm-resourcedatasync-s3destination-syncformat
            '''
            result = self._values.get("sync_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnResourceDataSyncPropsMixin.SyncSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_organizations_source": "awsOrganizationsSource",
            "include_future_regions": "includeFutureRegions",
            "source_regions": "sourceRegions",
            "source_type": "sourceType",
        },
    )
    class SyncSourceProperty:
        def __init__(
            self,
            *,
            aws_organizations_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceDataSyncPropsMixin.AwsOrganizationsSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            include_future_regions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            source_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the source of the data included in the resource data sync.

            :param aws_organizations_source: Information about the AwsOrganizationsSource resource data sync source. A sync source of this type can synchronize data from AWS Organizations .
            :param include_future_regions: Whether to automatically synchronize and aggregate data from new AWS Regions when those Regions come online.
            :param source_regions: The ``SyncSource`` AWS Regions included in the resource data sync.
            :param source_type: The type of data source for the resource data sync. ``SourceType`` is either ``AwsOrganizations`` (if an organization is present in AWS Organizations ) or ``SingleAccountMultiRegions`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
                
                sync_source_property = ssm_mixins.CfnResourceDataSyncPropsMixin.SyncSourceProperty(
                    aws_organizations_source=ssm_mixins.CfnResourceDataSyncPropsMixin.AwsOrganizationsSourceProperty(
                        organizational_units=["organizationalUnits"],
                        organization_source_type="organizationSourceType"
                    ),
                    include_future_regions=False,
                    source_regions=["sourceRegions"],
                    source_type="sourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a596c72c56950a2238b583ba4d5e1ebd0a6d5846f4834c0d689ced979a42a26)
                check_type(argname="argument aws_organizations_source", value=aws_organizations_source, expected_type=type_hints["aws_organizations_source"])
                check_type(argname="argument include_future_regions", value=include_future_regions, expected_type=type_hints["include_future_regions"])
                check_type(argname="argument source_regions", value=source_regions, expected_type=type_hints["source_regions"])
                check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_organizations_source is not None:
                self._values["aws_organizations_source"] = aws_organizations_source
            if include_future_regions is not None:
                self._values["include_future_regions"] = include_future_regions
            if source_regions is not None:
                self._values["source_regions"] = source_regions
            if source_type is not None:
                self._values["source_type"] = source_type

        @builtins.property
        def aws_organizations_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDataSyncPropsMixin.AwsOrganizationsSourceProperty"]]:
            '''Information about the AwsOrganizationsSource resource data sync source.

            A sync source of this type can synchronize data from AWS Organizations .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html#cfn-ssm-resourcedatasync-syncsource-awsorganizationssource
            '''
            result = self._values.get("aws_organizations_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceDataSyncPropsMixin.AwsOrganizationsSourceProperty"]], result)

        @builtins.property
        def include_future_regions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to automatically synchronize and aggregate data from new AWS Regions when those Regions come online.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html#cfn-ssm-resourcedatasync-syncsource-includefutureregions
            '''
            result = self._values.get("include_future_regions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def source_regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ``SyncSource`` AWS Regions included in the resource data sync.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html#cfn-ssm-resourcedatasync-syncsource-sourceregions
            '''
            result = self._values.get("source_regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            '''The type of data source for the resource data sync.

            ``SourceType`` is either ``AwsOrganizations`` (if an organization is present in AWS Organizations ) or ``SingleAccountMultiRegions`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssm-resourcedatasync-syncsource.html#cfn-ssm-resourcedatasync-syncsource-sourcetype
            '''
            result = self._values.get("source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SyncSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_arn": "resourceArn"},
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        policy: typing.Any = None,
        resource_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param policy: A policy you want to associate with a resource.
        :param resource_arn: The Amazon Resource Name (ARN) of the resource to which you want to attach a policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
            
            # policy: Any
            
            cfn_resource_policy_mixin_props = ssm_mixins.CfnResourcePolicyMixinProps(
                policy=policy,
                resource_arn="resourceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8deb55ef2df04fdf2d2263b6bfb38300fc04dd48fa01e154acc271cce50300f4)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn

    @builtins.property
    def policy(self) -> typing.Any:
        '''A policy you want to associate with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcepolicy.html#cfn-ssm-resourcepolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resource to which you want to attach a policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcepolicy.html#cfn-ssm-resourcepolicy-resourcearn
        '''
        result = self._values.get("resource_arn")
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
    jsii_type="@aws-cdk/mixins-preview.aws_ssm.mixins.CfnResourcePolicyPropsMixin",
):
    '''Creates or updates a Systems Manager resource policy.

    A resource policy helps you to define the IAM entity (for example, an AWS account ) that can manage your Systems Manager resources. Currently, ``OpsItemGroup`` is the only resource that supports Systems Manager resource policies. The resource policy for ``OpsItemGroup`` enables AWS accounts to view and interact with OpsCenter operational work items (OpsItems). OpsCenter is a tool in Systems Manager .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-resourcepolicy.html
    :cloudformationResource: AWS::SSM::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssm import mixins as ssm_mixins
        
        # policy: Any
        
        cfn_resource_policy_props_mixin = ssm_mixins.CfnResourcePolicyPropsMixin(ssm_mixins.CfnResourcePolicyMixinProps(
            policy=policy,
            resource_arn="resourceArn"
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
        '''Create a mixin to apply properties to ``AWS::SSM::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603bb3035acd2ae76e37cf91b1fa3255e4a1cb41abc44b9c267746fe966a63a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8175030cab65ed3ca672bb7e38f73ea722e5f3f8540aa85f16f3b13b4274f733)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790ef9373a123a0e1a6a848f9da28edbdafc1d43be1b3e40554c0fc3f312561f)
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


__all__ = [
    "CfnAssociationMixinProps",
    "CfnAssociationPropsMixin",
    "CfnDocumentMixinProps",
    "CfnDocumentPropsMixin",
    "CfnMaintenanceWindowMixinProps",
    "CfnMaintenanceWindowPropsMixin",
    "CfnMaintenanceWindowTargetMixinProps",
    "CfnMaintenanceWindowTargetPropsMixin",
    "CfnMaintenanceWindowTaskMixinProps",
    "CfnMaintenanceWindowTaskPropsMixin",
    "CfnParameterMixinProps",
    "CfnParameterPropsMixin",
    "CfnPatchBaselineMixinProps",
    "CfnPatchBaselinePropsMixin",
    "CfnResourceDataSyncMixinProps",
    "CfnResourceDataSyncPropsMixin",
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
]

publication.publish()

def _typecheckingstub__237e10943445760b75f55cdb0541f55052f71657b70d772dd866a04ab57513cf(
    *,
    apply_only_at_cron_interval: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    association_name: typing.Optional[builtins.str] = None,
    automation_target_parameter_name: typing.Optional[builtins.str] = None,
    calendar_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    compliance_severity: typing.Optional[builtins.str] = None,
    document_version: typing.Optional[builtins.str] = None,
    instance_id: typing.Optional[builtins.str] = None,
    max_concurrency: typing.Optional[builtins.str] = None,
    max_errors: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    output_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.InstanceAssociationOutputLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameters: typing.Any = None,
    schedule_expression: typing.Optional[builtins.str] = None,
    schedule_offset: typing.Optional[jsii.Number] = None,
    sync_compliance: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.TargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    wait_for_success_timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef7239a34cf2c04cdc979bf72d3aefc65b2032a4513efa4828a4c016c34f3f5(
    props: typing.Union[CfnAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e1200633f9c85b8f82c01cee343d0b5add4d3539536c518f80cc581cdaf4e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5aa56aab0de65e2006b16c18b20216f36afa43f831e4101ebba0209a70edde(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f022ac6e7db47f2a2087a86176a91aa8105cc9ad9c47a3d1a4d187ab367b4bcb(
    *,
    s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssociationPropsMixin.S3OutputLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2de6ab18cc5ae748fb31dc82400281ee33905140bf309eb7138746716f78b9(
    *,
    output_s3_bucket_name: typing.Optional[builtins.str] = None,
    output_s3_key_prefix: typing.Optional[builtins.str] = None,
    output_s3_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c839f6fd4381378868d2885eea7f45688dd0b110bbfbd7911e03354086737f(
    *,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b3156f6822f24d51787d10f3b2a4be3cc8c9db409872be40ce5330d060eb55(
    *,
    attachments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDocumentPropsMixin.AttachmentsSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    content: typing.Any = None,
    document_format: typing.Optional[builtins.str] = None,
    document_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    requires: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDocumentPropsMixin.DocumentRequiresProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_type: typing.Optional[builtins.str] = None,
    update_method: typing.Optional[builtins.str] = None,
    version_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328d0637df58f5d44d6a1d8ffa5ed10890456ce95a38ae4980b3b5778d492805(
    props: typing.Union[CfnDocumentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a6a0f764ee7002c98fb8289b6fd2320b122ea51d9dd5d75db7100fb29dc45e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6edb37bdd487b2b1fad069c510dab4731285e14c8a4c93a212a4de4c264c492(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a2953f7a288bd92d78b3535a6aacbd4beb84c23cef557d1b57b959f558ff63(
    *,
    key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83dddb128ea59994df081c4a9f3bc414748bf47341a3564f06486c99d6131b60(
    *,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb00a90bb49285cb6cda21fa7f42015d755a7022319000416f09d2cbbb36229(
    *,
    allow_unassociated_targets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    cutoff: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    duration: typing.Optional[jsii.Number] = None,
    end_date: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    schedule_offset: typing.Optional[jsii.Number] = None,
    schedule_timezone: typing.Optional[builtins.str] = None,
    start_date: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b878a6571d4bd09f090a8296169df5fcfa3c825c69d08d71e06e155e92e1237(
    props: typing.Union[CfnMaintenanceWindowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81fa8c91cb74a1aba3c05a739ebb96e162072d3ff2bce9afb8c7bf5c3f9be93(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74269da83810d1a884979ab661d35b1710cf578f6f531cc8c0c0de540917d33b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3bad47b3d001408f796cabaf23f89432c7922ade7eafedf8217cc812bdcddec(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner_information: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTargetPropsMixin.TargetsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    window_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e2d7e04e8085178df58e178e0af0f23afbdcb4b824a7f504898fc76572c4cc(
    props: typing.Union[CfnMaintenanceWindowTargetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9bbd4b6162bcdaab7436c660142881e6caead051024d3c8d8a1202594df9a7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94af1a6ee85b44c849e4202248da6b0be02916cb3132ba911a53f88d5f701f02(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34aedd0978f76f8ba5595844e354384d81f6adf737b8d48e28b8ae7f06b258b8(
    *,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a02d9ae989a99922d8c20aa70332bbca5a3b6bae8fcbd4e51bb00ad049d6c91(
    *,
    cutoff_behavior: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    logging_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTaskPropsMixin.LoggingInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_concurrency: typing.Optional[builtins.str] = None,
    max_errors: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTaskPropsMixin.TargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    task_arn: typing.Optional[builtins.str] = None,
    task_invocation_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTaskPropsMixin.TaskInvocationParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_parameters: typing.Any = None,
    task_type: typing.Optional[builtins.str] = None,
    window_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ddcb054f72d1febc2d453c908c26ba0846b9857386d8e1586accedb12455033(
    props: typing.Union[CfnMaintenanceWindowTaskMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9024c9bbb127b6f07670ea32fa31988cfd9b8a6c40525e994b0e33cd89598d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08862be412f7046aea50da93885dd2df69cd4d1139484a3f2720edaf823b56b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb9f5882685186ebc9c2608126233a577b2ff3c64db1c2a063d9e612f4583d4(
    *,
    cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
    cloud_watch_output_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce31eccd03df75ed4002dcc39662ab329ff3888e9154f1ce73263a7736e91ce1(
    *,
    region: typing.Optional[builtins.str] = None,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ce5abb429327c99b22c0ea934b12796ab62f9c8f3dd7b5dad9286053fbbfa3(
    *,
    document_version: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2cca521862d2c2ff42dcf494a3a5f795a9347ca061cc8b9fcb98b02912b572(
    *,
    client_context: typing.Optional[builtins.str] = None,
    payload: typing.Optional[builtins.str] = None,
    qualifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95cf7ce26230c6225059e32b81aaa0a600c0f84124bff555b3b1b7ae4b3e3ed8(
    *,
    cloud_watch_output_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTaskPropsMixin.CloudWatchOutputConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    document_hash: typing.Optional[builtins.str] = None,
    document_hash_type: typing.Optional[builtins.str] = None,
    document_version: typing.Optional[builtins.str] = None,
    notification_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTaskPropsMixin.NotificationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    output_s3_bucket_name: typing.Optional[builtins.str] = None,
    output_s3_key_prefix: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    service_role_arn: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5635767fb55f0832bc70b49f1ed74758e33802a63fa33dc8b7fbb9ed31996e8b(
    *,
    input: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfa1c003d4c01e5180d8b406d458ae04d7397cac92bb91ba18e6e953dbcb253(
    *,
    notification_arn: typing.Optional[builtins.str] = None,
    notification_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    notification_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb11e06c6e5faca943765f6bb2e5c3e1ce01190dc467e752e8f91028c9867876(
    *,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da427e718906b6a7041417cdc4a65ddd9bb12d6bef75266389c644d547e80d1b(
    *,
    maintenance_window_automation_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowAutomationParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maintenance_window_lambda_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowLambdaParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maintenance_window_run_command_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowRunCommandParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maintenance_window_step_functions_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMaintenanceWindowTaskPropsMixin.MaintenanceWindowStepFunctionsParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3200d2546f786b8279189677af1b9b028c21a94fc18ff28e03e79a12cddfe5(
    *,
    allowed_pattern: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policies: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tier: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449a24370b660ac8c714a3cd1177e6ea5891369c619578b02f87bc131125825d(
    props: typing.Union[CfnParameterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2798d459a3a0bfd521995b390921aa4756015386a25f986cc969f8be9e850388(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed17a0f9995ef4b5920ba9e67f3aeb77de97df3852d4ad8aab59444290391fe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966a6783d92096bb4b3f576bc68e3ff3211ba3ef759c338392ded72d30ffb6df(
    *,
    approval_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPatchBaselinePropsMixin.RuleGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    approved_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
    approved_patches_compliance_level: typing.Optional[builtins.str] = None,
    approved_patches_enable_non_security: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    available_security_updates_compliance_status: typing.Optional[builtins.str] = None,
    default_baseline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    global_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPatchBaselinePropsMixin.PatchFilterGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    operating_system: typing.Optional[builtins.str] = None,
    patch_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    rejected_patches: typing.Optional[typing.Sequence[builtins.str]] = None,
    rejected_patches_action: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPatchBaselinePropsMixin.PatchSourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2a2324ac64be0d38fa6a05fdd473bf1c6ff4acf8f5e9b3b7977a432c4d085a(
    props: typing.Union[CfnPatchBaselineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5a6eebf31980a352d94ca8cd8ea5895e71ea2970919423c0a142616f6caf04(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cda3936807b9e9080f40f697d2a404802db4658f16fa50f6a508a8790e43d51(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a623dcc484fa5af0b2adfd92911cfc120fddfd8aee73e7cd620bcbf26b8774a9(
    *,
    patch_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPatchBaselinePropsMixin.PatchFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e1c5fcef15226e878845215765bb25c876a8b353c1b4699bdd8200b0168b63(
    *,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869ea368f29938b8034592b9bcf91f7555a5903059ceea893ee631183fbb4cfe(
    *,
    configuration: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    products: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a83f81319b0664e874ee904bdd73e4447949b65e14bc4cb88fcd35cd1d43f01(
    *,
    patch_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPatchBaselinePropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a5d6ff43db6455f5f654f90ad1947cee6cb76c6908b8442f3fbdd8940add40(
    *,
    approve_after_days: typing.Optional[jsii.Number] = None,
    approve_until_date: typing.Optional[builtins.str] = None,
    compliance_level: typing.Optional[builtins.str] = None,
    enable_non_security: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    patch_filter_group: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPatchBaselinePropsMixin.PatchFilterGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a736424ee96a2735d58cb4a4cb1dd523bccad28c3b82ca96b047602144a4905(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    bucket_region: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    s3_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDataSyncPropsMixin.S3DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sync_format: typing.Optional[builtins.str] = None,
    sync_name: typing.Optional[builtins.str] = None,
    sync_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDataSyncPropsMixin.SyncSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sync_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5abc563b92671b1c760dc2a666f004a52463b57c7fe1f70f41de3909b2ff05(
    props: typing.Union[CfnResourceDataSyncMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142561541e3f4fb02aa2e58d9f7eb9cbe2d251b72f9a4e66e1b40df58bd9593b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c1c5d1af9138ea1b525e658e517b25904ac29693bff39de112bedf6798f7ae(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a9f496c8d7a0e1bf9d7c176ea82ac1fff0091db0e62240cb61aeec09dcb4cf(
    *,
    organizational_units: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_source_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde99a29e26cc2a2d55a061067aca5086c035c2052ebb833391fd22df69b4c76(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    bucket_region: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    sync_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a596c72c56950a2238b583ba4d5e1ebd0a6d5846f4834c0d689ced979a42a26(
    *,
    aws_organizations_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceDataSyncPropsMixin.AwsOrganizationsSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_future_regions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    source_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8deb55ef2df04fdf2d2263b6bfb38300fc04dd48fa01e154acc271cce50300f4(
    *,
    policy: typing.Any = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603bb3035acd2ae76e37cf91b1fa3255e4a1cb41abc44b9c267746fe966a63a1(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8175030cab65ed3ca672bb7e38f73ea722e5f3f8540aa85f16f3b13b4274f733(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790ef9373a123a0e1a6a848f9da28edbdafc1d43be1b3e40554c0fc3f312561f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
