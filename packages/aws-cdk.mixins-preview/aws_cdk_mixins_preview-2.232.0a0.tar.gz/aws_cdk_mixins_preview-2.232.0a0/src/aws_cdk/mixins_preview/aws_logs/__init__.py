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

from .._jsii import *

import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="@aws-cdk/mixins-preview.aws_logs.ILogsDelivery")
class ILogsDelivery(typing_extensions.Protocol):
    '''(experimental) Represents the delivery of vended logs to a destination.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
        source_resource_arn: builtins.str,
    ) -> "ILogsDeliveryConfig":
        '''(experimental) Binds the destination to a delivery source and creates a delivery connection between the source and destination.

        :param scope: - The construct scope.
        :param delivery_source: - The delivery source reference.
        :param source_resource_arn: - The Arn of the source resource.

        :return: The delivery reference

        :stability: experimental
        '''
        ...


class _ILogsDeliveryProxy:
    '''(experimental) Represents the delivery of vended logs to a destination.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/mixins-preview.aws_logs.ILogsDelivery"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
        source_resource_arn: builtins.str,
    ) -> "ILogsDeliveryConfig":
        '''(experimental) Binds the destination to a delivery source and creates a delivery connection between the source and destination.

        :param scope: - The construct scope.
        :param delivery_source: - The delivery source reference.
        :param source_resource_arn: - The Arn of the source resource.

        :return: The delivery reference

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40d3cac2e91f6aaddd07e548330430a47757a92baefe0e8435310cf7030c46b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument delivery_source", value=delivery_source, expected_type=type_hints["delivery_source"])
            check_type(argname="argument source_resource_arn", value=source_resource_arn, expected_type=type_hints["source_resource_arn"])
        return typing.cast("ILogsDeliveryConfig", jsii.invoke(self, "bind", [scope, delivery_source, source_resource_arn]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogsDelivery).__jsii_proxy_class__ = lambda : _ILogsDeliveryProxy


@jsii.interface(jsii_type="@aws-cdk/mixins-preview.aws_logs.ILogsDeliveryConfig")
class ILogsDeliveryConfig(typing_extensions.Protocol):
    '''(experimental) The individual elements of a logs delivery integration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="delivery")
    def delivery(self) -> _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliveryRef:
        '''(experimental) The logs delivery.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="deliveryDestination")
    def delivery_destination(
        self,
    ) -> _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliveryDestinationRef:
        '''(experimental) The logs delivery destination.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="deliverySource")
    def delivery_source(
        self,
    ) -> _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef:
        '''(experimental) The logs delivery source.

        :stability: experimental
        '''
        ...


class _ILogsDeliveryConfigProxy:
    '''(experimental) The individual elements of a logs delivery integration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/mixins-preview.aws_logs.ILogsDeliveryConfig"

    @builtins.property
    @jsii.member(jsii_name="delivery")
    def delivery(self) -> _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliveryRef:
        '''(experimental) The logs delivery.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_interfaces_aws_logs_ceddda9d.IDeliveryRef, jsii.get(self, "delivery"))

    @builtins.property
    @jsii.member(jsii_name="deliveryDestination")
    def delivery_destination(
        self,
    ) -> _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliveryDestinationRef:
        '''(experimental) The logs delivery destination.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_interfaces_aws_logs_ceddda9d.IDeliveryDestinationRef, jsii.get(self, "deliveryDestination"))

    @builtins.property
    @jsii.member(jsii_name="deliverySource")
    def delivery_source(
        self,
    ) -> _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef:
        '''(experimental) The logs delivery source.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef, jsii.get(self, "deliverySource"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogsDeliveryConfig).__jsii_proxy_class__ = lambda : _ILogsDeliveryConfigProxy


@jsii.implements(ILogsDelivery)
class LogGroupLogsDelivery(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.LogGroupLogsDelivery",
):
    '''(experimental) Delivers vended logs to a CloudWatch Log Group.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.interfaces import aws_logs as interfaces_logs
        
        # log_group_ref: interfaces_logs.ILogGroupRef
        
        log_group_logs_delivery = logs.LogGroupLogsDelivery(log_group_ref)
    '''

    def __init__(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> None:
        '''(experimental) Creates a new log group delivery.

        :param log_group: - The CloudWatch Logs log group reference.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a309989d5d7187cf24683386068fad207515b2576eeb8c48e05d73bff1f48e)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        jsii.create(self.__class__, self, [log_group])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
        _source_resource_arn: builtins.str,
    ) -> ILogsDeliveryConfig:
        '''(experimental) Binds the log group destination to a delivery source and creates a delivery connection between them.

        :param scope: -
        :param delivery_source: -
        :param _source_resource_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e79469f5cbd3e4cbe225c0f77e8931bcbaa38f24a1dbedf8f27e8de6f2a1684)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument delivery_source", value=delivery_source, expected_type=type_hints["delivery_source"])
            check_type(argname="argument _source_resource_arn", value=_source_resource_arn, expected_type=type_hints["_source_resource_arn"])
        return typing.cast(ILogsDeliveryConfig, jsii.invoke(self, "bind", [scope, delivery_source, _source_resource_arn]))


@jsii.implements(ILogsDelivery)
class S3LogsDelivery(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.S3LogsDelivery",
):
    '''(experimental) Delivers vended logs to an S3 Bucket.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.interfaces import aws_s3 as interfaces_s3
        
        # bucket_ref: interfaces_s3.IBucketRef
        
        s3_logs_delivery = logs.S3LogsDelivery(bucket_ref,
            permissions_version=logs.S3LogsDeliveryPermissionsVersion.V1
        )
    '''

    def __init__(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
        *,
        permissions_version: typing.Optional["S3LogsDeliveryPermissionsVersion"] = None,
    ) -> None:
        '''(experimental) Creates a new S3 Bucket delivery.

        :param bucket: -
        :param permissions_version: (experimental) The permissions version ('V1' or 'V2') to be used for this delivery. Depending on the source of the logs, different permissions are required. Default: "V2"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a123400340e622550ee0692a1be65c353fc5d0686c01e30601595a4e7d6e91ed)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        props = S3LogsDeliveryProps(permissions_version=permissions_version)

        jsii.create(self.__class__, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
        _source_resource_arn: builtins.str,
    ) -> ILogsDeliveryConfig:
        '''(experimental) Binds the S3 destination to a delivery source and creates a delivery connection between them.

        :param scope: -
        :param delivery_source: -
        :param _source_resource_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef5b209cd95fb6ed852e9ae5b30d866d8c4d527a173a6acf38342d2ead7f3e0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument delivery_source", value=delivery_source, expected_type=type_hints["delivery_source"])
            check_type(argname="argument _source_resource_arn", value=_source_resource_arn, expected_type=type_hints["_source_resource_arn"])
        return typing.cast(ILogsDeliveryConfig, jsii.invoke(self, "bind", [scope, delivery_source, _source_resource_arn]))


@jsii.enum(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.S3LogsDeliveryPermissionsVersion"
)
class S3LogsDeliveryPermissionsVersion(enum.Enum):
    '''(experimental) S3 Vended Logs Permissions version.

    :stability: experimental
    '''

    V1 = "V1"
    '''(experimental) V1.

    :stability: experimental
    '''
    V2 = "V2"
    '''(experimental) V2.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.S3LogsDeliveryProps",
    jsii_struct_bases=[],
    name_mapping={"permissions_version": "permissionsVersion"},
)
class S3LogsDeliveryProps:
    def __init__(
        self,
        *,
        permissions_version: typing.Optional[S3LogsDeliveryPermissionsVersion] = None,
    ) -> None:
        '''(experimental) Props for S3LogsDelivery.

        :param permissions_version: (experimental) The permissions version ('V1' or 'V2') to be used for this delivery. Depending on the source of the logs, different permissions are required. Default: "V2"

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview import aws_logs as logs
            
            s3_logs_delivery_props = logs.S3LogsDeliveryProps(
                permissions_version=logs.S3LogsDeliveryPermissionsVersion.V1
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965d6da0502509cc8b0a3bf4ed55be1a6e577c7cd78c674370ee559100584de5)
            check_type(argname="argument permissions_version", value=permissions_version, expected_type=type_hints["permissions_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if permissions_version is not None:
            self._values["permissions_version"] = permissions_version

    @builtins.property
    def permissions_version(self) -> typing.Optional[S3LogsDeliveryPermissionsVersion]:
        '''(experimental) The permissions version ('V1' or 'V2') to be used for this delivery.

        Depending on the source of the logs, different permissions are required.

        :default: "V2"

        :stability: experimental
        '''
        result = self._values.get("permissions_version")
        return typing.cast(typing.Optional[S3LogsDeliveryPermissionsVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3LogsDeliveryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILogsDelivery)
class XRayLogsDelivery(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.XRayLogsDelivery",
):
    '''(experimental) Delivers vended logs to AWS X-Ray.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        
        x_ray_logs_delivery = logs.XRayLogsDelivery()
    '''

    def __init__(self) -> None:
        '''(experimental) Creates a new X-Ray delivery.

        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
        source_resource_arn: builtins.str,
    ) -> ILogsDeliveryConfig:
        '''(experimental) Binds the X-Ray destination to a delivery source and creates a delivery connection between them.

        :param scope: -
        :param delivery_source: -
        :param source_resource_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1fe6c2c446c40af17ce3976872564b1c99e7609366cd6b223ac1075c26d73d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument delivery_source", value=delivery_source, expected_type=type_hints["delivery_source"])
            check_type(argname="argument source_resource_arn", value=source_resource_arn, expected_type=type_hints["source_resource_arn"])
        return typing.cast(ILogsDeliveryConfig, jsii.invoke(self, "bind", [scope, delivery_source, source_resource_arn]))


@jsii.implements(ILogsDelivery)
class FirehoseLogsDelivery(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.FirehoseLogsDelivery",
):
    '''(experimental) Delivers vended logs to a Firehose Delivery Stream.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.interfaces import aws_kinesisfirehose as interfaces_kinesisfirehose
        
        # delivery_stream_ref: interfaces_kinesisfirehose.IDeliveryStreamRef
        
        firehose_logs_delivery = logs.FirehoseLogsDelivery(delivery_stream_ref)
    '''

    def __init__(
        self,
        stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> None:
        '''(experimental) Creates a new Firehose delivery.

        :param stream: - The Kinesis Data Firehose delivery stream.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0b24d190fc62c060eef3e86d06686a87e03b4269c251da1b3a3cc7d20774d7)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        jsii.create(self.__class__, self, [stream])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
        _source_resource_arn: builtins.str,
    ) -> ILogsDeliveryConfig:
        '''(experimental) Binds the Firehose destination to a delivery source and creates a delivery connection between them.

        :param scope: -
        :param delivery_source: -
        :param _source_resource_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64902ab0b4e9bc2c5da4e4e81c16d8d2c90b2bd79f4f0d8f5e95ddd4e909e65)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument delivery_source", value=delivery_source, expected_type=type_hints["delivery_source"])
            check_type(argname="argument _source_resource_arn", value=_source_resource_arn, expected_type=type_hints["_source_resource_arn"])
        return typing.cast(ILogsDeliveryConfig, jsii.invoke(self, "bind", [scope, delivery_source, _source_resource_arn]))


__all__ = [
    "FirehoseLogsDelivery",
    "ILogsDelivery",
    "ILogsDeliveryConfig",
    "LogGroupLogsDelivery",
    "S3LogsDelivery",
    "S3LogsDeliveryPermissionsVersion",
    "S3LogsDeliveryProps",
    "XRayLogsDelivery",
    "events",
    "mixins",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import events
from . import mixins

def _typecheckingstub__f40d3cac2e91f6aaddd07e548330430a47757a92baefe0e8435310cf7030c46b(
    scope: _constructs_77d1e7e8.IConstruct,
    delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
    source_resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a309989d5d7187cf24683386068fad207515b2576eeb8c48e05d73bff1f48e(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e79469f5cbd3e4cbe225c0f77e8931bcbaa38f24a1dbedf8f27e8de6f2a1684(
    scope: _constructs_77d1e7e8.IConstruct,
    delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
    _source_resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a123400340e622550ee0692a1be65c353fc5d0686c01e30601595a4e7d6e91ed(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    *,
    permissions_version: typing.Optional[S3LogsDeliveryPermissionsVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef5b209cd95fb6ed852e9ae5b30d866d8c4d527a173a6acf38342d2ead7f3e0(
    scope: _constructs_77d1e7e8.IConstruct,
    delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
    _source_resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965d6da0502509cc8b0a3bf4ed55be1a6e577c7cd78c674370ee559100584de5(
    *,
    permissions_version: typing.Optional[S3LogsDeliveryPermissionsVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1fe6c2c446c40af17ce3976872564b1c99e7609366cd6b223ac1075c26d73d(
    scope: _constructs_77d1e7e8.IConstruct,
    delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
    source_resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0b24d190fc62c060eef3e86d06686a87e03b4269c251da1b3a3cc7d20774d7(
    stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64902ab0b4e9bc2c5da4e4e81c16d8d2c90b2bd79f4f0d8f5e95ddd4e909e65(
    scope: _constructs_77d1e7e8.IConstruct,
    delivery_source: _aws_cdk_interfaces_aws_logs_ceddda9d.IDeliverySourceRef,
    _source_resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ILogsDelivery, ILogsDeliveryConfig]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
