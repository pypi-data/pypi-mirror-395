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
    jsii_type="@aws-cdk/mixins-preview.aws_simspaceweaver.mixins.CfnSimulationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_duration": "maximumDuration",
        "name": "name",
        "role_arn": "roleArn",
        "schema_s3_location": "schemaS3Location",
        "snapshot_s3_location": "snapshotS3Location",
    },
)
class CfnSimulationMixinProps:
    def __init__(
        self,
        *,
        maximum_duration: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schema_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSimulationPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        snapshot_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSimulationPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSimulationPropsMixin.

        :param maximum_duration: The maximum running time of the simulation, specified as a number of minutes (m or M), hours (h or H), or days (d or D). The simulation stops when it reaches this limit. The maximum value is ``14D`` , or its equivalent in the other units. The default value is ``14D`` . A value equivalent to ``0`` makes the simulation immediately transition to ``STOPPING`` as soon as it reaches ``STARTED`` .
        :param name: The name of the simulation.
        :param role_arn: The Amazon Resource Name (ARN) of the AWS Identity and Access Management ( IAM ) role that the simulation assumes to perform actions. For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* . For more information about IAM roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_ in the *AWS Identity and Access Management User Guide* .
        :param schema_s3_location: The location of the simulation schema in Amazon Simple Storage Service ( Amazon S3 ). For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ . Provide a ``SchemaS3Location`` to start your simulation from a schema. If you provide a ``SchemaS3Location`` then you can't provide a ``SnapshotS3Location`` .
        :param snapshot_s3_location: The location of the snapshot in Amazon Simple Storage Service ( Amazon S3 ). For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ . Provide a ``SnapshotS3Location`` to start your simulation from a snapshot. If you provide a ``SnapshotS3Location`` then you can't provide a ``SchemaS3Location`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_simspaceweaver import mixins as simspaceweaver_mixins
            
            cfn_simulation_mixin_props = simspaceweaver_mixins.CfnSimulationMixinProps(
                maximum_duration="maximumDuration",
                name="name",
                role_arn="roleArn",
                schema_s3_location=simspaceweaver_mixins.CfnSimulationPropsMixin.S3LocationProperty(
                    bucket_name="bucketName",
                    object_key="objectKey"
                ),
                snapshot_s3_location=simspaceweaver_mixins.CfnSimulationPropsMixin.S3LocationProperty(
                    bucket_name="bucketName",
                    object_key="objectKey"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d0696bc057e3ab6079f34e33eaf64cb5c648fc8da7d6905fedaba9e45506d0)
            check_type(argname="argument maximum_duration", value=maximum_duration, expected_type=type_hints["maximum_duration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument schema_s3_location", value=schema_s3_location, expected_type=type_hints["schema_s3_location"])
            check_type(argname="argument snapshot_s3_location", value=snapshot_s3_location, expected_type=type_hints["snapshot_s3_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if maximum_duration is not None:
            self._values["maximum_duration"] = maximum_duration
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if schema_s3_location is not None:
            self._values["schema_s3_location"] = schema_s3_location
        if snapshot_s3_location is not None:
            self._values["snapshot_s3_location"] = snapshot_s3_location

    @builtins.property
    def maximum_duration(self) -> typing.Optional[builtins.str]:
        '''The maximum running time of the simulation, specified as a number of minutes (m or M), hours (h or H), or days (d or D).

        The simulation stops when it reaches this limit. The maximum value is ``14D`` , or its equivalent in the other units. The default value is ``14D`` . A value equivalent to ``0`` makes the simulation immediately transition to ``STOPPING`` as soon as it reaches ``STARTED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-maximumduration
        '''
        result = self._values.get("maximum_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the simulation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management ( IAM ) role that the simulation assumes to perform actions.

        For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* . For more information about IAM roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_ in the *AWS Identity and Access Management User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimulationPropsMixin.S3LocationProperty"]]:
        '''The location of the simulation schema in Amazon Simple Storage Service ( Amazon S3 ).

        For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ .

        Provide a ``SchemaS3Location`` to start your simulation from a schema.

        If you provide a ``SchemaS3Location`` then you can't provide a ``SnapshotS3Location`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-schemas3location
        '''
        result = self._values.get("schema_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimulationPropsMixin.S3LocationProperty"]], result)

    @builtins.property
    def snapshot_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimulationPropsMixin.S3LocationProperty"]]:
        '''The location of the snapshot in Amazon Simple Storage Service ( Amazon S3 ).

        For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ .

        Provide a ``SnapshotS3Location`` to start your simulation from a snapshot.

        If you provide a ``SnapshotS3Location`` then you can't provide a ``SchemaS3Location`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-snapshots3location
        '''
        result = self._values.get("snapshot_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimulationPropsMixin.S3LocationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimulationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSimulationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_simspaceweaver.mixins.CfnSimulationPropsMixin",
):
    '''Use the ``AWS::SimSpaceWeaver::Simulation`` resource to specify a simulation that CloudFormation starts in the AWS Cloud , in your AWS account .

    In the resource properties section of your template, provide the name of an existing IAM role configured with the proper permissions, and the name of an existing Amazon S3 bucket. Your account must have permissions to read the Amazon S3 bucket. The Amazon S3 bucket must contain a valid schema. The schema must refer to simulation assets that are already uploaded to the AWS Cloud . For more information, see the `detailed tutorial <https://docs.aws.amazon.com/simspaceweaver/latest/userguide/getting-started_detailed.html>`_ in the *AWS SimSpace Weaver User Guide* .

    Specify a ``SnapshotS3Location`` to start a simulation from a snapshot instead of from a schema. When you start a simulation from a snapshot, SimSpace Weaver initializes the entity data in the State Fabric with data saved in the snapshot, starts the spatial and service apps that were running when the snapshot was created, and restores the clock to the appropriate tick. Your app zip files must be in the same location in Amazon S3 as they were in for the original simulation. You must start any custom apps separately. For more information about snapshots, see `Snapshots <https://docs.aws.amazon.com/simspaceweaver/latest/userguide/working-with_snapshots.html>`_ in the *AWS SimSpace Weaver User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html
    :cloudformationResource: AWS::SimSpaceWeaver::Simulation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_simspaceweaver import mixins as simspaceweaver_mixins
        
        cfn_simulation_props_mixin = simspaceweaver_mixins.CfnSimulationPropsMixin(simspaceweaver_mixins.CfnSimulationMixinProps(
            maximum_duration="maximumDuration",
            name="name",
            role_arn="roleArn",
            schema_s3_location=simspaceweaver_mixins.CfnSimulationPropsMixin.S3LocationProperty(
                bucket_name="bucketName",
                object_key="objectKey"
            ),
            snapshot_s3_location=simspaceweaver_mixins.CfnSimulationPropsMixin.S3LocationProperty(
                bucket_name="bucketName",
                object_key="objectKey"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSimulationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SimSpaceWeaver::Simulation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eab1f0ba016851f54319d92a73dee8dc80f42b2a45d66e4ae1f9b09d3bc2863)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d0cb4fe804ae8e0107f6a792e8419f890d9ebc7e693d4ef01d3dda04fe1c66a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52977f8883595c8fa80fbe859aca827e5ed481b38652b063e193e54986f64973)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSimulationMixinProps:
        return typing.cast(CfnSimulationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_simspaceweaver.mixins.CfnSimulationPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "object_key": "objectKey"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            object_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A location in Amazon Simple Storage Service ( Amazon S3 ) where SimSpace Weaver stores simulation data, such as your app .zip files and schema file. For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ .

            :param bucket_name: The name of an Amazon S3 bucket. For more information about buckets, see `Creating, configuring, and working with Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html>`_ in the *Amazon Simple Storage Service User Guide* .
            :param object_key: The key name of an object in Amazon S3. For more information about Amazon S3 objects and object keys, see `Uploading, downloading, and working with objects in Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/uploading-downloading-objects.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-simspaceweaver-simulation-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_simspaceweaver import mixins as simspaceweaver_mixins
                
                s3_location_property = simspaceweaver_mixins.CfnSimulationPropsMixin.S3LocationProperty(
                    bucket_name="bucketName",
                    object_key="objectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b76995e7f1499c3c8924cc5d4bd1dd190055440d4822b7f44caeabc0e1217be)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument object_key", value=object_key, expected_type=type_hints["object_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if object_key is not None:
                self._values["object_key"] = object_key

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of an Amazon S3 bucket.

            For more information about buckets, see `Creating, configuring, and working with Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-simspaceweaver-simulation-s3location.html#cfn-simspaceweaver-simulation-s3location-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_key(self) -> typing.Optional[builtins.str]:
            '''The key name of an object in Amazon S3.

            For more information about Amazon S3 objects and object keys, see `Uploading, downloading, and working with objects in Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/uploading-downloading-objects.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-simspaceweaver-simulation-s3location.html#cfn-simspaceweaver-simulation-s3location-objectkey
            '''
            result = self._values.get("object_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnSimulationMixinProps",
    "CfnSimulationPropsMixin",
]

publication.publish()

def _typecheckingstub__f2d0696bc057e3ab6079f34e33eaf64cb5c648fc8da7d6905fedaba9e45506d0(
    *,
    maximum_duration: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schema_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSimulationPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snapshot_s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSimulationPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eab1f0ba016851f54319d92a73dee8dc80f42b2a45d66e4ae1f9b09d3bc2863(
    props: typing.Union[CfnSimulationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0cb4fe804ae8e0107f6a792e8419f890d9ebc7e693d4ef01d3dda04fe1c66a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52977f8883595c8fa80fbe859aca827e5ed481b38652b063e193e54986f64973(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b76995e7f1499c3c8924cc5d4bd1dd190055440d4822b7f44caeabc0e1217be(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    object_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
