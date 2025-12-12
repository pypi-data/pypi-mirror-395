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
    jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnAppMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "auto_branch_creation_config": "autoBranchCreationConfig",
        "basic_auth_config": "basicAuthConfig",
        "build_spec": "buildSpec",
        "cache_config": "cacheConfig",
        "compute_role_arn": "computeRoleArn",
        "custom_headers": "customHeaders",
        "custom_rules": "customRules",
        "description": "description",
        "enable_branch_auto_deletion": "enableBranchAutoDeletion",
        "environment_variables": "environmentVariables",
        "iam_service_role": "iamServiceRole",
        "job_config": "jobConfig",
        "name": "name",
        "oauth_token": "oauthToken",
        "platform": "platform",
        "repository": "repository",
        "tags": "tags",
    },
)
class CfnAppMixinProps:
    def __init__(
        self,
        *,
        access_token: typing.Optional[builtins.str] = None,
        auto_branch_creation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.AutoBranchCreationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        basic_auth_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.BasicAuthConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        cache_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.CacheConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        compute_role_arn: typing.Optional[builtins.str] = None,
        custom_headers: typing.Optional[builtins.str] = None,
        custom_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.CustomRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        iam_service_role: typing.Optional[builtins.str] = None,
        job_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.JobConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAppPropsMixin.

        :param access_token: The personal access token for a GitHub repository for an Amplify app. The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored. Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` . You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .
        :param auto_branch_creation_config: Sets the configuration for your automatic branch creation.
        :param basic_auth_config: The credentials for basic authorization for an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param build_spec: The build specification (build spec) for an Amplify app.
        :param cache_config: The cache configuration for the Amplify app. If you don't specify the cache configuration ``type`` , Amplify uses the default ``AMPLIFY_MANAGED`` setting.
        :param compute_role_arn: The Amazon Resource Name (ARN) of the IAM role for an SSR app. The Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. For more information about the SSR Compute role, see `Adding an SSR Compute role <https://docs.aws.amazon.com/amplify/latest/userguide/amplify-SSR-compute-role.html>`_ in the *Amplify User Guide* .
        :param custom_headers: The custom HTTP headers for an Amplify app.
        :param custom_rules: The custom rewrite and redirect rules for an Amplify app.
        :param description: The description of the Amplify app.
        :param enable_branch_auto_deletion: Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.
        :param environment_variables: The environment variables for the Amplify app. For a list of the environment variables that are accessible to Amplify by default, see `Amplify Environment variables <https://docs.aws.amazon.com/amplify/latest/userguide/amplify-console-environment-variables.html>`_ in the *Amplify Hosting User Guide* .
        :param iam_service_role: AWS Identity and Access Management ( IAM ) service role for the Amazon Resource Name (ARN) of the Amplify app.
        :param job_config: The configuration details that apply to the jobs for an Amplify app.
        :param name: The name of the Amplify app.
        :param oauth_token: The OAuth token for a third-party source control system for an Amplify app. The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored. Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` . You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .
        :param platform: The platform for the Amplify app. For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` . If you are deploying an SSG only app with Next.js version 14 or later, you must set the platform type to ``WEB_COMPUTE`` and set the artifacts ``baseDirectory`` to ``.next`` in the application's build settings. For an example of the build specification settings, see `Amplify build settings for a Next.js 14 SSG application <https://docs.aws.amazon.com/amplify/latest/userguide/deploy-nextjs-app.html#build-setting-detection-ssg-14>`_ in the *Amplify Hosting User Guide* .
        :param repository: The Git repository for the Amplify app.
        :param tags: The tag for an Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
            
            cfn_app_mixin_props = amplify_mixins.CfnAppMixinProps(
                access_token="accessToken",
                auto_branch_creation_config=amplify_mixins.CfnAppPropsMixin.AutoBranchCreationConfigProperty(
                    auto_branch_creation_patterns=["autoBranchCreationPatterns"],
                    basic_auth_config=amplify_mixins.CfnAppPropsMixin.BasicAuthConfigProperty(
                        enable_basic_auth=False,
                        password="password",
                        username="username"
                    ),
                    build_spec="buildSpec",
                    enable_auto_branch_creation=False,
                    enable_auto_build=False,
                    enable_performance_mode=False,
                    enable_pull_request_preview=False,
                    environment_variables=[amplify_mixins.CfnAppPropsMixin.EnvironmentVariableProperty(
                        name="name",
                        value="value"
                    )],
                    framework="framework",
                    pull_request_environment_name="pullRequestEnvironmentName",
                    stage="stage"
                ),
                basic_auth_config=amplify_mixins.CfnAppPropsMixin.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                ),
                build_spec="buildSpec",
                cache_config=amplify_mixins.CfnAppPropsMixin.CacheConfigProperty(
                    type="type"
                ),
                compute_role_arn="computeRoleArn",
                custom_headers="customHeaders",
                custom_rules=[amplify_mixins.CfnAppPropsMixin.CustomRuleProperty(
                    condition="condition",
                    source="source",
                    status="status",
                    target="target"
                )],
                description="description",
                enable_branch_auto_deletion=False,
                environment_variables=[amplify_mixins.CfnAppPropsMixin.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )],
                iam_service_role="iamServiceRole",
                job_config=amplify_mixins.CfnAppPropsMixin.JobConfigProperty(
                    build_compute_type="buildComputeType"
                ),
                name="name",
                oauth_token="oauthToken",
                platform="platform",
                repository="repository",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491cf09d3c3dbe1c8a80a90a6f3aa38ae700af4da457fa228eac630a79e84749)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument auto_branch_creation_config", value=auto_branch_creation_config, expected_type=type_hints["auto_branch_creation_config"])
            check_type(argname="argument basic_auth_config", value=basic_auth_config, expected_type=type_hints["basic_auth_config"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument cache_config", value=cache_config, expected_type=type_hints["cache_config"])
            check_type(argname="argument compute_role_arn", value=compute_role_arn, expected_type=type_hints["compute_role_arn"])
            check_type(argname="argument custom_headers", value=custom_headers, expected_type=type_hints["custom_headers"])
            check_type(argname="argument custom_rules", value=custom_rules, expected_type=type_hints["custom_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_branch_auto_deletion", value=enable_branch_auto_deletion, expected_type=type_hints["enable_branch_auto_deletion"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument iam_service_role", value=iam_service_role, expected_type=type_hints["iam_service_role"])
            check_type(argname="argument job_config", value=job_config, expected_type=type_hints["job_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_token is not None:
            self._values["access_token"] = access_token
        if auto_branch_creation_config is not None:
            self._values["auto_branch_creation_config"] = auto_branch_creation_config
        if basic_auth_config is not None:
            self._values["basic_auth_config"] = basic_auth_config
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cache_config is not None:
            self._values["cache_config"] = cache_config
        if compute_role_arn is not None:
            self._values["compute_role_arn"] = compute_role_arn
        if custom_headers is not None:
            self._values["custom_headers"] = custom_headers
        if custom_rules is not None:
            self._values["custom_rules"] = custom_rules
        if description is not None:
            self._values["description"] = description
        if enable_branch_auto_deletion is not None:
            self._values["enable_branch_auto_deletion"] = enable_branch_auto_deletion
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if iam_service_role is not None:
            self._values["iam_service_role"] = iam_service_role
        if job_config is not None:
            self._values["job_config"] = job_config
        if name is not None:
            self._values["name"] = name
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token
        if platform is not None:
            self._values["platform"] = platform
        if repository is not None:
            self._values["repository"] = repository
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''The personal access token for a GitHub repository for an Amplify app.

        The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored.

        Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` .

        You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-accesstoken
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_branch_creation_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.AutoBranchCreationConfigProperty"]]:
        '''Sets the configuration for your automatic branch creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-autobranchcreationconfig
        '''
        result = self._values.get("auto_branch_creation_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.AutoBranchCreationConfigProperty"]], result)

    @builtins.property
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.BasicAuthConfigProperty"]]:
        '''The credentials for basic authorization for an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-basicauthconfig
        '''
        result = self._values.get("basic_auth_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.BasicAuthConfigProperty"]], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for an Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-buildspec
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.CacheConfigProperty"]]:
        '''The cache configuration for the Amplify app.

        If you don't specify the cache configuration ``type`` , Amplify uses the default ``AMPLIFY_MANAGED`` setting.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-cacheconfig
        '''
        result = self._values.get("cache_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.CacheConfigProperty"]], result)

    @builtins.property
    def compute_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role for an SSR app.

        The Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. For more information about the SSR Compute role, see `Adding an SSR Compute role <https://docs.aws.amazon.com/amplify/latest/userguide/amplify-SSR-compute-role.html>`_ in the *Amplify User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-computerolearn
        '''
        result = self._values.get("compute_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_headers(self) -> typing.Optional[builtins.str]:
        '''The custom HTTP headers for an Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customheaders
        '''
        result = self._values.get("custom_headers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.CustomRuleProperty"]]]]:
        '''The custom rewrite and redirect rules for an Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customrules
        '''
        result = self._values.get("custom_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.CustomRuleProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_branch_auto_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-enablebranchautodeletion
        '''
        result = self._values.get("enable_branch_auto_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.EnvironmentVariableProperty"]]]]:
        '''The environment variables for the Amplify app.

        For a list of the environment variables that are accessible to Amplify by default, see `Amplify Environment variables <https://docs.aws.amazon.com/amplify/latest/userguide/amplify-console-environment-variables.html>`_ in the *Amplify Hosting User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-environmentvariables
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.EnvironmentVariableProperty"]]]], result)

    @builtins.property
    def iam_service_role(self) -> typing.Optional[builtins.str]:
        '''AWS Identity and Access Management ( IAM ) service role for the Amazon Resource Name (ARN) of the Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-iamservicerole
        '''
        result = self._values.get("iam_service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.JobConfigProperty"]]:
        '''The configuration details that apply to the jobs for an Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-jobconfig
        '''
        result = self._values.get("job_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.JobConfigProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_token(self) -> typing.Optional[builtins.str]:
        '''The OAuth token for a third-party source control system for an Amplify app.

        The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored.

        Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` .

        You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-oauthtoken
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform for the Amplify app.

        For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` .

        If you are deploying an SSG only app with Next.js version 14 or later, you must set the platform type to ``WEB_COMPUTE`` and set the artifacts ``baseDirectory`` to ``.next`` in the application's build settings. For an example of the build specification settings, see `Amplify build settings for a Next.js 14 SSG application <https://docs.aws.amazon.com/amplify/latest/userguide/deploy-nextjs-app.html#build-setting-detection-ssg-14>`_ in the *Amplify Hosting User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-platform
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The Git repository for the Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-repository
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tag for an Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnAppPropsMixin",
):
    '''The AWS::Amplify::App resource specifies Apps in Amplify Hosting.

    An App is a collection of branches.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html
    :cloudformationResource: AWS::Amplify::App
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
        
        cfn_app_props_mixin = amplify_mixins.CfnAppPropsMixin(amplify_mixins.CfnAppMixinProps(
            access_token="accessToken",
            auto_branch_creation_config=amplify_mixins.CfnAppPropsMixin.AutoBranchCreationConfigProperty(
                auto_branch_creation_patterns=["autoBranchCreationPatterns"],
                basic_auth_config=amplify_mixins.CfnAppPropsMixin.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                ),
                build_spec="buildSpec",
                enable_auto_branch_creation=False,
                enable_auto_build=False,
                enable_performance_mode=False,
                enable_pull_request_preview=False,
                environment_variables=[amplify_mixins.CfnAppPropsMixin.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )],
                framework="framework",
                pull_request_environment_name="pullRequestEnvironmentName",
                stage="stage"
            ),
            basic_auth_config=amplify_mixins.CfnAppPropsMixin.BasicAuthConfigProperty(
                enable_basic_auth=False,
                password="password",
                username="username"
            ),
            build_spec="buildSpec",
            cache_config=amplify_mixins.CfnAppPropsMixin.CacheConfigProperty(
                type="type"
            ),
            compute_role_arn="computeRoleArn",
            custom_headers="customHeaders",
            custom_rules=[amplify_mixins.CfnAppPropsMixin.CustomRuleProperty(
                condition="condition",
                source="source",
                status="status",
                target="target"
            )],
            description="description",
            enable_branch_auto_deletion=False,
            environment_variables=[amplify_mixins.CfnAppPropsMixin.EnvironmentVariableProperty(
                name="name",
                value="value"
            )],
            iam_service_role="iamServiceRole",
            job_config=amplify_mixins.CfnAppPropsMixin.JobConfigProperty(
                build_compute_type="buildComputeType"
            ),
            name="name",
            oauth_token="oauthToken",
            platform="platform",
            repository="repository",
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
        props: typing.Union[CfnAppMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Amplify::App``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0779f99136f3e972a2faa60ebb0f7d82e0f6589b98a0b3016874cc18a6d829)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac2ca9ffa03d6e3cbc9f583a02304d9a56b6876f9bacc76c008d79e1344b3b10)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c067b61126d2da68584d921d94a9d1ee2839c076b8964b4026c8e03f7bfbfa)
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
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnAppPropsMixin.AutoBranchCreationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_branch_creation_patterns": "autoBranchCreationPatterns",
            "basic_auth_config": "basicAuthConfig",
            "build_spec": "buildSpec",
            "enable_auto_branch_creation": "enableAutoBranchCreation",
            "enable_auto_build": "enableAutoBuild",
            "enable_performance_mode": "enablePerformanceMode",
            "enable_pull_request_preview": "enablePullRequestPreview",
            "environment_variables": "environmentVariables",
            "framework": "framework",
            "pull_request_environment_name": "pullRequestEnvironmentName",
            "stage": "stage",
        },
    )
    class AutoBranchCreationConfigProperty:
        def __init__(
            self,
            *,
            auto_branch_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            basic_auth_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.BasicAuthConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            build_spec: typing.Optional[builtins.str] = None,
            enable_auto_branch_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAppPropsMixin.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            framework: typing.Optional[builtins.str] = None,
            pull_request_environment_name: typing.Optional[builtins.str] = None,
            stage: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the AutoBranchCreationConfig property type to automatically create branches that match a certain pattern.

            :param auto_branch_creation_patterns: Automated branch creation glob patterns for the Amplify app.
            :param basic_auth_config: Sets password protection for your auto created branch.
            :param build_spec: The build specification (build spec) for the autocreated branch.
            :param enable_auto_branch_creation: Enables automated branch creation for the Amplify app.
            :param enable_auto_build: Enables auto building for the auto created branch.
            :param enable_performance_mode: Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
            :param enable_pull_request_preview: Sets whether pull request previews are enabled for each branch that Amplify Hosting automatically creates for your app. Amplify creates previews by deploying your app to a unique URL whenever a pull request is opened for the branch. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch. To provide backend support for your preview, Amplify Hosting automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property. For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .
            :param environment_variables: The environment variables for the autocreated branch.
            :param framework: The framework for the autocreated branch.
            :param pull_request_environment_name: If pull request previews are enabled, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI. To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` . If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify deletes this environment when the pull request is closed. For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .
            :param stage: Stage for the auto created branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                auto_branch_creation_config_property = amplify_mixins.CfnAppPropsMixin.AutoBranchCreationConfigProperty(
                    auto_branch_creation_patterns=["autoBranchCreationPatterns"],
                    basic_auth_config=amplify_mixins.CfnAppPropsMixin.BasicAuthConfigProperty(
                        enable_basic_auth=False,
                        password="password",
                        username="username"
                    ),
                    build_spec="buildSpec",
                    enable_auto_branch_creation=False,
                    enable_auto_build=False,
                    enable_performance_mode=False,
                    enable_pull_request_preview=False,
                    environment_variables=[amplify_mixins.CfnAppPropsMixin.EnvironmentVariableProperty(
                        name="name",
                        value="value"
                    )],
                    framework="framework",
                    pull_request_environment_name="pullRequestEnvironmentName",
                    stage="stage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90266383c2db12f7f18c1a037797e9afa1432c4ab4ff58488a57e4c650df1332)
                check_type(argname="argument auto_branch_creation_patterns", value=auto_branch_creation_patterns, expected_type=type_hints["auto_branch_creation_patterns"])
                check_type(argname="argument basic_auth_config", value=basic_auth_config, expected_type=type_hints["basic_auth_config"])
                check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
                check_type(argname="argument enable_auto_branch_creation", value=enable_auto_branch_creation, expected_type=type_hints["enable_auto_branch_creation"])
                check_type(argname="argument enable_auto_build", value=enable_auto_build, expected_type=type_hints["enable_auto_build"])
                check_type(argname="argument enable_performance_mode", value=enable_performance_mode, expected_type=type_hints["enable_performance_mode"])
                check_type(argname="argument enable_pull_request_preview", value=enable_pull_request_preview, expected_type=type_hints["enable_pull_request_preview"])
                check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
                check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
                check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
                check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_branch_creation_patterns is not None:
                self._values["auto_branch_creation_patterns"] = auto_branch_creation_patterns
            if basic_auth_config is not None:
                self._values["basic_auth_config"] = basic_auth_config
            if build_spec is not None:
                self._values["build_spec"] = build_spec
            if enable_auto_branch_creation is not None:
                self._values["enable_auto_branch_creation"] = enable_auto_branch_creation
            if enable_auto_build is not None:
                self._values["enable_auto_build"] = enable_auto_build
            if enable_performance_mode is not None:
                self._values["enable_performance_mode"] = enable_performance_mode
            if enable_pull_request_preview is not None:
                self._values["enable_pull_request_preview"] = enable_pull_request_preview
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if framework is not None:
                self._values["framework"] = framework
            if pull_request_environment_name is not None:
                self._values["pull_request_environment_name"] = pull_request_environment_name
            if stage is not None:
                self._values["stage"] = stage

        @builtins.property
        def auto_branch_creation_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Automated branch creation glob patterns for the Amplify app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-autobranchcreationpatterns
            '''
            result = self._values.get("auto_branch_creation_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def basic_auth_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.BasicAuthConfigProperty"]]:
            '''Sets password protection for your auto created branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-basicauthconfig
            '''
            result = self._values.get("basic_auth_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.BasicAuthConfigProperty"]], result)

        @builtins.property
        def build_spec(self) -> typing.Optional[builtins.str]:
            '''The build specification (build spec) for the autocreated branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-buildspec
            '''
            result = self._values.get("build_spec")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_auto_branch_creation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables automated branch creation for the Amplify app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableautobranchcreation
            '''
            result = self._values.get("enable_auto_branch_creation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_auto_build(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables auto building for the auto created branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableautobuild
            '''
            result = self._values.get("enable_auto_build")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_performance_mode(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables performance mode for the branch.

            Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableperformancemode
            '''
            result = self._values.get("enable_performance_mode")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_pull_request_preview(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Sets whether pull request previews are enabled for each branch that Amplify Hosting automatically creates for your app.

            Amplify creates previews by deploying your app to a unique URL whenever a pull request is opened for the branch. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

            To provide backend support for your preview, Amplify Hosting automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property.

            For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enablepullrequestpreview
            '''
            result = self._values.get("enable_pull_request_preview")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.EnvironmentVariableProperty"]]]]:
            '''The environment variables for the autocreated branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAppPropsMixin.EnvironmentVariableProperty"]]]], result)

        @builtins.property
        def framework(self) -> typing.Optional[builtins.str]:
            '''The framework for the autocreated branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-framework
            '''
            result = self._values.get("framework")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
            '''If pull request previews are enabled, you can use this property to specify a dedicated backend environment for your previews.

            For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI.

            To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` .

            If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify deletes this environment when the pull request is closed.

            For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-pullrequestenvironmentname
            '''
            result = self._values.get("pull_request_environment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage(self) -> typing.Optional[builtins.str]:
            '''Stage for the auto created branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-stage
            '''
            result = self._values.get("stage")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoBranchCreationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnAppPropsMixin.BasicAuthConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_basic_auth": "enableBasicAuth",
            "password": "password",
            "username": "username",
        },
    )
    class BasicAuthConfigProperty:
        def __init__(
            self,
            *,
            enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the BasicAuthConfig property type to set password protection at an app level to all your branches.

            :param enable_basic_auth: Enables basic authorization for the Amplify app's branches.
            :param password: The password for basic authorization.
            :param username: The user name for basic authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                basic_auth_config_property = amplify_mixins.CfnAppPropsMixin.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a76184300b47cf6c80fbd6378c0a94736d330fc21430f78d4ff7df575bee377)
                check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_basic_auth is not None:
                self._values["enable_basic_auth"] = enable_basic_auth
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def enable_basic_auth(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables basic authorization for the Amplify app's branches.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-enablebasicauth
            '''
            result = self._values.get("enable_basic_auth")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password for basic authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The user name for basic authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnAppPropsMixin.CacheConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class CacheConfigProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''Describes the cache configuration for an Amplify app.

            For more information about how Amplify applies an optimal cache configuration for your app based on the type of content that is being served, see `Managing cache configuration <https://docs.aws.amazon.com/amplify/latest/userguide/managing-cache-configuration>`_ in the *Amplify User guide* .

            :param type: The type of cache configuration to use for an Amplify app. The ``AMPLIFY_MANAGED`` cache configuration automatically applies an optimized cache configuration for your app based on its platform, routing rules, and rewrite rules. The ``AMPLIFY_MANAGED_NO_COOKIES`` cache configuration type is the same as ``AMPLIFY_MANAGED`` , except that it excludes all cookies from the cache key. This is the default setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-cacheconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                cache_config_property = amplify_mixins.CfnAppPropsMixin.CacheConfigProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30cb868617d871cf5a5a17a03dabc2af0f932392ae2d3c3d79db85a9c39e616e)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of cache configuration to use for an Amplify app.

            The ``AMPLIFY_MANAGED`` cache configuration automatically applies an optimized cache configuration for your app based on its platform, routing rules, and rewrite rules.

            The ``AMPLIFY_MANAGED_NO_COOKIES`` cache configuration type is the same as ``AMPLIFY_MANAGED`` , except that it excludes all cookies from the cache key. This is the default setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-cacheconfig.html#cfn-amplify-app-cacheconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CacheConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnAppPropsMixin.CustomRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition": "condition",
            "source": "source",
            "status": "status",
            "target": "target",
        },
    )
    class CustomRuleProperty:
        def __init__(
            self,
            *,
            condition: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The CustomRule property type allows you to specify redirects, rewrites, and reverse proxies.

            Redirects enable a web app to reroute navigation from one URL to another.

            :param condition: The condition for a URL rewrite or redirect rule, such as a country code.
            :param source: The source pattern for a URL rewrite or redirect rule.
            :param status: The status code for a URL rewrite or redirect rule. - **200** - Represents a 200 rewrite rule. - **301** - Represents a 301 (moved pemanently) redirect rule. This and all future requests should be directed to the target URL. - **302** - Represents a 302 temporary redirect rule. - **404** - Represents a 404 redirect rule. - **404-200** - Represents a 404 rewrite rule.
            :param target: The target pattern for a URL rewrite or redirect rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                custom_rule_property = amplify_mixins.CfnAppPropsMixin.CustomRuleProperty(
                    condition="condition",
                    source="source",
                    status="status",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5aac565f5494ac94b33a8604988964e6a36e92c23b58a2277958412e70ae409b)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition is not None:
                self._values["condition"] = condition
            if source is not None:
                self._values["source"] = source
            if status is not None:
                self._values["status"] = status
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''The condition for a URL rewrite or redirect rule, such as a country code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The source pattern for a URL rewrite or redirect rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status code for a URL rewrite or redirect rule.

            - **200** - Represents a 200 rewrite rule.
            - **301** - Represents a 301 (moved pemanently) redirect rule. This and all future requests should be directed to the target URL.
            - **302** - Represents a 302 temporary redirect rule.
            - **404** - Represents a 404 redirect rule.
            - **404-200** - Represents a 404 rewrite rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The target pattern for a URL rewrite or redirect rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnAppPropsMixin.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentVariableProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Environment variables are key-value pairs that are available at build time.

            Set environment variables for all branches in your app.

            :param name: The environment variable name.
            :param value: The environment variable value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                environment_variable_property = amplify_mixins.CfnAppPropsMixin.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__424c43fc268ef71b7ee1d8133767aa3e4a877c2445784cacfcfa8c091401e218)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The environment variable name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html#cfn-amplify-app-environmentvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The environment variable value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html#cfn-amplify-app-environmentvariable-value
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
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnAppPropsMixin.JobConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"build_compute_type": "buildComputeType"},
    )
    class JobConfigProperty:
        def __init__(
            self,
            *,
            build_compute_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration details that apply to the jobs for an Amplify app.

            Use ``JobConfig`` to apply configuration to jobs, such as customizing the build instance size when you create or update an Amplify app. For more information about customizable build instances, see `Custom build instances <https://docs.aws.amazon.com/amplify/latest/userguide/custom-build-instance.html>`_ in the *Amplify User Guide* .

            :param build_compute_type: Specifies the size of the build instance. Amplify supports three instance sizes: ``STANDARD_8GB`` , ``LARGE_16GB`` , and ``XLARGE_72GB`` . If you don't specify a value, Amplify uses the ``STANDARD_8GB`` default. The following list describes the CPU, memory, and storage capacity for each build instance type: - **STANDARD_8GB** - - vCPUs: 4 - Memory: 8 GiB - Disk space: 128 GB - **LARGE_16GB** - - vCPUs: 8 - Memory: 16 GiB - Disk space: 128 GB - **XLARGE_72GB** - - vCPUs: 36 - Memory: 72 GiB - Disk space: 256 GB

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-jobconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                job_config_property = amplify_mixins.CfnAppPropsMixin.JobConfigProperty(
                    build_compute_type="buildComputeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9122763fb601fa31de9d419d43841fd7809e38c0cac9cd56b86651feedc3d93c)
                check_type(argname="argument build_compute_type", value=build_compute_type, expected_type=type_hints["build_compute_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if build_compute_type is not None:
                self._values["build_compute_type"] = build_compute_type

        @builtins.property
        def build_compute_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the size of the build instance.

            Amplify supports three instance sizes: ``STANDARD_8GB`` , ``LARGE_16GB`` , and ``XLARGE_72GB`` . If you don't specify a value, Amplify uses the ``STANDARD_8GB`` default.

            The following list describes the CPU, memory, and storage capacity for each build instance type:

            - **STANDARD_8GB** - - vCPUs: 4
            - Memory: 8 GiB
            - Disk space: 128 GB
            - **LARGE_16GB** - - vCPUs: 8
            - Memory: 16 GiB
            - Disk space: 128 GB
            - **XLARGE_72GB** - - vCPUs: 36
            - Memory: 72 GiB
            - Disk space: 256 GB

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-jobconfig.html#cfn-amplify-app-jobconfig-buildcomputetype
            '''
            result = self._values.get("build_compute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnBranchMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "backend": "backend",
        "basic_auth_config": "basicAuthConfig",
        "branch_name": "branchName",
        "build_spec": "buildSpec",
        "compute_role_arn": "computeRoleArn",
        "description": "description",
        "enable_auto_build": "enableAutoBuild",
        "enable_performance_mode": "enablePerformanceMode",
        "enable_pull_request_preview": "enablePullRequestPreview",
        "enable_skew_protection": "enableSkewProtection",
        "environment_variables": "environmentVariables",
        "framework": "framework",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "stage": "stage",
        "tags": "tags",
    },
)
class CfnBranchMixinProps:
    def __init__(
        self,
        *,
        app_id: typing.Optional[builtins.str] = None,
        backend: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBranchPropsMixin.BackendProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        basic_auth_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBranchPropsMixin.BasicAuthConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[builtins.str] = None,
        compute_role_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_skew_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBranchPropsMixin.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        framework: typing.Optional[builtins.str] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBranchPropsMixin.

        :param app_id: The unique ID for an Amplify app.
        :param backend: The backend for a ``Branch`` of an Amplify app. Use for a backend created from an CloudFormation stack. This field is available to Amplify Gen 2 apps only. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code.
        :param basic_auth_config: The basic authorization credentials for a branch of an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param branch_name: The name for the branch.
        :param build_spec: The build specification (build spec) for the branch.
        :param compute_role_arn: The Amazon Resource Name (ARN) of the IAM role to assign to a branch of an SSR app. The SSR Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. For more information about the SSR Compute role, see `Adding an SSR Compute role <https://docs.aws.amazon.com/amplify/latest/userguide/amplify-SSR-compute-role.html>`_ in the *Amplify User Guide* .
        :param description: The description for the branch that is part of an Amplify app.
        :param enable_auto_build: Enables auto building for the branch.
        :param enable_performance_mode: Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        :param enable_pull_request_preview: Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch. To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property. For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .
        :param enable_skew_protection: Specifies whether the skew protection feature is enabled for the branch. Deployment skew protection is available to Amplify applications to eliminate version skew issues between client and servers in web applications. When you apply skew protection to a branch, you can ensure that your clients always interact with the correct version of server-side assets, regardless of when a deployment occurs. For more information about skew protection, see `Skew protection for Amplify deployments <https://docs.aws.amazon.com/amplify/latest/userguide/skew-protection.html>`_ in the *Amplify User Guide* .
        :param environment_variables: The environment variables for the branch.
        :param framework: The framework for the branch.
        :param pull_request_environment_name: If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch. To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` . If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed. For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .
        :param stage: Describes the current stage for the branch.
        :param tags: The tag for the branch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
            
            cfn_branch_mixin_props = amplify_mixins.CfnBranchMixinProps(
                app_id="appId",
                backend=amplify_mixins.CfnBranchPropsMixin.BackendProperty(
                    stack_arn="stackArn"
                ),
                basic_auth_config=amplify_mixins.CfnBranchPropsMixin.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                ),
                branch_name="branchName",
                build_spec="buildSpec",
                compute_role_arn="computeRoleArn",
                description="description",
                enable_auto_build=False,
                enable_performance_mode=False,
                enable_pull_request_preview=False,
                enable_skew_protection=False,
                environment_variables=[amplify_mixins.CfnBranchPropsMixin.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )],
                framework="framework",
                pull_request_environment_name="pullRequestEnvironmentName",
                stage="stage",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d20f87ae7880ae7ad1f48f53d5be4af99d0ae129909c15919ad9a1195332adb)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument basic_auth_config", value=basic_auth_config, expected_type=type_hints["basic_auth_config"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument compute_role_arn", value=compute_role_arn, expected_type=type_hints["compute_role_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_auto_build", value=enable_auto_build, expected_type=type_hints["enable_auto_build"])
            check_type(argname="argument enable_performance_mode", value=enable_performance_mode, expected_type=type_hints["enable_performance_mode"])
            check_type(argname="argument enable_pull_request_preview", value=enable_pull_request_preview, expected_type=type_hints["enable_pull_request_preview"])
            check_type(argname="argument enable_skew_protection", value=enable_skew_protection, expected_type=type_hints["enable_skew_protection"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_id is not None:
            self._values["app_id"] = app_id
        if backend is not None:
            self._values["backend"] = backend
        if basic_auth_config is not None:
            self._values["basic_auth_config"] = basic_auth_config
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if compute_role_arn is not None:
            self._values["compute_role_arn"] = compute_role_arn
        if description is not None:
            self._values["description"] = description
        if enable_auto_build is not None:
            self._values["enable_auto_build"] = enable_auto_build
        if enable_performance_mode is not None:
            self._values["enable_performance_mode"] = enable_performance_mode
        if enable_pull_request_preview is not None:
            self._values["enable_pull_request_preview"] = enable_pull_request_preview
        if enable_skew_protection is not None:
            self._values["enable_skew_protection"] = enable_skew_protection
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if framework is not None:
            self._values["framework"] = framework
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if stage is not None:
            self._values["stage"] = stage
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID for an Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-appid
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backend(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBranchPropsMixin.BackendProperty"]]:
        '''The backend for a ``Branch`` of an Amplify app. Use for a backend created from an CloudFormation stack.

        This field is available to Amplify Gen 2 apps only. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-backend
        '''
        result = self._values.get("backend")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBranchPropsMixin.BackendProperty"]], result)

    @builtins.property
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBranchPropsMixin.BasicAuthConfigProperty"]]:
        '''The basic authorization credentials for a branch of an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-basicauthconfig
        '''
        result = self._values.get("basic_auth_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBranchPropsMixin.BasicAuthConfigProperty"]], result)

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''The name for the branch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-branchname
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for the branch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-buildspec
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role to assign to a branch of an SSR app.

        The SSR Compute role allows the Amplify Hosting compute service to securely access specific AWS resources based on the role's permissions. For more information about the SSR Compute role, see `Adding an SSR Compute role <https://docs.aws.amazon.com/amplify/latest/userguide/amplify-SSR-compute-role.html>`_ in the *Amplify User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-computerolearn
        '''
        result = self._values.get("compute_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the branch that is part of an Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_build(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables auto building for the branch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableautobuild
        '''
        result = self._values.get("enable_auto_build")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_performance_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableperformancemode
        '''
        result = self._values.get("enable_performance_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_pull_request_preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch.

        If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

        To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property.

        For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enablepullrequestpreview
        '''
        result = self._values.get("enable_pull_request_preview")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_skew_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the skew protection feature is enabled for the branch.

        Deployment skew protection is available to Amplify applications to eliminate version skew issues between client and servers in web applications. When you apply skew protection to a branch, you can ensure that your clients always interact with the correct version of server-side assets, regardless of when a deployment occurs. For more information about skew protection, see `Skew protection for Amplify deployments <https://docs.aws.amazon.com/amplify/latest/userguide/skew-protection.html>`_ in the *Amplify User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableskewprotection
        '''
        result = self._values.get("enable_skew_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBranchPropsMixin.EnvironmentVariableProperty"]]]]:
        '''The environment variables for the branch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-environmentvariables
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBranchPropsMixin.EnvironmentVariableProperty"]]]], result)

    @builtins.property
    def framework(self) -> typing.Optional[builtins.str]:
        '''The framework for the branch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-framework
        '''
        result = self._values.get("framework")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews.

        For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch.

        To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` .

        If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.

        For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-pullrequestenvironmentname
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''Describes the current stage for the branch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-stage
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tag for the branch.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBranchMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBranchPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnBranchPropsMixin",
):
    '''The AWS::Amplify::Branch resource specifies a new branch within an app.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html
    :cloudformationResource: AWS::Amplify::Branch
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
        
        cfn_branch_props_mixin = amplify_mixins.CfnBranchPropsMixin(amplify_mixins.CfnBranchMixinProps(
            app_id="appId",
            backend=amplify_mixins.CfnBranchPropsMixin.BackendProperty(
                stack_arn="stackArn"
            ),
            basic_auth_config=amplify_mixins.CfnBranchPropsMixin.BasicAuthConfigProperty(
                enable_basic_auth=False,
                password="password",
                username="username"
            ),
            branch_name="branchName",
            build_spec="buildSpec",
            compute_role_arn="computeRoleArn",
            description="description",
            enable_auto_build=False,
            enable_performance_mode=False,
            enable_pull_request_preview=False,
            enable_skew_protection=False,
            environment_variables=[amplify_mixins.CfnBranchPropsMixin.EnvironmentVariableProperty(
                name="name",
                value="value"
            )],
            framework="framework",
            pull_request_environment_name="pullRequestEnvironmentName",
            stage="stage",
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
        props: typing.Union[CfnBranchMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Amplify::Branch``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04deb53363a362a10428547718953f0d05949754ecdaf6219ef18a06a5a57d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c1de6ab99b271db895fbc435bd3ddebe03f6fbf9e64ac991431fe3b3be55d4e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7f1bec3cd0391556941fa0de0fb850b4047fcb19835bb8ebd912a7c0b35902)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBranchMixinProps:
        return typing.cast(CfnBranchMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnBranchPropsMixin.BackendProperty",
        jsii_struct_bases=[],
        name_mapping={"stack_arn": "stackArn"},
    )
    class BackendProperty:
        def __init__(self, *, stack_arn: typing.Optional[builtins.str] = None) -> None:
            '''Describes the backend associated with an Amplify ``Branch`` .

            This property is available to Amplify Gen 2 apps only. When you deploy an application with Amplify Gen 2, you provision the app's backend infrastructure using Typescript code.

            :param stack_arn: The Amazon Resource Name (ARN) for the CloudFormation stack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-backend.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                backend_property = amplify_mixins.CfnBranchPropsMixin.BackendProperty(
                    stack_arn="stackArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce4d6b9171693fc3c66f1dc65246f5683e3db5162c69d856b04a8f47e8f6f3f9)
                check_type(argname="argument stack_arn", value=stack_arn, expected_type=type_hints["stack_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stack_arn is not None:
                self._values["stack_arn"] = stack_arn

        @builtins.property
        def stack_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the CloudFormation stack.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-backend.html#cfn-amplify-branch-backend-stackarn
            '''
            result = self._values.get("stack_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackendProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnBranchPropsMixin.BasicAuthConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_basic_auth": "enableBasicAuth",
            "password": "password",
            "username": "username",
        },
    )
    class BasicAuthConfigProperty:
        def __init__(
            self,
            *,
            enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the BasicAuthConfig property type to set password protection for a specific branch.

            :param enable_basic_auth: Enables basic authorization for the branch.
            :param password: The password for basic authorization.
            :param username: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                basic_auth_config_property = amplify_mixins.CfnBranchPropsMixin.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aecaf9dbe8dc141d118a0c9bfd12849da582199bdb408aba4360b6cd6ec67efe)
                check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_basic_auth is not None:
                self._values["enable_basic_auth"] = enable_basic_auth
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def enable_basic_auth(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables basic authorization for the branch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-enablebasicauth
            '''
            result = self._values.get("enable_basic_auth")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password for basic authorization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnBranchPropsMixin.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentVariableProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The EnvironmentVariable property type sets environment variables for a specific branch.

            Environment variables are key-value pairs that are available at build time.

            :param name: The environment variable name.
            :param value: The environment variable value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                environment_variable_property = amplify_mixins.CfnBranchPropsMixin.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3034546195d92a21658c547b406b3e208caa1b1c0bc39970b67650ce82537bc)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The environment variable name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html#cfn-amplify-branch-environmentvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The environment variable value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html#cfn-amplify-branch-environmentvariable-value
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
    jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnDomainMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "auto_sub_domain_creation_patterns": "autoSubDomainCreationPatterns",
        "auto_sub_domain_iam_role": "autoSubDomainIamRole",
        "certificate_settings": "certificateSettings",
        "domain_name": "domainName",
        "enable_auto_sub_domain": "enableAutoSubDomain",
        "sub_domain_settings": "subDomainSettings",
    },
)
class CfnDomainMixinProps:
    def __init__(
        self,
        *,
        app_id: typing.Optional[builtins.str] = None,
        auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
        certificate_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.CertificateSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        sub_domain_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.SubDomainSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnDomainPropsMixin.

        :param app_id: The unique ID for an Amplify app.
        :param auto_sub_domain_creation_patterns: Sets the branch patterns for automatic subdomain creation.
        :param auto_sub_domain_iam_role: The required AWS Identity and Access Management (IAMlong) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.
        :param certificate_settings: The type of SSL/TLS certificate to use for your custom domain. If you don't specify a certificate type, Amplify uses the default certificate that it provisions and manages for you.
        :param domain_name: The domain name for the domain association.
        :param enable_auto_sub_domain: Enables the automated creation of subdomains for branches.
        :param sub_domain_settings: The setting for the subdomain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
            
            cfn_domain_mixin_props = amplify_mixins.CfnDomainMixinProps(
                app_id="appId",
                auto_sub_domain_creation_patterns=["autoSubDomainCreationPatterns"],
                auto_sub_domain_iam_role="autoSubDomainIamRole",
                certificate_settings=amplify_mixins.CfnDomainPropsMixin.CertificateSettingsProperty(
                    certificate_type="certificateType",
                    custom_certificate_arn="customCertificateArn"
                ),
                domain_name="domainName",
                enable_auto_sub_domain=False,
                sub_domain_settings=[amplify_mixins.CfnDomainPropsMixin.SubDomainSettingProperty(
                    branch_name="branchName",
                    prefix="prefix"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8559fa9e3de266a201c1c2e5450a7a7ec7280bb5a489395b4e055b2f6cbbae)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument auto_sub_domain_creation_patterns", value=auto_sub_domain_creation_patterns, expected_type=type_hints["auto_sub_domain_creation_patterns"])
            check_type(argname="argument auto_sub_domain_iam_role", value=auto_sub_domain_iam_role, expected_type=type_hints["auto_sub_domain_iam_role"])
            check_type(argname="argument certificate_settings", value=certificate_settings, expected_type=type_hints["certificate_settings"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_auto_sub_domain", value=enable_auto_sub_domain, expected_type=type_hints["enable_auto_sub_domain"])
            check_type(argname="argument sub_domain_settings", value=sub_domain_settings, expected_type=type_hints["sub_domain_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_id is not None:
            self._values["app_id"] = app_id
        if auto_sub_domain_creation_patterns is not None:
            self._values["auto_sub_domain_creation_patterns"] = auto_sub_domain_creation_patterns
        if auto_sub_domain_iam_role is not None:
            self._values["auto_sub_domain_iam_role"] = auto_sub_domain_iam_role
        if certificate_settings is not None:
            self._values["certificate_settings"] = certificate_settings
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_auto_sub_domain is not None:
            self._values["enable_auto_sub_domain"] = enable_auto_sub_domain
        if sub_domain_settings is not None:
            self._values["sub_domain_settings"] = sub_domain_settings

    @builtins.property
    def app_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID for an Amplify app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-appid
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_sub_domain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Sets the branch patterns for automatic subdomain creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomaincreationpatterns
        '''
        result = self._values.get("auto_sub_domain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_sub_domain_iam_role(self) -> typing.Optional[builtins.str]:
        '''The required AWS Identity and Access Management (IAMlong) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomainiamrole
        '''
        result = self._values.get("auto_sub_domain_iam_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.CertificateSettingsProperty"]]:
        '''The type of SSL/TLS certificate to use for your custom domain.

        If you don't specify a certificate type, Amplify uses the default certificate that it provisions and manages for you.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-certificatesettings
        '''
        result = self._values.get("certificate_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.CertificateSettingsProperty"]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the domain association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_sub_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables the automated creation of subdomains for branches.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-enableautosubdomain
        '''
        result = self._values.get("enable_auto_sub_domain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def sub_domain_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SubDomainSettingProperty"]]]]:
        '''The setting for the subdomain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-subdomainsettings
        '''
        result = self._values.get("sub_domain_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.SubDomainSettingProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnDomainPropsMixin",
):
    '''Specifies the AWS::Amplify::Domain resource that enables you to connect a custom domain to your app.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html
    :cloudformationResource: AWS::Amplify::Domain
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
        
        cfn_domain_props_mixin = amplify_mixins.CfnDomainPropsMixin(amplify_mixins.CfnDomainMixinProps(
            app_id="appId",
            auto_sub_domain_creation_patterns=["autoSubDomainCreationPatterns"],
            auto_sub_domain_iam_role="autoSubDomainIamRole",
            certificate_settings=amplify_mixins.CfnDomainPropsMixin.CertificateSettingsProperty(
                certificate_type="certificateType",
                custom_certificate_arn="customCertificateArn"
            ),
            domain_name="domainName",
            enable_auto_sub_domain=False,
            sub_domain_settings=[amplify_mixins.CfnDomainPropsMixin.SubDomainSettingProperty(
                branch_name="branchName",
                prefix="prefix"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Amplify::Domain``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed280363f43fcd6284c39dac9f7bacf7d4e7ddd843fd2d17c14afbe765c5480a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71f7b1f34c8778dcc4721ac4dd8ad06e1a6c6dafa460cc94e2b787332c62289a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b85b9b1cd791b458976fbd2716a4c1edc2b17f8f21b42ebb0ffbd60a97d852)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainMixinProps:
        return typing.cast(CfnDomainMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnDomainPropsMixin.CertificateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "certificate_type": "certificateType",
            "certificate_verification_dns_record": "certificateVerificationDnsRecord",
        },
    )
    class CertificateProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
            certificate_type: typing.Optional[builtins.str] = None,
            certificate_verification_dns_record: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the SSL/TLS certificate for the domain association.

            This can be your own custom certificate or the default certificate that Amplify provisions for you.

            If you are updating your domain to use a different certificate, ``Certificate`` points to the new certificate that is being created instead of the current active certificate. Otherwise, ``Certificate`` points to the current active certificate.

            :param certificate_arn: The Amazon resource name (ARN) for a custom certificate that you have already added to Certificate Manager in your AWS account . This field is required only when the certificate type is ``CUSTOM`` .
            :param certificate_type: The type of SSL/TLS certificate that you want to use. Specify ``AMPLIFY_MANAGED`` to use the default certificate that Amplify provisions for you. Specify ``CUSTOM`` to use your own certificate that you have already added to Certificate Manager in your AWS account . Make sure you request (or import) the certificate in the US East (N. Virginia) Region (us-east-1). For more information about using ACM, see `Importing certificates into Certificate Manager <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *ACM User guide* .
            :param certificate_verification_dns_record: The DNS record for certificate verification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-certificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                certificate_property = amplify_mixins.CfnDomainPropsMixin.CertificateProperty(
                    certificate_arn="certificateArn",
                    certificate_type="certificateType",
                    certificate_verification_dns_record="certificateVerificationDnsRecord"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e4e0f0d6972661d934946d640394aebe9f256af9b4a93d80753e0b2eb71018c)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument certificate_type", value=certificate_type, expected_type=type_hints["certificate_type"])
                check_type(argname="argument certificate_verification_dns_record", value=certificate_verification_dns_record, expected_type=type_hints["certificate_verification_dns_record"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if certificate_type is not None:
                self._values["certificate_type"] = certificate_type
            if certificate_verification_dns_record is not None:
                self._values["certificate_verification_dns_record"] = certificate_verification_dns_record

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon resource name (ARN) for a custom certificate that you have already added to Certificate Manager in your AWS account .

            This field is required only when the certificate type is ``CUSTOM`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-certificate.html#cfn-amplify-domain-certificate-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def certificate_type(self) -> typing.Optional[builtins.str]:
            '''The type of SSL/TLS certificate that you want to use.

            Specify ``AMPLIFY_MANAGED`` to use the default certificate that Amplify provisions for you.

            Specify ``CUSTOM`` to use your own certificate that you have already added to Certificate Manager in your AWS account . Make sure you request (or import) the certificate in the US East (N. Virginia) Region (us-east-1). For more information about using ACM, see `Importing certificates into Certificate Manager <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *ACM User guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-certificate.html#cfn-amplify-domain-certificate-certificatetype
            '''
            result = self._values.get("certificate_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def certificate_verification_dns_record(self) -> typing.Optional[builtins.str]:
            '''The DNS record for certificate verification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-certificate.html#cfn-amplify-domain-certificate-certificateverificationdnsrecord
            '''
            result = self._values.get("certificate_verification_dns_record")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnDomainPropsMixin.CertificateSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_type": "certificateType",
            "custom_certificate_arn": "customCertificateArn",
        },
    )
    class CertificateSettingsProperty:
        def __init__(
            self,
            *,
            certificate_type: typing.Optional[builtins.str] = None,
            custom_certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The type of SSL/TLS certificate to use for your custom domain.

            If a certificate type isn't specified, Amplify uses the default ``AMPLIFY_MANAGED`` certificate.

            :param certificate_type: The certificate type. Specify ``AMPLIFY_MANAGED`` to use the default certificate that Amplify provisions for you. Specify ``CUSTOM`` to use your own certificate that you have already added to Certificate Manager in your AWS account . Make sure you request (or import) the certificate in the US East (N. Virginia) Region (us-east-1). For more information about using ACM, see `Importing certificates into Certificate Manager <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *ACM User guide* .
            :param custom_certificate_arn: The Amazon resource name (ARN) for the custom certificate that you have already added to Certificate Manager in your AWS account . This field is required only when the certificate type is ``CUSTOM`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-certificatesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                certificate_settings_property = amplify_mixins.CfnDomainPropsMixin.CertificateSettingsProperty(
                    certificate_type="certificateType",
                    custom_certificate_arn="customCertificateArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fab1b0fb7ca4394cef6caa0aa6846739072ab6379760be76325901d5ee7eedcd)
                check_type(argname="argument certificate_type", value=certificate_type, expected_type=type_hints["certificate_type"])
                check_type(argname="argument custom_certificate_arn", value=custom_certificate_arn, expected_type=type_hints["custom_certificate_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_type is not None:
                self._values["certificate_type"] = certificate_type
            if custom_certificate_arn is not None:
                self._values["custom_certificate_arn"] = custom_certificate_arn

        @builtins.property
        def certificate_type(self) -> typing.Optional[builtins.str]:
            '''The certificate type.

            Specify ``AMPLIFY_MANAGED`` to use the default certificate that Amplify provisions for you.

            Specify ``CUSTOM`` to use your own certificate that you have already added to Certificate Manager in your AWS account . Make sure you request (or import) the certificate in the US East (N. Virginia) Region (us-east-1). For more information about using ACM, see `Importing certificates into Certificate Manager <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *ACM User guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-certificatesettings.html#cfn-amplify-domain-certificatesettings-certificatetype
            '''
            result = self._values.get("certificate_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon resource name (ARN) for the custom certificate that you have already added to Certificate Manager in your AWS account .

            This field is required only when the certificate type is ``CUSTOM`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-certificatesettings.html#cfn-amplify-domain-certificatesettings-customcertificatearn
            '''
            result = self._values.get("custom_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_amplify.mixins.CfnDomainPropsMixin.SubDomainSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"branch_name": "branchName", "prefix": "prefix"},
    )
    class SubDomainSettingProperty:
        def __init__(
            self,
            *,
            branch_name: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The SubDomainSetting property type enables you to connect a subdomain (for example, example.exampledomain.com) to a specific branch.

            :param branch_name: The branch name setting for the subdomain. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
            :param prefix: The prefix setting for the subdomain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_amplify import mixins as amplify_mixins
                
                sub_domain_setting_property = amplify_mixins.CfnDomainPropsMixin.SubDomainSettingProperty(
                    branch_name="branchName",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7139a674e280894cdefcae7d5410f5748cc0fce10f063fc005e5789193a10f23)
                check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if branch_name is not None:
                self._values["branch_name"] = branch_name
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def branch_name(self) -> typing.Optional[builtins.str]:
            '''The branch name setting for the subdomain.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            *Pattern:* (?s).+

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html#cfn-amplify-domain-subdomainsetting-branchname
            '''
            result = self._values.get("branch_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix setting for the subdomain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html#cfn-amplify-domain-subdomainsetting-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubDomainSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAppMixinProps",
    "CfnAppPropsMixin",
    "CfnBranchMixinProps",
    "CfnBranchPropsMixin",
    "CfnDomainMixinProps",
    "CfnDomainPropsMixin",
]

publication.publish()

def _typecheckingstub__491cf09d3c3dbe1c8a80a90a6f3aa38ae700af4da457fa228eac630a79e84749(
    *,
    access_token: typing.Optional[builtins.str] = None,
    auto_branch_creation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.AutoBranchCreationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    basic_auth_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    cache_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.CacheConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    compute_role_arn: typing.Optional[builtins.str] = None,
    custom_headers: typing.Optional[builtins.str] = None,
    custom_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.CustomRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    iam_service_role: typing.Optional[builtins.str] = None,
    job_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.JobConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    oauth_token: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0779f99136f3e972a2faa60ebb0f7d82e0f6589b98a0b3016874cc18a6d829(
    props: typing.Union[CfnAppMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2ca9ffa03d6e3cbc9f583a02304d9a56b6876f9bacc76c008d79e1344b3b10(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c067b61126d2da68584d921d94a9d1ee2839c076b8964b4026c8e03f7bfbfa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90266383c2db12f7f18c1a037797e9afa1432c4ab4ff58488a57e4c650df1332(
    *,
    auto_branch_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    basic_auth_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    enable_auto_branch_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAppPropsMixin.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    framework: typing.Optional[builtins.str] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a76184300b47cf6c80fbd6378c0a94736d330fc21430f78d4ff7df575bee377(
    *,
    enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30cb868617d871cf5a5a17a03dabc2af0f932392ae2d3c3d79db85a9c39e616e(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aac565f5494ac94b33a8604988964e6a36e92c23b58a2277958412e70ae409b(
    *,
    condition: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424c43fc268ef71b7ee1d8133767aa3e4a877c2445784cacfcfa8c091401e218(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9122763fb601fa31de9d419d43841fd7809e38c0cac9cd56b86651feedc3d93c(
    *,
    build_compute_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d20f87ae7880ae7ad1f48f53d5be4af99d0ae129909c15919ad9a1195332adb(
    *,
    app_id: typing.Optional[builtins.str] = None,
    backend: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBranchPropsMixin.BackendProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    basic_auth_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBranchPropsMixin.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[builtins.str] = None,
    compute_role_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_auto_build: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_skew_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBranchPropsMixin.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    framework: typing.Optional[builtins.str] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04deb53363a362a10428547718953f0d05949754ecdaf6219ef18a06a5a57d9(
    props: typing.Union[CfnBranchMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c1de6ab99b271db895fbc435bd3ddebe03f6fbf9e64ac991431fe3b3be55d4e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7f1bec3cd0391556941fa0de0fb850b4047fcb19835bb8ebd912a7c0b35902(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4d6b9171693fc3c66f1dc65246f5683e3db5162c69d856b04a8f47e8f6f3f9(
    *,
    stack_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecaf9dbe8dc141d118a0c9bfd12849da582199bdb408aba4360b6cd6ec67efe(
    *,
    enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3034546195d92a21658c547b406b3e208caa1b1c0bc39970b67650ce82537bc(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8559fa9e3de266a201c1c2e5450a7a7ec7280bb5a489395b4e055b2f6cbbae(
    *,
    app_id: typing.Optional[builtins.str] = None,
    auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
    certificate_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.CertificateSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sub_domain_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.SubDomainSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed280363f43fcd6284c39dac9f7bacf7d4e7ddd843fd2d17c14afbe765c5480a(
    props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f7b1f34c8778dcc4721ac4dd8ad06e1a6c6dafa460cc94e2b787332c62289a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b85b9b1cd791b458976fbd2716a4c1edc2b17f8f21b42ebb0ffbd60a97d852(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4e0f0d6972661d934946d640394aebe9f256af9b4a93d80753e0b2eb71018c(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
    certificate_type: typing.Optional[builtins.str] = None,
    certificate_verification_dns_record: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab1b0fb7ca4394cef6caa0aa6846739072ab6379760be76325901d5ee7eedcd(
    *,
    certificate_type: typing.Optional[builtins.str] = None,
    custom_certificate_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7139a674e280894cdefcae7d5410f5748cc0fce10f063fc005e5789193a10f23(
    *,
    branch_name: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
