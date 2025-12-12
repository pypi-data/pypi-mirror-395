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
    jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnCollectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"collection_id": "collectionId", "tags": "tags"},
)
class CfnCollectionMixinProps:
    def __init__(
        self,
        *,
        collection_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCollectionPropsMixin.

        :param collection_id: ID for the collection that you are creating.
        :param tags: A set of tags (key-value pairs) that you want to attach to the collection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
            
            cfn_collection_mixin_props = rekognition_mixins.CfnCollectionMixinProps(
                collection_id="collectionId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eaaec4b5f60fe9309cfb96e370ce2b053ada681c78b40486d01b617d5897e90)
            check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collection_id is not None:
            self._values["collection_id"] = collection_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def collection_id(self) -> typing.Optional[builtins.str]:
        '''ID for the collection that you are creating.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html#cfn-rekognition-collection-collectionid
        '''
        result = self._values.get("collection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A set of tags (key-value pairs) that you want to attach to the collection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html#cfn-rekognition-collection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCollectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCollectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnCollectionPropsMixin",
):
    '''The ``AWS::Rekognition::Collection`` type creates a server-side container called a collection.

    You can use a collection to store information about detected faces and search for known faces in images, stored videos, and streaming videos.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html
    :cloudformationResource: AWS::Rekognition::Collection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
        
        cfn_collection_props_mixin = rekognition_mixins.CfnCollectionPropsMixin(rekognition_mixins.CfnCollectionMixinProps(
            collection_id="collectionId",
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
        props: typing.Union[CfnCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Rekognition::Collection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad8812c57a1c83a6f19522a96017d517e8e5b98ba1b391fb8185f618d857c36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3d414220f1956e27f0f738aa3fa536b2ec7408b1be16719bb16cda9dc9bf21a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ceb14432ef9fb7fb15c3ab11de478b346b9d3d798f9ea4a90ca2e82be68df0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCollectionMixinProps:
        return typing.cast(CfnCollectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnProjectMixinProps",
    jsii_struct_bases=[],
    name_mapping={"project_name": "projectName", "tags": "tags"},
)
class CfnProjectMixinProps:
    def __init__(
        self,
        *,
        project_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProjectPropsMixin.

        :param project_name: The name of the project to create.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
            
            cfn_project_mixin_props = rekognition_mixins.CfnProjectMixinProps(
                project_name="projectName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eea4de502451c491813dfad9766a13d447f8411b485898ccd772dd64d81b25a)
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project_name is not None:
            self._values["project_name"] = project_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''The name of the project to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-project.html#cfn-rekognition-project-projectname
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-project.html#cfn-rekognition-project-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProjectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnProjectPropsMixin",
):
    '''The ``AWS::Rekognition::Project`` type creates an Amazon Rekognition Custom Labels project.

    A project is a group of resources needed to create and manage versions of an Amazon Rekognition Custom Labels model.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-project.html
    :cloudformationResource: AWS::Rekognition::Project
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
        
        cfn_project_props_mixin = rekognition_mixins.CfnProjectPropsMixin(rekognition_mixins.CfnProjectMixinProps(
            project_name="projectName",
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
        props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Rekognition::Project``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4bf5af8cd0a7374b82eeecc827a5056b63de7142e423ed74cbc71fcf740e93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a00b0dc34c1df6aed04731c148c8680623a21e56943a4d6db951b0c9c61867a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0bf8d9f98dbb68c6c635e716ded34d80f44ee92b372f4ff2f67268be278093)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProjectMixinProps:
        return typing.cast(CfnProjectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bounding_box_regions_of_interest": "boundingBoxRegionsOfInterest",
        "connected_home_settings": "connectedHomeSettings",
        "data_sharing_preference": "dataSharingPreference",
        "face_search_settings": "faceSearchSettings",
        "kinesis_data_stream": "kinesisDataStream",
        "kinesis_video_stream": "kinesisVideoStream",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "notification_channel": "notificationChannel",
        "polygon_regions_of_interest": "polygonRegionsOfInterest",
        "role_arn": "roleArn",
        "s3_destination": "s3Destination",
        "tags": "tags",
    },
)
class CfnStreamProcessorMixinProps:
    def __init__(
        self,
        *,
        bounding_box_regions_of_interest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamProcessorPropsMixin.BoundingBoxProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        connected_home_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamProcessorPropsMixin.ConnectedHomeSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_sharing_preference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamProcessorPropsMixin.DataSharingPreferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        face_search_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamProcessorPropsMixin.FaceSearchSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_data_stream: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamProcessorPropsMixin.KinesisDataStreamProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_video_stream: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamProcessorPropsMixin.KinesisVideoStreamProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        notification_channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamProcessorPropsMixin.NotificationChannelProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        polygon_regions_of_interest: typing.Any = None,
        role_arn: typing.Optional[builtins.str] = None,
        s3_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamProcessorPropsMixin.S3DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStreamProcessorPropsMixin.

        :param bounding_box_regions_of_interest: List of BoundingBox objects, each of which denotes a region of interest on screen. For more information, see the BoundingBox field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .
        :param connected_home_settings: Connected home settings to use on a streaming video. You can use a stream processor for connected home features and select what you want the stream processor to detect, such as people or pets. When the stream processor has started, one notification is sent for each object class specified. For more information, see the ConnectedHome section of `StreamProcessorSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorSettings>`_ .
        :param data_sharing_preference: Allows you to opt in or opt out to share data with Rekognition to improve model performance. You can choose this option at the account level or on a per-stream basis. Note that if you opt out at the account level this setting is ignored on individual streams. For more information, see `StreamProcessorDataSharingPreference <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorDataSharingPreference>`_ .
        :param face_search_settings: The input parameters used to recognize faces in a streaming video analyzed by an Amazon Rekognition stream processor. For more information regarding the contents of the parameters, see `FaceSearchSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_FaceSearchSettings>`_ .
        :param kinesis_data_stream: Amazon Rekognition's Video Stream Processor takes a Kinesis video stream as input. This is the Amazon Kinesis Data Streams instance to which the Amazon Rekognition stream processor streams the analysis results. This must be created within the constraints specified at `KinesisDataStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisDataStream>`_ .
        :param kinesis_video_stream: The Kinesis video stream that provides the source of the streaming video for an Amazon Rekognition Video stream processor. For more information, see `KinesisVideoStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisVideoStream>`_ .
        :param kms_key_id: The identifier for your Amazon Key Management Service key (Amazon KMS key). Optional parameter for connected home stream processors used to encrypt results and data published to your Amazon S3 bucket. For more information, see the KMSKeyId section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .
        :param name: The Name attribute specifies the name of the stream processor and it must be within the constraints described in the Name section of `StreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessor>`_ . If you don't specify a name, Amazon CloudFormation generates a unique ID and uses that ID for the stream processor name.
        :param notification_channel: The Amazon Simple Notification Service topic to which Amazon Rekognition publishes the object detection results and completion status of a video analysis operation. Amazon Rekognition publishes a notification the first time an object of interest or a person is detected in the video stream. Amazon Rekognition also publishes an end-of-session notification with a summary when the stream processing session is complete. For more information, see `StreamProcessorNotificationChannel <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorNotificationChannel>`_ .
        :param polygon_regions_of_interest: A set of ordered lists of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. Each entry of the set contains a polygon denoting a region of interest on the screen. Each polygon is an ordered list of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. For more information, see the Polygon field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .
        :param role_arn: The ARN of the IAM role that allows access to the stream processor. The IAM role provides Rekognition read permissions to the Kinesis stream. It also provides write permissions to an Amazon S3 bucket and Amazon Simple Notification Service topic for a connected home stream processor. This is required for both face search and connected home stream processors. For information about constraints, see the RoleArn section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .
        :param s3_destination: The Amazon S3 bucket location to which Amazon Rekognition publishes the detailed inference results of a video analysis operation. For more information, see the S3Destination section of `StreamProcessorOutput <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorOutput>`_ .
        :param tags: A set of tags (key-value pairs) that you want to attach to the stream processor. For more information, see the Tags section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
            
            # polygon_regions_of_interest: Any
            
            cfn_stream_processor_mixin_props = rekognition_mixins.CfnStreamProcessorMixinProps(
                bounding_box_regions_of_interest=[rekognition_mixins.CfnStreamProcessorPropsMixin.BoundingBoxProperty(
                    height=123,
                    left=123,
                    top=123,
                    width=123
                )],
                connected_home_settings=rekognition_mixins.CfnStreamProcessorPropsMixin.ConnectedHomeSettingsProperty(
                    labels=["labels"],
                    min_confidence=123
                ),
                data_sharing_preference=rekognition_mixins.CfnStreamProcessorPropsMixin.DataSharingPreferenceProperty(
                    opt_in=False
                ),
                face_search_settings=rekognition_mixins.CfnStreamProcessorPropsMixin.FaceSearchSettingsProperty(
                    collection_id="collectionId",
                    face_match_threshold=123
                ),
                kinesis_data_stream=rekognition_mixins.CfnStreamProcessorPropsMixin.KinesisDataStreamProperty(
                    arn="arn"
                ),
                kinesis_video_stream=rekognition_mixins.CfnStreamProcessorPropsMixin.KinesisVideoStreamProperty(
                    arn="arn"
                ),
                kms_key_id="kmsKeyId",
                name="name",
                notification_channel=rekognition_mixins.CfnStreamProcessorPropsMixin.NotificationChannelProperty(
                    arn="arn"
                ),
                polygon_regions_of_interest=polygon_regions_of_interest,
                role_arn="roleArn",
                s3_destination=rekognition_mixins.CfnStreamProcessorPropsMixin.S3DestinationProperty(
                    bucket_name="bucketName",
                    object_key_prefix="objectKeyPrefix"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f399901cab0ddb6be2db1ebb9f2c4a4db1572d74ee8f611a5433eee48efadf6b)
            check_type(argname="argument bounding_box_regions_of_interest", value=bounding_box_regions_of_interest, expected_type=type_hints["bounding_box_regions_of_interest"])
            check_type(argname="argument connected_home_settings", value=connected_home_settings, expected_type=type_hints["connected_home_settings"])
            check_type(argname="argument data_sharing_preference", value=data_sharing_preference, expected_type=type_hints["data_sharing_preference"])
            check_type(argname="argument face_search_settings", value=face_search_settings, expected_type=type_hints["face_search_settings"])
            check_type(argname="argument kinesis_data_stream", value=kinesis_data_stream, expected_type=type_hints["kinesis_data_stream"])
            check_type(argname="argument kinesis_video_stream", value=kinesis_video_stream, expected_type=type_hints["kinesis_video_stream"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_channel", value=notification_channel, expected_type=type_hints["notification_channel"])
            check_type(argname="argument polygon_regions_of_interest", value=polygon_regions_of_interest, expected_type=type_hints["polygon_regions_of_interest"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument s3_destination", value=s3_destination, expected_type=type_hints["s3_destination"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bounding_box_regions_of_interest is not None:
            self._values["bounding_box_regions_of_interest"] = bounding_box_regions_of_interest
        if connected_home_settings is not None:
            self._values["connected_home_settings"] = connected_home_settings
        if data_sharing_preference is not None:
            self._values["data_sharing_preference"] = data_sharing_preference
        if face_search_settings is not None:
            self._values["face_search_settings"] = face_search_settings
        if kinesis_data_stream is not None:
            self._values["kinesis_data_stream"] = kinesis_data_stream
        if kinesis_video_stream is not None:
            self._values["kinesis_video_stream"] = kinesis_video_stream
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if notification_channel is not None:
            self._values["notification_channel"] = notification_channel
        if polygon_regions_of_interest is not None:
            self._values["polygon_regions_of_interest"] = polygon_regions_of_interest
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if s3_destination is not None:
            self._values["s3_destination"] = s3_destination
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def bounding_box_regions_of_interest(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.BoundingBoxProperty"]]]]:
        '''List of BoundingBox objects, each of which denotes a region of interest on screen.

        For more information, see the BoundingBox field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-boundingboxregionsofinterest
        '''
        result = self._values.get("bounding_box_regions_of_interest")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.BoundingBoxProperty"]]]], result)

    @builtins.property
    def connected_home_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.ConnectedHomeSettingsProperty"]]:
        '''Connected home settings to use on a streaming video.

        You can use a stream processor for connected home features and select what you want the stream processor to detect, such as people or pets. When the stream processor has started, one notification is sent for each object class specified. For more information, see the ConnectedHome section of `StreamProcessorSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorSettings>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-connectedhomesettings
        '''
        result = self._values.get("connected_home_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.ConnectedHomeSettingsProperty"]], result)

    @builtins.property
    def data_sharing_preference(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.DataSharingPreferenceProperty"]]:
        '''Allows you to opt in or opt out to share data with Rekognition to improve model performance.

        You can choose this option at the account level or on a per-stream basis. Note that if you opt out at the account level this setting is ignored on individual streams. For more information, see `StreamProcessorDataSharingPreference <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorDataSharingPreference>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-datasharingpreference
        '''
        result = self._values.get("data_sharing_preference")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.DataSharingPreferenceProperty"]], result)

    @builtins.property
    def face_search_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.FaceSearchSettingsProperty"]]:
        '''The input parameters used to recognize faces in a streaming video analyzed by an Amazon Rekognition stream processor.

        For more information regarding the contents of the parameters, see `FaceSearchSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_FaceSearchSettings>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-facesearchsettings
        '''
        result = self._values.get("face_search_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.FaceSearchSettingsProperty"]], result)

    @builtins.property
    def kinesis_data_stream(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.KinesisDataStreamProperty"]]:
        '''Amazon Rekognition's Video Stream Processor takes a Kinesis video stream as input.

        This is the Amazon Kinesis Data Streams instance to which the Amazon Rekognition stream processor streams the analysis results. This must be created within the constraints specified at `KinesisDataStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisDataStream>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-kinesisdatastream
        '''
        result = self._values.get("kinesis_data_stream")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.KinesisDataStreamProperty"]], result)

    @builtins.property
    def kinesis_video_stream(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.KinesisVideoStreamProperty"]]:
        '''The Kinesis video stream that provides the source of the streaming video for an Amazon Rekognition Video stream processor.

        For more information, see `KinesisVideoStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisVideoStream>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-kinesisvideostream
        '''
        result = self._values.get("kinesis_video_stream")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.KinesisVideoStreamProperty"]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for your Amazon Key Management Service key (Amazon KMS key).

        Optional parameter for connected home stream processors used to encrypt results and data published to your Amazon S3 bucket. For more information, see the KMSKeyId section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The Name attribute specifies the name of the stream processor and it must be within the constraints described in the Name section of `StreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessor>`_ . If you don't specify a name, Amazon CloudFormation generates a unique ID and uses that ID for the stream processor name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_channel(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.NotificationChannelProperty"]]:
        '''The Amazon Simple Notification Service topic to which Amazon Rekognition publishes the object detection results and completion status of a video analysis operation.

        Amazon Rekognition publishes a notification the first time an object of interest or a person is detected in the video stream. Amazon Rekognition also publishes an end-of-session notification with a summary when the stream processing session is complete. For more information, see `StreamProcessorNotificationChannel <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorNotificationChannel>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-notificationchannel
        '''
        result = self._values.get("notification_channel")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.NotificationChannelProperty"]], result)

    @builtins.property
    def polygon_regions_of_interest(self) -> typing.Any:
        '''A set of ordered lists of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. Each entry of the set contains a polygon denoting a region of interest on the screen. Each polygon is an ordered list of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. For more information, see the Polygon field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-polygonregionsofinterest
        '''
        result = self._values.get("polygon_regions_of_interest")
        return typing.cast(typing.Any, result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that allows access to the stream processor.

        The IAM role provides Rekognition read permissions to the Kinesis stream. It also provides write permissions to an Amazon S3 bucket and Amazon Simple Notification Service topic for a connected home stream processor. This is required for both face search and connected home stream processors. For information about constraints, see the RoleArn section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_destination(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.S3DestinationProperty"]]:
        '''The Amazon S3 bucket location to which Amazon Rekognition publishes the detailed inference results of a video analysis operation.

        For more information, see the S3Destination section of `StreamProcessorOutput <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorOutput>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-s3destination
        '''
        result = self._values.get("s3_destination")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamProcessorPropsMixin.S3DestinationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A set of tags (key-value pairs) that you want to attach to the stream processor.

        For more information, see the Tags section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamProcessorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStreamProcessorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin",
):
    '''The ``AWS::Rekognition::StreamProcessor`` type creates a stream processor used to detect and recognize faces or to detect connected home labels in a streaming video.

    Amazon Rekognition Video is a consumer of live video from Amazon Kinesis Video Streams. There are two different settings for stream processors in Amazon Rekognition, one for detecting faces and one for connected home features.

    If you are creating a stream processor for detecting faces, you provide a Kinesis video stream (input) and a Kinesis data stream (output). You also specify the face recognition criteria in FaceSearchSettings. For example, the collection containing faces that you want to recognize.

    If you are creating a stream processor for detection of connected home labels, you provide a Kinesis video stream for input, and for output an Amazon S3 bucket and an Amazon SNS topic. You can also provide a KMS key ID to encrypt the data sent to your Amazon S3 bucket. You specify what you want to detect in ConnectedHomeSettings, such as people, packages, and pets.

    You can also specify where in the frame you want Amazon Rekognition to monitor with BoundingBoxRegionsOfInterest and PolygonRegionsOfInterest. The Name is used to manage the stream processor and it is the identifier for the stream processor. The ``AWS::Rekognition::StreamProcessor`` resource creates a stream processor in the same Region where you create the Amazon CloudFormation stack.

    For more information, see `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html
    :cloudformationResource: AWS::Rekognition::StreamProcessor
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
        
        # polygon_regions_of_interest: Any
        
        cfn_stream_processor_props_mixin = rekognition_mixins.CfnStreamProcessorPropsMixin(rekognition_mixins.CfnStreamProcessorMixinProps(
            bounding_box_regions_of_interest=[rekognition_mixins.CfnStreamProcessorPropsMixin.BoundingBoxProperty(
                height=123,
                left=123,
                top=123,
                width=123
            )],
            connected_home_settings=rekognition_mixins.CfnStreamProcessorPropsMixin.ConnectedHomeSettingsProperty(
                labels=["labels"],
                min_confidence=123
            ),
            data_sharing_preference=rekognition_mixins.CfnStreamProcessorPropsMixin.DataSharingPreferenceProperty(
                opt_in=False
            ),
            face_search_settings=rekognition_mixins.CfnStreamProcessorPropsMixin.FaceSearchSettingsProperty(
                collection_id="collectionId",
                face_match_threshold=123
            ),
            kinesis_data_stream=rekognition_mixins.CfnStreamProcessorPropsMixin.KinesisDataStreamProperty(
                arn="arn"
            ),
            kinesis_video_stream=rekognition_mixins.CfnStreamProcessorPropsMixin.KinesisVideoStreamProperty(
                arn="arn"
            ),
            kms_key_id="kmsKeyId",
            name="name",
            notification_channel=rekognition_mixins.CfnStreamProcessorPropsMixin.NotificationChannelProperty(
                arn="arn"
            ),
            polygon_regions_of_interest=polygon_regions_of_interest,
            role_arn="roleArn",
            s3_destination=rekognition_mixins.CfnStreamProcessorPropsMixin.S3DestinationProperty(
                bucket_name="bucketName",
                object_key_prefix="objectKeyPrefix"
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
        props: typing.Union[CfnStreamProcessorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Rekognition::StreamProcessor``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87359ed86d98b64edc1f2dd40bbea1f386e26984514201975960b1c7f495e55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__592cf7b03190368beb4519e94d18bc1ad92ca148f64a30a185748b37fd65ab4e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5dbef3d7eadca37d20db123387b8e98ae2de5e34e4c40b5dfd184827f3c5a12)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStreamProcessorMixinProps:
        return typing.cast(CfnStreamProcessorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin.BoundingBoxProperty",
        jsii_struct_bases=[],
        name_mapping={
            "height": "height",
            "left": "left",
            "top": "top",
            "width": "width",
        },
    )
    class BoundingBoxProperty:
        def __init__(
            self,
            *,
            height: typing.Optional[jsii.Number] = None,
            left: typing.Optional[jsii.Number] = None,
            top: typing.Optional[jsii.Number] = None,
            width: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Identifies the bounding box around the label, face, text, or personal protective equipment.

            The ``left`` (x-coordinate) and ``top`` (y-coordinate) are coordinates representing the top and left sides of the bounding box. Note that the upper-left corner of the image is the origin (0,0).

            The ``top`` and ``left`` values returned are ratios of the overall image size. For example, if the input image is 700x200 pixels, and the top-left coordinate of the bounding box is 350x50 pixels, the API returns a ``left`` value of 0.5 (350/700) and a ``top`` value of 0.25 (50/200).

            The ``width`` and ``height`` values represent the dimensions of the bounding box as a ratio of the overall image dimension. For example, if the input image is 700x200 pixels, and the bounding box width is 70 pixels, the width returned is 0.1. For more information, see `BoundingBox <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_BoundingBox>`_ .
            .. epigraph::

               The bounding box coordinates can have negative values. For example, if Amazon Rekognition is able to detect a face that is at the image edge and is only partially visible, the service can return coordinates that are outside the image bounds and, depending on the image edge, you might get negative values or values greater than 1 for the ``left`` or ``top`` values.

            :param height: Height of the bounding box as a ratio of the overall image height.
            :param left: Left coordinate of the bounding box as a ratio of overall image width.
            :param top: Top coordinate of the bounding box as a ratio of overall image height.
            :param width: Width of the bounding box as a ratio of the overall image width.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
                
                bounding_box_property = rekognition_mixins.CfnStreamProcessorPropsMixin.BoundingBoxProperty(
                    height=123,
                    left=123,
                    top=123,
                    width=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86d47abf859936405c70e0b072b1383a54824e618f852bfd5511faf78f4250e3)
                check_type(argname="argument height", value=height, expected_type=type_hints["height"])
                check_type(argname="argument left", value=left, expected_type=type_hints["left"])
                check_type(argname="argument top", value=top, expected_type=type_hints["top"])
                check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if height is not None:
                self._values["height"] = height
            if left is not None:
                self._values["left"] = left
            if top is not None:
                self._values["top"] = top
            if width is not None:
                self._values["width"] = width

        @builtins.property
        def height(self) -> typing.Optional[jsii.Number]:
            '''Height of the bounding box as a ratio of the overall image height.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html#cfn-rekognition-streamprocessor-boundingbox-height
            '''
            result = self._values.get("height")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def left(self) -> typing.Optional[jsii.Number]:
            '''Left coordinate of the bounding box as a ratio of overall image width.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html#cfn-rekognition-streamprocessor-boundingbox-left
            '''
            result = self._values.get("left")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def top(self) -> typing.Optional[jsii.Number]:
            '''Top coordinate of the bounding box as a ratio of overall image height.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html#cfn-rekognition-streamprocessor-boundingbox-top
            '''
            result = self._values.get("top")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def width(self) -> typing.Optional[jsii.Number]:
            '''Width of the bounding box as a ratio of the overall image width.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html#cfn-rekognition-streamprocessor-boundingbox-width
            '''
            result = self._values.get("width")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BoundingBoxProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin.ConnectedHomeSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"labels": "labels", "min_confidence": "minConfidence"},
    )
    class ConnectedHomeSettingsProperty:
        def __init__(
            self,
            *,
            labels: typing.Optional[typing.Sequence[builtins.str]] = None,
            min_confidence: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Connected home settings to use on a streaming video.

            Defining the settings is required in the request parameter for ``CreateStreamProcessor`` . Including this setting in the CreateStreamProcessor request lets you use the stream processor for connected home features. You can then select what you want the stream processor to detect, such as people or pets.

            When the stream processor has started, one notification is sent for each object class specified. For example, if packages and pets are selected, one SNS notification is published the first time a package is detected and one SNS notification is published the first time a pet is detected. An end-of-session summary is also published. For more information, see the ConnectedHome section of `StreamProcessorSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorSettings>`_ .

            :param labels: Specifies what you want to detect in the video, such as people, packages, or pets. The current valid labels you can include in this list are: "PERSON", "PET", "PACKAGE", and "ALL".
            :param min_confidence: The minimum confidence required to label an object in the video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-connectedhomesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
                
                connected_home_settings_property = rekognition_mixins.CfnStreamProcessorPropsMixin.ConnectedHomeSettingsProperty(
                    labels=["labels"],
                    min_confidence=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a655c99cd41c58cf65fa1adb637068b6ba9e1025c9d4f7a180990ec80ee0a47)
                check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
                check_type(argname="argument min_confidence", value=min_confidence, expected_type=type_hints["min_confidence"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if labels is not None:
                self._values["labels"] = labels
            if min_confidence is not None:
                self._values["min_confidence"] = min_confidence

        @builtins.property
        def labels(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies what you want to detect in the video, such as people, packages, or pets.

            The current valid labels you can include in this list are: "PERSON", "PET", "PACKAGE", and "ALL".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-connectedhomesettings.html#cfn-rekognition-streamprocessor-connectedhomesettings-labels
            '''
            result = self._values.get("labels")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def min_confidence(self) -> typing.Optional[jsii.Number]:
            '''The minimum confidence required to label an object in the video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-connectedhomesettings.html#cfn-rekognition-streamprocessor-connectedhomesettings-minconfidence
            '''
            result = self._values.get("min_confidence")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectedHomeSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin.DataSharingPreferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"opt_in": "optIn"},
    )
    class DataSharingPreferenceProperty:
        def __init__(
            self,
            *,
            opt_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Allows you to opt in or opt out to share data with Rekognition to improve model performance.

            You can choose this option at the account level or on a per-stream basis. Note that if you opt out at the account level, this setting is ignored on individual streams. For more information, see `StreamProcessorDataSharingPreference <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorDataSharingPreference>`_ .

            :param opt_in: Describes the opt-in status applied to a stream processor's data sharing policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-datasharingpreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
                
                data_sharing_preference_property = rekognition_mixins.CfnStreamProcessorPropsMixin.DataSharingPreferenceProperty(
                    opt_in=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b0b40c6dd860fc45c9aab2170c7d141ef7751534b53d3f3c28e6edc44b00aa5)
                check_type(argname="argument opt_in", value=opt_in, expected_type=type_hints["opt_in"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if opt_in is not None:
                self._values["opt_in"] = opt_in

        @builtins.property
        def opt_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Describes the opt-in status applied to a stream processor's data sharing policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-datasharingpreference.html#cfn-rekognition-streamprocessor-datasharingpreference-optin
            '''
            result = self._values.get("opt_in")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSharingPreferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin.FaceSearchSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "collection_id": "collectionId",
            "face_match_threshold": "faceMatchThreshold",
        },
    )
    class FaceSearchSettingsProperty:
        def __init__(
            self,
            *,
            collection_id: typing.Optional[builtins.str] = None,
            face_match_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The input parameters used to recognize faces in a streaming video analyzed by a Amazon Rekognition stream processor.

            ``FaceSearchSettings`` is a request parameter for `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ . For more information, see `FaceSearchSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_FaceSearchSettings>`_ .

            :param collection_id: The ID of a collection that contains faces that you want to search for.
            :param face_match_threshold: Minimum face match confidence score that must be met to return a result for a recognized face. The default is 80. 0 is the lowest confidence. 100 is the highest confidence. Values between 0 and 100 are accepted, and values lower than 80 are set to 80.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-facesearchsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
                
                face_search_settings_property = rekognition_mixins.CfnStreamProcessorPropsMixin.FaceSearchSettingsProperty(
                    collection_id="collectionId",
                    face_match_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a98e2bf3b46d6a2712190eed94e4e3d663816c47546f7efb70317b689d68cc84)
                check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
                check_type(argname="argument face_match_threshold", value=face_match_threshold, expected_type=type_hints["face_match_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if collection_id is not None:
                self._values["collection_id"] = collection_id
            if face_match_threshold is not None:
                self._values["face_match_threshold"] = face_match_threshold

        @builtins.property
        def collection_id(self) -> typing.Optional[builtins.str]:
            '''The ID of a collection that contains faces that you want to search for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-facesearchsettings.html#cfn-rekognition-streamprocessor-facesearchsettings-collectionid
            '''
            result = self._values.get("collection_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def face_match_threshold(self) -> typing.Optional[jsii.Number]:
            '''Minimum face match confidence score that must be met to return a result for a recognized face.

            The default is 80. 0 is the lowest confidence. 100 is the highest confidence. Values between 0 and 100 are accepted, and values lower than 80 are set to 80.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-facesearchsettings.html#cfn-rekognition-streamprocessor-facesearchsettings-facematchthreshold
            '''
            result = self._values.get("face_match_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FaceSearchSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin.KinesisDataStreamProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class KinesisDataStreamProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''Amazon Rekognition Video Stream Processor take as input a Kinesis video stream (Input) and a Kinesis data stream (Output).

            This is the Amazon Kinesis Data Streams instance to which the Amazon Rekognition stream processor streams the analysis results. This must be created within the constraints specified at `KinesisDataStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisDataStream>`_ .

            :param arn: ARN of the output Amazon Kinesis Data Streams stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-kinesisdatastream.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
                
                kinesis_data_stream_property = rekognition_mixins.CfnStreamProcessorPropsMixin.KinesisDataStreamProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d79f4ac0ee5e27995eb9ce753eb9f90efa7589cd6fb872ef51a6cdc44132f265)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the output Amazon Kinesis Data Streams stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-kinesisdatastream.html#cfn-rekognition-streamprocessor-kinesisdatastream-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisDataStreamProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin.KinesisVideoStreamProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class KinesisVideoStreamProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''The Kinesis video stream that provides the source of the streaming video for an Amazon Rekognition Video stream processor.

            For more information, see `KinesisVideoStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisVideoStream>`_ .

            :param arn: ARN of the Kinesis video stream stream that streams the source video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-kinesisvideostream.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
                
                kinesis_video_stream_property = rekognition_mixins.CfnStreamProcessorPropsMixin.KinesisVideoStreamProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__555454e5d591a74288f5205bd81a132603b2a7a72a73012954105da0faf7d18f)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the Kinesis video stream stream that streams the source video.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-kinesisvideostream.html#cfn-rekognition-streamprocessor-kinesisvideostream-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisVideoStreamProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin.NotificationChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class NotificationChannelProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''The Amazon Simple Notification Service topic to which Amazon Rekognition publishes the object detection results and completion status of a video analysis operation.

            Amazon Rekognition publishes a notification the first time an object of interest or a person is detected in the video stream. Amazon Rekognition also publishes an an end-of-session notification with a summary when the stream processing session is complete. For more information, see `StreamProcessorNotificationChannel <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorNotificationChannel>`_ .

            :param arn: The ARN of the SNS topic that receives notifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-notificationchannel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
                
                notification_channel_property = rekognition_mixins.CfnStreamProcessorPropsMixin.NotificationChannelProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1acdc11f820ab3681422211730a767966b2cc057ae5363ce9b309c553cff5843)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the SNS topic that receives notifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-notificationchannel.html#cfn-rekognition-streamprocessor-notificationchannel-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin.PointProperty",
        jsii_struct_bases=[],
        name_mapping={"x": "x", "y": "y"},
    )
    class PointProperty:
        def __init__(
            self,
            *,
            x: typing.Optional[jsii.Number] = None,
            y: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The X and Y coordinates of a point on an image or video frame.

            The X and Y values are ratios of the overall image size or video resolution. For example, if the input image is 700x200 and the values are X=0.5 and Y=0.25, then the point is at the (350,50) pixel coordinate on the image.

            An array of ``Point`` objects, ``Polygon`` , is returned by `DetectText <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_DetectText>`_ and by `DetectCustomLabels <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_DetectCustomLabels>`_ or used to define regions of interest in Amazon Rekognition Video operations such as ``CreateStreamProcessor`` . ``Polygon`` represents a fine-grained polygon around a detected item. For more information, see `Geometry <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Geometry>`_ .

            :param x: The value of the X coordinate for a point on a ``Polygon`` .
            :param y: The value of the Y coordinate for a point on a ``Polygon`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-point.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
                
                point_property = rekognition_mixins.CfnStreamProcessorPropsMixin.PointProperty(
                    x=123,
                    y=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5917b0010c512c4fe3bd509ff12413c967891949f4a1472b4014a584a314bcc8)
                check_type(argname="argument x", value=x, expected_type=type_hints["x"])
                check_type(argname="argument y", value=y, expected_type=type_hints["y"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if x is not None:
                self._values["x"] = x
            if y is not None:
                self._values["y"] = y

        @builtins.property
        def x(self) -> typing.Optional[jsii.Number]:
            '''The value of the X coordinate for a point on a ``Polygon`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-point.html#cfn-rekognition-streamprocessor-point-x
            '''
            result = self._values.get("x")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def y(self) -> typing.Optional[jsii.Number]:
            '''The value of the Y coordinate for a point on a ``Polygon`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-point.html#cfn-rekognition-streamprocessor-point-y
            '''
            result = self._values.get("y")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_rekognition.mixins.CfnStreamProcessorPropsMixin.S3DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "object_key_prefix": "objectKeyPrefix",
        },
    )
    class S3DestinationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            object_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon S3 bucket location to which Amazon Rekognition publishes the detailed inference results of a video analysis operation.

            These results include the name of the stream processor resource, the session ID of the stream processing session, and labeled timestamps and bounding boxes for detected labels. For more information, see `S3Destination <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_S3Destination>`_ .

            :param bucket_name: Describes the destination Amazon Simple Storage Service (Amazon S3) bucket name of a stream processor's exports.
            :param object_key_prefix: Describes the destination Amazon Simple Storage Service (Amazon S3) object keys of a stream processor's exports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-s3destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_rekognition import mixins as rekognition_mixins
                
                s3_destination_property = rekognition_mixins.CfnStreamProcessorPropsMixin.S3DestinationProperty(
                    bucket_name="bucketName",
                    object_key_prefix="objectKeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c6880dc3afd8b7e371416e1a2911f83295e344d5ddf2e290c8fc8db11fd9df7)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if object_key_prefix is not None:
                self._values["object_key_prefix"] = object_key_prefix

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''Describes the destination Amazon Simple Storage Service (Amazon S3) bucket name of a stream processor's exports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-s3destination.html#cfn-rekognition-streamprocessor-s3destination-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_key_prefix(self) -> typing.Optional[builtins.str]:
            '''Describes the destination Amazon Simple Storage Service (Amazon S3) object keys of a stream processor's exports.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-s3destination.html#cfn-rekognition-streamprocessor-s3destination-objectkeyprefix
            '''
            result = self._values.get("object_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCollectionMixinProps",
    "CfnCollectionPropsMixin",
    "CfnProjectMixinProps",
    "CfnProjectPropsMixin",
    "CfnStreamProcessorMixinProps",
    "CfnStreamProcessorPropsMixin",
]

publication.publish()

def _typecheckingstub__4eaaec4b5f60fe9309cfb96e370ce2b053ada681c78b40486d01b617d5897e90(
    *,
    collection_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad8812c57a1c83a6f19522a96017d517e8e5b98ba1b391fb8185f618d857c36(
    props: typing.Union[CfnCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d414220f1956e27f0f738aa3fa536b2ec7408b1be16719bb16cda9dc9bf21a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ceb14432ef9fb7fb15c3ab11de478b346b9d3d798f9ea4a90ca2e82be68df0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eea4de502451c491813dfad9766a13d447f8411b485898ccd772dd64d81b25a(
    *,
    project_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4bf5af8cd0a7374b82eeecc827a5056b63de7142e423ed74cbc71fcf740e93(
    props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a00b0dc34c1df6aed04731c148c8680623a21e56943a4d6db951b0c9c61867a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0bf8d9f98dbb68c6c635e716ded34d80f44ee92b372f4ff2f67268be278093(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f399901cab0ddb6be2db1ebb9f2c4a4db1572d74ee8f611a5433eee48efadf6b(
    *,
    bounding_box_regions_of_interest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamProcessorPropsMixin.BoundingBoxProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    connected_home_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamProcessorPropsMixin.ConnectedHomeSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_sharing_preference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamProcessorPropsMixin.DataSharingPreferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    face_search_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamProcessorPropsMixin.FaceSearchSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_data_stream: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamProcessorPropsMixin.KinesisDataStreamProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_video_stream: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamProcessorPropsMixin.KinesisVideoStreamProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    notification_channel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamProcessorPropsMixin.NotificationChannelProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    polygon_regions_of_interest: typing.Any = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamProcessorPropsMixin.S3DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87359ed86d98b64edc1f2dd40bbea1f386e26984514201975960b1c7f495e55(
    props: typing.Union[CfnStreamProcessorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592cf7b03190368beb4519e94d18bc1ad92ca148f64a30a185748b37fd65ab4e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5dbef3d7eadca37d20db123387b8e98ae2de5e34e4c40b5dfd184827f3c5a12(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d47abf859936405c70e0b072b1383a54824e618f852bfd5511faf78f4250e3(
    *,
    height: typing.Optional[jsii.Number] = None,
    left: typing.Optional[jsii.Number] = None,
    top: typing.Optional[jsii.Number] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a655c99cd41c58cf65fa1adb637068b6ba9e1025c9d4f7a180990ec80ee0a47(
    *,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    min_confidence: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0b40c6dd860fc45c9aab2170c7d141ef7751534b53d3f3c28e6edc44b00aa5(
    *,
    opt_in: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98e2bf3b46d6a2712190eed94e4e3d663816c47546f7efb70317b689d68cc84(
    *,
    collection_id: typing.Optional[builtins.str] = None,
    face_match_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79f4ac0ee5e27995eb9ce753eb9f90efa7589cd6fb872ef51a6cdc44132f265(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555454e5d591a74288f5205bd81a132603b2a7a72a73012954105da0faf7d18f(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1acdc11f820ab3681422211730a767966b2cc057ae5363ce9b309c553cff5843(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5917b0010c512c4fe3bd509ff12413c967891949f4a1472b4014a584a314bcc8(
    *,
    x: typing.Optional[jsii.Number] = None,
    y: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6880dc3afd8b7e371416e1a2911f83295e344d5ddf2e290c8fc8db11fd9df7(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
