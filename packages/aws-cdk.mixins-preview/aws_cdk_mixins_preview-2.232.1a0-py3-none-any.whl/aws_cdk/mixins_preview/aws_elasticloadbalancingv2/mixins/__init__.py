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
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerCertificateMixinProps",
    jsii_struct_bases=[],
    name_mapping={"certificates": "certificates", "listener_arn": "listenerArn"},
)
class CfnListenerCertificateMixinProps:
    def __init__(
        self,
        *,
        certificates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerCertificatePropsMixin.CertificateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        listener_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnListenerCertificatePropsMixin.

        :param certificates: The certificate. You can specify one certificate per resource.
        :param listener_arn: The Amazon Resource Name (ARN) of the listener.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
            
            cfn_listener_certificate_mixin_props = elasticloadbalancingv2_mixins.CfnListenerCertificateMixinProps(
                certificates=[elasticloadbalancingv2_mixins.CfnListenerCertificatePropsMixin.CertificateProperty(
                    certificate_arn="certificateArn"
                )],
                listener_arn="listenerArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd4a0920ebd9083a8b6884831e95a1ca30c77b6c4b49241c1a98a499ff91b09)
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument listener_arn", value=listener_arn, expected_type=type_hints["listener_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificates is not None:
            self._values["certificates"] = certificates
        if listener_arn is not None:
            self._values["listener_arn"] = listener_arn

    @builtins.property
    def certificates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerCertificatePropsMixin.CertificateProperty"]]]]:
        '''The certificate.

        You can specify one certificate per resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-certificates
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerCertificatePropsMixin.CertificateProperty"]]]], result)

    @builtins.property
    def listener_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the listener.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html#cfn-elasticloadbalancingv2-listenercertificate-listenerarn
        '''
        result = self._values.get("listener_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerCertificateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnListenerCertificatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerCertificatePropsMixin",
):
    '''Specifies an SSL server certificate to add to the certificate list for an HTTPS or TLS listener.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::ListenerCertificate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
        
        cfn_listener_certificate_props_mixin = elasticloadbalancingv2_mixins.CfnListenerCertificatePropsMixin(elasticloadbalancingv2_mixins.CfnListenerCertificateMixinProps(
            certificates=[elasticloadbalancingv2_mixins.CfnListenerCertificatePropsMixin.CertificateProperty(
                certificate_arn="certificateArn"
            )],
            listener_arn="listenerArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnListenerCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElasticLoadBalancingV2::ListenerCertificate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52cc605200dff47f364b1296ed5142468adaaadc9a05cf0e5a4b197f2097af11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb36165841822a2beb662efa7765ed40dd7b31a2242cfcdc83ed84616a8d9041)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b940234e5b147001411793655ec14f3537298241850051153bffbc864e987ed6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnListenerCertificateMixinProps:
        return typing.cast(CfnListenerCertificateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerCertificatePropsMixin.CertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class CertificateProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an SSL server certificate for the certificate list of a secure listener.

            :param certificate_arn: The Amazon Resource Name (ARN) of the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenercertificate-certificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                certificate_property = elasticloadbalancingv2_mixins.CfnListenerCertificatePropsMixin.CertificateProperty(
                    certificate_arn="certificateArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5bf665640a0b849aea40c0099a6ac5b7f18cf0c9fefdd753e076f397eae50e75)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenercertificate-certificate.html#cfn-elasticloadbalancingv2-listenercertificate-certificate-certificatearn
            '''
            result = self._values.get("certificate_arn")
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
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alpn_policy": "alpnPolicy",
        "certificates": "certificates",
        "default_actions": "defaultActions",
        "listener_attributes": "listenerAttributes",
        "load_balancer_arn": "loadBalancerArn",
        "mutual_authentication": "mutualAuthentication",
        "port": "port",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
    },
)
class CfnListenerMixinProps:
    def __init__(
        self,
        *,
        alpn_policy: typing.Optional[typing.Sequence[builtins.str]] = None,
        certificates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.CertificateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        default_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        listener_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.ListenerAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        mutual_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.MutualAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnListenerPropsMixin.

        :param alpn_policy: [TLS listener] The name of the Application-Layer Protocol Negotiation (ALPN) policy.
        :param certificates: The default SSL server certificate for a secure listener. You must provide exactly one certificate if the listener protocol is HTTPS or TLS. For an HTTPS listener, update requires some interruptions. For a TLS listener, update requires no interruption. To create a certificate list for a secure listener, use `AWS::ElasticLoadBalancingV2::ListenerCertificate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html>`_ .
        :param default_actions: The actions for the default rule. You cannot define a condition for a default rule. To create additional rules for an Application Load Balancer, use `AWS::ElasticLoadBalancingV2::ListenerRule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html>`_ .
        :param listener_attributes: The listener attributes. Attributes that you do not modify retain their current values.
        :param load_balancer_arn: The Amazon Resource Name (ARN) of the load balancer.
        :param mutual_authentication: The mutual authentication configuration information.
        :param port: The port on which the load balancer is listening. You can't specify a port for a Gateway Load Balancer.
        :param protocol: The protocol for connections from clients to the load balancer. For Application Load Balancers, the supported protocols are HTTP and HTTPS. For Network Load Balancers, the supported protocols are TCP, TLS, UDP, TCP_UDP, QUIC, and TCP_QUIC. You can’t specify the UDP, TCP_UDP, QUIC, or TCP_QUIC protocol if dual-stack mode is enabled. You can't specify a protocol for a Gateway Load Balancer.
        :param ssl_policy: [HTTPS and TLS listeners] The security policy that defines which protocols and ciphers are supported. For more information, see `Security policies <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/describe-ssl-policies.html>`_ in the *Application Load Balancers Guide* and `Security policies <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/describe-ssl-policies.html>`_ in the *Network Load Balancers Guide* . [HTTPS listeners] Updating the security policy can result in interruptions if the load balancer is handling a high volume of traffic. To decrease the possibility of an interruption if your load balancer is handling a high volume of traffic, create an additional load balancer or request an LCU reservation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
            
            cfn_listener_mixin_props = elasticloadbalancingv2_mixins.CfnListenerMixinProps(
                alpn_policy=["alpnPolicy"],
                certificates=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.CertificateProperty(
                    certificate_arn="certificateArn"
                )],
                default_actions=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ActionProperty(
                    authenticate_cognito_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.AuthenticateCognitoConfigProperty(
                        authentication_request_extra_params={
                            "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                        },
                        on_unauthenticated_request="onUnauthenticatedRequest",
                        scope="scope",
                        session_cookie_name="sessionCookieName",
                        session_timeout="sessionTimeout",
                        user_pool_arn="userPoolArn",
                        user_pool_client_id="userPoolClientId",
                        user_pool_domain="userPoolDomain"
                    ),
                    authenticate_oidc_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.AuthenticateOidcConfigProperty(
                        authentication_request_extra_params={
                            "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                        },
                        authorization_endpoint="authorizationEndpoint",
                        client_id="clientId",
                        client_secret="clientSecret",
                        issuer="issuer",
                        on_unauthenticated_request="onUnauthenticatedRequest",
                        scope="scope",
                        session_cookie_name="sessionCookieName",
                        session_timeout="sessionTimeout",
                        token_endpoint="tokenEndpoint",
                        use_existing_client_secret=False,
                        user_info_endpoint="userInfoEndpoint"
                    ),
                    fixed_response_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.FixedResponseConfigProperty(
                        content_type="contentType",
                        message_body="messageBody",
                        status_code="statusCode"
                    ),
                    forward_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ForwardConfigProperty(
                        target_groups=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupTupleProperty(
                            target_group_arn="targetGroupArn",
                            weight=123
                        )],
                        target_group_stickiness_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupStickinessConfigProperty(
                            duration_seconds=123,
                            enabled=False
                        )
                    ),
                    jwt_validation_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.JwtValidationConfigProperty(
                        additional_claims=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty(
                            format="format",
                            name="name",
                            values=["values"]
                        )],
                        issuer="issuer",
                        jwks_endpoint="jwksEndpoint"
                    ),
                    order=123,
                    redirect_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.RedirectConfigProperty(
                        host="host",
                        path="path",
                        port="port",
                        protocol="protocol",
                        query="query",
                        status_code="statusCode"
                    ),
                    target_group_arn="targetGroupArn",
                    type="type"
                )],
                listener_attributes=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ListenerAttributeProperty(
                    key="key",
                    value="value"
                )],
                load_balancer_arn="loadBalancerArn",
                mutual_authentication=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.MutualAuthenticationProperty(
                    advertise_trust_store_ca_names="advertiseTrustStoreCaNames",
                    ignore_client_certificate_expiry=False,
                    mode="mode",
                    trust_store_arn="trustStoreArn"
                ),
                port=123,
                protocol="protocol",
                ssl_policy="sslPolicy"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a54e0531834474855b49794758830af6eb94e7a6d8d4187da28e9d51346ff6)
            check_type(argname="argument alpn_policy", value=alpn_policy, expected_type=type_hints["alpn_policy"])
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument default_actions", value=default_actions, expected_type=type_hints["default_actions"])
            check_type(argname="argument listener_attributes", value=listener_attributes, expected_type=type_hints["listener_attributes"])
            check_type(argname="argument load_balancer_arn", value=load_balancer_arn, expected_type=type_hints["load_balancer_arn"])
            check_type(argname="argument mutual_authentication", value=mutual_authentication, expected_type=type_hints["mutual_authentication"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alpn_policy is not None:
            self._values["alpn_policy"] = alpn_policy
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_actions is not None:
            self._values["default_actions"] = default_actions
        if listener_attributes is not None:
            self._values["listener_attributes"] = listener_attributes
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if mutual_authentication is not None:
            self._values["mutual_authentication"] = mutual_authentication
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def alpn_policy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''[TLS listener] The name of the Application-Layer Protocol Negotiation (ALPN) policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-alpnpolicy
        '''
        result = self._values.get("alpn_policy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def certificates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.CertificateProperty"]]]]:
        '''The default SSL server certificate for a secure listener.

        You must provide exactly one certificate if the listener protocol is HTTPS or TLS.

        For an HTTPS listener, update requires some interruptions. For a TLS listener, update requires no interruption.

        To create a certificate list for a secure listener, use `AWS::ElasticLoadBalancingV2::ListenerCertificate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenercertificate.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-certificates
        '''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.CertificateProperty"]]]], result)

    @builtins.property
    def default_actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.ActionProperty"]]]]:
        '''The actions for the default rule. You cannot define a condition for a default rule.

        To create additional rules for an Application Load Balancer, use `AWS::ElasticLoadBalancingV2::ListenerRule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-defaultactions
        '''
        result = self._values.get("default_actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.ActionProperty"]]]], result)

    @builtins.property
    def listener_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.ListenerAttributeProperty"]]]]:
        '''The listener attributes.

        Attributes that you do not modify retain their current values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-listenerattributes
        '''
        result = self._values.get("listener_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.ListenerAttributeProperty"]]]], result)

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-loadbalancerarn
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mutual_authentication(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.MutualAuthenticationProperty"]]:
        '''The mutual authentication configuration information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-mutualauthentication
        '''
        result = self._values.get("mutual_authentication")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.MutualAuthenticationProperty"]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port on which the load balancer is listening.

        You can't specify a port for a Gateway Load Balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol for connections from clients to the load balancer.

        For Application Load Balancers, the supported protocols are HTTP and HTTPS. For Network Load Balancers, the supported protocols are TCP, TLS, UDP, TCP_UDP, QUIC, and TCP_QUIC. You can’t specify the UDP, TCP_UDP, QUIC, or TCP_QUIC protocol if dual-stack mode is enabled. You can't specify a protocol for a Gateway Load Balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_policy(self) -> typing.Optional[builtins.str]:
        '''[HTTPS and TLS listeners] The security policy that defines which protocols and ciphers are supported.

        For more information, see `Security policies <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/describe-ssl-policies.html>`_ in the *Application Load Balancers Guide* and `Security policies <https://docs.aws.amazon.com/elasticloadbalancing/latest/network/describe-ssl-policies.html>`_ in the *Network Load Balancers Guide* .

        [HTTPS listeners] Updating the security policy can result in interruptions if the load balancer is handling a high volume of traffic. To decrease the possibility of an interruption if your load balancer is handling a high volume of traffic, create an additional load balancer or request an LCU reservation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html#cfn-elasticloadbalancingv2-listener-sslpolicy
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin",
):
    '''Specifies a listener for an Application Load Balancer, Network Load Balancer, or Gateway Load Balancer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listener.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::Listener
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
        
        cfn_listener_props_mixin = elasticloadbalancingv2_mixins.CfnListenerPropsMixin(elasticloadbalancingv2_mixins.CfnListenerMixinProps(
            alpn_policy=["alpnPolicy"],
            certificates=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.CertificateProperty(
                certificate_arn="certificateArn"
            )],
            default_actions=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ActionProperty(
                authenticate_cognito_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.AuthenticateCognitoConfigProperty(
                    authentication_request_extra_params={
                        "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                    },
                    on_unauthenticated_request="onUnauthenticatedRequest",
                    scope="scope",
                    session_cookie_name="sessionCookieName",
                    session_timeout="sessionTimeout",
                    user_pool_arn="userPoolArn",
                    user_pool_client_id="userPoolClientId",
                    user_pool_domain="userPoolDomain"
                ),
                authenticate_oidc_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.AuthenticateOidcConfigProperty(
                    authentication_request_extra_params={
                        "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                    },
                    authorization_endpoint="authorizationEndpoint",
                    client_id="clientId",
                    client_secret="clientSecret",
                    issuer="issuer",
                    on_unauthenticated_request="onUnauthenticatedRequest",
                    scope="scope",
                    session_cookie_name="sessionCookieName",
                    session_timeout="sessionTimeout",
                    token_endpoint="tokenEndpoint",
                    use_existing_client_secret=False,
                    user_info_endpoint="userInfoEndpoint"
                ),
                fixed_response_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.FixedResponseConfigProperty(
                    content_type="contentType",
                    message_body="messageBody",
                    status_code="statusCode"
                ),
                forward_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ForwardConfigProperty(
                    target_groups=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupTupleProperty(
                        target_group_arn="targetGroupArn",
                        weight=123
                    )],
                    target_group_stickiness_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupStickinessConfigProperty(
                        duration_seconds=123,
                        enabled=False
                    )
                ),
                jwt_validation_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.JwtValidationConfigProperty(
                    additional_claims=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty(
                        format="format",
                        name="name",
                        values=["values"]
                    )],
                    issuer="issuer",
                    jwks_endpoint="jwksEndpoint"
                ),
                order=123,
                redirect_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.RedirectConfigProperty(
                    host="host",
                    path="path",
                    port="port",
                    protocol="protocol",
                    query="query",
                    status_code="statusCode"
                ),
                target_group_arn="targetGroupArn",
                type="type"
            )],
            listener_attributes=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ListenerAttributeProperty(
                key="key",
                value="value"
            )],
            load_balancer_arn="loadBalancerArn",
            mutual_authentication=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.MutualAuthenticationProperty(
                advertise_trust_store_ca_names="advertiseTrustStoreCaNames",
                ignore_client_certificate_expiry=False,
                mode="mode",
                trust_store_arn="trustStoreArn"
            ),
            port=123,
            protocol="protocol",
            ssl_policy="sslPolicy"
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
        '''Create a mixin to apply properties to ``AWS::ElasticLoadBalancingV2::Listener``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611b2b4e1db18db78ba3801600a74f03b790c74ceb3d08b9afa7e1b4d9e97d3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b741337cb3742f325e9b5a9dd202eb0264c0d65b92011415d7dc94eb783cc63d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138efa762549808ca303d6c600cb4445426bd2dbdaea7ea4269e1650b1ad2564)
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
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authenticate_cognito_config": "authenticateCognitoConfig",
            "authenticate_oidc_config": "authenticateOidcConfig",
            "fixed_response_config": "fixedResponseConfig",
            "forward_config": "forwardConfig",
            "jwt_validation_config": "jwtValidationConfig",
            "order": "order",
            "redirect_config": "redirectConfig",
            "target_group_arn": "targetGroupArn",
            "type": "type",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            authenticate_cognito_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.AuthenticateCognitoConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            authenticate_oidc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.AuthenticateOidcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fixed_response_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.FixedResponseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            forward_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.ForwardConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            jwt_validation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.JwtValidationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            order: typing.Optional[jsii.Number] = None,
            redirect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.RedirectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_group_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an action for a listener rule.

            :param authenticate_cognito_config: [HTTPS listeners] Information for using Amazon Cognito to authenticate users. Specify only when ``Type`` is ``authenticate-cognito`` .
            :param authenticate_oidc_config: [HTTPS listeners] Information about an identity provider that is compliant with OpenID Connect (OIDC). Specify only when ``Type`` is ``authenticate-oidc`` .
            :param fixed_response_config: [Application Load Balancer] Information for creating an action that returns a custom HTTP response. Specify only when ``Type`` is ``fixed-response`` .
            :param forward_config: Information for creating an action that distributes requests among multiple target groups. Specify only when ``Type`` is ``forward`` . If you specify both ``ForwardConfig`` and ``TargetGroupArn`` , you can specify only one target group using ``ForwardConfig`` and it must be the same target group specified in ``TargetGroupArn`` .
            :param jwt_validation_config: [HTTPS listeners] Information for validating JWT access tokens in client requests. Specify only when ``Type`` is ``jwt-validation`` .
            :param order: The order for the action. This value is required for rules with multiple actions. The action with the lowest value for order is performed first.
            :param redirect_config: [Application Load Balancer] Information for creating a redirect action. Specify only when ``Type`` is ``redirect`` .
            :param target_group_arn: The Amazon Resource Name (ARN) of the target group. Specify only when ``Type`` is ``forward`` and you want to route to a single target group. To route to multiple target groups, you must use ``ForwardConfig`` instead.
            :param type: The type of action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                action_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ActionProperty(
                    authenticate_cognito_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.AuthenticateCognitoConfigProperty(
                        authentication_request_extra_params={
                            "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                        },
                        on_unauthenticated_request="onUnauthenticatedRequest",
                        scope="scope",
                        session_cookie_name="sessionCookieName",
                        session_timeout="sessionTimeout",
                        user_pool_arn="userPoolArn",
                        user_pool_client_id="userPoolClientId",
                        user_pool_domain="userPoolDomain"
                    ),
                    authenticate_oidc_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.AuthenticateOidcConfigProperty(
                        authentication_request_extra_params={
                            "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                        },
                        authorization_endpoint="authorizationEndpoint",
                        client_id="clientId",
                        client_secret="clientSecret",
                        issuer="issuer",
                        on_unauthenticated_request="onUnauthenticatedRequest",
                        scope="scope",
                        session_cookie_name="sessionCookieName",
                        session_timeout="sessionTimeout",
                        token_endpoint="tokenEndpoint",
                        use_existing_client_secret=False,
                        user_info_endpoint="userInfoEndpoint"
                    ),
                    fixed_response_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.FixedResponseConfigProperty(
                        content_type="contentType",
                        message_body="messageBody",
                        status_code="statusCode"
                    ),
                    forward_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ForwardConfigProperty(
                        target_groups=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupTupleProperty(
                            target_group_arn="targetGroupArn",
                            weight=123
                        )],
                        target_group_stickiness_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupStickinessConfigProperty(
                            duration_seconds=123,
                            enabled=False
                        )
                    ),
                    jwt_validation_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.JwtValidationConfigProperty(
                        additional_claims=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty(
                            format="format",
                            name="name",
                            values=["values"]
                        )],
                        issuer="issuer",
                        jwks_endpoint="jwksEndpoint"
                    ),
                    order=123,
                    redirect_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.RedirectConfigProperty(
                        host="host",
                        path="path",
                        port="port",
                        protocol="protocol",
                        query="query",
                        status_code="statusCode"
                    ),
                    target_group_arn="targetGroupArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb6ae4e175bcc0b912c38eb71850cf0605c31e0949744750bbe30d5a50c3491d)
                check_type(argname="argument authenticate_cognito_config", value=authenticate_cognito_config, expected_type=type_hints["authenticate_cognito_config"])
                check_type(argname="argument authenticate_oidc_config", value=authenticate_oidc_config, expected_type=type_hints["authenticate_oidc_config"])
                check_type(argname="argument fixed_response_config", value=fixed_response_config, expected_type=type_hints["fixed_response_config"])
                check_type(argname="argument forward_config", value=forward_config, expected_type=type_hints["forward_config"])
                check_type(argname="argument jwt_validation_config", value=jwt_validation_config, expected_type=type_hints["jwt_validation_config"])
                check_type(argname="argument order", value=order, expected_type=type_hints["order"])
                check_type(argname="argument redirect_config", value=redirect_config, expected_type=type_hints["redirect_config"])
                check_type(argname="argument target_group_arn", value=target_group_arn, expected_type=type_hints["target_group_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authenticate_cognito_config is not None:
                self._values["authenticate_cognito_config"] = authenticate_cognito_config
            if authenticate_oidc_config is not None:
                self._values["authenticate_oidc_config"] = authenticate_oidc_config
            if fixed_response_config is not None:
                self._values["fixed_response_config"] = fixed_response_config
            if forward_config is not None:
                self._values["forward_config"] = forward_config
            if jwt_validation_config is not None:
                self._values["jwt_validation_config"] = jwt_validation_config
            if order is not None:
                self._values["order"] = order
            if redirect_config is not None:
                self._values["redirect_config"] = redirect_config
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def authenticate_cognito_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.AuthenticateCognitoConfigProperty"]]:
            '''[HTTPS listeners] Information for using Amazon Cognito to authenticate users.

            Specify only when ``Type`` is ``authenticate-cognito`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-authenticatecognitoconfig
            '''
            result = self._values.get("authenticate_cognito_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.AuthenticateCognitoConfigProperty"]], result)

        @builtins.property
        def authenticate_oidc_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.AuthenticateOidcConfigProperty"]]:
            '''[HTTPS listeners] Information about an identity provider that is compliant with OpenID Connect (OIDC).

            Specify only when ``Type`` is ``authenticate-oidc`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-authenticateoidcconfig
            '''
            result = self._values.get("authenticate_oidc_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.AuthenticateOidcConfigProperty"]], result)

        @builtins.property
        def fixed_response_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.FixedResponseConfigProperty"]]:
            '''[Application Load Balancer] Information for creating an action that returns a custom HTTP response.

            Specify only when ``Type`` is ``fixed-response`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-fixedresponseconfig
            '''
            result = self._values.get("fixed_response_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.FixedResponseConfigProperty"]], result)

        @builtins.property
        def forward_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.ForwardConfigProperty"]]:
            '''Information for creating an action that distributes requests among multiple target groups. Specify only when ``Type`` is ``forward`` .

            If you specify both ``ForwardConfig`` and ``TargetGroupArn`` , you can specify only one target group using ``ForwardConfig`` and it must be the same target group specified in ``TargetGroupArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-forwardconfig
            '''
            result = self._values.get("forward_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.ForwardConfigProperty"]], result)

        @builtins.property
        def jwt_validation_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.JwtValidationConfigProperty"]]:
            '''[HTTPS listeners] Information for validating JWT access tokens in client requests.

            Specify only when ``Type`` is ``jwt-validation`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-jwtvalidationconfig
            '''
            result = self._values.get("jwt_validation_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.JwtValidationConfigProperty"]], result)

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            '''The order for the action.

            This value is required for rules with multiple actions. The action with the lowest value for order is performed first.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-order
            '''
            result = self._values.get("order")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def redirect_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.RedirectConfigProperty"]]:
            '''[Application Load Balancer] Information for creating a redirect action.

            Specify only when ``Type`` is ``redirect`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-redirectconfig
            '''
            result = self._values.get("redirect_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.RedirectConfigProperty"]], result)

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the target group.

            Specify only when ``Type`` is ``forward`` and you want to route to a single target group. To route to multiple target groups, you must use ``ForwardConfig`` instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-targetgrouparn
            '''
            result = self._values.get("target_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-action.html#cfn-elasticloadbalancingv2-listener-action-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.AuthenticateCognitoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
            "user_pool_arn": "userPoolArn",
            "user_pool_client_id": "userPoolClientId",
            "user_pool_domain": "userPoolDomain",
        },
    )
    class AuthenticateCognitoConfigProperty:
        def __init__(
            self,
            *,
            authentication_request_extra_params: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[builtins.str] = None,
            user_pool_arn: typing.Optional[builtins.str] = None,
            user_pool_client_id: typing.Optional[builtins.str] = None,
            user_pool_domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information required when integrating with Amazon Cognito to authenticate users.

            :param authentication_request_extra_params: The query parameters (up to 10) to include in the redirect request to the authorization endpoint.
            :param on_unauthenticated_request: The behavior if the user is not authenticated. The following are possible values:. - deny `` - Return an HTTP 401 Unauthorized error. - allow `` - Allow the request to be forwarded to the target. - authenticate `` - Redirect the request to the IdP authorization endpoint. This is the default value.
            :param scope: The set of user claims to be requested from the IdP. The default is ``openid`` . To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.
            :param session_cookie_name: The name of the cookie used to maintain session information. The default is AWSELBAuthSessionCookie.
            :param session_timeout: The maximum duration of the authentication session, in seconds. The default is 604800 seconds (7 days).
            :param user_pool_arn: The Amazon Resource Name (ARN) of the Amazon Cognito user pool.
            :param user_pool_client_id: The ID of the Amazon Cognito user pool client.
            :param user_pool_domain: The domain prefix or fully-qualified domain name of the Amazon Cognito user pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                authenticate_cognito_config_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.AuthenticateCognitoConfigProperty(
                    authentication_request_extra_params={
                        "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                    },
                    on_unauthenticated_request="onUnauthenticatedRequest",
                    scope="scope",
                    session_cookie_name="sessionCookieName",
                    session_timeout="sessionTimeout",
                    user_pool_arn="userPoolArn",
                    user_pool_client_id="userPoolClientId",
                    user_pool_domain="userPoolDomain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b98fb1886a3f069e3ea658db4c42aa2259b299948743e3891aba72e7c72d36de)
                check_type(argname="argument authentication_request_extra_params", value=authentication_request_extra_params, expected_type=type_hints["authentication_request_extra_params"])
                check_type(argname="argument on_unauthenticated_request", value=on_unauthenticated_request, expected_type=type_hints["on_unauthenticated_request"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument session_cookie_name", value=session_cookie_name, expected_type=type_hints["session_cookie_name"])
                check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
                check_type(argname="argument user_pool_arn", value=user_pool_arn, expected_type=type_hints["user_pool_arn"])
                check_type(argname="argument user_pool_client_id", value=user_pool_client_id, expected_type=type_hints["user_pool_client_id"])
                check_type(argname="argument user_pool_domain", value=user_pool_domain, expected_type=type_hints["user_pool_domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout
            if user_pool_arn is not None:
                self._values["user_pool_arn"] = user_pool_arn
            if user_pool_client_id is not None:
                self._values["user_pool_client_id"] = user_pool_client_id
            if user_pool_domain is not None:
                self._values["user_pool_domain"] = user_pool_domain

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The query parameters (up to 10) to include in the redirect request to the authorization endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-authenticationrequestextraparams
            '''
            result = self._values.get("authentication_request_extra_params")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            '''The behavior if the user is not authenticated. The following are possible values:.

            - deny `` - Return an HTTP 401 Unauthorized error.
            - allow `` - Allow the request to be forwarded to the target.
            - authenticate `` - Redirect the request to the IdP authorization endpoint. This is the default value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-onunauthenticatedrequest
            '''
            result = self._values.get("on_unauthenticated_request")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The set of user claims to be requested from the IdP. The default is ``openid`` .

            To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            '''The name of the cookie used to maintain session information.

            The default is AWSELBAuthSessionCookie.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessioncookiename
            '''
            result = self._values.get("session_cookie_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[builtins.str]:
            '''The maximum duration of the authentication session, in seconds.

            The default is 604800 seconds (7 days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Cognito user pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolarn
            '''
            result = self._values.get("user_pool_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_client_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the Amazon Cognito user pool client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpoolclientid
            '''
            result = self._values.get("user_pool_client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_domain(self) -> typing.Optional[builtins.str]:
            '''The domain prefix or fully-qualified domain name of the Amazon Cognito user pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listener-authenticatecognitoconfig-userpooldomain
            '''
            result = self._values.get("user_pool_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateCognitoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.AuthenticateOidcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "authorization_endpoint": "authorizationEndpoint",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "issuer": "issuer",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
            "token_endpoint": "tokenEndpoint",
            "use_existing_client_secret": "useExistingClientSecret",
            "user_info_endpoint": "userInfoEndpoint",
        },
    )
    class AuthenticateOidcConfigProperty:
        def __init__(
            self,
            *,
            authentication_request_extra_params: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            authorization_endpoint: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            issuer: typing.Optional[builtins.str] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[builtins.str] = None,
            token_endpoint: typing.Optional[builtins.str] = None,
            use_existing_client_secret: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            user_info_endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information required using an identity provide (IdP) that is compliant with OpenID Connect (OIDC) to authenticate users.

            :param authentication_request_extra_params: The query parameters (up to 10) to include in the redirect request to the authorization endpoint.
            :param authorization_endpoint: The authorization endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
            :param client_id: The OAuth 2.0 client identifier.
            :param client_secret: The OAuth 2.0 client secret. This parameter is required if you are creating a rule. If you are modifying a rule, you can omit this parameter if you set ``UseExistingClientSecret`` to true.
            :param issuer: The OIDC issuer identifier of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
            :param on_unauthenticated_request: The behavior if the user is not authenticated. The following are possible values:. - deny `` - Return an HTTP 401 Unauthorized error. - allow `` - Allow the request to be forwarded to the target. - authenticate `` - Redirect the request to the IdP authorization endpoint. This is the default value.
            :param scope: The set of user claims to be requested from the IdP. The default is ``openid`` . To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.
            :param session_cookie_name: The name of the cookie used to maintain session information. The default is AWSELBAuthSessionCookie.
            :param session_timeout: The maximum duration of the authentication session, in seconds. The default is 604800 seconds (7 days).
            :param token_endpoint: The token endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
            :param use_existing_client_secret: Indicates whether to use the existing client secret when modifying a rule. If you are creating a rule, you can omit this parameter or set it to false.
            :param user_info_endpoint: The user info endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                authenticate_oidc_config_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.AuthenticateOidcConfigProperty(
                    authentication_request_extra_params={
                        "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                    },
                    authorization_endpoint="authorizationEndpoint",
                    client_id="clientId",
                    client_secret="clientSecret",
                    issuer="issuer",
                    on_unauthenticated_request="onUnauthenticatedRequest",
                    scope="scope",
                    session_cookie_name="sessionCookieName",
                    session_timeout="sessionTimeout",
                    token_endpoint="tokenEndpoint",
                    use_existing_client_secret=False,
                    user_info_endpoint="userInfoEndpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f1bc80f9f9f49c0c4bf22eaf904be3c7a3c050e4dfdd476c7661c05ceebbd7a)
                check_type(argname="argument authentication_request_extra_params", value=authentication_request_extra_params, expected_type=type_hints["authentication_request_extra_params"])
                check_type(argname="argument authorization_endpoint", value=authorization_endpoint, expected_type=type_hints["authorization_endpoint"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
                check_type(argname="argument on_unauthenticated_request", value=on_unauthenticated_request, expected_type=type_hints["on_unauthenticated_request"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument session_cookie_name", value=session_cookie_name, expected_type=type_hints["session_cookie_name"])
                check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
                check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
                check_type(argname="argument use_existing_client_secret", value=use_existing_client_secret, expected_type=type_hints["use_existing_client_secret"])
                check_type(argname="argument user_info_endpoint", value=user_info_endpoint, expected_type=type_hints["user_info_endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if authorization_endpoint is not None:
                self._values["authorization_endpoint"] = authorization_endpoint
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if issuer is not None:
                self._values["issuer"] = issuer
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout
            if token_endpoint is not None:
                self._values["token_endpoint"] = token_endpoint
            if use_existing_client_secret is not None:
                self._values["use_existing_client_secret"] = use_existing_client_secret
            if user_info_endpoint is not None:
                self._values["user_info_endpoint"] = user_info_endpoint

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The query parameters (up to 10) to include in the redirect request to the authorization endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authenticationrequestextraparams
            '''
            result = self._values.get("authentication_request_extra_params")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def authorization_endpoint(self) -> typing.Optional[builtins.str]:
            '''The authorization endpoint of the IdP.

            This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-authorizationendpoint
            '''
            result = self._values.get("authorization_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The OAuth 2.0 client identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The OAuth 2.0 client secret. This parameter is required if you are creating a rule. If you are modifying a rule, you can omit this parameter if you set ``UseExistingClientSecret`` to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The OIDC issuer identifier of the IdP.

            This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            '''The behavior if the user is not authenticated. The following are possible values:.

            - deny `` - Return an HTTP 401 Unauthorized error.
            - allow `` - Allow the request to be forwarded to the target.
            - authenticate `` - Redirect the request to the IdP authorization endpoint. This is the default value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-onunauthenticatedrequest
            '''
            result = self._values.get("on_unauthenticated_request")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The set of user claims to be requested from the IdP. The default is ``openid`` .

            To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            '''The name of the cookie used to maintain session information.

            The default is AWSELBAuthSessionCookie.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessioncookiename
            '''
            result = self._values.get("session_cookie_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[builtins.str]:
            '''The maximum duration of the authentication session, in seconds.

            The default is 604800 seconds (7 days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_endpoint(self) -> typing.Optional[builtins.str]:
            '''The token endpoint of the IdP.

            This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-tokenendpoint
            '''
            result = self._values.get("token_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_existing_client_secret(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to use the existing client secret when modifying a rule.

            If you are creating a rule, you can omit this parameter or set it to false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-useexistingclientsecret
            '''
            result = self._values.get("use_existing_client_secret")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def user_info_endpoint(self) -> typing.Optional[builtins.str]:
            '''The user info endpoint of the IdP.

            This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listener-authenticateoidcconfig-userinfoendpoint
            '''
            result = self._values.get("user_info_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateOidcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.CertificateProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_arn": "certificateArn"},
    )
    class CertificateProperty:
        def __init__(
            self,
            *,
            certificate_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an SSL server certificate to use as the default certificate for a secure listener.

            :param certificate_arn: The Amazon Resource Name (ARN) of the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                certificate_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.CertificateProperty(
                    certificate_arn="certificateArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9a8febd7d4e4609847159309ef3f72605700533e5fd8be5c05bcdda2f456eb0)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-certificate.html#cfn-elasticloadbalancingv2-listener-certificate-certificatearn
            '''
            result = self._values.get("certificate_arn")
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
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.FixedResponseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content_type": "contentType",
            "message_body": "messageBody",
            "status_code": "statusCode",
        },
    )
    class FixedResponseConfigProperty:
        def __init__(
            self,
            *,
            content_type: typing.Optional[builtins.str] = None,
            message_body: typing.Optional[builtins.str] = None,
            status_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information required when returning a custom HTTP response.

            :param content_type: The content type. Valid Values: text/plain | text/css | text/html | application/javascript | application/json
            :param message_body: The message.
            :param status_code: The HTTP response code (2XX, 4XX, or 5XX).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                fixed_response_config_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.FixedResponseConfigProperty(
                    content_type="contentType",
                    message_body="messageBody",
                    status_code="statusCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__720f82e9d76e0fe00881e4ed805683d1871292b734e79d3bb8f2a449366a7541)
                check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
                check_type(argname="argument message_body", value=message_body, expected_type=type_hints["message_body"])
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content_type is not None:
                self._values["content_type"] = content_type
            if message_body is not None:
                self._values["message_body"] = message_body
            if status_code is not None:
                self._values["status_code"] = status_code

        @builtins.property
        def content_type(self) -> typing.Optional[builtins.str]:
            '''The content type.

            Valid Values: text/plain | text/css | text/html | application/javascript | application/json

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-contenttype
            '''
            result = self._values.get("content_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_body(self) -> typing.Optional[builtins.str]:
            '''The message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-messagebody
            '''
            result = self._values.get("message_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_code(self) -> typing.Optional[builtins.str]:
            '''The HTTP response code (2XX, 4XX, or 5XX).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listener-fixedresponseconfig-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.ForwardConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_groups": "targetGroups",
            "target_group_stickiness_config": "targetGroupStickinessConfig",
        },
    )
    class ForwardConfigProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.TargetGroupTupleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            target_group_stickiness_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.TargetGroupStickinessConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information for creating an action that distributes requests among multiple target groups. Specify only when ``Type`` is ``forward`` .

            If you specify both ``ForwardConfig`` and ``TargetGroupArn`` , you can specify only one target group using ``ForwardConfig`` and it must be the same target group specified in ``TargetGroupArn`` .

            :param target_groups: Information about how traffic will be distributed between multiple target groups in a forward rule.
            :param target_group_stickiness_config: Information about the target group stickiness for a rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-forwardconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                forward_config_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ForwardConfigProperty(
                    target_groups=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupTupleProperty(
                        target_group_arn="targetGroupArn",
                        weight=123
                    )],
                    target_group_stickiness_config=elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupStickinessConfigProperty(
                        duration_seconds=123,
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eba4fa84071e1576afe45fd42f5750c3f883e20780a6d4f2c9103e0b20d13757)
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
                check_type(argname="argument target_group_stickiness_config", value=target_group_stickiness_config, expected_type=type_hints["target_group_stickiness_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_groups is not None:
                self._values["target_groups"] = target_groups
            if target_group_stickiness_config is not None:
                self._values["target_group_stickiness_config"] = target_group_stickiness_config

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.TargetGroupTupleProperty"]]]]:
            '''Information about how traffic will be distributed between multiple target groups in a forward rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-forwardconfig.html#cfn-elasticloadbalancingv2-listener-forwardconfig-targetgroups
            '''
            result = self._values.get("target_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.TargetGroupTupleProperty"]]]], result)

        @builtins.property
        def target_group_stickiness_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.TargetGroupStickinessConfigProperty"]]:
            '''Information about the target group stickiness for a rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-forwardconfig.html#cfn-elasticloadbalancingv2-listener-forwardconfig-targetgroupstickinessconfig
            '''
            result = self._values.get("target_group_stickiness_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.TargetGroupStickinessConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty",
        jsii_struct_bases=[],
        name_mapping={"format": "format", "name": "name", "values": "values"},
    )
    class JwtValidationActionAdditionalClaimProperty:
        def __init__(
            self,
            *,
            format: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about an additional claim to validate.

            :param format: The format of the claim value.
            :param name: The name of the claim. You can't specify ``exp`` , ``iss`` , ``nbf`` , or ``iat`` because we validate them by default.
            :param values: The claim value. The maximum size of the list is 10. Each value can be up to 256 characters in length. If the format is ``space-separated-values`` , the values can't include spaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-jwtvalidationactionadditionalclaim.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                jwt_validation_action_additional_claim_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty(
                    format="format",
                    name="name",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ca6baf40c1611e72da9e6c172ce9ed97e9c666f3c6932883342baf029dd9d1a)
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if format is not None:
                self._values["format"] = format
            if name is not None:
                self._values["name"] = name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''The format of the claim value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-jwtvalidationactionadditionalclaim.html#cfn-elasticloadbalancingv2-listener-jwtvalidationactionadditionalclaim-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the claim.

            You can't specify ``exp`` , ``iss`` , ``nbf`` , or ``iat`` because we validate them by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-jwtvalidationactionadditionalclaim.html#cfn-elasticloadbalancingv2-listener-jwtvalidationactionadditionalclaim-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The claim value.

            The maximum size of the list is 10. Each value can be up to 256 characters in length. If the format is ``space-separated-values`` , the values can't include spaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-jwtvalidationactionadditionalclaim.html#cfn-elasticloadbalancingv2-listener-jwtvalidationactionadditionalclaim-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JwtValidationActionAdditionalClaimProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.JwtValidationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_claims": "additionalClaims",
            "issuer": "issuer",
            "jwks_endpoint": "jwksEndpoint",
        },
    )
    class JwtValidationConfigProperty:
        def __init__(
            self,
            *,
            additional_claims: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            issuer: typing.Optional[builtins.str] = None,
            jwks_endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param additional_claims: 
            :param issuer: 
            :param jwks_endpoint: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-jwtvalidationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                jwt_validation_config_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.JwtValidationConfigProperty(
                    additional_claims=[elasticloadbalancingv2_mixins.CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty(
                        format="format",
                        name="name",
                        values=["values"]
                    )],
                    issuer="issuer",
                    jwks_endpoint="jwksEndpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cffddb1d47dc3f20a4e25c1b9d989d83c711537563cd49a742ea8456c1f72387)
                check_type(argname="argument additional_claims", value=additional_claims, expected_type=type_hints["additional_claims"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
                check_type(argname="argument jwks_endpoint", value=jwks_endpoint, expected_type=type_hints["jwks_endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_claims is not None:
                self._values["additional_claims"] = additional_claims
            if issuer is not None:
                self._values["issuer"] = issuer
            if jwks_endpoint is not None:
                self._values["jwks_endpoint"] = jwks_endpoint

        @builtins.property
        def additional_claims(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-jwtvalidationconfig.html#cfn-elasticloadbalancingv2-listener-jwtvalidationconfig-additionalclaims
            '''
            result = self._values.get("additional_claims")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty"]]]], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-jwtvalidationconfig.html#cfn-elasticloadbalancingv2-listener-jwtvalidationconfig-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def jwks_endpoint(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-jwtvalidationconfig.html#cfn-elasticloadbalancingv2-listener-jwtvalidationconfig-jwksendpoint
            '''
            result = self._values.get("jwks_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JwtValidationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.ListenerAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ListenerAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a listener attribute.

            :param key: The name of the attribute. The following attribute is supported by Network Load Balancers, and Gateway Load Balancers. - ``tcp.idle_timeout.seconds`` - The tcp idle timeout value, in seconds. The valid range is 60-6000 seconds. The default is 350 seconds. The following attributes are only supported by Application Load Balancers. - ``routing.http.request.x_amzn_mtls_clientcert_serial_number.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Serial-Number* HTTP request header. - ``routing.http.request.x_amzn_mtls_clientcert_issuer.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Issuer* HTTP request header. - ``routing.http.request.x_amzn_mtls_clientcert_subject.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Subject* HTTP request header. - ``routing.http.request.x_amzn_mtls_clientcert_validity.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Validity* HTTP request header. - ``routing.http.request.x_amzn_mtls_clientcert_leaf.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Leaf* HTTP request header. - ``routing.http.request.x_amzn_mtls_clientcert.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert* HTTP request header. - ``routing.http.request.x_amzn_tls_version.header_name`` - Enables you to modify the header name of the *X-Amzn-Tls-Version* HTTP request header. - ``routing.http.request.x_amzn_tls_cipher_suite.header_name`` - Enables you to modify the header name of the *X-Amzn-Tls-Cipher-Suite* HTTP request header. - ``routing.http.response.server.enabled`` - Enables you to allow or remove the HTTP response server header. - ``routing.http.response.strict_transport_security.header_value`` - Informs browsers that the site should only be accessed using HTTPS, and that any future attempts to access it using HTTP should automatically be converted to HTTPS. - ``routing.http.response.access_control_allow_origin.header_value`` - Specifies which origins are allowed to access the server. - ``routing.http.response.access_control_allow_methods.header_value`` - Returns which HTTP methods are allowed when accessing the server from a different origin. - ``routing.http.response.access_control_allow_headers.header_value`` - Specifies which headers can be used during the request. - ``routing.http.response.access_control_allow_credentials.header_value`` - Indicates whether the browser should include credentials such as cookies or authentication when making requests. - ``routing.http.response.access_control_expose_headers.header_value`` - Returns which headers the browser can expose to the requesting client. - ``routing.http.response.access_control_max_age.header_value`` - Specifies how long the results of a preflight request can be cached, in seconds. - ``routing.http.response.content_security_policy.header_value`` - Specifies restrictions enforced by the browser to help minimize the risk of certain types of security threats. - ``routing.http.response.x_content_type_options.header_value`` - Indicates whether the MIME types advertised in the *Content-Type* headers should be followed and not be changed. - ``routing.http.response.x_frame_options.header_value`` - Indicates whether the browser is allowed to render a page in a *frame* , *iframe* , *embed* or *object* .
            :param value: The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-listenerattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                listener_attribute_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.ListenerAttributeProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2bda0779c9d7a9a7f6f294c5910ffb7406dc222fd98399051ce81254faff668)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute.

            The following attribute is supported by Network Load Balancers, and Gateway Load Balancers.

            - ``tcp.idle_timeout.seconds`` - The tcp idle timeout value, in seconds. The valid range is 60-6000 seconds. The default is 350 seconds.

            The following attributes are only supported by Application Load Balancers.

            - ``routing.http.request.x_amzn_mtls_clientcert_serial_number.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Serial-Number* HTTP request header.
            - ``routing.http.request.x_amzn_mtls_clientcert_issuer.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Issuer* HTTP request header.
            - ``routing.http.request.x_amzn_mtls_clientcert_subject.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Subject* HTTP request header.
            - ``routing.http.request.x_amzn_mtls_clientcert_validity.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Validity* HTTP request header.
            - ``routing.http.request.x_amzn_mtls_clientcert_leaf.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert-Leaf* HTTP request header.
            - ``routing.http.request.x_amzn_mtls_clientcert.header_name`` - Enables you to modify the header name of the *X-Amzn-Mtls-Clientcert* HTTP request header.
            - ``routing.http.request.x_amzn_tls_version.header_name`` - Enables you to modify the header name of the *X-Amzn-Tls-Version* HTTP request header.
            - ``routing.http.request.x_amzn_tls_cipher_suite.header_name`` - Enables you to modify the header name of the *X-Amzn-Tls-Cipher-Suite* HTTP request header.
            - ``routing.http.response.server.enabled`` - Enables you to allow or remove the HTTP response server header.
            - ``routing.http.response.strict_transport_security.header_value`` - Informs browsers that the site should only be accessed using HTTPS, and that any future attempts to access it using HTTP should automatically be converted to HTTPS.
            - ``routing.http.response.access_control_allow_origin.header_value`` - Specifies which origins are allowed to access the server.
            - ``routing.http.response.access_control_allow_methods.header_value`` - Returns which HTTP methods are allowed when accessing the server from a different origin.
            - ``routing.http.response.access_control_allow_headers.header_value`` - Specifies which headers can be used during the request.
            - ``routing.http.response.access_control_allow_credentials.header_value`` - Indicates whether the browser should include credentials such as cookies or authentication when making requests.
            - ``routing.http.response.access_control_expose_headers.header_value`` - Returns which headers the browser can expose to the requesting client.
            - ``routing.http.response.access_control_max_age.header_value`` - Specifies how long the results of a preflight request can be cached, in seconds.
            - ``routing.http.response.content_security_policy.header_value`` - Specifies restrictions enforced by the browser to help minimize the risk of certain types of security threats.
            - ``routing.http.response.x_content_type_options.header_value`` - Indicates whether the MIME types advertised in the *Content-Type* headers should be followed and not be changed.
            - ``routing.http.response.x_frame_options.header_value`` - Indicates whether the browser is allowed to render a page in a *frame* , *iframe* , *embed* or *object* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-listenerattribute.html#cfn-elasticloadbalancingv2-listener-listenerattribute-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-listenerattribute.html#cfn-elasticloadbalancingv2-listener-listenerattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListenerAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.MutualAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "advertise_trust_store_ca_names": "advertiseTrustStoreCaNames",
            "ignore_client_certificate_expiry": "ignoreClientCertificateExpiry",
            "mode": "mode",
            "trust_store_arn": "trustStoreArn",
        },
    )
    class MutualAuthenticationProperty:
        def __init__(
            self,
            *,
            advertise_trust_store_ca_names: typing.Optional[builtins.str] = None,
            ignore_client_certificate_expiry: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            mode: typing.Optional[builtins.str] = None,
            trust_store_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The mutual authentication configuration information.

            :param advertise_trust_store_ca_names: Indicates whether trust store CA certificate names are advertised.
            :param ignore_client_certificate_expiry: Indicates whether expired client certificates are ignored.
            :param mode: The client certificate handling method. Options are ``off`` , ``passthrough`` or ``verify`` . The default value is ``off`` .
            :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-mutualauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                mutual_authentication_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.MutualAuthenticationProperty(
                    advertise_trust_store_ca_names="advertiseTrustStoreCaNames",
                    ignore_client_certificate_expiry=False,
                    mode="mode",
                    trust_store_arn="trustStoreArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da49eeb51af3bf6cf7086262ea378fe86da5a86d61f0d3977969352b27a45c30)
                check_type(argname="argument advertise_trust_store_ca_names", value=advertise_trust_store_ca_names, expected_type=type_hints["advertise_trust_store_ca_names"])
                check_type(argname="argument ignore_client_certificate_expiry", value=ignore_client_certificate_expiry, expected_type=type_hints["ignore_client_certificate_expiry"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument trust_store_arn", value=trust_store_arn, expected_type=type_hints["trust_store_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if advertise_trust_store_ca_names is not None:
                self._values["advertise_trust_store_ca_names"] = advertise_trust_store_ca_names
            if ignore_client_certificate_expiry is not None:
                self._values["ignore_client_certificate_expiry"] = ignore_client_certificate_expiry
            if mode is not None:
                self._values["mode"] = mode
            if trust_store_arn is not None:
                self._values["trust_store_arn"] = trust_store_arn

        @builtins.property
        def advertise_trust_store_ca_names(self) -> typing.Optional[builtins.str]:
            '''Indicates whether trust store CA certificate names are advertised.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-mutualauthentication.html#cfn-elasticloadbalancingv2-listener-mutualauthentication-advertisetruststorecanames
            '''
            result = self._values.get("advertise_trust_store_ca_names")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ignore_client_certificate_expiry(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether expired client certificates are ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-mutualauthentication.html#cfn-elasticloadbalancingv2-listener-mutualauthentication-ignoreclientcertificateexpiry
            '''
            result = self._values.get("ignore_client_certificate_expiry")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The client certificate handling method.

            Options are ``off`` , ``passthrough`` or ``verify`` . The default value is ``off`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-mutualauthentication.html#cfn-elasticloadbalancingv2-listener-mutualauthentication-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trust_store_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the trust store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-mutualauthentication.html#cfn-elasticloadbalancingv2-listener-mutualauthentication-truststorearn
            '''
            result = self._values.get("trust_store_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutualAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.RedirectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "host": "host",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "query": "query",
            "status_code": "statusCode",
        },
    )
    class RedirectConfigProperty:
        def __init__(
            self,
            *,
            host: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            query: typing.Optional[builtins.str] = None,
            status_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a redirect action.

            A URI consists of the following components: protocol://hostname:port/path?query. You must modify at least one of the following components to avoid a redirect loop: protocol, hostname, port, or path. Any components that you do not modify retain their original values.

            You can reuse URI components using the following reserved keywords:

            - #{protocol}
            - #{host}
            - #{port}
            - #{path} (the leading "/" is removed)
            - #{query}

            For example, you can change the path to "/new/#{path}", the hostname to "example.#{host}", or the query to "#{query}&value=xyz".

            :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}.
            :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}.
            :param port: The port. You can specify a value from 1 to 65535 or #{port}.
            :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You can't redirect HTTPS to HTTP.
            :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords.
            :param status_code: The HTTP redirect code. The redirect is either permanent (HTTP 301) or temporary (HTTP 302).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                redirect_config_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.RedirectConfigProperty(
                    host="host",
                    path="path",
                    port="port",
                    protocol="protocol",
                    query="query",
                    status_code="statusCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db2a3315d2d259b2825b700441a6286a8ff73072084c23213ccb8298f5cfbde2)
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument query", value=query, expected_type=type_hints["query"])
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if host is not None:
                self._values["host"] = host
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if query is not None:
                self._values["query"] = query
            if status_code is not None:
                self._values["status_code"] = status_code

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''The hostname.

            This component is not percent-encoded. The hostname can contain #{host}.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The absolute path, starting with the leading "/".

            This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port.

            You can specify a value from 1 to 65535 or #{port}.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol.

            You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You can't redirect HTTPS to HTTP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query(self) -> typing.Optional[builtins.str]:
            '''The query parameters, URL-encoded when necessary, but not percent-encoded.

            Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-query
            '''
            result = self._values.get("query")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_code(self) -> typing.Optional[builtins.str]:
            '''The HTTP redirect code.

            The redirect is either permanent (HTTP 301) or temporary (HTTP 302).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-redirectconfig.html#cfn-elasticloadbalancingv2-listener-redirectconfig-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.TargetGroupStickinessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_seconds": "durationSeconds", "enabled": "enabled"},
    )
    class TargetGroupStickinessConfigProperty:
        def __init__(
            self,
            *,
            duration_seconds: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Information about the target group stickiness for a rule.

            :param duration_seconds: [Application Load Balancers] The time period, in seconds, during which requests from a client should be routed to the same target group. The range is 1-604800 seconds (7 days). You must specify this value when enabling target group stickiness.
            :param enabled: Indicates whether target group stickiness is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgroupstickinessconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                target_group_stickiness_config_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupStickinessConfigProperty(
                    duration_seconds=123,
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfc0dc6dba13be8372e183d073e38ab39c10f63a44b0d11107184df25273942c)
                check_type(argname="argument duration_seconds", value=duration_seconds, expected_type=type_hints["duration_seconds"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_seconds is not None:
                self._values["duration_seconds"] = duration_seconds
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''[Application Load Balancers] The time period, in seconds, during which requests from a client should be routed to the same target group.

            The range is 1-604800 seconds (7 days). You must specify this value when enabling target group stickiness.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listener-targetgroupstickinessconfig-durationseconds
            '''
            result = self._values.get("duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether target group stickiness is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listener-targetgroupstickinessconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupStickinessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerPropsMixin.TargetGroupTupleProperty",
        jsii_struct_bases=[],
        name_mapping={"target_group_arn": "targetGroupArn", "weight": "weight"},
    )
    class TargetGroupTupleProperty:
        def __init__(
            self,
            *,
            target_group_arn: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about how traffic will be distributed between multiple target groups in a forward rule.

            :param target_group_arn: The Amazon Resource Name (ARN) of the target group.
            :param weight: The weight. The range is 0 to 999.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgrouptuple.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                target_group_tuple_property = elasticloadbalancingv2_mixins.CfnListenerPropsMixin.TargetGroupTupleProperty(
                    target_group_arn="targetGroupArn",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7aef165b7060984ab0cd9301bba1dddd35d809b79f0807926b788a6774871ec6)
                check_type(argname="argument target_group_arn", value=target_group_arn, expected_type=type_hints["target_group_arn"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgrouptuple.html#cfn-elasticloadbalancingv2-listener-targetgrouptuple-targetgrouparn
            '''
            result = self._values.get("target_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The weight.

            The range is 0 to 999.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listener-targetgrouptuple.html#cfn-elasticloadbalancingv2-listener-targetgrouptuple-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "conditions": "conditions",
        "listener_arn": "listenerArn",
        "priority": "priority",
        "transforms": "transforms",
    },
)
class CfnListenerRuleMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.RuleConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        listener_arn: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        transforms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.TransformProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnListenerRulePropsMixin.

        :param actions: The actions. The rule must include exactly one of the following types of actions: ``forward`` , ``fixed-response`` , or ``redirect`` , and it must be the last action to be performed. If the rule is for an HTTPS listener, it can also optionally include an authentication action.
        :param conditions: The conditions. The rule can optionally include up to one of each of the following conditions: ``http-request-method`` , ``host-header`` , ``path-pattern`` , and ``source-ip`` . A rule can also optionally include one or more of each of the following conditions: ``http-header`` and ``query-string`` .
        :param listener_arn: The Amazon Resource Name (ARN) of the listener.
        :param priority: The rule priority. A listener can't have multiple rules with the same priority. If you try to reorder rules by updating their priorities, do not specify a new priority if an existing rule already uses this priority, as this can cause an error. If you need to reuse a priority with a different rule, you must remove it as a priority first, and then specify it in a subsequent update.
        :param transforms: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
            
            cfn_listener_rule_mixin_props = elasticloadbalancingv2_mixins.CfnListenerRuleMixinProps(
                actions=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.ActionProperty(
                    authenticate_cognito_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.AuthenticateCognitoConfigProperty(
                        authentication_request_extra_params={
                            "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                        },
                        on_unauthenticated_request="onUnauthenticatedRequest",
                        scope="scope",
                        session_cookie_name="sessionCookieName",
                        session_timeout=123,
                        user_pool_arn="userPoolArn",
                        user_pool_client_id="userPoolClientId",
                        user_pool_domain="userPoolDomain"
                    ),
                    authenticate_oidc_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.AuthenticateOidcConfigProperty(
                        authentication_request_extra_params={
                            "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                        },
                        authorization_endpoint="authorizationEndpoint",
                        client_id="clientId",
                        client_secret="clientSecret",
                        issuer="issuer",
                        on_unauthenticated_request="onUnauthenticatedRequest",
                        scope="scope",
                        session_cookie_name="sessionCookieName",
                        session_timeout=123,
                        token_endpoint="tokenEndpoint",
                        use_existing_client_secret=False,
                        user_info_endpoint="userInfoEndpoint"
                    ),
                    fixed_response_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.FixedResponseConfigProperty(
                        content_type="contentType",
                        message_body="messageBody",
                        status_code="statusCode"
                    ),
                    forward_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.ForwardConfigProperty(
                        target_groups=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupTupleProperty(
                            target_group_arn="targetGroupArn",
                            weight=123
                        )],
                        target_group_stickiness_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty(
                            duration_seconds=123,
                            enabled=False
                        )
                    ),
                    jwt_validation_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.JwtValidationConfigProperty(
                        additional_claims=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty(
                            format="format",
                            name="name",
                            values=["values"]
                        )],
                        issuer="issuer",
                        jwks_endpoint="jwksEndpoint"
                    ),
                    order=123,
                    redirect_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RedirectConfigProperty(
                        host="host",
                        path="path",
                        port="port",
                        protocol="protocol",
                        query="query",
                        status_code="statusCode"
                    ),
                    target_group_arn="targetGroupArn",
                    type="type"
                )],
                conditions=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RuleConditionProperty(
                    field="field",
                    host_header_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HostHeaderConfigProperty(
                        regex_values=["regexValues"],
                        values=["values"]
                    ),
                    http_header_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HttpHeaderConfigProperty(
                        http_header_name="httpHeaderName",
                        regex_values=["regexValues"],
                        values=["values"]
                    ),
                    http_request_method_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HttpRequestMethodConfigProperty(
                        values=["values"]
                    ),
                    path_pattern_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.PathPatternConfigProperty(
                        regex_values=["regexValues"],
                        values=["values"]
                    ),
                    query_string_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.QueryStringConfigProperty(
                        values=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.QueryStringKeyValueProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    regex_values=["regexValues"],
                    source_ip_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.SourceIpConfigProperty(
                        values=["values"]
                    ),
                    values=["values"]
                )],
                listener_arn="listenerArn",
                priority=123,
                transforms=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TransformProperty(
                    host_header_rewrite_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigObjectProperty(
                        rewrites=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigProperty(
                            regex="regex",
                            replace="replace"
                        )]
                    ),
                    type="type",
                    url_rewrite_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigObjectProperty(
                        rewrites=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigProperty(
                            regex="regex",
                            replace="replace"
                        )]
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea08f4f4b1a53b43adc7323321cddd555635073ac1aa82b6c9668bdf3d94874)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument listener_arn", value=listener_arn, expected_type=type_hints["listener_arn"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument transforms", value=transforms, expected_type=type_hints["transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if conditions is not None:
            self._values["conditions"] = conditions
        if listener_arn is not None:
            self._values["listener_arn"] = listener_arn
        if priority is not None:
            self._values["priority"] = priority
        if transforms is not None:
            self._values["transforms"] = transforms

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.ActionProperty"]]]]:
        '''The actions.

        The rule must include exactly one of the following types of actions: ``forward`` , ``fixed-response`` , or ``redirect`` , and it must be the last action to be performed. If the rule is for an HTTPS listener, it can also optionally include an authentication action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.ActionProperty"]]]], result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RuleConditionProperty"]]]]:
        '''The conditions.

        The rule can optionally include up to one of each of the following conditions: ``http-request-method`` , ``host-header`` , ``path-pattern`` , and ``source-ip`` . A rule can also optionally include one or more of each of the following conditions: ``http-header`` and ``query-string`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-conditions
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RuleConditionProperty"]]]], result)

    @builtins.property
    def listener_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the listener.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-listenerarn
        '''
        result = self._values.get("listener_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The rule priority. A listener can't have multiple rules with the same priority.

        If you try to reorder rules by updating their priorities, do not specify a new priority if an existing rule already uses this priority, as this can cause an error. If you need to reuse a priority with a different rule, you must remove it as a priority first, and then specify it in a subsequent update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def transforms(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.TransformProperty"]]]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html#cfn-elasticloadbalancingv2-listenerrule-transforms
        '''
        result = self._values.get("transforms")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.TransformProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnListenerRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin",
):
    '''Specifies a listener rule.

    The listener must be associated with an Application Load Balancer. Each rule consists of a priority, one or more actions, and one or more conditions.

    For more information, see `Quotas for your Application Load Balancers <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-limits.html>`_ in the *User Guide for Application Load Balancers* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-listenerrule.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::ListenerRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
        
        cfn_listener_rule_props_mixin = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin(elasticloadbalancingv2_mixins.CfnListenerRuleMixinProps(
            actions=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.ActionProperty(
                authenticate_cognito_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.AuthenticateCognitoConfigProperty(
                    authentication_request_extra_params={
                        "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                    },
                    on_unauthenticated_request="onUnauthenticatedRequest",
                    scope="scope",
                    session_cookie_name="sessionCookieName",
                    session_timeout=123,
                    user_pool_arn="userPoolArn",
                    user_pool_client_id="userPoolClientId",
                    user_pool_domain="userPoolDomain"
                ),
                authenticate_oidc_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.AuthenticateOidcConfigProperty(
                    authentication_request_extra_params={
                        "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                    },
                    authorization_endpoint="authorizationEndpoint",
                    client_id="clientId",
                    client_secret="clientSecret",
                    issuer="issuer",
                    on_unauthenticated_request="onUnauthenticatedRequest",
                    scope="scope",
                    session_cookie_name="sessionCookieName",
                    session_timeout=123,
                    token_endpoint="tokenEndpoint",
                    use_existing_client_secret=False,
                    user_info_endpoint="userInfoEndpoint"
                ),
                fixed_response_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.FixedResponseConfigProperty(
                    content_type="contentType",
                    message_body="messageBody",
                    status_code="statusCode"
                ),
                forward_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.ForwardConfigProperty(
                    target_groups=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupTupleProperty(
                        target_group_arn="targetGroupArn",
                        weight=123
                    )],
                    target_group_stickiness_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty(
                        duration_seconds=123,
                        enabled=False
                    )
                ),
                jwt_validation_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.JwtValidationConfigProperty(
                    additional_claims=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty(
                        format="format",
                        name="name",
                        values=["values"]
                    )],
                    issuer="issuer",
                    jwks_endpoint="jwksEndpoint"
                ),
                order=123,
                redirect_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RedirectConfigProperty(
                    host="host",
                    path="path",
                    port="port",
                    protocol="protocol",
                    query="query",
                    status_code="statusCode"
                ),
                target_group_arn="targetGroupArn",
                type="type"
            )],
            conditions=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RuleConditionProperty(
                field="field",
                host_header_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HostHeaderConfigProperty(
                    regex_values=["regexValues"],
                    values=["values"]
                ),
                http_header_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HttpHeaderConfigProperty(
                    http_header_name="httpHeaderName",
                    regex_values=["regexValues"],
                    values=["values"]
                ),
                http_request_method_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HttpRequestMethodConfigProperty(
                    values=["values"]
                ),
                path_pattern_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.PathPatternConfigProperty(
                    regex_values=["regexValues"],
                    values=["values"]
                ),
                query_string_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.QueryStringConfigProperty(
                    values=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.QueryStringKeyValueProperty(
                        key="key",
                        value="value"
                    )]
                ),
                regex_values=["regexValues"],
                source_ip_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.SourceIpConfigProperty(
                    values=["values"]
                ),
                values=["values"]
            )],
            listener_arn="listenerArn",
            priority=123,
            transforms=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TransformProperty(
                host_header_rewrite_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigObjectProperty(
                    rewrites=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigProperty(
                        regex="regex",
                        replace="replace"
                    )]
                ),
                type="type",
                url_rewrite_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigObjectProperty(
                    rewrites=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigProperty(
                        regex="regex",
                        replace="replace"
                    )]
                )
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnListenerRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElasticLoadBalancingV2::ListenerRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15479d312fceb9ae3ee3d0ac0fecc320eaeb0b527d94a64253f869f31107c7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d8bb3d3ed776a4b23d9486fa5a160342b87c6dfa557d1a9a503bf9fdfeb8457)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5860e55e710d556e04fce55dc515e71f0e91b8d4f4c173e56b25c7042c871454)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnListenerRuleMixinProps:
        return typing.cast(CfnListenerRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authenticate_cognito_config": "authenticateCognitoConfig",
            "authenticate_oidc_config": "authenticateOidcConfig",
            "fixed_response_config": "fixedResponseConfig",
            "forward_config": "forwardConfig",
            "jwt_validation_config": "jwtValidationConfig",
            "order": "order",
            "redirect_config": "redirectConfig",
            "target_group_arn": "targetGroupArn",
            "type": "type",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            authenticate_cognito_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.AuthenticateCognitoConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            authenticate_oidc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.AuthenticateOidcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fixed_response_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.FixedResponseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            forward_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.ForwardConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            jwt_validation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.JwtValidationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            order: typing.Optional[jsii.Number] = None,
            redirect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.RedirectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_group_arn: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an action for a listener rule.

            :param authenticate_cognito_config: [HTTPS listeners] Information for using Amazon Cognito to authenticate users. Specify only when ``Type`` is ``authenticate-cognito`` .
            :param authenticate_oidc_config: [HTTPS listeners] Information about an identity provider that is compliant with OpenID Connect (OIDC). Specify only when ``Type`` is ``authenticate-oidc`` .
            :param fixed_response_config: [Application Load Balancer] Information for creating an action that returns a custom HTTP response. Specify only when ``Type`` is ``fixed-response`` .
            :param forward_config: Information for creating an action that distributes requests among multiple target groups. Specify only when ``Type`` is ``forward`` . If you specify both ``ForwardConfig`` and ``TargetGroupArn`` , you can specify only one target group using ``ForwardConfig`` and it must be the same target group specified in ``TargetGroupArn`` .
            :param jwt_validation_config: [HTTPS listeners] Information for validating JWT access tokens in client requests. Specify only when ``Type`` is ``jwt-validation`` .
            :param order: The order for the action. This value is required for rules with multiple actions. The action with the lowest value for order is performed first.
            :param redirect_config: [Application Load Balancer] Information for creating a redirect action. Specify only when ``Type`` is ``redirect`` .
            :param target_group_arn: The Amazon Resource Name (ARN) of the target group. Specify only when ``Type`` is ``forward`` and you want to route to a single target group. To route to multiple target groups, you must use ``ForwardConfig`` instead.
            :param type: The type of action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                action_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.ActionProperty(
                    authenticate_cognito_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.AuthenticateCognitoConfigProperty(
                        authentication_request_extra_params={
                            "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                        },
                        on_unauthenticated_request="onUnauthenticatedRequest",
                        scope="scope",
                        session_cookie_name="sessionCookieName",
                        session_timeout=123,
                        user_pool_arn="userPoolArn",
                        user_pool_client_id="userPoolClientId",
                        user_pool_domain="userPoolDomain"
                    ),
                    authenticate_oidc_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.AuthenticateOidcConfigProperty(
                        authentication_request_extra_params={
                            "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                        },
                        authorization_endpoint="authorizationEndpoint",
                        client_id="clientId",
                        client_secret="clientSecret",
                        issuer="issuer",
                        on_unauthenticated_request="onUnauthenticatedRequest",
                        scope="scope",
                        session_cookie_name="sessionCookieName",
                        session_timeout=123,
                        token_endpoint="tokenEndpoint",
                        use_existing_client_secret=False,
                        user_info_endpoint="userInfoEndpoint"
                    ),
                    fixed_response_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.FixedResponseConfigProperty(
                        content_type="contentType",
                        message_body="messageBody",
                        status_code="statusCode"
                    ),
                    forward_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.ForwardConfigProperty(
                        target_groups=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupTupleProperty(
                            target_group_arn="targetGroupArn",
                            weight=123
                        )],
                        target_group_stickiness_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty(
                            duration_seconds=123,
                            enabled=False
                        )
                    ),
                    jwt_validation_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.JwtValidationConfigProperty(
                        additional_claims=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty(
                            format="format",
                            name="name",
                            values=["values"]
                        )],
                        issuer="issuer",
                        jwks_endpoint="jwksEndpoint"
                    ),
                    order=123,
                    redirect_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RedirectConfigProperty(
                        host="host",
                        path="path",
                        port="port",
                        protocol="protocol",
                        query="query",
                        status_code="statusCode"
                    ),
                    target_group_arn="targetGroupArn",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51d0669b581ef3dd0491b5b6fa4a693a2831a56fca9272464b441db8731a2772)
                check_type(argname="argument authenticate_cognito_config", value=authenticate_cognito_config, expected_type=type_hints["authenticate_cognito_config"])
                check_type(argname="argument authenticate_oidc_config", value=authenticate_oidc_config, expected_type=type_hints["authenticate_oidc_config"])
                check_type(argname="argument fixed_response_config", value=fixed_response_config, expected_type=type_hints["fixed_response_config"])
                check_type(argname="argument forward_config", value=forward_config, expected_type=type_hints["forward_config"])
                check_type(argname="argument jwt_validation_config", value=jwt_validation_config, expected_type=type_hints["jwt_validation_config"])
                check_type(argname="argument order", value=order, expected_type=type_hints["order"])
                check_type(argname="argument redirect_config", value=redirect_config, expected_type=type_hints["redirect_config"])
                check_type(argname="argument target_group_arn", value=target_group_arn, expected_type=type_hints["target_group_arn"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authenticate_cognito_config is not None:
                self._values["authenticate_cognito_config"] = authenticate_cognito_config
            if authenticate_oidc_config is not None:
                self._values["authenticate_oidc_config"] = authenticate_oidc_config
            if fixed_response_config is not None:
                self._values["fixed_response_config"] = fixed_response_config
            if forward_config is not None:
                self._values["forward_config"] = forward_config
            if jwt_validation_config is not None:
                self._values["jwt_validation_config"] = jwt_validation_config
            if order is not None:
                self._values["order"] = order
            if redirect_config is not None:
                self._values["redirect_config"] = redirect_config
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def authenticate_cognito_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.AuthenticateCognitoConfigProperty"]]:
            '''[HTTPS listeners] Information for using Amazon Cognito to authenticate users.

            Specify only when ``Type`` is ``authenticate-cognito`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticatecognitoconfig
            '''
            result = self._values.get("authenticate_cognito_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.AuthenticateCognitoConfigProperty"]], result)

        @builtins.property
        def authenticate_oidc_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.AuthenticateOidcConfigProperty"]]:
            '''[HTTPS listeners] Information about an identity provider that is compliant with OpenID Connect (OIDC).

            Specify only when ``Type`` is ``authenticate-oidc`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-authenticateoidcconfig
            '''
            result = self._values.get("authenticate_oidc_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.AuthenticateOidcConfigProperty"]], result)

        @builtins.property
        def fixed_response_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.FixedResponseConfigProperty"]]:
            '''[Application Load Balancer] Information for creating an action that returns a custom HTTP response.

            Specify only when ``Type`` is ``fixed-response`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-fixedresponseconfig
            '''
            result = self._values.get("fixed_response_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.FixedResponseConfigProperty"]], result)

        @builtins.property
        def forward_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.ForwardConfigProperty"]]:
            '''Information for creating an action that distributes requests among multiple target groups. Specify only when ``Type`` is ``forward`` .

            If you specify both ``ForwardConfig`` and ``TargetGroupArn`` , you can specify only one target group using ``ForwardConfig`` and it must be the same target group specified in ``TargetGroupArn`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-forwardconfig
            '''
            result = self._values.get("forward_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.ForwardConfigProperty"]], result)

        @builtins.property
        def jwt_validation_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.JwtValidationConfigProperty"]]:
            '''[HTTPS listeners] Information for validating JWT access tokens in client requests.

            Specify only when ``Type`` is ``jwt-validation`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-jwtvalidationconfig
            '''
            result = self._values.get("jwt_validation_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.JwtValidationConfigProperty"]], result)

        @builtins.property
        def order(self) -> typing.Optional[jsii.Number]:
            '''The order for the action.

            This value is required for rules with multiple actions. The action with the lowest value for order is performed first.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-order
            '''
            result = self._values.get("order")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def redirect_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RedirectConfigProperty"]]:
            '''[Application Load Balancer] Information for creating a redirect action.

            Specify only when ``Type`` is ``redirect`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-redirectconfig
            '''
            result = self._values.get("redirect_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RedirectConfigProperty"]], result)

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the target group.

            Specify only when ``Type`` is ``forward`` and you want to route to a single target group. To route to multiple target groups, you must use ``ForwardConfig`` instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-targetgrouparn
            '''
            result = self._values.get("target_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-action.html#cfn-elasticloadbalancingv2-listenerrule-action-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.AuthenticateCognitoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
            "user_pool_arn": "userPoolArn",
            "user_pool_client_id": "userPoolClientId",
            "user_pool_domain": "userPoolDomain",
        },
    )
    class AuthenticateCognitoConfigProperty:
        def __init__(
            self,
            *,
            authentication_request_extra_params: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[jsii.Number] = None,
            user_pool_arn: typing.Optional[builtins.str] = None,
            user_pool_client_id: typing.Optional[builtins.str] = None,
            user_pool_domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information required when integrating with Amazon Cognito to authenticate users.

            :param authentication_request_extra_params: The query parameters (up to 10) to include in the redirect request to the authorization endpoint.
            :param on_unauthenticated_request: The behavior if the user is not authenticated. The following are possible values:. - deny `` - Return an HTTP 401 Unauthorized error. - allow `` - Allow the request to be forwarded to the target. - authenticate `` - Redirect the request to the IdP authorization endpoint. This is the default value.
            :param scope: The set of user claims to be requested from the IdP. The default is ``openid`` . To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.
            :param session_cookie_name: The name of the cookie used to maintain session information. The default is AWSELBAuthSessionCookie.
            :param session_timeout: The maximum duration of the authentication session, in seconds. The default is 604800 seconds (7 days).
            :param user_pool_arn: The Amazon Resource Name (ARN) of the Amazon Cognito user pool.
            :param user_pool_client_id: The ID of the Amazon Cognito user pool client.
            :param user_pool_domain: The domain prefix or fully-qualified domain name of the Amazon Cognito user pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                authenticate_cognito_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.AuthenticateCognitoConfigProperty(
                    authentication_request_extra_params={
                        "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                    },
                    on_unauthenticated_request="onUnauthenticatedRequest",
                    scope="scope",
                    session_cookie_name="sessionCookieName",
                    session_timeout=123,
                    user_pool_arn="userPoolArn",
                    user_pool_client_id="userPoolClientId",
                    user_pool_domain="userPoolDomain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f794b505aa15c193a9425640c0ea50b463ad07e73a7f3f7330decd52328fcbdc)
                check_type(argname="argument authentication_request_extra_params", value=authentication_request_extra_params, expected_type=type_hints["authentication_request_extra_params"])
                check_type(argname="argument on_unauthenticated_request", value=on_unauthenticated_request, expected_type=type_hints["on_unauthenticated_request"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument session_cookie_name", value=session_cookie_name, expected_type=type_hints["session_cookie_name"])
                check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
                check_type(argname="argument user_pool_arn", value=user_pool_arn, expected_type=type_hints["user_pool_arn"])
                check_type(argname="argument user_pool_client_id", value=user_pool_client_id, expected_type=type_hints["user_pool_client_id"])
                check_type(argname="argument user_pool_domain", value=user_pool_domain, expected_type=type_hints["user_pool_domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout
            if user_pool_arn is not None:
                self._values["user_pool_arn"] = user_pool_arn
            if user_pool_client_id is not None:
                self._values["user_pool_client_id"] = user_pool_client_id
            if user_pool_domain is not None:
                self._values["user_pool_domain"] = user_pool_domain

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The query parameters (up to 10) to include in the redirect request to the authorization endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-authenticationrequestextraparams
            '''
            result = self._values.get("authentication_request_extra_params")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            '''The behavior if the user is not authenticated. The following are possible values:.

            - deny `` - Return an HTTP 401 Unauthorized error.
            - allow `` - Allow the request to be forwarded to the target.
            - authenticate `` - Redirect the request to the IdP authorization endpoint. This is the default value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-onunauthenticatedrequest
            '''
            result = self._values.get("on_unauthenticated_request")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The set of user claims to be requested from the IdP. The default is ``openid`` .

            To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            '''The name of the cookie used to maintain session information.

            The default is AWSELBAuthSessionCookie.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessioncookiename
            '''
            result = self._values.get("session_cookie_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            '''The maximum duration of the authentication session, in seconds.

            The default is 604800 seconds (7 days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def user_pool_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Cognito user pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolarn
            '''
            result = self._values.get("user_pool_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_client_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the Amazon Cognito user pool client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpoolclientid
            '''
            result = self._values.get("user_pool_client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_domain(self) -> typing.Optional[builtins.str]:
            '''The domain prefix or fully-qualified domain name of the Amazon Cognito user pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticatecognitoconfig-userpooldomain
            '''
            result = self._values.get("user_pool_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateCognitoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.AuthenticateOidcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_request_extra_params": "authenticationRequestExtraParams",
            "authorization_endpoint": "authorizationEndpoint",
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "issuer": "issuer",
            "on_unauthenticated_request": "onUnauthenticatedRequest",
            "scope": "scope",
            "session_cookie_name": "sessionCookieName",
            "session_timeout": "sessionTimeout",
            "token_endpoint": "tokenEndpoint",
            "use_existing_client_secret": "useExistingClientSecret",
            "user_info_endpoint": "userInfoEndpoint",
        },
    )
    class AuthenticateOidcConfigProperty:
        def __init__(
            self,
            *,
            authentication_request_extra_params: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            authorization_endpoint: typing.Optional[builtins.str] = None,
            client_id: typing.Optional[builtins.str] = None,
            client_secret: typing.Optional[builtins.str] = None,
            issuer: typing.Optional[builtins.str] = None,
            on_unauthenticated_request: typing.Optional[builtins.str] = None,
            scope: typing.Optional[builtins.str] = None,
            session_cookie_name: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[jsii.Number] = None,
            token_endpoint: typing.Optional[builtins.str] = None,
            use_existing_client_secret: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            user_info_endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information required using an identity provide (IdP) that is compliant with OpenID Connect (OIDC) to authenticate users.

            :param authentication_request_extra_params: The query parameters (up to 10) to include in the redirect request to the authorization endpoint.
            :param authorization_endpoint: The authorization endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
            :param client_id: The OAuth 2.0 client identifier.
            :param client_secret: The OAuth 2.0 client secret. This parameter is required if you are creating a rule. If you are modifying a rule, you can omit this parameter if you set ``UseExistingClientSecret`` to true.
            :param issuer: The OIDC issuer identifier of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
            :param on_unauthenticated_request: The behavior if the user is not authenticated. The following are possible values:. - deny `` - Return an HTTP 401 Unauthorized error. - allow `` - Allow the request to be forwarded to the target. - authenticate `` - Redirect the request to the IdP authorization endpoint. This is the default value.
            :param scope: The set of user claims to be requested from the IdP. The default is ``openid`` . To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.
            :param session_cookie_name: The name of the cookie used to maintain session information. The default is AWSELBAuthSessionCookie.
            :param session_timeout: The maximum duration of the authentication session, in seconds. The default is 604800 seconds (7 days).
            :param token_endpoint: The token endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.
            :param use_existing_client_secret: Indicates whether to use the existing client secret when modifying a rule. If you are creating a rule, you can omit this parameter or set it to false.
            :param user_info_endpoint: The user info endpoint of the IdP. This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                authenticate_oidc_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.AuthenticateOidcConfigProperty(
                    authentication_request_extra_params={
                        "authentication_request_extra_params_key": "authenticationRequestExtraParams"
                    },
                    authorization_endpoint="authorizationEndpoint",
                    client_id="clientId",
                    client_secret="clientSecret",
                    issuer="issuer",
                    on_unauthenticated_request="onUnauthenticatedRequest",
                    scope="scope",
                    session_cookie_name="sessionCookieName",
                    session_timeout=123,
                    token_endpoint="tokenEndpoint",
                    use_existing_client_secret=False,
                    user_info_endpoint="userInfoEndpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__156e06f0da43a4b71d4a85a923aa120fe5fba81a4a4a4186aa8d1a0e57fd0089)
                check_type(argname="argument authentication_request_extra_params", value=authentication_request_extra_params, expected_type=type_hints["authentication_request_extra_params"])
                check_type(argname="argument authorization_endpoint", value=authorization_endpoint, expected_type=type_hints["authorization_endpoint"])
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
                check_type(argname="argument on_unauthenticated_request", value=on_unauthenticated_request, expected_type=type_hints["on_unauthenticated_request"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument session_cookie_name", value=session_cookie_name, expected_type=type_hints["session_cookie_name"])
                check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
                check_type(argname="argument token_endpoint", value=token_endpoint, expected_type=type_hints["token_endpoint"])
                check_type(argname="argument use_existing_client_secret", value=use_existing_client_secret, expected_type=type_hints["use_existing_client_secret"])
                check_type(argname="argument user_info_endpoint", value=user_info_endpoint, expected_type=type_hints["user_info_endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_request_extra_params is not None:
                self._values["authentication_request_extra_params"] = authentication_request_extra_params
            if authorization_endpoint is not None:
                self._values["authorization_endpoint"] = authorization_endpoint
            if client_id is not None:
                self._values["client_id"] = client_id
            if client_secret is not None:
                self._values["client_secret"] = client_secret
            if issuer is not None:
                self._values["issuer"] = issuer
            if on_unauthenticated_request is not None:
                self._values["on_unauthenticated_request"] = on_unauthenticated_request
            if scope is not None:
                self._values["scope"] = scope
            if session_cookie_name is not None:
                self._values["session_cookie_name"] = session_cookie_name
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout
            if token_endpoint is not None:
                self._values["token_endpoint"] = token_endpoint
            if use_existing_client_secret is not None:
                self._values["use_existing_client_secret"] = use_existing_client_secret
            if user_info_endpoint is not None:
                self._values["user_info_endpoint"] = user_info_endpoint

        @builtins.property
        def authentication_request_extra_params(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The query parameters (up to 10) to include in the redirect request to the authorization endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authenticationrequestextraparams
            '''
            result = self._values.get("authentication_request_extra_params")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def authorization_endpoint(self) -> typing.Optional[builtins.str]:
            '''The authorization endpoint of the IdP.

            This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-authorizationendpoint
            '''
            result = self._values.get("authorization_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''The OAuth 2.0 client identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_secret(self) -> typing.Optional[builtins.str]:
            '''The OAuth 2.0 client secret. This parameter is required if you are creating a rule. If you are modifying a rule, you can omit this parameter if you set ``UseExistingClientSecret`` to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-clientsecret
            '''
            result = self._values.get("client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The OIDC issuer identifier of the IdP.

            This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_unauthenticated_request(self) -> typing.Optional[builtins.str]:
            '''The behavior if the user is not authenticated. The following are possible values:.

            - deny `` - Return an HTTP 401 Unauthorized error.
            - allow `` - Allow the request to be forwarded to the target.
            - authenticate `` - Redirect the request to the IdP authorization endpoint. This is the default value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-onunauthenticatedrequest
            '''
            result = self._values.get("on_unauthenticated_request")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The set of user claims to be requested from the IdP. The default is ``openid`` .

            To verify which scope values your IdP supports and how to separate multiple values, see the documentation for your IdP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_cookie_name(self) -> typing.Optional[builtins.str]:
            '''The name of the cookie used to maintain session information.

            The default is AWSELBAuthSessionCookie.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessioncookiename
            '''
            result = self._values.get("session_cookie_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            '''The maximum duration of the authentication session, in seconds.

            The default is 604800 seconds (7 days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def token_endpoint(self) -> typing.Optional[builtins.str]:
            '''The token endpoint of the IdP.

            This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-tokenendpoint
            '''
            result = self._values.get("token_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_existing_client_secret(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to use the existing client secret when modifying a rule.

            If you are creating a rule, you can omit this parameter or set it to false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-useexistingclientsecret
            '''
            result = self._values.get("use_existing_client_secret")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def user_info_endpoint(self) -> typing.Optional[builtins.str]:
            '''The user info endpoint of the IdP.

            This must be a full URL, including the HTTPS protocol, the domain, and the path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html#cfn-elasticloadbalancingv2-listenerrule-authenticateoidcconfig-userinfoendpoint
            '''
            result = self._values.get("user_info_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticateOidcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.FixedResponseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content_type": "contentType",
            "message_body": "messageBody",
            "status_code": "statusCode",
        },
    )
    class FixedResponseConfigProperty:
        def __init__(
            self,
            *,
            content_type: typing.Optional[builtins.str] = None,
            message_body: typing.Optional[builtins.str] = None,
            status_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies information required when returning a custom HTTP response.

            :param content_type: The content type. Valid Values: text/plain | text/css | text/html | application/javascript | application/json
            :param message_body: The message.
            :param status_code: The HTTP response code (2XX, 4XX, or 5XX).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                fixed_response_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.FixedResponseConfigProperty(
                    content_type="contentType",
                    message_body="messageBody",
                    status_code="statusCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17fa2051d8d9f311ead5336a60a8b0bc6ae627f819c6cec79ec5cac432ad8d3e)
                check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
                check_type(argname="argument message_body", value=message_body, expected_type=type_hints["message_body"])
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content_type is not None:
                self._values["content_type"] = content_type
            if message_body is not None:
                self._values["message_body"] = message_body
            if status_code is not None:
                self._values["status_code"] = status_code

        @builtins.property
        def content_type(self) -> typing.Optional[builtins.str]:
            '''The content type.

            Valid Values: text/plain | text/css | text/html | application/javascript | application/json

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-contenttype
            '''
            result = self._values.get("content_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_body(self) -> typing.Optional[builtins.str]:
            '''The message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-messagebody
            '''
            result = self._values.get("message_body")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_code(self) -> typing.Optional[builtins.str]:
            '''The HTTP response code (2XX, 4XX, or 5XX).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-fixedresponseconfig.html#cfn-elasticloadbalancingv2-listenerrule-fixedresponseconfig-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.ForwardConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_groups": "targetGroups",
            "target_group_stickiness_config": "targetGroupStickinessConfig",
        },
    )
    class ForwardConfigProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.TargetGroupTupleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            target_group_stickiness_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information for creating an action that distributes requests among multiple target groups. Specify only when ``Type`` is ``forward`` .

            If you specify both ``ForwardConfig`` and ``TargetGroupArn`` , you can specify only one target group using ``ForwardConfig`` and it must be the same target group specified in ``TargetGroupArn`` .

            :param target_groups: Information about how traffic will be distributed between multiple target groups in a forward rule.
            :param target_group_stickiness_config: Information about the target group stickiness for a rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-forwardconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                forward_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.ForwardConfigProperty(
                    target_groups=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupTupleProperty(
                        target_group_arn="targetGroupArn",
                        weight=123
                    )],
                    target_group_stickiness_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty(
                        duration_seconds=123,
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4247c16ea7d9e81887d43e40f9a5cf8948d56e3b2106b51d8858bda7b171d83e)
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
                check_type(argname="argument target_group_stickiness_config", value=target_group_stickiness_config, expected_type=type_hints["target_group_stickiness_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_groups is not None:
                self._values["target_groups"] = target_groups
            if target_group_stickiness_config is not None:
                self._values["target_group_stickiness_config"] = target_group_stickiness_config

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.TargetGroupTupleProperty"]]]]:
            '''Information about how traffic will be distributed between multiple target groups in a forward rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-forwardconfig.html#cfn-elasticloadbalancingv2-listenerrule-forwardconfig-targetgroups
            '''
            result = self._values.get("target_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.TargetGroupTupleProperty"]]]], result)

        @builtins.property
        def target_group_stickiness_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty"]]:
            '''Information about the target group stickiness for a rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-forwardconfig.html#cfn-elasticloadbalancingv2-listenerrule-forwardconfig-targetgroupstickinessconfig
            '''
            result = self._values.get("target_group_stickiness_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.HostHeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"regex_values": "regexValues", "values": "values"},
    )
    class HostHeaderConfigProperty:
        def __init__(
            self,
            *,
            regex_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about a host header condition.

            :param regex_values: 
            :param values: The host names. The maximum length of each string is 128 characters. The comparison is case insensitive. The following wildcard characters are supported: * (matches 0 or more characters) and ? (matches exactly 1 character). You must include at least one "." character. You can include only alphabetical characters after the final "." character. If you specify multiple strings, the condition is satisfied if one of the strings matches the host name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-hostheaderconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                host_header_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HostHeaderConfigProperty(
                    regex_values=["regexValues"],
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6cd5fa6094eeaf9e0a34093cb72f9ee2913b8eb9489d369b06127c65111ab04)
                check_type(argname="argument regex_values", value=regex_values, expected_type=type_hints["regex_values"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if regex_values is not None:
                self._values["regex_values"] = regex_values
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def regex_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-hostheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-hostheaderconfig-regexvalues
            '''
            result = self._values.get("regex_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The host names.

            The maximum length of each string is 128 characters. The comparison is case insensitive. The following wildcard characters are supported: * (matches 0 or more characters) and ? (matches exactly 1 character). You must include at least one "." character. You can include only alphabetical characters after the final "." character.

            If you specify multiple strings, the condition is satisfied if one of the strings matches the host name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-hostheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-hostheaderconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostHeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.HttpHeaderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "http_header_name": "httpHeaderName",
            "regex_values": "regexValues",
            "values": "values",
        },
    )
    class HttpHeaderConfigProperty:
        def __init__(
            self,
            *,
            http_header_name: typing.Optional[builtins.str] = None,
            regex_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about an HTTP header condition.

            There is a set of standard HTTP header fields. You can also define custom HTTP header fields.

            :param http_header_name: The name of the HTTP header field. The maximum size is 40 characters. The header name is case insensitive. The allowed characters are specified by RFC 7230. Wildcards are not supported.
            :param regex_values: 
            :param values: The strings to compare against the value of the HTTP header. The maximum length of each string is 128 characters. The comparison strings are case insensitive. The following wildcard characters are supported: * (matches 0 or more characters) and ? (matches exactly 1 character). If the same header appears multiple times in the request, we search them in order until a match is found. If you specify multiple strings, the condition is satisfied if one of the strings matches the value of the HTTP header. To require that all of the strings are a match, create one condition per string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                http_header_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HttpHeaderConfigProperty(
                    http_header_name="httpHeaderName",
                    regex_values=["regexValues"],
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c82afa754d2183edb46229da7253561c0bf5afb887ecad6c2edd980322e4f78d)
                check_type(argname="argument http_header_name", value=http_header_name, expected_type=type_hints["http_header_name"])
                check_type(argname="argument regex_values", value=regex_values, expected_type=type_hints["regex_values"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if http_header_name is not None:
                self._values["http_header_name"] = http_header_name
            if regex_values is not None:
                self._values["regex_values"] = regex_values
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def http_header_name(self) -> typing.Optional[builtins.str]:
            '''The name of the HTTP header field.

            The maximum size is 40 characters. The header name is case insensitive. The allowed characters are specified by RFC 7230. Wildcards are not supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-httpheaderconfig-httpheadername
            '''
            result = self._values.get("http_header_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def regex_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-httpheaderconfig-regexvalues
            '''
            result = self._values.get("regex_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The strings to compare against the value of the HTTP header.

            The maximum length of each string is 128 characters. The comparison strings are case insensitive. The following wildcard characters are supported: * (matches 0 or more characters) and ? (matches exactly 1 character).

            If the same header appears multiple times in the request, we search them in order until a match is found.

            If you specify multiple strings, the condition is satisfied if one of the strings matches the value of the HTTP header. To require that all of the strings are a match, create one condition per string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httpheaderconfig.html#cfn-elasticloadbalancingv2-listenerrule-httpheaderconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpHeaderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.HttpRequestMethodConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class HttpRequestMethodConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about an HTTP method condition.

            HTTP defines a set of request methods, also referred to as HTTP verbs. For more information, see the `HTTP Method Registry <https://docs.aws.amazon.com/https://www.iana.org/assignments/http-methods/http-methods.xhtml>`_ . You can also define custom HTTP methods.

            :param values: The name of the request method. The maximum length is 40 characters. The allowed characters are A-Z, hyphen (-), and underscore (_). The comparison is case sensitive. Wildcards are not supported; therefore, the method name must be an exact match. If you specify multiple strings, the condition is satisfied if one of the strings matches the HTTP request method. We recommend that you route GET and HEAD requests in the same way, because the response to a HEAD request may be cached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httprequestmethodconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                http_request_method_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HttpRequestMethodConfigProperty(
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72bb8b9a58c7606ccbeb741f73a47b2eae46b76991fca484b7d19b0164e38a7b)
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The name of the request method.

            The maximum length is 40 characters. The allowed characters are A-Z, hyphen (-), and underscore (_). The comparison is case sensitive. Wildcards are not supported; therefore, the method name must be an exact match.

            If you specify multiple strings, the condition is satisfied if one of the strings matches the HTTP request method. We recommend that you route GET and HEAD requests in the same way, because the response to a HEAD request may be cached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-httprequestmethodconfig.html#cfn-elasticloadbalancingv2-listenerrule-httprequestmethodconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpRequestMethodConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty",
        jsii_struct_bases=[],
        name_mapping={"format": "format", "name": "name", "values": "values"},
    )
    class JwtValidationActionAdditionalClaimProperty:
        def __init__(
            self,
            *,
            format: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about an additional claim to validate.

            :param format: The format of the claim value.
            :param name: The name of the claim. You can't specify ``exp`` , ``iss`` , ``nbf`` , or ``iat`` because we validate them by default.
            :param values: The claim value. The maximum size of the list is 10. Each value can be up to 256 characters in length. If the format is ``space-separated-values`` , the values can't include spaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-jwtvalidationactionadditionalclaim.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                jwt_validation_action_additional_claim_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty(
                    format="format",
                    name="name",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__155795b8b53918d8e249d68aa0b58c2ceec02c3e0b737a2f8a1e7dc84a14f8ff)
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if format is not None:
                self._values["format"] = format
            if name is not None:
                self._values["name"] = name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''The format of the claim value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-jwtvalidationactionadditionalclaim.html#cfn-elasticloadbalancingv2-listenerrule-jwtvalidationactionadditionalclaim-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the claim.

            You can't specify ``exp`` , ``iss`` , ``nbf`` , or ``iat`` because we validate them by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-jwtvalidationactionadditionalclaim.html#cfn-elasticloadbalancingv2-listenerrule-jwtvalidationactionadditionalclaim-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The claim value.

            The maximum size of the list is 10. Each value can be up to 256 characters in length. If the format is ``space-separated-values`` , the values can't include spaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-jwtvalidationactionadditionalclaim.html#cfn-elasticloadbalancingv2-listenerrule-jwtvalidationactionadditionalclaim-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JwtValidationActionAdditionalClaimProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.JwtValidationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_claims": "additionalClaims",
            "issuer": "issuer",
            "jwks_endpoint": "jwksEndpoint",
        },
    )
    class JwtValidationConfigProperty:
        def __init__(
            self,
            *,
            additional_claims: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            issuer: typing.Optional[builtins.str] = None,
            jwks_endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param additional_claims: 
            :param issuer: 
            :param jwks_endpoint: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-jwtvalidationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                jwt_validation_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.JwtValidationConfigProperty(
                    additional_claims=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty(
                        format="format",
                        name="name",
                        values=["values"]
                    )],
                    issuer="issuer",
                    jwks_endpoint="jwksEndpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4881da15ef93699aeab31b1095ce236507b5a59defdb43451b737a07290e4fcd)
                check_type(argname="argument additional_claims", value=additional_claims, expected_type=type_hints["additional_claims"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
                check_type(argname="argument jwks_endpoint", value=jwks_endpoint, expected_type=type_hints["jwks_endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_claims is not None:
                self._values["additional_claims"] = additional_claims
            if issuer is not None:
                self._values["issuer"] = issuer
            if jwks_endpoint is not None:
                self._values["jwks_endpoint"] = jwks_endpoint

        @builtins.property
        def additional_claims(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-jwtvalidationconfig.html#cfn-elasticloadbalancingv2-listenerrule-jwtvalidationconfig-additionalclaims
            '''
            result = self._values.get("additional_claims")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty"]]]], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-jwtvalidationconfig.html#cfn-elasticloadbalancingv2-listenerrule-jwtvalidationconfig-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def jwks_endpoint(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-jwtvalidationconfig.html#cfn-elasticloadbalancingv2-listenerrule-jwtvalidationconfig-jwksendpoint
            '''
            result = self._values.get("jwks_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JwtValidationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.PathPatternConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"regex_values": "regexValues", "values": "values"},
    )
    class PathPatternConfigProperty:
        def __init__(
            self,
            *,
            regex_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about a path pattern condition.

            :param regex_values: 
            :param values: The path patterns to compare against the request URL. The maximum size of each string is 128 characters. The comparison is case sensitive. The following wildcard characters are supported: * (matches 0 or more characters) and ? (matches exactly 1 character). If you specify multiple strings, the condition is satisfied if one of them matches the request URL. The path pattern is compared only to the path of the URL, not to its query string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-pathpatternconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                path_pattern_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.PathPatternConfigProperty(
                    regex_values=["regexValues"],
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24070f52616f8426e9871ad2c63a33d7bab2fb1d715c539d26c323dbe2245f00)
                check_type(argname="argument regex_values", value=regex_values, expected_type=type_hints["regex_values"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if regex_values is not None:
                self._values["regex_values"] = regex_values
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def regex_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-pathpatternconfig.html#cfn-elasticloadbalancingv2-listenerrule-pathpatternconfig-regexvalues
            '''
            result = self._values.get("regex_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The path patterns to compare against the request URL.

            The maximum size of each string is 128 characters. The comparison is case sensitive. The following wildcard characters are supported: * (matches 0 or more characters) and ? (matches exactly 1 character).

            If you specify multiple strings, the condition is satisfied if one of them matches the request URL. The path pattern is compared only to the path of the URL, not to its query string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-pathpatternconfig.html#cfn-elasticloadbalancingv2-listenerrule-pathpatternconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathPatternConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.QueryStringConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class QueryStringConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.QueryStringKeyValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information about a query string condition.

            The query string component of a URI starts after the first '?' character and is terminated by either a '#' character or the end of the URI. A typical query string contains key/value pairs separated by '&' characters. The allowed characters are specified by RFC 3986. Any character can be percentage encoded.

            :param values: The key/value pairs or values to find in the query string. The maximum length of each string is 128 characters. The comparison is case insensitive. The following wildcard characters are supported: * (matches 0 or more characters) and ? (matches exactly 1 character). To search for a literal '*' or '?' character in a query string, you must escape these characters in ``Values`` using a '' character. If you specify multiple key/value pairs or values, the condition is satisfied if one of them is found in the query string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                query_string_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.QueryStringConfigProperty(
                    values=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.QueryStringKeyValueProperty(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__830791bf4de3573dac6c0b6b758d53cae934431a1e83c8ac5e5e633f86170a13)
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.QueryStringKeyValueProperty"]]]]:
            '''The key/value pairs or values to find in the query string.

            The maximum length of each string is 128 characters. The comparison is case insensitive. The following wildcard characters are supported: * (matches 0 or more characters) and ? (matches exactly 1 character). To search for a literal '*' or '?' character in a query string, you must escape these characters in ``Values`` using a '' character.

            If you specify multiple key/value pairs or values, the condition is satisfied if one of them is found in the query string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringconfig.html#cfn-elasticloadbalancingv2-listenerrule-querystringconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.QueryStringKeyValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryStringConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.QueryStringKeyValueProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class QueryStringKeyValueProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a key/value pair.

            :param key: The key. You can omit the key.
            :param value: The value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                query_string_key_value_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.QueryStringKeyValueProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53f53b371064128611e16b475b6e39045e21016cae5ff726ad920fea2b9be6bf)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key.

            You can omit the key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html#cfn-elasticloadbalancingv2-listenerrule-querystringkeyvalue-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-querystringkeyvalue.html#cfn-elasticloadbalancingv2-listenerrule-querystringkeyvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryStringKeyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.RedirectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "host": "host",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "query": "query",
            "status_code": "statusCode",
        },
    )
    class RedirectConfigProperty:
        def __init__(
            self,
            *,
            host: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            query: typing.Optional[builtins.str] = None,
            status_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a redirect action.

            A URI consists of the following components: protocol://hostname:port/path?query. You must modify at least one of the following components to avoid a redirect loop: protocol, hostname, port, or path. Any components that you do not modify retain their original values.

            You can reuse URI components using the following reserved keywords:

            - #{protocol}
            - #{host}
            - #{port}
            - #{path} (the leading "/" is removed)
            - #{query}

            For example, you can change the path to "/new/#{path}", the hostname to "example.#{host}", or the query to "#{query}&value=xyz".

            :param host: The hostname. This component is not percent-encoded. The hostname can contain #{host}.
            :param path: The absolute path, starting with the leading "/". This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}.
            :param port: The port. You can specify a value from 1 to 65535 or #{port}.
            :param protocol: The protocol. You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You can't redirect HTTPS to HTTP.
            :param query: The query parameters, URL-encoded when necessary, but not percent-encoded. Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords.
            :param status_code: The HTTP redirect code. The redirect is either permanent (HTTP 301) or temporary (HTTP 302).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                redirect_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RedirectConfigProperty(
                    host="host",
                    path="path",
                    port="port",
                    protocol="protocol",
                    query="query",
                    status_code="statusCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb6b0e432bbb900701173eb76d7db590b7313643eb184198dc7b0064a68d0f8d)
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument query", value=query, expected_type=type_hints["query"])
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if host is not None:
                self._values["host"] = host
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if query is not None:
                self._values["query"] = query
            if status_code is not None:
                self._values["status_code"] = status_code

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''The hostname.

            This component is not percent-encoded. The hostname can contain #{host}.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The absolute path, starting with the leading "/".

            This component is not percent-encoded. The path can contain #{host}, #{path}, and #{port}.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port.

            You can specify a value from 1 to 65535 or #{port}.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol.

            You can specify HTTP, HTTPS, or #{protocol}. You can redirect HTTP to HTTP, HTTP to HTTPS, and HTTPS to HTTPS. You can't redirect HTTPS to HTTP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query(self) -> typing.Optional[builtins.str]:
            '''The query parameters, URL-encoded when necessary, but not percent-encoded.

            Do not include the leading "?", as it is automatically added. You can specify any of the reserved keywords.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-query
            '''
            result = self._values.get("query")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_code(self) -> typing.Optional[builtins.str]:
            '''The HTTP redirect code.

            The redirect is either permanent (HTTP 301) or temporary (HTTP 302).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-redirectconfig.html#cfn-elasticloadbalancingv2-listenerrule-redirectconfig-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.RewriteConfigObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"rewrites": "rewrites"},
    )
    class RewriteConfigObjectProperty:
        def __init__(
            self,
            *,
            rewrites: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.RewriteConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param rewrites: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rewriteconfigobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                rewrite_config_object_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigObjectProperty(
                    rewrites=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigProperty(
                        regex="regex",
                        replace="replace"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c46adf1532088f895c2b86c4e0f216b98f0b08d1ab15eadf8773f16e079d802)
                check_type(argname="argument rewrites", value=rewrites, expected_type=type_hints["rewrites"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rewrites is not None:
                self._values["rewrites"] = rewrites

        @builtins.property
        def rewrites(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RewriteConfigProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rewriteconfigobject.html#cfn-elasticloadbalancingv2-listenerrule-rewriteconfigobject-rewrites
            '''
            result = self._values.get("rewrites")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RewriteConfigProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RewriteConfigObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.RewriteConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"regex": "regex", "replace": "replace"},
    )
    class RewriteConfigProperty:
        def __init__(
            self,
            *,
            regex: typing.Optional[builtins.str] = None,
            replace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a rewrite transform.

            This transform matches a pattern and replaces it with the specified string.

            :param regex: The regular expression to match in the input string. The maximum length of the string is 1,024 characters.
            :param replace: The replacement string to use when rewriting the matched input. The maximum length of the string is 1,024 characters. You can specify capture groups in the regular expression (for example, $1 and $2).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rewriteconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                rewrite_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigProperty(
                    regex="regex",
                    replace="replace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf5a411efc3ddee921b236d1a2337f5e385d9c34b119678b8d3cb3d01a402a35)
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
                check_type(argname="argument replace", value=replace, expected_type=type_hints["replace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if regex is not None:
                self._values["regex"] = regex
            if replace is not None:
                self._values["replace"] = replace

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''The regular expression to match in the input string.

            The maximum length of the string is 1,024 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rewriteconfig.html#cfn-elasticloadbalancingv2-listenerrule-rewriteconfig-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replace(self) -> typing.Optional[builtins.str]:
            '''The replacement string to use when rewriting the matched input.

            The maximum length of the string is 1,024 characters. You can specify capture groups in the regular expression (for example, $1 and $2).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rewriteconfig.html#cfn-elasticloadbalancingv2-listenerrule-rewriteconfig-replace
            '''
            result = self._values.get("replace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RewriteConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.RuleConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field": "field",
            "host_header_config": "hostHeaderConfig",
            "http_header_config": "httpHeaderConfig",
            "http_request_method_config": "httpRequestMethodConfig",
            "path_pattern_config": "pathPatternConfig",
            "query_string_config": "queryStringConfig",
            "regex_values": "regexValues",
            "source_ip_config": "sourceIpConfig",
            "values": "values",
        },
    )
    class RuleConditionProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            host_header_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.HostHeaderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http_header_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.HttpHeaderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            http_request_method_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.HttpRequestMethodConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            path_pattern_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.PathPatternConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            query_string_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.QueryStringConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            regex_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_ip_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.SourceIpConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies a condition for a listener rule.

            :param field: The field in the HTTP request. The following are the possible values:. - ``http-header`` - ``http-request-method`` - ``host-header`` - ``path-pattern`` - ``query-string`` - ``source-ip``
            :param host_header_config: Information for a host header condition. Specify only when ``Field`` is ``host-header`` .
            :param http_header_config: Information for an HTTP header condition. Specify only when ``Field`` is ``http-header`` .
            :param http_request_method_config: Information for an HTTP method condition. Specify only when ``Field`` is ``http-request-method`` .
            :param path_pattern_config: Information for a path pattern condition. Specify only when ``Field`` is ``path-pattern`` .
            :param query_string_config: Information for a query string condition. Specify only when ``Field`` is ``query-string`` .
            :param regex_values: The regular expressions to match against the condition field. The maximum length of each string is 128 characters. Specify only when ``Field`` is ``http-header`` , ``host-header`` , or ``path-pattern`` .
            :param source_ip_config: Information for a source IP condition. Specify only when ``Field`` is ``source-ip`` .
            :param values: The condition value. Specify only when ``Field`` is ``host-header`` or ``path-pattern`` . Alternatively, to specify multiple host names or multiple path patterns, use ``HostHeaderConfig`` or ``PathPatternConfig`` . If ``Field`` is ``host-header`` and you're not using ``HostHeaderConfig`` , you can specify a single host name (for example, my.example.com). A host name is case insensitive, can be up to 128 characters in length, and can contain any of the following characters. - A-Z, a-z, 0-9 - - . - - (matches 0 or more characters) - ? (matches exactly 1 character) If ``Field`` is ``path-pattern`` and you're not using ``PathPatternConfig`` , you can specify a single path pattern (for example, /img/*). A path pattern is case-sensitive, can be up to 128 characters in length, and can contain any of the following characters. - A-Z, a-z, 0-9 - _ - . $ / ~ " ' @ : + - & (using &) - - (matches 0 or more characters) - ? (matches exactly 1 character)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                rule_condition_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RuleConditionProperty(
                    field="field",
                    host_header_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HostHeaderConfigProperty(
                        regex_values=["regexValues"],
                        values=["values"]
                    ),
                    http_header_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HttpHeaderConfigProperty(
                        http_header_name="httpHeaderName",
                        regex_values=["regexValues"],
                        values=["values"]
                    ),
                    http_request_method_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.HttpRequestMethodConfigProperty(
                        values=["values"]
                    ),
                    path_pattern_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.PathPatternConfigProperty(
                        regex_values=["regexValues"],
                        values=["values"]
                    ),
                    query_string_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.QueryStringConfigProperty(
                        values=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.QueryStringKeyValueProperty(
                            key="key",
                            value="value"
                        )]
                    ),
                    regex_values=["regexValues"],
                    source_ip_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.SourceIpConfigProperty(
                        values=["values"]
                    ),
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8d26139e1f026ae7622ca192057e867dc5863d9350c24e1ef6675c38332429d)
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument host_header_config", value=host_header_config, expected_type=type_hints["host_header_config"])
                check_type(argname="argument http_header_config", value=http_header_config, expected_type=type_hints["http_header_config"])
                check_type(argname="argument http_request_method_config", value=http_request_method_config, expected_type=type_hints["http_request_method_config"])
                check_type(argname="argument path_pattern_config", value=path_pattern_config, expected_type=type_hints["path_pattern_config"])
                check_type(argname="argument query_string_config", value=query_string_config, expected_type=type_hints["query_string_config"])
                check_type(argname="argument regex_values", value=regex_values, expected_type=type_hints["regex_values"])
                check_type(argname="argument source_ip_config", value=source_ip_config, expected_type=type_hints["source_ip_config"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field is not None:
                self._values["field"] = field
            if host_header_config is not None:
                self._values["host_header_config"] = host_header_config
            if http_header_config is not None:
                self._values["http_header_config"] = http_header_config
            if http_request_method_config is not None:
                self._values["http_request_method_config"] = http_request_method_config
            if path_pattern_config is not None:
                self._values["path_pattern_config"] = path_pattern_config
            if query_string_config is not None:
                self._values["query_string_config"] = query_string_config
            if regex_values is not None:
                self._values["regex_values"] = regex_values
            if source_ip_config is not None:
                self._values["source_ip_config"] = source_ip_config
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field in the HTTP request. The following are the possible values:.

            - ``http-header``
            - ``http-request-method``
            - ``host-header``
            - ``path-pattern``
            - ``query-string``
            - ``source-ip``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_header_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.HostHeaderConfigProperty"]]:
            '''Information for a host header condition.

            Specify only when ``Field`` is ``host-header`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-hostheaderconfig
            '''
            result = self._values.get("host_header_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.HostHeaderConfigProperty"]], result)

        @builtins.property
        def http_header_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.HttpHeaderConfigProperty"]]:
            '''Information for an HTTP header condition.

            Specify only when ``Field`` is ``http-header`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-httpheaderconfig
            '''
            result = self._values.get("http_header_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.HttpHeaderConfigProperty"]], result)

        @builtins.property
        def http_request_method_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.HttpRequestMethodConfigProperty"]]:
            '''Information for an HTTP method condition.

            Specify only when ``Field`` is ``http-request-method`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-httprequestmethodconfig
            '''
            result = self._values.get("http_request_method_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.HttpRequestMethodConfigProperty"]], result)

        @builtins.property
        def path_pattern_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.PathPatternConfigProperty"]]:
            '''Information for a path pattern condition.

            Specify only when ``Field`` is ``path-pattern`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-pathpatternconfig
            '''
            result = self._values.get("path_pattern_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.PathPatternConfigProperty"]], result)

        @builtins.property
        def query_string_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.QueryStringConfigProperty"]]:
            '''Information for a query string condition.

            Specify only when ``Field`` is ``query-string`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-querystringconfig
            '''
            result = self._values.get("query_string_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.QueryStringConfigProperty"]], result)

        @builtins.property
        def regex_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The regular expressions to match against the condition field.

            The maximum length of each string is 128 characters. Specify only when ``Field`` is ``http-header`` , ``host-header`` , or ``path-pattern`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-regexvalues
            '''
            result = self._values.get("regex_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_ip_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.SourceIpConfigProperty"]]:
            '''Information for a source IP condition.

            Specify only when ``Field`` is ``source-ip`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-sourceipconfig
            '''
            result = self._values.get("source_ip_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.SourceIpConfigProperty"]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The condition value.

            Specify only when ``Field`` is ``host-header`` or ``path-pattern`` . Alternatively, to specify multiple host names or multiple path patterns, use ``HostHeaderConfig`` or ``PathPatternConfig`` .

            If ``Field`` is ``host-header`` and you're not using ``HostHeaderConfig`` , you can specify a single host name (for example, my.example.com). A host name is case insensitive, can be up to 128 characters in length, and can contain any of the following characters.

            - A-Z, a-z, 0-9
            -
              - .

            -
              - (matches 0 or more characters)

            - ? (matches exactly 1 character)

            If ``Field`` is ``path-pattern`` and you're not using ``PathPatternConfig`` , you can specify a single path pattern (for example, /img/*). A path pattern is case-sensitive, can be up to 128 characters in length, and can contain any of the following characters.

            - A-Z, a-z, 0-9
            - _ - . $ / ~ " ' @ : +
            - & (using &)
            -
              - (matches 0 or more characters)

            - ? (matches exactly 1 character)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-rulecondition.html#cfn-elasticloadbalancingv2-listenerrule-rulecondition-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.SourceIpConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class SourceIpConfigProperty:
        def __init__(
            self,
            *,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about a source IP condition.

            You can use this condition to route based on the IP address of the source that connects to the load balancer. If a client is behind a proxy, this is the IP address of the proxy not the IP address of the client.

            :param values: The source IP addresses, in CIDR format. You can use both IPv4 and IPv6 addresses. Wildcards are not supported. If you specify multiple addresses, the condition is satisfied if the source IP address of the request matches one of the CIDR blocks. This condition is not satisfied by the addresses in the X-Forwarded-For header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-sourceipconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                source_ip_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.SourceIpConfigProperty(
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d529a7ac2cdedd83105eb6a5a355b24d3ae79903316ca86de97beb00e1bb8c9)
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The source IP addresses, in CIDR format. You can use both IPv4 and IPv6 addresses. Wildcards are not supported.

            If you specify multiple addresses, the condition is satisfied if the source IP address of the request matches one of the CIDR blocks. This condition is not satisfied by the addresses in the X-Forwarded-For header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-sourceipconfig.html#cfn-elasticloadbalancingv2-listenerrule-sourceipconfig-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceIpConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_seconds": "durationSeconds", "enabled": "enabled"},
    )
    class TargetGroupStickinessConfigProperty:
        def __init__(
            self,
            *,
            duration_seconds: typing.Optional[jsii.Number] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Information about the target group stickiness for a rule.

            :param duration_seconds: [Application Load Balancers] The time period, in seconds, during which requests from a client should be routed to the same target group. The range is 1-604800 seconds (7 days). You must specify this value when enabling target group stickiness.
            :param enabled: Indicates whether target group stickiness is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                target_group_stickiness_config_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty(
                    duration_seconds=123,
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fefa1b3687b6050545bf8fdcdbbcd3bb8125a5f344b46ad1e3fb6edad7fd8f95)
                check_type(argname="argument duration_seconds", value=duration_seconds, expected_type=type_hints["duration_seconds"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_seconds is not None:
                self._values["duration_seconds"] = duration_seconds
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''[Application Load Balancers] The time period, in seconds, during which requests from a client should be routed to the same target group.

            The range is 1-604800 seconds (7 days). You must specify this value when enabling target group stickiness.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig-durationseconds
            '''
            result = self._values.get("duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether target group stickiness is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig.html#cfn-elasticloadbalancingv2-listenerrule-targetgroupstickinessconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupStickinessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.TargetGroupTupleProperty",
        jsii_struct_bases=[],
        name_mapping={"target_group_arn": "targetGroupArn", "weight": "weight"},
    )
    class TargetGroupTupleProperty:
        def __init__(
            self,
            *,
            target_group_arn: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about how traffic will be distributed between multiple target groups in a forward rule.

            :param target_group_arn: The Amazon Resource Name (ARN) of the target group.
            :param weight: The weight. The range is 0 to 999.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgrouptuple.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                target_group_tuple_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TargetGroupTupleProperty(
                    target_group_arn="targetGroupArn",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f331c4d3033f215ffdef674f5f799cb75dad01369b879280714d8246eea9021)
                check_type(argname="argument target_group_arn", value=target_group_arn, expected_type=type_hints["target_group_arn"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_group_arn is not None:
                self._values["target_group_arn"] = target_group_arn
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the target group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgrouptuple.html#cfn-elasticloadbalancingv2-listenerrule-targetgrouptuple-targetgrouparn
            '''
            result = self._values.get("target_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The weight.

            The range is 0 to 999.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-targetgrouptuple.html#cfn-elasticloadbalancingv2-listenerrule-targetgrouptuple-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnListenerRulePropsMixin.TransformProperty",
        jsii_struct_bases=[],
        name_mapping={
            "host_header_rewrite_config": "hostHeaderRewriteConfig",
            "type": "type",
            "url_rewrite_config": "urlRewriteConfig",
        },
    )
    class TransformProperty:
        def __init__(
            self,
            *,
            host_header_rewrite_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.RewriteConfigObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
            url_rewrite_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnListenerRulePropsMixin.RewriteConfigObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param host_header_rewrite_config: 
            :param type: 
            :param url_rewrite_config: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-transform.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                transform_property = elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.TransformProperty(
                    host_header_rewrite_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigObjectProperty(
                        rewrites=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigProperty(
                            regex="regex",
                            replace="replace"
                        )]
                    ),
                    type="type",
                    url_rewrite_config=elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigObjectProperty(
                        rewrites=[elasticloadbalancingv2_mixins.CfnListenerRulePropsMixin.RewriteConfigProperty(
                            regex="regex",
                            replace="replace"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5763572884fc0ab981b00d58b7b30076af5a7a0285e55c9f09b6cd64fb86654a)
                check_type(argname="argument host_header_rewrite_config", value=host_header_rewrite_config, expected_type=type_hints["host_header_rewrite_config"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument url_rewrite_config", value=url_rewrite_config, expected_type=type_hints["url_rewrite_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if host_header_rewrite_config is not None:
                self._values["host_header_rewrite_config"] = host_header_rewrite_config
            if type is not None:
                self._values["type"] = type
            if url_rewrite_config is not None:
                self._values["url_rewrite_config"] = url_rewrite_config

        @builtins.property
        def host_header_rewrite_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RewriteConfigObjectProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-transform.html#cfn-elasticloadbalancingv2-listenerrule-transform-hostheaderrewriteconfig
            '''
            result = self._values.get("host_header_rewrite_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RewriteConfigObjectProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-transform.html#cfn-elasticloadbalancingv2-listenerrule-transform-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url_rewrite_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RewriteConfigObjectProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-transform.html#cfn-elasticloadbalancingv2-listenerrule-transform-urlrewriteconfig
            '''
            result = self._values.get("url_rewrite_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnListenerRulePropsMixin.RewriteConfigObjectProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnLoadBalancerLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnLoadBalancerLogsMixin",
):
    '''Specifies an Application Load Balancer, a Network Load Balancer, or a Gateway Load Balancer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::LoadBalancer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_load_balancer_logs_mixin = elasticloadbalancingv2_mixins.CfnLoadBalancerLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b848bb4689a98590b8a6fc047bafa7a29fd77d0479ef3b786049c84f916fe02d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6347508044aef58390c2e951930478ca1748f1808b2e95ccbe023e500bc026e)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ddadc9aab0991bd8e586a6c33aeb9089405abe394b02532e7e1e4554f98111)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NLB_ACCESS_LOGS")
    def NLB_ACCESS_LOGS(cls) -> "CfnLoadBalancerNlbAccessLogs":
        return typing.cast("CfnLoadBalancerNlbAccessLogs", jsii.sget(cls, "NLB_ACCESS_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnLoadBalancerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "enable_capacity_reservation_provision_stabilize": "enableCapacityReservationProvisionStabilize",
        "enable_prefix_for_ipv6_source_nat": "enablePrefixForIpv6SourceNat",
        "enforce_security_group_inbound_rules_on_private_link_traffic": "enforceSecurityGroupInboundRulesOnPrivateLinkTraffic",
        "ip_address_type": "ipAddressType",
        "ipv4_ipam_pool_id": "ipv4IpamPoolId",
        "load_balancer_attributes": "loadBalancerAttributes",
        "minimum_load_balancer_capacity": "minimumLoadBalancerCapacity",
        "name": "name",
        "scheme": "scheme",
        "security_groups": "securityGroups",
        "subnet_mappings": "subnetMappings",
        "subnets": "subnets",
        "tags": "tags",
        "type": "type",
    },
)
class CfnLoadBalancerMixinProps:
    def __init__(
        self,
        *,
        enable_capacity_reservation_provision_stabilize: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_prefix_for_ipv6_source_nat: typing.Optional[builtins.str] = None,
        enforce_security_group_inbound_rules_on_private_link_traffic: typing.Optional[builtins.str] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        ipv4_ipam_pool_id: typing.Optional[builtins.str] = None,
        load_balancer_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.LoadBalancerAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        minimum_load_balancer_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.MinimumLoadBalancerCapacityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        scheme: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLoadBalancerPropsMixin.SubnetMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLoadBalancerPropsMixin.

        :param enable_capacity_reservation_provision_stabilize: Indicates whether to enable stabilization when creating or updating an LCU reservation. This ensures that the final stack status reflects the status of the LCU reservation. The default is ``false`` . Default: - false
        :param enable_prefix_for_ipv6_source_nat: [Network Load Balancers with UDP listeners] Indicates whether to use an IPv6 prefix from each subnet for source NAT. The IP address type must be ``dualstack`` . The default value is ``off`` .
        :param enforce_security_group_inbound_rules_on_private_link_traffic: Indicates whether to evaluate inbound security group rules for traffic sent to a Network Load Balancer through AWS PrivateLink . The default is ``on`` . You can't configure this property on a Network Load Balancer unless you associated a security group with the load balancer when you created it.
        :param ip_address_type: The IP address type. Internal load balancers must use ``ipv4`` . [Application Load Balancers] The possible values are ``ipv4`` (IPv4 addresses), ``dualstack`` (IPv4 and IPv6 addresses), and ``dualstack-without-public-ipv4`` (public IPv6 addresses and private IPv4 and IPv6 addresses). Application Load Balancer authentication supports IPv4 addresses only when connecting to an Identity Provider (IdP) or Amazon Cognito endpoint. Without a public IPv4 address the load balancer can't complete the authentication process, resulting in HTTP 500 errors. [Network Load Balancers and Gateway Load Balancers] The possible values are ``ipv4`` (IPv4 addresses) and ``dualstack`` (IPv4 and IPv6 addresses).
        :param ipv4_ipam_pool_id: The ID of the IPv4 IPAM pool.
        :param load_balancer_attributes: The load balancer attributes. Attributes that you do not modify retain their current values.
        :param minimum_load_balancer_capacity: The minimum capacity for a load balancer.
        :param name: The name of the load balancer. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, must not begin or end with a hyphen, and must not begin with "internal-". If you don't specify a name, AWS CloudFormation generates a unique physical ID for the load balancer. If you specify a name, you cannot perform updates that require replacement of this resource, but you can perform other updates. To replace the resource, specify a new name.
        :param scheme: The nodes of an Internet-facing load balancer have public IP addresses. The DNS name of an Internet-facing load balancer is publicly resolvable to the public IP addresses of the nodes. Therefore, Internet-facing load balancers can route requests from clients over the internet. The nodes of an internal load balancer have only private IP addresses. The DNS name of an internal load balancer is publicly resolvable to the private IP addresses of the nodes. Therefore, internal load balancers can route requests only from clients with access to the VPC for the load balancer. The default is an Internet-facing load balancer. You can't specify a scheme for a Gateway Load Balancer.
        :param security_groups: [Application Load Balancers and Network Load Balancers] The IDs of the security groups for the load balancer.
        :param subnet_mappings: The IDs of the subnets. You can specify only one subnet per Availability Zone. You must specify either subnets or subnet mappings, but not both. [Application Load Balancers] You must specify subnets from at least two Availability Zones. You can't specify Elastic IP addresses for your subnets. [Application Load Balancers on Outposts] You must specify one Outpost subnet. [Application Load Balancers on Local Zones] You can specify subnets from one or more Local Zones. [Network Load Balancers] You can specify subnets from one or more Availability Zones. You can specify one Elastic IP address per subnet if you need static IP addresses for your internet-facing load balancer. For internal load balancers, you can specify one private IP address per subnet from the IPv4 range of the subnet. For internet-facing load balancer, you can specify one IPv6 address per subnet. [Gateway Load Balancers] You can specify subnets from one or more Availability Zones. You can't specify Elastic IP addresses for your subnets.
        :param subnets: The IDs of the subnets. You can specify only one subnet per Availability Zone. You must specify either subnets or subnet mappings, but not both. To specify an Elastic IP address, specify subnet mappings instead of subnets. [Application Load Balancers] You must specify subnets from at least two Availability Zones. [Application Load Balancers on Outposts] You must specify one Outpost subnet. [Application Load Balancers on Local Zones] You can specify subnets from one or more Local Zones. [Network Load Balancers and Gateway Load Balancers] You can specify subnets from one or more Availability Zones.
        :param tags: The tags to assign to the load balancer.
        :param type: The type of load balancer. The default is ``application`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
            
            cfn_load_balancer_mixin_props = elasticloadbalancingv2_mixins.CfnLoadBalancerMixinProps(
                enable_capacity_reservation_provision_stabilize=False,
                enable_prefix_for_ipv6_source_nat="enablePrefixForIpv6SourceNat",
                enforce_security_group_inbound_rules_on_private_link_traffic="enforceSecurityGroupInboundRulesOnPrivateLinkTraffic",
                ip_address_type="ipAddressType",
                ipv4_ipam_pool_id="ipv4IpamPoolId",
                load_balancer_attributes=[elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin.LoadBalancerAttributeProperty(
                    key="key",
                    value="value"
                )],
                minimum_load_balancer_capacity=elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin.MinimumLoadBalancerCapacityProperty(
                    capacity_units=123
                ),
                name="name",
                scheme="scheme",
                security_groups=["securityGroups"],
                subnet_mappings=[elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin.SubnetMappingProperty(
                    allocation_id="allocationId",
                    i_pv6_address="iPv6Address",
                    private_iPv4_address="privateIPv4Address",
                    source_nat_ipv6_prefix="sourceNatIpv6Prefix",
                    subnet_id="subnetId"
                )],
                subnets=["subnets"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9a2fb6ae18a559290eca5f22e663aed9fbcba3fd09d40a214d6b2d73d43eaf2)
            check_type(argname="argument enable_capacity_reservation_provision_stabilize", value=enable_capacity_reservation_provision_stabilize, expected_type=type_hints["enable_capacity_reservation_provision_stabilize"])
            check_type(argname="argument enable_prefix_for_ipv6_source_nat", value=enable_prefix_for_ipv6_source_nat, expected_type=type_hints["enable_prefix_for_ipv6_source_nat"])
            check_type(argname="argument enforce_security_group_inbound_rules_on_private_link_traffic", value=enforce_security_group_inbound_rules_on_private_link_traffic, expected_type=type_hints["enforce_security_group_inbound_rules_on_private_link_traffic"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument ipv4_ipam_pool_id", value=ipv4_ipam_pool_id, expected_type=type_hints["ipv4_ipam_pool_id"])
            check_type(argname="argument load_balancer_attributes", value=load_balancer_attributes, expected_type=type_hints["load_balancer_attributes"])
            check_type(argname="argument minimum_load_balancer_capacity", value=minimum_load_balancer_capacity, expected_type=type_hints["minimum_load_balancer_capacity"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_mappings", value=subnet_mappings, expected_type=type_hints["subnet_mappings"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_capacity_reservation_provision_stabilize is not None:
            self._values["enable_capacity_reservation_provision_stabilize"] = enable_capacity_reservation_provision_stabilize
        if enable_prefix_for_ipv6_source_nat is not None:
            self._values["enable_prefix_for_ipv6_source_nat"] = enable_prefix_for_ipv6_source_nat
        if enforce_security_group_inbound_rules_on_private_link_traffic is not None:
            self._values["enforce_security_group_inbound_rules_on_private_link_traffic"] = enforce_security_group_inbound_rules_on_private_link_traffic
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if ipv4_ipam_pool_id is not None:
            self._values["ipv4_ipam_pool_id"] = ipv4_ipam_pool_id
        if load_balancer_attributes is not None:
            self._values["load_balancer_attributes"] = load_balancer_attributes
        if minimum_load_balancer_capacity is not None:
            self._values["minimum_load_balancer_capacity"] = minimum_load_balancer_capacity
        if name is not None:
            self._values["name"] = name
        if scheme is not None:
            self._values["scheme"] = scheme
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_mappings is not None:
            self._values["subnet_mappings"] = subnet_mappings
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def enable_capacity_reservation_provision_stabilize(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether to enable stabilization when creating or updating an LCU reservation.

        This ensures that the final stack status reflects the status of the LCU reservation. The default is ``false`` .

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-enablecapacityreservationprovisionstabilize
        '''
        result = self._values.get("enable_capacity_reservation_provision_stabilize")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_prefix_for_ipv6_source_nat(self) -> typing.Optional[builtins.str]:
        '''[Network Load Balancers with UDP listeners] Indicates whether to use an IPv6 prefix from each subnet for source NAT.

        The IP address type must be ``dualstack`` . The default value is ``off`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-enableprefixforipv6sourcenat
        '''
        result = self._values.get("enable_prefix_for_ipv6_source_nat")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_security_group_inbound_rules_on_private_link_traffic(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Indicates whether to evaluate inbound security group rules for traffic sent to a Network Load Balancer through AWS PrivateLink .

        The default is ``on`` .

        You can't configure this property on a Network Load Balancer unless you associated a security group with the load balancer when you created it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-enforcesecuritygroupinboundrulesonprivatelinktraffic
        '''
        result = self._values.get("enforce_security_group_inbound_rules_on_private_link_traffic")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''The IP address type. Internal load balancers must use ``ipv4`` .

        [Application Load Balancers] The possible values are ``ipv4`` (IPv4 addresses), ``dualstack`` (IPv4 and IPv6 addresses), and ``dualstack-without-public-ipv4`` (public IPv6 addresses and private IPv4 and IPv6 addresses).

        Application Load Balancer authentication supports IPv4 addresses only when connecting to an Identity Provider (IdP) or Amazon Cognito endpoint. Without a public IPv4 address the load balancer can't complete the authentication process, resulting in HTTP 500 errors.

        [Network Load Balancers and Gateway Load Balancers] The possible values are ``ipv4`` (IPv4 addresses) and ``dualstack`` (IPv4 and IPv6 addresses).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4_ipam_pool_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the IPv4 IPAM pool.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-ipv4ipampoolid
        '''
        result = self._values.get("ipv4_ipam_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.LoadBalancerAttributeProperty"]]]]:
        '''The load balancer attributes.

        Attributes that you do not modify retain their current values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattributes
        '''
        result = self._values.get("load_balancer_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.LoadBalancerAttributeProperty"]]]], result)

    @builtins.property
    def minimum_load_balancer_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.MinimumLoadBalancerCapacityProperty"]]:
        '''The minimum capacity for a load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-minimumloadbalancercapacity
        '''
        result = self._values.get("minimum_load_balancer_capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.MinimumLoadBalancerCapacityProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the load balancer.

        This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, must not begin or end with a hyphen, and must not begin with "internal-".

        If you don't specify a name, AWS CloudFormation generates a unique physical ID for the load balancer. If you specify a name, you cannot perform updates that require replacement of this resource, but you can perform other updates. To replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''The nodes of an Internet-facing load balancer have public IP addresses.

        The DNS name of an Internet-facing load balancer is publicly resolvable to the public IP addresses of the nodes. Therefore, Internet-facing load balancers can route requests from clients over the internet.

        The nodes of an internal load balancer have only private IP addresses. The DNS name of an internal load balancer is publicly resolvable to the private IP addresses of the nodes. Therefore, internal load balancers can route requests only from clients with access to the VPC for the load balancer.

        The default is an Internet-facing load balancer.

        You can't specify a scheme for a Gateway Load Balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-scheme
        '''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''[Application Load Balancers and Network Load Balancers] The IDs of the security groups for the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.SubnetMappingProperty"]]]]:
        '''The IDs of the subnets.

        You can specify only one subnet per Availability Zone. You must specify either subnets or subnet mappings, but not both.

        [Application Load Balancers] You must specify subnets from at least two Availability Zones. You can't specify Elastic IP addresses for your subnets.

        [Application Load Balancers on Outposts] You must specify one Outpost subnet.

        [Application Load Balancers on Local Zones] You can specify subnets from one or more Local Zones.

        [Network Load Balancers] You can specify subnets from one or more Availability Zones. You can specify one Elastic IP address per subnet if you need static IP addresses for your internet-facing load balancer. For internal load balancers, you can specify one private IP address per subnet from the IPv4 range of the subnet. For internet-facing load balancer, you can specify one IPv6 address per subnet.

        [Gateway Load Balancers] You can specify subnets from one or more Availability Zones. You can't specify Elastic IP addresses for your subnets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmappings
        '''
        result = self._values.get("subnet_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLoadBalancerPropsMixin.SubnetMappingProperty"]]]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the subnets.

        You can specify only one subnet per Availability Zone. You must specify either subnets or subnet mappings, but not both. To specify an Elastic IP address, specify subnet mappings instead of subnets.

        [Application Load Balancers] You must specify subnets from at least two Availability Zones.

        [Application Load Balancers on Outposts] You must specify one Outpost subnet.

        [Application Load Balancers on Local Zones] You can specify subnets from one or more Local Zones.

        [Network Load Balancers and Gateway Load Balancers] You can specify subnets from one or more Availability Zones.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-subnets
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of load balancer.

        The default is ``application`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html#cfn-elasticloadbalancingv2-loadbalancer-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfnLoadBalancerNlbAccessLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnLoadBalancerNlbAccessLogs",
):
    '''Builder for CfnLoadBalancerLogsMixin to generate NLB_ACCESS_LOGS for CfnLoadBalancer.

    :cloudformationResource: AWS::ElasticLoadBalancingV2::LoadBalancer
    :logType: NLB_ACCESS_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
        
        cfn_load_balancer_nlb_access_logs = elasticloadbalancingv2_mixins.CfnLoadBalancerNlbAccessLogs()
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
    ) -> CfnLoadBalancerLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b7c2fd5285227fc29c1e77091fbe5c147f267bd517f1677cca97dbcc4a6991)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnLoadBalancerLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnLoadBalancerLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0057ad6d34907f35d5f44bbde771658360c7c0bc7db3f602a473395c3898bf6a)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnLoadBalancerLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnLoadBalancerLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef113a91a0e02a6d9ec5aada7139824824dd154242bbd42424915757e179420)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnLoadBalancerLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnLoadBalancerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnLoadBalancerPropsMixin",
):
    '''Specifies an Application Load Balancer, a Network Load Balancer, or a Gateway Load Balancer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::LoadBalancer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
        
        cfn_load_balancer_props_mixin = elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin(elasticloadbalancingv2_mixins.CfnLoadBalancerMixinProps(
            enable_capacity_reservation_provision_stabilize=False,
            enable_prefix_for_ipv6_source_nat="enablePrefixForIpv6SourceNat",
            enforce_security_group_inbound_rules_on_private_link_traffic="enforceSecurityGroupInboundRulesOnPrivateLinkTraffic",
            ip_address_type="ipAddressType",
            ipv4_ipam_pool_id="ipv4IpamPoolId",
            load_balancer_attributes=[elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin.LoadBalancerAttributeProperty(
                key="key",
                value="value"
            )],
            minimum_load_balancer_capacity=elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin.MinimumLoadBalancerCapacityProperty(
                capacity_units=123
            ),
            name="name",
            scheme="scheme",
            security_groups=["securityGroups"],
            subnet_mappings=[elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin.SubnetMappingProperty(
                allocation_id="allocationId",
                i_pv6_address="iPv6Address",
                private_iPv4_address="privateIPv4Address",
                source_nat_ipv6_prefix="sourceNatIpv6Prefix",
                subnet_id="subnetId"
            )],
            subnets=["subnets"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLoadBalancerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElasticLoadBalancingV2::LoadBalancer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17634bb3cd1dc716c352daa3abd35d744df6aed19e3823cd9a9d24fa4e77a954)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acfbf579d4aa60e3ed858622c556d0ec64f77724c5b22e6d557cb652c50db4be)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820349c7e727fd62f2e0a07c853ebfe64822ab660dfb1a6625538cf475f8d541)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLoadBalancerMixinProps:
        return typing.cast(CfnLoadBalancerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnLoadBalancerPropsMixin.LoadBalancerAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class LoadBalancerAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an attribute for an Application Load Balancer, a Network Load Balancer, or a Gateway Load Balancer.

            :param key: The name of the attribute. The following attributes are supported by all load balancers: - ``deletion_protection.enabled`` - Indicates whether deletion protection is enabled. The value is ``true`` or ``false`` . The default is ``false`` . - ``load_balancing.cross_zone.enabled`` - Indicates whether cross-zone load balancing is enabled. The possible values are ``true`` and ``false`` . The default for Network Load Balancers and Gateway Load Balancers is ``false`` . The default for Application Load Balancers is ``true`` , and can't be changed. The following attributes are supported by both Application Load Balancers and Network Load Balancers: - ``access_logs.s3.enabled`` - Indicates whether access logs are enabled. The value is ``true`` or ``false`` . The default is ``false`` . - ``access_logs.s3.bucket`` - The name of the S3 bucket for the access logs. This attribute is required if access logs are enabled. The bucket must exist in the same region as the load balancer and have a bucket policy that grants Elastic Load Balancing permissions to write to the bucket. - ``access_logs.s3.prefix`` - The prefix for the location in the S3 bucket for the access logs. - ``ipv6.deny_all_igw_traffic`` - Blocks internet gateway (IGW) access to the load balancer. It is set to ``false`` for internet-facing load balancers and ``true`` for internal load balancers, preventing unintended access to your internal load balancer through an internet gateway. - ``zonal_shift.config.enabled`` - Indicates whether zonal shift is enabled. The possible values are ``true`` and ``false`` . The default is ``false`` . The following attributes are supported by only Application Load Balancers: - ``idle_timeout.timeout_seconds`` - The idle timeout value, in seconds. The valid range is 1-4000 seconds. The default is 60 seconds. - ``client_keep_alive.seconds`` - The client keep alive value, in seconds. The valid range is 60-604800 seconds. The default is 3600 seconds. - ``connection_logs.s3.enabled`` - Indicates whether connection logs are enabled. The value is ``true`` or ``false`` . The default is ``false`` . - ``connection_logs.s3.bucket`` - The name of the S3 bucket for the connection logs. This attribute is required if connection logs are enabled. The bucket must exist in the same region as the load balancer and have a bucket policy that grants Elastic Load Balancing permissions to write to the bucket. - ``connection_logs.s3.prefix`` - The prefix for the location in the S3 bucket for the connection logs. - ``health_check_logs.s3.enabled`` - Indicates whether health check logs are enabled. The value is ``true`` or ``false`` . The default is ``false`` . - ``health_check_logs.s3.bucket`` - The name of the S3 bucket for the health check logs. This attribute is required if health check logs are enabled. The bucket must exist in the same region as the load balancer and have a bucket policy that grants Elastic Load Balancing permissions to write to the bucket. - ``health_check_logs.s3.prefix`` - The prefix for the location in the S3 bucket for the health check logs. - ``routing.http.desync_mitigation_mode`` - Determines how the load balancer handles requests that might pose a security risk to your application. The possible values are ``monitor`` , ``defensive`` , and ``strictest`` . The default is ``defensive`` . - ``routing.http.drop_invalid_header_fields.enabled`` - Indicates whether HTTP headers with invalid header fields are removed by the load balancer ( ``true`` ) or routed to targets ( ``false`` ). The default is ``false`` . - ``routing.http.preserve_host_header.enabled`` - Indicates whether the Application Load Balancer should preserve the ``Host`` header in the HTTP request and send it to the target without any change. The possible values are ``true`` and ``false`` . The default is ``false`` . - ``routing.http.x_amzn_tls_version_and_cipher_suite.enabled`` - Indicates whether the two headers ( ``x-amzn-tls-version`` and ``x-amzn-tls-cipher-suite`` ), which contain information about the negotiated TLS version and cipher suite, are added to the client request before sending it to the target. The ``x-amzn-tls-version`` header has information about the TLS protocol version negotiated with the client, and the ``x-amzn-tls-cipher-suite`` header has information about the cipher suite negotiated with the client. Both headers are in OpenSSL format. The possible values for the attribute are ``true`` and ``false`` . The default is ``false`` . - ``routing.http.xff_client_port.enabled`` - Indicates whether the ``X-Forwarded-For`` header should preserve the source port that the client used to connect to the load balancer. The possible values are ``true`` and ``false`` . The default is ``false`` . - ``routing.http.xff_header_processing.mode`` - Enables you to modify, preserve, or remove the ``X-Forwarded-For`` header in the HTTP request before the Application Load Balancer sends the request to the target. The possible values are ``append`` , ``preserve`` , and ``remove`` . The default is ``append`` . - If the value is ``append`` , the Application Load Balancer adds the client IP address (of the last hop) to the ``X-Forwarded-For`` header in the HTTP request before it sends it to targets. - If the value is ``preserve`` the Application Load Balancer preserves the ``X-Forwarded-For`` header in the HTTP request, and sends it to targets without any change. - If the value is ``remove`` , the Application Load Balancer removes the ``X-Forwarded-For`` header in the HTTP request before it sends it to targets. - ``routing.http2.enabled`` - Indicates whether clients can connect to the load balancer using HTTP/2. If ``true`` , clients can connect using HTTP/2 or HTTP/1.1. However, all client requests are subject to the stricter HTTP/2 header validation rules. For example, message header names must contain only alphanumeric characters and hyphens. If ``false`` , clients must connect using HTTP/1.1. The default is ``true`` . - ``waf.fail_open.enabled`` - Indicates whether to allow a WAF-enabled load balancer to route requests to targets if it is unable to forward the request to AWS WAF. The possible values are ``true`` and ``false`` . The default is ``false`` . The following attributes are supported by only Network Load Balancers: - ``dns_record.client_routing_policy`` - Indicates how traffic is distributed among the load balancer Availability Zones. The possible values are ``availability_zone_affinity`` with 100 percent zonal affinity, ``partial_availability_zone_affinity`` with 85 percent zonal affinity, and ``any_availability_zone`` with 0 percent zonal affinity. - ``secondary_ips.auto_assigned.per_subnet`` - The number of secondary IP addresses to configure for your load balancer nodes. Use to address port allocation errors if you can't add targets. The valid range is 0 to 7. The default is 0. After you set this value, you can't decrease it.
            :param value: The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                load_balancer_attribute_property = elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin.LoadBalancerAttributeProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3bd4efc3af9faf703e6f344d81baafa3474f52433ab82b2892f497d4067d6ff1)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute.

            The following attributes are supported by all load balancers:

            - ``deletion_protection.enabled`` - Indicates whether deletion protection is enabled. The value is ``true`` or ``false`` . The default is ``false`` .
            - ``load_balancing.cross_zone.enabled`` - Indicates whether cross-zone load balancing is enabled. The possible values are ``true`` and ``false`` . The default for Network Load Balancers and Gateway Load Balancers is ``false`` . The default for Application Load Balancers is ``true`` , and can't be changed.

            The following attributes are supported by both Application Load Balancers and Network Load Balancers:

            - ``access_logs.s3.enabled`` - Indicates whether access logs are enabled. The value is ``true`` or ``false`` . The default is ``false`` .
            - ``access_logs.s3.bucket`` - The name of the S3 bucket for the access logs. This attribute is required if access logs are enabled. The bucket must exist in the same region as the load balancer and have a bucket policy that grants Elastic Load Balancing permissions to write to the bucket.
            - ``access_logs.s3.prefix`` - The prefix for the location in the S3 bucket for the access logs.
            - ``ipv6.deny_all_igw_traffic`` - Blocks internet gateway (IGW) access to the load balancer. It is set to ``false`` for internet-facing load balancers and ``true`` for internal load balancers, preventing unintended access to your internal load balancer through an internet gateway.
            - ``zonal_shift.config.enabled`` - Indicates whether zonal shift is enabled. The possible values are ``true`` and ``false`` . The default is ``false`` .

            The following attributes are supported by only Application Load Balancers:

            - ``idle_timeout.timeout_seconds`` - The idle timeout value, in seconds. The valid range is 1-4000 seconds. The default is 60 seconds.
            - ``client_keep_alive.seconds`` - The client keep alive value, in seconds. The valid range is 60-604800 seconds. The default is 3600 seconds.
            - ``connection_logs.s3.enabled`` - Indicates whether connection logs are enabled. The value is ``true`` or ``false`` . The default is ``false`` .
            - ``connection_logs.s3.bucket`` - The name of the S3 bucket for the connection logs. This attribute is required if connection logs are enabled. The bucket must exist in the same region as the load balancer and have a bucket policy that grants Elastic Load Balancing permissions to write to the bucket.
            - ``connection_logs.s3.prefix`` - The prefix for the location in the S3 bucket for the connection logs.
            - ``health_check_logs.s3.enabled`` - Indicates whether health check logs are enabled. The value is ``true`` or ``false`` . The default is ``false`` .
            - ``health_check_logs.s3.bucket`` - The name of the S3 bucket for the health check logs. This attribute is required if health check logs are enabled. The bucket must exist in the same region as the load balancer and have a bucket policy that grants Elastic Load Balancing permissions to write to the bucket.
            - ``health_check_logs.s3.prefix`` - The prefix for the location in the S3 bucket for the health check logs.
            - ``routing.http.desync_mitigation_mode`` - Determines how the load balancer handles requests that might pose a security risk to your application. The possible values are ``monitor`` , ``defensive`` , and ``strictest`` . The default is ``defensive`` .
            - ``routing.http.drop_invalid_header_fields.enabled`` - Indicates whether HTTP headers with invalid header fields are removed by the load balancer ( ``true`` ) or routed to targets ( ``false`` ). The default is ``false`` .
            - ``routing.http.preserve_host_header.enabled`` - Indicates whether the Application Load Balancer should preserve the ``Host`` header in the HTTP request and send it to the target without any change. The possible values are ``true`` and ``false`` . The default is ``false`` .
            - ``routing.http.x_amzn_tls_version_and_cipher_suite.enabled`` - Indicates whether the two headers ( ``x-amzn-tls-version`` and ``x-amzn-tls-cipher-suite`` ), which contain information about the negotiated TLS version and cipher suite, are added to the client request before sending it to the target. The ``x-amzn-tls-version`` header has information about the TLS protocol version negotiated with the client, and the ``x-amzn-tls-cipher-suite`` header has information about the cipher suite negotiated with the client. Both headers are in OpenSSL format. The possible values for the attribute are ``true`` and ``false`` . The default is ``false`` .
            - ``routing.http.xff_client_port.enabled`` - Indicates whether the ``X-Forwarded-For`` header should preserve the source port that the client used to connect to the load balancer. The possible values are ``true`` and ``false`` . The default is ``false`` .
            - ``routing.http.xff_header_processing.mode`` - Enables you to modify, preserve, or remove the ``X-Forwarded-For`` header in the HTTP request before the Application Load Balancer sends the request to the target. The possible values are ``append`` , ``preserve`` , and ``remove`` . The default is ``append`` .
            - If the value is ``append`` , the Application Load Balancer adds the client IP address (of the last hop) to the ``X-Forwarded-For`` header in the HTTP request before it sends it to targets.
            - If the value is ``preserve`` the Application Load Balancer preserves the ``X-Forwarded-For`` header in the HTTP request, and sends it to targets without any change.
            - If the value is ``remove`` , the Application Load Balancer removes the ``X-Forwarded-For`` header in the HTTP request before it sends it to targets.
            - ``routing.http2.enabled`` - Indicates whether clients can connect to the load balancer using HTTP/2. If ``true`` , clients can connect using HTTP/2 or HTTP/1.1. However, all client requests are subject to the stricter HTTP/2 header validation rules. For example, message header names must contain only alphanumeric characters and hyphens. If ``false`` , clients must connect using HTTP/1.1. The default is ``true`` .
            - ``waf.fail_open.enabled`` - Indicates whether to allow a WAF-enabled load balancer to route requests to targets if it is unable to forward the request to AWS WAF. The possible values are ``true`` and ``false`` . The default is ``false`` .

            The following attributes are supported by only Network Load Balancers:

            - ``dns_record.client_routing_policy`` - Indicates how traffic is distributed among the load balancer Availability Zones. The possible values are ``availability_zone_affinity`` with 100 percent zonal affinity, ``partial_availability_zone_affinity`` with 85 percent zonal affinity, and ``any_availability_zone`` with 0 percent zonal affinity.
            - ``secondary_ips.auto_assigned.per_subnet`` - The number of secondary IP addresses to configure for your load balancer nodes. Use to address port allocation errors if you can't add targets. The valid range is 0 to 7. The default is 0. After you set this value, you can't decrease it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattribute.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattribute-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-loadbalancerattribute.html#cfn-elasticloadbalancingv2-loadbalancer-loadbalancerattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoadBalancerAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnLoadBalancerPropsMixin.MinimumLoadBalancerCapacityProperty",
        jsii_struct_bases=[],
        name_mapping={"capacity_units": "capacityUnits"},
    )
    class MinimumLoadBalancerCapacityProperty:
        def __init__(
            self,
            *,
            capacity_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The minimum capacity for a load balancer.

            :param capacity_units: The number of capacity units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-minimumloadbalancercapacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                minimum_load_balancer_capacity_property = elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin.MinimumLoadBalancerCapacityProperty(
                    capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3e422dc7a657bfa64e416a79b1d54468e46ee594fbdd0813885fa9a3213d5afb)
                check_type(argname="argument capacity_units", value=capacity_units, expected_type=type_hints["capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_units is not None:
                self._values["capacity_units"] = capacity_units

        @builtins.property
        def capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The number of capacity units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-minimumloadbalancercapacity.html#cfn-elasticloadbalancingv2-loadbalancer-minimumloadbalancercapacity-capacityunits
            '''
            result = self._values.get("capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MinimumLoadBalancerCapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnLoadBalancerPropsMixin.SubnetMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allocation_id": "allocationId",
            "i_pv6_address": "iPv6Address",
            "private_i_pv4_address": "privateIPv4Address",
            "source_nat_ipv6_prefix": "sourceNatIpv6Prefix",
            "subnet_id": "subnetId",
        },
    )
    class SubnetMappingProperty:
        def __init__(
            self,
            *,
            allocation_id: typing.Optional[builtins.str] = None,
            i_pv6_address: typing.Optional[builtins.str] = None,
            private_i_pv4_address: typing.Optional[builtins.str] = None,
            source_nat_ipv6_prefix: typing.Optional[builtins.str] = None,
            subnet_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a subnet for a load balancer.

            :param allocation_id: [Network Load Balancers] The allocation ID of the Elastic IP address for an internet-facing load balancer.
            :param i_pv6_address: [Network Load Balancers] The IPv6 address.
            :param private_i_pv4_address: [Network Load Balancers] The private IPv4 address for an internal load balancer.
            :param source_nat_ipv6_prefix: [Network Load Balancers with UDP listeners] The IPv6 prefix to use for source NAT. Specify an IPv6 prefix (/80 netmask) from the subnet CIDR block or ``auto_assigned`` to use an IPv6 prefix selected at random from the subnet CIDR block.
            :param subnet_id: The ID of the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                subnet_mapping_property = elasticloadbalancingv2_mixins.CfnLoadBalancerPropsMixin.SubnetMappingProperty(
                    allocation_id="allocationId",
                    i_pv6_address="iPv6Address",
                    private_iPv4_address="privateIPv4Address",
                    source_nat_ipv6_prefix="sourceNatIpv6Prefix",
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac3fda4bdd7b375e01f46ed8e8406edc462920d2f26f8b2e8fdd485cd1349245)
                check_type(argname="argument allocation_id", value=allocation_id, expected_type=type_hints["allocation_id"])
                check_type(argname="argument i_pv6_address", value=i_pv6_address, expected_type=type_hints["i_pv6_address"])
                check_type(argname="argument private_i_pv4_address", value=private_i_pv4_address, expected_type=type_hints["private_i_pv4_address"])
                check_type(argname="argument source_nat_ipv6_prefix", value=source_nat_ipv6_prefix, expected_type=type_hints["source_nat_ipv6_prefix"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_id is not None:
                self._values["allocation_id"] = allocation_id
            if i_pv6_address is not None:
                self._values["i_pv6_address"] = i_pv6_address
            if private_i_pv4_address is not None:
                self._values["private_i_pv4_address"] = private_i_pv4_address
            if source_nat_ipv6_prefix is not None:
                self._values["source_nat_ipv6_prefix"] = source_nat_ipv6_prefix
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id

        @builtins.property
        def allocation_id(self) -> typing.Optional[builtins.str]:
            '''[Network Load Balancers] The allocation ID of the Elastic IP address for an internet-facing load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-allocationid
            '''
            result = self._values.get("allocation_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def i_pv6_address(self) -> typing.Optional[builtins.str]:
            '''[Network Load Balancers] The IPv6 address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-ipv6address
            '''
            result = self._values.get("i_pv6_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_i_pv4_address(self) -> typing.Optional[builtins.str]:
            '''[Network Load Balancers] The private IPv4 address for an internal load balancer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-privateipv4address
            '''
            result = self._values.get("private_i_pv4_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_nat_ipv6_prefix(self) -> typing.Optional[builtins.str]:
            '''[Network Load Balancers with UDP listeners] The IPv6 prefix to use for source NAT.

            Specify an IPv6 prefix (/80 netmask) from the subnet CIDR block or ``auto_assigned`` to use an IPv6 prefix selected at random from the subnet CIDR block.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-sourcenatipv6prefix
            '''
            result = self._values.get("source_nat_ipv6_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-loadbalancer-subnetmapping.html#cfn-elasticloadbalancingv2-loadbalancer-subnetmapping-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubnetMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTargetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "health_check_enabled": "healthCheckEnabled",
        "health_check_interval_seconds": "healthCheckIntervalSeconds",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "health_check_timeout_seconds": "healthCheckTimeoutSeconds",
        "healthy_threshold_count": "healthyThresholdCount",
        "ip_address_type": "ipAddressType",
        "matcher": "matcher",
        "name": "name",
        "port": "port",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
        "tags": "tags",
        "target_control_port": "targetControlPort",
        "target_group_attributes": "targetGroupAttributes",
        "targets": "targets",
        "target_type": "targetType",
        "unhealthy_threshold_count": "unhealthyThresholdCount",
        "vpc_id": "vpcId",
    },
)
class CfnTargetGroupMixinProps:
    def __init__(
        self,
        *,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[builtins.str] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
        healthy_threshold_count: typing.Optional[jsii.Number] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        matcher: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTargetGroupPropsMixin.MatcherProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        protocol_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_control_port: typing.Optional[jsii.Number] = None,
        target_group_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTargetGroupPropsMixin.TargetGroupAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTargetGroupPropsMixin.TargetDescriptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        target_type: typing.Optional[builtins.str] = None,
        unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTargetGroupPropsMixin.

        :param health_check_enabled: Indicates whether health checks are enabled. If the target type is ``lambda`` , health checks are disabled by default but can be enabled. If the target type is ``instance`` , ``ip`` , or ``alb`` , health checks are always enabled and can't be disabled.
        :param health_check_interval_seconds: The approximate amount of time, in seconds, between health checks of an individual target. The range is 5-300. If the target group protocol is TCP, TLS, UDP, TCP_UDP, QUIC, TCP_QUIC, HTTP or HTTPS, the default is 30 seconds. If the target group protocol is GENEVE, the default is 10 seconds. If the target type is ``lambda`` , the default is 35 seconds.
        :param health_check_path: [HTTP/HTTPS health checks] The destination for health checks on the targets. [HTTP1 or HTTP2 protocol version] The ping path. The default is /. [GRPC protocol version] The path of a custom health check method with the format /package.service/method. The default is / AWS .ALB/healthcheck.
        :param health_check_port: The port the load balancer uses when performing health checks on targets. If the protocol is HTTP, HTTPS, TCP, TLS, UDP, TCP_UDP, QUIC, or TCP_QUIC the default is ``traffic-port`` , which is the port on which each target receives traffic from the load balancer. If the protocol is GENEVE, the default is port 80.
        :param health_check_protocol: The protocol the load balancer uses when performing health checks on targets. For Application Load Balancers, the default is HTTP. For Network Load Balancers and Gateway Load Balancers, the default is TCP. The TCP protocol is not supported for health checks if the protocol of the target group is HTTP or HTTPS. The GENEVE, TLS, UDP, TCP_UDP, QUIC, and TCP_QUIC protocols are not supported for health checks.
        :param health_check_timeout_seconds: The amount of time, in seconds, during which no response from a target means a failed health check. The range is 2–120 seconds. For target groups with a protocol of HTTP, the default is 6 seconds. For target groups with a protocol of TCP, TLS or HTTPS, the default is 10 seconds. For target groups with a protocol of GENEVE, the default is 5 seconds. If the target type is ``lambda`` , the default is 30 seconds.
        :param healthy_threshold_count: The number of consecutive health check successes required before considering a target healthy. The range is 2-10. If the target group protocol is TCP, TCP_UDP, UDP, TLS, HTTP or HTTPS, the default is 5. For target groups with a protocol of GENEVE, the default is 5. If the target type is ``lambda`` , the default is 5.
        :param ip_address_type: The IP address type. The default value is ``ipv4`` .
        :param matcher: [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking for a successful response from a target. For target groups with a protocol of TCP, TCP_UDP, UDP, QUIC, TCP_QUIC, or TLS the range is 200-599. For target groups with a protocol of HTTP or HTTPS, the range is 200-499. For target groups with a protocol of GENEVE, the range is 200-399.
        :param name: The name of the target group. This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen.
        :param port: The port on which the targets receive traffic. This port is used unless you specify a port override when registering the target. If the target is a Lambda function, this parameter does not apply. If the protocol is GENEVE, the supported port is 6081.
        :param protocol: The protocol to use for routing traffic to the targets. For Application Load Balancers, the supported protocols are HTTP and HTTPS. For Network Load Balancers, the supported protocols are TCP, TLS, UDP, TCP_UDP, QUIC, or TCP_QUIC. For Gateway Load Balancers, the supported protocol is GENEVE. A TCP_UDP listener must be associated with a TCP_UDP target group. A TCP_QUIC listener must be associated with a TCP_QUIC target group. If the target is a Lambda function, this parameter does not apply.
        :param protocol_version: [HTTP/HTTPS protocol] The protocol version. The possible values are ``GRPC`` , ``HTTP1`` , and ``HTTP2`` .
        :param tags: The tags.
        :param target_control_port: The port on which the target control agent and application load balancer exchange management traffic for the target optimizer feature.
        :param target_group_attributes: The target group attributes. Attributes that you do not modify retain their current values.
        :param targets: The targets.
        :param target_type: The type of target that you must specify when registering targets with this target group. You can't specify targets for a target group using more than one target type. - ``instance`` - Register targets by instance ID. This is the default value. - ``ip`` - Register targets by IP address. You can specify IP addresses from the subnets of the virtual private cloud (VPC) for the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify publicly routable IP addresses. - ``lambda`` - Register a single Lambda function as a target. - ``alb`` - Register a single Application Load Balancer as a target.
        :param unhealthy_threshold_count: The number of consecutive health check failures required before considering a target unhealthy. The range is 2-10. If the target group protocol is TCP, TCP_UDP, UDP, TLS, QUIC, TCP_QUIC, HTTP or HTTPS, the default is 2. For target groups with a protocol of GENEVE, the default is 2. If the target type is ``lambda`` , the default is 5.
        :param vpc_id: The identifier of the virtual private cloud (VPC). If the target is a Lambda function, this parameter does not apply. Otherwise, this parameter is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
            
            cfn_target_group_mixin_props = elasticloadbalancingv2_mixins.CfnTargetGroupMixinProps(
                health_check_enabled=False,
                health_check_interval_seconds=123,
                health_check_path="healthCheckPath",
                health_check_port="healthCheckPort",
                health_check_protocol="healthCheckProtocol",
                health_check_timeout_seconds=123,
                healthy_threshold_count=123,
                ip_address_type="ipAddressType",
                matcher=elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin.MatcherProperty(
                    grpc_code="grpcCode",
                    http_code="httpCode"
                ),
                name="name",
                port=123,
                protocol="protocol",
                protocol_version="protocolVersion",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_control_port=123,
                target_group_attributes=[elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin.TargetGroupAttributeProperty(
                    key="key",
                    value="value"
                )],
                targets=[elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin.TargetDescriptionProperty(
                    availability_zone="availabilityZone",
                    id="id",
                    port=123,
                    quic_server_id="quicServerId"
                )],
                target_type="targetType",
                unhealthy_threshold_count=123,
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f56a4f0480826af06f2b7d1c6fc8d84b3aa7cbb862933bf2ac49648044a3994)
            check_type(argname="argument health_check_enabled", value=health_check_enabled, expected_type=type_hints["health_check_enabled"])
            check_type(argname="argument health_check_interval_seconds", value=health_check_interval_seconds, expected_type=type_hints["health_check_interval_seconds"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument health_check_port", value=health_check_port, expected_type=type_hints["health_check_port"])
            check_type(argname="argument health_check_protocol", value=health_check_protocol, expected_type=type_hints["health_check_protocol"])
            check_type(argname="argument health_check_timeout_seconds", value=health_check_timeout_seconds, expected_type=type_hints["health_check_timeout_seconds"])
            check_type(argname="argument healthy_threshold_count", value=healthy_threshold_count, expected_type=type_hints["healthy_threshold_count"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_control_port", value=target_control_port, expected_type=type_hints["target_control_port"])
            check_type(argname="argument target_group_attributes", value=target_group_attributes, expected_type=type_hints["target_group_attributes"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
            check_type(argname="argument unhealthy_threshold_count", value=unhealthy_threshold_count, expected_type=type_hints["unhealthy_threshold_count"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if health_check_enabled is not None:
            self._values["health_check_enabled"] = health_check_enabled
        if health_check_interval_seconds is not None:
            self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if health_check_timeout_seconds is not None:
            self._values["health_check_timeout_seconds"] = health_check_timeout_seconds
        if healthy_threshold_count is not None:
            self._values["healthy_threshold_count"] = healthy_threshold_count
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if matcher is not None:
            self._values["matcher"] = matcher
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if tags is not None:
            self._values["tags"] = tags
        if target_control_port is not None:
            self._values["target_control_port"] = target_control_port
        if target_group_attributes is not None:
            self._values["target_group_attributes"] = target_group_attributes
        if targets is not None:
            self._values["targets"] = targets
        if target_type is not None:
            self._values["target_type"] = target_type
        if unhealthy_threshold_count is not None:
            self._values["unhealthy_threshold_count"] = unhealthy_threshold_count
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether health checks are enabled.

        If the target type is ``lambda`` , health checks are disabled by default but can be enabled. If the target type is ``instance`` , ``ip`` , or ``alb`` , health checks are always enabled and can't be disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckenabled
        '''
        result = self._values.get("health_check_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''The approximate amount of time, in seconds, between health checks of an individual target.

        The range is 5-300. If the target group protocol is TCP, TLS, UDP, TCP_UDP, QUIC, TCP_QUIC, HTTP or HTTPS, the default is 30 seconds. If the target group protocol is GENEVE, the default is 10 seconds. If the target type is ``lambda`` , the default is 35 seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckintervalseconds
        '''
        result = self._values.get("health_check_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''[HTTP/HTTPS health checks] The destination for health checks on the targets.

        [HTTP1 or HTTP2 protocol version] The ping path. The default is /.

        [GRPC protocol version] The path of a custom health check method with the format /package.service/method. The default is / AWS .ALB/healthcheck.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckpath
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_port(self) -> typing.Optional[builtins.str]:
        '''The port the load balancer uses when performing health checks on targets.

        If the protocol is HTTP, HTTPS, TCP, TLS, UDP, TCP_UDP, QUIC, or TCP_QUIC the default is ``traffic-port`` , which is the port on which each target receives traffic from the load balancer. If the protocol is GENEVE, the default is port 80.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckport
        '''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol the load balancer uses when performing health checks on targets.

        For Application Load Balancers, the default is HTTP. For Network Load Balancers and Gateway Load Balancers, the default is TCP. The TCP protocol is not supported for health checks if the protocol of the target group is HTTP or HTTPS. The GENEVE, TLS, UDP, TCP_UDP, QUIC, and TCP_QUIC protocols are not supported for health checks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthcheckprotocol
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''The amount of time, in seconds, during which no response from a target means a failed health check.

        The range is 2–120 seconds. For target groups with a protocol of HTTP, the default is 6 seconds. For target groups with a protocol of TCP, TLS or HTTPS, the default is 10 seconds. For target groups with a protocol of GENEVE, the default is 5 seconds. If the target type is ``lambda`` , the default is 30 seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthchecktimeoutseconds
        '''
        result = self._values.get("health_check_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive health check successes required before considering a target healthy.

        The range is 2-10. If the target group protocol is TCP, TCP_UDP, UDP, TLS, HTTP or HTTPS, the default is 5. For target groups with a protocol of GENEVE, the default is 5. If the target type is ``lambda`` , the default is 5.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-healthythresholdcount
        '''
        result = self._values.get("healthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''The IP address type.

        The default value is ``ipv4`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def matcher(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.MatcherProperty"]]:
        '''[HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking for a successful response from a target.

        For target groups with a protocol of TCP, TCP_UDP, UDP, QUIC, TCP_QUIC, or TLS the range is 200-599. For target groups with a protocol of HTTP or HTTPS, the range is 200-499. For target groups with a protocol of GENEVE, the range is 200-399.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-matcher
        '''
        result = self._values.get("matcher")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.MatcherProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the target group.

        This name must be unique per region per account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port on which the targets receive traffic.

        This port is used unless you specify a port override when registering the target. If the target is a Lambda function, this parameter does not apply. If the protocol is GENEVE, the supported port is 6081.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol to use for routing traffic to the targets.

        For Application Load Balancers, the supported protocols are HTTP and HTTPS. For Network Load Balancers, the supported protocols are TCP, TLS, UDP, TCP_UDP, QUIC, or TCP_QUIC. For Gateway Load Balancers, the supported protocol is GENEVE. A TCP_UDP listener must be associated with a TCP_UDP target group. A TCP_QUIC listener must be associated with a TCP_QUIC target group. If the target is a Lambda function, this parameter does not apply.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_version(self) -> typing.Optional[builtins.str]:
        '''[HTTP/HTTPS protocol] The protocol version.

        The possible values are ``GRPC`` , ``HTTP1`` , and ``HTTP2`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-protocolversion
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_control_port(self) -> typing.Optional[jsii.Number]:
        '''The port on which the target control agent and application load balancer exchange management traffic for the target optimizer feature.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targetcontrolport
        '''
        result = self._values.get("target_control_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_group_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.TargetGroupAttributeProperty"]]]]:
        '''The target group attributes.

        Attributes that you do not modify retain their current values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattributes
        '''
        result = self._values.get("target_group_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.TargetGroupAttributeProperty"]]]], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.TargetDescriptionProperty"]]]]:
        '''The targets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTargetGroupPropsMixin.TargetDescriptionProperty"]]]], result)

    @builtins.property
    def target_type(self) -> typing.Optional[builtins.str]:
        '''The type of target that you must specify when registering targets with this target group.

        You can't specify targets for a target group using more than one target type.

        - ``instance`` - Register targets by instance ID. This is the default value.
        - ``ip`` - Register targets by IP address. You can specify IP addresses from the subnets of the virtual private cloud (VPC) for the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify publicly routable IP addresses.
        - ``lambda`` - Register a single Lambda function as a target.
        - ``alb`` - Register a single Application Load Balancer as a target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-targettype
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive health check failures required before considering a target unhealthy.

        The range is 2-10. If the target group protocol is TCP, TCP_UDP, UDP, TLS, QUIC, TCP_QUIC, HTTP or HTTPS, the default is 2. For target groups with a protocol of GENEVE, the default is 2. If the target type is ``lambda`` , the default is 5.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-unhealthythresholdcount
        '''
        result = self._values.get("unhealthy_threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the virtual private cloud (VPC).

        If the target is a Lambda function, this parameter does not apply. Otherwise, this parameter is required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html#cfn-elasticloadbalancingv2-targetgroup-vpcid
        '''
        result = self._values.get("vpc_id")
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
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTargetGroupPropsMixin",
):
    '''Specifies a target group for an Application Load Balancer, a Network Load Balancer, or a Gateway Load Balancer.

    Before you register a Lambda function as a target, you must create a ``AWS::Lambda::Permission`` resource that grants the Elastic Load Balancing service principal permission to invoke the Lambda function.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-targetgroup.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::TargetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
        
        cfn_target_group_props_mixin = elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin(elasticloadbalancingv2_mixins.CfnTargetGroupMixinProps(
            health_check_enabled=False,
            health_check_interval_seconds=123,
            health_check_path="healthCheckPath",
            health_check_port="healthCheckPort",
            health_check_protocol="healthCheckProtocol",
            health_check_timeout_seconds=123,
            healthy_threshold_count=123,
            ip_address_type="ipAddressType",
            matcher=elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin.MatcherProperty(
                grpc_code="grpcCode",
                http_code="httpCode"
            ),
            name="name",
            port=123,
            protocol="protocol",
            protocol_version="protocolVersion",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_control_port=123,
            target_group_attributes=[elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin.TargetGroupAttributeProperty(
                key="key",
                value="value"
            )],
            targets=[elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin.TargetDescriptionProperty(
                availability_zone="availabilityZone",
                id="id",
                port=123,
                quic_server_id="quicServerId"
            )],
            target_type="targetType",
            unhealthy_threshold_count=123,
            vpc_id="vpcId"
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
        '''Create a mixin to apply properties to ``AWS::ElasticLoadBalancingV2::TargetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e298cff45ee7b60e5b36ca88d00ea9012fd40cef14a2330c94fa46d5a8f5ad4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eecfb4d446c79456d1876e93f642576d47888a7e9fe376861f258e19766b2cce)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f97dd90339604918076758f4650d0417ad1c220cadf2d60077d1fdd5f2e7b9e)
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
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTargetGroupPropsMixin.MatcherProperty",
        jsii_struct_bases=[],
        name_mapping={"grpc_code": "grpcCode", "http_code": "httpCode"},
    )
    class MatcherProperty:
        def __init__(
            self,
            *,
            grpc_code: typing.Optional[builtins.str] = None,
            http_code: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the HTTP codes that healthy targets must use when responding to an HTTP health check.

            :param grpc_code: You can specify values between 0 and 99. You can specify multiple values (for example, "0,1") or a range of values (for example, "0-5"). The default value is 12.
            :param http_code: For Application Load Balancers, you can specify values between 200 and 499, with the default value being 200. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299"). For Network Load Balancers, you can specify values between 200 and 599, with the default value being 200-399. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299"). For Gateway Load Balancers, this must be "200–399". Note that when using shorthand syntax, some values such as commas need to be escaped.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                matcher_property = elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin.MatcherProperty(
                    grpc_code="grpcCode",
                    http_code="httpCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ccf480d74424e9174ab76df40056ce252eb7835ee18eb39d5db2458d8ca6a443)
                check_type(argname="argument grpc_code", value=grpc_code, expected_type=type_hints["grpc_code"])
                check_type(argname="argument http_code", value=http_code, expected_type=type_hints["http_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if grpc_code is not None:
                self._values["grpc_code"] = grpc_code
            if http_code is not None:
                self._values["http_code"] = http_code

        @builtins.property
        def grpc_code(self) -> typing.Optional[builtins.str]:
            '''You can specify values between 0 and 99.

            You can specify multiple values (for example, "0,1") or a range of values (for example, "0-5"). The default value is 12.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html#cfn-elasticloadbalancingv2-targetgroup-matcher-grpccode
            '''
            result = self._values.get("grpc_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_code(self) -> typing.Optional[builtins.str]:
            '''For Application Load Balancers, you can specify values between 200 and 499, with the default value being 200.

            You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").

            For Network Load Balancers, you can specify values between 200 and 599, with the default value being 200-399. You can specify multiple values (for example, "200,202") or a range of values (for example, "200-299").

            For Gateway Load Balancers, this must be "200–399".

            Note that when using shorthand syntax, some values such as commas need to be escaped.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-matcher.html#cfn-elasticloadbalancingv2-targetgroup-matcher-httpcode
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
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTargetGroupPropsMixin.TargetDescriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "id": "id",
            "port": "port",
            "quic_server_id": "quicServerId",
        },
    )
    class TargetDescriptionProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            quic_server_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a target to add to a target group.

            :param availability_zone: An Availability Zone or ``all`` . This determines whether the target receives traffic from the load balancer nodes in the specified Availability Zone or from all enabled Availability Zones for the load balancer. For Application Load Balancer target groups, the specified Availability Zone value is only applicable when cross-zone load balancing is off. Otherwise the parameter is ignored and treated as ``all`` . This parameter is not supported if the target type of the target group is ``instance`` or ``alb`` . If the target type is ``ip`` and the IP address is in a subnet of the VPC for the target group, the Availability Zone is automatically detected and this parameter is optional. If the IP address is outside the VPC, this parameter is required. For Application Load Balancer target groups with cross-zone load balancing off, if the target type is ``ip`` and the IP address is outside of the VPC for the target group, this should be an Availability Zone inside the VPC for the target group. If the target type is ``lambda`` , this parameter is optional and the only supported value is ``all`` .
            :param id: The ID of the target. If the target type of the target group is ``instance`` , specify an instance ID. If the target type is ``ip`` , specify an IP address. If the target type is ``lambda`` , specify the ARN of the Lambda function. If the target type is ``alb`` , specify the ARN of the Application Load Balancer target.
            :param port: The port on which the target is listening. If the target group protocol is GENEVE, the supported port is 6081. If the target type is ``alb`` , the targeted Application Load Balancer must have at least one listener whose port matches the target group port. This parameter is not used if the target is a Lambda function.
            :param quic_server_id: The server ID for the targets. This value is required if the protocol is ``QUIC`` or ``TCP_QUIC`` and can't be used with other protocols. The ID consists of the ``0x`` prefix followed by 16 hexadecimal characters. Any letters must be lowercase. The value must be unique at the listener level. You can't modify the server ID for a registered target. You must deregister the target and then provide a new server ID when you register the target again.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                target_description_property = elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin.TargetDescriptionProperty(
                    availability_zone="availabilityZone",
                    id="id",
                    port=123,
                    quic_server_id="quicServerId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e47eda529e310819bd8ab70b476e6fe9bb345aabb085b1e48c1182cd06f06c90)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument quic_server_id", value=quic_server_id, expected_type=type_hints["quic_server_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if id is not None:
                self._values["id"] = id
            if port is not None:
                self._values["port"] = port
            if quic_server_id is not None:
                self._values["quic_server_id"] = quic_server_id

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''An Availability Zone or ``all`` .

            This determines whether the target receives traffic from the load balancer nodes in the specified Availability Zone or from all enabled Availability Zones for the load balancer.

            For Application Load Balancer target groups, the specified Availability Zone value is only applicable when cross-zone load balancing is off. Otherwise the parameter is ignored and treated as ``all`` .

            This parameter is not supported if the target type of the target group is ``instance`` or ``alb`` .

            If the target type is ``ip`` and the IP address is in a subnet of the VPC for the target group, the Availability Zone is automatically detected and this parameter is optional. If the IP address is outside the VPC, this parameter is required.

            For Application Load Balancer target groups with cross-zone load balancing off, if the target type is ``ip`` and the IP address is outside of the VPC for the target group, this should be an Availability Zone inside the VPC for the target group.

            If the target type is ``lambda`` , this parameter is optional and the only supported value is ``all`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the target.

            If the target type of the target group is ``instance`` , specify an instance ID. If the target type is ``ip`` , specify an IP address. If the target type is ``lambda`` , specify the ARN of the Lambda function. If the target type is ``alb`` , specify the ARN of the Application Load Balancer target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port on which the target is listening.

            If the target group protocol is GENEVE, the supported port is 6081. If the target type is ``alb`` , the targeted Application Load Balancer must have at least one listener whose port matches the target group port. This parameter is not used if the target is a Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def quic_server_id(self) -> typing.Optional[builtins.str]:
            '''The server ID for the targets.

            This value is required if the protocol is ``QUIC`` or ``TCP_QUIC`` and can't be used with other protocols.

            The ID consists of the ``0x`` prefix followed by 16 hexadecimal characters. Any letters must be lowercase. The value must be unique at the listener level. You can't modify the server ID for a registered target. You must deregister the target and then provide a new server ID when you register the target again.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetdescription.html#cfn-elasticloadbalancingv2-targetgroup-targetdescription-quicserverid
            '''
            result = self._values.get("quic_server_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetDescriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTargetGroupPropsMixin.TargetGroupAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TargetGroupAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a target group attribute.

            :param key: The name of the attribute. The following attributes are supported by all load balancers: - ``deregistration_delay.timeout_seconds`` - The amount of time, in seconds, for Elastic Load Balancing to wait before changing the state of a deregistering target from ``draining`` to ``unused`` . The range is 0-3600 seconds. The default value is 300 seconds. If the target is a Lambda function, this attribute is not supported. - ``stickiness.enabled`` - Indicates whether target stickiness is enabled. The value is ``true`` or ``false`` . The default is ``false`` . - ``stickiness.type`` - Indicates the type of stickiness. The possible values are: - ``lb_cookie`` and ``app_cookie`` for Application Load Balancers. - ``source_ip`` for Network Load Balancers. - ``source_ip_dest_ip`` and ``source_ip_dest_ip_proto`` for Gateway Load Balancers. The following attributes are supported by Application Load Balancers and Network Load Balancers: - ``load_balancing.cross_zone.enabled`` - Indicates whether cross zone load balancing is enabled. The value is ``true`` , ``false`` or ``use_load_balancer_configuration`` . The default is ``use_load_balancer_configuration`` . - ``target_group_health.dns_failover.minimum_healthy_targets.count`` - The minimum number of targets that must be healthy. If the number of healthy targets is below this value, mark the zone as unhealthy in DNS, so that traffic is routed only to healthy zones. The possible values are ``off`` or an integer from 1 to the maximum number of targets. The default is 1. - ``target_group_health.dns_failover.minimum_healthy_targets.percentage`` - The minimum percentage of targets that must be healthy. If the percentage of healthy targets is below this value, mark the zone as unhealthy in DNS, so that traffic is routed only to healthy zones. The possible values are ``off`` or an integer from 1 to 100. The default is ``off`` . - ``target_group_health.unhealthy_state_routing.minimum_healthy_targets.count`` - The minimum number of targets that must be healthy. If the number of healthy targets is below this value, send traffic to all targets, including unhealthy targets. The possible values are 1 to the maximum number of targets. The default is 1. - ``target_group_health.unhealthy_state_routing.minimum_healthy_targets.percentage`` - The minimum percentage of targets that must be healthy. If the percentage of healthy targets is below this value, send traffic to all targets, including unhealthy targets. The possible values are ``off`` or an integer from 1 to 100. The default is ``off`` . The following attributes are supported only if the load balancer is an Application Load Balancer and the target is an instance or an IP address: - ``load_balancing.algorithm.type`` - The load balancing algorithm determines how the load balancer selects targets when routing requests. The value is ``round_robin`` , ``least_outstanding_requests`` , or ``weighted_random`` . The default is ``round_robin`` . - ``load_balancing.algorithm.anomaly_mitigation`` - Only available when ``load_balancing.algorithm.type`` is ``weighted_random`` . Indicates whether anomaly mitigation is enabled. The value is ``on`` or ``off`` . The default is ``off`` . - ``slow_start.duration_seconds`` - The time period, in seconds, during which a newly registered target receives an increasing share of the traffic to the target group. After this time period ends, the target receives its full share of traffic. The range is 30-900 seconds (15 minutes). The default is 0 seconds (disabled). - ``stickiness.app_cookie.cookie_name`` - Indicates the name of the application-based cookie. Names that start with the following prefixes are not allowed: ``AWSALB`` , ``AWSALBAPP`` , and ``AWSALBTG`` ; they're reserved for use by the load balancer. - ``stickiness.app_cookie.duration_seconds`` - The time period, in seconds, during which requests from a client should be routed to the same target. After this time period expires, the application-based cookie is considered stale. The range is 1 second to 1 week (604800 seconds). The default value is 1 day (86400 seconds). - ``stickiness.lb_cookie.duration_seconds`` - The time period, in seconds, during which requests from a client should be routed to the same target. After this time period expires, the load balancer-generated cookie is considered stale. The range is 1 second to 1 week (604800 seconds). The default value is 1 day (86400 seconds). The following attribute is supported only if the load balancer is an Application Load Balancer and the target is a Lambda function: - ``lambda.multi_value_headers.enabled`` - Indicates whether the request and response headers that are exchanged between the load balancer and the Lambda function include arrays of values or strings. The value is ``true`` or ``false`` . The default is ``false`` . If the value is ``false`` and the request contains a duplicate header field name or query parameter key, the load balancer uses the last value sent by the client. The following attributes are supported only by Network Load Balancers: - ``deregistration_delay.connection_termination.enabled`` - Indicates whether the load balancer terminates connections at the end of the deregistration timeout. The value is ``true`` or ``false`` . For new UDP/TCP_UDP target groups the default is ``true`` . Otherwise, the default is ``false`` . - ``preserve_client_ip.enabled`` - Indicates whether client IP preservation is enabled. The value is ``true`` or ``false`` . The default is disabled if the target group type is IP address and the target group protocol is TCP or TLS. Otherwise, the default is enabled. Client IP preservation can't be disabled for UDP and TCP_UDP target groups. - ``proxy_protocol_v2.enabled`` - Indicates whether Proxy Protocol version 2 is enabled. The value is ``true`` or ``false`` . The default is ``false`` . - ``target_health_state.unhealthy.connection_termination.enabled`` - Indicates whether the load balancer terminates connections to unhealthy targets. The value is ``true`` or ``false`` . The default is ``true`` . This attribute can't be enabled for UDP and TCP_UDP target groups. - ``target_health_state.unhealthy.draining_interval_seconds`` - The amount of time for Elastic Load Balancing to wait before changing the state of an unhealthy target from ``unhealthy.draining`` to ``unhealthy`` . The range is 0-360000 seconds. The default value is 0 seconds. Note: This attribute can only be configured when ``target_health_state.unhealthy.connection_termination.enabled`` is ``false`` . The following attributes are supported only by Gateway Load Balancers: - ``target_failover.on_deregistration`` - Indicates how the Gateway Load Balancer handles existing flows when a target is deregistered. The possible values are ``rebalance`` and ``no_rebalance`` . The default is ``no_rebalance`` . The two attributes ( ``target_failover.on_deregistration`` and ``target_failover.on_unhealthy`` ) can't be set independently. The value you set for both attributes must be the same. - ``target_failover.on_unhealthy`` - Indicates how the Gateway Load Balancer handles existing flows when a target is unhealthy. The possible values are ``rebalance`` and ``no_rebalance`` . The default is ``no_rebalance`` . The two attributes ( ``target_failover.on_deregistration`` and ``target_failover.on_unhealthy`` ) can't be set independently. The value you set for both attributes must be the same.
            :param value: The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                target_group_attribute_property = elasticloadbalancingv2_mixins.CfnTargetGroupPropsMixin.TargetGroupAttributeProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e06b1bf67317411ed881924e77fa37e6f331975b19cce36f380714388e094d60)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute.

            The following attributes are supported by all load balancers:

            - ``deregistration_delay.timeout_seconds`` - The amount of time, in seconds, for Elastic Load Balancing to wait before changing the state of a deregistering target from ``draining`` to ``unused`` . The range is 0-3600 seconds. The default value is 300 seconds. If the target is a Lambda function, this attribute is not supported.
            - ``stickiness.enabled`` - Indicates whether target stickiness is enabled. The value is ``true`` or ``false`` . The default is ``false`` .
            - ``stickiness.type`` - Indicates the type of stickiness. The possible values are:
            - ``lb_cookie`` and ``app_cookie`` for Application Load Balancers.
            - ``source_ip`` for Network Load Balancers.
            - ``source_ip_dest_ip`` and ``source_ip_dest_ip_proto`` for Gateway Load Balancers.

            The following attributes are supported by Application Load Balancers and Network Load Balancers:

            - ``load_balancing.cross_zone.enabled`` - Indicates whether cross zone load balancing is enabled. The value is ``true`` , ``false`` or ``use_load_balancer_configuration`` . The default is ``use_load_balancer_configuration`` .
            - ``target_group_health.dns_failover.minimum_healthy_targets.count`` - The minimum number of targets that must be healthy. If the number of healthy targets is below this value, mark the zone as unhealthy in DNS, so that traffic is routed only to healthy zones. The possible values are ``off`` or an integer from 1 to the maximum number of targets. The default is 1.
            - ``target_group_health.dns_failover.minimum_healthy_targets.percentage`` - The minimum percentage of targets that must be healthy. If the percentage of healthy targets is below this value, mark the zone as unhealthy in DNS, so that traffic is routed only to healthy zones. The possible values are ``off`` or an integer from 1 to 100. The default is ``off`` .
            - ``target_group_health.unhealthy_state_routing.minimum_healthy_targets.count`` - The minimum number of targets that must be healthy. If the number of healthy targets is below this value, send traffic to all targets, including unhealthy targets. The possible values are 1 to the maximum number of targets. The default is 1.
            - ``target_group_health.unhealthy_state_routing.minimum_healthy_targets.percentage`` - The minimum percentage of targets that must be healthy. If the percentage of healthy targets is below this value, send traffic to all targets, including unhealthy targets. The possible values are ``off`` or an integer from 1 to 100. The default is ``off`` .

            The following attributes are supported only if the load balancer is an Application Load Balancer and the target is an instance or an IP address:

            - ``load_balancing.algorithm.type`` - The load balancing algorithm determines how the load balancer selects targets when routing requests. The value is ``round_robin`` , ``least_outstanding_requests`` , or ``weighted_random`` . The default is ``round_robin`` .
            - ``load_balancing.algorithm.anomaly_mitigation`` - Only available when ``load_balancing.algorithm.type`` is ``weighted_random`` . Indicates whether anomaly mitigation is enabled. The value is ``on`` or ``off`` . The default is ``off`` .
            - ``slow_start.duration_seconds`` - The time period, in seconds, during which a newly registered target receives an increasing share of the traffic to the target group. After this time period ends, the target receives its full share of traffic. The range is 30-900 seconds (15 minutes). The default is 0 seconds (disabled).
            - ``stickiness.app_cookie.cookie_name`` - Indicates the name of the application-based cookie. Names that start with the following prefixes are not allowed: ``AWSALB`` , ``AWSALBAPP`` , and ``AWSALBTG`` ; they're reserved for use by the load balancer.
            - ``stickiness.app_cookie.duration_seconds`` - The time period, in seconds, during which requests from a client should be routed to the same target. After this time period expires, the application-based cookie is considered stale. The range is 1 second to 1 week (604800 seconds). The default value is 1 day (86400 seconds).
            - ``stickiness.lb_cookie.duration_seconds`` - The time period, in seconds, during which requests from a client should be routed to the same target. After this time period expires, the load balancer-generated cookie is considered stale. The range is 1 second to 1 week (604800 seconds). The default value is 1 day (86400 seconds).

            The following attribute is supported only if the load balancer is an Application Load Balancer and the target is a Lambda function:

            - ``lambda.multi_value_headers.enabled`` - Indicates whether the request and response headers that are exchanged between the load balancer and the Lambda function include arrays of values or strings. The value is ``true`` or ``false`` . The default is ``false`` . If the value is ``false`` and the request contains a duplicate header field name or query parameter key, the load balancer uses the last value sent by the client.

            The following attributes are supported only by Network Load Balancers:

            - ``deregistration_delay.connection_termination.enabled`` - Indicates whether the load balancer terminates connections at the end of the deregistration timeout. The value is ``true`` or ``false`` . For new UDP/TCP_UDP target groups the default is ``true`` . Otherwise, the default is ``false`` .
            - ``preserve_client_ip.enabled`` - Indicates whether client IP preservation is enabled. The value is ``true`` or ``false`` . The default is disabled if the target group type is IP address and the target group protocol is TCP or TLS. Otherwise, the default is enabled. Client IP preservation can't be disabled for UDP and TCP_UDP target groups.
            - ``proxy_protocol_v2.enabled`` - Indicates whether Proxy Protocol version 2 is enabled. The value is ``true`` or ``false`` . The default is ``false`` .
            - ``target_health_state.unhealthy.connection_termination.enabled`` - Indicates whether the load balancer terminates connections to unhealthy targets. The value is ``true`` or ``false`` . The default is ``true`` . This attribute can't be enabled for UDP and TCP_UDP target groups.
            - ``target_health_state.unhealthy.draining_interval_seconds`` - The amount of time for Elastic Load Balancing to wait before changing the state of an unhealthy target from ``unhealthy.draining`` to ``unhealthy`` . The range is 0-360000 seconds. The default value is 0 seconds.

            Note: This attribute can only be configured when ``target_health_state.unhealthy.connection_termination.enabled`` is ``false`` .

            The following attributes are supported only by Gateway Load Balancers:

            - ``target_failover.on_deregistration`` - Indicates how the Gateway Load Balancer handles existing flows when a target is deregistered. The possible values are ``rebalance`` and ``no_rebalance`` . The default is ``no_rebalance`` . The two attributes ( ``target_failover.on_deregistration`` and ``target_failover.on_unhealthy`` ) can't be set independently. The value you set for both attributes must be the same.
            - ``target_failover.on_unhealthy`` - Indicates how the Gateway Load Balancer handles existing flows when a target is unhealthy. The possible values are ``rebalance`` and ``no_rebalance`` . The default is ``no_rebalance`` . The two attributes ( ``target_failover.on_deregistration`` and ``target_failover.on_unhealthy`` ) can't be set independently. The value you set for both attributes must be the same.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html#cfn-elasticloadbalancingv2-targetgroup-targetgroupattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTrustStoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ca_certificates_bundle_s3_bucket": "caCertificatesBundleS3Bucket",
        "ca_certificates_bundle_s3_key": "caCertificatesBundleS3Key",
        "ca_certificates_bundle_s3_object_version": "caCertificatesBundleS3ObjectVersion",
        "name": "name",
        "tags": "tags",
    },
)
class CfnTrustStoreMixinProps:
    def __init__(
        self,
        *,
        ca_certificates_bundle_s3_bucket: typing.Optional[builtins.str] = None,
        ca_certificates_bundle_s3_key: typing.Optional[builtins.str] = None,
        ca_certificates_bundle_s3_object_version: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTrustStorePropsMixin.

        :param ca_certificates_bundle_s3_bucket: The Amazon S3 bucket for the ca certificates bundle.
        :param ca_certificates_bundle_s3_key: The Amazon S3 path for the ca certificates bundle.
        :param ca_certificates_bundle_s3_object_version: The Amazon S3 object version for the ca certificates bundle. If undefined the current version is used.
        :param name: The name of the trust store.
        :param tags: The tags to assign to the trust store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
            
            cfn_trust_store_mixin_props = elasticloadbalancingv2_mixins.CfnTrustStoreMixinProps(
                ca_certificates_bundle_s3_bucket="caCertificatesBundleS3Bucket",
                ca_certificates_bundle_s3_key="caCertificatesBundleS3Key",
                ca_certificates_bundle_s3_object_version="caCertificatesBundleS3ObjectVersion",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c0c5e60dd4620f8742ae439c2cfd8cc03e032a296ac018ed4e4aa42237e153)
            check_type(argname="argument ca_certificates_bundle_s3_bucket", value=ca_certificates_bundle_s3_bucket, expected_type=type_hints["ca_certificates_bundle_s3_bucket"])
            check_type(argname="argument ca_certificates_bundle_s3_key", value=ca_certificates_bundle_s3_key, expected_type=type_hints["ca_certificates_bundle_s3_key"])
            check_type(argname="argument ca_certificates_bundle_s3_object_version", value=ca_certificates_bundle_s3_object_version, expected_type=type_hints["ca_certificates_bundle_s3_object_version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ca_certificates_bundle_s3_bucket is not None:
            self._values["ca_certificates_bundle_s3_bucket"] = ca_certificates_bundle_s3_bucket
        if ca_certificates_bundle_s3_key is not None:
            self._values["ca_certificates_bundle_s3_key"] = ca_certificates_bundle_s3_key
        if ca_certificates_bundle_s3_object_version is not None:
            self._values["ca_certificates_bundle_s3_object_version"] = ca_certificates_bundle_s3_object_version
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ca_certificates_bundle_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 bucket for the ca certificates bundle.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststore.html#cfn-elasticloadbalancingv2-truststore-cacertificatesbundles3bucket
        '''
        result = self._values.get("ca_certificates_bundle_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_certificates_bundle_s3_key(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 path for the ca certificates bundle.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststore.html#cfn-elasticloadbalancingv2-truststore-cacertificatesbundles3key
        '''
        result = self._values.get("ca_certificates_bundle_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_certificates_bundle_s3_object_version(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 object version for the ca certificates bundle.

        If undefined the current version is used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststore.html#cfn-elasticloadbalancingv2-truststore-cacertificatesbundles3objectversion
        '''
        result = self._values.get("ca_certificates_bundle_s3_object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the trust store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststore.html#cfn-elasticloadbalancingv2-truststore-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to assign to the trust store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststore.html#cfn-elasticloadbalancingv2-truststore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrustStoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrustStorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTrustStorePropsMixin",
):
    '''Creates a trust store.

    You must specify ``CaCertificatesBundleS3Bucket`` and ``CaCertificatesBundleS3Key`` . When you create a trust store, you must specify ``Name`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststore.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::TrustStore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
        
        cfn_trust_store_props_mixin = elasticloadbalancingv2_mixins.CfnTrustStorePropsMixin(elasticloadbalancingv2_mixins.CfnTrustStoreMixinProps(
            ca_certificates_bundle_s3_bucket="caCertificatesBundleS3Bucket",
            ca_certificates_bundle_s3_key="caCertificatesBundleS3Key",
            ca_certificates_bundle_s3_object_version="caCertificatesBundleS3ObjectVersion",
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
        props: typing.Union[CfnTrustStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElasticLoadBalancingV2::TrustStore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a7527b1fd1337564f1ff6453078a4afe93a676096fbdcc45ae341a9f7cff33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8173cb041e4f8eb5b3975d479789468ecb2b40424da9cc87d7033c29c4f815d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2d8679703550ef96398b3714670995a51efc519adc33f8e279393ee37784fa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrustStoreMixinProps:
        return typing.cast(CfnTrustStoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTrustStoreRevocationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "revocation_contents": "revocationContents",
        "trust_store_arn": "trustStoreArn",
    },
)
class CfnTrustStoreRevocationMixinProps:
    def __init__(
        self,
        *,
        revocation_contents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrustStoreRevocationPropsMixin.RevocationContentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        trust_store_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTrustStoreRevocationPropsMixin.

        :param revocation_contents: The revocation file to add.
        :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststorerevocation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
            
            cfn_trust_store_revocation_mixin_props = elasticloadbalancingv2_mixins.CfnTrustStoreRevocationMixinProps(
                revocation_contents=[elasticloadbalancingv2_mixins.CfnTrustStoreRevocationPropsMixin.RevocationContentProperty(
                    revocation_type="revocationType",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion"
                )],
                trust_store_arn="trustStoreArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472cd0e80390dca4458ea06ac19198dc51718da392ad6b1e5f516f763d190f59)
            check_type(argname="argument revocation_contents", value=revocation_contents, expected_type=type_hints["revocation_contents"])
            check_type(argname="argument trust_store_arn", value=trust_store_arn, expected_type=type_hints["trust_store_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if revocation_contents is not None:
            self._values["revocation_contents"] = revocation_contents
        if trust_store_arn is not None:
            self._values["trust_store_arn"] = trust_store_arn

    @builtins.property
    def revocation_contents(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrustStoreRevocationPropsMixin.RevocationContentProperty"]]]]:
        '''The revocation file to add.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststorerevocation.html#cfn-elasticloadbalancingv2-truststorerevocation-revocationcontents
        '''
        result = self._values.get("revocation_contents")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrustStoreRevocationPropsMixin.RevocationContentProperty"]]]], result)

    @builtins.property
    def trust_store_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the trust store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststorerevocation.html#cfn-elasticloadbalancingv2-truststorerevocation-truststorearn
        '''
        result = self._values.get("trust_store_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrustStoreRevocationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrustStoreRevocationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTrustStoreRevocationPropsMixin",
):
    '''Adds the specified revocation contents to the specified trust store.

    You must specify ``TrustStoreArn`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-truststorerevocation.html
    :cloudformationResource: AWS::ElasticLoadBalancingV2::TrustStoreRevocation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
        
        cfn_trust_store_revocation_props_mixin = elasticloadbalancingv2_mixins.CfnTrustStoreRevocationPropsMixin(elasticloadbalancingv2_mixins.CfnTrustStoreRevocationMixinProps(
            revocation_contents=[elasticloadbalancingv2_mixins.CfnTrustStoreRevocationPropsMixin.RevocationContentProperty(
                revocation_type="revocationType",
                s3_bucket="s3Bucket",
                s3_key="s3Key",
                s3_object_version="s3ObjectVersion"
            )],
            trust_store_arn="trustStoreArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTrustStoreRevocationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ElasticLoadBalancingV2::TrustStoreRevocation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93bd08de6f6559f86296f36ccc698e5292ca075b6698e76fc933802bc2aa1534)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9bbd16ea4863380709ac1956703d87ce3720f5890a8839f08cdf7a9004bc382)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3461beb8029f5293541f51d175ab65b50a109c948f15045a66a8af74bfaad6a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrustStoreRevocationMixinProps:
        return typing.cast(CfnTrustStoreRevocationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTrustStoreRevocationPropsMixin.RevocationContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "revocation_type": "revocationType",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
            "s3_object_version": "s3ObjectVersion",
        },
    )
    class RevocationContentProperty:
        def __init__(
            self,
            *,
            revocation_type: typing.Optional[builtins.str] = None,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
            s3_object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a revocation file.

            You must specify ``S3Bucket`` and ``S3Key`` .

            :param revocation_type: The type of revocation file.
            :param s3_bucket: The Amazon S3 bucket for the revocation file.
            :param s3_key: The Amazon S3 path for the revocation file.
            :param s3_object_version: The Amazon S3 object version of the revocation file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-revocationcontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                revocation_content_property = elasticloadbalancingv2_mixins.CfnTrustStoreRevocationPropsMixin.RevocationContentProperty(
                    revocation_type="revocationType",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key",
                    s3_object_version="s3ObjectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6503dfc0b26fd477d6f05c9f04c477cb3d4edfdb7ce7cda4aac47a3440c83abe)
                check_type(argname="argument revocation_type", value=revocation_type, expected_type=type_hints["revocation_type"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
                check_type(argname="argument s3_object_version", value=s3_object_version, expected_type=type_hints["s3_object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if revocation_type is not None:
                self._values["revocation_type"] = revocation_type
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version

        @builtins.property
        def revocation_type(self) -> typing.Optional[builtins.str]:
            '''The type of revocation file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-revocationcontent.html#cfn-elasticloadbalancingv2-truststorerevocation-revocationcontent-revocationtype
            '''
            result = self._values.get("revocation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket for the revocation file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-revocationcontent.html#cfn-elasticloadbalancingv2-truststorerevocation-revocationcontent-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 path for the revocation file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-revocationcontent.html#cfn-elasticloadbalancingv2-truststorerevocation-revocationcontent-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 object version of the revocation file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-revocationcontent.html#cfn-elasticloadbalancingv2-truststorerevocation-revocationcontent-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RevocationContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_elasticloadbalancingv2.mixins.CfnTrustStoreRevocationPropsMixin.TrustStoreRevocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "number_of_revoked_entries": "numberOfRevokedEntries",
            "revocation_id": "revocationId",
            "revocation_type": "revocationType",
            "trust_store_arn": "trustStoreArn",
        },
    )
    class TrustStoreRevocationProperty:
        def __init__(
            self,
            *,
            number_of_revoked_entries: typing.Optional[jsii.Number] = None,
            revocation_id: typing.Optional[builtins.str] = None,
            revocation_type: typing.Optional[builtins.str] = None,
            trust_store_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a revocation file in use by a trust store.

            :param number_of_revoked_entries: The number of revoked certificates.
            :param revocation_id: The revocation ID of the revocation file.
            :param revocation_type: The type of revocation file.
            :param trust_store_arn: The Amazon Resource Name (ARN) of the trust store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-truststorerevocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_elasticloadbalancingv2 import mixins as elasticloadbalancingv2_mixins
                
                trust_store_revocation_property = elasticloadbalancingv2_mixins.CfnTrustStoreRevocationPropsMixin.TrustStoreRevocationProperty(
                    number_of_revoked_entries=123,
                    revocation_id="revocationId",
                    revocation_type="revocationType",
                    trust_store_arn="trustStoreArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e50f589e840a69cf6b6de5cbc2428a12eb29eb32a7784532f39ce85253d578a3)
                check_type(argname="argument number_of_revoked_entries", value=number_of_revoked_entries, expected_type=type_hints["number_of_revoked_entries"])
                check_type(argname="argument revocation_id", value=revocation_id, expected_type=type_hints["revocation_id"])
                check_type(argname="argument revocation_type", value=revocation_type, expected_type=type_hints["revocation_type"])
                check_type(argname="argument trust_store_arn", value=trust_store_arn, expected_type=type_hints["trust_store_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if number_of_revoked_entries is not None:
                self._values["number_of_revoked_entries"] = number_of_revoked_entries
            if revocation_id is not None:
                self._values["revocation_id"] = revocation_id
            if revocation_type is not None:
                self._values["revocation_type"] = revocation_type
            if trust_store_arn is not None:
                self._values["trust_store_arn"] = trust_store_arn

        @builtins.property
        def number_of_revoked_entries(self) -> typing.Optional[jsii.Number]:
            '''The number of revoked certificates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-truststorerevocation.html#cfn-elasticloadbalancingv2-truststorerevocation-truststorerevocation-numberofrevokedentries
            '''
            result = self._values.get("number_of_revoked_entries")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def revocation_id(self) -> typing.Optional[builtins.str]:
            '''The revocation ID of the revocation file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-truststorerevocation.html#cfn-elasticloadbalancingv2-truststorerevocation-truststorerevocation-revocationid
            '''
            result = self._values.get("revocation_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def revocation_type(self) -> typing.Optional[builtins.str]:
            '''The type of revocation file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-truststorerevocation.html#cfn-elasticloadbalancingv2-truststorerevocation-truststorerevocation-revocationtype
            '''
            result = self._values.get("revocation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trust_store_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the trust store.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-truststorerevocation-truststorerevocation.html#cfn-elasticloadbalancingv2-truststorerevocation-truststorerevocation-truststorearn
            '''
            result = self._values.get("trust_store_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrustStoreRevocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnListenerCertificateMixinProps",
    "CfnListenerCertificatePropsMixin",
    "CfnListenerMixinProps",
    "CfnListenerPropsMixin",
    "CfnListenerRuleMixinProps",
    "CfnListenerRulePropsMixin",
    "CfnLoadBalancerLogsMixin",
    "CfnLoadBalancerMixinProps",
    "CfnLoadBalancerNlbAccessLogs",
    "CfnLoadBalancerPropsMixin",
    "CfnTargetGroupMixinProps",
    "CfnTargetGroupPropsMixin",
    "CfnTrustStoreMixinProps",
    "CfnTrustStorePropsMixin",
    "CfnTrustStoreRevocationMixinProps",
    "CfnTrustStoreRevocationPropsMixin",
]

publication.publish()

def _typecheckingstub__8dd4a0920ebd9083a8b6884831e95a1ca30c77b6c4b49241c1a98a499ff91b09(
    *,
    certificates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerCertificatePropsMixin.CertificateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    listener_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52cc605200dff47f364b1296ed5142468adaaadc9a05cf0e5a4b197f2097af11(
    props: typing.Union[CfnListenerCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb36165841822a2beb662efa7765ed40dd7b31a2242cfcdc83ed84616a8d9041(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b940234e5b147001411793655ec14f3537298241850051153bffbc864e987ed6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf665640a0b849aea40c0099a6ac5b7f18cf0c9fefdd753e076f397eae50e75(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a54e0531834474855b49794758830af6eb94e7a6d8d4187da28e9d51346ff6(
    *,
    alpn_policy: typing.Optional[typing.Sequence[builtins.str]] = None,
    certificates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.CertificateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    default_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    listener_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.ListenerAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    load_balancer_arn: typing.Optional[builtins.str] = None,
    mutual_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.MutualAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611b2b4e1db18db78ba3801600a74f03b790c74ceb3d08b9afa7e1b4d9e97d3c(
    props: typing.Union[CfnListenerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b741337cb3742f325e9b5a9dd202eb0264c0d65b92011415d7dc94eb783cc63d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138efa762549808ca303d6c600cb4445426bd2dbdaea7ea4269e1650b1ad2564(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6ae4e175bcc0b912c38eb71850cf0605c31e0949744750bbe30d5a50c3491d(
    *,
    authenticate_cognito_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.AuthenticateCognitoConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    authenticate_oidc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.AuthenticateOidcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fixed_response_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.FixedResponseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    forward_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.ForwardConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    jwt_validation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.JwtValidationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    order: typing.Optional[jsii.Number] = None,
    redirect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.RedirectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_group_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98fb1886a3f069e3ea658db4c42aa2259b299948743e3891aba72e7c72d36de(
    *,
    authentication_request_extra_params: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    on_unauthenticated_request: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    session_cookie_name: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[builtins.str] = None,
    user_pool_arn: typing.Optional[builtins.str] = None,
    user_pool_client_id: typing.Optional[builtins.str] = None,
    user_pool_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1bc80f9f9f49c0c4bf22eaf904be3c7a3c050e4dfdd476c7661c05ceebbd7a(
    *,
    authentication_request_extra_params: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    authorization_endpoint: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    on_unauthenticated_request: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    session_cookie_name: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[builtins.str] = None,
    token_endpoint: typing.Optional[builtins.str] = None,
    use_existing_client_secret: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    user_info_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a8febd7d4e4609847159309ef3f72605700533e5fd8be5c05bcdda2f456eb0(
    *,
    certificate_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720f82e9d76e0fe00881e4ed805683d1871292b734e79d3bb8f2a449366a7541(
    *,
    content_type: typing.Optional[builtins.str] = None,
    message_body: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba4fa84071e1576afe45fd42f5750c3f883e20780a6d4f2c9103e0b20d13757(
    *,
    target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.TargetGroupTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_group_stickiness_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.TargetGroupStickinessConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca6baf40c1611e72da9e6c172ce9ed97e9c666f3c6932883342baf029dd9d1a(
    *,
    format: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffddb1d47dc3f20a4e25c1b9d989d83c711537563cd49a742ea8456c1f72387(
    *,
    additional_claims: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerPropsMixin.JwtValidationActionAdditionalClaimProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    issuer: typing.Optional[builtins.str] = None,
    jwks_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bda0779c9d7a9a7f6f294c5910ffb7406dc222fd98399051ce81254faff668(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da49eeb51af3bf6cf7086262ea378fe86da5a86d61f0d3977969352b27a45c30(
    *,
    advertise_trust_store_ca_names: typing.Optional[builtins.str] = None,
    ignore_client_certificate_expiry: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    mode: typing.Optional[builtins.str] = None,
    trust_store_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2a3315d2d259b2825b700441a6286a8ff73072084c23213ccb8298f5cfbde2(
    *,
    host: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    query: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc0dc6dba13be8372e183d073e38ab39c10f63a44b0d11107184df25273942c(
    *,
    duration_seconds: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aef165b7060984ab0cd9301bba1dddd35d809b79f0807926b788a6774871ec6(
    *,
    target_group_arn: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea08f4f4b1a53b43adc7323321cddd555635073ac1aa82b6c9668bdf3d94874(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.RuleConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    listener_arn: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    transforms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.TransformProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15479d312fceb9ae3ee3d0ac0fecc320eaeb0b527d94a64253f869f31107c7d(
    props: typing.Union[CfnListenerRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8bb3d3ed776a4b23d9486fa5a160342b87c6dfa557d1a9a503bf9fdfeb8457(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5860e55e710d556e04fce55dc515e71f0e91b8d4f4c173e56b25c7042c871454(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d0669b581ef3dd0491b5b6fa4a693a2831a56fca9272464b441db8731a2772(
    *,
    authenticate_cognito_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.AuthenticateCognitoConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    authenticate_oidc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.AuthenticateOidcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fixed_response_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.FixedResponseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    forward_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.ForwardConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    jwt_validation_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.JwtValidationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    order: typing.Optional[jsii.Number] = None,
    redirect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.RedirectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_group_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f794b505aa15c193a9425640c0ea50b463ad07e73a7f3f7330decd52328fcbdc(
    *,
    authentication_request_extra_params: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    on_unauthenticated_request: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    session_cookie_name: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
    user_pool_arn: typing.Optional[builtins.str] = None,
    user_pool_client_id: typing.Optional[builtins.str] = None,
    user_pool_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156e06f0da43a4b71d4a85a923aa120fe5fba81a4a4a4186aa8d1a0e57fd0089(
    *,
    authentication_request_extra_params: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    authorization_endpoint: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    on_unauthenticated_request: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    session_cookie_name: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
    token_endpoint: typing.Optional[builtins.str] = None,
    use_existing_client_secret: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    user_info_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17fa2051d8d9f311ead5336a60a8b0bc6ae627f819c6cec79ec5cac432ad8d3e(
    *,
    content_type: typing.Optional[builtins.str] = None,
    message_body: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4247c16ea7d9e81887d43e40f9a5cf8948d56e3b2106b51d8858bda7b171d83e(
    *,
    target_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.TargetGroupTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_group_stickiness_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.TargetGroupStickinessConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6cd5fa6094eeaf9e0a34093cb72f9ee2913b8eb9489d369b06127c65111ab04(
    *,
    regex_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82afa754d2183edb46229da7253561c0bf5afb887ecad6c2edd980322e4f78d(
    *,
    http_header_name: typing.Optional[builtins.str] = None,
    regex_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bb8b9a58c7606ccbeb741f73a47b2eae46b76991fca484b7d19b0164e38a7b(
    *,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155795b8b53918d8e249d68aa0b58c2ceec02c3e0b737a2f8a1e7dc84a14f8ff(
    *,
    format: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4881da15ef93699aeab31b1095ce236507b5a59defdb43451b737a07290e4fcd(
    *,
    additional_claims: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.JwtValidationActionAdditionalClaimProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    issuer: typing.Optional[builtins.str] = None,
    jwks_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24070f52616f8426e9871ad2c63a33d7bab2fb1d715c539d26c323dbe2245f00(
    *,
    regex_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830791bf4de3573dac6c0b6b758d53cae934431a1e83c8ac5e5e633f86170a13(
    *,
    values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.QueryStringKeyValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f53b371064128611e16b475b6e39045e21016cae5ff726ad920fea2b9be6bf(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6b0e432bbb900701173eb76d7db590b7313643eb184198dc7b0064a68d0f8d(
    *,
    host: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    query: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c46adf1532088f895c2b86c4e0f216b98f0b08d1ab15eadf8773f16e079d802(
    *,
    rewrites: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.RewriteConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5a411efc3ddee921b236d1a2337f5e385d9c34b119678b8d3cb3d01a402a35(
    *,
    regex: typing.Optional[builtins.str] = None,
    replace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d26139e1f026ae7622ca192057e867dc5863d9350c24e1ef6675c38332429d(
    *,
    field: typing.Optional[builtins.str] = None,
    host_header_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.HostHeaderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_header_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.HttpHeaderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_request_method_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.HttpRequestMethodConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    path_pattern_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.PathPatternConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    query_string_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.QueryStringConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    regex_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_ip_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.SourceIpConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d529a7ac2cdedd83105eb6a5a355b24d3ae79903316ca86de97beb00e1bb8c9(
    *,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefa1b3687b6050545bf8fdcdbbcd3bb8125a5f344b46ad1e3fb6edad7fd8f95(
    *,
    duration_seconds: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f331c4d3033f215ffdef674f5f799cb75dad01369b879280714d8246eea9021(
    *,
    target_group_arn: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5763572884fc0ab981b00d58b7b30076af5a7a0285e55c9f09b6cd64fb86654a(
    *,
    host_header_rewrite_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.RewriteConfigObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    url_rewrite_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnListenerRulePropsMixin.RewriteConfigObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b848bb4689a98590b8a6fc047bafa7a29fd77d0479ef3b786049c84f916fe02d(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6347508044aef58390c2e951930478ca1748f1808b2e95ccbe023e500bc026e(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ddadc9aab0991bd8e586a6c33aeb9089405abe394b02532e7e1e4554f98111(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a2fb6ae18a559290eca5f22e663aed9fbcba3fd09d40a214d6b2d73d43eaf2(
    *,
    enable_capacity_reservation_provision_stabilize: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_prefix_for_ipv6_source_nat: typing.Optional[builtins.str] = None,
    enforce_security_group_inbound_rules_on_private_link_traffic: typing.Optional[builtins.str] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    ipv4_ipam_pool_id: typing.Optional[builtins.str] = None,
    load_balancer_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.LoadBalancerAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    minimum_load_balancer_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.MinimumLoadBalancerCapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    scheme: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLoadBalancerPropsMixin.SubnetMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b7c2fd5285227fc29c1e77091fbe5c147f267bd517f1677cca97dbcc4a6991(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0057ad6d34907f35d5f44bbde771658360c7c0bc7db3f602a473395c3898bf6a(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef113a91a0e02a6d9ec5aada7139824824dd154242bbd42424915757e179420(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17634bb3cd1dc716c352daa3abd35d744df6aed19e3823cd9a9d24fa4e77a954(
    props: typing.Union[CfnLoadBalancerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfbf579d4aa60e3ed858622c556d0ec64f77724c5b22e6d557cb652c50db4be(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820349c7e727fd62f2e0a07c853ebfe64822ab660dfb1a6625538cf475f8d541(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd4efc3af9faf703e6f344d81baafa3474f52433ab82b2892f497d4067d6ff1(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e422dc7a657bfa64e416a79b1d54468e46ee594fbdd0813885fa9a3213d5afb(
    *,
    capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3fda4bdd7b375e01f46ed8e8406edc462920d2f26f8b2e8fdd485cd1349245(
    *,
    allocation_id: typing.Optional[builtins.str] = None,
    i_pv6_address: typing.Optional[builtins.str] = None,
    private_i_pv4_address: typing.Optional[builtins.str] = None,
    source_nat_ipv6_prefix: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f56a4f0480826af06f2b7d1c6fc8d84b3aa7cbb862933bf2ac49648044a3994(
    *,
    health_check_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    health_check_interval_seconds: typing.Optional[jsii.Number] = None,
    health_check_path: typing.Optional[builtins.str] = None,
    health_check_port: typing.Optional[builtins.str] = None,
    health_check_protocol: typing.Optional[builtins.str] = None,
    health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
    healthy_threshold_count: typing.Optional[jsii.Number] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    matcher: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTargetGroupPropsMixin.MatcherProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_control_port: typing.Optional[jsii.Number] = None,
    target_group_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTargetGroupPropsMixin.TargetGroupAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTargetGroupPropsMixin.TargetDescriptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    target_type: typing.Optional[builtins.str] = None,
    unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e298cff45ee7b60e5b36ca88d00ea9012fd40cef14a2330c94fa46d5a8f5ad4(
    props: typing.Union[CfnTargetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eecfb4d446c79456d1876e93f642576d47888a7e9fe376861f258e19766b2cce(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f97dd90339604918076758f4650d0417ad1c220cadf2d60077d1fdd5f2e7b9e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf480d74424e9174ab76df40056ce252eb7835ee18eb39d5db2458d8ca6a443(
    *,
    grpc_code: typing.Optional[builtins.str] = None,
    http_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47eda529e310819bd8ab70b476e6fe9bb345aabb085b1e48c1182cd06f06c90(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    quic_server_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06b1bf67317411ed881924e77fa37e6f331975b19cce36f380714388e094d60(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c0c5e60dd4620f8742ae439c2cfd8cc03e032a296ac018ed4e4aa42237e153(
    *,
    ca_certificates_bundle_s3_bucket: typing.Optional[builtins.str] = None,
    ca_certificates_bundle_s3_key: typing.Optional[builtins.str] = None,
    ca_certificates_bundle_s3_object_version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a7527b1fd1337564f1ff6453078a4afe93a676096fbdcc45ae341a9f7cff33(
    props: typing.Union[CfnTrustStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8173cb041e4f8eb5b3975d479789468ecb2b40424da9cc87d7033c29c4f815d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2d8679703550ef96398b3714670995a51efc519adc33f8e279393ee37784fa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472cd0e80390dca4458ea06ac19198dc51718da392ad6b1e5f516f763d190f59(
    *,
    revocation_contents: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrustStoreRevocationPropsMixin.RevocationContentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    trust_store_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93bd08de6f6559f86296f36ccc698e5292ca075b6698e76fc933802bc2aa1534(
    props: typing.Union[CfnTrustStoreRevocationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bbd16ea4863380709ac1956703d87ce3720f5890a8839f08cdf7a9004bc382(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3461beb8029f5293541f51d175ab65b50a109c948f15045a66a8af74bfaad6a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6503dfc0b26fd477d6f05c9f04c477cb3d4edfdb7ce7cda4aac47a3440c83abe(
    *,
    revocation_type: typing.Optional[builtins.str] = None,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_key: typing.Optional[builtins.str] = None,
    s3_object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e50f589e840a69cf6b6de5cbc2428a12eb29eb32a7784532f39ce85253d578a3(
    *,
    number_of_revoked_entries: typing.Optional[jsii.Number] = None,
    revocation_id: typing.Optional[builtins.str] = None,
    revocation_type: typing.Optional[builtins.str] = None,
    trust_store_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
