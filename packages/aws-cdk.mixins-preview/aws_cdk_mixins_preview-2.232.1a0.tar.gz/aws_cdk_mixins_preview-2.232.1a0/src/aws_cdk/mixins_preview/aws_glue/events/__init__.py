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
import aws_cdk.interfaces.aws_glue as _aws_cdk_interfaces_aws_glue_ceddda9d


class DatabaseEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.events.DatabaseEvents",
):
    '''(experimental) EventBridge event patterns for Database.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_glue import events as glue_events
        from aws_cdk.interfaces import aws_glue as interfaces_glue
        
        # database_ref: interfaces_glue.IDatabaseRef
        
        database_events = glue_events.DatabaseEvents.from_database(database_ref)
    '''

    @jsii.member(jsii_name="fromDatabase")
    @builtins.classmethod
    def from_database(
        cls,
        database_ref: _aws_cdk_interfaces_aws_glue_ceddda9d.IDatabaseRef,
    ) -> "DatabaseEvents":
        '''(experimental) Create DatabaseEvents from a Database reference.

        :param database_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2d6630272f025e0bdf5a5049990f34233e994eee27d7e5c881306067d239d3)
            check_type(argname="argument database_ref", value=database_ref, expected_type=type_hints["database_ref"])
        return typing.cast("DatabaseEvents", jsii.sinvoke(cls, "fromDatabase", [database_ref]))

    @jsii.member(jsii_name="glueDataCatalogDatabaseStateChangePattern")
    def glue_data_catalog_database_state_change_pattern(
        self,
        *,
        changed_tables: typing.Optional[typing.Sequence[builtins.str]] = None,
        database_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        type_of_change: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Database Glue Data Catalog Database State Change.

        :param changed_tables: (experimental) changedTables property. Specify an array of string values to match this event if the actual value of changedTables is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param database_name: (experimental) databaseName property. Specify an array of string values to match this event if the actual value of databaseName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Database reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param type_of_change: (experimental) typeOfChange property. Specify an array of string values to match this event if the actual value of typeOfChange is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatabaseEvents.GlueDataCatalogDatabaseStateChange.GlueDataCatalogDatabaseStateChangeProps(
            changed_tables=changed_tables,
            database_name=database_name,
            event_metadata=event_metadata,
            type_of_change=type_of_change,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "glueDataCatalogDatabaseStateChangePattern", [options]))

    @jsii.member(jsii_name="glueDataCatalogTableStateChangePattern")
    def glue_data_catalog_table_state_change_pattern(
        self,
        *,
        changed_partitions: typing.Optional[typing.Sequence[builtins.str]] = None,
        database_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        table_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        type_of_change: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Database Glue Data Catalog Table State Change.

        :param changed_partitions: (experimental) changedPartitions property. Specify an array of string values to match this event if the actual value of changedPartitions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param database_name: (experimental) databaseName property. Specify an array of string values to match this event if the actual value of databaseName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Database reference
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param table_name: (experimental) tableName property. Specify an array of string values to match this event if the actual value of tableName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param type_of_change: (experimental) typeOfChange property. Specify an array of string values to match this event if the actual value of typeOfChange is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = DatabaseEvents.GlueDataCatalogTableStateChange.GlueDataCatalogTableStateChangeProps(
            changed_partitions=changed_partitions,
            database_name=database_name,
            event_metadata=event_metadata,
            table_name=table_name,
            type_of_change=type_of_change,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "glueDataCatalogTableStateChangePattern", [options]))

    class GlueDataCatalogDatabaseStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_glue.events.DatabaseEvents.GlueDataCatalogDatabaseStateChange",
    ):
        '''(experimental) aws.glue@GlueDataCatalogDatabaseStateChange event types for Database.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import events as glue_events
            
            glue_data_catalog_database_state_change = glue_events.DatabaseEvents.GlueDataCatalogDatabaseStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.DatabaseEvents.GlueDataCatalogDatabaseStateChange.GlueDataCatalogDatabaseStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "changed_tables": "changedTables",
                "database_name": "databaseName",
                "event_metadata": "eventMetadata",
                "type_of_change": "typeOfChange",
            },
        )
        class GlueDataCatalogDatabaseStateChangeProps:
            def __init__(
                self,
                *,
                changed_tables: typing.Optional[typing.Sequence[builtins.str]] = None,
                database_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                type_of_change: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Database aws.glue@GlueDataCatalogDatabaseStateChange event.

                :param changed_tables: (experimental) changedTables property. Specify an array of string values to match this event if the actual value of changedTables is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param database_name: (experimental) databaseName property. Specify an array of string values to match this event if the actual value of databaseName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Database reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param type_of_change: (experimental) typeOfChange property. Specify an array of string values to match this event if the actual value of typeOfChange is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    glue_data_catalog_database_state_change_props = glue_events.DatabaseEvents.GlueDataCatalogDatabaseStateChange.GlueDataCatalogDatabaseStateChangeProps(
                        changed_tables=["changedTables"],
                        database_name=["databaseName"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        type_of_change=["typeOfChange"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__94eaeccd9af954cc94b05f1e1493e8db487d1a4996de9a9f1c3dc0d928c91901)
                    check_type(argname="argument changed_tables", value=changed_tables, expected_type=type_hints["changed_tables"])
                    check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument type_of_change", value=type_of_change, expected_type=type_hints["type_of_change"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if changed_tables is not None:
                    self._values["changed_tables"] = changed_tables
                if database_name is not None:
                    self._values["database_name"] = database_name
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if type_of_change is not None:
                    self._values["type_of_change"] = type_of_change

            @builtins.property
            def changed_tables(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) changedTables property.

                Specify an array of string values to match this event if the actual value of changedTables is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("changed_tables")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def database_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) databaseName property.

                Specify an array of string values to match this event if the actual value of databaseName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Database reference

                :stability: experimental
                '''
                result = self._values.get("database_name")
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
            def type_of_change(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) typeOfChange property.

                Specify an array of string values to match this event if the actual value of typeOfChange is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type_of_change")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GlueDataCatalogDatabaseStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class GlueDataCatalogTableStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_glue.events.DatabaseEvents.GlueDataCatalogTableStateChange",
    ):
        '''(experimental) aws.glue@GlueDataCatalogTableStateChange event types for Database.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import events as glue_events
            
            glue_data_catalog_table_state_change = glue_events.DatabaseEvents.GlueDataCatalogTableStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.DatabaseEvents.GlueDataCatalogTableStateChange.GlueDataCatalogTableStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "changed_partitions": "changedPartitions",
                "database_name": "databaseName",
                "event_metadata": "eventMetadata",
                "table_name": "tableName",
                "type_of_change": "typeOfChange",
            },
        )
        class GlueDataCatalogTableStateChangeProps:
            def __init__(
                self,
                *,
                changed_partitions: typing.Optional[typing.Sequence[builtins.str]] = None,
                database_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                table_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                type_of_change: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Database aws.glue@GlueDataCatalogTableStateChange event.

                :param changed_partitions: (experimental) changedPartitions property. Specify an array of string values to match this event if the actual value of changedPartitions is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param database_name: (experimental) databaseName property. Specify an array of string values to match this event if the actual value of databaseName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Database reference
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param table_name: (experimental) tableName property. Specify an array of string values to match this event if the actual value of tableName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type_of_change: (experimental) typeOfChange property. Specify an array of string values to match this event if the actual value of typeOfChange is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    glue_data_catalog_table_state_change_props = glue_events.DatabaseEvents.GlueDataCatalogTableStateChange.GlueDataCatalogTableStateChangeProps(
                        changed_partitions=["changedPartitions"],
                        database_name=["databaseName"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        table_name=["tableName"],
                        type_of_change=["typeOfChange"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__4b5c53e8030abf756977c7d24f76d193e16b36e2cbe0de6f7d47819d08d7cb78)
                    check_type(argname="argument changed_partitions", value=changed_partitions, expected_type=type_hints["changed_partitions"])
                    check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                    check_type(argname="argument type_of_change", value=type_of_change, expected_type=type_hints["type_of_change"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if changed_partitions is not None:
                    self._values["changed_partitions"] = changed_partitions
                if database_name is not None:
                    self._values["database_name"] = database_name
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if table_name is not None:
                    self._values["table_name"] = table_name
                if type_of_change is not None:
                    self._values["type_of_change"] = type_of_change

            @builtins.property
            def changed_partitions(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) changedPartitions property.

                Specify an array of string values to match this event if the actual value of changedPartitions is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("changed_partitions")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def database_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) databaseName property.

                Specify an array of string values to match this event if the actual value of databaseName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Database reference

                :stability: experimental
                '''
                result = self._values.get("database_name")
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
            def table_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) tableName property.

                Specify an array of string values to match this event if the actual value of tableName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("table_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def type_of_change(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) typeOfChange property.

                Specify an array of string values to match this event if the actual value of typeOfChange is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("type_of_change")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GlueDataCatalogTableStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


class JobEvents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents",
):
    '''(experimental) EventBridge event patterns for Job.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_glue import events as glue_events
        from aws_cdk.interfaces import aws_glue as interfaces_glue
        
        # job_ref: interfaces_glue.IJobRef
        
        job_events = glue_events.JobEvents.from_job(job_ref)
    '''

    @jsii.member(jsii_name="fromJob")
    @builtins.classmethod
    def from_job(
        cls,
        job_ref: _aws_cdk_interfaces_aws_glue_ceddda9d.IJobRef,
    ) -> "JobEvents":
        '''(experimental) Create JobEvents from a Job reference.

        :param job_ref: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f340070d96881e1bd24abb24dc216429124aa474068a56ed67ba01781a3a2f3)
            check_type(argname="argument job_ref", value=job_ref, expected_type=type_hints["job_ref"])
        return typing.cast("JobEvents", jsii.sinvoke(cls, "fromJob", [job_ref]))

    @jsii.member(jsii_name="awsAPICallViaCloudTrailPattern")
    def aws_api_call_via_cloud_trail_pattern(
        self,
        *,
        aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        request_parameters: typing.Optional[typing.Union["JobEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        response_elements: typing.Optional[typing.Union["JobEvents.AWSAPICallViaCloudTrail.ResponseElements", typing.Dict[builtins.str, typing.Any]]] = None,
        source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_identity: typing.Optional[typing.Union["JobEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Job AWS API Call via CloudTrail.

        :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = JobEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
            aws_region=aws_region,
            event_id=event_id,
            event_metadata=event_metadata,
            event_name=event_name,
            event_source=event_source,
            event_time=event_time,
            event_type=event_type,
            event_version=event_version,
            request_id=request_id,
            request_parameters=request_parameters,
            response_elements=response_elements,
            source_ip_address=source_ip_address,
            user_agent=user_agent,
            user_identity=user_identity,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "awsAPICallViaCloudTrailPattern", [options]))

    @jsii.member(jsii_name="glueJobRunStatusPattern")
    def glue_job_run_status_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_run_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        message: typing.Optional[typing.Sequence[builtins.str]] = None,
        notification_condition: typing.Optional[typing.Union["JobEvents.GlueJobRunStatus.NotificationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Sequence[builtins.str]] = None,
        started_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        state: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Job Glue Job Run Status.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Job reference
        :param job_run_id: (experimental) jobRunId property. Specify an array of string values to match this event if the actual value of jobRunId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param notification_condition: (experimental) notificationCondition property. Specify an array of string values to match this event if the actual value of notificationCondition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param severity: (experimental) severity property. Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param started_on: (experimental) startedOn property. Specify an array of string values to match this event if the actual value of startedOn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = JobEvents.GlueJobRunStatus.GlueJobRunStatusProps(
            event_metadata=event_metadata,
            job_name=job_name,
            job_run_id=job_run_id,
            message=message,
            notification_condition=notification_condition,
            severity=severity,
            started_on=started_on,
            state=state,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "glueJobRunStatusPattern", [options]))

    @jsii.member(jsii_name="glueJobStateChangePattern")
    def glue_job_state_change_pattern(
        self,
        *,
        event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
        job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
        job_run_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        message: typing.Optional[typing.Sequence[builtins.str]] = None,
        severity: typing.Optional[typing.Sequence[builtins.str]] = None,
        state: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        '''(experimental) EventBridge event pattern for Job Glue Job State Change.

        :param event_metadata: (experimental) EventBridge event metadata. Default: - -
        :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Job reference
        :param job_run_id: (experimental) jobRunId property. Specify an array of string values to match this event if the actual value of jobRunId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param severity: (experimental) severity property. Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
        :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

        :stability: experimental
        '''
        options = JobEvents.GlueJobStateChange.GlueJobStateChangeProps(
            event_metadata=event_metadata,
            job_name=job_name,
            job_run_id=job_run_id,
            message=message,
            severity=severity,
            state=state,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.invoke(self, "glueJobStateChangePattern", [options]))

    class AWSAPICallViaCloudTrail(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.AWSAPICallViaCloudTrail",
    ):
        '''(experimental) aws.glue@AWSAPICallViaCloudTrail event types for Job.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import events as glue_events
            
            a_wSAPICall_via_cloud_trail = glue_events.JobEvents.AWSAPICallViaCloudTrail()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps",
            jsii_struct_bases=[],
            name_mapping={
                "aws_region": "awsRegion",
                "event_id": "eventId",
                "event_metadata": "eventMetadata",
                "event_name": "eventName",
                "event_source": "eventSource",
                "event_time": "eventTime",
                "event_type": "eventType",
                "event_version": "eventVersion",
                "request_id": "requestId",
                "request_parameters": "requestParameters",
                "response_elements": "responseElements",
                "source_ip_address": "sourceIpAddress",
                "user_agent": "userAgent",
                "user_identity": "userIdentity",
            },
        )
        class AWSAPICallViaCloudTrailProps:
            def __init__(
                self,
                *,
                aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
                event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                request_parameters: typing.Optional[typing.Union["JobEvents.AWSAPICallViaCloudTrail.RequestParameters", typing.Dict[builtins.str, typing.Any]]] = None,
                response_elements: typing.Optional[typing.Union["JobEvents.AWSAPICallViaCloudTrail.ResponseElements", typing.Dict[builtins.str, typing.Any]]] = None,
                source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_identity: typing.Optional[typing.Union["JobEvents.AWSAPICallViaCloudTrail.UserIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Props type for Job aws.glue@AWSAPICallViaCloudTrail event.

                :param aws_region: (experimental) awsRegion property. Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_id: (experimental) eventID property. Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param event_name: (experimental) eventName property. Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_source: (experimental) eventSource property. Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_time: (experimental) eventTime property. Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_type: (experimental) eventType property. Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param event_version: (experimental) eventVersion property. Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_id: (experimental) requestID property. Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param request_parameters: (experimental) requestParameters property. Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param response_elements: (experimental) responseElements property. Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param source_ip_address: (experimental) sourceIPAddress property. Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_agent: (experimental) userAgent property. Specify an array of string values to match this event if the actual value of userAgent is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_identity: (experimental) userIdentity property. Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    a_wSAPICall_via_cloud_trail_props = glue_events.JobEvents.AWSAPICallViaCloudTrail.AWSAPICallViaCloudTrailProps(
                        aws_region=["awsRegion"],
                        event_id=["eventId"],
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        event_name=["eventName"],
                        event_source=["eventSource"],
                        event_time=["eventTime"],
                        event_type=["eventType"],
                        event_version=["eventVersion"],
                        request_id=["requestId"],
                        request_parameters=glue_events.JobEvents.AWSAPICallViaCloudTrail.RequestParameters(
                            allocated_capacity=["allocatedCapacity"],
                            job_name=["jobName"]
                        ),
                        response_elements=glue_events.JobEvents.AWSAPICallViaCloudTrail.ResponseElements(
                            job_run_id=["jobRunId"]
                        ),
                        source_ip_address=["sourceIpAddress"],
                        user_agent=["userAgent"],
                        user_identity=glue_events.JobEvents.AWSAPICallViaCloudTrail.UserIdentity(
                            access_key_id=["accessKeyId"],
                            account_id=["accountId"],
                            arn=["arn"],
                            invoked_by=["invokedBy"],
                            principal_id=["principalId"],
                            session_context=glue_events.JobEvents.AWSAPICallViaCloudTrail.SessionContext(
                                attributes=glue_events.JobEvents.AWSAPICallViaCloudTrail.Attributes(
                                    creation_date=["creationDate"],
                                    mfa_authenticated=["mfaAuthenticated"]
                                ),
                                session_issuer=glue_events.JobEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                    account_id=["accountId"],
                                    arn=["arn"],
                                    principal_id=["principalId"],
                                    type=["type"],
                                    user_name=["userName"]
                                )
                            ),
                            type=["type"]
                        )
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(request_parameters, dict):
                    request_parameters = JobEvents.AWSAPICallViaCloudTrail.RequestParameters(**request_parameters)
                if isinstance(response_elements, dict):
                    response_elements = JobEvents.AWSAPICallViaCloudTrail.ResponseElements(**response_elements)
                if isinstance(user_identity, dict):
                    user_identity = JobEvents.AWSAPICallViaCloudTrail.UserIdentity(**user_identity)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__01813815731b39cd5d33d5a01518a5767906176a1e6279d28b9130430608e668)
                    check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
                    check_type(argname="argument event_id", value=event_id, expected_type=type_hints["event_id"])
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                    check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                    check_type(argname="argument event_time", value=event_time, expected_type=type_hints["event_time"])
                    check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
                    check_type(argname="argument event_version", value=event_version, expected_type=type_hints["event_version"])
                    check_type(argname="argument request_id", value=request_id, expected_type=type_hints["request_id"])
                    check_type(argname="argument request_parameters", value=request_parameters, expected_type=type_hints["request_parameters"])
                    check_type(argname="argument response_elements", value=response_elements, expected_type=type_hints["response_elements"])
                    check_type(argname="argument source_ip_address", value=source_ip_address, expected_type=type_hints["source_ip_address"])
                    check_type(argname="argument user_agent", value=user_agent, expected_type=type_hints["user_agent"])
                    check_type(argname="argument user_identity", value=user_identity, expected_type=type_hints["user_identity"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if aws_region is not None:
                    self._values["aws_region"] = aws_region
                if event_id is not None:
                    self._values["event_id"] = event_id
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if event_name is not None:
                    self._values["event_name"] = event_name
                if event_source is not None:
                    self._values["event_source"] = event_source
                if event_time is not None:
                    self._values["event_time"] = event_time
                if event_type is not None:
                    self._values["event_type"] = event_type
                if event_version is not None:
                    self._values["event_version"] = event_version
                if request_id is not None:
                    self._values["request_id"] = request_id
                if request_parameters is not None:
                    self._values["request_parameters"] = request_parameters
                if response_elements is not None:
                    self._values["response_elements"] = response_elements
                if source_ip_address is not None:
                    self._values["source_ip_address"] = source_ip_address
                if user_agent is not None:
                    self._values["user_agent"] = user_agent
                if user_identity is not None:
                    self._values["user_identity"] = user_identity

            @builtins.property
            def aws_region(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) awsRegion property.

                Specify an array of string values to match this event if the actual value of awsRegion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("aws_region")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventID property.

                Specify an array of string values to match this event if the actual value of eventID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_id")
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
            def event_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventName property.

                Specify an array of string values to match this event if the actual value of eventName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_source(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventSource property.

                Specify an array of string values to match this event if the actual value of eventSource is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_source")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_time(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventTime property.

                Specify an array of string values to match this event if the actual value of eventTime is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_time")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_type(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventType property.

                Specify an array of string values to match this event if the actual value of eventType is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_type")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def event_version(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) eventVersion property.

                Specify an array of string values to match this event if the actual value of eventVersion is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("event_version")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) requestID property.

                Specify an array of string values to match this event if the actual value of requestID is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def request_parameters(
                self,
            ) -> typing.Optional["JobEvents.AWSAPICallViaCloudTrail.RequestParameters"]:
                '''(experimental) requestParameters property.

                Specify an array of string values to match this event if the actual value of requestParameters is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("request_parameters")
                return typing.cast(typing.Optional["JobEvents.AWSAPICallViaCloudTrail.RequestParameters"], result)

            @builtins.property
            def response_elements(
                self,
            ) -> typing.Optional["JobEvents.AWSAPICallViaCloudTrail.ResponseElements"]:
                '''(experimental) responseElements property.

                Specify an array of string values to match this event if the actual value of responseElements is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("response_elements")
                return typing.cast(typing.Optional["JobEvents.AWSAPICallViaCloudTrail.ResponseElements"], result)

            @builtins.property
            def source_ip_address(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) sourceIPAddress property.

                Specify an array of string values to match this event if the actual value of sourceIPAddress is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("source_ip_address")
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
            def user_identity(
                self,
            ) -> typing.Optional["JobEvents.AWSAPICallViaCloudTrail.UserIdentity"]:
                '''(experimental) userIdentity property.

                Specify an array of string values to match this event if the actual value of userIdentity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_identity")
                return typing.cast(typing.Optional["JobEvents.AWSAPICallViaCloudTrail.UserIdentity"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "AWSAPICallViaCloudTrailProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.AWSAPICallViaCloudTrail.Attributes",
            jsii_struct_bases=[],
            name_mapping={
                "creation_date": "creationDate",
                "mfa_authenticated": "mfaAuthenticated",
            },
        )
        class Attributes:
            def __init__(
                self,
                *,
                creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
                mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for Attributes.

                :param creation_date: (experimental) creationDate property. Specify an array of string values to match this event if the actual value of creationDate is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param mfa_authenticated: (experimental) mfaAuthenticated property. Specify an array of string values to match this event if the actual value of mfaAuthenticated is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    attributes = glue_events.JobEvents.AWSAPICallViaCloudTrail.Attributes(
                        creation_date=["creationDate"],
                        mfa_authenticated=["mfaAuthenticated"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__443c9438b5292f5eba42a2144da45c65fcc5b4a9da24298c55ebcf9dfbf08c2c)
                    check_type(argname="argument creation_date", value=creation_date, expected_type=type_hints["creation_date"])
                    check_type(argname="argument mfa_authenticated", value=mfa_authenticated, expected_type=type_hints["mfa_authenticated"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if creation_date is not None:
                    self._values["creation_date"] = creation_date
                if mfa_authenticated is not None:
                    self._values["mfa_authenticated"] = mfa_authenticated

            @builtins.property
            def creation_date(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) creationDate property.

                Specify an array of string values to match this event if the actual value of creationDate is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("creation_date")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def mfa_authenticated(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) mfaAuthenticated property.

                Specify an array of string values to match this event if the actual value of mfaAuthenticated is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("mfa_authenticated")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "Attributes(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.AWSAPICallViaCloudTrail.RequestParameters",
            jsii_struct_bases=[],
            name_mapping={
                "allocated_capacity": "allocatedCapacity",
                "job_name": "jobName",
            },
        )
        class RequestParameters:
            def __init__(
                self,
                *,
                allocated_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for RequestParameters.

                :param allocated_capacity: (experimental) allocatedCapacity property. Specify an array of string values to match this event if the actual value of allocatedCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Job reference

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    request_parameters = glue_events.JobEvents.AWSAPICallViaCloudTrail.RequestParameters(
                        allocated_capacity=["allocatedCapacity"],
                        job_name=["jobName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__677e4378a192502b59dc7ef5b66aa87dfd5eb7801417dea410378d9e301ff2d1)
                    check_type(argname="argument allocated_capacity", value=allocated_capacity, expected_type=type_hints["allocated_capacity"])
                    check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if allocated_capacity is not None:
                    self._values["allocated_capacity"] = allocated_capacity
                if job_name is not None:
                    self._values["job_name"] = job_name

            @builtins.property
            def allocated_capacity(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) allocatedCapacity property.

                Specify an array of string values to match this event if the actual value of allocatedCapacity is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("allocated_capacity")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobName property.

                Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Job reference

                :stability: experimental
                '''
                result = self._values.get("job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "RequestParameters(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.AWSAPICallViaCloudTrail.ResponseElements",
            jsii_struct_bases=[],
            name_mapping={"job_run_id": "jobRunId"},
        )
        class ResponseElements:
            def __init__(
                self,
                *,
                job_run_id: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for ResponseElements.

                :param job_run_id: (experimental) jobRunId property. Specify an array of string values to match this event if the actual value of jobRunId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    response_elements = glue_events.JobEvents.AWSAPICallViaCloudTrail.ResponseElements(
                        job_run_id=["jobRunId"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__eda1cc39cd5305cddf4798fc81b76273bd0ed6d258b16b15d5e30f26c052ba34)
                    check_type(argname="argument job_run_id", value=job_run_id, expected_type=type_hints["job_run_id"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if job_run_id is not None:
                    self._values["job_run_id"] = job_run_id

            @builtins.property
            def job_run_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobRunId property.

                Specify an array of string values to match this event if the actual value of jobRunId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_run_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "ResponseElements(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.AWSAPICallViaCloudTrail.SessionContext",
            jsii_struct_bases=[],
            name_mapping={
                "attributes": "attributes",
                "session_issuer": "sessionIssuer",
            },
        )
        class SessionContext:
            def __init__(
                self,
                *,
                attributes: typing.Optional[typing.Union["JobEvents.AWSAPICallViaCloudTrail.Attributes", typing.Dict[builtins.str, typing.Any]]] = None,
                session_issuer: typing.Optional[typing.Union["JobEvents.AWSAPICallViaCloudTrail.SessionIssuer", typing.Dict[builtins.str, typing.Any]]] = None,
            ) -> None:
                '''(experimental) Type definition for SessionContext.

                :param attributes: (experimental) attributes property. Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_issuer: (experimental) sessionIssuer property. Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    session_context = glue_events.JobEvents.AWSAPICallViaCloudTrail.SessionContext(
                        attributes=glue_events.JobEvents.AWSAPICallViaCloudTrail.Attributes(
                            creation_date=["creationDate"],
                            mfa_authenticated=["mfaAuthenticated"]
                        ),
                        session_issuer=glue_events.JobEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                            account_id=["accountId"],
                            arn=["arn"],
                            principal_id=["principalId"],
                            type=["type"],
                            user_name=["userName"]
                        )
                    )
                '''
                if isinstance(attributes, dict):
                    attributes = JobEvents.AWSAPICallViaCloudTrail.Attributes(**attributes)
                if isinstance(session_issuer, dict):
                    session_issuer = JobEvents.AWSAPICallViaCloudTrail.SessionIssuer(**session_issuer)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__3bea9616c665d6753867eb2a26dfe90cf52468b37204fcf1c2440cf1288a63d2)
                    check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                    check_type(argname="argument session_issuer", value=session_issuer, expected_type=type_hints["session_issuer"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if attributes is not None:
                    self._values["attributes"] = attributes
                if session_issuer is not None:
                    self._values["session_issuer"] = session_issuer

            @builtins.property
            def attributes(
                self,
            ) -> typing.Optional["JobEvents.AWSAPICallViaCloudTrail.Attributes"]:
                '''(experimental) attributes property.

                Specify an array of string values to match this event if the actual value of attributes is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("attributes")
                return typing.cast(typing.Optional["JobEvents.AWSAPICallViaCloudTrail.Attributes"], result)

            @builtins.property
            def session_issuer(
                self,
            ) -> typing.Optional["JobEvents.AWSAPICallViaCloudTrail.SessionIssuer"]:
                '''(experimental) sessionIssuer property.

                Specify an array of string values to match this event if the actual value of sessionIssuer is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_issuer")
                return typing.cast(typing.Optional["JobEvents.AWSAPICallViaCloudTrail.SessionIssuer"], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SessionContext(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.AWSAPICallViaCloudTrail.SessionIssuer",
            jsii_struct_bases=[],
            name_mapping={
                "account_id": "accountId",
                "arn": "arn",
                "principal_id": "principalId",
                "type": "type",
                "user_name": "userName",
            },
        )
        class SessionIssuer:
            def __init__(
                self,
                *,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for SessionIssuer.

                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param user_name: (experimental) userName property. Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    session_issuer = glue_events.JobEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                        account_id=["accountId"],
                        arn=["arn"],
                        principal_id=["principalId"],
                        type=["type"],
                        user_name=["userName"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__f5f502338216ebffff257636b8f78c4e9b6c80ce30808dfff34a705f516fcaa5)
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                    check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if principal_id is not None:
                    self._values["principal_id"] = principal_id
                if type is not None:
                    self._values["type"] = type
                if user_name is not None:
                    self._values["user_name"] = user_name

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
            def principal_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) principalId property.

                Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("principal_id")
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
            def user_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) userName property.

                Specify an array of string values to match this event if the actual value of userName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("user_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "SessionIssuer(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.AWSAPICallViaCloudTrail.UserIdentity",
            jsii_struct_bases=[],
            name_mapping={
                "access_key_id": "accessKeyId",
                "account_id": "accountId",
                "arn": "arn",
                "invoked_by": "invokedBy",
                "principal_id": "principalId",
                "session_context": "sessionContext",
                "type": "type",
            },
        )
        class UserIdentity:
            def __init__(
                self,
                *,
                access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                arn: typing.Optional[typing.Sequence[builtins.str]] = None,
                invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
                principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                session_context: typing.Optional[typing.Union["JobEvents.AWSAPICallViaCloudTrail.SessionContext", typing.Dict[builtins.str, typing.Any]]] = None,
                type: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for UserIdentity.

                :param access_key_id: (experimental) accessKeyId property. Specify an array of string values to match this event if the actual value of accessKeyId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param account_id: (experimental) accountId property. Specify an array of string values to match this event if the actual value of accountId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param arn: (experimental) arn property. Specify an array of string values to match this event if the actual value of arn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param invoked_by: (experimental) invokedBy property. Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param principal_id: (experimental) principalId property. Specify an array of string values to match this event if the actual value of principalId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param session_context: (experimental) sessionContext property. Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param type: (experimental) type property. Specify an array of string values to match this event if the actual value of type is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    user_identity = glue_events.JobEvents.AWSAPICallViaCloudTrail.UserIdentity(
                        access_key_id=["accessKeyId"],
                        account_id=["accountId"],
                        arn=["arn"],
                        invoked_by=["invokedBy"],
                        principal_id=["principalId"],
                        session_context=glue_events.JobEvents.AWSAPICallViaCloudTrail.SessionContext(
                            attributes=glue_events.JobEvents.AWSAPICallViaCloudTrail.Attributes(
                                creation_date=["creationDate"],
                                mfa_authenticated=["mfaAuthenticated"]
                            ),
                            session_issuer=glue_events.JobEvents.AWSAPICallViaCloudTrail.SessionIssuer(
                                account_id=["accountId"],
                                arn=["arn"],
                                principal_id=["principalId"],
                                type=["type"],
                                user_name=["userName"]
                            )
                        ),
                        type=["type"]
                    )
                '''
                if isinstance(session_context, dict):
                    session_context = JobEvents.AWSAPICallViaCloudTrail.SessionContext(**session_context)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__ad728ebfad76f7c283ee3a288fe0d561c4dd0ed5ad44d61e029d5d07196ad324)
                    check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
                    check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                    check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                    check_type(argname="argument invoked_by", value=invoked_by, expected_type=type_hints["invoked_by"])
                    check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
                    check_type(argname="argument session_context", value=session_context, expected_type=type_hints["session_context"])
                    check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if access_key_id is not None:
                    self._values["access_key_id"] = access_key_id
                if account_id is not None:
                    self._values["account_id"] = account_id
                if arn is not None:
                    self._values["arn"] = arn
                if invoked_by is not None:
                    self._values["invoked_by"] = invoked_by
                if principal_id is not None:
                    self._values["principal_id"] = principal_id
                if session_context is not None:
                    self._values["session_context"] = session_context
                if type is not None:
                    self._values["type"] = type

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
            def invoked_by(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) invokedBy property.

                Specify an array of string values to match this event if the actual value of invokedBy is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("invoked_by")
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
            def session_context(
                self,
            ) -> typing.Optional["JobEvents.AWSAPICallViaCloudTrail.SessionContext"]:
                '''(experimental) sessionContext property.

                Specify an array of string values to match this event if the actual value of sessionContext is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("session_context")
                return typing.cast(typing.Optional["JobEvents.AWSAPICallViaCloudTrail.SessionContext"], result)

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
                return "UserIdentity(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class GlueJobRunStatus(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.GlueJobRunStatus",
    ):
        '''(experimental) aws.glue@GlueJobRunStatus event types for Job.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import events as glue_events
            
            glue_job_run_status = glue_events.JobEvents.GlueJobRunStatus()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.GlueJobRunStatus.GlueJobRunStatusProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "job_name": "jobName",
                "job_run_id": "jobRunId",
                "message": "message",
                "notification_condition": "notificationCondition",
                "severity": "severity",
                "started_on": "startedOn",
                "state": "state",
            },
        )
        class GlueJobRunStatusProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_run_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                message: typing.Optional[typing.Sequence[builtins.str]] = None,
                notification_condition: typing.Optional[typing.Union["JobEvents.GlueJobRunStatus.NotificationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
                severity: typing.Optional[typing.Sequence[builtins.str]] = None,
                started_on: typing.Optional[typing.Sequence[builtins.str]] = None,
                state: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Job aws.glue@GlueJobRunStatus event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Job reference
                :param job_run_id: (experimental) jobRunId property. Specify an array of string values to match this event if the actual value of jobRunId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param notification_condition: (experimental) notificationCondition property. Specify an array of string values to match this event if the actual value of notificationCondition is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param severity: (experimental) severity property. Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param started_on: (experimental) startedOn property. Specify an array of string values to match this event if the actual value of startedOn is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    glue_job_run_status_props = glue_events.JobEvents.GlueJobRunStatus.GlueJobRunStatusProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        job_name=["jobName"],
                        job_run_id=["jobRunId"],
                        message=["message"],
                        notification_condition=glue_events.JobEvents.GlueJobRunStatus.NotificationCondition(
                            notify_delay_after=["notifyDelayAfter"]
                        ),
                        severity=["severity"],
                        started_on=["startedOn"],
                        state=["state"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if isinstance(notification_condition, dict):
                    notification_condition = JobEvents.GlueJobRunStatus.NotificationCondition(**notification_condition)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__33c588d79dd14bdbfe08cc16185b4bb9b733af0fd95d99c8fe519102266b2fe9)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                    check_type(argname="argument job_run_id", value=job_run_id, expected_type=type_hints["job_run_id"])
                    check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                    check_type(argname="argument notification_condition", value=notification_condition, expected_type=type_hints["notification_condition"])
                    check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
                    check_type(argname="argument started_on", value=started_on, expected_type=type_hints["started_on"])
                    check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if job_name is not None:
                    self._values["job_name"] = job_name
                if job_run_id is not None:
                    self._values["job_run_id"] = job_run_id
                if message is not None:
                    self._values["message"] = message
                if notification_condition is not None:
                    self._values["notification_condition"] = notification_condition
                if severity is not None:
                    self._values["severity"] = severity
                if started_on is not None:
                    self._values["started_on"] = started_on
                if state is not None:
                    self._values["state"] = state

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
            def job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobName property.

                Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Job reference

                :stability: experimental
                '''
                result = self._values.get("job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_run_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobRunId property.

                Specify an array of string values to match this event if the actual value of jobRunId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_run_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message property.

                Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def notification_condition(
                self,
            ) -> typing.Optional["JobEvents.GlueJobRunStatus.NotificationCondition"]:
                '''(experimental) notificationCondition property.

                Specify an array of string values to match this event if the actual value of notificationCondition is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("notification_condition")
                return typing.cast(typing.Optional["JobEvents.GlueJobRunStatus.NotificationCondition"], result)

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
            def started_on(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) startedOn property.

                Specify an array of string values to match this event if the actual value of startedOn is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("started_on")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) state property.

                Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GlueJobRunStatusProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.GlueJobRunStatus.NotificationCondition",
            jsii_struct_bases=[],
            name_mapping={"notify_delay_after": "notifyDelayAfter"},
        )
        class NotificationCondition:
            def __init__(
                self,
                *,
                notify_delay_after: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Type definition for NotificationCondition.

                :param notify_delay_after: (experimental) NotifyDelayAfter property. Specify an array of string values to match this event if the actual value of NotifyDelayAfter is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    notification_condition = glue_events.JobEvents.GlueJobRunStatus.NotificationCondition(
                        notify_delay_after=["notifyDelayAfter"]
                    )
                '''
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__a87ffbe6d2038f08dee4ae9e6af5c29ddbb8f85114fa81a01ff62601825928d0)
                    check_type(argname="argument notify_delay_after", value=notify_delay_after, expected_type=type_hints["notify_delay_after"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if notify_delay_after is not None:
                    self._values["notify_delay_after"] = notify_delay_after

            @builtins.property
            def notify_delay_after(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) NotifyDelayAfter property.

                Specify an array of string values to match this event if the actual value of NotifyDelayAfter is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("notify_delay_after")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "NotificationCondition(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )

    class GlueJobStateChange(
        metaclass=jsii.JSIIMeta,
        jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.GlueJobStateChange",
    ):
        '''(experimental) aws.glue@GlueJobStateChange event types for Job.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import events as glue_events
            
            glue_job_state_change = glue_events.JobEvents.GlueJobStateChange()
        '''

        def __init__(self) -> None:
            '''
            :stability: experimental
            '''
            jsii.create(self.__class__, self, [])

        @jsii.data_type(
            jsii_type="@aws-cdk/mixins-preview.aws_glue.events.JobEvents.GlueJobStateChange.GlueJobStateChangeProps",
            jsii_struct_bases=[],
            name_mapping={
                "event_metadata": "eventMetadata",
                "job_name": "jobName",
                "job_run_id": "jobRunId",
                "message": "message",
                "severity": "severity",
                "state": "state",
            },
        )
        class GlueJobStateChangeProps:
            def __init__(
                self,
                *,
                event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
                job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
                job_run_id: typing.Optional[typing.Sequence[builtins.str]] = None,
                message: typing.Optional[typing.Sequence[builtins.str]] = None,
                severity: typing.Optional[typing.Sequence[builtins.str]] = None,
                state: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                '''(experimental) Props type for Job aws.glue@GlueJobStateChange event.

                :param event_metadata: (experimental) EventBridge event metadata. Default: - -
                :param job_name: (experimental) jobName property. Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Filter with the Job reference
                :param job_run_id: (experimental) jobRunId property. Specify an array of string values to match this event if the actual value of jobRunId is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param message: (experimental) message property. Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param severity: (experimental) severity property. Specify an array of string values to match this event if the actual value of severity is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field
                :param state: (experimental) state property. Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match`` for more advanced matching options. Default: - Do not filter on this field

                :stability: experimental
                :exampleMetadata: fixture=_generated

                Example::

                    # The code below shows an example of how to instantiate this type.
                    # The values are placeholders you should change.
                    from aws_cdk.mixins_preview.aws_glue import events as glue_events
                    
                    glue_job_state_change_props = glue_events.JobEvents.GlueJobStateChange.GlueJobStateChangeProps(
                        event_metadata=AWSEventMetadataProps(
                            region=["region"],
                            resources=["resources"],
                            version=["version"]
                        ),
                        job_name=["jobName"],
                        job_run_id=["jobRunId"],
                        message=["message"],
                        severity=["severity"],
                        state=["state"]
                    )
                '''
                if isinstance(event_metadata, dict):
                    event_metadata = _aws_cdk_ceddda9d.AWSEventMetadataProps(**event_metadata)
                if __debug__:
                    type_hints = typing.get_type_hints(_typecheckingstub__9a246e796f72c762c9e80b9c7e3ea080a2befe0996b6e7eeae89bbd1f5f45577)
                    check_type(argname="argument event_metadata", value=event_metadata, expected_type=type_hints["event_metadata"])
                    check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                    check_type(argname="argument job_run_id", value=job_run_id, expected_type=type_hints["job_run_id"])
                    check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                    check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
                    check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                self._values: typing.Dict[builtins.str, typing.Any] = {}
                if event_metadata is not None:
                    self._values["event_metadata"] = event_metadata
                if job_name is not None:
                    self._values["job_name"] = job_name
                if job_run_id is not None:
                    self._values["job_run_id"] = job_run_id
                if message is not None:
                    self._values["message"] = message
                if severity is not None:
                    self._values["severity"] = severity
                if state is not None:
                    self._values["state"] = state

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
            def job_name(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobName property.

                Specify an array of string values to match this event if the actual value of jobName is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Filter with the Job reference

                :stability: experimental
                '''
                result = self._values.get("job_name")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def job_run_id(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) jobRunId property.

                Specify an array of string values to match this event if the actual value of jobRunId is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("job_run_id")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            @builtins.property
            def message(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) message property.

                Specify an array of string values to match this event if the actual value of message is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("message")
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
            def state(self) -> typing.Optional[typing.List[builtins.str]]:
                '''(experimental) state property.

                Specify an array of string values to match this event if the actual value of state is one of the values in the array. Use one of the constructors on the ``aws_events.Match``  for more advanced matching options.

                :default: - Do not filter on this field

                :stability: experimental
                '''
                result = self._values.get("state")
                return typing.cast(typing.Optional[typing.List[builtins.str]], result)

            def __eq__(self, rhs: typing.Any) -> builtins.bool:
                return isinstance(rhs, self.__class__) and rhs._values == self._values

            def __ne__(self, rhs: typing.Any) -> builtins.bool:
                return not (rhs == self)

            def __repr__(self) -> str:
                return "GlueJobStateChangeProps(%s)" % ", ".join(
                    k + "=" + repr(v) for k, v in self._values.items()
                )


__all__ = [
    "DatabaseEvents",
    "JobEvents",
]

publication.publish()

def _typecheckingstub__1d2d6630272f025e0bdf5a5049990f34233e994eee27d7e5c881306067d239d3(
    database_ref: _aws_cdk_interfaces_aws_glue_ceddda9d.IDatabaseRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94eaeccd9af954cc94b05f1e1493e8db487d1a4996de9a9f1c3dc0d928c91901(
    *,
    changed_tables: typing.Optional[typing.Sequence[builtins.str]] = None,
    database_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    type_of_change: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5c53e8030abf756977c7d24f76d193e16b36e2cbe0de6f7d47819d08d7cb78(
    *,
    changed_partitions: typing.Optional[typing.Sequence[builtins.str]] = None,
    database_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    table_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    type_of_change: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f340070d96881e1bd24abb24dc216429124aa474068a56ed67ba01781a3a2f3(
    job_ref: _aws_cdk_interfaces_aws_glue_ceddda9d.IJobRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01813815731b39cd5d33d5a01518a5767906176a1e6279d28b9130430608e668(
    *,
    aws_region: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    event_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_source: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_time: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    event_version: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    request_parameters: typing.Optional[typing.Union[JobEvents.AWSAPICallViaCloudTrail.RequestParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    response_elements: typing.Optional[typing.Union[JobEvents.AWSAPICallViaCloudTrail.ResponseElements, typing.Dict[builtins.str, typing.Any]]] = None,
    source_ip_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_agent: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_identity: typing.Optional[typing.Union[JobEvents.AWSAPICallViaCloudTrail.UserIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443c9438b5292f5eba42a2144da45c65fcc5b4a9da24298c55ebcf9dfbf08c2c(
    *,
    creation_date: typing.Optional[typing.Sequence[builtins.str]] = None,
    mfa_authenticated: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677e4378a192502b59dc7ef5b66aa87dfd5eb7801417dea410378d9e301ff2d1(
    *,
    allocated_capacity: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda1cc39cd5305cddf4798fc81b76273bd0ed6d258b16b15d5e30f26c052ba34(
    *,
    job_run_id: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bea9616c665d6753867eb2a26dfe90cf52468b37204fcf1c2440cf1288a63d2(
    *,
    attributes: typing.Optional[typing.Union[JobEvents.AWSAPICallViaCloudTrail.Attributes, typing.Dict[builtins.str, typing.Any]]] = None,
    session_issuer: typing.Optional[typing.Union[JobEvents.AWSAPICallViaCloudTrail.SessionIssuer, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f502338216ebffff257636b8f78c4e9b6c80ce30808dfff34a705f516fcaa5(
    *,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_name: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad728ebfad76f7c283ee3a288fe0d561c4dd0ed5ad44d61e029d5d07196ad324(
    *,
    access_key_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    account_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    arn: typing.Optional[typing.Sequence[builtins.str]] = None,
    invoked_by: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_context: typing.Optional[typing.Union[JobEvents.AWSAPICallViaCloudTrail.SessionContext, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c588d79dd14bdbfe08cc16185b4bb9b733af0fd95d99c8fe519102266b2fe9(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_run_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    message: typing.Optional[typing.Sequence[builtins.str]] = None,
    notification_condition: typing.Optional[typing.Union[JobEvents.GlueJobRunStatus.NotificationCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    severity: typing.Optional[typing.Sequence[builtins.str]] = None,
    started_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    state: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87ffbe6d2038f08dee4ae9e6af5c29ddbb8f85114fa81a01ff62601825928d0(
    *,
    notify_delay_after: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a246e796f72c762c9e80b9c7e3ea080a2befe0996b6e7eeae89bbd1f5f45577(
    *,
    event_metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.AWSEventMetadataProps, typing.Dict[builtins.str, typing.Any]]] = None,
    job_name: typing.Optional[typing.Sequence[builtins.str]] = None,
    job_run_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    message: typing.Optional[typing.Sequence[builtins.str]] = None,
    severity: typing.Optional[typing.Sequence[builtins.str]] = None,
    state: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
