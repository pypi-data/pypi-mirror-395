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
    jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnLaunchProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "ec2_subnet_ids": "ec2SubnetIds",
        "launch_profile_protocol_versions": "launchProfileProtocolVersions",
        "name": "name",
        "stream_configuration": "streamConfiguration",
        "studio_component_ids": "studioComponentIds",
        "studio_id": "studioId",
        "tags": "tags",
    },
)
class CfnLaunchProfileMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        ec2_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        launch_profile_protocol_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        stream_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchProfilePropsMixin.StreamConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        studio_component_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        studio_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnLaunchProfilePropsMixin.

        :param description: 
        :param ec2_subnet_ids: 
        :param launch_profile_protocol_versions: 
        :param name: 
        :param stream_configuration: 
        :param studio_component_ids: 
        :param studio_id: 
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
            
            cfn_launch_profile_mixin_props = nimblestudio_mixins.CfnLaunchProfileMixinProps(
                description="description",
                ec2_subnet_ids=["ec2SubnetIds"],
                launch_profile_protocol_versions=["launchProfileProtocolVersions"],
                name="name",
                stream_configuration=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationProperty(
                    automatic_termination_mode="automaticTerminationMode",
                    clipboard_mode="clipboardMode",
                    ec2_instance_types=["ec2InstanceTypes"],
                    max_session_length_in_minutes=123,
                    max_stopped_session_length_in_minutes=123,
                    session_backup=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionBackupProperty(
                        max_backups_to_retain=123,
                        mode="mode"
                    ),
                    session_persistence_mode="sessionPersistenceMode",
                    session_storage=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionStorageProperty(
                        mode=["mode"],
                        root=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty(
                            linux="linux",
                            windows="windows"
                        )
                    ),
                    streaming_image_ids=["streamingImageIds"],
                    volume_configuration=nimblestudio_mixins.CfnLaunchProfilePropsMixin.VolumeConfigurationProperty(
                        iops=123,
                        size=123,
                        throughput=123
                    )
                ),
                studio_component_ids=["studioComponentIds"],
                studio_id="studioId",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8fdf768b5988a2c0edae90978df052e2a4dff30cf84f5a4e825eb0b129e425f)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ec2_subnet_ids", value=ec2_subnet_ids, expected_type=type_hints["ec2_subnet_ids"])
            check_type(argname="argument launch_profile_protocol_versions", value=launch_profile_protocol_versions, expected_type=type_hints["launch_profile_protocol_versions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stream_configuration", value=stream_configuration, expected_type=type_hints["stream_configuration"])
            check_type(argname="argument studio_component_ids", value=studio_component_ids, expected_type=type_hints["studio_component_ids"])
            check_type(argname="argument studio_id", value=studio_id, expected_type=type_hints["studio_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if ec2_subnet_ids is not None:
            self._values["ec2_subnet_ids"] = ec2_subnet_ids
        if launch_profile_protocol_versions is not None:
            self._values["launch_profile_protocol_versions"] = launch_profile_protocol_versions
        if name is not None:
            self._values["name"] = name
        if stream_configuration is not None:
            self._values["stream_configuration"] = stream_configuration
        if studio_component_ids is not None:
            self._values["studio_component_ids"] = studio_component_ids
        if studio_id is not None:
            self._values["studio_id"] = studio_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-ec2subnetids
        '''
        result = self._values.get("ec2_subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def launch_profile_protocol_versions(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-launchprofileprotocolversions
        '''
        result = self._values.get("launch_profile_protocol_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.StreamConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-streamconfiguration
        '''
        result = self._values.get("stream_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.StreamConfigurationProperty"]], result)

    @builtins.property
    def studio_component_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-studiocomponentids
        '''
        result = self._values.get("studio_component_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def studio_id(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-studioid
        '''
        result = self._values.get("studio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLaunchProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnLaunchProfilePropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html
    :cloudformationResource: AWS::NimbleStudio::LaunchProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
        
        cfn_launch_profile_props_mixin = nimblestudio_mixins.CfnLaunchProfilePropsMixin(nimblestudio_mixins.CfnLaunchProfileMixinProps(
            description="description",
            ec2_subnet_ids=["ec2SubnetIds"],
            launch_profile_protocol_versions=["launchProfileProtocolVersions"],
            name="name",
            stream_configuration=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationProperty(
                automatic_termination_mode="automaticTerminationMode",
                clipboard_mode="clipboardMode",
                ec2_instance_types=["ec2InstanceTypes"],
                max_session_length_in_minutes=123,
                max_stopped_session_length_in_minutes=123,
                session_backup=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionBackupProperty(
                    max_backups_to_retain=123,
                    mode="mode"
                ),
                session_persistence_mode="sessionPersistenceMode",
                session_storage=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionStorageProperty(
                    mode=["mode"],
                    root=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty(
                        linux="linux",
                        windows="windows"
                    )
                ),
                streaming_image_ids=["streamingImageIds"],
                volume_configuration=nimblestudio_mixins.CfnLaunchProfilePropsMixin.VolumeConfigurationProperty(
                    iops=123,
                    size=123,
                    throughput=123
                )
            ),
            studio_component_ids=["studioComponentIds"],
            studio_id="studioId",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLaunchProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NimbleStudio::LaunchProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53487321a1a17d63c0b3fe0dbc72329d5c78231bb68062b87949d73a3b57a4da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bab25b2992af2b2c8171224f3eaa10ab3f402090570dff6bb773a54f3279c6ad)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5b6cd380a49d85aac8b3d317c503b52e7de72943091aa0f31cee695577feb1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLaunchProfileMixinProps:
        return typing.cast(CfnLaunchProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnLaunchProfilePropsMixin.StreamConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automatic_termination_mode": "automaticTerminationMode",
            "clipboard_mode": "clipboardMode",
            "ec2_instance_types": "ec2InstanceTypes",
            "max_session_length_in_minutes": "maxSessionLengthInMinutes",
            "max_stopped_session_length_in_minutes": "maxStoppedSessionLengthInMinutes",
            "session_backup": "sessionBackup",
            "session_persistence_mode": "sessionPersistenceMode",
            "session_storage": "sessionStorage",
            "streaming_image_ids": "streamingImageIds",
            "volume_configuration": "volumeConfiguration",
        },
    )
    class StreamConfigurationProperty:
        def __init__(
            self,
            *,
            automatic_termination_mode: typing.Optional[builtins.str] = None,
            clipboard_mode: typing.Optional[builtins.str] = None,
            ec2_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            max_session_length_in_minutes: typing.Optional[jsii.Number] = None,
            max_stopped_session_length_in_minutes: typing.Optional[jsii.Number] = None,
            session_backup: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchProfilePropsMixin.StreamConfigurationSessionBackupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            session_persistence_mode: typing.Optional[builtins.str] = None,
            session_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchProfilePropsMixin.StreamConfigurationSessionStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            streaming_image_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            volume_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchProfilePropsMixin.VolumeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param automatic_termination_mode: 
            :param clipboard_mode: 
            :param ec2_instance_types: 
            :param max_session_length_in_minutes: 
            :param max_stopped_session_length_in_minutes: 
            :param session_backup: 
            :param session_persistence_mode: 
            :param session_storage: 
            :param streaming_image_ids: 
            :param volume_configuration: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                stream_configuration_property = nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationProperty(
                    automatic_termination_mode="automaticTerminationMode",
                    clipboard_mode="clipboardMode",
                    ec2_instance_types=["ec2InstanceTypes"],
                    max_session_length_in_minutes=123,
                    max_stopped_session_length_in_minutes=123,
                    session_backup=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionBackupProperty(
                        max_backups_to_retain=123,
                        mode="mode"
                    ),
                    session_persistence_mode="sessionPersistenceMode",
                    session_storage=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionStorageProperty(
                        mode=["mode"],
                        root=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty(
                            linux="linux",
                            windows="windows"
                        )
                    ),
                    streaming_image_ids=["streamingImageIds"],
                    volume_configuration=nimblestudio_mixins.CfnLaunchProfilePropsMixin.VolumeConfigurationProperty(
                        iops=123,
                        size=123,
                        throughput=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66159604e1e0b15e9c7e72e5802c1a16b1cc5094927fc43a792d1fdafbb6ccf0)
                check_type(argname="argument automatic_termination_mode", value=automatic_termination_mode, expected_type=type_hints["automatic_termination_mode"])
                check_type(argname="argument clipboard_mode", value=clipboard_mode, expected_type=type_hints["clipboard_mode"])
                check_type(argname="argument ec2_instance_types", value=ec2_instance_types, expected_type=type_hints["ec2_instance_types"])
                check_type(argname="argument max_session_length_in_minutes", value=max_session_length_in_minutes, expected_type=type_hints["max_session_length_in_minutes"])
                check_type(argname="argument max_stopped_session_length_in_minutes", value=max_stopped_session_length_in_minutes, expected_type=type_hints["max_stopped_session_length_in_minutes"])
                check_type(argname="argument session_backup", value=session_backup, expected_type=type_hints["session_backup"])
                check_type(argname="argument session_persistence_mode", value=session_persistence_mode, expected_type=type_hints["session_persistence_mode"])
                check_type(argname="argument session_storage", value=session_storage, expected_type=type_hints["session_storage"])
                check_type(argname="argument streaming_image_ids", value=streaming_image_ids, expected_type=type_hints["streaming_image_ids"])
                check_type(argname="argument volume_configuration", value=volume_configuration, expected_type=type_hints["volume_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic_termination_mode is not None:
                self._values["automatic_termination_mode"] = automatic_termination_mode
            if clipboard_mode is not None:
                self._values["clipboard_mode"] = clipboard_mode
            if ec2_instance_types is not None:
                self._values["ec2_instance_types"] = ec2_instance_types
            if max_session_length_in_minutes is not None:
                self._values["max_session_length_in_minutes"] = max_session_length_in_minutes
            if max_stopped_session_length_in_minutes is not None:
                self._values["max_stopped_session_length_in_minutes"] = max_stopped_session_length_in_minutes
            if session_backup is not None:
                self._values["session_backup"] = session_backup
            if session_persistence_mode is not None:
                self._values["session_persistence_mode"] = session_persistence_mode
            if session_storage is not None:
                self._values["session_storage"] = session_storage
            if streaming_image_ids is not None:
                self._values["streaming_image_ids"] = streaming_image_ids
            if volume_configuration is not None:
                self._values["volume_configuration"] = volume_configuration

        @builtins.property
        def automatic_termination_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-automaticterminationmode
            '''
            result = self._values.get("automatic_termination_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def clipboard_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-clipboardmode
            '''
            result = self._values.get("clipboard_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ec2_instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-ec2instancetypes
            '''
            result = self._values.get("ec2_instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def max_session_length_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-maxsessionlengthinminutes
            '''
            result = self._values.get("max_session_length_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_stopped_session_length_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-maxstoppedsessionlengthinminutes
            '''
            result = self._values.get("max_stopped_session_length_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def session_backup(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.StreamConfigurationSessionBackupProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-sessionbackup
            '''
            result = self._values.get("session_backup")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.StreamConfigurationSessionBackupProperty"]], result)

        @builtins.property
        def session_persistence_mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-sessionpersistencemode
            '''
            result = self._values.get("session_persistence_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.StreamConfigurationSessionStorageProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-sessionstorage
            '''
            result = self._values.get("session_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.StreamConfigurationSessionStorageProperty"]], result)

        @builtins.property
        def streaming_image_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-streamingimageids
            '''
            result = self._values.get("streaming_image_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def volume_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.VolumeConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-volumeconfiguration
            '''
            result = self._values.get("volume_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.VolumeConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionBackupProperty",
        jsii_struct_bases=[],
        name_mapping={"max_backups_to_retain": "maxBackupsToRetain", "mode": "mode"},
    )
    class StreamConfigurationSessionBackupProperty:
        def __init__(
            self,
            *,
            max_backups_to_retain: typing.Optional[jsii.Number] = None,
            mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param max_backups_to_retain: 
            :param mode: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfigurationsessionbackup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                stream_configuration_session_backup_property = nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionBackupProperty(
                    max_backups_to_retain=123,
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de1e3ab63a3d70755319091359067d6783250a676e931b224d4966ef413623f9)
                check_type(argname="argument max_backups_to_retain", value=max_backups_to_retain, expected_type=type_hints["max_backups_to_retain"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_backups_to_retain is not None:
                self._values["max_backups_to_retain"] = max_backups_to_retain
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def max_backups_to_retain(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfigurationsessionbackup.html#cfn-nimblestudio-launchprofile-streamconfigurationsessionbackup-maxbackupstoretain
            '''
            result = self._values.get("max_backups_to_retain")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfigurationsessionbackup.html#cfn-nimblestudio-launchprofile-streamconfigurationsessionbackup-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamConfigurationSessionBackupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode", "root": "root"},
    )
    class StreamConfigurationSessionStorageProperty:
        def __init__(
            self,
            *,
            mode: typing.Optional[typing.Sequence[builtins.str]] = None,
            root: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param mode: 
            :param root: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfigurationsessionstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                stream_configuration_session_storage_property = nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamConfigurationSessionStorageProperty(
                    mode=["mode"],
                    root=nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty(
                        linux="linux",
                        windows="windows"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4e0323aae0f131ec6784686195eed10edd33d50a5e71e94acb32f2e26207f15)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument root", value=root, expected_type=type_hints["root"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode
            if root is not None:
                self._values["root"] = root

        @builtins.property
        def mode(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfigurationsessionstorage.html#cfn-nimblestudio-launchprofile-streamconfigurationsessionstorage-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def root(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfigurationsessionstorage.html#cfn-nimblestudio-launchprofile-streamconfigurationsessionstorage-root
            '''
            result = self._values.get("root")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamConfigurationSessionStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty",
        jsii_struct_bases=[],
        name_mapping={"linux": "linux", "windows": "windows"},
    )
    class StreamingSessionStorageRootProperty:
        def __init__(
            self,
            *,
            linux: typing.Optional[builtins.str] = None,
            windows: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param linux: 
            :param windows: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamingsessionstorageroot.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                streaming_session_storage_root_property = nimblestudio_mixins.CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty(
                    linux="linux",
                    windows="windows"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c57930f4ee97bc45870ca43b36f15bd3eab4907b8dedda0f57641a2e23baaabb)
                check_type(argname="argument linux", value=linux, expected_type=type_hints["linux"])
                check_type(argname="argument windows", value=windows, expected_type=type_hints["windows"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if linux is not None:
                self._values["linux"] = linux
            if windows is not None:
                self._values["windows"] = windows

        @builtins.property
        def linux(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamingsessionstorageroot.html#cfn-nimblestudio-launchprofile-streamingsessionstorageroot-linux
            '''
            result = self._values.get("linux")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def windows(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamingsessionstorageroot.html#cfn-nimblestudio-launchprofile-streamingsessionstorageroot-windows
            '''
            result = self._values.get("windows")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamingSessionStorageRootProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnLaunchProfilePropsMixin.VolumeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"iops": "iops", "size": "size", "throughput": "throughput"},
    )
    class VolumeConfigurationProperty:
        def __init__(
            self,
            *,
            iops: typing.Optional[jsii.Number] = None,
            size: typing.Optional[jsii.Number] = None,
            throughput: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param iops: 
            :param size: 
            :param throughput: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-volumeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                volume_configuration_property = nimblestudio_mixins.CfnLaunchProfilePropsMixin.VolumeConfigurationProperty(
                    iops=123,
                    size=123,
                    throughput=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4f0da5f3082c61e141d5c2e171749c4fd80f1c7d463dec58469e3b4f7f61ce9)
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iops is not None:
                self._values["iops"] = iops
            if size is not None:
                self._values["size"] = size
            if throughput is not None:
                self._values["throughput"] = throughput

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-volumeconfiguration.html#cfn-nimblestudio-launchprofile-volumeconfiguration-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-volumeconfiguration.html#cfn-nimblestudio-launchprofile-volumeconfiguration-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-volumeconfiguration.html#cfn-nimblestudio-launchprofile-volumeconfiguration-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStreamingImageMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "ec2_image_id": "ec2ImageId",
        "name": "name",
        "studio_id": "studioId",
        "tags": "tags",
    },
)
class CfnStreamingImageMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        ec2_image_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        studio_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnStreamingImagePropsMixin.

        :param description: 
        :param ec2_image_id: 
        :param name: 
        :param studio_id: 
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
            
            cfn_streaming_image_mixin_props = nimblestudio_mixins.CfnStreamingImageMixinProps(
                description="description",
                ec2_image_id="ec2ImageId",
                name="name",
                studio_id="studioId",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e915832123172290b0e76ff06af51b7c4d10b1299389be1c12b13233a0e8c8fb)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ec2_image_id", value=ec2_image_id, expected_type=type_hints["ec2_image_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument studio_id", value=studio_id, expected_type=type_hints["studio_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if ec2_image_id is not None:
            self._values["ec2_image_id"] = ec2_image_id
        if name is not None:
            self._values["name"] = name
        if studio_id is not None:
            self._values["studio_id"] = studio_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_image_id(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-ec2imageid
        '''
        result = self._values.get("ec2_image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def studio_id(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-studioid
        '''
        result = self._values.get("studio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamingImageMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStreamingImagePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStreamingImagePropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html
    :cloudformationResource: AWS::NimbleStudio::StreamingImage
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
        
        cfn_streaming_image_props_mixin = nimblestudio_mixins.CfnStreamingImagePropsMixin(nimblestudio_mixins.CfnStreamingImageMixinProps(
            description="description",
            ec2_image_id="ec2ImageId",
            name="name",
            studio_id="studioId",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStreamingImageMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NimbleStudio::StreamingImage``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd90898e892273ed86ad5be4eb1e6c9e7389730aa8c440fe20922088753ed64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fd14fbcfe2a78815f4ae91cfe3ea6a9dc2015e94b3dd2009aeb9a2eebc316f9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a1dfe9910095ed15062c27e90e0e19ccabbd57ea8329cf15908724dcc01a9d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStreamingImageMixinProps:
        return typing.cast(CfnStreamingImageMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStreamingImagePropsMixin.StreamingImageEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"key_arn": "keyArn", "key_type": "keyType"},
    )
    class StreamingImageEncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            key_arn: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key_arn: 
            :param key_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-streamingimage-streamingimageencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                streaming_image_encryption_configuration_property = nimblestudio_mixins.CfnStreamingImagePropsMixin.StreamingImageEncryptionConfigurationProperty(
                    key_arn="keyArn",
                    key_type="keyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd9de0c9133c610837b3775afea8c06260c1064733da596a77a0795bc10b829a)
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_arn is not None:
                self._values["key_arn"] = key_arn
            if key_type is not None:
                self._values["key_type"] = key_type

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-streamingimage-streamingimageencryptionconfiguration.html#cfn-nimblestudio-streamingimage-streamingimageencryptionconfiguration-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-streamingimage-streamingimageencryptionconfiguration.html#cfn-nimblestudio-streamingimage-streamingimageencryptionconfiguration-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamingImageEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "description": "description",
        "ec2_security_group_ids": "ec2SecurityGroupIds",
        "initialization_scripts": "initializationScripts",
        "name": "name",
        "script_parameters": "scriptParameters",
        "studio_id": "studioId",
        "subtype": "subtype",
        "tags": "tags",
        "type": "type",
    },
)
class CfnStudioComponentMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStudioComponentPropsMixin.StudioComponentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        ec2_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        initialization_scripts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStudioComponentPropsMixin.StudioComponentInitializationScriptProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        script_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStudioComponentPropsMixin.ScriptParameterKeyValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        studio_id: typing.Optional[builtins.str] = None,
        subtype: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStudioComponentPropsMixin.

        :param configuration: 
        :param description: 
        :param ec2_security_group_ids: 
        :param initialization_scripts: 
        :param name: 
        :param script_parameters: 
        :param studio_id: 
        :param subtype: 
        :param tags: 
        :param type: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
            
            cfn_studio_component_mixin_props = nimblestudio_mixins.CfnStudioComponentMixinProps(
                configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.StudioComponentConfigurationProperty(
                    active_directory_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.ActiveDirectoryConfigurationProperty(
                        computer_attributes=[nimblestudio_mixins.CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty(
                            name="name",
                            value="value"
                        )],
                        directory_id="directoryId",
                        organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                    ),
                    compute_farm_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.ComputeFarmConfigurationProperty(
                        active_directory_user="activeDirectoryUser",
                        endpoint="endpoint"
                    ),
                    license_service_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.LicenseServiceConfigurationProperty(
                        endpoint="endpoint"
                    ),
                    shared_file_system_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.SharedFileSystemConfigurationProperty(
                        endpoint="endpoint",
                        file_system_id="fileSystemId",
                        linux_mount_point="linuxMountPoint",
                        share_name="shareName",
                        windows_mount_drive="windowsMountDrive"
                    )
                ),
                description="description",
                ec2_security_group_ids=["ec2SecurityGroupIds"],
                initialization_scripts=[nimblestudio_mixins.CfnStudioComponentPropsMixin.StudioComponentInitializationScriptProperty(
                    launch_profile_protocol_version="launchProfileProtocolVersion",
                    platform="platform",
                    run_context="runContext",
                    script="script"
                )],
                name="name",
                script_parameters=[nimblestudio_mixins.CfnStudioComponentPropsMixin.ScriptParameterKeyValueProperty(
                    key="key",
                    value="value"
                )],
                studio_id="studioId",
                subtype="subtype",
                tags={
                    "tags_key": "tags"
                },
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba1372431139e4349e6afa90bcc496f4af395a9964d28013840c1b1d1e7bc1c)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ec2_security_group_ids", value=ec2_security_group_ids, expected_type=type_hints["ec2_security_group_ids"])
            check_type(argname="argument initialization_scripts", value=initialization_scripts, expected_type=type_hints["initialization_scripts"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument script_parameters", value=script_parameters, expected_type=type_hints["script_parameters"])
            check_type(argname="argument studio_id", value=studio_id, expected_type=type_hints["studio_id"])
            check_type(argname="argument subtype", value=subtype, expected_type=type_hints["subtype"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if ec2_security_group_ids is not None:
            self._values["ec2_security_group_ids"] = ec2_security_group_ids
        if initialization_scripts is not None:
            self._values["initialization_scripts"] = initialization_scripts
        if name is not None:
            self._values["name"] = name
        if script_parameters is not None:
            self._values["script_parameters"] = script_parameters
        if studio_id is not None:
            self._values["studio_id"] = studio_id
        if subtype is not None:
            self._values["subtype"] = subtype
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.StudioComponentConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.StudioComponentConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-ec2securitygroupids
        '''
        result = self._values.get("ec2_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def initialization_scripts(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.StudioComponentInitializationScriptProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-initializationscripts
        '''
        result = self._values.get("initialization_scripts")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.StudioComponentInitializationScriptProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.ScriptParameterKeyValueProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-scriptparameters
        '''
        result = self._values.get("script_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.ScriptParameterKeyValueProperty"]]]], result)

    @builtins.property
    def studio_id(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-studioid
        '''
        result = self._values.get("studio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subtype(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-subtype
        '''
        result = self._values.get("subtype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStudioComponentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStudioComponentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html
    :cloudformationResource: AWS::NimbleStudio::StudioComponent
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
        
        cfn_studio_component_props_mixin = nimblestudio_mixins.CfnStudioComponentPropsMixin(nimblestudio_mixins.CfnStudioComponentMixinProps(
            configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.StudioComponentConfigurationProperty(
                active_directory_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.ActiveDirectoryConfigurationProperty(
                    computer_attributes=[nimblestudio_mixins.CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty(
                        name="name",
                        value="value"
                    )],
                    directory_id="directoryId",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                ),
                compute_farm_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.ComputeFarmConfigurationProperty(
                    active_directory_user="activeDirectoryUser",
                    endpoint="endpoint"
                ),
                license_service_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.LicenseServiceConfigurationProperty(
                    endpoint="endpoint"
                ),
                shared_file_system_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.SharedFileSystemConfigurationProperty(
                    endpoint="endpoint",
                    file_system_id="fileSystemId",
                    linux_mount_point="linuxMountPoint",
                    share_name="shareName",
                    windows_mount_drive="windowsMountDrive"
                )
            ),
            description="description",
            ec2_security_group_ids=["ec2SecurityGroupIds"],
            initialization_scripts=[nimblestudio_mixins.CfnStudioComponentPropsMixin.StudioComponentInitializationScriptProperty(
                launch_profile_protocol_version="launchProfileProtocolVersion",
                platform="platform",
                run_context="runContext",
                script="script"
            )],
            name="name",
            script_parameters=[nimblestudio_mixins.CfnStudioComponentPropsMixin.ScriptParameterKeyValueProperty(
                key="key",
                value="value"
            )],
            studio_id="studioId",
            subtype="subtype",
            tags={
                "tags_key": "tags"
            },
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStudioComponentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NimbleStudio::StudioComponent``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5e657cb2b187a278e22fdbc14ce3acd34d3f57149a2c549c22229df3561c0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceead7746d29597976794d74d2369e6d449fe8bd6d11de32e32c5afd13ac01b2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a60586b0a3706693b3e48b4e804d82506434e7a8f0a855b0352af5f6f2da1bc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStudioComponentMixinProps:
        return typing.cast(CfnStudioComponentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ActiveDirectoryComputerAttributeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectorycomputerattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                active_directory_computer_attribute_property = nimblestudio_mixins.CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79151c931926cd170b5d11382406e6a5d7c35ebaa64abcf61c3bf46c9e969ff0)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectorycomputerattribute.html#cfn-nimblestudio-studiocomponent-activedirectorycomputerattribute-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectorycomputerattribute.html#cfn-nimblestudio-studiocomponent-activedirectorycomputerattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActiveDirectoryComputerAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentPropsMixin.ActiveDirectoryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "computer_attributes": "computerAttributes",
            "directory_id": "directoryId",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
        },
    )
    class ActiveDirectoryConfigurationProperty:
        def __init__(
            self,
            *,
            computer_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            directory_id: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param computer_attributes: 
            :param directory_id: 
            :param organizational_unit_distinguished_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectoryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                active_directory_configuration_property = nimblestudio_mixins.CfnStudioComponentPropsMixin.ActiveDirectoryConfigurationProperty(
                    computer_attributes=[nimblestudio_mixins.CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty(
                        name="name",
                        value="value"
                    )],
                    directory_id="directoryId",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c253d6b457a24f6308f37c37f70d09f6d78f1ea1950255ca4f5d835b80bff5b9)
                check_type(argname="argument computer_attributes", value=computer_attributes, expected_type=type_hints["computer_attributes"])
                check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
                check_type(argname="argument organizational_unit_distinguished_name", value=organizational_unit_distinguished_name, expected_type=type_hints["organizational_unit_distinguished_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if computer_attributes is not None:
                self._values["computer_attributes"] = computer_attributes
            if directory_id is not None:
                self._values["directory_id"] = directory_id
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

        @builtins.property
        def computer_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectoryconfiguration.html#cfn-nimblestudio-studiocomponent-activedirectoryconfiguration-computerattributes
            '''
            result = self._values.get("computer_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty"]]]], result)

        @builtins.property
        def directory_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectoryconfiguration.html#cfn-nimblestudio-studiocomponent-activedirectoryconfiguration-directoryid
            '''
            result = self._values.get("directory_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectoryconfiguration.html#cfn-nimblestudio-studiocomponent-activedirectoryconfiguration-organizationalunitdistinguishedname
            '''
            result = self._values.get("organizational_unit_distinguished_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActiveDirectoryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentPropsMixin.ComputeFarmConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active_directory_user": "activeDirectoryUser",
            "endpoint": "endpoint",
        },
    )
    class ComputeFarmConfigurationProperty:
        def __init__(
            self,
            *,
            active_directory_user: typing.Optional[builtins.str] = None,
            endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param active_directory_user: 
            :param endpoint: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-computefarmconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                compute_farm_configuration_property = nimblestudio_mixins.CfnStudioComponentPropsMixin.ComputeFarmConfigurationProperty(
                    active_directory_user="activeDirectoryUser",
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5019473acc5871b458c9e96e319215fdb93a909f43217d55d45ea9fd097c5d0)
                check_type(argname="argument active_directory_user", value=active_directory_user, expected_type=type_hints["active_directory_user"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active_directory_user is not None:
                self._values["active_directory_user"] = active_directory_user
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def active_directory_user(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-computefarmconfiguration.html#cfn-nimblestudio-studiocomponent-computefarmconfiguration-activedirectoryuser
            '''
            result = self._values.get("active_directory_user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-computefarmconfiguration.html#cfn-nimblestudio-studiocomponent-computefarmconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeFarmConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentPropsMixin.LicenseServiceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint": "endpoint"},
    )
    class LicenseServiceConfigurationProperty:
        def __init__(self, *, endpoint: typing.Optional[builtins.str] = None) -> None:
            '''
            :param endpoint: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-licenseserviceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                license_service_configuration_property = nimblestudio_mixins.CfnStudioComponentPropsMixin.LicenseServiceConfigurationProperty(
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf57f92c7d04b16f6f39c29a2f4e50a911e7e15e685e984157c7a862cb46efa3)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-licenseserviceconfiguration.html#cfn-nimblestudio-studiocomponent-licenseserviceconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LicenseServiceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentPropsMixin.ScriptParameterKeyValueProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ScriptParameterKeyValueProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key: 
            :param value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-scriptparameterkeyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                script_parameter_key_value_property = nimblestudio_mixins.CfnStudioComponentPropsMixin.ScriptParameterKeyValueProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92da1cc94580b0bf36833dcb28c3fb4dd2a097caf3515fd5c653e39a20779986)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-scriptparameterkeyvalue.html#cfn-nimblestudio-studiocomponent-scriptparameterkeyvalue-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-scriptparameterkeyvalue.html#cfn-nimblestudio-studiocomponent-scriptparameterkeyvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScriptParameterKeyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentPropsMixin.SharedFileSystemConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint": "endpoint",
            "file_system_id": "fileSystemId",
            "linux_mount_point": "linuxMountPoint",
            "share_name": "shareName",
            "windows_mount_drive": "windowsMountDrive",
        },
    )
    class SharedFileSystemConfigurationProperty:
        def __init__(
            self,
            *,
            endpoint: typing.Optional[builtins.str] = None,
            file_system_id: typing.Optional[builtins.str] = None,
            linux_mount_point: typing.Optional[builtins.str] = None,
            share_name: typing.Optional[builtins.str] = None,
            windows_mount_drive: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param endpoint: 
            :param file_system_id: 
            :param linux_mount_point: 
            :param share_name: 
            :param windows_mount_drive: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                shared_file_system_configuration_property = nimblestudio_mixins.CfnStudioComponentPropsMixin.SharedFileSystemConfigurationProperty(
                    endpoint="endpoint",
                    file_system_id="fileSystemId",
                    linux_mount_point="linuxMountPoint",
                    share_name="shareName",
                    windows_mount_drive="windowsMountDrive"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f71e54923ae97e78351b07afc3558a4a3c364c9002f039a379a1840b400d80df)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
                check_type(argname="argument linux_mount_point", value=linux_mount_point, expected_type=type_hints["linux_mount_point"])
                check_type(argname="argument share_name", value=share_name, expected_type=type_hints["share_name"])
                check_type(argname="argument windows_mount_drive", value=windows_mount_drive, expected_type=type_hints["windows_mount_drive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if file_system_id is not None:
                self._values["file_system_id"] = file_system_id
            if linux_mount_point is not None:
                self._values["linux_mount_point"] = linux_mount_point
            if share_name is not None:
                self._values["share_name"] = share_name
            if windows_mount_drive is not None:
                self._values["windows_mount_drive"] = windows_mount_drive

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_system_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-filesystemid
            '''
            result = self._values.get("file_system_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def linux_mount_point(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-linuxmountpoint
            '''
            result = self._values.get("linux_mount_point")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def share_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-sharename
            '''
            result = self._values.get("share_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def windows_mount_drive(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-windowsmountdrive
            '''
            result = self._values.get("windows_mount_drive")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SharedFileSystemConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentPropsMixin.StudioComponentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active_directory_configuration": "activeDirectoryConfiguration",
            "compute_farm_configuration": "computeFarmConfiguration",
            "license_service_configuration": "licenseServiceConfiguration",
            "shared_file_system_configuration": "sharedFileSystemConfiguration",
        },
    )
    class StudioComponentConfigurationProperty:
        def __init__(
            self,
            *,
            active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStudioComponentPropsMixin.ActiveDirectoryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            compute_farm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStudioComponentPropsMixin.ComputeFarmConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            license_service_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStudioComponentPropsMixin.LicenseServiceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            shared_file_system_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStudioComponentPropsMixin.SharedFileSystemConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param active_directory_configuration: 
            :param compute_farm_configuration: 
            :param license_service_configuration: 
            :param shared_file_system_configuration: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                studio_component_configuration_property = nimblestudio_mixins.CfnStudioComponentPropsMixin.StudioComponentConfigurationProperty(
                    active_directory_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.ActiveDirectoryConfigurationProperty(
                        computer_attributes=[nimblestudio_mixins.CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty(
                            name="name",
                            value="value"
                        )],
                        directory_id="directoryId",
                        organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                    ),
                    compute_farm_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.ComputeFarmConfigurationProperty(
                        active_directory_user="activeDirectoryUser",
                        endpoint="endpoint"
                    ),
                    license_service_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.LicenseServiceConfigurationProperty(
                        endpoint="endpoint"
                    ),
                    shared_file_system_configuration=nimblestudio_mixins.CfnStudioComponentPropsMixin.SharedFileSystemConfigurationProperty(
                        endpoint="endpoint",
                        file_system_id="fileSystemId",
                        linux_mount_point="linuxMountPoint",
                        share_name="shareName",
                        windows_mount_drive="windowsMountDrive"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8bbe1df3863411ecfcde2056db84159a71e00c67b1707cdf7ec78fdc409166c)
                check_type(argname="argument active_directory_configuration", value=active_directory_configuration, expected_type=type_hints["active_directory_configuration"])
                check_type(argname="argument compute_farm_configuration", value=compute_farm_configuration, expected_type=type_hints["compute_farm_configuration"])
                check_type(argname="argument license_service_configuration", value=license_service_configuration, expected_type=type_hints["license_service_configuration"])
                check_type(argname="argument shared_file_system_configuration", value=shared_file_system_configuration, expected_type=type_hints["shared_file_system_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active_directory_configuration is not None:
                self._values["active_directory_configuration"] = active_directory_configuration
            if compute_farm_configuration is not None:
                self._values["compute_farm_configuration"] = compute_farm_configuration
            if license_service_configuration is not None:
                self._values["license_service_configuration"] = license_service_configuration
            if shared_file_system_configuration is not None:
                self._values["shared_file_system_configuration"] = shared_file_system_configuration

        @builtins.property
        def active_directory_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.ActiveDirectoryConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html#cfn-nimblestudio-studiocomponent-studiocomponentconfiguration-activedirectoryconfiguration
            '''
            result = self._values.get("active_directory_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.ActiveDirectoryConfigurationProperty"]], result)

        @builtins.property
        def compute_farm_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.ComputeFarmConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html#cfn-nimblestudio-studiocomponent-studiocomponentconfiguration-computefarmconfiguration
            '''
            result = self._values.get("compute_farm_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.ComputeFarmConfigurationProperty"]], result)

        @builtins.property
        def license_service_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.LicenseServiceConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html#cfn-nimblestudio-studiocomponent-studiocomponentconfiguration-licenseserviceconfiguration
            '''
            result = self._values.get("license_service_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.LicenseServiceConfigurationProperty"]], result)

        @builtins.property
        def shared_file_system_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.SharedFileSystemConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html#cfn-nimblestudio-studiocomponent-studiocomponentconfiguration-sharedfilesystemconfiguration
            '''
            result = self._values.get("shared_file_system_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioComponentPropsMixin.SharedFileSystemConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StudioComponentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioComponentPropsMixin.StudioComponentInitializationScriptProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_profile_protocol_version": "launchProfileProtocolVersion",
            "platform": "platform",
            "run_context": "runContext",
            "script": "script",
        },
    )
    class StudioComponentInitializationScriptProperty:
        def __init__(
            self,
            *,
            launch_profile_protocol_version: typing.Optional[builtins.str] = None,
            platform: typing.Optional[builtins.str] = None,
            run_context: typing.Optional[builtins.str] = None,
            script: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param launch_profile_protocol_version: 
            :param platform: 
            :param run_context: 
            :param script: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                studio_component_initialization_script_property = nimblestudio_mixins.CfnStudioComponentPropsMixin.StudioComponentInitializationScriptProperty(
                    launch_profile_protocol_version="launchProfileProtocolVersion",
                    platform="platform",
                    run_context="runContext",
                    script="script"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7efe74291570df153e977df3f4e3685e24367744d59d003f432aba58682fa307)
                check_type(argname="argument launch_profile_protocol_version", value=launch_profile_protocol_version, expected_type=type_hints["launch_profile_protocol_version"])
                check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
                check_type(argname="argument run_context", value=run_context, expected_type=type_hints["run_context"])
                check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if launch_profile_protocol_version is not None:
                self._values["launch_profile_protocol_version"] = launch_profile_protocol_version
            if platform is not None:
                self._values["platform"] = platform
            if run_context is not None:
                self._values["run_context"] = run_context
            if script is not None:
                self._values["script"] = script

        @builtins.property
        def launch_profile_protocol_version(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html#cfn-nimblestudio-studiocomponent-studiocomponentinitializationscript-launchprofileprotocolversion
            '''
            result = self._values.get("launch_profile_protocol_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def platform(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html#cfn-nimblestudio-studiocomponent-studiocomponentinitializationscript-platform
            '''
            result = self._values.get("platform")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def run_context(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html#cfn-nimblestudio-studiocomponent-studiocomponentinitializationscript-runcontext
            '''
            result = self._values.get("run_context")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def script(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html#cfn-nimblestudio-studiocomponent-studiocomponentinitializationscript-script
            '''
            result = self._values.get("script")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StudioComponentInitializationScriptProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_role_arn": "adminRoleArn",
        "display_name": "displayName",
        "studio_encryption_configuration": "studioEncryptionConfiguration",
        "studio_name": "studioName",
        "tags": "tags",
        "user_role_arn": "userRoleArn",
    },
)
class CfnStudioMixinProps:
    def __init__(
        self,
        *,
        admin_role_arn: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        studio_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStudioPropsMixin.StudioEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        studio_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStudioPropsMixin.

        :param admin_role_arn: 
        :param display_name: 
        :param studio_encryption_configuration: 
        :param studio_name: 
        :param tags: 
        :param user_role_arn: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
            
            cfn_studio_mixin_props = nimblestudio_mixins.CfnStudioMixinProps(
                admin_role_arn="adminRoleArn",
                display_name="displayName",
                studio_encryption_configuration=nimblestudio_mixins.CfnStudioPropsMixin.StudioEncryptionConfigurationProperty(
                    key_arn="keyArn",
                    key_type="keyType"
                ),
                studio_name="studioName",
                tags={
                    "tags_key": "tags"
                },
                user_role_arn="userRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6ed7b1dc5b6fa3a3eb81b31f0443dd56cba94ea9199c1a079e376ae0d62083a)
            check_type(argname="argument admin_role_arn", value=admin_role_arn, expected_type=type_hints["admin_role_arn"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument studio_encryption_configuration", value=studio_encryption_configuration, expected_type=type_hints["studio_encryption_configuration"])
            check_type(argname="argument studio_name", value=studio_name, expected_type=type_hints["studio_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_role_arn", value=user_role_arn, expected_type=type_hints["user_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admin_role_arn is not None:
            self._values["admin_role_arn"] = admin_role_arn
        if display_name is not None:
            self._values["display_name"] = display_name
        if studio_encryption_configuration is not None:
            self._values["studio_encryption_configuration"] = studio_encryption_configuration
        if studio_name is not None:
            self._values["studio_name"] = studio_name
        if tags is not None:
            self._values["tags"] = tags
        if user_role_arn is not None:
            self._values["user_role_arn"] = user_role_arn

    @builtins.property
    def admin_role_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-adminrolearn
        '''
        result = self._values.get("admin_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def studio_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioPropsMixin.StudioEncryptionConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-studioencryptionconfiguration
        '''
        result = self._values.get("studio_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStudioPropsMixin.StudioEncryptionConfigurationProperty"]], result)

    @builtins.property
    def studio_name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-studioname
        '''
        result = self._values.get("studio_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def user_role_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-userrolearn
        '''
        result = self._values.get("user_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStudioMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStudioPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioPropsMixin",
):
    '''http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html
    :cloudformationResource: AWS::NimbleStudio::Studio
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
        
        cfn_studio_props_mixin = nimblestudio_mixins.CfnStudioPropsMixin(nimblestudio_mixins.CfnStudioMixinProps(
            admin_role_arn="adminRoleArn",
            display_name="displayName",
            studio_encryption_configuration=nimblestudio_mixins.CfnStudioPropsMixin.StudioEncryptionConfigurationProperty(
                key_arn="keyArn",
                key_type="keyType"
            ),
            studio_name="studioName",
            tags={
                "tags_key": "tags"
            },
            user_role_arn="userRoleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStudioMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NimbleStudio::Studio``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa18e4ea3b678d88c10976820a4c1221b66c83de009dc8e971514c34f9541f19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47c6b23b1bcbb226e85c37a22ddd0efd34772a111041a0f7a3f3b8847c473aec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__595fc242f21ff8842d876755218ed51cbdd478afdf22e12efe2ece043625c0d1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStudioMixinProps:
        return typing.cast(CfnStudioMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_nimblestudio.mixins.CfnStudioPropsMixin.StudioEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"key_arn": "keyArn", "key_type": "keyType"},
    )
    class StudioEncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            key_arn: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key_arn: 
            :param key_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studio-studioencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_nimblestudio import mixins as nimblestudio_mixins
                
                studio_encryption_configuration_property = nimblestudio_mixins.CfnStudioPropsMixin.StudioEncryptionConfigurationProperty(
                    key_arn="keyArn",
                    key_type="keyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb2c71d4408d07a458a391967e9318a856225fae745c34e9715a7fa06f251a26)
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_arn is not None:
                self._values["key_arn"] = key_arn
            if key_type is not None:
                self._values["key_type"] = key_type

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studio-studioencryptionconfiguration.html#cfn-nimblestudio-studio-studioencryptionconfiguration-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studio-studioencryptionconfiguration.html#cfn-nimblestudio-studio-studioencryptionconfiguration-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StudioEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnLaunchProfileMixinProps",
    "CfnLaunchProfilePropsMixin",
    "CfnStreamingImageMixinProps",
    "CfnStreamingImagePropsMixin",
    "CfnStudioComponentMixinProps",
    "CfnStudioComponentPropsMixin",
    "CfnStudioMixinProps",
    "CfnStudioPropsMixin",
]

publication.publish()

def _typecheckingstub__a8fdf768b5988a2c0edae90978df052e2a4dff30cf84f5a4e825eb0b129e425f(
    *,
    description: typing.Optional[builtins.str] = None,
    ec2_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_profile_protocol_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    stream_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchProfilePropsMixin.StreamConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    studio_component_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    studio_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53487321a1a17d63c0b3fe0dbc72329d5c78231bb68062b87949d73a3b57a4da(
    props: typing.Union[CfnLaunchProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab25b2992af2b2c8171224f3eaa10ab3f402090570dff6bb773a54f3279c6ad(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5b6cd380a49d85aac8b3d317c503b52e7de72943091aa0f31cee695577feb1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66159604e1e0b15e9c7e72e5802c1a16b1cc5094927fc43a792d1fdafbb6ccf0(
    *,
    automatic_termination_mode: typing.Optional[builtins.str] = None,
    clipboard_mode: typing.Optional[builtins.str] = None,
    ec2_instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_session_length_in_minutes: typing.Optional[jsii.Number] = None,
    max_stopped_session_length_in_minutes: typing.Optional[jsii.Number] = None,
    session_backup: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchProfilePropsMixin.StreamConfigurationSessionBackupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    session_persistence_mode: typing.Optional[builtins.str] = None,
    session_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchProfilePropsMixin.StreamConfigurationSessionStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    streaming_image_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchProfilePropsMixin.VolumeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1e3ab63a3d70755319091359067d6783250a676e931b224d4966ef413623f9(
    *,
    max_backups_to_retain: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e0323aae0f131ec6784686195eed10edd33d50a5e71e94acb32f2e26207f15(
    *,
    mode: typing.Optional[typing.Sequence[builtins.str]] = None,
    root: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLaunchProfilePropsMixin.StreamingSessionStorageRootProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57930f4ee97bc45870ca43b36f15bd3eab4907b8dedda0f57641a2e23baaabb(
    *,
    linux: typing.Optional[builtins.str] = None,
    windows: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f0da5f3082c61e141d5c2e171749c4fd80f1c7d463dec58469e3b4f7f61ce9(
    *,
    iops: typing.Optional[jsii.Number] = None,
    size: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e915832123172290b0e76ff06af51b7c4d10b1299389be1c12b13233a0e8c8fb(
    *,
    description: typing.Optional[builtins.str] = None,
    ec2_image_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    studio_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd90898e892273ed86ad5be4eb1e6c9e7389730aa8c440fe20922088753ed64(
    props: typing.Union[CfnStreamingImageMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd14fbcfe2a78815f4ae91cfe3ea6a9dc2015e94b3dd2009aeb9a2eebc316f9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a1dfe9910095ed15062c27e90e0e19ccabbd57ea8329cf15908724dcc01a9d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9de0c9133c610837b3775afea8c06260c1064733da596a77a0795bc10b829a(
    *,
    key_arn: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba1372431139e4349e6afa90bcc496f4af395a9964d28013840c1b1d1e7bc1c(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStudioComponentPropsMixin.StudioComponentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    ec2_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    initialization_scripts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStudioComponentPropsMixin.StudioComponentInitializationScriptProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    script_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStudioComponentPropsMixin.ScriptParameterKeyValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    studio_id: typing.Optional[builtins.str] = None,
    subtype: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5e657cb2b187a278e22fdbc14ce3acd34d3f57149a2c549c22229df3561c0b(
    props: typing.Union[CfnStudioComponentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceead7746d29597976794d74d2369e6d449fe8bd6d11de32e32c5afd13ac01b2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a60586b0a3706693b3e48b4e804d82506434e7a8f0a855b0352af5f6f2da1bc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79151c931926cd170b5d11382406e6a5d7c35ebaa64abcf61c3bf46c9e969ff0(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c253d6b457a24f6308f37c37f70d09f6d78f1ea1950255ca4f5d835b80bff5b9(
    *,
    computer_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStudioComponentPropsMixin.ActiveDirectoryComputerAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    directory_id: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5019473acc5871b458c9e96e319215fdb93a909f43217d55d45ea9fd097c5d0(
    *,
    active_directory_user: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf57f92c7d04b16f6f39c29a2f4e50a911e7e15e685e984157c7a862cb46efa3(
    *,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92da1cc94580b0bf36833dcb28c3fb4dd2a097caf3515fd5c653e39a20779986(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71e54923ae97e78351b07afc3558a4a3c364c9002f039a379a1840b400d80df(
    *,
    endpoint: typing.Optional[builtins.str] = None,
    file_system_id: typing.Optional[builtins.str] = None,
    linux_mount_point: typing.Optional[builtins.str] = None,
    share_name: typing.Optional[builtins.str] = None,
    windows_mount_drive: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bbe1df3863411ecfcde2056db84159a71e00c67b1707cdf7ec78fdc409166c(
    *,
    active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStudioComponentPropsMixin.ActiveDirectoryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    compute_farm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStudioComponentPropsMixin.ComputeFarmConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    license_service_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStudioComponentPropsMixin.LicenseServiceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    shared_file_system_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStudioComponentPropsMixin.SharedFileSystemConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7efe74291570df153e977df3f4e3685e24367744d59d003f432aba58682fa307(
    *,
    launch_profile_protocol_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    run_context: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ed7b1dc5b6fa3a3eb81b31f0443dd56cba94ea9199c1a079e376ae0d62083a(
    *,
    admin_role_arn: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    studio_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStudioPropsMixin.StudioEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    studio_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa18e4ea3b678d88c10976820a4c1221b66c83de009dc8e971514c34f9541f19(
    props: typing.Union[CfnStudioMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c6b23b1bcbb226e85c37a22ddd0efd34772a111041a0f7a3f3b8847c473aec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595fc242f21ff8842d876755218ed51cbdd478afdf22e12efe2ece043625c0d1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2c71d4408d07a458a391967e9318a856225fae745c34e9715a7fa06f251a26(
    *,
    key_arn: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
