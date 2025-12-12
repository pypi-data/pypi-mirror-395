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
import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnAccountMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_name": "accountName",
        "email": "email",
        "parent_ids": "parentIds",
        "role_name": "roleName",
        "tags": "tags",
    },
)
class CfnAccountMixinProps:
    def __init__(
        self,
        *,
        account_name: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        parent_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccountPropsMixin.

        :param account_name: The account name given to the account when it was created.
        :param email: The email address associated with the AWS account. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ for this parameter is a string of characters that represents a standard internet email address.
        :param parent_ids: The unique identifier (ID) of the root or organizational unit (OU) that you want to create the new account in. If you don't specify this parameter, the ``ParentId`` defaults to the root ID. This parameter only accepts a string array with one string value. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ for a parent ID string requires one of the following: - *Root* - A string that begins with "r-" followed by from 4 to 32 lowercase letters or digits. - *Organizational unit (OU)* - A string that begins with "ou-" followed by from 4 to 32 lowercase letters or digits (the ID of the root that the OU is in). This string is followed by a second "-" dash and from 8 to 32 additional lowercase letters or digits.
        :param role_name: The name of an IAM role that AWS Organizations automatically preconfigures in the new member account. This role trusts the management account, allowing users in the management account to assume the role, as permitted by the management account administrator. The role has administrator permissions in the new member account. If you don't specify this parameter, the role name defaults to ``OrganizationAccountAccessRole`` . For more information about how to use this role to access the member account, see the following links: - `Creating the OrganizationAccountAccessRole in an invited member account <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html#orgs_manage_accounts_create-cross-account-role>`_ in the *AWS Organizations User Guide* - Steps 2 and 3 in `IAM Tutorial: Delegate access across AWS accounts using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html>`_ in the *IAM User Guide* The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ that is used to validate this parameter. The pattern can include uppercase letters, lowercase letters, digits with no spaces, and any of the following characters: =,.@- Default: - "OrganizationAccountAccessRole"
        :param tags: A list of tags that you want to attach to the newly created account. For each tag in the list, you must specify both a tag key and a value. You can set the value to an empty string, but you can't set it to ``null`` . For more information about tagging, see `Tagging AWS Organizations resources <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tagging.html>`_ in the AWS Organizations User Guide. .. epigraph:: If any one of the tags is not valid or if you exceed the maximum allowed number of tags for an account, then the entire request fails and the account is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-account.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
            
            cfn_account_mixin_props = organizations_mixins.CfnAccountMixinProps(
                account_name="accountName",
                email="email",
                parent_ids=["parentIds"],
                role_name="roleName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f09f23d3cb98afe35c104d8b30e816b3c843b6c86f6398ea30cc34c34ac63257)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument parent_ids", value=parent_ids, expected_type=type_hints["parent_ids"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_name is not None:
            self._values["account_name"] = account_name
        if email is not None:
            self._values["email"] = email
        if parent_ids is not None:
            self._values["parent_ids"] = parent_ids
        if role_name is not None:
            self._values["role_name"] = role_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def account_name(self) -> typing.Optional[builtins.str]:
        '''The account name given to the account when it was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-account.html#cfn-organizations-account-accountname
        '''
        result = self._values.get("account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''The email address associated with the AWS account.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ for this parameter is a string of characters that represents a standard internet email address.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-account.html#cfn-organizations-account-email
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifier (ID) of the root or organizational unit (OU) that you want to create the new account in.

        If you don't specify this parameter, the ``ParentId`` defaults to the root ID.

        This parameter only accepts a string array with one string value.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ for a parent ID string requires one of the following:

        - *Root* - A string that begins with "r-" followed by from 4 to 32 lowercase letters or digits.
        - *Organizational unit (OU)* - A string that begins with "ou-" followed by from 4 to 32 lowercase letters or digits (the ID of the root that the OU is in). This string is followed by a second "-" dash and from 8 to 32 additional lowercase letters or digits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-account.html#cfn-organizations-account-parentids
        '''
        result = self._values.get("parent_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''The name of an IAM role that AWS Organizations automatically preconfigures in the new member account.

        This role trusts the management account, allowing users in the management account to assume the role, as permitted by the management account administrator. The role has administrator permissions in the new member account.

        If you don't specify this parameter, the role name defaults to ``OrganizationAccountAccessRole`` .

        For more information about how to use this role to access the member account, see the following links:

        - `Creating the OrganizationAccountAccessRole in an invited member account <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html#orgs_manage_accounts_create-cross-account-role>`_ in the *AWS Organizations User Guide*
        - Steps 2 and 3 in `IAM Tutorial: Delegate access across AWS accounts using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html>`_ in the *IAM User Guide*

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ that is used to validate this parameter. The pattern can include uppercase letters, lowercase letters, digits with no spaces, and any of the following characters: =,.@-

        :default: - "OrganizationAccountAccessRole"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-account.html#cfn-organizations-account-rolename
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that you want to attach to the newly created account.

        For each tag in the list, you must specify both a tag key and a value. You can set the value to an empty string, but you can't set it to ``null`` . For more information about tagging, see `Tagging AWS Organizations resources <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tagging.html>`_ in the AWS Organizations User Guide.
        .. epigraph::

           If any one of the tags is not valid or if you exceed the maximum allowed number of tags for an account, then the entire request fails and the account is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-account.html#cfn-organizations-account-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnAccountPropsMixin",
):
    '''Creates an AWS account that is automatically a member of the organization whose credentials made the request.

    CloudFormation uses the ```CreateAccount`` <https://docs.aws.amazon.com/organizations/latest/APIReference/API_CreateAccount.html>`_ operation to create accounts. This is an asynchronous request that AWS performs in the background. Because ``CreateAccount`` operates asynchronously, it can return a successful completion message even though account initialization might still be in progress. You might need to wait a few minutes before you can successfully access the account. To check the status of the request, do one of the following:

    - Use the ``Id`` value of the ``CreateAccountStatus`` response element from the ``CreateAccount`` operation to provide as a parameter to the ```DescribeCreateAccountStatus`` <https://docs.aws.amazon.com/organizations/latest/APIReference/API_DescribeCreateAccountStatus.html>`_ operation.
    - Check the CloudTrail log for the ``CreateAccountResult`` event. For information on using CloudTrail with AWS Organizations , see `Logging and monitoring in AWS Organizations <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_security_incident-response.html#orgs_cloudtrail-integration>`_ in the *AWS Organizations User Guide* .

    The user who calls the API to create an account must have the ``organizations:CreateAccount`` permission. If you enabled all features in the organization, AWS Organizations creates the required service-linked role named ``AWSServiceRoleForOrganizations`` . For more information, see `AWS Organizations and service-linked roles <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_services.html#orgs_integrate_services-using_slrs>`_ in the *AWS Organizations User Guide* .

    If the request includes tags, then the requester must have the ``organizations:TagResource`` permission.

    AWS Organizations preconfigures the new member account with a role (named ``OrganizationAccountAccessRole`` by default) that grants users in the management account administrator permissions in the new member account. Principals in the management account can assume the role. AWS Organizations clones the company name and address information for the new account from the organization's management account.

    For more information about creating accounts, see `Creating a member account in your organization <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_create.html>`_ in the *AWS Organizations User Guide* .

    This operation can be called only from the organization's management account.

    *Deleting Account resources*

    The default ``DeletionPolicy`` for resource ``AWS::Organizations::Account`` is ``Retain`` . For more information about how CloudFormation deletes resources, see `DeletionPolicy Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .
    .. epigraph::

       - If you include multiple accounts in a single template, you must use the ``DependsOn`` attribute on each account resource type so that the accounts are created sequentially. If you create multiple accounts at the same time, Organizations returns an error and the stack operation fails.
       - You can't modify the following list of ``Account`` resource parameters using CloudFormation updates.
       - AccountName
       - Email
       - RoleName

       If you attempt to update the listed parameters, CloudFormation will attempt the update, but you will receive an error message as those updates are not supported from an Organizations management account or a `registered delegated administrator <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-delegated-admin.html>`_ account. Both the update and the update roll-back will fail, so you must skip the account resource update. To update parameters ``AccountName`` and ``Email`` , you must sign in to the AWS Management Console as the AWS account root user. For more information, see `Update the AWS account name, email address, or password for the root user <https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-update-root-user.html>`_ in the *Account Management Reference Guide* .

       - When you create an account in an organization using the AWS Organizations console, API, or AWS CLI commands, we don't automatically collect the information required for the account to operate as a standalone account. That includes collecting the payment method and signing the end user license agreement (EULA). If you must remove an account from your organization later, you can do so only after you provide the missing information. For more information, see `Considerations before removing an account from an organization <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_account-before-remove.html>`_ in the *AWS Organizations User Guide* .
       - When you create an account in an organization using CloudFormation , you can't specify a value for the ``CreateAccount`` operation parameter ``IamUserAccessToBilling`` . The default value for parameter ``IamUserAccessToBilling`` is ``ALLOW`` , and IAM users and roles with the required permissions can access billing information for the new account.
       - If you get an exception that indicates ``DescribeCreateAccountStatus returns IN_PROGRESS state before time out`` . You must check the account creation status using the ```DescribeCreateAccountStatus`` <https://docs.aws.amazon.com/organizations/latest/APIReference/API_DescribeCreateAccountStatus.html>`_ operation. If the account state returns as ``SUCCEEDED`` , you can import the account into CloudFormation management using ```resource import`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import.html>`_ .
       - If you get an exception that indicates you have exceeded your account quota for the organization, you can request an increase by using the `Service Quotas console <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html>`_ .
       - If you get an exception that indicates the operation failed because your organization is still initializing, wait one hour and then try again. If the error persists, contact `AWS Support <https://docs.aws.amazon.com/support/home#/>`_ .
       - We don't recommend that you use the ``CreateAccount`` operation to create multiple temporary accounts. You can close accounts using the ```CloseAccount`` <https://docs.aws.amazon.com/organizations/latest/APIReference/API_CloseAccount.html>`_ operation or from the AWS Organizations console in the organization's management account. For information on the requirements and process for closing an account, see `Closing a member account in your organization <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_close.html>`_ in the *AWS Organizations User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-account.html
    :cloudformationResource: AWS::Organizations::Account
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        cfn_account_props_mixin = organizations_mixins.CfnAccountPropsMixin(organizations_mixins.CfnAccountMixinProps(
            account_name="accountName",
            email="email",
            parent_ids=["parentIds"],
            role_name="roleName",
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
        props: typing.Union[CfnAccountMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Organizations::Account``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1353fbd8b0533a2f3c3c3fa868b3f034bf4910ba55f09e67a224dcd4fada6d78)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bfe93aedc2e50d3d3453b79a91ffa5c63a3703ef69821d5c1987551383ed4af)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111cd040093c584df164c2bf2b2a9b218eaab4a31ed8ea0d72f2ae05b9d6c0e5)
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


class CfnOrganizationAccessControlLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationAccessControlLogs",
):
    '''Builder for CfnOrganizationLogsMixin to generate ACCESS_CONTROL_LOGS for CfnOrganization.

    :cloudformationResource: AWS::Organizations::Organization
    :logType: ACCESS_CONTROL_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        cfn_organization_access_control_logs = organizations_mixins.CfnOrganizationAccessControlLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnOrganizationLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c75c9965f031f93de06df251e2e219a07b532ab416835deb31171d7798ccfa5)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnOrganizationLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnOrganizationLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1b92f0ca0c7e591a62ec68333f8529277e2c3dad616987e25edefe365954c8)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnOrganizationLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnOrganizationLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47cc864281ecacf0cefb6f08b77c5fad9d3ff87f453506d86ebb137c1205d080)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnOrganizationLogsMixin", jsii.invoke(self, "toS3", [bucket]))


class CfnOrganizationAuthenticationLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationAuthenticationLogs",
):
    '''Builder for CfnOrganizationLogsMixin to generate AUTHENTICATION_LOGS for CfnOrganization.

    :cloudformationResource: AWS::Organizations::Organization
    :logType: AUTHENTICATION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        cfn_organization_authentication_logs = organizations_mixins.CfnOrganizationAuthenticationLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnOrganizationLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d570aa7966afe8ce2c51babecbb24fe2967cd77697ea05cf438d54b70a94498d)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnOrganizationLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnOrganizationLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183d14714684762752848cb68f5e5668bba6783f1e73a0d0ab06d549bae8bffd)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnOrganizationLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnOrganizationLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe2cd0cc98f883c4605dedc05cb63c1ca21ed3f214eed05f5ca3a977f74b778)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnOrganizationLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationLogsMixin",
):
    '''Creates an AWS organization.

    The account whose user is calling the ```CreateOrganization`` <https://docs.aws.amazon.com/organizations/latest/APIReference/API_CreateOrganization.html>`_ operation automatically becomes the `management account <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html#account>`_ of the new organization.

    This operation must be called using credentials from the account that is to become the new organization's management account. The principal must also have the `relevant IAM permissions <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_org_create.html>`_ .
    .. epigraph::

       - If you delete an organization, you can't recover it. If you created any policies inside of the organization, they're also deleted and you can't recover them.
       - You can delete an organization only after you remove all member accounts from the organization. If you created some of your member accounts using AWS Organizations , you might be blocked from removing those accounts. You can remove a member account only if it has all the information that's required to operate as a standalone AWS account. For more information about how to provide that information and then remove the account, see `Leave an organization from your member account <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_leave-as-member.html>`_ in the *AWS Organizations User Guide* .
       - If you closed a member account before you remove it from the organization, it enters a 'suspended' state for a period of time and you can't remove the account from the organization until it is finally closed. This can take up to 90 days and can prevent you from deleting the organization until all member accounts are completely closed.

       For more information, see `Deleting an organization <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_org_delete.html>`_ in the *AWS Organizations User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-organization.html
    :cloudformationResource: AWS::Organizations::Organization
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_organization_logs_mixin = organizations_mixins.CfnOrganizationLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::Organizations::Organization``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6f2b1d166e4c6adac315bf6d8077552c715af90c9c9edf21ce66bf84446f59)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d169d4803ec52bf91f38e255df25c9e94f4d91fe13cde26a73b231434918e720)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c526ab69b7ea47bcfb35b16947ca682cc6494be8be24fdc0735ee25bdd0b215d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCESS_CONTROL_LOGS")
    def ACCESS_CONTROL_LOGS(cls) -> CfnOrganizationAccessControlLogs:
        return typing.cast(CfnOrganizationAccessControlLogs, jsii.sget(cls, "ACCESS_CONTROL_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AUTHENTICATION_LOGS")
    def AUTHENTICATION_LOGS(cls) -> CfnOrganizationAuthenticationLogs:
        return typing.cast(CfnOrganizationAuthenticationLogs, jsii.sget(cls, "AUTHENTICATION_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WORKMAIL_AVAILABILITY_PROVIDER_LOGS")
    def WORKMAIL_AVAILABILITY_PROVIDER_LOGS(
        cls,
    ) -> "CfnOrganizationWorkmailAvailabilityProviderLogs":
        return typing.cast("CfnOrganizationWorkmailAvailabilityProviderLogs", jsii.sget(cls, "WORKMAIL_AVAILABILITY_PROVIDER_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WORKMAIL_MAILBOX_ACCESS_LOGS")
    def WORKMAIL_MAILBOX_ACCESS_LOGS(cls) -> "CfnOrganizationWorkmailMailboxAccessLogs":
        return typing.cast("CfnOrganizationWorkmailMailboxAccessLogs", jsii.sget(cls, "WORKMAIL_MAILBOX_ACCESS_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WORKMAIL_PERSONAL_ACCESS_TOKEN_LOGS")
    def WORKMAIL_PERSONAL_ACCESS_TOKEN_LOGS(
        cls,
    ) -> "CfnOrganizationWorkmailPersonalAccessTokenLogs":
        return typing.cast("CfnOrganizationWorkmailPersonalAccessTokenLogs", jsii.sget(cls, "WORKMAIL_PERSONAL_ACCESS_TOKEN_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"feature_set": "featureSet"},
)
class CfnOrganizationMixinProps:
    def __init__(self, *, feature_set: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnOrganizationPropsMixin.

        :param feature_set: Specifies the feature set supported by the new organization. Each feature set supports different levels of functionality. - ``ALL`` In addition to all the features supported by the consolidated billing feature set, the management account gains access to advanced features that give you more control over accounts in your organization. For more information, see `All features <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html#feature-set-all>`_ in the *AWS Organizations User Guide* . - ``CONSOLIDATED_BILLING`` All member accounts have their bills consolidated to and paid by the management account. For more information, see `Consolidated billing <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html#feature-set-cb-only>`_ in the *AWS Organizations User Guide* . .. epigraph:: The consolidated billing feature feature set isn't available for organizations in the AWS GovCloud (US) Region. If you don't specify this property, the default value is ``ALL`` . Default: - "ALL"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-organization.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
            
            cfn_organization_mixin_props = organizations_mixins.CfnOrganizationMixinProps(
                feature_set="featureSet"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bafcea6e59f0f0e81fc60013eafb74681a447ba66f05dd9a5543152d64c108bf)
            check_type(argname="argument feature_set", value=feature_set, expected_type=type_hints["feature_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if feature_set is not None:
            self._values["feature_set"] = feature_set

    @builtins.property
    def feature_set(self) -> typing.Optional[builtins.str]:
        '''Specifies the feature set supported by the new organization. Each feature set supports different levels of functionality.

        - ``ALL``  In addition to all the features supported by the consolidated billing feature set, the management account gains access to advanced features that give you more control over accounts in your organization. For more information, see `All features <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html#feature-set-all>`_ in the *AWS Organizations User Guide* .
        - ``CONSOLIDATED_BILLING``  All member accounts have their bills consolidated to and paid by the management account. For more information, see `Consolidated billing <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html#feature-set-cb-only>`_ in the *AWS Organizations User Guide* .

        .. epigraph::

           The consolidated billing feature feature set isn't available for organizations in the AWS GovCloud (US) Region.

        If you don't specify this property, the default value is ``ALL`` .

        :default: - "ALL"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-organization.html#cfn-organizations-organization-featureset
        '''
        result = self._values.get("feature_set")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationPropsMixin",
):
    '''Creates an AWS organization.

    The account whose user is calling the ```CreateOrganization`` <https://docs.aws.amazon.com/organizations/latest/APIReference/API_CreateOrganization.html>`_ operation automatically becomes the `management account <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html#account>`_ of the new organization.

    This operation must be called using credentials from the account that is to become the new organization's management account. The principal must also have the `relevant IAM permissions <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_org_create.html>`_ .
    .. epigraph::

       - If you delete an organization, you can't recover it. If you created any policies inside of the organization, they're also deleted and you can't recover them.
       - You can delete an organization only after you remove all member accounts from the organization. If you created some of your member accounts using AWS Organizations , you might be blocked from removing those accounts. You can remove a member account only if it has all the information that's required to operate as a standalone AWS account. For more information about how to provide that information and then remove the account, see `Leave an organization from your member account <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_leave-as-member.html>`_ in the *AWS Organizations User Guide* .
       - If you closed a member account before you remove it from the organization, it enters a 'suspended' state for a period of time and you can't remove the account from the organization until it is finally closed. This can take up to 90 days and can prevent you from deleting the organization until all member accounts are completely closed.

       For more information, see `Deleting an organization <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_org_delete.html>`_ in the *AWS Organizations User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-organization.html
    :cloudformationResource: AWS::Organizations::Organization
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        cfn_organization_props_mixin = organizations_mixins.CfnOrganizationPropsMixin(organizations_mixins.CfnOrganizationMixinProps(
            feature_set="featureSet"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOrganizationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Organizations::Organization``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b907c04775d4d71434ad24f8bfcc0a171cb4426567c31fa88390371d37b19e1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d6a6b3d9b53afc4c66582c472397dcd3212779335f3d2f9cc14ed3f21aed221)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24dd2b2b47babb7f5c283ebfe40ad05b456f72cdc2851000f9072f84de57552c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOrganizationMixinProps:
        return typing.cast(CfnOrganizationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


class CfnOrganizationWorkmailAvailabilityProviderLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationWorkmailAvailabilityProviderLogs",
):
    '''Builder for CfnOrganizationLogsMixin to generate WORKMAIL_AVAILABILITY_PROVIDER_LOGS for CfnOrganization.

    :cloudformationResource: AWS::Organizations::Organization
    :logType: WORKMAIL_AVAILABILITY_PROVIDER_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        cfn_organization_workmail_availability_provider_logs = organizations_mixins.CfnOrganizationWorkmailAvailabilityProviderLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> CfnOrganizationLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc711e758964a192b1923cb1066bf56872c7f3483e176d2bad413b472af99531)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnOrganizationLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnOrganizationLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e53a9e17ec4ee75b54fa4106ad33d3f21e78a1d2118fdab63b52adf238ff79)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnOrganizationLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnOrganizationLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ecaa370ade6d07d617746db66eeea3f0009aa721426665c98f12b68bd7d6d0)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnOrganizationLogsMixin, jsii.invoke(self, "toS3", [bucket]))


class CfnOrganizationWorkmailMailboxAccessLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationWorkmailMailboxAccessLogs",
):
    '''Builder for CfnOrganizationLogsMixin to generate WORKMAIL_MAILBOX_ACCESS_LOGS for CfnOrganization.

    :cloudformationResource: AWS::Organizations::Organization
    :logType: WORKMAIL_MAILBOX_ACCESS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        cfn_organization_workmail_mailbox_access_logs = organizations_mixins.CfnOrganizationWorkmailMailboxAccessLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> CfnOrganizationLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9cd6816625f29dac09fda5f2fa8a05e4c3b1d8a2663f13e774542ca7a2ab41)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnOrganizationLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnOrganizationLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66fa03b42941ef1901bd1ad64cef0489b316012570c93f0e287ac208c9f3ad5f)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnOrganizationLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnOrganizationLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a99cd81e3b4e29dfe23ea8c6252a18ca162d2c4dbc53583e5bfe9531814666a)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnOrganizationLogsMixin, jsii.invoke(self, "toS3", [bucket]))


class CfnOrganizationWorkmailPersonalAccessTokenLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationWorkmailPersonalAccessTokenLogs",
):
    '''Builder for CfnOrganizationLogsMixin to generate WORKMAIL_PERSONAL_ACCESS_TOKEN_LOGS for CfnOrganization.

    :cloudformationResource: AWS::Organizations::Organization
    :logType: WORKMAIL_PERSONAL_ACCESS_TOKEN_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        cfn_organization_workmail_personal_access_token_logs = organizations_mixins.CfnOrganizationWorkmailPersonalAccessTokenLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> CfnOrganizationLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a5496947541fec532e44b2cf7969222cfae76561be620dcb2e1bd17c0e2317)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnOrganizationLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnOrganizationLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e3f009306d62c8b126808eea9cccaded5fb6a8d4634c293a31e2688b293730)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnOrganizationLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnOrganizationLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4ba20ea679a7d5cc28493263f3a4f129f0a315897a49bb1a783322581cb63d)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnOrganizationLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationalUnitMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parent_id": "parentId", "tags": "tags"},
)
class CfnOrganizationalUnitMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        parent_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnOrganizationalUnitPropsMixin.

        :param name: The friendly name of this OU. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ that is used to validate this parameter is a string of any of the characters in the ASCII character range.
        :param parent_id: The unique identifier (ID) of the parent root or OU that you want to create the new OU in. .. epigraph:: To update the ``ParentId`` parameter value, you must first remove all accounts attached to the organizational unit (OU). OUs can't be moved within the organization with accounts still attached. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ for a parent ID string requires one of the following: - *Root* - A string that begins with "r-" followed by from 4 to 32 lowercase letters or digits. - *Organizational unit (OU)* - A string that begins with "ou-" followed by from 4 to 32 lowercase letters or digits (the ID of the root that the OU is in). This string is followed by a second "-" dash and from 8 to 32 additional lowercase letters or digits.
        :param tags: A list of tags that you want to attach to the newly created OU. For each tag in the list, you must specify both a tag key and a value. You can set the value to an empty string, but you can't set it to ``null`` . For more information about tagging, see `Tagging AWS Organizations resources <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tagging.html>`_ in the AWS Organizations User Guide. .. epigraph:: If any one of the tags is not valid or if you exceed the allowed number of tags for an OU, then the entire request fails and the OU is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-organizationalunit.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
            
            cfn_organizational_unit_mixin_props = organizations_mixins.CfnOrganizationalUnitMixinProps(
                name="name",
                parent_id="parentId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47cc73c3102b65f743acc84c37ced82f6682126b41d2b155a623a907a24a54d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_id", value=parent_id, expected_type=type_hints["parent_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if parent_id is not None:
            self._values["parent_id"] = parent_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The friendly name of this OU.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ that is used to validate this parameter is a string of any of the characters in the ASCII character range.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-organizationalunit.html#cfn-organizations-organizationalunit-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier (ID) of the parent root or OU that you want to create the new OU in.

        .. epigraph::

           To update the ``ParentId`` parameter value, you must first remove all accounts attached to the organizational unit (OU). OUs can't be moved within the organization with accounts still attached.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ for a parent ID string requires one of the following:

        - *Root* - A string that begins with "r-" followed by from 4 to 32 lowercase letters or digits.
        - *Organizational unit (OU)* - A string that begins with "ou-" followed by from 4 to 32 lowercase letters or digits (the ID of the root that the OU is in). This string is followed by a second "-" dash and from 8 to 32 additional lowercase letters or digits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-organizationalunit.html#cfn-organizations-organizationalunit-parentid
        '''
        result = self._values.get("parent_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that you want to attach to the newly created OU.

        For each tag in the list, you must specify both a tag key and a value. You can set the value to an empty string, but you can't set it to ``null`` . For more information about tagging, see `Tagging AWS Organizations resources <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tagging.html>`_ in the AWS Organizations User Guide.
        .. epigraph::

           If any one of the tags is not valid or if you exceed the allowed number of tags for an OU, then the entire request fails and the OU is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-organizationalunit.html#cfn-organizations-organizationalunit-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationalUnitMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationalUnitPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnOrganizationalUnitPropsMixin",
):
    '''Creates an organizational unit (OU) within a root or parent OU.

    An OU is a container for accounts that enables you to organize your accounts to apply policies according to your business requirements. The number of levels deep that you can nest OUs is dependent upon the policy types enabled for that root. For service control policies, the limit is five.

    For more information about OUs, see `Managing organizational units (OUs) <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ous.html>`_ in the *AWS Organizations User Guide* .

    If the request includes tags, then the requester must have the ``organizations:TagResource`` permission.

    You can only call this operation from the management account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-organizationalunit.html
    :cloudformationResource: AWS::Organizations::OrganizationalUnit
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        cfn_organizational_unit_props_mixin = organizations_mixins.CfnOrganizationalUnitPropsMixin(organizations_mixins.CfnOrganizationalUnitMixinProps(
            name="name",
            parent_id="parentId",
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
        props: typing.Union[CfnOrganizationalUnitMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Organizations::OrganizationalUnit``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c765bcc810cf318c4c85cf0ef22a0833e567ca1f04f68de6ae04c2ee14fe3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b638610cfe98425f53d57a3df81fa71e3f9eed1a3deadf6e78976042f99227f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd1b3122bf5c9bdcac53c33a0ec315f9ef41643e2a8cf432ec03102be8e0912)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOrganizationalUnitMixinProps:
        return typing.cast(CfnOrganizationalUnitMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "description": "description",
        "name": "name",
        "tags": "tags",
        "target_ids": "targetIds",
        "type": "type",
    },
)
class CfnPolicyMixinProps:
    def __init__(
        self,
        *,
        content: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPolicyPropsMixin.

        :param content: The policy text content. You can specify the policy content as a JSON object or a JSON string. .. epigraph:: When you specify the policy content as a JSON string, you can't perform drift detection on the CloudFormation stack. For this reason, we recommend specifying the policy content as a JSON object instead. The text that you supply must adhere to the rules of the policy type you specify in the ``Type`` parameter. The following AWS Organizations quotas are enforced for the maximum size of a policy document: - Service control policies: 5,120 characters - Resource control policies: 5,120 characters - Declarative policies: 10,000 characters - Backup policies: 10,000 characters - Tag policies: 10,000 characters - Chat applications policies: 10,000 characters - AI services opt-out policies: 2,500 characters - Security Hub policies: 10,000 characters - Amazon Inspector policies: 10,000 characters - Amazon Bedrock policies: 10,000 characters - Upgrade rollout policies: 10,000 characters For more information about Organizations service quotas, see `Quotas for AWS Organizations <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html>`_ in the *AWS Organizations User Guide* .
        :param description: Human readable description of the policy.
        :param name: Name of the policy. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ that is used to validate this parameter is a string of any of the characters in the ASCII character range.
        :param tags: A list of tags that you want to attach to the newly created policy. For each tag in the list, you must specify both a tag key and a value. You can set the value to an empty string, but you can't set it to ``null`` . For more information about tagging, see `Tagging AWS Organizations resources <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tagging.html>`_ in the AWS Organizations User Guide. .. epigraph:: If any one of the tags is not valid or if you exceed the allowed number of tags for a policy, then the entire request fails and the policy is not created.
        :param target_ids: List of unique identifiers (IDs) of the root, OU, or account that you want to attach the policy to. You can get the ID by calling the `ListRoots <https://docs.aws.amazon.com/organizations/latest/APIReference/API_ListRoots.html>`_ , `ListOrganizationalUnitsForParent <https://docs.aws.amazon.com/organizations/latest/APIReference/API_ListOrganizationalUnitsForParent.html>`_ , or `ListAccounts <https://docs.aws.amazon.com/organizations/latest/APIReference/API_ListAccounts.html>`_ operations. If you don't specify this parameter, the policy is created but not attached to any organization resource. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ for a target ID string requires one of the following: - *Root* - A string that begins with "r-" followed by from 4 to 32 lowercase letters or digits. - *Account* - A string that consists of exactly 12 digits. - *Organizational unit (OU)* - A string that begins with "ou-" followed by from 4 to 32 lowercase letters or digits (the ID of the root that the OU is in). This string is followed by a second "-" dash and from 8 to 32 additional lowercase letters or digits.
        :param type: The type of policy to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
            
            # content: Any
            
            cfn_policy_mixin_props = organizations_mixins.CfnPolicyMixinProps(
                content=content,
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_ids=["targetIds"],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c3132d82c3f1b1a82ad29fd8608e670614204c5d009f84306b2e67ac5919b8)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_ids", value=target_ids, expected_type=type_hints["target_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if target_ids is not None:
            self._values["target_ids"] = target_ids
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def content(self) -> typing.Any:
        '''The policy text content. You can specify the policy content as a JSON object or a JSON string.

        .. epigraph::

           When you specify the policy content as a JSON string, you can't perform drift detection on the CloudFormation stack. For this reason, we recommend specifying the policy content as a JSON object instead.

        The text that you supply must adhere to the rules of the policy type you specify in the ``Type`` parameter. The following AWS Organizations quotas are enforced for the maximum size of a policy document:

        - Service control policies: 5,120 characters
        - Resource control policies: 5,120 characters
        - Declarative policies: 10,000 characters
        - Backup policies: 10,000 characters
        - Tag policies: 10,000 characters
        - Chat applications policies: 10,000 characters
        - AI services opt-out policies: 2,500 characters
        - Security Hub policies: 10,000 characters
        - Amazon Inspector policies: 10,000 characters
        - Amazon Bedrock policies: 10,000 characters
        - Upgrade rollout policies: 10,000 characters

        For more information about Organizations service quotas, see `Quotas for AWS Organizations <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html>`_ in the *AWS Organizations User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-policy.html#cfn-organizations-policy-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Human readable description of the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-policy.html#cfn-organizations-policy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the policy.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ that is used to validate this parameter is a string of any of the characters in the ASCII character range.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-policy.html#cfn-organizations-policy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that you want to attach to the newly created policy.

        For each tag in the list, you must specify both a tag key and a value. You can set the value to an empty string, but you can't set it to ``null`` . For more information about tagging, see `Tagging AWS Organizations resources <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tagging.html>`_ in the AWS Organizations User Guide.
        .. epigraph::

           If any one of the tags is not valid or if you exceed the allowed number of tags for a policy, then the entire request fails and the policy is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-policy.html#cfn-organizations-policy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of unique identifiers (IDs) of the root, OU, or account that you want to attach the policy to.

        You can get the ID by calling the `ListRoots <https://docs.aws.amazon.com/organizations/latest/APIReference/API_ListRoots.html>`_ , `ListOrganizationalUnitsForParent <https://docs.aws.amazon.com/organizations/latest/APIReference/API_ListOrganizationalUnitsForParent.html>`_ , or `ListAccounts <https://docs.aws.amazon.com/organizations/latest/APIReference/API_ListAccounts.html>`_ operations. If you don't specify this parameter, the policy is created but not attached to any organization resource.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ for a target ID string requires one of the following:

        - *Root* - A string that begins with "r-" followed by from 4 to 32 lowercase letters or digits.
        - *Account* - A string that consists of exactly 12 digits.
        - *Organizational unit (OU)* - A string that begins with "ou-" followed by from 4 to 32 lowercase letters or digits (the ID of the root that the OU is in). This string is followed by a second "-" dash and from 8 to 32 additional lowercase letters or digits.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-policy.html#cfn-organizations-policy-targetids
        '''
        result = self._values.get("target_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of policy to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-policy.html#cfn-organizations-policy-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnPolicyPropsMixin",
):
    '''Creates a policy of a specified type that you can attach to a root, an organizational unit (OU), or an individual AWS account .

    For more information about policies and their use, see `Managing AWS Organizations policies <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies.html>`_ .

    If the request includes tags, then the requester must have the ``organizations:TagResource`` permission.

    This operation can be called only from the organization's management account or a member account designated as a delegated administrator.
    .. epigraph::

       Before you can create a policy of a given type, you must first `enable that policy type <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_enable-disable.html>`_ in your organization.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-policy.html
    :cloudformationResource: AWS::Organizations::Policy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        # content: Any
        
        cfn_policy_props_mixin = organizations_mixins.CfnPolicyPropsMixin(organizations_mixins.CfnPolicyMixinProps(
            content=content,
            description="description",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_ids=["targetIds"],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Organizations::Policy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce01f275377e8248e3fe745e155225706ee39bfe5813dbbf8b619338631709d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac56d7f28c8ac1241cb58641b778da71a3c82441c17ef04833d35d9ce87b6ac1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f621cefc40dcd44e86b167e9c042fc161374daa4169f419f4747e65ba267f67)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPolicyMixinProps:
        return typing.cast(CfnPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "tags": "tags"},
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        content: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param content: The policy text of the organization resource policy. You can specify the resource policy content as a JSON object or a JSON string. .. epigraph:: When you specify the resource policy content as a JSON string, you can't perform drift detection on the CloudFormation stack. For this reason, we recommend specifying the resource policy content as a JSON object instead.
        :param tags: A list of tags that you want to attach to the newly created resource policy. For each tag in the list, you must specify both a tag key and a value. You can set the value to an empty string, but you can't set it to ``null`` . For more information about tagging, see `Tagging AWS Organizations resources <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tagging.html>`_ in the *AWS Organizations User Guide* . .. epigraph:: If any one of the tags is not valid or if you exceed the allowed number of tags for the resource policy, then the entire request fails and the resource policy is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
            
            # content: Any
            
            cfn_resource_policy_mixin_props = organizations_mixins.CfnResourcePolicyMixinProps(
                content=content,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71abb11069e006e7339d53867738cc6359395c7b6445b84ecd4d299fbd90ff21)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content(self) -> typing.Any:
        '''The policy text of the organization resource policy.

        You can specify the resource policy content as a JSON object or a JSON string.
        .. epigraph::

           When you specify the resource policy content as a JSON string, you can't perform drift detection on the CloudFormation stack. For this reason, we recommend specifying the resource policy content as a JSON object instead.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-resourcepolicy.html#cfn-organizations-resourcepolicy-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that you want to attach to the newly created resource policy.

        For each tag in the list, you must specify both a tag key and a value. You can set the value to an empty string, but you can't set it to ``null`` . For more information about tagging, see `Tagging AWS Organizations resources <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_tagging.html>`_ in the *AWS Organizations User Guide* .
        .. epigraph::

           If any one of the tags is not valid or if you exceed the allowed number of tags for the resource policy, then the entire request fails and the resource policy is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-resourcepolicy.html#cfn-organizations-resourcepolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_organizations.mixins.CfnResourcePolicyPropsMixin",
):
    '''Creates or updates a resource-based delegation policy that can be used to delegate policy management for AWS Organizations to specified member accounts to perform policy actions that are by default available only to the management account.

    For more information about delegated policy management, see `Delegated administrator for AWS Organizations <https://docs.aws.amazon.com/organizations/latest/userguide/orgs_delegate_policies.html>`_ in the *AWS Organizations User Guide* .

    You can only call this operation from the organization's management account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-organizations-resourcepolicy.html
    :cloudformationResource: AWS::Organizations::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_organizations import mixins as organizations_mixins
        
        # content: Any
        
        cfn_resource_policy_props_mixin = organizations_mixins.CfnResourcePolicyPropsMixin(organizations_mixins.CfnResourcePolicyMixinProps(
            content=content,
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
        props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Organizations::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37eed5d73951dc77b99f748141e22c64cb72c6b64c016b5664914d5701da5dcb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d7ee0f565089ef6da68f4687c9215d31eb2304065d452aef44ab99e9b3643b3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce65178aff06f305c49f65be4d236661eb386963b53eb2ad89725976c75dae8)
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
    "CfnAccountMixinProps",
    "CfnAccountPropsMixin",
    "CfnOrganizationAccessControlLogs",
    "CfnOrganizationAuthenticationLogs",
    "CfnOrganizationLogsMixin",
    "CfnOrganizationMixinProps",
    "CfnOrganizationPropsMixin",
    "CfnOrganizationWorkmailAvailabilityProviderLogs",
    "CfnOrganizationWorkmailMailboxAccessLogs",
    "CfnOrganizationWorkmailPersonalAccessTokenLogs",
    "CfnOrganizationalUnitMixinProps",
    "CfnOrganizationalUnitPropsMixin",
    "CfnPolicyMixinProps",
    "CfnPolicyPropsMixin",
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
]

publication.publish()

def _typecheckingstub__f09f23d3cb98afe35c104d8b30e816b3c843b6c86f6398ea30cc34c34ac63257(
    *,
    account_name: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    parent_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1353fbd8b0533a2f3c3c3fa868b3f034bf4910ba55f09e67a224dcd4fada6d78(
    props: typing.Union[CfnAccountMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfe93aedc2e50d3d3453b79a91ffa5c63a3703ef69821d5c1987551383ed4af(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111cd040093c584df164c2bf2b2a9b218eaab4a31ed8ea0d72f2ae05b9d6c0e5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c75c9965f031f93de06df251e2e219a07b532ab416835deb31171d7798ccfa5(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1b92f0ca0c7e591a62ec68333f8529277e2c3dad616987e25edefe365954c8(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47cc864281ecacf0cefb6f08b77c5fad9d3ff87f453506d86ebb137c1205d080(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d570aa7966afe8ce2c51babecbb24fe2967cd77697ea05cf438d54b70a94498d(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183d14714684762752848cb68f5e5668bba6783f1e73a0d0ab06d549bae8bffd(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe2cd0cc98f883c4605dedc05cb63c1ca21ed3f214eed05f5ca3a977f74b778(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6f2b1d166e4c6adac315bf6d8077552c715af90c9c9edf21ce66bf84446f59(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d169d4803ec52bf91f38e255df25c9e94f4d91fe13cde26a73b231434918e720(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c526ab69b7ea47bcfb35b16947ca682cc6494be8be24fdc0735ee25bdd0b215d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafcea6e59f0f0e81fc60013eafb74681a447ba66f05dd9a5543152d64c108bf(
    *,
    feature_set: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b907c04775d4d71434ad24f8bfcc0a171cb4426567c31fa88390371d37b19e1b(
    props: typing.Union[CfnOrganizationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6a6b3d9b53afc4c66582c472397dcd3212779335f3d2f9cc14ed3f21aed221(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24dd2b2b47babb7f5c283ebfe40ad05b456f72cdc2851000f9072f84de57552c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc711e758964a192b1923cb1066bf56872c7f3483e176d2bad413b472af99531(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e53a9e17ec4ee75b54fa4106ad33d3f21e78a1d2118fdab63b52adf238ff79(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ecaa370ade6d07d617746db66eeea3f0009aa721426665c98f12b68bd7d6d0(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9cd6816625f29dac09fda5f2fa8a05e4c3b1d8a2663f13e774542ca7a2ab41(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66fa03b42941ef1901bd1ad64cef0489b316012570c93f0e287ac208c9f3ad5f(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a99cd81e3b4e29dfe23ea8c6252a18ca162d2c4dbc53583e5bfe9531814666a(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a5496947541fec532e44b2cf7969222cfae76561be620dcb2e1bd17c0e2317(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e3f009306d62c8b126808eea9cccaded5fb6a8d4634c293a31e2688b293730(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4ba20ea679a7d5cc28493263f3a4f129f0a315897a49bb1a783322581cb63d(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47cc73c3102b65f743acc84c37ced82f6682126b41d2b155a623a907a24a54d(
    *,
    name: typing.Optional[builtins.str] = None,
    parent_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c765bcc810cf318c4c85cf0ef22a0833e567ca1f04f68de6ae04c2ee14fe3a(
    props: typing.Union[CfnOrganizationalUnitMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b638610cfe98425f53d57a3df81fa71e3f9eed1a3deadf6e78976042f99227f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd1b3122bf5c9bdcac53c33a0ec315f9ef41643e2a8cf432ec03102be8e0912(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c3132d82c3f1b1a82ad29fd8608e670614204c5d009f84306b2e67ac5919b8(
    *,
    content: typing.Any = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce01f275377e8248e3fe745e155225706ee39bfe5813dbbf8b619338631709d(
    props: typing.Union[CfnPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac56d7f28c8ac1241cb58641b778da71a3c82441c17ef04833d35d9ce87b6ac1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f621cefc40dcd44e86b167e9c042fc161374daa4169f419f4747e65ba267f67(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71abb11069e006e7339d53867738cc6359395c7b6445b84ecd4d299fbd90ff21(
    *,
    content: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37eed5d73951dc77b99f748141e22c64cb72c6b64c016b5664914d5701da5dcb(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7ee0f565089ef6da68f4687c9215d31eb2304065d452aef44ab99e9b3643b3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce65178aff06f305c49f65be4d236661eb386963b53eb2ad89725976c75dae8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
