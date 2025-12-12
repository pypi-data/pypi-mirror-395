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
import aws_cdk.interfaces.aws_workspaces as _aws_cdk_interfaces_aws_workspaces_ceddda9d


class WorkspaceEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_workspaces.events.WorkspaceEvents",
):
    '''(experimental) EventBridge event patterns for Workspace.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_workspaces import events as workspaces_events
        from aws_cdk.interfaces import aws_workspaces as interfaces_workspaces
        
        # workspace_ref: interfaces_workspaces.IWorkspaceRef
        
        workspace_events = workspaces_events.WorkspaceEvents.from_workspace(workspace_ref)
    '''

    @jsii.member(jsii_name="fromWorkspace")
    @builtins.classmethod
    def from_workspace(
        cls,
        workspace_ref: _aws_cdk_interfaces_aws_workspaces_ceddda9d.IWorkspaceRef,
    ) -> "WorkspaceEvents":
        '''(experimental) Create WorkspaceEvents from a Workspace reference.

        :param workspace_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f55770025c7a2318556b5ed2d5f24989cc0696953f2ca480174c03511eee48)
            check_type(argname="argument workspace_ref", value=workspace_ref, expected_type=type_hints["workspace_ref"])
        return typing.cast("WorkspaceEvents", jsii.sinvoke(cls, "fromWorkspace", [workspace_ref]))

    @jsii.member(jsii_name="workSpacesAccessPattern")
    def work_spaces_access_pattern(
        self,
        *,
        action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_platform: typing.Optional[typing.Sequence[builtins.str]] = None,
        directory_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        login_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        workspace_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        workspaces_client_product_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Workspace WorkSpaces Access.

        :param action_type: (experimental) actionType property. Specify an array of string values to match this event if the actual value of actionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param client_ip_address: (experimental) clientIpAddress property. Specify an array of string values to match this event if the actual value of clientIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param client_platform: (experimental) clientPlatform property. Specify an array of string values to match this event if the actual value of clientPlatform is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param directory_id: (experimental) directoryId property. Specify an array of string values to match this event if the actual value of directoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param login_time: (experimental) loginTime property. Specify an array of string values to match this event if the actual value of loginTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param workspace_id: (experimental) workspaceId property. Specify an array of string values to match this event if the actual value of workspaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Workspace reference
        :param workspaces_client_product_name: (experimental) workspacesClientProductName property. Specify an array of string values to match this event if the actual value of workspacesClientProductName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = WorkspaceEvents.WorkSpacesAccess.WorkSpacesAccessProps(
            action_type=action_type,
            client_ip_address=client_ip_address,
            client_platform=client_platform,
            directory_id=directory_id,
            event_metadata=event_metadata,
            login_time=login_time,
            workspace_id=workspace_id,
            workspaces_client_product_name=workspaces_client_product_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "workSpacesAccessPattern", [options]))

    class WorkSpacesAccess(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_workspaces.events.WorkspaceEvents.WorkSpacesAccess",
    ):
        '''(experimental) aws.workspaces@WorkSpacesAccess event types for Workspace.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_workspaces import events as workspaces_events
            
            work_spaces_access = workspaces_events.WorkspaceEvents.WorkSpacesAccess()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_workspaces.events.WorkspaceEvents.WorkSpacesAccess.WorkSpacesAccessProps",
            jsii_struct_bases=[],
            name_mapping={
                "action_type": "actionType",
                "client_ip_address": "clientIpAddress",
                "client_platform": "clientPlatform",
                "directory_id": "directoryId",
                "event_metadata": "eventMetadata",
                "login_time": "loginTime",
                "workspace_id": "workspaceId",
                "workspaces_client_product_name": "workspacesClientProductName",
            },
        )
        class WorkSpacesAccessProps:
            def __init__(
                self,
                *,
                action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                client_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                client_platform: typing.Optional[typing.Sequence[builtins.str]] = None,
                directory_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                login_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                workspace_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                workspaces_client_product_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Workspace aws.workspaces@WorkSpacesAccess event.

                :param action_type: (experimental) actionType property. Specify an array of string values to match this event if the actual value of actionType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_ip_address: (experimental) clientIpAddress property. Specify an array of string values to match this event if the actual value of clientIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param client_platform: (experimental) clientPlatform property. Specify an array of string values to match this event if the actual value of clientPlatform is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param directory_id: (experimental) directoryId property. Specify an array of string values to match this event if the actual value of directoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param login_time: (experimental) loginTime property. Specify an array of string values to match this event if the actual value of loginTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param workspace_id: (experimental) workspaceId property. Specify an array of string values to match this event if the actual value of workspaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Workspace reference
                :param workspaces_client_product_name: (experimental) workspacesClientProductName property. Specify an array of string values to match this event if the actual value of workspacesClientProductName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_workspaces import events as workspaces_events
                    
                    work_spaces_access_props = workspaces_events.WorkspaceEvents.WorkSpacesAccess.WorkSpacesAccessProps(
                        action_type=["actionType"],
                        client_ip_address=["clientIpAddress"],
                        client_platform=["clientPlatform"],
                        directory_id=["directoryId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        login_time=["loginTime"],
                        workspace_id=["workspaceId"],
                        workspaces_client_product_name=["workspacesClientProductName"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__b0cd0c9c45edb4cabf80e51c1ff893230defbf31e8c9ea0de25f838da6dc107e)
                    check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
                    check_type(argname="argument client_ip_address", value=client_ip_address, expected_type=type_hints["client_ip_address"])
                    check_type(argname="argument client_platform", value=client_platform, expected_type=type_hints["client_platform"])
                    check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument login_time", value=login_time, expected_type=type_hints["login_time"])
                    check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
                    check_type(argname="argument workspaces_client_product_name", value=workspaces_client_product_name, expected_type=type_hints["workspaces_client_product_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if action_type is not None:
                    self._values["action_type"] = action_type
                if client_ip_address is not None:
                    self._values["client_ip_address"] = client_ip_address
                if client_platform is not None:
                    self._values["client_platform"] = client_platform
                if directory_id is not None:
                    self._values["directory_id"] = directory_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if login_time is not None:
                    self._values["login_time"] = login_time
                if workspace_id is not None:
                    self._values["workspace_id"] = workspace_id
                if workspaces_client_product_name is not None:
                    self._values["workspaces_client_product_name"] = workspaces_client_product_name

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
            def client_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clientIpAddress property.

                Specify an array of string values to match this event if the actual value of clientIpAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_ip_address")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def client_platform(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) clientPlatform property.

                Specify an array of string values to match this event if the actual value of clientPlatform is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("client_platform")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def directory_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) directoryId property.

                Specify an array of string values to match this event if the actual value of directoryId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("directory_id")
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
            def login_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) loginTime property.

                Specify an array of string values to match this event if the actual value of loginTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("login_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def workspace_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) workspaceId property.

                Specify an array of string values to match this event if the actual value of workspaceId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Workspace reference

                :stability: experimental
                '''
                result = self._values.get("workspace_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def workspaces_client_product_name(
                self,
            ) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) workspacesClientProductName property.

                Specify an array of string values to match this event if the actual value of workspacesClientProductName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("workspaces_client_product_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "WorkSpacesAccessProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "WorkspaceEvents",
]

publication.publish()

def _typecheckingstub__e8f55770025c7a2318556b5ed2d5f24989cc0696953f2ca480174c03511eee48(
    workspace_ref: _aws_cdk_interfaces_aws_workspaces_ceddda9d.IWorkspaceRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0cd0c9c45edb4cabf80e51c1ff893230defbf31e8c9ea0de25f838da6dc107e(
    *,
    action_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_platform: typing.Optional[typing.Sequence[builtins.str]] = None,
    directory_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    login_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    workspace_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    workspaces_client_product_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
