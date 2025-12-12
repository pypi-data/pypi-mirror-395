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
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.interfaces.aws_guardduty as _aws_cdk_interfaces_aws_guardduty_ceddda9d


class DetectorEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents",
):
    '''(experimental) EventBridge event patterns for Detector.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
        from aws_cdk.interfaces import aws_guardduty as interfaces_guardduty
        
        # detector_ref: interfaces_guardduty.IDetectorRef
        
        detector_events = guardduty_events.DetectorEvents.from_detector(detector_ref)
    '''

    @jsii.member(jsii_name="fromDetector")
    @builtins.classmethod
    def from_detector(
        cls,
        detector_ref: _aws_cdk_interfaces_aws_guardduty_ceddda9d.IDetectorRef,
    ) -> "DetectorEvents":
        '''(experimental) Create DetectorEvents from a Detector reference.

        :param detector_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2ed68f21b5de2203dd9426bc451d5e6795e90fab35300d03fd0111488cebde)
            check_type(argname="argument detector_ref", value=detector_ref, expected_type=type_hints["detector_ref"])
        return typing.cast("DetectorEvents", jsii.sinvoke(cls, "fromDetector", [detector_ref]))

    @jsii.member(jsii_name="guardDutyFindingPattern")
    def guard_duty_finding_pattern(
        self,
        *,
        account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        arn: typing.Optional[typing.Sequence[builtins.str]] = None,
        created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[typing.Sequence[builtins.str]] = None,
        partition: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Resource", typing.Dict[builtins.str, typing.Any]]] = None,
        schema_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        service: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Service", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Sequence[builtins.str]] = None,
        title: typing.Optional[typing.Sequence[builtins.str]] = None,
        type: typing.Optional[typing.Sequence[builtins.str]] = None,
        updated_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Detector GuardDuty Finding.

        :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param description: (experimental) description property. Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param partition: (experimental) partition property. Specify an array of string values to match this event if the actual value of partition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param region: (experimental) region property. Specify an array of string values to match this event if the actual value of region is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param resource: (experimental) resource property. Specify an array of string values to match this event if the actual value of resource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param schema_version: (experimental) schemaVersion property. Specify an array of string values to match this event if the actual value of schemaVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param service: (experimental) service property. Specify an array of string values to match this event if the actual value of service is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param severity: (experimental) severity property. Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param title: (experimental) title property. Specify an array of string values to match this event if the actual value of title is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param updated_at: (experimental) updatedAt property. Specify an array of string values to match this event if the actual value of updatedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DetectorEvents.GuardDutyFinding.GuardDutyFindingProps(
            account_id=account_id,
            arn=arn,
            created_at=created_at,
            description=description,
            event_metadata=event_metadata,
            id=id,
            partition=partition,
            region=region,
            resource=resource,
            schema_version=schema_version,
            service=service,
            severity=severity,
            title=title,
            type=type,
            updated_at=updated_at,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "guardDutyFindingPattern", [options]))

    class GuardDutyFinding(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding",
    ):
        '''(experimental) aws.guardduty@GuardDutyFinding event types for Detector.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
            
            guard_duty_finding = guardduty_events.DetectorEvents.GuardDutyFinding()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.AccessControlList",
            jsii_struct_bases=[],
            name_mapping={
                "allows_public_read_access": "allowsPublicReadAccess",
                "allows_public_write_access": "allowsPublicWriteAccess",
            },
        )
        class AccessControlList:
            def __init__(
                self,
                *,
                allows_public_read_access: typing.Optional[typing.Sequence[builtins.str]] = None,
                allows_public_write_access: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AccessControlList.

                :param allows_public_read_access: (experimental) allowsPublicReadAccess property. Specify an array of string values to match this event if the actual value of allowsPublicReadAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param allows_public_write_access: (experimental) allowsPublicWriteAccess property. Specify an array of string values to match this event if the actual value of allowsPublicWriteAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    access_control_list = guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                        allows_public_read_access=["allowsPublicReadAccess"],
                        allows_public_write_access=["allowsPublicWriteAccess"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__bdf230a77c1ae2921dd5e96d011b389bbba9d62e719e60888e273e27fe44456c)
                    check_type(argname="argument allows_public_read_access", value=allows_public_read_access, expected_type=type_hints["allows_public_read_access"])
                    check_type(argname="argument allows_public_write_access", value=allows_public_write_access, expected_type=type_hints["allows_public_write_access"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if allows_public_read_access is not None:
                    self._values["allows_public_read_access"] = allows_public_read_access
                if allows_public_write_access is not None:
                    self._values["allows_public_write_access"] = allows_public_write_access

            @builtins.property
            def allows_public_read_access(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) allowsPublicReadAccess property.

                Specify an array of string values to match this event if the actual value of allowsPublicReadAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("allows_public_read_access")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def allows_public_write_access(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) allowsPublicWriteAccess property.

                Specify an array of string values to match this event if the actual value of allowsPublicWriteAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("allows_public_write_access")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AccessControlList(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.AccessKeyDetails",
            jsii_struct_bases=[],
            name_mapping={
                "access_key_id": "accessKeyId",
                "principal_id": "principalId",
                "user_name": "userName",
                "user_type": "userType",
            },
        )
        class AccessKeyDetails:
            def __init__(
                self,
                *,
                access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AccessKeyDetails.

                :param access_key_id: (experimental) accessKeyId property. Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_name: (experimental) userName property. Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_type: (experimental) userType property. Specify an array of string values to match this event if the actual value of userType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    access_key_details = guardduty_events.DetectorEvents.GuardDutyFinding.AccessKeyDetails(
                        access_key_id=["accessKeyId"],
                        principal_id=["principalId"],
                        user_name=["userName"],
                        user_type=["userType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7dec947658ddcc560e486e8ea48b738916cb3aeef4090706ff72bf649ef0244d)
                    check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                    check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
                    check_type(argname="argument user_type", value=user_type, expected_type=type_hints["user_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if access_key_id is not None:
                    self._values["access_key_id"] = access_key_id
                if principal_id is not None:
                    self._values["principal_id"] = principal_id
                if user_name is not None:
                    self._values["user_name"] = user_name
                if user_type is not None:
                    self._values["user_type"] = user_type

            @builtins.property
            def access_key_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accessKeyId property.

                Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("access_key_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def principal_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) principalId property.

                Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("principal_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userName property.

                Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userType property.

                Specify an array of string values to match this event if the actual value of userType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AccessKeyDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.AccountLevelPermissions",
            jsii_struct_bases=[],
            name_mapping={"block_public_access": "blockPublicAccess"},
        )
        class AccountLevelPermissions:
            def __init__(
                self,
                *,
                block_public_access: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.BlockPublicAccess", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for AccountLevelPermissions.

                :param block_public_access: (experimental) blockPublicAccess property. Specify an array of string values to match this event if the actual value of blockPublicAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    account_level_permissions = guardduty_events.DetectorEvents.GuardDutyFinding.AccountLevelPermissions(
                        block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                            block_public_acls=["blockPublicAcls"],
                            block_public_policy=["blockPublicPolicy"],
                            ignore_public_acls=["ignorePublicAcls"],
                            restrict_public_buckets=["restrictPublicBuckets"]
                        )
                    )
                '''
                if isinstance(block_public_access, dict):
                    block_public_access = DetectorEvents.GuardDutyFinding.BlockPublicAccess(**block_public_access)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c66a78f2cd84ba6f94ad571c83a29f5e4c05730084b58f89738a2147fbc98cf9)
                    check_type(argname="argument block_public_access", value=block_public_access, expected_type=type_hints["block_public_access"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if block_public_access is not None:
                    self._values["block_public_access"] = block_public_access

            @builtins.property
            def block_public_access(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.BlockPublicAccess"]:
                '''(experimental) blockPublicAccess property.

                Specify an array of string values to match this event if the actual value of blockPublicAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("block_public_access")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.BlockPublicAccess"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AccountLevelPermissions(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Action",
            jsii_struct_bases=[],
            name_mapping={
                "action_type": "actionType",
                "aws_api_call_action": "awsApiCallAction",
                "dns_request_action": "dnsRequestAction",
                "kubernetes_api_call_action": "kubernetesApiCallAction",
                "network_connection_action": "networkConnectionAction",
                "port_probe_action": "portProbeAction",
            },
        )
        class Action:
            def __init__(
                self,
                *,
                action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                aws_api_call_action: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.AwsApiCallAction1", typing.Dict[builtins.str, typing.Any]]] = None,
                dns_request_action: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.DnsRequestAction", typing.Dict[builtins.str, typing.Any]]] = None,
                kubernetes_api_call_action: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.KubernetesApiCallAction", typing.Dict[builtins.str, typing.Any]]] = None,
                network_connection_action: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.NetworkConnectionAction", typing.Dict[builtins.str, typing.Any]]] = None,
                port_probe_action: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.PortProbeAction", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for Action.

                :param action_type: (experimental) actionType property. Specify an array of string values to match this event if the actual value of actionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param aws_api_call_action: (experimental) awsApiCallAction property. Specify an array of string values to match this event if the actual value of awsApiCallAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param dns_request_action: (experimental) dnsRequestAction property. Specify an array of string values to match this event if the actual value of dnsRequestAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param kubernetes_api_call_action: (experimental) kubernetesApiCallAction property. Specify an array of string values to match this event if the actual value of kubernetesApiCallAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_connection_action: (experimental) networkConnectionAction property. Specify an array of string values to match this event if the actual value of networkConnectionAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param port_probe_action: (experimental) portProbeAction property. Specify an array of string values to match this event if the actual value of portProbeAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    action = guardduty_events.DetectorEvents.GuardDutyFinding.Action(
                        action_type=["actionType"],
                        aws_api_call_action=guardduty_events.DetectorEvents.GuardDutyFinding.AwsApiCallAction1(
                            affected_resources=guardduty_events.DetectorEvents.GuardDutyFinding.AffectedResources1(
                                aws_cloud_trail_trail=["awsCloudTrailTrail"],
                                aws_ec2_instance=["awsEc2Instance"],
                                aws_s3_bucket=["awsS3Bucket"]
                            ),
                            api=["api"],
                            caller_type=["callerType"],
                            error_code=["errorCode"],
                            remote_account_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteAccountDetails(
                                account_id=["accountId"],
                                affiliated=["affiliated"]
                            ),
                            remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails1(
                                city=guardduty_events.DetectorEvents.GuardDutyFinding.City1(
                                    city_name=["cityName"]
                                ),
                                country=guardduty_events.DetectorEvents.GuardDutyFinding.Country1(
                                    country_name=["countryName"]
                                ),
                                geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                    lat=["lat"],
                                    lon=["lon"]
                                ),
                                ip_address_v4=["ipAddressV4"],
                                organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization1(
                                    asn=["asn"],
                                    asn_org=["asnOrg"],
                                    isp=["isp"],
                                    org=["org"]
                                )
                            ),
                            service_name=["serviceName"]
                        ),
                        dns_request_action=guardduty_events.DetectorEvents.GuardDutyFinding.DnsRequestAction(
                            blocked=["blocked"],
                            domain=["domain"],
                            protocol=["protocol"]
                        ),
                        kubernetes_api_call_action=guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesApiCallAction(
                            parameters=["parameters"],
                            remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails2(
                                city=guardduty_events.DetectorEvents.GuardDutyFinding.City2(
                                    city_name=["cityName"]
                                ),
                                country=guardduty_events.DetectorEvents.GuardDutyFinding.Country2(
                                    country_name=["countryName"]
                                ),
                                geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                    lat=["lat"],
                                    lon=["lon"]
                                ),
                                ip_address_v4=["ipAddressV4"],
                                organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization2(
                                    asn=["asn"],
                                    asn_org=["asnOrg"],
                                    isp=["isp"],
                                    org=["org"]
                                )
                            ),
                            request_uri=["requestUri"],
                            source_iPs=["sourceIPs"],
                            status_code=["statusCode"],
                            user_agent=["userAgent"],
                            verb=["verb"]
                        ),
                        network_connection_action=guardduty_events.DetectorEvents.GuardDutyFinding.NetworkConnectionAction(
                            blocked=["blocked"],
                            connection_direction=["connectionDirection"],
                            local_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalIpDetails(
                                ip_address_v4=["ipAddressV4"]
                            ),
                            local_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalPortDetails(
                                port=["port"],
                                port_name=["portName"]
                            ),
                            protocol=["protocol"],
                            remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails3(
                                city=guardduty_events.DetectorEvents.GuardDutyFinding.City3(
                                    city_name=["cityName"]
                                ),
                                country=guardduty_events.DetectorEvents.GuardDutyFinding.Country3(
                                    country_name=["countryName"]
                                ),
                                geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                    lat=["lat"],
                                    lon=["lon"]
                                ),
                                ip_address_v4=["ipAddressV4"],
                                organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization3(
                                    asn=["asn"],
                                    asn_org=["asnOrg"],
                                    isp=["isp"],
                                    org=["org"]
                                )
                            ),
                            remote_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemotePortDetails(
                                port=["port"],
                                port_name=["portName"]
                            )
                        ),
                        port_probe_action=guardduty_events.DetectorEvents.GuardDutyFinding.PortProbeAction(
                            blocked=["blocked"],
                            port_probe_details=[guardduty_events.DetectorEvents.GuardDutyFinding.PortProbeActionItem(
                                local_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalIpDetails1(
                                    ip_address_v4=["ipAddressV4"]
                                ),
                                local_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalPortDetails1(
                                    port=["port"],
                                    port_name=["portName"]
                                ),
                                remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails4(
                                    city=guardduty_events.DetectorEvents.GuardDutyFinding.City4(
                                        city_name=["cityName"]
                                    ),
                                    country=guardduty_events.DetectorEvents.GuardDutyFinding.Country4(
                                        country_name=["countryName"]
                                    ),
                                    geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation1(
                                        lat=["lat"],
                                        lon=["lon"]
                                    ),
                                    ip_address_v4=["ipAddressV4"],
                                    organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization4(
                                        asn=["asn"],
                                        asn_org=["asnOrg"],
                                        isp=["isp"],
                                        org=["org"]
                                    )
                                )
                            )]
                        )
                    )
                '''
                if isinstance(aws_api_call_action, dict):
                    aws_api_call_action = DetectorEvents.GuardDutyFinding.AwsApiCallAction1(**aws_api_call_action)
                if isinstance(dns_request_action, dict):
                    dns_request_action = DetectorEvents.GuardDutyFinding.DnsRequestAction(**dns_request_action)
                if isinstance(kubernetes_api_call_action, dict):
                    kubernetes_api_call_action = DetectorEvents.GuardDutyFinding.KubernetesApiCallAction(**kubernetes_api_call_action)
                if isinstance(network_connection_action, dict):
                    network_connection_action = DetectorEvents.GuardDutyFinding.NetworkConnectionAction(**network_connection_action)
                if isinstance(port_probe_action, dict):
                    port_probe_action = DetectorEvents.GuardDutyFinding.PortProbeAction(**port_probe_action)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3351eebe7a99b26e5472a7a96d38813de51f5a74c072263c2ecfd1af70f983e5)
                    check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
                    check_type(argname="argument aws_api_call_action", value=aws_api_call_action, expected_type=type_hints["aws_api_call_action"])
                    check_type(argname="argument dns_request_action", value=dns_request_action, expected_type=type_hints["dns_request_action"])
                    check_type(argname="argument kubernetes_api_call_action", value=kubernetes_api_call_action, expected_type=type_hints["kubernetes_api_call_action"])
                    check_type(argname="argument network_connection_action", value=network_connection_action, expected_type=type_hints["network_connection_action"])
                    check_type(argname="argument port_probe_action", value=port_probe_action, expected_type=type_hints["port_probe_action"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action_type is not None:
                    self._values["action_type"] = action_type
                if aws_api_call_action is not None:
                    self._values["aws_api_call_action"] = aws_api_call_action
                if dns_request_action is not None:
                    self._values["dns_request_action"] = dns_request_action
                if kubernetes_api_call_action is not None:
                    self._values["kubernetes_api_call_action"] = kubernetes_api_call_action
                if network_connection_action is not None:
                    self._values["network_connection_action"] = network_connection_action
                if port_probe_action is not None:
                    self._values["port_probe_action"] = port_probe_action

            @builtins.property
            def action_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) actionType property.

                Specify an array of string values to match this event if the actual value of actionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def aws_api_call_action(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.AwsApiCallAction1"]:
                '''(experimental) awsApiCallAction property.

                Specify an array of string values to match this event if the actual value of awsApiCallAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_api_call_action")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.AwsApiCallAction1"], result)

            @builtins.property
            def dns_request_action(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.DnsRequestAction"]:
                '''(experimental) dnsRequestAction property.

                Specify an array of string values to match this event if the actual value of dnsRequestAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("dns_request_action")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.DnsRequestAction"], result)

            @builtins.property
            def kubernetes_api_call_action(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.KubernetesApiCallAction"]:
                '''(experimental) kubernetesApiCallAction property.

                Specify an array of string values to match this event if the actual value of kubernetesApiCallAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("kubernetes_api_call_action")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.KubernetesApiCallAction"], result)

            @builtins.property
            def network_connection_action(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.NetworkConnectionAction"]:
                '''(experimental) networkConnectionAction property.

                Specify an array of string values to match this event if the actual value of networkConnectionAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_connection_action")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.NetworkConnectionAction"], result)

            @builtins.property
            def port_probe_action(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.PortProbeAction"]:
                '''(experimental) portProbeAction property.

                Specify an array of string values to match this event if the actual value of portProbeAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("port_probe_action")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.PortProbeAction"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Action(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.AdditionalInfo",
            jsii_struct_bases=[],
            name_mapping={
                "additional_scanned_ports": "additionalScannedPorts",
                "anomalies": "anomalies",
                "api_calls": "apiCalls",
                "domain": "domain",
                "in_bytes": "inBytes",
                "local_port": "localPort",
                "new_policy": "newPolicy",
                "old_policy": "oldPolicy",
                "out_bytes": "outBytes",
                "ports_scanned_sample": "portsScannedSample",
                "profiled_behavior": "profiledBehavior",
                "recent_credentials": "recentCredentials",
                "sample": "sample",
                "scanned_port": "scannedPort",
                "threat_list_name": "threatListName",
                "threat_name": "threatName",
                "type": "type",
                "unusual": "unusual",
                "unusual_behavior": "unusualBehavior",
                "unusual_protocol": "unusualProtocol",
                "user_agent": "userAgent",
                "value": "value",
            },
        )
        class AdditionalInfo:
            def __init__(
                self,
                *,
                additional_scanned_ports: typing.Optional[typing.Sequence[typing.Any]] = None,
                anomalies: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Anomalies", typing.Dict[builtins.str, typing.Any]]] = None,
                api_calls: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.AdditionalInfoItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                domain: typing.Optional[typing.Sequence[builtins.str]] = None,
                in_bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                local_port: typing.Optional[typing.Sequence[builtins.str]] = None,
                new_policy: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.NewPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
                old_policy: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.OldPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
                out_bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
                ports_scanned_sample: typing.Optional[typing.Sequence[jsii.Number]] = None,
                profiled_behavior: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.ProfiledBehavior", typing.Dict[builtins.str, typing.Any]]] = None,
                recent_credentials: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.AdditionalInfoItem1", typing.Dict[builtins.str, typing.Any]]]] = None,
                sample: typing.Optional[typing.Sequence[builtins.str]] = None,
                scanned_port: typing.Optional[typing.Sequence[builtins.str]] = None,
                threat_list_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                threat_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual: typing.Any = None,
                unusual_behavior: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.UnusualBehavior", typing.Dict[builtins.str, typing.Any]]] = None,
                unusual_protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.UserAgent", typing.Dict[builtins.str, typing.Any]]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AdditionalInfo.

                :param additional_scanned_ports: (experimental) additionalScannedPorts property. Specify an array of string values to match this event if the actual value of additionalScannedPorts is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param anomalies: (experimental) anomalies property. Specify an array of string values to match this event if the actual value of anomalies is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param api_calls: (experimental) apiCalls property. Specify an array of string values to match this event if the actual value of apiCalls is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain: (experimental) domain property. Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param in_bytes: (experimental) inBytes property. Specify an array of string values to match this event if the actual value of inBytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_port: (experimental) localPort property. Specify an array of string values to match this event if the actual value of localPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param new_policy: (experimental) newPolicy property. Specify an array of string values to match this event if the actual value of newPolicy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param old_policy: (experimental) oldPolicy property. Specify an array of string values to match this event if the actual value of oldPolicy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param out_bytes: (experimental) outBytes property. Specify an array of string values to match this event if the actual value of outBytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ports_scanned_sample: (experimental) portsScannedSample property. Specify an array of string values to match this event if the actual value of portsScannedSample is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param profiled_behavior: (experimental) profiledBehavior property. Specify an array of string values to match this event if the actual value of profiledBehavior is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param recent_credentials: (experimental) recentCredentials property. Specify an array of string values to match this event if the actual value of recentCredentials is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param sample: (experimental) sample property. Specify an array of string values to match this event if the actual value of sample is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param scanned_port: (experimental) scannedPort property. Specify an array of string values to match this event if the actual value of scannedPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param threat_list_name: (experimental) threatListName property. Specify an array of string values to match this event if the actual value of threatListName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param threat_name: (experimental) threatName property. Specify an array of string values to match this event if the actual value of threatName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual: (experimental) unusual property. Specify an array of string values to match this event if the actual value of unusual is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_behavior: (experimental) unusualBehavior property. Specify an array of string values to match this event if the actual value of unusualBehavior is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_protocol: (experimental) unusualProtocol property. Specify an array of string values to match this event if the actual value of unusualProtocol is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    # additional_scanned_ports: Any
                    # unusual: Any
                    
                    additional_info = guardduty_events.DetectorEvents.GuardDutyFinding.AdditionalInfo(
                        additional_scanned_ports=[additional_scanned_ports],
                        anomalies=guardduty_events.DetectorEvents.GuardDutyFinding.Anomalies(
                            anomalous_ap_is=["anomalousApIs"]
                        ),
                        api_calls=[guardduty_events.DetectorEvents.GuardDutyFinding.AdditionalInfoItem(
                            count=["count"],
                            first_seen=["firstSeen"],
                            last_seen=["lastSeen"],
                            name=["name"]
                        )],
                        domain=["domain"],
                        in_bytes=["inBytes"],
                        local_port=["localPort"],
                        new_policy=guardduty_events.DetectorEvents.GuardDutyFinding.NewPolicy(
                            allow_users_to_change_password=["allowUsersToChangePassword"],
                            hard_expiry=["hardExpiry"],
                            max_password_age=["maxPasswordAge"],
                            minimum_password_length=["minimumPasswordLength"],
                            password_reuse_prevention=["passwordReusePrevention"],
                            require_lowercase_characters=["requireLowercaseCharacters"],
                            require_numbers=["requireNumbers"],
                            require_symbols=["requireSymbols"],
                            require_uppercase_characters=["requireUppercaseCharacters"]
                        ),
                        old_policy=guardduty_events.DetectorEvents.GuardDutyFinding.OldPolicy(
                            allow_users_to_change_password=["allowUsersToChangePassword"],
                            hard_expiry=["hardExpiry"],
                            max_password_age=["maxPasswordAge"],
                            minimum_password_length=["minimumPasswordLength"],
                            password_reuse_prevention=["passwordReusePrevention"],
                            require_lowercase_characters=["requireLowercaseCharacters"],
                            require_numbers=["requireNumbers"],
                            require_symbols=["requireSymbols"],
                            require_uppercase_characters=["requireUppercaseCharacters"]
                        ),
                        out_bytes=["outBytes"],
                        ports_scanned_sample=[123],
                        profiled_behavior=guardduty_events.DetectorEvents.GuardDutyFinding.ProfiledBehavior(
                            frequent_profiled_ap_is_account_profiling=["frequentProfiledApIsAccountProfiling"],
                            frequent_profiled_ap_is_user_identity_profiling=["frequentProfiledApIsUserIdentityProfiling"],
                            frequent_profiled_as_ns_account_profiling=["frequentProfiledAsNsAccountProfiling"],
                            frequent_profiled_as_ns_bucket_profiling=["frequentProfiledAsNsBucketProfiling"],
                            frequent_profiled_as_ns_user_identity_profiling=["frequentProfiledAsNsUserIdentityProfiling"],
                            frequent_profiled_buckets_account_profiling=["frequentProfiledBucketsAccountProfiling"],
                            frequent_profiled_buckets_user_identity_profiling=["frequentProfiledBucketsUserIdentityProfiling"],
                            frequent_profiled_user_agents_account_profiling=["frequentProfiledUserAgentsAccountProfiling"],
                            frequent_profiled_user_agents_user_identity_profiling=["frequentProfiledUserAgentsUserIdentityProfiling"],
                            frequent_profiled_user_names_account_profiling=["frequentProfiledUserNamesAccountProfiling"],
                            frequent_profiled_user_names_bucket_profiling=["frequentProfiledUserNamesBucketProfiling"],
                            frequent_profiled_user_types_account_profiling=["frequentProfiledUserTypesAccountProfiling"],
                            infrequent_profiled_ap_is_account_profiling=["infrequentProfiledApIsAccountProfiling"],
                            infrequent_profiled_ap_is_user_identity_profiling=["infrequentProfiledApIsUserIdentityProfiling"],
                            infrequent_profiled_as_ns_account_profiling=["infrequentProfiledAsNsAccountProfiling"],
                            infrequent_profiled_as_ns_bucket_profiling=["infrequentProfiledAsNsBucketProfiling"],
                            infrequent_profiled_as_ns_user_identity_profiling=["infrequentProfiledAsNsUserIdentityProfiling"],
                            infrequent_profiled_buckets_account_profiling=["infrequentProfiledBucketsAccountProfiling"],
                            infrequent_profiled_buckets_user_identity_profiling=["infrequentProfiledBucketsUserIdentityProfiling"],
                            infrequent_profiled_user_agents_account_profiling=["infrequentProfiledUserAgentsAccountProfiling"],
                            infrequent_profiled_user_agents_user_identity_profiling=["infrequentProfiledUserAgentsUserIdentityProfiling"],
                            infrequent_profiled_user_names_account_profiling=["infrequentProfiledUserNamesAccountProfiling"],
                            infrequent_profiled_user_names_bucket_profiling=["infrequentProfiledUserNamesBucketProfiling"],
                            infrequent_profiled_user_types_account_profiling=["infrequentProfiledUserTypesAccountProfiling"],
                            number_of_historical_daily_avg_ap_is_bucket_profiling=["numberOfHistoricalDailyAvgApIsBucketProfiling"],
                            number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling=["numberOfHistoricalDailyAvgApIsBucketUserIdentityProfiling"],
                            number_of_historical_daily_avg_ap_is_user_identity_profiling=["numberOfHistoricalDailyAvgApIsUserIdentityProfiling"],
                            number_of_historical_daily_max_ap_is_bucket_profiling=["numberOfHistoricalDailyMaxApIsBucketProfiling"],
                            number_of_historical_daily_max_ap_is_bucket_user_identity_profiling=["numberOfHistoricalDailyMaxApIsBucketUserIdentityProfiling"],
                            number_of_historical_daily_max_ap_is_user_identity_profiling=["numberOfHistoricalDailyMaxApIsUserIdentityProfiling"],
                            rare_profiled_ap_is_account_profiling=["rareProfiledApIsAccountProfiling"],
                            rare_profiled_ap_is_user_identity_profiling=["rareProfiledApIsUserIdentityProfiling"],
                            rare_profiled_as_ns_account_profiling=["rareProfiledAsNsAccountProfiling"],
                            rare_profiled_as_ns_bucket_profiling=["rareProfiledAsNsBucketProfiling"],
                            rare_profiled_as_ns_user_identity_profiling=["rareProfiledAsNsUserIdentityProfiling"],
                            rare_profiled_buckets_account_profiling=["rareProfiledBucketsAccountProfiling"],
                            rare_profiled_buckets_user_identity_profiling=["rareProfiledBucketsUserIdentityProfiling"],
                            rare_profiled_user_agents_account_profiling=["rareProfiledUserAgentsAccountProfiling"],
                            rare_profiled_user_agents_user_identity_profiling=["rareProfiledUserAgentsUserIdentityProfiling"],
                            rare_profiled_user_names_account_profiling=["rareProfiledUserNamesAccountProfiling"],
                            rare_profiled_user_names_bucket_profiling=["rareProfiledUserNamesBucketProfiling"],
                            rare_profiled_user_types_account_profiling=["rareProfiledUserTypesAccountProfiling"]
                        ),
                        recent_credentials=[guardduty_events.DetectorEvents.GuardDutyFinding.AdditionalInfoItem1(
                            access_key_id=["accessKeyId"],
                            ip_address_v4=["ipAddressV4"],
                            principal_id=["principalId"]
                        )],
                        sample=["sample"],
                        scanned_port=["scannedPort"],
                        threat_list_name=["threatListName"],
                        threat_name=["threatName"],
                        type=["type"],
                        unusual=unusual,
                        unusual_behavior=guardduty_events.DetectorEvents.GuardDutyFinding.UnusualBehavior(
                            is_unusual_user_identity=["isUnusualUserIdentity"],
                            number_of_past24_hours_ap_is_bucket_profiling=["numberOfPast24HoursApIsBucketProfiling"],
                            number_of_past24_hours_ap_is_bucket_user_identity_profiling=["numberOfPast24HoursApIsBucketUserIdentityProfiling"],
                            number_of_past24_hours_ap_is_user_identity_profiling=["numberOfPast24HoursApIsUserIdentityProfiling"],
                            unusual_ap_is_account_profiling=["unusualApIsAccountProfiling"],
                            unusual_ap_is_user_identity_profiling=["unusualApIsUserIdentityProfiling"],
                            unusual_as_ns_account_profiling=["unusualAsNsAccountProfiling"],
                            unusual_as_ns_bucket_profiling=["unusualAsNsBucketProfiling"],
                            unusual_as_ns_user_identity_profiling=["unusualAsNsUserIdentityProfiling"],
                            unusual_buckets_account_profiling=["unusualBucketsAccountProfiling"],
                            unusual_buckets_user_identity_profiling=["unusualBucketsUserIdentityProfiling"],
                            unusual_user_agents_account_profiling=["unusualUserAgentsAccountProfiling"],
                            unusual_user_agents_user_identity_profiling=["unusualUserAgentsUserIdentityProfiling"],
                            unusual_user_names_account_profiling=["unusualUserNamesAccountProfiling"],
                            unusual_user_names_bucket_profiling=["unusualUserNamesBucketProfiling"],
                            unusual_user_types_account_profiling=["unusualUserTypesAccountProfiling"]
                        ),
                        unusual_protocol=["unusualProtocol"],
                        user_agent=guardduty_events.DetectorEvents.GuardDutyFinding.UserAgent(
                            full_user_agent=["fullUserAgent"],
                            user_agent_category=["userAgentCategory"]
                        ),
                        value=["value"]
                    )
                '''
                if isinstance(anomalies, dict):
                    anomalies = DetectorEvents.GuardDutyFinding.Anomalies(**anomalies)
                if isinstance(new_policy, dict):
                    new_policy = DetectorEvents.GuardDutyFinding.NewPolicy(**new_policy)
                if isinstance(old_policy, dict):
                    old_policy = DetectorEvents.GuardDutyFinding.OldPolicy(**old_policy)
                if isinstance(profiled_behavior, dict):
                    profiled_behavior = DetectorEvents.GuardDutyFinding.ProfiledBehavior(**profiled_behavior)
                if isinstance(unusual_behavior, dict):
                    unusual_behavior = DetectorEvents.GuardDutyFinding.UnusualBehavior(**unusual_behavior)
                if isinstance(user_agent, dict):
                    user_agent = DetectorEvents.GuardDutyFinding.UserAgent(**user_agent)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__83891d8a1ae4766f914d9b450ccb3460200d6beaf98785d675a1509984c62215)
                    check_type(argname="argument additional_scanned_ports", value=additional_scanned_ports, expected_type=type_hints["additional_scanned_ports"])
                    check_type(argname="argument anomalies", value=anomalies, expected_type=type_hints["anomalies"])
                    check_type(argname="argument api_calls", value=api_calls, expected_type=type_hints["api_calls"])
                    check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                    check_type(argname="argument in_bytes", value=in_bytes, expected_type=type_hints["in_bytes"])
                    check_type(argname="argument local_port", value=local_port, expected_type=type_hints["local_port"])
                    check_type(argname="argument new_policy", value=new_policy, expected_type=type_hints["new_policy"])
                    check_type(argname="argument old_policy", value=old_policy, expected_type=type_hints["old_policy"])
                    check_type(argname="argument out_bytes", value=out_bytes, expected_type=type_hints["out_bytes"])
                    check_type(argname="argument ports_scanned_sample", value=ports_scanned_sample, expected_type=type_hints["ports_scanned_sample"])
                    check_type(argname="argument profiled_behavior", value=profiled_behavior, expected_type=type_hints["profiled_behavior"])
                    check_type(argname="argument recent_credentials", value=recent_credentials, expected_type=type_hints["recent_credentials"])
                    check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
                    check_type(argname="argument scanned_port", value=scanned_port, expected_type=type_hints["scanned_port"])
                    check_type(argname="argument threat_list_name", value=threat_list_name, expected_type=type_hints["threat_list_name"])
                    check_type(argname="argument threat_name", value=threat_name, expected_type=type_hints["threat_name"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                    check_type(argname="argument unusual", value=unusual, expected_type=type_hints["unusual"])
                    check_type(argname="argument unusual_behavior", value=unusual_behavior, expected_type=type_hints["unusual_behavior"])
                    check_type(argname="argument unusual_protocol", value=unusual_protocol, expected_type=type_hints["unusual_protocol"])
                    check_type(argname="argument user_agent", value=user_agent, expected_type=type_hints["user_agent"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if additional_scanned_ports is not None:
                    self._values["additional_scanned_ports"] = additional_scanned_ports
                if anomalies is not None:
                    self._values["anomalies"] = anomalies
                if api_calls is not None:
                    self._values["api_calls"] = api_calls
                if domain is not None:
                    self._values["domain"] = domain
                if in_bytes is not None:
                    self._values["in_bytes"] = in_bytes
                if local_port is not None:
                    self._values["local_port"] = local_port
                if new_policy is not None:
                    self._values["new_policy"] = new_policy
                if old_policy is not None:
                    self._values["old_policy"] = old_policy
                if out_bytes is not None:
                    self._values["out_bytes"] = out_bytes
                if ports_scanned_sample is not None:
                    self._values["ports_scanned_sample"] = ports_scanned_sample
                if profiled_behavior is not None:
                    self._values["profiled_behavior"] = profiled_behavior
                if recent_credentials is not None:
                    self._values["recent_credentials"] = recent_credentials
                if sample is not None:
                    self._values["sample"] = sample
                if scanned_port is not None:
                    self._values["scanned_port"] = scanned_port
                if threat_list_name is not None:
                    self._values["threat_list_name"] = threat_list_name
                if threat_name is not None:
                    self._values["threat_name"] = threat_name
                if type is not None:
                    self._values["type"] = type
                if unusual is not None:
                    self._values["unusual"] = unusual
                if unusual_behavior is not None:
                    self._values["unusual_behavior"] = unusual_behavior
                if unusual_protocol is not None:
                    self._values["unusual_protocol"] = unusual_protocol
                if user_agent is not None:
                    self._values["user_agent"] = user_agent
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def additional_scanned_ports(
                self,
            ) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) additionalScannedPorts property.

                Specify an array of string values to match this event if the actual value of additionalScannedPorts is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("additional_scanned_ports")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            @builtins.property
            def anomalies(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Anomalies"]:
                '''(experimental) anomalies property.

                Specify an array of string values to match this event if the actual value of anomalies is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("anomalies")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Anomalies"], result)

            @builtins.property
            def api_calls(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.AdditionalInfoItem"]]:
                '''(experimental) apiCalls property.

                Specify an array of string values to match this event if the actual value of apiCalls is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("api_calls")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.AdditionalInfoItem"]], result)

            @builtins.property
            def domain(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domain property.

                Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("domain")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def in_bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) inBytes property.

                Specify an array of string values to match this event if the actual value of inBytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("in_bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def local_port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) localPort property.

                Specify an array of string values to match this event if the actual value of localPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def new_policy(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.NewPolicy"]:
                '''(experimental) newPolicy property.

                Specify an array of string values to match this event if the actual value of newPolicy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("new_policy")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.NewPolicy"], result)

            @builtins.property
            def old_policy(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.OldPolicy"]:
                '''(experimental) oldPolicy property.

                Specify an array of string values to match this event if the actual value of oldPolicy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("old_policy")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.OldPolicy"], result)

            @builtins.property
            def out_bytes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) outBytes property.

                Specify an array of string values to match this event if the actual value of outBytes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("out_bytes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ports_scanned_sample(self) -> typing.Optional[typing.List[jsii.Number]]:
                '''(experimental) portsScannedSample property.

                Specify an array of string values to match this event if the actual value of portsScannedSample is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ports_scanned_sample")
                return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

            @builtins.property
            def profiled_behavior(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.ProfiledBehavior"]:
                '''(experimental) profiledBehavior property.

                Specify an array of string values to match this event if the actual value of profiledBehavior is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("profiled_behavior")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.ProfiledBehavior"], result)

            @builtins.property
            def recent_credentials(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.AdditionalInfoItem1"]]:
                '''(experimental) recentCredentials property.

                Specify an array of string values to match this event if the actual value of recentCredentials is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("recent_credentials")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.AdditionalInfoItem1"]], result)

            @builtins.property
            def sample(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sample property.

                Specify an array of string values to match this event if the actual value of sample is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("sample")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def scanned_port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) scannedPort property.

                Specify an array of string values to match this event if the actual value of scannedPort is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("scanned_port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def threat_list_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) threatListName property.

                Specify an array of string values to match this event if the actual value of threatListName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threat_list_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def threat_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) threatName property.

                Specify an array of string values to match this event if the actual value of threatName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threat_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual(self) -> typing.Any:
                '''(experimental) unusual property.

                Specify an array of string values to match this event if the actual value of unusual is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual")
                return typing.cast(typing.Any, result)

            @builtins.property
            def unusual_behavior(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.UnusualBehavior"]:
                '''(experimental) unusualBehavior property.

                Specify an array of string values to match this event if the actual value of unusualBehavior is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_behavior")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.UnusualBehavior"], result)

            @builtins.property
            def unusual_protocol(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualProtocol property.

                Specify an array of string values to match this event if the actual value of unusualProtocol is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_protocol")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_agent(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.UserAgent"]:
                '''(experimental) userAgent property.

                Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_agent")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.UserAgent"], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AdditionalInfo(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.AdditionalInfoItem",
            jsii_struct_bases=[],
            name_mapping={
                "count": "count",
                "first_seen": "firstSeen",
                "last_seen": "lastSeen",
                "name": "name",
            },
        )
        class AdditionalInfoItem:
            def __init__(
                self,
                *,
                count: typing.Optional[typing.Sequence[builtins.str]] = None,
                first_seen: typing.Optional[typing.Sequence[builtins.str]] = None,
                last_seen: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AdditionalInfoItem.

                :param count: (experimental) count property. Specify an array of string values to match this event if the actual value of count is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param first_seen: (experimental) firstSeen property. Specify an array of string values to match this event if the actual value of firstSeen is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param last_seen: (experimental) lastSeen property. Specify an array of string values to match this event if the actual value of lastSeen is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    additional_info_item = guardduty_events.DetectorEvents.GuardDutyFinding.AdditionalInfoItem(
                        count=["count"],
                        first_seen=["firstSeen"],
                        last_seen=["lastSeen"],
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0fc7f7c34d3564f3838357e7b6b92b9841158118a0ab3a941a4189e392d2bb5e)
                    check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                    check_type(argname="argument first_seen", value=first_seen, expected_type=type_hints["first_seen"])
                    check_type(argname="argument last_seen", value=last_seen, expected_type=type_hints["last_seen"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if count is not None:
                    self._values["count"] = count
                if first_seen is not None:
                    self._values["first_seen"] = first_seen
                if last_seen is not None:
                    self._values["last_seen"] = last_seen
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) count property.

                Specify an array of string values to match this event if the actual value of count is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def first_seen(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) firstSeen property.

                Specify an array of string values to match this event if the actual value of firstSeen is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("first_seen")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def last_seen(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lastSeen property.

                Specify an array of string values to match this event if the actual value of lastSeen is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("last_seen")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AdditionalInfoItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.AdditionalInfoItem1",
            jsii_struct_bases=[],
            name_mapping={
                "access_key_id": "accessKeyId",
                "ip_address_v4": "ipAddressV4",
                "principal_id": "principalId",
            },
        )
        class AdditionalInfoItem1:
            def __init__(
                self,
                *,
                access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AdditionalInfoItem_1.

                :param access_key_id: (experimental) accessKeyId property. Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ip_address_v4: (experimental) ipAddressV4 property. Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    additional_info_item1 = guardduty_events.DetectorEvents.GuardDutyFinding.AdditionalInfoItem1(
                        access_key_id=["accessKeyId"],
                        ip_address_v4=["ipAddressV4"],
                        principal_id=["principalId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0a3444e5abb7243a4fb235333e278865881a6fa69a7831cc691501ccd3db7894)
                    check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
                    check_type(argname="argument ip_address_v4", value=ip_address_v4, expected_type=type_hints["ip_address_v4"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if access_key_id is not None:
                    self._values["access_key_id"] = access_key_id
                if ip_address_v4 is not None:
                    self._values["ip_address_v4"] = ip_address_v4
                if principal_id is not None:
                    self._values["principal_id"] = principal_id

            @builtins.property
            def access_key_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accessKeyId property.

                Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("access_key_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ip_address_v4(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipAddressV4 property.

                Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ip_address_v4")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def principal_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) principalId property.

                Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("principal_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AdditionalInfoItem1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.AffectedResources1",
            jsii_struct_bases=[],
            name_mapping={
                "aws_cloud_trail_trail": "awsCloudTrailTrail",
                "aws_ec2_instance": "awsEc2Instance",
                "aws_s3_bucket": "awsS3Bucket",
            },
        )
        class AffectedResources1:
            def __init__(
                self,
                *,
                aws_cloud_trail_trail: typing.Optional[typing.Sequence[builtins.str]] = None,
                aws_ec2_instance: typing.Optional[typing.Sequence[builtins.str]] = None,
                aws_s3_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AffectedResources_1.

                :param aws_cloud_trail_trail: (experimental) AWS-CloudTrail-Trail property. Specify an array of string values to match this event if the actual value of AWS-CloudTrail-Trail is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param aws_ec2_instance: (experimental) AWS-EC2-Instance property. Specify an array of string values to match this event if the actual value of AWS-EC2-Instance is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param aws_s3_bucket: (experimental) AWS-S3-Bucket property. Specify an array of string values to match this event if the actual value of AWS-S3-Bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    affected_resources1 = guardduty_events.DetectorEvents.GuardDutyFinding.AffectedResources1(
                        aws_cloud_trail_trail=["awsCloudTrailTrail"],
                        aws_ec2_instance=["awsEc2Instance"],
                        aws_s3_bucket=["awsS3Bucket"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3475e6a752314ad9d7d41dbd665e3b27acb284be2ab5ff8a03b1fea154ba3534)
                    check_type(argname="argument aws_cloud_trail_trail", value=aws_cloud_trail_trail, expected_type=type_hints["aws_cloud_trail_trail"])
                    check_type(argname="argument aws_ec2_instance", value=aws_ec2_instance, expected_type=type_hints["aws_ec2_instance"])
                    check_type(argname="argument aws_s3_bucket", value=aws_s3_bucket, expected_type=type_hints["aws_s3_bucket"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if aws_cloud_trail_trail is not None:
                    self._values["aws_cloud_trail_trail"] = aws_cloud_trail_trail
                if aws_ec2_instance is not None:
                    self._values["aws_ec2_instance"] = aws_ec2_instance
                if aws_s3_bucket is not None:
                    self._values["aws_s3_bucket"] = aws_s3_bucket

            @builtins.property
            def aws_cloud_trail_trail(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AWS-CloudTrail-Trail property.

                Specify an array of string values to match this event if the actual value of AWS-CloudTrail-Trail is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_cloud_trail_trail")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def aws_ec2_instance(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AWS-EC2-Instance property.

                Specify an array of string values to match this event if the actual value of AWS-EC2-Instance is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_ec2_instance")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def aws_s3_bucket(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) AWS-S3-Bucket property.

                Specify an array of string values to match this event if the actual value of AWS-S3-Bucket is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_s3_bucket")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AffectedResources1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Anomalies",
            jsii_struct_bases=[],
            name_mapping={"anomalous_ap_is": "anomalousApIs"},
        )
        class Anomalies:
            def __init__(
                self,
                *,
                anomalous_ap_is: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Anomalies.

                :param anomalous_ap_is: (experimental) anomalousAPIs property. Specify an array of string values to match this event if the actual value of anomalousAPIs is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    anomalies = guardduty_events.DetectorEvents.GuardDutyFinding.Anomalies(
                        anomalous_ap_is=["anomalousApIs"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7dd37caf22cf4f8d9ad621aa1607bab78fe28120e96d5112e396dcdf661b3bc7)
                    check_type(argname="argument anomalous_ap_is", value=anomalous_ap_is, expected_type=type_hints["anomalous_ap_is"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if anomalous_ap_is is not None:
                    self._values["anomalous_ap_is"] = anomalous_ap_is

            @builtins.property
            def anomalous_ap_is(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) anomalousAPIs property.

                Specify an array of string values to match this event if the actual value of anomalousAPIs is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("anomalous_ap_is")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Anomalies(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.AwsApiCallAction",
            jsii_struct_bases=[],
            name_mapping={
                "affected_resources": "affectedResources",
                "api": "api",
                "caller_type": "callerType",
                "error_code": "errorCode",
                "remote_ip_details": "remoteIpDetails",
                "service_name": "serviceName",
            },
        )
        class AwsApiCallAction:
            def __init__(
                self,
                *,
                affected_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
                api: typing.Optional[typing.Sequence[builtins.str]] = None,
                caller_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                remote_ip_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.RemoteIpDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                service_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AwsApiCallAction.

                :param affected_resources: (experimental) affectedResources property. Specify an array of string values to match this event if the actual value of affectedResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param api: (experimental) api property. Specify an array of string values to match this event if the actual value of api is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param caller_type: (experimental) callerType property. Specify an array of string values to match this event if the actual value of callerType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_ip_details: (experimental) remoteIpDetails property. Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param service_name: (experimental) serviceName property. Specify an array of string values to match this event if the actual value of serviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    aws_api_call_action = guardduty_events.DetectorEvents.GuardDutyFinding.AwsApiCallAction(
                        affected_resources=["affectedResources"],
                        api=["api"],
                        caller_type=["callerType"],
                        error_code=["errorCode"],
                        remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails(
                            city=guardduty_events.DetectorEvents.GuardDutyFinding.City(
                                city_name=["cityName"]
                            ),
                            country=guardduty_events.DetectorEvents.GuardDutyFinding.Country(
                                country_name=["countryName"]
                            ),
                            geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                lat=["lat"],
                                lon=["lon"]
                            ),
                            ip_address_v4=["ipAddressV4"],
                            organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization(
                                asn=["asn"],
                                asn_org=["asnOrg"],
                                isp=["isp"],
                                org=["org"]
                            )
                        ),
                        service_name=["serviceName"]
                    )
                '''
                if isinstance(remote_ip_details, dict):
                    remote_ip_details = DetectorEvents.GuardDutyFinding.RemoteIpDetails(**remote_ip_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3344c294298851525cefe304b9cd58006245abd6c242b431e2c81e54ea256dcc)
                    check_type(argname="argument affected_resources", value=affected_resources, expected_type=type_hints["affected_resources"])
                    check_type(argname="argument api", value=api, expected_type=type_hints["api"])
                    check_type(argname="argument caller_type", value=caller_type, expected_type=type_hints["caller_type"])
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument remote_ip_details", value=remote_ip_details, expected_type=type_hints["remote_ip_details"])
                    check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if affected_resources is not None:
                    self._values["affected_resources"] = affected_resources
                if api is not None:
                    self._values["api"] = api
                if caller_type is not None:
                    self._values["caller_type"] = caller_type
                if error_code is not None:
                    self._values["error_code"] = error_code
                if remote_ip_details is not None:
                    self._values["remote_ip_details"] = remote_ip_details
                if service_name is not None:
                    self._values["service_name"] = service_name

            @builtins.property
            def affected_resources(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) affectedResources property.

                Specify an array of string values to match this event if the actual value of affectedResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("affected_resources")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def api(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) api property.

                Specify an array of string values to match this event if the actual value of api is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("api")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def caller_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) callerType property.

                Specify an array of string values to match this event if the actual value of callerType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("caller_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorCode property.

                Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def remote_ip_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails"]:
                '''(experimental) remoteIpDetails property.

                Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_ip_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails"], result)

            @builtins.property
            def service_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) serviceName property.

                Specify an array of string values to match this event if the actual value of serviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("service_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AwsApiCallAction(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.AwsApiCallAction1",
            jsii_struct_bases=[],
            name_mapping={
                "affected_resources": "affectedResources",
                "api": "api",
                "caller_type": "callerType",
                "error_code": "errorCode",
                "remote_account_details": "remoteAccountDetails",
                "remote_ip_details": "remoteIpDetails",
                "service_name": "serviceName",
            },
        )
        class AwsApiCallAction1:
            def __init__(
                self,
                *,
                affected_resources: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.AffectedResources1", typing.Dict[builtins.str, typing.Any]]] = None,
                api: typing.Optional[typing.Sequence[builtins.str]] = None,
                caller_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                remote_account_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.RemoteAccountDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                remote_ip_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.RemoteIpDetails1", typing.Dict[builtins.str, typing.Any]]] = None,
                service_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for AwsApiCallAction_1.

                :param affected_resources: (experimental) affectedResources property. Specify an array of string values to match this event if the actual value of affectedResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param api: (experimental) api property. Specify an array of string values to match this event if the actual value of api is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param caller_type: (experimental) callerType property. Specify an array of string values to match this event if the actual value of callerType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param error_code: (experimental) errorCode property. Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_account_details: (experimental) remoteAccountDetails property. Specify an array of string values to match this event if the actual value of remoteAccountDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_ip_details: (experimental) remoteIpDetails property. Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param service_name: (experimental) serviceName property. Specify an array of string values to match this event if the actual value of serviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    aws_api_call_action1 = guardduty_events.DetectorEvents.GuardDutyFinding.AwsApiCallAction1(
                        affected_resources=guardduty_events.DetectorEvents.GuardDutyFinding.AffectedResources1(
                            aws_cloud_trail_trail=["awsCloudTrailTrail"],
                            aws_ec2_instance=["awsEc2Instance"],
                            aws_s3_bucket=["awsS3Bucket"]
                        ),
                        api=["api"],
                        caller_type=["callerType"],
                        error_code=["errorCode"],
                        remote_account_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteAccountDetails(
                            account_id=["accountId"],
                            affiliated=["affiliated"]
                        ),
                        remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails1(
                            city=guardduty_events.DetectorEvents.GuardDutyFinding.City1(
                                city_name=["cityName"]
                            ),
                            country=guardduty_events.DetectorEvents.GuardDutyFinding.Country1(
                                country_name=["countryName"]
                            ),
                            geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                lat=["lat"],
                                lon=["lon"]
                            ),
                            ip_address_v4=["ipAddressV4"],
                            organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization1(
                                asn=["asn"],
                                asn_org=["asnOrg"],
                                isp=["isp"],
                                org=["org"]
                            )
                        ),
                        service_name=["serviceName"]
                    )
                '''
                if isinstance(affected_resources, dict):
                    affected_resources = DetectorEvents.GuardDutyFinding.AffectedResources1(**affected_resources)
                if isinstance(remote_account_details, dict):
                    remote_account_details = DetectorEvents.GuardDutyFinding.RemoteAccountDetails(**remote_account_details)
                if isinstance(remote_ip_details, dict):
                    remote_ip_details = DetectorEvents.GuardDutyFinding.RemoteIpDetails1(**remote_ip_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__21ccfd632960f96e322c8c9ca3db124bcb6aa4927363971bfb3bb95722a15ace)
                    check_type(argname="argument affected_resources", value=affected_resources, expected_type=type_hints["affected_resources"])
                    check_type(argname="argument api", value=api, expected_type=type_hints["api"])
                    check_type(argname="argument caller_type", value=caller_type, expected_type=type_hints["caller_type"])
                    check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
                    check_type(argname="argument remote_account_details", value=remote_account_details, expected_type=type_hints["remote_account_details"])
                    check_type(argname="argument remote_ip_details", value=remote_ip_details, expected_type=type_hints["remote_ip_details"])
                    check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if affected_resources is not None:
                    self._values["affected_resources"] = affected_resources
                if api is not None:
                    self._values["api"] = api
                if caller_type is not None:
                    self._values["caller_type"] = caller_type
                if error_code is not None:
                    self._values["error_code"] = error_code
                if remote_account_details is not None:
                    self._values["remote_account_details"] = remote_account_details
                if remote_ip_details is not None:
                    self._values["remote_ip_details"] = remote_ip_details
                if service_name is not None:
                    self._values["service_name"] = service_name

            @builtins.property
            def affected_resources(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.AffectedResources1"]:
                '''(experimental) affectedResources property.

                Specify an array of string values to match this event if the actual value of affectedResources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("affected_resources")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.AffectedResources1"], result)

            @builtins.property
            def api(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) api property.

                Specify an array of string values to match this event if the actual value of api is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("api")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def caller_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) callerType property.

                Specify an array of string values to match this event if the actual value of callerType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("caller_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def error_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) errorCode property.

                Specify an array of string values to match this event if the actual value of errorCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("error_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def remote_account_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.RemoteAccountDetails"]:
                '''(experimental) remoteAccountDetails property.

                Specify an array of string values to match this event if the actual value of remoteAccountDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_account_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.RemoteAccountDetails"], result)

            @builtins.property
            def remote_ip_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails1"]:
                '''(experimental) remoteIpDetails property.

                Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_ip_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails1"], result)

            @builtins.property
            def service_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) serviceName property.

                Specify an array of string values to match this event if the actual value of serviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("service_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AwsApiCallAction1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.BlockPublicAccess",
            jsii_struct_bases=[],
            name_mapping={
                "block_public_acls": "blockPublicAcls",
                "block_public_policy": "blockPublicPolicy",
                "ignore_public_acls": "ignorePublicAcls",
                "restrict_public_buckets": "restrictPublicBuckets",
            },
        )
        class BlockPublicAccess:
            def __init__(
                self,
                *,
                block_public_acls: typing.Optional[typing.Sequence[builtins.str]] = None,
                block_public_policy: typing.Optional[typing.Sequence[builtins.str]] = None,
                ignore_public_acls: typing.Optional[typing.Sequence[builtins.str]] = None,
                restrict_public_buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for BlockPublicAccess.

                :param block_public_acls: (experimental) blockPublicAcls property. Specify an array of string values to match this event if the actual value of blockPublicAcls is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param block_public_policy: (experimental) blockPublicPolicy property. Specify an array of string values to match this event if the actual value of blockPublicPolicy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ignore_public_acls: (experimental) ignorePublicAcls property. Specify an array of string values to match this event if the actual value of ignorePublicAcls is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param restrict_public_buckets: (experimental) restrictPublicBuckets property. Specify an array of string values to match this event if the actual value of restrictPublicBuckets is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    block_public_access = guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                        block_public_acls=["blockPublicAcls"],
                        block_public_policy=["blockPublicPolicy"],
                        ignore_public_acls=["ignorePublicAcls"],
                        restrict_public_buckets=["restrictPublicBuckets"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b670adcd86867e24324da3675a0bfa35f089cbd4af64abbe6e205a44f47f239b)
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
            def block_public_acls(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) blockPublicAcls property.

                Specify an array of string values to match this event if the actual value of blockPublicAcls is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("block_public_acls")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def block_public_policy(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) blockPublicPolicy property.

                Specify an array of string values to match this event if the actual value of blockPublicPolicy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("block_public_policy")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ignore_public_acls(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ignorePublicAcls property.

                Specify an array of string values to match this event if the actual value of ignorePublicAcls is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ignore_public_acls")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def restrict_public_buckets(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) restrictPublicBuckets property.

                Specify an array of string values to match this event if the actual value of restrictPublicBuckets is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("restrict_public_buckets")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "BlockPublicAccess(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.BucketLevelPermissions",
            jsii_struct_bases=[],
            name_mapping={
                "access_control_list": "accessControlList",
                "block_public_access": "blockPublicAccess",
                "bucket_policy": "bucketPolicy",
            },
        )
        class BucketLevelPermissions:
            def __init__(
                self,
                *,
                access_control_list: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.AccessControlList", typing.Dict[builtins.str, typing.Any]]] = None,
                block_public_access: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.BlockPublicAccess", typing.Dict[builtins.str, typing.Any]]] = None,
                bucket_policy: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.AccessControlList", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for BucketLevelPermissions.

                :param access_control_list: (experimental) accessControlList property. Specify an array of string values to match this event if the actual value of accessControlList is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param block_public_access: (experimental) blockPublicAccess property. Specify an array of string values to match this event if the actual value of blockPublicAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bucket_policy: (experimental) bucketPolicy property. Specify an array of string values to match this event if the actual value of bucketPolicy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    bucket_level_permissions = guardduty_events.DetectorEvents.GuardDutyFinding.BucketLevelPermissions(
                        access_control_list=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                            allows_public_read_access=["allowsPublicReadAccess"],
                            allows_public_write_access=["allowsPublicWriteAccess"]
                        ),
                        block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                            block_public_acls=["blockPublicAcls"],
                            block_public_policy=["blockPublicPolicy"],
                            ignore_public_acls=["ignorePublicAcls"],
                            restrict_public_buckets=["restrictPublicBuckets"]
                        ),
                        bucket_policy=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                            allows_public_read_access=["allowsPublicReadAccess"],
                            allows_public_write_access=["allowsPublicWriteAccess"]
                        )
                    )
                '''
                if isinstance(access_control_list, dict):
                    access_control_list = DetectorEvents.GuardDutyFinding.AccessControlList(**access_control_list)
                if isinstance(block_public_access, dict):
                    block_public_access = DetectorEvents.GuardDutyFinding.BlockPublicAccess(**block_public_access)
                if isinstance(bucket_policy, dict):
                    bucket_policy = DetectorEvents.GuardDutyFinding.AccessControlList(**bucket_policy)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__76dbf150835ed6cc815ec6861bf29a8b244cbef02b3bfc784971f28c53552820)
                    check_type(argname="argument access_control_list", value=access_control_list, expected_type=type_hints["access_control_list"])
                    check_type(argname="argument block_public_access", value=block_public_access, expected_type=type_hints["block_public_access"])
                    check_type(argname="argument bucket_policy", value=bucket_policy, expected_type=type_hints["bucket_policy"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if access_control_list is not None:
                    self._values["access_control_list"] = access_control_list
                if block_public_access is not None:
                    self._values["block_public_access"] = block_public_access
                if bucket_policy is not None:
                    self._values["bucket_policy"] = bucket_policy

            @builtins.property
            def access_control_list(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.AccessControlList"]:
                '''(experimental) accessControlList property.

                Specify an array of string values to match this event if the actual value of accessControlList is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("access_control_list")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.AccessControlList"], result)

            @builtins.property
            def block_public_access(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.BlockPublicAccess"]:
                '''(experimental) blockPublicAccess property.

                Specify an array of string values to match this event if the actual value of blockPublicAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("block_public_access")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.BlockPublicAccess"], result)

            @builtins.property
            def bucket_policy(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.AccessControlList"]:
                '''(experimental) bucketPolicy property.

                Specify an array of string values to match this event if the actual value of bucketPolicy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket_policy")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.AccessControlList"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "BucketLevelPermissions(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.City",
            jsii_struct_bases=[],
            name_mapping={"city_name": "cityName"},
        )
        class City:
            def __init__(
                self,
                *,
                city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for City.

                :param city_name: (experimental) cityName property. Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    city = guardduty_events.DetectorEvents.GuardDutyFinding.City(
                        city_name=["cityName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__05a7e231cd730573bbafea735f5ad64c5dd6ce864321f0bb014fa4ae29a1f1d6)
                    check_type(argname="argument city_name", value=city_name, expected_type=type_hints["city_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city_name is not None:
                    self._values["city_name"] = city_name

            @builtins.property
            def city_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cityName property.

                Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "City(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.City1",
            jsii_struct_bases=[],
            name_mapping={"city_name": "cityName"},
        )
        class City1:
            def __init__(
                self,
                *,
                city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for City_1.

                :param city_name: (experimental) cityName property. Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    city1 = guardduty_events.DetectorEvents.GuardDutyFinding.City1(
                        city_name=["cityName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__80e7ec261905b9d0ac89c7d18a81c2082cc3e6909039278b62d040998de4f60b)
                    check_type(argname="argument city_name", value=city_name, expected_type=type_hints["city_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city_name is not None:
                    self._values["city_name"] = city_name

            @builtins.property
            def city_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cityName property.

                Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "City1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.City2",
            jsii_struct_bases=[],
            name_mapping={"city_name": "cityName"},
        )
        class City2:
            def __init__(
                self,
                *,
                city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for City_2.

                :param city_name: (experimental) cityName property. Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    city2 = guardduty_events.DetectorEvents.GuardDutyFinding.City2(
                        city_name=["cityName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e63a2d3e84ac2f87b6b6a27652a831674085533d45e8b5382b61959dd397b21e)
                    check_type(argname="argument city_name", value=city_name, expected_type=type_hints["city_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city_name is not None:
                    self._values["city_name"] = city_name

            @builtins.property
            def city_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cityName property.

                Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "City2(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.City3",
            jsii_struct_bases=[],
            name_mapping={"city_name": "cityName"},
        )
        class City3:
            def __init__(
                self,
                *,
                city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for City_3.

                :param city_name: (experimental) cityName property. Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    city3 = guardduty_events.DetectorEvents.GuardDutyFinding.City3(
                        city_name=["cityName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__bc56a271d8c4fa4be9d2f6c68f3abb6feab1a843e1d2a401dc89a8aee25a7233)
                    check_type(argname="argument city_name", value=city_name, expected_type=type_hints["city_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city_name is not None:
                    self._values["city_name"] = city_name

            @builtins.property
            def city_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cityName property.

                Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "City3(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.City4",
            jsii_struct_bases=[],
            name_mapping={"city_name": "cityName"},
        )
        class City4:
            def __init__(
                self,
                *,
                city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for City_4.

                :param city_name: (experimental) cityName property. Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    city4 = guardduty_events.DetectorEvents.GuardDutyFinding.City4(
                        city_name=["cityName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e885c8e49e6007011ee14917881ac249d3066e903af472ff518d4a4a2b786985)
                    check_type(argname="argument city_name", value=city_name, expected_type=type_hints["city_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city_name is not None:
                    self._values["city_name"] = city_name

            @builtins.property
            def city_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) cityName property.

                Specify an array of string values to match this event if the actual value of cityName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "City4(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.ContainerDetails",
            jsii_struct_bases=[],
            name_mapping={"id": "id", "image": "image", "name": "name"},
        )
        class ContainerDetails:
            def __init__(
                self,
                *,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                image: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ContainerDetails.

                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image: (experimental) image property. Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    container_details = guardduty_events.DetectorEvents.GuardDutyFinding.ContainerDetails(
                        id=["id"],
                        image=["image"],
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3bf080cb6d51ee16f9fdc9df79ae8cfa6166a026c9e56ad4ff99a5e1e16fe59f)
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if id is not None:
                    self._values["id"] = id
                if image is not None:
                    self._values["image"] = image
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image property.

                Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ContainerDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Country",
            jsii_struct_bases=[],
            name_mapping={"country_name": "countryName"},
        )
        class Country:
            def __init__(
                self,
                *,
                country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Country.

                :param country_name: (experimental) countryName property. Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    country = guardduty_events.DetectorEvents.GuardDutyFinding.Country(
                        country_name=["countryName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__30237ff2810eabe9b20a7ca216ff919f8564c9226cf4b19adc58218d2b7cc70a)
                    check_type(argname="argument country_name", value=country_name, expected_type=type_hints["country_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if country_name is not None:
                    self._values["country_name"] = country_name

            @builtins.property
            def country_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) countryName property.

                Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Country(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Country1",
            jsii_struct_bases=[],
            name_mapping={"country_name": "countryName"},
        )
        class Country1:
            def __init__(
                self,
                *,
                country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Country_1.

                :param country_name: (experimental) countryName property. Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    country1 = guardduty_events.DetectorEvents.GuardDutyFinding.Country1(
                        country_name=["countryName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c7143c4c38f9d665423b26efbb3bf504931b6cab1d8ed236ee3a0eb07b957b44)
                    check_type(argname="argument country_name", value=country_name, expected_type=type_hints["country_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if country_name is not None:
                    self._values["country_name"] = country_name

            @builtins.property
            def country_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) countryName property.

                Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Country1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Country2",
            jsii_struct_bases=[],
            name_mapping={"country_name": "countryName"},
        )
        class Country2:
            def __init__(
                self,
                *,
                country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Country_2.

                :param country_name: (experimental) countryName property. Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    country2 = guardduty_events.DetectorEvents.GuardDutyFinding.Country2(
                        country_name=["countryName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8d5f64998c17f42143afa6451d38f7b34ade8104dac8a15d44060874409627f2)
                    check_type(argname="argument country_name", value=country_name, expected_type=type_hints["country_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if country_name is not None:
                    self._values["country_name"] = country_name

            @builtins.property
            def country_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) countryName property.

                Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Country2(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Country3",
            jsii_struct_bases=[],
            name_mapping={"country_name": "countryName"},
        )
        class Country3:
            def __init__(
                self,
                *,
                country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Country_3.

                :param country_name: (experimental) countryName property. Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    country3 = guardduty_events.DetectorEvents.GuardDutyFinding.Country3(
                        country_name=["countryName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f36f66863f8321a333c574dbb8665235d3d9c75a77ac754f0821fb6fe27d8be7)
                    check_type(argname="argument country_name", value=country_name, expected_type=type_hints["country_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if country_name is not None:
                    self._values["country_name"] = country_name

            @builtins.property
            def country_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) countryName property.

                Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Country3(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Country4",
            jsii_struct_bases=[],
            name_mapping={"country_name": "countryName"},
        )
        class Country4:
            def __init__(
                self,
                *,
                country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Country_4.

                :param country_name: (experimental) countryName property. Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    country4 = guardduty_events.DetectorEvents.GuardDutyFinding.Country4(
                        country_name=["countryName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cbb8267a05b15ef44790db97ea43fd868310a575ec61c4234dd51b59fd3b16cb)
                    check_type(argname="argument country_name", value=country_name, expected_type=type_hints["country_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if country_name is not None:
                    self._values["country_name"] = country_name

            @builtins.property
            def country_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) countryName property.

                Specify an array of string values to match this event if the actual value of countryName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Country4(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.DefaultServerSideEncryption",
            jsii_struct_bases=[],
            name_mapping={
                "encryption_type": "encryptionType",
                "kms_master_key_arn": "kmsMasterKeyArn",
            },
        )
        class DefaultServerSideEncryption:
            def __init__(
                self,
                *,
                encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                kms_master_key_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for DefaultServerSideEncryption.

                :param encryption_type: (experimental) encryptionType property. Specify an array of string values to match this event if the actual value of encryptionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param kms_master_key_arn: (experimental) kmsMasterKeyArn property. Specify an array of string values to match this event if the actual value of kmsMasterKeyArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    default_server_side_encryption = guardduty_events.DetectorEvents.GuardDutyFinding.DefaultServerSideEncryption(
                        encryption_type=["encryptionType"],
                        kms_master_key_arn=["kmsMasterKeyArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2fa9d04c947a7f9b7d1dc525bc8a0150ab7c23e3a85d46023c05ee986adaf636)
                    check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                    check_type(argname="argument kms_master_key_arn", value=kms_master_key_arn, expected_type=type_hints["kms_master_key_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if encryption_type is not None:
                    self._values["encryption_type"] = encryption_type
                if kms_master_key_arn is not None:
                    self._values["kms_master_key_arn"] = kms_master_key_arn

            @builtins.property
            def encryption_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) encryptionType property.

                Specify an array of string values to match this event if the actual value of encryptionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("encryption_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def kms_master_key_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) kmsMasterKeyArn property.

                Specify an array of string values to match this event if the actual value of kmsMasterKeyArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("kms_master_key_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DefaultServerSideEncryption(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.DnsRequestAction",
            jsii_struct_bases=[],
            name_mapping={
                "blocked": "blocked",
                "domain": "domain",
                "protocol": "protocol",
            },
        )
        class DnsRequestAction:
            def __init__(
                self,
                *,
                blocked: typing.Optional[typing.Sequence[builtins.str]] = None,
                domain: typing.Optional[typing.Sequence[builtins.str]] = None,
                protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for DnsRequestAction.

                :param blocked: (experimental) blocked property. Specify an array of string values to match this event if the actual value of blocked is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param domain: (experimental) domain property. Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param protocol: (experimental) protocol property. Specify an array of string values to match this event if the actual value of protocol is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    dns_request_action = guardduty_events.DetectorEvents.GuardDutyFinding.DnsRequestAction(
                        blocked=["blocked"],
                        domain=["domain"],
                        protocol=["protocol"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__c00c1ee0d9a007e987319e9979eb02a6ba0f22db7d9791761c212eaad7cc8991)
                    check_type(argname="argument blocked", value=blocked, expected_type=type_hints["blocked"])
                    check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
                    check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if blocked is not None:
                    self._values["blocked"] = blocked
                if domain is not None:
                    self._values["domain"] = domain
                if protocol is not None:
                    self._values["protocol"] = protocol

            @builtins.property
            def blocked(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) blocked property.

                Specify an array of string values to match this event if the actual value of blocked is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("blocked")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def domain(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) domain property.

                Specify an array of string values to match this event if the actual value of domain is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("domain")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def protocol(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) protocol property.

                Specify an array of string values to match this event if the actual value of protocol is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("protocol")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "DnsRequestAction(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.EbsVolumeDetails",
            jsii_struct_bases=[],
            name_mapping={
                "scanned_volume_details": "scannedVolumeDetails",
                "skipped_volume_details": "skippedVolumeDetails",
            },
        )
        class EbsVolumeDetails:
            def __init__(
                self,
                *,
                scanned_volume_details: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.EbsVolumeDetailsItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                skipped_volume_details: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for EbsVolumeDetails.

                :param scanned_volume_details: (experimental) scannedVolumeDetails property. Specify an array of string values to match this event if the actual value of scannedVolumeDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param skipped_volume_details: (experimental) skippedVolumeDetails property. Specify an array of string values to match this event if the actual value of skippedVolumeDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    ebs_volume_details = guardduty_events.DetectorEvents.GuardDutyFinding.EbsVolumeDetails(
                        scanned_volume_details=[guardduty_events.DetectorEvents.GuardDutyFinding.EbsVolumeDetailsItem(
                            device_name=["deviceName"],
                            encryption_type=["encryptionType"],
                            kms_key_arn=["kmsKeyArn"],
                            snapshot_arn=["snapshotArn"],
                            volume_arn=["volumeArn"],
                            volume_size_in_gb=["volumeSizeInGb"],
                            volume_type=["volumeType"]
                        )],
                        skipped_volume_details=["skippedVolumeDetails"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3b52118043d4134545238996820c8d60d7fc4334aceb115446f9fbb8db9cad41)
                    check_type(argname="argument scanned_volume_details", value=scanned_volume_details, expected_type=type_hints["scanned_volume_details"])
                    check_type(argname="argument skipped_volume_details", value=skipped_volume_details, expected_type=type_hints["skipped_volume_details"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if scanned_volume_details is not None:
                    self._values["scanned_volume_details"] = scanned_volume_details
                if skipped_volume_details is not None:
                    self._values["skipped_volume_details"] = skipped_volume_details

            @builtins.property
            def scanned_volume_details(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EbsVolumeDetailsItem"]]:
                '''(experimental) scannedVolumeDetails property.

                Specify an array of string values to match this event if the actual value of scannedVolumeDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("scanned_volume_details")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EbsVolumeDetailsItem"]], result)

            @builtins.property
            def skipped_volume_details(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) skippedVolumeDetails property.

                Specify an array of string values to match this event if the actual value of skippedVolumeDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("skipped_volume_details")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EbsVolumeDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.EbsVolumeDetailsItem",
            jsii_struct_bases=[],
            name_mapping={
                "device_name": "deviceName",
                "encryption_type": "encryptionType",
                "kms_key_arn": "kmsKeyArn",
                "snapshot_arn": "snapshotArn",
                "volume_arn": "volumeArn",
                "volume_size_in_gb": "volumeSizeInGb",
                "volume_type": "volumeType",
            },
        )
        class EbsVolumeDetailsItem:
            def __init__(
                self,
                *,
                device_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                kms_key_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                snapshot_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                volume_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                volume_size_in_gb: typing.Optional[typing.Sequence[builtins.str]] = None,
                volume_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for EbsVolumeDetailsItem.

                :param device_name: (experimental) deviceName property. Specify an array of string values to match this event if the actual value of deviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param encryption_type: (experimental) encryptionType property. Specify an array of string values to match this event if the actual value of encryptionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param kms_key_arn: (experimental) kmsKeyArn property. Specify an array of string values to match this event if the actual value of kmsKeyArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param snapshot_arn: (experimental) snapshotArn property. Specify an array of string values to match this event if the actual value of snapshotArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param volume_arn: (experimental) volumeArn property. Specify an array of string values to match this event if the actual value of volumeArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param volume_size_in_gb: (experimental) volumeSizeInGB property. Specify an array of string values to match this event if the actual value of volumeSizeInGB is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param volume_type: (experimental) volumeType property. Specify an array of string values to match this event if the actual value of volumeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    ebs_volume_details_item = guardduty_events.DetectorEvents.GuardDutyFinding.EbsVolumeDetailsItem(
                        device_name=["deviceName"],
                        encryption_type=["encryptionType"],
                        kms_key_arn=["kmsKeyArn"],
                        snapshot_arn=["snapshotArn"],
                        volume_arn=["volumeArn"],
                        volume_size_in_gb=["volumeSizeInGb"],
                        volume_type=["volumeType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__fef6023280e9b1a85f0df8488ff161da532e17610266d37dea1f4e79dd4bcf77)
                    check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
                    check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                    check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                    check_type(argname="argument snapshot_arn", value=snapshot_arn, expected_type=type_hints["snapshot_arn"])
                    check_type(argname="argument volume_arn", value=volume_arn, expected_type=type_hints["volume_arn"])
                    check_type(argname="argument volume_size_in_gb", value=volume_size_in_gb, expected_type=type_hints["volume_size_in_gb"])
                    check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if device_name is not None:
                    self._values["device_name"] = device_name
                if encryption_type is not None:
                    self._values["encryption_type"] = encryption_type
                if kms_key_arn is not None:
                    self._values["kms_key_arn"] = kms_key_arn
                if snapshot_arn is not None:
                    self._values["snapshot_arn"] = snapshot_arn
                if volume_arn is not None:
                    self._values["volume_arn"] = volume_arn
                if volume_size_in_gb is not None:
                    self._values["volume_size_in_gb"] = volume_size_in_gb
                if volume_type is not None:
                    self._values["volume_type"] = volume_type

            @builtins.property
            def device_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) deviceName property.

                Specify an array of string values to match this event if the actual value of deviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("device_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def encryption_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) encryptionType property.

                Specify an array of string values to match this event if the actual value of encryptionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("encryption_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def kms_key_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) kmsKeyArn property.

                Specify an array of string values to match this event if the actual value of kmsKeyArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("kms_key_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def snapshot_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) snapshotArn property.

                Specify an array of string values to match this event if the actual value of snapshotArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("snapshot_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def volume_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) volumeArn property.

                Specify an array of string values to match this event if the actual value of volumeArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("volume_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def volume_size_in_gb(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) volumeSizeInGB property.

                Specify an array of string values to match this event if the actual value of volumeSizeInGB is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("volume_size_in_gb")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def volume_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) volumeType property.

                Specify an array of string values to match this event if the actual value of volumeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("volume_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EbsVolumeDetailsItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.EbsVolumeScanDetails",
            jsii_struct_bases=[],
            name_mapping={
                "scan_completed_at": "scanCompletedAt",
                "scan_detections": "scanDetections",
                "scan_id": "scanId",
                "scan_started_at": "scanStartedAt",
                "sources": "sources",
                "trigger_finding_id": "triggerFindingId",
            },
        )
        class EbsVolumeScanDetails:
            def __init__(
                self,
                *,
                scan_completed_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                scan_detections: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.ScanDetections", typing.Dict[builtins.str, typing.Any]]] = None,
                scan_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                scan_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                sources: typing.Optional[typing.Sequence[builtins.str]] = None,
                trigger_finding_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for EbsVolumeScanDetails.

                :param scan_completed_at: (experimental) scanCompletedAt property. Specify an array of string values to match this event if the actual value of scanCompletedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param scan_detections: (experimental) scanDetections property. Specify an array of string values to match this event if the actual value of scanDetections is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param scan_id: (experimental) scanId property. Specify an array of string values to match this event if the actual value of scanId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param scan_started_at: (experimental) scanStartedAt property. Specify an array of string values to match this event if the actual value of scanStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param sources: (experimental) sources property. Specify an array of string values to match this event if the actual value of sources is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param trigger_finding_id: (experimental) triggerFindingId property. Specify an array of string values to match this event if the actual value of triggerFindingId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    ebs_volume_scan_details = guardduty_events.DetectorEvents.GuardDutyFinding.EbsVolumeScanDetails(
                        scan_completed_at=["scanCompletedAt"],
                        scan_detections=guardduty_events.DetectorEvents.GuardDutyFinding.ScanDetections(
                            highest_severity_threat_details=guardduty_events.DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails(
                                count=["count"],
                                severity=["severity"],
                                threat_name=["threatName"]
                            ),
                            scanned_item_count=guardduty_events.DetectorEvents.GuardDutyFinding.ScannedItemCount(
                                files=["files"],
                                total_gb=["totalGb"],
                                volumes=["volumes"]
                            ),
                            threat_detected_by_name=guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByName(
                                item_count=["itemCount"],
                                shortened=["shortened"],
                                threat_names=[guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem(
                                    file_paths=[guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem(
                                        file_name=["fileName"],
                                        file_path=["filePath"],
                                        hash=["hash"],
                                        volume_arn=["volumeArn"]
                                    )],
                                    item_count=["itemCount"],
                                    name=["name"],
                                    severity=["severity"]
                                )],
                                unique_threat_name_count=["uniqueThreatNameCount"]
                            ),
                            threats_detected_item_count=guardduty_events.DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount(
                                files=["files"]
                            )
                        ),
                        scan_id=["scanId"],
                        scan_started_at=["scanStartedAt"],
                        sources=["sources"],
                        trigger_finding_id=["triggerFindingId"]
                    )
                '''
                if isinstance(scan_detections, dict):
                    scan_detections = DetectorEvents.GuardDutyFinding.ScanDetections(**scan_detections)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7545d367135761a6f7ce2ceda9af5f1fff0c33eae3c7967a4ec3f6fc43ad79db)
                    check_type(argname="argument scan_completed_at", value=scan_completed_at, expected_type=type_hints["scan_completed_at"])
                    check_type(argname="argument scan_detections", value=scan_detections, expected_type=type_hints["scan_detections"])
                    check_type(argname="argument scan_id", value=scan_id, expected_type=type_hints["scan_id"])
                    check_type(argname="argument scan_started_at", value=scan_started_at, expected_type=type_hints["scan_started_at"])
                    check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
                    check_type(argname="argument trigger_finding_id", value=trigger_finding_id, expected_type=type_hints["trigger_finding_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if scan_completed_at is not None:
                    self._values["scan_completed_at"] = scan_completed_at
                if scan_detections is not None:
                    self._values["scan_detections"] = scan_detections
                if scan_id is not None:
                    self._values["scan_id"] = scan_id
                if scan_started_at is not None:
                    self._values["scan_started_at"] = scan_started_at
                if sources is not None:
                    self._values["sources"] = sources
                if trigger_finding_id is not None:
                    self._values["trigger_finding_id"] = trigger_finding_id

            @builtins.property
            def scan_completed_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) scanCompletedAt property.

                Specify an array of string values to match this event if the actual value of scanCompletedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("scan_completed_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def scan_detections(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.ScanDetections"]:
                '''(experimental) scanDetections property.

                Specify an array of string values to match this event if the actual value of scanDetections is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("scan_detections")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.ScanDetections"], result)

            @builtins.property
            def scan_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) scanId property.

                Specify an array of string values to match this event if the actual value of scanId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("scan_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def scan_started_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) scanStartedAt property.

                Specify an array of string values to match this event if the actual value of scanStartedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("scan_started_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def sources(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sources property.

                Specify an array of string values to match this event if the actual value of sources is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("sources")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def trigger_finding_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) triggerFindingId property.

                Specify an array of string values to match this event if the actual value of triggerFindingId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("trigger_finding_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EbsVolumeScanDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.EcsClusterDetails",
            jsii_struct_bases=[],
            name_mapping={
                "arn": "arn",
                "name": "name",
                "status": "status",
                "tags": "tags",
                "task_details": "taskDetails",
            },
        )
        class EcsClusterDetails:
            def __init__(
                self,
                *,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                task_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.TaskDetails", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for EcsClusterDetails.

                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tags: (experimental) tags property. Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param task_details: (experimental) taskDetails property. Specify an array of string values to match this event if the actual value of taskDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    ecs_cluster_details = guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetails(
                        arn=["arn"],
                        name=["name"],
                        status=["status"],
                        tags=[guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem(
                            key=["key"],
                            value=["value"]
                        )],
                        task_details=guardduty_events.DetectorEvents.GuardDutyFinding.TaskDetails(
                            arn=["arn"],
                            containers=[guardduty_events.DetectorEvents.GuardDutyFinding.TaskDetailsItem(
                                image=["image"],
                                name=["name"]
                            )],
                            created_at=["createdAt"],
                            definition_arn=["definitionArn"],
                            started_at=["startedAt"],
                            started_by=["startedBy"],
                            version=["version"]
                        )
                    )
                '''
                if isinstance(task_details, dict):
                    task_details = DetectorEvents.GuardDutyFinding.TaskDetails(**task_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9fc1924b3ca3db2b07b18acebff7f916de793d2d831e0bf34b5d37a14316ae79)
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                    check_type(argname="argument task_details", value=task_details, expected_type=type_hints["task_details"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if arn is not None:
                    self._values["arn"] = arn
                if name is not None:
                    self._values["name"] = name
                if status is not None:
                    self._values["status"] = status
                if tags is not None:
                    self._values["tags"] = tags
                if task_details is not None:
                    self._values["task_details"] = task_details

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tags(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem"]]:
                '''(experimental) tags property.

                Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem"]], result)

            @builtins.property
            def task_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.TaskDetails"]:
                '''(experimental) taskDetails property.

                Specify an array of string values to match this event if the actual value of taskDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("task_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.TaskDetails"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EcsClusterDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem",
            jsii_struct_bases=[],
            name_mapping={"key": "key", "value": "value"},
        )
        class EcsClusterDetailsItem:
            def __init__(
                self,
                *,
                key: typing.Optional[typing.Sequence[builtins.str]] = None,
                value: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for EcsClusterDetailsItem.

                :param key: (experimental) key property. Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param value: (experimental) value property. Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    ecs_cluster_details_item = guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem(
                        key=["key"],
                        value=["value"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9483d79a5a8974555a84597ab576164697c0f920416deb279b29ef4f56e5ee2e)
                    check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                    check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if key is not None:
                    self._values["key"] = key
                if value is not None:
                    self._values["value"] = value

            @builtins.property
            def key(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) key property.

                Specify an array of string values to match this event if the actual value of key is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("key")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def value(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) value property.

                Specify an array of string values to match this event if the actual value of value is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("value")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EcsClusterDetailsItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.EksClusterDetails",
            jsii_struct_bases=[],
            name_mapping={
                "arn": "arn",
                "created_at": "createdAt",
                "name": "name",
                "status": "status",
                "tags": "tags",
                "vpc_id": "vpcId",
            },
        )
        class EksClusterDetails:
            def __init__(
                self,
                *,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                status: typing.Optional[typing.Sequence[builtins.str]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for EksClusterDetails.

                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status: (experimental) status property. Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tags: (experimental) tags property. Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param vpc_id: (experimental) vpcId property. Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    eks_cluster_details = guardduty_events.DetectorEvents.GuardDutyFinding.EksClusterDetails(
                        arn=["arn"],
                        created_at=["createdAt"],
                        name=["name"],
                        status=["status"],
                        tags=[guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem(
                            key=["key"],
                            value=["value"]
                        )],
                        vpc_id=["vpcId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d83bcf2a34559dd7633e231cf69bedeb815ad7a7c71321813580a7c539470906)
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                    check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if arn is not None:
                    self._values["arn"] = arn
                if created_at is not None:
                    self._values["created_at"] = created_at
                if name is not None:
                    self._values["name"] = name
                if status is not None:
                    self._values["status"] = status
                if tags is not None:
                    self._values["tags"] = tags
                if vpc_id is not None:
                    self._values["vpc_id"] = vpc_id

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def created_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) createdAt property.

                Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("created_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) status property.

                Specify an array of string values to match this event if the actual value of status is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def tags(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem"]]:
                '''(experimental) tags property.

                Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem"]], result)

            @builtins.property
            def vpc_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) vpcId property.

                Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("vpc_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EksClusterDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Evidence",
            jsii_struct_bases=[],
            name_mapping={"threat_intelligence_details": "threatIntelligenceDetails"},
        )
        class Evidence:
            def __init__(
                self,
                *,
                threat_intelligence_details: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.EvidenceItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for Evidence.

                :param threat_intelligence_details: (experimental) threatIntelligenceDetails property. Specify an array of string values to match this event if the actual value of threatIntelligenceDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    evidence = guardduty_events.DetectorEvents.GuardDutyFinding.Evidence(
                        threat_intelligence_details=[guardduty_events.DetectorEvents.GuardDutyFinding.EvidenceItem(
                            threat_list_name=["threatListName"],
                            threat_names=["threatNames"]
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d8c713fa355e53ae2622feceaa3d5f141b5684677ef577ba4bfe54f2fd479413)
                    check_type(argname="argument threat_intelligence_details", value=threat_intelligence_details, expected_type=type_hints["threat_intelligence_details"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if threat_intelligence_details is not None:
                    self._values["threat_intelligence_details"] = threat_intelligence_details

            @builtins.property
            def threat_intelligence_details(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EvidenceItem"]]:
                '''(experimental) threatIntelligenceDetails property.

                Specify an array of string values to match this event if the actual value of threatIntelligenceDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threat_intelligence_details")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EvidenceItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Evidence(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.EvidenceItem",
            jsii_struct_bases=[],
            name_mapping={
                "threat_list_name": "threatListName",
                "threat_names": "threatNames",
            },
        )
        class EvidenceItem:
            def __init__(
                self,
                *,
                threat_list_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                threat_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for EvidenceItem.

                :param threat_list_name: (experimental) threatListName property. Specify an array of string values to match this event if the actual value of threatListName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param threat_names: (experimental) threatNames property. Specify an array of string values to match this event if the actual value of threatNames is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    evidence_item = guardduty_events.DetectorEvents.GuardDutyFinding.EvidenceItem(
                        threat_list_name=["threatListName"],
                        threat_names=["threatNames"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__7869f95b17e09579f07d4f67fa4a04c75909e8a3dedb0649ff88335a0ed2fb59)
                    check_type(argname="argument threat_list_name", value=threat_list_name, expected_type=type_hints["threat_list_name"])
                    check_type(argname="argument threat_names", value=threat_names, expected_type=type_hints["threat_names"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if threat_list_name is not None:
                    self._values["threat_list_name"] = threat_list_name
                if threat_names is not None:
                    self._values["threat_names"] = threat_names

            @builtins.property
            def threat_list_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) threatListName property.

                Specify an array of string values to match this event if the actual value of threatListName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threat_list_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def threat_names(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) threatNames property.

                Specify an array of string values to match this event if the actual value of threatNames is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threat_names")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "EvidenceItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.GeoLocation",
            jsii_struct_bases=[],
            name_mapping={"lat": "lat", "lon": "lon"},
        )
        class GeoLocation:
            def __init__(
                self,
                *,
                lat: typing.Optional[typing.Sequence[builtins.str]] = None,
                lon: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for GeoLocation.

                :param lat: (experimental) lat property. Specify an array of string values to match this event if the actual value of lat is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param lon: (experimental) lon property. Specify an array of string values to match this event if the actual value of lon is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    geo_location = guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                        lat=["lat"],
                        lon=["lon"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__160acc8f927005550ea8915557aa67945f6ab0578d496d3435af86316ff76146)
                    check_type(argname="argument lat", value=lat, expected_type=type_hints["lat"])
                    check_type(argname="argument lon", value=lon, expected_type=type_hints["lon"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if lat is not None:
                    self._values["lat"] = lat
                if lon is not None:
                    self._values["lon"] = lon

            @builtins.property
            def lat(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lat property.

                Specify an array of string values to match this event if the actual value of lat is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lat")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def lon(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lon property.

                Specify an array of string values to match this event if the actual value of lon is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lon")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GeoLocation(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.GeoLocation1",
            jsii_struct_bases=[],
            name_mapping={"lat": "lat", "lon": "lon"},
        )
        class GeoLocation1:
            def __init__(
                self,
                *,
                lat: typing.Optional[typing.Sequence[builtins.str]] = None,
                lon: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for GeoLocation_1.

                :param lat: (experimental) lat property. Specify an array of string values to match this event if the actual value of lat is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param lon: (experimental) lon property. Specify an array of string values to match this event if the actual value of lon is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    geo_location1 = guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation1(
                        lat=["lat"],
                        lon=["lon"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a7a9b878db2b3fd6e87f26e6d06c036d4b5a1a1e66a1195fef6d158e9ff92561)
                    check_type(argname="argument lat", value=lat, expected_type=type_hints["lat"])
                    check_type(argname="argument lon", value=lon, expected_type=type_hints["lon"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if lat is not None:
                    self._values["lat"] = lat
                if lon is not None:
                    self._values["lon"] = lon

            @builtins.property
            def lat(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lat property.

                Specify an array of string values to match this event if the actual value of lat is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lat")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def lon(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) lon property.

                Specify an array of string values to match this event if the actual value of lon is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("lon")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GeoLocation1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.GuardDutyFindingProps",
            jsii_struct_bases=[],
            name_mapping={
                "account_id": "accountId",
                "arn": "arn",
                "created_at": "createdAt",
                "description": "description",
                "event_metadata": "eventMetadata",
                "id": "id",
                "partition": "partition",
                "region": "region",
                "resource": "resource",
                "schema_version": "schemaVersion",
                "service": "service",
                "severity": "severity",
                "title": "title",
                "type": "type",
                "updated_at": "updatedAt",
            },
        )
        class GuardDutyFindingProps:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                description: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
                partition: typing.Optional[typing.Sequence[builtins.str]] = None,
                region: typing.Optional[typing.Sequence[builtins.str]] = None,
                resource: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Resource", typing.Dict[builtins.str, typing.Any]]] = None,
                schema_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                service: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Service", typing.Dict[builtins.str, typing.Any]]] = None,
                severity: typing.Optional[typing.Sequence[builtins.str]] = None,
                title: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
                updated_at: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Detector aws.guardduty@GuardDutyFinding event.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param description: (experimental) description property. Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param partition: (experimental) partition property. Specify an array of string values to match this event if the actual value of partition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param region: (experimental) region property. Specify an array of string values to match this event if the actual value of region is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resource: (experimental) resource property. Specify an array of string values to match this event if the actual value of resource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param schema_version: (experimental) schemaVersion property. Specify an array of string values to match this event if the actual value of schemaVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param service: (experimental) service property. Specify an array of string values to match this event if the actual value of service is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param severity: (experimental) severity property. Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param title: (experimental) title property. Specify an array of string values to match this event if the actual value of title is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param updated_at: (experimental) updatedAt property. Specify an array of string values to match this event if the actual value of updatedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(resource, dict):
                    resource = DetectorEvents.GuardDutyFinding.Resource(**resource)
                if isinstance(service, dict):
                    service = DetectorEvents.GuardDutyFinding.Service(**service)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__37f9aa2b12b06325b6d5ef217562a3b7f33f1b2b0a889b09c011766d5c188827)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                    check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                    check_type(argname="argument partition", value=partition, expected_type=type_hints["partition"])
                    check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                    check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
                    check_type(argname="argument schema_version", value=schema_version, expected_type=type_hints["schema_version"])
                    check_type(argname="argument service", value=service, expected_type=type_hints["service"])
                    check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
                    check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                    check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if created_at is not None:
                    self._values["created_at"] = created_at
                if description is not None:
                    self._values["description"] = description
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if id is not None:
                    self._values["id"] = id
                if partition is not None:
                    self._values["partition"] = partition
                if region is not None:
                    self._values["region"] = region
                if resource is not None:
                    self._values["resource"] = resource
                if schema_version is not None:
                    self._values["schema_version"] = schema_version
                if service is not None:
                    self._values["service"] = service
                if severity is not None:
                    self._values["severity"] = severity
                if title is not None:
                    self._values["title"] = title
                if type is not None:
                    self._values["type"] = type
                if updated_at is not None:
                    self._values["updated_at"] = updated_at

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountId property.

                Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def created_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) createdAt property.

                Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("created_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) description property.

                Specify an array of string values to match this event if the actual value of description is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_metadata(
                self,
            ) -> typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps]:
                '''(experimental) EventBridge event metadata.

                :default:

                -
                -

                :stability: experimental
                '''
                result = self._values.get("event_metadata")
                return typing.cast(typing.Optional[_aws_cdk_ceddda9d.AWSEventMetadataProps], result)

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def partition(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) partition property.

                Specify an array of string values to match this event if the actual value of partition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("partition")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def region(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) region property.

                Specify an array of string values to match this event if the actual value of region is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("region")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def resource(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Resource"]:
                '''(experimental) resource property.

                Specify an array of string values to match this event if the actual value of resource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Resource"], result)

            @builtins.property
            def schema_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) schemaVersion property.

                Specify an array of string values to match this event if the actual value of schemaVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("schema_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def service(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Service"]:
                '''(experimental) service property.

                Specify an array of string values to match this event if the actual value of service is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("service")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Service"], result)

            @builtins.property
            def severity(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) severity property.

                Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("severity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def title(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) title property.

                Specify an array of string values to match this event if the actual value of title is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("title")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def updated_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) updatedAt property.

                Specify an array of string values to match this event if the actual value of updatedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("updated_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GuardDutyFindingProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails",
            jsii_struct_bases=[],
            name_mapping={
                "count": "count",
                "severity": "severity",
                "threat_name": "threatName",
            },
        )
        class HighestSeverityThreatDetails:
            def __init__(
                self,
                *,
                count: typing.Optional[typing.Sequence[builtins.str]] = None,
                severity: typing.Optional[typing.Sequence[builtins.str]] = None,
                threat_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for HighestSeverityThreatDetails.

                :param count: (experimental) count property. Specify an array of string values to match this event if the actual value of count is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param severity: (experimental) severity property. Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param threat_name: (experimental) threatName property. Specify an array of string values to match this event if the actual value of threatName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    highest_severity_threat_details = guardduty_events.DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails(
                        count=["count"],
                        severity=["severity"],
                        threat_name=["threatName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d45ae80c621ac2524961891ffefd32357f6046228dfa0819678360015b43ce62)
                    check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                    check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
                    check_type(argname="argument threat_name", value=threat_name, expected_type=type_hints["threat_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if count is not None:
                    self._values["count"] = count
                if severity is not None:
                    self._values["severity"] = severity
                if threat_name is not None:
                    self._values["threat_name"] = threat_name

            @builtins.property
            def count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) count property.

                Specify an array of string values to match this event if the actual value of count is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def severity(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) severity property.

                Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("severity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def threat_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) threatName property.

                Specify an array of string values to match this event if the actual value of threatName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threat_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "HighestSeverityThreatDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.IamInstanceProfile",
            jsii_struct_bases=[],
            name_mapping={"arn": "arn", "id": "id"},
        )
        class IamInstanceProfile:
            def __init__(
                self,
                *,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for IamInstanceProfile.

                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    iam_instance_profile = guardduty_events.DetectorEvents.GuardDutyFinding.IamInstanceProfile(
                        arn=["arn"],
                        id=["id"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__fe804246448e1ae068fd522757ffa163425487b4f3428ae8faf73d905867a1c3)
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if arn is not None:
                    self._values["arn"] = arn
                if id is not None:
                    self._values["id"] = id

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "IamInstanceProfile(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.InstanceDetails",
            jsii_struct_bases=[],
            name_mapping={
                "availability_zone": "availabilityZone",
                "iam_instance_profile": "iamInstanceProfile",
                "image_description": "imageDescription",
                "image_id": "imageId",
                "instance_id": "instanceId",
                "instance_state": "instanceState",
                "instance_type": "instanceType",
                "launch_time": "launchTime",
                "network_interfaces": "networkInterfaces",
                "outpost_arn": "outpostArn",
                "platform": "platform",
                "product_codes": "productCodes",
                "tags": "tags",
            },
        )
        class InstanceDetails:
            def __init__(
                self,
                *,
                availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
                iam_instance_profile: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.IamInstanceProfile", typing.Dict[builtins.str, typing.Any]]] = None,
                image_description: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_state: typing.Optional[typing.Sequence[builtins.str]] = None,
                instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                launch_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_interfaces: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.InstanceDetailsItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                outpost_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                platform: typing.Optional[typing.Sequence[builtins.str]] = None,
                product_codes: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.InstanceDetailsItem1", typing.Dict[builtins.str, typing.Any]]]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for InstanceDetails.

                :param availability_zone: (experimental) availabilityZone property. Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param iam_instance_profile: (experimental) iamInstanceProfile property. Specify an array of string values to match this event if the actual value of iamInstanceProfile is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_description: (experimental) imageDescription property. Specify an array of string values to match this event if the actual value of imageDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_id: (experimental) imageId property. Specify an array of string values to match this event if the actual value of imageId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_id: (experimental) instanceId property. Specify an array of string values to match this event if the actual value of instanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_state: (experimental) instanceState property. Specify an array of string values to match this event if the actual value of instanceState is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_type: (experimental) instanceType property. Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param launch_time: (experimental) launchTime property. Specify an array of string values to match this event if the actual value of launchTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interfaces: (experimental) networkInterfaces property. Specify an array of string values to match this event if the actual value of networkInterfaces is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param outpost_arn: (experimental) outpostArn property. Specify an array of string values to match this event if the actual value of outpostArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param platform: (experimental) platform property. Specify an array of string values to match this event if the actual value of platform is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param product_codes: (experimental) productCodes property. Specify an array of string values to match this event if the actual value of productCodes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tags: (experimental) tags property. Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    # ipv6_addresses: Any
                    
                    instance_details = guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetails(
                        availability_zone=["availabilityZone"],
                        iam_instance_profile=guardduty_events.DetectorEvents.GuardDutyFinding.IamInstanceProfile(
                            arn=["arn"],
                            id=["id"]
                        ),
                        image_description=["imageDescription"],
                        image_id=["imageId"],
                        instance_id=["instanceId"],
                        instance_state=["instanceState"],
                        instance_type=["instanceType"],
                        launch_time=["launchTime"],
                        network_interfaces=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItem(
                            ipv6_addresses=[ipv6_addresses],
                            network_interface_id=["networkInterfaceId"],
                            private_dns_name=["privateDnsName"],
                            private_ip_address=["privateIpAddress"],
                            private_ip_addresses=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem(
                                private_dns_name=["privateDnsName"],
                                private_ip_address=["privateIpAddress"]
                            )],
                            public_dns_name=["publicDnsName"],
                            public_ip=["publicIp"],
                            security_groups=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem1(
                                group_id=["groupId"],
                                group_name=["groupName"]
                            )],
                            subnet_id=["subnetId"],
                            vpc_id=["vpcId"]
                        )],
                        outpost_arn=["outpostArn"],
                        platform=["platform"],
                        product_codes=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItem1(
                            product_code_id=["productCodeId"],
                            product_code_type=["productCodeType"]
                        )],
                        tags=[guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem(
                            key=["key"],
                            value=["value"]
                        )]
                    )
                '''
                if isinstance(iam_instance_profile, dict):
                    iam_instance_profile = DetectorEvents.GuardDutyFinding.IamInstanceProfile(**iam_instance_profile)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__29357cb4ee83ef3773445fd3c784d164fc6e9fc8e452c1833fb8406872b34683)
                    check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                    check_type(argname="argument iam_instance_profile", value=iam_instance_profile, expected_type=type_hints["iam_instance_profile"])
                    check_type(argname="argument image_description", value=image_description, expected_type=type_hints["image_description"])
                    check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
                    check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
                    check_type(argname="argument instance_state", value=instance_state, expected_type=type_hints["instance_state"])
                    check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                    check_type(argname="argument launch_time", value=launch_time, expected_type=type_hints["launch_time"])
                    check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
                    check_type(argname="argument outpost_arn", value=outpost_arn, expected_type=type_hints["outpost_arn"])
                    check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
                    check_type(argname="argument product_codes", value=product_codes, expected_type=type_hints["product_codes"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if availability_zone is not None:
                    self._values["availability_zone"] = availability_zone
                if iam_instance_profile is not None:
                    self._values["iam_instance_profile"] = iam_instance_profile
                if image_description is not None:
                    self._values["image_description"] = image_description
                if image_id is not None:
                    self._values["image_id"] = image_id
                if instance_id is not None:
                    self._values["instance_id"] = instance_id
                if instance_state is not None:
                    self._values["instance_state"] = instance_state
                if instance_type is not None:
                    self._values["instance_type"] = instance_type
                if launch_time is not None:
                    self._values["launch_time"] = launch_time
                if network_interfaces is not None:
                    self._values["network_interfaces"] = network_interfaces
                if outpost_arn is not None:
                    self._values["outpost_arn"] = outpost_arn
                if platform is not None:
                    self._values["platform"] = platform
                if product_codes is not None:
                    self._values["product_codes"] = product_codes
                if tags is not None:
                    self._values["tags"] = tags

            @builtins.property
            def availability_zone(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) availabilityZone property.

                Specify an array of string values to match this event if the actual value of availabilityZone is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("availability_zone")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def iam_instance_profile(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.IamInstanceProfile"]:
                '''(experimental) iamInstanceProfile property.

                Specify an array of string values to match this event if the actual value of iamInstanceProfile is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("iam_instance_profile")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.IamInstanceProfile"], result)

            @builtins.property
            def image_description(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageDescription property.

                Specify an array of string values to match this event if the actual value of imageDescription is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_description")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imageId property.

                Specify an array of string values to match this event if the actual value of imageId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceId property.

                Specify an array of string values to match this event if the actual value of instanceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceState property.

                Specify an array of string values to match this event if the actual value of instanceState is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def instance_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) instanceType property.

                Specify an array of string values to match this event if the actual value of instanceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def launch_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) launchTime property.

                Specify an array of string values to match this event if the actual value of launchTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("launch_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def network_interfaces(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.InstanceDetailsItem"]]:
                '''(experimental) networkInterfaces property.

                Specify an array of string values to match this event if the actual value of networkInterfaces is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interfaces")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.InstanceDetailsItem"]], result)

            @builtins.property
            def outpost_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) outpostArn property.

                Specify an array of string values to match this event if the actual value of outpostArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("outpost_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def platform(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) platform property.

                Specify an array of string values to match this event if the actual value of platform is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("platform")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def product_codes(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.InstanceDetailsItem1"]]:
                '''(experimental) productCodes property.

                Specify an array of string values to match this event if the actual value of productCodes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("product_codes")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.InstanceDetailsItem1"]], result)

            @builtins.property
            def tags(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem"]]:
                '''(experimental) tags property.

                Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstanceDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.InstanceDetailsItem",
            jsii_struct_bases=[],
            name_mapping={
                "ipv6_addresses": "ipv6Addresses",
                "network_interface_id": "networkInterfaceId",
                "private_dns_name": "privateDnsName",
                "private_ip_address": "privateIpAddress",
                "private_ip_addresses": "privateIpAddresses",
                "public_dns_name": "publicDnsName",
                "public_ip": "publicIp",
                "security_groups": "securityGroups",
                "subnet_id": "subnetId",
                "vpc_id": "vpcId",
            },
        )
        class InstanceDetailsItem:
            def __init__(
                self,
                *,
                ipv6_addresses: typing.Optional[typing.Sequence[typing.Any]] = None,
                network_interface_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_dns_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_ip_addresses: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                public_dns_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                public_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
                security_groups: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem1", typing.Dict[builtins.str, typing.Any]]]] = None,
                subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for InstanceDetailsItem.

                :param ipv6_addresses: (experimental) ipv6Addresses property. Specify an array of string values to match this event if the actual value of ipv6Addresses is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param network_interface_id: (experimental) networkInterfaceId property. Specify an array of string values to match this event if the actual value of networkInterfaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_dns_name: (experimental) privateDnsName property. Specify an array of string values to match this event if the actual value of privateDnsName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_address: (experimental) privateIpAddress property. Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_addresses: (experimental) privateIpAddresses property. Specify an array of string values to match this event if the actual value of privateIpAddresses is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param public_dns_name: (experimental) publicDnsName property. Specify an array of string values to match this event if the actual value of publicDnsName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param public_ip: (experimental) publicIp property. Specify an array of string values to match this event if the actual value of publicIp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param security_groups: (experimental) securityGroups property. Specify an array of string values to match this event if the actual value of securityGroups is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param subnet_id: (experimental) subnetId property. Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param vpc_id: (experimental) vpcId property. Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    # ipv6_addresses: Any
                    
                    instance_details_item = guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItem(
                        ipv6_addresses=[ipv6_addresses],
                        network_interface_id=["networkInterfaceId"],
                        private_dns_name=["privateDnsName"],
                        private_ip_address=["privateIpAddress"],
                        private_ip_addresses=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem(
                            private_dns_name=["privateDnsName"],
                            private_ip_address=["privateIpAddress"]
                        )],
                        public_dns_name=["publicDnsName"],
                        public_ip=["publicIp"],
                        security_groups=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem1(
                            group_id=["groupId"],
                            group_name=["groupName"]
                        )],
                        subnet_id=["subnetId"],
                        vpc_id=["vpcId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__047077e2ce9c98e6e9f13d7068c7731f8f39012c7ff88a99d7c011a0d3a907b1)
                    check_type(argname="argument ipv6_addresses", value=ipv6_addresses, expected_type=type_hints["ipv6_addresses"])
                    check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
                    check_type(argname="argument private_dns_name", value=private_dns_name, expected_type=type_hints["private_dns_name"])
                    check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
                    check_type(argname="argument private_ip_addresses", value=private_ip_addresses, expected_type=type_hints["private_ip_addresses"])
                    check_type(argname="argument public_dns_name", value=public_dns_name, expected_type=type_hints["public_dns_name"])
                    check_type(argname="argument public_ip", value=public_ip, expected_type=type_hints["public_ip"])
                    check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                    check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                    check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if ipv6_addresses is not None:
                    self._values["ipv6_addresses"] = ipv6_addresses
                if network_interface_id is not None:
                    self._values["network_interface_id"] = network_interface_id
                if private_dns_name is not None:
                    self._values["private_dns_name"] = private_dns_name
                if private_ip_address is not None:
                    self._values["private_ip_address"] = private_ip_address
                if private_ip_addresses is not None:
                    self._values["private_ip_addresses"] = private_ip_addresses
                if public_dns_name is not None:
                    self._values["public_dns_name"] = public_dns_name
                if public_ip is not None:
                    self._values["public_ip"] = public_ip
                if security_groups is not None:
                    self._values["security_groups"] = security_groups
                if subnet_id is not None:
                    self._values["subnet_id"] = subnet_id
                if vpc_id is not None:
                    self._values["vpc_id"] = vpc_id

            @builtins.property
            def ipv6_addresses(self) -> typing.Optional[typing.List[typing.Any]]:
                '''(experimental) ipv6Addresses property.

                Specify an array of string values to match this event if the actual value of ipv6Addresses is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ipv6_addresses")
                return typing.cast(typing.Optional[typing.List[typing.Any]], result)

            @builtins.property
            def network_interface_id(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) networkInterfaceId property.

                Specify an array of string values to match this event if the actual value of networkInterfaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("network_interface_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_dns_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateDnsName property.

                Specify an array of string values to match this event if the actual value of privateDnsName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_dns_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateIpAddress property.

                Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_ip_addresses(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem"]]:
                '''(experimental) privateIpAddresses property.

                Specify an array of string values to match this event if the actual value of privateIpAddresses is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_addresses")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem"]], result)

            @builtins.property
            def public_dns_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) publicDnsName property.

                Specify an array of string values to match this event if the actual value of publicDnsName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("public_dns_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def public_ip(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) publicIp property.

                Specify an array of string values to match this event if the actual value of publicIp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("public_ip")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def security_groups(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem1"]]:
                '''(experimental) securityGroups property.

                Specify an array of string values to match this event if the actual value of securityGroups is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("security_groups")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem1"]], result)

            @builtins.property
            def subnet_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) subnetId property.

                Specify an array of string values to match this event if the actual value of subnetId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("subnet_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def vpc_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) vpcId property.

                Specify an array of string values to match this event if the actual value of vpcId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("vpc_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstanceDetailsItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.InstanceDetailsItem1",
            jsii_struct_bases=[],
            name_mapping={
                "product_code_id": "productCodeId",
                "product_code_type": "productCodeType",
            },
        )
        class InstanceDetailsItem1:
            def __init__(
                self,
                *,
                product_code_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                product_code_type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for InstanceDetailsItem_1.

                :param product_code_id: (experimental) productCodeId property. Specify an array of string values to match this event if the actual value of productCodeId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param product_code_type: (experimental) productCodeType property. Specify an array of string values to match this event if the actual value of productCodeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    instance_details_item1 = guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItem1(
                        product_code_id=["productCodeId"],
                        product_code_type=["productCodeType"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__fc89e298878b8a28b8245311aa07dbeb9dc306e3bc065a4dced2f5b754a13b07)
                    check_type(argname="argument product_code_id", value=product_code_id, expected_type=type_hints["product_code_id"])
                    check_type(argname="argument product_code_type", value=product_code_type, expected_type=type_hints["product_code_type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if product_code_id is not None:
                    self._values["product_code_id"] = product_code_id
                if product_code_type is not None:
                    self._values["product_code_type"] = product_code_type

            @builtins.property
            def product_code_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) productCodeId property.

                Specify an array of string values to match this event if the actual value of productCodeId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("product_code_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def product_code_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) productCodeType property.

                Specify an array of string values to match this event if the actual value of productCodeType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("product_code_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstanceDetailsItem1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem",
            jsii_struct_bases=[],
            name_mapping={
                "private_dns_name": "privateDnsName",
                "private_ip_address": "privateIpAddress",
            },
        )
        class InstanceDetailsItemItem:
            def __init__(
                self,
                *,
                private_dns_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for InstanceDetailsItemItem.

                :param private_dns_name: (experimental) privateDnsName property. Specify an array of string values to match this event if the actual value of privateDnsName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param private_ip_address: (experimental) privateIpAddress property. Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    instance_details_item_item = guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem(
                        private_dns_name=["privateDnsName"],
                        private_ip_address=["privateIpAddress"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f24e67f58384287a948289bb21e6c213d5129c3b16b5815b05dc0050df08e60f)
                    check_type(argname="argument private_dns_name", value=private_dns_name, expected_type=type_hints["private_dns_name"])
                    check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if private_dns_name is not None:
                    self._values["private_dns_name"] = private_dns_name
                if private_ip_address is not None:
                    self._values["private_ip_address"] = private_ip_address

            @builtins.property
            def private_dns_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateDnsName property.

                Specify an array of string values to match this event if the actual value of privateDnsName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_dns_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def private_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privateIpAddress property.

                Specify an array of string values to match this event if the actual value of privateIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("private_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstanceDetailsItemItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem1",
            jsii_struct_bases=[],
            name_mapping={"group_id": "groupId", "group_name": "groupName"},
        )
        class InstanceDetailsItemItem1:
            def __init__(
                self,
                *,
                group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for InstanceDetailsItemItem_1.

                :param group_id: (experimental) groupId property. Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param group_name: (experimental) groupName property. Specify an array of string values to match this event if the actual value of groupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    instance_details_item_item1 = guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem1(
                        group_id=["groupId"],
                        group_name=["groupName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f8891b8187664bb916b21624e6981d9f8081688a59b8d31a75f2660e66591d06)
                    check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
                    check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if group_id is not None:
                    self._values["group_id"] = group_id
                if group_name is not None:
                    self._values["group_name"] = group_name

            @builtins.property
            def group_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupId property.

                Specify an array of string values to match this event if the actual value of groupId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def group_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groupName property.

                Specify an array of string values to match this event if the actual value of groupName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("group_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "InstanceDetailsItemItem1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.KubernetesApiCallAction",
            jsii_struct_bases=[],
            name_mapping={
                "parameters": "parameters",
                "remote_ip_details": "remoteIpDetails",
                "request_uri": "requestUri",
                "source_i_ps": "sourceIPs",
                "status_code": "statusCode",
                "user_agent": "userAgent",
                "verb": "verb",
            },
        )
        class KubernetesApiCallAction:
            def __init__(
                self,
                *,
                parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
                remote_ip_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.RemoteIpDetails2", typing.Dict[builtins.str, typing.Any]]] = None,
                request_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
                source_i_ps: typing.Optional[typing.Sequence[builtins.str]] = None,
                status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                verb: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for KubernetesApiCallAction.

                :param parameters: (experimental) parameters property. Specify an array of string values to match this event if the actual value of parameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_ip_details: (experimental) remoteIpDetails property. Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_uri: (experimental) requestUri property. Specify an array of string values to match this event if the actual value of requestUri is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_i_ps: (experimental) sourceIPs property. Specify an array of string values to match this event if the actual value of sourceIPs is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param status_code: (experimental) statusCode property. Specify an array of string values to match this event if the actual value of statusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param verb: (experimental) verb property. Specify an array of string values to match this event if the actual value of verb is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    kubernetes_api_call_action = guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesApiCallAction(
                        parameters=["parameters"],
                        remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails2(
                            city=guardduty_events.DetectorEvents.GuardDutyFinding.City2(
                                city_name=["cityName"]
                            ),
                            country=guardduty_events.DetectorEvents.GuardDutyFinding.Country2(
                                country_name=["countryName"]
                            ),
                            geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                lat=["lat"],
                                lon=["lon"]
                            ),
                            ip_address_v4=["ipAddressV4"],
                            organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization2(
                                asn=["asn"],
                                asn_org=["asnOrg"],
                                isp=["isp"],
                                org=["org"]
                            )
                        ),
                        request_uri=["requestUri"],
                        source_iPs=["sourceIPs"],
                        status_code=["statusCode"],
                        user_agent=["userAgent"],
                        verb=["verb"]
                    )
                '''
                if isinstance(remote_ip_details, dict):
                    remote_ip_details = DetectorEvents.GuardDutyFinding.RemoteIpDetails2(**remote_ip_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__1d14dd55b9a564106dafc818ddb36588805b63c65748851e113c05417ae2f38f)
                    check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                    check_type(argname="argument remote_ip_details", value=remote_ip_details, expected_type=type_hints["remote_ip_details"])
                    check_type(argname="argument request_uri", value=request_uri, expected_type=type_hints["request_uri"])
                    check_type(argname="argument source_i_ps", value=source_i_ps, expected_type=type_hints["source_i_ps"])
                    check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                    check_type(argname="argument user_agent", value=user_agent, expected_type=type_hints["user_agent"])
                    check_type(argname="argument verb", value=verb, expected_type=type_hints["verb"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if parameters is not None:
                    self._values["parameters"] = parameters
                if remote_ip_details is not None:
                    self._values["remote_ip_details"] = remote_ip_details
                if request_uri is not None:
                    self._values["request_uri"] = request_uri
                if source_i_ps is not None:
                    self._values["source_i_ps"] = source_i_ps
                if status_code is not None:
                    self._values["status_code"] = status_code
                if user_agent is not None:
                    self._values["user_agent"] = user_agent
                if verb is not None:
                    self._values["verb"] = verb

            @builtins.property
            def parameters(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) parameters property.

                Specify an array of string values to match this event if the actual value of parameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("parameters")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def remote_ip_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails2"]:
                '''(experimental) remoteIpDetails property.

                Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_ip_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails2"], result)

            @builtins.property
            def request_uri(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requestUri property.

                Specify an array of string values to match this event if the actual value of requestUri is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_uri")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def source_i_ps(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceIPs property.

                Specify an array of string values to match this event if the actual value of sourceIPs is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_i_ps")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def status_code(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) statusCode property.

                Specify an array of string values to match this event if the actual value of statusCode is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("status_code")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_agent(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userAgent property.

                Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_agent")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def verb(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) verb property.

                Specify an array of string values to match this event if the actual value of verb is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("verb")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "KubernetesApiCallAction(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.KubernetesDetails",
            jsii_struct_bases=[],
            name_mapping={
                "kubernetes_user_details": "kubernetesUserDetails",
                "kubernetes_workload_details": "kubernetesWorkloadDetails",
            },
        )
        class KubernetesDetails:
            def __init__(
                self,
                *,
                kubernetes_user_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.KubernetesUserDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                kubernetes_workload_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetails", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for KubernetesDetails.

                :param kubernetes_user_details: (experimental) kubernetesUserDetails property. Specify an array of string values to match this event if the actual value of kubernetesUserDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param kubernetes_workload_details: (experimental) kubernetesWorkloadDetails property. Specify an array of string values to match this event if the actual value of kubernetesWorkloadDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    kubernetes_details = guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesDetails(
                        kubernetes_user_details=guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesUserDetails(
                            groups=["groups"],
                            uid=["uid"],
                            username=["username"]
                        ),
                        kubernetes_workload_details=guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetails(
                            containers=[guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetailsItem(
                                image=["image"],
                                image_prefix=["imagePrefix"],
                                name=["name"],
                                security_context=guardduty_events.DetectorEvents.GuardDutyFinding.SecurityContext(
                                    privileged=["privileged"]
                                )
                            )],
                            name=["name"],
                            namespace=["namespace"],
                            type=["type"],
                            uid=["uid"]
                        )
                    )
                '''
                if isinstance(kubernetes_user_details, dict):
                    kubernetes_user_details = DetectorEvents.GuardDutyFinding.KubernetesUserDetails(**kubernetes_user_details)
                if isinstance(kubernetes_workload_details, dict):
                    kubernetes_workload_details = DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetails(**kubernetes_workload_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__409cae5bbca7b6cb6cabc224fe780d4d83f5dd25df9c910a05be260c3be53774)
                    check_type(argname="argument kubernetes_user_details", value=kubernetes_user_details, expected_type=type_hints["kubernetes_user_details"])
                    check_type(argname="argument kubernetes_workload_details", value=kubernetes_workload_details, expected_type=type_hints["kubernetes_workload_details"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if kubernetes_user_details is not None:
                    self._values["kubernetes_user_details"] = kubernetes_user_details
                if kubernetes_workload_details is not None:
                    self._values["kubernetes_workload_details"] = kubernetes_workload_details

            @builtins.property
            def kubernetes_user_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.KubernetesUserDetails"]:
                '''(experimental) kubernetesUserDetails property.

                Specify an array of string values to match this event if the actual value of kubernetesUserDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("kubernetes_user_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.KubernetesUserDetails"], result)

            @builtins.property
            def kubernetes_workload_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetails"]:
                '''(experimental) kubernetesWorkloadDetails property.

                Specify an array of string values to match this event if the actual value of kubernetesWorkloadDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("kubernetes_workload_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetails"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "KubernetesDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.KubernetesUserDetails",
            jsii_struct_bases=[],
            name_mapping={"groups": "groups", "uid": "uid", "username": "username"},
        )
        class KubernetesUserDetails:
            def __init__(
                self,
                *,
                groups: typing.Optional[typing.Sequence[builtins.str]] = None,
                uid: typing.Optional[typing.Sequence[builtins.str]] = None,
                username: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for KubernetesUserDetails.

                :param groups: (experimental) groups property. Specify an array of string values to match this event if the actual value of groups is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param uid: (experimental) uid property. Specify an array of string values to match this event if the actual value of uid is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param username: (experimental) username property. Specify an array of string values to match this event if the actual value of username is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    kubernetes_user_details = guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesUserDetails(
                        groups=["groups"],
                        uid=["uid"],
                        username=["username"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8937b582f66237c4ec5ea0ab48321159c15a52217d24c1a809f76720bba14db0)
                    check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
                    check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
                    check_type(argname="argument username", value=username, expected_type=type_hints["username"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if groups is not None:
                    self._values["groups"] = groups
                if uid is not None:
                    self._values["uid"] = uid
                if username is not None:
                    self._values["username"] = username

            @builtins.property
            def groups(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) groups property.

                Specify an array of string values to match this event if the actual value of groups is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("groups")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def uid(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) uid property.

                Specify an array of string values to match this event if the actual value of uid is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("uid")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def username(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) username property.

                Specify an array of string values to match this event if the actual value of username is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("username")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "KubernetesUserDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetails",
            jsii_struct_bases=[],
            name_mapping={
                "containers": "containers",
                "name": "name",
                "namespace": "namespace",
                "type": "type",
                "uid": "uid",
            },
        )
        class KubernetesWorkloadDetails:
            def __init__(
                self,
                *,
                containers: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetailsItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                namespace: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
                uid: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for KubernetesWorkloadDetails.

                :param containers: (experimental) containers property. Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param namespace: (experimental) namespace property. Specify an array of string values to match this event if the actual value of namespace is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param uid: (experimental) uid property. Specify an array of string values to match this event if the actual value of uid is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    kubernetes_workload_details = guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetails(
                        containers=[guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetailsItem(
                            image=["image"],
                            image_prefix=["imagePrefix"],
                            name=["name"],
                            security_context=guardduty_events.DetectorEvents.GuardDutyFinding.SecurityContext(
                                privileged=["privileged"]
                            )
                        )],
                        name=["name"],
                        namespace=["namespace"],
                        type=["type"],
                        uid=["uid"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a098779f496e4b53815f8c47bf0b8b2b8fa5cbbbc341874c66723759702dec4a)
                    check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                    check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if containers is not None:
                    self._values["containers"] = containers
                if name is not None:
                    self._values["name"] = name
                if namespace is not None:
                    self._values["namespace"] = namespace
                if type is not None:
                    self._values["type"] = type
                if uid is not None:
                    self._values["uid"] = uid

            @builtins.property
            def containers(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetailsItem"]]:
                '''(experimental) containers property.

                Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("containers")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetailsItem"]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def namespace(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) namespace property.

                Specify an array of string values to match this event if the actual value of namespace is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("namespace")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def uid(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) uid property.

                Specify an array of string values to match this event if the actual value of uid is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("uid")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "KubernetesWorkloadDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetailsItem",
            jsii_struct_bases=[],
            name_mapping={
                "image": "image",
                "image_prefix": "imagePrefix",
                "name": "name",
                "security_context": "securityContext",
            },
        )
        class KubernetesWorkloadDetailsItem:
            def __init__(
                self,
                *,
                image: typing.Optional[typing.Sequence[builtins.str]] = None,
                image_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                security_context: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.SecurityContext", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for KubernetesWorkloadDetailsItem.

                :param image: (experimental) image property. Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param image_prefix: (experimental) imagePrefix property. Specify an array of string values to match this event if the actual value of imagePrefix is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param security_context: (experimental) securityContext property. Specify an array of string values to match this event if the actual value of securityContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    kubernetes_workload_details_item = guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetailsItem(
                        image=["image"],
                        image_prefix=["imagePrefix"],
                        name=["name"],
                        security_context=guardduty_events.DetectorEvents.GuardDutyFinding.SecurityContext(
                            privileged=["privileged"]
                        )
                    )
                '''
                if isinstance(security_context, dict):
                    security_context = DetectorEvents.GuardDutyFinding.SecurityContext(**security_context)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__90fe6f2400a267e1531dddeba1c4c7470f5eea0df62f81666c03577cca335f4c)
                    check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                    check_type(argname="argument image_prefix", value=image_prefix, expected_type=type_hints["image_prefix"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument security_context", value=security_context, expected_type=type_hints["security_context"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if image is not None:
                    self._values["image"] = image
                if image_prefix is not None:
                    self._values["image_prefix"] = image_prefix
                if name is not None:
                    self._values["name"] = name
                if security_context is not None:
                    self._values["security_context"] = security_context

            @builtins.property
            def image(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image property.

                Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def image_prefix(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) imagePrefix property.

                Specify an array of string values to match this event if the actual value of imagePrefix is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image_prefix")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def security_context(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.SecurityContext"]:
                '''(experimental) securityContext property.

                Specify an array of string values to match this event if the actual value of securityContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("security_context")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.SecurityContext"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "KubernetesWorkloadDetailsItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.LocalIpDetails",
            jsii_struct_bases=[],
            name_mapping={"ip_address_v4": "ipAddressV4"},
        )
        class LocalIpDetails:
            def __init__(
                self,
                *,
                ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LocalIpDetails.

                :param ip_address_v4: (experimental) ipAddressV4 property. Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    local_ip_details = guardduty_events.DetectorEvents.GuardDutyFinding.LocalIpDetails(
                        ip_address_v4=["ipAddressV4"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__dbb378356f2c43b68a8a1d29ebfb917d3768101efe33565e05a8cfe5c3c8be9a)
                    check_type(argname="argument ip_address_v4", value=ip_address_v4, expected_type=type_hints["ip_address_v4"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if ip_address_v4 is not None:
                    self._values["ip_address_v4"] = ip_address_v4

            @builtins.property
            def ip_address_v4(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipAddressV4 property.

                Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ip_address_v4")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LocalIpDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.LocalIpDetails1",
            jsii_struct_bases=[],
            name_mapping={"ip_address_v4": "ipAddressV4"},
        )
        class LocalIpDetails1:
            def __init__(
                self,
                *,
                ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LocalIpDetails_1.

                :param ip_address_v4: (experimental) ipAddressV4 property. Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    local_ip_details1 = guardduty_events.DetectorEvents.GuardDutyFinding.LocalIpDetails1(
                        ip_address_v4=["ipAddressV4"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a7d2ab04ea7b1a816e02a755b76704f186426582528331f0f4586216b6e40f37)
                    check_type(argname="argument ip_address_v4", value=ip_address_v4, expected_type=type_hints["ip_address_v4"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if ip_address_v4 is not None:
                    self._values["ip_address_v4"] = ip_address_v4

            @builtins.property
            def ip_address_v4(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipAddressV4 property.

                Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ip_address_v4")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LocalIpDetails1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.LocalPortDetails",
            jsii_struct_bases=[],
            name_mapping={"port": "port", "port_name": "portName"},
        )
        class LocalPortDetails:
            def __init__(
                self,
                *,
                port: typing.Optional[typing.Sequence[builtins.str]] = None,
                port_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LocalPortDetails.

                :param port: (experimental) port property. Specify an array of string values to match this event if the actual value of port is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param port_name: (experimental) portName property. Specify an array of string values to match this event if the actual value of portName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    local_port_details = guardduty_events.DetectorEvents.GuardDutyFinding.LocalPortDetails(
                        port=["port"],
                        port_name=["portName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4abef2d8ccfb8d34439cc503f6fc9bbebba154f6e41556c2be8f000bb9858e1e)
                    check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                    check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if port is not None:
                    self._values["port"] = port
                if port_name is not None:
                    self._values["port_name"] = port_name

            @builtins.property
            def port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) port property.

                Specify an array of string values to match this event if the actual value of port is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def port_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) portName property.

                Specify an array of string values to match this event if the actual value of portName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("port_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LocalPortDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.LocalPortDetails1",
            jsii_struct_bases=[],
            name_mapping={"port": "port", "port_name": "portName"},
        )
        class LocalPortDetails1:
            def __init__(
                self,
                *,
                port: typing.Optional[typing.Sequence[builtins.str]] = None,
                port_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for LocalPortDetails_1.

                :param port: (experimental) port property. Specify an array of string values to match this event if the actual value of port is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param port_name: (experimental) portName property. Specify an array of string values to match this event if the actual value of portName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    local_port_details1 = guardduty_events.DetectorEvents.GuardDutyFinding.LocalPortDetails1(
                        port=["port"],
                        port_name=["portName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__e8cdd652f596c32bf8369dc912536d71bc717904fd75e86f9d44430f0d36709d)
                    check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                    check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if port is not None:
                    self._values["port"] = port
                if port_name is not None:
                    self._values["port_name"] = port_name

            @builtins.property
            def port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) port property.

                Specify an array of string values to match this event if the actual value of port is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def port_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) portName property.

                Specify an array of string values to match this event if the actual value of portName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("port_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "LocalPortDetails1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.NetworkConnectionAction",
            jsii_struct_bases=[],
            name_mapping={
                "blocked": "blocked",
                "connection_direction": "connectionDirection",
                "local_ip_details": "localIpDetails",
                "local_port_details": "localPortDetails",
                "protocol": "protocol",
                "remote_ip_details": "remoteIpDetails",
                "remote_port_details": "remotePortDetails",
            },
        )
        class NetworkConnectionAction:
            def __init__(
                self,
                *,
                blocked: typing.Optional[typing.Sequence[builtins.str]] = None,
                connection_direction: typing.Optional[typing.Sequence[builtins.str]] = None,
                local_ip_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.LocalIpDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                local_port_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.LocalPortDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
                remote_ip_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.RemoteIpDetails3", typing.Dict[builtins.str, typing.Any]]] = None,
                remote_port_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.RemotePortDetails", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for NetworkConnectionAction.

                :param blocked: (experimental) blocked property. Specify an array of string values to match this event if the actual value of blocked is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param connection_direction: (experimental) connectionDirection property. Specify an array of string values to match this event if the actual value of connectionDirection is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_ip_details: (experimental) localIpDetails property. Specify an array of string values to match this event if the actual value of localIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_port_details: (experimental) localPortDetails property. Specify an array of string values to match this event if the actual value of localPortDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param protocol: (experimental) protocol property. Specify an array of string values to match this event if the actual value of protocol is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_ip_details: (experimental) remoteIpDetails property. Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_port_details: (experimental) remotePortDetails property. Specify an array of string values to match this event if the actual value of remotePortDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    network_connection_action = guardduty_events.DetectorEvents.GuardDutyFinding.NetworkConnectionAction(
                        blocked=["blocked"],
                        connection_direction=["connectionDirection"],
                        local_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalIpDetails(
                            ip_address_v4=["ipAddressV4"]
                        ),
                        local_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalPortDetails(
                            port=["port"],
                            port_name=["portName"]
                        ),
                        protocol=["protocol"],
                        remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails3(
                            city=guardduty_events.DetectorEvents.GuardDutyFinding.City3(
                                city_name=["cityName"]
                            ),
                            country=guardduty_events.DetectorEvents.GuardDutyFinding.Country3(
                                country_name=["countryName"]
                            ),
                            geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                lat=["lat"],
                                lon=["lon"]
                            ),
                            ip_address_v4=["ipAddressV4"],
                            organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization3(
                                asn=["asn"],
                                asn_org=["asnOrg"],
                                isp=["isp"],
                                org=["org"]
                            )
                        ),
                        remote_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemotePortDetails(
                            port=["port"],
                            port_name=["portName"]
                        )
                    )
                '''
                if isinstance(local_ip_details, dict):
                    local_ip_details = DetectorEvents.GuardDutyFinding.LocalIpDetails(**local_ip_details)
                if isinstance(local_port_details, dict):
                    local_port_details = DetectorEvents.GuardDutyFinding.LocalPortDetails(**local_port_details)
                if isinstance(remote_ip_details, dict):
                    remote_ip_details = DetectorEvents.GuardDutyFinding.RemoteIpDetails3(**remote_ip_details)
                if isinstance(remote_port_details, dict):
                    remote_port_details = DetectorEvents.GuardDutyFinding.RemotePortDetails(**remote_port_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__625d2b273312166fdbc39412944782c1691d747e717ed3f372ee62c4f61cf710)
                    check_type(argname="argument blocked", value=blocked, expected_type=type_hints["blocked"])
                    check_type(argname="argument connection_direction", value=connection_direction, expected_type=type_hints["connection_direction"])
                    check_type(argname="argument local_ip_details", value=local_ip_details, expected_type=type_hints["local_ip_details"])
                    check_type(argname="argument local_port_details", value=local_port_details, expected_type=type_hints["local_port_details"])
                    check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                    check_type(argname="argument remote_ip_details", value=remote_ip_details, expected_type=type_hints["remote_ip_details"])
                    check_type(argname="argument remote_port_details", value=remote_port_details, expected_type=type_hints["remote_port_details"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if blocked is not None:
                    self._values["blocked"] = blocked
                if connection_direction is not None:
                    self._values["connection_direction"] = connection_direction
                if local_ip_details is not None:
                    self._values["local_ip_details"] = local_ip_details
                if local_port_details is not None:
                    self._values["local_port_details"] = local_port_details
                if protocol is not None:
                    self._values["protocol"] = protocol
                if remote_ip_details is not None:
                    self._values["remote_ip_details"] = remote_ip_details
                if remote_port_details is not None:
                    self._values["remote_port_details"] = remote_port_details

            @builtins.property
            def blocked(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) blocked property.

                Specify an array of string values to match this event if the actual value of blocked is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("blocked")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def connection_direction(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) connectionDirection property.

                Specify an array of string values to match this event if the actual value of connectionDirection is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("connection_direction")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def local_ip_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.LocalIpDetails"]:
                '''(experimental) localIpDetails property.

                Specify an array of string values to match this event if the actual value of localIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_ip_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.LocalIpDetails"], result)

            @builtins.property
            def local_port_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.LocalPortDetails"]:
                '''(experimental) localPortDetails property.

                Specify an array of string values to match this event if the actual value of localPortDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_port_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.LocalPortDetails"], result)

            @builtins.property
            def protocol(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) protocol property.

                Specify an array of string values to match this event if the actual value of protocol is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("protocol")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def remote_ip_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails3"]:
                '''(experimental) remoteIpDetails property.

                Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_ip_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails3"], result)

            @builtins.property
            def remote_port_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.RemotePortDetails"]:
                '''(experimental) remotePortDetails property.

                Specify an array of string values to match this event if the actual value of remotePortDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_port_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.RemotePortDetails"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NetworkConnectionAction(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.NewPolicy",
            jsii_struct_bases=[],
            name_mapping={
                "allow_users_to_change_password": "allowUsersToChangePassword",
                "hard_expiry": "hardExpiry",
                "max_password_age": "maxPasswordAge",
                "minimum_password_length": "minimumPasswordLength",
                "password_reuse_prevention": "passwordReusePrevention",
                "require_lowercase_characters": "requireLowercaseCharacters",
                "require_numbers": "requireNumbers",
                "require_symbols": "requireSymbols",
                "require_uppercase_characters": "requireUppercaseCharacters",
            },
        )
        class NewPolicy:
            def __init__(
                self,
                *,
                allow_users_to_change_password: typing.Optional[typing.Sequence[builtins.str]] = None,
                hard_expiry: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_password_age: typing.Optional[typing.Sequence[builtins.str]] = None,
                minimum_password_length: typing.Optional[typing.Sequence[builtins.str]] = None,
                password_reuse_prevention: typing.Optional[typing.Sequence[builtins.str]] = None,
                require_lowercase_characters: typing.Optional[typing.Sequence[builtins.str]] = None,
                require_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
                require_symbols: typing.Optional[typing.Sequence[builtins.str]] = None,
                require_uppercase_characters: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for NewPolicy.

                :param allow_users_to_change_password: (experimental) allowUsersToChangePassword property. Specify an array of string values to match this event if the actual value of allowUsersToChangePassword is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param hard_expiry: (experimental) hardExpiry property. Specify an array of string values to match this event if the actual value of hardExpiry is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_password_age: (experimental) maxPasswordAge property. Specify an array of string values to match this event if the actual value of maxPasswordAge is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param minimum_password_length: (experimental) minimumPasswordLength property. Specify an array of string values to match this event if the actual value of minimumPasswordLength is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param password_reuse_prevention: (experimental) passwordReusePrevention property. Specify an array of string values to match this event if the actual value of passwordReusePrevention is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param require_lowercase_characters: (experimental) requireLowercaseCharacters property. Specify an array of string values to match this event if the actual value of requireLowercaseCharacters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param require_numbers: (experimental) requireNumbers property. Specify an array of string values to match this event if the actual value of requireNumbers is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param require_symbols: (experimental) requireSymbols property. Specify an array of string values to match this event if the actual value of requireSymbols is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param require_uppercase_characters: (experimental) requireUppercaseCharacters property. Specify an array of string values to match this event if the actual value of requireUppercaseCharacters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    new_policy = guardduty_events.DetectorEvents.GuardDutyFinding.NewPolicy(
                        allow_users_to_change_password=["allowUsersToChangePassword"],
                        hard_expiry=["hardExpiry"],
                        max_password_age=["maxPasswordAge"],
                        minimum_password_length=["minimumPasswordLength"],
                        password_reuse_prevention=["passwordReusePrevention"],
                        require_lowercase_characters=["requireLowercaseCharacters"],
                        require_numbers=["requireNumbers"],
                        require_symbols=["requireSymbols"],
                        require_uppercase_characters=["requireUppercaseCharacters"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__eefa27d7e1fc67feabdc0317ec400bda434620acd3d0e03be7fa507d98397f65)
                    check_type(argname="argument allow_users_to_change_password", value=allow_users_to_change_password, expected_type=type_hints["allow_users_to_change_password"])
                    check_type(argname="argument hard_expiry", value=hard_expiry, expected_type=type_hints["hard_expiry"])
                    check_type(argname="argument max_password_age", value=max_password_age, expected_type=type_hints["max_password_age"])
                    check_type(argname="argument minimum_password_length", value=minimum_password_length, expected_type=type_hints["minimum_password_length"])
                    check_type(argname="argument password_reuse_prevention", value=password_reuse_prevention, expected_type=type_hints["password_reuse_prevention"])
                    check_type(argname="argument require_lowercase_characters", value=require_lowercase_characters, expected_type=type_hints["require_lowercase_characters"])
                    check_type(argname="argument require_numbers", value=require_numbers, expected_type=type_hints["require_numbers"])
                    check_type(argname="argument require_symbols", value=require_symbols, expected_type=type_hints["require_symbols"])
                    check_type(argname="argument require_uppercase_characters", value=require_uppercase_characters, expected_type=type_hints["require_uppercase_characters"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if allow_users_to_change_password is not None:
                    self._values["allow_users_to_change_password"] = allow_users_to_change_password
                if hard_expiry is not None:
                    self._values["hard_expiry"] = hard_expiry
                if max_password_age is not None:
                    self._values["max_password_age"] = max_password_age
                if minimum_password_length is not None:
                    self._values["minimum_password_length"] = minimum_password_length
                if password_reuse_prevention is not None:
                    self._values["password_reuse_prevention"] = password_reuse_prevention
                if require_lowercase_characters is not None:
                    self._values["require_lowercase_characters"] = require_lowercase_characters
                if require_numbers is not None:
                    self._values["require_numbers"] = require_numbers
                if require_symbols is not None:
                    self._values["require_symbols"] = require_symbols
                if require_uppercase_characters is not None:
                    self._values["require_uppercase_characters"] = require_uppercase_characters

            @builtins.property
            def allow_users_to_change_password(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) allowUsersToChangePassword property.

                Specify an array of string values to match this event if the actual value of allowUsersToChangePassword is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("allow_users_to_change_password")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def hard_expiry(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) hardExpiry property.

                Specify an array of string values to match this event if the actual value of hardExpiry is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("hard_expiry")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_password_age(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) maxPasswordAge property.

                Specify an array of string values to match this event if the actual value of maxPasswordAge is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_password_age")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def minimum_password_length(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) minimumPasswordLength property.

                Specify an array of string values to match this event if the actual value of minimumPasswordLength is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("minimum_password_length")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def password_reuse_prevention(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) passwordReusePrevention property.

                Specify an array of string values to match this event if the actual value of passwordReusePrevention is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("password_reuse_prevention")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def require_lowercase_characters(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requireLowercaseCharacters property.

                Specify an array of string values to match this event if the actual value of requireLowercaseCharacters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("require_lowercase_characters")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def require_numbers(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requireNumbers property.

                Specify an array of string values to match this event if the actual value of requireNumbers is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("require_numbers")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def require_symbols(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requireSymbols property.

                Specify an array of string values to match this event if the actual value of requireSymbols is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("require_symbols")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def require_uppercase_characters(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requireUppercaseCharacters property.

                Specify an array of string values to match this event if the actual value of requireUppercaseCharacters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("require_uppercase_characters")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NewPolicy(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.OldPolicy",
            jsii_struct_bases=[],
            name_mapping={
                "allow_users_to_change_password": "allowUsersToChangePassword",
                "hard_expiry": "hardExpiry",
                "max_password_age": "maxPasswordAge",
                "minimum_password_length": "minimumPasswordLength",
                "password_reuse_prevention": "passwordReusePrevention",
                "require_lowercase_characters": "requireLowercaseCharacters",
                "require_numbers": "requireNumbers",
                "require_symbols": "requireSymbols",
                "require_uppercase_characters": "requireUppercaseCharacters",
            },
        )
        class OldPolicy:
            def __init__(
                self,
                *,
                allow_users_to_change_password: typing.Optional[typing.Sequence[builtins.str]] = None,
                hard_expiry: typing.Optional[typing.Sequence[builtins.str]] = None,
                max_password_age: typing.Optional[typing.Sequence[builtins.str]] = None,
                minimum_password_length: typing.Optional[typing.Sequence[builtins.str]] = None,
                password_reuse_prevention: typing.Optional[typing.Sequence[builtins.str]] = None,
                require_lowercase_characters: typing.Optional[typing.Sequence[builtins.str]] = None,
                require_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
                require_symbols: typing.Optional[typing.Sequence[builtins.str]] = None,
                require_uppercase_characters: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for OldPolicy.

                :param allow_users_to_change_password: (experimental) allowUsersToChangePassword property. Specify an array of string values to match this event if the actual value of allowUsersToChangePassword is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param hard_expiry: (experimental) hardExpiry property. Specify an array of string values to match this event if the actual value of hardExpiry is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param max_password_age: (experimental) maxPasswordAge property. Specify an array of string values to match this event if the actual value of maxPasswordAge is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param minimum_password_length: (experimental) minimumPasswordLength property. Specify an array of string values to match this event if the actual value of minimumPasswordLength is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param password_reuse_prevention: (experimental) passwordReusePrevention property. Specify an array of string values to match this event if the actual value of passwordReusePrevention is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param require_lowercase_characters: (experimental) requireLowercaseCharacters property. Specify an array of string values to match this event if the actual value of requireLowercaseCharacters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param require_numbers: (experimental) requireNumbers property. Specify an array of string values to match this event if the actual value of requireNumbers is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param require_symbols: (experimental) requireSymbols property. Specify an array of string values to match this event if the actual value of requireSymbols is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param require_uppercase_characters: (experimental) requireUppercaseCharacters property. Specify an array of string values to match this event if the actual value of requireUppercaseCharacters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    old_policy = guardduty_events.DetectorEvents.GuardDutyFinding.OldPolicy(
                        allow_users_to_change_password=["allowUsersToChangePassword"],
                        hard_expiry=["hardExpiry"],
                        max_password_age=["maxPasswordAge"],
                        minimum_password_length=["minimumPasswordLength"],
                        password_reuse_prevention=["passwordReusePrevention"],
                        require_lowercase_characters=["requireLowercaseCharacters"],
                        require_numbers=["requireNumbers"],
                        require_symbols=["requireSymbols"],
                        require_uppercase_characters=["requireUppercaseCharacters"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a4a1c41b6ef82c76a2fa48612d00fe1940b5e12a2d12732562b867ddaa3c1cd5)
                    check_type(argname="argument allow_users_to_change_password", value=allow_users_to_change_password, expected_type=type_hints["allow_users_to_change_password"])
                    check_type(argname="argument hard_expiry", value=hard_expiry, expected_type=type_hints["hard_expiry"])
                    check_type(argname="argument max_password_age", value=max_password_age, expected_type=type_hints["max_password_age"])
                    check_type(argname="argument minimum_password_length", value=minimum_password_length, expected_type=type_hints["minimum_password_length"])
                    check_type(argname="argument password_reuse_prevention", value=password_reuse_prevention, expected_type=type_hints["password_reuse_prevention"])
                    check_type(argname="argument require_lowercase_characters", value=require_lowercase_characters, expected_type=type_hints["require_lowercase_characters"])
                    check_type(argname="argument require_numbers", value=require_numbers, expected_type=type_hints["require_numbers"])
                    check_type(argname="argument require_symbols", value=require_symbols, expected_type=type_hints["require_symbols"])
                    check_type(argname="argument require_uppercase_characters", value=require_uppercase_characters, expected_type=type_hints["require_uppercase_characters"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if allow_users_to_change_password is not None:
                    self._values["allow_users_to_change_password"] = allow_users_to_change_password
                if hard_expiry is not None:
                    self._values["hard_expiry"] = hard_expiry
                if max_password_age is not None:
                    self._values["max_password_age"] = max_password_age
                if minimum_password_length is not None:
                    self._values["minimum_password_length"] = minimum_password_length
                if password_reuse_prevention is not None:
                    self._values["password_reuse_prevention"] = password_reuse_prevention
                if require_lowercase_characters is not None:
                    self._values["require_lowercase_characters"] = require_lowercase_characters
                if require_numbers is not None:
                    self._values["require_numbers"] = require_numbers
                if require_symbols is not None:
                    self._values["require_symbols"] = require_symbols
                if require_uppercase_characters is not None:
                    self._values["require_uppercase_characters"] = require_uppercase_characters

            @builtins.property
            def allow_users_to_change_password(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) allowUsersToChangePassword property.

                Specify an array of string values to match this event if the actual value of allowUsersToChangePassword is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("allow_users_to_change_password")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def hard_expiry(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) hardExpiry property.

                Specify an array of string values to match this event if the actual value of hardExpiry is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("hard_expiry")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def max_password_age(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) maxPasswordAge property.

                Specify an array of string values to match this event if the actual value of maxPasswordAge is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("max_password_age")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def minimum_password_length(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) minimumPasswordLength property.

                Specify an array of string values to match this event if the actual value of minimumPasswordLength is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("minimum_password_length")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def password_reuse_prevention(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) passwordReusePrevention property.

                Specify an array of string values to match this event if the actual value of passwordReusePrevention is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("password_reuse_prevention")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def require_lowercase_characters(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requireLowercaseCharacters property.

                Specify an array of string values to match this event if the actual value of requireLowercaseCharacters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("require_lowercase_characters")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def require_numbers(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requireNumbers property.

                Specify an array of string values to match this event if the actual value of requireNumbers is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("require_numbers")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def require_symbols(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requireSymbols property.

                Specify an array of string values to match this event if the actual value of requireSymbols is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("require_symbols")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def require_uppercase_characters(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requireUppercaseCharacters property.

                Specify an array of string values to match this event if the actual value of requireUppercaseCharacters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("require_uppercase_characters")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "OldPolicy(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Organization",
            jsii_struct_bases=[],
            name_mapping={
                "asn": "asn",
                "asn_org": "asnOrg",
                "isp": "isp",
                "org": "org",
            },
        )
        class Organization:
            def __init__(
                self,
                *,
                asn: typing.Optional[typing.Sequence[builtins.str]] = None,
                asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
                isp: typing.Optional[typing.Sequence[builtins.str]] = None,
                org: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Organization.

                :param asn: (experimental) asn property. Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param asn_org: (experimental) asnOrg property. Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param isp: (experimental) isp property. Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param org: (experimental) org property. Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    organization = guardduty_events.DetectorEvents.GuardDutyFinding.Organization(
                        asn=["asn"],
                        asn_org=["asnOrg"],
                        isp=["isp"],
                        org=["org"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__6ce79719b930174499948ac310659403f89da2bf128714d06bdd5916164e91f4)
                    check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
                    check_type(argname="argument asn_org", value=asn_org, expected_type=type_hints["asn_org"])
                    check_type(argname="argument isp", value=isp, expected_type=type_hints["isp"])
                    check_type(argname="argument org", value=org, expected_type=type_hints["org"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if asn is not None:
                    self._values["asn"] = asn
                if asn_org is not None:
                    self._values["asn_org"] = asn_org
                if isp is not None:
                    self._values["isp"] = isp
                if org is not None:
                    self._values["org"] = org

            @builtins.property
            def asn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asn property.

                Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def asn_org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asnOrg property.

                Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn_org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def isp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) isp property.

                Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("isp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) org property.

                Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Organization(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Organization1",
            jsii_struct_bases=[],
            name_mapping={
                "asn": "asn",
                "asn_org": "asnOrg",
                "isp": "isp",
                "org": "org",
            },
        )
        class Organization1:
            def __init__(
                self,
                *,
                asn: typing.Optional[typing.Sequence[builtins.str]] = None,
                asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
                isp: typing.Optional[typing.Sequence[builtins.str]] = None,
                org: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Organization_1.

                :param asn: (experimental) asn property. Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param asn_org: (experimental) asnOrg property. Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param isp: (experimental) isp property. Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param org: (experimental) org property. Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    organization1 = guardduty_events.DetectorEvents.GuardDutyFinding.Organization1(
                        asn=["asn"],
                        asn_org=["asnOrg"],
                        isp=["isp"],
                        org=["org"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__97245bf7dc97810e50807468d9bad6489379d07d09da600ba8a53ff0c3dedad0)
                    check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
                    check_type(argname="argument asn_org", value=asn_org, expected_type=type_hints["asn_org"])
                    check_type(argname="argument isp", value=isp, expected_type=type_hints["isp"])
                    check_type(argname="argument org", value=org, expected_type=type_hints["org"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if asn is not None:
                    self._values["asn"] = asn
                if asn_org is not None:
                    self._values["asn_org"] = asn_org
                if isp is not None:
                    self._values["isp"] = isp
                if org is not None:
                    self._values["org"] = org

            @builtins.property
            def asn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asn property.

                Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def asn_org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asnOrg property.

                Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn_org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def isp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) isp property.

                Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("isp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) org property.

                Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Organization1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Organization2",
            jsii_struct_bases=[],
            name_mapping={
                "asn": "asn",
                "asn_org": "asnOrg",
                "isp": "isp",
                "org": "org",
            },
        )
        class Organization2:
            def __init__(
                self,
                *,
                asn: typing.Optional[typing.Sequence[builtins.str]] = None,
                asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
                isp: typing.Optional[typing.Sequence[builtins.str]] = None,
                org: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Organization_2.

                :param asn: (experimental) asn property. Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param asn_org: (experimental) asnOrg property. Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param isp: (experimental) isp property. Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param org: (experimental) org property. Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    organization2 = guardduty_events.DetectorEvents.GuardDutyFinding.Organization2(
                        asn=["asn"],
                        asn_org=["asnOrg"],
                        isp=["isp"],
                        org=["org"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__836d25b383f439608c2684e9268431c0490d501ed07137f684ca7d7adfb3f109)
                    check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
                    check_type(argname="argument asn_org", value=asn_org, expected_type=type_hints["asn_org"])
                    check_type(argname="argument isp", value=isp, expected_type=type_hints["isp"])
                    check_type(argname="argument org", value=org, expected_type=type_hints["org"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if asn is not None:
                    self._values["asn"] = asn
                if asn_org is not None:
                    self._values["asn_org"] = asn_org
                if isp is not None:
                    self._values["isp"] = isp
                if org is not None:
                    self._values["org"] = org

            @builtins.property
            def asn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asn property.

                Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def asn_org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asnOrg property.

                Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn_org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def isp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) isp property.

                Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("isp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) org property.

                Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Organization2(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Organization3",
            jsii_struct_bases=[],
            name_mapping={
                "asn": "asn",
                "asn_org": "asnOrg",
                "isp": "isp",
                "org": "org",
            },
        )
        class Organization3:
            def __init__(
                self,
                *,
                asn: typing.Optional[typing.Sequence[builtins.str]] = None,
                asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
                isp: typing.Optional[typing.Sequence[builtins.str]] = None,
                org: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Organization_3.

                :param asn: (experimental) asn property. Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param asn_org: (experimental) asnOrg property. Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param isp: (experimental) isp property. Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param org: (experimental) org property. Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    organization3 = guardduty_events.DetectorEvents.GuardDutyFinding.Organization3(
                        asn=["asn"],
                        asn_org=["asnOrg"],
                        isp=["isp"],
                        org=["org"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__08dcc94ba2b3386031400acf9fa0466f6c6df9f1add8c70e0a54caecceab2678)
                    check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
                    check_type(argname="argument asn_org", value=asn_org, expected_type=type_hints["asn_org"])
                    check_type(argname="argument isp", value=isp, expected_type=type_hints["isp"])
                    check_type(argname="argument org", value=org, expected_type=type_hints["org"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if asn is not None:
                    self._values["asn"] = asn
                if asn_org is not None:
                    self._values["asn_org"] = asn_org
                if isp is not None:
                    self._values["isp"] = isp
                if org is not None:
                    self._values["org"] = org

            @builtins.property
            def asn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asn property.

                Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def asn_org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asnOrg property.

                Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn_org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def isp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) isp property.

                Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("isp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) org property.

                Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Organization3(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Organization4",
            jsii_struct_bases=[],
            name_mapping={
                "asn": "asn",
                "asn_org": "asnOrg",
                "isp": "isp",
                "org": "org",
            },
        )
        class Organization4:
            def __init__(
                self,
                *,
                asn: typing.Optional[typing.Sequence[builtins.str]] = None,
                asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
                isp: typing.Optional[typing.Sequence[builtins.str]] = None,
                org: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Organization_4.

                :param asn: (experimental) asn property. Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param asn_org: (experimental) asnOrg property. Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param isp: (experimental) isp property. Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param org: (experimental) org property. Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    organization4 = guardduty_events.DetectorEvents.GuardDutyFinding.Organization4(
                        asn=["asn"],
                        asn_org=["asnOrg"],
                        isp=["isp"],
                        org=["org"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__724a5a0b038a0630073c88b7192c03aa9bcbf5de3106924e2707ad1003ed8f2f)
                    check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
                    check_type(argname="argument asn_org", value=asn_org, expected_type=type_hints["asn_org"])
                    check_type(argname="argument isp", value=isp, expected_type=type_hints["isp"])
                    check_type(argname="argument org", value=org, expected_type=type_hints["org"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if asn is not None:
                    self._values["asn"] = asn
                if asn_org is not None:
                    self._values["asn_org"] = asn_org
                if isp is not None:
                    self._values["isp"] = isp
                if org is not None:
                    self._values["org"] = org

            @builtins.property
            def asn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asn property.

                Specify an array of string values to match this event if the actual value of asn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def asn_org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) asnOrg property.

                Specify an array of string values to match this event if the actual value of asnOrg is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("asn_org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def isp(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) isp property.

                Specify an array of string values to match this event if the actual value of isp is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("isp")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def org(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) org property.

                Specify an array of string values to match this event if the actual value of org is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("org")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Organization4(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Owner",
            jsii_struct_bases=[],
            name_mapping={"id": "id"},
        )
        class Owner:
            def __init__(
                self,
                *,
                id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Owner.

                :param id: (experimental) id property. Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    owner = guardduty_events.DetectorEvents.GuardDutyFinding.Owner(
                        id=["id"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__efa91b09c2725eef92d0244422b38c5550601262d07b695e8b23a14a44b8b407)
                    check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if id is not None:
                    self._values["id"] = id

            @builtins.property
            def id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) id property.

                Specify an array of string values to match this event if the actual value of id is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Owner(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.PermissionConfiguration",
            jsii_struct_bases=[],
            name_mapping={
                "account_level_permissions": "accountLevelPermissions",
                "bucket_level_permissions": "bucketLevelPermissions",
            },
        )
        class PermissionConfiguration:
            def __init__(
                self,
                *,
                account_level_permissions: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.AccountLevelPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
                bucket_level_permissions: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.BucketLevelPermissions", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for PermissionConfiguration.

                :param account_level_permissions: (experimental) accountLevelPermissions property. Specify an array of string values to match this event if the actual value of accountLevelPermissions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param bucket_level_permissions: (experimental) bucketLevelPermissions property. Specify an array of string values to match this event if the actual value of bucketLevelPermissions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    permission_configuration = guardduty_events.DetectorEvents.GuardDutyFinding.PermissionConfiguration(
                        account_level_permissions=guardduty_events.DetectorEvents.GuardDutyFinding.AccountLevelPermissions(
                            block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                                block_public_acls=["blockPublicAcls"],
                                block_public_policy=["blockPublicPolicy"],
                                ignore_public_acls=["ignorePublicAcls"],
                                restrict_public_buckets=["restrictPublicBuckets"]
                            )
                        ),
                        bucket_level_permissions=guardduty_events.DetectorEvents.GuardDutyFinding.BucketLevelPermissions(
                            access_control_list=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                                allows_public_read_access=["allowsPublicReadAccess"],
                                allows_public_write_access=["allowsPublicWriteAccess"]
                            ),
                            block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                                block_public_acls=["blockPublicAcls"],
                                block_public_policy=["blockPublicPolicy"],
                                ignore_public_acls=["ignorePublicAcls"],
                                restrict_public_buckets=["restrictPublicBuckets"]
                            ),
                            bucket_policy=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                                allows_public_read_access=["allowsPublicReadAccess"],
                                allows_public_write_access=["allowsPublicWriteAccess"]
                            )
                        )
                    )
                '''
                if isinstance(account_level_permissions, dict):
                    account_level_permissions = DetectorEvents.GuardDutyFinding.AccountLevelPermissions(**account_level_permissions)
                if isinstance(bucket_level_permissions, dict):
                    bucket_level_permissions = DetectorEvents.GuardDutyFinding.BucketLevelPermissions(**bucket_level_permissions)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__d0b605bfb16386b0ae75ffed5dab0ac487890d4177e488aa4323faf8e7dfbcf1)
                    check_type(argname="argument account_level_permissions", value=account_level_permissions, expected_type=type_hints["account_level_permissions"])
                    check_type(argname="argument bucket_level_permissions", value=bucket_level_permissions, expected_type=type_hints["bucket_level_permissions"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_level_permissions is not None:
                    self._values["account_level_permissions"] = account_level_permissions
                if bucket_level_permissions is not None:
                    self._values["bucket_level_permissions"] = bucket_level_permissions

            @builtins.property
            def account_level_permissions(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.AccountLevelPermissions"]:
                '''(experimental) accountLevelPermissions property.

                Specify an array of string values to match this event if the actual value of accountLevelPermissions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_level_permissions")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.AccountLevelPermissions"], result)

            @builtins.property
            def bucket_level_permissions(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.BucketLevelPermissions"]:
                '''(experimental) bucketLevelPermissions property.

                Specify an array of string values to match this event if the actual value of bucketLevelPermissions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("bucket_level_permissions")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.BucketLevelPermissions"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "PermissionConfiguration(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.PortProbeAction",
            jsii_struct_bases=[],
            name_mapping={
                "blocked": "blocked",
                "port_probe_details": "portProbeDetails",
            },
        )
        class PortProbeAction:
            def __init__(
                self,
                *,
                blocked: typing.Optional[typing.Sequence[builtins.str]] = None,
                port_probe_details: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.PortProbeActionItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for PortProbeAction.

                :param blocked: (experimental) blocked property. Specify an array of string values to match this event if the actual value of blocked is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param port_probe_details: (experimental) portProbeDetails property. Specify an array of string values to match this event if the actual value of portProbeDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    port_probe_action = guardduty_events.DetectorEvents.GuardDutyFinding.PortProbeAction(
                        blocked=["blocked"],
                        port_probe_details=[guardduty_events.DetectorEvents.GuardDutyFinding.PortProbeActionItem(
                            local_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalIpDetails1(
                                ip_address_v4=["ipAddressV4"]
                            ),
                            local_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalPortDetails1(
                                port=["port"],
                                port_name=["portName"]
                            ),
                            remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails4(
                                city=guardduty_events.DetectorEvents.GuardDutyFinding.City4(
                                    city_name=["cityName"]
                                ),
                                country=guardduty_events.DetectorEvents.GuardDutyFinding.Country4(
                                    country_name=["countryName"]
                                ),
                                geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation1(
                                    lat=["lat"],
                                    lon=["lon"]
                                ),
                                ip_address_v4=["ipAddressV4"],
                                organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization4(
                                    asn=["asn"],
                                    asn_org=["asnOrg"],
                                    isp=["isp"],
                                    org=["org"]
                                )
                            )
                        )]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4c6b04c50dea6e36fb577a16af0c41a89426ed73039d0db2b4794e4569cd02b0)
                    check_type(argname="argument blocked", value=blocked, expected_type=type_hints["blocked"])
                    check_type(argname="argument port_probe_details", value=port_probe_details, expected_type=type_hints["port_probe_details"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if blocked is not None:
                    self._values["blocked"] = blocked
                if port_probe_details is not None:
                    self._values["port_probe_details"] = port_probe_details

            @builtins.property
            def blocked(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) blocked property.

                Specify an array of string values to match this event if the actual value of blocked is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("blocked")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def port_probe_details(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.PortProbeActionItem"]]:
                '''(experimental) portProbeDetails property.

                Specify an array of string values to match this event if the actual value of portProbeDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("port_probe_details")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.PortProbeActionItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "PortProbeAction(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.PortProbeActionItem",
            jsii_struct_bases=[],
            name_mapping={
                "local_ip_details": "localIpDetails",
                "local_port_details": "localPortDetails",
                "remote_ip_details": "remoteIpDetails",
            },
        )
        class PortProbeActionItem:
            def __init__(
                self,
                *,
                local_ip_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.LocalIpDetails1", typing.Dict[builtins.str, typing.Any]]] = None,
                local_port_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.LocalPortDetails1", typing.Dict[builtins.str, typing.Any]]] = None,
                remote_ip_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.RemoteIpDetails4", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for PortProbeActionItem.

                :param local_ip_details: (experimental) localIpDetails property. Specify an array of string values to match this event if the actual value of localIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param local_port_details: (experimental) localPortDetails property. Specify an array of string values to match this event if the actual value of localPortDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param remote_ip_details: (experimental) remoteIpDetails property. Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    port_probe_action_item = guardduty_events.DetectorEvents.GuardDutyFinding.PortProbeActionItem(
                        local_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalIpDetails1(
                            ip_address_v4=["ipAddressV4"]
                        ),
                        local_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalPortDetails1(
                            port=["port"],
                            port_name=["portName"]
                        ),
                        remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails4(
                            city=guardduty_events.DetectorEvents.GuardDutyFinding.City4(
                                city_name=["cityName"]
                            ),
                            country=guardduty_events.DetectorEvents.GuardDutyFinding.Country4(
                                country_name=["countryName"]
                            ),
                            geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation1(
                                lat=["lat"],
                                lon=["lon"]
                            ),
                            ip_address_v4=["ipAddressV4"],
                            organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization4(
                                asn=["asn"],
                                asn_org=["asnOrg"],
                                isp=["isp"],
                                org=["org"]
                            )
                        )
                    )
                '''
                if isinstance(local_ip_details, dict):
                    local_ip_details = DetectorEvents.GuardDutyFinding.LocalIpDetails1(**local_ip_details)
                if isinstance(local_port_details, dict):
                    local_port_details = DetectorEvents.GuardDutyFinding.LocalPortDetails1(**local_port_details)
                if isinstance(remote_ip_details, dict):
                    remote_ip_details = DetectorEvents.GuardDutyFinding.RemoteIpDetails4(**remote_ip_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a164d412cc1dec9080783cac00424fc458df1636a02ba64a7fe69406e2736b71)
                    check_type(argname="argument local_ip_details", value=local_ip_details, expected_type=type_hints["local_ip_details"])
                    check_type(argname="argument local_port_details", value=local_port_details, expected_type=type_hints["local_port_details"])
                    check_type(argname="argument remote_ip_details", value=remote_ip_details, expected_type=type_hints["remote_ip_details"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if local_ip_details is not None:
                    self._values["local_ip_details"] = local_ip_details
                if local_port_details is not None:
                    self._values["local_port_details"] = local_port_details
                if remote_ip_details is not None:
                    self._values["remote_ip_details"] = remote_ip_details

            @builtins.property
            def local_ip_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.LocalIpDetails1"]:
                '''(experimental) localIpDetails property.

                Specify an array of string values to match this event if the actual value of localIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_ip_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.LocalIpDetails1"], result)

            @builtins.property
            def local_port_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.LocalPortDetails1"]:
                '''(experimental) localPortDetails property.

                Specify an array of string values to match this event if the actual value of localPortDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("local_port_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.LocalPortDetails1"], result)

            @builtins.property
            def remote_ip_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails4"]:
                '''(experimental) remoteIpDetails property.

                Specify an array of string values to match this event if the actual value of remoteIpDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("remote_ip_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.RemoteIpDetails4"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "PortProbeActionItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.ProfiledBehavior",
            jsii_struct_bases=[],
            name_mapping={
                "frequent_profiled_ap_is_account_profiling": "frequentProfiledApIsAccountProfiling",
                "frequent_profiled_ap_is_user_identity_profiling": "frequentProfiledApIsUserIdentityProfiling",
                "frequent_profiled_as_ns_account_profiling": "frequentProfiledAsNsAccountProfiling",
                "frequent_profiled_as_ns_bucket_profiling": "frequentProfiledAsNsBucketProfiling",
                "frequent_profiled_as_ns_user_identity_profiling": "frequentProfiledAsNsUserIdentityProfiling",
                "frequent_profiled_buckets_account_profiling": "frequentProfiledBucketsAccountProfiling",
                "frequent_profiled_buckets_user_identity_profiling": "frequentProfiledBucketsUserIdentityProfiling",
                "frequent_profiled_user_agents_account_profiling": "frequentProfiledUserAgentsAccountProfiling",
                "frequent_profiled_user_agents_user_identity_profiling": "frequentProfiledUserAgentsUserIdentityProfiling",
                "frequent_profiled_user_names_account_profiling": "frequentProfiledUserNamesAccountProfiling",
                "frequent_profiled_user_names_bucket_profiling": "frequentProfiledUserNamesBucketProfiling",
                "frequent_profiled_user_types_account_profiling": "frequentProfiledUserTypesAccountProfiling",
                "infrequent_profiled_ap_is_account_profiling": "infrequentProfiledApIsAccountProfiling",
                "infrequent_profiled_ap_is_user_identity_profiling": "infrequentProfiledApIsUserIdentityProfiling",
                "infrequent_profiled_as_ns_account_profiling": "infrequentProfiledAsNsAccountProfiling",
                "infrequent_profiled_as_ns_bucket_profiling": "infrequentProfiledAsNsBucketProfiling",
                "infrequent_profiled_as_ns_user_identity_profiling": "infrequentProfiledAsNsUserIdentityProfiling",
                "infrequent_profiled_buckets_account_profiling": "infrequentProfiledBucketsAccountProfiling",
                "infrequent_profiled_buckets_user_identity_profiling": "infrequentProfiledBucketsUserIdentityProfiling",
                "infrequent_profiled_user_agents_account_profiling": "infrequentProfiledUserAgentsAccountProfiling",
                "infrequent_profiled_user_agents_user_identity_profiling": "infrequentProfiledUserAgentsUserIdentityProfiling",
                "infrequent_profiled_user_names_account_profiling": "infrequentProfiledUserNamesAccountProfiling",
                "infrequent_profiled_user_names_bucket_profiling": "infrequentProfiledUserNamesBucketProfiling",
                "infrequent_profiled_user_types_account_profiling": "infrequentProfiledUserTypesAccountProfiling",
                "number_of_historical_daily_avg_ap_is_bucket_profiling": "numberOfHistoricalDailyAvgApIsBucketProfiling",
                "number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling": "numberOfHistoricalDailyAvgApIsBucketUserIdentityProfiling",
                "number_of_historical_daily_avg_ap_is_user_identity_profiling": "numberOfHistoricalDailyAvgApIsUserIdentityProfiling",
                "number_of_historical_daily_max_ap_is_bucket_profiling": "numberOfHistoricalDailyMaxApIsBucketProfiling",
                "number_of_historical_daily_max_ap_is_bucket_user_identity_profiling": "numberOfHistoricalDailyMaxApIsBucketUserIdentityProfiling",
                "number_of_historical_daily_max_ap_is_user_identity_profiling": "numberOfHistoricalDailyMaxApIsUserIdentityProfiling",
                "rare_profiled_ap_is_account_profiling": "rareProfiledApIsAccountProfiling",
                "rare_profiled_ap_is_user_identity_profiling": "rareProfiledApIsUserIdentityProfiling",
                "rare_profiled_as_ns_account_profiling": "rareProfiledAsNsAccountProfiling",
                "rare_profiled_as_ns_bucket_profiling": "rareProfiledAsNsBucketProfiling",
                "rare_profiled_as_ns_user_identity_profiling": "rareProfiledAsNsUserIdentityProfiling",
                "rare_profiled_buckets_account_profiling": "rareProfiledBucketsAccountProfiling",
                "rare_profiled_buckets_user_identity_profiling": "rareProfiledBucketsUserIdentityProfiling",
                "rare_profiled_user_agents_account_profiling": "rareProfiledUserAgentsAccountProfiling",
                "rare_profiled_user_agents_user_identity_profiling": "rareProfiledUserAgentsUserIdentityProfiling",
                "rare_profiled_user_names_account_profiling": "rareProfiledUserNamesAccountProfiling",
                "rare_profiled_user_names_bucket_profiling": "rareProfiledUserNamesBucketProfiling",
                "rare_profiled_user_types_account_profiling": "rareProfiledUserTypesAccountProfiling",
            },
        )
        class ProfiledBehavior:
            def __init__(
                self,
                *,
                frequent_profiled_ap_is_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_as_ns_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_as_ns_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_as_ns_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_buckets_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_buckets_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_user_agents_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_user_agents_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_user_names_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_user_names_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                frequent_profiled_user_types_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_ap_is_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_as_ns_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_as_ns_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_as_ns_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_buckets_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_buckets_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_user_agents_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_user_agents_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_user_names_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_user_names_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                infrequent_profiled_user_types_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                number_of_historical_daily_avg_ap_is_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                number_of_historical_daily_avg_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                number_of_historical_daily_max_ap_is_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                number_of_historical_daily_max_ap_is_bucket_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                number_of_historical_daily_max_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_ap_is_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_as_ns_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_as_ns_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_as_ns_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_buckets_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_buckets_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_user_agents_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_user_agents_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_user_names_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_user_names_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                rare_profiled_user_types_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ProfiledBehavior.

                :param frequent_profiled_ap_is_account_profiling: (experimental) frequentProfiledAPIsAccountProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledAPIsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_ap_is_user_identity_profiling: (experimental) frequentProfiledAPIsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_as_ns_account_profiling: (experimental) frequentProfiledASNsAccountProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledASNsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_as_ns_bucket_profiling: (experimental) frequentProfiledASNsBucketProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledASNsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_as_ns_user_identity_profiling: (experimental) frequentProfiledASNsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledASNsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_buckets_account_profiling: (experimental) frequentProfiledBucketsAccountProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledBucketsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_buckets_user_identity_profiling: (experimental) frequentProfiledBucketsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledBucketsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_user_agents_account_profiling: (experimental) frequentProfiledUserAgentsAccountProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledUserAgentsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_user_agents_user_identity_profiling: (experimental) frequentProfiledUserAgentsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledUserAgentsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_user_names_account_profiling: (experimental) frequentProfiledUserNamesAccountProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledUserNamesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_user_names_bucket_profiling: (experimental) frequentProfiledUserNamesBucketProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledUserNamesBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param frequent_profiled_user_types_account_profiling: (experimental) frequentProfiledUserTypesAccountProfiling property. Specify an array of string values to match this event if the actual value of frequentProfiledUserTypesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_ap_is_account_profiling: (experimental) infrequentProfiledAPIsAccountProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledAPIsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_ap_is_user_identity_profiling: (experimental) infrequentProfiledAPIsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_as_ns_account_profiling: (experimental) infrequentProfiledASNsAccountProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledASNsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_as_ns_bucket_profiling: (experimental) infrequentProfiledASNsBucketProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledASNsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_as_ns_user_identity_profiling: (experimental) infrequentProfiledASNsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledASNsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_buckets_account_profiling: (experimental) infrequentProfiledBucketsAccountProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledBucketsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_buckets_user_identity_profiling: (experimental) infrequentProfiledBucketsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledBucketsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_user_agents_account_profiling: (experimental) infrequentProfiledUserAgentsAccountProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledUserAgentsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_user_agents_user_identity_profiling: (experimental) infrequentProfiledUserAgentsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledUserAgentsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_user_names_account_profiling: (experimental) infrequentProfiledUserNamesAccountProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledUserNamesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_user_names_bucket_profiling: (experimental) infrequentProfiledUserNamesBucketProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledUserNamesBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param infrequent_profiled_user_types_account_profiling: (experimental) infrequentProfiledUserTypesAccountProfiling property. Specify an array of string values to match this event if the actual value of infrequentProfiledUserTypesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param number_of_historical_daily_avg_ap_is_bucket_profiling: (experimental) numberOfHistoricalDailyAvgAPIsBucketProfiling property. Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyAvgAPIsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling: (experimental) numberOfHistoricalDailyAvgAPIsBucketUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyAvgAPIsBucketUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param number_of_historical_daily_avg_ap_is_user_identity_profiling: (experimental) numberOfHistoricalDailyAvgAPIsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyAvgAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param number_of_historical_daily_max_ap_is_bucket_profiling: (experimental) numberOfHistoricalDailyMaxAPIsBucketProfiling property. Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyMaxAPIsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param number_of_historical_daily_max_ap_is_bucket_user_identity_profiling: (experimental) numberOfHistoricalDailyMaxAPIsBucketUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyMaxAPIsBucketUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param number_of_historical_daily_max_ap_is_user_identity_profiling: (experimental) numberOfHistoricalDailyMaxAPIsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyMaxAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_ap_is_account_profiling: (experimental) rareProfiledAPIsAccountProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledAPIsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_ap_is_user_identity_profiling: (experimental) rareProfiledAPIsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_as_ns_account_profiling: (experimental) rareProfiledASNsAccountProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledASNsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_as_ns_bucket_profiling: (experimental) rareProfiledASNsBucketProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledASNsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_as_ns_user_identity_profiling: (experimental) rareProfiledASNsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledASNsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_buckets_account_profiling: (experimental) rareProfiledBucketsAccountProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledBucketsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_buckets_user_identity_profiling: (experimental) rareProfiledBucketsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledBucketsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_user_agents_account_profiling: (experimental) rareProfiledUserAgentsAccountProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledUserAgentsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_user_agents_user_identity_profiling: (experimental) rareProfiledUserAgentsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledUserAgentsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_user_names_account_profiling: (experimental) rareProfiledUserNamesAccountProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledUserNamesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_user_names_bucket_profiling: (experimental) rareProfiledUserNamesBucketProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledUserNamesBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param rare_profiled_user_types_account_profiling: (experimental) rareProfiledUserTypesAccountProfiling property. Specify an array of string values to match this event if the actual value of rareProfiledUserTypesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    profiled_behavior = guardduty_events.DetectorEvents.GuardDutyFinding.ProfiledBehavior(
                        frequent_profiled_ap_is_account_profiling=["frequentProfiledApIsAccountProfiling"],
                        frequent_profiled_ap_is_user_identity_profiling=["frequentProfiledApIsUserIdentityProfiling"],
                        frequent_profiled_as_ns_account_profiling=["frequentProfiledAsNsAccountProfiling"],
                        frequent_profiled_as_ns_bucket_profiling=["frequentProfiledAsNsBucketProfiling"],
                        frequent_profiled_as_ns_user_identity_profiling=["frequentProfiledAsNsUserIdentityProfiling"],
                        frequent_profiled_buckets_account_profiling=["frequentProfiledBucketsAccountProfiling"],
                        frequent_profiled_buckets_user_identity_profiling=["frequentProfiledBucketsUserIdentityProfiling"],
                        frequent_profiled_user_agents_account_profiling=["frequentProfiledUserAgentsAccountProfiling"],
                        frequent_profiled_user_agents_user_identity_profiling=["frequentProfiledUserAgentsUserIdentityProfiling"],
                        frequent_profiled_user_names_account_profiling=["frequentProfiledUserNamesAccountProfiling"],
                        frequent_profiled_user_names_bucket_profiling=["frequentProfiledUserNamesBucketProfiling"],
                        frequent_profiled_user_types_account_profiling=["frequentProfiledUserTypesAccountProfiling"],
                        infrequent_profiled_ap_is_account_profiling=["infrequentProfiledApIsAccountProfiling"],
                        infrequent_profiled_ap_is_user_identity_profiling=["infrequentProfiledApIsUserIdentityProfiling"],
                        infrequent_profiled_as_ns_account_profiling=["infrequentProfiledAsNsAccountProfiling"],
                        infrequent_profiled_as_ns_bucket_profiling=["infrequentProfiledAsNsBucketProfiling"],
                        infrequent_profiled_as_ns_user_identity_profiling=["infrequentProfiledAsNsUserIdentityProfiling"],
                        infrequent_profiled_buckets_account_profiling=["infrequentProfiledBucketsAccountProfiling"],
                        infrequent_profiled_buckets_user_identity_profiling=["infrequentProfiledBucketsUserIdentityProfiling"],
                        infrequent_profiled_user_agents_account_profiling=["infrequentProfiledUserAgentsAccountProfiling"],
                        infrequent_profiled_user_agents_user_identity_profiling=["infrequentProfiledUserAgentsUserIdentityProfiling"],
                        infrequent_profiled_user_names_account_profiling=["infrequentProfiledUserNamesAccountProfiling"],
                        infrequent_profiled_user_names_bucket_profiling=["infrequentProfiledUserNamesBucketProfiling"],
                        infrequent_profiled_user_types_account_profiling=["infrequentProfiledUserTypesAccountProfiling"],
                        number_of_historical_daily_avg_ap_is_bucket_profiling=["numberOfHistoricalDailyAvgApIsBucketProfiling"],
                        number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling=["numberOfHistoricalDailyAvgApIsBucketUserIdentityProfiling"],
                        number_of_historical_daily_avg_ap_is_user_identity_profiling=["numberOfHistoricalDailyAvgApIsUserIdentityProfiling"],
                        number_of_historical_daily_max_ap_is_bucket_profiling=["numberOfHistoricalDailyMaxApIsBucketProfiling"],
                        number_of_historical_daily_max_ap_is_bucket_user_identity_profiling=["numberOfHistoricalDailyMaxApIsBucketUserIdentityProfiling"],
                        number_of_historical_daily_max_ap_is_user_identity_profiling=["numberOfHistoricalDailyMaxApIsUserIdentityProfiling"],
                        rare_profiled_ap_is_account_profiling=["rareProfiledApIsAccountProfiling"],
                        rare_profiled_ap_is_user_identity_profiling=["rareProfiledApIsUserIdentityProfiling"],
                        rare_profiled_as_ns_account_profiling=["rareProfiledAsNsAccountProfiling"],
                        rare_profiled_as_ns_bucket_profiling=["rareProfiledAsNsBucketProfiling"],
                        rare_profiled_as_ns_user_identity_profiling=["rareProfiledAsNsUserIdentityProfiling"],
                        rare_profiled_buckets_account_profiling=["rareProfiledBucketsAccountProfiling"],
                        rare_profiled_buckets_user_identity_profiling=["rareProfiledBucketsUserIdentityProfiling"],
                        rare_profiled_user_agents_account_profiling=["rareProfiledUserAgentsAccountProfiling"],
                        rare_profiled_user_agents_user_identity_profiling=["rareProfiledUserAgentsUserIdentityProfiling"],
                        rare_profiled_user_names_account_profiling=["rareProfiledUserNamesAccountProfiling"],
                        rare_profiled_user_names_bucket_profiling=["rareProfiledUserNamesBucketProfiling"],
                        rare_profiled_user_types_account_profiling=["rareProfiledUserTypesAccountProfiling"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0f18247c965dfb9a54eed68047876b63935732fa10e624015d568ad935c36de5)
                    check_type(argname="argument frequent_profiled_ap_is_account_profiling", value=frequent_profiled_ap_is_account_profiling, expected_type=type_hints["frequent_profiled_ap_is_account_profiling"])
                    check_type(argname="argument frequent_profiled_ap_is_user_identity_profiling", value=frequent_profiled_ap_is_user_identity_profiling, expected_type=type_hints["frequent_profiled_ap_is_user_identity_profiling"])
                    check_type(argname="argument frequent_profiled_as_ns_account_profiling", value=frequent_profiled_as_ns_account_profiling, expected_type=type_hints["frequent_profiled_as_ns_account_profiling"])
                    check_type(argname="argument frequent_profiled_as_ns_bucket_profiling", value=frequent_profiled_as_ns_bucket_profiling, expected_type=type_hints["frequent_profiled_as_ns_bucket_profiling"])
                    check_type(argname="argument frequent_profiled_as_ns_user_identity_profiling", value=frequent_profiled_as_ns_user_identity_profiling, expected_type=type_hints["frequent_profiled_as_ns_user_identity_profiling"])
                    check_type(argname="argument frequent_profiled_buckets_account_profiling", value=frequent_profiled_buckets_account_profiling, expected_type=type_hints["frequent_profiled_buckets_account_profiling"])
                    check_type(argname="argument frequent_profiled_buckets_user_identity_profiling", value=frequent_profiled_buckets_user_identity_profiling, expected_type=type_hints["frequent_profiled_buckets_user_identity_profiling"])
                    check_type(argname="argument frequent_profiled_user_agents_account_profiling", value=frequent_profiled_user_agents_account_profiling, expected_type=type_hints["frequent_profiled_user_agents_account_profiling"])
                    check_type(argname="argument frequent_profiled_user_agents_user_identity_profiling", value=frequent_profiled_user_agents_user_identity_profiling, expected_type=type_hints["frequent_profiled_user_agents_user_identity_profiling"])
                    check_type(argname="argument frequent_profiled_user_names_account_profiling", value=frequent_profiled_user_names_account_profiling, expected_type=type_hints["frequent_profiled_user_names_account_profiling"])
                    check_type(argname="argument frequent_profiled_user_names_bucket_profiling", value=frequent_profiled_user_names_bucket_profiling, expected_type=type_hints["frequent_profiled_user_names_bucket_profiling"])
                    check_type(argname="argument frequent_profiled_user_types_account_profiling", value=frequent_profiled_user_types_account_profiling, expected_type=type_hints["frequent_profiled_user_types_account_profiling"])
                    check_type(argname="argument infrequent_profiled_ap_is_account_profiling", value=infrequent_profiled_ap_is_account_profiling, expected_type=type_hints["infrequent_profiled_ap_is_account_profiling"])
                    check_type(argname="argument infrequent_profiled_ap_is_user_identity_profiling", value=infrequent_profiled_ap_is_user_identity_profiling, expected_type=type_hints["infrequent_profiled_ap_is_user_identity_profiling"])
                    check_type(argname="argument infrequent_profiled_as_ns_account_profiling", value=infrequent_profiled_as_ns_account_profiling, expected_type=type_hints["infrequent_profiled_as_ns_account_profiling"])
                    check_type(argname="argument infrequent_profiled_as_ns_bucket_profiling", value=infrequent_profiled_as_ns_bucket_profiling, expected_type=type_hints["infrequent_profiled_as_ns_bucket_profiling"])
                    check_type(argname="argument infrequent_profiled_as_ns_user_identity_profiling", value=infrequent_profiled_as_ns_user_identity_profiling, expected_type=type_hints["infrequent_profiled_as_ns_user_identity_profiling"])
                    check_type(argname="argument infrequent_profiled_buckets_account_profiling", value=infrequent_profiled_buckets_account_profiling, expected_type=type_hints["infrequent_profiled_buckets_account_profiling"])
                    check_type(argname="argument infrequent_profiled_buckets_user_identity_profiling", value=infrequent_profiled_buckets_user_identity_profiling, expected_type=type_hints["infrequent_profiled_buckets_user_identity_profiling"])
                    check_type(argname="argument infrequent_profiled_user_agents_account_profiling", value=infrequent_profiled_user_agents_account_profiling, expected_type=type_hints["infrequent_profiled_user_agents_account_profiling"])
                    check_type(argname="argument infrequent_profiled_user_agents_user_identity_profiling", value=infrequent_profiled_user_agents_user_identity_profiling, expected_type=type_hints["infrequent_profiled_user_agents_user_identity_profiling"])
                    check_type(argname="argument infrequent_profiled_user_names_account_profiling", value=infrequent_profiled_user_names_account_profiling, expected_type=type_hints["infrequent_profiled_user_names_account_profiling"])
                    check_type(argname="argument infrequent_profiled_user_names_bucket_profiling", value=infrequent_profiled_user_names_bucket_profiling, expected_type=type_hints["infrequent_profiled_user_names_bucket_profiling"])
                    check_type(argname="argument infrequent_profiled_user_types_account_profiling", value=infrequent_profiled_user_types_account_profiling, expected_type=type_hints["infrequent_profiled_user_types_account_profiling"])
                    check_type(argname="argument number_of_historical_daily_avg_ap_is_bucket_profiling", value=number_of_historical_daily_avg_ap_is_bucket_profiling, expected_type=type_hints["number_of_historical_daily_avg_ap_is_bucket_profiling"])
                    check_type(argname="argument number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling", value=number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling, expected_type=type_hints["number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling"])
                    check_type(argname="argument number_of_historical_daily_avg_ap_is_user_identity_profiling", value=number_of_historical_daily_avg_ap_is_user_identity_profiling, expected_type=type_hints["number_of_historical_daily_avg_ap_is_user_identity_profiling"])
                    check_type(argname="argument number_of_historical_daily_max_ap_is_bucket_profiling", value=number_of_historical_daily_max_ap_is_bucket_profiling, expected_type=type_hints["number_of_historical_daily_max_ap_is_bucket_profiling"])
                    check_type(argname="argument number_of_historical_daily_max_ap_is_bucket_user_identity_profiling", value=number_of_historical_daily_max_ap_is_bucket_user_identity_profiling, expected_type=type_hints["number_of_historical_daily_max_ap_is_bucket_user_identity_profiling"])
                    check_type(argname="argument number_of_historical_daily_max_ap_is_user_identity_profiling", value=number_of_historical_daily_max_ap_is_user_identity_profiling, expected_type=type_hints["number_of_historical_daily_max_ap_is_user_identity_profiling"])
                    check_type(argname="argument rare_profiled_ap_is_account_profiling", value=rare_profiled_ap_is_account_profiling, expected_type=type_hints["rare_profiled_ap_is_account_profiling"])
                    check_type(argname="argument rare_profiled_ap_is_user_identity_profiling", value=rare_profiled_ap_is_user_identity_profiling, expected_type=type_hints["rare_profiled_ap_is_user_identity_profiling"])
                    check_type(argname="argument rare_profiled_as_ns_account_profiling", value=rare_profiled_as_ns_account_profiling, expected_type=type_hints["rare_profiled_as_ns_account_profiling"])
                    check_type(argname="argument rare_profiled_as_ns_bucket_profiling", value=rare_profiled_as_ns_bucket_profiling, expected_type=type_hints["rare_profiled_as_ns_bucket_profiling"])
                    check_type(argname="argument rare_profiled_as_ns_user_identity_profiling", value=rare_profiled_as_ns_user_identity_profiling, expected_type=type_hints["rare_profiled_as_ns_user_identity_profiling"])
                    check_type(argname="argument rare_profiled_buckets_account_profiling", value=rare_profiled_buckets_account_profiling, expected_type=type_hints["rare_profiled_buckets_account_profiling"])
                    check_type(argname="argument rare_profiled_buckets_user_identity_profiling", value=rare_profiled_buckets_user_identity_profiling, expected_type=type_hints["rare_profiled_buckets_user_identity_profiling"])
                    check_type(argname="argument rare_profiled_user_agents_account_profiling", value=rare_profiled_user_agents_account_profiling, expected_type=type_hints["rare_profiled_user_agents_account_profiling"])
                    check_type(argname="argument rare_profiled_user_agents_user_identity_profiling", value=rare_profiled_user_agents_user_identity_profiling, expected_type=type_hints["rare_profiled_user_agents_user_identity_profiling"])
                    check_type(argname="argument rare_profiled_user_names_account_profiling", value=rare_profiled_user_names_account_profiling, expected_type=type_hints["rare_profiled_user_names_account_profiling"])
                    check_type(argname="argument rare_profiled_user_names_bucket_profiling", value=rare_profiled_user_names_bucket_profiling, expected_type=type_hints["rare_profiled_user_names_bucket_profiling"])
                    check_type(argname="argument rare_profiled_user_types_account_profiling", value=rare_profiled_user_types_account_profiling, expected_type=type_hints["rare_profiled_user_types_account_profiling"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if frequent_profiled_ap_is_account_profiling is not None:
                    self._values["frequent_profiled_ap_is_account_profiling"] = frequent_profiled_ap_is_account_profiling
                if frequent_profiled_ap_is_user_identity_profiling is not None:
                    self._values["frequent_profiled_ap_is_user_identity_profiling"] = frequent_profiled_ap_is_user_identity_profiling
                if frequent_profiled_as_ns_account_profiling is not None:
                    self._values["frequent_profiled_as_ns_account_profiling"] = frequent_profiled_as_ns_account_profiling
                if frequent_profiled_as_ns_bucket_profiling is not None:
                    self._values["frequent_profiled_as_ns_bucket_profiling"] = frequent_profiled_as_ns_bucket_profiling
                if frequent_profiled_as_ns_user_identity_profiling is not None:
                    self._values["frequent_profiled_as_ns_user_identity_profiling"] = frequent_profiled_as_ns_user_identity_profiling
                if frequent_profiled_buckets_account_profiling is not None:
                    self._values["frequent_profiled_buckets_account_profiling"] = frequent_profiled_buckets_account_profiling
                if frequent_profiled_buckets_user_identity_profiling is not None:
                    self._values["frequent_profiled_buckets_user_identity_profiling"] = frequent_profiled_buckets_user_identity_profiling
                if frequent_profiled_user_agents_account_profiling is not None:
                    self._values["frequent_profiled_user_agents_account_profiling"] = frequent_profiled_user_agents_account_profiling
                if frequent_profiled_user_agents_user_identity_profiling is not None:
                    self._values["frequent_profiled_user_agents_user_identity_profiling"] = frequent_profiled_user_agents_user_identity_profiling
                if frequent_profiled_user_names_account_profiling is not None:
                    self._values["frequent_profiled_user_names_account_profiling"] = frequent_profiled_user_names_account_profiling
                if frequent_profiled_user_names_bucket_profiling is not None:
                    self._values["frequent_profiled_user_names_bucket_profiling"] = frequent_profiled_user_names_bucket_profiling
                if frequent_profiled_user_types_account_profiling is not None:
                    self._values["frequent_profiled_user_types_account_profiling"] = frequent_profiled_user_types_account_profiling
                if infrequent_profiled_ap_is_account_profiling is not None:
                    self._values["infrequent_profiled_ap_is_account_profiling"] = infrequent_profiled_ap_is_account_profiling
                if infrequent_profiled_ap_is_user_identity_profiling is not None:
                    self._values["infrequent_profiled_ap_is_user_identity_profiling"] = infrequent_profiled_ap_is_user_identity_profiling
                if infrequent_profiled_as_ns_account_profiling is not None:
                    self._values["infrequent_profiled_as_ns_account_profiling"] = infrequent_profiled_as_ns_account_profiling
                if infrequent_profiled_as_ns_bucket_profiling is not None:
                    self._values["infrequent_profiled_as_ns_bucket_profiling"] = infrequent_profiled_as_ns_bucket_profiling
                if infrequent_profiled_as_ns_user_identity_profiling is not None:
                    self._values["infrequent_profiled_as_ns_user_identity_profiling"] = infrequent_profiled_as_ns_user_identity_profiling
                if infrequent_profiled_buckets_account_profiling is not None:
                    self._values["infrequent_profiled_buckets_account_profiling"] = infrequent_profiled_buckets_account_profiling
                if infrequent_profiled_buckets_user_identity_profiling is not None:
                    self._values["infrequent_profiled_buckets_user_identity_profiling"] = infrequent_profiled_buckets_user_identity_profiling
                if infrequent_profiled_user_agents_account_profiling is not None:
                    self._values["infrequent_profiled_user_agents_account_profiling"] = infrequent_profiled_user_agents_account_profiling
                if infrequent_profiled_user_agents_user_identity_profiling is not None:
                    self._values["infrequent_profiled_user_agents_user_identity_profiling"] = infrequent_profiled_user_agents_user_identity_profiling
                if infrequent_profiled_user_names_account_profiling is not None:
                    self._values["infrequent_profiled_user_names_account_profiling"] = infrequent_profiled_user_names_account_profiling
                if infrequent_profiled_user_names_bucket_profiling is not None:
                    self._values["infrequent_profiled_user_names_bucket_profiling"] = infrequent_profiled_user_names_bucket_profiling
                if infrequent_profiled_user_types_account_profiling is not None:
                    self._values["infrequent_profiled_user_types_account_profiling"] = infrequent_profiled_user_types_account_profiling
                if number_of_historical_daily_avg_ap_is_bucket_profiling is not None:
                    self._values["number_of_historical_daily_avg_ap_is_bucket_profiling"] = number_of_historical_daily_avg_ap_is_bucket_profiling
                if number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling is not None:
                    self._values["number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling"] = number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling
                if number_of_historical_daily_avg_ap_is_user_identity_profiling is not None:
                    self._values["number_of_historical_daily_avg_ap_is_user_identity_profiling"] = number_of_historical_daily_avg_ap_is_user_identity_profiling
                if number_of_historical_daily_max_ap_is_bucket_profiling is not None:
                    self._values["number_of_historical_daily_max_ap_is_bucket_profiling"] = number_of_historical_daily_max_ap_is_bucket_profiling
                if number_of_historical_daily_max_ap_is_bucket_user_identity_profiling is not None:
                    self._values["number_of_historical_daily_max_ap_is_bucket_user_identity_profiling"] = number_of_historical_daily_max_ap_is_bucket_user_identity_profiling
                if number_of_historical_daily_max_ap_is_user_identity_profiling is not None:
                    self._values["number_of_historical_daily_max_ap_is_user_identity_profiling"] = number_of_historical_daily_max_ap_is_user_identity_profiling
                if rare_profiled_ap_is_account_profiling is not None:
                    self._values["rare_profiled_ap_is_account_profiling"] = rare_profiled_ap_is_account_profiling
                if rare_profiled_ap_is_user_identity_profiling is not None:
                    self._values["rare_profiled_ap_is_user_identity_profiling"] = rare_profiled_ap_is_user_identity_profiling
                if rare_profiled_as_ns_account_profiling is not None:
                    self._values["rare_profiled_as_ns_account_profiling"] = rare_profiled_as_ns_account_profiling
                if rare_profiled_as_ns_bucket_profiling is not None:
                    self._values["rare_profiled_as_ns_bucket_profiling"] = rare_profiled_as_ns_bucket_profiling
                if rare_profiled_as_ns_user_identity_profiling is not None:
                    self._values["rare_profiled_as_ns_user_identity_profiling"] = rare_profiled_as_ns_user_identity_profiling
                if rare_profiled_buckets_account_profiling is not None:
                    self._values["rare_profiled_buckets_account_profiling"] = rare_profiled_buckets_account_profiling
                if rare_profiled_buckets_user_identity_profiling is not None:
                    self._values["rare_profiled_buckets_user_identity_profiling"] = rare_profiled_buckets_user_identity_profiling
                if rare_profiled_user_agents_account_profiling is not None:
                    self._values["rare_profiled_user_agents_account_profiling"] = rare_profiled_user_agents_account_profiling
                if rare_profiled_user_agents_user_identity_profiling is not None:
                    self._values["rare_profiled_user_agents_user_identity_profiling"] = rare_profiled_user_agents_user_identity_profiling
                if rare_profiled_user_names_account_profiling is not None:
                    self._values["rare_profiled_user_names_account_profiling"] = rare_profiled_user_names_account_profiling
                if rare_profiled_user_names_bucket_profiling is not None:
                    self._values["rare_profiled_user_names_bucket_profiling"] = rare_profiled_user_names_bucket_profiling
                if rare_profiled_user_types_account_profiling is not None:
                    self._values["rare_profiled_user_types_account_profiling"] = rare_profiled_user_types_account_profiling

            @builtins.property
            def frequent_profiled_ap_is_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledAPIsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledAPIsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_ap_is_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_ap_is_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledAPIsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_ap_is_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_as_ns_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledASNsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledASNsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_as_ns_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_as_ns_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledASNsBucketProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledASNsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_as_ns_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_as_ns_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledASNsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledASNsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_as_ns_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_buckets_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledBucketsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledBucketsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_buckets_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_buckets_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledBucketsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledBucketsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_buckets_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_user_agents_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledUserAgentsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledUserAgentsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_user_agents_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_user_agents_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledUserAgentsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledUserAgentsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_user_agents_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_user_names_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledUserNamesAccountProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledUserNamesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_user_names_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_user_names_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledUserNamesBucketProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledUserNamesBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_user_names_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def frequent_profiled_user_types_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) frequentProfiledUserTypesAccountProfiling property.

                Specify an array of string values to match this event if the actual value of frequentProfiledUserTypesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("frequent_profiled_user_types_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_ap_is_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledAPIsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledAPIsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_ap_is_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_ap_is_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledAPIsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_ap_is_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_as_ns_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledASNsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledASNsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_as_ns_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_as_ns_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledASNsBucketProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledASNsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_as_ns_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_as_ns_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledASNsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledASNsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_as_ns_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_buckets_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledBucketsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledBucketsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_buckets_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_buckets_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledBucketsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledBucketsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_buckets_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_user_agents_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledUserAgentsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledUserAgentsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_user_agents_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_user_agents_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledUserAgentsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledUserAgentsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_user_agents_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_user_names_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledUserNamesAccountProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledUserNamesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_user_names_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_user_names_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledUserNamesBucketProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledUserNamesBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_user_names_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def infrequent_profiled_user_types_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) infrequentProfiledUserTypesAccountProfiling property.

                Specify an array of string values to match this event if the actual value of infrequentProfiledUserTypesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("infrequent_profiled_user_types_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def number_of_historical_daily_avg_ap_is_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) numberOfHistoricalDailyAvgAPIsBucketProfiling property.

                Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyAvgAPIsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("number_of_historical_daily_avg_ap_is_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) numberOfHistoricalDailyAvgAPIsBucketUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyAvgAPIsBucketUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def number_of_historical_daily_avg_ap_is_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) numberOfHistoricalDailyAvgAPIsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyAvgAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("number_of_historical_daily_avg_ap_is_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def number_of_historical_daily_max_ap_is_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) numberOfHistoricalDailyMaxAPIsBucketProfiling property.

                Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyMaxAPIsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("number_of_historical_daily_max_ap_is_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def number_of_historical_daily_max_ap_is_bucket_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) numberOfHistoricalDailyMaxAPIsBucketUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyMaxAPIsBucketUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("number_of_historical_daily_max_ap_is_bucket_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def number_of_historical_daily_max_ap_is_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) numberOfHistoricalDailyMaxAPIsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of numberOfHistoricalDailyMaxAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("number_of_historical_daily_max_ap_is_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_ap_is_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledAPIsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledAPIsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_ap_is_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_ap_is_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledAPIsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_ap_is_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_as_ns_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledASNsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledASNsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_as_ns_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_as_ns_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledASNsBucketProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledASNsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_as_ns_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_as_ns_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledASNsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledASNsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_as_ns_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_buckets_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledBucketsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledBucketsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_buckets_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_buckets_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledBucketsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledBucketsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_buckets_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_user_agents_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledUserAgentsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledUserAgentsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_user_agents_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_user_agents_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledUserAgentsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledUserAgentsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_user_agents_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_user_names_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledUserNamesAccountProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledUserNamesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_user_names_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_user_names_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledUserNamesBucketProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledUserNamesBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_user_names_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def rare_profiled_user_types_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) rareProfiledUserTypesAccountProfiling property.

                Specify an array of string values to match this event if the actual value of rareProfiledUserTypesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("rare_profiled_user_types_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ProfiledBehavior(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.PublicAccess",
            jsii_struct_bases=[],
            name_mapping={
                "effective_permission": "effectivePermission",
                "permission_configuration": "permissionConfiguration",
            },
        )
        class PublicAccess:
            def __init__(
                self,
                *,
                effective_permission: typing.Optional[typing.Sequence[builtins.str]] = None,
                permission_configuration: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.PermissionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for PublicAccess.

                :param effective_permission: (experimental) effectivePermission property. Specify an array of string values to match this event if the actual value of effectivePermission is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param permission_configuration: (experimental) permissionConfiguration property. Specify an array of string values to match this event if the actual value of permissionConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    public_access = guardduty_events.DetectorEvents.GuardDutyFinding.PublicAccess(
                        effective_permission=["effectivePermission"],
                        permission_configuration=guardduty_events.DetectorEvents.GuardDutyFinding.PermissionConfiguration(
                            account_level_permissions=guardduty_events.DetectorEvents.GuardDutyFinding.AccountLevelPermissions(
                                block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                                    block_public_acls=["blockPublicAcls"],
                                    block_public_policy=["blockPublicPolicy"],
                                    ignore_public_acls=["ignorePublicAcls"],
                                    restrict_public_buckets=["restrictPublicBuckets"]
                                )
                            ),
                            bucket_level_permissions=guardduty_events.DetectorEvents.GuardDutyFinding.BucketLevelPermissions(
                                access_control_list=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                                    allows_public_read_access=["allowsPublicReadAccess"],
                                    allows_public_write_access=["allowsPublicWriteAccess"]
                                ),
                                block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                                    block_public_acls=["blockPublicAcls"],
                                    block_public_policy=["blockPublicPolicy"],
                                    ignore_public_acls=["ignorePublicAcls"],
                                    restrict_public_buckets=["restrictPublicBuckets"]
                                ),
                                bucket_policy=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                                    allows_public_read_access=["allowsPublicReadAccess"],
                                    allows_public_write_access=["allowsPublicWriteAccess"]
                                )
                            )
                        )
                    )
                '''
                if isinstance(permission_configuration, dict):
                    permission_configuration = DetectorEvents.GuardDutyFinding.PermissionConfiguration(**permission_configuration)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__be019c8462db9519eb1d9f5de31c19055d4ac3088d0091d4bd89a6b9721a42ec)
                    check_type(argname="argument effective_permission", value=effective_permission, expected_type=type_hints["effective_permission"])
                    check_type(argname="argument permission_configuration", value=permission_configuration, expected_type=type_hints["permission_configuration"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if effective_permission is not None:
                    self._values["effective_permission"] = effective_permission
                if permission_configuration is not None:
                    self._values["permission_configuration"] = permission_configuration

            @builtins.property
            def effective_permission(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) effectivePermission property.

                Specify an array of string values to match this event if the actual value of effectivePermission is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("effective_permission")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def permission_configuration(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.PermissionConfiguration"]:
                '''(experimental) permissionConfiguration property.

                Specify an array of string values to match this event if the actual value of permissionConfiguration is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("permission_configuration")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.PermissionConfiguration"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "PublicAccess(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.RemoteAccountDetails",
            jsii_struct_bases=[],
            name_mapping={"account_id": "accountId", "affiliated": "affiliated"},
        )
        class RemoteAccountDetails:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                affiliated: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RemoteAccountDetails.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param affiliated: (experimental) affiliated property. Specify an array of string values to match this event if the actual value of affiliated is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    remote_account_details = guardduty_events.DetectorEvents.GuardDutyFinding.RemoteAccountDetails(
                        account_id=["accountId"],
                        affiliated=["affiliated"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__53fd3cdf671e62c58347d5e709699aa7a0303e91a626bc45313cfc887e4e32a6)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument affiliated", value=affiliated, expected_type=type_hints["affiliated"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if affiliated is not None:
                    self._values["affiliated"] = affiliated

            @builtins.property
            def account_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) accountId property.

                Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("account_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def affiliated(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) affiliated property.

                Specify an array of string values to match this event if the actual value of affiliated is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("affiliated")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RemoteAccountDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.RemoteIpDetails",
            jsii_struct_bases=[],
            name_mapping={
                "city": "city",
                "country": "country",
                "geo_location": "geoLocation",
                "ip_address_v4": "ipAddressV4",
                "organization": "organization",
            },
        )
        class RemoteIpDetails:
            def __init__(
                self,
                *,
                city: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.City", typing.Dict[builtins.str, typing.Any]]] = None,
                country: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Country", typing.Dict[builtins.str, typing.Any]]] = None,
                geo_location: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.GeoLocation", typing.Dict[builtins.str, typing.Any]]] = None,
                ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
                organization: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Organization", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for RemoteIpDetails.

                :param city: (experimental) city property. Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param country: (experimental) country property. Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param geo_location: (experimental) geoLocation property. Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ip_address_v4: (experimental) ipAddressV4 property. Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param organization: (experimental) organization property. Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    remote_ip_details = guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails(
                        city=guardduty_events.DetectorEvents.GuardDutyFinding.City(
                            city_name=["cityName"]
                        ),
                        country=guardduty_events.DetectorEvents.GuardDutyFinding.Country(
                            country_name=["countryName"]
                        ),
                        geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                            lat=["lat"],
                            lon=["lon"]
                        ),
                        ip_address_v4=["ipAddressV4"],
                        organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization(
                            asn=["asn"],
                            asn_org=["asnOrg"],
                            isp=["isp"],
                            org=["org"]
                        )
                    )
                '''
                if isinstance(city, dict):
                    city = DetectorEvents.GuardDutyFinding.City(**city)
                if isinstance(country, dict):
                    country = DetectorEvents.GuardDutyFinding.Country(**country)
                if isinstance(geo_location, dict):
                    geo_location = DetectorEvents.GuardDutyFinding.GeoLocation(**geo_location)
                if isinstance(organization, dict):
                    organization = DetectorEvents.GuardDutyFinding.Organization(**organization)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4914e8c1709d60da2023db68256bfd7362651bc0d5f2d8e094ee9450460333f2)
                    check_type(argname="argument city", value=city, expected_type=type_hints["city"])
                    check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                    check_type(argname="argument geo_location", value=geo_location, expected_type=type_hints["geo_location"])
                    check_type(argname="argument ip_address_v4", value=ip_address_v4, expected_type=type_hints["ip_address_v4"])
                    check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city is not None:
                    self._values["city"] = city
                if country is not None:
                    self._values["country"] = country
                if geo_location is not None:
                    self._values["geo_location"] = geo_location
                if ip_address_v4 is not None:
                    self._values["ip_address_v4"] = ip_address_v4
                if organization is not None:
                    self._values["organization"] = organization

            @builtins.property
            def city(self) -> typing.Optional["DetectorEvents.GuardDutyFinding.City"]:
                '''(experimental) city property.

                Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.City"], result)

            @builtins.property
            def country(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Country"]:
                '''(experimental) country property.

                Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Country"], result)

            @builtins.property
            def geo_location(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation"]:
                '''(experimental) geoLocation property.

                Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("geo_location")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation"], result)

            @builtins.property
            def ip_address_v4(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipAddressV4 property.

                Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ip_address_v4")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def organization(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Organization"]:
                '''(experimental) organization property.

                Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("organization")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Organization"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RemoteIpDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.RemoteIpDetails1",
            jsii_struct_bases=[],
            name_mapping={
                "city": "city",
                "country": "country",
                "geo_location": "geoLocation",
                "ip_address_v4": "ipAddressV4",
                "organization": "organization",
            },
        )
        class RemoteIpDetails1:
            def __init__(
                self,
                *,
                city: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.City1", typing.Dict[builtins.str, typing.Any]]] = None,
                country: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Country1", typing.Dict[builtins.str, typing.Any]]] = None,
                geo_location: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.GeoLocation", typing.Dict[builtins.str, typing.Any]]] = None,
                ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
                organization: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Organization1", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for RemoteIpDetails_1.

                :param city: (experimental) city property. Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param country: (experimental) country property. Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param geo_location: (experimental) geoLocation property. Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ip_address_v4: (experimental) ipAddressV4 property. Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param organization: (experimental) organization property. Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    remote_ip_details1 = guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails1(
                        city=guardduty_events.DetectorEvents.GuardDutyFinding.City1(
                            city_name=["cityName"]
                        ),
                        country=guardduty_events.DetectorEvents.GuardDutyFinding.Country1(
                            country_name=["countryName"]
                        ),
                        geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                            lat=["lat"],
                            lon=["lon"]
                        ),
                        ip_address_v4=["ipAddressV4"],
                        organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization1(
                            asn=["asn"],
                            asn_org=["asnOrg"],
                            isp=["isp"],
                            org=["org"]
                        )
                    )
                '''
                if isinstance(city, dict):
                    city = DetectorEvents.GuardDutyFinding.City1(**city)
                if isinstance(country, dict):
                    country = DetectorEvents.GuardDutyFinding.Country1(**country)
                if isinstance(geo_location, dict):
                    geo_location = DetectorEvents.GuardDutyFinding.GeoLocation(**geo_location)
                if isinstance(organization, dict):
                    organization = DetectorEvents.GuardDutyFinding.Organization1(**organization)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__30e3fce8091b03f60574411d0220ff033792d03bd0622d44c5407c65ba13ff67)
                    check_type(argname="argument city", value=city, expected_type=type_hints["city"])
                    check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                    check_type(argname="argument geo_location", value=geo_location, expected_type=type_hints["geo_location"])
                    check_type(argname="argument ip_address_v4", value=ip_address_v4, expected_type=type_hints["ip_address_v4"])
                    check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city is not None:
                    self._values["city"] = city
                if country is not None:
                    self._values["country"] = country
                if geo_location is not None:
                    self._values["geo_location"] = geo_location
                if ip_address_v4 is not None:
                    self._values["ip_address_v4"] = ip_address_v4
                if organization is not None:
                    self._values["organization"] = organization

            @builtins.property
            def city(self) -> typing.Optional["DetectorEvents.GuardDutyFinding.City1"]:
                '''(experimental) city property.

                Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.City1"], result)

            @builtins.property
            def country(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Country1"]:
                '''(experimental) country property.

                Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Country1"], result)

            @builtins.property
            def geo_location(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation"]:
                '''(experimental) geoLocation property.

                Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("geo_location")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation"], result)

            @builtins.property
            def ip_address_v4(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipAddressV4 property.

                Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ip_address_v4")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def organization(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Organization1"]:
                '''(experimental) organization property.

                Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("organization")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Organization1"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RemoteIpDetails1(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.RemoteIpDetails2",
            jsii_struct_bases=[],
            name_mapping={
                "city": "city",
                "country": "country",
                "geo_location": "geoLocation",
                "ip_address_v4": "ipAddressV4",
                "organization": "organization",
            },
        )
        class RemoteIpDetails2:
            def __init__(
                self,
                *,
                city: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.City2", typing.Dict[builtins.str, typing.Any]]] = None,
                country: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Country2", typing.Dict[builtins.str, typing.Any]]] = None,
                geo_location: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.GeoLocation", typing.Dict[builtins.str, typing.Any]]] = None,
                ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
                organization: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Organization2", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for RemoteIpDetails_2.

                :param city: (experimental) city property. Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param country: (experimental) country property. Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param geo_location: (experimental) geoLocation property. Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ip_address_v4: (experimental) ipAddressV4 property. Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param organization: (experimental) organization property. Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    remote_ip_details2 = guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails2(
                        city=guardduty_events.DetectorEvents.GuardDutyFinding.City2(
                            city_name=["cityName"]
                        ),
                        country=guardduty_events.DetectorEvents.GuardDutyFinding.Country2(
                            country_name=["countryName"]
                        ),
                        geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                            lat=["lat"],
                            lon=["lon"]
                        ),
                        ip_address_v4=["ipAddressV4"],
                        organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization2(
                            asn=["asn"],
                            asn_org=["asnOrg"],
                            isp=["isp"],
                            org=["org"]
                        )
                    )
                '''
                if isinstance(city, dict):
                    city = DetectorEvents.GuardDutyFinding.City2(**city)
                if isinstance(country, dict):
                    country = DetectorEvents.GuardDutyFinding.Country2(**country)
                if isinstance(geo_location, dict):
                    geo_location = DetectorEvents.GuardDutyFinding.GeoLocation(**geo_location)
                if isinstance(organization, dict):
                    organization = DetectorEvents.GuardDutyFinding.Organization2(**organization)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b2d71e9efdd5679d0029316e6c525bc02503955e7b5eef9be05bc648ccf2a5e1)
                    check_type(argname="argument city", value=city, expected_type=type_hints["city"])
                    check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                    check_type(argname="argument geo_location", value=geo_location, expected_type=type_hints["geo_location"])
                    check_type(argname="argument ip_address_v4", value=ip_address_v4, expected_type=type_hints["ip_address_v4"])
                    check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city is not None:
                    self._values["city"] = city
                if country is not None:
                    self._values["country"] = country
                if geo_location is not None:
                    self._values["geo_location"] = geo_location
                if ip_address_v4 is not None:
                    self._values["ip_address_v4"] = ip_address_v4
                if organization is not None:
                    self._values["organization"] = organization

            @builtins.property
            def city(self) -> typing.Optional["DetectorEvents.GuardDutyFinding.City2"]:
                '''(experimental) city property.

                Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.City2"], result)

            @builtins.property
            def country(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Country2"]:
                '''(experimental) country property.

                Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Country2"], result)

            @builtins.property
            def geo_location(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation"]:
                '''(experimental) geoLocation property.

                Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("geo_location")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation"], result)

            @builtins.property
            def ip_address_v4(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipAddressV4 property.

                Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ip_address_v4")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def organization(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Organization2"]:
                '''(experimental) organization property.

                Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("organization")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Organization2"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RemoteIpDetails2(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.RemoteIpDetails3",
            jsii_struct_bases=[],
            name_mapping={
                "city": "city",
                "country": "country",
                "geo_location": "geoLocation",
                "ip_address_v4": "ipAddressV4",
                "organization": "organization",
            },
        )
        class RemoteIpDetails3:
            def __init__(
                self,
                *,
                city: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.City3", typing.Dict[builtins.str, typing.Any]]] = None,
                country: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Country3", typing.Dict[builtins.str, typing.Any]]] = None,
                geo_location: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.GeoLocation", typing.Dict[builtins.str, typing.Any]]] = None,
                ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
                organization: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Organization3", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for RemoteIpDetails_3.

                :param city: (experimental) city property. Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param country: (experimental) country property. Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param geo_location: (experimental) geoLocation property. Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ip_address_v4: (experimental) ipAddressV4 property. Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param organization: (experimental) organization property. Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    remote_ip_details3 = guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails3(
                        city=guardduty_events.DetectorEvents.GuardDutyFinding.City3(
                            city_name=["cityName"]
                        ),
                        country=guardduty_events.DetectorEvents.GuardDutyFinding.Country3(
                            country_name=["countryName"]
                        ),
                        geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                            lat=["lat"],
                            lon=["lon"]
                        ),
                        ip_address_v4=["ipAddressV4"],
                        organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization3(
                            asn=["asn"],
                            asn_org=["asnOrg"],
                            isp=["isp"],
                            org=["org"]
                        )
                    )
                '''
                if isinstance(city, dict):
                    city = DetectorEvents.GuardDutyFinding.City3(**city)
                if isinstance(country, dict):
                    country = DetectorEvents.GuardDutyFinding.Country3(**country)
                if isinstance(geo_location, dict):
                    geo_location = DetectorEvents.GuardDutyFinding.GeoLocation(**geo_location)
                if isinstance(organization, dict):
                    organization = DetectorEvents.GuardDutyFinding.Organization3(**organization)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__40feccc8bf09aef0318879909051495cece42bf865692c4e63036b38de135f4c)
                    check_type(argname="argument city", value=city, expected_type=type_hints["city"])
                    check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                    check_type(argname="argument geo_location", value=geo_location, expected_type=type_hints["geo_location"])
                    check_type(argname="argument ip_address_v4", value=ip_address_v4, expected_type=type_hints["ip_address_v4"])
                    check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city is not None:
                    self._values["city"] = city
                if country is not None:
                    self._values["country"] = country
                if geo_location is not None:
                    self._values["geo_location"] = geo_location
                if ip_address_v4 is not None:
                    self._values["ip_address_v4"] = ip_address_v4
                if organization is not None:
                    self._values["organization"] = organization

            @builtins.property
            def city(self) -> typing.Optional["DetectorEvents.GuardDutyFinding.City3"]:
                '''(experimental) city property.

                Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.City3"], result)

            @builtins.property
            def country(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Country3"]:
                '''(experimental) country property.

                Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Country3"], result)

            @builtins.property
            def geo_location(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation"]:
                '''(experimental) geoLocation property.

                Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("geo_location")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation"], result)

            @builtins.property
            def ip_address_v4(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipAddressV4 property.

                Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ip_address_v4")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def organization(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Organization3"]:
                '''(experimental) organization property.

                Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("organization")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Organization3"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RemoteIpDetails3(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.RemoteIpDetails4",
            jsii_struct_bases=[],
            name_mapping={
                "city": "city",
                "country": "country",
                "geo_location": "geoLocation",
                "ip_address_v4": "ipAddressV4",
                "organization": "organization",
            },
        )
        class RemoteIpDetails4:
            def __init__(
                self,
                *,
                city: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.City4", typing.Dict[builtins.str, typing.Any]]] = None,
                country: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Country4", typing.Dict[builtins.str, typing.Any]]] = None,
                geo_location: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.GeoLocation1", typing.Dict[builtins.str, typing.Any]]] = None,
                ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
                organization: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Organization4", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for RemoteIpDetails_4.

                :param city: (experimental) city property. Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param country: (experimental) country property. Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param geo_location: (experimental) geoLocation property. Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ip_address_v4: (experimental) ipAddressV4 property. Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param organization: (experimental) organization property. Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    remote_ip_details4 = guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails4(
                        city=guardduty_events.DetectorEvents.GuardDutyFinding.City4(
                            city_name=["cityName"]
                        ),
                        country=guardduty_events.DetectorEvents.GuardDutyFinding.Country4(
                            country_name=["countryName"]
                        ),
                        geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation1(
                            lat=["lat"],
                            lon=["lon"]
                        ),
                        ip_address_v4=["ipAddressV4"],
                        organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization4(
                            asn=["asn"],
                            asn_org=["asnOrg"],
                            isp=["isp"],
                            org=["org"]
                        )
                    )
                '''
                if isinstance(city, dict):
                    city = DetectorEvents.GuardDutyFinding.City4(**city)
                if isinstance(country, dict):
                    country = DetectorEvents.GuardDutyFinding.Country4(**country)
                if isinstance(geo_location, dict):
                    geo_location = DetectorEvents.GuardDutyFinding.GeoLocation1(**geo_location)
                if isinstance(organization, dict):
                    organization = DetectorEvents.GuardDutyFinding.Organization4(**organization)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b0f479ea1916c9fb4efda1668face8d76356a362cdc7178c89c55d305ee1704f)
                    check_type(argname="argument city", value=city, expected_type=type_hints["city"])
                    check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                    check_type(argname="argument geo_location", value=geo_location, expected_type=type_hints["geo_location"])
                    check_type(argname="argument ip_address_v4", value=ip_address_v4, expected_type=type_hints["ip_address_v4"])
                    check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if city is not None:
                    self._values["city"] = city
                if country is not None:
                    self._values["country"] = country
                if geo_location is not None:
                    self._values["geo_location"] = geo_location
                if ip_address_v4 is not None:
                    self._values["ip_address_v4"] = ip_address_v4
                if organization is not None:
                    self._values["organization"] = organization

            @builtins.property
            def city(self) -> typing.Optional["DetectorEvents.GuardDutyFinding.City4"]:
                '''(experimental) city property.

                Specify an array of string values to match this event if the actual value of city is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("city")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.City4"], result)

            @builtins.property
            def country(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Country4"]:
                '''(experimental) country property.

                Specify an array of string values to match this event if the actual value of country is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("country")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Country4"], result)

            @builtins.property
            def geo_location(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation1"]:
                '''(experimental) geoLocation property.

                Specify an array of string values to match this event if the actual value of geoLocation is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("geo_location")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.GeoLocation1"], result)

            @builtins.property
            def ip_address_v4(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) ipAddressV4 property.

                Specify an array of string values to match this event if the actual value of ipAddressV4 is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ip_address_v4")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def organization(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Organization4"]:
                '''(experimental) organization property.

                Specify an array of string values to match this event if the actual value of organization is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("organization")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Organization4"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RemoteIpDetails4(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.RemotePortDetails",
            jsii_struct_bases=[],
            name_mapping={"port": "port", "port_name": "portName"},
        )
        class RemotePortDetails:
            def __init__(
                self,
                *,
                port: typing.Optional[typing.Sequence[builtins.str]] = None,
                port_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RemotePortDetails.

                :param port: (experimental) port property. Specify an array of string values to match this event if the actual value of port is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param port_name: (experimental) portName property. Specify an array of string values to match this event if the actual value of portName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    remote_port_details = guardduty_events.DetectorEvents.GuardDutyFinding.RemotePortDetails(
                        port=["port"],
                        port_name=["portName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__80ca6d507c2901eb356e5b2e2b0bcafa8477547b22db8cd6cc643698283fd4f7)
                    check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                    check_type(argname="argument port_name", value=port_name, expected_type=type_hints["port_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if port is not None:
                    self._values["port"] = port
                if port_name is not None:
                    self._values["port_name"] = port_name

            @builtins.property
            def port(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) port property.

                Specify an array of string values to match this event if the actual value of port is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("port")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def port_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) portName property.

                Specify an array of string values to match this event if the actual value of portName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("port_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RemotePortDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Resource",
            jsii_struct_bases=[],
            name_mapping={
                "access_key_details": "accessKeyDetails",
                "container_details": "containerDetails",
                "ebs_volume_details": "ebsVolumeDetails",
                "ecs_cluster_details": "ecsClusterDetails",
                "eks_cluster_details": "eksClusterDetails",
                "instance_details": "instanceDetails",
                "kubernetes_details": "kubernetesDetails",
                "resource_type": "resourceType",
                "s3_bucket_details": "s3BucketDetails",
            },
        )
        class Resource:
            def __init__(
                self,
                *,
                access_key_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.AccessKeyDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                container_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.ContainerDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                ebs_volume_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.EbsVolumeDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                ecs_cluster_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.EcsClusterDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                eks_cluster_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.EksClusterDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                instance_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.InstanceDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                kubernetes_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.KubernetesDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                s3_bucket_details: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.ResourceItem", typing.Dict[builtins.str, typing.Any]]]] = None,
            ) -> None:
                '''(experimental) Type definition for Resource.

                :param access_key_details: (experimental) accessKeyDetails property. Specify an array of string values to match this event if the actual value of accessKeyDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param container_details: (experimental) containerDetails property. Specify an array of string values to match this event if the actual value of containerDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ebs_volume_details: (experimental) ebsVolumeDetails property. Specify an array of string values to match this event if the actual value of ebsVolumeDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param ecs_cluster_details: (experimental) ecsClusterDetails property. Specify an array of string values to match this event if the actual value of ecsClusterDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param eks_cluster_details: (experimental) eksClusterDetails property. Specify an array of string values to match this event if the actual value of eksClusterDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param instance_details: (experimental) instanceDetails property. Specify an array of string values to match this event if the actual value of instanceDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param kubernetes_details: (experimental) kubernetesDetails property. Specify an array of string values to match this event if the actual value of kubernetesDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resource_type: (experimental) resourceType property. Specify an array of string values to match this event if the actual value of resourceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param s3_bucket_details: (experimental) s3BucketDetails property. Specify an array of string values to match this event if the actual value of s3BucketDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    # ipv6_addresses: Any
                    
                    resource = guardduty_events.DetectorEvents.GuardDutyFinding.Resource(
                        access_key_details=guardduty_events.DetectorEvents.GuardDutyFinding.AccessKeyDetails(
                            access_key_id=["accessKeyId"],
                            principal_id=["principalId"],
                            user_name=["userName"],
                            user_type=["userType"]
                        ),
                        container_details=guardduty_events.DetectorEvents.GuardDutyFinding.ContainerDetails(
                            id=["id"],
                            image=["image"],
                            name=["name"]
                        ),
                        ebs_volume_details=guardduty_events.DetectorEvents.GuardDutyFinding.EbsVolumeDetails(
                            scanned_volume_details=[guardduty_events.DetectorEvents.GuardDutyFinding.EbsVolumeDetailsItem(
                                device_name=["deviceName"],
                                encryption_type=["encryptionType"],
                                kms_key_arn=["kmsKeyArn"],
                                snapshot_arn=["snapshotArn"],
                                volume_arn=["volumeArn"],
                                volume_size_in_gb=["volumeSizeInGb"],
                                volume_type=["volumeType"]
                            )],
                            skipped_volume_details=["skippedVolumeDetails"]
                        ),
                        ecs_cluster_details=guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetails(
                            arn=["arn"],
                            name=["name"],
                            status=["status"],
                            tags=[guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem(
                                key=["key"],
                                value=["value"]
                            )],
                            task_details=guardduty_events.DetectorEvents.GuardDutyFinding.TaskDetails(
                                arn=["arn"],
                                containers=[guardduty_events.DetectorEvents.GuardDutyFinding.TaskDetailsItem(
                                    image=["image"],
                                    name=["name"]
                                )],
                                created_at=["createdAt"],
                                definition_arn=["definitionArn"],
                                started_at=["startedAt"],
                                started_by=["startedBy"],
                                version=["version"]
                            )
                        ),
                        eks_cluster_details=guardduty_events.DetectorEvents.GuardDutyFinding.EksClusterDetails(
                            arn=["arn"],
                            created_at=["createdAt"],
                            name=["name"],
                            status=["status"],
                            tags=[guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem(
                                key=["key"],
                                value=["value"]
                            )],
                            vpc_id=["vpcId"]
                        ),
                        instance_details=guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetails(
                            availability_zone=["availabilityZone"],
                            iam_instance_profile=guardduty_events.DetectorEvents.GuardDutyFinding.IamInstanceProfile(
                                arn=["arn"],
                                id=["id"]
                            ),
                            image_description=["imageDescription"],
                            image_id=["imageId"],
                            instance_id=["instanceId"],
                            instance_state=["instanceState"],
                            instance_type=["instanceType"],
                            launch_time=["launchTime"],
                            network_interfaces=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItem(
                                ipv6_addresses=[ipv6_addresses],
                                network_interface_id=["networkInterfaceId"],
                                private_dns_name=["privateDnsName"],
                                private_ip_address=["privateIpAddress"],
                                private_ip_addresses=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem(
                                    private_dns_name=["privateDnsName"],
                                    private_ip_address=["privateIpAddress"]
                                )],
                                public_dns_name=["publicDnsName"],
                                public_ip=["publicIp"],
                                security_groups=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem1(
                                    group_id=["groupId"],
                                    group_name=["groupName"]
                                )],
                                subnet_id=["subnetId"],
                                vpc_id=["vpcId"]
                            )],
                            outpost_arn=["outpostArn"],
                            platform=["platform"],
                            product_codes=[guardduty_events.DetectorEvents.GuardDutyFinding.InstanceDetailsItem1(
                                product_code_id=["productCodeId"],
                                product_code_type=["productCodeType"]
                            )],
                            tags=[guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem(
                                key=["key"],
                                value=["value"]
                            )]
                        ),
                        kubernetes_details=guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesDetails(
                            kubernetes_user_details=guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesUserDetails(
                                groups=["groups"],
                                uid=["uid"],
                                username=["username"]
                            ),
                            kubernetes_workload_details=guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetails(
                                containers=[guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetailsItem(
                                    image=["image"],
                                    image_prefix=["imagePrefix"],
                                    name=["name"],
                                    security_context=guardduty_events.DetectorEvents.GuardDutyFinding.SecurityContext(
                                        privileged=["privileged"]
                                    )
                                )],
                                name=["name"],
                                namespace=["namespace"],
                                type=["type"],
                                uid=["uid"]
                            )
                        ),
                        resource_type=["resourceType"],
                        s3_bucket_details=[guardduty_events.DetectorEvents.GuardDutyFinding.ResourceItem(
                            arn=["arn"],
                            created_at=["createdAt"],
                            default_server_side_encryption=guardduty_events.DetectorEvents.GuardDutyFinding.DefaultServerSideEncryption(
                                encryption_type=["encryptionType"],
                                kms_master_key_arn=["kmsMasterKeyArn"]
                            ),
                            name=["name"],
                            owner=guardduty_events.DetectorEvents.GuardDutyFinding.Owner(
                                id=["id"]
                            ),
                            public_access=guardduty_events.DetectorEvents.GuardDutyFinding.PublicAccess(
                                effective_permission=["effectivePermission"],
                                permission_configuration=guardduty_events.DetectorEvents.GuardDutyFinding.PermissionConfiguration(
                                    account_level_permissions=guardduty_events.DetectorEvents.GuardDutyFinding.AccountLevelPermissions(
                                        block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                                            block_public_acls=["blockPublicAcls"],
                                            block_public_policy=["blockPublicPolicy"],
                                            ignore_public_acls=["ignorePublicAcls"],
                                            restrict_public_buckets=["restrictPublicBuckets"]
                                        )
                                    ),
                                    bucket_level_permissions=guardduty_events.DetectorEvents.GuardDutyFinding.BucketLevelPermissions(
                                        access_control_list=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                                            allows_public_read_access=["allowsPublicReadAccess"],
                                            allows_public_write_access=["allowsPublicWriteAccess"]
                                        ),
                                        block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                                            block_public_acls=["blockPublicAcls"],
                                            block_public_policy=["blockPublicPolicy"],
                                            ignore_public_acls=["ignorePublicAcls"],
                                            restrict_public_buckets=["restrictPublicBuckets"]
                                        ),
                                        bucket_policy=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                                            allows_public_read_access=["allowsPublicReadAccess"],
                                            allows_public_write_access=["allowsPublicWriteAccess"]
                                        )
                                    )
                                )
                            ),
                            tags=[guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem(
                                key=["key"],
                                value=["value"]
                            )],
                            type=["type"]
                        )]
                    )
                '''
                if isinstance(access_key_details, dict):
                    access_key_details = DetectorEvents.GuardDutyFinding.AccessKeyDetails(**access_key_details)
                if isinstance(container_details, dict):
                    container_details = DetectorEvents.GuardDutyFinding.ContainerDetails(**container_details)
                if isinstance(ebs_volume_details, dict):
                    ebs_volume_details = DetectorEvents.GuardDutyFinding.EbsVolumeDetails(**ebs_volume_details)
                if isinstance(ecs_cluster_details, dict):
                    ecs_cluster_details = DetectorEvents.GuardDutyFinding.EcsClusterDetails(**ecs_cluster_details)
                if isinstance(eks_cluster_details, dict):
                    eks_cluster_details = DetectorEvents.GuardDutyFinding.EksClusterDetails(**eks_cluster_details)
                if isinstance(instance_details, dict):
                    instance_details = DetectorEvents.GuardDutyFinding.InstanceDetails(**instance_details)
                if isinstance(kubernetes_details, dict):
                    kubernetes_details = DetectorEvents.GuardDutyFinding.KubernetesDetails(**kubernetes_details)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8d27074d7f9daad6d326e7f8d2fb49220e7494d3b522cb13133eef62d7a0b79d)
                    check_type(argname="argument access_key_details", value=access_key_details, expected_type=type_hints["access_key_details"])
                    check_type(argname="argument container_details", value=container_details, expected_type=type_hints["container_details"])
                    check_type(argname="argument ebs_volume_details", value=ebs_volume_details, expected_type=type_hints["ebs_volume_details"])
                    check_type(argname="argument ecs_cluster_details", value=ecs_cluster_details, expected_type=type_hints["ecs_cluster_details"])
                    check_type(argname="argument eks_cluster_details", value=eks_cluster_details, expected_type=type_hints["eks_cluster_details"])
                    check_type(argname="argument instance_details", value=instance_details, expected_type=type_hints["instance_details"])
                    check_type(argname="argument kubernetes_details", value=kubernetes_details, expected_type=type_hints["kubernetes_details"])
                    check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                    check_type(argname="argument s3_bucket_details", value=s3_bucket_details, expected_type=type_hints["s3_bucket_details"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if access_key_details is not None:
                    self._values["access_key_details"] = access_key_details
                if container_details is not None:
                    self._values["container_details"] = container_details
                if ebs_volume_details is not None:
                    self._values["ebs_volume_details"] = ebs_volume_details
                if ecs_cluster_details is not None:
                    self._values["ecs_cluster_details"] = ecs_cluster_details
                if eks_cluster_details is not None:
                    self._values["eks_cluster_details"] = eks_cluster_details
                if instance_details is not None:
                    self._values["instance_details"] = instance_details
                if kubernetes_details is not None:
                    self._values["kubernetes_details"] = kubernetes_details
                if resource_type is not None:
                    self._values["resource_type"] = resource_type
                if s3_bucket_details is not None:
                    self._values["s3_bucket_details"] = s3_bucket_details

            @builtins.property
            def access_key_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.AccessKeyDetails"]:
                '''(experimental) accessKeyDetails property.

                Specify an array of string values to match this event if the actual value of accessKeyDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("access_key_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.AccessKeyDetails"], result)

            @builtins.property
            def container_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.ContainerDetails"]:
                '''(experimental) containerDetails property.

                Specify an array of string values to match this event if the actual value of containerDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("container_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.ContainerDetails"], result)

            @builtins.property
            def ebs_volume_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.EbsVolumeDetails"]:
                '''(experimental) ebsVolumeDetails property.

                Specify an array of string values to match this event if the actual value of ebsVolumeDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ebs_volume_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.EbsVolumeDetails"], result)

            @builtins.property
            def ecs_cluster_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.EcsClusterDetails"]:
                '''(experimental) ecsClusterDetails property.

                Specify an array of string values to match this event if the actual value of ecsClusterDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ecs_cluster_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.EcsClusterDetails"], result)

            @builtins.property
            def eks_cluster_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.EksClusterDetails"]:
                '''(experimental) eksClusterDetails property.

                Specify an array of string values to match this event if the actual value of eksClusterDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("eks_cluster_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.EksClusterDetails"], result)

            @builtins.property
            def instance_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.InstanceDetails"]:
                '''(experimental) instanceDetails property.

                Specify an array of string values to match this event if the actual value of instanceDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("instance_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.InstanceDetails"], result)

            @builtins.property
            def kubernetes_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.KubernetesDetails"]:
                '''(experimental) kubernetesDetails property.

                Specify an array of string values to match this event if the actual value of kubernetesDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("kubernetes_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.KubernetesDetails"], result)

            @builtins.property
            def resource_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) resourceType property.

                Specify an array of string values to match this event if the actual value of resourceType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def s3_bucket_details(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.ResourceItem"]]:
                '''(experimental) s3BucketDetails property.

                Specify an array of string values to match this event if the actual value of s3BucketDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("s3_bucket_details")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.ResourceItem"]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Resource(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.ResourceItem",
            jsii_struct_bases=[],
            name_mapping={
                "arn": "arn",
                "created_at": "createdAt",
                "default_server_side_encryption": "defaultServerSideEncryption",
                "name": "name",
                "owner": "owner",
                "public_access": "publicAccess",
                "tags": "tags",
                "type": "type",
            },
        )
        class ResourceItem:
            def __init__(
                self,
                *,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                default_server_side_encryption: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.DefaultServerSideEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                owner: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Owner", typing.Dict[builtins.str, typing.Any]]] = None,
                public_access: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.PublicAccess", typing.Dict[builtins.str, typing.Any]]] = None,
                tags: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResourceItem.

                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param default_server_side_encryption: (experimental) defaultServerSideEncryption property. Specify an array of string values to match this event if the actual value of defaultServerSideEncryption is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param owner: (experimental) owner property. Specify an array of string values to match this event if the actual value of owner is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param public_access: (experimental) publicAccess property. Specify an array of string values to match this event if the actual value of publicAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param tags: (experimental) tags property. Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    resource_item = guardduty_events.DetectorEvents.GuardDutyFinding.ResourceItem(
                        arn=["arn"],
                        created_at=["createdAt"],
                        default_server_side_encryption=guardduty_events.DetectorEvents.GuardDutyFinding.DefaultServerSideEncryption(
                            encryption_type=["encryptionType"],
                            kms_master_key_arn=["kmsMasterKeyArn"]
                        ),
                        name=["name"],
                        owner=guardduty_events.DetectorEvents.GuardDutyFinding.Owner(
                            id=["id"]
                        ),
                        public_access=guardduty_events.DetectorEvents.GuardDutyFinding.PublicAccess(
                            effective_permission=["effectivePermission"],
                            permission_configuration=guardduty_events.DetectorEvents.GuardDutyFinding.PermissionConfiguration(
                                account_level_permissions=guardduty_events.DetectorEvents.GuardDutyFinding.AccountLevelPermissions(
                                    block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                                        block_public_acls=["blockPublicAcls"],
                                        block_public_policy=["blockPublicPolicy"],
                                        ignore_public_acls=["ignorePublicAcls"],
                                        restrict_public_buckets=["restrictPublicBuckets"]
                                    )
                                ),
                                bucket_level_permissions=guardduty_events.DetectorEvents.GuardDutyFinding.BucketLevelPermissions(
                                    access_control_list=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                                        allows_public_read_access=["allowsPublicReadAccess"],
                                        allows_public_write_access=["allowsPublicWriteAccess"]
                                    ),
                                    block_public_access=guardduty_events.DetectorEvents.GuardDutyFinding.BlockPublicAccess(
                                        block_public_acls=["blockPublicAcls"],
                                        block_public_policy=["blockPublicPolicy"],
                                        ignore_public_acls=["ignorePublicAcls"],
                                        restrict_public_buckets=["restrictPublicBuckets"]
                                    ),
                                    bucket_policy=guardduty_events.DetectorEvents.GuardDutyFinding.AccessControlList(
                                        allows_public_read_access=["allowsPublicReadAccess"],
                                        allows_public_write_access=["allowsPublicWriteAccess"]
                                    )
                                )
                            )
                        ),
                        tags=[guardduty_events.DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem(
                            key=["key"],
                            value=["value"]
                        )],
                        type=["type"]
                    )
                '''
                if isinstance(default_server_side_encryption, dict):
                    default_server_side_encryption = DetectorEvents.GuardDutyFinding.DefaultServerSideEncryption(**default_server_side_encryption)
                if isinstance(owner, dict):
                    owner = DetectorEvents.GuardDutyFinding.Owner(**owner)
                if isinstance(public_access, dict):
                    public_access = DetectorEvents.GuardDutyFinding.PublicAccess(**public_access)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3e5b1ac95333036d79a6164e6f92176701f4dc757cf088f8079547cdb0462ec2)
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                    check_type(argname="argument default_server_side_encryption", value=default_server_side_encryption, expected_type=type_hints["default_server_side_encryption"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
                    check_type(argname="argument public_access", value=public_access, expected_type=type_hints["public_access"])
                    check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if arn is not None:
                    self._values["arn"] = arn
                if created_at is not None:
                    self._values["created_at"] = created_at
                if default_server_side_encryption is not None:
                    self._values["default_server_side_encryption"] = default_server_side_encryption
                if name is not None:
                    self._values["name"] = name
                if owner is not None:
                    self._values["owner"] = owner
                if public_access is not None:
                    self._values["public_access"] = public_access
                if tags is not None:
                    self._values["tags"] = tags
                if type is not None:
                    self._values["type"] = type

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def created_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) createdAt property.

                Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("created_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def default_server_side_encryption(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.DefaultServerSideEncryption"]:
                '''(experimental) defaultServerSideEncryption property.

                Specify an array of string values to match this event if the actual value of defaultServerSideEncryption is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("default_server_side_encryption")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.DefaultServerSideEncryption"], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def owner(self) -> typing.Optional["DetectorEvents.GuardDutyFinding.Owner"]:
                '''(experimental) owner property.

                Specify an array of string values to match this event if the actual value of owner is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("owner")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Owner"], result)

            @builtins.property
            def public_access(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.PublicAccess"]:
                '''(experimental) publicAccess property.

                Specify an array of string values to match this event if the actual value of publicAccess is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("public_access")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.PublicAccess"], result)

            @builtins.property
            def tags(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem"]]:
                '''(experimental) tags property.

                Specify an array of string values to match this event if the actual value of tags is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("tags")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem"]], result)

            @builtins.property
            def type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) type property.

                Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResourceItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.ScanDetections",
            jsii_struct_bases=[],
            name_mapping={
                "highest_severity_threat_details": "highestSeverityThreatDetails",
                "scanned_item_count": "scannedItemCount",
                "threat_detected_by_name": "threatDetectedByName",
                "threats_detected_item_count": "threatsDetectedItemCount",
            },
        )
        class ScanDetections:
            def __init__(
                self,
                *,
                highest_severity_threat_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                scanned_item_count: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.ScannedItemCount", typing.Dict[builtins.str, typing.Any]]] = None,
                threat_detected_by_name: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.ThreatDetectedByName", typing.Dict[builtins.str, typing.Any]]] = None,
                threats_detected_item_count: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for ScanDetections.

                :param highest_severity_threat_details: (experimental) highestSeverityThreatDetails property. Specify an array of string values to match this event if the actual value of highestSeverityThreatDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param scanned_item_count: (experimental) scannedItemCount property. Specify an array of string values to match this event if the actual value of scannedItemCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param threat_detected_by_name: (experimental) threatDetectedByName property. Specify an array of string values to match this event if the actual value of threatDetectedByName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param threats_detected_item_count: (experimental) threatsDetectedItemCount property. Specify an array of string values to match this event if the actual value of threatsDetectedItemCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    scan_detections = guardduty_events.DetectorEvents.GuardDutyFinding.ScanDetections(
                        highest_severity_threat_details=guardduty_events.DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails(
                            count=["count"],
                            severity=["severity"],
                            threat_name=["threatName"]
                        ),
                        scanned_item_count=guardduty_events.DetectorEvents.GuardDutyFinding.ScannedItemCount(
                            files=["files"],
                            total_gb=["totalGb"],
                            volumes=["volumes"]
                        ),
                        threat_detected_by_name=guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByName(
                            item_count=["itemCount"],
                            shortened=["shortened"],
                            threat_names=[guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem(
                                file_paths=[guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem(
                                    file_name=["fileName"],
                                    file_path=["filePath"],
                                    hash=["hash"],
                                    volume_arn=["volumeArn"]
                                )],
                                item_count=["itemCount"],
                                name=["name"],
                                severity=["severity"]
                            )],
                            unique_threat_name_count=["uniqueThreatNameCount"]
                        ),
                        threats_detected_item_count=guardduty_events.DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount(
                            files=["files"]
                        )
                    )
                '''
                if isinstance(highest_severity_threat_details, dict):
                    highest_severity_threat_details = DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails(**highest_severity_threat_details)
                if isinstance(scanned_item_count, dict):
                    scanned_item_count = DetectorEvents.GuardDutyFinding.ScannedItemCount(**scanned_item_count)
                if isinstance(threat_detected_by_name, dict):
                    threat_detected_by_name = DetectorEvents.GuardDutyFinding.ThreatDetectedByName(**threat_detected_by_name)
                if isinstance(threats_detected_item_count, dict):
                    threats_detected_item_count = DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount(**threats_detected_item_count)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__016ead5d197c9e60651c9e3ac6fdc113e22d737271a4a81e3ae806cc4a9fdf4e)
                    check_type(argname="argument highest_severity_threat_details", value=highest_severity_threat_details, expected_type=type_hints["highest_severity_threat_details"])
                    check_type(argname="argument scanned_item_count", value=scanned_item_count, expected_type=type_hints["scanned_item_count"])
                    check_type(argname="argument threat_detected_by_name", value=threat_detected_by_name, expected_type=type_hints["threat_detected_by_name"])
                    check_type(argname="argument threats_detected_item_count", value=threats_detected_item_count, expected_type=type_hints["threats_detected_item_count"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if highest_severity_threat_details is not None:
                    self._values["highest_severity_threat_details"] = highest_severity_threat_details
                if scanned_item_count is not None:
                    self._values["scanned_item_count"] = scanned_item_count
                if threat_detected_by_name is not None:
                    self._values["threat_detected_by_name"] = threat_detected_by_name
                if threats_detected_item_count is not None:
                    self._values["threats_detected_item_count"] = threats_detected_item_count

            @builtins.property
            def highest_severity_threat_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails"]:
                '''(experimental) highestSeverityThreatDetails property.

                Specify an array of string values to match this event if the actual value of highestSeverityThreatDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("highest_severity_threat_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails"], result)

            @builtins.property
            def scanned_item_count(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.ScannedItemCount"]:
                '''(experimental) scannedItemCount property.

                Specify an array of string values to match this event if the actual value of scannedItemCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("scanned_item_count")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.ScannedItemCount"], result)

            @builtins.property
            def threat_detected_by_name(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.ThreatDetectedByName"]:
                '''(experimental) threatDetectedByName property.

                Specify an array of string values to match this event if the actual value of threatDetectedByName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threat_detected_by_name")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.ThreatDetectedByName"], result)

            @builtins.property
            def threats_detected_item_count(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount"]:
                '''(experimental) threatsDetectedItemCount property.

                Specify an array of string values to match this event if the actual value of threatsDetectedItemCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threats_detected_item_count")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ScanDetections(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.ScannedItemCount",
            jsii_struct_bases=[],
            name_mapping={
                "files": "files",
                "total_gb": "totalGb",
                "volumes": "volumes",
            },
        )
        class ScannedItemCount:
            def __init__(
                self,
                *,
                files: typing.Optional[typing.Sequence[builtins.str]] = None,
                total_gb: typing.Optional[typing.Sequence[builtins.str]] = None,
                volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ScannedItemCount.

                :param files: (experimental) files property. Specify an array of string values to match this event if the actual value of files is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param total_gb: (experimental) totalGb property. Specify an array of string values to match this event if the actual value of totalGb is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param volumes: (experimental) volumes property. Specify an array of string values to match this event if the actual value of volumes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    scanned_item_count = guardduty_events.DetectorEvents.GuardDutyFinding.ScannedItemCount(
                        files=["files"],
                        total_gb=["totalGb"],
                        volumes=["volumes"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4bede3607d3ef63971edc8cbfdb3fcb26dafc7a78ba567095d9f282ef8d8a352)
                    check_type(argname="argument files", value=files, expected_type=type_hints["files"])
                    check_type(argname="argument total_gb", value=total_gb, expected_type=type_hints["total_gb"])
                    check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if files is not None:
                    self._values["files"] = files
                if total_gb is not None:
                    self._values["total_gb"] = total_gb
                if volumes is not None:
                    self._values["volumes"] = volumes

            @builtins.property
            def files(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) files property.

                Specify an array of string values to match this event if the actual value of files is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("files")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def total_gb(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) totalGb property.

                Specify an array of string values to match this event if the actual value of totalGb is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("total_gb")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) volumes property.

                Specify an array of string values to match this event if the actual value of volumes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("volumes")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ScannedItemCount(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.SecurityContext",
            jsii_struct_bases=[],
            name_mapping={"privileged": "privileged"},
        )
        class SecurityContext:
            def __init__(
                self,
                *,
                privileged: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SecurityContext.

                :param privileged: (experimental) privileged property. Specify an array of string values to match this event if the actual value of privileged is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    security_context = guardduty_events.DetectorEvents.GuardDutyFinding.SecurityContext(
                        privileged=["privileged"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__2b9378038c6bf58d1213cb7aec0f485556ef488c447dad819c6afcddc9c9cfe2)
                    check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if privileged is not None:
                    self._values["privileged"] = privileged

            @builtins.property
            def privileged(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) privileged property.

                Specify an array of string values to match this event if the actual value of privileged is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("privileged")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SecurityContext(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.Service",
            jsii_struct_bases=[],
            name_mapping={
                "action": "action",
                "additional_info": "additionalInfo",
                "archived": "archived",
                "aws_api_call_action": "awsApiCallAction",
                "count": "count",
                "detector_id": "detectorId",
                "ebs_volume_scan_details": "ebsVolumeScanDetails",
                "event_first_seen": "eventFirstSeen",
                "event_last_seen": "eventLastSeen",
                "evidence": "evidence",
                "feature_name": "featureName",
                "resource_role": "resourceRole",
                "service_name": "serviceName",
            },
        )
        class Service:
            def __init__(
                self,
                *,
                action: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Action", typing.Dict[builtins.str, typing.Any]]] = None,
                additional_info: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.AdditionalInfo", typing.Dict[builtins.str, typing.Any]]] = None,
                archived: typing.Optional[typing.Sequence[builtins.str]] = None,
                aws_api_call_action: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.AwsApiCallAction", typing.Dict[builtins.str, typing.Any]]] = None,
                count: typing.Optional[typing.Sequence[builtins.str]] = None,
                detector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                ebs_volume_scan_details: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.EbsVolumeScanDetails", typing.Dict[builtins.str, typing.Any]]] = None,
                event_first_seen: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_last_seen: typing.Optional[typing.Sequence[builtins.str]] = None,
                evidence: typing.Optional[typing.Union["DetectorEvents.GuardDutyFinding.Evidence", typing.Dict[builtins.str, typing.Any]]] = None,
                feature_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                resource_role: typing.Optional[typing.Sequence[builtins.str]] = None,
                service_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Service.

                :param action: (experimental) action property. Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param additional_info: (experimental) additionalInfo property. Specify an array of string values to match this event if the actual value of additionalInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param archived: (experimental) archived property. Specify an array of string values to match this event if the actual value of archived is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param aws_api_call_action: (experimental) awsApiCallAction property. Specify an array of string values to match this event if the actual value of awsApiCallAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param count: (experimental) count property. Specify an array of string values to match this event if the actual value of count is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param detector_id: (experimental) detectorId property. Specify an array of string values to match this event if the actual value of detectorId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Detector reference
                :param ebs_volume_scan_details: (experimental) ebsVolumeScanDetails property. Specify an array of string values to match this event if the actual value of ebsVolumeScanDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_first_seen: (experimental) eventFirstSeen property. Specify an array of string values to match this event if the actual value of eventFirstSeen is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_last_seen: (experimental) eventLastSeen property. Specify an array of string values to match this event if the actual value of eventLastSeen is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param evidence: (experimental) evidence property. Specify an array of string values to match this event if the actual value of evidence is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param feature_name: (experimental) featureName property. Specify an array of string values to match this event if the actual value of featureName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param resource_role: (experimental) resourceRole property. Specify an array of string values to match this event if the actual value of resourceRole is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param service_name: (experimental) serviceName property. Specify an array of string values to match this event if the actual value of serviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    # additional_scanned_ports: Any
                    # unusual: Any
                    
                    service = guardduty_events.DetectorEvents.GuardDutyFinding.Service(
                        action=guardduty_events.DetectorEvents.GuardDutyFinding.Action(
                            action_type=["actionType"],
                            aws_api_call_action=guardduty_events.DetectorEvents.GuardDutyFinding.AwsApiCallAction1(
                                affected_resources=guardduty_events.DetectorEvents.GuardDutyFinding.AffectedResources1(
                                    aws_cloud_trail_trail=["awsCloudTrailTrail"],
                                    aws_ec2_instance=["awsEc2Instance"],
                                    aws_s3_bucket=["awsS3Bucket"]
                                ),
                                api=["api"],
                                caller_type=["callerType"],
                                error_code=["errorCode"],
                                remote_account_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteAccountDetails(
                                    account_id=["accountId"],
                                    affiliated=["affiliated"]
                                ),
                                remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails1(
                                    city=guardduty_events.DetectorEvents.GuardDutyFinding.City1(
                                        city_name=["cityName"]
                                    ),
                                    country=guardduty_events.DetectorEvents.GuardDutyFinding.Country1(
                                        country_name=["countryName"]
                                    ),
                                    geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                        lat=["lat"],
                                        lon=["lon"]
                                    ),
                                    ip_address_v4=["ipAddressV4"],
                                    organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization1(
                                        asn=["asn"],
                                        asn_org=["asnOrg"],
                                        isp=["isp"],
                                        org=["org"]
                                    )
                                ),
                                service_name=["serviceName"]
                            ),
                            dns_request_action=guardduty_events.DetectorEvents.GuardDutyFinding.DnsRequestAction(
                                blocked=["blocked"],
                                domain=["domain"],
                                protocol=["protocol"]
                            ),
                            kubernetes_api_call_action=guardduty_events.DetectorEvents.GuardDutyFinding.KubernetesApiCallAction(
                                parameters=["parameters"],
                                remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails2(
                                    city=guardduty_events.DetectorEvents.GuardDutyFinding.City2(
                                        city_name=["cityName"]
                                    ),
                                    country=guardduty_events.DetectorEvents.GuardDutyFinding.Country2(
                                        country_name=["countryName"]
                                    ),
                                    geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                        lat=["lat"],
                                        lon=["lon"]
                                    ),
                                    ip_address_v4=["ipAddressV4"],
                                    organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization2(
                                        asn=["asn"],
                                        asn_org=["asnOrg"],
                                        isp=["isp"],
                                        org=["org"]
                                    )
                                ),
                                request_uri=["requestUri"],
                                source_iPs=["sourceIPs"],
                                status_code=["statusCode"],
                                user_agent=["userAgent"],
                                verb=["verb"]
                            ),
                            network_connection_action=guardduty_events.DetectorEvents.GuardDutyFinding.NetworkConnectionAction(
                                blocked=["blocked"],
                                connection_direction=["connectionDirection"],
                                local_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalIpDetails(
                                    ip_address_v4=["ipAddressV4"]
                                ),
                                local_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalPortDetails(
                                    port=["port"],
                                    port_name=["portName"]
                                ),
                                protocol=["protocol"],
                                remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails3(
                                    city=guardduty_events.DetectorEvents.GuardDutyFinding.City3(
                                        city_name=["cityName"]
                                    ),
                                    country=guardduty_events.DetectorEvents.GuardDutyFinding.Country3(
                                        country_name=["countryName"]
                                    ),
                                    geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                        lat=["lat"],
                                        lon=["lon"]
                                    ),
                                    ip_address_v4=["ipAddressV4"],
                                    organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization3(
                                        asn=["asn"],
                                        asn_org=["asnOrg"],
                                        isp=["isp"],
                                        org=["org"]
                                    )
                                ),
                                remote_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemotePortDetails(
                                    port=["port"],
                                    port_name=["portName"]
                                )
                            ),
                            port_probe_action=guardduty_events.DetectorEvents.GuardDutyFinding.PortProbeAction(
                                blocked=["blocked"],
                                port_probe_details=[guardduty_events.DetectorEvents.GuardDutyFinding.PortProbeActionItem(
                                    local_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalIpDetails1(
                                        ip_address_v4=["ipAddressV4"]
                                    ),
                                    local_port_details=guardduty_events.DetectorEvents.GuardDutyFinding.LocalPortDetails1(
                                        port=["port"],
                                        port_name=["portName"]
                                    ),
                                    remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails4(
                                        city=guardduty_events.DetectorEvents.GuardDutyFinding.City4(
                                            city_name=["cityName"]
                                        ),
                                        country=guardduty_events.DetectorEvents.GuardDutyFinding.Country4(
                                            country_name=["countryName"]
                                        ),
                                        geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation1(
                                            lat=["lat"],
                                            lon=["lon"]
                                        ),
                                        ip_address_v4=["ipAddressV4"],
                                        organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization4(
                                            asn=["asn"],
                                            asn_org=["asnOrg"],
                                            isp=["isp"],
                                            org=["org"]
                                        )
                                    )
                                )]
                            )
                        ),
                        additional_info=guardduty_events.DetectorEvents.GuardDutyFinding.AdditionalInfo(
                            additional_scanned_ports=[additional_scanned_ports],
                            anomalies=guardduty_events.DetectorEvents.GuardDutyFinding.Anomalies(
                                anomalous_ap_is=["anomalousApIs"]
                            ),
                            api_calls=[guardduty_events.DetectorEvents.GuardDutyFinding.AdditionalInfoItem(
                                count=["count"],
                                first_seen=["firstSeen"],
                                last_seen=["lastSeen"],
                                name=["name"]
                            )],
                            domain=["domain"],
                            in_bytes=["inBytes"],
                            local_port=["localPort"],
                            new_policy=guardduty_events.DetectorEvents.GuardDutyFinding.NewPolicy(
                                allow_users_to_change_password=["allowUsersToChangePassword"],
                                hard_expiry=["hardExpiry"],
                                max_password_age=["maxPasswordAge"],
                                minimum_password_length=["minimumPasswordLength"],
                                password_reuse_prevention=["passwordReusePrevention"],
                                require_lowercase_characters=["requireLowercaseCharacters"],
                                require_numbers=["requireNumbers"],
                                require_symbols=["requireSymbols"],
                                require_uppercase_characters=["requireUppercaseCharacters"]
                            ),
                            old_policy=guardduty_events.DetectorEvents.GuardDutyFinding.OldPolicy(
                                allow_users_to_change_password=["allowUsersToChangePassword"],
                                hard_expiry=["hardExpiry"],
                                max_password_age=["maxPasswordAge"],
                                minimum_password_length=["minimumPasswordLength"],
                                password_reuse_prevention=["passwordReusePrevention"],
                                require_lowercase_characters=["requireLowercaseCharacters"],
                                require_numbers=["requireNumbers"],
                                require_symbols=["requireSymbols"],
                                require_uppercase_characters=["requireUppercaseCharacters"]
                            ),
                            out_bytes=["outBytes"],
                            ports_scanned_sample=[123],
                            profiled_behavior=guardduty_events.DetectorEvents.GuardDutyFinding.ProfiledBehavior(
                                frequent_profiled_ap_is_account_profiling=["frequentProfiledApIsAccountProfiling"],
                                frequent_profiled_ap_is_user_identity_profiling=["frequentProfiledApIsUserIdentityProfiling"],
                                frequent_profiled_as_ns_account_profiling=["frequentProfiledAsNsAccountProfiling"],
                                frequent_profiled_as_ns_bucket_profiling=["frequentProfiledAsNsBucketProfiling"],
                                frequent_profiled_as_ns_user_identity_profiling=["frequentProfiledAsNsUserIdentityProfiling"],
                                frequent_profiled_buckets_account_profiling=["frequentProfiledBucketsAccountProfiling"],
                                frequent_profiled_buckets_user_identity_profiling=["frequentProfiledBucketsUserIdentityProfiling"],
                                frequent_profiled_user_agents_account_profiling=["frequentProfiledUserAgentsAccountProfiling"],
                                frequent_profiled_user_agents_user_identity_profiling=["frequentProfiledUserAgentsUserIdentityProfiling"],
                                frequent_profiled_user_names_account_profiling=["frequentProfiledUserNamesAccountProfiling"],
                                frequent_profiled_user_names_bucket_profiling=["frequentProfiledUserNamesBucketProfiling"],
                                frequent_profiled_user_types_account_profiling=["frequentProfiledUserTypesAccountProfiling"],
                                infrequent_profiled_ap_is_account_profiling=["infrequentProfiledApIsAccountProfiling"],
                                infrequent_profiled_ap_is_user_identity_profiling=["infrequentProfiledApIsUserIdentityProfiling"],
                                infrequent_profiled_as_ns_account_profiling=["infrequentProfiledAsNsAccountProfiling"],
                                infrequent_profiled_as_ns_bucket_profiling=["infrequentProfiledAsNsBucketProfiling"],
                                infrequent_profiled_as_ns_user_identity_profiling=["infrequentProfiledAsNsUserIdentityProfiling"],
                                infrequent_profiled_buckets_account_profiling=["infrequentProfiledBucketsAccountProfiling"],
                                infrequent_profiled_buckets_user_identity_profiling=["infrequentProfiledBucketsUserIdentityProfiling"],
                                infrequent_profiled_user_agents_account_profiling=["infrequentProfiledUserAgentsAccountProfiling"],
                                infrequent_profiled_user_agents_user_identity_profiling=["infrequentProfiledUserAgentsUserIdentityProfiling"],
                                infrequent_profiled_user_names_account_profiling=["infrequentProfiledUserNamesAccountProfiling"],
                                infrequent_profiled_user_names_bucket_profiling=["infrequentProfiledUserNamesBucketProfiling"],
                                infrequent_profiled_user_types_account_profiling=["infrequentProfiledUserTypesAccountProfiling"],
                                number_of_historical_daily_avg_ap_is_bucket_profiling=["numberOfHistoricalDailyAvgApIsBucketProfiling"],
                                number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling=["numberOfHistoricalDailyAvgApIsBucketUserIdentityProfiling"],
                                number_of_historical_daily_avg_ap_is_user_identity_profiling=["numberOfHistoricalDailyAvgApIsUserIdentityProfiling"],
                                number_of_historical_daily_max_ap_is_bucket_profiling=["numberOfHistoricalDailyMaxApIsBucketProfiling"],
                                number_of_historical_daily_max_ap_is_bucket_user_identity_profiling=["numberOfHistoricalDailyMaxApIsBucketUserIdentityProfiling"],
                                number_of_historical_daily_max_ap_is_user_identity_profiling=["numberOfHistoricalDailyMaxApIsUserIdentityProfiling"],
                                rare_profiled_ap_is_account_profiling=["rareProfiledApIsAccountProfiling"],
                                rare_profiled_ap_is_user_identity_profiling=["rareProfiledApIsUserIdentityProfiling"],
                                rare_profiled_as_ns_account_profiling=["rareProfiledAsNsAccountProfiling"],
                                rare_profiled_as_ns_bucket_profiling=["rareProfiledAsNsBucketProfiling"],
                                rare_profiled_as_ns_user_identity_profiling=["rareProfiledAsNsUserIdentityProfiling"],
                                rare_profiled_buckets_account_profiling=["rareProfiledBucketsAccountProfiling"],
                                rare_profiled_buckets_user_identity_profiling=["rareProfiledBucketsUserIdentityProfiling"],
                                rare_profiled_user_agents_account_profiling=["rareProfiledUserAgentsAccountProfiling"],
                                rare_profiled_user_agents_user_identity_profiling=["rareProfiledUserAgentsUserIdentityProfiling"],
                                rare_profiled_user_names_account_profiling=["rareProfiledUserNamesAccountProfiling"],
                                rare_profiled_user_names_bucket_profiling=["rareProfiledUserNamesBucketProfiling"],
                                rare_profiled_user_types_account_profiling=["rareProfiledUserTypesAccountProfiling"]
                            ),
                            recent_credentials=[guardduty_events.DetectorEvents.GuardDutyFinding.AdditionalInfoItem1(
                                access_key_id=["accessKeyId"],
                                ip_address_v4=["ipAddressV4"],
                                principal_id=["principalId"]
                            )],
                            sample=["sample"],
                            scanned_port=["scannedPort"],
                            threat_list_name=["threatListName"],
                            threat_name=["threatName"],
                            type=["type"],
                            unusual=unusual,
                            unusual_behavior=guardduty_events.DetectorEvents.GuardDutyFinding.UnusualBehavior(
                                is_unusual_user_identity=["isUnusualUserIdentity"],
                                number_of_past24_hours_ap_is_bucket_profiling=["numberOfPast24HoursApIsBucketProfiling"],
                                number_of_past24_hours_ap_is_bucket_user_identity_profiling=["numberOfPast24HoursApIsBucketUserIdentityProfiling"],
                                number_of_past24_hours_ap_is_user_identity_profiling=["numberOfPast24HoursApIsUserIdentityProfiling"],
                                unusual_ap_is_account_profiling=["unusualApIsAccountProfiling"],
                                unusual_ap_is_user_identity_profiling=["unusualApIsUserIdentityProfiling"],
                                unusual_as_ns_account_profiling=["unusualAsNsAccountProfiling"],
                                unusual_as_ns_bucket_profiling=["unusualAsNsBucketProfiling"],
                                unusual_as_ns_user_identity_profiling=["unusualAsNsUserIdentityProfiling"],
                                unusual_buckets_account_profiling=["unusualBucketsAccountProfiling"],
                                unusual_buckets_user_identity_profiling=["unusualBucketsUserIdentityProfiling"],
                                unusual_user_agents_account_profiling=["unusualUserAgentsAccountProfiling"],
                                unusual_user_agents_user_identity_profiling=["unusualUserAgentsUserIdentityProfiling"],
                                unusual_user_names_account_profiling=["unusualUserNamesAccountProfiling"],
                                unusual_user_names_bucket_profiling=["unusualUserNamesBucketProfiling"],
                                unusual_user_types_account_profiling=["unusualUserTypesAccountProfiling"]
                            ),
                            unusual_protocol=["unusualProtocol"],
                            user_agent=guardduty_events.DetectorEvents.GuardDutyFinding.UserAgent(
                                full_user_agent=["fullUserAgent"],
                                user_agent_category=["userAgentCategory"]
                            ),
                            value=["value"]
                        ),
                        archived=["archived"],
                        aws_api_call_action=guardduty_events.DetectorEvents.GuardDutyFinding.AwsApiCallAction(
                            affected_resources=["affectedResources"],
                            api=["api"],
                            caller_type=["callerType"],
                            error_code=["errorCode"],
                            remote_ip_details=guardduty_events.DetectorEvents.GuardDutyFinding.RemoteIpDetails(
                                city=guardduty_events.DetectorEvents.GuardDutyFinding.City(
                                    city_name=["cityName"]
                                ),
                                country=guardduty_events.DetectorEvents.GuardDutyFinding.Country(
                                    country_name=["countryName"]
                                ),
                                geo_location=guardduty_events.DetectorEvents.GuardDutyFinding.GeoLocation(
                                    lat=["lat"],
                                    lon=["lon"]
                                ),
                                ip_address_v4=["ipAddressV4"],
                                organization=guardduty_events.DetectorEvents.GuardDutyFinding.Organization(
                                    asn=["asn"],
                                    asn_org=["asnOrg"],
                                    isp=["isp"],
                                    org=["org"]
                                )
                            ),
                            service_name=["serviceName"]
                        ),
                        count=["count"],
                        detector_id=["detectorId"],
                        ebs_volume_scan_details=guardduty_events.DetectorEvents.GuardDutyFinding.EbsVolumeScanDetails(
                            scan_completed_at=["scanCompletedAt"],
                            scan_detections=guardduty_events.DetectorEvents.GuardDutyFinding.ScanDetections(
                                highest_severity_threat_details=guardduty_events.DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails(
                                    count=["count"],
                                    severity=["severity"],
                                    threat_name=["threatName"]
                                ),
                                scanned_item_count=guardduty_events.DetectorEvents.GuardDutyFinding.ScannedItemCount(
                                    files=["files"],
                                    total_gb=["totalGb"],
                                    volumes=["volumes"]
                                ),
                                threat_detected_by_name=guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByName(
                                    item_count=["itemCount"],
                                    shortened=["shortened"],
                                    threat_names=[guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem(
                                        file_paths=[guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem(
                                            file_name=["fileName"],
                                            file_path=["filePath"],
                                            hash=["hash"],
                                            volume_arn=["volumeArn"]
                                        )],
                                        item_count=["itemCount"],
                                        name=["name"],
                                        severity=["severity"]
                                    )],
                                    unique_threat_name_count=["uniqueThreatNameCount"]
                                ),
                                threats_detected_item_count=guardduty_events.DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount(
                                    files=["files"]
                                )
                            ),
                            scan_id=["scanId"],
                            scan_started_at=["scanStartedAt"],
                            sources=["sources"],
                            trigger_finding_id=["triggerFindingId"]
                        ),
                        event_first_seen=["eventFirstSeen"],
                        event_last_seen=["eventLastSeen"],
                        evidence=guardduty_events.DetectorEvents.GuardDutyFinding.Evidence(
                            threat_intelligence_details=[guardduty_events.DetectorEvents.GuardDutyFinding.EvidenceItem(
                                threat_list_name=["threatListName"],
                                threat_names=["threatNames"]
                            )]
                        ),
                        feature_name=["featureName"],
                        resource_role=["resourceRole"],
                        service_name=["serviceName"]
                    )
                '''
                if isinstance(action, dict):
                    action = DetectorEvents.GuardDutyFinding.Action(**action)
                if isinstance(additional_info, dict):
                    additional_info = DetectorEvents.GuardDutyFinding.AdditionalInfo(**additional_info)
                if isinstance(aws_api_call_action, dict):
                    aws_api_call_action = DetectorEvents.GuardDutyFinding.AwsApiCallAction(**aws_api_call_action)
                if isinstance(ebs_volume_scan_details, dict):
                    ebs_volume_scan_details = DetectorEvents.GuardDutyFinding.EbsVolumeScanDetails(**ebs_volume_scan_details)
                if isinstance(evidence, dict):
                    evidence = DetectorEvents.GuardDutyFinding.Evidence(**evidence)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__338aadb3ef02cff7973f431c245179b88935141c6ccce3291ef06151c0effe77)
                    check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                    check_type(argname="argument additional_info", value=additional_info, expected_type=type_hints["additional_info"])
                    check_type(argname="argument archived", value=archived, expected_type=type_hints["archived"])
                    check_type(argname="argument aws_api_call_action", value=aws_api_call_action, expected_type=type_hints["aws_api_call_action"])
                    check_type(argname="argument count", value=count, expected_type=type_hints["count"])
                    check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
                    check_type(argname="argument ebs_volume_scan_details", value=ebs_volume_scan_details, expected_type=type_hints["ebs_volume_scan_details"])
                    check_type(argname="argument event_first_seen", value=event_first_seen, expected_type=type_hints["event_first_seen"])
                    check_type(argname="argument event_last_seen", value=event_last_seen, expected_type=type_hints["event_last_seen"])
                    check_type(argname="argument evidence", value=evidence, expected_type=type_hints["evidence"])
                    check_type(argname="argument feature_name", value=feature_name, expected_type=type_hints["feature_name"])
                    check_type(argname="argument resource_role", value=resource_role, expected_type=type_hints["resource_role"])
                    check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action is not None:
                    self._values["action"] = action
                if additional_info is not None:
                    self._values["additional_info"] = additional_info
                if archived is not None:
                    self._values["archived"] = archived
                if aws_api_call_action is not None:
                    self._values["aws_api_call_action"] = aws_api_call_action
                if count is not None:
                    self._values["count"] = count
                if detector_id is not None:
                    self._values["detector_id"] = detector_id
                if ebs_volume_scan_details is not None:
                    self._values["ebs_volume_scan_details"] = ebs_volume_scan_details
                if event_first_seen is not None:
                    self._values["event_first_seen"] = event_first_seen
                if event_last_seen is not None:
                    self._values["event_last_seen"] = event_last_seen
                if evidence is not None:
                    self._values["evidence"] = evidence
                if feature_name is not None:
                    self._values["feature_name"] = feature_name
                if resource_role is not None:
                    self._values["resource_role"] = resource_role
                if service_name is not None:
                    self._values["service_name"] = service_name

            @builtins.property
            def action(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Action"]:
                '''(experimental) action property.

                Specify an array of string values to match this event if the actual value of action is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("action")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Action"], result)

            @builtins.property
            def additional_info(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.AdditionalInfo"]:
                '''(experimental) additionalInfo property.

                Specify an array of string values to match this event if the actual value of additionalInfo is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("additional_info")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.AdditionalInfo"], result)

            @builtins.property
            def archived(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) archived property.

                Specify an array of string values to match this event if the actual value of archived is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("archived")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def aws_api_call_action(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.AwsApiCallAction"]:
                '''(experimental) awsApiCallAction property.

                Specify an array of string values to match this event if the actual value of awsApiCallAction is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_api_call_action")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.AwsApiCallAction"], result)

            @builtins.property
            def count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) count property.

                Specify an array of string values to match this event if the actual value of count is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def detector_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) detectorId property.

                Specify an array of string values to match this event if the actual value of detectorId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Detector reference

                :stability: experimental
                '''
                result = self._values.get("detector_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def ebs_volume_scan_details(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.EbsVolumeScanDetails"]:
                '''(experimental) ebsVolumeScanDetails property.

                Specify an array of string values to match this event if the actual value of ebsVolumeScanDetails is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("ebs_volume_scan_details")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.EbsVolumeScanDetails"], result)

            @builtins.property
            def event_first_seen(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventFirstSeen property.

                Specify an array of string values to match this event if the actual value of eventFirstSeen is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_first_seen")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_last_seen(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventLastSeen property.

                Specify an array of string values to match this event if the actual value of eventLastSeen is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_last_seen")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def evidence(
                self,
            ) -> typing.Optional["DetectorEvents.GuardDutyFinding.Evidence"]:
                '''(experimental) evidence property.

                Specify an array of string values to match this event if the actual value of evidence is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("evidence")
                return typing.cast(typing.Optional["DetectorEvents.GuardDutyFinding.Evidence"], result)

            @builtins.property
            def feature_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) featureName property.

                Specify an array of string values to match this event if the actual value of featureName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("feature_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def resource_role(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) resourceRole property.

                Specify an array of string values to match this event if the actual value of resourceRole is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("resource_role")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def service_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) serviceName property.

                Specify an array of string values to match this event if the actual value of serviceName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("service_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Service(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.TaskDetails",
            jsii_struct_bases=[],
            name_mapping={
                "arn": "arn",
                "containers": "containers",
                "created_at": "createdAt",
                "definition_arn": "definitionArn",
                "started_at": "startedAt",
                "started_by": "startedBy",
                "version": "version",
            },
        )
        class TaskDetails:
            def __init__(
                self,
                *,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                containers: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.TaskDetailsItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                definition_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
                started_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                version: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TaskDetails.

                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param containers: (experimental) containers property. Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param created_at: (experimental) createdAt property. Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param definition_arn: (experimental) definitionArn property. Specify an array of string values to match this event if the actual value of definitionArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param started_at: (experimental) startedAt property. Specify an array of string values to match this event if the actual value of startedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param started_by: (experimental) startedBy property. Specify an array of string values to match this event if the actual value of startedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param version: (experimental) version property. Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    task_details = guardduty_events.DetectorEvents.GuardDutyFinding.TaskDetails(
                        arn=["arn"],
                        containers=[guardduty_events.DetectorEvents.GuardDutyFinding.TaskDetailsItem(
                            image=["image"],
                            name=["name"]
                        )],
                        created_at=["createdAt"],
                        definition_arn=["definitionArn"],
                        started_at=["startedAt"],
                        started_by=["startedBy"],
                        version=["version"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0bb3f07ac9b72f8da76a9352b71e9138cc12333c71f6f0412555b802f9264702)
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                    check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                    check_type(argname="argument definition_arn", value=definition_arn, expected_type=type_hints["definition_arn"])
                    check_type(argname="argument started_at", value=started_at, expected_type=type_hints["started_at"])
                    check_type(argname="argument started_by", value=started_by, expected_type=type_hints["started_by"])
                    check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if arn is not None:
                    self._values["arn"] = arn
                if containers is not None:
                    self._values["containers"] = containers
                if created_at is not None:
                    self._values["created_at"] = created_at
                if definition_arn is not None:
                    self._values["definition_arn"] = definition_arn
                if started_at is not None:
                    self._values["started_at"] = started_at
                if started_by is not None:
                    self._values["started_by"] = started_by
                if version is not None:
                    self._values["version"] = version

            @builtins.property
            def arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) arn property.

                Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def containers(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.TaskDetailsItem"]]:
                '''(experimental) containers property.

                Specify an array of string values to match this event if the actual value of containers is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("containers")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.TaskDetailsItem"]], result)

            @builtins.property
            def created_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) createdAt property.

                Specify an array of string values to match this event if the actual value of createdAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("created_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def definition_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) definitionArn property.

                Specify an array of string values to match this event if the actual value of definitionArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("definition_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def started_at(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) startedAt property.

                Specify an array of string values to match this event if the actual value of startedAt is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("started_at")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def started_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) startedBy property.

                Specify an array of string values to match this event if the actual value of startedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("started_by")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) version property.

                Specify an array of string values to match this event if the actual value of version is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TaskDetails(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.TaskDetailsItem",
            jsii_struct_bases=[],
            name_mapping={"image": "image", "name": "name"},
        )
        class TaskDetailsItem:
            def __init__(
                self,
                *,
                image: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for TaskDetailsItem.

                :param image: (experimental) image property. Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    task_details_item = guardduty_events.DetectorEvents.GuardDutyFinding.TaskDetailsItem(
                        image=["image"],
                        name=["name"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__0c5ed7e420c5db12f37a5fd538443081565ea8fdc4ba6237cec19ee092d8f811)
                    check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if image is not None:
                    self._values["image"] = image
                if name is not None:
                    self._values["name"] = name

            @builtins.property
            def image(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) image property.

                Specify an array of string values to match this event if the actual value of image is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("image")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "TaskDetailsItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.ThreatDetectedByName",
            jsii_struct_bases=[],
            name_mapping={
                "item_count": "itemCount",
                "shortened": "shortened",
                "threat_names": "threatNames",
                "unique_threat_name_count": "uniqueThreatNameCount",
            },
        )
        class ThreatDetectedByName:
            def __init__(
                self,
                *,
                item_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                shortened: typing.Optional[typing.Sequence[builtins.str]] = None,
                threat_names: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                unique_threat_name_count: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ThreatDetectedByName.

                :param item_count: (experimental) itemCount property. Specify an array of string values to match this event if the actual value of itemCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param shortened: (experimental) shortened property. Specify an array of string values to match this event if the actual value of shortened is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param threat_names: (experimental) threatNames property. Specify an array of string values to match this event if the actual value of threatNames is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unique_threat_name_count: (experimental) uniqueThreatNameCount property. Specify an array of string values to match this event if the actual value of uniqueThreatNameCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    threat_detected_by_name = guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByName(
                        item_count=["itemCount"],
                        shortened=["shortened"],
                        threat_names=[guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem(
                            file_paths=[guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem(
                                file_name=["fileName"],
                                file_path=["filePath"],
                                hash=["hash"],
                                volume_arn=["volumeArn"]
                            )],
                            item_count=["itemCount"],
                            name=["name"],
                            severity=["severity"]
                        )],
                        unique_threat_name_count=["uniqueThreatNameCount"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__fd7a00ac8e9067897d6314bd2fa8456fbc5038a7b05831fa3395d92562bd2269)
                    check_type(argname="argument item_count", value=item_count, expected_type=type_hints["item_count"])
                    check_type(argname="argument shortened", value=shortened, expected_type=type_hints["shortened"])
                    check_type(argname="argument threat_names", value=threat_names, expected_type=type_hints["threat_names"])
                    check_type(argname="argument unique_threat_name_count", value=unique_threat_name_count, expected_type=type_hints["unique_threat_name_count"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if item_count is not None:
                    self._values["item_count"] = item_count
                if shortened is not None:
                    self._values["shortened"] = shortened
                if threat_names is not None:
                    self._values["threat_names"] = threat_names
                if unique_threat_name_count is not None:
                    self._values["unique_threat_name_count"] = unique_threat_name_count

            @builtins.property
            def item_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) itemCount property.

                Specify an array of string values to match this event if the actual value of itemCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("item_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def shortened(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) shortened property.

                Specify an array of string values to match this event if the actual value of shortened is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("shortened")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def threat_names(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem"]]:
                '''(experimental) threatNames property.

                Specify an array of string values to match this event if the actual value of threatNames is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("threat_names")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem"]], result)

            @builtins.property
            def unique_threat_name_count(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) uniqueThreatNameCount property.

                Specify an array of string values to match this event if the actual value of uniqueThreatNameCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unique_threat_name_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ThreatDetectedByName(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem",
            jsii_struct_bases=[],
            name_mapping={
                "file_paths": "filePaths",
                "item_count": "itemCount",
                "name": "name",
                "severity": "severity",
            },
        )
        class ThreatDetectedByNameItem:
            def __init__(
                self,
                *,
                file_paths: typing.Optional[typing.Sequence[typing.Union["DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem", typing.Dict[builtins.str, typing.Any]]]] = None,
                item_count: typing.Optional[typing.Sequence[builtins.str]] = None,
                name: typing.Optional[typing.Sequence[builtins.str]] = None,
                severity: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ThreatDetectedByNameItem.

                :param file_paths: (experimental) filePaths property. Specify an array of string values to match this event if the actual value of filePaths is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param item_count: (experimental) itemCount property. Specify an array of string values to match this event if the actual value of itemCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param name: (experimental) name property. Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param severity: (experimental) severity property. Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    threat_detected_by_name_item = guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem(
                        file_paths=[guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem(
                            file_name=["fileName"],
                            file_path=["filePath"],
                            hash=["hash"],
                            volume_arn=["volumeArn"]
                        )],
                        item_count=["itemCount"],
                        name=["name"],
                        severity=["severity"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__cd71a4ef7f341379a832d1ad3b566c26c83404f679320802e287d39880d94288)
                    check_type(argname="argument file_paths", value=file_paths, expected_type=type_hints["file_paths"])
                    check_type(argname="argument item_count", value=item_count, expected_type=type_hints["item_count"])
                    check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                    check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_paths is not None:
                    self._values["file_paths"] = file_paths
                if item_count is not None:
                    self._values["item_count"] = item_count
                if name is not None:
                    self._values["name"] = name
                if severity is not None:
                    self._values["severity"] = severity

            @builtins.property
            def file_paths(
                self,
            ) -> typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem"]]:
                '''(experimental) filePaths property.

                Specify an array of string values to match this event if the actual value of filePaths is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_paths")
                return typing.cast(typing.Optional[typing.List["DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem"]], result)

            @builtins.property
            def item_count(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) itemCount property.

                Specify an array of string values to match this event if the actual value of itemCount is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("item_count")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) name property.

                Specify an array of string values to match this event if the actual value of name is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def severity(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) severity property.

                Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("severity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ThreatDetectedByNameItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem",
            jsii_struct_bases=[],
            name_mapping={
                "file_name": "fileName",
                "file_path": "filePath",
                "hash": "hash",
                "volume_arn": "volumeArn",
            },
        )
        class ThreatDetectedByNameItemItem:
            def __init__(
                self,
                *,
                file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
                hash: typing.Optional[typing.Sequence[builtins.str]] = None,
                volume_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ThreatDetectedByNameItemItem.

                :param file_name: (experimental) fileName property. Specify an array of string values to match this event if the actual value of fileName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param file_path: (experimental) filePath property. Specify an array of string values to match this event if the actual value of filePath is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param hash: (experimental) hash property. Specify an array of string values to match this event if the actual value of hash is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param volume_arn: (experimental) volumeArn property. Specify an array of string values to match this event if the actual value of volumeArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    threat_detected_by_name_item_item = guardduty_events.DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem(
                        file_name=["fileName"],
                        file_path=["filePath"],
                        hash=["hash"],
                        volume_arn=["volumeArn"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a7d09c8c8e3db5b8545c93b8d94b15dc57902b474c1d75ddde4c5e9a7627e466)
                    check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
                    check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
                    check_type(argname="argument hash", value=hash, expected_type=type_hints["hash"])
                    check_type(argname="argument volume_arn", value=volume_arn, expected_type=type_hints["volume_arn"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if file_name is not None:
                    self._values["file_name"] = file_name
                if file_path is not None:
                    self._values["file_path"] = file_path
                if hash is not None:
                    self._values["hash"] = hash
                if volume_arn is not None:
                    self._values["volume_arn"] = volume_arn

            @builtins.property
            def file_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) fileName property.

                Specify an array of string values to match this event if the actual value of fileName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def file_path(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) filePath property.

                Specify an array of string values to match this event if the actual value of filePath is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("file_path")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def hash(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) hash property.

                Specify an array of string values to match this event if the actual value of hash is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("hash")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def volume_arn(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) volumeArn property.

                Specify an array of string values to match this event if the actual value of volumeArn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("volume_arn")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ThreatDetectedByNameItemItem(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount",
            jsii_struct_bases=[],
            name_mapping={"files": "files"},
        )
        class ThreatsDetectedItemCount:
            def __init__(
                self,
                *,
                files: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ThreatsDetectedItemCount.

                :param files: (experimental) files property. Specify an array of string values to match this event if the actual value of files is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    threats_detected_item_count = guardduty_events.DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount(
                        files=["files"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8cbe11b8247576ae9e482598a0f42c3f4aaee612a85808ad0750340dcbcb1351)
                    check_type(argname="argument files", value=files, expected_type=type_hints["files"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if files is not None:
                    self._values["files"] = files

            @builtins.property
            def files(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) files property.

                Specify an array of string values to match this event if the actual value of files is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("files")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ThreatsDetectedItemCount(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.UnusualBehavior",
            jsii_struct_bases=[],
            name_mapping={
                "is_unusual_user_identity": "isUnusualUserIdentity",
                "number_of_past24_hours_ap_is_bucket_profiling": "numberOfPast24HoursApIsBucketProfiling",
                "number_of_past24_hours_ap_is_bucket_user_identity_profiling": "numberOfPast24HoursApIsBucketUserIdentityProfiling",
                "number_of_past24_hours_ap_is_user_identity_profiling": "numberOfPast24HoursApIsUserIdentityProfiling",
                "unusual_ap_is_account_profiling": "unusualApIsAccountProfiling",
                "unusual_ap_is_user_identity_profiling": "unusualApIsUserIdentityProfiling",
                "unusual_as_ns_account_profiling": "unusualAsNsAccountProfiling",
                "unusual_as_ns_bucket_profiling": "unusualAsNsBucketProfiling",
                "unusual_as_ns_user_identity_profiling": "unusualAsNsUserIdentityProfiling",
                "unusual_buckets_account_profiling": "unusualBucketsAccountProfiling",
                "unusual_buckets_user_identity_profiling": "unusualBucketsUserIdentityProfiling",
                "unusual_user_agents_account_profiling": "unusualUserAgentsAccountProfiling",
                "unusual_user_agents_user_identity_profiling": "unusualUserAgentsUserIdentityProfiling",
                "unusual_user_names_account_profiling": "unusualUserNamesAccountProfiling",
                "unusual_user_names_bucket_profiling": "unusualUserNamesBucketProfiling",
                "unusual_user_types_account_profiling": "unusualUserTypesAccountProfiling",
            },
        )
        class UnusualBehavior:
            def __init__(
                self,
                *,
                is_unusual_user_identity: typing.Optional[typing.Sequence[builtins.str]] = None,
                number_of_past24_hours_ap_is_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                number_of_past24_hours_ap_is_bucket_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                number_of_past24_hours_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_ap_is_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_as_ns_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_as_ns_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_as_ns_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_buckets_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_buckets_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_user_agents_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_user_agents_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_user_names_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_user_names_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
                unusual_user_types_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for UnusualBehavior.

                :param is_unusual_user_identity: (experimental) isUnusualUserIdentity property. Specify an array of string values to match this event if the actual value of isUnusualUserIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param number_of_past24_hours_ap_is_bucket_profiling: (experimental) numberOfPast24HoursAPIsBucketProfiling property. Specify an array of string values to match this event if the actual value of numberOfPast24HoursAPIsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param number_of_past24_hours_ap_is_bucket_user_identity_profiling: (experimental) numberOfPast24HoursAPIsBucketUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of numberOfPast24HoursAPIsBucketUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param number_of_past24_hours_ap_is_user_identity_profiling: (experimental) numberOfPast24HoursAPIsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of numberOfPast24HoursAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_ap_is_account_profiling: (experimental) unusualAPIsAccountProfiling property. Specify an array of string values to match this event if the actual value of unusualAPIsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_ap_is_user_identity_profiling: (experimental) unusualAPIsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of unusualAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_as_ns_account_profiling: (experimental) unusualASNsAccountProfiling property. Specify an array of string values to match this event if the actual value of unusualASNsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_as_ns_bucket_profiling: (experimental) unusualASNsBucketProfiling property. Specify an array of string values to match this event if the actual value of unusualASNsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_as_ns_user_identity_profiling: (experimental) unusualASNsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of unusualASNsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_buckets_account_profiling: (experimental) unusualBucketsAccountProfiling property. Specify an array of string values to match this event if the actual value of unusualBucketsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_buckets_user_identity_profiling: (experimental) unusualBucketsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of unusualBucketsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_user_agents_account_profiling: (experimental) unusualUserAgentsAccountProfiling property. Specify an array of string values to match this event if the actual value of unusualUserAgentsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_user_agents_user_identity_profiling: (experimental) unusualUserAgentsUserIdentityProfiling property. Specify an array of string values to match this event if the actual value of unusualUserAgentsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_user_names_account_profiling: (experimental) unusualUserNamesAccountProfiling property. Specify an array of string values to match this event if the actual value of unusualUserNamesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_user_names_bucket_profiling: (experimental) unusualUserNamesBucketProfiling property. Specify an array of string values to match this event if the actual value of unusualUserNamesBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param unusual_user_types_account_profiling: (experimental) unusualUserTypesAccountProfiling property. Specify an array of string values to match this event if the actual value of unusualUserTypesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    unusual_behavior = guardduty_events.DetectorEvents.GuardDutyFinding.UnusualBehavior(
                        is_unusual_user_identity=["isUnusualUserIdentity"],
                        number_of_past24_hours_ap_is_bucket_profiling=["numberOfPast24HoursApIsBucketProfiling"],
                        number_of_past24_hours_ap_is_bucket_user_identity_profiling=["numberOfPast24HoursApIsBucketUserIdentityProfiling"],
                        number_of_past24_hours_ap_is_user_identity_profiling=["numberOfPast24HoursApIsUserIdentityProfiling"],
                        unusual_ap_is_account_profiling=["unusualApIsAccountProfiling"],
                        unusual_ap_is_user_identity_profiling=["unusualApIsUserIdentityProfiling"],
                        unusual_as_ns_account_profiling=["unusualAsNsAccountProfiling"],
                        unusual_as_ns_bucket_profiling=["unusualAsNsBucketProfiling"],
                        unusual_as_ns_user_identity_profiling=["unusualAsNsUserIdentityProfiling"],
                        unusual_buckets_account_profiling=["unusualBucketsAccountProfiling"],
                        unusual_buckets_user_identity_profiling=["unusualBucketsUserIdentityProfiling"],
                        unusual_user_agents_account_profiling=["unusualUserAgentsAccountProfiling"],
                        unusual_user_agents_user_identity_profiling=["unusualUserAgentsUserIdentityProfiling"],
                        unusual_user_names_account_profiling=["unusualUserNamesAccountProfiling"],
                        unusual_user_names_bucket_profiling=["unusualUserNamesBucketProfiling"],
                        unusual_user_types_account_profiling=["unusualUserTypesAccountProfiling"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__8ca3557d1ca44f8b19e87383c7d9c9a9b7c10891a0bd8752490adaee0f2726d2)
                    check_type(argname="argument is_unusual_user_identity", value=is_unusual_user_identity, expected_type=type_hints["is_unusual_user_identity"])
                    check_type(argname="argument number_of_past24_hours_ap_is_bucket_profiling", value=number_of_past24_hours_ap_is_bucket_profiling, expected_type=type_hints["number_of_past24_hours_ap_is_bucket_profiling"])
                    check_type(argname="argument number_of_past24_hours_ap_is_bucket_user_identity_profiling", value=number_of_past24_hours_ap_is_bucket_user_identity_profiling, expected_type=type_hints["number_of_past24_hours_ap_is_bucket_user_identity_profiling"])
                    check_type(argname="argument number_of_past24_hours_ap_is_user_identity_profiling", value=number_of_past24_hours_ap_is_user_identity_profiling, expected_type=type_hints["number_of_past24_hours_ap_is_user_identity_profiling"])
                    check_type(argname="argument unusual_ap_is_account_profiling", value=unusual_ap_is_account_profiling, expected_type=type_hints["unusual_ap_is_account_profiling"])
                    check_type(argname="argument unusual_ap_is_user_identity_profiling", value=unusual_ap_is_user_identity_profiling, expected_type=type_hints["unusual_ap_is_user_identity_profiling"])
                    check_type(argname="argument unusual_as_ns_account_profiling", value=unusual_as_ns_account_profiling, expected_type=type_hints["unusual_as_ns_account_profiling"])
                    check_type(argname="argument unusual_as_ns_bucket_profiling", value=unusual_as_ns_bucket_profiling, expected_type=type_hints["unusual_as_ns_bucket_profiling"])
                    check_type(argname="argument unusual_as_ns_user_identity_profiling", value=unusual_as_ns_user_identity_profiling, expected_type=type_hints["unusual_as_ns_user_identity_profiling"])
                    check_type(argname="argument unusual_buckets_account_profiling", value=unusual_buckets_account_profiling, expected_type=type_hints["unusual_buckets_account_profiling"])
                    check_type(argname="argument unusual_buckets_user_identity_profiling", value=unusual_buckets_user_identity_profiling, expected_type=type_hints["unusual_buckets_user_identity_profiling"])
                    check_type(argname="argument unusual_user_agents_account_profiling", value=unusual_user_agents_account_profiling, expected_type=type_hints["unusual_user_agents_account_profiling"])
                    check_type(argname="argument unusual_user_agents_user_identity_profiling", value=unusual_user_agents_user_identity_profiling, expected_type=type_hints["unusual_user_agents_user_identity_profiling"])
                    check_type(argname="argument unusual_user_names_account_profiling", value=unusual_user_names_account_profiling, expected_type=type_hints["unusual_user_names_account_profiling"])
                    check_type(argname="argument unusual_user_names_bucket_profiling", value=unusual_user_names_bucket_profiling, expected_type=type_hints["unusual_user_names_bucket_profiling"])
                    check_type(argname="argument unusual_user_types_account_profiling", value=unusual_user_types_account_profiling, expected_type=type_hints["unusual_user_types_account_profiling"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if is_unusual_user_identity is not None:
                    self._values["is_unusual_user_identity"] = is_unusual_user_identity
                if number_of_past24_hours_ap_is_bucket_profiling is not None:
                    self._values["number_of_past24_hours_ap_is_bucket_profiling"] = number_of_past24_hours_ap_is_bucket_profiling
                if number_of_past24_hours_ap_is_bucket_user_identity_profiling is not None:
                    self._values["number_of_past24_hours_ap_is_bucket_user_identity_profiling"] = number_of_past24_hours_ap_is_bucket_user_identity_profiling
                if number_of_past24_hours_ap_is_user_identity_profiling is not None:
                    self._values["number_of_past24_hours_ap_is_user_identity_profiling"] = number_of_past24_hours_ap_is_user_identity_profiling
                if unusual_ap_is_account_profiling is not None:
                    self._values["unusual_ap_is_account_profiling"] = unusual_ap_is_account_profiling
                if unusual_ap_is_user_identity_profiling is not None:
                    self._values["unusual_ap_is_user_identity_profiling"] = unusual_ap_is_user_identity_profiling
                if unusual_as_ns_account_profiling is not None:
                    self._values["unusual_as_ns_account_profiling"] = unusual_as_ns_account_profiling
                if unusual_as_ns_bucket_profiling is not None:
                    self._values["unusual_as_ns_bucket_profiling"] = unusual_as_ns_bucket_profiling
                if unusual_as_ns_user_identity_profiling is not None:
                    self._values["unusual_as_ns_user_identity_profiling"] = unusual_as_ns_user_identity_profiling
                if unusual_buckets_account_profiling is not None:
                    self._values["unusual_buckets_account_profiling"] = unusual_buckets_account_profiling
                if unusual_buckets_user_identity_profiling is not None:
                    self._values["unusual_buckets_user_identity_profiling"] = unusual_buckets_user_identity_profiling
                if unusual_user_agents_account_profiling is not None:
                    self._values["unusual_user_agents_account_profiling"] = unusual_user_agents_account_profiling
                if unusual_user_agents_user_identity_profiling is not None:
                    self._values["unusual_user_agents_user_identity_profiling"] = unusual_user_agents_user_identity_profiling
                if unusual_user_names_account_profiling is not None:
                    self._values["unusual_user_names_account_profiling"] = unusual_user_names_account_profiling
                if unusual_user_names_bucket_profiling is not None:
                    self._values["unusual_user_names_bucket_profiling"] = unusual_user_names_bucket_profiling
                if unusual_user_types_account_profiling is not None:
                    self._values["unusual_user_types_account_profiling"] = unusual_user_types_account_profiling

            @builtins.property
            def is_unusual_user_identity(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) isUnusualUserIdentity property.

                Specify an array of string values to match this event if the actual value of isUnusualUserIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("is_unusual_user_identity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def number_of_past24_hours_ap_is_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) numberOfPast24HoursAPIsBucketProfiling property.

                Specify an array of string values to match this event if the actual value of numberOfPast24HoursAPIsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("number_of_past24_hours_ap_is_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def number_of_past24_hours_ap_is_bucket_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) numberOfPast24HoursAPIsBucketUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of numberOfPast24HoursAPIsBucketUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("number_of_past24_hours_ap_is_bucket_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def number_of_past24_hours_ap_is_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) numberOfPast24HoursAPIsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of numberOfPast24HoursAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("number_of_past24_hours_ap_is_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_ap_is_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualAPIsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of unusualAPIsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_ap_is_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_ap_is_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualAPIsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of unusualAPIsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_ap_is_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_as_ns_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualASNsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of unusualASNsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_as_ns_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_as_ns_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualASNsBucketProfiling property.

                Specify an array of string values to match this event if the actual value of unusualASNsBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_as_ns_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_as_ns_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualASNsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of unusualASNsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_as_ns_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_buckets_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualBucketsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of unusualBucketsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_buckets_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_buckets_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualBucketsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of unusualBucketsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_buckets_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_user_agents_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualUserAgentsAccountProfiling property.

                Specify an array of string values to match this event if the actual value of unusualUserAgentsAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_user_agents_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_user_agents_user_identity_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualUserAgentsUserIdentityProfiling property.

                Specify an array of string values to match this event if the actual value of unusualUserAgentsUserIdentityProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_user_agents_user_identity_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_user_names_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualUserNamesAccountProfiling property.

                Specify an array of string values to match this event if the actual value of unusualUserNamesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_user_names_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_user_names_bucket_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualUserNamesBucketProfiling property.

                Specify an array of string values to match this event if the actual value of unusualUserNamesBucketProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_user_names_bucket_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def unusual_user_types_account_profiling(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) unusualUserTypesAccountProfiling property.

                Specify an array of string values to match this event if the actual value of unusualUserTypesAccountProfiling is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("unusual_user_types_account_profiling")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "UnusualBehavior(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_guardduty.events.DetectorEvents.GuardDutyFinding.UserAgent",
            jsii_struct_bases=[],
            name_mapping={
                "full_user_agent": "fullUserAgent",
                "user_agent_category": "userAgentCategory",
            },
        )
        class UserAgent:
            def __init__(
                self,
                *,
                full_user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent_category: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for UserAgent.

                :param full_user_agent: (experimental) fullUserAgent property. Specify an array of string values to match this event if the actual value of fullUserAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent_category: (experimental) userAgentCategory property. Specify an array of string values to match this event if the actual value of userAgentCategory is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_guardduty import events as guardduty_events
                    
                    user_agent = guardduty_events.DetectorEvents.GuardDutyFinding.UserAgent(
                        full_user_agent=["fullUserAgent"],
                        user_agent_category=["userAgentCategory"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__99011198967c4cbb9d0d2837404549ba216d0ef0de3f5171090f2d1aeb3369af)
                    check_type(argname="argument full_user_agent", value=full_user_agent, expected_type=type_hints["full_user_agent"])
                    check_type(argname="argument user_agent_category", value=user_agent_category, expected_type=type_hints["user_agent_category"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if full_user_agent is not None:
                    self._values["full_user_agent"] = full_user_agent
                if user_agent_category is not None:
                    self._values["user_agent_category"] = user_agent_category

            @builtins.property
            def full_user_agent(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) fullUserAgent property.

                Specify an array of string values to match this event if the actual value of fullUserAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("full_user_agent")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def user_agent_category(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userAgentCategory property.

                Specify an array of string values to match this event if the actual value of userAgentCategory is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_agent_category")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "UserAgent(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "DetectorEvents",
]

publication.publish()

def _typecheckingstub__ce2ed68f21b5de2203dd9426bc451d5e6795e90fab35300d03fd0111488cebde(
    detector_ref: _aws_cdk_interfaces_aws_guardduty_ceddda9d.IDetectorRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf230a77c1ae2921dd5e96d011b389bbba9d62e719e60888e273e27fe44456c(
    *,
    allows_public_read_access: typing.Optional[typing.Sequence[builtins.str]] = None,
    allows_public_write_access: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dec947658ddcc560e486e8ea48b738916cb3aeef4090706ff72bf649ef0244d(
    *,
    access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66a78f2cd84ba6f94ad571c83a29f5e4c05730084b58f89738a2147fbc98cf9(
    *,
    block_public_access: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.BlockPublicAccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3351eebe7a99b26e5472a7a96d38813de51f5a74c072263c2ecfd1af70f983e5(
    *,
    action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    aws_api_call_action: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.AwsApiCallAction1, typing.Dict[builtins.str, typing.Any]]] = None,
    dns_request_action: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.DnsRequestAction, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes_api_call_action: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.KubernetesApiCallAction, typing.Dict[builtins.str, typing.Any]]] = None,
    network_connection_action: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.NetworkConnectionAction, typing.Dict[builtins.str, typing.Any]]] = None,
    port_probe_action: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.PortProbeAction, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83891d8a1ae4766f914d9b450ccb3460200d6beaf98785d675a1509984c62215(
    *,
    additional_scanned_ports: typing.Optional[typing.Sequence[typing.Any]] = None,
    anomalies: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Anomalies, typing.Dict[builtins.str, typing.Any]]] = None,
    api_calls: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.AdditionalInfoItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    in_bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_port: typing.Optional[typing.Sequence[builtins.str]] = None,
    new_policy: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.NewPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    old_policy: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.OldPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    out_bytes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ports_scanned_sample: typing.Optional[typing.Sequence[jsii.Number]] = None,
    profiled_behavior: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.ProfiledBehavior, typing.Dict[builtins.str, typing.Any]]] = None,
    recent_credentials: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.AdditionalInfoItem1, typing.Dict[builtins.str, typing.Any]]]] = None,
    sample: typing.Optional[typing.Sequence[builtins.str]] = None,
    scanned_port: typing.Optional[typing.Sequence[builtins.str]] = None,
    threat_list_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    threat_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual: typing.Any = None,
    unusual_behavior: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.UnusualBehavior, typing.Dict[builtins.str, typing.Any]]] = None,
    unusual_protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.UserAgent, typing.Dict[builtins.str, typing.Any]]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc7f7c34d3564f3838357e7b6b92b9841158118a0ab3a941a4189e392d2bb5e(
    *,
    count: typing.Optional[typing.Sequence[builtins.str]] = None,
    first_seen: typing.Optional[typing.Sequence[builtins.str]] = None,
    last_seen: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3444e5abb7243a4fb235333e278865881a6fa69a7831cc691501ccd3db7894(
    *,
    access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3475e6a752314ad9d7d41dbd665e3b27acb284be2ab5ff8a03b1fea154ba3534(
    *,
    aws_cloud_trail_trail: typing.Optional[typing.Sequence[builtins.str]] = None,
    aws_ec2_instance: typing.Optional[typing.Sequence[builtins.str]] = None,
    aws_s3_bucket: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd37caf22cf4f8d9ad621aa1607bab78fe28120e96d5112e396dcdf661b3bc7(
    *,
    anomalous_ap_is: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3344c294298851525cefe304b9cd58006245abd6c242b431e2c81e54ea256dcc(
    *,
    affected_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    api: typing.Optional[typing.Sequence[builtins.str]] = None,
    caller_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    remote_ip_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.RemoteIpDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    service_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ccfd632960f96e322c8c9ca3db124bcb6aa4927363971bfb3bb95722a15ace(
    *,
    affected_resources: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.AffectedResources1, typing.Dict[builtins.str, typing.Any]]] = None,
    api: typing.Optional[typing.Sequence[builtins.str]] = None,
    caller_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    error_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    remote_account_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.RemoteAccountDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    remote_ip_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.RemoteIpDetails1, typing.Dict[builtins.str, typing.Any]]] = None,
    service_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b670adcd86867e24324da3675a0bfa35f089cbd4af64abbe6e205a44f47f239b(
    *,
    block_public_acls: typing.Optional[typing.Sequence[builtins.str]] = None,
    block_public_policy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignore_public_acls: typing.Optional[typing.Sequence[builtins.str]] = None,
    restrict_public_buckets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76dbf150835ed6cc815ec6861bf29a8b244cbef02b3bfc784971f28c53552820(
    *,
    access_control_list: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.AccessControlList, typing.Dict[builtins.str, typing.Any]]] = None,
    block_public_access: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.BlockPublicAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket_policy: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.AccessControlList, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a7e231cd730573bbafea735f5ad64c5dd6ce864321f0bb014fa4ae29a1f1d6(
    *,
    city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e7ec261905b9d0ac89c7d18a81c2082cc3e6909039278b62d040998de4f60b(
    *,
    city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63a2d3e84ac2f87b6b6a27652a831674085533d45e8b5382b61959dd397b21e(
    *,
    city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc56a271d8c4fa4be9d2f6c68f3abb6feab1a843e1d2a401dc89a8aee25a7233(
    *,
    city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e885c8e49e6007011ee14917881ac249d3066e903af472ff518d4a4a2b786985(
    *,
    city_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf080cb6d51ee16f9fdc9df79ae8cfa6166a026c9e56ad4ff99a5e1e16fe59f(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    image: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30237ff2810eabe9b20a7ca216ff919f8564c9226cf4b19adc58218d2b7cc70a(
    *,
    country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7143c4c38f9d665423b26efbb3bf504931b6cab1d8ed236ee3a0eb07b957b44(
    *,
    country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5f64998c17f42143afa6451d38f7b34ade8104dac8a15d44060874409627f2(
    *,
    country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36f66863f8321a333c574dbb8665235d3d9c75a77ac754f0821fb6fe27d8be7(
    *,
    country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb8267a05b15ef44790db97ea43fd868310a575ec61c4234dd51b59fd3b16cb(
    *,
    country_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa9d04c947a7f9b7d1dc525bc8a0150ab7c23e3a85d46023c05ee986adaf636(
    *,
    encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_master_key_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00c1ee0d9a007e987319e9979eb02a6ba0f22db7d9791761c212eaad7cc8991(
    *,
    blocked: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain: typing.Optional[typing.Sequence[builtins.str]] = None,
    protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b52118043d4134545238996820c8d60d7fc4334aceb115446f9fbb8db9cad41(
    *,
    scanned_volume_details: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.EbsVolumeDetailsItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    skipped_volume_details: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef6023280e9b1a85f0df8488ff161da532e17610266d37dea1f4e79dd4bcf77(
    *,
    device_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    kms_key_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_size_in_gb: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7545d367135761a6f7ce2ceda9af5f1fff0c33eae3c7967a4ec3f6fc43ad79db(
    *,
    scan_completed_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_detections: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.ScanDetections, typing.Dict[builtins.str, typing.Any]]] = None,
    scan_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    trigger_finding_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc1924b3ca3db2b07b18acebff7f916de793d2d831e0bf34b5d37a14316ae79(
    *,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.TaskDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9483d79a5a8974555a84597ab576164697c0f920416deb279b29ef4f56e5ee2e(
    *,
    key: typing.Optional[typing.Sequence[builtins.str]] = None,
    value: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83bcf2a34559dd7633e231cf69bedeb815ad7a7c71321813580a7c539470906(
    *,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c713fa355e53ae2622feceaa3d5f141b5684677ef577ba4bfe54f2fd479413(
    *,
    threat_intelligence_details: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.EvidenceItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7869f95b17e09579f07d4f67fa4a04c75909e8a3dedb0649ff88335a0ed2fb59(
    *,
    threat_list_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    threat_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160acc8f927005550ea8915557aa67945f6ab0578d496d3435af86316ff76146(
    *,
    lat: typing.Optional[typing.Sequence[builtins.str]] = None,
    lon: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a9b878db2b3fd6e87f26e6d06c036d4b5a1a1e66a1195fef6d158e9ff92561(
    *,
    lat: typing.Optional[typing.Sequence[builtins.str]] = None,
    lon: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f9aa2b12b06325b6d5ef217562a3b7f33f1b2b0a889b09c011766d5c188827(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
    partition: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Resource, typing.Dict[builtins.str, typing.Any]]] = None,
    schema_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    service: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Service, typing.Dict[builtins.str, typing.Any]]] = None,
    severity: typing.Optional[typing.Sequence[builtins.str]] = None,
    title: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    updated_at: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45ae80c621ac2524961891ffefd32357f6046228dfa0819678360015b43ce62(
    *,
    count: typing.Optional[typing.Sequence[builtins.str]] = None,
    severity: typing.Optional[typing.Sequence[builtins.str]] = None,
    threat_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe804246448e1ae068fd522757ffa163425487b4f3428ae8faf73d905867a1c3(
    *,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29357cb4ee83ef3773445fd3c784d164fc6e9fc8e452c1833fb8406872b34683(
    *,
    availability_zone: typing.Optional[typing.Sequence[builtins.str]] = None,
    iam_instance_profile: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.IamInstanceProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    image_description: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_state: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_interfaces: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.InstanceDetailsItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    outpost_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    platform: typing.Optional[typing.Sequence[builtins.str]] = None,
    product_codes: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.InstanceDetailsItem1, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047077e2ce9c98e6e9f13d7068c7731f8f39012c7ff88a99d7c011a0d3a907b1(
    *,
    ipv6_addresses: typing.Optional[typing.Sequence[typing.Any]] = None,
    network_interface_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_dns_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ip_addresses: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    public_dns_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    public_ip: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_groups: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.InstanceDetailsItemItem1, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc89e298878b8a28b8245311aa07dbeb9dc306e3bc065a4dced2f5b754a13b07(
    *,
    product_code_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    product_code_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24e67f58384287a948289bb21e6c213d5129c3b16b5815b05dc0050df08e60f(
    *,
    private_dns_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8891b8187664bb916b21624e6981d9f8081688a59b8d31a75f2660e66591d06(
    *,
    group_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d14dd55b9a564106dafc818ddb36588805b63c65748851e113c05417ae2f38f(
    *,
    parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    remote_ip_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.RemoteIpDetails2, typing.Dict[builtins.str, typing.Any]]] = None,
    request_uri: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_i_ps: typing.Optional[typing.Sequence[builtins.str]] = None,
    status_code: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    verb: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409cae5bbca7b6cb6cabc224fe780d4d83f5dd25df9c910a05be260c3be53774(
    *,
    kubernetes_user_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.KubernetesUserDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes_workload_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8937b582f66237c4ec5ea0ab48321159c15a52217d24c1a809f76720bba14db0(
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    uid: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a098779f496e4b53815f8c47bf0b8b2b8fa5cbbbc341874c66723759702dec4a(
    *,
    containers: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.KubernetesWorkloadDetailsItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    uid: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90fe6f2400a267e1531dddeba1c4c7470f5eea0df62f81666c03577cca335f4c(
    *,
    image: typing.Optional[typing.Sequence[builtins.str]] = None,
    image_prefix: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_context: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.SecurityContext, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb378356f2c43b68a8a1d29ebfb917d3768101efe33565e05a8cfe5c3c8be9a(
    *,
    ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d2ab04ea7b1a816e02a755b76704f186426582528331f0f4586216b6e40f37(
    *,
    ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abef2d8ccfb8d34439cc503f6fc9bbebba154f6e41556c2be8f000bb9858e1e(
    *,
    port: typing.Optional[typing.Sequence[builtins.str]] = None,
    port_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cdd652f596c32bf8369dc912536d71bc717904fd75e86f9d44430f0d36709d(
    *,
    port: typing.Optional[typing.Sequence[builtins.str]] = None,
    port_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625d2b273312166fdbc39412944782c1691d747e717ed3f372ee62c4f61cf710(
    *,
    blocked: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_direction: typing.Optional[typing.Sequence[builtins.str]] = None,
    local_ip_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.LocalIpDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    local_port_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.LocalPortDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    protocol: typing.Optional[typing.Sequence[builtins.str]] = None,
    remote_ip_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.RemoteIpDetails3, typing.Dict[builtins.str, typing.Any]]] = None,
    remote_port_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.RemotePortDetails, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefa27d7e1fc67feabdc0317ec400bda434620acd3d0e03be7fa507d98397f65(
    *,
    allow_users_to_change_password: typing.Optional[typing.Sequence[builtins.str]] = None,
    hard_expiry: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_password_age: typing.Optional[typing.Sequence[builtins.str]] = None,
    minimum_password_length: typing.Optional[typing.Sequence[builtins.str]] = None,
    password_reuse_prevention: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_lowercase_characters: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_symbols: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_uppercase_characters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a1c41b6ef82c76a2fa48612d00fe1940b5e12a2d12732562b867ddaa3c1cd5(
    *,
    allow_users_to_change_password: typing.Optional[typing.Sequence[builtins.str]] = None,
    hard_expiry: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_password_age: typing.Optional[typing.Sequence[builtins.str]] = None,
    minimum_password_length: typing.Optional[typing.Sequence[builtins.str]] = None,
    password_reuse_prevention: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_lowercase_characters: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_numbers: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_symbols: typing.Optional[typing.Sequence[builtins.str]] = None,
    require_uppercase_characters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce79719b930174499948ac310659403f89da2bf128714d06bdd5916164e91f4(
    *,
    asn: typing.Optional[typing.Sequence[builtins.str]] = None,
    asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
    isp: typing.Optional[typing.Sequence[builtins.str]] = None,
    org: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97245bf7dc97810e50807468d9bad6489379d07d09da600ba8a53ff0c3dedad0(
    *,
    asn: typing.Optional[typing.Sequence[builtins.str]] = None,
    asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
    isp: typing.Optional[typing.Sequence[builtins.str]] = None,
    org: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836d25b383f439608c2684e9268431c0490d501ed07137f684ca7d7adfb3f109(
    *,
    asn: typing.Optional[typing.Sequence[builtins.str]] = None,
    asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
    isp: typing.Optional[typing.Sequence[builtins.str]] = None,
    org: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dcc94ba2b3386031400acf9fa0466f6c6df9f1add8c70e0a54caecceab2678(
    *,
    asn: typing.Optional[typing.Sequence[builtins.str]] = None,
    asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
    isp: typing.Optional[typing.Sequence[builtins.str]] = None,
    org: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724a5a0b038a0630073c88b7192c03aa9bcbf5de3106924e2707ad1003ed8f2f(
    *,
    asn: typing.Optional[typing.Sequence[builtins.str]] = None,
    asn_org: typing.Optional[typing.Sequence[builtins.str]] = None,
    isp: typing.Optional[typing.Sequence[builtins.str]] = None,
    org: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa91b09c2725eef92d0244422b38c5550601262d07b695e8b23a14a44b8b407(
    *,
    id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b605bfb16386b0ae75ffed5dab0ac487890d4177e488aa4323faf8e7dfbcf1(
    *,
    account_level_permissions: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.AccountLevelPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
    bucket_level_permissions: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.BucketLevelPermissions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6b04c50dea6e36fb577a16af0c41a89426ed73039d0db2b4794e4569cd02b0(
    *,
    blocked: typing.Optional[typing.Sequence[builtins.str]] = None,
    port_probe_details: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.PortProbeActionItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a164d412cc1dec9080783cac00424fc458df1636a02ba64a7fe69406e2736b71(
    *,
    local_ip_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.LocalIpDetails1, typing.Dict[builtins.str, typing.Any]]] = None,
    local_port_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.LocalPortDetails1, typing.Dict[builtins.str, typing.Any]]] = None,
    remote_ip_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.RemoteIpDetails4, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f18247c965dfb9a54eed68047876b63935732fa10e624015d568ad935c36de5(
    *,
    frequent_profiled_ap_is_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_as_ns_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_as_ns_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_as_ns_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_buckets_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_buckets_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_user_agents_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_user_agents_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_user_names_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_user_names_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    frequent_profiled_user_types_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_ap_is_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_as_ns_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_as_ns_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_as_ns_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_buckets_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_buckets_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_user_agents_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_user_agents_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_user_names_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_user_names_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrequent_profiled_user_types_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_of_historical_daily_avg_ap_is_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_of_historical_daily_avg_ap_is_bucket_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_of_historical_daily_avg_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_of_historical_daily_max_ap_is_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_of_historical_daily_max_ap_is_bucket_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_of_historical_daily_max_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_ap_is_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_as_ns_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_as_ns_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_as_ns_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_buckets_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_buckets_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_user_agents_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_user_agents_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_user_names_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_user_names_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    rare_profiled_user_types_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be019c8462db9519eb1d9f5de31c19055d4ac3088d0091d4bd89a6b9721a42ec(
    *,
    effective_permission: typing.Optional[typing.Sequence[builtins.str]] = None,
    permission_configuration: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.PermissionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fd3cdf671e62c58347d5e709699aa7a0303e91a626bc45313cfc887e4e32a6(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    affiliated: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4914e8c1709d60da2023db68256bfd7362651bc0d5f2d8e094ee9450460333f2(
    *,
    city: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.City, typing.Dict[builtins.str, typing.Any]]] = None,
    country: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Country, typing.Dict[builtins.str, typing.Any]]] = None,
    geo_location: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.GeoLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Organization, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e3fce8091b03f60574411d0220ff033792d03bd0622d44c5407c65ba13ff67(
    *,
    city: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.City1, typing.Dict[builtins.str, typing.Any]]] = None,
    country: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Country1, typing.Dict[builtins.str, typing.Any]]] = None,
    geo_location: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.GeoLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Organization1, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d71e9efdd5679d0029316e6c525bc02503955e7b5eef9be05bc648ccf2a5e1(
    *,
    city: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.City2, typing.Dict[builtins.str, typing.Any]]] = None,
    country: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Country2, typing.Dict[builtins.str, typing.Any]]] = None,
    geo_location: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.GeoLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Organization2, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40feccc8bf09aef0318879909051495cece42bf865692c4e63036b38de135f4c(
    *,
    city: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.City3, typing.Dict[builtins.str, typing.Any]]] = None,
    country: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Country3, typing.Dict[builtins.str, typing.Any]]] = None,
    geo_location: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.GeoLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Organization3, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f479ea1916c9fb4efda1668face8d76356a362cdc7178c89c55d305ee1704f(
    *,
    city: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.City4, typing.Dict[builtins.str, typing.Any]]] = None,
    country: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Country4, typing.Dict[builtins.str, typing.Any]]] = None,
    geo_location: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.GeoLocation1, typing.Dict[builtins.str, typing.Any]]] = None,
    ip_address_v4: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Organization4, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ca6d507c2901eb356e5b2e2b0bcafa8477547b22db8cd6cc643698283fd4f7(
    *,
    port: typing.Optional[typing.Sequence[builtins.str]] = None,
    port_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d27074d7f9daad6d326e7f8d2fb49220e7494d3b522cb13133eef62d7a0b79d(
    *,
    access_key_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.AccessKeyDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    container_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.ContainerDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs_volume_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.EbsVolumeDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    ecs_cluster_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.EcsClusterDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    eks_cluster_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.EksClusterDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.InstanceDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.KubernetesDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_bucket_details: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.ResourceItem, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5b1ac95333036d79a6164e6f92176701f4dc757cf088f8079547cdb0462ec2(
    *,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_server_side_encryption: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.DefaultServerSideEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    owner: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Owner, typing.Dict[builtins.str, typing.Any]]] = None,
    public_access: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.PublicAccess, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.EcsClusterDetailsItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016ead5d197c9e60651c9e3ac6fdc113e22d737271a4a81e3ae806cc4a9fdf4e(
    *,
    highest_severity_threat_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.HighestSeverityThreatDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    scanned_item_count: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.ScannedItemCount, typing.Dict[builtins.str, typing.Any]]] = None,
    threat_detected_by_name: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.ThreatDetectedByName, typing.Dict[builtins.str, typing.Any]]] = None,
    threats_detected_item_count: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.ThreatsDetectedItemCount, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bede3607d3ef63971edc8cbfdb3fcb26dafc7a78ba567095d9f282ef8d8a352(
    *,
    files: typing.Optional[typing.Sequence[builtins.str]] = None,
    total_gb: typing.Optional[typing.Sequence[builtins.str]] = None,
    volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9378038c6bf58d1213cb7aec0f485556ef488c447dad819c6afcddc9c9cfe2(
    *,
    privileged: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338aadb3ef02cff7973f431c245179b88935141c6ccce3291ef06151c0effe77(
    *,
    action: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Action, typing.Dict[builtins.str, typing.Any]]] = None,
    additional_info: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.AdditionalInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    archived: typing.Optional[typing.Sequence[builtins.str]] = None,
    aws_api_call_action: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.AwsApiCallAction, typing.Dict[builtins.str, typing.Any]]] = None,
    count: typing.Optional[typing.Sequence[builtins.str]] = None,
    detector_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    ebs_volume_scan_details: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.EbsVolumeScanDetails, typing.Dict[builtins.str, typing.Any]]] = None,
    event_first_seen: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_last_seen: typing.Optional[typing.Sequence[builtins.str]] = None,
    evidence: typing.Optional[typing.Union[DetectorEvents.GuardDutyFinding.Evidence, typing.Dict[builtins.str, typing.Any]]] = None,
    feature_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_role: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb3f07ac9b72f8da76a9352b71e9138cc12333c71f6f0412555b802f9264702(
    *,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    containers: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.TaskDetailsItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    created_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    definition_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    started_at: typing.Optional[typing.Sequence[builtins.str]] = None,
    started_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5ed7e420c5db12f37a5fd538443081565ea8fdc4ba6237cec19ee092d8f811(
    *,
    image: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7a00ac8e9067897d6314bd2fa8456fbc5038a7b05831fa3395d92562bd2269(
    *,
    item_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    shortened: typing.Optional[typing.Sequence[builtins.str]] = None,
    threat_names: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    unique_threat_name_count: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd71a4ef7f341379a832d1ad3b566c26c83404f679320802e287d39880d94288(
    *,
    file_paths: typing.Optional[typing.Sequence[typing.Union[DetectorEvents.GuardDutyFinding.ThreatDetectedByNameItemItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    item_count: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[typing.Sequence[builtins.str]] = None,
    severity: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d09c8c8e3db5b8545c93b8d94b15dc57902b474c1d75ddde4c5e9a7627e466(
    *,
    file_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    hash: typing.Optional[typing.Sequence[builtins.str]] = None,
    volume_arn: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbe11b8247576ae9e482598a0f42c3f4aaee612a85808ad0750340dcbcb1351(
    *,
    files: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca3557d1ca44f8b19e87383c7d9c9a9b7c10891a0bd8752490adaee0f2726d2(
    *,
    is_unusual_user_identity: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_of_past24_hours_ap_is_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_of_past24_hours_ap_is_bucket_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    number_of_past24_hours_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_ap_is_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_ap_is_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_as_ns_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_as_ns_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_as_ns_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_buckets_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_buckets_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_user_agents_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_user_agents_user_identity_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_user_names_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_user_names_bucket_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
    unusual_user_types_account_profiling: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99011198967c4cbb9d0d2837404549ba216d0ef0de3f5171090f2d1aeb3369af(
    *,
    full_user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent_category: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
