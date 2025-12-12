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
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnVolumeAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "device": "device",
        "disassociate_mode": "disassociateMode",
        "volume_id": "volumeId",
        "workspace_instance_id": "workspaceInstanceId",
    },
)
class CfnVolumeAssociationMixinProps:
    def __init__(
        self,
        *,
        device: typing.Optional[builtins.str] = None,
        disassociate_mode: typing.Optional[builtins.str] = None,
        volume_id: typing.Optional[builtins.str] = None,
        workspace_instance_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVolumeAssociationPropsMixin.

        :param device: The device name for the volume attachment.
        :param disassociate_mode: Mode to use when disassociating the volume.
        :param volume_id: ID of the volume to attach to the workspace instance.
        :param workspace_instance_id: ID of the workspace instance to associate with the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volumeassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
            
            cfn_volume_association_mixin_props = workspacesinstances_mixins.CfnVolumeAssociationMixinProps(
                device="device",
                disassociate_mode="disassociateMode",
                volume_id="volumeId",
                workspace_instance_id="workspaceInstanceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f979d28fb8b4d1fe0cb2c60e9a385add3062ad9803f384b71ebcfc7acc8d2c7b)
            check_type(argname="argument device", value=device, expected_type=type_hints["device"])
            check_type(argname="argument disassociate_mode", value=disassociate_mode, expected_type=type_hints["disassociate_mode"])
            check_type(argname="argument volume_id", value=volume_id, expected_type=type_hints["volume_id"])
            check_type(argname="argument workspace_instance_id", value=workspace_instance_id, expected_type=type_hints["workspace_instance_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device is not None:
            self._values["device"] = device
        if disassociate_mode is not None:
            self._values["disassociate_mode"] = disassociate_mode
        if volume_id is not None:
            self._values["volume_id"] = volume_id
        if workspace_instance_id is not None:
            self._values["workspace_instance_id"] = workspace_instance_id

    @builtins.property
    def device(self) -> typing.Optional[builtins.str]:
        '''The device name for the volume attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volumeassociation.html#cfn-workspacesinstances-volumeassociation-device
        '''
        result = self._values.get("device")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disassociate_mode(self) -> typing.Optional[builtins.str]:
        '''Mode to use when disassociating the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volumeassociation.html#cfn-workspacesinstances-volumeassociation-disassociatemode
        '''
        result = self._values.get("disassociate_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume_id(self) -> typing.Optional[builtins.str]:
        '''ID of the volume to attach to the workspace instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volumeassociation.html#cfn-workspacesinstances-volumeassociation-volumeid
        '''
        result = self._values.get("volume_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_instance_id(self) -> typing.Optional[builtins.str]:
        '''ID of the workspace instance to associate with the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volumeassociation.html#cfn-workspacesinstances-volumeassociation-workspaceinstanceid
        '''
        result = self._values.get("workspace_instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVolumeAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVolumeAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnVolumeAssociationPropsMixin",
):
    '''Resource Type definition for AWS::WorkspacesInstances::VolumeAssociation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volumeassociation.html
    :cloudformationResource: AWS::WorkspacesInstances::VolumeAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
        
        cfn_volume_association_props_mixin = workspacesinstances_mixins.CfnVolumeAssociationPropsMixin(workspacesinstances_mixins.CfnVolumeAssociationMixinProps(
            device="device",
            disassociate_mode="disassociateMode",
            volume_id="volumeId",
            workspace_instance_id="workspaceInstanceId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVolumeAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkspacesInstances::VolumeAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e33def94ee64b58a414963c8dec56fec498fb68f05b91bd43cb8c185c5e475e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26ae7f96874ef76458876d5bcff00e9a7f651a1698a3dea3e71519e87f1d2cda)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf1bbcab3a2d9915102c98a6d6b54a460b8e459a5c7fa4d60fade01bfd22098)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVolumeAssociationMixinProps:
        return typing.cast(CfnVolumeAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnVolumeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "encrypted": "encrypted",
        "iops": "iops",
        "kms_key_id": "kmsKeyId",
        "size_in_gb": "sizeInGb",
        "snapshot_id": "snapshotId",
        "tag_specifications": "tagSpecifications",
        "throughput": "throughput",
        "volume_type": "volumeType",
    },
)
class CfnVolumeMixinProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        size_in_gb: typing.Optional[jsii.Number] = None,
        snapshot_id: typing.Optional[builtins.str] = None,
        tag_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.TagSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVolumePropsMixin.

        :param availability_zone: The Availability Zone in which to create the volume.
        :param encrypted: Indicates whether the volume should be encrypted.
        :param iops: The number of I/O operations per second (IOPS).
        :param kms_key_id: The identifier of the AWS Key Management Service (AWS KMS) customer master key (CMK) to use for Amazon EBS encryption.
        :param size_in_gb: The size of the volume, in GiBs.
        :param snapshot_id: The snapshot from which to create the volume.
        :param tag_specifications: The tags passed to EBS volume.
        :param throughput: The throughput to provision for a volume, with a maximum of 1,000 MiB/s.
        :param volume_type: The volume type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
            
            cfn_volume_mixin_props = workspacesinstances_mixins.CfnVolumeMixinProps(
                availability_zone="availabilityZone",
                encrypted=False,
                iops=123,
                kms_key_id="kmsKeyId",
                size_in_gb=123,
                snapshot_id="snapshotId",
                tag_specifications=[workspacesinstances_mixins.CfnVolumePropsMixin.TagSpecificationProperty(
                    resource_type="resourceType",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                throughput=123,
                volume_type="volumeType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61dd9762848a093660e288711ac534e0a5ba4817cbae17a3aab73f18e63517e2)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument size_in_gb", value=size_in_gb, expected_type=type_hints["size_in_gb"])
            check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
            check_type(argname="argument tag_specifications", value=tag_specifications, expected_type=type_hints["tag_specifications"])
            check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if iops is not None:
            self._values["iops"] = iops
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if size_in_gb is not None:
            self._values["size_in_gb"] = size_in_gb
        if snapshot_id is not None:
            self._values["snapshot_id"] = snapshot_id
        if tag_specifications is not None:
            self._values["tag_specifications"] = tag_specifications
        if throughput is not None:
            self._values["throughput"] = throughput
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone in which to create the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html#cfn-workspacesinstances-volume-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the volume should be encrypted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html#cfn-workspacesinstances-volume-encrypted
        '''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''The number of I/O operations per second (IOPS).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html#cfn-workspacesinstances-volume-iops
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AWS Key Management Service (AWS KMS) customer master key (CMK) to use for Amazon EBS encryption.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html#cfn-workspacesinstances-volume-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_in_gb(self) -> typing.Optional[jsii.Number]:
        '''The size of the volume, in GiBs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html#cfn-workspacesinstances-volume-sizeingb
        '''
        result = self._values.get("size_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot_id(self) -> typing.Optional[builtins.str]:
        '''The snapshot from which to create the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html#cfn-workspacesinstances-volume-snapshotid
        '''
        result = self._values.get("snapshot_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_specifications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.TagSpecificationProperty"]]]]:
        '''The tags passed to EBS volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html#cfn-workspacesinstances-volume-tagspecifications
        '''
        result = self._values.get("tag_specifications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.TagSpecificationProperty"]]]], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''The throughput to provision for a volume, with a maximum of 1,000 MiB/s.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html#cfn-workspacesinstances-volume-throughput
        '''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''The volume type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html#cfn-workspacesinstances-volume-volumetype
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVolumeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVolumePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnVolumePropsMixin",
):
    '''Resource Type definition for AWS::WorkspacesInstances::Volume - Manages WorkSpaces Volume resources.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-volume.html
    :cloudformationResource: AWS::WorkspacesInstances::Volume
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
        
        cfn_volume_props_mixin = workspacesinstances_mixins.CfnVolumePropsMixin(workspacesinstances_mixins.CfnVolumeMixinProps(
            availability_zone="availabilityZone",
            encrypted=False,
            iops=123,
            kms_key_id="kmsKeyId",
            size_in_gb=123,
            snapshot_id="snapshotId",
            tag_specifications=[workspacesinstances_mixins.CfnVolumePropsMixin.TagSpecificationProperty(
                resource_type="resourceType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )],
            throughput=123,
            volume_type="volumeType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVolumeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkspacesInstances::Volume``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9996df0155c8ecf3cc53358442c19a1513bc1174e36b3e58f384c8b3d740f99d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f55a7d9ab49276d4ee085dcd015455a2cfce94b090a90f58483fc1e841951531)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ffd83f6929f849977a80f19bf16d2ab31f8dffc85f848ba1a1b71b56772ee9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVolumeMixinProps:
        return typing.cast(CfnVolumeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnVolumePropsMixin.TagSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_type": "resourceType", "tags": "tags"},
    )
    class TagSpecificationProperty:
        def __init__(
            self,
            *,
            resource_type: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param resource_type: 
            :param tags: The tags to apply to the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-volume-tagspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                tag_specification_property = workspacesinstances_mixins.CfnVolumePropsMixin.TagSpecificationProperty(
                    resource_type="resourceType",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e94a068c9d41d798dd8aa1a87867f9f6d2b5a9701740e3b366c380f833fc992b)
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_type is not None:
                self._values["resource_type"] = resource_type
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-volume-tagspecification.html#cfn-workspacesinstances-volume-tagspecification-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The tags to apply to the resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-volume-tagspecification.html#cfn-workspacesinstances-volume-tagspecification-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={"managed_instance": "managedInstance", "tags": "tags"},
)
class CfnWorkspaceInstanceMixinProps:
    def __init__(
        self,
        *,
        managed_instance: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.ManagedInstanceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWorkspaceInstancePropsMixin.

        :param managed_instance: 
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-workspaceinstance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
            
            cfn_workspace_instance_mixin_props = workspacesinstances_mixins.CfnWorkspaceInstanceMixinProps(
                managed_instance=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.ManagedInstanceProperty(
                    block_device_mappings=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.BlockDeviceMappingProperty(
                        device_name="deviceName",
                        ebs=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty(
                            encrypted=False,
                            iops=123,
                            kms_key_id="kmsKeyId",
                            throughput=123,
                            volume_size=123,
                            volume_type="volumeType"
                        ),
                        no_device="noDevice",
                        virtual_name="virtualName"
                    )],
                    capacity_reservation_specification=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationSpecificationProperty(
                        capacity_reservation_preference="capacityReservationPreference",
                        capacity_reservation_target=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty(
                            capacity_reservation_id="capacityReservationId",
                            capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn"
                        )
                    ),
                    cpu_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CpuOptionsRequestProperty(
                        core_count=123,
                        threads_per_core=123
                    ),
                    credit_specification=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CreditSpecificationRequestProperty(
                        cpu_credits="cpuCredits"
                    ),
                    disable_api_stop=False,
                    ebs_optimized=False,
                    enable_primary_ipv6=False,
                    enclave_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EnclaveOptionsRequestProperty(
                        enabled=False
                    ),
                    hibernation_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.HibernationOptionsRequestProperty(
                        configured=False
                    ),
                    iam_instance_profile=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.IamInstanceProfileSpecificationProperty(
                        arn="arn",
                        name="name"
                    ),
                    image_id="imageId",
                    instance_market_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMarketOptionsRequestProperty(
                        market_type="marketType",
                        spot_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty(
                            instance_interruption_behavior="instanceInterruptionBehavior",
                            max_price="maxPrice",
                            spot_instance_type="spotInstanceType",
                            valid_until_utc="validUntilUtc"
                        )
                    ),
                    instance_type="instanceType",
                    ipv6_address_count=123,
                    key_name="keyName",
                    license_specifications=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.LicenseConfigurationRequestProperty(
                        license_configuration_arn="licenseConfigurationArn"
                    )],
                    maintenance_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMaintenanceOptionsRequestProperty(
                        auto_recovery="autoRecovery"
                    ),
                    metadata_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMetadataOptionsRequestProperty(
                        http_endpoint="httpEndpoint",
                        http_protocol_ipv6="httpProtocolIpv6",
                        http_put_response_hop_limit=123,
                        http_tokens="httpTokens",
                        instance_metadata_tags="instanceMetadataTags"
                    ),
                    monitoring=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.RunInstancesMonitoringEnabledProperty(
                        enabled=False
                    ),
                    network_interfaces=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkInterfaceSpecificationProperty(
                        description="description",
                        device_index=123,
                        groups=["groups"],
                        subnet_id="subnetId"
                    )],
                    network_performance_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkPerformanceOptionsRequestProperty(
                        bandwidth_weighting="bandwidthWeighting"
                    ),
                    placement=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.PlacementProperty(
                        availability_zone="availabilityZone",
                        group_id="groupId",
                        group_name="groupName",
                        partition_number=123,
                        tenancy="tenancy"
                    ),
                    private_dns_name_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.PrivateDnsNameOptionsRequestProperty(
                        enable_resource_name_dns_aaaa_record=False,
                        enable_resource_name_dns_aRecord=False,
                        hostname_type="hostnameType"
                    ),
                    subnet_id="subnetId",
                    tag_specifications=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.TagSpecificationProperty(
                        resource_type="resourceType",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    user_data="userData"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc2815c47fd4b097149158a5a4b6d1f8cf76f17a7e8a69aba50f679c5e198e8)
            check_type(argname="argument managed_instance", value=managed_instance, expected_type=type_hints["managed_instance"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if managed_instance is not None:
            self._values["managed_instance"] = managed_instance
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def managed_instance(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.ManagedInstanceProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-workspaceinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance
        '''
        result = self._values.get("managed_instance")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.ManagedInstanceProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-workspaceinstance.html#cfn-workspacesinstances-workspaceinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkspaceInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin",
):
    '''Resource Type definition for AWS::WorkspacesInstances::WorkspaceInstance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-workspacesinstances-workspaceinstance.html
    :cloudformationResource: AWS::WorkspacesInstances::WorkspaceInstance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
        
        cfn_workspace_instance_props_mixin = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin(workspacesinstances_mixins.CfnWorkspaceInstanceMixinProps(
            managed_instance=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.ManagedInstanceProperty(
                block_device_mappings=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.BlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty(
                        encrypted=False,
                        iops=123,
                        kms_key_id="kmsKeyId",
                        throughput=123,
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device="noDevice",
                    virtual_name="virtualName"
                )],
                capacity_reservation_specification=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationSpecificationProperty(
                    capacity_reservation_preference="capacityReservationPreference",
                    capacity_reservation_target=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty(
                        capacity_reservation_id="capacityReservationId",
                        capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn"
                    )
                ),
                cpu_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CpuOptionsRequestProperty(
                    core_count=123,
                    threads_per_core=123
                ),
                credit_specification=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CreditSpecificationRequestProperty(
                    cpu_credits="cpuCredits"
                ),
                disable_api_stop=False,
                ebs_optimized=False,
                enable_primary_ipv6=False,
                enclave_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EnclaveOptionsRequestProperty(
                    enabled=False
                ),
                hibernation_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.HibernationOptionsRequestProperty(
                    configured=False
                ),
                iam_instance_profile=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.IamInstanceProfileSpecificationProperty(
                    arn="arn",
                    name="name"
                ),
                image_id="imageId",
                instance_market_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMarketOptionsRequestProperty(
                    market_type="marketType",
                    spot_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty(
                        instance_interruption_behavior="instanceInterruptionBehavior",
                        max_price="maxPrice",
                        spot_instance_type="spotInstanceType",
                        valid_until_utc="validUntilUtc"
                    )
                ),
                instance_type="instanceType",
                ipv6_address_count=123,
                key_name="keyName",
                license_specifications=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.LicenseConfigurationRequestProperty(
                    license_configuration_arn="licenseConfigurationArn"
                )],
                maintenance_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMaintenanceOptionsRequestProperty(
                    auto_recovery="autoRecovery"
                ),
                metadata_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMetadataOptionsRequestProperty(
                    http_endpoint="httpEndpoint",
                    http_protocol_ipv6="httpProtocolIpv6",
                    http_put_response_hop_limit=123,
                    http_tokens="httpTokens",
                    instance_metadata_tags="instanceMetadataTags"
                ),
                monitoring=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.RunInstancesMonitoringEnabledProperty(
                    enabled=False
                ),
                network_interfaces=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkInterfaceSpecificationProperty(
                    description="description",
                    device_index=123,
                    groups=["groups"],
                    subnet_id="subnetId"
                )],
                network_performance_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkPerformanceOptionsRequestProperty(
                    bandwidth_weighting="bandwidthWeighting"
                ),
                placement=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.PlacementProperty(
                    availability_zone="availabilityZone",
                    group_id="groupId",
                    group_name="groupName",
                    partition_number=123,
                    tenancy="tenancy"
                ),
                private_dns_name_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.PrivateDnsNameOptionsRequestProperty(
                    enable_resource_name_dns_aaaa_record=False,
                    enable_resource_name_dns_aRecord=False,
                    hostname_type="hostnameType"
                ),
                subnet_id="subnetId",
                tag_specifications=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.TagSpecificationProperty(
                    resource_type="resourceType",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                user_data="userData"
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
        props: typing.Union[CfnWorkspaceInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WorkspacesInstances::WorkspaceInstance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0b4108c54ee74fe608438414bac4a3ed4c298bdcda6b52d8d18f4e4366e5c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4d6e53dbb420652ed5b59498580ad8d1280c0c65edbd4ad9760b57dead5d835)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07bafa9340d192c502df273ae2aee955fa7eb19830655d023e7187cf19974dc7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkspaceInstanceMixinProps:
        return typing.cast(CfnWorkspaceInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.BlockDeviceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "device_name": "deviceName",
            "ebs": "ebs",
            "no_device": "noDevice",
            "virtual_name": "virtualName",
        },
    )
    class BlockDeviceMappingProperty:
        def __init__(
            self,
            *,
            device_name: typing.Optional[builtins.str] = None,
            ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            no_device: typing.Optional[builtins.str] = None,
            virtual_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param device_name: 
            :param ebs: 
            :param no_device: 
            :param virtual_name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-blockdevicemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                block_device_mapping_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.BlockDeviceMappingProperty(
                    device_name="deviceName",
                    ebs=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty(
                        encrypted=False,
                        iops=123,
                        kms_key_id="kmsKeyId",
                        throughput=123,
                        volume_size=123,
                        volume_type="volumeType"
                    ),
                    no_device="noDevice",
                    virtual_name="virtualName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ac96f27b7cfc2df0a3dc61271b46fc9f1fc690227b778beea443eaab557112b)
                check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
                check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
                check_type(argname="argument no_device", value=no_device, expected_type=type_hints["no_device"])
                check_type(argname="argument virtual_name", value=virtual_name, expected_type=type_hints["virtual_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if device_name is not None:
                self._values["device_name"] = device_name
            if ebs is not None:
                self._values["ebs"] = ebs
            if no_device is not None:
                self._values["no_device"] = no_device
            if virtual_name is not None:
                self._values["virtual_name"] = virtual_name

        @builtins.property
        def device_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-blockdevicemapping.html#cfn-workspacesinstances-workspaceinstance-blockdevicemapping-devicename
            '''
            result = self._values.get("device_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ebs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-blockdevicemapping.html#cfn-workspacesinstances-workspaceinstance-blockdevicemapping-ebs
            '''
            result = self._values.get("ebs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty"]], result)

        @builtins.property
        def no_device(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-blockdevicemapping.html#cfn-workspacesinstances-workspaceinstance-blockdevicemapping-nodevice
            '''
            result = self._values.get("no_device")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def virtual_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-blockdevicemapping.html#cfn-workspacesinstances-workspaceinstance-blockdevicemapping-virtualname
            '''
            result = self._values.get("virtual_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockDeviceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_reservation_preference": "capacityReservationPreference",
            "capacity_reservation_target": "capacityReservationTarget",
        },
    )
    class CapacityReservationSpecificationProperty:
        def __init__(
            self,
            *,
            capacity_reservation_preference: typing.Optional[builtins.str] = None,
            capacity_reservation_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param capacity_reservation_preference: 
            :param capacity_reservation_target: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-capacityreservationspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                capacity_reservation_specification_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationSpecificationProperty(
                    capacity_reservation_preference="capacityReservationPreference",
                    capacity_reservation_target=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty(
                        capacity_reservation_id="capacityReservationId",
                        capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f330706ed23bb89236fb2d977a905fe7e04dbf27f6e9820df20df40808600411)
                check_type(argname="argument capacity_reservation_preference", value=capacity_reservation_preference, expected_type=type_hints["capacity_reservation_preference"])
                check_type(argname="argument capacity_reservation_target", value=capacity_reservation_target, expected_type=type_hints["capacity_reservation_target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_reservation_preference is not None:
                self._values["capacity_reservation_preference"] = capacity_reservation_preference
            if capacity_reservation_target is not None:
                self._values["capacity_reservation_target"] = capacity_reservation_target

        @builtins.property
        def capacity_reservation_preference(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-capacityreservationspecification.html#cfn-workspacesinstances-workspaceinstance-capacityreservationspecification-capacityreservationpreference
            '''
            result = self._values.get("capacity_reservation_preference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capacity_reservation_target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-capacityreservationspecification.html#cfn-workspacesinstances-workspaceinstance-capacityreservationspecification-capacityreservationtarget
            '''
            result = self._values.get("capacity_reservation_target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityReservationSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_reservation_id": "capacityReservationId",
            "capacity_reservation_resource_group_arn": "capacityReservationResourceGroupArn",
        },
    )
    class CapacityReservationTargetProperty:
        def __init__(
            self,
            *,
            capacity_reservation_id: typing.Optional[builtins.str] = None,
            capacity_reservation_resource_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param capacity_reservation_id: 
            :param capacity_reservation_resource_group_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-capacityreservationtarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                capacity_reservation_target_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty(
                    capacity_reservation_id="capacityReservationId",
                    capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63b4536b56a519845d862cf01ed9ac8481a4b5138d1b66bfe0fe56fe13be3f20)
                check_type(argname="argument capacity_reservation_id", value=capacity_reservation_id, expected_type=type_hints["capacity_reservation_id"])
                check_type(argname="argument capacity_reservation_resource_group_arn", value=capacity_reservation_resource_group_arn, expected_type=type_hints["capacity_reservation_resource_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_reservation_id is not None:
                self._values["capacity_reservation_id"] = capacity_reservation_id
            if capacity_reservation_resource_group_arn is not None:
                self._values["capacity_reservation_resource_group_arn"] = capacity_reservation_resource_group_arn

        @builtins.property
        def capacity_reservation_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-capacityreservationtarget.html#cfn-workspacesinstances-workspaceinstance-capacityreservationtarget-capacityreservationid
            '''
            result = self._values.get("capacity_reservation_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capacity_reservation_resource_group_arn(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-capacityreservationtarget.html#cfn-workspacesinstances-workspaceinstance-capacityreservationtarget-capacityreservationresourcegrouparn
            '''
            result = self._values.get("capacity_reservation_resource_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityReservationTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.CpuOptionsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"core_count": "coreCount", "threads_per_core": "threadsPerCore"},
    )
    class CpuOptionsRequestProperty:
        def __init__(
            self,
            *,
            core_count: typing.Optional[jsii.Number] = None,
            threads_per_core: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param core_count: 
            :param threads_per_core: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-cpuoptionsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                cpu_options_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CpuOptionsRequestProperty(
                    core_count=123,
                    threads_per_core=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f357c3d4e744ca751e6a0e7233f03500fc45df0f949c226f1fd2b22add705f72)
                check_type(argname="argument core_count", value=core_count, expected_type=type_hints["core_count"])
                check_type(argname="argument threads_per_core", value=threads_per_core, expected_type=type_hints["threads_per_core"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if core_count is not None:
                self._values["core_count"] = core_count
            if threads_per_core is not None:
                self._values["threads_per_core"] = threads_per_core

        @builtins.property
        def core_count(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-cpuoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-cpuoptionsrequest-corecount
            '''
            result = self._values.get("core_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def threads_per_core(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-cpuoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-cpuoptionsrequest-threadspercore
            '''
            result = self._values.get("threads_per_core")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CpuOptionsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.CreditSpecificationRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu_credits": "cpuCredits"},
    )
    class CreditSpecificationRequestProperty:
        def __init__(
            self,
            *,
            cpu_credits: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param cpu_credits: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-creditspecificationrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                credit_specification_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CreditSpecificationRequestProperty(
                    cpu_credits="cpuCredits"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f8a3a572a1fb7c958aaf3a482a18bb4b830422732791cbe2ebdf4dac28fda27)
                check_type(argname="argument cpu_credits", value=cpu_credits, expected_type=type_hints["cpu_credits"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu_credits is not None:
                self._values["cpu_credits"] = cpu_credits

        @builtins.property
        def cpu_credits(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-creditspecificationrequest.html#cfn-workspacesinstances-workspaceinstance-creditspecificationrequest-cpucredits
            '''
            result = self._values.get("cpu_credits")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreditSpecificationRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.EC2ManagedInstanceProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_id": "instanceId"},
    )
    class EC2ManagedInstanceProperty:
        def __init__(
            self,
            *,
            instance_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param instance_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-ec2managedinstance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                e_c2_managed_instance_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EC2ManagedInstanceProperty(
                    instance_id="instanceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3420a80ad3f8412cb20ff01c8fd96bba01a14438eb26ce2b4c7398d4efaee41b)
                check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_id is not None:
                self._values["instance_id"] = instance_id

        @builtins.property
        def instance_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-ec2managedinstance.html#cfn-workspacesinstances-workspaceinstance-ec2managedinstance-instanceid
            '''
            result = self._values.get("instance_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2ManagedInstanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encrypted": "encrypted",
            "iops": "iops",
            "kms_key_id": "kmsKeyId",
            "throughput": "throughput",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EbsBlockDeviceProperty:
        def __init__(
            self,
            *,
            encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
            throughput: typing.Optional[jsii.Number] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param encrypted: 
            :param iops: 
            :param kms_key_id: 
            :param throughput: 
            :param volume_size: 
            :param volume_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-ebsblockdevice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                ebs_block_device_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty(
                    encrypted=False,
                    iops=123,
                    kms_key_id="kmsKeyId",
                    throughput=123,
                    volume_size=123,
                    volume_type="volumeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__531ee82d9003c8c02eee69321de3529af6937d63427be5c39fe213bc434852e8)
                check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
                check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
                check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encrypted is not None:
                self._values["encrypted"] = encrypted
            if iops is not None:
                self._values["iops"] = iops
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if throughput is not None:
                self._values["throughput"] = throughput
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-ebsblockdevice.html#cfn-workspacesinstances-workspaceinstance-ebsblockdevice-encrypted
            '''
            result = self._values.get("encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-ebsblockdevice.html#cfn-workspacesinstances-workspaceinstance-ebsblockdevice-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-ebsblockdevice.html#cfn-workspacesinstances-workspaceinstance-ebsblockdevice-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-ebsblockdevice.html#cfn-workspacesinstances-workspaceinstance-ebsblockdevice-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-ebsblockdevice.html#cfn-workspacesinstances-workspaceinstance-ebsblockdevice-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-ebsblockdevice.html#cfn-workspacesinstances-workspaceinstance-ebsblockdevice-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsBlockDeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.EnclaveOptionsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class EnclaveOptionsRequestProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param enabled: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-enclaveoptionsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                enclave_options_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EnclaveOptionsRequestProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a2e9e13a0b1fe6c85b7adb4e30c2955f3b2248d980c0c2b91e7507357621d05)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-enclaveoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-enclaveoptionsrequest-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnclaveOptionsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.HibernationOptionsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"configured": "configured"},
    )
    class HibernationOptionsRequestProperty:
        def __init__(
            self,
            *,
            configured: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param configured: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-hibernationoptionsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                hibernation_options_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.HibernationOptionsRequestProperty(
                    configured=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__428e8ea41a407d7bf18513d2e1e6d547f2a986f45b636acece504967e30971d7)
                check_type(argname="argument configured", value=configured, expected_type=type_hints["configured"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configured is not None:
                self._values["configured"] = configured

        @builtins.property
        def configured(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-hibernationoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-hibernationoptionsrequest-configured
            '''
            result = self._values.get("configured")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HibernationOptionsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.IamInstanceProfileSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "name": "name"},
    )
    class IamInstanceProfileSpecificationProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param arn: 
            :param name: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-iaminstanceprofilespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                iam_instance_profile_specification_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.IamInstanceProfileSpecificationProperty(
                    arn="arn",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__520d1945f11566dbe2e7922e00f4b826a41c7ed457b209e2dffcabeb3f4cc6b0)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-iaminstanceprofilespecification.html#cfn-workspacesinstances-workspaceinstance-iaminstanceprofilespecification-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-iaminstanceprofilespecification.html#cfn-workspacesinstances-workspaceinstance-iaminstanceprofilespecification-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamInstanceProfileSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.InstanceMaintenanceOptionsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"auto_recovery": "autoRecovery"},
    )
    class InstanceMaintenanceOptionsRequestProperty:
        def __init__(
            self,
            *,
            auto_recovery: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param auto_recovery: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemaintenanceoptionsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                instance_maintenance_options_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMaintenanceOptionsRequestProperty(
                    auto_recovery="autoRecovery"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5bf6cd28b0d867a3a18d78070751bb9d7f6bb54168201ae8c3f2214cd6d2ae2b)
                check_type(argname="argument auto_recovery", value=auto_recovery, expected_type=type_hints["auto_recovery"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_recovery is not None:
                self._values["auto_recovery"] = auto_recovery

        @builtins.property
        def auto_recovery(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemaintenanceoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-instancemaintenanceoptionsrequest-autorecovery
            '''
            result = self._values.get("auto_recovery")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceMaintenanceOptionsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.InstanceMarketOptionsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"market_type": "marketType", "spot_options": "spotOptions"},
    )
    class InstanceMarketOptionsRequestProperty:
        def __init__(
            self,
            *,
            market_type: typing.Optional[builtins.str] = None,
            spot_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param market_type: 
            :param spot_options: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemarketoptionsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                instance_market_options_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMarketOptionsRequestProperty(
                    market_type="marketType",
                    spot_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty(
                        instance_interruption_behavior="instanceInterruptionBehavior",
                        max_price="maxPrice",
                        spot_instance_type="spotInstanceType",
                        valid_until_utc="validUntilUtc"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ec9611eb4ce7118d9ac0336bd8cbd62d9a2ca6192a36f405fcfb28f756f27fe)
                check_type(argname="argument market_type", value=market_type, expected_type=type_hints["market_type"])
                check_type(argname="argument spot_options", value=spot_options, expected_type=type_hints["spot_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if market_type is not None:
                self._values["market_type"] = market_type
            if spot_options is not None:
                self._values["spot_options"] = spot_options

        @builtins.property
        def market_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemarketoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-instancemarketoptionsrequest-markettype
            '''
            result = self._values.get("market_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def spot_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemarketoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-instancemarketoptionsrequest-spotoptions
            '''
            result = self._values.get("spot_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceMarketOptionsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.InstanceMetadataOptionsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "http_endpoint": "httpEndpoint",
            "http_protocol_ipv6": "httpProtocolIpv6",
            "http_put_response_hop_limit": "httpPutResponseHopLimit",
            "http_tokens": "httpTokens",
            "instance_metadata_tags": "instanceMetadataTags",
        },
    )
    class InstanceMetadataOptionsRequestProperty:
        def __init__(
            self,
            *,
            http_endpoint: typing.Optional[builtins.str] = None,
            http_protocol_ipv6: typing.Optional[builtins.str] = None,
            http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
            http_tokens: typing.Optional[builtins.str] = None,
            instance_metadata_tags: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param http_endpoint: 
            :param http_protocol_ipv6: 
            :param http_put_response_hop_limit: 
            :param http_tokens: 
            :param instance_metadata_tags: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                instance_metadata_options_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMetadataOptionsRequestProperty(
                    http_endpoint="httpEndpoint",
                    http_protocol_ipv6="httpProtocolIpv6",
                    http_put_response_hop_limit=123,
                    http_tokens="httpTokens",
                    instance_metadata_tags="instanceMetadataTags"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9741a29072902432aa59f5a07a038ae58c282dbb9c7c6e5f02a61e0d59127c9a)
                check_type(argname="argument http_endpoint", value=http_endpoint, expected_type=type_hints["http_endpoint"])
                check_type(argname="argument http_protocol_ipv6", value=http_protocol_ipv6, expected_type=type_hints["http_protocol_ipv6"])
                check_type(argname="argument http_put_response_hop_limit", value=http_put_response_hop_limit, expected_type=type_hints["http_put_response_hop_limit"])
                check_type(argname="argument http_tokens", value=http_tokens, expected_type=type_hints["http_tokens"])
                check_type(argname="argument instance_metadata_tags", value=instance_metadata_tags, expected_type=type_hints["instance_metadata_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http_endpoint is not None:
                self._values["http_endpoint"] = http_endpoint
            if http_protocol_ipv6 is not None:
                self._values["http_protocol_ipv6"] = http_protocol_ipv6
            if http_put_response_hop_limit is not None:
                self._values["http_put_response_hop_limit"] = http_put_response_hop_limit
            if http_tokens is not None:
                self._values["http_tokens"] = http_tokens
            if instance_metadata_tags is not None:
                self._values["instance_metadata_tags"] = instance_metadata_tags

        @builtins.property
        def http_endpoint(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest-httpendpoint
            '''
            result = self._values.get("http_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_protocol_ipv6(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest-httpprotocolipv6
            '''
            result = self._values.get("http_protocol_ipv6")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_put_response_hop_limit(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest-httpputresponsehoplimit
            '''
            result = self._values.get("http_put_response_hop_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def http_tokens(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest-httptokens
            '''
            result = self._values.get("http_tokens")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_metadata_tags(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-instancemetadataoptionsrequest-instancemetadatatags
            '''
            result = self._values.get("instance_metadata_tags")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceMetadataOptionsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkInterfaceSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "device_index": "deviceIndex",
            "groups": "groups",
            "subnet_id": "subnetId",
        },
    )
    class InstanceNetworkInterfaceSpecificationProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            device_index: typing.Optional[jsii.Number] = None,
            groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param description: 
            :param device_index: 
            :param groups: 
            :param subnet_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancenetworkinterfacespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                instance_network_interface_specification_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkInterfaceSpecificationProperty(
                    description="description",
                    device_index=123,
                    groups=["groups"],
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cfcf0d5aa490d29539143d56dfa8a5a38a3714241770cede20cabbc740d2198)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument device_index", value=device_index, expected_type=type_hints["device_index"])
                check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if device_index is not None:
                self._values["device_index"] = device_index
            if groups is not None:
                self._values["groups"] = groups
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancenetworkinterfacespecification.html#cfn-workspacesinstances-workspaceinstance-instancenetworkinterfacespecification-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_index(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancenetworkinterfacespecification.html#cfn-workspacesinstances-workspaceinstance-instancenetworkinterfacespecification-deviceindex
            '''
            result = self._values.get("device_index")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancenetworkinterfacespecification.html#cfn-workspacesinstances-workspaceinstance-instancenetworkinterfacespecification-groups
            '''
            result = self._values.get("groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancenetworkinterfacespecification.html#cfn-workspacesinstances-workspaceinstance-instancenetworkinterfacespecification-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceNetworkInterfaceSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkPerformanceOptionsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"bandwidth_weighting": "bandwidthWeighting"},
    )
    class InstanceNetworkPerformanceOptionsRequestProperty:
        def __init__(
            self,
            *,
            bandwidth_weighting: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bandwidth_weighting: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancenetworkperformanceoptionsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                instance_network_performance_options_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkPerformanceOptionsRequestProperty(
                    bandwidth_weighting="bandwidthWeighting"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a218184e44b0c108cf1e6ed1911f61630ff3c51583f525198d20d7ef4fc42b16)
                check_type(argname="argument bandwidth_weighting", value=bandwidth_weighting, expected_type=type_hints["bandwidth_weighting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bandwidth_weighting is not None:
                self._values["bandwidth_weighting"] = bandwidth_weighting

        @builtins.property
        def bandwidth_weighting(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-instancenetworkperformanceoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-instancenetworkperformanceoptionsrequest-bandwidthweighting
            '''
            result = self._values.get("bandwidth_weighting")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceNetworkPerformanceOptionsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.LicenseConfigurationRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"license_configuration_arn": "licenseConfigurationArn"},
    )
    class LicenseConfigurationRequestProperty:
        def __init__(
            self,
            *,
            license_configuration_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param license_configuration_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-licenseconfigurationrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                license_configuration_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.LicenseConfigurationRequestProperty(
                    license_configuration_arn="licenseConfigurationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34721097bb4d5024991d9b06018a81cda36f7fd52e52d567785010a937d4ff38)
                check_type(argname="argument license_configuration_arn", value=license_configuration_arn, expected_type=type_hints["license_configuration_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if license_configuration_arn is not None:
                self._values["license_configuration_arn"] = license_configuration_arn

        @builtins.property
        def license_configuration_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-licenseconfigurationrequest.html#cfn-workspacesinstances-workspaceinstance-licenseconfigurationrequest-licenseconfigurationarn
            '''
            result = self._values.get("license_configuration_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LicenseConfigurationRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.ManagedInstanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_device_mappings": "blockDeviceMappings",
            "capacity_reservation_specification": "capacityReservationSpecification",
            "cpu_options": "cpuOptions",
            "credit_specification": "creditSpecification",
            "disable_api_stop": "disableApiStop",
            "ebs_optimized": "ebsOptimized",
            "enable_primary_ipv6": "enablePrimaryIpv6",
            "enclave_options": "enclaveOptions",
            "hibernation_options": "hibernationOptions",
            "iam_instance_profile": "iamInstanceProfile",
            "image_id": "imageId",
            "instance_market_options": "instanceMarketOptions",
            "instance_type": "instanceType",
            "ipv6_address_count": "ipv6AddressCount",
            "key_name": "keyName",
            "license_specifications": "licenseSpecifications",
            "maintenance_options": "maintenanceOptions",
            "metadata_options": "metadataOptions",
            "monitoring": "monitoring",
            "network_interfaces": "networkInterfaces",
            "network_performance_options": "networkPerformanceOptions",
            "placement": "placement",
            "private_dns_name_options": "privateDnsNameOptions",
            "subnet_id": "subnetId",
            "tag_specifications": "tagSpecifications",
            "user_data": "userData",
        },
    )
    class ManagedInstanceProperty:
        def __init__(
            self,
            *,
            block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.BlockDeviceMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            capacity_reservation_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.CapacityReservationSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            cpu_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.CpuOptionsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            credit_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.CreditSpecificationRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            disable_api_stop: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_primary_ipv6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enclave_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.EnclaveOptionsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hibernation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.HibernationOptionsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iam_instance_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.IamInstanceProfileSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            image_id: typing.Optional[builtins.str] = None,
            instance_market_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.InstanceMarketOptionsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_type: typing.Optional[builtins.str] = None,
            ipv6_address_count: typing.Optional[jsii.Number] = None,
            key_name: typing.Optional[builtins.str] = None,
            license_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.LicenseConfigurationRequestProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            maintenance_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.InstanceMaintenanceOptionsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metadata_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.InstanceMetadataOptionsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            monitoring: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.RunInstancesMonitoringEnabledProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            network_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.InstanceNetworkInterfaceSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_performance_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.InstanceNetworkPerformanceOptionsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            placement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.PlacementProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            private_dns_name_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.PrivateDnsNameOptionsRequestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            subnet_id: typing.Optional[builtins.str] = None,
            tag_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkspaceInstancePropsMixin.TagSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            user_data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param block_device_mappings: 
            :param capacity_reservation_specification: 
            :param cpu_options: 
            :param credit_specification: 
            :param disable_api_stop: 
            :param ebs_optimized: 
            :param enable_primary_ipv6: 
            :param enclave_options: 
            :param hibernation_options: 
            :param iam_instance_profile: 
            :param image_id: 
            :param instance_market_options: 
            :param instance_type: 
            :param ipv6_address_count: 
            :param key_name: 
            :param license_specifications: 
            :param maintenance_options: 
            :param metadata_options: 
            :param monitoring: 
            :param network_interfaces: 
            :param network_performance_options: 
            :param placement: 
            :param private_dns_name_options: 
            :param subnet_id: 
            :param tag_specifications: 
            :param user_data: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                managed_instance_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.ManagedInstanceProperty(
                    block_device_mappings=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.BlockDeviceMappingProperty(
                        device_name="deviceName",
                        ebs=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty(
                            encrypted=False,
                            iops=123,
                            kms_key_id="kmsKeyId",
                            throughput=123,
                            volume_size=123,
                            volume_type="volumeType"
                        ),
                        no_device="noDevice",
                        virtual_name="virtualName"
                    )],
                    capacity_reservation_specification=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationSpecificationProperty(
                        capacity_reservation_preference="capacityReservationPreference",
                        capacity_reservation_target=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty(
                            capacity_reservation_id="capacityReservationId",
                            capacity_reservation_resource_group_arn="capacityReservationResourceGroupArn"
                        )
                    ),
                    cpu_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CpuOptionsRequestProperty(
                        core_count=123,
                        threads_per_core=123
                    ),
                    credit_specification=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.CreditSpecificationRequestProperty(
                        cpu_credits="cpuCredits"
                    ),
                    disable_api_stop=False,
                    ebs_optimized=False,
                    enable_primary_ipv6=False,
                    enclave_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.EnclaveOptionsRequestProperty(
                        enabled=False
                    ),
                    hibernation_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.HibernationOptionsRequestProperty(
                        configured=False
                    ),
                    iam_instance_profile=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.IamInstanceProfileSpecificationProperty(
                        arn="arn",
                        name="name"
                    ),
                    image_id="imageId",
                    instance_market_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMarketOptionsRequestProperty(
                        market_type="marketType",
                        spot_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty(
                            instance_interruption_behavior="instanceInterruptionBehavior",
                            max_price="maxPrice",
                            spot_instance_type="spotInstanceType",
                            valid_until_utc="validUntilUtc"
                        )
                    ),
                    instance_type="instanceType",
                    ipv6_address_count=123,
                    key_name="keyName",
                    license_specifications=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.LicenseConfigurationRequestProperty(
                        license_configuration_arn="licenseConfigurationArn"
                    )],
                    maintenance_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMaintenanceOptionsRequestProperty(
                        auto_recovery="autoRecovery"
                    ),
                    metadata_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceMetadataOptionsRequestProperty(
                        http_endpoint="httpEndpoint",
                        http_protocol_ipv6="httpProtocolIpv6",
                        http_put_response_hop_limit=123,
                        http_tokens="httpTokens",
                        instance_metadata_tags="instanceMetadataTags"
                    ),
                    monitoring=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.RunInstancesMonitoringEnabledProperty(
                        enabled=False
                    ),
                    network_interfaces=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkInterfaceSpecificationProperty(
                        description="description",
                        device_index=123,
                        groups=["groups"],
                        subnet_id="subnetId"
                    )],
                    network_performance_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.InstanceNetworkPerformanceOptionsRequestProperty(
                        bandwidth_weighting="bandwidthWeighting"
                    ),
                    placement=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.PlacementProperty(
                        availability_zone="availabilityZone",
                        group_id="groupId",
                        group_name="groupName",
                        partition_number=123,
                        tenancy="tenancy"
                    ),
                    private_dns_name_options=workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.PrivateDnsNameOptionsRequestProperty(
                        enable_resource_name_dns_aaaa_record=False,
                        enable_resource_name_dns_aRecord=False,
                        hostname_type="hostnameType"
                    ),
                    subnet_id="subnetId",
                    tag_specifications=[workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.TagSpecificationProperty(
                        resource_type="resourceType",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    user_data="userData"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__638327636a9c0f60e6f4c5e9aa8a94bea77508dc4899f68910b5a4d105a02c4a)
                check_type(argname="argument block_device_mappings", value=block_device_mappings, expected_type=type_hints["block_device_mappings"])
                check_type(argname="argument capacity_reservation_specification", value=capacity_reservation_specification, expected_type=type_hints["capacity_reservation_specification"])
                check_type(argname="argument cpu_options", value=cpu_options, expected_type=type_hints["cpu_options"])
                check_type(argname="argument credit_specification", value=credit_specification, expected_type=type_hints["credit_specification"])
                check_type(argname="argument disable_api_stop", value=disable_api_stop, expected_type=type_hints["disable_api_stop"])
                check_type(argname="argument ebs_optimized", value=ebs_optimized, expected_type=type_hints["ebs_optimized"])
                check_type(argname="argument enable_primary_ipv6", value=enable_primary_ipv6, expected_type=type_hints["enable_primary_ipv6"])
                check_type(argname="argument enclave_options", value=enclave_options, expected_type=type_hints["enclave_options"])
                check_type(argname="argument hibernation_options", value=hibernation_options, expected_type=type_hints["hibernation_options"])
                check_type(argname="argument iam_instance_profile", value=iam_instance_profile, expected_type=type_hints["iam_instance_profile"])
                check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
                check_type(argname="argument instance_market_options", value=instance_market_options, expected_type=type_hints["instance_market_options"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument ipv6_address_count", value=ipv6_address_count, expected_type=type_hints["ipv6_address_count"])
                check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
                check_type(argname="argument license_specifications", value=license_specifications, expected_type=type_hints["license_specifications"])
                check_type(argname="argument maintenance_options", value=maintenance_options, expected_type=type_hints["maintenance_options"])
                check_type(argname="argument metadata_options", value=metadata_options, expected_type=type_hints["metadata_options"])
                check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
                check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
                check_type(argname="argument network_performance_options", value=network_performance_options, expected_type=type_hints["network_performance_options"])
                check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
                check_type(argname="argument private_dns_name_options", value=private_dns_name_options, expected_type=type_hints["private_dns_name_options"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                check_type(argname="argument tag_specifications", value=tag_specifications, expected_type=type_hints["tag_specifications"])
                check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block_device_mappings is not None:
                self._values["block_device_mappings"] = block_device_mappings
            if capacity_reservation_specification is not None:
                self._values["capacity_reservation_specification"] = capacity_reservation_specification
            if cpu_options is not None:
                self._values["cpu_options"] = cpu_options
            if credit_specification is not None:
                self._values["credit_specification"] = credit_specification
            if disable_api_stop is not None:
                self._values["disable_api_stop"] = disable_api_stop
            if ebs_optimized is not None:
                self._values["ebs_optimized"] = ebs_optimized
            if enable_primary_ipv6 is not None:
                self._values["enable_primary_ipv6"] = enable_primary_ipv6
            if enclave_options is not None:
                self._values["enclave_options"] = enclave_options
            if hibernation_options is not None:
                self._values["hibernation_options"] = hibernation_options
            if iam_instance_profile is not None:
                self._values["iam_instance_profile"] = iam_instance_profile
            if image_id is not None:
                self._values["image_id"] = image_id
            if instance_market_options is not None:
                self._values["instance_market_options"] = instance_market_options
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if ipv6_address_count is not None:
                self._values["ipv6_address_count"] = ipv6_address_count
            if key_name is not None:
                self._values["key_name"] = key_name
            if license_specifications is not None:
                self._values["license_specifications"] = license_specifications
            if maintenance_options is not None:
                self._values["maintenance_options"] = maintenance_options
            if metadata_options is not None:
                self._values["metadata_options"] = metadata_options
            if monitoring is not None:
                self._values["monitoring"] = monitoring
            if network_interfaces is not None:
                self._values["network_interfaces"] = network_interfaces
            if network_performance_options is not None:
                self._values["network_performance_options"] = network_performance_options
            if placement is not None:
                self._values["placement"] = placement
            if private_dns_name_options is not None:
                self._values["private_dns_name_options"] = private_dns_name_options
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id
            if tag_specifications is not None:
                self._values["tag_specifications"] = tag_specifications
            if user_data is not None:
                self._values["user_data"] = user_data

        @builtins.property
        def block_device_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.BlockDeviceMappingProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-blockdevicemappings
            '''
            result = self._values.get("block_device_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.BlockDeviceMappingProperty"]]]], result)

        @builtins.property
        def capacity_reservation_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.CapacityReservationSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-capacityreservationspecification
            '''
            result = self._values.get("capacity_reservation_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.CapacityReservationSpecificationProperty"]], result)

        @builtins.property
        def cpu_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.CpuOptionsRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-cpuoptions
            '''
            result = self._values.get("cpu_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.CpuOptionsRequestProperty"]], result)

        @builtins.property
        def credit_specification(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.CreditSpecificationRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-creditspecification
            '''
            result = self._values.get("credit_specification")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.CreditSpecificationRequestProperty"]], result)

        @builtins.property
        def disable_api_stop(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-disableapistop
            '''
            result = self._values.get("disable_api_stop")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ebs_optimized(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-ebsoptimized
            '''
            result = self._values.get("ebs_optimized")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_primary_ipv6(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-enableprimaryipv6
            '''
            result = self._values.get("enable_primary_ipv6")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enclave_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.EnclaveOptionsRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-enclaveoptions
            '''
            result = self._values.get("enclave_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.EnclaveOptionsRequestProperty"]], result)

        @builtins.property
        def hibernation_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.HibernationOptionsRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-hibernationoptions
            '''
            result = self._values.get("hibernation_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.HibernationOptionsRequestProperty"]], result)

        @builtins.property
        def iam_instance_profile(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.IamInstanceProfileSpecificationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-iaminstanceprofile
            '''
            result = self._values.get("iam_instance_profile")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.IamInstanceProfileSpecificationProperty"]], result)

        @builtins.property
        def image_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-imageid
            '''
            result = self._values.get("image_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_market_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceMarketOptionsRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-instancemarketoptions
            '''
            result = self._values.get("instance_market_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceMarketOptionsRequestProperty"]], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ipv6_address_count(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-ipv6addresscount
            '''
            result = self._values.get("ipv6_address_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def key_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-keyname
            '''
            result = self._values.get("key_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def license_specifications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.LicenseConfigurationRequestProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-licensespecifications
            '''
            result = self._values.get("license_specifications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.LicenseConfigurationRequestProperty"]]]], result)

        @builtins.property
        def maintenance_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceMaintenanceOptionsRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-maintenanceoptions
            '''
            result = self._values.get("maintenance_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceMaintenanceOptionsRequestProperty"]], result)

        @builtins.property
        def metadata_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceMetadataOptionsRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-metadataoptions
            '''
            result = self._values.get("metadata_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceMetadataOptionsRequestProperty"]], result)

        @builtins.property
        def monitoring(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.RunInstancesMonitoringEnabledProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-monitoring
            '''
            result = self._values.get("monitoring")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.RunInstancesMonitoringEnabledProperty"]], result)

        @builtins.property
        def network_interfaces(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceNetworkInterfaceSpecificationProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-networkinterfaces
            '''
            result = self._values.get("network_interfaces")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceNetworkInterfaceSpecificationProperty"]]]], result)

        @builtins.property
        def network_performance_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceNetworkPerformanceOptionsRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-networkperformanceoptions
            '''
            result = self._values.get("network_performance_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.InstanceNetworkPerformanceOptionsRequestProperty"]], result)

        @builtins.property
        def placement(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.PlacementProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-placement
            '''
            result = self._values.get("placement")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.PlacementProperty"]], result)

        @builtins.property
        def private_dns_name_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.PrivateDnsNameOptionsRequestProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-privatednsnameoptions
            '''
            result = self._values.get("private_dns_name_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.PrivateDnsNameOptionsRequestProperty"]], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_specifications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.TagSpecificationProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-tagspecifications
            '''
            result = self._values.get("tag_specifications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkspaceInstancePropsMixin.TagSpecificationProperty"]]]], result)

        @builtins.property
        def user_data(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-managedinstance.html#cfn-workspacesinstances-workspaceinstance-managedinstance-userdata
            '''
            result = self._values.get("user_data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedInstanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.PlacementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "group_id": "groupId",
            "group_name": "groupName",
            "partition_number": "partitionNumber",
            "tenancy": "tenancy",
        },
    )
    class PlacementProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            group_id: typing.Optional[builtins.str] = None,
            group_name: typing.Optional[builtins.str] = None,
            partition_number: typing.Optional[jsii.Number] = None,
            tenancy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param availability_zone: 
            :param group_id: 
            :param group_name: 
            :param partition_number: 
            :param tenancy: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-placement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                placement_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.PlacementProperty(
                    availability_zone="availabilityZone",
                    group_id="groupId",
                    group_name="groupName",
                    partition_number=123,
                    tenancy="tenancy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__05bba15c9fb32c00a955667e50e1bff93e840bb1faca1e4ccaafba170c88a48e)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
                check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
                check_type(argname="argument partition_number", value=partition_number, expected_type=type_hints["partition_number"])
                check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if group_id is not None:
                self._values["group_id"] = group_id
            if group_name is not None:
                self._values["group_name"] = group_name
            if partition_number is not None:
                self._values["partition_number"] = partition_number
            if tenancy is not None:
                self._values["tenancy"] = tenancy

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-placement.html#cfn-workspacesinstances-workspaceinstance-placement-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-placement.html#cfn-workspacesinstances-workspaceinstance-placement-groupid
            '''
            result = self._values.get("group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_name(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-placement.html#cfn-workspacesinstances-workspaceinstance-placement-groupname
            '''
            result = self._values.get("group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def partition_number(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-placement.html#cfn-workspacesinstances-workspaceinstance-placement-partitionnumber
            '''
            result = self._values.get("partition_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def tenancy(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-placement.html#cfn-workspacesinstances-workspaceinstance-placement-tenancy
            '''
            result = self._values.get("tenancy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.PrivateDnsNameOptionsRequestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_resource_name_dns_aaaa_record": "enableResourceNameDnsAaaaRecord",
            "enable_resource_name_dns_a_record": "enableResourceNameDnsARecord",
            "hostname_type": "hostnameType",
        },
    )
    class PrivateDnsNameOptionsRequestProperty:
        def __init__(
            self,
            *,
            enable_resource_name_dns_aaaa_record: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_resource_name_dns_a_record: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            hostname_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param enable_resource_name_dns_aaaa_record: 
            :param enable_resource_name_dns_a_record: 
            :param hostname_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-privatednsnameoptionsrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                private_dns_name_options_request_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.PrivateDnsNameOptionsRequestProperty(
                    enable_resource_name_dns_aaaa_record=False,
                    enable_resource_name_dns_aRecord=False,
                    hostname_type="hostnameType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__614c34ec8ed85bda4a8cf5e8516a6dc83e45d60c0e29bd2740ea7f6c01ddc3c3)
                check_type(argname="argument enable_resource_name_dns_aaaa_record", value=enable_resource_name_dns_aaaa_record, expected_type=type_hints["enable_resource_name_dns_aaaa_record"])
                check_type(argname="argument enable_resource_name_dns_a_record", value=enable_resource_name_dns_a_record, expected_type=type_hints["enable_resource_name_dns_a_record"])
                check_type(argname="argument hostname_type", value=hostname_type, expected_type=type_hints["hostname_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_resource_name_dns_aaaa_record is not None:
                self._values["enable_resource_name_dns_aaaa_record"] = enable_resource_name_dns_aaaa_record
            if enable_resource_name_dns_a_record is not None:
                self._values["enable_resource_name_dns_a_record"] = enable_resource_name_dns_a_record
            if hostname_type is not None:
                self._values["hostname_type"] = hostname_type

        @builtins.property
        def enable_resource_name_dns_aaaa_record(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-privatednsnameoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-privatednsnameoptionsrequest-enableresourcenamednsaaaarecord
            '''
            result = self._values.get("enable_resource_name_dns_aaaa_record")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_resource_name_dns_a_record(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-privatednsnameoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-privatednsnameoptionsrequest-enableresourcenamednsarecord
            '''
            result = self._values.get("enable_resource_name_dns_a_record")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def hostname_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-privatednsnameoptionsrequest.html#cfn-workspacesinstances-workspaceinstance-privatednsnameoptionsrequest-hostnametype
            '''
            result = self._values.get("hostname_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateDnsNameOptionsRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.RunInstancesMonitoringEnabledProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class RunInstancesMonitoringEnabledProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''
            :param enabled: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-runinstancesmonitoringenabled.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                run_instances_monitoring_enabled_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.RunInstancesMonitoringEnabledProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__688760a14c800268f572de73177e51b61155a9dedd2b2512e09d57aaf9fcba09)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-runinstancesmonitoringenabled.html#cfn-workspacesinstances-workspaceinstance-runinstancesmonitoringenabled-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunInstancesMonitoringEnabledProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_interruption_behavior": "instanceInterruptionBehavior",
            "max_price": "maxPrice",
            "spot_instance_type": "spotInstanceType",
            "valid_until_utc": "validUntilUtc",
        },
    )
    class SpotMarketOptionsProperty:
        def __init__(
            self,
            *,
            instance_interruption_behavior: typing.Optional[builtins.str] = None,
            max_price: typing.Optional[builtins.str] = None,
            spot_instance_type: typing.Optional[builtins.str] = None,
            valid_until_utc: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param instance_interruption_behavior: 
            :param max_price: 
            :param spot_instance_type: 
            :param valid_until_utc: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-spotmarketoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                spot_market_options_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty(
                    instance_interruption_behavior="instanceInterruptionBehavior",
                    max_price="maxPrice",
                    spot_instance_type="spotInstanceType",
                    valid_until_utc="validUntilUtc"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80b4a6198346b2e4455376c94260328effac8b918d110b24cf61c3517aef1803)
                check_type(argname="argument instance_interruption_behavior", value=instance_interruption_behavior, expected_type=type_hints["instance_interruption_behavior"])
                check_type(argname="argument max_price", value=max_price, expected_type=type_hints["max_price"])
                check_type(argname="argument spot_instance_type", value=spot_instance_type, expected_type=type_hints["spot_instance_type"])
                check_type(argname="argument valid_until_utc", value=valid_until_utc, expected_type=type_hints["valid_until_utc"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_interruption_behavior is not None:
                self._values["instance_interruption_behavior"] = instance_interruption_behavior
            if max_price is not None:
                self._values["max_price"] = max_price
            if spot_instance_type is not None:
                self._values["spot_instance_type"] = spot_instance_type
            if valid_until_utc is not None:
                self._values["valid_until_utc"] = valid_until_utc

        @builtins.property
        def instance_interruption_behavior(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-spotmarketoptions.html#cfn-workspacesinstances-workspaceinstance-spotmarketoptions-instanceinterruptionbehavior
            '''
            result = self._values.get("instance_interruption_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_price(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-spotmarketoptions.html#cfn-workspacesinstances-workspaceinstance-spotmarketoptions-maxprice
            '''
            result = self._values.get("max_price")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def spot_instance_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-spotmarketoptions.html#cfn-workspacesinstances-workspaceinstance-spotmarketoptions-spotinstancetype
            '''
            result = self._values.get("spot_instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def valid_until_utc(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-spotmarketoptions.html#cfn-workspacesinstances-workspaceinstance-spotmarketoptions-validuntilutc
            '''
            result = self._values.get("valid_until_utc")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpotMarketOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_workspacesinstances.mixins.CfnWorkspaceInstancePropsMixin.TagSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_type": "resourceType", "tags": "tags"},
    )
    class TagSpecificationProperty:
        def __init__(
            self,
            *,
            resource_type: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param resource_type: 
            :param tags: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-tagspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_workspacesinstances import mixins as workspacesinstances_mixins
                
                tag_specification_property = workspacesinstances_mixins.CfnWorkspaceInstancePropsMixin.TagSpecificationProperty(
                    resource_type="resourceType",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f67d29546a46298d02a6fe6c6ac96c3839a742fdd4bffafbc0011deb409c3d37)
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_type is not None:
                self._values["resource_type"] = resource_type
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-tagspecification.html#cfn-workspacesinstances-workspaceinstance-tagspecification-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-workspacesinstances-workspaceinstance-tagspecification.html#cfn-workspacesinstances-workspaceinstance-tagspecification-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnVolumeAssociationMixinProps",
    "CfnVolumeAssociationPropsMixin",
    "CfnVolumeMixinProps",
    "CfnVolumePropsMixin",
    "CfnWorkspaceInstanceMixinProps",
    "CfnWorkspaceInstancePropsMixin",
]

publication.publish()

def _typecheckingstub__f979d28fb8b4d1fe0cb2c60e9a385add3062ad9803f384b71ebcfc7acc8d2c7b(
    *,
    device: typing.Optional[builtins.str] = None,
    disassociate_mode: typing.Optional[builtins.str] = None,
    volume_id: typing.Optional[builtins.str] = None,
    workspace_instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e33def94ee64b58a414963c8dec56fec498fb68f05b91bd43cb8c185c5e475e(
    props: typing.Union[CfnVolumeAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ae7f96874ef76458876d5bcff00e9a7f651a1698a3dea3e71519e87f1d2cda(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faf1bbcab3a2d9915102c98a6d6b54a460b8e459a5c7fa4d60fade01bfd22098(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61dd9762848a093660e288711ac534e0a5ba4817cbae17a3aab73f18e63517e2(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    size_in_gb: typing.Optional[jsii.Number] = None,
    snapshot_id: typing.Optional[builtins.str] = None,
    tag_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.TagSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9996df0155c8ecf3cc53358442c19a1513bc1174e36b3e58f384c8b3d740f99d(
    props: typing.Union[CfnVolumeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f55a7d9ab49276d4ee085dcd015455a2cfce94b090a90f58483fc1e841951531(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ffd83f6929f849977a80f19bf16d2ab31f8dffc85f848ba1a1b71b56772ee9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94a068c9d41d798dd8aa1a87867f9f6d2b5a9701740e3b366c380f833fc992b(
    *,
    resource_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc2815c47fd4b097149158a5a4b6d1f8cf76f17a7e8a69aba50f679c5e198e8(
    *,
    managed_instance: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.ManagedInstanceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0b4108c54ee74fe608438414bac4a3ed4c298bdcda6b52d8d18f4e4366e5c7(
    props: typing.Union[CfnWorkspaceInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d6e53dbb420652ed5b59498580ad8d1280c0c65edbd4ad9760b57dead5d835(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07bafa9340d192c502df273ae2aee955fa7eb19830655d023e7187cf19974dc7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac96f27b7cfc2df0a3dc61271b46fc9f1fc690227b778beea443eaab557112b(
    *,
    device_name: typing.Optional[builtins.str] = None,
    ebs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.EbsBlockDeviceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    no_device: typing.Optional[builtins.str] = None,
    virtual_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f330706ed23bb89236fb2d977a905fe7e04dbf27f6e9820df20df40808600411(
    *,
    capacity_reservation_preference: typing.Optional[builtins.str] = None,
    capacity_reservation_target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.CapacityReservationTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b4536b56a519845d862cf01ed9ac8481a4b5138d1b66bfe0fe56fe13be3f20(
    *,
    capacity_reservation_id: typing.Optional[builtins.str] = None,
    capacity_reservation_resource_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f357c3d4e744ca751e6a0e7233f03500fc45df0f949c226f1fd2b22add705f72(
    *,
    core_count: typing.Optional[jsii.Number] = None,
    threads_per_core: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8a3a572a1fb7c958aaf3a482a18bb4b830422732791cbe2ebdf4dac28fda27(
    *,
    cpu_credits: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3420a80ad3f8412cb20ff01c8fd96bba01a14438eb26ce2b4c7398d4efaee41b(
    *,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__531ee82d9003c8c02eee69321de3529af6937d63427be5c39fe213bc434852e8(
    *,
    encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_size: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2e9e13a0b1fe6c85b7adb4e30c2955f3b2248d980c0c2b91e7507357621d05(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428e8ea41a407d7bf18513d2e1e6d547f2a986f45b636acece504967e30971d7(
    *,
    configured: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520d1945f11566dbe2e7922e00f4b826a41c7ed457b209e2dffcabeb3f4cc6b0(
    *,
    arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf6cd28b0d867a3a18d78070751bb9d7f6bb54168201ae8c3f2214cd6d2ae2b(
    *,
    auto_recovery: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec9611eb4ce7118d9ac0336bd8cbd62d9a2ca6192a36f405fcfb28f756f27fe(
    *,
    market_type: typing.Optional[builtins.str] = None,
    spot_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.SpotMarketOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9741a29072902432aa59f5a07a038ae58c282dbb9c7c6e5f02a61e0d59127c9a(
    *,
    http_endpoint: typing.Optional[builtins.str] = None,
    http_protocol_ipv6: typing.Optional[builtins.str] = None,
    http_put_response_hop_limit: typing.Optional[jsii.Number] = None,
    http_tokens: typing.Optional[builtins.str] = None,
    instance_metadata_tags: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfcf0d5aa490d29539143d56dfa8a5a38a3714241770cede20cabbc740d2198(
    *,
    description: typing.Optional[builtins.str] = None,
    device_index: typing.Optional[jsii.Number] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a218184e44b0c108cf1e6ed1911f61630ff3c51583f525198d20d7ef4fc42b16(
    *,
    bandwidth_weighting: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34721097bb4d5024991d9b06018a81cda36f7fd52e52d567785010a937d4ff38(
    *,
    license_configuration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638327636a9c0f60e6f4c5e9aa8a94bea77508dc4899f68910b5a4d105a02c4a(
    *,
    block_device_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.BlockDeviceMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    capacity_reservation_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.CapacityReservationSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cpu_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.CpuOptionsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    credit_specification: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.CreditSpecificationRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    disable_api_stop: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ebs_optimized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_primary_ipv6: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enclave_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.EnclaveOptionsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hibernation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.HibernationOptionsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iam_instance_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.IamInstanceProfileSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_id: typing.Optional[builtins.str] = None,
    instance_market_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.InstanceMarketOptionsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    ipv6_address_count: typing.Optional[jsii.Number] = None,
    key_name: typing.Optional[builtins.str] = None,
    license_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.LicenseConfigurationRequestProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    maintenance_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.InstanceMaintenanceOptionsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metadata_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.InstanceMetadataOptionsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    monitoring: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.RunInstancesMonitoringEnabledProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_interfaces: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.InstanceNetworkInterfaceSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_performance_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.InstanceNetworkPerformanceOptionsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    placement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.PlacementProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    private_dns_name_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.PrivateDnsNameOptionsRequestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tag_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkspaceInstancePropsMixin.TagSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    user_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05bba15c9fb32c00a955667e50e1bff93e840bb1faca1e4ccaafba170c88a48e(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    group_name: typing.Optional[builtins.str] = None,
    partition_number: typing.Optional[jsii.Number] = None,
    tenancy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614c34ec8ed85bda4a8cf5e8516a6dc83e45d60c0e29bd2740ea7f6c01ddc3c3(
    *,
    enable_resource_name_dns_aaaa_record: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_resource_name_dns_a_record: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    hostname_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688760a14c800268f572de73177e51b61155a9dedd2b2512e09d57aaf9fcba09(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b4a6198346b2e4455376c94260328effac8b918d110b24cf61c3517aef1803(
    *,
    instance_interruption_behavior: typing.Optional[builtins.str] = None,
    max_price: typing.Optional[builtins.str] = None,
    spot_instance_type: typing.Optional[builtins.str] = None,
    valid_until_utc: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67d29546a46298d02a6fe6c6ac96c3839a742fdd4bffafbc0011deb409c3d37(
    *,
    resource_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
