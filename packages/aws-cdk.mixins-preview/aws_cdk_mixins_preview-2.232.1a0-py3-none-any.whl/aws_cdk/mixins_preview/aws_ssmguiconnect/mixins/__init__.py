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
    jsii_type="@aws-cdk/mixins-preview.aws_ssmguiconnect.mixins.CfnPreferencesMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_recording_preferences": "connectionRecordingPreferences",
    },
)
class CfnPreferencesMixinProps:
    def __init__(
        self,
        *,
        connection_recording_preferences: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPreferencesPropsMixin.ConnectionRecordingPreferencesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPreferencesPropsMixin.

        :param connection_recording_preferences: The set of preferences used for recording RDP connections in the requesting AWS account and AWS Region . This includes details such as which S3 bucket recordings are stored in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmguiconnect-preferences.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssmguiconnect import mixins as ssmguiconnect_mixins
            
            cfn_preferences_mixin_props = ssmguiconnect_mixins.CfnPreferencesMixinProps(
                connection_recording_preferences=ssmguiconnect_mixins.CfnPreferencesPropsMixin.ConnectionRecordingPreferencesProperty(
                    kms_key_arn="kmsKeyArn",
                    recording_destinations=ssmguiconnect_mixins.CfnPreferencesPropsMixin.RecordingDestinationsProperty(
                        s3_buckets=[ssmguiconnect_mixins.CfnPreferencesPropsMixin.S3BucketProperty(
                            bucket_name="bucketName",
                            bucket_owner="bucketOwner"
                        )]
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db5d3b0052378cacda5f324a6d2960bbc5057bd7c839527bdfe76294c43ff46)
            check_type(argname="argument connection_recording_preferences", value=connection_recording_preferences, expected_type=type_hints["connection_recording_preferences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_recording_preferences is not None:
            self._values["connection_recording_preferences"] = connection_recording_preferences

    @builtins.property
    def connection_recording_preferences(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPreferencesPropsMixin.ConnectionRecordingPreferencesProperty"]]:
        '''The set of preferences used for recording RDP connections in the requesting AWS account and AWS Region .

        This includes details such as which S3 bucket recordings are stored in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmguiconnect-preferences.html#cfn-ssmguiconnect-preferences-connectionrecordingpreferences
        '''
        result = self._values.get("connection_recording_preferences")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPreferencesPropsMixin.ConnectionRecordingPreferencesProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPreferencesMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPreferencesPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssmguiconnect.mixins.CfnPreferencesPropsMixin",
):
    '''Specify new or changed connection recording preferences for your AWS Systems Manager GUI Connect connections.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmguiconnect-preferences.html
    :cloudformationResource: AWS::SSMGuiConnect::Preferences
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssmguiconnect import mixins as ssmguiconnect_mixins
        
        cfn_preferences_props_mixin = ssmguiconnect_mixins.CfnPreferencesPropsMixin(ssmguiconnect_mixins.CfnPreferencesMixinProps(
            connection_recording_preferences=ssmguiconnect_mixins.CfnPreferencesPropsMixin.ConnectionRecordingPreferencesProperty(
                kms_key_arn="kmsKeyArn",
                recording_destinations=ssmguiconnect_mixins.CfnPreferencesPropsMixin.RecordingDestinationsProperty(
                    s3_buckets=[ssmguiconnect_mixins.CfnPreferencesPropsMixin.S3BucketProperty(
                        bucket_name="bucketName",
                        bucket_owner="bucketOwner"
                    )]
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPreferencesMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSMGuiConnect::Preferences``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6420833f6beb6c5813811b51a0c96b9cb2b1f15ecae7e30c82a26e61674e5ac4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffc3850cab5c5391dec27502c4449931eb3f3699759e6e9bbe6ce1061cb6f780)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1bafb6f760ddcdbe40722b5572a32de2bce5e633fb9b3dcb02b135d839623d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPreferencesMixinProps:
        return typing.cast(CfnPreferencesMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmguiconnect.mixins.CfnPreferencesPropsMixin.ConnectionRecordingPreferencesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_arn": "kmsKeyArn",
            "recording_destinations": "recordingDestinations",
        },
    )
    class ConnectionRecordingPreferencesProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            recording_destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPreferencesPropsMixin.RecordingDestinationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The set of preferences used for recording RDP connections in the requesting AWS account and AWS Region .

            This includes details such as which S3 bucket recordings are stored in.

            :param kms_key_arn: The ARN of a AWS key that is used to encrypt data while it is being processed by the service. This key must exist in the same AWS Region as the node you start an RDP connection to.
            :param recording_destinations: Determines where recordings of RDP connections are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmguiconnect-preferences-connectionrecordingpreferences.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmguiconnect import mixins as ssmguiconnect_mixins
                
                connection_recording_preferences_property = ssmguiconnect_mixins.CfnPreferencesPropsMixin.ConnectionRecordingPreferencesProperty(
                    kms_key_arn="kmsKeyArn",
                    recording_destinations=ssmguiconnect_mixins.CfnPreferencesPropsMixin.RecordingDestinationsProperty(
                        s3_buckets=[ssmguiconnect_mixins.CfnPreferencesPropsMixin.S3BucketProperty(
                            bucket_name="bucketName",
                            bucket_owner="bucketOwner"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cbc636224a5521cb155b2b809f46da3a0354729ec8ad600475769b8ac76fcdd7)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument recording_destinations", value=recording_destinations, expected_type=type_hints["recording_destinations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if recording_destinations is not None:
                self._values["recording_destinations"] = recording_destinations

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of a AWS  key that is used to encrypt data while it is being processed by the service.

            This key must exist in the same AWS Region as the node you start an RDP connection to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmguiconnect-preferences-connectionrecordingpreferences.html#cfn-ssmguiconnect-preferences-connectionrecordingpreferences-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recording_destinations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPreferencesPropsMixin.RecordingDestinationsProperty"]]:
            '''Determines where recordings of RDP connections are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmguiconnect-preferences-connectionrecordingpreferences.html#cfn-ssmguiconnect-preferences-connectionrecordingpreferences-recordingdestinations
            '''
            result = self._values.get("recording_destinations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPreferencesPropsMixin.RecordingDestinationsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionRecordingPreferencesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmguiconnect.mixins.CfnPreferencesPropsMixin.RecordingDestinationsProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_buckets": "s3Buckets"},
    )
    class RecordingDestinationsProperty:
        def __init__(
            self,
            *,
            s3_buckets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPreferencesPropsMixin.S3BucketProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Determines where recordings of RDP connections are stored.

            :param s3_buckets: The S3 bucket where RDP connection recordings are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmguiconnect-preferences-recordingdestinations.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmguiconnect import mixins as ssmguiconnect_mixins
                
                recording_destinations_property = ssmguiconnect_mixins.CfnPreferencesPropsMixin.RecordingDestinationsProperty(
                    s3_buckets=[ssmguiconnect_mixins.CfnPreferencesPropsMixin.S3BucketProperty(
                        bucket_name="bucketName",
                        bucket_owner="bucketOwner"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7895b4fb846f6d5f8d51d4601cbcd5757d8f6a35ae04991f6356fec9fa71c8c4)
                check_type(argname="argument s3_buckets", value=s3_buckets, expected_type=type_hints["s3_buckets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_buckets is not None:
                self._values["s3_buckets"] = s3_buckets

        @builtins.property
        def s3_buckets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPreferencesPropsMixin.S3BucketProperty"]]]]:
            '''The S3 bucket where RDP connection recordings are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmguiconnect-preferences-recordingdestinations.html#cfn-ssmguiconnect-preferences-recordingdestinations-s3buckets
            '''
            result = self._values.get("s3_buckets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPreferencesPropsMixin.S3BucketProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordingDestinationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmguiconnect.mixins.CfnPreferencesPropsMixin.S3BucketProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "bucket_owner": "bucketOwner"},
    )
    class S3BucketProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_owner: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The S3 bucket where RDP connection recordings are stored.

            :param bucket_name: The name of the S3 bucket where RDP connection recordings are stored.
            :param bucket_owner: The AWS account number that owns the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmguiconnect-preferences-s3bucket.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmguiconnect import mixins as ssmguiconnect_mixins
                
                s3_bucket_property = ssmguiconnect_mixins.CfnPreferencesPropsMixin.S3BucketProperty(
                    bucket_name="bucketName",
                    bucket_owner="bucketOwner"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__943d727dd4aad1217ed23c0a3d3d403981089114bd73be9b97ebe1ac8100e0b5)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_owner is not None:
                self._values["bucket_owner"] = bucket_owner

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket where RDP connection recordings are stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmguiconnect-preferences-s3bucket.html#cfn-ssmguiconnect-preferences-s3bucket-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The AWS account number that owns the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmguiconnect-preferences-s3bucket.html#cfn-ssmguiconnect-preferences-s3bucket-bucketowner
            '''
            result = self._values.get("bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnPreferencesMixinProps",
    "CfnPreferencesPropsMixin",
]

publication.publish()

def _typecheckingstub__4db5d3b0052378cacda5f324a6d2960bbc5057bd7c839527bdfe76294c43ff46(
    *,
    connection_recording_preferences: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPreferencesPropsMixin.ConnectionRecordingPreferencesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6420833f6beb6c5813811b51a0c96b9cb2b1f15ecae7e30c82a26e61674e5ac4(
    props: typing.Union[CfnPreferencesMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc3850cab5c5391dec27502c4449931eb3f3699759e6e9bbe6ce1061cb6f780(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1bafb6f760ddcdbe40722b5572a32de2bce5e633fb9b3dcb02b135d839623d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc636224a5521cb155b2b809f46da3a0354729ec8ad600475769b8ac76fcdd7(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    recording_destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPreferencesPropsMixin.RecordingDestinationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7895b4fb846f6d5f8d51d4601cbcd5757d8f6a35ae04991f6356fec9fa71c8c4(
    *,
    s3_buckets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPreferencesPropsMixin.S3BucketProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943d727dd4aad1217ed23c0a3d3d403981089114bd73be9b97ebe1ac8100e0b5(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
