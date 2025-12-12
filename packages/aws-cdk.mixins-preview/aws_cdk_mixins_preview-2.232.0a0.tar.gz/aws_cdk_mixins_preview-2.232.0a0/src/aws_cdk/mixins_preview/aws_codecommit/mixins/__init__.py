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
    jsii_type="@aws-cdk/mixins-preview.aws_codecommit.mixins.CfnRepositoryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "code": "code",
        "kms_key_id": "kmsKeyId",
        "repository_description": "repositoryDescription",
        "repository_name": "repositoryName",
        "tags": "tags",
        "triggers": "triggers",
    },
)
class CfnRepositoryMixinProps:
    def __init__(
        self,
        *,
        code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRepositoryPropsMixin.CodeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        repository_description: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRepositoryPropsMixin.RepositoryTriggerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnRepositoryPropsMixin.

        :param code: Information about code to be committed to a repository after it is created in an AWS CloudFormation stack. Information about code is only used in resource creation. Updates to a stack will not reflect changes made to code properties after initial resource creation. .. epigraph:: You can only use this property to add code when creating a repository with a CloudFormation template at creation time. This property cannot be used for updating code to an existing repository.
        :param kms_key_id: The ID of the AWS Key Management Service encryption key used to encrypt and decrypt the repository. .. epigraph:: The input can be the full ARN, the key ID, or the key alias. For more information, see `Finding the key ID and key ARN <https://docs.aws.amazon.com/kms/latest/developerguide/find-cmk-id-arn.html>`_ .
        :param repository_description: A comment or description about the new repository. .. epigraph:: The description field for a repository accepts all HTML characters and all valid Unicode characters. Applications that do not HTML-encode the description and display it in a webpage can expose users to potentially malicious code. Make sure that you HTML-encode the description field in any application that uses this API to display the repository description on a webpage.
        :param repository_name: The name of the new repository to be created. .. epigraph:: The repository name must be unique across the calling AWS account . Repository names are limited to 100 alphanumeric, dash, and underscore characters, and cannot include certain characters. For more information about the limits on repository names, see `Quotas <https://docs.aws.amazon.com/codecommit/latest/userguide/limits.html>`_ in the *AWS CodeCommit User Guide* . The suffix .git is prohibited.
        :param tags: One or more tag key-value pairs to use when tagging this repository.
        :param triggers: The JSON block of configuration information for each trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_codecommit import mixins as codecommit_mixins
            
            cfn_repository_mixin_props = codecommit_mixins.CfnRepositoryMixinProps(
                code=codecommit_mixins.CfnRepositoryPropsMixin.CodeProperty(
                    branch_name="branchName",
                    s3=codecommit_mixins.CfnRepositoryPropsMixin.S3Property(
                        bucket="bucket",
                        key="key",
                        object_version="objectVersion"
                    )
                ),
                kms_key_id="kmsKeyId",
                repository_description="repositoryDescription",
                repository_name="repositoryName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                triggers=[codecommit_mixins.CfnRepositoryPropsMixin.RepositoryTriggerProperty(
                    branches=["branches"],
                    custom_data="customData",
                    destination_arn="destinationArn",
                    events=["events"],
                    name="name"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f0bdd37028aeec3fe0fd52ebaa16211cb96b010fb743ab58af5ffcd9531815)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument repository_description", value=repository_description, expected_type=type_hints["repository_description"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code is not None:
            self._values["code"] = code
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if repository_description is not None:
            self._values["repository_description"] = repository_description
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if tags is not None:
            self._values["tags"] = tags
        if triggers is not None:
            self._values["triggers"] = triggers

    @builtins.property
    def code(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.CodeProperty"]]:
        '''Information about code to be committed to a repository after it is created in an AWS CloudFormation stack.

        Information about code is only used in resource creation. Updates to a stack will not reflect changes made to code properties after initial resource creation.
        .. epigraph::

           You can only use this property to add code when creating a repository with a CloudFormation template at creation time. This property cannot be used for updating code to an existing repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.CodeProperty"]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS Key Management Service encryption key used to encrypt and decrypt the repository.

        .. epigraph::

           The input can be the full ARN, the key ID, or the key alias. For more information, see `Finding the key ID and key ARN <https://docs.aws.amazon.com/kms/latest/developerguide/find-cmk-id-arn.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_description(self) -> typing.Optional[builtins.str]:
        '''A comment or description about the new repository.

        .. epigraph::

           The description field for a repository accepts all HTML characters and all valid Unicode characters. Applications that do not HTML-encode the description and display it in a webpage can expose users to potentially malicious code. Make sure that you HTML-encode the description field in any application that uses this API to display the repository description on a webpage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositorydescription
        '''
        result = self._values.get("repository_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''The name of the new repository to be created.

        .. epigraph::

           The repository name must be unique across the calling AWS account . Repository names are limited to 100 alphanumeric, dash, and underscore characters, and cannot include certain characters. For more information about the limits on repository names, see `Quotas <https://docs.aws.amazon.com/codecommit/latest/userguide/limits.html>`_ in the *AWS CodeCommit User Guide* . The suffix .git is prohibited.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositoryname
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tag key-value pairs to use when tagging this repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.RepositoryTriggerProperty"]]]]:
        '''The JSON block of configuration information for each trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-triggers
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.RepositoryTriggerProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRepositoryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_codecommit.mixins.CfnRepositoryPropsMixin",
):
    '''Creates a new, empty repository.

    .. epigraph::

       AWS CodeCommit is no longer available to new customers. Existing customers of AWS CodeCommit can continue to use the service as normal. `Learn more" <https://docs.aws.amazon.com/devops/how-to-migrate-your-aws-codecommit-repository-to-another-git-provider>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html
    :cloudformationResource: AWS::CodeCommit::Repository
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_codecommit import mixins as codecommit_mixins
        
        cfn_repository_props_mixin = codecommit_mixins.CfnRepositoryPropsMixin(codecommit_mixins.CfnRepositoryMixinProps(
            code=codecommit_mixins.CfnRepositoryPropsMixin.CodeProperty(
                branch_name="branchName",
                s3=codecommit_mixins.CfnRepositoryPropsMixin.S3Property(
                    bucket="bucket",
                    key="key",
                    object_version="objectVersion"
                )
            ),
            kms_key_id="kmsKeyId",
            repository_description="repositoryDescription",
            repository_name="repositoryName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            triggers=[codecommit_mixins.CfnRepositoryPropsMixin.RepositoryTriggerProperty(
                branches=["branches"],
                custom_data="customData",
                destination_arn="destinationArn",
                events=["events"],
                name="name"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CodeCommit::Repository``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9682f62a48548925fb79902db35f5812557b482afe8633e12b6d6da55f8a2cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d3ef2f8c0c2d9ab126542f1435c8d14458a8598b05ed51e546a228876bca3d2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3864c857f2b0d9b04ddc648f54d7b6fd7a24dd7b71eecbcd1fd9648f73b3bb1c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRepositoryMixinProps:
        return typing.cast(CfnRepositoryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codecommit.mixins.CfnRepositoryPropsMixin.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={"branch_name": "branchName", "s3": "s3"},
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            branch_name: typing.Optional[builtins.str] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRepositoryPropsMixin.S3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about code to be committed.

            :param branch_name: Optional. Specifies a branch name to be used as the default branch when importing code into a repository on initial creation. If this property is not set, the name *main* will be used for the default branch for the repository. Changes to this property are ignored after initial resource creation. We recommend using this parameter to set the name to *main* to align with the default behavior of CodeCommit unless another name is needed.
            :param s3: Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository. Changes to this property are ignored after initial resource creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-code.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codecommit import mixins as codecommit_mixins
                
                code_property = codecommit_mixins.CfnRepositoryPropsMixin.CodeProperty(
                    branch_name="branchName",
                    s3=codecommit_mixins.CfnRepositoryPropsMixin.S3Property(
                        bucket="bucket",
                        key="key",
                        object_version="objectVersion"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4a0daa449f742951cf1b6569d9f7963afcd322592ea20ccea2bee43e907956b)
                check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if branch_name is not None:
                self._values["branch_name"] = branch_name
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def branch_name(self) -> typing.Optional[builtins.str]:
            '''Optional.

            Specifies a branch name to be used as the default branch when importing code into a repository on initial creation. If this property is not set, the name *main* will be used for the default branch for the repository. Changes to this property are ignored after initial resource creation. We recommend using this parameter to set the name to *main* to align with the default behavior of CodeCommit unless another name is needed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-code.html#cfn-codecommit-repository-code-branchname
            '''
            result = self._values.get("branch_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.S3Property"]]:
            '''Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository.

            Changes to this property are ignored after initial resource creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-code.html#cfn-codecommit-repository-code-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRepositoryPropsMixin.S3Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codecommit.mixins.CfnRepositoryPropsMixin.RepositoryTriggerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "branches": "branches",
            "custom_data": "customData",
            "destination_arn": "destinationArn",
            "events": "events",
            "name": "name",
        },
    )
    class RepositoryTriggerProperty:
        def __init__(
            self,
            *,
            branches: typing.Optional[typing.Sequence[builtins.str]] = None,
            custom_data: typing.Optional[builtins.str] = None,
            destination_arn: typing.Optional[builtins.str] = None,
            events: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a trigger for a repository.

            .. epigraph::

               If you want to receive notifications about repository events, consider using notifications instead of triggers. For more information, see `Configuring notifications for repository events <https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-repository-email.html>`_ .

            :param branches: The branches to be included in the trigger configuration. If you specify an empty array, the trigger applies to all branches. .. epigraph:: Although no content is required in the array, you must include the array itself.
            :param custom_data: Any custom data associated with the trigger to be included in the information sent to the target of the trigger.
            :param destination_arn: The ARN of the resource that is the target for a trigger (for example, the ARN of a topic in Amazon SNS).
            :param events: The repository events that cause the trigger to run actions in another service, such as sending a notification through Amazon SNS. .. epigraph:: The valid value "all" cannot be used with any other values.
            :param name: The name of the trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codecommit import mixins as codecommit_mixins
                
                repository_trigger_property = codecommit_mixins.CfnRepositoryPropsMixin.RepositoryTriggerProperty(
                    branches=["branches"],
                    custom_data="customData",
                    destination_arn="destinationArn",
                    events=["events"],
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e7222997aa23ddd4ba91049c64f430ed3e31beb1ea510a571f2b42b1c2ed9e1)
                check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
                check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if branches is not None:
                self._values["branches"] = branches
            if custom_data is not None:
                self._values["custom_data"] = custom_data
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn
            if events is not None:
                self._values["events"] = events
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def branches(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The branches to be included in the trigger configuration.

            If you specify an empty array, the trigger applies to all branches.
            .. epigraph::

               Although no content is required in the array, you must include the array itself.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-branches
            '''
            result = self._values.get("branches")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def custom_data(self) -> typing.Optional[builtins.str]:
            '''Any custom data associated with the trigger to be included in the information sent to the target of the trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-customdata
            '''
            result = self._values.get("custom_data")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the resource that is the target for a trigger (for example, the ARN of a topic in Amazon SNS).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-destinationarn
            '''
            result = self._values.get("destination_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The repository events that cause the trigger to run actions in another service, such as sending a notification through Amazon SNS.

            .. epigraph::

               The valid value "all" cannot be used with any other values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the trigger.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RepositoryTriggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_codecommit.mixins.CfnRepositoryPropsMixin.S3Property",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "object_version": "objectVersion",
        },
    )
    class S3Property:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the Amazon S3 bucket that contains the code that will be committed to the new repository.

            Changes to this property are ignored after initial resource creation.

            :param bucket: The name of the Amazon S3 bucket that contains the ZIP file with the content that will be committed to the new repository. This can be specified using the name of the bucket in the AWS account . Changes to this property are ignored after initial resource creation.
            :param key: The key to use for accessing the Amazon S3 bucket. Changes to this property are ignored after initial resource creation. For more information, see `Creating object key names <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html>`_ and `Uploading objects <https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html>`_ in the Amazon S3 User Guide.
            :param object_version: The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket. Changes to this property are ignored after initial resource creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_codecommit import mixins as codecommit_mixins
                
                s3_property = codecommit_mixins.CfnRepositoryPropsMixin.S3Property(
                    bucket="bucket",
                    key="key",
                    object_version="objectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__279c14aa7ea1e91cfb4a7d0634ecc56e356777ac93a2a94bd2b35172df0091a7)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument object_version", value=object_version, expected_type=type_hints["object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key
            if object_version is not None:
                self._values["object_version"] = object_version

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket that contains the ZIP file with the content that will be committed to the new repository.

            This can be specified using the name of the bucket in the AWS account . Changes to this property are ignored after initial resource creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html#cfn-codecommit-repository-s3-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key to use for accessing the Amazon S3 bucket.

            Changes to this property are ignored after initial resource creation. For more information, see `Creating object key names <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html>`_ and `Uploading objects <https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html>`_ in the Amazon S3 User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html#cfn-codecommit-repository-s3-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            '''The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket.

            Changes to this property are ignored after initial resource creation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html#cfn-codecommit-repository-s3-objectversion
            '''
            result = self._values.get("object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnRepositoryMixinProps",
    "CfnRepositoryPropsMixin",
]

publication.publish()

def _typecheckingstub__21f0bdd37028aeec3fe0fd52ebaa16211cb96b010fb743ab58af5ffcd9531815(
    *,
    code: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRepositoryPropsMixin.CodeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    repository_description: typing.Optional[builtins.str] = None,
    repository_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    triggers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRepositoryPropsMixin.RepositoryTriggerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9682f62a48548925fb79902db35f5812557b482afe8633e12b6d6da55f8a2cb(
    props: typing.Union[CfnRepositoryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3ef2f8c0c2d9ab126542f1435c8d14458a8598b05ed51e546a228876bca3d2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3864c857f2b0d9b04ddc648f54d7b6fd7a24dd7b71eecbcd1fd9648f73b3bb1c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a0daa449f742951cf1b6569d9f7963afcd322592ea20ccea2bee43e907956b(
    *,
    branch_name: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRepositoryPropsMixin.S3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7222997aa23ddd4ba91049c64f430ed3e31beb1ea510a571f2b42b1c2ed9e1(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_data: typing.Optional[builtins.str] = None,
    destination_arn: typing.Optional[builtins.str] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279c14aa7ea1e91cfb4a7d0634ecc56e356777ac93a2a94bd2b35172df0091a7(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
