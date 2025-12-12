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
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnAccessLogSubscriptionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_arn": "destinationArn",
        "resource_identifier": "resourceIdentifier",
        "service_network_log_type": "serviceNetworkLogType",
        "tags": "tags",
    },
)
class CfnAccessLogSubscriptionMixinProps:
    def __init__(
        self,
        *,
        destination_arn: typing.Optional[builtins.str] = None,
        resource_identifier: typing.Optional[builtins.str] = None,
        service_network_log_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessLogSubscriptionPropsMixin.

        :param destination_arn: The Amazon Resource Name (ARN) of the destination. The supported destination types are CloudWatch Log groups, Kinesis Data Firehose delivery streams, and Amazon S3 buckets.
        :param resource_identifier: The ID or ARN of the service network or service.
        :param service_network_log_type: Log type of the service network.
        :param tags: The tags for the access log subscription.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_access_log_subscription_mixin_props = vpclattice_mixins.CfnAccessLogSubscriptionMixinProps(
                destination_arn="destinationArn",
                resource_identifier="resourceIdentifier",
                service_network_log_type="serviceNetworkLogType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b19c5f911504ae2e72dfd7bd3f412c37738f34a84318990f190e2ce94bcfc2)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            check_type(argname="argument service_network_log_type", value=service_network_log_type, expected_type=type_hints["service_network_log_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_arn is not None:
            self._values["destination_arn"] = destination_arn
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier
        if service_network_log_type is not None:
            self._values["service_network_log_type"] = service_network_log_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the destination.

        The supported destination types are CloudWatch Log groups, Kinesis Data Firehose delivery streams, and Amazon S3 buckets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-destinationarn
        '''
        result = self._values.get("destination_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or ARN of the service network or service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_network_log_type(self) -> typing.Optional[builtins.str]:
        '''Log type of the service network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-servicenetworklogtype
        '''
        result = self._values.get("service_network_log_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the access log subscription.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessLogSubscriptionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessLogSubscriptionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnAccessLogSubscriptionPropsMixin",
):
    '''Enables access logs to be sent to Amazon CloudWatch, Amazon S3, and Amazon Kinesis Data Firehose.

    The service network owner can use the access logs to audit the services in the network. The service network owner can only see access logs from clients and services that are associated with their service network. Access log entries represent traffic originated from VPCs associated with that network. For more information, see `Access logs <https://docs.aws.amazon.com/vpc-lattice/latest/ug/monitoring-access-logs.html>`_ in the *Amazon VPC Lattice User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html
    :cloudformationResource: AWS::VpcLattice::AccessLogSubscription
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_access_log_subscription_props_mixin = vpclattice_mixins.CfnAccessLogSubscriptionPropsMixin(vpclattice_mixins.CfnAccessLogSubscriptionMixinProps(
            destination_arn="destinationArn",
            resource_identifier="resourceIdentifier",
            service_network_log_type="serviceNetworkLogType",
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
        props: typing.Union[CfnAccessLogSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::AccessLogSubscription``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ea917003345f231bdc77b75d6e8bd4c1f417c9c79da1af13e5750b99b83c5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83c5f382a88f28833cae01a605ccaf0d319508f5518d628d7159a1f62b016926)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0eefbc5245328855ccc28982acd3c8aca6a9ab1b159df2e49834e1515b4c18)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessLogSubscriptionMixinProps:
        return typing.cast(CfnAccessLogSubscriptionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnAuthPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_identifier": "resourceIdentifier"},
)
class CfnAuthPolicyMixinProps:
    def __init__(
        self,
        *,
        policy: typing.Any = None,
        resource_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAuthPolicyPropsMixin.

        :param policy: The auth policy.
        :param resource_identifier: The ID or ARN of the service network or service for which the policy is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            # policy: Any
            
            cfn_auth_policy_mixin_props = vpclattice_mixins.CfnAuthPolicyMixinProps(
                policy=policy,
                resource_identifier="resourceIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f16c8e0ec6e8f9250204821d638421e660faa78ce415caa9a79d030bba3f29b5)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier

    @builtins.property
    def policy(self) -> typing.Any:
        '''The auth policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or ARN of the service network or service for which the policy is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAuthPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAuthPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnAuthPolicyPropsMixin",
):
    '''Creates or updates the auth policy. The policy string in JSON must not contain newlines or blank lines.

    For more information, see `Auth policies <https://docs.aws.amazon.com/vpc-lattice/latest/ug/auth-policies.html>`_ in the *Amazon VPC Lattice User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html
    :cloudformationResource: AWS::VpcLattice::AuthPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        # policy: Any
        
        cfn_auth_policy_props_mixin = vpclattice_mixins.CfnAuthPolicyPropsMixin(vpclattice_mixins.CfnAuthPolicyMixinProps(
            policy=policy,
            resource_identifier="resourceIdentifier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAuthPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::AuthPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b067642476d1c88f343ff0f6d912ae9ceb55f84de65b23313a0d5f56756a9c00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9cc0d242d82bd8f319fc7c6a76dde34779c517b6116ca113e9c3a3aaacddc0a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bea0b4be304e015678e1d287d1cfec94a48b0dcde4bb4af304fea3e92d57799)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAuthPolicyMixinProps:
        return typing.cast(CfnAuthPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnDomainVerificationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"domain_name": "domainName", "tags": "tags"},
)
class CfnDomainVerificationMixinProps:
    def __init__(
        self,
        *,
        domain_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainVerificationPropsMixin.

        :param domain_name: The domain name being verified.
        :param tags: The tags associated with the domain verification.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-domainverification.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_domain_verification_mixin_props = vpclattice_mixins.CfnDomainVerificationMixinProps(
                domain_name="domainName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5dee590516d62f29986336b91b580ee3d44f68d33cbc896806fa064dfae7725)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name being verified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-domainverification.html#cfn-vpclattice-domainverification-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags associated with the domain verification.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-domainverification.html#cfn-vpclattice-domainverification-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainVerificationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainVerificationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnDomainVerificationPropsMixin",
):
    '''A domain name verification is an entity that allows you to prove your ownership of a given domain.

    When you create a domain verification using CloudFormation, use a waiter to make sure the domain verification is complete before you create a service network resource association, a VPC endpoint, or a service network VPC association with this domain.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-domainverification.html
    :cloudformationResource: AWS::VpcLattice::DomainVerification
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_domain_verification_props_mixin = vpclattice_mixins.CfnDomainVerificationPropsMixin(vpclattice_mixins.CfnDomainVerificationMixinProps(
            domain_name="domainName",
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
        props: typing.Union[CfnDomainVerificationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::DomainVerification``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98565fc1d897e2393ef399ad60a02ea7ee687d19120f5f7b8138fe66a281fcdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1042653f7f4b4dddada6ee8cc81ab6792ddb8fc05b61074b1eeafb29a80a7ead)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dea3c50f7a05c4f17fbd00df567d9407a44190c7732e7a5608cee5eb3dcfeaa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainVerificationMixinProps:
        return typing.cast(CfnDomainVerificationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnDomainVerificationPropsMixin.TxtMethodConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class TxtMethodConfigProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for TXT record-based domain verification method.

            :param name: The name of the TXT record that must be created for domain verification.
            :param value: The value that must be added to the TXT record for domain verification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-domainverification-txtmethodconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                txt_method_config_property = vpclattice_mixins.CfnDomainVerificationPropsMixin.TxtMethodConfigProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b7cf231bd065f3f7e286b4589475fb0704cfd328aec875b1fc8239b996003f6)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the TXT record that must be created for domain verification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-domainverification-txtmethodconfig.html#cfn-vpclattice-domainverification-txtmethodconfig-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value that must be added to the TXT record for domain verification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-domainverification-txtmethodconfig.html#cfn-vpclattice-domainverification-txtmethodconfig-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TxtMethodConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnListenerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "name": "name",
        "port": "port",
        "protocol": "protocol",
        "service_identifier": "serviceIdentifier",
        "tags": "tags",
    },
)
class CfnListenerMixinProps:
    def __init__(
        self,
        *,
        default_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.DefaultActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnListenerPropsMixin.

        :param default_action: The action for the default rule. Each listener has a default rule. The default rule is used if no other rules match.
        :param name: The name of the listener. A listener name must be unique within a service. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param port: The listener port. You can specify a value from 1 to 65535. For HTTP, the default is 80. For HTTPS, the default is 443.
        :param protocol: The listener protocol.
        :param service_identifier: The ID or ARN of the service.
        :param tags: The tags for the listener.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_listener_mixin_props = vpclattice_mixins.CfnListenerMixinProps(
                default_action=vpclattice_mixins.CfnListenerPropsMixin.DefaultActionProperty(
                    fixed_response=vpclattice_mixins.CfnListenerPropsMixin.FixedResponseProperty(
                        status_code=123
                    ),
                    forward=vpclattice_mixins.CfnListenerPropsMixin.ForwardProperty(
                        target_groups=[vpclattice_mixins.CfnListenerPropsMixin.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
                            weight=123
                        )]
                    )
                ),
                name="name",
                port=123,
                protocol="protocol",
                service_identifier="serviceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5af3e3a4383db753b84c63b0ae72fdaa4f98a1a65d32bca5f61de73926be6a9)
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_action is not None:
            self._values["default_action"] = default_action
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_action(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.DefaultActionProperty"]]:
        '''The action for the default rule.

        Each listener has a default rule. The default rule is used if no other rules match.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-defaultaction
        '''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.DefaultActionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the listener.

        A listener name must be unique within a service. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The listener port.

        You can specify a value from 1 to 65535. For HTTP, the default is 80. For HTTPS, the default is 443.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The listener protocol.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or ARN of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the listener.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnListenerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnListenerPropsMixin",
):
    '''Creates a listener for a service.

    Before you start using your Amazon VPC Lattice service, you must add one or more listeners. A listener is a process that checks for connection requests to your services. For more information, see `Listeners <https://docs.aws.amazon.com/vpc-lattice/latest/ug/listeners.html>`_ in the *Amazon VPC Lattice User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html
    :cloudformationResource: AWS::VpcLattice::Listener
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_listener_props_mixin = vpclattice_mixins.CfnListenerPropsMixin(vpclattice_mixins.CfnListenerMixinProps(
            default_action=vpclattice_mixins.CfnListenerPropsMixin.DefaultActionProperty(
                fixed_response=vpclattice_mixins.CfnListenerPropsMixin.FixedResponseProperty(
                    status_code=123
                ),
                forward=vpclattice_mixins.CfnListenerPropsMixin.ForwardProperty(
                    target_groups=[vpclattice_mixins.CfnListenerPropsMixin.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
                        weight=123
                    )]
                )
            ),
            name="name",
            port=123,
            protocol="protocol",
            service_identifier="serviceIdentifier",
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
        props: typing.Union[CfnListenerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::Listener``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e9e4a1e8b9a579d4d73f5f8049e7b1e82cd714c38ec888e8f760679bd18486)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65d78473cba0d1739df6a2127fea6f28f7fc151f599f247a7bf51388dd6740f8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37bbf60dd3c00734693823c4b11086727adbd3fe22a65d6e38532db76a2311ab)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnListenerMixinProps:
        return typing.cast(CfnListenerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnListenerPropsMixin.DefaultActionProperty",
        jsii_struct_bases=[],
        name_mapping={"fixed_response": "fixedResponse", "forward": "forward"},
    )
    class DefaultActionProperty:
        def __init__(
            self,
            *,
            fixed_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.FixedResponseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            forward: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.ForwardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The action for the default rule.

            Each listener has a default rule. The default rule is used if no other rules match.

            :param fixed_response: Describes an action that returns a custom HTTP response.
            :param forward: Describes a forward action. You can use forward actions to route requests to one or more target groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-defaultaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                default_action_property = vpclattice_mixins.CfnListenerPropsMixin.DefaultActionProperty(
                    fixed_response=vpclattice_mixins.CfnListenerPropsMixin.FixedResponseProperty(
                        status_code=123
                    ),
                    forward=vpclattice_mixins.CfnListenerPropsMixin.ForwardProperty(
                        target_groups=[vpclattice_mixins.CfnListenerPropsMixin.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
                            weight=123
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d747f7b2bc805c2bf3496c6c2f20e58b6cb61584909245cb0d5e34b2872b9494)
                check_type(argname="argument fixed_response", value=fixed_response, expected_type=type_hints["fixed_response"])
                check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fixed_response is not None:
                self._values["fixed_response"] = fixed_response
            if forward is not None:
                self._values["forward"] = forward

        @builtins.property
        def fixed_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.FixedResponseProperty"]]:
            '''Describes an action that returns a custom HTTP response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-defaultaction.html#cfn-vpclattice-listener-defaultaction-fixedresponse
            '''
            result = self._values.get("fixed_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.FixedResponseProperty"]], result)

        @builtins.property
        def forward(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.ForwardProperty"]]:
            '''Describes a forward action.

            You can use forward actions to route requests to one or more target groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-defaultaction.html#cfn-vpclattice-listener-defaultaction-forward
            '''
            result = self._values.get("forward")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.ForwardProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnListenerPropsMixin.FixedResponseProperty",
        jsii_struct_bases=[],
        name_mapping={"status_code": "statusCode"},
    )
    class FixedResponseProperty:
        def __init__(self, *, status_code: typing.Optional[jsii.Number] = None) -> None:
            '''Describes an action that returns a custom HTTP response.

            :param status_code: The HTTP response code. Only ``404`` and ``500`` status codes are supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-fixedresponse.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                fixed_response_property = vpclattice_mixins.CfnListenerPropsMixin.FixedResponseProperty(
                    status_code=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e13f45434f6aeeeda7b1b8a6ddb0811c5dd49875fe767aafe776296f361444e8)
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status_code is not None:
                self._values["status_code"] = status_code

        @builtins.property
        def status_code(self) -> typing.Optional[jsii.Number]:
            '''The HTTP response code.

            Only ``404`` and ``500`` status codes are supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-fixedresponse.html#cfn-vpclattice-listener-fixedresponse-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnListenerPropsMixin.ForwardProperty",
        jsii_struct_bases=[],
        name_mapping={"target_groups": "targetGroups"},
    )
    class ForwardProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.WeightedTargetGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The forward action.

            Traffic that matches the rule is forwarded to the specified target groups.

            :param target_groups: The target groups. Traffic matching the rule is forwarded to the specified target groups. With forward actions, you can assign a weight that controls the prioritization and selection of each target group. This means that requests are distributed to individual target groups based on their weights. For example, if two target groups have the same weight, each target group receives half of the traffic. The default value is 1. This means that if only one target group is provided, there is no need to set the weight; 100% of the traffic goes to that target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-forward.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                forward_property = vpclattice_mixins.CfnListenerPropsMixin.ForwardProperty(
                    target_groups=[vpclattice_mixins.CfnListenerPropsMixin.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb30b71628a90366a46496321b42c01678a89a62943c3658b47a0e9e54e71ee6)
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_groups is not None:
                self._values["target_groups"] = target_groups

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.WeightedTargetGroupProperty"]]]]:
            '''The target groups.

            Traffic matching the rule is forwarded to the specified target groups. With forward actions, you can assign a weight that controls the prioritization and selection of each target group. This means that requests are distributed to individual target groups based on their weights. For example, if two target groups have the same weight, each target group receives half of the traffic.

            The default value is 1. This means that if only one target group is provided, there is no need to set the weight; 100% of the traffic goes to that target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-forward.html#cfn-vpclattice-listener-forward-targetgroups
            '''
            result = self._values.get("target_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.WeightedTargetGroupProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnListenerPropsMixin.WeightedTargetGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_group_identifier": "targetGroupIdentifier",
            "weight": "weight",
        },
    )
    class WeightedTargetGroupProperty:
        def __init__(
            self,
            *,
            target_group_identifier: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the weight of a target group.

            :param target_group_identifier: The ID of the target group.
            :param weight: Only required if you specify multiple target groups for a forward action. The weight determines how requests are distributed to the target group. For example, if you specify two target groups, each with a weight of 10, each target group receives half the requests. If you specify two target groups, one with a weight of 10 and the other with a weight of 20, the target group with a weight of 20 receives twice as many requests as the other target group. If there's only one target group specified, then the default value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-weightedtargetgroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                weighted_target_group_property = vpclattice_mixins.CfnListenerPropsMixin.WeightedTargetGroupProperty(
                    target_group_identifier="targetGroupIdentifier",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a1ef3d4cadb14a807a8d69f6783c2eafdd3b921ce4c6b71af93870c0f3e6590)
                check_type(argname="argument target_group_identifier", value=target_group_identifier, expected_type=type_hints["target_group_identifier"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_group_identifier is not None:
                self._values["target_group_identifier"] = target_group_identifier
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_identifier(self) -> typing.Optional[builtins.str]:
            '''The ID of the target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-weightedtargetgroup.html#cfn-vpclattice-listener-weightedtargetgroup-targetgroupidentifier
            '''
            result = self._values.get("target_group_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''Only required if you specify multiple target groups for a forward action.

            The weight determines how requests are distributed to the target group. For example, if you specify two target groups, each with a weight of 10, each target group receives half the requests. If you specify two target groups, one with a weight of 10 and the other with a weight of 20, the target group with a weight of 20 receives twice as many requests as the other target group. If there's only one target group specified, then the default value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-weightedtargetgroup.html#cfn-vpclattice-listener-weightedtargetgroup-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeightedTargetGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceConfigurationLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourceConfigurationLogsMixin",
):
    '''Creates a resource configuration.

    A resource configuration defines a specific resource. You can associate a resource configuration with a service network or a VPC endpoint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html
    :cloudformationResource: AWS::VpcLattice::ResourceConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_resource_configuration_logs_mixin = vpclattice_mixins.CfnResourceConfigurationLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::VpcLattice::ResourceConfiguration``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf692ae198356efde102dcc1479407fb4a9b7603189f45384dc6a93d773f572)
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
            type_hints = typing.get_type_hints(_typecheckingstub__254761cc919ffdcbc3319bdac9d3a03a04933e18c7c76d96c8b2253f2b7c2e77)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bad8c4b06a67e7c820a22d0a853b0190f471905ad0b9260ecdaa70648c6c7b2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RESOURCE_ACCESS_LOGS")
    def RESOURCE_ACCESS_LOGS(cls) -> "CfnResourceConfigurationResourceAccessLogs":
        return typing.cast("CfnResourceConfigurationResourceAccessLogs", jsii.sget(cls, "RESOURCE_ACCESS_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourceConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_association_to_sharable_service_network": "allowAssociationToSharableServiceNetwork",
        "custom_domain_name": "customDomainName",
        "domain_verification_id": "domainVerificationId",
        "group_domain": "groupDomain",
        "name": "name",
        "port_ranges": "portRanges",
        "protocol_type": "protocolType",
        "resource_configuration_auth_type": "resourceConfigurationAuthType",
        "resource_configuration_definition": "resourceConfigurationDefinition",
        "resource_configuration_group_id": "resourceConfigurationGroupId",
        "resource_configuration_type": "resourceConfigurationType",
        "resource_gateway_id": "resourceGatewayId",
        "tags": "tags",
    },
)
class CfnResourceConfigurationMixinProps:
    def __init__(
        self,
        *,
        allow_association_to_sharable_service_network: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        domain_verification_id: typing.Optional[builtins.str] = None,
        group_domain: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        protocol_type: typing.Optional[builtins.str] = None,
        resource_configuration_auth_type: typing.Optional[builtins.str] = None,
        resource_configuration_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceConfigurationPropsMixin.ResourceConfigurationDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_configuration_group_id: typing.Optional[builtins.str] = None,
        resource_configuration_type: typing.Optional[builtins.str] = None,
        resource_gateway_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnResourceConfigurationPropsMixin.

        :param allow_association_to_sharable_service_network: Specifies whether the resource configuration can be associated with a sharable service network.
        :param custom_domain_name: The custom domain name.
        :param domain_verification_id: The domain verification ID.
        :param group_domain: (GROUP) The group domain for a group resource configuration. Any domains that you create for the child resource are subdomains of the group domain. Child resources inherit the verification status of the domain.
        :param name: The name of the resource configuration.
        :param port_ranges: (SINGLE, GROUP, CHILD) The TCP port ranges that a consumer can use to access a resource configuration (for example: 1-65535). You can separate port ranges using commas (for example: 1,2,22-30).
        :param protocol_type: (SINGLE, GROUP) The protocol accepted by the resource configuration.
        :param resource_configuration_auth_type: The auth type for the resource configuration.
        :param resource_configuration_definition: Identifies the resource configuration in one of the following ways:. - *Amazon Resource Name (ARN)* - Supported resource-types that are provisioned by AWS services, such as RDS databases, can be identified by their ARN. - *Domain name* - Any domain name that is publicly resolvable. - *IP address* - For IPv4 and IPv6, only IP addresses in the VPC are supported.
        :param resource_configuration_group_id: The ID of the group resource configuration.
        :param resource_configuration_type: The type of resource configuration. A resource configuration can be one of the following types:. - *SINGLE* - A single resource. - *GROUP* - A group of resources. You must create a group resource configuration before you create a child resource configuration. - *CHILD* - A single resource that is part of a group resource configuration. - *ARN* - An AWS resource.
        :param resource_gateway_id: The ID of the resource gateway.
        :param tags: The tags for the resource configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_resource_configuration_mixin_props = vpclattice_mixins.CfnResourceConfigurationMixinProps(
                allow_association_to_sharable_service_network=False,
                custom_domain_name="customDomainName",
                domain_verification_id="domainVerificationId",
                group_domain="groupDomain",
                name="name",
                port_ranges=["portRanges"],
                protocol_type="protocolType",
                resource_configuration_auth_type="resourceConfigurationAuthType",
                resource_configuration_definition=vpclattice_mixins.CfnResourceConfigurationPropsMixin.ResourceConfigurationDefinitionProperty(
                    arn_resource="arnResource",
                    dns_resource=vpclattice_mixins.CfnResourceConfigurationPropsMixin.DnsResourceProperty(
                        domain_name="domainName",
                        ip_address_type="ipAddressType"
                    ),
                    ip_resource="ipResource"
                ),
                resource_configuration_group_id="resourceConfigurationGroupId",
                resource_configuration_type="resourceConfigurationType",
                resource_gateway_id="resourceGatewayId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7b4f9de9ffef31bd8d989021cfe1a54e72f78afc004a1dde95a0a75197c93b)
            check_type(argname="argument allow_association_to_sharable_service_network", value=allow_association_to_sharable_service_network, expected_type=type_hints["allow_association_to_sharable_service_network"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument domain_verification_id", value=domain_verification_id, expected_type=type_hints["domain_verification_id"])
            check_type(argname="argument group_domain", value=group_domain, expected_type=type_hints["group_domain"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port_ranges", value=port_ranges, expected_type=type_hints["port_ranges"])
            check_type(argname="argument protocol_type", value=protocol_type, expected_type=type_hints["protocol_type"])
            check_type(argname="argument resource_configuration_auth_type", value=resource_configuration_auth_type, expected_type=type_hints["resource_configuration_auth_type"])
            check_type(argname="argument resource_configuration_definition", value=resource_configuration_definition, expected_type=type_hints["resource_configuration_definition"])
            check_type(argname="argument resource_configuration_group_id", value=resource_configuration_group_id, expected_type=type_hints["resource_configuration_group_id"])
            check_type(argname="argument resource_configuration_type", value=resource_configuration_type, expected_type=type_hints["resource_configuration_type"])
            check_type(argname="argument resource_gateway_id", value=resource_gateway_id, expected_type=type_hints["resource_gateway_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_association_to_sharable_service_network is not None:
            self._values["allow_association_to_sharable_service_network"] = allow_association_to_sharable_service_network
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if domain_verification_id is not None:
            self._values["domain_verification_id"] = domain_verification_id
        if group_domain is not None:
            self._values["group_domain"] = group_domain
        if name is not None:
            self._values["name"] = name
        if port_ranges is not None:
            self._values["port_ranges"] = port_ranges
        if protocol_type is not None:
            self._values["protocol_type"] = protocol_type
        if resource_configuration_auth_type is not None:
            self._values["resource_configuration_auth_type"] = resource_configuration_auth_type
        if resource_configuration_definition is not None:
            self._values["resource_configuration_definition"] = resource_configuration_definition
        if resource_configuration_group_id is not None:
            self._values["resource_configuration_group_id"] = resource_configuration_group_id
        if resource_configuration_type is not None:
            self._values["resource_configuration_type"] = resource_configuration_type
        if resource_gateway_id is not None:
            self._values["resource_gateway_id"] = resource_gateway_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allow_association_to_sharable_service_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the resource configuration can be associated with a sharable service network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-allowassociationtosharableservicenetwork
        '''
        result = self._values.get("allow_association_to_sharable_service_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''The custom domain name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-customdomainname
        '''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_verification_id(self) -> typing.Optional[builtins.str]:
        '''The domain verification ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-domainverificationid
        '''
        result = self._values.get("domain_verification_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_domain(self) -> typing.Optional[builtins.str]:
        '''(GROUP) The group domain for a group resource configuration.

        Any domains that you create for the child resource are subdomains of the group domain. Child resources inherit the verification status of the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-groupdomain
        '''
        result = self._values.get("group_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(SINGLE, GROUP, CHILD) The TCP port ranges that a consumer can use to access a resource configuration (for example: 1-65535).

        You can separate port ranges using commas (for example: 1,2,22-30).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-portranges
        '''
        result = self._values.get("port_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def protocol_type(self) -> typing.Optional[builtins.str]:
        '''(SINGLE, GROUP) The protocol accepted by the resource configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-protocoltype
        '''
        result = self._values.get("protocol_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_configuration_auth_type(self) -> typing.Optional[builtins.str]:
        '''The auth type for the resource configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-resourceconfigurationauthtype
        '''
        result = self._values.get("resource_configuration_auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_configuration_definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceConfigurationPropsMixin.ResourceConfigurationDefinitionProperty"]]:
        '''Identifies the resource configuration in one of the following ways:.

        - *Amazon Resource Name (ARN)* - Supported resource-types that are provisioned by AWS services, such as RDS databases, can be identified by their ARN.
        - *Domain name* - Any domain name that is publicly resolvable.
        - *IP address* - For IPv4 and IPv6, only IP addresses in the VPC are supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-resourceconfigurationdefinition
        '''
        result = self._values.get("resource_configuration_definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceConfigurationPropsMixin.ResourceConfigurationDefinitionProperty"]], result)

    @builtins.property
    def resource_configuration_group_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the group resource configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-resourceconfigurationgroupid
        '''
        result = self._values.get("resource_configuration_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_configuration_type(self) -> typing.Optional[builtins.str]:
        '''The type of resource configuration. A resource configuration can be one of the following types:.

        - *SINGLE* - A single resource.
        - *GROUP* - A group of resources. You must create a group resource configuration before you create a child resource configuration.
        - *CHILD* - A single resource that is part of a group resource configuration.
        - *ARN* - An AWS resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-resourceconfigurationtype
        '''
        result = self._values.get("resource_configuration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_gateway_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the resource gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-resourcegatewayid
        '''
        result = self._values.get("resource_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the resource configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html#cfn-vpclattice-resourceconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourceConfigurationPropsMixin",
):
    '''Creates a resource configuration.

    A resource configuration defines a specific resource. You can associate a resource configuration with a service network or a VPC endpoint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourceconfiguration.html
    :cloudformationResource: AWS::VpcLattice::ResourceConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_resource_configuration_props_mixin = vpclattice_mixins.CfnResourceConfigurationPropsMixin(vpclattice_mixins.CfnResourceConfigurationMixinProps(
            allow_association_to_sharable_service_network=False,
            custom_domain_name="customDomainName",
            domain_verification_id="domainVerificationId",
            group_domain="groupDomain",
            name="name",
            port_ranges=["portRanges"],
            protocol_type="protocolType",
            resource_configuration_auth_type="resourceConfigurationAuthType",
            resource_configuration_definition=vpclattice_mixins.CfnResourceConfigurationPropsMixin.ResourceConfigurationDefinitionProperty(
                arn_resource="arnResource",
                dns_resource=vpclattice_mixins.CfnResourceConfigurationPropsMixin.DnsResourceProperty(
                    domain_name="domainName",
                    ip_address_type="ipAddressType"
                ),
                ip_resource="ipResource"
            ),
            resource_configuration_group_id="resourceConfigurationGroupId",
            resource_configuration_type="resourceConfigurationType",
            resource_gateway_id="resourceGatewayId",
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
        props: typing.Union[CfnResourceConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::ResourceConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c74739924c89c6b85dc8eb70f8b8b8fb7f5a662452e7cbc1b1c154d172952b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a960caa03a6c94f47ac5300cd93d4cf5401d41c12d52803e2e9a2339f556d507)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f1a5a724948c9c20123f2d283971a9b69f9ecfb49ae198c6075ff167e9c2be4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceConfigurationMixinProps:
        return typing.cast(CfnResourceConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourceConfigurationPropsMixin.DnsResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName", "ip_address_type": "ipAddressType"},
    )
    class DnsResourceProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            ip_address_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The domain name of the resource configuration.

            :param domain_name: The domain name of the resource configuration.
            :param ip_address_type: The IP address type for the resource configuration. Dualstack is not currently supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-resourceconfiguration-dnsresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                dns_resource_property = vpclattice_mixins.CfnResourceConfigurationPropsMixin.DnsResourceProperty(
                    domain_name="domainName",
                    ip_address_type="ipAddressType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f148788bdb7b3b202487ee636400fb76bfa2c51318f419f92c7168795ace1ca7)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The domain name of the resource configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-resourceconfiguration-dnsresource.html#cfn-vpclattice-resourceconfiguration-dnsresource-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''The IP address type for the resource configuration.

            Dualstack is not currently supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-resourceconfiguration-dnsresource.html#cfn-vpclattice-resourceconfiguration-dnsresource-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourceConfigurationPropsMixin.ResourceConfigurationDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn_resource": "arnResource",
            "dns_resource": "dnsResource",
            "ip_resource": "ipResource",
        },
    )
    class ResourceConfigurationDefinitionProperty:
        def __init__(
            self,
            *,
            arn_resource: typing.Optional[builtins.str] = None,
            dns_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnResourceConfigurationPropsMixin.DnsResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_resource: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies the resource configuration in one of the following ways:.

            - *Amazon Resource Name (ARN)* - Supported resource-types that are provisioned by AWS services, such as RDS databases, can be identified by their ARN.
            - *Domain name* - Any domain name that is publicly resolvable.
            - *IP address* - For IPv4 and IPv6, only IP addresses in the VPC are supported.

            :param arn_resource: The Amazon Resource Name (ARN) of the resource configuration. For the ARN syntax and format, see `ARN format <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html#arns-syntax>`_ in the *AWS Identity and Access Management user guide* .
            :param dns_resource: The DNS name of the resource configuration.
            :param ip_resource: The IP address of the resource configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-resourceconfiguration-resourceconfigurationdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                resource_configuration_definition_property = vpclattice_mixins.CfnResourceConfigurationPropsMixin.ResourceConfigurationDefinitionProperty(
                    arn_resource="arnResource",
                    dns_resource=vpclattice_mixins.CfnResourceConfigurationPropsMixin.DnsResourceProperty(
                        domain_name="domainName",
                        ip_address_type="ipAddressType"
                    ),
                    ip_resource="ipResource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e96179f4d47e2d8df2b023dc2f14b425148dc48471356407c61bb0ab0f88e9f)
                check_type(argname="argument arn_resource", value=arn_resource, expected_type=type_hints["arn_resource"])
                check_type(argname="argument dns_resource", value=dns_resource, expected_type=type_hints["dns_resource"])
                check_type(argname="argument ip_resource", value=ip_resource, expected_type=type_hints["ip_resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn_resource is not None:
                self._values["arn_resource"] = arn_resource
            if dns_resource is not None:
                self._values["dns_resource"] = dns_resource
            if ip_resource is not None:
                self._values["ip_resource"] = ip_resource

        @builtins.property
        def arn_resource(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the resource configuration.

            For the ARN syntax and format, see `ARN format <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html#arns-syntax>`_ in the *AWS Identity and Access Management user guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-resourceconfiguration-resourceconfigurationdefinition.html#cfn-vpclattice-resourceconfiguration-resourceconfigurationdefinition-arnresource
            '''
            result = self._values.get("arn_resource")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dns_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceConfigurationPropsMixin.DnsResourceProperty"]]:
            '''The DNS name of the resource configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-resourceconfiguration-resourceconfigurationdefinition.html#cfn-vpclattice-resourceconfiguration-resourceconfigurationdefinition-dnsresource
            '''
            result = self._values.get("dns_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnResourceConfigurationPropsMixin.DnsResourceProperty"]], result)

        @builtins.property
        def ip_resource(self) -> typing.Optional[builtins.str]:
            '''The IP address of the resource configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-resourceconfiguration-resourceconfigurationdefinition.html#cfn-vpclattice-resourceconfiguration-resourceconfigurationdefinition-ipresource
            '''
            result = self._values.get("ip_resource")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceConfigurationDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnResourceConfigurationResourceAccessLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourceConfigurationResourceAccessLogs",
):
    '''Builder for CfnResourceConfigurationLogsMixin to generate RESOURCE_ACCESS_LOGS for CfnResourceConfiguration.

    :cloudformationResource: AWS::VpcLattice::ResourceConfiguration
    :logType: RESOURCE_ACCESS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_resource_configuration_resource_access_logs = vpclattice_mixins.CfnResourceConfigurationResourceAccessLogs()
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
    ) -> CfnResourceConfigurationLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0468383b1b092d6afbf8ed80c82d0b204dba50e671ef4c3a66fda59cdbc0ca4a)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnResourceConfigurationLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnResourceConfigurationLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a2fbfdd658b0dc699e303dbfc31886b53478189e59adf59f1abe1c1be202aa)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnResourceConfigurationLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnResourceConfigurationLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a8067ac69dd9b14962cae87ebf1347cd25eaabb40dd86908fc47f0cdc9573a)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnResourceConfigurationLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourceGatewayMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ip_address_type": "ipAddressType",
        "ipv4_addresses_per_eni": "ipv4AddressesPerEni",
        "name": "name",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "vpc_identifier": "vpcIdentifier",
    },
)
class CfnResourceGatewayMixinProps:
    def __init__(
        self,
        *,
        ip_address_type: typing.Optional[builtins.str] = None,
        ipv4_addresses_per_eni: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourceGatewayPropsMixin.

        :param ip_address_type: The type of IP address used by the resource gateway.
        :param ipv4_addresses_per_eni: The number of IPv4 addresses in each ENI for the resource gateway.
        :param name: The name of the resource gateway.
        :param security_group_ids: The IDs of the security groups applied to the resource gateway.
        :param subnet_ids: The IDs of the VPC subnets for the resource gateway.
        :param tags: The tags for the resource gateway.
        :param vpc_identifier: The ID of the VPC for the resource gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcegateway.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_resource_gateway_mixin_props = vpclattice_mixins.CfnResourceGatewayMixinProps(
                ip_address_type="ipAddressType",
                ipv4_addresses_per_eni=123,
                name="name",
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_identifier="vpcIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740c7d75f00c8baa80b427a6e3035b67408a3d08dba7cc9bbff811d9f5bedab6)
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument ipv4_addresses_per_eni", value=ipv4_addresses_per_eni, expected_type=type_hints["ipv4_addresses_per_eni"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_identifier", value=vpc_identifier, expected_type=type_hints["vpc_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if ipv4_addresses_per_eni is not None:
            self._values["ipv4_addresses_per_eni"] = ipv4_addresses_per_eni
        if name is not None:
            self._values["name"] = name
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if vpc_identifier is not None:
            self._values["vpc_identifier"] = vpc_identifier

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''The type of IP address used by the resource gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcegateway.html#cfn-vpclattice-resourcegateway-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4_addresses_per_eni(self) -> typing.Optional[jsii.Number]:
        '''The number of IPv4 addresses in each ENI for the resource gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcegateway.html#cfn-vpclattice-resourcegateway-ipv4addressespereni
        '''
        result = self._values.get("ipv4_addresses_per_eni")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcegateway.html#cfn-vpclattice-resourcegateway-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the security groups applied to the resource gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcegateway.html#cfn-vpclattice-resourcegateway-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the VPC subnets for the resource gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcegateway.html#cfn-vpclattice-resourcegateway-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the resource gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcegateway.html#cfn-vpclattice-resourcegateway-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPC for the resource gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcegateway.html#cfn-vpclattice-resourcegateway-vpcidentifier
        '''
        result = self._values.get("vpc_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceGatewayMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceGatewayPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourceGatewayPropsMixin",
):
    '''A resource gateway is a point of ingress into the VPC where a resource resides.

    It spans multiple Availability Zones. For your resource to be accessible from all Availability Zones, you should create your resource gateways to span as many Availability Zones as possible. A VPC can have multiple resource gateways.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcegateway.html
    :cloudformationResource: AWS::VpcLattice::ResourceGateway
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_resource_gateway_props_mixin = vpclattice_mixins.CfnResourceGatewayPropsMixin(vpclattice_mixins.CfnResourceGatewayMixinProps(
            ip_address_type="ipAddressType",
            ipv4_addresses_per_eni=123,
            name="name",
            security_group_ids=["securityGroupIds"],
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_identifier="vpcIdentifier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::ResourceGateway``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d94e924413bc94a0f83a88f7a3794e04e1f6b52abd77155185a1443bdc0d97e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6565c3446668181a5f6ff7f8aabc274bfe700c29e680c4372de472b6fec82ec8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c776223f252c37f9a2975fd4991e1ac058a29c34e925f0d79c99ca0a77f67c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceGatewayMixinProps:
        return typing.cast(CfnResourceGatewayMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_arn": "resourceArn"},
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        policy: typing.Any = None,
        resource_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param policy: The Amazon Resource Name (ARN) of the service network or service.
        :param resource_arn: An IAM policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            # policy: Any
            
            cfn_resource_policy_mixin_props = vpclattice_mixins.CfnResourcePolicyMixinProps(
                policy=policy,
                resource_arn="resourceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ec25d8f9b0e0f6d4c5d48afa35864541bd4781cba8b9662438f47314524e01)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn

    @builtins.property
    def policy(self) -> typing.Any:
        '''The Amazon Resource Name (ARN) of the service network or service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''An IAM policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-resourcearn
        '''
        result = self._values.get("resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnResourcePolicyPropsMixin",
):
    '''Retrieves information about the specified resource policy.

    The resource policy is an IAM policy created on behalf of the resource owner when they share a resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html
    :cloudformationResource: AWS::VpcLattice::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        # policy: Any
        
        cfn_resource_policy_props_mixin = vpclattice_mixins.CfnResourcePolicyPropsMixin(vpclattice_mixins.CfnResourcePolicyMixinProps(
            policy=policy,
            resource_arn="resourceArn"
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
        '''Create a mixin to apply properties to ``AWS::VpcLattice::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b19400862255a39c09ea99e54729ca473ac50ae3c3f63caa61d6775b90cda3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca8d7e12ca2fdffe3eecb9cc053074c4832d88ef4801535e29f55e2877ff632e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d0b9530e95c5576d498262b203351046db8252411390652369106ff8572940)
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


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "listener_identifier": "listenerIdentifier",
        "match": "match",
        "name": "name",
        "priority": "priority",
        "service_identifier": "serviceIdentifier",
        "tags": "tags",
    },
)
class CfnRuleMixinProps:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        listener_identifier: typing.Optional[builtins.str] = None,
        match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.MatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRulePropsMixin.

        :param action: Describes the action for a rule.
        :param listener_identifier: The ID or ARN of the listener.
        :param match: The rule match.
        :param name: The name of the rule. The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param priority: The priority assigned to the rule. Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.
        :param service_identifier: The ID or ARN of the service.
        :param tags: The tags for the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_rule_mixin_props = vpclattice_mixins.CfnRuleMixinProps(
                action=vpclattice_mixins.CfnRulePropsMixin.ActionProperty(
                    fixed_response=vpclattice_mixins.CfnRulePropsMixin.FixedResponseProperty(
                        status_code=123
                    ),
                    forward=vpclattice_mixins.CfnRulePropsMixin.ForwardProperty(
                        target_groups=[vpclattice_mixins.CfnRulePropsMixin.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
                            weight=123
                        )]
                    )
                ),
                listener_identifier="listenerIdentifier",
                match=vpclattice_mixins.CfnRulePropsMixin.MatchProperty(
                    http_match=vpclattice_mixins.CfnRulePropsMixin.HttpMatchProperty(
                        header_matches=[vpclattice_mixins.CfnRulePropsMixin.HeaderMatchProperty(
                            case_sensitive=False,
                            match=vpclattice_mixins.CfnRulePropsMixin.HeaderMatchTypeProperty(
                                contains="contains",
                                exact="exact",
                                prefix="prefix"
                            ),
                            name="name"
                        )],
                        method="method",
                        path_match=vpclattice_mixins.CfnRulePropsMixin.PathMatchProperty(
                            case_sensitive=False,
                            match=vpclattice_mixins.CfnRulePropsMixin.PathMatchTypeProperty(
                                exact="exact",
                                prefix="prefix"
                            )
                        )
                    )
                ),
                name="name",
                priority=123,
                service_identifier="serviceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921458faafcacb158b2229ec1ba51076f6a37c5c53fbae1f405a86af382ba86a)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument listener_identifier", value=listener_identifier, expected_type=type_hints["listener_identifier"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if listener_identifier is not None:
            self._values["listener_identifier"] = listener_identifier
        if match is not None:
            self._values["match"] = match
        if name is not None:
            self._values["name"] = name
        if priority is not None:
            self._values["priority"] = priority
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def action(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ActionProperty"]]:
        '''Describes the action for a rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ActionProperty"]], result)

    @builtins.property
    def listener_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or ARN of the listener.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-listeneridentifier
        '''
        result = self._values.get("listener_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.MatchProperty"]]:
        '''The rule match.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-match
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.MatchProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule.

        The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority assigned to the rule.

        Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or ARN of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin",
):
    '''Creates a listener rule.

    Each listener has a default rule for checking connection requests, but you can define additional rules. Each rule consists of a priority, one or more actions, and one or more conditions. For more information, see `Listener rules <https://docs.aws.amazon.com/vpc-lattice/latest/ug/listeners.html#listener-rules>`_ in the *Amazon VPC Lattice User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html
    :cloudformationResource: AWS::VpcLattice::Rule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_rule_props_mixin = vpclattice_mixins.CfnRulePropsMixin(vpclattice_mixins.CfnRuleMixinProps(
            action=vpclattice_mixins.CfnRulePropsMixin.ActionProperty(
                fixed_response=vpclattice_mixins.CfnRulePropsMixin.FixedResponseProperty(
                    status_code=123
                ),
                forward=vpclattice_mixins.CfnRulePropsMixin.ForwardProperty(
                    target_groups=[vpclattice_mixins.CfnRulePropsMixin.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
                        weight=123
                    )]
                )
            ),
            listener_identifier="listenerIdentifier",
            match=vpclattice_mixins.CfnRulePropsMixin.MatchProperty(
                http_match=vpclattice_mixins.CfnRulePropsMixin.HttpMatchProperty(
                    header_matches=[vpclattice_mixins.CfnRulePropsMixin.HeaderMatchProperty(
                        case_sensitive=False,
                        match=vpclattice_mixins.CfnRulePropsMixin.HeaderMatchTypeProperty(
                            contains="contains",
                            exact="exact",
                            prefix="prefix"
                        ),
                        name="name"
                    )],
                    method="method",
                    path_match=vpclattice_mixins.CfnRulePropsMixin.PathMatchProperty(
                        case_sensitive=False,
                        match=vpclattice_mixins.CfnRulePropsMixin.PathMatchTypeProperty(
                            exact="exact",
                            prefix="prefix"
                        )
                    )
                )
            ),
            name="name",
            priority=123,
            service_identifier="serviceIdentifier",
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
        props: typing.Union[CfnRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::Rule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a7e81220c754b88620e05ead6469413754639ffb1e5f9cb987925065e1652bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f9d3186e21b1f7b960447638ba1586650af08e329fe15d196b9c6b178eabb24)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161b0d12ccaac85822f3e485fe6760a77d711d8fbb12db1825910d033d596773)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRuleMixinProps:
        return typing.cast(CfnRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"fixed_response": "fixedResponse", "forward": "forward"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            fixed_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.FixedResponseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            forward: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.ForwardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the action for a rule.

            :param fixed_response: The fixed response action. The rule returns a custom HTTP response.
            :param forward: The forward action. Traffic that matches the rule is forwarded to the specified target groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                action_property = vpclattice_mixins.CfnRulePropsMixin.ActionProperty(
                    fixed_response=vpclattice_mixins.CfnRulePropsMixin.FixedResponseProperty(
                        status_code=123
                    ),
                    forward=vpclattice_mixins.CfnRulePropsMixin.ForwardProperty(
                        target_groups=[vpclattice_mixins.CfnRulePropsMixin.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
                            weight=123
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75bc328d5fce5ce70358c3d6abe462c7c6c28026f0bed91e477747b3be265460)
                check_type(argname="argument fixed_response", value=fixed_response, expected_type=type_hints["fixed_response"])
                check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fixed_response is not None:
                self._values["fixed_response"] = fixed_response
            if forward is not None:
                self._values["forward"] = forward

        @builtins.property
        def fixed_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.FixedResponseProperty"]]:
            '''The fixed response action.

            The rule returns a custom HTTP response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-action.html#cfn-vpclattice-rule-action-fixedresponse
            '''
            result = self._values.get("fixed_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.FixedResponseProperty"]], result)

        @builtins.property
        def forward(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ForwardProperty"]]:
            '''The forward action.

            Traffic that matches the rule is forwarded to the specified target groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-action.html#cfn-vpclattice-rule-action-forward
            '''
            result = self._values.get("forward")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ForwardProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.FixedResponseProperty",
        jsii_struct_bases=[],
        name_mapping={"status_code": "statusCode"},
    )
    class FixedResponseProperty:
        def __init__(self, *, status_code: typing.Optional[jsii.Number] = None) -> None:
            '''Describes an action that returns a custom HTTP response.

            :param status_code: The HTTP response code. Only ``404`` and ``500`` status codes are supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-fixedresponse.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                fixed_response_property = vpclattice_mixins.CfnRulePropsMixin.FixedResponseProperty(
                    status_code=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__329958e08bfeee95d553e8c3f755bdf7436abe53262da7031739827692a68cd7)
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status_code is not None:
                self._values["status_code"] = status_code

        @builtins.property
        def status_code(self) -> typing.Optional[jsii.Number]:
            '''The HTTP response code.

            Only ``404`` and ``500`` status codes are supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-fixedresponse.html#cfn-vpclattice-rule-fixedresponse-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.ForwardProperty",
        jsii_struct_bases=[],
        name_mapping={"target_groups": "targetGroups"},
    )
    class ForwardProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.WeightedTargetGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The forward action.

            Traffic that matches the rule is forwarded to the specified target groups.

            :param target_groups: The target groups. Traffic matching the rule is forwarded to the specified target groups. With forward actions, you can assign a weight that controls the prioritization and selection of each target group. This means that requests are distributed to individual target groups based on their weights. For example, if two target groups have the same weight, each target group receives half of the traffic. The default value is 1. This means that if only one target group is provided, there is no need to set the weight; 100% of the traffic goes to that target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-forward.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                forward_property = vpclattice_mixins.CfnRulePropsMixin.ForwardProperty(
                    target_groups=[vpclattice_mixins.CfnRulePropsMixin.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16702d7ca2d7afbc1bc141129efcd5be691247424728556d6867d44597152c4d)
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_groups is not None:
                self._values["target_groups"] = target_groups

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.WeightedTargetGroupProperty"]]]]:
            '''The target groups.

            Traffic matching the rule is forwarded to the specified target groups. With forward actions, you can assign a weight that controls the prioritization and selection of each target group. This means that requests are distributed to individual target groups based on their weights. For example, if two target groups have the same weight, each target group receives half of the traffic.

            The default value is 1. This means that if only one target group is provided, there is no need to set the weight; 100% of the traffic goes to that target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-forward.html#cfn-vpclattice-rule-forward-targetgroups
            '''
            result = self._values.get("target_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.WeightedTargetGroupProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.HeaderMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "case_sensitive": "caseSensitive",
            "match": "match",
            "name": "name",
        },
    )
    class HeaderMatchProperty:
        def __init__(
            self,
            *,
            case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.HeaderMatchTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the constraints for a header match.

            Matches incoming requests with rule based on request header value before applying rule action.

            :param case_sensitive: Indicates whether the match is case sensitive. Default: - false
            :param match: The header match type.
            :param name: The name of the header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                header_match_property = vpclattice_mixins.CfnRulePropsMixin.HeaderMatchProperty(
                    case_sensitive=False,
                    match=vpclattice_mixins.CfnRulePropsMixin.HeaderMatchTypeProperty(
                        contains="contains",
                        exact="exact",
                        prefix="prefix"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__283684fb1e2017674bf9471a7d0cf0237fd6b0052063d253f1db24960d374f8b)
                check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if case_sensitive is not None:
                self._values["case_sensitive"] = case_sensitive
            if match is not None:
                self._values["match"] = match
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def case_sensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the match is case sensitive.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html#cfn-vpclattice-rule-headermatch-casesensitive
            '''
            result = self._values.get("case_sensitive")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.HeaderMatchTypeProperty"]]:
            '''The header match type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html#cfn-vpclattice-rule-headermatch-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.HeaderMatchTypeProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html#cfn-vpclattice-rule-headermatch-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.HeaderMatchTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"contains": "contains", "exact": "exact", "prefix": "prefix"},
    )
    class HeaderMatchTypeProperty:
        def __init__(
            self,
            *,
            contains: typing.Optional[builtins.str] = None,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a header match type.

            :param contains: A contains type match.
            :param exact: An exact type match.
            :param prefix: A prefix type match. Matches the value with the prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                header_match_type_property = vpclattice_mixins.CfnRulePropsMixin.HeaderMatchTypeProperty(
                    contains="contains",
                    exact="exact",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__472599b164493e7af0e29c8ac973e63dd1cb759e95adcb682c82f258bac5060f)
                check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contains is not None:
                self._values["contains"] = contains
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def contains(self) -> typing.Optional[builtins.str]:
            '''A contains type match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html#cfn-vpclattice-rule-headermatchtype-contains
            '''
            result = self._values.get("contains")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''An exact type match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html#cfn-vpclattice-rule-headermatchtype-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''A prefix type match.

            Matches the value with the prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html#cfn-vpclattice-rule-headermatchtype-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderMatchTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.HttpMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "header_matches": "headerMatches",
            "method": "method",
            "path_match": "pathMatch",
        },
    )
    class HttpMatchProperty:
        def __init__(
            self,
            *,
            header_matches: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.HeaderMatchProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            method: typing.Optional[builtins.str] = None,
            path_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.PathMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes criteria that can be applied to incoming requests.

            :param header_matches: The header matches. Matches incoming requests with rule based on request header value before applying rule action.
            :param method: The HTTP method type.
            :param path_match: The path match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                http_match_property = vpclattice_mixins.CfnRulePropsMixin.HttpMatchProperty(
                    header_matches=[vpclattice_mixins.CfnRulePropsMixin.HeaderMatchProperty(
                        case_sensitive=False,
                        match=vpclattice_mixins.CfnRulePropsMixin.HeaderMatchTypeProperty(
                            contains="contains",
                            exact="exact",
                            prefix="prefix"
                        ),
                        name="name"
                    )],
                    method="method",
                    path_match=vpclattice_mixins.CfnRulePropsMixin.PathMatchProperty(
                        case_sensitive=False,
                        match=vpclattice_mixins.CfnRulePropsMixin.PathMatchTypeProperty(
                            exact="exact",
                            prefix="prefix"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93ac5195436605f7b191517808e619c161ec73681de6c32deb226fce4a6ba99d)
                check_type(argname="argument header_matches", value=header_matches, expected_type=type_hints["header_matches"])
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path_match", value=path_match, expected_type=type_hints["path_match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_matches is not None:
                self._values["header_matches"] = header_matches
            if method is not None:
                self._values["method"] = method
            if path_match is not None:
                self._values["path_match"] = path_match

        @builtins.property
        def header_matches(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.HeaderMatchProperty"]]]]:
            '''The header matches.

            Matches incoming requests with rule based on request header value before applying rule action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html#cfn-vpclattice-rule-httpmatch-headermatches
            '''
            result = self._values.get("header_matches")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.HeaderMatchProperty"]]]], result)

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''The HTTP method type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html#cfn-vpclattice-rule-httpmatch-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path_match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.PathMatchProperty"]]:
            '''The path match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html#cfn-vpclattice-rule-httpmatch-pathmatch
            '''
            result = self._values.get("path_match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.PathMatchProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.MatchProperty",
        jsii_struct_bases=[],
        name_mapping={"http_match": "httpMatch"},
    )
    class MatchProperty:
        def __init__(
            self,
            *,
            http_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.HttpMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a rule match.

            :param http_match: The HTTP criteria that a rule must match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-match.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                match_property = vpclattice_mixins.CfnRulePropsMixin.MatchProperty(
                    http_match=vpclattice_mixins.CfnRulePropsMixin.HttpMatchProperty(
                        header_matches=[vpclattice_mixins.CfnRulePropsMixin.HeaderMatchProperty(
                            case_sensitive=False,
                            match=vpclattice_mixins.CfnRulePropsMixin.HeaderMatchTypeProperty(
                                contains="contains",
                                exact="exact",
                                prefix="prefix"
                            ),
                            name="name"
                        )],
                        method="method",
                        path_match=vpclattice_mixins.CfnRulePropsMixin.PathMatchProperty(
                            case_sensitive=False,
                            match=vpclattice_mixins.CfnRulePropsMixin.PathMatchTypeProperty(
                                exact="exact",
                                prefix="prefix"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5f16d7f452b405594ba99230f0cc6348ced34c9816be75f5952f0ce2d17ec4b)
                check_type(argname="argument http_match", value=http_match, expected_type=type_hints["http_match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http_match is not None:
                self._values["http_match"] = http_match

        @builtins.property
        def http_match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.HttpMatchProperty"]]:
            '''The HTTP criteria that a rule must match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-match.html#cfn-vpclattice-rule-match-httpmatch
            '''
            result = self._values.get("http_match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.HttpMatchProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.PathMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"case_sensitive": "caseSensitive", "match": "match"},
    )
    class PathMatchProperty:
        def __init__(
            self,
            *,
            case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.PathMatchTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the conditions that can be applied when matching a path for incoming requests.

            :param case_sensitive: Indicates whether the match is case sensitive. Default: - false
            :param match: The type of path match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                path_match_property = vpclattice_mixins.CfnRulePropsMixin.PathMatchProperty(
                    case_sensitive=False,
                    match=vpclattice_mixins.CfnRulePropsMixin.PathMatchTypeProperty(
                        exact="exact",
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__424b4ba0e9ec9ec0075558858b16d73f22acf53b260b9a8eece722a2683f73d4)
                check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if case_sensitive is not None:
                self._values["case_sensitive"] = case_sensitive
            if match is not None:
                self._values["match"] = match

        @builtins.property
        def case_sensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the match is case sensitive.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatch.html#cfn-vpclattice-rule-pathmatch-casesensitive
            '''
            result = self._values.get("case_sensitive")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.PathMatchTypeProperty"]]:
            '''The type of path match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatch.html#cfn-vpclattice-rule-pathmatch-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.PathMatchTypeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.PathMatchTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact", "prefix": "prefix"},
    )
    class PathMatchTypeProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a path match type.

            Each rule can include only one of the following types of paths.

            :param exact: An exact match of the path.
            :param prefix: A prefix match of the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatchtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                path_match_type_property = vpclattice_mixins.CfnRulePropsMixin.PathMatchTypeProperty(
                    exact="exact",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f4ddb7aec3752ed4b7ec97bd6152d5fd03f1a1f72638b97d90d4e15ea3225fa)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''An exact match of the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatchtype.html#cfn-vpclattice-rule-pathmatchtype-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''A prefix match of the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatchtype.html#cfn-vpclattice-rule-pathmatchtype-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathMatchTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnRulePropsMixin.WeightedTargetGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_group_identifier": "targetGroupIdentifier",
            "weight": "weight",
        },
    )
    class WeightedTargetGroupProperty:
        def __init__(
            self,
            *,
            target_group_identifier: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the weight of a target group.

            :param target_group_identifier: The ID of the target group.
            :param weight: Only required if you specify multiple target groups for a forward action. The weight determines how requests are distributed to the target group. For example, if you specify two target groups, each with a weight of 10, each target group receives half the requests. If you specify two target groups, one with a weight of 10 and the other with a weight of 20, the target group with a weight of 20 receives twice as many requests as the other target group. If there's only one target group specified, then the default value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-weightedtargetgroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                weighted_target_group_property = vpclattice_mixins.CfnRulePropsMixin.WeightedTargetGroupProperty(
                    target_group_identifier="targetGroupIdentifier",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ffd7245b2f24e9f8d38346b0c5a577905c8dba92ead7659e1aacdc57cda31795)
                check_type(argname="argument target_group_identifier", value=target_group_identifier, expected_type=type_hints["target_group_identifier"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_group_identifier is not None:
                self._values["target_group_identifier"] = target_group_identifier
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_identifier(self) -> typing.Optional[builtins.str]:
            '''The ID of the target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-weightedtargetgroup.html#cfn-vpclattice-rule-weightedtargetgroup-targetgroupidentifier
            '''
            result = self._values.get("target_group_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''Only required if you specify multiple target groups for a forward action.

            The weight determines how requests are distributed to the target group. For example, if you specify two target groups, each with a weight of 10, each target group receives half the requests. If you specify two target groups, one with a weight of 10 and the other with a weight of 20, the target group with a weight of 20 receives twice as many requests as the other target group. If there's only one target group specified, then the default value is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-weightedtargetgroup.html#cfn-vpclattice-rule-weightedtargetgroup-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeightedTargetGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnServiceAccessLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceAccessLogs",
):
    '''Builder for CfnServiceLogsMixin to generate ACCESS_LOGS for CfnService.

    :cloudformationResource: AWS::VpcLattice::Service
    :logType: ACCESS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_service_access_logs = vpclattice_mixins.CfnServiceAccessLogs()
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
    ) -> "CfnServiceLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f24bef0310e78e6bc9afd718e7c1b87dd76ffcfef8fe4b1e33f9bab6ac2427e)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnServiceLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnServiceLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2d3866865e111d61a11b5ec70292d8121bcb7a817985bf0c4a33ebcfe02486)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnServiceLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnServiceLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb29b532c6cc094e697a80e978e5462c3a4c081e4f3403e739b92de5eef97c1)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnServiceLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnServiceLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceLogsMixin",
):
    '''Creates a service.

    A service is any software application that can run on instances containers, or serverless functions within an account or virtual private cloud (VPC).

    For more information, see `Services <https://docs.aws.amazon.com/vpc-lattice/latest/ug/services.html>`_ in the *Amazon VPC Lattice User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html
    :cloudformationResource: AWS::VpcLattice::Service
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_service_logs_mixin = vpclattice_mixins.CfnServiceLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::VpcLattice::Service``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a307cfd341317cb2049d64334601f6c0551285b2200830e003f645f52e76be8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9bc90ce1bdd13d53c0c4f879d3085cda6d6eada37ac5d9a800126ee1ccd82d7)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367caec71d9e9cffa20dadd005b1837bb3447594e7aae83a778f5c31d5e295bd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCESS_LOGS")
    def ACCESS_LOGS(cls) -> CfnServiceAccessLogs:
        return typing.cast(CfnServiceAccessLogs, jsii.sget(cls, "ACCESS_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "certificate_arn": "certificateArn",
        "custom_domain_name": "customDomainName",
        "dns_entry": "dnsEntry",
        "name": "name",
        "tags": "tags",
    },
)
class CfnServiceMixinProps:
    def __init__(
        self,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        certificate_arn: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        dns_entry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServicePropsMixin.DnsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServicePropsMixin.

        :param auth_type: The type of IAM policy. - ``NONE`` : The resource does not use an IAM policy. This is the default. - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required. Default: - "NONE"
        :param certificate_arn: The Amazon Resource Name (ARN) of the certificate.
        :param custom_domain_name: The custom domain name of the service.
        :param dns_entry: Describes the DNS information of the service. This field is read-only.
        :param name: The name of the service. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param tags: The tags for the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_service_mixin_props = vpclattice_mixins.CfnServiceMixinProps(
                auth_type="authType",
                certificate_arn="certificateArn",
                custom_domain_name="customDomainName",
                dns_entry=vpclattice_mixins.CfnServicePropsMixin.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04ec87cc8751141399746a73ba226ce5900cd2da1b707f3df78b1a814dafed6)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument dns_entry", value=dns_entry, expected_type=type_hints["dns_entry"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if dns_entry is not None:
            self._values["dns_entry"] = dns_entry
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''The type of IAM policy.

        - ``NONE`` : The resource does not use an IAM policy. This is the default.
        - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.

        :default: - "NONE"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-authtype
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-certificatearn
        '''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''The custom domain name of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-customdomainname
        '''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.DnsEntryProperty"]]:
        '''Describes the DNS information of the service.

        This field is read-only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-dnsentry
        '''
        result = self._values.get("dns_entry")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServicePropsMixin.DnsEntryProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "name": "name",
        "sharing_config": "sharingConfig",
        "tags": "tags",
    },
)
class CfnServiceNetworkMixinProps:
    def __init__(
        self,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        sharing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceNetworkPropsMixin.SharingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServiceNetworkPropsMixin.

        :param auth_type: The type of IAM policy. - ``NONE`` : The resource does not use an IAM policy. This is the default. - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required. Default: - "NONE"
        :param name: The name of the service network. The name must be unique to the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param sharing_config: Specify if the service network should be enabled for sharing.
        :param tags: The tags for the service network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_service_network_mixin_props = vpclattice_mixins.CfnServiceNetworkMixinProps(
                auth_type="authType",
                name="name",
                sharing_config=vpclattice_mixins.CfnServiceNetworkPropsMixin.SharingConfigProperty(
                    enabled=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f651e3fdad38e52e0e57766ba91558ae972bcda101e14580e81df122902252b1)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sharing_config", value=sharing_config, expected_type=type_hints["sharing_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if name is not None:
            self._values["name"] = name
        if sharing_config is not None:
            self._values["sharing_config"] = sharing_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''The type of IAM policy.

        - ``NONE`` : The resource does not use an IAM policy. This is the default.
        - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.

        :default: - "NONE"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-authtype
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service network.

        The name must be unique to the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sharing_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceNetworkPropsMixin.SharingConfigProperty"]]:
        '''Specify if the service network should be enabled for sharing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-sharingconfig
        '''
        result = self._values.get("sharing_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceNetworkPropsMixin.SharingConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the service network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceNetworkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkPropsMixin",
):
    '''Creates a service network.

    A service network is a logical boundary for a collection of services. You can associate services and VPCs with a service network.

    For more information, see `Service networks <https://docs.aws.amazon.com/vpc-lattice/latest/ug/service-networks.html>`_ in the *Amazon VPC Lattice User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html
    :cloudformationResource: AWS::VpcLattice::ServiceNetwork
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_service_network_props_mixin = vpclattice_mixins.CfnServiceNetworkPropsMixin(vpclattice_mixins.CfnServiceNetworkMixinProps(
            auth_type="authType",
            name="name",
            sharing_config=vpclattice_mixins.CfnServiceNetworkPropsMixin.SharingConfigProperty(
                enabled=False
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
        props: typing.Union[CfnServiceNetworkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::ServiceNetwork``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c97ba60b541e5b79ea1b236ba1fa9f6b693ba24c281766f560e4c9a381c921)
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
            type_hints = typing.get_type_hints(_typecheckingstub__465a21059ca410047be05fa65dba09acc89412e18d299bad05863580dbf823e0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d223bc08aa2064db3d92a11931629ed011bf9217ec752446fc30583cdfec7f5b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceNetworkMixinProps:
        return typing.cast(CfnServiceNetworkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkPropsMixin.SharingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class SharingConfigProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specify if the service network should be enabled for sharing.

            :param enabled: Specify if the service network should be enabled for sharing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetwork-sharingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                sharing_config_property = vpclattice_mixins.CfnServiceNetworkPropsMixin.SharingConfigProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f7158550f94f317a2ca5df4a0b6329fe8e84f29fff97cd5668856d2f415fcc4)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify if the service network should be enabled for sharing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetwork-sharingconfig.html#cfn-vpclattice-servicenetwork-sharingconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SharingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkResourceAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "private_dns_enabled": "privateDnsEnabled",
        "resource_configuration_id": "resourceConfigurationId",
        "service_network_id": "serviceNetworkId",
        "tags": "tags",
    },
)
class CfnServiceNetworkResourceAssociationMixinProps:
    def __init__(
        self,
        *,
        private_dns_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        resource_configuration_id: typing.Optional[builtins.str] = None,
        service_network_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServiceNetworkResourceAssociationPropsMixin.

        :param private_dns_enabled: Indicates if private DNS is enabled for the service network resource association.
        :param resource_configuration_id: The ID of the resource configuration associated with the service network.
        :param service_network_id: The ID of the service network associated with the resource configuration.
        :param tags: A key-value pair to associate with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkresourceassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_service_network_resource_association_mixin_props = vpclattice_mixins.CfnServiceNetworkResourceAssociationMixinProps(
                private_dns_enabled=False,
                resource_configuration_id="resourceConfigurationId",
                service_network_id="serviceNetworkId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6f6f8bebb42f68e89477ee4ee6af9b2535a17a5d1380cce40786ad38af6ed4)
            check_type(argname="argument private_dns_enabled", value=private_dns_enabled, expected_type=type_hints["private_dns_enabled"])
            check_type(argname="argument resource_configuration_id", value=resource_configuration_id, expected_type=type_hints["resource_configuration_id"])
            check_type(argname="argument service_network_id", value=service_network_id, expected_type=type_hints["service_network_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if private_dns_enabled is not None:
            self._values["private_dns_enabled"] = private_dns_enabled
        if resource_configuration_id is not None:
            self._values["resource_configuration_id"] = resource_configuration_id
        if service_network_id is not None:
            self._values["service_network_id"] = service_network_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def private_dns_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates if private DNS is enabled for the service network resource association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkresourceassociation.html#cfn-vpclattice-servicenetworkresourceassociation-privatednsenabled
        '''
        result = self._values.get("private_dns_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def resource_configuration_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the resource configuration associated with the service network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkresourceassociation.html#cfn-vpclattice-servicenetworkresourceassociation-resourceconfigurationid
        '''
        result = self._values.get("resource_configuration_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the service network associated with the resource configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkresourceassociation.html#cfn-vpclattice-servicenetworkresourceassociation-servicenetworkid
        '''
        result = self._values.get("service_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A key-value pair to associate with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkresourceassociation.html#cfn-vpclattice-servicenetworkresourceassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkResourceAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceNetworkResourceAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkResourceAssociationPropsMixin",
):
    '''Associates the specified service network with the specified resource configuration.

    This allows the resource configuration to receive connections through the service network, including through a service network VPC endpoint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkresourceassociation.html
    :cloudformationResource: AWS::VpcLattice::ServiceNetworkResourceAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_service_network_resource_association_props_mixin = vpclattice_mixins.CfnServiceNetworkResourceAssociationPropsMixin(vpclattice_mixins.CfnServiceNetworkResourceAssociationMixinProps(
            private_dns_enabled=False,
            resource_configuration_id="resourceConfigurationId",
            service_network_id="serviceNetworkId",
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
        props: typing.Union[CfnServiceNetworkResourceAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::ServiceNetworkResourceAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb105cccc9deff25420a09674c50f189ca0370b4b2463c70732d594d5e00629f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d04694a1c7f930a5f96bbef0179fab507650fb19c2b46fb0ed2a4863baaaaad1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe938c07f3b2e6ae0451eda0d0fd90cf37194c2fd6f426926ef77a52b805695d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceNetworkResourceAssociationMixinProps:
        return typing.cast(CfnServiceNetworkResourceAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkServiceAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dns_entry": "dnsEntry",
        "service_identifier": "serviceIdentifier",
        "service_network_identifier": "serviceNetworkIdentifier",
        "tags": "tags",
    },
)
class CfnServiceNetworkServiceAssociationMixinProps:
    def __init__(
        self,
        *,
        dns_entry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceNetworkServiceAssociationPropsMixin.DnsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServiceNetworkServiceAssociationPropsMixin.

        :param dns_entry: The DNS information of the service.
        :param service_identifier: The ID or ARN of the service.
        :param service_network_identifier: The ID or ARN of the service network. You must use an ARN if the resources are in different accounts.
        :param tags: The tags for the association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_service_network_service_association_mixin_props = vpclattice_mixins.CfnServiceNetworkServiceAssociationMixinProps(
                dns_entry=vpclattice_mixins.CfnServiceNetworkServiceAssociationPropsMixin.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                ),
                service_identifier="serviceIdentifier",
                service_network_identifier="serviceNetworkIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd111c29effa59d64519462ceefa9ef8296f77ae1fb9d259c70b05fe76c1db34)
            check_type(argname="argument dns_entry", value=dns_entry, expected_type=type_hints["dns_entry"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument service_network_identifier", value=service_network_identifier, expected_type=type_hints["service_network_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_entry is not None:
            self._values["dns_entry"] = dns_entry
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if service_network_identifier is not None:
            self._values["service_network_identifier"] = service_network_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceNetworkServiceAssociationPropsMixin.DnsEntryProperty"]]:
        '''The DNS information of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry
        '''
        result = self._values.get("dns_entry")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceNetworkServiceAssociationPropsMixin.DnsEntryProperty"]], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or ARN of the service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or ARN of the service network.

        You must use an ARN if the resources are in different accounts.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-servicenetworkidentifier
        '''
        result = self._values.get("service_network_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkServiceAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceNetworkServiceAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkServiceAssociationPropsMixin",
):
    '''Associates the specified service with the specified service network.

    For more information, see `Manage service associations <https://docs.aws.amazon.com/vpc-lattice/latest/ug/service-network-associations.html#service-network-service-associations>`_ in the *Amazon VPC Lattice User Guide* .

    You can't use this operation if the service and service network are already associated or if there is a disassociation or deletion in progress. If the association fails, you can retry the operation by deleting the association and recreating it.

    You cannot associate a service and service network that are shared with a caller. The caller must own either the service or the service network.

    As a result of this operation, the association is created in the service network account and the association owner account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html
    :cloudformationResource: AWS::VpcLattice::ServiceNetworkServiceAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_service_network_service_association_props_mixin = vpclattice_mixins.CfnServiceNetworkServiceAssociationPropsMixin(vpclattice_mixins.CfnServiceNetworkServiceAssociationMixinProps(
            dns_entry=vpclattice_mixins.CfnServiceNetworkServiceAssociationPropsMixin.DnsEntryProperty(
                domain_name="domainName",
                hosted_zone_id="hostedZoneId"
            ),
            service_identifier="serviceIdentifier",
            service_network_identifier="serviceNetworkIdentifier",
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
        props: typing.Union[CfnServiceNetworkServiceAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::ServiceNetworkServiceAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157e17bfde9566dc29b55a365b6e727cbe1ba0d4b2b8219fae2ac6d6834af10d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0de4df9527aa6d4de0b376c68926c088a5baf46e4b9b62cdaf442aee0a03c9b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ce61831b451db19c1aaff31034af3bf65207ba1fcbae3164d83d575fd9c2f0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceNetworkServiceAssociationMixinProps:
        return typing.cast(CfnServiceNetworkServiceAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkServiceAssociationPropsMixin.DnsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName", "hosted_zone_id": "hostedZoneId"},
    )
    class DnsEntryProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The DNS information.

            :param domain_name: The domain name of the service.
            :param hosted_zone_id: The ID of the hosted zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkserviceassociation-dnsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                dns_entry_property = vpclattice_mixins.CfnServiceNetworkServiceAssociationPropsMixin.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73c6356085fecee5040ad06e5ff79082e5261d0fa0492bce91631ccb16601cd9)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The domain name of the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkserviceassociation-dnsentry.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the hosted zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkserviceassociation-dnsentry.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkVpcAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dns_options": "dnsOptions",
        "private_dns_enabled": "privateDnsEnabled",
        "security_group_ids": "securityGroupIds",
        "service_network_identifier": "serviceNetworkIdentifier",
        "tags": "tags",
        "vpc_identifier": "vpcIdentifier",
    },
)
class CfnServiceNetworkVpcAssociationMixinProps:
    def __init__(
        self,
        *,
        dns_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceNetworkVpcAssociationPropsMixin.DnsOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        private_dns_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnServiceNetworkVpcAssociationPropsMixin.

        :param dns_options: The DNS options for the service network VPC association.
        :param private_dns_enabled: Indicates if private DNS is enabled for the service network VPC association.
        :param security_group_ids: The IDs of the security groups. Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see `Control traffic to resources using security groups <https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .
        :param service_network_identifier: The ID or ARN of the service network. You must use an ARN if the resources are in different accounts.
        :param tags: The tags for the association.
        :param vpc_identifier: The ID of the VPC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_service_network_vpc_association_mixin_props = vpclattice_mixins.CfnServiceNetworkVpcAssociationMixinProps(
                dns_options=vpclattice_mixins.CfnServiceNetworkVpcAssociationPropsMixin.DnsOptionsProperty(
                    private_dns_preference="privateDnsPreference",
                    private_dns_specified_domains=["privateDnsSpecifiedDomains"]
                ),
                private_dns_enabled=False,
                security_group_ids=["securityGroupIds"],
                service_network_identifier="serviceNetworkIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_identifier="vpcIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610e1a7aab36e8531270b1e1b9a1507a0221ff1f6e3ae10cad6ed6d3e40584a4)
            check_type(argname="argument dns_options", value=dns_options, expected_type=type_hints["dns_options"])
            check_type(argname="argument private_dns_enabled", value=private_dns_enabled, expected_type=type_hints["private_dns_enabled"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument service_network_identifier", value=service_network_identifier, expected_type=type_hints["service_network_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_identifier", value=vpc_identifier, expected_type=type_hints["vpc_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_options is not None:
            self._values["dns_options"] = dns_options
        if private_dns_enabled is not None:
            self._values["private_dns_enabled"] = private_dns_enabled
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if service_network_identifier is not None:
            self._values["service_network_identifier"] = service_network_identifier
        if tags is not None:
            self._values["tags"] = tags
        if vpc_identifier is not None:
            self._values["vpc_identifier"] = vpc_identifier

    @builtins.property
    def dns_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceNetworkVpcAssociationPropsMixin.DnsOptionsProperty"]]:
        '''The DNS options for the service network VPC association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-dnsoptions
        '''
        result = self._values.get("dns_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceNetworkVpcAssociationPropsMixin.DnsOptionsProperty"]], result)

    @builtins.property
    def private_dns_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates if private DNS is enabled for the service network VPC association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-privatednsenabled
        '''
        result = self._values.get("private_dns_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the security groups.

        Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see `Control traffic to resources using security groups <https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or ARN of the service network.

        You must use an ARN if the resources are in different accounts.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-servicenetworkidentifier
        '''
        result = self._values.get("service_network_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPC.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-vpcidentifier
        '''
        result = self._values.get("vpc_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkVpcAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceNetworkVpcAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkVpcAssociationPropsMixin",
):
    '''Associates a VPC with a service network.

    When you associate a VPC with the service network, it enables all the resources within that VPC to be clients and communicate with other services in the service network. For more information, see `Manage VPC associations <https://docs.aws.amazon.com/vpc-lattice/latest/ug/service-network-associations.html#service-network-vpc-associations>`_ in the *Amazon VPC Lattice User Guide* .

    You can't use this operation if there is a disassociation in progress. If the association fails, retry by deleting the association and recreating it.

    As a result of this operation, the association gets created in the service network account and the VPC owner account.

    If you add a security group to the service network and VPC association, the association must continue to always have at least one security group. You can add or edit security groups at any time. However, to remove all security groups, you must first delete the association and recreate it without security groups.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html
    :cloudformationResource: AWS::VpcLattice::ServiceNetworkVpcAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_service_network_vpc_association_props_mixin = vpclattice_mixins.CfnServiceNetworkVpcAssociationPropsMixin(vpclattice_mixins.CfnServiceNetworkVpcAssociationMixinProps(
            dns_options=vpclattice_mixins.CfnServiceNetworkVpcAssociationPropsMixin.DnsOptionsProperty(
                private_dns_preference="privateDnsPreference",
                private_dns_specified_domains=["privateDnsSpecifiedDomains"]
            ),
            private_dns_enabled=False,
            security_group_ids=["securityGroupIds"],
            service_network_identifier="serviceNetworkIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_identifier="vpcIdentifier"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServiceNetworkVpcAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::ServiceNetworkVpcAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc51dda1ff7ad1fc195189378127bb3fc64ab90b4c2358fe3ffc8f238e6d0410)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28e174e3520191a2905b02fe183cdcd735ef39c85627adb63edbbf29445bdf64)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5137337ab78aa36ed0b20f199ca4888b5024b59585073de38125934749af108a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceNetworkVpcAssociationMixinProps:
        return typing.cast(CfnServiceNetworkVpcAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServiceNetworkVpcAssociationPropsMixin.DnsOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "private_dns_preference": "privateDnsPreference",
            "private_dns_specified_domains": "privateDnsSpecifiedDomains",
        },
    )
    class DnsOptionsProperty:
        def __init__(
            self,
            *,
            private_dns_preference: typing.Optional[builtins.str] = None,
            private_dns_specified_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The DNS configuration options.

            :param private_dns_preference: The preference for which private domains have a private hosted zone created for and associated with the specified VPC. Only supported when private DNS is enabled and when the VPC endpoint type is ServiceNetwork or Resource.
            :param private_dns_specified_domains: Indicates which of the private domains to create private hosted zones for and associate with the specified VPC. Only supported when private DNS is enabled and the private DNS preference is ``VERIFIED_DOMAINS_AND_SPECIFIED_DOMAINS`` or ``SPECIFIED_DOMAINS_ONLY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkvpcassociation-dnsoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                dns_options_property = vpclattice_mixins.CfnServiceNetworkVpcAssociationPropsMixin.DnsOptionsProperty(
                    private_dns_preference="privateDnsPreference",
                    private_dns_specified_domains=["privateDnsSpecifiedDomains"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3016e523076862ae758ef005200eee42376bbb5c2f04eaf7106d921773b64016)
                check_type(argname="argument private_dns_preference", value=private_dns_preference, expected_type=type_hints["private_dns_preference"])
                check_type(argname="argument private_dns_specified_domains", value=private_dns_specified_domains, expected_type=type_hints["private_dns_specified_domains"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if private_dns_preference is not None:
                self._values["private_dns_preference"] = private_dns_preference
            if private_dns_specified_domains is not None:
                self._values["private_dns_specified_domains"] = private_dns_specified_domains

        @builtins.property
        def private_dns_preference(self) -> typing.Optional[builtins.str]:
            '''The preference for which private domains have a private hosted zone created for and associated with the specified VPC.

            Only supported when private DNS is enabled and when the VPC endpoint type is ServiceNetwork or Resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkvpcassociation-dnsoptions.html#cfn-vpclattice-servicenetworkvpcassociation-dnsoptions-privatednspreference
            '''
            result = self._values.get("private_dns_preference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_dns_specified_domains(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates which of the private domains to create private hosted zones for and associate with the specified VPC.

            Only supported when private DNS is enabled and the private DNS preference is ``VERIFIED_DOMAINS_AND_SPECIFIED_DOMAINS`` or ``SPECIFIED_DOMAINS_ONLY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkvpcassociation-dnsoptions.html#cfn-vpclattice-servicenetworkvpcassociation-dnsoptions-privatednsspecifieddomains
            '''
            result = self._values.get("private_dns_specified_domains")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnServicePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServicePropsMixin",
):
    '''Creates a service.

    A service is any software application that can run on instances containers, or serverless functions within an account or virtual private cloud (VPC).

    For more information, see `Services <https://docs.aws.amazon.com/vpc-lattice/latest/ug/services.html>`_ in the *Amazon VPC Lattice User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html
    :cloudformationResource: AWS::VpcLattice::Service
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_service_props_mixin = vpclattice_mixins.CfnServicePropsMixin(vpclattice_mixins.CfnServiceMixinProps(
            auth_type="authType",
            certificate_arn="certificateArn",
            custom_domain_name="customDomainName",
            dns_entry=vpclattice_mixins.CfnServicePropsMixin.DnsEntryProperty(
                domain_name="domainName",
                hosted_zone_id="hostedZoneId"
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
        props: typing.Union[CfnServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::Service``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea4040fe70eca12519b920683c17bb2e37c27e631536f95f6523824ce533b82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f1e0619cb31c9a0b9bd666f4c241891c6e5e8ef684ac3fe518fb1c826c2a5d4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b6269fb1bcb43cca4c4c5a5069aed9372a43db13225e149c6c94562d24ea6fb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceMixinProps:
        return typing.cast(CfnServiceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnServicePropsMixin.DnsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName", "hosted_zone_id": "hostedZoneId"},
    )
    class DnsEntryProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the DNS information of a service.

            :param domain_name: The domain name of the service.
            :param hosted_zone_id: The ID of the hosted zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-service-dnsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                dns_entry_property = vpclattice_mixins.CfnServicePropsMixin.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__140815a3d44013923a415df7f1fd58ef14e3f8cee6f251ec3df76c7e0dce1105)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The domain name of the service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-service-dnsentry.html#cfn-vpclattice-service-dnsentry-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the hosted zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-service-dnsentry.html#cfn-vpclattice-service-dnsentry-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnTargetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "name": "name",
        "tags": "tags",
        "targets": "targets",
        "type": "type",
    },
)
class CfnTargetGroupMixinProps:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTargetGroupPropsMixin.TargetGroupConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTargetGroupPropsMixin.TargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTargetGroupPropsMixin.

        :param config: The target group configuration.
        :param name: The name of the target group. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param tags: The tags for the target group.
        :param targets: Describes a target.
        :param type: The type of target group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
            
            cfn_target_group_mixin_props = vpclattice_mixins.CfnTargetGroupMixinProps(
                config=vpclattice_mixins.CfnTargetGroupPropsMixin.TargetGroupConfigProperty(
                    health_check=vpclattice_mixins.CfnTargetGroupPropsMixin.HealthCheckConfigProperty(
                        enabled=False,
                        health_check_interval_seconds=123,
                        health_check_timeout_seconds=123,
                        healthy_threshold_count=123,
                        matcher=vpclattice_mixins.CfnTargetGroupPropsMixin.MatcherProperty(
                            http_code="httpCode"
                        ),
                        path="path",
                        port=123,
                        protocol="protocol",
                        protocol_version="protocolVersion",
                        unhealthy_threshold_count=123
                    ),
                    ip_address_type="ipAddressType",
                    lambda_event_structure_version="lambdaEventStructureVersion",
                    port=123,
                    protocol="protocol",
                    protocol_version="protocolVersion",
                    vpc_identifier="vpcIdentifier"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                targets=[vpclattice_mixins.CfnTargetGroupPropsMixin.TargetProperty(
                    id="id",
                    port=123
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8757dfcbd310a33abbf453d4321b2dce5ffb4299ef208c7118974761fb05af6)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if targets is not None:
            self._values["targets"] = targets
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.TargetGroupConfigProperty"]]:
        '''The target group configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.TargetGroupConfigProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the target group.

        The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the target group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.TargetProperty"]]]]:
        '''Describes a target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.TargetProperty"]]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of target group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTargetGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTargetGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnTargetGroupPropsMixin",
):
    '''Creates a target group.

    A target group is a collection of targets, or compute resources, that run your application or service. A target group can only be used by a single service.

    For more information, see `Target groups <https://docs.aws.amazon.com/vpc-lattice/latest/ug/target-groups.html>`_ in the *Amazon VPC Lattice User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html
    :cloudformationResource: AWS::VpcLattice::TargetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
        
        cfn_target_group_props_mixin = vpclattice_mixins.CfnTargetGroupPropsMixin(vpclattice_mixins.CfnTargetGroupMixinProps(
            config=vpclattice_mixins.CfnTargetGroupPropsMixin.TargetGroupConfigProperty(
                health_check=vpclattice_mixins.CfnTargetGroupPropsMixin.HealthCheckConfigProperty(
                    enabled=False,
                    health_check_interval_seconds=123,
                    health_check_timeout_seconds=123,
                    healthy_threshold_count=123,
                    matcher=vpclattice_mixins.CfnTargetGroupPropsMixin.MatcherProperty(
                        http_code="httpCode"
                    ),
                    path="path",
                    port=123,
                    protocol="protocol",
                    protocol_version="protocolVersion",
                    unhealthy_threshold_count=123
                ),
                ip_address_type="ipAddressType",
                lambda_event_structure_version="lambdaEventStructureVersion",
                port=123,
                protocol="protocol",
                protocol_version="protocolVersion",
                vpc_identifier="vpcIdentifier"
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            targets=[vpclattice_mixins.CfnTargetGroupPropsMixin.TargetProperty(
                id="id",
                port=123
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTargetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::VpcLattice::TargetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ea67a45814e97a6178419047eb1869a8687533de42248ead10b6415bcf1c8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dec268cfac4ef0233041b97231a9bb1c6b614856a3dfe7f570273cb43ae9cb9a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407367ccb239ce1f8e59292988a8be4d8022a36a7b2b7296e7fed1f6c2bb5d0e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTargetGroupMixinProps:
        return typing.cast(CfnTargetGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnTargetGroupPropsMixin.HealthCheckConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "health_check_interval_seconds": "healthCheckIntervalSeconds",
            "health_check_timeout_seconds": "healthCheckTimeoutSeconds",
            "healthy_threshold_count": "healthyThresholdCount",
            "matcher": "matcher",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "protocol_version": "protocolVersion",
            "unhealthy_threshold_count": "unhealthyThresholdCount",
        },
    )
    class HealthCheckConfigProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            health_check_interval_seconds: typing.Optional[jsii.Number] = None,
            health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
            healthy_threshold_count: typing.Optional[jsii.Number] = None,
            matcher: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTargetGroupPropsMixin.MatcherProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
            protocol_version: typing.Optional[builtins.str] = None,
            unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the health check configuration of a target group.

            Health check configurations aren't used for target groups of type ``LAMBDA`` or ``ALB`` .

            :param enabled: Indicates whether health checking is enabled.
            :param health_check_interval_seconds: The approximate amount of time, in seconds, between health checks of an individual target. The range is 5–300 seconds. The default is 30 seconds.
            :param health_check_timeout_seconds: The amount of time, in seconds, to wait before reporting a target as unhealthy. The range is 1–120 seconds. The default is 5 seconds.
            :param healthy_threshold_count: The number of consecutive successful health checks required before considering an unhealthy target healthy. The range is 2–10. The default is 5.
            :param matcher: The codes to use when checking for a successful response from a target.
            :param path: The destination for health checks on the targets. If the protocol version is ``HTTP/1.1`` or ``HTTP/2`` , specify a valid URI (for example, ``/path?query`` ). The default path is ``/`` . Health checks are not supported if the protocol version is ``gRPC`` , however, you can choose ``HTTP/1.1`` or ``HTTP/2`` and specify a valid URI.
            :param port: The port used when performing health checks on targets. The default setting is the port that a target receives traffic on.
            :param protocol: The protocol used when performing health checks on targets. The possible protocols are ``HTTP`` and ``HTTPS`` . The default is ``HTTP`` .
            :param protocol_version: The protocol version used when performing health checks on targets. The possible protocol versions are ``HTTP1`` and ``HTTP2`` .
            :param unhealthy_threshold_count: The number of consecutive failed health checks required before considering a target unhealthy. The range is 2–10. The default is 2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                health_check_config_property = vpclattice_mixins.CfnTargetGroupPropsMixin.HealthCheckConfigProperty(
                    enabled=False,
                    health_check_interval_seconds=123,
                    health_check_timeout_seconds=123,
                    healthy_threshold_count=123,
                    matcher=vpclattice_mixins.CfnTargetGroupPropsMixin.MatcherProperty(
                        http_code="httpCode"
                    ),
                    path="path",
                    port=123,
                    protocol="protocol",
                    protocol_version="protocolVersion",
                    unhealthy_threshold_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f75339d082ce44e06251b34af8203864a78299bd211bcf8645e4352af0e5f4a1)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument health_check_interval_seconds", value=health_check_interval_seconds, expected_type=type_hints["health_check_interval_seconds"])
                check_type(argname="argument health_check_timeout_seconds", value=health_check_timeout_seconds, expected_type=type_hints["health_check_timeout_seconds"])
                check_type(argname="argument healthy_threshold_count", value=healthy_threshold_count, expected_type=type_hints["healthy_threshold_count"])
                check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
                check_type(argname="argument unhealthy_threshold_count", value=unhealthy_threshold_count, expected_type=type_hints["unhealthy_threshold_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if health_check_interval_seconds is not None:
                self._values["health_check_interval_seconds"] = health_check_interval_seconds
            if health_check_timeout_seconds is not None:
                self._values["health_check_timeout_seconds"] = health_check_timeout_seconds
            if healthy_threshold_count is not None:
                self._values["healthy_threshold_count"] = healthy_threshold_count
            if matcher is not None:
                self._values["matcher"] = matcher
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if protocol_version is not None:
                self._values["protocol_version"] = protocol_version
            if unhealthy_threshold_count is not None:
                self._values["unhealthy_threshold_count"] = unhealthy_threshold_count

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether health checking is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''The approximate amount of time, in seconds, between health checks of an individual target.

            The range is 5–300 seconds. The default is 30 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-healthcheckintervalseconds
            '''
            result = self._values.get("health_check_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, to wait before reporting a target as unhealthy.

            The range is 1–120 seconds. The default is 5 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-healthchecktimeoutseconds
            '''
            result = self._values.get("health_check_timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive successful health checks required before considering an unhealthy target healthy.

            The range is 2–10. The default is 5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-healthythresholdcount
            '''
            result = self._values.get("healthy_threshold_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def matcher(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.MatcherProperty"]]:
            '''The codes to use when checking for a successful response from a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-matcher
            '''
            result = self._values.get("matcher")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.MatcherProperty"]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The destination for health checks on the targets.

            If the protocol version is ``HTTP/1.1`` or ``HTTP/2`` , specify a valid URI (for example, ``/path?query`` ). The default path is ``/`` . Health checks are not supported if the protocol version is ``gRPC`` , however, you can choose ``HTTP/1.1`` or ``HTTP/2`` and specify a valid URI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port used when performing health checks on targets.

            The default setting is the port that a target receives traffic on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol used when performing health checks on targets.

            The possible protocols are ``HTTP`` and ``HTTPS`` . The default is ``HTTP`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_version(self) -> typing.Optional[builtins.str]:
            '''The protocol version used when performing health checks on targets.

            The possible protocol versions are ``HTTP1`` and ``HTTP2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-protocolversion
            '''
            result = self._values.get("protocol_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive failed health checks required before considering a target unhealthy.

            The range is 2–10. The default is 2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-unhealthythresholdcount
            '''
            result = self._values.get("unhealthy_threshold_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnTargetGroupPropsMixin.MatcherProperty",
        jsii_struct_bases=[],
        name_mapping={"http_code": "httpCode"},
    )
    class MatcherProperty:
        def __init__(self, *, http_code: typing.Optional[builtins.str] = None) -> None:
            '''Describes the codes to use when checking for a successful response from a target for health checks.

            :param http_code: The HTTP code to use when checking for a successful response from a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-matcher.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                matcher_property = vpclattice_mixins.CfnTargetGroupPropsMixin.MatcherProperty(
                    http_code="httpCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1f168421da6bb4b58a58753b5b148b0347de66b794a1151e5b4a898baceb853)
                check_type(argname="argument http_code", value=http_code, expected_type=type_hints["http_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http_code is not None:
                self._values["http_code"] = http_code

        @builtins.property
        def http_code(self) -> typing.Optional[builtins.str]:
            '''The HTTP code to use when checking for a successful response from a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-matcher.html#cfn-vpclattice-targetgroup-matcher-httpcode
            '''
            result = self._values.get("http_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatcherProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnTargetGroupPropsMixin.TargetGroupConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "health_check": "healthCheck",
            "ip_address_type": "ipAddressType",
            "lambda_event_structure_version": "lambdaEventStructureVersion",
            "port": "port",
            "protocol": "protocol",
            "protocol_version": "protocolVersion",
            "vpc_identifier": "vpcIdentifier",
        },
    )
    class TargetGroupConfigProperty:
        def __init__(
            self,
            *,
            health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTargetGroupPropsMixin.HealthCheckConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_address_type: typing.Optional[builtins.str] = None,
            lambda_event_structure_version: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
            protocol_version: typing.Optional[builtins.str] = None,
            vpc_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration of a target group.

            For more information, see `Target groups <https://docs.aws.amazon.com/vpc-lattice/latest/ug/target-groups.html>`_ in the *Amazon VPC Lattice User Guide* .

            :param health_check: The health check configuration. Not supported if the target group type is ``LAMBDA`` or ``ALB`` .
            :param ip_address_type: The type of IP address used for the target group. Supported only if the target group type is ``IP`` . The default is ``IPV4`` . Default: - "IPV4"
            :param lambda_event_structure_version: The version of the event structure that your Lambda function receives. Supported only if the target group type is ``LAMBDA`` . The default is ``V1`` .
            :param port: The port on which the targets are listening. For HTTP, the default is 80. For HTTPS, the default is 443. Not supported if the target group type is ``LAMBDA`` .
            :param protocol: The protocol to use for routing traffic to the targets. The default is the protocol of the target group. Not supported if the target group type is ``LAMBDA`` .
            :param protocol_version: The protocol version. The default is ``HTTP1`` . Not supported if the target group type is ``LAMBDA`` . Default: - "HTTP1"
            :param vpc_identifier: The ID of the VPC. Not supported if the target group type is ``LAMBDA`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                target_group_config_property = vpclattice_mixins.CfnTargetGroupPropsMixin.TargetGroupConfigProperty(
                    health_check=vpclattice_mixins.CfnTargetGroupPropsMixin.HealthCheckConfigProperty(
                        enabled=False,
                        health_check_interval_seconds=123,
                        health_check_timeout_seconds=123,
                        healthy_threshold_count=123,
                        matcher=vpclattice_mixins.CfnTargetGroupPropsMixin.MatcherProperty(
                            http_code="httpCode"
                        ),
                        path="path",
                        port=123,
                        protocol="protocol",
                        protocol_version="protocolVersion",
                        unhealthy_threshold_count=123
                    ),
                    ip_address_type="ipAddressType",
                    lambda_event_structure_version="lambdaEventStructureVersion",
                    port=123,
                    protocol="protocol",
                    protocol_version="protocolVersion",
                    vpc_identifier="vpcIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc086029a15e12422342ebb2bc5ab432c9af27a19942a515c6f066be86754788)
                check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
                check_type(argname="argument lambda_event_structure_version", value=lambda_event_structure_version, expected_type=type_hints["lambda_event_structure_version"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
                check_type(argname="argument vpc_identifier", value=vpc_identifier, expected_type=type_hints["vpc_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if health_check is not None:
                self._values["health_check"] = health_check
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type
            if lambda_event_structure_version is not None:
                self._values["lambda_event_structure_version"] = lambda_event_structure_version
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if protocol_version is not None:
                self._values["protocol_version"] = protocol_version
            if vpc_identifier is not None:
                self._values["vpc_identifier"] = vpc_identifier

        @builtins.property
        def health_check(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.HealthCheckConfigProperty"]]:
            '''The health check configuration.

            Not supported if the target group type is ``LAMBDA`` or ``ALB`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-healthcheck
            '''
            result = self._values.get("health_check")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.HealthCheckConfigProperty"]], result)

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''The type of IP address used for the target group.

            Supported only if the target group type is ``IP`` . The default is ``IPV4`` .

            :default: - "IPV4"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_event_structure_version(self) -> typing.Optional[builtins.str]:
            '''The version of the event structure that your Lambda function receives.

            Supported only if the target group type is ``LAMBDA`` . The default is ``V1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-lambdaeventstructureversion
            '''
            result = self._values.get("lambda_event_structure_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port on which the targets are listening.

            For HTTP, the default is 80. For HTTPS, the default is 443. Not supported if the target group type is ``LAMBDA`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol to use for routing traffic to the targets.

            The default is the protocol of the target group. Not supported if the target group type is ``LAMBDA`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_version(self) -> typing.Optional[builtins.str]:
            '''The protocol version.

            The default is ``HTTP1`` . Not supported if the target group type is ``LAMBDA`` .

            :default: - "HTTP1"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-protocolversion
            '''
            result = self._values.get("protocol_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_identifier(self) -> typing.Optional[builtins.str]:
            '''The ID of the VPC.

            Not supported if the target group type is ``LAMBDA`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-vpcidentifier
            '''
            result = self._values.get("vpc_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_vpclattice.mixins.CfnTargetGroupPropsMixin.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "port": "port"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a target.

            :param id: The ID of the target. If the target group type is ``INSTANCE`` , this is an instance ID. If the target group type is ``IP`` , this is an IP address. If the target group type is ``LAMBDA`` , this is the ARN of a Lambda function. If the target group type is ``ALB`` , this is the ARN of an Application Load Balancer.
            :param port: The port on which the target is listening. For HTTP, the default is 80. For HTTPS, the default is 443.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_vpclattice import mixins as vpclattice_mixins
                
                target_property = vpclattice_mixins.CfnTargetGroupPropsMixin.TargetProperty(
                    id="id",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3115a31762224941ffb14f50138d1e4224ee10b5155105faa906bb3d948ac401)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the target.

            If the target group type is ``INSTANCE`` , this is an instance ID. If the target group type is ``IP`` , this is an IP address. If the target group type is ``LAMBDA`` , this is the ARN of a Lambda function. If the target group type is ``ALB`` , this is the ARN of an Application Load Balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-target.html#cfn-vpclattice-targetgroup-target-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port on which the target is listening.

            For HTTP, the default is 80. For HTTPS, the default is 443.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-target.html#cfn-vpclattice-targetgroup-target-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAccessLogSubscriptionMixinProps",
    "CfnAccessLogSubscriptionPropsMixin",
    "CfnAuthPolicyMixinProps",
    "CfnAuthPolicyPropsMixin",
    "CfnDomainVerificationMixinProps",
    "CfnDomainVerificationPropsMixin",
    "CfnListenerMixinProps",
    "CfnListenerPropsMixin",
    "CfnResourceConfigurationLogsMixin",
    "CfnResourceConfigurationMixinProps",
    "CfnResourceConfigurationPropsMixin",
    "CfnResourceConfigurationResourceAccessLogs",
    "CfnResourceGatewayMixinProps",
    "CfnResourceGatewayPropsMixin",
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
    "CfnRuleMixinProps",
    "CfnRulePropsMixin",
    "CfnServiceAccessLogs",
    "CfnServiceLogsMixin",
    "CfnServiceMixinProps",
    "CfnServiceNetworkMixinProps",
    "CfnServiceNetworkPropsMixin",
    "CfnServiceNetworkResourceAssociationMixinProps",
    "CfnServiceNetworkResourceAssociationPropsMixin",
    "CfnServiceNetworkServiceAssociationMixinProps",
    "CfnServiceNetworkServiceAssociationPropsMixin",
    "CfnServiceNetworkVpcAssociationMixinProps",
    "CfnServiceNetworkVpcAssociationPropsMixin",
    "CfnServicePropsMixin",
    "CfnTargetGroupMixinProps",
    "CfnTargetGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__d8b19c5f911504ae2e72dfd7bd3f412c37738f34a84318990f190e2ce94bcfc2(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
    service_network_log_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ea917003345f231bdc77b75d6e8bd4c1f417c9c79da1af13e5750b99b83c5a(
    props: typing.Union[CfnAccessLogSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c5f382a88f28833cae01a605ccaf0d319508f5518d628d7159a1f62b016926(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0eefbc5245328855ccc28982acd3c8aca6a9ab1b159df2e49834e1515b4c18(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16c8e0ec6e8f9250204821d638421e660faa78ce415caa9a79d030bba3f29b5(
    *,
    policy: typing.Any = None,
    resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b067642476d1c88f343ff0f6d912ae9ceb55f84de65b23313a0d5f56756a9c00(
    props: typing.Union[CfnAuthPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cc0d242d82bd8f319fc7c6a76dde34779c517b6116ca113e9c3a3aaacddc0a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bea0b4be304e015678e1d287d1cfec94a48b0dcde4bb4af304fea3e92d57799(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5dee590516d62f29986336b91b580ee3d44f68d33cbc896806fa064dfae7725(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98565fc1d897e2393ef399ad60a02ea7ee687d19120f5f7b8138fe66a281fcdc(
    props: typing.Union[CfnDomainVerificationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1042653f7f4b4dddada6ee8cc81ab6792ddb8fc05b61074b1eeafb29a80a7ead(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dea3c50f7a05c4f17fbd00df567d9407a44190c7732e7a5608cee5eb3dcfeaa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7cf231bd065f3f7e286b4589475fb0704cfd328aec875b1fc8239b996003f6(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5af3e3a4383db753b84c63b0ae72fdaa4f98a1a65d32bca5f61de73926be6a9(
    *,
    default_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.DefaultActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e9e4a1e8b9a579d4d73f5f8049e7b1e82cd714c38ec888e8f760679bd18486(
    props: typing.Union[CfnListenerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d78473cba0d1739df6a2127fea6f28f7fc151f599f247a7bf51388dd6740f8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bbf60dd3c00734693823c4b11086727adbd3fe22a65d6e38532db76a2311ab(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d747f7b2bc805c2bf3496c6c2f20e58b6cb61584909245cb0d5e34b2872b9494(
    *,
    fixed_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.FixedResponseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    forward: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.ForwardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13f45434f6aeeeda7b1b8a6ddb0811c5dd49875fe767aafe776296f361444e8(
    *,
    status_code: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb30b71628a90366a46496321b42c01678a89a62943c3658b47a0e9e54e71ee6(
    *,
    target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.WeightedTargetGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1ef3d4cadb14a807a8d69f6783c2eafdd3b921ce4c6b71af93870c0f3e6590(
    *,
    target_group_identifier: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf692ae198356efde102dcc1479407fb4a9b7603189f45384dc6a93d773f572(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254761cc919ffdcbc3319bdac9d3a03a04933e18c7c76d96c8b2253f2b7c2e77(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bad8c4b06a67e7c820a22d0a853b0190f471905ad0b9260ecdaa70648c6c7b2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7b4f9de9ffef31bd8d989021cfe1a54e72f78afc004a1dde95a0a75197c93b(
    *,
    allow_association_to_sharable_service_network: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    domain_verification_id: typing.Optional[builtins.str] = None,
    group_domain: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    port_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    protocol_type: typing.Optional[builtins.str] = None,
    resource_configuration_auth_type: typing.Optional[builtins.str] = None,
    resource_configuration_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceConfigurationPropsMixin.ResourceConfigurationDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_configuration_group_id: typing.Optional[builtins.str] = None,
    resource_configuration_type: typing.Optional[builtins.str] = None,
    resource_gateway_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c74739924c89c6b85dc8eb70f8b8b8fb7f5a662452e7cbc1b1c154d172952b2(
    props: typing.Union[CfnResourceConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a960caa03a6c94f47ac5300cd93d4cf5401d41c12d52803e2e9a2339f556d507(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1a5a724948c9c20123f2d283971a9b69f9ecfb49ae198c6075ff167e9c2be4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f148788bdb7b3b202487ee636400fb76bfa2c51318f419f92c7168795ace1ca7(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e96179f4d47e2d8df2b023dc2f14b425148dc48471356407c61bb0ab0f88e9f(
    *,
    arn_resource: typing.Optional[builtins.str] = None,
    dns_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnResourceConfigurationPropsMixin.DnsResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0468383b1b092d6afbf8ed80c82d0b204dba50e671ef4c3a66fda59cdbc0ca4a(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a2fbfdd658b0dc699e303dbfc31886b53478189e59adf59f1abe1c1be202aa(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a8067ac69dd9b14962cae87ebf1347cd25eaabb40dd86908fc47f0cdc9573a(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740c7d75f00c8baa80b427a6e3035b67408a3d08dba7cc9bbff811d9f5bedab6(
    *,
    ip_address_type: typing.Optional[builtins.str] = None,
    ipv4_addresses_per_eni: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d94e924413bc94a0f83a88f7a3794e04e1f6b52abd77155185a1443bdc0d97e(
    props: typing.Union[CfnResourceGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6565c3446668181a5f6ff7f8aabc274bfe700c29e680c4372de472b6fec82ec8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c776223f252c37f9a2975fd4991e1ac058a29c34e925f0d79c99ca0a77f67c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ec25d8f9b0e0f6d4c5d48afa35864541bd4781cba8b9662438f47314524e01(
    *,
    policy: typing.Any = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b19400862255a39c09ea99e54729ca473ac50ae3c3f63caa61d6775b90cda3(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8d7e12ca2fdffe3eecb9cc053074c4832d88ef4801535e29f55e2877ff632e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d0b9530e95c5576d498262b203351046db8252411390652369106ff8572940(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921458faafcacb158b2229ec1ba51076f6a37c5c53fbae1f405a86af382ba86a(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    listener_identifier: typing.Optional[builtins.str] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.MatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7e81220c754b88620e05ead6469413754639ffb1e5f9cb987925065e1652bb(
    props: typing.Union[CfnRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9d3186e21b1f7b960447638ba1586650af08e329fe15d196b9c6b178eabb24(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161b0d12ccaac85822f3e485fe6760a77d711d8fbb12db1825910d033d596773(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bc328d5fce5ce70358c3d6abe462c7c6c28026f0bed91e477747b3be265460(
    *,
    fixed_response: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.FixedResponseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    forward: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.ForwardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329958e08bfeee95d553e8c3f755bdf7436abe53262da7031739827692a68cd7(
    *,
    status_code: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16702d7ca2d7afbc1bc141129efcd5be691247424728556d6867d44597152c4d(
    *,
    target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.WeightedTargetGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283684fb1e2017674bf9471a7d0cf0237fd6b0052063d253f1db24960d374f8b(
    *,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.HeaderMatchTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472599b164493e7af0e29c8ac973e63dd1cb759e95adcb682c82f258bac5060f(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ac5195436605f7b191517808e619c161ec73681de6c32deb226fce4a6ba99d(
    *,
    header_matches: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.HeaderMatchProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.PathMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f16d7f452b405594ba99230f0cc6348ced34c9816be75f5952f0ce2d17ec4b(
    *,
    http_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.HttpMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424b4ba0e9ec9ec0075558858b16d73f22acf53b260b9a8eece722a2683f73d4(
    *,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.PathMatchTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4ddb7aec3752ed4b7ec97bd6152d5fd03f1a1f72638b97d90d4e15ea3225fa(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd7245b2f24e9f8d38346b0c5a577905c8dba92ead7659e1aacdc57cda31795(
    *,
    target_group_identifier: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f24bef0310e78e6bc9afd718e7c1b87dd76ffcfef8fe4b1e33f9bab6ac2427e(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2d3866865e111d61a11b5ec70292d8121bcb7a817985bf0c4a33ebcfe02486(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb29b532c6cc094e697a80e978e5462c3a4c081e4f3403e739b92de5eef97c1(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a307cfd341317cb2049d64334601f6c0551285b2200830e003f645f52e76be8(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bc90ce1bdd13d53c0c4f879d3085cda6d6eada37ac5d9a800126ee1ccd82d7(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367caec71d9e9cffa20dadd005b1837bb3447594e7aae83a778f5c31d5e295bd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04ec87cc8751141399746a73ba226ce5900cd2da1b707f3df78b1a814dafed6(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    dns_entry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServicePropsMixin.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f651e3fdad38e52e0e57766ba91558ae972bcda101e14580e81df122902252b1(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sharing_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceNetworkPropsMixin.SharingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c97ba60b541e5b79ea1b236ba1fa9f6b693ba24c281766f560e4c9a381c921(
    props: typing.Union[CfnServiceNetworkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465a21059ca410047be05fa65dba09acc89412e18d299bad05863580dbf823e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d223bc08aa2064db3d92a11931629ed011bf9217ec752446fc30583cdfec7f5b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7158550f94f317a2ca5df4a0b6329fe8e84f29fff97cd5668856d2f415fcc4(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6f6f8bebb42f68e89477ee4ee6af9b2535a17a5d1380cce40786ad38af6ed4(
    *,
    private_dns_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_configuration_id: typing.Optional[builtins.str] = None,
    service_network_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb105cccc9deff25420a09674c50f189ca0370b4b2463c70732d594d5e00629f(
    props: typing.Union[CfnServiceNetworkResourceAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04694a1c7f930a5f96bbef0179fab507650fb19c2b46fb0ed2a4863baaaaad1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe938c07f3b2e6ae0451eda0d0fd90cf37194c2fd6f426926ef77a52b805695d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd111c29effa59d64519462ceefa9ef8296f77ae1fb9d259c70b05fe76c1db34(
    *,
    dns_entry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceNetworkServiceAssociationPropsMixin.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157e17bfde9566dc29b55a365b6e727cbe1ba0d4b2b8219fae2ac6d6834af10d(
    props: typing.Union[CfnServiceNetworkServiceAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0de4df9527aa6d4de0b376c68926c088a5baf46e4b9b62cdaf442aee0a03c9b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ce61831b451db19c1aaff31034af3bf65207ba1fcbae3164d83d575fd9c2f0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c6356085fecee5040ad06e5ff79082e5261d0fa0492bce91631ccb16601cd9(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610e1a7aab36e8531270b1e1b9a1507a0221ff1f6e3ae10cad6ed6d3e40584a4(
    *,
    dns_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceNetworkVpcAssociationPropsMixin.DnsOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    private_dns_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc51dda1ff7ad1fc195189378127bb3fc64ab90b4c2358fe3ffc8f238e6d0410(
    props: typing.Union[CfnServiceNetworkVpcAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e174e3520191a2905b02fe183cdcd735ef39c85627adb63edbbf29445bdf64(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5137337ab78aa36ed0b20f199ca4888b5024b59585073de38125934749af108a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3016e523076862ae758ef005200eee42376bbb5c2f04eaf7106d921773b64016(
    *,
    private_dns_preference: typing.Optional[builtins.str] = None,
    private_dns_specified_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea4040fe70eca12519b920683c17bb2e37c27e631536f95f6523824ce533b82(
    props: typing.Union[CfnServiceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1e0619cb31c9a0b9bd666f4c241891c6e5e8ef684ac3fe518fb1c826c2a5d4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6269fb1bcb43cca4c4c5a5069aed9372a43db13225e149c6c94562d24ea6fb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140815a3d44013923a415df7f1fd58ef14e3f8cee6f251ec3df76c7e0dce1105(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8757dfcbd310a33abbf453d4321b2dce5ffb4299ef208c7118974761fb05af6(
    *,
    config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTargetGroupPropsMixin.TargetGroupConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTargetGroupPropsMixin.TargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ea67a45814e97a6178419047eb1869a8687533de42248ead10b6415bcf1c8e(
    props: typing.Union[CfnTargetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec268cfac4ef0233041b97231a9bb1c6b614856a3dfe7f570273cb43ae9cb9a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407367ccb239ce1f8e59292988a8be4d8022a36a7b2b7296e7fed1f6c2bb5d0e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75339d082ce44e06251b34af8203864a78299bd211bcf8645e4352af0e5f4a1(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    health_check_interval_seconds: typing.Optional[jsii.Number] = None,
    health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
    healthy_threshold_count: typing.Optional[jsii.Number] = None,
    matcher: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTargetGroupPropsMixin.MatcherProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_version: typing.Optional[builtins.str] = None,
    unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f168421da6bb4b58a58753b5b148b0347de66b794a1151e5b4a898baceb853(
    *,
    http_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc086029a15e12422342ebb2bc5ab432c9af27a19942a515c6f066be86754788(
    *,
    health_check: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTargetGroupPropsMixin.HealthCheckConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    lambda_event_structure_version: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_version: typing.Optional[builtins.str] = None,
    vpc_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3115a31762224941ffb14f50138d1e4224ee10b5155105faa906bb3d948ac401(
    *,
    id: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
