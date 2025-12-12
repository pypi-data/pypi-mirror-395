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


@jsii.implements(_IMixin_11e4b965)
class AutoDeleteObjects(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.AutoDeleteObjects",
):
    '''(experimental) S3-specific mixin for auto-deleting objects.

    :stability: experimental
    :mixin: true
    :exampleMetadata: infused

    Example::

        bucket = s3.CfnBucket(scope, "Bucket")
        Mixins.of(bucket).apply(AutoDeleteObjects())
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''(experimental) Applies the mixin functionality to the target construct.

        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb5c6efe66133c819e03a85248d34a1546552976e543c729b7c59473feeaa5e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''(experimental) Determines whether this mixin can be applied to the given construct.

        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__115e9c22c6e163c9a298d1fdfa9412db199559c6b0db57bdf647c6aa33591410)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessGrantMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_grants_location_configuration": "accessGrantsLocationConfiguration",
        "access_grants_location_id": "accessGrantsLocationId",
        "application_arn": "applicationArn",
        "grantee": "grantee",
        "permission": "permission",
        "s3_prefix_type": "s3PrefixType",
        "tags": "tags",
    },
)
class CfnAccessGrantMixinProps:
    def __init__(
        self,
        *,
        access_grants_location_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessGrantPropsMixin.AccessGrantsLocationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        access_grants_location_id: typing.Optional[builtins.str] = None,
        application_arn: typing.Optional[builtins.str] = None,
        grantee: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessGrantPropsMixin.GranteeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        permission: typing.Optional[builtins.str] = None,
        s3_prefix_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessGrantPropsMixin.

        :param access_grants_location_configuration: The configuration options of the grant location. The grant location is the S3 path to the data to which you are granting access. It contains the ``S3SubPrefix`` field. The grant scope is the result of appending the subprefix to the location scope of the registered location.
        :param access_grants_location_id: The ID of the registered location to which you are granting access. S3 Access Grants assigns this ID when you register the location. S3 Access Grants assigns the ID ``default`` to the default location ``s3://`` and assigns an auto-generated ID to other locations that you register.
        :param application_arn: The Amazon Resource Name (ARN) of an AWS IAM Identity Center application associated with your Identity Center instance. If the grant includes an application ARN, the grantee can only access the S3 data through this application.
        :param grantee: The user, group, or role to which you are granting access. You can grant access to an IAM user or role. If you have added your corporate directory to AWS IAM Identity Center and associated your Identity Center instance with your S3 Access Grants instance, the grantee can also be a corporate directory user or group.
        :param permission: The type of access that you are granting to your S3 data, which can be set to one of the following values: - ``READ`` – Grant read-only access to the S3 data. - ``WRITE`` – Grant write-only access to the S3 data. - ``READWRITE`` – Grant both read and write access to the S3 data.
        :param s3_prefix_type: The type of ``S3SubPrefix`` . The only possible value is ``Object`` . Pass this value if the access grant scope is an object. Do not pass this value if the access grant scope is a bucket or a bucket and a prefix.
        :param tags: The AWS resource tags that you are adding to the access grant. Each tag is a label consisting of a user-defined key and value. Tags can help you manage, identify, organize, search for, and filter resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrant.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
            
            cfn_access_grant_mixin_props = s3_mixins.CfnAccessGrantMixinProps(
                access_grants_location_configuration=s3_mixins.CfnAccessGrantPropsMixin.AccessGrantsLocationConfigurationProperty(
                    s3_sub_prefix="s3SubPrefix"
                ),
                access_grants_location_id="accessGrantsLocationId",
                application_arn="applicationArn",
                grantee=s3_mixins.CfnAccessGrantPropsMixin.GranteeProperty(
                    grantee_identifier="granteeIdentifier",
                    grantee_type="granteeType"
                ),
                permission="permission",
                s3_prefix_type="s3PrefixType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d63a79f6b3185ee38cd2afb12318d6d88f2a77f0877c7f3bf3380cb18cbfcbe)
            check_type(argname="argument access_grants_location_configuration", value=access_grants_location_configuration, expected_type=type_hints["access_grants_location_configuration"])
            check_type(argname="argument access_grants_location_id", value=access_grants_location_id, expected_type=type_hints["access_grants_location_id"])
            check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            check_type(argname="argument s3_prefix_type", value=s3_prefix_type, expected_type=type_hints["s3_prefix_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_grants_location_configuration is not None:
            self._values["access_grants_location_configuration"] = access_grants_location_configuration
        if access_grants_location_id is not None:
            self._values["access_grants_location_id"] = access_grants_location_id
        if application_arn is not None:
            self._values["application_arn"] = application_arn
        if grantee is not None:
            self._values["grantee"] = grantee
        if permission is not None:
            self._values["permission"] = permission
        if s3_prefix_type is not None:
            self._values["s3_prefix_type"] = s3_prefix_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_grants_location_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessGrantPropsMixin.AccessGrantsLocationConfigurationProperty"]]:
        '''The configuration options of the grant location.

        The grant location is the S3 path to the data to which you are granting access. It contains the ``S3SubPrefix`` field. The grant scope is the result of appending the subprefix to the location scope of the registered location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrant.html#cfn-s3-accessgrant-accessgrantslocationconfiguration
        '''
        result = self._values.get("access_grants_location_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessGrantPropsMixin.AccessGrantsLocationConfigurationProperty"]], result)

    @builtins.property
    def access_grants_location_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the registered location to which you are granting access.

        S3 Access Grants assigns this ID when you register the location. S3 Access Grants assigns the ID ``default`` to the default location ``s3://`` and assigns an auto-generated ID to other locations that you register.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrant.html#cfn-s3-accessgrant-accessgrantslocationid
        '''
        result = self._values.get("access_grants_location_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an AWS IAM Identity Center application associated with your Identity Center instance.

        If the grant includes an application ARN, the grantee can only access the S3 data through this application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrant.html#cfn-s3-accessgrant-applicationarn
        '''
        result = self._values.get("application_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grantee(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessGrantPropsMixin.GranteeProperty"]]:
        '''The user, group, or role to which you are granting access.

        You can grant access to an IAM user or role. If you have added your corporate directory to AWS IAM Identity Center and associated your Identity Center instance with your S3 Access Grants instance, the grantee can also be a corporate directory user or group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrant.html#cfn-s3-accessgrant-grantee
        '''
        result = self._values.get("grantee")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessGrantPropsMixin.GranteeProperty"]], result)

    @builtins.property
    def permission(self) -> typing.Optional[builtins.str]:
        '''The type of access that you are granting to your S3 data, which can be set to one of the following values:  - ``READ`` – Grant read-only access to the S3 data.

        - ``WRITE`` – Grant write-only access to the S3 data.
        - ``READWRITE`` – Grant both read and write access to the S3 data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrant.html#cfn-s3-accessgrant-permission
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_prefix_type(self) -> typing.Optional[builtins.str]:
        '''The type of ``S3SubPrefix`` .

        The only possible value is ``Object`` . Pass this value if the access grant scope is an object. Do not pass this value if the access grant scope is a bucket or a bucket and a prefix.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrant.html#cfn-s3-accessgrant-s3prefixtype
        '''
        result = self._values.get("s3_prefix_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The AWS resource tags that you are adding to the access grant.

        Each tag is a label consisting of a user-defined key and value. Tags can help you manage, identify, organize, search for, and filter resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrant.html#cfn-s3-accessgrant-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessGrantMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessGrantPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessGrantPropsMixin",
):
    '''The ``AWS::S3::AccessGrant`` resource creates an access grant that gives a grantee access to your S3 data.

    The grantee can be an IAM user or role or a directory user, or group. Before you can create a grant, you must have an S3 Access Grants instance in the same Region as the S3 data. You can create an S3 Access Grants instance using the `AWS::S3::AccessGrantsInstance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantsinstance.html>`_ . You must also have registered at least one S3 data location in your S3 Access Grants instance using `AWS::S3::AccessGrantsLocation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantslocation.html>`_ .

    - **Permissions** - You must have the ``s3:CreateAccessGrant`` permission to use this resource.
    - **Additional Permissions** - For any directory identity - ``sso:DescribeInstance`` and ``sso:DescribeApplication``

    For directory users - ``identitystore:DescribeUser``

    For directory groups - ``identitystore:DescribeGroup``

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrant.html
    :cloudformationResource: AWS::S3::AccessGrant
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
        
        cfn_access_grant_props_mixin = s3_mixins.CfnAccessGrantPropsMixin(s3_mixins.CfnAccessGrantMixinProps(
            access_grants_location_configuration=s3_mixins.CfnAccessGrantPropsMixin.AccessGrantsLocationConfigurationProperty(
                s3_sub_prefix="s3SubPrefix"
            ),
            access_grants_location_id="accessGrantsLocationId",
            application_arn="applicationArn",
            grantee=s3_mixins.CfnAccessGrantPropsMixin.GranteeProperty(
                grantee_identifier="granteeIdentifier",
                grantee_type="granteeType"
            ),
            permission="permission",
            s3_prefix_type="s3PrefixType",
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
        props: typing.Union[CfnAccessGrantMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3::AccessGrant``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64cf74afbc86b9b14eb312a819cf979b02c0519853f170ddd98198884f05566)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8ab06d7b8b96290ab1cfc9220cb691cb856617524dc5926122d40b0c9a2403c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777f6df6b0b3cd9d84d00edf0919288b3f912fc705867f08107017fa1134f531)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessGrantMixinProps:
        return typing.cast(CfnAccessGrantMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessGrantPropsMixin.AccessGrantsLocationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_sub_prefix": "s3SubPrefix"},
    )
    class AccessGrantsLocationConfigurationProperty:
        def __init__(
            self,
            *,
            s3_sub_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration options of the S3 Access Grants location.

            It contains the ``S3SubPrefix`` field. The grant scope, the data to which you are granting access, is the result of appending the ``Subprefix`` field to the scope of the registered location.

            :param s3_sub_prefix: The ``S3SubPrefix`` is appended to the location scope creating the grant scope. Use this field to narrow the scope of the grant to a subset of the location scope. This field is required if the location scope is the default location ``s3://`` because you cannot create a grant for all of your S3 data in the Region and must narrow the scope. For example, if the location scope is the default location ``s3://`` , the ``S3SubPrefx`` can be a ``<bucket-name>/*`` , so the full grant scope path would be ``s3://<bucket-name>/*`` . Or the ``S3SubPrefx`` can be ``<bucket-name>/<prefix-name>*`` , so the full grant scope path would be ``s3://<bucket-name>/<prefix-name>*`` . If the ``S3SubPrefix`` includes a prefix, append the wildcard character ``*`` after the prefix to indicate that you want to include all object key names in the bucket that start with that prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accessgrant-accessgrantslocationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                access_grants_location_configuration_property = s3_mixins.CfnAccessGrantPropsMixin.AccessGrantsLocationConfigurationProperty(
                    s3_sub_prefix="s3SubPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__749df6fc3ef01799e4f2036b476c815c462473804963856a15cec956d3a168e8)
                check_type(argname="argument s3_sub_prefix", value=s3_sub_prefix, expected_type=type_hints["s3_sub_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_sub_prefix is not None:
                self._values["s3_sub_prefix"] = s3_sub_prefix

        @builtins.property
        def s3_sub_prefix(self) -> typing.Optional[builtins.str]:
            '''The ``S3SubPrefix`` is appended to the location scope creating the grant scope.

            Use this field to narrow the scope of the grant to a subset of the location scope. This field is required if the location scope is the default location ``s3://`` because you cannot create a grant for all of your S3 data in the Region and must narrow the scope. For example, if the location scope is the default location ``s3://`` , the ``S3SubPrefx`` can be a ``<bucket-name>/*`` , so the full grant scope path would be ``s3://<bucket-name>/*`` . Or the ``S3SubPrefx`` can be ``<bucket-name>/<prefix-name>*`` , so the full grant scope path would be ``s3://<bucket-name>/<prefix-name>*`` .

            If the ``S3SubPrefix`` includes a prefix, append the wildcard character ``*`` after the prefix to indicate that you want to include all object key names in the bucket that start with that prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accessgrant-accessgrantslocationconfiguration.html#cfn-s3-accessgrant-accessgrantslocationconfiguration-s3subprefix
            '''
            result = self._values.get("s3_sub_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessGrantsLocationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessGrantPropsMixin.GranteeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "grantee_identifier": "granteeIdentifier",
            "grantee_type": "granteeType",
        },
    )
    class GranteeProperty:
        def __init__(
            self,
            *,
            grantee_identifier: typing.Optional[builtins.str] = None,
            grantee_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The user, group, or role to which you are granting access.

            You can grant access to an IAM user or role. If you have added your corporate directory to AWS IAM Identity Center and associated your Identity Center instance with your S3 Access Grants instance, the grantee can also be a corporate directory user or group.

            :param grantee_identifier: The unique identifier of the ``Grantee`` . If the grantee type is ``IAM`` , the identifier is the IAM Amazon Resource Name (ARN) of the user or role. If the grantee type is a directory user or group, the identifier is 128-bit universally unique identifier (UUID) in the format ``a1b2c3d4-5678-90ab-cdef-EXAMPLE11111`` . You can obtain this UUID from your AWS IAM Identity Center instance.
            :param grantee_type: The type of the grantee to which access has been granted. It can be one of the following values:. - ``IAM`` - An IAM user or role. - ``DIRECTORY_USER`` - Your corporate directory user. You can use this option if you have added your corporate identity directory to IAM Identity Center and associated the IAM Identity Center instance with your S3 Access Grants instance. - ``DIRECTORY_GROUP`` - Your corporate directory group. You can use this option if you have added your corporate identity directory to IAM Identity Center and associated the IAM Identity Center instance with your S3 Access Grants instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accessgrant-grantee.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                grantee_property = s3_mixins.CfnAccessGrantPropsMixin.GranteeProperty(
                    grantee_identifier="granteeIdentifier",
                    grantee_type="granteeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72bf404b7d07091e7aa4e773d6c0d6442b1c354771c30c3b9cb35fdf8aa7bcee)
                check_type(argname="argument grantee_identifier", value=grantee_identifier, expected_type=type_hints["grantee_identifier"])
                check_type(argname="argument grantee_type", value=grantee_type, expected_type=type_hints["grantee_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grantee_identifier is not None:
                self._values["grantee_identifier"] = grantee_identifier
            if grantee_type is not None:
                self._values["grantee_type"] = grantee_type

        @builtins.property
        def grantee_identifier(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the ``Grantee`` .

            If the grantee type is ``IAM`` , the identifier is the IAM Amazon Resource Name (ARN) of the user or role. If the grantee type is a directory user or group, the identifier is 128-bit universally unique identifier (UUID) in the format ``a1b2c3d4-5678-90ab-cdef-EXAMPLE11111`` . You can obtain this UUID from your AWS IAM Identity Center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accessgrant-grantee.html#cfn-s3-accessgrant-grantee-granteeidentifier
            '''
            result = self._values.get("grantee_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def grantee_type(self) -> typing.Optional[builtins.str]:
            '''The type of the grantee to which access has been granted. It can be one of the following values:.

            - ``IAM`` - An IAM user or role.
            - ``DIRECTORY_USER`` - Your corporate directory user. You can use this option if you have added your corporate identity directory to IAM Identity Center and associated the IAM Identity Center instance with your S3 Access Grants instance.
            - ``DIRECTORY_GROUP`` - Your corporate directory group. You can use this option if you have added your corporate identity directory to IAM Identity Center and associated the IAM Identity Center instance with your S3 Access Grants instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accessgrant-grantee.html#cfn-s3-accessgrant-grantee-granteetype
            '''
            result = self._values.get("grantee_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GranteeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessGrantsInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={"identity_center_arn": "identityCenterArn", "tags": "tags"},
)
class CfnAccessGrantsInstanceMixinProps:
    def __init__(
        self,
        *,
        identity_center_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessGrantsInstancePropsMixin.

        :param identity_center_arn: If you would like to associate your S3 Access Grants instance with an AWS IAM Identity Center instance, use this field to pass the Amazon Resource Name (ARN) of the AWS IAM Identity Center instance that you are associating with your S3 Access Grants instance. An IAM Identity Center instance is your corporate identity directory that you added to the IAM Identity Center.
        :param tags: The AWS resource tags that you are adding to the S3 Access Grants instance. Each tag is a label consisting of a user-defined key and value. Tags can help you manage, identify, organize, search for, and filter resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantsinstance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
            
            cfn_access_grants_instance_mixin_props = s3_mixins.CfnAccessGrantsInstanceMixinProps(
                identity_center_arn="identityCenterArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905491084cc789e5eab0d8486092b1ba98ff35b18e7d26e3c2040ab67ee3fab9)
            check_type(argname="argument identity_center_arn", value=identity_center_arn, expected_type=type_hints["identity_center_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_center_arn is not None:
            self._values["identity_center_arn"] = identity_center_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def identity_center_arn(self) -> typing.Optional[builtins.str]:
        '''If you would like to associate your S3 Access Grants instance with an AWS IAM Identity Center instance, use this field to pass the Amazon Resource Name (ARN) of the AWS IAM Identity Center instance that you are associating with your S3 Access Grants instance.

        An IAM Identity Center instance is your corporate identity directory that you added to the IAM Identity Center.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantsinstance.html#cfn-s3-accessgrantsinstance-identitycenterarn
        '''
        result = self._values.get("identity_center_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The AWS resource tags that you are adding to the S3 Access Grants instance.

        Each tag is a label consisting of a user-defined key and value. Tags can help you manage, identify, organize, search for, and filter resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantsinstance.html#cfn-s3-accessgrantsinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessGrantsInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessGrantsInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessGrantsInstancePropsMixin",
):
    '''The ``AWS::S3::AccessGrantInstance`` resource creates an S3 Access Grants instance, which serves as a logical grouping for access grants.

    You can create one S3 Access Grants instance per Region per account.

    - **Permissions** - You must have the ``s3:CreateAccessGrantsInstance`` permission to use this resource.
    - **Additional Permissions** - To associate an IAM Identity Center instance with your S3 Access Grants instance, you must also have the ``sso:DescribeInstance`` , ``sso:CreateApplication`` , ``sso:PutApplicationGrant`` , and ``sso:PutApplicationAuthenticationMethod`` permissions.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantsinstance.html
    :cloudformationResource: AWS::S3::AccessGrantsInstance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
        
        cfn_access_grants_instance_props_mixin = s3_mixins.CfnAccessGrantsInstancePropsMixin(s3_mixins.CfnAccessGrantsInstanceMixinProps(
            identity_center_arn="identityCenterArn",
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
        props: typing.Union[CfnAccessGrantsInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3::AccessGrantsInstance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8233ab5d9e31c8379ee61c8c4b28b205c2eed0432260b66a9bf0208b8713802d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fab575a3ce1d40f12d0bcb1acee6c4c5688092d256773d3cf2e15dea1a53248)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a7dea07ccec4bdcbae70f1761d2b008f5e3eea91f3cd38ba0e11957eda0486)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessGrantsInstanceMixinProps:
        return typing.cast(CfnAccessGrantsInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessGrantsLocationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_role_arn": "iamRoleArn",
        "location_scope": "locationScope",
        "tags": "tags",
    },
)
class CfnAccessGrantsLocationMixinProps:
    def __init__(
        self,
        *,
        iam_role_arn: typing.Optional[builtins.str] = None,
        location_scope: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessGrantsLocationPropsMixin.

        :param iam_role_arn: The Amazon Resource Name (ARN) of the IAM role for the registered location. S3 Access Grants assumes this role to manage access to the registered location.
        :param location_scope: The S3 URI path to the location that you are registering. The location scope can be the default S3 location ``s3://`` , the S3 path to a bucket, or the S3 path to a bucket and prefix. A prefix in S3 is a string of characters at the beginning of an object key name used to organize the objects that you store in your S3 buckets. For example, object key names that start with the ``engineering/`` prefix or object key names that start with the ``marketing/campaigns/`` prefix.
        :param tags: The AWS resource tags that you are adding to the S3 Access Grants location. Each tag is a label consisting of a user-defined key and value. Tags can help you manage, identify, organize, search for, and filter resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantslocation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
            
            cfn_access_grants_location_mixin_props = s3_mixins.CfnAccessGrantsLocationMixinProps(
                iam_role_arn="iamRoleArn",
                location_scope="locationScope",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42357b6c1032cd8d0c91cc40e5a8c00d0831ccbc3e503e2d0a753d440b6924e6)
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument location_scope", value=location_scope, expected_type=type_hints["location_scope"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if location_scope is not None:
            self._values["location_scope"] = location_scope
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role for the registered location.

        S3 Access Grants assumes this role to manage access to the registered location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantslocation.html#cfn-s3-accessgrantslocation-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location_scope(self) -> typing.Optional[builtins.str]:
        '''The S3 URI path to the location that you are registering.

        The location scope can be the default S3 location ``s3://`` , the S3 path to a bucket, or the S3 path to a bucket and prefix. A prefix in S3 is a string of characters at the beginning of an object key name used to organize the objects that you store in your S3 buckets. For example, object key names that start with the ``engineering/`` prefix or object key names that start with the ``marketing/campaigns/`` prefix.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantslocation.html#cfn-s3-accessgrantslocation-locationscope
        '''
        result = self._values.get("location_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The AWS resource tags that you are adding to the S3 Access Grants location.

        Each tag is a label consisting of a user-defined key and value. Tags can help you manage, identify, organize, search for, and filter resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantslocation.html#cfn-s3-accessgrantslocation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessGrantsLocationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessGrantsLocationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessGrantsLocationPropsMixin",
):
    '''The ``AWS::S3::AccessGrantsLocation`` resource creates the S3 data location that you would like to register in your S3 Access Grants instance.

    Your S3 data must be in the same Region as your S3 Access Grants instance. The location can be one of the following:

    - The default S3 location ``s3://``
    - A bucket - ``S3://<bucket-name>``
    - A bucket and prefix - ``S3://<bucket-name>/<prefix>``

    When you register a location, you must include the IAM role that has permission to manage the S3 location that you are registering. Give S3 Access Grants permission to assume this role `using a policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-grants-location.html>`_ . S3 Access Grants assumes this role to manage access to the location and to vend temporary credentials to grantees or client applications.

    - **Permissions** - You must have the ``s3:CreateAccessGrantsLocation`` permission to use this resource.
    - **Additional Permissions** - You must also have the following permission for the specified IAM role: ``iam:PassRole``

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accessgrantslocation.html
    :cloudformationResource: AWS::S3::AccessGrantsLocation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
        
        cfn_access_grants_location_props_mixin = s3_mixins.CfnAccessGrantsLocationPropsMixin(s3_mixins.CfnAccessGrantsLocationMixinProps(
            iam_role_arn="iamRoleArn",
            location_scope="locationScope",
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
        props: typing.Union[CfnAccessGrantsLocationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3::AccessGrantsLocation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b869310af785b8e83acbaa7090141dc83be561dac775e09e90d08975fafbd67d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9dc49e59a6254c3bb812639d8eb881a88b1697cd3e0ac1fd35624bba07759b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7395ca2deaa925285e6b0047535b017170e3e939fb72b8b01fdc77bf446ad2e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessGrantsLocationMixinProps:
        return typing.cast(CfnAccessGrantsLocationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessPointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "bucket_account_id": "bucketAccountId",
        "name": "name",
        "policy": "policy",
        "public_access_block_configuration": "publicAccessBlockConfiguration",
        "tags": "tags",
        "vpc_configuration": "vpcConfiguration",
    },
)
class CfnAccessPointMixinProps:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        bucket_account_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
        public_access_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPointPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessPointPropsMixin.

        :param bucket: The name of the bucket associated with this access point.
        :param bucket_account_id: The AWS account ID associated with the S3 bucket associated with this access point.
        :param name: The name of this access point. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the access point name.
        :param policy: The access point policy associated with this access point.
        :param public_access_block_configuration: The PublicAccessBlock configuration that you want to apply to this Amazon S3 bucket. You can enable the configuration options in any combination. For more information about when Amazon S3 considers a bucket or object public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .
        :param tags: An array of tags that you can apply to access points. Tags are key-value pairs of metadata used to categorize your access points and control access. For more information, see `Using tags for attribute-based access control (ABAC) <https://docs.aws.amazon.com/AmazonS3/latest/userguide/tagging.html#using-tags-for-abac>`_ .
        :param vpc_configuration: The Virtual Private Cloud (VPC) configuration for this access point, if one exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
            
            # policy: Any
            
            cfn_access_point_mixin_props = s3_mixins.CfnAccessPointMixinProps(
                bucket="bucket",
                bucket_account_id="bucketAccountId",
                name="name",
                policy=policy,
                public_access_block_configuration=s3_mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_configuration=s3_mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty(
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9758e9f6a7a88d9cf7c5712f30c90d13f32b4eb605f020dee34e06a9cc1cfc4b)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument bucket_account_id", value=bucket_account_id, expected_type=type_hints["bucket_account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument public_access_block_configuration", value=public_access_block_configuration, expected_type=type_hints["public_access_block_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if bucket_account_id is not None:
            self._values["bucket_account_id"] = bucket_account_id
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if public_access_block_configuration is not None:
            self._values["public_access_block_configuration"] = public_access_block_configuration
        if tags is not None:
            self._values["tags"] = tags
        if vpc_configuration is not None:
            self._values["vpc_configuration"] = vpc_configuration

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the bucket associated with this access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-bucket
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_account_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID associated with the S3 bucket associated with this access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-bucketaccountid
        '''
        result = self._values.get("bucket_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this access point.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the access point name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The access point policy associated with this access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def public_access_block_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty"]]:
        '''The PublicAccessBlock configuration that you want to apply to this Amazon S3 bucket.

        You can enable the configuration options in any combination. For more information about when Amazon S3 considers a bucket or object public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-publicaccessblockconfiguration
        '''
        result = self._values.get("public_access_block_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tags that you can apply to access points.

        Tags are key-value pairs of metadata used to categorize your access points and control access. For more information, see `Using tags for attribute-based access control (ABAC) <https://docs.aws.amazon.com/AmazonS3/latest/userguide/tagging.html#using-tags-for-abac>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.VpcConfigurationProperty"]]:
        '''The Virtual Private Cloud (VPC) configuration for this access point, if one exists.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-vpcconfiguration
        '''
        result = self._values.get("vpc_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPointPropsMixin.VpcConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessPointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessPointPropsMixin",
):
    '''The AWS::S3::AccessPoint resource is an Amazon S3 resource type that you can use to access buckets.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html
    :cloudformationResource: AWS::S3::AccessPoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
        
        # policy: Any
        
        cfn_access_point_props_mixin = s3_mixins.CfnAccessPointPropsMixin(s3_mixins.CfnAccessPointMixinProps(
            bucket="bucket",
            bucket_account_id="bucketAccountId",
            name="name",
            policy=policy,
            public_access_block_configuration=s3_mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_configuration=s3_mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty(
                vpc_id="vpcId"
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
        '''Create a mixin to apply properties to ``AWS::S3::AccessPoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e541decfca52291e8f7bcfb16959c2743b26929e7869c76ba26601bcdf0a103)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99301948fb6a9fb492fe084e74dc558804b1ca0c367788c07e49ff064e4480f8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60fdfc2a64b21c4d6f915033df9fdbb15db74d65a1e303e065e4fe05f6b49c8)
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
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty",
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
            '''The PublicAccessBlock configuration that you want to apply to this Amazon S3 bucket.

            You can enable the configuration options in any combination. Bucket-level settings work alongside account-level settings (which may inherit from organization-level policies). For more information about when Amazon S3 considers a bucket or object public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .

            :param block_public_acls: Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and objects in this bucket. Setting this element to ``TRUE`` causes the following behavior: - PUT Bucket ACL and PUT Object ACL calls fail if the specified ACL is public. - PUT Object calls fail if the request includes a public ACL. - PUT Bucket calls fail if the request includes a public ACL. Enabling this setting doesn't affect existing policies or ACLs.
            :param block_public_policy: Specifies whether Amazon S3 should block public bucket policies for this bucket. Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access. Enabling this setting doesn't affect existing bucket policies.
            :param ignore_public_acls: Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this bucket. Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on this bucket and objects in this bucket. Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.
            :param restrict_public_buckets: Specifies whether Amazon S3 should restrict public bucket policies for this bucket. Setting this element to ``TRUE`` restricts access to this bucket to only AWS service principals and authorized users within this account if the bucket has a public policy. Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                public_access_block_configuration_property = s3_mixins.CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c60cc0c59b095bcd9ce6d2d2fe0b26059813bf18d72cc97693c3e795024af40)
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
            '''Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and objects in this bucket.

            Setting this element to ``TRUE`` causes the following behavior:

            - PUT Bucket ACL and PUT Object ACL calls fail if the specified ACL is public.
            - PUT Object calls fail if the request includes a public ACL.
            - PUT Bucket calls fail if the request includes a public ACL.

            Enabling this setting doesn't affect existing policies or ACLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-blockpublicacls
            '''
            result = self._values.get("block_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def block_public_policy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should block public bucket policies for this bucket.

            Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access.

            Enabling this setting doesn't affect existing bucket policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-blockpublicpolicy
            '''
            result = self._values.get("block_public_policy")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ignore_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this bucket.

            Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on this bucket and objects in this bucket.

            Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-ignorepublicacls
            '''
            result = self._values.get("ignore_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def restrict_public_buckets(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should restrict public bucket policies for this bucket.

            Setting this element to ``TRUE`` restricts access to this bucket to only AWS service principals and authorized users within this account if the bucket has a public policy.

            Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-restrictpublicbuckets
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
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_id": "vpcId"},
    )
    class VpcConfigurationProperty:
        def __init__(self, *, vpc_id: typing.Optional[builtins.str] = None) -> None:
            '''The Virtual Private Cloud (VPC) configuration for this access point.

            :param vpc_id: If this field is specified, the access point will only allow connections from the specified VPC ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                vpc_configuration_property = s3_mixins.CfnAccessPointPropsMixin.VpcConfigurationProperty(
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bfa00eb2d5282079476358e347abd4b17821b4424a01ff4068c25718630adc07)
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''If this field is specified, the access point will only allow connections from the specified VPC ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-vpcconfiguration.html#cfn-s3-accesspoint-vpcconfiguration-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "abac_status": "abacStatus",
        "accelerate_configuration": "accelerateConfiguration",
        "access_control": "accessControl",
        "analytics_configurations": "analyticsConfigurations",
        "bucket_encryption": "bucketEncryption",
        "bucket_name": "bucketName",
        "cors_configuration": "corsConfiguration",
        "intelligent_tiering_configurations": "intelligentTieringConfigurations",
        "inventory_configurations": "inventoryConfigurations",
        "lifecycle_configuration": "lifecycleConfiguration",
        "logging_configuration": "loggingConfiguration",
        "metadata_configuration": "metadataConfiguration",
        "metadata_table_configuration": "metadataTableConfiguration",
        "metrics_configurations": "metricsConfigurations",
        "notification_configuration": "notificationConfiguration",
        "object_lock_configuration": "objectLockConfiguration",
        "object_lock_enabled": "objectLockEnabled",
        "ownership_controls": "ownershipControls",
        "public_access_block_configuration": "publicAccessBlockConfiguration",
        "replication_configuration": "replicationConfiguration",
        "tags": "tags",
        "versioning_configuration": "versioningConfiguration",
        "website_configuration": "websiteConfiguration",
    },
)
class CfnBucketMixinProps:
    def __init__(
        self,
        *,
        abac_status: typing.Optional[builtins.str] = None,
        accelerate_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.AccelerateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        access_control: typing.Optional[builtins.str] = None,
        analytics_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.AnalyticsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        bucket_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.BucketEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.CorsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.IntelligentTieringConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        inventory_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.InventoryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.LifecycleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metadata_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.MetadataConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metadata_table_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.MetadataTableConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.MetricsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.NotificationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        object_lock_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ObjectLockConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        object_lock_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ownership_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.OwnershipControlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        public_access_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.PublicAccessBlockConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        replication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ReplicationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        versioning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.VersioningConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        website_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.WebsiteConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBucketPropsMixin.

        :param abac_status: The ABAC status of the general purpose bucket. When ABAC is enabled for the general purpose bucket, you can use tags to manage access to the general purpose buckets as well as for cost tracking purposes. When ABAC is disabled for the general purpose buckets, you can only use tags for cost tracking purposes. For more information, see `Using tags with S3 general purpose buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/buckets-tagging.html>`_ .
        :param accelerate_configuration: Configures the transfer acceleration state for an Amazon S3 bucket. For more information, see `Amazon S3 Transfer Acceleration <https://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration.html>`_ in the *Amazon S3 User Guide* .
        :param access_control: .. epigraph:: This is a legacy property, and it is not recommended for most use cases. A majority of modern use cases in Amazon S3 no longer require the use of ACLs, and we recommend that you keep ACLs disabled. For more information, see `Controlling object ownership <https://docs.aws.amazon.com//AmazonS3/latest/userguide/about-object-ownership.html>`_ in the *Amazon S3 User Guide* . A canned access control list (ACL) that grants predefined permissions to the bucket. For more information about canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ in the *Amazon S3 User Guide* . S3 buckets are created with ACLs disabled by default. Therefore, unless you explicitly set the `AWS::S3::OwnershipControls <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrols.html>`_ property to enable ACLs, your resource will fail to deploy with any value other than Private. Use cases requiring ACLs are uncommon. The majority of access control configurations can be successfully and more easily achieved with bucket policies. For more information, see `AWS::S3::BucketPolicy <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html>`_ . For examples of common policy configurations, including S3 Server Access Logs buckets and more, see `Bucket policy examples <https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html>`_ in the *Amazon S3 User Guide* .
        :param analytics_configurations: Specifies the configuration and any analyses for the analytics filter of an Amazon S3 bucket.
        :param bucket_encryption: Specifies default encryption for a bucket using server-side encryption with Amazon S3-managed keys (SSE-S3), AWS KMS-managed keys (SSE-KMS), or dual-layer server-side encryption with KMS-managed keys (DSSE-KMS). For information about the Amazon S3 default encryption feature, see `Amazon S3 Default Encryption for S3 Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html>`_ in the *Amazon S3 User Guide* .
        :param bucket_name: A name for the bucket. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html>`_ . For more information, see `Rules for naming Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ in the *Amazon S3 User Guide* . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.
        :param cors_configuration: Describes the cross-origin access configuration for objects in an Amazon S3 bucket. For more information, see `Enabling Cross-Origin Resource Sharing <https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html>`_ in the *Amazon S3 User Guide* .
        :param intelligent_tiering_configurations: Defines how Amazon S3 handles Intelligent-Tiering storage.
        :param inventory_configurations: Specifies the S3 Inventory configuration for an Amazon S3 bucket. For more information, see `GET Bucket inventory <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETInventoryConfig.html>`_ in the *Amazon S3 API Reference* .
        :param lifecycle_configuration: Specifies the lifecycle configuration for objects in an Amazon S3 bucket. For more information, see `Object Lifecycle Management <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html>`_ in the *Amazon S3 User Guide* .
        :param logging_configuration: Settings that define where logs are stored.
        :param metadata_configuration: The S3 Metadata configuration for a general purpose bucket.
        :param metadata_table_configuration: The metadata table configuration of an Amazon S3 general purpose bucket.
        :param metrics_configurations: Specifies a metrics configuration for the CloudWatch request metrics (specified by the metrics configuration ID) from an Amazon S3 bucket. If you're updating an existing metrics configuration, note that this is a full replacement of the existing metrics configuration. If you don't include the elements you want to keep, they are erased. For more information, see `PutBucketMetricsConfiguration <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTMetricConfiguration.html>`_ .
        :param notification_configuration: Configuration that defines how Amazon S3 handles bucket notifications.
        :param object_lock_configuration: .. epigraph:: This operation is not supported for directory buckets. Places an Object Lock configuration on the specified bucket. The rule specified in the Object Lock configuration will be applied by default to every new object placed in the specified bucket. For more information, see `Locking Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock.html>`_ . .. epigraph:: - The ``DefaultRetention`` settings require both a mode and a period. - The ``DefaultRetention`` period can be either ``Days`` or ``Years`` but you must select one. You cannot specify ``Days`` and ``Years`` at the same time. - You can enable Object Lock for new or existing buckets. For more information, see `Configuring Object Lock <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-configure.html>`_ . > You must URL encode any signed header values that contain spaces. For example, if your header value is ``my file.txt`` , containing two spaces after ``my`` , you must URL encode this value to ``my%20%20file.txt`` .
        :param object_lock_enabled: Indicates whether this bucket has an Object Lock configuration enabled. Enable ``ObjectLockEnabled`` when you apply ``ObjectLockConfiguration`` to a bucket.
        :param ownership_controls: Configuration that defines how Amazon S3 handles Object Ownership rules.
        :param public_access_block_configuration: Configuration that defines how Amazon S3 handles public access.
        :param replication_configuration: Configuration for replicating objects in an S3 bucket. To enable replication, you must also enable versioning by using the ``VersioningConfiguration`` property. Amazon S3 can store replicated objects in a single destination bucket or multiple destination buckets. The destination bucket or buckets must already exist.
        :param tags: An arbitrary set of tags (key-value pairs) for this S3 bucket.
        :param versioning_configuration: Enables multiple versions of all objects in this bucket. You might enable versioning to prevent objects from being deleted or overwritten by mistake or to archive objects so that you can retrieve previous versions of them. .. epigraph:: When you enable versioning on a bucket for the first time, it might take a short amount of time for the change to be fully propagated. We recommend that you wait for 15 minutes after enabling versioning before issuing write operations ( ``PUT`` or ``DELETE`` ) on objects in the bucket.
        :param website_configuration: Information used to configure the bucket as a static website. For more information, see `Hosting Websites on Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html
        :exampleMetadata: infused

        Example::

            from aws_cdk.mixins_preview.with import
            
            
            bucket = s3.Bucket(scope, "Bucket").with(CfnBucketPropsMixin(
                versioning_configuration=CfnBucketPropsMixin.VersioningConfigurationProperty(status="Enabled"),
                public_access_block_configuration=CfnBucketPropsMixin.PublicAccessBlockConfigurationProperty(
                    block_public_acls=True,
                    block_public_policy=True
                )
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61da27b1ee7f447df9c6a01c1fb0e0a80c311b33f345bf35f9c3ef6a8f7152d)
            check_type(argname="argument abac_status", value=abac_status, expected_type=type_hints["abac_status"])
            check_type(argname="argument accelerate_configuration", value=accelerate_configuration, expected_type=type_hints["accelerate_configuration"])
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument analytics_configurations", value=analytics_configurations, expected_type=type_hints["analytics_configurations"])
            check_type(argname="argument bucket_encryption", value=bucket_encryption, expected_type=type_hints["bucket_encryption"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument cors_configuration", value=cors_configuration, expected_type=type_hints["cors_configuration"])
            check_type(argname="argument intelligent_tiering_configurations", value=intelligent_tiering_configurations, expected_type=type_hints["intelligent_tiering_configurations"])
            check_type(argname="argument inventory_configurations", value=inventory_configurations, expected_type=type_hints["inventory_configurations"])
            check_type(argname="argument lifecycle_configuration", value=lifecycle_configuration, expected_type=type_hints["lifecycle_configuration"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument metadata_configuration", value=metadata_configuration, expected_type=type_hints["metadata_configuration"])
            check_type(argname="argument metadata_table_configuration", value=metadata_table_configuration, expected_type=type_hints["metadata_table_configuration"])
            check_type(argname="argument metrics_configurations", value=metrics_configurations, expected_type=type_hints["metrics_configurations"])
            check_type(argname="argument notification_configuration", value=notification_configuration, expected_type=type_hints["notification_configuration"])
            check_type(argname="argument object_lock_configuration", value=object_lock_configuration, expected_type=type_hints["object_lock_configuration"])
            check_type(argname="argument object_lock_enabled", value=object_lock_enabled, expected_type=type_hints["object_lock_enabled"])
            check_type(argname="argument ownership_controls", value=ownership_controls, expected_type=type_hints["ownership_controls"])
            check_type(argname="argument public_access_block_configuration", value=public_access_block_configuration, expected_type=type_hints["public_access_block_configuration"])
            check_type(argname="argument replication_configuration", value=replication_configuration, expected_type=type_hints["replication_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument versioning_configuration", value=versioning_configuration, expected_type=type_hints["versioning_configuration"])
            check_type(argname="argument website_configuration", value=website_configuration, expected_type=type_hints["website_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if abac_status is not None:
            self._values["abac_status"] = abac_status
        if accelerate_configuration is not None:
            self._values["accelerate_configuration"] = accelerate_configuration
        if access_control is not None:
            self._values["access_control"] = access_control
        if analytics_configurations is not None:
            self._values["analytics_configurations"] = analytics_configurations
        if bucket_encryption is not None:
            self._values["bucket_encryption"] = bucket_encryption
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if cors_configuration is not None:
            self._values["cors_configuration"] = cors_configuration
        if intelligent_tiering_configurations is not None:
            self._values["intelligent_tiering_configurations"] = intelligent_tiering_configurations
        if inventory_configurations is not None:
            self._values["inventory_configurations"] = inventory_configurations
        if lifecycle_configuration is not None:
            self._values["lifecycle_configuration"] = lifecycle_configuration
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if metadata_configuration is not None:
            self._values["metadata_configuration"] = metadata_configuration
        if metadata_table_configuration is not None:
            self._values["metadata_table_configuration"] = metadata_table_configuration
        if metrics_configurations is not None:
            self._values["metrics_configurations"] = metrics_configurations
        if notification_configuration is not None:
            self._values["notification_configuration"] = notification_configuration
        if object_lock_configuration is not None:
            self._values["object_lock_configuration"] = object_lock_configuration
        if object_lock_enabled is not None:
            self._values["object_lock_enabled"] = object_lock_enabled
        if ownership_controls is not None:
            self._values["ownership_controls"] = ownership_controls
        if public_access_block_configuration is not None:
            self._values["public_access_block_configuration"] = public_access_block_configuration
        if replication_configuration is not None:
            self._values["replication_configuration"] = replication_configuration
        if tags is not None:
            self._values["tags"] = tags
        if versioning_configuration is not None:
            self._values["versioning_configuration"] = versioning_configuration
        if website_configuration is not None:
            self._values["website_configuration"] = website_configuration

    @builtins.property
    def abac_status(self) -> typing.Optional[builtins.str]:
        '''The ABAC status of the general purpose bucket.

        When ABAC is enabled for the general purpose bucket, you can use tags to manage access to the general purpose buckets as well as for cost tracking purposes. When ABAC is disabled for the general purpose buckets, you can only use tags for cost tracking purposes. For more information, see `Using tags with S3 general purpose buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/buckets-tagging.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-abacstatus
        '''
        result = self._values.get("abac_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def accelerate_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AccelerateConfigurationProperty"]]:
        '''Configures the transfer acceleration state for an Amazon S3 bucket.

        For more information, see `Amazon S3 Transfer Acceleration <https://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-accelerateconfiguration
        '''
        result = self._values.get("accelerate_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AccelerateConfigurationProperty"]], result)

    @builtins.property
    def access_control(self) -> typing.Optional[builtins.str]:
        '''.. epigraph::

   This is a legacy property, and it is not recommended for most use cases.

        A majority of modern use cases in Amazon S3 no longer require the use of ACLs, and we recommend that you keep ACLs disabled. For more information, see `Controlling object ownership <https://docs.aws.amazon.com//AmazonS3/latest/userguide/about-object-ownership.html>`_ in the *Amazon S3 User Guide* .

        A canned access control list (ACL) that grants predefined permissions to the bucket. For more information about canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl>`_ in the *Amazon S3 User Guide* .

        S3 buckets are created with ACLs disabled by default. Therefore, unless you explicitly set the `AWS::S3::OwnershipControls <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrols.html>`_ property to enable ACLs, your resource will fail to deploy with any value other than Private. Use cases requiring ACLs are uncommon.

        The majority of access control configurations can be successfully and more easily achieved with bucket policies. For more information, see `AWS::S3::BucketPolicy <https://docs.aws.amazon.com//AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html>`_ . For examples of common policy configurations, including S3 Server Access Logs buckets and more, see `Bucket policy examples <https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-accesscontrol
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def analytics_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AnalyticsConfigurationProperty"]]]]:
        '''Specifies the configuration and any analyses for the analytics filter of an Amazon S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-analyticsconfigurations
        '''
        result = self._values.get("analytics_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AnalyticsConfigurationProperty"]]]], result)

    @builtins.property
    def bucket_encryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.BucketEncryptionProperty"]]:
        '''Specifies default encryption for a bucket using server-side encryption with Amazon S3-managed keys (SSE-S3), AWS KMS-managed keys (SSE-KMS), or dual-layer server-side encryption with KMS-managed keys (DSSE-KMS).

        For information about the Amazon S3 default encryption feature, see `Amazon S3 Default Encryption for S3 Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-bucketencryption
        '''
        result = self._values.get("bucket_encryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.BucketEncryptionProperty"]], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''A name for the bucket.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html>`_ . For more information, see `Rules for naming Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ in the *Amazon S3 User Guide* .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-bucketname
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.CorsConfigurationProperty"]]:
        '''Describes the cross-origin access configuration for objects in an Amazon S3 bucket.

        For more information, see `Enabling Cross-Origin Resource Sharing <https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-corsconfiguration
        '''
        result = self._values.get("cors_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.CorsConfigurationProperty"]], result)

    @builtins.property
    def intelligent_tiering_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.IntelligentTieringConfigurationProperty"]]]]:
        '''Defines how Amazon S3 handles Intelligent-Tiering storage.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-intelligenttieringconfigurations
        '''
        result = self._values.get("intelligent_tiering_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.IntelligentTieringConfigurationProperty"]]]], result)

    @builtins.property
    def inventory_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.InventoryConfigurationProperty"]]]]:
        '''Specifies the S3 Inventory configuration for an Amazon S3 bucket.

        For more information, see `GET Bucket inventory <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETInventoryConfig.html>`_ in the *Amazon S3 API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-inventoryconfigurations
        '''
        result = self._values.get("inventory_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.InventoryConfigurationProperty"]]]], result)

    @builtins.property
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.LifecycleConfigurationProperty"]]:
        '''Specifies the lifecycle configuration for objects in an Amazon S3 bucket.

        For more information, see `Object Lifecycle Management <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-lifecycleconfiguration
        '''
        result = self._values.get("lifecycle_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.LifecycleConfigurationProperty"]], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.LoggingConfigurationProperty"]]:
        '''Settings that define where logs are stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.LoggingConfigurationProperty"]], result)

    @builtins.property
    def metadata_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataConfigurationProperty"]]:
        '''The S3 Metadata configuration for a general purpose bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-metadataconfiguration
        '''
        result = self._values.get("metadata_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataConfigurationProperty"]], result)

    @builtins.property
    def metadata_table_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataTableConfigurationProperty"]]:
        '''The metadata table configuration of an Amazon S3 general purpose bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-metadatatableconfiguration
        '''
        result = self._values.get("metadata_table_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataTableConfigurationProperty"]], result)

    @builtins.property
    def metrics_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetricsConfigurationProperty"]]]]:
        '''Specifies a metrics configuration for the CloudWatch request metrics (specified by the metrics configuration ID) from an Amazon S3 bucket.

        If you're updating an existing metrics configuration, note that this is a full replacement of the existing metrics configuration. If you don't include the elements you want to keep, they are erased. For more information, see `PutBucketMetricsConfiguration <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTMetricConfiguration.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-metricsconfigurations
        '''
        result = self._values.get("metrics_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetricsConfigurationProperty"]]]], result)

    @builtins.property
    def notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NotificationConfigurationProperty"]]:
        '''Configuration that defines how Amazon S3 handles bucket notifications.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-notificationconfiguration
        '''
        result = self._values.get("notification_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NotificationConfigurationProperty"]], result)

    @builtins.property
    def object_lock_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ObjectLockConfigurationProperty"]]:
        '''.. epigraph::

   This operation is not supported for directory buckets.

        Places an Object Lock configuration on the specified bucket. The rule specified in the Object Lock configuration will be applied by default to every new object placed in the specified bucket. For more information, see `Locking Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock.html>`_ .
        .. epigraph::

           - The ``DefaultRetention`` settings require both a mode and a period.
           - The ``DefaultRetention`` period can be either ``Days`` or ``Years`` but you must select one. You cannot specify ``Days`` and ``Years`` at the same time.
           - You can enable Object Lock for new or existing buckets. For more information, see `Configuring Object Lock <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-configure.html>`_ . > You must URL encode any signed header values that contain spaces. For example, if your header value is ``my file.txt`` , containing two spaces after ``my`` , you must URL encode this value to ``my%20%20file.txt`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-objectlockconfiguration
        '''
        result = self._values.get("object_lock_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ObjectLockConfigurationProperty"]], result)

    @builtins.property
    def object_lock_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether this bucket has an Object Lock configuration enabled.

        Enable ``ObjectLockEnabled`` when you apply ``ObjectLockConfiguration`` to a bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-objectlockenabled
        '''
        result = self._values.get("object_lock_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def ownership_controls(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.OwnershipControlsProperty"]]:
        '''Configuration that defines how Amazon S3 handles Object Ownership rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-ownershipcontrols
        '''
        result = self._values.get("ownership_controls")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.OwnershipControlsProperty"]], result)

    @builtins.property
    def public_access_block_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.PublicAccessBlockConfigurationProperty"]]:
        '''Configuration that defines how Amazon S3 handles public access.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-publicaccessblockconfiguration
        '''
        result = self._values.get("public_access_block_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.PublicAccessBlockConfigurationProperty"]], result)

    @builtins.property
    def replication_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationConfigurationProperty"]]:
        '''Configuration for replicating objects in an S3 bucket.

        To enable replication, you must also enable versioning by using the ``VersioningConfiguration`` property.

        Amazon S3 can store replicated objects in a single destination bucket or multiple destination buckets. The destination bucket or buckets must already exist.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-replicationconfiguration
        '''
        result = self._values.get("replication_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An arbitrary set of tags (key-value pairs) for this S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def versioning_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.VersioningConfigurationProperty"]]:
        '''Enables multiple versions of all objects in this bucket.

        You might enable versioning to prevent objects from being deleted or overwritten by mistake or to archive objects so that you can retrieve previous versions of them.
        .. epigraph::

           When you enable versioning on a bucket for the first time, it might take a short amount of time for the change to be fully propagated. We recommend that you wait for 15 minutes after enabling versioning before issuing write operations ( ``PUT`` or ``DELETE`` ) on objects in the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-versioningconfiguration
        '''
        result = self._values.get("versioning_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.VersioningConfigurationProperty"]], result)

    @builtins.property
    def website_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.WebsiteConfigurationProperty"]]:
        '''Information used to configure the bucket as a static website.

        For more information, see `Hosting Websites on Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html#cfn-s3-bucket-websiteconfiguration
        '''
        result = self._values.get("website_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.WebsiteConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBucketMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "policy_document": "policyDocument"},
)
class CfnBucketPolicyMixinProps:
    def __init__(
        self,
        *,
        bucket: typing.Optional[builtins.str] = None,
        policy_document: typing.Any = None,
    ) -> None:
        '''Properties for CfnBucketPolicyPropsMixin.

        :param bucket: The name of the Amazon S3 bucket to which the policy applies.
        :param policy_document: A policy document containing permissions to add to the specified bucket. In IAM, you must provide policy documents in JSON format. However, in CloudFormation you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-policy-language-overview.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucketpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
            
            # policy_document: Any
            
            cfn_bucket_policy_mixin_props = s3_mixins.CfnBucketPolicyMixinProps(
                bucket="bucket",
                policy_document=policy_document
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49243bb3447168c9b8f04db1d04200ac216ace48f2bd3399ee15f4571bd748c3)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if policy_document is not None:
            self._values["policy_document"] = policy_document

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon S3 bucket to which the policy applies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucketpolicy.html#cfn-s3-bucketpolicy-bucket
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document containing permissions to add to the specified bucket.

        In IAM, you must provide policy documents in JSON format. However, in CloudFormation you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-policy-language-overview.html>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucketpolicy.html#cfn-s3-bucketpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBucketPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBucketPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPolicyPropsMixin",
):
    '''Applies an Amazon S3 bucket policy to an Amazon S3 bucket.

    If you are using an identity other than the root user of the AWS account that owns the bucket, the calling identity must have the ``PutBucketPolicy`` permissions on the specified bucket and belong to the bucket owner's account in order to use this operation.

    If you don't have ``PutBucketPolicy`` permissions, Amazon S3 returns a ``403 Access Denied`` error. If you have the correct permissions, but you're not using an identity that belongs to the bucket owner's account, Amazon S3 returns a ``405 Method Not Allowed`` error.
    .. epigraph::

       As a security precaution, the root user of the AWS account that owns a bucket can always use this operation, even if the policy explicitly denies the root user the ability to perform this action.

    When using the ``AWS::S3::BucketPolicy`` resource, you can create, update, and delete bucket policies for S3 buckets located in Regions that are different from the stack's Region. However, the CloudFormation stacks should be deployed in the US East (N. Virginia) or ``us-east-1`` Region. This cross-region bucket policy modification functionality is supported for backward compatibility with existing workflows.
    .. epigraph::

       If the `DeletionPolicy attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ is not specified or set to ``Delete`` , the bucket policy will be removed when the stack is deleted. If set to ``Retain`` , the bucket policy will be preserved even after the stack is deleted.

    For example, a CloudFormation stack in ``us-east-1`` can use the ``AWS::S3::BucketPolicy`` resource to manage the bucket policy for an S3 bucket in ``us-west-2`` . The retention or removal of the bucket policy during the stack deletion is determined by the ``DeletionPolicy`` attribute specified in the stack template.

    For more information, see `Bucket policy examples <https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html>`_ .

    The following operations are related to ``PutBucketPolicy`` :

    - `CreateBucket <https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateBucket.html>`_
    - `DeleteBucket <https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucket.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucketpolicy.html
    :cloudformationResource: AWS::S3::BucketPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
        
        # policy_document: Any
        
        cfn_bucket_policy_props_mixin = s3_mixins.CfnBucketPolicyPropsMixin(s3_mixins.CfnBucketPolicyMixinProps(
            bucket="bucket",
            policy_document=policy_document
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBucketPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3::BucketPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ba73c23bd95b2bdb442ee38220a48b79357d3265990c2543f6223060b38203)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f2a1bb9d82f07e4c23eeec546476b008de055845a0840f640fefc086ee2d587)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdaccd8321315b52e3b7e3399f4f66e8285cc4b1f984dcc2a40cff123cfa810)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBucketPolicyMixinProps:
        return typing.cast(CfnBucketPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnBucketPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin",
):
    '''The ``AWS::S3::Bucket`` resource creates an Amazon S3 bucket in the same AWS Region where you create the AWS CloudFormation stack.

    To control how AWS CloudFormation handles the bucket when the stack is deleted, you can set a deletion policy for your bucket. You can choose to *retain* the bucket or to *delete* the bucket. For more information, see `DeletionPolicy Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .
    .. epigraph::

       You can only delete empty buckets. Deletion fails for buckets that have contents.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html
    :cloudformationResource: AWS::S3::Bucket
    :mixin: true
    :exampleMetadata: infused

    Example::

        from aws_cdk.mixins_preview.with import
        
        
        bucket = s3.Bucket(scope, "Bucket").with(CfnBucketPropsMixin(
            versioning_configuration=CfnBucketPropsMixin.VersioningConfigurationProperty(status="Enabled"),
            public_access_block_configuration=CfnBucketPropsMixin.PublicAccessBlockConfigurationProperty(
                block_public_acls=True,
                block_public_policy=True
            )
        ))
    '''

    def __init__(
        self,
        props: typing.Union[CfnBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3::Bucket``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca009243f8b97752937936d645805cf8600918eadec76b14de35814057d6064a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__597bbd801bf04c01f97d6c1358f13c246b8778dadc489438e60feb7754706152)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663c2df5c06167346b9feac924041f49bb0c252a06ca4bd47e8ebb1ab5cdcefc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBucketMixinProps:
        return typing.cast(CfnBucketMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty",
        jsii_struct_bases=[],
        name_mapping={"days_after_initiation": "daysAfterInitiation"},
    )
    class AbortIncompleteMultipartUploadProperty:
        def __init__(
            self,
            *,
            days_after_initiation: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the days since the initiation of an incomplete multipart upload that Amazon S3 will wait before permanently removing all parts of the upload.

            For more information, see `Stopping Incomplete Multipart Uploads Using a Bucket Lifecycle Policy <https://docs.aws.amazon.com/AmazonS3/latest/dev/mpuoverview.html#mpu-abort-incomplete-mpu-lifecycle-config>`_ in the *Amazon S3 User Guide* .

            :param days_after_initiation: Specifies the number of days after which Amazon S3 stops an incomplete multipart upload.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-abortincompletemultipartupload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                abort_incomplete_multipart_upload_property = s3_mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                    days_after_initiation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4b64b6421e663632b82d272c2095d04b08eb4f2cd50965706dfa88db9cf95ab)
                check_type(argname="argument days_after_initiation", value=days_after_initiation, expected_type=type_hints["days_after_initiation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days_after_initiation is not None:
                self._values["days_after_initiation"] = days_after_initiation

        @builtins.property
        def days_after_initiation(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of days after which Amazon S3 stops an incomplete multipart upload.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-abortincompletemultipartupload.html#cfn-s3-bucket-abortincompletemultipartupload-daysafterinitiation
            '''
            result = self._values.get("days_after_initiation")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AbortIncompleteMultipartUploadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.AccelerateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"acceleration_status": "accelerationStatus"},
    )
    class AccelerateConfigurationProperty:
        def __init__(
            self,
            *,
            acceleration_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures the transfer acceleration state for an Amazon S3 bucket.

            For more information, see `Amazon S3 Transfer Acceleration <https://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration.html>`_ in the *Amazon S3 User Guide* .

            :param acceleration_status: Specifies the transfer acceleration status of the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accelerateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                accelerate_configuration_property = s3_mixins.CfnBucketPropsMixin.AccelerateConfigurationProperty(
                    acceleration_status="accelerationStatus"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2406ffdf7e4679a419c07f1e747779cabbbd2e1af1cced5f673acaf45e46eb1c)
                check_type(argname="argument acceleration_status", value=acceleration_status, expected_type=type_hints["acceleration_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acceleration_status is not None:
                self._values["acceleration_status"] = acceleration_status

        @builtins.property
        def acceleration_status(self) -> typing.Optional[builtins.str]:
            '''Specifies the transfer acceleration status of the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accelerateconfiguration.html#cfn-s3-bucket-accelerateconfiguration-accelerationstatus
            '''
            result = self._values.get("acceleration_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccelerateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.AccessControlTranslationProperty",
        jsii_struct_bases=[],
        name_mapping={"owner": "owner"},
    )
    class AccessControlTranslationProperty:
        def __init__(self, *, owner: typing.Optional[builtins.str] = None) -> None:
            '''Specify this only in a cross-account scenario (where source and destination bucket owners are not the same), and you want to change replica ownership to the AWS account that owns the destination bucket.

            If this is not specified in the replication configuration, the replicas are owned by same AWS account that owns the source object.

            :param owner: Specifies the replica ownership. For default and valid values, see `PUT bucket replication <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTreplication.html>`_ in the *Amazon S3 API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accesscontroltranslation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                access_control_translation_property = s3_mixins.CfnBucketPropsMixin.AccessControlTranslationProperty(
                    owner="owner"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b61e4133712e2cb7aece492a07d0d50977070b005aed4e6abc0437db93afc2de)
                check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if owner is not None:
                self._values["owner"] = owner

        @builtins.property
        def owner(self) -> typing.Optional[builtins.str]:
            '''Specifies the replica ownership.

            For default and valid values, see `PUT bucket replication <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTreplication.html>`_ in the *Amazon S3 API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accesscontroltranslation.html#cfn-s3-bucket-accesscontroltranslation-owner
            '''
            result = self._values.get("owner")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessControlTranslationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.AnalyticsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "prefix": "prefix",
            "storage_class_analysis": "storageClassAnalysis",
            "tag_filters": "tagFilters",
        },
    )
    class AnalyticsConfigurationProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            storage_class_analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.StorageClassAnalysisProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies the configuration and any analyses for the analytics filter of an Amazon S3 bucket.

            :param id: The ID that identifies the analytics configuration.
            :param prefix: The prefix that an object must have to be included in the analytics results.
            :param storage_class_analysis: Contains data related to access patterns to be collected and made available to analyze the tradeoffs between different storage classes.
            :param tag_filters: The tags to use when evaluating an analytics filter. The analytics only includes objects that meet the filter's criteria. If no filter is specified, all of the contents of the bucket are included in the analysis.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                analytics_configuration_property = s3_mixins.CfnBucketPropsMixin.AnalyticsConfigurationProperty(
                    id="id",
                    prefix="prefix",
                    storage_class_analysis=s3_mixins.CfnBucketPropsMixin.StorageClassAnalysisProperty(
                        data_export=s3_mixins.CfnBucketPropsMixin.DataExportProperty(
                            destination=s3_mixins.CfnBucketPropsMixin.DestinationProperty(
                                bucket_account_id="bucketAccountId",
                                bucket_arn="bucketArn",
                                format="format",
                                prefix="prefix"
                            ),
                            output_schema_version="outputSchemaVersion"
                        )
                    ),
                    tag_filters=[s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1442b1c097dccc3b47e486d134f7ed58ee51bb29c613ac67ee59d1faf009e50b)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument storage_class_analysis", value=storage_class_analysis, expected_type=type_hints["storage_class_analysis"])
                check_type(argname="argument tag_filters", value=tag_filters, expected_type=type_hints["tag_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if prefix is not None:
                self._values["prefix"] = prefix
            if storage_class_analysis is not None:
                self._values["storage_class_analysis"] = storage_class_analysis
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID that identifies the analytics configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix that an object must have to be included in the analytics results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def storage_class_analysis(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.StorageClassAnalysisProperty"]]:
            '''Contains data related to access patterns to be collected and made available to analyze the tradeoffs between different storage classes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-storageclassanalysis
            '''
            result = self._values.get("storage_class_analysis")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.StorageClassAnalysisProperty"]], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]]:
            '''The tags to use when evaluating an analytics filter.

            The analytics only includes objects that meet the filter's criteria. If no filter is specified, all of the contents of the bucket are included in the analysis.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalyticsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.BlockedEncryptionTypesProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType"},
    )
    class BlockedEncryptionTypesProperty:
        def __init__(
            self,
            *,
            encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A bucket-level setting for Amazon S3 general purpose buckets used to prevent the upload of new objects encrypted with the specified server-side encryption type.

            For example, blocking an encryption type will block ``PutObject`` , ``CopyObject`` , ``PostObject`` , multipart upload, and replication requests to the bucket for objects with the specified encryption type. However, you can continue to read and list any pre-existing objects already encrypted with the specified encryption type. For more information, see `Blocking or unblocking SSE-C for a general purpose bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/blocking-unblocking-s3-c-encryption-gpb.html>`_ .

            This data type is used with the following actions:

            - `PutBucketEncryption <https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketEncryption.html>`_
            - `GetBucketEncryption <https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketEncryption.html>`_
            - `DeleteBucketEncryption <https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteBucketEncryption.html>`_
            - **Permissions** - You must have the ``s3:PutEncryptionConfiguration`` permission to block or unblock an encryption type for a bucket.

            You must have the ``s3:GetEncryptionConfiguration`` permission to view a bucket's encryption type.

            :param encryption_type: The object encryption type that you want to block or unblock for an Amazon S3 general purpose bucket. .. epigraph:: Currently, this parameter only supports blocking or unblocking server side encryption with customer-provided keys (SSE-C). For more information about SSE-C, see `Using server-side encryption with customer-provided keys (SSE-C) <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-blockedencryptiontypes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                blocked_encryption_types_property = s3_mixins.CfnBucketPropsMixin.BlockedEncryptionTypesProperty(
                    encryption_type=["encryptionType"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd8b48c55f8deacff80062f0cad9eb734f05bbc58e6abf8872674b00b9ea7785)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_type is not None:
                self._values["encryption_type"] = encryption_type

        @builtins.property
        def encryption_type(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The object encryption type that you want to block or unblock for an Amazon S3 general purpose bucket.

            .. epigraph::

               Currently, this parameter only supports blocking or unblocking server side encryption with customer-provided keys (SSE-C). For more information about SSE-C, see `Using server-side encryption with customer-provided keys (SSE-C) <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-blockedencryptiontypes.html#cfn-s3-bucket-blockedencryptiontypes-encryptiontype
            '''
            result = self._values.get("encryption_type")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockedEncryptionTypesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.BucketEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        },
    )
    class BucketEncryptionProperty:
        def __init__(
            self,
            *,
            server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ServerSideEncryptionRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies default encryption for a bucket using server-side encryption with Amazon S3-managed keys (SSE-S3), AWS KMS-managed keys (SSE-KMS), or dual-layer server-side encryption with KMS-managed keys (DSSE-KMS).

            For information about the Amazon S3 default encryption feature, see `Amazon S3 Default Encryption for S3 Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html>`_ in the *Amazon S3 User Guide* .

            :param server_side_encryption_configuration: Specifies the default server-side-encryption configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-bucketencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                bucket_encryption_property = s3_mixins.CfnBucketPropsMixin.BucketEncryptionProperty(
                    server_side_encryption_configuration=[s3_mixins.CfnBucketPropsMixin.ServerSideEncryptionRuleProperty(
                        blocked_encryption_types=s3_mixins.CfnBucketPropsMixin.BlockedEncryptionTypesProperty(
                            encryption_type=["encryptionType"]
                        ),
                        bucket_key_enabled=False,
                        server_side_encryption_by_default=s3_mixins.CfnBucketPropsMixin.ServerSideEncryptionByDefaultProperty(
                            kms_master_key_id="kmsMasterKeyId",
                            sse_algorithm="sseAlgorithm"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__863511f6faeec8e709e8e592901c449026bcd85cccf9f5bc9361838b429f44b5)
                check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if server_side_encryption_configuration is not None:
                self._values["server_side_encryption_configuration"] = server_side_encryption_configuration

        @builtins.property
        def server_side_encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ServerSideEncryptionRuleProperty"]]]]:
            '''Specifies the default server-side-encryption configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-bucketencryption.html#cfn-s3-bucket-bucketencryption-serversideencryptionconfiguration
            '''
            result = self._values.get("server_side_encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ServerSideEncryptionRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.CorsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"cors_rules": "corsRules"},
    )
    class CorsConfigurationProperty:
        def __init__(
            self,
            *,
            cors_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.CorsRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes the cross-origin access configuration for objects in an Amazon S3 bucket.

            For more information, see `Enabling Cross-Origin Resource Sharing <https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html>`_ in the *Amazon S3 User Guide* .

            :param cors_rules: A set of origins and methods (cross-origin access that you want to allow). You can add up to 100 rules to the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-corsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                cors_configuration_property = s3_mixins.CfnBucketPropsMixin.CorsConfigurationProperty(
                    cors_rules=[s3_mixins.CfnBucketPropsMixin.CorsRuleProperty(
                        allowed_headers=["allowedHeaders"],
                        allowed_methods=["allowedMethods"],
                        allowed_origins=["allowedOrigins"],
                        exposed_headers=["exposedHeaders"],
                        id="id",
                        max_age=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ba82944dc39c257239f70201bd5a3e19c4b9d7c57b1c52602d67795c2eb0f43)
                check_type(argname="argument cors_rules", value=cors_rules, expected_type=type_hints["cors_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cors_rules is not None:
                self._values["cors_rules"] = cors_rules

        @builtins.property
        def cors_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.CorsRuleProperty"]]]]:
            '''A set of origins and methods (cross-origin access that you want to allow).

            You can add up to 100 rules to the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-corsconfiguration.html#cfn-s3-bucket-corsconfiguration-corsrules
            '''
            result = self._values.get("cors_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.CorsRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.CorsRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_headers": "allowedHeaders",
            "allowed_methods": "allowedMethods",
            "allowed_origins": "allowedOrigins",
            "exposed_headers": "exposedHeaders",
            "id": "id",
            "max_age": "maxAge",
        },
    )
    class CorsRuleProperty:
        def __init__(
            self,
            *,
            allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
            exposed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
            id: typing.Optional[builtins.str] = None,
            max_age: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies a cross-origin access rule for an Amazon S3 bucket.

            :param allowed_headers: Headers that are specified in the ``Access-Control-Request-Headers`` header. These headers are allowed in a preflight OPTIONS request. In response to any preflight OPTIONS request, Amazon S3 returns any requested headers that are allowed.
            :param allowed_methods: An HTTP method that you allow the origin to run. *Allowed values* : ``GET`` | ``PUT`` | ``HEAD`` | ``POST`` | ``DELETE``
            :param allowed_origins: One or more origins you want customers to be able to access the bucket from.
            :param exposed_headers: One or more headers in the response that you want customers to be able to access from their applications (for example, from a JavaScript ``XMLHttpRequest`` object).
            :param id: A unique identifier for this rule. The value must be no more than 255 characters.
            :param max_age: The time in seconds that your browser is to cache the preflight response for the specified resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-corsrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                cors_rule_property = s3_mixins.CfnBucketPropsMixin.CorsRuleProperty(
                    allowed_headers=["allowedHeaders"],
                    allowed_methods=["allowedMethods"],
                    allowed_origins=["allowedOrigins"],
                    exposed_headers=["exposedHeaders"],
                    id="id",
                    max_age=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8cb5582959cc4fa0159ce14255a5c9937b5c1d184fa459b8b5828114915f971)
                check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
                check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
                check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
                check_type(argname="argument exposed_headers", value=exposed_headers, expected_type=type_hints["exposed_headers"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_headers is not None:
                self._values["allowed_headers"] = allowed_headers
            if allowed_methods is not None:
                self._values["allowed_methods"] = allowed_methods
            if allowed_origins is not None:
                self._values["allowed_origins"] = allowed_origins
            if exposed_headers is not None:
                self._values["exposed_headers"] = exposed_headers
            if id is not None:
                self._values["id"] = id
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Headers that are specified in the ``Access-Control-Request-Headers`` header.

            These headers are allowed in a preflight OPTIONS request. In response to any preflight OPTIONS request, Amazon S3 returns any requested headers that are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-corsrule.html#cfn-s3-bucket-corsrule-allowedheaders
            '''
            result = self._values.get("allowed_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An HTTP method that you allow the origin to run.

            *Allowed values* : ``GET`` | ``PUT`` | ``HEAD`` | ``POST`` | ``DELETE``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-corsrule.html#cfn-s3-bucket-corsrule-allowedmethods
            '''
            result = self._values.get("allowed_methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more origins you want customers to be able to access the bucket from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-corsrule.html#cfn-s3-bucket-corsrule-allowedorigins
            '''
            result = self._values.get("allowed_origins")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exposed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more headers in the response that you want customers to be able to access from their applications (for example, from a JavaScript ``XMLHttpRequest`` object).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-corsrule.html#cfn-s3-bucket-corsrule-exposedheaders
            '''
            result = self._values.get("exposed_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for this rule.

            The value must be no more than 255 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-corsrule.html#cfn-s3-bucket-corsrule-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            '''The time in seconds that your browser is to cache the preflight response for the specified resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-corsrule.html#cfn-s3-bucket-corsrule-maxage
            '''
            result = self._values.get("max_age")
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
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.DataExportProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "output_schema_version": "outputSchemaVersion",
        },
    )
    class DataExportProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            output_schema_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies how data related to the storage class analysis for an Amazon S3 bucket should be exported.

            :param destination: The place to store the data for an analysis.
            :param output_schema_version: The version of the output schema to use when exporting data. Must be ``V_1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-dataexport.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                data_export_property = s3_mixins.CfnBucketPropsMixin.DataExportProperty(
                    destination=s3_mixins.CfnBucketPropsMixin.DestinationProperty(
                        bucket_account_id="bucketAccountId",
                        bucket_arn="bucketArn",
                        format="format",
                        prefix="prefix"
                    ),
                    output_schema_version="outputSchemaVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__230b944b912f854dbaf0410cdbb1c7d05fe9627ec6a8e02bc63b01fdc5bde990)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument output_schema_version", value=output_schema_version, expected_type=type_hints["output_schema_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if output_schema_version is not None:
                self._values["output_schema_version"] = output_schema_version

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DestinationProperty"]]:
            '''The place to store the data for an analysis.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-dataexport.html#cfn-s3-bucket-dataexport-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DestinationProperty"]], result)

        @builtins.property
        def output_schema_version(self) -> typing.Optional[builtins.str]:
            '''The version of the output schema to use when exporting data.

            Must be ``V_1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-dataexport.html#cfn-s3-bucket-dataexport-outputschemaversion
            '''
            result = self._values.get("output_schema_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataExportProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.DefaultRetentionProperty",
        jsii_struct_bases=[],
        name_mapping={"days": "days", "mode": "mode", "years": "years"},
    )
    class DefaultRetentionProperty:
        def __init__(
            self,
            *,
            days: typing.Optional[jsii.Number] = None,
            mode: typing.Optional[builtins.str] = None,
            years: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The container element for optionally specifying the default Object Lock retention settings for new objects placed in the specified bucket.

            .. epigraph::

               - The ``DefaultRetention`` settings require both a mode and a period.
               - The ``DefaultRetention`` period can be either ``Days`` or ``Years`` but you must select one. You cannot specify ``Days`` and ``Years`` at the same time.

            :param days: The number of days that you want to specify for the default retention period. If Object Lock is turned on, you must specify ``Mode`` and specify either ``Days`` or ``Years`` .
            :param mode: The default Object Lock retention mode you want to apply to new objects placed in the specified bucket. If Object Lock is turned on, you must specify ``Mode`` and specify either ``Days`` or ``Years`` .
            :param years: The number of years that you want to specify for the default retention period. If Object Lock is turned on, you must specify ``Mode`` and specify either ``Days`` or ``Years`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                default_retention_property = s3_mixins.CfnBucketPropsMixin.DefaultRetentionProperty(
                    days=123,
                    mode="mode",
                    years=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__077127c5e8afe4d07cfd9d48a98dc170a9257a634e8de80d8484522e73681065)
                check_type(argname="argument days", value=days, expected_type=type_hints["days"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument years", value=years, expected_type=type_hints["years"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days is not None:
                self._values["days"] = days
            if mode is not None:
                self._values["mode"] = mode
            if years is not None:
                self._values["years"] = years

        @builtins.property
        def days(self) -> typing.Optional[jsii.Number]:
            '''The number of days that you want to specify for the default retention period.

            If Object Lock is turned on, you must specify ``Mode`` and specify either ``Days`` or ``Years`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html#cfn-s3-bucket-defaultretention-days
            '''
            result = self._values.get("days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The default Object Lock retention mode you want to apply to new objects placed in the specified bucket.

            If Object Lock is turned on, you must specify ``Mode`` and specify either ``Days`` or ``Years`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html#cfn-s3-bucket-defaultretention-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def years(self) -> typing.Optional[jsii.Number]:
            '''The number of years that you want to specify for the default retention period.

            If Object Lock is turned on, you must specify ``Mode`` and specify either ``Days`` or ``Years`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html#cfn-s3-bucket-defaultretention-years
            '''
            result = self._values.get("years")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultRetentionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.DeleteMarkerReplicationProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class DeleteMarkerReplicationProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''Specifies whether Amazon S3 replicates delete markers.

            If you specify a ``Filter`` in your replication configuration, you must also include a ``DeleteMarkerReplication`` element. If your ``Filter`` includes a ``Tag`` element, the ``DeleteMarkerReplication`` ``Status`` must be set to Disabled, because Amazon S3 does not support replicating delete markers for tag-based rules. For an example configuration, see `Basic Rule Configuration <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-add-config.html#replication-config-min-rule-config>`_ .

            For more information about delete marker replication, see `Basic Rule Configuration <https://docs.aws.amazon.com/AmazonS3/latest/dev/delete-marker-replication.html>`_ .
            .. epigraph::

               If you are using an earlier version of the replication configuration, Amazon S3 handles replication of delete markers differently. For more information, see `Backward Compatibility <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-add-config.html#replication-backward-compat-considerations>`_ .

            :param status: Indicates whether to replicate delete markers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-deletemarkerreplication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                delete_marker_replication_property = s3_mixins.CfnBucketPropsMixin.DeleteMarkerReplicationProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fad0b0de523104cf3b2adb023578b786db52918bc40706dd3e102537a2f5da53)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Indicates whether to replicate delete markers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-deletemarkerreplication.html#cfn-s3-bucket-deletemarkerreplication-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeleteMarkerReplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_account_id": "bucketAccountId",
            "bucket_arn": "bucketArn",
            "format": "format",
            "prefix": "prefix",
        },
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            bucket_account_id: typing.Optional[builtins.str] = None,
            bucket_arn: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information about where to publish analysis or configuration results for an Amazon S3 bucket.

            :param bucket_account_id: The account ID that owns the destination S3 bucket. If no account ID is provided, the owner is not validated before exporting data. .. epigraph:: Although this value is optional, we strongly recommend that you set it to help prevent problems if the destination bucket ownership changes.
            :param bucket_arn: The Amazon Resource Name (ARN) of the bucket to which data is exported.
            :param format: Specifies the file format used when exporting data to Amazon S3. *Allowed values* : ``CSV`` | ``ORC`` | ``Parquet``
            :param prefix: The prefix to use when exporting data. The prefix is prepended to all results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                destination_property = s3_mixins.CfnBucketPropsMixin.DestinationProperty(
                    bucket_account_id="bucketAccountId",
                    bucket_arn="bucketArn",
                    format="format",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__961597f5613486a51f088843f499bb1ca619ce13572e6e59b839c0df37825f1c)
                check_type(argname="argument bucket_account_id", value=bucket_account_id, expected_type=type_hints["bucket_account_id"])
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_account_id is not None:
                self._values["bucket_account_id"] = bucket_account_id
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if format is not None:
                self._values["format"] = format
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket_account_id(self) -> typing.Optional[builtins.str]:
            '''The account ID that owns the destination S3 bucket.

            If no account ID is provided, the owner is not validated before exporting data.
            .. epigraph::

               Although this value is optional, we strongly recommend that you set it to help prevent problems if the destination bucket ownership changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-bucketaccountid
            '''
            result = self._values.get("bucket_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the bucket to which data is exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''Specifies the file format used when exporting data to Amazon S3.

            *Allowed values* : ``CSV`` | ``ORC`` | ``Parquet``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix to use when exporting data.

            The prefix is prepended to all results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"replica_kms_key_id": "replicaKmsKeyId"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            replica_kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies encryption-related information for an Amazon S3 bucket that is a destination for replicated objects.

            .. epigraph::

               If you're specifying a customer managed KMS key, we recommend using a fully qualified KMS key ARN. If you use a KMS key alias instead, then AWS  resolves the key within the requester’s account. This behavior can result in data that's encrypted with a KMS key that belongs to the requester, and not the bucket owner.

            :param replica_kms_key_id: Specifies the ID (Key ARN or Alias ARN) of the customer managed AWS KMS key stored in AWS Key Management Service (KMS) for the destination bucket. Amazon S3 uses this key to encrypt replica objects. Amazon S3 only supports symmetric encryption KMS keys. For more information, see `Asymmetric keys in AWS KMS <https://docs.aws.amazon.com//kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                encryption_configuration_property = s3_mixins.CfnBucketPropsMixin.EncryptionConfigurationProperty(
                    replica_kms_key_id="replicaKmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__69072e1d8dff103d2196f16fbe1540c5d4b6226200498b5a7a8e505164c448e9)
                check_type(argname="argument replica_kms_key_id", value=replica_kms_key_id, expected_type=type_hints["replica_kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if replica_kms_key_id is not None:
                self._values["replica_kms_key_id"] = replica_kms_key_id

        @builtins.property
        def replica_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the ID (Key ARN or Alias ARN) of the customer managed AWS KMS key stored in AWS Key Management Service (KMS) for the destination bucket.

            Amazon S3 uses this key to encrypt replica objects. Amazon S3 only supports symmetric encryption KMS keys. For more information, see `Asymmetric keys in AWS KMS <https://docs.aws.amazon.com//kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-encryptionconfiguration.html#cfn-s3-bucket-encryptionconfiguration-replicakmskeyid
            '''
            result = self._values.get("replica_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.EventBridgeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"event_bridge_enabled": "eventBridgeEnabled"},
    )
    class EventBridgeConfigurationProperty:
        def __init__(
            self,
            *,
            event_bridge_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Amazon S3 can send events to Amazon EventBridge whenever certain events happen in your bucket, see `Using EventBridge <https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html>`_ in the *Amazon S3 User Guide* .

            Unlike other destinations, delivery of events to EventBridge can be either enabled or disabled for a bucket. If enabled, all events will be sent to EventBridge and you can use EventBridge rules to route events to additional targets. For more information, see `What Is Amazon EventBridge <https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html>`_ in the *Amazon EventBridge User Guide*

            :param event_bridge_enabled: Enables delivery of events to Amazon EventBridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-eventbridgeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                event_bridge_configuration_property = s3_mixins.CfnBucketPropsMixin.EventBridgeConfigurationProperty(
                    event_bridge_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44df92e978075efa2b5af256e9aa2dbbeaf7f193582438bd054a66874133ba2a)
                check_type(argname="argument event_bridge_enabled", value=event_bridge_enabled, expected_type=type_hints["event_bridge_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_bridge_enabled is not None:
                self._values["event_bridge_enabled"] = event_bridge_enabled

        @builtins.property
        def event_bridge_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables delivery of events to Amazon EventBridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-eventbridgeconfiguration.html#cfn-s3-bucket-eventbridgeconfiguration-eventbridgeenabled
            '''
            result = self._values.get("event_bridge_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.FilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class FilterRuleProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Amazon S3 object key name to filter on.

            An object key name is the name assigned to an object in your Amazon S3 bucket. You specify whether to filter on the suffix or prefix of the object key name. A prefix is a specific string of characters at the beginning of an object key name, which you can use to organize objects. For example, you can start the key names of related objects with a prefix, such as ``2023-`` or ``engineering/`` . Then, you can use ``FilterRule`` to find objects in a bucket with key names that have the same prefix. A suffix is similar to a prefix, but it is at the end of the object key name instead of at the beginning.

            :param name: The object key name prefix or suffix identifying one or more objects to which the filtering rule applies. The maximum length is 1,024 characters. Overlapping prefixes and suffixes are not supported. For more information, see `Configuring Event Notifications <https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html>`_ in the *Amazon S3 User Guide* .
            :param value: The value that the filter searches for in object key names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-filterrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                filter_rule_property = s3_mixins.CfnBucketPropsMixin.FilterRuleProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__359f601d97992243da5c3da82dc6f03ce2961b27ab9755c698e765ca4935b4b3)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The object key name prefix or suffix identifying one or more objects to which the filtering rule applies.

            The maximum length is 1,024 characters. Overlapping prefixes and suffixes are not supported. For more information, see `Configuring Event Notifications <https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-filterrule.html#cfn-s3-bucket-filterrule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value that the filter searches for in object key names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-filterrule.html#cfn-s3-bucket-filterrule-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.IntelligentTieringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "prefix": "prefix",
            "status": "status",
            "tag_filters": "tagFilters",
            "tierings": "tierings",
        },
    )
    class IntelligentTieringConfigurationProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tierings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TieringProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies the S3 Intelligent-Tiering configuration for an Amazon S3 bucket.

            For information about the S3 Intelligent-Tiering storage class, see `Storage class for automatically optimizing frequently and infrequently accessed objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html#sc-dynamic-data-access>`_ .

            :param id: The ID used to identify the S3 Intelligent-Tiering configuration.
            :param prefix: An object key name prefix that identifies the subset of objects to which the rule applies.
            :param status: Specifies the status of the configuration.
            :param tag_filters: A container for a key-value pair.
            :param tierings: Specifies a list of S3 Intelligent-Tiering storage class tiers in the configuration. At least one tier must be defined in the list. At most, you can specify two tiers in the list, one for each available AccessTier: ``ARCHIVE_ACCESS`` and ``DEEP_ARCHIVE_ACCESS`` . .. epigraph:: You only need Intelligent Tiering Configuration enabled on a bucket if you want to automatically move objects stored in the Intelligent-Tiering storage class to Archive Access or Deep Archive Access tiers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                intelligent_tiering_configuration_property = s3_mixins.CfnBucketPropsMixin.IntelligentTieringConfigurationProperty(
                    id="id",
                    prefix="prefix",
                    status="status",
                    tag_filters=[s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                        key="key",
                        value="value"
                    )],
                    tierings=[s3_mixins.CfnBucketPropsMixin.TieringProperty(
                        access_tier="accessTier",
                        days=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c21c827b8aa4a9f5946175db6b8d1583ee7adaae67915e04e66e1a135d5ef37)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument tag_filters", value=tag_filters, expected_type=type_hints["tag_filters"])
                check_type(argname="argument tierings", value=tierings, expected_type=type_hints["tierings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if prefix is not None:
                self._values["prefix"] = prefix
            if status is not None:
                self._values["status"] = status
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters
            if tierings is not None:
                self._values["tierings"] = tierings

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID used to identify the S3 Intelligent-Tiering configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''An object key name prefix that identifies the subset of objects to which the rule applies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Specifies the status of the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]]:
            '''A container for a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]], result)

        @builtins.property
        def tierings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TieringProperty"]]]]:
            '''Specifies a list of S3 Intelligent-Tiering storage class tiers in the configuration.

            At least one tier must be defined in the list. At most, you can specify two tiers in the list, one for each available AccessTier: ``ARCHIVE_ACCESS`` and ``DEEP_ARCHIVE_ACCESS`` .
            .. epigraph::

               You only need Intelligent Tiering Configuration enabled on a bucket if you want to automatically move objects stored in the Intelligent-Tiering storage class to Archive Access or Deep Archive Access tiers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-tierings
            '''
            result = self._values.get("tierings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TieringProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntelligentTieringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.InventoryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "enabled": "enabled",
            "id": "id",
            "included_object_versions": "includedObjectVersions",
            "optional_fields": "optionalFields",
            "prefix": "prefix",
            "schedule_frequency": "scheduleFrequency",
        },
    )
    class InventoryConfigurationProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            id: typing.Optional[builtins.str] = None,
            included_object_versions: typing.Optional[builtins.str] = None,
            optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
            prefix: typing.Optional[builtins.str] = None,
            schedule_frequency: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the S3 Inventory configuration for an Amazon S3 bucket.

            For more information, see `GET Bucket inventory <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETInventoryConfig.html>`_ in the *Amazon S3 API Reference* .

            :param destination: Contains information about where to publish the inventory results.
            :param enabled: Specifies whether the inventory is enabled or disabled. If set to ``True`` , an inventory list is generated. If set to ``False`` , no inventory list is generated.
            :param id: The ID used to identify the inventory configuration.
            :param included_object_versions: Object versions to include in the inventory list. If set to ``All`` , the list includes all the object versions, which adds the version-related fields ``VersionId`` , ``IsLatest`` , and ``DeleteMarker`` to the list. If set to ``Current`` , the list does not contain these version-related fields.
            :param optional_fields: Contains the optional fields that are included in the inventory results.
            :param prefix: Specifies the inventory filter prefix.
            :param schedule_frequency: Specifies the schedule for generating inventory results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                inventory_configuration_property = s3_mixins.CfnBucketPropsMixin.InventoryConfigurationProperty(
                    destination=s3_mixins.CfnBucketPropsMixin.DestinationProperty(
                        bucket_account_id="bucketAccountId",
                        bucket_arn="bucketArn",
                        format="format",
                        prefix="prefix"
                    ),
                    enabled=False,
                    id="id",
                    included_object_versions="includedObjectVersions",
                    optional_fields=["optionalFields"],
                    prefix="prefix",
                    schedule_frequency="scheduleFrequency"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5701426a2687424386b689a1eb323dc5e32bb9d66fd3ab3c4e7388cf91cfa9c1)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument included_object_versions", value=included_object_versions, expected_type=type_hints["included_object_versions"])
                check_type(argname="argument optional_fields", value=optional_fields, expected_type=type_hints["optional_fields"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument schedule_frequency", value=schedule_frequency, expected_type=type_hints["schedule_frequency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if enabled is not None:
                self._values["enabled"] = enabled
            if id is not None:
                self._values["id"] = id
            if included_object_versions is not None:
                self._values["included_object_versions"] = included_object_versions
            if optional_fields is not None:
                self._values["optional_fields"] = optional_fields
            if prefix is not None:
                self._values["prefix"] = prefix
            if schedule_frequency is not None:
                self._values["schedule_frequency"] = schedule_frequency

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DestinationProperty"]]:
            '''Contains information about where to publish the inventory results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DestinationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the inventory is enabled or disabled.

            If set to ``True`` , an inventory list is generated. If set to ``False`` , no inventory list is generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID used to identify the inventory configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def included_object_versions(self) -> typing.Optional[builtins.str]:
            '''Object versions to include in the inventory list.

            If set to ``All`` , the list includes all the object versions, which adds the version-related fields ``VersionId`` , ``IsLatest`` , and ``DeleteMarker`` to the list. If set to ``Current`` , the list does not contain these version-related fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-includedobjectversions
            '''
            result = self._values.get("included_object_versions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def optional_fields(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Contains the optional fields that are included in the inventory results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-optionalfields
            '''
            result = self._values.get("optional_fields")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''Specifies the inventory filter prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_frequency(self) -> typing.Optional[builtins.str]:
            '''Specifies the schedule for generating inventory results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-schedulefrequency
            '''
            result = self._values.get("schedule_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InventoryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.InventoryTableConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_state": "configurationState",
            "encryption_configuration": "encryptionConfiguration",
            "table_arn": "tableArn",
            "table_name": "tableName",
        },
    )
    class InventoryTableConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_state: typing.Optional[builtins.str] = None,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_arn: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The inventory table configuration for an S3 Metadata configuration.

            :param configuration_state: The configuration state of the inventory table, indicating whether the inventory table is enabled or disabled.
            :param encryption_configuration: The encryption configuration for the inventory table.
            :param table_arn: The Amazon Resource Name (ARN) for the inventory table.
            :param table_name: The name of the inventory table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventorytableconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                inventory_table_configuration_property = s3_mixins.CfnBucketPropsMixin.InventoryTableConfigurationProperty(
                    configuration_state="configurationState",
                    encryption_configuration=s3_mixins.CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty(
                        kms_key_arn="kmsKeyArn",
                        sse_algorithm="sseAlgorithm"
                    ),
                    table_arn="tableArn",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__035cb9f72b132fcc4c32f97b15b79fb192d466b0016e8cc8cade3b721689d04e)
                check_type(argname="argument configuration_state", value=configuration_state, expected_type=type_hints["configuration_state"])
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration_state is not None:
                self._values["configuration_state"] = configuration_state
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if table_arn is not None:
                self._values["table_arn"] = table_arn
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def configuration_state(self) -> typing.Optional[builtins.str]:
            '''The configuration state of the inventory table, indicating whether the inventory table is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventorytableconfiguration.html#cfn-s3-bucket-inventorytableconfiguration-configurationstate
            '''
            result = self._values.get("configuration_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty"]]:
            '''The encryption configuration for the inventory table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventorytableconfiguration.html#cfn-s3-bucket-inventorytableconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty"]], result)

        @builtins.property
        def table_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the inventory table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventorytableconfiguration.html#cfn-s3-bucket-inventorytableconfiguration-tablearn
            '''
            result = self._values.get("table_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the inventory table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventorytableconfiguration.html#cfn-s3-bucket-inventorytableconfiguration-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InventoryTableConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.JournalTableConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_configuration": "encryptionConfiguration",
            "record_expiration": "recordExpiration",
            "table_arn": "tableArn",
            "table_name": "tableName",
        },
    )
    class JournalTableConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            record_expiration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.RecordExpirationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_arn: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The journal table configuration for an S3 Metadata configuration.

            :param encryption_configuration: The encryption configuration for the journal table.
            :param record_expiration: The journal table record expiration settings for the journal table.
            :param table_arn: The Amazon Resource Name (ARN) for the journal table.
            :param table_name: The name of the journal table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-journaltableconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                journal_table_configuration_property = s3_mixins.CfnBucketPropsMixin.JournalTableConfigurationProperty(
                    encryption_configuration=s3_mixins.CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty(
                        kms_key_arn="kmsKeyArn",
                        sse_algorithm="sseAlgorithm"
                    ),
                    record_expiration=s3_mixins.CfnBucketPropsMixin.RecordExpirationProperty(
                        days=123,
                        expiration="expiration"
                    ),
                    table_arn="tableArn",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5923a017aa9456c9e573060a7edba1e2511cc79b87302ee3ccc99c3832c864fd)
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument record_expiration", value=record_expiration, expected_type=type_hints["record_expiration"])
                check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if record_expiration is not None:
                self._values["record_expiration"] = record_expiration
            if table_arn is not None:
                self._values["table_arn"] = table_arn
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty"]]:
            '''The encryption configuration for the journal table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-journaltableconfiguration.html#cfn-s3-bucket-journaltableconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty"]], result)

        @builtins.property
        def record_expiration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RecordExpirationProperty"]]:
            '''The journal table record expiration settings for the journal table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-journaltableconfiguration.html#cfn-s3-bucket-journaltableconfiguration-recordexpiration
            '''
            result = self._values.get("record_expiration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RecordExpirationProperty"]], result)

        @builtins.property
        def table_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the journal table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-journaltableconfiguration.html#cfn-s3-bucket-journaltableconfiguration-tablearn
            '''
            result = self._values.get("table_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the journal table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-journaltableconfiguration.html#cfn-s3-bucket-journaltableconfiguration-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JournalTableConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.LambdaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"event": "event", "filter": "filter", "function": "function"},
    )
    class LambdaConfigurationProperty:
        def __init__(
            self,
            *,
            event: typing.Optional[builtins.str] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.NotificationFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            function: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the AWS Lambda functions to invoke and the events for which to invoke them.

            :param event: The Amazon S3 bucket event for which to invoke the AWS Lambda function. For more information, see `Supported Event Types <https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html>`_ in the *Amazon S3 User Guide* .
            :param filter: The filtering rules that determine which objects invoke the AWS Lambda function. For example, you can create a filter so that only image files with a ``.jpg`` extension invoke the function when they are added to the Amazon S3 bucket.
            :param function: The Amazon Resource Name (ARN) of the AWS Lambda function that Amazon S3 invokes when the specified event type occurs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lambdaconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                lambda_configuration_property = s3_mixins.CfnBucketPropsMixin.LambdaConfigurationProperty(
                    event="event",
                    filter=s3_mixins.CfnBucketPropsMixin.NotificationFilterProperty(
                        s3_key=s3_mixins.CfnBucketPropsMixin.S3KeyFilterProperty(
                            rules=[s3_mixins.CfnBucketPropsMixin.FilterRuleProperty(
                                name="name",
                                value="value"
                            )]
                        )
                    ),
                    function="function"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__926c6a45a529cd64437e9280f2f8c50954c58201e27270a774fcc74ee27ceea3)
                check_type(argname="argument event", value=event, expected_type=type_hints["event"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event is not None:
                self._values["event"] = event
            if filter is not None:
                self._values["filter"] = filter
            if function is not None:
                self._values["function"] = function

        @builtins.property
        def event(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket event for which to invoke the AWS Lambda function.

            For more information, see `Supported Event Types <https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lambdaconfiguration.html#cfn-s3-bucket-lambdaconfiguration-event
            '''
            result = self._values.get("event")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NotificationFilterProperty"]]:
            '''The filtering rules that determine which objects invoke the AWS Lambda function.

            For example, you can create a filter so that only image files with a ``.jpg`` extension invoke the function when they are added to the Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lambdaconfiguration.html#cfn-s3-bucket-lambdaconfiguration-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NotificationFilterProperty"]], result)

        @builtins.property
        def function(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Lambda function that Amazon S3 invokes when the specified event type occurs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lambdaconfiguration.html#cfn-s3-bucket-lambdaconfiguration-function
            '''
            result = self._values.get("function")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.LifecycleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rules": "rules",
            "transition_default_minimum_object_size": "transitionDefaultMinimumObjectSize",
        },
    )
    class LifecycleConfigurationProperty:
        def __init__(
            self,
            *,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            transition_default_minimum_object_size: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the lifecycle configuration for objects in an Amazon S3 bucket.

            For more information, see `Object Lifecycle Management <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html>`_ in the *Amazon S3 User Guide* .

            :param rules: A lifecycle rule for individual objects in an Amazon S3 bucket.
            :param transition_default_minimum_object_size: Indicates which default minimum object size behavior is applied to the lifecycle configuration. .. epigraph:: This parameter applies to general purpose buckets only. It isn't supported for directory bucket lifecycle configurations. - ``all_storage_classes_128K`` - Objects smaller than 128 KB will not transition to any storage class by default. - ``varies_by_storage_class`` - Objects smaller than 128 KB will transition to Glacier Flexible Retrieval or Glacier Deep Archive storage classes. By default, all other storage classes will prevent transitions smaller than 128 KB. To customize the minimum object size for any transition you can add a filter that specifies a custom ``ObjectSizeGreaterThan`` or ``ObjectSizeLessThan`` in the body of your transition rule. Custom filters always take precedence over the default transition behavior.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                lifecycle_configuration_property = s3_mixins.CfnBucketPropsMixin.LifecycleConfigurationProperty(
                    rules=[s3_mixins.CfnBucketPropsMixin.RuleProperty(
                        abort_incomplete_multipart_upload=s3_mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                            days_after_initiation=123
                        ),
                        expiration_date=Date(),
                        expiration_in_days=123,
                        expired_object_delete_marker=False,
                        id="id",
                        noncurrent_version_expiration=s3_mixins.CfnBucketPropsMixin.NoncurrentVersionExpirationProperty(
                            newer_noncurrent_versions=123,
                            noncurrent_days=123
                        ),
                        noncurrent_version_expiration_in_days=123,
                        noncurrent_version_transition=s3_mixins.CfnBucketPropsMixin.NoncurrentVersionTransitionProperty(
                            newer_noncurrent_versions=123,
                            storage_class="storageClass",
                            transition_in_days=123
                        ),
                        noncurrent_version_transitions=[s3_mixins.CfnBucketPropsMixin.NoncurrentVersionTransitionProperty(
                            newer_noncurrent_versions=123,
                            storage_class="storageClass",
                            transition_in_days=123
                        )],
                        object_size_greater_than=123,
                        object_size_less_than=123,
                        prefix="prefix",
                        status="status",
                        tag_filters=[s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                            key="key",
                            value="value"
                        )],
                        transition=s3_mixins.CfnBucketPropsMixin.TransitionProperty(
                            storage_class="storageClass",
                            transition_date=Date(),
                            transition_in_days=123
                        ),
                        transitions=[s3_mixins.CfnBucketPropsMixin.TransitionProperty(
                            storage_class="storageClass",
                            transition_date=Date(),
                            transition_in_days=123
                        )]
                    )],
                    transition_default_minimum_object_size="transitionDefaultMinimumObjectSize"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1fe77de25f12309c650326e9ac3a42351cc0d19b0e68914ee89b32da1d5cc14d)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
                check_type(argname="argument transition_default_minimum_object_size", value=transition_default_minimum_object_size, expected_type=type_hints["transition_default_minimum_object_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules is not None:
                self._values["rules"] = rules
            if transition_default_minimum_object_size is not None:
                self._values["transition_default_minimum_object_size"] = transition_default_minimum_object_size

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RuleProperty"]]]]:
            '''A lifecycle rule for individual objects in an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfiguration.html#cfn-s3-bucket-lifecycleconfiguration-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RuleProperty"]]]], result)

        @builtins.property
        def transition_default_minimum_object_size(
            self,
        ) -> typing.Optional[builtins.str]:
            '''Indicates which default minimum object size behavior is applied to the lifecycle configuration.

            .. epigraph::

               This parameter applies to general purpose buckets only. It isn't supported for directory bucket lifecycle configurations.

            - ``all_storage_classes_128K`` - Objects smaller than 128 KB will not transition to any storage class by default.
            - ``varies_by_storage_class`` - Objects smaller than 128 KB will transition to Glacier Flexible Retrieval or Glacier Deep Archive storage classes. By default, all other storage classes will prevent transitions smaller than 128 KB.

            To customize the minimum object size for any transition you can add a filter that specifies a custom ``ObjectSizeGreaterThan`` or ``ObjectSizeLessThan`` in the body of your transition rule. Custom filters always take precedence over the default transition behavior.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfiguration.html#cfn-s3-bucket-lifecycleconfiguration-transitiondefaultminimumobjectsize
            '''
            result = self._values.get("transition_default_minimum_object_size")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_bucket_name": "destinationBucketName",
            "log_file_prefix": "logFilePrefix",
            "target_object_key_format": "targetObjectKeyFormat",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            destination_bucket_name: typing.Optional[builtins.str] = None,
            log_file_prefix: typing.Optional[builtins.str] = None,
            target_object_key_format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TargetObjectKeyFormatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes where logs are stored and the prefix that Amazon S3 assigns to all log object keys for a bucket.

            For examples and more information, see `PUT Bucket logging <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTlogging.html>`_ in the *Amazon S3 API Reference* .
            .. epigraph::

               To successfully complete the ``AWS::S3::Bucket LoggingConfiguration`` request, you must have ``s3:PutObject`` and ``s3:PutObjectAcl`` in your IAM permissions.

            :param destination_bucket_name: The name of the bucket where Amazon S3 should store server access log files. You can store log files in any bucket that you own. By default, logs are stored in the bucket where the ``LoggingConfiguration`` property is defined.
            :param log_file_prefix: A prefix for all log object keys. If you store log files from multiple Amazon S3 buckets in a single bucket, you can use a prefix to distinguish which log files came from which bucket.
            :param target_object_key_format: Amazon S3 key format for log objects. Only one format, either PartitionedPrefix or SimplePrefix, is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                # simple_prefix: Any
                
                logging_configuration_property = s3_mixins.CfnBucketPropsMixin.LoggingConfigurationProperty(
                    destination_bucket_name="destinationBucketName",
                    log_file_prefix="logFilePrefix",
                    target_object_key_format=s3_mixins.CfnBucketPropsMixin.TargetObjectKeyFormatProperty(
                        partitioned_prefix=s3_mixins.CfnBucketPropsMixin.PartitionedPrefixProperty(
                            partition_date_source="partitionDateSource"
                        ),
                        simple_prefix=simple_prefix
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12f377ce0c94a5c9b7d29d6ab0a709768d4dbf1eb7461b7f144f4ccc083ace09)
                check_type(argname="argument destination_bucket_name", value=destination_bucket_name, expected_type=type_hints["destination_bucket_name"])
                check_type(argname="argument log_file_prefix", value=log_file_prefix, expected_type=type_hints["log_file_prefix"])
                check_type(argname="argument target_object_key_format", value=target_object_key_format, expected_type=type_hints["target_object_key_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_bucket_name is not None:
                self._values["destination_bucket_name"] = destination_bucket_name
            if log_file_prefix is not None:
                self._values["log_file_prefix"] = log_file_prefix
            if target_object_key_format is not None:
                self._values["target_object_key_format"] = target_object_key_format

        @builtins.property
        def destination_bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the bucket where Amazon S3 should store server access log files.

            You can store log files in any bucket that you own. By default, logs are stored in the bucket where the ``LoggingConfiguration`` property is defined.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfiguration.html#cfn-s3-bucket-loggingconfiguration-destinationbucketname
            '''
            result = self._values.get("destination_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_file_prefix(self) -> typing.Optional[builtins.str]:
            '''A prefix for all log object keys.

            If you store log files from multiple Amazon S3 buckets in a single bucket, you can use a prefix to distinguish which log files came from which bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfiguration.html#cfn-s3-bucket-loggingconfiguration-logfileprefix
            '''
            result = self._values.get("log_file_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_object_key_format(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TargetObjectKeyFormatProperty"]]:
            '''Amazon S3 key format for log objects.

            Only one format, either PartitionedPrefix or SimplePrefix, is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfiguration.html#cfn-s3-bucket-loggingconfiguration-targetobjectkeyformat
            '''
            result = self._values.get("target_object_key_format")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TargetObjectKeyFormatProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.MetadataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "inventory_table_configuration": "inventoryTableConfiguration",
            "journal_table_configuration": "journalTableConfiguration",
        },
    )
    class MetadataConfigurationProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.MetadataDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            inventory_table_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.InventoryTableConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            journal_table_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.JournalTableConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Creates a V2 Amazon S3 Metadata configuration of a general purpose bucket.

            For more information, see `Accelerating data discovery with S3 Metadata <https://docs.aws.amazon.com/AmazonS3/latest/userguide/metadata-tables-overview.html>`_ in the *Amazon S3 User Guide* .

            :param destination: The destination information for the S3 Metadata configuration.
            :param inventory_table_configuration: The inventory table configuration for a metadata configuration.
            :param journal_table_configuration: The journal table configuration for a metadata configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                metadata_configuration_property = s3_mixins.CfnBucketPropsMixin.MetadataConfigurationProperty(
                    destination=s3_mixins.CfnBucketPropsMixin.MetadataDestinationProperty(
                        table_bucket_arn="tableBucketArn",
                        table_bucket_type="tableBucketType",
                        table_namespace="tableNamespace"
                    ),
                    inventory_table_configuration=s3_mixins.CfnBucketPropsMixin.InventoryTableConfigurationProperty(
                        configuration_state="configurationState",
                        encryption_configuration=s3_mixins.CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty(
                            kms_key_arn="kmsKeyArn",
                            sse_algorithm="sseAlgorithm"
                        ),
                        table_arn="tableArn",
                        table_name="tableName"
                    ),
                    journal_table_configuration=s3_mixins.CfnBucketPropsMixin.JournalTableConfigurationProperty(
                        encryption_configuration=s3_mixins.CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty(
                            kms_key_arn="kmsKeyArn",
                            sse_algorithm="sseAlgorithm"
                        ),
                        record_expiration=s3_mixins.CfnBucketPropsMixin.RecordExpirationProperty(
                            days=123,
                            expiration="expiration"
                        ),
                        table_arn="tableArn",
                        table_name="tableName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f98a78eb65f2e0f0b916847010bac1317995d462e993f64cbc21a777472cdfa)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument inventory_table_configuration", value=inventory_table_configuration, expected_type=type_hints["inventory_table_configuration"])
                check_type(argname="argument journal_table_configuration", value=journal_table_configuration, expected_type=type_hints["journal_table_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if inventory_table_configuration is not None:
                self._values["inventory_table_configuration"] = inventory_table_configuration
            if journal_table_configuration is not None:
                self._values["journal_table_configuration"] = journal_table_configuration

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataDestinationProperty"]]:
            '''The destination information for the S3 Metadata configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadataconfiguration.html#cfn-s3-bucket-metadataconfiguration-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetadataDestinationProperty"]], result)

        @builtins.property
        def inventory_table_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.InventoryTableConfigurationProperty"]]:
            '''The inventory table configuration for a metadata configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadataconfiguration.html#cfn-s3-bucket-metadataconfiguration-inventorytableconfiguration
            '''
            result = self._values.get("inventory_table_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.InventoryTableConfigurationProperty"]], result)

        @builtins.property
        def journal_table_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.JournalTableConfigurationProperty"]]:
            '''The journal table configuration for a metadata configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadataconfiguration.html#cfn-s3-bucket-metadataconfiguration-journaltableconfiguration
            '''
            result = self._values.get("journal_table_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.JournalTableConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.MetadataDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "table_bucket_arn": "tableBucketArn",
            "table_bucket_type": "tableBucketType",
            "table_namespace": "tableNamespace",
        },
    )
    class MetadataDestinationProperty:
        def __init__(
            self,
            *,
            table_bucket_arn: typing.Optional[builtins.str] = None,
            table_bucket_type: typing.Optional[builtins.str] = None,
            table_namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The destination information for the S3 Metadata configuration.

            :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket where the metadata configuration is stored.
            :param table_bucket_type: The type of the table bucket where the metadata configuration is stored. The ``aws`` value indicates an AWS managed table bucket, and the ``customer`` value indicates a customer-managed table bucket. V2 metadata configurations are stored in AWS managed table buckets, and V1 metadata configurations are stored in customer-managed table buckets.
            :param table_namespace: The namespace in the table bucket where the metadata tables for a metadata configuration are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadatadestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                metadata_destination_property = s3_mixins.CfnBucketPropsMixin.MetadataDestinationProperty(
                    table_bucket_arn="tableBucketArn",
                    table_bucket_type="tableBucketType",
                    table_namespace="tableNamespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eda645bd09169eb4cc8e766535d98f550bf2a3969f3fac25d836ac3e7c517744)
                check_type(argname="argument table_bucket_arn", value=table_bucket_arn, expected_type=type_hints["table_bucket_arn"])
                check_type(argname="argument table_bucket_type", value=table_bucket_type, expected_type=type_hints["table_bucket_type"])
                check_type(argname="argument table_namespace", value=table_namespace, expected_type=type_hints["table_namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if table_bucket_arn is not None:
                self._values["table_bucket_arn"] = table_bucket_arn
            if table_bucket_type is not None:
                self._values["table_bucket_type"] = table_bucket_type
            if table_namespace is not None:
                self._values["table_namespace"] = table_namespace

        @builtins.property
        def table_bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the table bucket where the metadata configuration is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadatadestination.html#cfn-s3-bucket-metadatadestination-tablebucketarn
            '''
            result = self._values.get("table_bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_bucket_type(self) -> typing.Optional[builtins.str]:
            '''The type of the table bucket where the metadata configuration is stored.

            The ``aws`` value indicates an AWS managed table bucket, and the ``customer`` value indicates a customer-managed table bucket. V2 metadata configurations are stored in AWS managed table buckets, and V1 metadata configurations are stored in customer-managed table buckets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadatadestination.html#cfn-s3-bucket-metadatadestination-tablebuckettype
            '''
            result = self._values.get("table_bucket_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace in the table bucket where the metadata tables for a metadata configuration are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadatadestination.html#cfn-s3-bucket-metadatadestination-tablenamespace
            '''
            result = self._values.get("table_namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.MetadataTableConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_tables_destination": "s3TablesDestination"},
    )
    class MetadataTableConfigurationProperty:
        def __init__(
            self,
            *,
            s3_tables_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.S3TablesDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''.. epigraph::

   We recommend that you create your S3 Metadata configurations by using the V2 `MetadataConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-s3-bucket-metadataconfiguration.html>`_ resource type. We no longer recommend using the V1 ``MetadataTableConfiguration`` resource type. >  > If you created your S3 Metadata configuration before July 15, 2025, we recommend that you delete and re-create your configuration by using the `MetadataConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-s3-bucket-metadataconfiguration.html>`_ resource type so that you can expire journal table records and create a live inventory table.

            Creates a V1 S3 Metadata configuration for a general purpose bucket. For more information, see `Accelerating data discovery with S3 Metadata <https://docs.aws.amazon.com/AmazonS3/latest/userguide/metadata-tables-overview.html>`_ in the *Amazon S3 User Guide* .

            :param s3_tables_destination: The destination information for the metadata table configuration. The destination table bucket must be in the same Region and AWS account as the general purpose bucket. The specified metadata table name must be unique within the ``aws_s3_metadata`` namespace in the destination table bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadatatableconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                metadata_table_configuration_property = s3_mixins.CfnBucketPropsMixin.MetadataTableConfigurationProperty(
                    s3_tables_destination=s3_mixins.CfnBucketPropsMixin.S3TablesDestinationProperty(
                        table_arn="tableArn",
                        table_bucket_arn="tableBucketArn",
                        table_name="tableName",
                        table_namespace="tableNamespace"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__91aedfd60b0461bda0100d746756a9f326a770005a50658d6e146c5be40c9edd)
                check_type(argname="argument s3_tables_destination", value=s3_tables_destination, expected_type=type_hints["s3_tables_destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_tables_destination is not None:
                self._values["s3_tables_destination"] = s3_tables_destination

        @builtins.property
        def s3_tables_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.S3TablesDestinationProperty"]]:
            '''The destination information for the metadata table configuration.

            The destination table bucket must be in the same Region and AWS account as the general purpose bucket. The specified metadata table name must be unique within the ``aws_s3_metadata`` namespace in the destination table bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadatatableconfiguration.html#cfn-s3-bucket-metadatatableconfiguration-s3tablesdestination
            '''
            result = self._values.get("s3_tables_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.S3TablesDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataTableConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "sse_algorithm": "sseAlgorithm"},
    )
    class MetadataTableEncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            sse_algorithm: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The encryption settings for an S3 Metadata journal table or inventory table configuration.

            :param kms_key_arn: If server-side encryption with AWS Key Management Service ( AWS ) keys (SSE-KMS) is specified, you must also specify the KMS key Amazon Resource Name (ARN). You must specify a customer-managed KMS key that's located in the same Region as the general purpose bucket that corresponds to the metadata table configuration.
            :param sse_algorithm: The encryption type specified for a metadata table. To specify server-side encryption with AWS Key Management Service ( AWS ) keys (SSE-KMS), use the ``aws:kms`` value. To specify server-side encryption with Amazon S3 managed keys (SSE-S3), use the ``AES256`` value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadatatableencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                metadata_table_encryption_configuration_property = s3_mixins.CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty(
                    kms_key_arn="kmsKeyArn",
                    sse_algorithm="sseAlgorithm"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7be8a5e52b5569d50fbceccd413765f072524c902d877f333161727a00d7c03)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument sse_algorithm", value=sse_algorithm, expected_type=type_hints["sse_algorithm"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if sse_algorithm is not None:
                self._values["sse_algorithm"] = sse_algorithm

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''If server-side encryption with AWS Key Management Service ( AWS  ) keys (SSE-KMS) is specified, you must also specify the KMS key Amazon Resource Name (ARN).

            You must specify a customer-managed KMS key that's located in the same Region as the general purpose bucket that corresponds to the metadata table configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadatatableencryptionconfiguration.html#cfn-s3-bucket-metadatatableencryptionconfiguration-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sse_algorithm(self) -> typing.Optional[builtins.str]:
            '''The encryption type specified for a metadata table.

            To specify server-side encryption with AWS Key Management Service ( AWS  ) keys (SSE-KMS), use the ``aws:kms`` value. To specify server-side encryption with Amazon S3 managed keys (SSE-S3), use the ``AES256`` value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metadatatableencryptionconfiguration.html#cfn-s3-bucket-metadatatableencryptionconfiguration-ssealgorithm
            '''
            result = self._values.get("sse_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataTableEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.MetricsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_point_arn": "accessPointArn",
            "id": "id",
            "prefix": "prefix",
            "tag_filters": "tagFilters",
        },
    )
    class MetricsConfigurationProperty:
        def __init__(
            self,
            *,
            access_point_arn: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies a metrics configuration for the CloudWatch request metrics (specified by the metrics configuration ID) from an Amazon S3 bucket.

            If you're updating an existing metrics configuration, note that this is a full replacement of the existing metrics configuration. If you don't include the elements you want to keep, they are erased. For examples, see `AWS::S3::Bucket <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#aws-properties-s3-bucket--examples>`_ . For more information, see `PUT Bucket metrics <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTMetricConfiguration.html>`_ in the *Amazon S3 API Reference* .

            :param access_point_arn: The access point that was used while performing operations on the object. The metrics configuration only includes objects that meet the filter's criteria.
            :param id: The ID used to identify the metrics configuration. This can be any value you choose that helps you identify your metrics configuration.
            :param prefix: The prefix that an object must have to be included in the metrics results.
            :param tag_filters: Specifies a list of tag filters to use as a metrics configuration filter. The metrics configuration includes only objects that meet the filter's criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                metrics_configuration_property = s3_mixins.CfnBucketPropsMixin.MetricsConfigurationProperty(
                    access_point_arn="accessPointArn",
                    id="id",
                    prefix="prefix",
                    tag_filters=[s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc26563dd9d4c453237cf39f0a0e83868255ba5d9b99a876d783ef848cc96d1b)
                check_type(argname="argument access_point_arn", value=access_point_arn, expected_type=type_hints["access_point_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument tag_filters", value=tag_filters, expected_type=type_hints["tag_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_point_arn is not None:
                self._values["access_point_arn"] = access_point_arn
            if id is not None:
                self._values["id"] = id
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters

        @builtins.property
        def access_point_arn(self) -> typing.Optional[builtins.str]:
            '''The access point that was used while performing operations on the object.

            The metrics configuration only includes objects that meet the filter's criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-accesspointarn
            '''
            result = self._values.get("access_point_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID used to identify the metrics configuration.

            This can be any value you choose that helps you identify your metrics configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix that an object must have to be included in the metrics results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]]:
            '''Specifies a list of tag filters to use as a metrics configuration filter.

            The metrics configuration includes only objects that meet the filter's criteria.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.MetricsProperty",
        jsii_struct_bases=[],
        name_mapping={"event_threshold": "eventThreshold", "status": "status"},
    )
    class MetricsProperty:
        def __init__(
            self,
            *,
            event_threshold: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ReplicationTimeValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A container specifying replication metrics-related settings enabling replication metrics and events.

            :param event_threshold: A container specifying the time threshold for emitting the ``s3:Replication:OperationMissedThreshold`` event.
            :param status: Specifies whether the replication metrics are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metrics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                metrics_property = s3_mixins.CfnBucketPropsMixin.MetricsProperty(
                    event_threshold=s3_mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty(
                        minutes=123
                    ),
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0889d5e5b8977f2613c8e94a683d46cfd72029e3ce9e7f6f7167adaa10a4d12a)
                check_type(argname="argument event_threshold", value=event_threshold, expected_type=type_hints["event_threshold"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_threshold is not None:
                self._values["event_threshold"] = event_threshold
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def event_threshold(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationTimeValueProperty"]]:
            '''A container specifying the time threshold for emitting the ``s3:Replication:OperationMissedThreshold`` event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metrics.html#cfn-s3-bucket-metrics-eventthreshold
            '''
            result = self._values.get("event_threshold")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationTimeValueProperty"]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the replication metrics are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metrics.html#cfn-s3-bucket-metrics-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.NoncurrentVersionExpirationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "newer_noncurrent_versions": "newerNoncurrentVersions",
            "noncurrent_days": "noncurrentDays",
        },
    )
    class NoncurrentVersionExpirationProperty:
        def __init__(
            self,
            *,
            newer_noncurrent_versions: typing.Optional[jsii.Number] = None,
            noncurrent_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies when noncurrent object versions expire.

            Upon expiration, Amazon S3 permanently deletes the noncurrent object versions. You set this lifecycle configuration action on a bucket that has versioning enabled (or suspended) to request that Amazon S3 delete noncurrent object versions at a specific period in the object's lifetime. For more information about setting a lifecycle rule configuration, see `AWS::S3::Bucket Rule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html>`_ .

            :param newer_noncurrent_versions: Specifies how many noncurrent versions Amazon S3 will retain. If there are this many more recent noncurrent versions, Amazon S3 will take the associated action. For more information about noncurrent versions, see `Lifecycle configuration elements <https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html>`_ in the *Amazon S3 User Guide* .
            :param noncurrent_days: Specifies the number of days an object is noncurrent before Amazon S3 can perform the associated action. For information about the noncurrent days calculations, see `How Amazon S3 Calculates When an Object Became Noncurrent <https://docs.aws.amazon.com/AmazonS3/latest/dev/intro-lifecycle-rules.html#non-current-days-calculations>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-noncurrentversionexpiration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                noncurrent_version_expiration_property = s3_mixins.CfnBucketPropsMixin.NoncurrentVersionExpirationProperty(
                    newer_noncurrent_versions=123,
                    noncurrent_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbd6c762736f1d33a330b19c025a6c4b96209a5c8a418b51b96cbfd0c2941b57)
                check_type(argname="argument newer_noncurrent_versions", value=newer_noncurrent_versions, expected_type=type_hints["newer_noncurrent_versions"])
                check_type(argname="argument noncurrent_days", value=noncurrent_days, expected_type=type_hints["noncurrent_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if newer_noncurrent_versions is not None:
                self._values["newer_noncurrent_versions"] = newer_noncurrent_versions
            if noncurrent_days is not None:
                self._values["noncurrent_days"] = noncurrent_days

        @builtins.property
        def newer_noncurrent_versions(self) -> typing.Optional[jsii.Number]:
            '''Specifies how many noncurrent versions Amazon S3 will retain.

            If there are this many more recent noncurrent versions, Amazon S3 will take the associated action. For more information about noncurrent versions, see `Lifecycle configuration elements <https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-noncurrentversionexpiration.html#cfn-s3-bucket-noncurrentversionexpiration-newernoncurrentversions
            '''
            result = self._values.get("newer_noncurrent_versions")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def noncurrent_days(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of days an object is noncurrent before Amazon S3 can perform the associated action.

            For information about the noncurrent days calculations, see `How Amazon S3 Calculates When an Object Became Noncurrent <https://docs.aws.amazon.com/AmazonS3/latest/dev/intro-lifecycle-rules.html#non-current-days-calculations>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-noncurrentversionexpiration.html#cfn-s3-bucket-noncurrentversionexpiration-noncurrentdays
            '''
            result = self._values.get("noncurrent_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NoncurrentVersionExpirationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.NoncurrentVersionTransitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "newer_noncurrent_versions": "newerNoncurrentVersions",
            "storage_class": "storageClass",
            "transition_in_days": "transitionInDays",
        },
    )
    class NoncurrentVersionTransitionProperty:
        def __init__(
            self,
            *,
            newer_noncurrent_versions: typing.Optional[jsii.Number] = None,
            storage_class: typing.Optional[builtins.str] = None,
            transition_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Container for the transition rule that describes when noncurrent objects transition to the ``STANDARD_IA`` , ``ONEZONE_IA`` , ``INTELLIGENT_TIERING`` , ``GLACIER_IR`` , ``GLACIER`` , or ``DEEP_ARCHIVE`` storage class.

            If your bucket is versioning-enabled (or versioning is suspended), you can set this action to request that Amazon S3 transition noncurrent object versions to the ``STANDARD_IA`` , ``ONEZONE_IA`` , ``INTELLIGENT_TIERING`` , ``GLACIER_IR`` , ``GLACIER`` , or ``DEEP_ARCHIVE`` storage class at a specific period in the object's lifetime. If you specify this property, don't specify the ``NoncurrentVersionTransitions`` property.

            :param newer_noncurrent_versions: Specifies how many noncurrent versions Amazon S3 will retain. If there are this many more recent noncurrent versions, Amazon S3 will take the associated action. For more information about noncurrent versions, see `Lifecycle configuration elements <https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html>`_ in the *Amazon S3 User Guide* .
            :param storage_class: The class of storage used to store the object.
            :param transition_in_days: Specifies the number of days an object is noncurrent before Amazon S3 can perform the associated action. For information about the noncurrent days calculations, see `How Amazon S3 Calculates How Long an Object Has Been Noncurrent <https://docs.aws.amazon.com/AmazonS3/latest/dev/intro-lifecycle-rules.html#non-current-days-calculations>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-noncurrentversiontransition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                noncurrent_version_transition_property = s3_mixins.CfnBucketPropsMixin.NoncurrentVersionTransitionProperty(
                    newer_noncurrent_versions=123,
                    storage_class="storageClass",
                    transition_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__143fab7f77f06aa28d069fd0eb1f9c334d256a6ad651786b90396624cf1f67cf)
                check_type(argname="argument newer_noncurrent_versions", value=newer_noncurrent_versions, expected_type=type_hints["newer_noncurrent_versions"])
                check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
                check_type(argname="argument transition_in_days", value=transition_in_days, expected_type=type_hints["transition_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if newer_noncurrent_versions is not None:
                self._values["newer_noncurrent_versions"] = newer_noncurrent_versions
            if storage_class is not None:
                self._values["storage_class"] = storage_class
            if transition_in_days is not None:
                self._values["transition_in_days"] = transition_in_days

        @builtins.property
        def newer_noncurrent_versions(self) -> typing.Optional[jsii.Number]:
            '''Specifies how many noncurrent versions Amazon S3 will retain.

            If there are this many more recent noncurrent versions, Amazon S3 will take the associated action. For more information about noncurrent versions, see `Lifecycle configuration elements <https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-noncurrentversiontransition.html#cfn-s3-bucket-noncurrentversiontransition-newernoncurrentversions
            '''
            result = self._values.get("newer_noncurrent_versions")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage_class(self) -> typing.Optional[builtins.str]:
            '''The class of storage used to store the object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-noncurrentversiontransition.html#cfn-s3-bucket-noncurrentversiontransition-storageclass
            '''
            result = self._values.get("storage_class")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transition_in_days(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of days an object is noncurrent before Amazon S3 can perform the associated action.

            For information about the noncurrent days calculations, see `How Amazon S3 Calculates How Long an Object Has Been Noncurrent <https://docs.aws.amazon.com/AmazonS3/latest/dev/intro-lifecycle-rules.html#non-current-days-calculations>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-noncurrentversiontransition.html#cfn-s3-bucket-noncurrentversiontransition-transitionindays
            '''
            result = self._values.get("transition_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NoncurrentVersionTransitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.NotificationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_bridge_configuration": "eventBridgeConfiguration",
            "lambda_configurations": "lambdaConfigurations",
            "queue_configurations": "queueConfigurations",
            "topic_configurations": "topicConfigurations",
        },
    )
    class NotificationConfigurationProperty:
        def __init__(
            self,
            *,
            event_bridge_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.EventBridgeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.LambdaConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            queue_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.QueueConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            topic_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TopicConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes the notification configuration for an Amazon S3 bucket.

            .. epigraph::

               If you create the target resource and related permissions in the same template, you might have a circular dependency.

               For example, you might use the ``AWS::Lambda::Permission`` resource to grant the bucket permission to invoke an AWS Lambda function. However, AWS CloudFormation can't create the bucket until the bucket has permission to invoke the function ( AWS CloudFormation checks whether the bucket can invoke the function). If you're using Refs to pass the bucket name, this leads to a circular dependency.

               To avoid this dependency, you can create all resources without specifying the notification configuration. Then, update the stack with a notification configuration.

               For more information on permissions, see `AWS::Lambda::Permission <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html>`_ and `Granting Permissions to Publish Event Notification Messages to a Destination <https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html#grant-destinations-permissions-to-s3>`_ .

            :param event_bridge_configuration: Enables delivery of events to Amazon EventBridge.
            :param lambda_configurations: Describes the AWS Lambda functions to invoke and the events for which to invoke them.
            :param queue_configurations: The Amazon Simple Queue Service queues to publish messages to and the events for which to publish messages.
            :param topic_configurations: The topic to which notifications are sent and the events for which notifications are generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                notification_configuration_property = s3_mixins.CfnBucketPropsMixin.NotificationConfigurationProperty(
                    event_bridge_configuration=s3_mixins.CfnBucketPropsMixin.EventBridgeConfigurationProperty(
                        event_bridge_enabled=False
                    ),
                    lambda_configurations=[s3_mixins.CfnBucketPropsMixin.LambdaConfigurationProperty(
                        event="event",
                        filter=s3_mixins.CfnBucketPropsMixin.NotificationFilterProperty(
                            s3_key=s3_mixins.CfnBucketPropsMixin.S3KeyFilterProperty(
                                rules=[s3_mixins.CfnBucketPropsMixin.FilterRuleProperty(
                                    name="name",
                                    value="value"
                                )]
                            )
                        ),
                        function="function"
                    )],
                    queue_configurations=[s3_mixins.CfnBucketPropsMixin.QueueConfigurationProperty(
                        event="event",
                        filter=s3_mixins.CfnBucketPropsMixin.NotificationFilterProperty(
                            s3_key=s3_mixins.CfnBucketPropsMixin.S3KeyFilterProperty(
                                rules=[s3_mixins.CfnBucketPropsMixin.FilterRuleProperty(
                                    name="name",
                                    value="value"
                                )]
                            )
                        ),
                        queue="queue"
                    )],
                    topic_configurations=[s3_mixins.CfnBucketPropsMixin.TopicConfigurationProperty(
                        event="event",
                        filter=s3_mixins.CfnBucketPropsMixin.NotificationFilterProperty(
                            s3_key=s3_mixins.CfnBucketPropsMixin.S3KeyFilterProperty(
                                rules=[s3_mixins.CfnBucketPropsMixin.FilterRuleProperty(
                                    name="name",
                                    value="value"
                                )]
                            )
                        ),
                        topic="topic"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5045bfcec644eb298a0d4b381b04b53eac85a884ec14ee9c080d4d30bf0be499)
                check_type(argname="argument event_bridge_configuration", value=event_bridge_configuration, expected_type=type_hints["event_bridge_configuration"])
                check_type(argname="argument lambda_configurations", value=lambda_configurations, expected_type=type_hints["lambda_configurations"])
                check_type(argname="argument queue_configurations", value=queue_configurations, expected_type=type_hints["queue_configurations"])
                check_type(argname="argument topic_configurations", value=topic_configurations, expected_type=type_hints["topic_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_bridge_configuration is not None:
                self._values["event_bridge_configuration"] = event_bridge_configuration
            if lambda_configurations is not None:
                self._values["lambda_configurations"] = lambda_configurations
            if queue_configurations is not None:
                self._values["queue_configurations"] = queue_configurations
            if topic_configurations is not None:
                self._values["topic_configurations"] = topic_configurations

        @builtins.property
        def event_bridge_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.EventBridgeConfigurationProperty"]]:
            '''Enables delivery of events to Amazon EventBridge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration.html#cfn-s3-bucket-notificationconfiguration-eventbridgeconfiguration
            '''
            result = self._values.get("event_bridge_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.EventBridgeConfigurationProperty"]], result)

        @builtins.property
        def lambda_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.LambdaConfigurationProperty"]]]]:
            '''Describes the AWS Lambda functions to invoke and the events for which to invoke them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration.html#cfn-s3-bucket-notificationconfiguration-lambdaconfigurations
            '''
            result = self._values.get("lambda_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.LambdaConfigurationProperty"]]]], result)

        @builtins.property
        def queue_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.QueueConfigurationProperty"]]]]:
            '''The Amazon Simple Queue Service queues to publish messages to and the events for which to publish messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration.html#cfn-s3-bucket-notificationconfiguration-queueconfigurations
            '''
            result = self._values.get("queue_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.QueueConfigurationProperty"]]]], result)

        @builtins.property
        def topic_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TopicConfigurationProperty"]]]]:
            '''The topic to which notifications are sent and the events for which notifications are generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration.html#cfn-s3-bucket-notificationconfiguration-topicconfigurations
            '''
            result = self._values.get("topic_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TopicConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.NotificationFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_key": "s3Key"},
    )
    class NotificationFilterProperty:
        def __init__(
            self,
            *,
            s3_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.S3KeyFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies object key name filtering rules.

            For information about key name filtering, see `Configuring event notifications using object key name filtering <https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html>`_ in the *Amazon S3 User Guide* .

            :param s3_key: A container for object key name prefix and suffix filtering rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                notification_filter_property = s3_mixins.CfnBucketPropsMixin.NotificationFilterProperty(
                    s3_key=s3_mixins.CfnBucketPropsMixin.S3KeyFilterProperty(
                        rules=[s3_mixins.CfnBucketPropsMixin.FilterRuleProperty(
                            name="name",
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d4687f94f101195a94936e1dedb83e8b9be8ff3c14adadf77c06058a115fac5)
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_key is not None:
                self._values["s3_key"] = s3_key

        @builtins.property
        def s3_key(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.S3KeyFilterProperty"]]:
            '''A container for object key name prefix and suffix filtering rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationfilter.html#cfn-s3-bucket-notificationfilter-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.S3KeyFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ObjectLockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"object_lock_enabled": "objectLockEnabled", "rule": "rule"},
    )
    class ObjectLockConfigurationProperty:
        def __init__(
            self,
            *,
            object_lock_enabled: typing.Optional[builtins.str] = None,
            rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ObjectLockRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Places an Object Lock configuration on the specified bucket.

            The rule specified in the Object Lock configuration will be applied by default to every new object placed in the specified bucket. For more information, see `Locking Objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock.html>`_ .

            :param object_lock_enabled: Indicates whether this bucket has an Object Lock configuration enabled. Enable ``ObjectLockEnabled`` when you apply ``ObjectLockConfiguration`` to a bucket.
            :param rule: Specifies the Object Lock rule for the specified object. Enable this rule when you apply ``ObjectLockConfiguration`` to a bucket. If Object Lock is turned on, bucket settings require both ``Mode`` and a period of either ``Days`` or ``Years`` . You cannot specify ``Days`` and ``Years`` at the same time. For more information, see `ObjectLockRule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockrule.html>`_ and `DefaultRetention <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                object_lock_configuration_property = s3_mixins.CfnBucketPropsMixin.ObjectLockConfigurationProperty(
                    object_lock_enabled="objectLockEnabled",
                    rule=s3_mixins.CfnBucketPropsMixin.ObjectLockRuleProperty(
                        default_retention=s3_mixins.CfnBucketPropsMixin.DefaultRetentionProperty(
                            days=123,
                            mode="mode",
                            years=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56d5076cf09478eda5c5d158a709090eddb243eae330d3d8624cd5eb30437776)
                check_type(argname="argument object_lock_enabled", value=object_lock_enabled, expected_type=type_hints["object_lock_enabled"])
                check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object_lock_enabled is not None:
                self._values["object_lock_enabled"] = object_lock_enabled
            if rule is not None:
                self._values["rule"] = rule

        @builtins.property
        def object_lock_enabled(self) -> typing.Optional[builtins.str]:
            '''Indicates whether this bucket has an Object Lock configuration enabled.

            Enable ``ObjectLockEnabled`` when you apply ``ObjectLockConfiguration`` to a bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockconfiguration.html#cfn-s3-bucket-objectlockconfiguration-objectlockenabled
            '''
            result = self._values.get("object_lock_enabled")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ObjectLockRuleProperty"]]:
            '''Specifies the Object Lock rule for the specified object.

            Enable this rule when you apply ``ObjectLockConfiguration`` to a bucket. If Object Lock is turned on, bucket settings require both ``Mode`` and a period of either ``Days`` or ``Years`` . You cannot specify ``Days`` and ``Years`` at the same time. For more information, see `ObjectLockRule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockrule.html>`_ and `DefaultRetention <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockconfiguration.html#cfn-s3-bucket-objectlockconfiguration-rule
            '''
            result = self._values.get("rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ObjectLockRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectLockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ObjectLockRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"default_retention": "defaultRetention"},
    )
    class ObjectLockRuleProperty:
        def __init__(
            self,
            *,
            default_retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.DefaultRetentionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the Object Lock rule for the specified object.

            Enable the this rule when you apply ``ObjectLockConfiguration`` to a bucket.

            :param default_retention: The default Object Lock retention mode and period that you want to apply to new objects placed in the specified bucket. If Object Lock is turned on, bucket settings require both ``Mode`` and a period of either ``Days`` or ``Years`` . You cannot specify ``Days`` and ``Years`` at the same time. For more information about allowable values for mode and period, see `DefaultRetention <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                object_lock_rule_property = s3_mixins.CfnBucketPropsMixin.ObjectLockRuleProperty(
                    default_retention=s3_mixins.CfnBucketPropsMixin.DefaultRetentionProperty(
                        days=123,
                        mode="mode",
                        years=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__241ad46ae1d861988a0a5a75d858471ac8dbcefefcd8d5fa15ac04a6c1853f86)
                check_type(argname="argument default_retention", value=default_retention, expected_type=type_hints["default_retention"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_retention is not None:
                self._values["default_retention"] = default_retention

        @builtins.property
        def default_retention(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DefaultRetentionProperty"]]:
            '''The default Object Lock retention mode and period that you want to apply to new objects placed in the specified bucket.

            If Object Lock is turned on, bucket settings require both ``Mode`` and a period of either ``Days`` or ``Years`` . You cannot specify ``Days`` and ``Years`` at the same time. For more information about allowable values for mode and period, see `DefaultRetention <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockrule.html#cfn-s3-bucket-objectlockrule-defaultretention
            '''
            result = self._values.get("default_retention")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DefaultRetentionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectLockRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.OwnershipControlsProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class OwnershipControlsProperty:
        def __init__(
            self,
            *,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.OwnershipControlsRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies the container element for Object Ownership rules.

            S3 Object Ownership is an Amazon S3 bucket-level setting that you can use to disable access control lists (ACLs) and take ownership of every object in your bucket, simplifying access management for data stored in Amazon S3. For more information, see `Controlling ownership of objects and disabling ACLs <https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html>`_ in the *Amazon S3 User Guide* .

            :param rules: Specifies the container element for Object Ownership rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrols.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                ownership_controls_property = s3_mixins.CfnBucketPropsMixin.OwnershipControlsProperty(
                    rules=[s3_mixins.CfnBucketPropsMixin.OwnershipControlsRuleProperty(
                        object_ownership="objectOwnership"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4468aa126ef70234daae44a533c6a5421bfd6d1b4bcf7b5c6139a9bcee1a2d2)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.OwnershipControlsRuleProperty"]]]]:
            '''Specifies the container element for Object Ownership rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrols.html#cfn-s3-bucket-ownershipcontrols-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.OwnershipControlsRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OwnershipControlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.OwnershipControlsRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"object_ownership": "objectOwnership"},
    )
    class OwnershipControlsRuleProperty:
        def __init__(
            self,
            *,
            object_ownership: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an Object Ownership rule.

            S3 Object Ownership is an Amazon S3 bucket-level setting that you can use to disable access control lists (ACLs) and take ownership of every object in your bucket, simplifying access management for data stored in Amazon S3. For more information, see `Controlling ownership of objects and disabling ACLs <https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html>`_ in the *Amazon S3 User Guide* .

            :param object_ownership: Specifies an object ownership rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrolsrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                ownership_controls_rule_property = s3_mixins.CfnBucketPropsMixin.OwnershipControlsRuleProperty(
                    object_ownership="objectOwnership"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9840834cd9416dd0888a22fde8fc873a02ffddfdfefe24e421b76953f3167ced)
                check_type(argname="argument object_ownership", value=object_ownership, expected_type=type_hints["object_ownership"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object_ownership is not None:
                self._values["object_ownership"] = object_ownership

        @builtins.property
        def object_ownership(self) -> typing.Optional[builtins.str]:
            '''Specifies an object ownership rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrolsrule.html#cfn-s3-bucket-ownershipcontrolsrule-objectownership
            '''
            result = self._values.get("object_ownership")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OwnershipControlsRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.PartitionedPrefixProperty",
        jsii_struct_bases=[],
        name_mapping={"partition_date_source": "partitionDateSource"},
    )
    class PartitionedPrefixProperty:
        def __init__(
            self,
            *,
            partition_date_source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Amazon S3 keys for log objects are partitioned in the following format:.

            ``[DestinationPrefix][SourceAccountId]/[SourceRegion]/[SourceBucket]/[YYYY]/[MM]/[DD]/[YYYY]-[MM]-[DD]-[hh]-[mm]-[ss]-[UniqueString]``

            PartitionedPrefix defaults to EventTime delivery when server access logs are delivered.

            :param partition_date_source: Specifies the partition date source for the partitioned prefix. ``PartitionDateSource`` can be ``EventTime`` or ``DeliveryTime`` . For ``DeliveryTime`` , the time in the log file names corresponds to the delivery time for the log files. For ``EventTime`` , The logs delivered are for a specific day only. The year, month, and day correspond to the day on which the event occurred, and the hour, minutes and seconds are set to 00 in the key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-partitionedprefix.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                partitioned_prefix_property = s3_mixins.CfnBucketPropsMixin.PartitionedPrefixProperty(
                    partition_date_source="partitionDateSource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__716f4398f43d66c6f8931005b60eb69a9bf9d2df6dfeca6bb640fea1e93c198a)
                check_type(argname="argument partition_date_source", value=partition_date_source, expected_type=type_hints["partition_date_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if partition_date_source is not None:
                self._values["partition_date_source"] = partition_date_source

        @builtins.property
        def partition_date_source(self) -> typing.Optional[builtins.str]:
            '''Specifies the partition date source for the partitioned prefix. ``PartitionDateSource`` can be ``EventTime`` or ``DeliveryTime`` .

            For ``DeliveryTime`` , the time in the log file names corresponds to the delivery time for the log files.

            For ``EventTime`` , The logs delivered are for a specific day only. The year, month, and day correspond to the day on which the event occurred, and the hour, minutes and seconds are set to 00 in the key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-partitionedprefix.html#cfn-s3-bucket-partitionedprefix-partitiondatesource
            '''
            result = self._values.get("partition_date_source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PartitionedPrefixProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.PublicAccessBlockConfigurationProperty",
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
            '''The PublicAccessBlock configuration that you want to apply to this Amazon S3 bucket.

            You can enable the configuration options in any combination. Bucket-level settings work alongside account-level settings (which may inherit from organization-level policies). For more information about when Amazon S3 considers a bucket or object public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .

            :param block_public_acls: Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and objects in this bucket. Setting this element to ``TRUE`` causes the following behavior: - PUT Bucket ACL and PUT Object ACL calls fail if the specified ACL is public. - PUT Object calls fail if the request includes a public ACL. - PUT Bucket calls fail if the request includes a public ACL. Enabling this setting doesn't affect existing policies or ACLs.
            :param block_public_policy: Specifies whether Amazon S3 should block public bucket policies for this bucket. Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access. Enabling this setting doesn't affect existing bucket policies.
            :param ignore_public_acls: Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this bucket. Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on this bucket and objects in this bucket. Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.
            :param restrict_public_buckets: Specifies whether Amazon S3 should restrict public bucket policies for this bucket. Setting this element to ``TRUE`` restricts access to this bucket to only AWS service principals and authorized users within this account if the bucket has a public policy. Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                public_access_block_configuration_property = s3_mixins.CfnBucketPropsMixin.PublicAccessBlockConfigurationProperty(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f133492b8537506aa79669270874517e396e3eb1509d9db68fef0ba566067725)
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
            '''Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and objects in this bucket.

            Setting this element to ``TRUE`` causes the following behavior:

            - PUT Bucket ACL and PUT Object ACL calls fail if the specified ACL is public.
            - PUT Object calls fail if the request includes a public ACL.
            - PUT Bucket calls fail if the request includes a public ACL.

            Enabling this setting doesn't affect existing policies or ACLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-blockpublicacls
            '''
            result = self._values.get("block_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def block_public_policy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should block public bucket policies for this bucket.

            Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access.

            Enabling this setting doesn't affect existing bucket policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-blockpublicpolicy
            '''
            result = self._values.get("block_public_policy")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ignore_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this bucket.

            Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on this bucket and objects in this bucket.

            Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-ignorepublicacls
            '''
            result = self._values.get("ignore_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def restrict_public_buckets(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should restrict public bucket policies for this bucket.

            Setting this element to ``TRUE`` restricts access to this bucket to only AWS service principals and authorized users within this account if the bucket has a public policy.

            Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-restrictpublicbuckets
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
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.QueueConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"event": "event", "filter": "filter", "queue": "queue"},
    )
    class QueueConfigurationProperty:
        def __init__(
            self,
            *,
            event: typing.Optional[builtins.str] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.NotificationFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            queue: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration for publishing messages to an Amazon Simple Queue Service (Amazon SQS) queue when Amazon S3 detects specified events.

            :param event: The Amazon S3 bucket event about which you want to publish messages to Amazon SQS. For more information, see `Supported Event Types <https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html>`_ in the *Amazon S3 User Guide* .
            :param filter: The filtering rules that determine which objects trigger notifications. For example, you can create a filter so that Amazon S3 sends notifications only when image files with a ``.jpg`` extension are added to the bucket. For more information, see `Configuring event notifications using object key name filtering <https://docs.aws.amazon.com/AmazonS3/latest/user-guide/notification-how-to-filtering.html>`_ in the *Amazon S3 User Guide* .
            :param queue: The Amazon Resource Name (ARN) of the Amazon SQS queue to which Amazon S3 publishes a message when it detects events of the specified type. FIFO queues are not allowed when enabling an SQS queue as the event notification destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-queueconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                queue_configuration_property = s3_mixins.CfnBucketPropsMixin.QueueConfigurationProperty(
                    event="event",
                    filter=s3_mixins.CfnBucketPropsMixin.NotificationFilterProperty(
                        s3_key=s3_mixins.CfnBucketPropsMixin.S3KeyFilterProperty(
                            rules=[s3_mixins.CfnBucketPropsMixin.FilterRuleProperty(
                                name="name",
                                value="value"
                            )]
                        )
                    ),
                    queue="queue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2577f0dd09ad20794bf3f684461355005bde4946142ed53b0c3b35427792ad3)
                check_type(argname="argument event", value=event, expected_type=type_hints["event"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event is not None:
                self._values["event"] = event
            if filter is not None:
                self._values["filter"] = filter
            if queue is not None:
                self._values["queue"] = queue

        @builtins.property
        def event(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket event about which you want to publish messages to Amazon SQS.

            For more information, see `Supported Event Types <https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-queueconfiguration.html#cfn-s3-bucket-queueconfiguration-event
            '''
            result = self._values.get("event")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NotificationFilterProperty"]]:
            '''The filtering rules that determine which objects trigger notifications.

            For example, you can create a filter so that Amazon S3 sends notifications only when image files with a ``.jpg`` extension are added to the bucket. For more information, see `Configuring event notifications using object key name filtering <https://docs.aws.amazon.com/AmazonS3/latest/user-guide/notification-how-to-filtering.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-queueconfiguration.html#cfn-s3-bucket-queueconfiguration-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NotificationFilterProperty"]], result)

        @builtins.property
        def queue(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SQS queue to which Amazon S3 publishes a message when it detects events of the specified type.

            FIFO queues are not allowed when enabling an SQS queue as the event notification destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-queueconfiguration.html#cfn-s3-bucket-queueconfiguration-queue
            '''
            result = self._values.get("queue")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueueConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.RecordExpirationProperty",
        jsii_struct_bases=[],
        name_mapping={"days": "days", "expiration": "expiration"},
    )
    class RecordExpirationProperty:
        def __init__(
            self,
            *,
            days: typing.Optional[jsii.Number] = None,
            expiration: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The journal table record expiration settings for a journal table in an S3 Metadata configuration.

            :param days: If you enable journal table record expiration, you can set the number of days to retain your journal table records. Journal table records must be retained for a minimum of 7 days. To set this value, specify any whole number from ``7`` to ``2147483647`` . For example, to retain your journal table records for one year, set this value to ``365`` .
            :param expiration: Specifies whether journal table record expiration is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-recordexpiration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                record_expiration_property = s3_mixins.CfnBucketPropsMixin.RecordExpirationProperty(
                    days=123,
                    expiration="expiration"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__437af7b76608d9657210b67c2ca3e8a1229d4da83769266766df90dd15931dda)
                check_type(argname="argument days", value=days, expected_type=type_hints["days"])
                check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days is not None:
                self._values["days"] = days
            if expiration is not None:
                self._values["expiration"] = expiration

        @builtins.property
        def days(self) -> typing.Optional[jsii.Number]:
            '''If you enable journal table record expiration, you can set the number of days to retain your journal table records.

            Journal table records must be retained for a minimum of 7 days. To set this value, specify any whole number from ``7`` to ``2147483647`` . For example, to retain your journal table records for one year, set this value to ``365`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-recordexpiration.html#cfn-s3-bucket-recordexpiration-days
            '''
            result = self._values.get("days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expiration(self) -> typing.Optional[builtins.str]:
            '''Specifies whether journal table record expiration is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-recordexpiration.html#cfn-s3-bucket-recordexpiration-expiration
            '''
            result = self._values.get("expiration")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordExpirationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.RedirectAllRequestsToProperty",
        jsii_struct_bases=[],
        name_mapping={"host_name": "hostName", "protocol": "protocol"},
    )
    class RedirectAllRequestsToProperty:
        def __init__(
            self,
            *,
            host_name: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the redirect behavior of all requests to a website endpoint of an Amazon S3 bucket.

            :param host_name: Name of the host where requests are redirected.
            :param protocol: Protocol to use when redirecting requests. The default is the protocol that is used in the original request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-redirectallrequeststo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                redirect_all_requests_to_property = s3_mixins.CfnBucketPropsMixin.RedirectAllRequestsToProperty(
                    host_name="hostName",
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__987a2fd463fd3ef55b6f4fd173cb15810ebeb370aaac679aabdbfcf87cffdb3a)
                check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if host_name is not None:
                self._values["host_name"] = host_name
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def host_name(self) -> typing.Optional[builtins.str]:
            '''Name of the host where requests are redirected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-redirectallrequeststo.html#cfn-s3-bucket-redirectallrequeststo-hostname
            '''
            result = self._values.get("host_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''Protocol to use when redirecting requests.

            The default is the protocol that is used in the original request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-redirectallrequeststo.html#cfn-s3-bucket-redirectallrequeststo-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectAllRequestsToProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.RedirectRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "host_name": "hostName",
            "http_redirect_code": "httpRedirectCode",
            "protocol": "protocol",
            "replace_key_prefix_with": "replaceKeyPrefixWith",
            "replace_key_with": "replaceKeyWith",
        },
    )
    class RedirectRuleProperty:
        def __init__(
            self,
            *,
            host_name: typing.Optional[builtins.str] = None,
            http_redirect_code: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            replace_key_prefix_with: typing.Optional[builtins.str] = None,
            replace_key_with: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies how requests are redirected.

            In the event of an error, you can specify a different error code to return.

            :param host_name: The host name to use in the redirect request.
            :param http_redirect_code: The HTTP redirect code to use on the response. Not required if one of the siblings is present.
            :param protocol: Protocol to use when redirecting requests. The default is the protocol that is used in the original request.
            :param replace_key_prefix_with: The object key prefix to use in the redirect request. For example, to redirect requests for all pages with prefix ``docs/`` (objects in the ``docs/`` folder) to ``documents/`` , you can set a condition block with ``KeyPrefixEquals`` set to ``docs/`` and in the Redirect set ``ReplaceKeyPrefixWith`` to ``/documents`` . Not required if one of the siblings is present. Can be present only if ``ReplaceKeyWith`` is not provided. .. epigraph:: Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .
            :param replace_key_with: The specific object key to use in the redirect request. For example, redirect request to ``error.html`` . Not required if one of the siblings is present. Can be present only if ``ReplaceKeyPrefixWith`` is not provided. .. epigraph:: Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-redirectrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                redirect_rule_property = s3_mixins.CfnBucketPropsMixin.RedirectRuleProperty(
                    host_name="hostName",
                    http_redirect_code="httpRedirectCode",
                    protocol="protocol",
                    replace_key_prefix_with="replaceKeyPrefixWith",
                    replace_key_with="replaceKeyWith"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5c27085142d05415b4057e4b02b618de9c96f1c4cadfd659dc0907ba2f4b7800)
                check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
                check_type(argname="argument http_redirect_code", value=http_redirect_code, expected_type=type_hints["http_redirect_code"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument replace_key_prefix_with", value=replace_key_prefix_with, expected_type=type_hints["replace_key_prefix_with"])
                check_type(argname="argument replace_key_with", value=replace_key_with, expected_type=type_hints["replace_key_with"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if host_name is not None:
                self._values["host_name"] = host_name
            if http_redirect_code is not None:
                self._values["http_redirect_code"] = http_redirect_code
            if protocol is not None:
                self._values["protocol"] = protocol
            if replace_key_prefix_with is not None:
                self._values["replace_key_prefix_with"] = replace_key_prefix_with
            if replace_key_with is not None:
                self._values["replace_key_with"] = replace_key_with

        @builtins.property
        def host_name(self) -> typing.Optional[builtins.str]:
            '''The host name to use in the redirect request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-redirectrule.html#cfn-s3-bucket-redirectrule-hostname
            '''
            result = self._values.get("host_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_redirect_code(self) -> typing.Optional[builtins.str]:
            '''The HTTP redirect code to use on the response.

            Not required if one of the siblings is present.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-redirectrule.html#cfn-s3-bucket-redirectrule-httpredirectcode
            '''
            result = self._values.get("http_redirect_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''Protocol to use when redirecting requests.

            The default is the protocol that is used in the original request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-redirectrule.html#cfn-s3-bucket-redirectrule-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replace_key_prefix_with(self) -> typing.Optional[builtins.str]:
            '''The object key prefix to use in the redirect request.

            For example, to redirect requests for all pages with prefix ``docs/`` (objects in the ``docs/`` folder) to ``documents/`` , you can set a condition block with ``KeyPrefixEquals`` set to ``docs/`` and in the Redirect set ``ReplaceKeyPrefixWith`` to ``/documents`` . Not required if one of the siblings is present. Can be present only if ``ReplaceKeyWith`` is not provided.
            .. epigraph::

               Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-redirectrule.html#cfn-s3-bucket-redirectrule-replacekeyprefixwith
            '''
            result = self._values.get("replace_key_prefix_with")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replace_key_with(self) -> typing.Optional[builtins.str]:
            '''The specific object key to use in the redirect request.

            For example, redirect request to ``error.html`` . Not required if one of the siblings is present. Can be present only if ``ReplaceKeyPrefixWith`` is not provided.
            .. epigraph::

               Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-redirectrule.html#cfn-s3-bucket-redirectrule-replacekeywith
            '''
            result = self._values.get("replace_key_with")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ReplicaModificationsProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class ReplicaModificationsProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''A filter that you can specify for selection for modifications on replicas.

            :param status: Specifies whether Amazon S3 replicates modifications on replicas. *Allowed values* : ``Enabled`` | ``Disabled``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicamodifications.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                replica_modifications_property = s3_mixins.CfnBucketPropsMixin.ReplicaModificationsProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d0fb7be36161dd3091d616351604e55684539eaeea2e7d1fad873443ad2a8d7)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Specifies whether Amazon S3 replicates modifications on replicas.

            *Allowed values* : ``Enabled`` | ``Disabled``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicamodifications.html#cfn-s3-bucket-replicamodifications-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaModificationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ReplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"role": "role", "rules": "rules"},
    )
    class ReplicationConfigurationProperty:
        def __init__(
            self,
            *,
            role: typing.Optional[builtins.str] = None,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ReplicationRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A container for replication rules.

            You can add up to 1,000 rules. The maximum size of a replication configuration is 2 MB. The latest version of the replication configuration XML is V2. For more information about XML V2 replication configurations, see `Replication configuration <https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-add-config.html>`_ in the *Amazon S3 User Guide* .

            :param role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that Amazon S3 assumes when replicating objects. For more information, see `How to Set Up Replication <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-how-setup.html>`_ in the *Amazon S3 User Guide* .
            :param rules: A container for one or more replication rules. A replication configuration must have at least one rule and can contain a maximum of 1,000 rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                replication_configuration_property = s3_mixins.CfnBucketPropsMixin.ReplicationConfigurationProperty(
                    role="role",
                    rules=[s3_mixins.CfnBucketPropsMixin.ReplicationRuleProperty(
                        delete_marker_replication=s3_mixins.CfnBucketPropsMixin.DeleteMarkerReplicationProperty(
                            status="status"
                        ),
                        destination=s3_mixins.CfnBucketPropsMixin.ReplicationDestinationProperty(
                            access_control_translation=s3_mixins.CfnBucketPropsMixin.AccessControlTranslationProperty(
                                owner="owner"
                            ),
                            account="account",
                            bucket="bucket",
                            encryption_configuration=s3_mixins.CfnBucketPropsMixin.EncryptionConfigurationProperty(
                                replica_kms_key_id="replicaKmsKeyId"
                            ),
                            metrics=s3_mixins.CfnBucketPropsMixin.MetricsProperty(
                                event_threshold=s3_mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty(
                                    minutes=123
                                ),
                                status="status"
                            ),
                            replication_time=s3_mixins.CfnBucketPropsMixin.ReplicationTimeProperty(
                                status="status",
                                time=s3_mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty(
                                    minutes=123
                                )
                            ),
                            storage_class="storageClass"
                        ),
                        filter=s3_mixins.CfnBucketPropsMixin.ReplicationRuleFilterProperty(
                            and=s3_mixins.CfnBucketPropsMixin.ReplicationRuleAndOperatorProperty(
                                prefix="prefix",
                                tag_filters=[s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                                    key="key",
                                    value="value"
                                )]
                            ),
                            prefix="prefix",
                            tag_filter=s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                                key="key",
                                value="value"
                            )
                        ),
                        id="id",
                        prefix="prefix",
                        priority=123,
                        source_selection_criteria=s3_mixins.CfnBucketPropsMixin.SourceSelectionCriteriaProperty(
                            replica_modifications=s3_mixins.CfnBucketPropsMixin.ReplicaModificationsProperty(
                                status="status"
                            ),
                            sse_kms_encrypted_objects=s3_mixins.CfnBucketPropsMixin.SseKmsEncryptedObjectsProperty(
                                status="status"
                            )
                        ),
                        status="status"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__befe5f67f40528ec587bd5180f03d3f5f1b18a03b5b7b8ee94bc1ba3ef23faea)
                check_type(argname="argument role", value=role, expected_type=type_hints["role"])
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role is not None:
                self._values["role"] = role
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def role(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that Amazon S3 assumes when replicating objects.

            For more information, see `How to Set Up Replication <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-how-setup.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration.html#cfn-s3-bucket-replicationconfiguration-role
            '''
            result = self._values.get("role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationRuleProperty"]]]]:
            '''A container for one or more replication rules.

            A replication configuration must have at least one rule and can contain a maximum of 1,000 rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration.html#cfn-s3-bucket-replicationconfiguration-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ReplicationDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_control_translation": "accessControlTranslation",
            "account": "account",
            "bucket": "bucket",
            "encryption_configuration": "encryptionConfiguration",
            "metrics": "metrics",
            "replication_time": "replicationTime",
            "storage_class": "storageClass",
        },
    )
    class ReplicationDestinationProperty:
        def __init__(
            self,
            *,
            access_control_translation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.AccessControlTranslationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            account: typing.Optional[builtins.str] = None,
            bucket: typing.Optional[builtins.str] = None,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.MetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            replication_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ReplicationTimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            storage_class: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A container for information about the replication destination and its configurations including enabling the S3 Replication Time Control (S3 RTC).

            :param access_control_translation: Specify this only in a cross-account scenario (where source and destination bucket owners are not the same), and you want to change replica ownership to the AWS account that owns the destination bucket. If this is not specified in the replication configuration, the replicas are owned by same AWS account that owns the source object.
            :param account: Destination bucket owner account ID. In a cross-account scenario, if you direct Amazon S3 to change replica ownership to the AWS account that owns the destination bucket by specifying the ``AccessControlTranslation`` property, this is the account ID of the destination bucket owner. For more information, see `Cross-Region Replication Additional Configuration: Change Replica Owner <https://docs.aws.amazon.com/AmazonS3/latest/dev/crr-change-owner.html>`_ in the *Amazon S3 User Guide* . If you specify the ``AccessControlTranslation`` property, the ``Account`` property is required.
            :param bucket: The Amazon Resource Name (ARN) of the bucket where you want Amazon S3 to store the results.
            :param encryption_configuration: Specifies encryption-related information.
            :param metrics: A container specifying replication metrics-related settings enabling replication metrics and events.
            :param replication_time: A container specifying S3 Replication Time Control (S3 RTC), including whether S3 RTC is enabled and the time when all objects and operations on objects must be replicated. Must be specified together with a ``Metrics`` block.
            :param storage_class: The storage class to use when replicating objects, such as S3 Standard or reduced redundancy. By default, Amazon S3 uses the storage class of the source object to create the object replica. For valid values, see the ``StorageClass`` element of the `PUT Bucket replication <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTreplication.html>`_ action in the *Amazon S3 API Reference* . ``FSX_OPENZFS`` is not an accepted value when replicating objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                replication_destination_property = s3_mixins.CfnBucketPropsMixin.ReplicationDestinationProperty(
                    access_control_translation=s3_mixins.CfnBucketPropsMixin.AccessControlTranslationProperty(
                        owner="owner"
                    ),
                    account="account",
                    bucket="bucket",
                    encryption_configuration=s3_mixins.CfnBucketPropsMixin.EncryptionConfigurationProperty(
                        replica_kms_key_id="replicaKmsKeyId"
                    ),
                    metrics=s3_mixins.CfnBucketPropsMixin.MetricsProperty(
                        event_threshold=s3_mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty(
                            minutes=123
                        ),
                        status="status"
                    ),
                    replication_time=s3_mixins.CfnBucketPropsMixin.ReplicationTimeProperty(
                        status="status",
                        time=s3_mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty(
                            minutes=123
                        )
                    ),
                    storage_class="storageClass"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da263f2ab26142b9ffe7168a134c11b9fcfda13609f5f8b3494f3574505f2834)
                check_type(argname="argument access_control_translation", value=access_control_translation, expected_type=type_hints["access_control_translation"])
                check_type(argname="argument account", value=account, expected_type=type_hints["account"])
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
                check_type(argname="argument replication_time", value=replication_time, expected_type=type_hints["replication_time"])
                check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_control_translation is not None:
                self._values["access_control_translation"] = access_control_translation
            if account is not None:
                self._values["account"] = account
            if bucket is not None:
                self._values["bucket"] = bucket
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if metrics is not None:
                self._values["metrics"] = metrics
            if replication_time is not None:
                self._values["replication_time"] = replication_time
            if storage_class is not None:
                self._values["storage_class"] = storage_class

        @builtins.property
        def access_control_translation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AccessControlTranslationProperty"]]:
            '''Specify this only in a cross-account scenario (where source and destination bucket owners are not the same), and you want to change replica ownership to the AWS account that owns the destination bucket.

            If this is not specified in the replication configuration, the replicas are owned by same AWS account that owns the source object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationdestination.html#cfn-s3-bucket-replicationdestination-accesscontroltranslation
            '''
            result = self._values.get("access_control_translation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AccessControlTranslationProperty"]], result)

        @builtins.property
        def account(self) -> typing.Optional[builtins.str]:
            '''Destination bucket owner account ID.

            In a cross-account scenario, if you direct Amazon S3 to change replica ownership to the AWS account that owns the destination bucket by specifying the ``AccessControlTranslation`` property, this is the account ID of the destination bucket owner. For more information, see `Cross-Region Replication Additional Configuration: Change Replica Owner <https://docs.aws.amazon.com/AmazonS3/latest/dev/crr-change-owner.html>`_ in the *Amazon S3 User Guide* .

            If you specify the ``AccessControlTranslation`` property, the ``Account`` property is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationdestination.html#cfn-s3-bucket-replicationdestination-account
            '''
            result = self._values.get("account")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the bucket where you want Amazon S3 to store the results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationdestination.html#cfn-s3-bucket-replicationdestination-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.EncryptionConfigurationProperty"]]:
            '''Specifies encryption-related information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationdestination.html#cfn-s3-bucket-replicationdestination-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.EncryptionConfigurationProperty"]], result)

        @builtins.property
        def metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetricsProperty"]]:
            '''A container specifying replication metrics-related settings enabling replication metrics and events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationdestination.html#cfn-s3-bucket-replicationdestination-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.MetricsProperty"]], result)

        @builtins.property
        def replication_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationTimeProperty"]]:
            '''A container specifying S3 Replication Time Control (S3 RTC), including whether S3 RTC is enabled and the time when all objects and operations on objects must be replicated.

            Must be specified together with a ``Metrics`` block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationdestination.html#cfn-s3-bucket-replicationdestination-replicationtime
            '''
            result = self._values.get("replication_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationTimeProperty"]], result)

        @builtins.property
        def storage_class(self) -> typing.Optional[builtins.str]:
            '''The storage class to use when replicating objects, such as S3 Standard or reduced redundancy.

            By default, Amazon S3 uses the storage class of the source object to create the object replica.

            For valid values, see the ``StorageClass`` element of the `PUT Bucket replication <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTreplication.html>`_ action in the *Amazon S3 API Reference* .

            ``FSX_OPENZFS`` is not an accepted value when replicating objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationdestination.html#cfn-s3-bucket-replicationdestination-storageclass
            '''
            result = self._values.get("storage_class")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ReplicationRuleAndOperatorProperty",
        jsii_struct_bases=[],
        name_mapping={"prefix": "prefix", "tag_filters": "tagFilters"},
    )
    class ReplicationRuleAndOperatorProperty:
        def __init__(
            self,
            *,
            prefix: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A container for specifying rule filters.

            The filters determine the subset of objects to which the rule applies. This element is required only if you specify more than one filter.

            For example:

            - If you specify both a ``Prefix`` and a ``TagFilter`` , wrap these filters in an ``And`` tag.
            - If you specify a filter based on multiple tags, wrap the ``TagFilter`` elements in an ``And`` tag

            :param prefix: An object key name prefix that identifies the subset of objects to which the rule applies.
            :param tag_filters: An array of tags containing key and value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationruleandoperator.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                replication_rule_and_operator_property = s3_mixins.CfnBucketPropsMixin.ReplicationRuleAndOperatorProperty(
                    prefix="prefix",
                    tag_filters=[s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7434e3092803baa965370f732163b4e4c65222c0a638827b157dd8a1b88219e6)
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument tag_filters", value=tag_filters, expected_type=type_hints["tag_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''An object key name prefix that identifies the subset of objects to which the rule applies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationruleandoperator.html#cfn-s3-bucket-replicationruleandoperator-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]]:
            '''An array of tags containing key and value pairs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationruleandoperator.html#cfn-s3-bucket-replicationruleandoperator-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationRuleAndOperatorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ReplicationRuleFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"and_": "and", "prefix": "prefix", "tag_filter": "tagFilter"},
    )
    class ReplicationRuleFilterProperty:
        def __init__(
            self,
            *,
            and_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ReplicationRuleAndOperatorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            prefix: typing.Optional[builtins.str] = None,
            tag_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A filter that identifies the subset of objects to which the replication rule applies.

            A ``Filter`` must specify exactly one ``Prefix`` , ``TagFilter`` , or an ``And`` child element.

            :param and_: A container for specifying rule filters. The filters determine the subset of objects to which the rule applies. This element is required only if you specify more than one filter. For example: - If you specify both a ``Prefix`` and a ``TagFilter`` , wrap these filters in an ``And`` tag. - If you specify a filter based on multiple tags, wrap the ``TagFilter`` elements in an ``And`` tag.
            :param prefix: An object key name prefix that identifies the subset of objects to which the rule applies. .. epigraph:: Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .
            :param tag_filter: A container for specifying a tag key and value. The rule applies only to objects that have the tag in their tag set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrulefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                replication_rule_filter_property = s3_mixins.CfnBucketPropsMixin.ReplicationRuleFilterProperty(
                    and=s3_mixins.CfnBucketPropsMixin.ReplicationRuleAndOperatorProperty(
                        prefix="prefix",
                        tag_filters=[s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    prefix="prefix",
                    tag_filter=s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                        key="key",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__52f34ced714fa25d22ba8df8ed44c6696ae77900c85cf4a32b3407e8024462c6)
                check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument tag_filter", value=tag_filter, expected_type=type_hints["tag_filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if and_ is not None:
                self._values["and_"] = and_
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag_filter is not None:
                self._values["tag_filter"] = tag_filter

        @builtins.property
        def and_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationRuleAndOperatorProperty"]]:
            '''A container for specifying rule filters.

            The filters determine the subset of objects to which the rule applies. This element is required only if you specify more than one filter. For example:

            - If you specify both a ``Prefix`` and a ``TagFilter`` , wrap these filters in an ``And`` tag.
            - If you specify a filter based on multiple tags, wrap the ``TagFilter`` elements in an ``And`` tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrulefilter.html#cfn-s3-bucket-replicationrulefilter-and
            '''
            result = self._values.get("and_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationRuleAndOperatorProperty"]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''An object key name prefix that identifies the subset of objects to which the rule applies.

            .. epigraph::

               Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrulefilter.html#cfn-s3-bucket-replicationrulefilter-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]:
            '''A container for specifying a tag key and value.

            The rule applies only to objects that have the tag in their tag set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrulefilter.html#cfn-s3-bucket-replicationrulefilter-tagfilter
            '''
            result = self._values.get("tag_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationRuleFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ReplicationRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_marker_replication": "deleteMarkerReplication",
            "destination": "destination",
            "filter": "filter",
            "id": "id",
            "prefix": "prefix",
            "priority": "priority",
            "source_selection_criteria": "sourceSelectionCriteria",
            "status": "status",
        },
    )
    class ReplicationRuleProperty:
        def __init__(
            self,
            *,
            delete_marker_replication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.DeleteMarkerReplicationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ReplicationDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ReplicationRuleFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            id: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
            source_selection_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.SourceSelectionCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies which Amazon S3 objects to replicate and where to store the replicas.

            :param delete_marker_replication: Specifies whether Amazon S3 replicates delete markers. If you specify a ``Filter`` in your replication configuration, you must also include a ``DeleteMarkerReplication`` element. If your ``Filter`` includes a ``Tag`` element, the ``DeleteMarkerReplication`` ``Status`` must be set to Disabled, because Amazon S3 does not support replicating delete markers for tag-based rules. For an example configuration, see `Basic Rule Configuration <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-add-config.html#replication-config-min-rule-config>`_ . For more information about delete marker replication, see `Basic Rule Configuration <https://docs.aws.amazon.com/AmazonS3/latest/dev/delete-marker-replication.html>`_ . .. epigraph:: If you are using an earlier version of the replication configuration, Amazon S3 handles replication of delete markers differently. For more information, see `Backward Compatibility <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-add-config.html#replication-backward-compat-considerations>`_ .
            :param destination: A container for information about the replication destination and its configurations including enabling the S3 Replication Time Control (S3 RTC).
            :param filter: A filter that identifies the subset of objects to which the replication rule applies. A ``Filter`` must specify exactly one ``Prefix`` , ``TagFilter`` , or an ``And`` child element. The use of the filter field indicates that this is a V2 replication configuration. This field isn't supported in a V1 replication configuration. .. epigraph:: V1 replication configuration only supports filtering by key prefix. To filter using a V1 replication configuration, add the ``Prefix`` directly as a child element of the ``Rule`` element.
            :param id: A unique identifier for the rule. The maximum value is 255 characters. If you don't specify a value, AWS CloudFormation generates a random ID. When using a V2 replication configuration this property is capitalized as "ID".
            :param prefix: An object key name prefix that identifies the object or objects to which the rule applies. The maximum prefix length is 1,024 characters. To include all objects in a bucket, specify an empty string. To filter using a V1 replication configuration, add the ``Prefix`` directly as a child element of the ``Rule`` element. .. epigraph:: Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .
            :param priority: The priority indicates which rule has precedence whenever two or more replication rules conflict. Amazon S3 will attempt to replicate objects according to all replication rules. However, if there are two or more rules with the same destination bucket, then objects will be replicated according to the rule with the highest priority. The higher the number, the higher the priority. For more information, see `Replication <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication.html>`_ in the *Amazon S3 User Guide* .
            :param source_selection_criteria: A container that describes additional filters for identifying the source objects that you want to replicate. You can choose to enable or disable the replication of these objects.
            :param status: Specifies whether the rule is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                replication_rule_property = s3_mixins.CfnBucketPropsMixin.ReplicationRuleProperty(
                    delete_marker_replication=s3_mixins.CfnBucketPropsMixin.DeleteMarkerReplicationProperty(
                        status="status"
                    ),
                    destination=s3_mixins.CfnBucketPropsMixin.ReplicationDestinationProperty(
                        access_control_translation=s3_mixins.CfnBucketPropsMixin.AccessControlTranslationProperty(
                            owner="owner"
                        ),
                        account="account",
                        bucket="bucket",
                        encryption_configuration=s3_mixins.CfnBucketPropsMixin.EncryptionConfigurationProperty(
                            replica_kms_key_id="replicaKmsKeyId"
                        ),
                        metrics=s3_mixins.CfnBucketPropsMixin.MetricsProperty(
                            event_threshold=s3_mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty(
                                minutes=123
                            ),
                            status="status"
                        ),
                        replication_time=s3_mixins.CfnBucketPropsMixin.ReplicationTimeProperty(
                            status="status",
                            time=s3_mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty(
                                minutes=123
                            )
                        ),
                        storage_class="storageClass"
                    ),
                    filter=s3_mixins.CfnBucketPropsMixin.ReplicationRuleFilterProperty(
                        and=s3_mixins.CfnBucketPropsMixin.ReplicationRuleAndOperatorProperty(
                            prefix="prefix",
                            tag_filters=[s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                                key="key",
                                value="value"
                            )]
                        ),
                        prefix="prefix",
                        tag_filter=s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                            key="key",
                            value="value"
                        )
                    ),
                    id="id",
                    prefix="prefix",
                    priority=123,
                    source_selection_criteria=s3_mixins.CfnBucketPropsMixin.SourceSelectionCriteriaProperty(
                        replica_modifications=s3_mixins.CfnBucketPropsMixin.ReplicaModificationsProperty(
                            status="status"
                        ),
                        sse_kms_encrypted_objects=s3_mixins.CfnBucketPropsMixin.SseKmsEncryptedObjectsProperty(
                            status="status"
                        )
                    ),
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d01568476cded2d4f766994bf9cdd2577146f6265570d265268aaabb0e4a5b4)
                check_type(argname="argument delete_marker_replication", value=delete_marker_replication, expected_type=type_hints["delete_marker_replication"])
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument source_selection_criteria", value=source_selection_criteria, expected_type=type_hints["source_selection_criteria"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_marker_replication is not None:
                self._values["delete_marker_replication"] = delete_marker_replication
            if destination is not None:
                self._values["destination"] = destination
            if filter is not None:
                self._values["filter"] = filter
            if id is not None:
                self._values["id"] = id
            if prefix is not None:
                self._values["prefix"] = prefix
            if priority is not None:
                self._values["priority"] = priority
            if source_selection_criteria is not None:
                self._values["source_selection_criteria"] = source_selection_criteria
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def delete_marker_replication(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DeleteMarkerReplicationProperty"]]:
            '''Specifies whether Amazon S3 replicates delete markers.

            If you specify a ``Filter`` in your replication configuration, you must also include a ``DeleteMarkerReplication`` element. If your ``Filter`` includes a ``Tag`` element, the ``DeleteMarkerReplication`` ``Status`` must be set to Disabled, because Amazon S3 does not support replicating delete markers for tag-based rules. For an example configuration, see `Basic Rule Configuration <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-add-config.html#replication-config-min-rule-config>`_ .

            For more information about delete marker replication, see `Basic Rule Configuration <https://docs.aws.amazon.com/AmazonS3/latest/dev/delete-marker-replication.html>`_ .
            .. epigraph::

               If you are using an earlier version of the replication configuration, Amazon S3 handles replication of delete markers differently. For more information, see `Backward Compatibility <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication-add-config.html#replication-backward-compat-considerations>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrule.html#cfn-s3-bucket-replicationrule-deletemarkerreplication
            '''
            result = self._values.get("delete_marker_replication")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DeleteMarkerReplicationProperty"]], result)

        @builtins.property
        def destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationDestinationProperty"]]:
            '''A container for information about the replication destination and its configurations including enabling the S3 Replication Time Control (S3 RTC).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrule.html#cfn-s3-bucket-replicationrule-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationDestinationProperty"]], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationRuleFilterProperty"]]:
            '''A filter that identifies the subset of objects to which the replication rule applies.

            A ``Filter`` must specify exactly one ``Prefix`` , ``TagFilter`` , or an ``And`` child element. The use of the filter field indicates that this is a V2 replication configuration. This field isn't supported in a V1 replication configuration.
            .. epigraph::

               V1 replication configuration only supports filtering by key prefix. To filter using a V1 replication configuration, add the ``Prefix`` directly as a child element of the ``Rule`` element.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrule.html#cfn-s3-bucket-replicationrule-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationRuleFilterProperty"]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for the rule.

            The maximum value is 255 characters. If you don't specify a value, AWS CloudFormation generates a random ID. When using a V2 replication configuration this property is capitalized as "ID".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrule.html#cfn-s3-bucket-replicationrule-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''An object key name prefix that identifies the object or objects to which the rule applies.

            The maximum prefix length is 1,024 characters. To include all objects in a bucket, specify an empty string. To filter using a V1 replication configuration, add the ``Prefix`` directly as a child element of the ``Rule`` element.
            .. epigraph::

               Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrule.html#cfn-s3-bucket-replicationrule-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority indicates which rule has precedence whenever two or more replication rules conflict.

            Amazon S3 will attempt to replicate objects according to all replication rules. However, if there are two or more rules with the same destination bucket, then objects will be replicated according to the rule with the highest priority. The higher the number, the higher the priority.

            For more information, see `Replication <https://docs.aws.amazon.com/AmazonS3/latest/dev/replication.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrule.html#cfn-s3-bucket-replicationrule-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def source_selection_criteria(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.SourceSelectionCriteriaProperty"]]:
            '''A container that describes additional filters for identifying the source objects that you want to replicate.

            You can choose to enable or disable the replication of these objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrule.html#cfn-s3-bucket-replicationrule-sourceselectioncriteria
            '''
            result = self._values.get("source_selection_criteria")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.SourceSelectionCriteriaProperty"]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the rule is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrule.html#cfn-s3-bucket-replicationrule-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ReplicationTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status", "time": "time"},
    )
    class ReplicationTimeProperty:
        def __init__(
            self,
            *,
            status: typing.Optional[builtins.str] = None,
            time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ReplicationTimeValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A container specifying S3 Replication Time Control (S3 RTC) related information, including whether S3 RTC is enabled and the time when all objects and operations on objects must be replicated.

            Must be specified together with a ``Metrics`` block.

            :param status: Specifies whether the replication time is enabled.
            :param time: A container specifying the time by which replication should be complete for all objects and operations on objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                replication_time_property = s3_mixins.CfnBucketPropsMixin.ReplicationTimeProperty(
                    status="status",
                    time=s3_mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty(
                        minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed7ae5247a136bad435b59aeb698335e0501ae09c6825fac7c7bc1865d570323)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status
            if time is not None:
                self._values["time"] = time

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the replication time is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtime.html#cfn-s3-bucket-replicationtime-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationTimeValueProperty"]]:
            '''A container specifying the time by which replication should be complete for all objects and operations on objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtime.html#cfn-s3-bucket-replicationtime-time
            '''
            result = self._values.get("time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicationTimeValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty",
        jsii_struct_bases=[],
        name_mapping={"minutes": "minutes"},
    )
    class ReplicationTimeValueProperty:
        def __init__(self, *, minutes: typing.Optional[jsii.Number] = None) -> None:
            '''A container specifying the time value for S3 Replication Time Control (S3 RTC) and replication metrics ``EventThreshold`` .

            :param minutes: Contains an integer specifying time in minutes. Valid value: 15

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtimevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                replication_time_value_property = s3_mixins.CfnBucketPropsMixin.ReplicationTimeValueProperty(
                    minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3297b3a4be64f370a3933ab9cc36a9899b36387ed140ee98ed5fef32c411916)
                check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if minutes is not None:
                self._values["minutes"] = minutes

        @builtins.property
        def minutes(self) -> typing.Optional[jsii.Number]:
            '''Contains an integer specifying time in minutes.

            Valid value: 15

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtimevalue.html#cfn-s3-bucket-replicationtimevalue-minutes
            '''
            result = self._values.get("minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationTimeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.RoutingRuleConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "http_error_code_returned_equals": "httpErrorCodeReturnedEquals",
            "key_prefix_equals": "keyPrefixEquals",
        },
    )
    class RoutingRuleConditionProperty:
        def __init__(
            self,
            *,
            http_error_code_returned_equals: typing.Optional[builtins.str] = None,
            key_prefix_equals: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A container for describing a condition that must be met for the specified redirect to apply.

            For example, 1. If request is for pages in the ``/docs`` folder, redirect to the ``/documents`` folder. 2. If request results in HTTP error 4xx, redirect request to another host where you might process the error.

            :param http_error_code_returned_equals: The HTTP error code when the redirect is applied. In the event of an error, if the error code equals this value, then the specified redirect is applied. Required when parent element ``Condition`` is specified and sibling ``KeyPrefixEquals`` is not specified. If both are specified, then both must be true for the redirect to be applied.
            :param key_prefix_equals: The object key name prefix when the redirect is applied. For example, to redirect requests for ``ExamplePage.html`` , the key prefix will be ``ExamplePage.html`` . To redirect request for all pages with the prefix ``docs/`` , the key prefix will be ``docs/`` , which identifies all objects in the docs/ folder. Required when the parent element ``Condition`` is specified and sibling ``HttpErrorCodeReturnedEquals`` is not specified. If both conditions are specified, both must be true for the redirect to be applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-routingrulecondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                routing_rule_condition_property = s3_mixins.CfnBucketPropsMixin.RoutingRuleConditionProperty(
                    http_error_code_returned_equals="httpErrorCodeReturnedEquals",
                    key_prefix_equals="keyPrefixEquals"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d891944c894ce60fb0c7465c013ff8dfbbe19954e56f81241a08488f8272a76)
                check_type(argname="argument http_error_code_returned_equals", value=http_error_code_returned_equals, expected_type=type_hints["http_error_code_returned_equals"])
                check_type(argname="argument key_prefix_equals", value=key_prefix_equals, expected_type=type_hints["key_prefix_equals"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http_error_code_returned_equals is not None:
                self._values["http_error_code_returned_equals"] = http_error_code_returned_equals
            if key_prefix_equals is not None:
                self._values["key_prefix_equals"] = key_prefix_equals

        @builtins.property
        def http_error_code_returned_equals(self) -> typing.Optional[builtins.str]:
            '''The HTTP error code when the redirect is applied.

            In the event of an error, if the error code equals this value, then the specified redirect is applied.

            Required when parent element ``Condition`` is specified and sibling ``KeyPrefixEquals`` is not specified. If both are specified, then both must be true for the redirect to be applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-routingrulecondition.html#cfn-s3-bucket-routingrulecondition-httperrorcodereturnedequals
            '''
            result = self._values.get("http_error_code_returned_equals")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_prefix_equals(self) -> typing.Optional[builtins.str]:
            '''The object key name prefix when the redirect is applied.

            For example, to redirect requests for ``ExamplePage.html`` , the key prefix will be ``ExamplePage.html`` . To redirect request for all pages with the prefix ``docs/`` , the key prefix will be ``docs/`` , which identifies all objects in the docs/ folder.

            Required when the parent element ``Condition`` is specified and sibling ``HttpErrorCodeReturnedEquals`` is not specified. If both conditions are specified, both must be true for the redirect to be applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-routingrulecondition.html#cfn-s3-bucket-routingrulecondition-keyprefixequals
            '''
            result = self._values.get("key_prefix_equals")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingRuleConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.RoutingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "redirect_rule": "redirectRule",
            "routing_rule_condition": "routingRuleCondition",
        },
    )
    class RoutingRuleProperty:
        def __init__(
            self,
            *,
            redirect_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.RedirectRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            routing_rule_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.RoutingRuleConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the redirect behavior and when a redirect is applied.

            For more information about routing rules, see `Configuring advanced conditional redirects <https://docs.aws.amazon.com/AmazonS3/latest/dev/how-to-page-redirect.html#advanced-conditional-redirects>`_ in the *Amazon S3 User Guide* .

            :param redirect_rule: Container for redirect information. You can redirect requests to another host, to another page, or with another protocol. In the event of an error, you can specify a different error code to return.
            :param routing_rule_condition: A container for describing a condition that must be met for the specified redirect to apply. For example, 1. If request is for pages in the ``/docs`` folder, redirect to the ``/documents`` folder. 2. If request results in HTTP error 4xx, redirect request to another host where you might process the error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-routingrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                routing_rule_property = s3_mixins.CfnBucketPropsMixin.RoutingRuleProperty(
                    redirect_rule=s3_mixins.CfnBucketPropsMixin.RedirectRuleProperty(
                        host_name="hostName",
                        http_redirect_code="httpRedirectCode",
                        protocol="protocol",
                        replace_key_prefix_with="replaceKeyPrefixWith",
                        replace_key_with="replaceKeyWith"
                    ),
                    routing_rule_condition=s3_mixins.CfnBucketPropsMixin.RoutingRuleConditionProperty(
                        http_error_code_returned_equals="httpErrorCodeReturnedEquals",
                        key_prefix_equals="keyPrefixEquals"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a30fea19308d4d38f9edc1a370bf7a799594d986b7c706e04c7dbb3e87f0aa4)
                check_type(argname="argument redirect_rule", value=redirect_rule, expected_type=type_hints["redirect_rule"])
                check_type(argname="argument routing_rule_condition", value=routing_rule_condition, expected_type=type_hints["routing_rule_condition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if redirect_rule is not None:
                self._values["redirect_rule"] = redirect_rule
            if routing_rule_condition is not None:
                self._values["routing_rule_condition"] = routing_rule_condition

        @builtins.property
        def redirect_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RedirectRuleProperty"]]:
            '''Container for redirect information.

            You can redirect requests to another host, to another page, or with another protocol. In the event of an error, you can specify a different error code to return.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-routingrule.html#cfn-s3-bucket-routingrule-redirectrule
            '''
            result = self._values.get("redirect_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RedirectRuleProperty"]], result)

        @builtins.property
        def routing_rule_condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RoutingRuleConditionProperty"]]:
            '''A container for describing a condition that must be met for the specified redirect to apply.

            For example, 1. If request is for pages in the ``/docs`` folder, redirect to the ``/documents`` folder. 2. If request results in HTTP error 4xx, redirect request to another host where you might process the error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-routingrule.html#cfn-s3-bucket-routingrule-routingrulecondition
            '''
            result = self._values.get("routing_rule_condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RoutingRuleConditionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "abort_incomplete_multipart_upload": "abortIncompleteMultipartUpload",
            "expiration_date": "expirationDate",
            "expiration_in_days": "expirationInDays",
            "expired_object_delete_marker": "expiredObjectDeleteMarker",
            "id": "id",
            "noncurrent_version_expiration": "noncurrentVersionExpiration",
            "noncurrent_version_expiration_in_days": "noncurrentVersionExpirationInDays",
            "noncurrent_version_transition": "noncurrentVersionTransition",
            "noncurrent_version_transitions": "noncurrentVersionTransitions",
            "object_size_greater_than": "objectSizeGreaterThan",
            "object_size_less_than": "objectSizeLessThan",
            "prefix": "prefix",
            "status": "status",
            "tag_filters": "tagFilters",
            "transition": "transition",
            "transitions": "transitions",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            abort_incomplete_multipart_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            expiration_date: typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]] = None,
            expiration_in_days: typing.Optional[jsii.Number] = None,
            expired_object_delete_marker: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            id: typing.Optional[builtins.str] = None,
            noncurrent_version_expiration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.NoncurrentVersionExpirationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            noncurrent_version_expiration_in_days: typing.Optional[jsii.Number] = None,
            noncurrent_version_transition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.NoncurrentVersionTransitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            noncurrent_version_transitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.NoncurrentVersionTransitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            object_size_greater_than: typing.Optional[jsii.Number] = None,
            object_size_less_than: typing.Optional[jsii.Number] = None,
            prefix: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            transition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TransitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            transitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.TransitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies lifecycle rules for an Amazon S3 bucket.

            For more information, see `Put Bucket Lifecycle Configuration <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTlifecycle.html>`_ in the *Amazon S3 API Reference* .

            You must specify at least one of the following properties: ``AbortIncompleteMultipartUpload`` , ``ExpirationDate`` , ``ExpirationInDays`` , ``NoncurrentVersionExpirationInDays`` , ``NoncurrentVersionTransition`` , ``NoncurrentVersionTransitions`` , ``Transition`` , or ``Transitions`` .

            :param abort_incomplete_multipart_upload: Specifies a lifecycle rule that stops incomplete multipart uploads to an Amazon S3 bucket.
            :param expiration_date: Indicates when objects are deleted from Amazon S3 and Amazon S3 Glacier. The date value must be in ISO 8601 format. The time is always midnight UTC. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time.
            :param expiration_in_days: Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon S3 Glacier. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time.
            :param expired_object_delete_marker: Indicates whether Amazon S3 will remove a delete marker without any noncurrent versions. If set to true, the delete marker will be removed if there are no noncurrent versions. This cannot be specified with ``ExpirationInDays`` , ``ExpirationDate`` , or ``TagFilters`` .
            :param id: Unique identifier for the rule. The value can't be longer than 255 characters.
            :param noncurrent_version_expiration: Specifies when noncurrent object versions expire. Upon expiration, Amazon S3 permanently deletes the noncurrent object versions. You set this lifecycle configuration action on a bucket that has versioning enabled (or suspended) to request that Amazon S3 delete noncurrent object versions at a specific period in the object's lifetime.
            :param noncurrent_version_expiration_in_days: (Deprecated.) For buckets with versioning enabled (or suspended), specifies the time, in days, between when a new version of the object is uploaded to the bucket and when old versions of the object expire. When object versions expire, Amazon S3 permanently deletes them. If you specify a transition and expiration time, the expiration time must be later than the transition time.
            :param noncurrent_version_transition: (Deprecated.) For buckets with versioning enabled (or suspended), specifies when non-current objects transition to a specified storage class. If you specify a transition and expiration time, the expiration time must be later than the transition time. If you specify this property, don't specify the ``NoncurrentVersionTransitions`` property.
            :param noncurrent_version_transitions: For buckets with versioning enabled (or suspended), one or more transition rules that specify when non-current objects transition to a specified storage class. If you specify a transition and expiration time, the expiration time must be later than the transition time. If you specify this property, don't specify the ``NoncurrentVersionTransition`` property.
            :param object_size_greater_than: Specifies the minimum object size in bytes for this rule to apply to. Objects must be larger than this value in bytes. For more information about size based rules, see `Lifecycle configuration using size-based rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html#lc-size-rules>`_ in the *Amazon S3 User Guide* .
            :param object_size_less_than: Specifies the maximum object size in bytes for this rule to apply to. Objects must be smaller than this value in bytes. For more information about sized based rules, see `Lifecycle configuration using size-based rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html#lc-size-rules>`_ in the *Amazon S3 User Guide* .
            :param prefix: Object key prefix that identifies one or more objects to which this rule applies. .. epigraph:: Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .
            :param status: If ``Enabled`` , the rule is currently being applied. If ``Disabled`` , the rule is not currently being applied.
            :param tag_filters: Tags to use to identify a subset of objects to which the lifecycle rule applies.
            :param transition: (Deprecated.) Specifies when an object transitions to a specified storage class. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. If you specify this property, don't specify the ``Transitions`` property.
            :param transitions: One or more transition rules that specify when an object transitions to a specified storage class. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. If you specify this property, don't specify the ``Transition`` property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                rule_property = s3_mixins.CfnBucketPropsMixin.RuleProperty(
                    abort_incomplete_multipart_upload=s3_mixins.CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty(
                        days_after_initiation=123
                    ),
                    expiration_date=Date(),
                    expiration_in_days=123,
                    expired_object_delete_marker=False,
                    id="id",
                    noncurrent_version_expiration=s3_mixins.CfnBucketPropsMixin.NoncurrentVersionExpirationProperty(
                        newer_noncurrent_versions=123,
                        noncurrent_days=123
                    ),
                    noncurrent_version_expiration_in_days=123,
                    noncurrent_version_transition=s3_mixins.CfnBucketPropsMixin.NoncurrentVersionTransitionProperty(
                        newer_noncurrent_versions=123,
                        storage_class="storageClass",
                        transition_in_days=123
                    ),
                    noncurrent_version_transitions=[s3_mixins.CfnBucketPropsMixin.NoncurrentVersionTransitionProperty(
                        newer_noncurrent_versions=123,
                        storage_class="storageClass",
                        transition_in_days=123
                    )],
                    object_size_greater_than=123,
                    object_size_less_than=123,
                    prefix="prefix",
                    status="status",
                    tag_filters=[s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                        key="key",
                        value="value"
                    )],
                    transition=s3_mixins.CfnBucketPropsMixin.TransitionProperty(
                        storage_class="storageClass",
                        transition_date=Date(),
                        transition_in_days=123
                    ),
                    transitions=[s3_mixins.CfnBucketPropsMixin.TransitionProperty(
                        storage_class="storageClass",
                        transition_date=Date(),
                        transition_in_days=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1204db2e4ba2a692a857f82cbefb3af5841b0f4d5495c7361545d246c04965b0)
                check_type(argname="argument abort_incomplete_multipart_upload", value=abort_incomplete_multipart_upload, expected_type=type_hints["abort_incomplete_multipart_upload"])
                check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
                check_type(argname="argument expiration_in_days", value=expiration_in_days, expected_type=type_hints["expiration_in_days"])
                check_type(argname="argument expired_object_delete_marker", value=expired_object_delete_marker, expected_type=type_hints["expired_object_delete_marker"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument noncurrent_version_expiration", value=noncurrent_version_expiration, expected_type=type_hints["noncurrent_version_expiration"])
                check_type(argname="argument noncurrent_version_expiration_in_days", value=noncurrent_version_expiration_in_days, expected_type=type_hints["noncurrent_version_expiration_in_days"])
                check_type(argname="argument noncurrent_version_transition", value=noncurrent_version_transition, expected_type=type_hints["noncurrent_version_transition"])
                check_type(argname="argument noncurrent_version_transitions", value=noncurrent_version_transitions, expected_type=type_hints["noncurrent_version_transitions"])
                check_type(argname="argument object_size_greater_than", value=object_size_greater_than, expected_type=type_hints["object_size_greater_than"])
                check_type(argname="argument object_size_less_than", value=object_size_less_than, expected_type=type_hints["object_size_less_than"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument tag_filters", value=tag_filters, expected_type=type_hints["tag_filters"])
                check_type(argname="argument transition", value=transition, expected_type=type_hints["transition"])
                check_type(argname="argument transitions", value=transitions, expected_type=type_hints["transitions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if abort_incomplete_multipart_upload is not None:
                self._values["abort_incomplete_multipart_upload"] = abort_incomplete_multipart_upload
            if expiration_date is not None:
                self._values["expiration_date"] = expiration_date
            if expiration_in_days is not None:
                self._values["expiration_in_days"] = expiration_in_days
            if expired_object_delete_marker is not None:
                self._values["expired_object_delete_marker"] = expired_object_delete_marker
            if id is not None:
                self._values["id"] = id
            if noncurrent_version_expiration is not None:
                self._values["noncurrent_version_expiration"] = noncurrent_version_expiration
            if noncurrent_version_expiration_in_days is not None:
                self._values["noncurrent_version_expiration_in_days"] = noncurrent_version_expiration_in_days
            if noncurrent_version_transition is not None:
                self._values["noncurrent_version_transition"] = noncurrent_version_transition
            if noncurrent_version_transitions is not None:
                self._values["noncurrent_version_transitions"] = noncurrent_version_transitions
            if object_size_greater_than is not None:
                self._values["object_size_greater_than"] = object_size_greater_than
            if object_size_less_than is not None:
                self._values["object_size_less_than"] = object_size_less_than
            if prefix is not None:
                self._values["prefix"] = prefix
            if status is not None:
                self._values["status"] = status
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters
            if transition is not None:
                self._values["transition"] = transition
            if transitions is not None:
                self._values["transitions"] = transitions

        @builtins.property
        def abort_incomplete_multipart_upload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty"]]:
            '''Specifies a lifecycle rule that stops incomplete multipart uploads to an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-abortincompletemultipartupload
            '''
            result = self._values.get("abort_incomplete_multipart_upload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty"]], result)

        @builtins.property
        def expiration_date(
            self,
        ) -> typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates when objects are deleted from Amazon S3 and Amazon S3 Glacier.

            The date value must be in ISO 8601 format. The time is always midnight UTC. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-expirationdate
            '''
            result = self._values.get("expiration_date")
            return typing.cast(typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            '''Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon S3 Glacier.

            If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-expirationindays
            '''
            result = self._values.get("expiration_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expired_object_delete_marker(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Amazon S3 will remove a delete marker without any noncurrent versions.

            If set to true, the delete marker will be removed if there are no noncurrent versions. This cannot be specified with ``ExpirationInDays`` , ``ExpirationDate`` , or ``TagFilters`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-expiredobjectdeletemarker
            '''
            result = self._values.get("expired_object_delete_marker")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''Unique identifier for the rule.

            The value can't be longer than 255 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def noncurrent_version_expiration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NoncurrentVersionExpirationProperty"]]:
            '''Specifies when noncurrent object versions expire.

            Upon expiration, Amazon S3 permanently deletes the noncurrent object versions. You set this lifecycle configuration action on a bucket that has versioning enabled (or suspended) to request that Amazon S3 delete noncurrent object versions at a specific period in the object's lifetime.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-noncurrentversionexpiration
            '''
            result = self._values.get("noncurrent_version_expiration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NoncurrentVersionExpirationProperty"]], result)

        @builtins.property
        def noncurrent_version_expiration_in_days(self) -> typing.Optional[jsii.Number]:
            '''(Deprecated.) For buckets with versioning enabled (or suspended), specifies the time, in days, between when a new version of the object is uploaded to the bucket and when old versions of the object expire. When object versions expire, Amazon S3 permanently deletes them. If you specify a transition and expiration time, the expiration time must be later than the transition time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-noncurrentversionexpirationindays
            '''
            result = self._values.get("noncurrent_version_expiration_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def noncurrent_version_transition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NoncurrentVersionTransitionProperty"]]:
            '''(Deprecated.) For buckets with versioning enabled (or suspended), specifies when non-current objects transition to a specified storage class. If you specify a transition and expiration time, the expiration time must be later than the transition time. If you specify this property, don't specify the ``NoncurrentVersionTransitions`` property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-noncurrentversiontransition
            '''
            result = self._values.get("noncurrent_version_transition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NoncurrentVersionTransitionProperty"]], result)

        @builtins.property
        def noncurrent_version_transitions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NoncurrentVersionTransitionProperty"]]]]:
            '''For buckets with versioning enabled (or suspended), one or more transition rules that specify when non-current objects transition to a specified storage class.

            If you specify a transition and expiration time, the expiration time must be later than the transition time. If you specify this property, don't specify the ``NoncurrentVersionTransition`` property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-noncurrentversiontransitions
            '''
            result = self._values.get("noncurrent_version_transitions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NoncurrentVersionTransitionProperty"]]]], result)

        @builtins.property
        def object_size_greater_than(self) -> typing.Optional[jsii.Number]:
            '''Specifies the minimum object size in bytes for this rule to apply to.

            Objects must be larger than this value in bytes. For more information about size based rules, see `Lifecycle configuration using size-based rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html#lc-size-rules>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-objectsizegreaterthan
            '''
            result = self._values.get("object_size_greater_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def object_size_less_than(self) -> typing.Optional[jsii.Number]:
            '''Specifies the maximum object size in bytes for this rule to apply to.

            Objects must be smaller than this value in bytes. For more information about sized based rules, see `Lifecycle configuration using size-based rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-configuration-examples.html#lc-size-rules>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-objectsizelessthan
            '''
            result = self._values.get("object_size_less_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''Object key prefix that identifies one or more objects to which this rule applies.

            .. epigraph::

               Replacement must be made for object keys containing special characters (such as carriage returns) when using XML requests. For more information, see `XML related object key constraints <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html#object-key-xml-related-constraints>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''If ``Enabled`` , the rule is currently being applied.

            If ``Disabled`` , the rule is not currently being applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]]:
            '''Tags to use to identify a subset of objects to which the lifecycle rule applies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TagFilterProperty"]]]], result)

        @builtins.property
        def transition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TransitionProperty"]]:
            '''(Deprecated.) Specifies when an object transitions to a specified storage class. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. If you specify this property, don't specify the ``Transitions`` property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-transition
            '''
            result = self._values.get("transition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TransitionProperty"]], result)

        @builtins.property
        def transitions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TransitionProperty"]]]]:
            '''One or more transition rules that specify when an object transitions to a specified storage class.

            If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. If you specify this property, don't specify the ``Transition`` property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-rule.html#cfn-s3-bucket-rule-transitions
            '''
            result = self._values.get("transitions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.TransitionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.S3KeyFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class S3KeyFilterProperty:
        def __init__(
            self,
            *,
            rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.FilterRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A container for object key name prefix and suffix filtering rules.

            For more information about object key name filtering, see `Configuring event notifications using object key name filtering <https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html>`_ in the *Amazon S3 User Guide* .
            .. epigraph::

               The same type of filter rule cannot be used more than once. For example, you cannot specify two prefix rules.

            :param rules: A list of containers for the key-value pair that defines the criteria for the filter rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-s3keyfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                s3_key_filter_property = s3_mixins.CfnBucketPropsMixin.S3KeyFilterProperty(
                    rules=[s3_mixins.CfnBucketPropsMixin.FilterRuleProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77fdc2f3cfe0b08a9fcd0cf9e56f7af8b2eedb0c818ed0e522b748c2ad5d3dfd)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules is not None:
                self._values["rules"] = rules

        @builtins.property
        def rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.FilterRuleProperty"]]]]:
            '''A list of containers for the key-value pair that defines the criteria for the filter rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-s3keyfilter.html#cfn-s3-bucket-s3keyfilter-rules
            '''
            result = self._values.get("rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.FilterRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.S3TablesDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "table_arn": "tableArn",
            "table_bucket_arn": "tableBucketArn",
            "table_name": "tableName",
            "table_namespace": "tableNamespace",
        },
    )
    class S3TablesDestinationProperty:
        def __init__(
            self,
            *,
            table_arn: typing.Optional[builtins.str] = None,
            table_bucket_arn: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
            table_namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The destination information for a V1 S3 Metadata configuration.

            The destination table bucket must be in the same Region and AWS account as the general purpose bucket. The specified metadata table name must be unique within the ``aws_s3_metadata`` namespace in the destination table bucket.

            :param table_arn: The Amazon Resource Name (ARN) for the metadata table in the metadata table configuration. The specified metadata table name must be unique within the ``aws_s3_metadata`` namespace in the destination table bucket.
            :param table_bucket_arn: The Amazon Resource Name (ARN) for the table bucket that's specified as the destination in the metadata table configuration. The destination table bucket must be in the same Region and AWS account as the general purpose bucket.
            :param table_name: The name for the metadata table in your metadata table configuration. The specified metadata table name must be unique within the ``aws_s3_metadata`` namespace in the destination table bucket.
            :param table_namespace: The table bucket namespace for the metadata table in your metadata table configuration. This value is always ``aws_s3_metadata`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-s3tablesdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                s3_tables_destination_property = s3_mixins.CfnBucketPropsMixin.S3TablesDestinationProperty(
                    table_arn="tableArn",
                    table_bucket_arn="tableBucketArn",
                    table_name="tableName",
                    table_namespace="tableNamespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80b0068e00ceef280e62fdef458ef0e709df19354378f6061115918b75f3e2ac)
                check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
                check_type(argname="argument table_bucket_arn", value=table_bucket_arn, expected_type=type_hints["table_bucket_arn"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument table_namespace", value=table_namespace, expected_type=type_hints["table_namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if table_arn is not None:
                self._values["table_arn"] = table_arn
            if table_bucket_arn is not None:
                self._values["table_bucket_arn"] = table_bucket_arn
            if table_name is not None:
                self._values["table_name"] = table_name
            if table_namespace is not None:
                self._values["table_namespace"] = table_namespace

        @builtins.property
        def table_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the metadata table in the metadata table configuration.

            The specified metadata table name must be unique within the ``aws_s3_metadata`` namespace in the destination table bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-s3tablesdestination.html#cfn-s3-bucket-s3tablesdestination-tablearn
            '''
            result = self._values.get("table_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the table bucket that's specified as the destination in the metadata table configuration.

            The destination table bucket must be in the same Region and AWS account as the general purpose bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-s3tablesdestination.html#cfn-s3-bucket-s3tablesdestination-tablebucketarn
            '''
            result = self._values.get("table_bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name for the metadata table in your metadata table configuration.

            The specified metadata table name must be unique within the ``aws_s3_metadata`` namespace in the destination table bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-s3tablesdestination.html#cfn-s3-bucket-s3tablesdestination-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_namespace(self) -> typing.Optional[builtins.str]:
            '''The table bucket namespace for the metadata table in your metadata table configuration.

            This value is always ``aws_s3_metadata`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-s3tablesdestination.html#cfn-s3-bucket-s3tablesdestination-tablenamespace
            '''
            result = self._values.get("table_namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3TablesDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ServerSideEncryptionByDefaultProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_master_key_id": "kmsMasterKeyId",
            "sse_algorithm": "sseAlgorithm",
        },
    )
    class ServerSideEncryptionByDefaultProperty:
        def __init__(
            self,
            *,
            kms_master_key_id: typing.Optional[builtins.str] = None,
            sse_algorithm: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the default server-side encryption to apply to new objects in the bucket.

            If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied. For more information, see `PutBucketEncryption <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTencryption.html>`_ .
            .. epigraph::

               - *General purpose buckets* - If you don't specify a customer managed key at configuration, Amazon S3 automatically creates an AWS KMS key ( ``aws/s3`` ) in your AWS account the first time that you add an object encrypted with SSE-KMS to a bucket. By default, Amazon S3 uses this KMS key for SSE-KMS.
               - *Directory buckets* - Your SSE-KMS configuration can only support 1 `customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ per directory bucket's lifetime. The `AWS managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ ( ``aws/s3`` ) isn't supported.
               - *Directory buckets* - For directory buckets, there are only two supported options for server-side encryption: SSE-S3 and SSE-KMS.

            :param kms_master_key_id: AWS Key Management Service (KMS) customer managed key ID to use for the default encryption. .. epigraph:: - *General purpose buckets* - This parameter is allowed if and only if ``SSEAlgorithm`` is set to ``aws:kms`` or ``aws:kms:dsse`` . - *Directory buckets* - This parameter is allowed if and only if ``SSEAlgorithm`` is set to ``aws:kms`` . You can specify the key ID, key alias, or the Amazon Resource Name (ARN) of the KMS key. - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` - Key Alias: ``alias/alias-name`` If you are using encryption with cross-account or AWS service operations, you must use a fully qualified KMS key ARN. For more information, see `Using encryption for cross-account operations <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html#bucket-encryption-update-bucket-policy>`_ . .. epigraph:: - *General purpose buckets* - If you're specifying a customer managed KMS key, we recommend using a fully qualified KMS key ARN. If you use a KMS key alias instead, then AWS resolves the key within the requester’s account. This behavior can result in data that's encrypted with a KMS key that belongs to the requester, and not the bucket owner. Also, if you use a key ID, you can run into a LogDestination undeliverable error when creating a VPC flow log. - *Directory buckets* - When you specify an `AWS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ for encryption in your directory bucket, only use the key ID or key ARN. The key alias format of the KMS key isn't supported. > Amazon S3 only supports symmetric encryption KMS keys. For more information, see `Asymmetric keys in AWS KMS <https://docs.aws.amazon.com//kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .
            :param sse_algorithm: Server-side encryption algorithm to use for the default encryption. .. epigraph:: For directory buckets, there are only two supported values for server-side encryption: ``AES256`` and ``aws:kms`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                server_side_encryption_by_default_property = s3_mixins.CfnBucketPropsMixin.ServerSideEncryptionByDefaultProperty(
                    kms_master_key_id="kmsMasterKeyId",
                    sse_algorithm="sseAlgorithm"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f63e82f3d697140d3a8cc022f88b1acc947b18f43fde26e9f1184facbed5baef)
                check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
                check_type(argname="argument sse_algorithm", value=sse_algorithm, expected_type=type_hints["sse_algorithm"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_master_key_id is not None:
                self._values["kms_master_key_id"] = kms_master_key_id
            if sse_algorithm is not None:
                self._values["sse_algorithm"] = sse_algorithm

        @builtins.property
        def kms_master_key_id(self) -> typing.Optional[builtins.str]:
            '''AWS Key Management Service (KMS) customer managed key ID to use for the default encryption.

            .. epigraph::

               - *General purpose buckets* - This parameter is allowed if and only if ``SSEAlgorithm`` is set to ``aws:kms`` or ``aws:kms:dsse`` .
               - *Directory buckets* - This parameter is allowed if and only if ``SSEAlgorithm`` is set to ``aws:kms`` .

            You can specify the key ID, key alias, or the Amazon Resource Name (ARN) of the KMS key.

            - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab``
            - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab``
            - Key Alias: ``alias/alias-name``

            If you are using encryption with cross-account or AWS service operations, you must use a fully qualified KMS key ARN. For more information, see `Using encryption for cross-account operations <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html#bucket-encryption-update-bucket-policy>`_ .
            .. epigraph::

               - *General purpose buckets* - If you're specifying a customer managed KMS key, we recommend using a fully qualified KMS key ARN. If you use a KMS key alias instead, then AWS  resolves the key within the requester’s account. This behavior can result in data that's encrypted with a KMS key that belongs to the requester, and not the bucket owner. Also, if you use a key ID, you can run into a LogDestination undeliverable error when creating a VPC flow log.
               - *Directory buckets* - When you specify an `AWS  customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ for encryption in your directory bucket, only use the key ID or key ARN. The key alias format of the KMS key isn't supported. > Amazon S3 only supports symmetric encryption KMS keys. For more information, see `Asymmetric keys in AWS KMS <https://docs.aws.amazon.com//kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html#cfn-s3-bucket-serversideencryptionbydefault-kmsmasterkeyid
            '''
            result = self._values.get("kms_master_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sse_algorithm(self) -> typing.Optional[builtins.str]:
            '''Server-side encryption algorithm to use for the default encryption.

            .. epigraph::

               For directory buckets, there are only two supported values for server-side encryption: ``AES256`` and ``aws:kms`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html#cfn-s3-bucket-serversideencryptionbydefault-ssealgorithm
            '''
            result = self._values.get("sse_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionByDefaultProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.ServerSideEncryptionRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "blocked_encryption_types": "blockedEncryptionTypes",
            "bucket_key_enabled": "bucketKeyEnabled",
            "server_side_encryption_by_default": "serverSideEncryptionByDefault",
        },
    )
    class ServerSideEncryptionRuleProperty:
        def __init__(
            self,
            *,
            blocked_encryption_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.BlockedEncryptionTypesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            bucket_key_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            server_side_encryption_by_default: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ServerSideEncryptionByDefaultProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the default server-side encryption configuration.

            .. epigraph::

               - *General purpose buckets* - If you're specifying a customer managed KMS key, we recommend using a fully qualified KMS key ARN. If you use a KMS key alias instead, then AWS  resolves the key within the requester’s account. This behavior can result in data that's encrypted with a KMS key that belongs to the requester, and not the bucket owner.
               - *Directory buckets* - When you specify an `AWS  customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ for encryption in your directory bucket, only use the key ID or key ARN. The key alias format of the KMS key isn't supported.

            :param blocked_encryption_types: A bucket-level setting for Amazon S3 general purpose buckets used to prevent the upload of new objects encrypted with the specified server-side encryption type. For example, blocking an encryption type will block ``PutObject`` , ``CopyObject`` , ``PostObject`` , multipart upload, and replication requests to the bucket for objects with the specified encryption type. However, you can continue to read and list any pre-existing objects already encrypted with the specified encryption type. For more information, see `Blocking or unblocking SSE-C for a general purpose bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/blocking-unblocking-s3-c-encryption-gpb.html>`_ . .. epigraph:: Currently, this parameter only supports blocking or unblocking server-side encryption with customer-provided keys (SSE-C). For more information about SSE-C, see `Using server-side encryption with customer-provided keys (SSE-C) <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html>`_ .
            :param bucket_key_enabled: Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Existing objects are not affected. Setting the ``BucketKeyEnabled`` element to ``true`` causes Amazon S3 to use an S3 Bucket Key. By default, S3 Bucket Key is not enabled. For more information, see `Amazon S3 Bucket Keys <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-key.html>`_ in the *Amazon S3 User Guide* .
            :param server_side_encryption_by_default: Specifies the default server-side encryption to apply to new objects in the bucket. If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                server_side_encryption_rule_property = s3_mixins.CfnBucketPropsMixin.ServerSideEncryptionRuleProperty(
                    blocked_encryption_types=s3_mixins.CfnBucketPropsMixin.BlockedEncryptionTypesProperty(
                        encryption_type=["encryptionType"]
                    ),
                    bucket_key_enabled=False,
                    server_side_encryption_by_default=s3_mixins.CfnBucketPropsMixin.ServerSideEncryptionByDefaultProperty(
                        kms_master_key_id="kmsMasterKeyId",
                        sse_algorithm="sseAlgorithm"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a7ae9dc1abee8744e63a7c9b51942066bc54ee6791f632cccbb7d14977804a5)
                check_type(argname="argument blocked_encryption_types", value=blocked_encryption_types, expected_type=type_hints["blocked_encryption_types"])
                check_type(argname="argument bucket_key_enabled", value=bucket_key_enabled, expected_type=type_hints["bucket_key_enabled"])
                check_type(argname="argument server_side_encryption_by_default", value=server_side_encryption_by_default, expected_type=type_hints["server_side_encryption_by_default"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if blocked_encryption_types is not None:
                self._values["blocked_encryption_types"] = blocked_encryption_types
            if bucket_key_enabled is not None:
                self._values["bucket_key_enabled"] = bucket_key_enabled
            if server_side_encryption_by_default is not None:
                self._values["server_side_encryption_by_default"] = server_side_encryption_by_default

        @builtins.property
        def blocked_encryption_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.BlockedEncryptionTypesProperty"]]:
            '''A bucket-level setting for Amazon S3 general purpose buckets used to prevent the upload of new objects encrypted with the specified server-side encryption type.

            For example, blocking an encryption type will block ``PutObject`` , ``CopyObject`` , ``PostObject`` , multipart upload, and replication requests to the bucket for objects with the specified encryption type. However, you can continue to read and list any pre-existing objects already encrypted with the specified encryption type. For more information, see `Blocking or unblocking SSE-C for a general purpose bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/blocking-unblocking-s3-c-encryption-gpb.html>`_ .
            .. epigraph::

               Currently, this parameter only supports blocking or unblocking server-side encryption with customer-provided keys (SSE-C). For more information about SSE-C, see `Using server-side encryption with customer-provided keys (SSE-C) <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionrule.html#cfn-s3-bucket-serversideencryptionrule-blockedencryptiontypes
            '''
            result = self._values.get("blocked_encryption_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.BlockedEncryptionTypesProperty"]], result)

        @builtins.property
        def bucket_key_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket.

            Existing objects are not affected. Setting the ``BucketKeyEnabled`` element to ``true`` causes Amazon S3 to use an S3 Bucket Key. By default, S3 Bucket Key is not enabled.

            For more information, see `Amazon S3 Bucket Keys <https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-key.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionrule.html#cfn-s3-bucket-serversideencryptionrule-bucketkeyenabled
            '''
            result = self._values.get("bucket_key_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def server_side_encryption_by_default(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ServerSideEncryptionByDefaultProperty"]]:
            '''Specifies the default server-side encryption to apply to new objects in the bucket.

            If a PUT Object request doesn't specify any server-side encryption, this default encryption will be applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionrule.html#cfn-s3-bucket-serversideencryptionrule-serversideencryptionbydefault
            '''
            result = self._values.get("server_side_encryption_by_default")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ServerSideEncryptionByDefaultProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.SourceSelectionCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "replica_modifications": "replicaModifications",
            "sse_kms_encrypted_objects": "sseKmsEncryptedObjects",
        },
    )
    class SourceSelectionCriteriaProperty:
        def __init__(
            self,
            *,
            replica_modifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.ReplicaModificationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sse_kms_encrypted_objects: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.SseKmsEncryptedObjectsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A container that describes additional filters for identifying the source objects that you want to replicate.

            You can choose to enable or disable the replication of these objects.

            :param replica_modifications: A filter that you can specify for selection for modifications on replicas.
            :param sse_kms_encrypted_objects: A container for filter information for the selection of Amazon S3 objects encrypted with AWS KMS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-sourceselectioncriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                source_selection_criteria_property = s3_mixins.CfnBucketPropsMixin.SourceSelectionCriteriaProperty(
                    replica_modifications=s3_mixins.CfnBucketPropsMixin.ReplicaModificationsProperty(
                        status="status"
                    ),
                    sse_kms_encrypted_objects=s3_mixins.CfnBucketPropsMixin.SseKmsEncryptedObjectsProperty(
                        status="status"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57188763a309906f90b4cf3ad1ad344c58f70cabf8b5e55cac575e1f53a9fc0a)
                check_type(argname="argument replica_modifications", value=replica_modifications, expected_type=type_hints["replica_modifications"])
                check_type(argname="argument sse_kms_encrypted_objects", value=sse_kms_encrypted_objects, expected_type=type_hints["sse_kms_encrypted_objects"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if replica_modifications is not None:
                self._values["replica_modifications"] = replica_modifications
            if sse_kms_encrypted_objects is not None:
                self._values["sse_kms_encrypted_objects"] = sse_kms_encrypted_objects

        @builtins.property
        def replica_modifications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicaModificationsProperty"]]:
            '''A filter that you can specify for selection for modifications on replicas.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-sourceselectioncriteria.html#cfn-s3-bucket-sourceselectioncriteria-replicamodifications
            '''
            result = self._values.get("replica_modifications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.ReplicaModificationsProperty"]], result)

        @builtins.property
        def sse_kms_encrypted_objects(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.SseKmsEncryptedObjectsProperty"]]:
            '''A container for filter information for the selection of Amazon S3 objects encrypted with AWS KMS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-sourceselectioncriteria.html#cfn-s3-bucket-sourceselectioncriteria-ssekmsencryptedobjects
            '''
            result = self._values.get("sse_kms_encrypted_objects")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.SseKmsEncryptedObjectsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceSelectionCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.SseKmsEncryptedObjectsProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class SseKmsEncryptedObjectsProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''A container for filter information for the selection of S3 objects encrypted with AWS KMS.

            :param status: Specifies whether Amazon S3 replicates objects created with server-side encryption using an AWS KMS key stored in AWS Key Management Service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ssekmsencryptedobjects.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                sse_kms_encrypted_objects_property = s3_mixins.CfnBucketPropsMixin.SseKmsEncryptedObjectsProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0dd84cade6b021c89383e07f5a348ae2ede45cd575a27afbf37095712df40e63)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Specifies whether Amazon S3 replicates objects created with server-side encryption using an AWS KMS key stored in AWS Key Management Service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ssekmsencryptedobjects.html#cfn-s3-bucket-ssekmsencryptedobjects-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseKmsEncryptedObjectsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.StorageClassAnalysisProperty",
        jsii_struct_bases=[],
        name_mapping={"data_export": "dataExport"},
    )
    class StorageClassAnalysisProperty:
        def __init__(
            self,
            *,
            data_export: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.DataExportProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies data related to access patterns to be collected and made available to analyze the tradeoffs between different storage classes for an Amazon S3 bucket.

            :param data_export: Specifies how data related to the storage class analysis for an Amazon S3 bucket should be exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-storageclassanalysis.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                storage_class_analysis_property = s3_mixins.CfnBucketPropsMixin.StorageClassAnalysisProperty(
                    data_export=s3_mixins.CfnBucketPropsMixin.DataExportProperty(
                        destination=s3_mixins.CfnBucketPropsMixin.DestinationProperty(
                            bucket_account_id="bucketAccountId",
                            bucket_arn="bucketArn",
                            format="format",
                            prefix="prefix"
                        ),
                        output_schema_version="outputSchemaVersion"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__43ac45e1d920bb7cb6633dcee01a27a4d7556163b0e8ef1970cac3a985050d4b)
                check_type(argname="argument data_export", value=data_export, expected_type=type_hints["data_export"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_export is not None:
                self._values["data_export"] = data_export

        @builtins.property
        def data_export(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DataExportProperty"]]:
            '''Specifies how data related to the storage class analysis for an Amazon S3 bucket should be exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-storageclassanalysis.html#cfn-s3-bucket-storageclassanalysis-dataexport
            '''
            result = self._values.get("data_export")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.DataExportProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageClassAnalysisProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies tags to use to identify a subset of objects for an Amazon S3 bucket.

            For more information, see `Categorizing your storage using tags <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-tagging.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :param key: The tag key.
            :param value: The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tagfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                tag_filter_property = s3_mixins.CfnBucketPropsMixin.TagFilterProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff902def2552c5cc5162b20079fbe8892941de65647befbd46dd333b9b9d5951)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tagfilter.html#cfn-s3-bucket-tagfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tagfilter.html#cfn-s3-bucket-tagfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.TargetObjectKeyFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "partitioned_prefix": "partitionedPrefix",
            "simple_prefix": "simplePrefix",
        },
    )
    class TargetObjectKeyFormatProperty:
        def __init__(
            self,
            *,
            partitioned_prefix: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.PartitionedPrefixProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            simple_prefix: typing.Any = None,
        ) -> None:
            '''Amazon S3 key format for log objects.

            Only one format, PartitionedPrefix or SimplePrefix, is allowed.

            :param partitioned_prefix: Partitioned S3 key for log objects.
            :param simple_prefix: To use the simple format for S3 keys for log objects. To specify SimplePrefix format, set SimplePrefix to {}.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-targetobjectkeyformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                # simple_prefix: Any
                
                target_object_key_format_property = s3_mixins.CfnBucketPropsMixin.TargetObjectKeyFormatProperty(
                    partitioned_prefix=s3_mixins.CfnBucketPropsMixin.PartitionedPrefixProperty(
                        partition_date_source="partitionDateSource"
                    ),
                    simple_prefix=simple_prefix
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41c75868b1de41292f6e09f7f1775d53fe5ed5e0c80c90d1c95cdc865d83ac09)
                check_type(argname="argument partitioned_prefix", value=partitioned_prefix, expected_type=type_hints["partitioned_prefix"])
                check_type(argname="argument simple_prefix", value=simple_prefix, expected_type=type_hints["simple_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if partitioned_prefix is not None:
                self._values["partitioned_prefix"] = partitioned_prefix
            if simple_prefix is not None:
                self._values["simple_prefix"] = simple_prefix

        @builtins.property
        def partitioned_prefix(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.PartitionedPrefixProperty"]]:
            '''Partitioned S3 key for log objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-targetobjectkeyformat.html#cfn-s3-bucket-targetobjectkeyformat-partitionedprefix
            '''
            result = self._values.get("partitioned_prefix")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.PartitionedPrefixProperty"]], result)

        @builtins.property
        def simple_prefix(self) -> typing.Any:
            '''To use the simple format for S3 keys for log objects.

            To specify SimplePrefix format, set SimplePrefix to {}.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-targetobjectkeyformat.html#cfn-s3-bucket-targetobjectkeyformat-simpleprefix
            '''
            result = self._values.get("simple_prefix")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetObjectKeyFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.TieringProperty",
        jsii_struct_bases=[],
        name_mapping={"access_tier": "accessTier", "days": "days"},
    )
    class TieringProperty:
        def __init__(
            self,
            *,
            access_tier: typing.Optional[builtins.str] = None,
            days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The S3 Intelligent-Tiering storage class is designed to optimize storage costs by automatically moving data to the most cost-effective storage access tier, without additional operational overhead.

            :param access_tier: S3 Intelligent-Tiering access tier. See `Storage class for automatically optimizing frequently and infrequently accessed objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html#sc-dynamic-data-access>`_ for a list of access tiers in the S3 Intelligent-Tiering storage class.
            :param days: The number of consecutive days of no access after which an object will be eligible to be transitioned to the corresponding tier. The minimum number of days specified for Archive Access tier must be at least 90 days and Deep Archive Access tier must be at least 180 days. The maximum can be up to 2 years (730 days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tiering.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                tiering_property = s3_mixins.CfnBucketPropsMixin.TieringProperty(
                    access_tier="accessTier",
                    days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9408b1ed1c9af817cf6363b3ff9d1500a00d54335d321306c4ee4c0c229d59a7)
                check_type(argname="argument access_tier", value=access_tier, expected_type=type_hints["access_tier"])
                check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_tier is not None:
                self._values["access_tier"] = access_tier
            if days is not None:
                self._values["days"] = days

        @builtins.property
        def access_tier(self) -> typing.Optional[builtins.str]:
            '''S3 Intelligent-Tiering access tier.

            See `Storage class for automatically optimizing frequently and infrequently accessed objects <https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html#sc-dynamic-data-access>`_ for a list of access tiers in the S3 Intelligent-Tiering storage class.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tiering.html#cfn-s3-bucket-tiering-accesstier
            '''
            result = self._values.get("access_tier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def days(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive days of no access after which an object will be eligible to be transitioned to the corresponding tier.

            The minimum number of days specified for Archive Access tier must be at least 90 days and Deep Archive Access tier must be at least 180 days. The maximum can be up to 2 years (730 days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tiering.html#cfn-s3-bucket-tiering-days
            '''
            result = self._values.get("days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TieringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.TopicConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"event": "event", "filter": "filter", "topic": "topic"},
    )
    class TopicConfigurationProperty:
        def __init__(
            self,
            *,
            event: typing.Optional[builtins.str] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.NotificationFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            topic: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A container for specifying the configuration for publication of messages to an Amazon Simple Notification Service (Amazon SNS) topic when Amazon S3 detects specified events.

            :param event: The Amazon S3 bucket event about which to send notifications. For more information, see `Supported Event Types <https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html>`_ in the *Amazon S3 User Guide* .
            :param filter: The filtering rules that determine for which objects to send notifications. For example, you can create a filter so that Amazon S3 sends notifications only when image files with a ``.jpg`` extension are added to the bucket.
            :param topic: The Amazon Resource Name (ARN) of the Amazon SNS topic to which Amazon S3 publishes a message when it detects events of the specified type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-topicconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                topic_configuration_property = s3_mixins.CfnBucketPropsMixin.TopicConfigurationProperty(
                    event="event",
                    filter=s3_mixins.CfnBucketPropsMixin.NotificationFilterProperty(
                        s3_key=s3_mixins.CfnBucketPropsMixin.S3KeyFilterProperty(
                            rules=[s3_mixins.CfnBucketPropsMixin.FilterRuleProperty(
                                name="name",
                                value="value"
                            )]
                        )
                    ),
                    topic="topic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__571777c71620a73c29f8dbda8487e1ff2dfb52e24dee9873c589148842e9975a)
                check_type(argname="argument event", value=event, expected_type=type_hints["event"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event is not None:
                self._values["event"] = event
            if filter is not None:
                self._values["filter"] = filter
            if topic is not None:
                self._values["topic"] = topic

        @builtins.property
        def event(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket event about which to send notifications.

            For more information, see `Supported Event Types <https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-topicconfiguration.html#cfn-s3-bucket-topicconfiguration-event
            '''
            result = self._values.get("event")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NotificationFilterProperty"]]:
            '''The filtering rules that determine for which objects to send notifications.

            For example, you can create a filter so that Amazon S3 sends notifications only when image files with a ``.jpg`` extension are added to the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-topicconfiguration.html#cfn-s3-bucket-topicconfiguration-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.NotificationFilterProperty"]], result)

        @builtins.property
        def topic(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to which Amazon S3 publishes a message when it detects events of the specified type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-topicconfiguration.html#cfn-s3-bucket-topicconfiguration-topic
            '''
            result = self._values.get("topic")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TopicConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.TransitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "storage_class": "storageClass",
            "transition_date": "transitionDate",
            "transition_in_days": "transitionInDays",
        },
    )
    class TransitionProperty:
        def __init__(
            self,
            *,
            storage_class: typing.Optional[builtins.str] = None,
            transition_date: typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]] = None,
            transition_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies when an object transitions to a specified storage class.

            For more information about Amazon S3 lifecycle configuration rules, see `Transitioning Objects Using Amazon S3 Lifecycle <https://docs.aws.amazon.com/AmazonS3/latest/dev/lifecycle-transition-general-considerations.html>`_ in the *Amazon S3 User Guide* .

            :param storage_class: The storage class to which you want the object to transition.
            :param transition_date: Indicates when objects are transitioned to the specified storage class. The date value must be in ISO 8601 format. The time is always midnight UTC.
            :param transition_in_days: Indicates the number of days after creation when objects are transitioned to the specified storage class. If the specified storage class is ``INTELLIGENT_TIERING`` , ``GLACIER_IR`` , ``GLACIER`` , or ``DEEP_ARCHIVE`` , valid values are ``0`` or positive integers. If the specified storage class is ``STANDARD_IA`` or ``ONEZONE_IA`` , valid values are positive integers greater than ``30`` . Be aware that some storage classes have a minimum storage duration and that you're charged for transitioning objects before their minimum storage duration. For more information, see `Constraints and considerations for transitions <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html#lifecycle-configuration-constraints>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-transition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                transition_property = s3_mixins.CfnBucketPropsMixin.TransitionProperty(
                    storage_class="storageClass",
                    transition_date=Date(),
                    transition_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a74dc017c7bb834f3c57974eb5f80ea0e9d60b6e1c04c64241c72b130eaefdb1)
                check_type(argname="argument storage_class", value=storage_class, expected_type=type_hints["storage_class"])
                check_type(argname="argument transition_date", value=transition_date, expected_type=type_hints["transition_date"])
                check_type(argname="argument transition_in_days", value=transition_in_days, expected_type=type_hints["transition_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if storage_class is not None:
                self._values["storage_class"] = storage_class
            if transition_date is not None:
                self._values["transition_date"] = transition_date
            if transition_in_days is not None:
                self._values["transition_in_days"] = transition_in_days

        @builtins.property
        def storage_class(self) -> typing.Optional[builtins.str]:
            '''The storage class to which you want the object to transition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-transition.html#cfn-s3-bucket-transition-storageclass
            '''
            result = self._values.get("storage_class")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transition_date(
            self,
        ) -> typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates when objects are transitioned to the specified storage class.

            The date value must be in ISO 8601 format. The time is always midnight UTC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-transition.html#cfn-s3-bucket-transition-transitiondate
            '''
            result = self._values.get("transition_date")
            return typing.cast(typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def transition_in_days(self) -> typing.Optional[jsii.Number]:
            '''Indicates the number of days after creation when objects are transitioned to the specified storage class.

            If the specified storage class is ``INTELLIGENT_TIERING`` , ``GLACIER_IR`` , ``GLACIER`` , or ``DEEP_ARCHIVE`` , valid values are ``0`` or positive integers. If the specified storage class is ``STANDARD_IA`` or ``ONEZONE_IA`` , valid values are positive integers greater than ``30`` . Be aware that some storage classes have a minimum storage duration and that you're charged for transitioning objects before their minimum storage duration. For more information, see `Constraints and considerations for transitions <https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html#lifecycle-configuration-constraints>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-transition.html#cfn-s3-bucket-transition-transitionindays
            '''
            result = self._values.get("transition_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.VersioningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class VersioningConfigurationProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''Describes the versioning state of an Amazon S3 bucket.

            For more information, see `PUT Bucket versioning <https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTVersioningStatus.html>`_ in the *Amazon S3 API Reference* .

            Keep the following timing in mind when enabling, suspending, or transitioning between versioning states:

            - *Enabling versioning* - Changes may take up to 15 minutes to propagate across all AWS regions for full consistency.
            - *Suspending versioning* - Takes effect immediately with no propagation delay.
            - *Transitioning between states* - Any change from Suspended to Enabled has a 15-minute delay.

            :param status: The versioning state of the bucket. Default: - "Suspended"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-versioningconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                versioning_configuration_property = s3_mixins.CfnBucketPropsMixin.VersioningConfigurationProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__885d64f9f5c382eb200d9b49fdb81ec3ee8de8d400b2ac3b9bc95212f159263c)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The versioning state of the bucket.

            :default: - "Suspended"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-versioningconfiguration.html#cfn-s3-bucket-versioningconfiguration-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VersioningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnBucketPropsMixin.WebsiteConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_document": "errorDocument",
            "index_document": "indexDocument",
            "redirect_all_requests_to": "redirectAllRequestsTo",
            "routing_rules": "routingRules",
        },
    )
    class WebsiteConfigurationProperty:
        def __init__(
            self,
            *,
            error_document: typing.Optional[builtins.str] = None,
            index_document: typing.Optional[builtins.str] = None,
            redirect_all_requests_to: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.RedirectAllRequestsToProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            routing_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.RoutingRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies website configuration parameters for an Amazon S3 bucket.

            :param error_document: The name of the error document for the website.
            :param index_document: The name of the index document for the website.
            :param redirect_all_requests_to: The redirect behavior for every request to this bucket's website endpoint. .. epigraph:: If you specify this property, you can't specify any other property.
            :param routing_rules: Rules that define when a redirect is applied and the redirect behavior.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-websiteconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                website_configuration_property = s3_mixins.CfnBucketPropsMixin.WebsiteConfigurationProperty(
                    error_document="errorDocument",
                    index_document="indexDocument",
                    redirect_all_requests_to=s3_mixins.CfnBucketPropsMixin.RedirectAllRequestsToProperty(
                        host_name="hostName",
                        protocol="protocol"
                    ),
                    routing_rules=[s3_mixins.CfnBucketPropsMixin.RoutingRuleProperty(
                        redirect_rule=s3_mixins.CfnBucketPropsMixin.RedirectRuleProperty(
                            host_name="hostName",
                            http_redirect_code="httpRedirectCode",
                            protocol="protocol",
                            replace_key_prefix_with="replaceKeyPrefixWith",
                            replace_key_with="replaceKeyWith"
                        ),
                        routing_rule_condition=s3_mixins.CfnBucketPropsMixin.RoutingRuleConditionProperty(
                            http_error_code_returned_equals="httpErrorCodeReturnedEquals",
                            key_prefix_equals="keyPrefixEquals"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__032fb9f64e772bfee9e52da277fc951f50bf72c817642bb4fea59beee9bc3eb3)
                check_type(argname="argument error_document", value=error_document, expected_type=type_hints["error_document"])
                check_type(argname="argument index_document", value=index_document, expected_type=type_hints["index_document"])
                check_type(argname="argument redirect_all_requests_to", value=redirect_all_requests_to, expected_type=type_hints["redirect_all_requests_to"])
                check_type(argname="argument routing_rules", value=routing_rules, expected_type=type_hints["routing_rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error_document is not None:
                self._values["error_document"] = error_document
            if index_document is not None:
                self._values["index_document"] = index_document
            if redirect_all_requests_to is not None:
                self._values["redirect_all_requests_to"] = redirect_all_requests_to
            if routing_rules is not None:
                self._values["routing_rules"] = routing_rules

        @builtins.property
        def error_document(self) -> typing.Optional[builtins.str]:
            '''The name of the error document for the website.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-websiteconfiguration.html#cfn-s3-bucket-websiteconfiguration-errordocument
            '''
            result = self._values.get("error_document")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_document(self) -> typing.Optional[builtins.str]:
            '''The name of the index document for the website.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-websiteconfiguration.html#cfn-s3-bucket-websiteconfiguration-indexdocument
            '''
            result = self._values.get("index_document")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def redirect_all_requests_to(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RedirectAllRequestsToProperty"]]:
            '''The redirect behavior for every request to this bucket's website endpoint.

            .. epigraph::

               If you specify this property, you can't specify any other property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-websiteconfiguration.html#cfn-s3-bucket-websiteconfiguration-redirectallrequeststo
            '''
            result = self._values.get("redirect_all_requests_to")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RedirectAllRequestsToProperty"]], result)

        @builtins.property
        def routing_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RoutingRuleProperty"]]]]:
            '''Rules that define when a redirect is applied and the redirect behavior.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-websiteconfiguration.html#cfn-s3-bucket-websiteconfiguration-routingrules
            '''
            result = self._values.get("routing_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.RoutingRuleProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebsiteConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnMultiRegionAccessPointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "public_access_block_configuration": "publicAccessBlockConfiguration",
        "regions": "regions",
    },
)
class CfnMultiRegionAccessPointMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        public_access_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMultiRegionAccessPointPropsMixin.PublicAccessBlockConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        regions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMultiRegionAccessPointPropsMixin.RegionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnMultiRegionAccessPointPropsMixin.

        :param name: The name of the Multi-Region Access Point.
        :param public_access_block_configuration: The PublicAccessBlock configuration that you want to apply to this Multi-Region Access Point. You can enable the configuration options in any combination. For more information about when Amazon S3 considers an object public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .
        :param regions: A collection of the Regions and buckets associated with the Multi-Region Access Point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-multiregionaccesspoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
            
            cfn_multi_region_access_point_mixin_props = s3_mixins.CfnMultiRegionAccessPointMixinProps(
                name="name",
                public_access_block_configuration=s3_mixins.CfnMultiRegionAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                ),
                regions=[s3_mixins.CfnMultiRegionAccessPointPropsMixin.RegionProperty(
                    bucket="bucket",
                    bucket_account_id="bucketAccountId"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f299e980c99133c2d3bfa5f685372c13176b82be3f2059e09ab26cbb7e0bfb9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument public_access_block_configuration", value=public_access_block_configuration, expected_type=type_hints["public_access_block_configuration"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if public_access_block_configuration is not None:
            self._values["public_access_block_configuration"] = public_access_block_configuration
        if regions is not None:
            self._values["regions"] = regions

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Multi-Region Access Point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-multiregionaccesspoint.html#cfn-s3-multiregionaccesspoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_access_block_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMultiRegionAccessPointPropsMixin.PublicAccessBlockConfigurationProperty"]]:
        '''The PublicAccessBlock configuration that you want to apply to this Multi-Region Access Point.

        You can enable the configuration options in any combination. For more information about when Amazon S3 considers an object public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-multiregionaccesspoint.html#cfn-s3-multiregionaccesspoint-publicaccessblockconfiguration
        '''
        result = self._values.get("public_access_block_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMultiRegionAccessPointPropsMixin.PublicAccessBlockConfigurationProperty"]], result)

    @builtins.property
    def regions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMultiRegionAccessPointPropsMixin.RegionProperty"]]]]:
        '''A collection of the Regions and buckets associated with the Multi-Region Access Point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-multiregionaccesspoint.html#cfn-s3-multiregionaccesspoint-regions
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMultiRegionAccessPointPropsMixin.RegionProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMultiRegionAccessPointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnMultiRegionAccessPointPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"mrap_name": "mrapName", "policy": "policy"},
)
class CfnMultiRegionAccessPointPolicyMixinProps:
    def __init__(
        self,
        *,
        mrap_name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
    ) -> None:
        '''Properties for CfnMultiRegionAccessPointPolicyPropsMixin.

        :param mrap_name: The name of the Multi-Region Access Point.
        :param policy: The access policy associated with the Multi-Region Access Point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-multiregionaccesspointpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
            
            # policy: Any
            
            cfn_multi_region_access_point_policy_mixin_props = s3_mixins.CfnMultiRegionAccessPointPolicyMixinProps(
                mrap_name="mrapName",
                policy=policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4a8045dd04aa4eb801095759465f3675aa01a75e7880d3d9b252502409ca18)
            check_type(argname="argument mrap_name", value=mrap_name, expected_type=type_hints["mrap_name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mrap_name is not None:
            self._values["mrap_name"] = mrap_name
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def mrap_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Multi-Region Access Point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-multiregionaccesspointpolicy.html#cfn-s3-multiregionaccesspointpolicy-mrapname
        '''
        result = self._values.get("mrap_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The access policy associated with the Multi-Region Access Point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-multiregionaccesspointpolicy.html#cfn-s3-multiregionaccesspointpolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMultiRegionAccessPointPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMultiRegionAccessPointPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnMultiRegionAccessPointPolicyPropsMixin",
):
    '''Applies an Amazon S3 access policy to an Amazon S3 Multi-Region Access Point.

    It is not possible to delete an access policy for a Multi-Region Access Point from the CloudFormation template. When you attempt to delete the policy, CloudFormation updates the policy using ``DeletionPolicy:Retain`` and ``UpdateReplacePolicy:Retain`` . CloudFormation updates the policy to only allow access to the account that created the bucket.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-multiregionaccesspointpolicy.html
    :cloudformationResource: AWS::S3::MultiRegionAccessPointPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
        
        # policy: Any
        
        cfn_multi_region_access_point_policy_props_mixin = s3_mixins.CfnMultiRegionAccessPointPolicyPropsMixin(s3_mixins.CfnMultiRegionAccessPointPolicyMixinProps(
            mrap_name="mrapName",
            policy=policy
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMultiRegionAccessPointPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3::MultiRegionAccessPointPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cddacae305f7dfbd0ff18f8930769c5456acc830276b33e14a8233d12340ee4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16646e2cd4bd9804f2d6bef3701c14f69dfd92fda9db8673eddf229dfaf7b118)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903ef159e47a64aa125f3c08dc3355d049a36fea6e71fdf9df341c3856168a69)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMultiRegionAccessPointPolicyMixinProps:
        return typing.cast(CfnMultiRegionAccessPointPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnMultiRegionAccessPointPolicyPropsMixin.PolicyStatusProperty",
        jsii_struct_bases=[],
        name_mapping={"is_public": "isPublic"},
    )
    class PolicyStatusProperty:
        def __init__(self, *, is_public: typing.Optional[builtins.str] = None) -> None:
            '''The container element for a bucket's policy status.

            :param is_public: The policy status for this bucket. ``TRUE`` indicates that this bucket is public. ``FALSE`` indicates that the bucket is not public.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspointpolicy-policystatus.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                policy_status_property = s3_mixins.CfnMultiRegionAccessPointPolicyPropsMixin.PolicyStatusProperty(
                    is_public="isPublic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__12ba0d62fe259fa60f1e29b5e2f730ab35dd52237da6005daafa1f78cec45787)
                check_type(argname="argument is_public", value=is_public, expected_type=type_hints["is_public"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_public is not None:
                self._values["is_public"] = is_public

        @builtins.property
        def is_public(self) -> typing.Optional[builtins.str]:
            '''The policy status for this bucket.

            ``TRUE`` indicates that this bucket is public. ``FALSE`` indicates that the bucket is not public.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspointpolicy-policystatus.html#cfn-s3-multiregionaccesspointpolicy-policystatus-ispublic
            '''
            result = self._values.get("is_public")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyStatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnMultiRegionAccessPointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnMultiRegionAccessPointPropsMixin",
):
    '''The ``AWS::S3::MultiRegionAccessPoint`` resource creates an Amazon S3 Multi-Region Access Point.

    To learn more about Multi-Region Access Points, see `Multi-Region Access Points in Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessPoints.html>`_ in the in the *Amazon S3 User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-multiregionaccesspoint.html
    :cloudformationResource: AWS::S3::MultiRegionAccessPoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
        
        cfn_multi_region_access_point_props_mixin = s3_mixins.CfnMultiRegionAccessPointPropsMixin(s3_mixins.CfnMultiRegionAccessPointMixinProps(
            name="name",
            public_access_block_configuration=s3_mixins.CfnMultiRegionAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            regions=[s3_mixins.CfnMultiRegionAccessPointPropsMixin.RegionProperty(
                bucket="bucket",
                bucket_account_id="bucketAccountId"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMultiRegionAccessPointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3::MultiRegionAccessPoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dad4ceb4433c845a98a94e94cb136199684d8155ea5abb04eeee942957236b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bb7b7a04207fe606c19f5b387d14762a327d65072adade1a2aeb628773f08c5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e0ff90278293be505e8053e0423ac4b2d7a733841fc2d91f64947e01da7127)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMultiRegionAccessPointMixinProps:
        return typing.cast(CfnMultiRegionAccessPointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnMultiRegionAccessPointPropsMixin.PublicAccessBlockConfigurationProperty",
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
            '''The PublicAccessBlock configuration that you want to apply to this Amazon S3 Multi-Region Access Point.

            You can enable the configuration options in any combination. For more information about when Amazon S3 considers an object public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .

            :param block_public_acls: Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and objects in this bucket. Setting this element to ``TRUE`` causes the following behavior: - PUT Bucket ACL and PUT Object ACL calls fail if the specified ACL is public. - PUT Object calls fail if the request includes a public ACL. - PUT Bucket calls fail if the request includes a public ACL. Enabling this setting doesn't affect existing policies or ACLs.
            :param block_public_policy: Specifies whether Amazon S3 should block public bucket policies for this bucket. Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access. Enabling this setting doesn't affect existing bucket policies.
            :param ignore_public_acls: Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this bucket. Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on this bucket and objects in this bucket. Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.
            :param restrict_public_buckets: Specifies whether Amazon S3 should restrict public bucket policies for this bucket. Setting this element to ``TRUE`` restricts access to this bucket to only AWS service principals and authorized users within this account if the bucket has a public policy. Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspoint-publicaccessblockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                public_access_block_configuration_property = s3_mixins.CfnMultiRegionAccessPointPropsMixin.PublicAccessBlockConfigurationProperty(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36006bb930af965ef9868643d18e1124d0ebfc3163dfce89c5691244b1302aaf)
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
            '''Specifies whether Amazon S3 should block public access control lists (ACLs) for this bucket and objects in this bucket.

            Setting this element to ``TRUE`` causes the following behavior:

            - PUT Bucket ACL and PUT Object ACL calls fail if the specified ACL is public.
            - PUT Object calls fail if the request includes a public ACL.
            - PUT Bucket calls fail if the request includes a public ACL.

            Enabling this setting doesn't affect existing policies or ACLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspoint-publicaccessblockconfiguration.html#cfn-s3-multiregionaccesspoint-publicaccessblockconfiguration-blockpublicacls
            '''
            result = self._values.get("block_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def block_public_policy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should block public bucket policies for this bucket.

            Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access.

            Enabling this setting doesn't affect existing bucket policies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspoint-publicaccessblockconfiguration.html#cfn-s3-multiregionaccesspoint-publicaccessblockconfiguration-blockpublicpolicy
            '''
            result = self._values.get("block_public_policy")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ignore_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should ignore public ACLs for this bucket and objects in this bucket.

            Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on this bucket and objects in this bucket.

            Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspoint-publicaccessblockconfiguration.html#cfn-s3-multiregionaccesspoint-publicaccessblockconfiguration-ignorepublicacls
            '''
            result = self._values.get("ignore_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def restrict_public_buckets(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether Amazon S3 should restrict public bucket policies for this bucket.

            Setting this element to ``TRUE`` restricts access to this bucket to only AWS service principals and authorized users within this account if the bucket has a public policy.

            Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspoint-publicaccessblockconfiguration.html#cfn-s3-multiregionaccesspoint-publicaccessblockconfiguration-restrictpublicbuckets
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
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnMultiRegionAccessPointPropsMixin.RegionProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "bucket_account_id": "bucketAccountId"},
    )
    class RegionProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            bucket_account_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A bucket associated with a specific Region when creating Multi-Region Access Points.

            :param bucket: The name of the associated bucket for the Region.
            :param bucket_account_id: The AWS account ID that owns the Amazon S3 bucket that's associated with this Multi-Region Access Point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspoint-region.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                region_property = s3_mixins.CfnMultiRegionAccessPointPropsMixin.RegionProperty(
                    bucket="bucket",
                    bucket_account_id="bucketAccountId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c397508cc3c3530150a921cc466c2ebc3caeb0ebe1c88a01c5170550f395cb9)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument bucket_account_id", value=bucket_account_id, expected_type=type_hints["bucket_account_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if bucket_account_id is not None:
                self._values["bucket_account_id"] = bucket_account_id

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the associated bucket for the Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspoint-region.html#cfn-s3-multiregionaccesspoint-region-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_account_id(self) -> typing.Optional[builtins.str]:
            '''The AWS account ID that owns the Amazon S3 bucket that's associated with this Multi-Region Access Point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-multiregionaccesspoint-region.html#cfn-s3-multiregionaccesspoint-region-bucketaccountid
            '''
            result = self._values.get("bucket_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter", "name": "name", "tags": "tags"},
)
class CfnStorageLensGroupMixinProps:
    def __init__(
        self,
        *,
        filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensGroupPropsMixin.FilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStorageLensGroupPropsMixin.

        :param filter: This property contains the criteria for the Storage Lens group data that is displayed.
        :param name: This property contains the Storage Lens group name.
        :param tags: This property contains the AWS resource tags that you're adding to your Storage Lens group. This parameter is optional.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelensgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
            
            cfn_storage_lens_group_mixin_props = s3_mixins.CfnStorageLensGroupMixinProps(
                filter=s3_mixins.CfnStorageLensGroupPropsMixin.FilterProperty(
                    and=s3_mixins.CfnStorageLensGroupPropsMixin.AndProperty(
                        match_any_prefix=["matchAnyPrefix"],
                        match_any_suffix=["matchAnySuffix"],
                        match_any_tag=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                            days_greater_than=123,
                            days_less_than=123
                        ),
                        match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                            bytes_greater_than=123,
                            bytes_less_than=123
                        )
                    ),
                    match_any_prefix=["matchAnyPrefix"],
                    match_any_suffix=["matchAnySuffix"],
                    match_any_tag=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                        days_greater_than=123,
                        days_less_than=123
                    ),
                    match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                        bytes_greater_than=123,
                        bytes_less_than=123
                    ),
                    or=s3_mixins.CfnStorageLensGroupPropsMixin.OrProperty(
                        match_any_prefix=["matchAnyPrefix"],
                        match_any_suffix=["matchAnySuffix"],
                        match_any_tag=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                            days_greater_than=123,
                            days_less_than=123
                        ),
                        match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                            bytes_greater_than=123,
                            bytes_less_than=123
                        )
                    )
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8c3baea9250ca2d66654501d87b3b98445d18ee99836e46fcf8a67e8fc403f)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter is not None:
            self._values["filter"] = filter
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.FilterProperty"]]:
        '''This property contains the criteria for the Storage Lens group data that is displayed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelensgroup.html#cfn-s3-storagelensgroup-filter
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.FilterProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''This property contains the Storage Lens group name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelensgroup.html#cfn-s3-storagelensgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''This property contains the AWS resource tags that you're adding to your Storage Lens group.

        This parameter is optional.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelensgroup.html#cfn-s3-storagelensgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStorageLensGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStorageLensGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensGroupPropsMixin",
):
    '''The ``AWS::S3::StorageLensGroup`` resource creates an S3 Storage Lens group.

    A Storage Lens group is a custom grouping of objects that include filters for prefixes, suffixes, object tags, object size, or object age. You can create an S3 Storage Lens group that includes a single filter or multiple filter conditions. To specify multiple filter conditions, you use ``AND`` or ``OR`` logical operators. For more information about S3 Storage Lens groups, see `Working with S3 Storage Lens groups <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-lens-groups-overview.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelensgroup.html
    :cloudformationResource: AWS::S3::StorageLensGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
        
        cfn_storage_lens_group_props_mixin = s3_mixins.CfnStorageLensGroupPropsMixin(s3_mixins.CfnStorageLensGroupMixinProps(
            filter=s3_mixins.CfnStorageLensGroupPropsMixin.FilterProperty(
                and=s3_mixins.CfnStorageLensGroupPropsMixin.AndProperty(
                    match_any_prefix=["matchAnyPrefix"],
                    match_any_suffix=["matchAnySuffix"],
                    match_any_tag=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                        days_greater_than=123,
                        days_less_than=123
                    ),
                    match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                        bytes_greater_than=123,
                        bytes_less_than=123
                    )
                ),
                match_any_prefix=["matchAnyPrefix"],
                match_any_suffix=["matchAnySuffix"],
                match_any_tag=[CfnTag(
                    key="key",
                    value="value"
                )],
                match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                    days_greater_than=123,
                    days_less_than=123
                ),
                match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                    bytes_greater_than=123,
                    bytes_less_than=123
                ),
                or=s3_mixins.CfnStorageLensGroupPropsMixin.OrProperty(
                    match_any_prefix=["matchAnyPrefix"],
                    match_any_suffix=["matchAnySuffix"],
                    match_any_tag=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                        days_greater_than=123,
                        days_less_than=123
                    ),
                    match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                        bytes_greater_than=123,
                        bytes_less_than=123
                    )
                )
            ),
            name="name",
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
        props: typing.Union[CfnStorageLensGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3::StorageLensGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b79176d6bba3db03f2a5acab34f14d04929bf3cb17440f5a55e34e6f8f5a30f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80513eaaf6ebe8aee666195e04cf5d93d98e2b2320f7cf77e9a190833344ec06)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0b7db7363fcc8048372fd4f1e1760550f1f1a0621d189eb54a749008cc563a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStorageLensGroupMixinProps:
        return typing.cast(CfnStorageLensGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensGroupPropsMixin.AndProperty",
        jsii_struct_bases=[],
        name_mapping={
            "match_any_prefix": "matchAnyPrefix",
            "match_any_suffix": "matchAnySuffix",
            "match_any_tag": "matchAnyTag",
            "match_object_age": "matchObjectAge",
            "match_object_size": "matchObjectSize",
        },
    )
    class AndProperty:
        def __init__(
            self,
            *,
            match_any_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
            match_any_suffix: typing.Optional[typing.Sequence[builtins.str]] = None,
            match_any_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
            match_object_age: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            match_object_size: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This resource is a logical operator that allows multiple filter conditions to be joined for more complex comparisons of Storage Lens group data.

            Objects must match all of the listed filter conditions that are joined by the ``And`` logical operator. Only one of each filter condition is allowed.

            :param match_any_prefix: This property contains a list of prefixes. At least one prefix must be specified. Up to 10 prefixes are allowed.
            :param match_any_suffix: This property contains a list of suffixes. At least one suffix must be specified. Up to 10 suffixes are allowed.
            :param match_any_tag: This property contains the list of object tags. At least one object tag must be specified. Up to 10 object tags are allowed.
            :param match_object_age: This property contains ``DaysGreaterThan`` and ``DaysLessThan`` properties to define the object age range (minimum and maximum number of days).
            :param match_object_size: This property contains ``BytesGreaterThan`` and ``BytesLessThan`` to define the object size range (minimum and maximum number of Bytes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-and.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                and_property = s3_mixins.CfnStorageLensGroupPropsMixin.AndProperty(
                    match_any_prefix=["matchAnyPrefix"],
                    match_any_suffix=["matchAnySuffix"],
                    match_any_tag=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                        days_greater_than=123,
                        days_less_than=123
                    ),
                    match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                        bytes_greater_than=123,
                        bytes_less_than=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__82069e5a3549b13848688189cc159471062f07db423e376490df557d6c36170f)
                check_type(argname="argument match_any_prefix", value=match_any_prefix, expected_type=type_hints["match_any_prefix"])
                check_type(argname="argument match_any_suffix", value=match_any_suffix, expected_type=type_hints["match_any_suffix"])
                check_type(argname="argument match_any_tag", value=match_any_tag, expected_type=type_hints["match_any_tag"])
                check_type(argname="argument match_object_age", value=match_object_age, expected_type=type_hints["match_object_age"])
                check_type(argname="argument match_object_size", value=match_object_size, expected_type=type_hints["match_object_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if match_any_prefix is not None:
                self._values["match_any_prefix"] = match_any_prefix
            if match_any_suffix is not None:
                self._values["match_any_suffix"] = match_any_suffix
            if match_any_tag is not None:
                self._values["match_any_tag"] = match_any_tag
            if match_object_age is not None:
                self._values["match_object_age"] = match_object_age
            if match_object_size is not None:
                self._values["match_object_size"] = match_object_size

        @builtins.property
        def match_any_prefix(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property contains a list of prefixes.

            At least one prefix must be specified. Up to 10 prefixes are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-and.html#cfn-s3-storagelensgroup-and-matchanyprefix
            '''
            result = self._values.get("match_any_prefix")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def match_any_suffix(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property contains a list of suffixes.

            At least one suffix must be specified. Up to 10 suffixes are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-and.html#cfn-s3-storagelensgroup-and-matchanysuffix
            '''
            result = self._values.get("match_any_suffix")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def match_any_tag(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
            '''This property contains the list of object tags.

            At least one object tag must be specified. Up to 10 object tags are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-and.html#cfn-s3-storagelensgroup-and-matchanytag
            '''
            result = self._values.get("match_any_tag")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

        @builtins.property
        def match_object_age(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty"]]:
            '''This property contains ``DaysGreaterThan`` and ``DaysLessThan`` properties to define the object age range (minimum and maximum number of days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-and.html#cfn-s3-storagelensgroup-and-matchobjectage
            '''
            result = self._values.get("match_object_age")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty"]], result)

        @builtins.property
        def match_object_size(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty"]]:
            '''This property contains ``BytesGreaterThan`` and ``BytesLessThan`` to define the object size range (minimum and maximum number of Bytes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-and.html#cfn-s3-storagelensgroup-and-matchobjectsize
            '''
            result = self._values.get("match_object_size")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensGroupPropsMixin.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_": "and",
            "match_any_prefix": "matchAnyPrefix",
            "match_any_suffix": "matchAnySuffix",
            "match_any_tag": "matchAnyTag",
            "match_object_age": "matchObjectAge",
            "match_object_size": "matchObjectSize",
            "or_": "or",
        },
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            and_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensGroupPropsMixin.AndProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            match_any_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
            match_any_suffix: typing.Optional[typing.Sequence[builtins.str]] = None,
            match_any_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
            match_object_age: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            match_object_size: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            or_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensGroupPropsMixin.OrProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This resource sets the criteria for the Storage Lens group data that is displayed.

            For multiple filter conditions, the ``AND`` or ``OR`` logical operator is used.

            :param and_: This property contains the ``And`` logical operator, which allows multiple filter conditions to be joined for more complex comparisons of Storage Lens group data. Objects must match all of the listed filter conditions that are joined by the ``And`` logical operator. Only one of each filter condition is allowed.
            :param match_any_prefix: This property contains a list of prefixes. At least one prefix must be specified. Up to 10 prefixes are allowed.
            :param match_any_suffix: This property contains a list of suffixes. At least one suffix must be specified. Up to 10 suffixes are allowed.
            :param match_any_tag: This property contains the list of S3 object tags. At least one object tag must be specified. Up to 10 object tags are allowed.
            :param match_object_age: This property contains ``DaysGreaterThan`` and ``DaysLessThan`` to define the object age range (minimum and maximum number of days).
            :param match_object_size: This property contains ``BytesGreaterThan`` and ``BytesLessThan`` to define the object size range (minimum and maximum number of Bytes).
            :param or_: This property contains the ``Or`` logical operator, which allows multiple filter conditions to be joined. Objects can match any of the listed filter conditions, which are joined by the ``Or`` logical operator. Only one of each filter condition is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                filter_property = s3_mixins.CfnStorageLensGroupPropsMixin.FilterProperty(
                    and=s3_mixins.CfnStorageLensGroupPropsMixin.AndProperty(
                        match_any_prefix=["matchAnyPrefix"],
                        match_any_suffix=["matchAnySuffix"],
                        match_any_tag=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                            days_greater_than=123,
                            days_less_than=123
                        ),
                        match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                            bytes_greater_than=123,
                            bytes_less_than=123
                        )
                    ),
                    match_any_prefix=["matchAnyPrefix"],
                    match_any_suffix=["matchAnySuffix"],
                    match_any_tag=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                        days_greater_than=123,
                        days_less_than=123
                    ),
                    match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                        bytes_greater_than=123,
                        bytes_less_than=123
                    ),
                    or=s3_mixins.CfnStorageLensGroupPropsMixin.OrProperty(
                        match_any_prefix=["matchAnyPrefix"],
                        match_any_suffix=["matchAnySuffix"],
                        match_any_tag=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                            days_greater_than=123,
                            days_less_than=123
                        ),
                        match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                            bytes_greater_than=123,
                            bytes_less_than=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e0a064e86223d6538f7bb62c14fe89718bd3102980b6939536f3fbf52783d73)
                check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
                check_type(argname="argument match_any_prefix", value=match_any_prefix, expected_type=type_hints["match_any_prefix"])
                check_type(argname="argument match_any_suffix", value=match_any_suffix, expected_type=type_hints["match_any_suffix"])
                check_type(argname="argument match_any_tag", value=match_any_tag, expected_type=type_hints["match_any_tag"])
                check_type(argname="argument match_object_age", value=match_object_age, expected_type=type_hints["match_object_age"])
                check_type(argname="argument match_object_size", value=match_object_size, expected_type=type_hints["match_object_size"])
                check_type(argname="argument or_", value=or_, expected_type=type_hints["or_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if and_ is not None:
                self._values["and_"] = and_
            if match_any_prefix is not None:
                self._values["match_any_prefix"] = match_any_prefix
            if match_any_suffix is not None:
                self._values["match_any_suffix"] = match_any_suffix
            if match_any_tag is not None:
                self._values["match_any_tag"] = match_any_tag
            if match_object_age is not None:
                self._values["match_object_age"] = match_object_age
            if match_object_size is not None:
                self._values["match_object_size"] = match_object_size
            if or_ is not None:
                self._values["or_"] = or_

        @builtins.property
        def and_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.AndProperty"]]:
            '''This property contains the ``And`` logical operator, which allows multiple filter conditions to be joined for more complex comparisons of Storage Lens group data.

            Objects must match all of the listed filter conditions that are joined by the ``And`` logical operator. Only one of each filter condition is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-filter.html#cfn-s3-storagelensgroup-filter-and
            '''
            result = self._values.get("and_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.AndProperty"]], result)

        @builtins.property
        def match_any_prefix(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property contains a list of prefixes.

            At least one prefix must be specified. Up to 10 prefixes are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-filter.html#cfn-s3-storagelensgroup-filter-matchanyprefix
            '''
            result = self._values.get("match_any_prefix")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def match_any_suffix(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property contains a list of suffixes.

            At least one suffix must be specified. Up to 10 suffixes are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-filter.html#cfn-s3-storagelensgroup-filter-matchanysuffix
            '''
            result = self._values.get("match_any_suffix")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def match_any_tag(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
            '''This property contains the list of S3 object tags.

            At least one object tag must be specified. Up to 10 object tags are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-filter.html#cfn-s3-storagelensgroup-filter-matchanytag
            '''
            result = self._values.get("match_any_tag")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

        @builtins.property
        def match_object_age(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty"]]:
            '''This property contains ``DaysGreaterThan`` and ``DaysLessThan`` to define the object age range (minimum and maximum number of days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-filter.html#cfn-s3-storagelensgroup-filter-matchobjectage
            '''
            result = self._values.get("match_object_age")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty"]], result)

        @builtins.property
        def match_object_size(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty"]]:
            '''This property contains ``BytesGreaterThan`` and ``BytesLessThan`` to define the object size range (minimum and maximum number of Bytes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-filter.html#cfn-s3-storagelensgroup-filter-matchobjectsize
            '''
            result = self._values.get("match_object_size")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty"]], result)

        @builtins.property
        def or_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.OrProperty"]]:
            '''This property contains the ``Or`` logical operator, which allows multiple filter conditions to be joined.

            Objects can match any of the listed filter conditions, which are joined by the ``Or`` logical operator. Only one of each filter condition is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-filter.html#cfn-s3-storagelensgroup-filter-or
            '''
            result = self._values.get("or_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.OrProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "days_greater_than": "daysGreaterThan",
            "days_less_than": "daysLessThan",
        },
    )
    class MatchObjectAgeProperty:
        def __init__(
            self,
            *,
            days_greater_than: typing.Optional[jsii.Number] = None,
            days_less_than: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''This resource contains ``DaysGreaterThan`` and ``DaysLessThan`` to define the object age range (minimum and maximum number of days).

            :param days_greater_than: This property indicates the minimum object age in days.
            :param days_less_than: This property indicates the maximum object age in days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-matchobjectage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                match_object_age_property = s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                    days_greater_than=123,
                    days_less_than=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58d672bdd83ff193b58a1279486f8f6f1f1e404c005b6ec6ad14879c25ac6bdd)
                check_type(argname="argument days_greater_than", value=days_greater_than, expected_type=type_hints["days_greater_than"])
                check_type(argname="argument days_less_than", value=days_less_than, expected_type=type_hints["days_less_than"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days_greater_than is not None:
                self._values["days_greater_than"] = days_greater_than
            if days_less_than is not None:
                self._values["days_less_than"] = days_less_than

        @builtins.property
        def days_greater_than(self) -> typing.Optional[jsii.Number]:
            '''This property indicates the minimum object age in days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-matchobjectage.html#cfn-s3-storagelensgroup-matchobjectage-daysgreaterthan
            '''
            result = self._values.get("days_greater_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def days_less_than(self) -> typing.Optional[jsii.Number]:
            '''This property indicates the maximum object age in days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-matchobjectage.html#cfn-s3-storagelensgroup-matchobjectage-dayslessthan
            '''
            result = self._values.get("days_less_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchObjectAgeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bytes_greater_than": "bytesGreaterThan",
            "bytes_less_than": "bytesLessThan",
        },
    )
    class MatchObjectSizeProperty:
        def __init__(
            self,
            *,
            bytes_greater_than: typing.Optional[jsii.Number] = None,
            bytes_less_than: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''This resource filters objects that match the specified object size range.

            :param bytes_greater_than: This property specifies the minimum object size in bytes. The value must be a positive number, greater than 0 and less than 5 TB.
            :param bytes_less_than: This property specifies the maximum object size in bytes. The value must be a positive number, greater than the minimum object size and less than 5 TB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-matchobjectsize.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                match_object_size_property = s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                    bytes_greater_than=123,
                    bytes_less_than=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8699187dbe4d5b7c954d01c920c102265b9d468cef471fd81829f3b087655eef)
                check_type(argname="argument bytes_greater_than", value=bytes_greater_than, expected_type=type_hints["bytes_greater_than"])
                check_type(argname="argument bytes_less_than", value=bytes_less_than, expected_type=type_hints["bytes_less_than"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bytes_greater_than is not None:
                self._values["bytes_greater_than"] = bytes_greater_than
            if bytes_less_than is not None:
                self._values["bytes_less_than"] = bytes_less_than

        @builtins.property
        def bytes_greater_than(self) -> typing.Optional[jsii.Number]:
            '''This property specifies the minimum object size in bytes.

            The value must be a positive number, greater than 0 and less than 5 TB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-matchobjectsize.html#cfn-s3-storagelensgroup-matchobjectsize-bytesgreaterthan
            '''
            result = self._values.get("bytes_greater_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def bytes_less_than(self) -> typing.Optional[jsii.Number]:
            '''This property specifies the maximum object size in bytes.

            The value must be a positive number, greater than the minimum object size and less than 5 TB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-matchobjectsize.html#cfn-s3-storagelensgroup-matchobjectsize-byteslessthan
            '''
            result = self._values.get("bytes_less_than")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchObjectSizeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensGroupPropsMixin.OrProperty",
        jsii_struct_bases=[],
        name_mapping={
            "match_any_prefix": "matchAnyPrefix",
            "match_any_suffix": "matchAnySuffix",
            "match_any_tag": "matchAnyTag",
            "match_object_age": "matchObjectAge",
            "match_object_size": "matchObjectSize",
        },
    )
    class OrProperty:
        def __init__(
            self,
            *,
            match_any_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
            match_any_suffix: typing.Optional[typing.Sequence[builtins.str]] = None,
            match_any_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
            match_object_age: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            match_object_size: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This resource contains the ``Or`` logical operator, which allows multiple filter conditions to be joined for more complex comparisons of Storage Lens group data.

            Objects can match any of the listed filter conditions that are joined by the ``Or`` logical operator. Only one of each filter condition is allowed.

            :param match_any_prefix: This property contains a list of prefixes. At least one prefix must be specified. Up to 10 prefixes are allowed.
            :param match_any_suffix: This property contains the list of suffixes. At least one suffix must be specified. Up to 10 suffixes are allowed.
            :param match_any_tag: This property contains the list of S3 object tags. At least one object tag must be specified. Up to 10 object tags are allowed.
            :param match_object_age: This property filters objects that match the specified object age range.
            :param match_object_size: This property contains the ``BytesGreaterThan`` and ``BytesLessThan`` values to define the object size range (minimum and maximum number of Bytes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-or.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                or_property = s3_mixins.CfnStorageLensGroupPropsMixin.OrProperty(
                    match_any_prefix=["matchAnyPrefix"],
                    match_any_suffix=["matchAnySuffix"],
                    match_any_tag=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    match_object_age=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty(
                        days_greater_than=123,
                        days_less_than=123
                    ),
                    match_object_size=s3_mixins.CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty(
                        bytes_greater_than=123,
                        bytes_less_than=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4659c4bd66e7d90c1c6d1cb5d6b9e8b2d5ca71a0c604f3584a3babbccb68793)
                check_type(argname="argument match_any_prefix", value=match_any_prefix, expected_type=type_hints["match_any_prefix"])
                check_type(argname="argument match_any_suffix", value=match_any_suffix, expected_type=type_hints["match_any_suffix"])
                check_type(argname="argument match_any_tag", value=match_any_tag, expected_type=type_hints["match_any_tag"])
                check_type(argname="argument match_object_age", value=match_object_age, expected_type=type_hints["match_object_age"])
                check_type(argname="argument match_object_size", value=match_object_size, expected_type=type_hints["match_object_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if match_any_prefix is not None:
                self._values["match_any_prefix"] = match_any_prefix
            if match_any_suffix is not None:
                self._values["match_any_suffix"] = match_any_suffix
            if match_any_tag is not None:
                self._values["match_any_tag"] = match_any_tag
            if match_object_age is not None:
                self._values["match_object_age"] = match_object_age
            if match_object_size is not None:
                self._values["match_object_size"] = match_object_size

        @builtins.property
        def match_any_prefix(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property contains a list of prefixes.

            At least one prefix must be specified. Up to 10 prefixes are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-or.html#cfn-s3-storagelensgroup-or-matchanyprefix
            '''
            result = self._values.get("match_any_prefix")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def match_any_suffix(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property contains the list of suffixes.

            At least one suffix must be specified. Up to 10 suffixes are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-or.html#cfn-s3-storagelensgroup-or-matchanysuffix
            '''
            result = self._values.get("match_any_suffix")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def match_any_tag(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
            '''This property contains the list of S3 object tags.

            At least one object tag must be specified. Up to 10 object tags are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-or.html#cfn-s3-storagelensgroup-or-matchanytag
            '''
            result = self._values.get("match_any_tag")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

        @builtins.property
        def match_object_age(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty"]]:
            '''This property filters objects that match the specified object age range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-or.html#cfn-s3-storagelensgroup-or-matchobjectage
            '''
            result = self._values.get("match_object_age")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty"]], result)

        @builtins.property
        def match_object_size(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty"]]:
            '''This property contains the ``BytesGreaterThan`` and ``BytesLessThan`` values to define the object size range (minimum and maximum number of Bytes).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelensgroup-or.html#cfn-s3-storagelensgroup-or-matchobjectsize
            '''
            result = self._values.get("match_object_size")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "storage_lens_configuration": "storageLensConfiguration",
        "tags": "tags",
    },
)
class CfnStorageLensMixinProps:
    def __init__(
        self,
        *,
        storage_lens_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.StorageLensConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStorageLensPropsMixin.

        :param storage_lens_configuration: This resource contains the details Amazon S3 Storage Lens configuration.
        :param tags: A set of tags (key–value pairs) to associate with the Storage Lens configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
            
            # sses3: Any
            
            cfn_storage_lens_mixin_props = s3_mixins.CfnStorageLensMixinProps(
                storage_lens_configuration=s3_mixins.CfnStorageLensPropsMixin.StorageLensConfigurationProperty(
                    account_level=s3_mixins.CfnStorageLensPropsMixin.AccountLevelProperty(
                        activity_metrics=s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_cost_optimization_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_data_protection_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_performance_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                            is_enabled=False
                        ),
                        bucket_level=s3_mixins.CfnStorageLensPropsMixin.BucketLevelProperty(
                            activity_metrics=s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                                is_enabled=False
                            ),
                            advanced_cost_optimization_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                                is_enabled=False
                            ),
                            advanced_data_protection_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                                is_enabled=False
                            ),
                            advanced_performance_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                                is_enabled=False
                            ),
                            detailed_status_codes_metrics=s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                                is_enabled=False
                            ),
                            prefix_level=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelProperty(
                                storage_metrics=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty(
                                    is_enabled=False,
                                    selection_criteria=s3_mixins.CfnStorageLensPropsMixin.SelectionCriteriaProperty(
                                        delimiter="delimiter",
                                        max_depth=123,
                                        min_storage_bytes_percentage=123
                                    )
                                )
                            )
                        ),
                        detailed_status_codes_metrics=s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                            is_enabled=False
                        ),
                        storage_lens_group_level=s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupLevelProperty(
                            storage_lens_group_selection_criteria=s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty(
                                exclude=["exclude"],
                                include=["include"]
                            )
                        )
                    ),
                    aws_org=s3_mixins.CfnStorageLensPropsMixin.AwsOrgProperty(
                        arn="arn"
                    ),
                    data_export=s3_mixins.CfnStorageLensPropsMixin.DataExportProperty(
                        cloud_watch_metrics=s3_mixins.CfnStorageLensPropsMixin.CloudWatchMetricsProperty(
                            is_enabled=False
                        ),
                        s3_bucket_destination=s3_mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty(
                            account_id="accountId",
                            arn="arn",
                            encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                                ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                    key_id="keyId"
                                ),
                                sses3=sses3
                            ),
                            format="format",
                            output_schema_version="outputSchemaVersion",
                            prefix="prefix"
                        ),
                        storage_lens_table_destination=s3_mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty(
                            encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                                ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                    key_id="keyId"
                                ),
                                sses3=sses3
                            ),
                            is_enabled=False
                        )
                    ),
                    exclude=s3_mixins.CfnStorageLensPropsMixin.BucketsAndRegionsProperty(
                        buckets=["buckets"],
                        regions=["regions"]
                    ),
                    expanded_prefixes_data_export=s3_mixins.CfnStorageLensPropsMixin.StorageLensExpandedPrefixesDataExportProperty(
                        s3_bucket_destination=s3_mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty(
                            account_id="accountId",
                            arn="arn",
                            encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                                ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                    key_id="keyId"
                                ),
                                sses3=sses3
                            ),
                            format="format",
                            output_schema_version="outputSchemaVersion",
                            prefix="prefix"
                        ),
                        storage_lens_table_destination=s3_mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty(
                            encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                                ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                    key_id="keyId"
                                ),
                                sses3=sses3
                            ),
                            is_enabled=False
                        )
                    ),
                    id="id",
                    include=s3_mixins.CfnStorageLensPropsMixin.BucketsAndRegionsProperty(
                        buckets=["buckets"],
                        regions=["regions"]
                    ),
                    is_enabled=False,
                    prefix_delimiter="prefixDelimiter",
                    storage_lens_arn="storageLensArn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5302d5961801bea27ca62e7f789bdcccb5e66dcef06529c2b903556435dec34)
            check_type(argname="argument storage_lens_configuration", value=storage_lens_configuration, expected_type=type_hints["storage_lens_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if storage_lens_configuration is not None:
            self._values["storage_lens_configuration"] = storage_lens_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def storage_lens_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensConfigurationProperty"]]:
        '''This resource contains the details Amazon S3 Storage Lens configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html#cfn-s3-storagelens-storagelensconfiguration
        '''
        result = self._values.get("storage_lens_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A set of tags (key–value pairs) to associate with the Storage Lens configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html#cfn-s3-storagelens-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStorageLensMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStorageLensPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin",
):
    '''The AWS::S3::StorageLens resource creates an Amazon S3 Storage Lens configuration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html
    :cloudformationResource: AWS::S3::StorageLens
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
        
        # sses3: Any
        
        cfn_storage_lens_props_mixin = s3_mixins.CfnStorageLensPropsMixin(s3_mixins.CfnStorageLensMixinProps(
            storage_lens_configuration=s3_mixins.CfnStorageLensPropsMixin.StorageLensConfigurationProperty(
                account_level=s3_mixins.CfnStorageLensPropsMixin.AccountLevelProperty(
                    activity_metrics=s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                        is_enabled=False
                    ),
                    advanced_cost_optimization_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                        is_enabled=False
                    ),
                    advanced_data_protection_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                        is_enabled=False
                    ),
                    advanced_performance_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                        is_enabled=False
                    ),
                    bucket_level=s3_mixins.CfnStorageLensPropsMixin.BucketLevelProperty(
                        activity_metrics=s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_cost_optimization_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_data_protection_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_performance_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                            is_enabled=False
                        ),
                        detailed_status_codes_metrics=s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                            is_enabled=False
                        ),
                        prefix_level=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelProperty(
                            storage_metrics=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty(
                                is_enabled=False,
                                selection_criteria=s3_mixins.CfnStorageLensPropsMixin.SelectionCriteriaProperty(
                                    delimiter="delimiter",
                                    max_depth=123,
                                    min_storage_bytes_percentage=123
                                )
                            )
                        )
                    ),
                    detailed_status_codes_metrics=s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                        is_enabled=False
                    ),
                    storage_lens_group_level=s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupLevelProperty(
                        storage_lens_group_selection_criteria=s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty(
                            exclude=["exclude"],
                            include=["include"]
                        )
                    )
                ),
                aws_org=s3_mixins.CfnStorageLensPropsMixin.AwsOrgProperty(
                    arn="arn"
                ),
                data_export=s3_mixins.CfnStorageLensPropsMixin.DataExportProperty(
                    cloud_watch_metrics=s3_mixins.CfnStorageLensPropsMixin.CloudWatchMetricsProperty(
                        is_enabled=False
                    ),
                    s3_bucket_destination=s3_mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty(
                        account_id="accountId",
                        arn="arn",
                        encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                            ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                key_id="keyId"
                            ),
                            sses3=sses3
                        ),
                        format="format",
                        output_schema_version="outputSchemaVersion",
                        prefix="prefix"
                    ),
                    storage_lens_table_destination=s3_mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty(
                        encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                            ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                key_id="keyId"
                            ),
                            sses3=sses3
                        ),
                        is_enabled=False
                    )
                ),
                exclude=s3_mixins.CfnStorageLensPropsMixin.BucketsAndRegionsProperty(
                    buckets=["buckets"],
                    regions=["regions"]
                ),
                expanded_prefixes_data_export=s3_mixins.CfnStorageLensPropsMixin.StorageLensExpandedPrefixesDataExportProperty(
                    s3_bucket_destination=s3_mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty(
                        account_id="accountId",
                        arn="arn",
                        encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                            ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                key_id="keyId"
                            ),
                            sses3=sses3
                        ),
                        format="format",
                        output_schema_version="outputSchemaVersion",
                        prefix="prefix"
                    ),
                    storage_lens_table_destination=s3_mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty(
                        encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                            ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                key_id="keyId"
                            ),
                            sses3=sses3
                        ),
                        is_enabled=False
                    )
                ),
                id="id",
                include=s3_mixins.CfnStorageLensPropsMixin.BucketsAndRegionsProperty(
                    buckets=["buckets"],
                    regions=["regions"]
                ),
                is_enabled=False,
                prefix_delimiter="prefixDelimiter",
                storage_lens_arn="storageLensArn"
            ),
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
        props: typing.Union[CfnStorageLensMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::S3::StorageLens``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a1654a1e996fe564733c1bbfaaf23198e628556131a0d6b6bd40231392d495)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd30fab91d72b8f2370d40d6ac324a33af8fae5622cf665fde0c6b47a30b90c2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346b5f50a2d3070dc98a9dddf7f1f55de8405110a30fb44660291a2b956c8aad)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStorageLensMixinProps:
        return typing.cast(CfnStorageLensMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.AccountLevelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "activity_metrics": "activityMetrics",
            "advanced_cost_optimization_metrics": "advancedCostOptimizationMetrics",
            "advanced_data_protection_metrics": "advancedDataProtectionMetrics",
            "advanced_performance_metrics": "advancedPerformanceMetrics",
            "bucket_level": "bucketLevel",
            "detailed_status_codes_metrics": "detailedStatusCodesMetrics",
            "storage_lens_group_level": "storageLensGroupLevel",
        },
    )
    class AccountLevelProperty:
        def __init__(
            self,
            *,
            activity_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.ActivityMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            advanced_cost_optimization_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            advanced_data_protection_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            advanced_performance_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            bucket_level: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.BucketLevelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            detailed_status_codes_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            storage_lens_group_level: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.StorageLensGroupLevelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This resource contains the details of the account-level metrics for Amazon S3 Storage Lens.

            :param activity_metrics: This property contains the details of account-level activity metrics for S3 Storage Lens.
            :param advanced_cost_optimization_metrics: This property contains the details of account-level advanced cost optimization metrics for S3 Storage Lens.
            :param advanced_data_protection_metrics: This property contains the details of account-level advanced data protection metrics for S3 Storage Lens.
            :param advanced_performance_metrics: Advanced Performance Metrics.
            :param bucket_level: This property contains the details of the account-level bucket-level configurations for Amazon S3 Storage Lens. To enable bucket-level configurations, make sure to also set the same metrics at the account level.
            :param detailed_status_codes_metrics: This property contains the details of account-level detailed status code metrics for S3 Storage Lens.
            :param storage_lens_group_level: This property determines the scope of Storage Lens group data that is displayed in the Storage Lens dashboard.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                account_level_property = s3_mixins.CfnStorageLensPropsMixin.AccountLevelProperty(
                    activity_metrics=s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                        is_enabled=False
                    ),
                    advanced_cost_optimization_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                        is_enabled=False
                    ),
                    advanced_data_protection_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                        is_enabled=False
                    ),
                    advanced_performance_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                        is_enabled=False
                    ),
                    bucket_level=s3_mixins.CfnStorageLensPropsMixin.BucketLevelProperty(
                        activity_metrics=s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_cost_optimization_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_data_protection_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_performance_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                            is_enabled=False
                        ),
                        detailed_status_codes_metrics=s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                            is_enabled=False
                        ),
                        prefix_level=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelProperty(
                            storage_metrics=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty(
                                is_enabled=False,
                                selection_criteria=s3_mixins.CfnStorageLensPropsMixin.SelectionCriteriaProperty(
                                    delimiter="delimiter",
                                    max_depth=123,
                                    min_storage_bytes_percentage=123
                                )
                            )
                        )
                    ),
                    detailed_status_codes_metrics=s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                        is_enabled=False
                    ),
                    storage_lens_group_level=s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupLevelProperty(
                        storage_lens_group_selection_criteria=s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty(
                            exclude=["exclude"],
                            include=["include"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7dd94050c0874e39c9eec5db42f0089e9020360ccf67303b60aceb1ee47737ce)
                check_type(argname="argument activity_metrics", value=activity_metrics, expected_type=type_hints["activity_metrics"])
                check_type(argname="argument advanced_cost_optimization_metrics", value=advanced_cost_optimization_metrics, expected_type=type_hints["advanced_cost_optimization_metrics"])
                check_type(argname="argument advanced_data_protection_metrics", value=advanced_data_protection_metrics, expected_type=type_hints["advanced_data_protection_metrics"])
                check_type(argname="argument advanced_performance_metrics", value=advanced_performance_metrics, expected_type=type_hints["advanced_performance_metrics"])
                check_type(argname="argument bucket_level", value=bucket_level, expected_type=type_hints["bucket_level"])
                check_type(argname="argument detailed_status_codes_metrics", value=detailed_status_codes_metrics, expected_type=type_hints["detailed_status_codes_metrics"])
                check_type(argname="argument storage_lens_group_level", value=storage_lens_group_level, expected_type=type_hints["storage_lens_group_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if activity_metrics is not None:
                self._values["activity_metrics"] = activity_metrics
            if advanced_cost_optimization_metrics is not None:
                self._values["advanced_cost_optimization_metrics"] = advanced_cost_optimization_metrics
            if advanced_data_protection_metrics is not None:
                self._values["advanced_data_protection_metrics"] = advanced_data_protection_metrics
            if advanced_performance_metrics is not None:
                self._values["advanced_performance_metrics"] = advanced_performance_metrics
            if bucket_level is not None:
                self._values["bucket_level"] = bucket_level
            if detailed_status_codes_metrics is not None:
                self._values["detailed_status_codes_metrics"] = detailed_status_codes_metrics
            if storage_lens_group_level is not None:
                self._values["storage_lens_group_level"] = storage_lens_group_level

        @builtins.property
        def activity_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.ActivityMetricsProperty"]]:
            '''This property contains the details of account-level activity metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html#cfn-s3-storagelens-accountlevel-activitymetrics
            '''
            result = self._values.get("activity_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.ActivityMetricsProperty"]], result)

        @builtins.property
        def advanced_cost_optimization_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty"]]:
            '''This property contains the details of account-level advanced cost optimization metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html#cfn-s3-storagelens-accountlevel-advancedcostoptimizationmetrics
            '''
            result = self._values.get("advanced_cost_optimization_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty"]], result)

        @builtins.property
        def advanced_data_protection_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty"]]:
            '''This property contains the details of account-level advanced data protection metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html#cfn-s3-storagelens-accountlevel-advanceddataprotectionmetrics
            '''
            result = self._values.get("advanced_data_protection_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty"]], result)

        @builtins.property
        def advanced_performance_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty"]]:
            '''Advanced Performance Metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html#cfn-s3-storagelens-accountlevel-advancedperformancemetrics
            '''
            result = self._values.get("advanced_performance_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty"]], result)

        @builtins.property
        def bucket_level(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.BucketLevelProperty"]]:
            '''This property contains the details of the account-level bucket-level configurations for Amazon S3 Storage Lens.

            To enable bucket-level configurations, make sure to also set the same metrics at the account level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html#cfn-s3-storagelens-accountlevel-bucketlevel
            '''
            result = self._values.get("bucket_level")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.BucketLevelProperty"]], result)

        @builtins.property
        def detailed_status_codes_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty"]]:
            '''This property contains the details of account-level detailed status code metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html#cfn-s3-storagelens-accountlevel-detailedstatuscodesmetrics
            '''
            result = self._values.get("detailed_status_codes_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty"]], result)

        @builtins.property
        def storage_lens_group_level(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensGroupLevelProperty"]]:
            '''This property determines the scope of Storage Lens group data that is displayed in the Storage Lens dashboard.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html#cfn-s3-storagelens-accountlevel-storagelensgrouplevel
            '''
            result = self._values.get("storage_lens_group_level")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensGroupLevelProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountLevelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty",
        jsii_struct_bases=[],
        name_mapping={"is_enabled": "isEnabled"},
    )
    class ActivityMetricsProperty:
        def __init__(
            self,
            *,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''This resource enables Amazon S3 Storage Lens activity metrics.

            Activity metrics show details about how your storage is requested, such as requests (for example, All requests, Get requests, Put requests), bytes uploaded or downloaded, and errors.

            For more information, see `Assessing your storage activity and usage with S3 Storage Lens <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html>`_ in the *Amazon S3 User Guide* . For a complete list of metrics, see `S3 Storage Lens metrics glossary <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens_metrics_glossary.html>`_ in the *Amazon S3 User Guide* .

            :param is_enabled: A property that indicates whether the activity metrics is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-activitymetrics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                activity_metrics_property = s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                    is_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d241db1c23fe443e57cce902531a349e1ac3fcf6c5732575ff2dbae14d3ba2c6)
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A property that indicates whether the activity metrics is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-activitymetrics.html#cfn-s3-storagelens-activitymetrics-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActivityMetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty",
        jsii_struct_bases=[],
        name_mapping={"is_enabled": "isEnabled"},
    )
    class AdvancedCostOptimizationMetricsProperty:
        def __init__(
            self,
            *,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''This resource enables Amazon S3 Storage Lens advanced cost optimization metrics.

            Advanced cost optimization metrics provide insights that you can use to manage and optimize your storage costs, for example, lifecycle rule counts for transitions, expirations, and incomplete multipart uploads.

            For more information, see `Assessing your storage activity and usage with S3 Storage Lens <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html>`_ in the *Amazon S3 User Guide* . For a complete list of metrics, see `S3 Storage Lens metrics glossary <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens_metrics_glossary.html>`_ in the *Amazon S3 User Guide* .

            :param is_enabled: Indicates whether advanced cost optimization metrics are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-advancedcostoptimizationmetrics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                advanced_cost_optimization_metrics_property = s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                    is_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e7678c3007adb96e428e572c1607f475d80e7ec26e8c39b3a49de335270b8db)
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether advanced cost optimization metrics are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-advancedcostoptimizationmetrics.html#cfn-s3-storagelens-advancedcostoptimizationmetrics-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedCostOptimizationMetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty",
        jsii_struct_bases=[],
        name_mapping={"is_enabled": "isEnabled"},
    )
    class AdvancedDataProtectionMetricsProperty:
        def __init__(
            self,
            *,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''This resource enables Amazon S3 Storage Lens advanced data protection metrics.

            Advanced data protection metrics provide insights that you can use to perform audits and protect your data, for example replication rule counts within and across Regions.

            For more information, see `Assessing your storage activity and usage with S3 Storage Lens <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html>`_ in the *Amazon S3 User Guide* . For a complete list of metrics, see `S3 Storage Lens metrics glossary <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens_metrics_glossary.html>`_ in the *Amazon S3 User Guide* .

            :param is_enabled: Indicates whether advanced data protection metrics are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-advanceddataprotectionmetrics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                advanced_data_protection_metrics_property = s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                    is_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__21e50fba85426f5da5848900a588a07dd594b47dab962c9a520b582539bb1350)
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether advanced data protection metrics are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-advanceddataprotectionmetrics.html#cfn-s3-storagelens-advanceddataprotectionmetrics-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedDataProtectionMetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty",
        jsii_struct_bases=[],
        name_mapping={"is_enabled": "isEnabled"},
    )
    class AdvancedPerformanceMetricsProperty:
        def __init__(
            self,
            *,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Advanced Performance Metrics.

            :param is_enabled: Specifies whether the Advanced Performance Metrics is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-advancedperformancemetrics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                advanced_performance_metrics_property = s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                    is_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42ba9314b98b8401c488777f79deb605b5e78fdb91b59ab2b5948f65fca98c5e)
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the Advanced Performance Metrics is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-advancedperformancemetrics.html#cfn-s3-storagelens-advancedperformancemetrics-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedPerformanceMetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.AwsOrgProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class AwsOrgProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''This resource contains the details of the AWS Organization for Amazon S3 Storage Lens.

            :param arn: This resource contains the ARN of the AWS Organization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-awsorg.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                aws_org_property = s3_mixins.CfnStorageLensPropsMixin.AwsOrgProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__263598804c0e04d8fc9c6c293ceac4d892e106f87d179f9bd11b72a19f99364b)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''This resource contains the ARN of the AWS Organization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-awsorg.html#cfn-s3-storagelens-awsorg-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsOrgProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.BucketLevelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "activity_metrics": "activityMetrics",
            "advanced_cost_optimization_metrics": "advancedCostOptimizationMetrics",
            "advanced_data_protection_metrics": "advancedDataProtectionMetrics",
            "advanced_performance_metrics": "advancedPerformanceMetrics",
            "detailed_status_codes_metrics": "detailedStatusCodesMetrics",
            "prefix_level": "prefixLevel",
        },
    )
    class BucketLevelProperty:
        def __init__(
            self,
            *,
            activity_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.ActivityMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            advanced_cost_optimization_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            advanced_data_protection_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            advanced_performance_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            detailed_status_codes_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            prefix_level: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.PrefixLevelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A property for the bucket-level storage metrics for Amazon S3 Storage Lens.

            :param activity_metrics: A property for bucket-level activity metrics for S3 Storage Lens.
            :param advanced_cost_optimization_metrics: A property for bucket-level advanced cost optimization metrics for S3 Storage Lens.
            :param advanced_data_protection_metrics: A property for bucket-level advanced data protection metrics for S3 Storage Lens.
            :param advanced_performance_metrics: Advanced Performance Metrics.
            :param detailed_status_codes_metrics: A property for bucket-level detailed status code metrics for S3 Storage Lens.
            :param prefix_level: A property for bucket-level prefix-level storage metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                bucket_level_property = s3_mixins.CfnStorageLensPropsMixin.BucketLevelProperty(
                    activity_metrics=s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                        is_enabled=False
                    ),
                    advanced_cost_optimization_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                        is_enabled=False
                    ),
                    advanced_data_protection_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                        is_enabled=False
                    ),
                    advanced_performance_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                        is_enabled=False
                    ),
                    detailed_status_codes_metrics=s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                        is_enabled=False
                    ),
                    prefix_level=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelProperty(
                        storage_metrics=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty(
                            is_enabled=False,
                            selection_criteria=s3_mixins.CfnStorageLensPropsMixin.SelectionCriteriaProperty(
                                delimiter="delimiter",
                                max_depth=123,
                                min_storage_bytes_percentage=123
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__973971fab07626ed79d92bf1a19f85d04447bfa6a94d42ded03e8947f6dd2b39)
                check_type(argname="argument activity_metrics", value=activity_metrics, expected_type=type_hints["activity_metrics"])
                check_type(argname="argument advanced_cost_optimization_metrics", value=advanced_cost_optimization_metrics, expected_type=type_hints["advanced_cost_optimization_metrics"])
                check_type(argname="argument advanced_data_protection_metrics", value=advanced_data_protection_metrics, expected_type=type_hints["advanced_data_protection_metrics"])
                check_type(argname="argument advanced_performance_metrics", value=advanced_performance_metrics, expected_type=type_hints["advanced_performance_metrics"])
                check_type(argname="argument detailed_status_codes_metrics", value=detailed_status_codes_metrics, expected_type=type_hints["detailed_status_codes_metrics"])
                check_type(argname="argument prefix_level", value=prefix_level, expected_type=type_hints["prefix_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if activity_metrics is not None:
                self._values["activity_metrics"] = activity_metrics
            if advanced_cost_optimization_metrics is not None:
                self._values["advanced_cost_optimization_metrics"] = advanced_cost_optimization_metrics
            if advanced_data_protection_metrics is not None:
                self._values["advanced_data_protection_metrics"] = advanced_data_protection_metrics
            if advanced_performance_metrics is not None:
                self._values["advanced_performance_metrics"] = advanced_performance_metrics
            if detailed_status_codes_metrics is not None:
                self._values["detailed_status_codes_metrics"] = detailed_status_codes_metrics
            if prefix_level is not None:
                self._values["prefix_level"] = prefix_level

        @builtins.property
        def activity_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.ActivityMetricsProperty"]]:
            '''A property for bucket-level activity metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html#cfn-s3-storagelens-bucketlevel-activitymetrics
            '''
            result = self._values.get("activity_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.ActivityMetricsProperty"]], result)

        @builtins.property
        def advanced_cost_optimization_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty"]]:
            '''A property for bucket-level advanced cost optimization metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html#cfn-s3-storagelens-bucketlevel-advancedcostoptimizationmetrics
            '''
            result = self._values.get("advanced_cost_optimization_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty"]], result)

        @builtins.property
        def advanced_data_protection_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty"]]:
            '''A property for bucket-level advanced data protection metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html#cfn-s3-storagelens-bucketlevel-advanceddataprotectionmetrics
            '''
            result = self._values.get("advanced_data_protection_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty"]], result)

        @builtins.property
        def advanced_performance_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty"]]:
            '''Advanced Performance Metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html#cfn-s3-storagelens-bucketlevel-advancedperformancemetrics
            '''
            result = self._values.get("advanced_performance_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty"]], result)

        @builtins.property
        def detailed_status_codes_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty"]]:
            '''A property for bucket-level detailed status code metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html#cfn-s3-storagelens-bucketlevel-detailedstatuscodesmetrics
            '''
            result = self._values.get("detailed_status_codes_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty"]], result)

        @builtins.property
        def prefix_level(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.PrefixLevelProperty"]]:
            '''A property for bucket-level prefix-level storage metrics for S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html#cfn-s3-storagelens-bucketlevel-prefixlevel
            '''
            result = self._values.get("prefix_level")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.PrefixLevelProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketLevelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.BucketsAndRegionsProperty",
        jsii_struct_bases=[],
        name_mapping={"buckets": "buckets", "regions": "regions"},
    )
    class BucketsAndRegionsProperty:
        def __init__(
            self,
            *,
            buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
            regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This resource contains the details of the buckets and Regions for the Amazon S3 Storage Lens configuration.

            :param buckets: This property contains the details of the buckets for the Amazon S3 Storage Lens configuration. This should be the bucket Amazon Resource Name(ARN). For valid values, see `Buckets ARN format here <https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_Include.html#API_control_Include_Contents>`_ in the *Amazon S3 API Reference* .
            :param regions: This property contains the details of the Regions for the S3 Storage Lens configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketsandregions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                buckets_and_regions_property = s3_mixins.CfnStorageLensPropsMixin.BucketsAndRegionsProperty(
                    buckets=["buckets"],
                    regions=["regions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0b65e25a5c0b1040054ea426eb49c97ab8b7c8357c9f7d593e2b8ac5d15a2f8)
                check_type(argname="argument buckets", value=buckets, expected_type=type_hints["buckets"])
                check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if buckets is not None:
                self._values["buckets"] = buckets
            if regions is not None:
                self._values["regions"] = regions

        @builtins.property
        def buckets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property contains the details of the buckets for the Amazon S3 Storage Lens configuration.

            This should be the bucket Amazon Resource Name(ARN). For valid values, see `Buckets ARN format here <https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_Include.html#API_control_Include_Contents>`_ in the *Amazon S3 API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketsandregions.html#cfn-s3-storagelens-bucketsandregions-buckets
            '''
            result = self._values.get("buckets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property contains the details of the Regions for the S3 Storage Lens configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketsandregions.html#cfn-s3-storagelens-bucketsandregions-regions
            '''
            result = self._values.get("regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketsAndRegionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.CloudWatchMetricsProperty",
        jsii_struct_bases=[],
        name_mapping={"is_enabled": "isEnabled"},
    )
    class CloudWatchMetricsProperty:
        def __init__(
            self,
            *,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''This resource enables the Amazon CloudWatch publishing option for Amazon S3 Storage Lens metrics.

            For more information, see `Monitor S3 Storage Lens metrics in CloudWatch <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens_view_metrics_cloudwatch.html>`_ in the *Amazon S3 User Guide* .

            :param is_enabled: This property identifies whether the CloudWatch publishing option for S3 Storage Lens is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-cloudwatchmetrics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                cloud_watch_metrics_property = s3_mixins.CfnStorageLensPropsMixin.CloudWatchMetricsProperty(
                    is_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45033ba3423020553245d401b9ba019c42753d0957e92d48d26624fe7fd422c8)
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This property identifies whether the CloudWatch publishing option for S3 Storage Lens is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-cloudwatchmetrics.html#cfn-s3-storagelens-cloudwatchmetrics-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchMetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.DataExportProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_metrics": "cloudWatchMetrics",
            "s3_bucket_destination": "s3BucketDestination",
            "storage_lens_table_destination": "storageLensTableDestination",
        },
    )
    class DataExportProperty:
        def __init__(
            self,
            *,
            cloud_watch_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.CloudWatchMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_bucket_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.S3BucketDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            storage_lens_table_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.StorageLensTableDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This resource contains the details of the Amazon S3 Storage Lens metrics export.

            :param cloud_watch_metrics: This property enables the Amazon CloudWatch publishing option for S3 Storage Lens metrics.
            :param s3_bucket_destination: This property contains the details of the bucket where the S3 Storage Lens metrics export will be placed.
            :param storage_lens_table_destination: S3 Tables destination settings for the Amazon S3 Storage Lens metrics export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-dataexport.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                # sses3: Any
                
                data_export_property = s3_mixins.CfnStorageLensPropsMixin.DataExportProperty(
                    cloud_watch_metrics=s3_mixins.CfnStorageLensPropsMixin.CloudWatchMetricsProperty(
                        is_enabled=False
                    ),
                    s3_bucket_destination=s3_mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty(
                        account_id="accountId",
                        arn="arn",
                        encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                            ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                key_id="keyId"
                            ),
                            sses3=sses3
                        ),
                        format="format",
                        output_schema_version="outputSchemaVersion",
                        prefix="prefix"
                    ),
                    storage_lens_table_destination=s3_mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty(
                        encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                            ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                key_id="keyId"
                            ),
                            sses3=sses3
                        ),
                        is_enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__25b99046d248317730675d1adc64e2e024edad3ad623dc4d372ae2b261e10e25)
                check_type(argname="argument cloud_watch_metrics", value=cloud_watch_metrics, expected_type=type_hints["cloud_watch_metrics"])
                check_type(argname="argument s3_bucket_destination", value=s3_bucket_destination, expected_type=type_hints["s3_bucket_destination"])
                check_type(argname="argument storage_lens_table_destination", value=storage_lens_table_destination, expected_type=type_hints["storage_lens_table_destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_metrics is not None:
                self._values["cloud_watch_metrics"] = cloud_watch_metrics
            if s3_bucket_destination is not None:
                self._values["s3_bucket_destination"] = s3_bucket_destination
            if storage_lens_table_destination is not None:
                self._values["storage_lens_table_destination"] = storage_lens_table_destination

        @builtins.property
        def cloud_watch_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.CloudWatchMetricsProperty"]]:
            '''This property enables the Amazon CloudWatch publishing option for S3 Storage Lens metrics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-dataexport.html#cfn-s3-storagelens-dataexport-cloudwatchmetrics
            '''
            result = self._values.get("cloud_watch_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.CloudWatchMetricsProperty"]], result)

        @builtins.property
        def s3_bucket_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.S3BucketDestinationProperty"]]:
            '''This property contains the details of the bucket where the S3 Storage Lens metrics export will be placed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-dataexport.html#cfn-s3-storagelens-dataexport-s3bucketdestination
            '''
            result = self._values.get("s3_bucket_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.S3BucketDestinationProperty"]], result)

        @builtins.property
        def storage_lens_table_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensTableDestinationProperty"]]:
            '''S3 Tables destination settings for the Amazon S3 Storage Lens metrics export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-dataexport.html#cfn-s3-storagelens-dataexport-storagelenstabledestination
            '''
            result = self._values.get("storage_lens_table_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensTableDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataExportProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty",
        jsii_struct_bases=[],
        name_mapping={"is_enabled": "isEnabled"},
    )
    class DetailedStatusCodesMetricsProperty:
        def __init__(
            self,
            *,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''This resource enables Amazon S3 Storage Lens detailed status code metrics.

            Detailed status code metrics generate metrics for HTTP status codes, such as ``200 OK`` , ``403 Forbidden`` , ``503 Service Unavailable`` and others.

            For more information, see `Assessing your storage activity and usage with S3 Storage Lens <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html>`_ in the *Amazon S3 User Guide* . For a complete list of metrics, see `S3 Storage Lens metrics glossary <https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens_metrics_glossary.html>`_ in the *Amazon S3 User Guide* .

            :param is_enabled: Indicates whether detailed status code metrics are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-detailedstatuscodesmetrics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                detailed_status_codes_metrics_property = s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                    is_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__919be7d62e6d428c9c835251bba65541537549f2ed02701885e804f944ebfa84)
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether detailed status code metrics are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-detailedstatuscodesmetrics.html#cfn-s3-storagelens-detailedstatuscodesmetrics-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DetailedStatusCodesMetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"ssekms": "ssekms", "sses3": "sses3"},
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            ssekms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.SSEKMSProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sses3: typing.Any = None,
        ) -> None:
            '''This resource contains the type of server-side encryption used to encrypt an Amazon S3 Storage Lens metrics export.

            For valid values, see the `StorageLensDataExportEncryption <https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_StorageLensDataExportEncryption.html>`_ in the *Amazon S3 API Reference* .

            :param ssekms: Specifies the use of AWS Key Management Service keys (SSE-KMS) to encrypt the S3 Storage Lens metrics export file.
            :param sses3: Specifies the use of an Amazon S3-managed key (SSE-S3) to encrypt the S3 Storage Lens metrics export file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                # sses3: Any
                
                encryption_property = s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                    ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                        key_id="keyId"
                    ),
                    sses3=sses3
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__495fa64b373cef3d00461464358a46d7639949cb19abcfbb1888ba041688df9d)
                check_type(argname="argument ssekms", value=ssekms, expected_type=type_hints["ssekms"])
                check_type(argname="argument sses3", value=sses3, expected_type=type_hints["sses3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ssekms is not None:
                self._values["ssekms"] = ssekms
            if sses3 is not None:
                self._values["sses3"] = sses3

        @builtins.property
        def ssekms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.SSEKMSProperty"]]:
            '''Specifies the use of AWS Key Management Service keys (SSE-KMS) to encrypt the S3 Storage Lens metrics export file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-encryption.html#cfn-s3-storagelens-encryption-ssekms
            '''
            result = self._values.get("ssekms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.SSEKMSProperty"]], result)

        @builtins.property
        def sses3(self) -> typing.Any:
            '''Specifies the use of an Amazon S3-managed key (SSE-S3) to encrypt the S3 Storage Lens metrics export file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-encryption.html#cfn-s3-storagelens-encryption-sses3
            '''
            result = self._values.get("sses3")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.PrefixLevelProperty",
        jsii_struct_bases=[],
        name_mapping={"storage_metrics": "storageMetrics"},
    )
    class PrefixLevelProperty:
        def __init__(
            self,
            *,
            storage_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This resource contains the details of the prefix-level of the Amazon S3 Storage Lens.

            :param storage_metrics: A property for the prefix-level storage metrics for Amazon S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                prefix_level_property = s3_mixins.CfnStorageLensPropsMixin.PrefixLevelProperty(
                    storage_metrics=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty(
                        is_enabled=False,
                        selection_criteria=s3_mixins.CfnStorageLensPropsMixin.SelectionCriteriaProperty(
                            delimiter="delimiter",
                            max_depth=123,
                            min_storage_bytes_percentage=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd8cc294b63b63079558c34c29ff76bbe8a9bf2401479cb531a4c8a7e94dbde2)
                check_type(argname="argument storage_metrics", value=storage_metrics, expected_type=type_hints["storage_metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if storage_metrics is not None:
                self._values["storage_metrics"] = storage_metrics

        @builtins.property
        def storage_metrics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty"]]:
            '''A property for the prefix-level storage metrics for Amazon S3 Storage Lens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevel.html#cfn-s3-storagelens-prefixlevel-storagemetrics
            '''
            result = self._values.get("storage_metrics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrefixLevelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "is_enabled": "isEnabled",
            "selection_criteria": "selectionCriteria",
        },
    )
    class PrefixLevelStorageMetricsProperty:
        def __init__(
            self,
            *,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            selection_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.SelectionCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This resource contains the details of the prefix-level storage metrics for Amazon S3 Storage Lens.

            :param is_enabled: This property identifies whether the details of the prefix-level storage metrics for S3 Storage Lens are enabled.
            :param selection_criteria: This property identifies whether the details of the prefix-level storage metrics for S3 Storage Lens are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevelstoragemetrics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                prefix_level_storage_metrics_property = s3_mixins.CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty(
                    is_enabled=False,
                    selection_criteria=s3_mixins.CfnStorageLensPropsMixin.SelectionCriteriaProperty(
                        delimiter="delimiter",
                        max_depth=123,
                        min_storage_bytes_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__479caa06ce603b6cb1fb538b9a25b201132cd3d2a3daf8d95efbff4831e88533)
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
                check_type(argname="argument selection_criteria", value=selection_criteria, expected_type=type_hints["selection_criteria"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled
            if selection_criteria is not None:
                self._values["selection_criteria"] = selection_criteria

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This property identifies whether the details of the prefix-level storage metrics for S3 Storage Lens are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevelstoragemetrics.html#cfn-s3-storagelens-prefixlevelstoragemetrics-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def selection_criteria(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.SelectionCriteriaProperty"]]:
            '''This property identifies whether the details of the prefix-level storage metrics for S3 Storage Lens are enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevelstoragemetrics.html#cfn-s3-storagelens-prefixlevelstoragemetrics-selectioncriteria
            '''
            result = self._values.get("selection_criteria")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.SelectionCriteriaProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrefixLevelStorageMetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "arn": "arn",
            "encryption": "encryption",
            "format": "format",
            "output_schema_version": "outputSchemaVersion",
            "prefix": "prefix",
        },
    )
    class S3BucketDestinationProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            arn: typing.Optional[builtins.str] = None,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            format: typing.Optional[builtins.str] = None,
            output_schema_version: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This resource contains the details of the bucket where the Amazon S3 Storage Lens metrics export will be placed.

            :param account_id: This property contains the details of the AWS account ID of the S3 Storage Lens export bucket destination.
            :param arn: This property contains the details of the ARN of the bucket destination of the S3 Storage Lens export.
            :param encryption: This property contains the details of the encryption of the bucket destination of the Amazon S3 Storage Lens metrics export.
            :param format: This property contains the details of the format of the S3 Storage Lens export bucket destination.
            :param output_schema_version: This property contains the details of the output schema version of the S3 Storage Lens export bucket destination.
            :param prefix: This property contains the details of the prefix of the bucket destination of the S3 Storage Lens export .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                # sses3: Any
                
                s3_bucket_destination_property = s3_mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty(
                    account_id="accountId",
                    arn="arn",
                    encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                        ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                            key_id="keyId"
                        ),
                        sses3=sses3
                    ),
                    format="format",
                    output_schema_version="outputSchemaVersion",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfe5c81092876e6ffcb7dd4dd9c7e6a0c2c9a90f5926593938f9ba06f0e61cdf)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument output_schema_version", value=output_schema_version, expected_type=type_hints["output_schema_version"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if arn is not None:
                self._values["arn"] = arn
            if encryption is not None:
                self._values["encryption"] = encryption
            if format is not None:
                self._values["format"] = format
            if output_schema_version is not None:
                self._values["output_schema_version"] = output_schema_version
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''This property contains the details of the AWS account ID of the S3 Storage Lens export bucket destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''This property contains the details of the ARN of the bucket destination of the S3 Storage Lens export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.EncryptionProperty"]]:
            '''This property contains the details of the encryption of the bucket destination of the Amazon S3 Storage Lens metrics export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.EncryptionProperty"]], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''This property contains the details of the format of the S3 Storage Lens export bucket destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_schema_version(self) -> typing.Optional[builtins.str]:
            '''This property contains the details of the output schema version of the S3 Storage Lens export bucket destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-outputschemaversion
            '''
            result = self._values.get("output_schema_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''This property contains the details of the prefix of the bucket destination of the S3 Storage Lens export .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.SSEKMSProperty",
        jsii_struct_bases=[],
        name_mapping={"key_id": "keyId"},
    )
    class SSEKMSProperty:
        def __init__(self, *, key_id: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the use of server-side encryption using an AWS Key Management Service key (SSE-KMS) to encrypt the delivered S3 Storage Lens metrics export file.

            :param key_id: Specifies the Amazon Resource Name (ARN) of the customer managed AWS key to use for encrypting the S3 Storage Lens metrics export file. Amazon S3 only supports symmetric encryption keys. For more information, see `Special-purpose keys <https://docs.aws.amazon.com/kms/latest/developerguide/key-types.html>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-ssekms.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                s_sEKMSProperty = s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                    key_id="keyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c48fc8c0507516ae26ae4f74a3c205fd7fe7b84db1bbe064e18d1be9d15b3a9)
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_id is not None:
                self._values["key_id"] = key_id

        @builtins.property
        def key_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the Amazon Resource Name (ARN) of the customer managed AWS  key to use for encrypting the S3 Storage Lens metrics export file.

            Amazon S3 only supports symmetric encryption keys. For more information, see `Special-purpose keys <https://docs.aws.amazon.com/kms/latest/developerguide/key-types.html>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-ssekms.html#cfn-s3-storagelens-ssekms-keyid
            '''
            result = self._values.get("key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSEKMSProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.SelectionCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delimiter": "delimiter",
            "max_depth": "maxDepth",
            "min_storage_bytes_percentage": "minStorageBytesPercentage",
        },
    )
    class SelectionCriteriaProperty:
        def __init__(
            self,
            *,
            delimiter: typing.Optional[builtins.str] = None,
            max_depth: typing.Optional[jsii.Number] = None,
            min_storage_bytes_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''This resource contains the details of the Amazon S3 Storage Lens selection criteria.

            :param delimiter: This property contains the details of the S3 Storage Lens delimiter being used.
            :param max_depth: This property contains the details of the max depth that S3 Storage Lens will collect metrics up to.
            :param min_storage_bytes_percentage: This property contains the details of the minimum storage bytes percentage threshold that S3 Storage Lens will collect metrics up to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-selectioncriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                selection_criteria_property = s3_mixins.CfnStorageLensPropsMixin.SelectionCriteriaProperty(
                    delimiter="delimiter",
                    max_depth=123,
                    min_storage_bytes_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b8388be336d55ebbb01053ed9cb1c40522292958177b16da50aa01a1b000ce91)
                check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
                check_type(argname="argument max_depth", value=max_depth, expected_type=type_hints["max_depth"])
                check_type(argname="argument min_storage_bytes_percentage", value=min_storage_bytes_percentage, expected_type=type_hints["min_storage_bytes_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if max_depth is not None:
                self._values["max_depth"] = max_depth
            if min_storage_bytes_percentage is not None:
                self._values["min_storage_bytes_percentage"] = min_storage_bytes_percentage

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''This property contains the details of the S3 Storage Lens delimiter being used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-selectioncriteria.html#cfn-s3-storagelens-selectioncriteria-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_depth(self) -> typing.Optional[jsii.Number]:
            '''This property contains the details of the max depth that S3 Storage Lens will collect metrics up to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-selectioncriteria.html#cfn-s3-storagelens-selectioncriteria-maxdepth
            '''
            result = self._values.get("max_depth")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_storage_bytes_percentage(self) -> typing.Optional[jsii.Number]:
            '''This property contains the details of the minimum storage bytes percentage threshold that S3 Storage Lens will collect metrics up to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-selectioncriteria.html#cfn-s3-storagelens-selectioncriteria-minstoragebytespercentage
            '''
            result = self._values.get("min_storage_bytes_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelectionCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.StorageLensConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_level": "accountLevel",
            "aws_org": "awsOrg",
            "data_export": "dataExport",
            "exclude": "exclude",
            "expanded_prefixes_data_export": "expandedPrefixesDataExport",
            "id": "id",
            "include": "include",
            "is_enabled": "isEnabled",
            "prefix_delimiter": "prefixDelimiter",
            "storage_lens_arn": "storageLensArn",
        },
    )
    class StorageLensConfigurationProperty:
        def __init__(
            self,
            *,
            account_level: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.AccountLevelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            aws_org: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.AwsOrgProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            data_export: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.DataExportProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exclude: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.BucketsAndRegionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            expanded_prefixes_data_export: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.StorageLensExpandedPrefixesDataExportProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            id: typing.Optional[builtins.str] = None,
            include: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.BucketsAndRegionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            prefix_delimiter: typing.Optional[builtins.str] = None,
            storage_lens_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This is the property of the Amazon S3 Storage Lens configuration.

            :param account_level: This property contains the details of the account-level metrics for Amazon S3 Storage Lens configuration.
            :param aws_org: This property contains the details of the AWS Organization for the S3 Storage Lens configuration.
            :param data_export: This property contains the details of this S3 Storage Lens configuration's metrics export.
            :param exclude: This property contains the details of the bucket and or Regions excluded for Amazon S3 Storage Lens configuration.
            :param expanded_prefixes_data_export: Expanded Prefixes Data Export.
            :param id: This property contains the details of the ID of the S3 Storage Lens configuration.
            :param include: This property contains the details of the bucket and or Regions included for Amazon S3 Storage Lens configuration.
            :param is_enabled: This property contains the details of whether the Amazon S3 Storage Lens configuration is enabled.
            :param prefix_delimiter: The delimiter to divide S3 key into hierarchy of prefixes.
            :param storage_lens_arn: This property contains the details of the ARN of the S3 Storage Lens configuration. This property is read-only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                # sses3: Any
                
                storage_lens_configuration_property = s3_mixins.CfnStorageLensPropsMixin.StorageLensConfigurationProperty(
                    account_level=s3_mixins.CfnStorageLensPropsMixin.AccountLevelProperty(
                        activity_metrics=s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_cost_optimization_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_data_protection_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                            is_enabled=False
                        ),
                        advanced_performance_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                            is_enabled=False
                        ),
                        bucket_level=s3_mixins.CfnStorageLensPropsMixin.BucketLevelProperty(
                            activity_metrics=s3_mixins.CfnStorageLensPropsMixin.ActivityMetricsProperty(
                                is_enabled=False
                            ),
                            advanced_cost_optimization_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty(
                                is_enabled=False
                            ),
                            advanced_data_protection_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty(
                                is_enabled=False
                            ),
                            advanced_performance_metrics=s3_mixins.CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty(
                                is_enabled=False
                            ),
                            detailed_status_codes_metrics=s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                                is_enabled=False
                            ),
                            prefix_level=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelProperty(
                                storage_metrics=s3_mixins.CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty(
                                    is_enabled=False,
                                    selection_criteria=s3_mixins.CfnStorageLensPropsMixin.SelectionCriteriaProperty(
                                        delimiter="delimiter",
                                        max_depth=123,
                                        min_storage_bytes_percentage=123
                                    )
                                )
                            )
                        ),
                        detailed_status_codes_metrics=s3_mixins.CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty(
                            is_enabled=False
                        ),
                        storage_lens_group_level=s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupLevelProperty(
                            storage_lens_group_selection_criteria=s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty(
                                exclude=["exclude"],
                                include=["include"]
                            )
                        )
                    ),
                    aws_org=s3_mixins.CfnStorageLensPropsMixin.AwsOrgProperty(
                        arn="arn"
                    ),
                    data_export=s3_mixins.CfnStorageLensPropsMixin.DataExportProperty(
                        cloud_watch_metrics=s3_mixins.CfnStorageLensPropsMixin.CloudWatchMetricsProperty(
                            is_enabled=False
                        ),
                        s3_bucket_destination=s3_mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty(
                            account_id="accountId",
                            arn="arn",
                            encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                                ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                    key_id="keyId"
                                ),
                                sses3=sses3
                            ),
                            format="format",
                            output_schema_version="outputSchemaVersion",
                            prefix="prefix"
                        ),
                        storage_lens_table_destination=s3_mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty(
                            encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                                ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                    key_id="keyId"
                                ),
                                sses3=sses3
                            ),
                            is_enabled=False
                        )
                    ),
                    exclude=s3_mixins.CfnStorageLensPropsMixin.BucketsAndRegionsProperty(
                        buckets=["buckets"],
                        regions=["regions"]
                    ),
                    expanded_prefixes_data_export=s3_mixins.CfnStorageLensPropsMixin.StorageLensExpandedPrefixesDataExportProperty(
                        s3_bucket_destination=s3_mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty(
                            account_id="accountId",
                            arn="arn",
                            encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                                ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                    key_id="keyId"
                                ),
                                sses3=sses3
                            ),
                            format="format",
                            output_schema_version="outputSchemaVersion",
                            prefix="prefix"
                        ),
                        storage_lens_table_destination=s3_mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty(
                            encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                                ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                    key_id="keyId"
                                ),
                                sses3=sses3
                            ),
                            is_enabled=False
                        )
                    ),
                    id="id",
                    include=s3_mixins.CfnStorageLensPropsMixin.BucketsAndRegionsProperty(
                        buckets=["buckets"],
                        regions=["regions"]
                    ),
                    is_enabled=False,
                    prefix_delimiter="prefixDelimiter",
                    storage_lens_arn="storageLensArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bfb046fc9cea51c7471fe4a2a4c9bd5402a7e23be1d1675ff6bea8fd1f88a015)
                check_type(argname="argument account_level", value=account_level, expected_type=type_hints["account_level"])
                check_type(argname="argument aws_org", value=aws_org, expected_type=type_hints["aws_org"])
                check_type(argname="argument data_export", value=data_export, expected_type=type_hints["data_export"])
                check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
                check_type(argname="argument expanded_prefixes_data_export", value=expanded_prefixes_data_export, expected_type=type_hints["expanded_prefixes_data_export"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
                check_type(argname="argument prefix_delimiter", value=prefix_delimiter, expected_type=type_hints["prefix_delimiter"])
                check_type(argname="argument storage_lens_arn", value=storage_lens_arn, expected_type=type_hints["storage_lens_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_level is not None:
                self._values["account_level"] = account_level
            if aws_org is not None:
                self._values["aws_org"] = aws_org
            if data_export is not None:
                self._values["data_export"] = data_export
            if exclude is not None:
                self._values["exclude"] = exclude
            if expanded_prefixes_data_export is not None:
                self._values["expanded_prefixes_data_export"] = expanded_prefixes_data_export
            if id is not None:
                self._values["id"] = id
            if include is not None:
                self._values["include"] = include
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled
            if prefix_delimiter is not None:
                self._values["prefix_delimiter"] = prefix_delimiter
            if storage_lens_arn is not None:
                self._values["storage_lens_arn"] = storage_lens_arn

        @builtins.property
        def account_level(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AccountLevelProperty"]]:
            '''This property contains the details of the account-level metrics for Amazon S3 Storage Lens configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-accountlevel
            '''
            result = self._values.get("account_level")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AccountLevelProperty"]], result)

        @builtins.property
        def aws_org(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AwsOrgProperty"]]:
            '''This property contains the details of the AWS Organization for the S3 Storage Lens configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-awsorg
            '''
            result = self._values.get("aws_org")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.AwsOrgProperty"]], result)

        @builtins.property
        def data_export(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.DataExportProperty"]]:
            '''This property contains the details of this S3 Storage Lens configuration's metrics export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-dataexport
            '''
            result = self._values.get("data_export")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.DataExportProperty"]], result)

        @builtins.property
        def exclude(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.BucketsAndRegionsProperty"]]:
            '''This property contains the details of the bucket and or Regions excluded for Amazon S3 Storage Lens configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.BucketsAndRegionsProperty"]], result)

        @builtins.property
        def expanded_prefixes_data_export(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensExpandedPrefixesDataExportProperty"]]:
            '''Expanded Prefixes Data Export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-expandedprefixesdataexport
            '''
            result = self._values.get("expanded_prefixes_data_export")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensExpandedPrefixesDataExportProperty"]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''This property contains the details of the ID of the S3 Storage Lens configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.BucketsAndRegionsProperty"]]:
            '''This property contains the details of the bucket and or Regions included for Amazon S3 Storage Lens configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.BucketsAndRegionsProperty"]], result)

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This property contains the details of whether the Amazon S3 Storage Lens configuration is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def prefix_delimiter(self) -> typing.Optional[builtins.str]:
            '''The delimiter to divide S3 key into hierarchy of prefixes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-prefixdelimiter
            '''
            result = self._values.get("prefix_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def storage_lens_arn(self) -> typing.Optional[builtins.str]:
            '''This property contains the details of the ARN of the S3 Storage Lens configuration.

            This property is read-only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-storagelensarn
            '''
            result = self._values.get("storage_lens_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageLensConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.StorageLensExpandedPrefixesDataExportProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket_destination": "s3BucketDestination",
            "storage_lens_table_destination": "storageLensTableDestination",
        },
    )
    class StorageLensExpandedPrefixesDataExportProperty:
        def __init__(
            self,
            *,
            s3_bucket_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.S3BucketDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            storage_lens_table_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.StorageLensTableDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Expanded Prefixes Data Export.

            :param s3_bucket_destination: S3 bucket destination settings for the Amazon S3 Storage Lens metrics export.
            :param storage_lens_table_destination: S3 Tables destination settings for the Amazon S3 Storage Lens metrics export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensexpandedprefixesdataexport.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                # sses3: Any
                
                storage_lens_expanded_prefixes_data_export_property = s3_mixins.CfnStorageLensPropsMixin.StorageLensExpandedPrefixesDataExportProperty(
                    s3_bucket_destination=s3_mixins.CfnStorageLensPropsMixin.S3BucketDestinationProperty(
                        account_id="accountId",
                        arn="arn",
                        encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                            ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                key_id="keyId"
                            ),
                            sses3=sses3
                        ),
                        format="format",
                        output_schema_version="outputSchemaVersion",
                        prefix="prefix"
                    ),
                    storage_lens_table_destination=s3_mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty(
                        encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                            ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                                key_id="keyId"
                            ),
                            sses3=sses3
                        ),
                        is_enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__787edca8bf89127e32cf68c8397b50c25b388775b7cd4b51f43be1495d61078b)
                check_type(argname="argument s3_bucket_destination", value=s3_bucket_destination, expected_type=type_hints["s3_bucket_destination"])
                check_type(argname="argument storage_lens_table_destination", value=storage_lens_table_destination, expected_type=type_hints["storage_lens_table_destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket_destination is not None:
                self._values["s3_bucket_destination"] = s3_bucket_destination
            if storage_lens_table_destination is not None:
                self._values["storage_lens_table_destination"] = storage_lens_table_destination

        @builtins.property
        def s3_bucket_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.S3BucketDestinationProperty"]]:
            '''S3 bucket destination settings for the Amazon S3 Storage Lens metrics export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensexpandedprefixesdataexport.html#cfn-s3-storagelens-storagelensexpandedprefixesdataexport-s3bucketdestination
            '''
            result = self._values.get("s3_bucket_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.S3BucketDestinationProperty"]], result)

        @builtins.property
        def storage_lens_table_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensTableDestinationProperty"]]:
            '''S3 Tables destination settings for the Amazon S3 Storage Lens metrics export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensexpandedprefixesdataexport.html#cfn-s3-storagelens-storagelensexpandedprefixesdataexport-storagelenstabledestination
            '''
            result = self._values.get("storage_lens_table_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensTableDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageLensExpandedPrefixesDataExportProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.StorageLensGroupLevelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "storage_lens_group_selection_criteria": "storageLensGroupSelectionCriteria",
        },
    )
    class StorageLensGroupLevelProperty:
        def __init__(
            self,
            *,
            storage_lens_group_selection_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This resource determines the scope of Storage Lens group data that is displayed in the Storage Lens dashboard.

            :param storage_lens_group_selection_criteria: This property indicates which Storage Lens group ARNs to include or exclude in the Storage Lens group aggregation. If this value is left null, then all Storage Lens groups are selected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensgrouplevel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                storage_lens_group_level_property = s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupLevelProperty(
                    storage_lens_group_selection_criteria=s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty(
                        exclude=["exclude"],
                        include=["include"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b7cdf3b9d40483bbad29be25d228fedc3e2784a463b059b0e39e74a8130826b)
                check_type(argname="argument storage_lens_group_selection_criteria", value=storage_lens_group_selection_criteria, expected_type=type_hints["storage_lens_group_selection_criteria"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if storage_lens_group_selection_criteria is not None:
                self._values["storage_lens_group_selection_criteria"] = storage_lens_group_selection_criteria

        @builtins.property
        def storage_lens_group_selection_criteria(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty"]]:
            '''This property indicates which Storage Lens group ARNs to include or exclude in the Storage Lens group aggregation.

            If this value is left null, then all Storage Lens groups are selected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensgrouplevel.html#cfn-s3-storagelens-storagelensgrouplevel-storagelensgroupselectioncriteria
            '''
            result = self._values.get("storage_lens_group_selection_criteria")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageLensGroupLevelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={"exclude": "exclude", "include": "include"},
    )
    class StorageLensGroupSelectionCriteriaProperty:
        def __init__(
            self,
            *,
            exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            include: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This resource indicates which Storage Lens group ARNs to include or exclude in the Storage Lens group aggregation.

            You can only attach Storage Lens groups to your dashboard if they're included in your Storage Lens group aggregation. If this value is left null, then all Storage Lens groups are selected.

            :param exclude: This property indicates which Storage Lens group ARNs to exclude from the Storage Lens group aggregation.
            :param include: This property indicates which Storage Lens group ARNs to include in the Storage Lens group aggregation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensgroupselectioncriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                storage_lens_group_selection_criteria_property = s3_mixins.CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty(
                    exclude=["exclude"],
                    include=["include"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d71e055ff043d03304ed1c3df89a53b97a0b7299400a25adbfd3a841a4c15121)
                check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
                check_type(argname="argument include", value=include, expected_type=type_hints["include"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude is not None:
                self._values["exclude"] = exclude
            if include is not None:
                self._values["include"] = include

        @builtins.property
        def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property indicates which Storage Lens group ARNs to exclude from the Storage Lens group aggregation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensgroupselectioncriteria.html#cfn-s3-storagelens-storagelensgroupselectioncriteria-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include(self) -> typing.Optional[typing.List[builtins.str]]:
            '''This property indicates which Storage Lens group ARNs to include in the Storage Lens group aggregation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensgroupselectioncriteria.html#cfn-s3-storagelens-storagelensgroupselectioncriteria-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageLensGroupSelectionCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption": "encryption", "is_enabled": "isEnabled"},
    )
    class StorageLensTableDestinationProperty:
        def __init__(
            self,
            *,
            encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageLensPropsMixin.EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''S3 Tables destination settings for the Amazon S3 Storage Lens metrics export.

            :param encryption: Configures the server-side encryption for Amazon S3 Storage Lens report files with either S3-managed keys (SSE-S3) or KMS-managed keys (SSE-KMS).
            :param is_enabled: Specifies whether the export to S3 Tables is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelenstabledestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_s3 import mixins as s3_mixins
                
                # sses3: Any
                
                storage_lens_table_destination_property = s3_mixins.CfnStorageLensPropsMixin.StorageLensTableDestinationProperty(
                    encryption=s3_mixins.CfnStorageLensPropsMixin.EncryptionProperty(
                        ssekms=s3_mixins.CfnStorageLensPropsMixin.SSEKMSProperty(
                            key_id="keyId"
                        ),
                        sses3=sses3
                    ),
                    is_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b89b0921f65204d659e1efb903232ed13eb3c5c1aef0f5af8c3884ac8c7bd5e)
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption is not None:
                self._values["encryption"] = encryption
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.EncryptionProperty"]]:
            '''Configures the server-side encryption for Amazon S3 Storage Lens report files with either S3-managed keys (SSE-S3) or KMS-managed keys (SSE-KMS).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelenstabledestination.html#cfn-s3-storagelens-storagelenstabledestination-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageLensPropsMixin.EncryptionProperty"]], result)

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the export to S3 Tables is enabled or disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelenstabledestination.html#cfn-s3-storagelens-storagelenstabledestination-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageLensTableDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class EnableVersioning(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_s3.mixins.EnableVersioning",
):
    '''(experimental) S3-specific mixin for enabling versioning.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.mixins_preview.with import
        
        
        bucket = s3.CfnBucket(scope, "MyBucket").with(EnableVersioning()).with(AutoDeleteObjects())
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''(experimental) Applies the mixin functionality to the target construct.

        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c01d3c5d608aa3f15ca64ebf3118cb4f7ec22b0c12536fc8f253761b266f991)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''(experimental) Determines whether this mixin can be applied to the given construct.

        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149fad6c3e56ef22449a553094039cca991cbf9644b0fd057cf4cbac284ea723)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))


__all__ = [
    "AutoDeleteObjects",
    "CfnAccessGrantMixinProps",
    "CfnAccessGrantPropsMixin",
    "CfnAccessGrantsInstanceMixinProps",
    "CfnAccessGrantsInstancePropsMixin",
    "CfnAccessGrantsLocationMixinProps",
    "CfnAccessGrantsLocationPropsMixin",
    "CfnAccessPointMixinProps",
    "CfnAccessPointPropsMixin",
    "CfnBucketMixinProps",
    "CfnBucketPolicyMixinProps",
    "CfnBucketPolicyPropsMixin",
    "CfnBucketPropsMixin",
    "CfnMultiRegionAccessPointMixinProps",
    "CfnMultiRegionAccessPointPolicyMixinProps",
    "CfnMultiRegionAccessPointPolicyPropsMixin",
    "CfnMultiRegionAccessPointPropsMixin",
    "CfnStorageLensGroupMixinProps",
    "CfnStorageLensGroupPropsMixin",
    "CfnStorageLensMixinProps",
    "CfnStorageLensPropsMixin",
    "EnableVersioning",
]

publication.publish()

def _typecheckingstub__5bb5c6efe66133c819e03a85248d34a1546552976e543c729b7c59473feeaa5e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115e9c22c6e163c9a298d1fdfa9412db199559c6b0db57bdf647c6aa33591410(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d63a79f6b3185ee38cd2afb12318d6d88f2a77f0877c7f3bf3380cb18cbfcbe(
    *,
    access_grants_location_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessGrantPropsMixin.AccessGrantsLocationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    access_grants_location_id: typing.Optional[builtins.str] = None,
    application_arn: typing.Optional[builtins.str] = None,
    grantee: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessGrantPropsMixin.GranteeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    permission: typing.Optional[builtins.str] = None,
    s3_prefix_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64cf74afbc86b9b14eb312a819cf979b02c0519853f170ddd98198884f05566(
    props: typing.Union[CfnAccessGrantMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ab06d7b8b96290ab1cfc9220cb691cb856617524dc5926122d40b0c9a2403c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777f6df6b0b3cd9d84d00edf0919288b3f912fc705867f08107017fa1134f531(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749df6fc3ef01799e4f2036b476c815c462473804963856a15cec956d3a168e8(
    *,
    s3_sub_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bf404b7d07091e7aa4e773d6c0d6442b1c354771c30c3b9cb35fdf8aa7bcee(
    *,
    grantee_identifier: typing.Optional[builtins.str] = None,
    grantee_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905491084cc789e5eab0d8486092b1ba98ff35b18e7d26e3c2040ab67ee3fab9(
    *,
    identity_center_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8233ab5d9e31c8379ee61c8c4b28b205c2eed0432260b66a9bf0208b8713802d(
    props: typing.Union[CfnAccessGrantsInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fab575a3ce1d40f12d0bcb1acee6c4c5688092d256773d3cf2e15dea1a53248(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a7dea07ccec4bdcbae70f1761d2b008f5e3eea91f3cd38ba0e11957eda0486(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42357b6c1032cd8d0c91cc40e5a8c00d0831ccbc3e503e2d0a753d440b6924e6(
    *,
    iam_role_arn: typing.Optional[builtins.str] = None,
    location_scope: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b869310af785b8e83acbaa7090141dc83be561dac775e09e90d08975fafbd67d(
    props: typing.Union[CfnAccessGrantsLocationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9dc49e59a6254c3bb812639d8eb881a88b1697cd3e0ac1fd35624bba07759b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7395ca2deaa925285e6b0047535b017170e3e939fb72b8b01fdc77bf446ad2e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9758e9f6a7a88d9cf7c5712f30c90d13f32b4eb605f020dee34e06a9cc1cfc4b(
    *,
    bucket: typing.Optional[builtins.str] = None,
    bucket_account_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
    public_access_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPointPropsMixin.PublicAccessBlockConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPointPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e541decfca52291e8f7bcfb16959c2743b26929e7869c76ba26601bcdf0a103(
    props: typing.Union[CfnAccessPointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99301948fb6a9fb492fe084e74dc558804b1ca0c367788c07e49ff064e4480f8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60fdfc2a64b21c4d6f915033df9fdbb15db74d65a1e303e065e4fe05f6b49c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c60cc0c59b095bcd9ce6d2d2fe0b26059813bf18d72cc97693c3e795024af40(
    *,
    block_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    block_public_policy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa00eb2d5282079476358e347abd4b17821b4424a01ff4068c25718630adc07(
    *,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61da27b1ee7f447df9c6a01c1fb0e0a80c311b33f345bf35f9c3ef6a8f7152d(
    *,
    abac_status: typing.Optional[builtins.str] = None,
    accelerate_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.AccelerateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    access_control: typing.Optional[builtins.str] = None,
    analytics_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.AnalyticsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    bucket_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.BucketEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    cors_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.CorsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    intelligent_tiering_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.IntelligentTieringConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    inventory_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.InventoryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.LifecycleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metadata_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.MetadataConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metadata_table_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.MetadataTableConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.MetricsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    notification_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.NotificationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    object_lock_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ObjectLockConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    object_lock_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ownership_controls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.OwnershipControlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    public_access_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.PublicAccessBlockConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ReplicationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    versioning_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.VersioningConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    website_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.WebsiteConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49243bb3447168c9b8f04db1d04200ac216ace48f2bd3399ee15f4571bd748c3(
    *,
    bucket: typing.Optional[builtins.str] = None,
    policy_document: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ba73c23bd95b2bdb442ee38220a48b79357d3265990c2543f6223060b38203(
    props: typing.Union[CfnBucketPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2a1bb9d82f07e4c23eeec546476b008de055845a0840f640fefc086ee2d587(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdaccd8321315b52e3b7e3399f4f66e8285cc4b1f984dcc2a40cff123cfa810(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca009243f8b97752937936d645805cf8600918eadec76b14de35814057d6064a(
    props: typing.Union[CfnBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597bbd801bf04c01f97d6c1358f13c246b8778dadc489438e60feb7754706152(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663c2df5c06167346b9feac924041f49bb0c252a06ca4bd47e8ebb1ab5cdcefc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b64b6421e663632b82d272c2095d04b08eb4f2cd50965706dfa88db9cf95ab(
    *,
    days_after_initiation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2406ffdf7e4679a419c07f1e747779cabbbd2e1af1cced5f673acaf45e46eb1c(
    *,
    acceleration_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61e4133712e2cb7aece492a07d0d50977070b005aed4e6abc0437db93afc2de(
    *,
    owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1442b1c097dccc3b47e486d134f7ed58ee51bb29c613ac67ee59d1faf009e50b(
    *,
    id: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    storage_class_analysis: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.StorageClassAnalysisProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8b48c55f8deacff80062f0cad9eb734f05bbc58e6abf8872674b00b9ea7785(
    *,
    encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863511f6faeec8e709e8e592901c449026bcd85cccf9f5bc9361838b429f44b5(
    *,
    server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ServerSideEncryptionRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba82944dc39c257239f70201bd5a3e19c4b9d7c57b1c52602d67795c2eb0f43(
    *,
    cors_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.CorsRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cb5582959cc4fa0159ce14255a5c9937b5c1d184fa459b8b5828114915f971(
    *,
    allowed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    exposed_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    max_age: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230b944b912f854dbaf0410cdbb1c7d05fe9627ec6a8e02bc63b01fdc5bde990(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    output_schema_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077127c5e8afe4d07cfd9d48a98dc170a9257a634e8de80d8484522e73681065(
    *,
    days: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
    years: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad0b0de523104cf3b2adb023578b786db52918bc40706dd3e102537a2f5da53(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961597f5613486a51f088843f499bb1ca619ce13572e6e59b839c0df37825f1c(
    *,
    bucket_account_id: typing.Optional[builtins.str] = None,
    bucket_arn: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69072e1d8dff103d2196f16fbe1540c5d4b6226200498b5a7a8e505164c448e9(
    *,
    replica_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44df92e978075efa2b5af256e9aa2dbbeaf7f193582438bd054a66874133ba2a(
    *,
    event_bridge_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359f601d97992243da5c3da82dc6f03ce2961b27ab9755c698e765ca4935b4b3(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c21c827b8aa4a9f5946175db6b8d1583ee7adaae67915e04e66e1a135d5ef37(
    *,
    id: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tierings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TieringProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5701426a2687424386b689a1eb323dc5e32bb9d66fd3ab3c4e7388cf91cfa9c1(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    included_object_versions: typing.Optional[builtins.str] = None,
    optional_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    prefix: typing.Optional[builtins.str] = None,
    schedule_frequency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035cb9f72b132fcc4c32f97b15b79fb192d466b0016e8cc8cade3b721689d04e(
    *,
    configuration_state: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5923a017aa9456c9e573060a7edba1e2511cc79b87302ee3ccc99c3832c864fd(
    *,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.MetadataTableEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    record_expiration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.RecordExpirationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926c6a45a529cd64437e9280f2f8c50954c58201e27270a774fcc74ee27ceea3(
    *,
    event: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.NotificationFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    function: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe77de25f12309c650326e9ac3a42351cc0d19b0e68914ee89b32da1d5cc14d(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    transition_default_minimum_object_size: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f377ce0c94a5c9b7d29d6ab0a709768d4dbf1eb7461b7f144f4ccc083ace09(
    *,
    destination_bucket_name: typing.Optional[builtins.str] = None,
    log_file_prefix: typing.Optional[builtins.str] = None,
    target_object_key_format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TargetObjectKeyFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f98a78eb65f2e0f0b916847010bac1317995d462e993f64cbc21a777472cdfa(
    *,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.MetadataDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    inventory_table_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.InventoryTableConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    journal_table_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.JournalTableConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda645bd09169eb4cc8e766535d98f550bf2a3969f3fac25d836ac3e7c517744(
    *,
    table_bucket_arn: typing.Optional[builtins.str] = None,
    table_bucket_type: typing.Optional[builtins.str] = None,
    table_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91aedfd60b0461bda0100d746756a9f326a770005a50658d6e146c5be40c9edd(
    *,
    s3_tables_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.S3TablesDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7be8a5e52b5569d50fbceccd413765f072524c902d877f333161727a00d7c03(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    sse_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc26563dd9d4c453237cf39f0a0e83868255ba5d9b99a876d783ef848cc96d1b(
    *,
    access_point_arn: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0889d5e5b8977f2613c8e94a683d46cfd72029e3ce9e7f6f7167adaa10a4d12a(
    *,
    event_threshold: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ReplicationTimeValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd6c762736f1d33a330b19c025a6c4b96209a5c8a418b51b96cbfd0c2941b57(
    *,
    newer_noncurrent_versions: typing.Optional[jsii.Number] = None,
    noncurrent_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__143fab7f77f06aa28d069fd0eb1f9c334d256a6ad651786b90396624cf1f67cf(
    *,
    newer_noncurrent_versions: typing.Optional[jsii.Number] = None,
    storage_class: typing.Optional[builtins.str] = None,
    transition_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5045bfcec644eb298a0d4b381b04b53eac85a884ec14ee9c080d4d30bf0be499(
    *,
    event_bridge_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.EventBridgeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.LambdaConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    queue_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.QueueConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    topic_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TopicConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4687f94f101195a94936e1dedb83e8b9be8ff3c14adadf77c06058a115fac5(
    *,
    s3_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.S3KeyFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d5076cf09478eda5c5d158a709090eddb243eae330d3d8624cd5eb30437776(
    *,
    object_lock_enabled: typing.Optional[builtins.str] = None,
    rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ObjectLockRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241ad46ae1d861988a0a5a75d858471ac8dbcefefcd8d5fa15ac04a6c1853f86(
    *,
    default_retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.DefaultRetentionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4468aa126ef70234daae44a533c6a5421bfd6d1b4bcf7b5c6139a9bcee1a2d2(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.OwnershipControlsRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9840834cd9416dd0888a22fde8fc873a02ffddfdfefe24e421b76953f3167ced(
    *,
    object_ownership: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716f4398f43d66c6f8931005b60eb69a9bf9d2df6dfeca6bb640fea1e93c198a(
    *,
    partition_date_source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f133492b8537506aa79669270874517e396e3eb1509d9db68fef0ba566067725(
    *,
    block_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    block_public_policy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2577f0dd09ad20794bf3f684461355005bde4946142ed53b0c3b35427792ad3(
    *,
    event: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.NotificationFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    queue: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437af7b76608d9657210b67c2ca3e8a1229d4da83769266766df90dd15931dda(
    *,
    days: typing.Optional[jsii.Number] = None,
    expiration: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987a2fd463fd3ef55b6f4fd173cb15810ebeb370aaac679aabdbfcf87cffdb3a(
    *,
    host_name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c27085142d05415b4057e4b02b618de9c96f1c4cadfd659dc0907ba2f4b7800(
    *,
    host_name: typing.Optional[builtins.str] = None,
    http_redirect_code: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    replace_key_prefix_with: typing.Optional[builtins.str] = None,
    replace_key_with: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0fb7be36161dd3091d616351604e55684539eaeea2e7d1fad873443ad2a8d7(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befe5f67f40528ec587bd5180f03d3f5f1b18a03b5b7b8ee94bc1ba3ef23faea(
    *,
    role: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ReplicationRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da263f2ab26142b9ffe7168a134c11b9fcfda13609f5f8b3494f3574505f2834(
    *,
    access_control_translation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.AccessControlTranslationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    account: typing.Optional[builtins.str] = None,
    bucket: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.MetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replication_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ReplicationTimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_class: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7434e3092803baa965370f732163b4e4c65222c0a638827b157dd8a1b88219e6(
    *,
    prefix: typing.Optional[builtins.str] = None,
    tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f34ced714fa25d22ba8df8ed44c6696ae77900c85cf4a32b3407e8024462c6(
    *,
    and_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ReplicationRuleAndOperatorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    prefix: typing.Optional[builtins.str] = None,
    tag_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d01568476cded2d4f766994bf9cdd2577146f6265570d265268aaabb0e4a5b4(
    *,
    delete_marker_replication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.DeleteMarkerReplicationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ReplicationDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ReplicationRuleFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    source_selection_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.SourceSelectionCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7ae5247a136bad435b59aeb698335e0501ae09c6825fac7c7bc1865d570323(
    *,
    status: typing.Optional[builtins.str] = None,
    time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ReplicationTimeValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3297b3a4be64f370a3933ab9cc36a9899b36387ed140ee98ed5fef32c411916(
    *,
    minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d891944c894ce60fb0c7465c013ff8dfbbe19954e56f81241a08488f8272a76(
    *,
    http_error_code_returned_equals: typing.Optional[builtins.str] = None,
    key_prefix_equals: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a30fea19308d4d38f9edc1a370bf7a799594d986b7c706e04c7dbb3e87f0aa4(
    *,
    redirect_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.RedirectRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    routing_rule_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.RoutingRuleConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1204db2e4ba2a692a857f82cbefb3af5841b0f4d5495c7361545d246c04965b0(
    *,
    abort_incomplete_multipart_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.AbortIncompleteMultipartUploadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    expiration_date: typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]] = None,
    expiration_in_days: typing.Optional[jsii.Number] = None,
    expired_object_delete_marker: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    noncurrent_version_expiration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.NoncurrentVersionExpirationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    noncurrent_version_expiration_in_days: typing.Optional[jsii.Number] = None,
    noncurrent_version_transition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.NoncurrentVersionTransitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    noncurrent_version_transitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.NoncurrentVersionTransitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    object_size_greater_than: typing.Optional[jsii.Number] = None,
    object_size_less_than: typing.Optional[jsii.Number] = None,
    prefix: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tag_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    transition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TransitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    transitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.TransitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fdc2f3cfe0b08a9fcd0cf9e56f7af8b2eedb0c818ed0e522b748c2ad5d3dfd(
    *,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b0068e00ceef280e62fdef458ef0e709df19354378f6061115918b75f3e2ac(
    *,
    table_arn: typing.Optional[builtins.str] = None,
    table_bucket_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    table_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63e82f3d697140d3a8cc022f88b1acc947b18f43fde26e9f1184facbed5baef(
    *,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    sse_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7ae9dc1abee8744e63a7c9b51942066bc54ee6791f632cccbb7d14977804a5(
    *,
    blocked_encryption_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.BlockedEncryptionTypesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bucket_key_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    server_side_encryption_by_default: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ServerSideEncryptionByDefaultProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57188763a309906f90b4cf3ad1ad344c58f70cabf8b5e55cac575e1f53a9fc0a(
    *,
    replica_modifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.ReplicaModificationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sse_kms_encrypted_objects: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.SseKmsEncryptedObjectsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd84cade6b021c89383e07f5a348ae2ede45cd575a27afbf37095712df40e63(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ac45e1d920bb7cb6633dcee01a27a4d7556163b0e8ef1970cac3a985050d4b(
    *,
    data_export: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.DataExportProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff902def2552c5cc5162b20079fbe8892941de65647befbd46dd333b9b9d5951(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c75868b1de41292f6e09f7f1775d53fe5ed5e0c80c90d1c95cdc865d83ac09(
    *,
    partitioned_prefix: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.PartitionedPrefixProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    simple_prefix: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9408b1ed1c9af817cf6363b3ff9d1500a00d54335d321306c4ee4c0c229d59a7(
    *,
    access_tier: typing.Optional[builtins.str] = None,
    days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571777c71620a73c29f8dbda8487e1ff2dfb52e24dee9873c589148842e9975a(
    *,
    event: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.NotificationFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    topic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74dc017c7bb834f3c57974eb5f80ea0e9d60b6e1c04c64241c72b130eaefdb1(
    *,
    storage_class: typing.Optional[builtins.str] = None,
    transition_date: typing.Optional[typing.Union[datetime.datetime, _aws_cdk_ceddda9d.IResolvable]] = None,
    transition_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885d64f9f5c382eb200d9b49fdb81ec3ee8de8d400b2ac3b9bc95212f159263c(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032fb9f64e772bfee9e52da277fc951f50bf72c817642bb4fea59beee9bc3eb3(
    *,
    error_document: typing.Optional[builtins.str] = None,
    index_document: typing.Optional[builtins.str] = None,
    redirect_all_requests_to: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.RedirectAllRequestsToProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    routing_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.RoutingRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f299e980c99133c2d3bfa5f685372c13176b82be3f2059e09ab26cbb7e0bfb9(
    *,
    name: typing.Optional[builtins.str] = None,
    public_access_block_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMultiRegionAccessPointPropsMixin.PublicAccessBlockConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    regions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMultiRegionAccessPointPropsMixin.RegionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4a8045dd04aa4eb801095759465f3675aa01a75e7880d3d9b252502409ca18(
    *,
    mrap_name: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cddacae305f7dfbd0ff18f8930769c5456acc830276b33e14a8233d12340ee4(
    props: typing.Union[CfnMultiRegionAccessPointPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16646e2cd4bd9804f2d6bef3701c14f69dfd92fda9db8673eddf229dfaf7b118(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903ef159e47a64aa125f3c08dc3355d049a36fea6e71fdf9df341c3856168a69(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ba0d62fe259fa60f1e29b5e2f730ab35dd52237da6005daafa1f78cec45787(
    *,
    is_public: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dad4ceb4433c845a98a94e94cb136199684d8155ea5abb04eeee942957236b9(
    props: typing.Union[CfnMultiRegionAccessPointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb7b7a04207fe606c19f5b387d14762a327d65072adade1a2aeb628773f08c5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e0ff90278293be505e8053e0423ac4b2d7a733841fc2d91f64947e01da7127(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36006bb930af965ef9868643d18e1124d0ebfc3163dfce89c5691244b1302aaf(
    *,
    block_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    block_public_policy: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c397508cc3c3530150a921cc466c2ebc3caeb0ebe1c88a01c5170550f395cb9(
    *,
    bucket: typing.Optional[builtins.str] = None,
    bucket_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8c3baea9250ca2d66654501d87b3b98445d18ee99836e46fcf8a67e8fc403f(
    *,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensGroupPropsMixin.FilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b79176d6bba3db03f2a5acab34f14d04929bf3cb17440f5a55e34e6f8f5a30f(
    props: typing.Union[CfnStorageLensGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80513eaaf6ebe8aee666195e04cf5d93d98e2b2320f7cf77e9a190833344ec06(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0b7db7363fcc8048372fd4f1e1760550f1f1a0621d189eb54a749008cc563a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82069e5a3549b13848688189cc159471062f07db423e376490df557d6c36170f(
    *,
    match_any_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
    match_any_suffix: typing.Optional[typing.Sequence[builtins.str]] = None,
    match_any_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    match_object_age: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    match_object_size: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0a064e86223d6538f7bb62c14fe89718bd3102980b6939536f3fbf52783d73(
    *,
    and_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensGroupPropsMixin.AndProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    match_any_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
    match_any_suffix: typing.Optional[typing.Sequence[builtins.str]] = None,
    match_any_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    match_object_age: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    match_object_size: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    or_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensGroupPropsMixin.OrProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d672bdd83ff193b58a1279486f8f6f1f1e404c005b6ec6ad14879c25ac6bdd(
    *,
    days_greater_than: typing.Optional[jsii.Number] = None,
    days_less_than: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8699187dbe4d5b7c954d01c920c102265b9d468cef471fd81829f3b087655eef(
    *,
    bytes_greater_than: typing.Optional[jsii.Number] = None,
    bytes_less_than: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4659c4bd66e7d90c1c6d1cb5d6b9e8b2d5ca71a0c604f3584a3babbccb68793(
    *,
    match_any_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
    match_any_suffix: typing.Optional[typing.Sequence[builtins.str]] = None,
    match_any_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    match_object_age: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensGroupPropsMixin.MatchObjectAgeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    match_object_size: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensGroupPropsMixin.MatchObjectSizeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5302d5961801bea27ca62e7f789bdcccb5e66dcef06529c2b903556435dec34(
    *,
    storage_lens_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.StorageLensConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a1654a1e996fe564733c1bbfaaf23198e628556131a0d6b6bd40231392d495(
    props: typing.Union[CfnStorageLensMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd30fab91d72b8f2370d40d6ac324a33af8fae5622cf665fde0c6b47a30b90c2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346b5f50a2d3070dc98a9dddf7f1f55de8405110a30fb44660291a2b956c8aad(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd94050c0874e39c9eec5db42f0089e9020360ccf67303b60aceb1ee47737ce(
    *,
    activity_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.ActivityMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    advanced_cost_optimization_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    advanced_data_protection_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    advanced_performance_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bucket_level: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.BucketLevelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    detailed_status_codes_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_lens_group_level: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.StorageLensGroupLevelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d241db1c23fe443e57cce902531a349e1ac3fcf6c5732575ff2dbae14d3ba2c6(
    *,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7678c3007adb96e428e572c1607f475d80e7ec26e8c39b3a49de335270b8db(
    *,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e50fba85426f5da5848900a588a07dd594b47dab962c9a520b582539bb1350(
    *,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ba9314b98b8401c488777f79deb605b5e78fdb91b59ab2b5948f65fca98c5e(
    *,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263598804c0e04d8fc9c6c293ceac4d892e106f87d179f9bd11b72a19f99364b(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973971fab07626ed79d92bf1a19f85d04447bfa6a94d42ded03e8947f6dd2b39(
    *,
    activity_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.ActivityMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    advanced_cost_optimization_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.AdvancedCostOptimizationMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    advanced_data_protection_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.AdvancedDataProtectionMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    advanced_performance_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.AdvancedPerformanceMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    detailed_status_codes_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.DetailedStatusCodesMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    prefix_level: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.PrefixLevelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b65e25a5c0b1040054ea426eb49c97ab8b7c8357c9f7d593e2b8ac5d15a2f8(
    *,
    buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45033ba3423020553245d401b9ba019c42753d0957e92d48d26624fe7fd422c8(
    *,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b99046d248317730675d1adc64e2e024edad3ad623dc4d372ae2b261e10e25(
    *,
    cloud_watch_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.CloudWatchMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_bucket_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.S3BucketDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_lens_table_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.StorageLensTableDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919be7d62e6d428c9c835251bba65541537549f2ed02701885e804f944ebfa84(
    *,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495fa64b373cef3d00461464358a46d7639949cb19abcfbb1888ba041688df9d(
    *,
    ssekms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.SSEKMSProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sses3: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8cc294b63b63079558c34c29ff76bbe8a9bf2401479cb531a4c8a7e94dbde2(
    *,
    storage_metrics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.PrefixLevelStorageMetricsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479caa06ce603b6cb1fb538b9a25b201132cd3d2a3daf8d95efbff4831e88533(
    *,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    selection_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.SelectionCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe5c81092876e6ffcb7dd4dd9c7e6a0c2c9a90f5926593938f9ba06f0e61cdf(
    *,
    account_id: typing.Optional[builtins.str] = None,
    arn: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    format: typing.Optional[builtins.str] = None,
    output_schema_version: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c48fc8c0507516ae26ae4f74a3c205fd7fe7b84db1bbe064e18d1be9d15b3a9(
    *,
    key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8388be336d55ebbb01053ed9cb1c40522292958177b16da50aa01a1b000ce91(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    max_depth: typing.Optional[jsii.Number] = None,
    min_storage_bytes_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb046fc9cea51c7471fe4a2a4c9bd5402a7e23be1d1675ff6bea8fd1f88a015(
    *,
    account_level: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.AccountLevelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    aws_org: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.AwsOrgProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_export: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.DataExportProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exclude: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.BucketsAndRegionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    expanded_prefixes_data_export: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.StorageLensExpandedPrefixesDataExportProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[builtins.str] = None,
    include: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.BucketsAndRegionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    prefix_delimiter: typing.Optional[builtins.str] = None,
    storage_lens_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787edca8bf89127e32cf68c8397b50c25b388775b7cd4b51f43be1495d61078b(
    *,
    s3_bucket_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.S3BucketDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_lens_table_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.StorageLensTableDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7cdf3b9d40483bbad29be25d228fedc3e2784a463b059b0e39e74a8130826b(
    *,
    storage_lens_group_selection_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.StorageLensGroupSelectionCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71e055ff043d03304ed1c3df89a53b97a0b7299400a25adbfd3a841a4c15121(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b89b0921f65204d659e1efb903232ed13eb3c5c1aef0f5af8c3884ac8c7bd5e(
    *,
    encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageLensPropsMixin.EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c01d3c5d608aa3f15ca64ebf3118cb4f7ec22b0c12536fc8f253761b266f991(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149fad6c3e56ef22449a553094039cca991cbf9644b0fd057cf4cbac284ea723(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
