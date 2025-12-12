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
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnCapacityReservationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_assignment_configuration": "capacityAssignmentConfiguration",
        "name": "name",
        "tags": "tags",
        "target_dpus": "targetDpus",
    },
)
class CfnCapacityReservationMixinProps:
    def __init__(
        self,
        *,
        capacity_assignment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapacityReservationPropsMixin.CapacityAssignmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_dpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnCapacityReservationPropsMixin.

        :param capacity_assignment_configuration: Assigns Athena workgroups (and hence their queries) to capacity reservations. A capacity reservation can have only one capacity assignment configuration, but the capacity assignment configuration can be made up of multiple individual assignments. Each assignment specifies how Athena queries can consume capacity from the capacity reservation that their workgroup is mapped to.
        :param name: The name of the capacity reservation.
        :param tags: An array of key-value pairs to apply to the capacity reservation. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param target_dpus: The number of data processing units requested.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-capacityreservation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
            
            cfn_capacity_reservation_mixin_props = athena_mixins.CfnCapacityReservationMixinProps(
                capacity_assignment_configuration=athena_mixins.CfnCapacityReservationPropsMixin.CapacityAssignmentConfigurationProperty(
                    capacity_assignments=[athena_mixins.CfnCapacityReservationPropsMixin.CapacityAssignmentProperty(
                        workgroup_names=["workgroupNames"]
                    )]
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_dpus=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ee2c7975f956dfc7e9b625720d72562025a14f8526a764b4dec46d90d6bcb0)
            check_type(argname="argument capacity_assignment_configuration", value=capacity_assignment_configuration, expected_type=type_hints["capacity_assignment_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_dpus", value=target_dpus, expected_type=type_hints["target_dpus"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity_assignment_configuration is not None:
            self._values["capacity_assignment_configuration"] = capacity_assignment_configuration
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if target_dpus is not None:
            self._values["target_dpus"] = target_dpus

    @builtins.property
    def capacity_assignment_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityReservationPropsMixin.CapacityAssignmentConfigurationProperty"]]:
        '''Assigns Athena workgroups (and hence their queries) to capacity reservations.

        A capacity reservation can have only one capacity assignment configuration, but the capacity assignment configuration can be made up of multiple individual assignments. Each assignment specifies how Athena queries can consume capacity from the capacity reservation that their workgroup is mapped to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-capacityreservation.html#cfn-athena-capacityreservation-capacityassignmentconfiguration
        '''
        result = self._values.get("capacity_assignment_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityReservationPropsMixin.CapacityAssignmentConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the capacity reservation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-capacityreservation.html#cfn-athena-capacityreservation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to the capacity reservation.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-capacityreservation.html#cfn-athena-capacityreservation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_dpus(self) -> typing.Optional[jsii.Number]:
        '''The number of data processing units requested.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-capacityreservation.html#cfn-athena-capacityreservation-targetdpus
        '''
        result = self._values.get("target_dpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCapacityReservationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCapacityReservationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnCapacityReservationPropsMixin",
):
    '''Specifies a capacity reservation with the provided name and number of requested data processing units.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-capacityreservation.html
    :cloudformationResource: AWS::Athena::CapacityReservation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
        
        cfn_capacity_reservation_props_mixin = athena_mixins.CfnCapacityReservationPropsMixin(athena_mixins.CfnCapacityReservationMixinProps(
            capacity_assignment_configuration=athena_mixins.CfnCapacityReservationPropsMixin.CapacityAssignmentConfigurationProperty(
                capacity_assignments=[athena_mixins.CfnCapacityReservationPropsMixin.CapacityAssignmentProperty(
                    workgroup_names=["workgroupNames"]
                )]
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_dpus=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCapacityReservationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Athena::CapacityReservation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34bbdaac95a876c2c6487794bb811243b92542acc648f6753283505377bffcee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f68bfb1bed5c98477d2c416730db01bf084e54f99f516320f93089aa7b7f81ea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9064dcc3ec5b6a56e6b2c6b15faf957fc5117757793d56c93a9adbb5dcd00f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCapacityReservationMixinProps:
        return typing.cast(CfnCapacityReservationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnCapacityReservationPropsMixin.CapacityAssignmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"capacity_assignments": "capacityAssignments"},
    )
    class CapacityAssignmentConfigurationProperty:
        def __init__(
            self,
            *,
            capacity_assignments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapacityReservationPropsMixin.CapacityAssignmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Assigns Athena workgroups (and hence their queries) to capacity reservations.

            A capacity reservation can have only one capacity assignment configuration, but the capacity assignment configuration can be made up of multiple individual assignments. Each assignment specifies how Athena queries can consume capacity from the capacity reservation that their workgroup is mapped to.

            :param capacity_assignments: The list of assignments that make up the capacity assignment configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-capacityreservation-capacityassignmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                capacity_assignment_configuration_property = athena_mixins.CfnCapacityReservationPropsMixin.CapacityAssignmentConfigurationProperty(
                    capacity_assignments=[athena_mixins.CfnCapacityReservationPropsMixin.CapacityAssignmentProperty(
                        workgroup_names=["workgroupNames"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__934ddff30bb89e8563e9a97c2c35f238318d86ab3d79530b16674c1696221e7d)
                check_type(argname="argument capacity_assignments", value=capacity_assignments, expected_type=type_hints["capacity_assignments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_assignments is not None:
                self._values["capacity_assignments"] = capacity_assignments

        @builtins.property
        def capacity_assignments(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityReservationPropsMixin.CapacityAssignmentProperty"]]]]:
            '''The list of assignments that make up the capacity assignment configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-capacityreservation-capacityassignmentconfiguration.html#cfn-athena-capacityreservation-capacityassignmentconfiguration-capacityassignments
            '''
            result = self._values.get("capacity_assignments")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapacityReservationPropsMixin.CapacityAssignmentProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityAssignmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnCapacityReservationPropsMixin.CapacityAssignmentProperty",
        jsii_struct_bases=[],
        name_mapping={"workgroup_names": "workgroupNames"},
    )
    class CapacityAssignmentProperty:
        def __init__(
            self,
            *,
            workgroup_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A mapping between one or more workgroups and a capacity reservation.

            :param workgroup_names: The list of workgroup names for the capacity assignment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-capacityreservation-capacityassignment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                capacity_assignment_property = athena_mixins.CfnCapacityReservationPropsMixin.CapacityAssignmentProperty(
                    workgroup_names=["workgroupNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af04eb5b4f2ba4696cc389c365112c75632ecc739046be7569140fc4e449b316)
                check_type(argname="argument workgroup_names", value=workgroup_names, expected_type=type_hints["workgroup_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if workgroup_names is not None:
                self._values["workgroup_names"] = workgroup_names

        @builtins.property
        def workgroup_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of workgroup names for the capacity assignment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-capacityreservation-capacityassignment.html#cfn-athena-capacityreservation-capacityassignment-workgroupnames
            '''
            result = self._values.get("workgroup_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityAssignmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnDataCatalogMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_type": "connectionType",
        "description": "description",
        "error": "error",
        "name": "name",
        "parameters": "parameters",
        "status": "status",
        "tags": "tags",
        "type": "type",
    },
)
class CfnDataCatalogMixinProps:
    def __init__(
        self,
        *,
        connection_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        error: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDataCatalogPropsMixin.

        :param connection_type: The type of connection for a ``FEDERATED`` data catalog (for example, ``REDSHIFT`` , ``MYSQL`` , or ``SQLSERVER`` ). For information about individual connectors, see `Available data source connectors <https://docs.aws.amazon.com/athena/latest/ug/connectors-available.html>`_ .
        :param description: A description of the data catalog.
        :param error: Text of the error that occurred during data catalog creation or deletion.
        :param name: The name of the data catalog. The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.
        :param parameters: Specifies the Lambda function or functions to use for creating the data catalog. This is a mapping whose values depend on the catalog type. - For the ``HIVE`` data catalog type, use the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version. ``metadata-function= *lambda_arn* , sdk-version= *version_number*`` - For the ``LAMBDA`` data catalog type, use one of the following sets of required parameters, but not both. - If you have one Lambda function that processes metadata and another for reading the actual data, use the following syntax. Both parameters are required. ``metadata-function= *lambda_arn* , record-function= *lambda_arn*`` - If you have a composite Lambda function that processes both metadata and data, use the following syntax to specify your Lambda function. ``function= *lambda_arn*`` - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the AWS Glue Data Catalog belongs. ``catalog-id= *catalog_id*`` - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify. - The ``FEDERATED`` data catalog type uses one of the following parameters, but not both. Use ``connection-arn`` for an existing AWS Glue connection. Use ``connection-type`` and ``connection-properties`` to specify the configuration setting for a new connection. - ``connection-arn: *<glue_connection_arn_to_reuse>*`` - ``lambda-role-arn`` (optional): The execution role to use for the Lambda function. If not provided, one is created. - ``connection-type:MYSQL|REDSHIFT|...., connection-properties:" *<json_string>* "`` For *``<json_string>``* , use escaped JSON text, as in the following example. ``"{\\"spill_bucket\\":\\"my_spill\\",\\"spill_prefix\\":\\"athena-spill\\",\\"host\\":\\"abc12345.snowflakecomputing.com\\",\\"port\\":\\"1234\\",\\"warehouse\\":\\"DEV_WH\\",\\"database\\":\\"TEST\\",\\"schema\\":\\"PUBLIC\\",\\"SecretArn\\":\\"arn:aws:secretsmanager:ap-south-1:111122223333:secret:snowflake-XHb67j\\"}"``
        :param status: The status of the creation or deletion of the data catalog. - The ``LAMBDA`` , ``GLUE`` , and ``HIVE`` data catalog types are created synchronously. Their status is either ``CREATE_COMPLETE`` or ``CREATE_FAILED`` . - The ``FEDERATED`` data catalog type is created asynchronously. Data catalog creation status: - ``CREATE_IN_PROGRESS`` : Federated data catalog creation in progress. - ``CREATE_COMPLETE`` : Data catalog creation complete. - ``CREATE_FAILED`` : Data catalog could not be created. - ``CREATE_FAILED_CLEANUP_IN_PROGRESS`` : Federated data catalog creation failed and is being removed. - ``CREATE_FAILED_CLEANUP_COMPLETE`` : Federated data catalog creation failed and was removed. - ``CREATE_FAILED_CLEANUP_FAILED`` : Federated data catalog creation failed but could not be removed. Data catalog deletion status: - ``DELETE_IN_PROGRESS`` : Federated data catalog deletion in progress. - ``DELETE_COMPLETE`` : Federated data catalog deleted. - ``DELETE_FAILED`` : Federated data catalog could not be deleted.
        :param tags: The tags (key-value pairs) to associate with this resource.
        :param type: The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
            
            cfn_data_catalog_mixin_props = athena_mixins.CfnDataCatalogMixinProps(
                connection_type="connectionType",
                description="description",
                error="error",
                name="name",
                parameters={
                    "parameters_key": "parameters"
                },
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46bb671fea4e862c9f65c8326220f4108aa3e0987c6b1ac8a584e2c02d70a608)
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument error", value=error, expected_type=type_hints["error"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if description is not None:
            self._values["description"] = description
        if error is not None:
            self._values["error"] = error
        if name is not None:
            self._values["name"] = name
        if parameters is not None:
            self._values["parameters"] = parameters
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def connection_type(self) -> typing.Optional[builtins.str]:
        '''The type of connection for a ``FEDERATED`` data catalog (for example, ``REDSHIFT`` , ``MYSQL`` , or ``SQLSERVER`` ).

        For information about individual connectors, see `Available data source connectors <https://docs.aws.amazon.com/athena/latest/ug/connectors-available.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-connectiontype
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the data catalog.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error(self) -> typing.Optional[builtins.str]:
        '''Text of the error that occurred during data catalog creation or deletion.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-error
        '''
        result = self._values.get("error")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the data catalog.

        The catalog name must be unique for the AWS account and can use a maximum of 128 alphanumeric, underscore, at sign, or hyphen characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies the Lambda function or functions to use for creating the data catalog.

        This is a mapping whose values depend on the catalog type.

        - For the ``HIVE`` data catalog type, use the following syntax. The ``metadata-function`` parameter is required. ``The sdk-version`` parameter is optional and defaults to the currently supported version.

        ``metadata-function= *lambda_arn* , sdk-version= *version_number*``

        - For the ``LAMBDA`` data catalog type, use one of the following sets of required parameters, but not both.
        - If you have one Lambda function that processes metadata and another for reading the actual data, use the following syntax. Both parameters are required.

        ``metadata-function= *lambda_arn* , record-function= *lambda_arn*``

        - If you have a composite Lambda function that processes both metadata and data, use the following syntax to specify your Lambda function.

        ``function= *lambda_arn*``

        - The ``GLUE`` type takes a catalog ID parameter and is required. The ``*catalog_id*`` is the account ID of the AWS account to which the AWS Glue Data Catalog belongs.

        ``catalog-id= *catalog_id*``

        - The ``GLUE`` data catalog type also applies to the default ``AwsDataCatalog`` that already exists in your account, of which you can have only one and cannot modify.
        - The ``FEDERATED`` data catalog type uses one of the following parameters, but not both. Use ``connection-arn`` for an existing AWS Glue connection. Use ``connection-type`` and ``connection-properties`` to specify the configuration setting for a new connection.
        - ``connection-arn: *<glue_connection_arn_to_reuse>*``
        - ``lambda-role-arn`` (optional): The execution role to use for the Lambda function. If not provided, one is created.
        - ``connection-type:MYSQL|REDSHIFT|...., connection-properties:" *<json_string>* "``

        For *``<json_string>``* , use escaped JSON text, as in the following example.

        ``"{\\"spill_bucket\\":\\"my_spill\\",\\"spill_prefix\\":\\"athena-spill\\",\\"host\\":\\"abc12345.snowflakecomputing.com\\",\\"port\\":\\"1234\\",\\"warehouse\\":\\"DEV_WH\\",\\"database\\":\\"TEST\\",\\"schema\\":\\"PUBLIC\\",\\"SecretArn\\":\\"arn:aws:secretsmanager:ap-south-1:111122223333:secret:snowflake-XHb67j\\"}"``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the creation or deletion of the data catalog.

        - The ``LAMBDA`` , ``GLUE`` , and ``HIVE`` data catalog types are created synchronously. Their status is either ``CREATE_COMPLETE`` or ``CREATE_FAILED`` .
        - The ``FEDERATED`` data catalog type is created asynchronously.

        Data catalog creation status:

        - ``CREATE_IN_PROGRESS`` : Federated data catalog creation in progress.
        - ``CREATE_COMPLETE`` : Data catalog creation complete.
        - ``CREATE_FAILED`` : Data catalog could not be created.
        - ``CREATE_FAILED_CLEANUP_IN_PROGRESS`` : Federated data catalog creation failed and is being removed.
        - ``CREATE_FAILED_CLEANUP_COMPLETE`` : Federated data catalog creation failed and was removed.
        - ``CREATE_FAILED_CLEANUP_FAILED`` : Federated data catalog creation failed but could not be removed.

        Data catalog deletion status:

        - ``DELETE_IN_PROGRESS`` : Federated data catalog deletion in progress.
        - ``DELETE_COMPLETE`` : Federated data catalog deleted.
        - ``DELETE_FAILED`` : Federated data catalog could not be deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags (key-value pairs) to associate with this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of data catalog: ``LAMBDA`` for a federated catalog, ``GLUE`` for AWS Glue Catalog, or ``HIVE`` for an external hive metastore.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html#cfn-athena-datacatalog-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataCatalogMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataCatalogPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnDataCatalogPropsMixin",
):
    '''The AWS::Athena::DataCatalog resource specifies an Amazon Athena data catalog, which contains a name, description, type, parameters, and tags.

    For more information, see `DataCatalog <https://docs.aws.amazon.com/athena/latest/APIReference/API_DataCatalog.html>`_ in the *Amazon Athena API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-datacatalog.html
    :cloudformationResource: AWS::Athena::DataCatalog
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
        
        cfn_data_catalog_props_mixin = athena_mixins.CfnDataCatalogPropsMixin(athena_mixins.CfnDataCatalogMixinProps(
            connection_type="connectionType",
            description="description",
            error="error",
            name="name",
            parameters={
                "parameters_key": "parameters"
            },
            status="status",
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
        props: typing.Union[CfnDataCatalogMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Athena::DataCatalog``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570f70585b42dd2757b7bf8bac72f472548501330ea28d66ca989cf8c220e1ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c4dc185a35fd6a945992041c91289ba4ddbb47e8c9de282f7b38c6a29cc85ca)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186cd9fce4dcd9dec5b821f70aff43a298b48ed868583e5546cb0e11ea350f46)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataCatalogMixinProps:
        return typing.cast(CfnDataCatalogMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnNamedQueryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "description": "description",
        "name": "name",
        "query_string": "queryString",
        "work_group": "workGroup",
    },
)
class CfnNamedQueryMixinProps:
    def __init__(
        self,
        *,
        database: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
        work_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnNamedQueryPropsMixin.

        :param database: The database to which the query belongs.
        :param description: The query description.
        :param name: The query name.
        :param query_string: The SQL statements that make up the query.
        :param work_group: The name of the workgroup that contains the named query.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
            
            cfn_named_query_mixin_props = athena_mixins.CfnNamedQueryMixinProps(
                database="database",
                description="description",
                name="name",
                query_string="queryString",
                work_group="workGroup"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545562a52e4919ed105308a7a9b3d51a3ed8cb5593a528e2f6b150739f97a6ff)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument work_group", value=work_group, expected_type=type_hints["work_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database is not None:
            self._values["database"] = database
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if query_string is not None:
            self._values["query_string"] = query_string
        if work_group is not None:
            self._values["work_group"] = work_group

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''The database to which the query belongs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-database
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The query description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The query name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_string(self) -> typing.Optional[builtins.str]:
        '''The SQL statements that make up the query.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-querystring
        '''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def work_group(self) -> typing.Optional[builtins.str]:
        '''The name of the workgroup that contains the named query.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html#cfn-athena-namedquery-workgroup
        '''
        result = self._values.get("work_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNamedQueryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNamedQueryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnNamedQueryPropsMixin",
):
    '''The ``AWS::Athena::NamedQuery`` resource specifies an Amazon Athena saved query, where ``QueryString`` contains the SQL query statements that make up the query.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-namedquery.html
    :cloudformationResource: AWS::Athena::NamedQuery
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
        
        cfn_named_query_props_mixin = athena_mixins.CfnNamedQueryPropsMixin(athena_mixins.CfnNamedQueryMixinProps(
            database="database",
            description="description",
            name="name",
            query_string="queryString",
            work_group="workGroup"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnNamedQueryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Athena::NamedQuery``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6484b6a8b68a37521c5753db983d5fdae4fa91d0bac7cd00b3d8c1cd11a78710)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4621c9d76ca901dddf6646c944a37ad76b2e43e3e136c6e2b20093e860a4348a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0338a673f732ca0b955dda1ef99ce1017db1dfdc1f8649b5cd535a8d5e21c59d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNamedQueryMixinProps:
        return typing.cast(CfnNamedQueryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnPreparedStatementMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "query_statement": "queryStatement",
        "statement_name": "statementName",
        "work_group": "workGroup",
    },
)
class CfnPreparedStatementMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        query_statement: typing.Optional[builtins.str] = None,
        statement_name: typing.Optional[builtins.str] = None,
        work_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPreparedStatementPropsMixin.

        :param description: The description of the prepared statement.
        :param query_statement: The query string for the prepared statement.
        :param statement_name: The name of the prepared statement.
        :param work_group: The workgroup to which the prepared statement belongs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
            
            cfn_prepared_statement_mixin_props = athena_mixins.CfnPreparedStatementMixinProps(
                description="description",
                query_statement="queryStatement",
                statement_name="statementName",
                work_group="workGroup"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd50cb05c32ed5054c831f6b42bb9722bab71fa7c745ecc182e9ea38f5a2f2e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument query_statement", value=query_statement, expected_type=type_hints["query_statement"])
            check_type(argname="argument statement_name", value=statement_name, expected_type=type_hints["statement_name"])
            check_type(argname="argument work_group", value=work_group, expected_type=type_hints["work_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if query_statement is not None:
            self._values["query_statement"] = query_statement
        if statement_name is not None:
            self._values["statement_name"] = statement_name
        if work_group is not None:
            self._values["work_group"] = work_group

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the prepared statement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_statement(self) -> typing.Optional[builtins.str]:
        '''The query string for the prepared statement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-querystatement
        '''
        result = self._values.get("query_statement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def statement_name(self) -> typing.Optional[builtins.str]:
        '''The name of the prepared statement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-statementname
        '''
        result = self._values.get("statement_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def work_group(self) -> typing.Optional[builtins.str]:
        '''The workgroup to which the prepared statement belongs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html#cfn-athena-preparedstatement-workgroup
        '''
        result = self._values.get("work_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPreparedStatementMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPreparedStatementPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnPreparedStatementPropsMixin",
):
    '''Specifies a prepared statement for use with SQL queries in Athena.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-preparedstatement.html
    :cloudformationResource: AWS::Athena::PreparedStatement
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
        
        cfn_prepared_statement_props_mixin = athena_mixins.CfnPreparedStatementPropsMixin(athena_mixins.CfnPreparedStatementMixinProps(
            description="description",
            query_statement="queryStatement",
            statement_name="statementName",
            work_group="workGroup"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPreparedStatementMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Athena::PreparedStatement``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a75ffd7e4ffba6bacbf7166f5343f5bfcce9fd77376677dbff4cbf1ce4b1469)
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
            type_hints = typing.get_type_hints(_typecheckingstub__145f38e9bd33e6e935d73d2a520ffe362c9462e974235a687d08f52c1279684c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d282108304ead98904b9b2c962df41e9687643601cecd5fb9296fe55e5e8237)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPreparedStatementMixinProps:
        return typing.cast(CfnPreparedStatementMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "recursive_delete_option": "recursiveDeleteOption",
        "state": "state",
        "tags": "tags",
        "work_group_configuration": "workGroupConfiguration",
        "work_group_configuration_updates": "workGroupConfigurationUpdates",
    },
)
class CfnWorkGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        work_group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.WorkGroupConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        work_group_configuration_updates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.WorkGroupConfigurationUpdatesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWorkGroupPropsMixin.

        :param description: The workgroup description.
        :param name: The workgroup name.
        :param recursive_delete_option: The option to delete a workgroup and its contents even if the workgroup contains any named queries. The default is false.
        :param state: The state of the workgroup: ENABLED or DISABLED.
        :param tags: The tags (key-value pairs) to associate with this resource.
        :param work_group_configuration: The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified. The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.
        :param work_group_configuration_updates: (deprecated) The configuration information that will be updated for this workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether the Amazon CloudWatch Metrics are enabled for the workgroup, whether the workgroup settings override the client-side settings, and the data usage limit for the amount of bytes scanned per query, if it is specified.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
            
            cfn_work_group_mixin_props = athena_mixins.CfnWorkGroupMixinProps(
                description="description",
                name="name",
                recursive_delete_option=False,
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                work_group_configuration=athena_mixins.CfnWorkGroupPropsMixin.WorkGroupConfigurationProperty(
                    additional_configuration="additionalConfiguration",
                    bytes_scanned_cutoff_per_query=123,
                    customer_content_encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty(
                        kms_key="kmsKey"
                    ),
                    enforce_work_group_configuration=False,
                    engine_configuration=athena_mixins.CfnWorkGroupPropsMixin.EngineConfigurationProperty(
                        additional_configs={
                            "additional_configs_key": "additionalConfigs"
                        },
                        classifications=[athena_mixins.CfnWorkGroupPropsMixin.ClassificationProperty(
                            name="name",
                            properties={
                                "properties_key": "properties"
                            }
                        )],
                        coordinator_dpu_size=123,
                        default_executor_dpu_size=123,
                        max_concurrent_dpus=123,
                        spark_properties={
                            "spark_properties_key": "sparkProperties"
                        }
                    ),
                    engine_version=athena_mixins.CfnWorkGroupPropsMixin.EngineVersionProperty(
                        effective_engine_version="effectiveEngineVersion",
                        selected_engine_version="selectedEngineVersion"
                    ),
                    execution_role="executionRole",
                    managed_query_results_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty(
                        enabled=False,
                        encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty(
                            kms_key="kmsKey"
                        )
                    ),
                    monitoring_configuration=athena_mixins.CfnWorkGroupPropsMixin.MonitoringConfigurationProperty(
                        cloud_watch_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty(
                            enabled=False,
                            log_group="logGroup",
                            log_stream_name_prefix="logStreamNamePrefix",
                            log_types={
                                "log_types_key": ["logTypes"]
                            }
                        ),
                        managed_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty(
                            enabled=False,
                            kms_key="kmsKey"
                        ),
                        s3_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty(
                            enabled=False,
                            kms_key="kmsKey",
                            log_location="logLocation"
                        )
                    ),
                    publish_cloud_watch_metrics_enabled=False,
                    requester_pays_enabled=False,
                    result_configuration=athena_mixins.CfnWorkGroupPropsMixin.ResultConfigurationProperty(
                        acl_configuration=athena_mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty(
                            s3_acl_option="s3AclOption"
                        ),
                        encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty(
                            encryption_option="encryptionOption",
                            kms_key="kmsKey"
                        ),
                        expected_bucket_owner="expectedBucketOwner",
                        output_location="outputLocation"
                    )
                ),
                work_group_configuration_updates=athena_mixins.CfnWorkGroupPropsMixin.WorkGroupConfigurationUpdatesProperty(
                    additional_configuration="additionalConfiguration",
                    bytes_scanned_cutoff_per_query=123,
                    customer_content_encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty(
                        kms_key="kmsKey"
                    ),
                    enforce_work_group_configuration=False,
                    engine_configuration=athena_mixins.CfnWorkGroupPropsMixin.EngineConfigurationProperty(
                        additional_configs={
                            "additional_configs_key": "additionalConfigs"
                        },
                        classifications=[athena_mixins.CfnWorkGroupPropsMixin.ClassificationProperty(
                            name="name",
                            properties={
                                "properties_key": "properties"
                            }
                        )],
                        coordinator_dpu_size=123,
                        default_executor_dpu_size=123,
                        max_concurrent_dpus=123,
                        spark_properties={
                            "spark_properties_key": "sparkProperties"
                        }
                    ),
                    engine_version=athena_mixins.CfnWorkGroupPropsMixin.EngineVersionProperty(
                        effective_engine_version="effectiveEngineVersion",
                        selected_engine_version="selectedEngineVersion"
                    ),
                    execution_role="executionRole",
                    managed_query_results_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty(
                        enabled=False,
                        encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty(
                            kms_key="kmsKey"
                        )
                    ),
                    monitoring_configuration=athena_mixins.CfnWorkGroupPropsMixin.MonitoringConfigurationProperty(
                        cloud_watch_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty(
                            enabled=False,
                            log_group="logGroup",
                            log_stream_name_prefix="logStreamNamePrefix",
                            log_types={
                                "log_types_key": ["logTypes"]
                            }
                        ),
                        managed_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty(
                            enabled=False,
                            kms_key="kmsKey"
                        ),
                        s3_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty(
                            enabled=False,
                            kms_key="kmsKey",
                            log_location="logLocation"
                        )
                    ),
                    publish_cloud_watch_metrics_enabled=False,
                    remove_bytes_scanned_cutoff_per_query=False,
                    remove_customer_content_encryption_configuration=False,
                    requester_pays_enabled=False,
                    result_configuration_updates=athena_mixins.CfnWorkGroupPropsMixin.ResultConfigurationUpdatesProperty(
                        acl_configuration=athena_mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty(
                            s3_acl_option="s3AclOption"
                        ),
                        encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty(
                            encryption_option="encryptionOption",
                            kms_key="kmsKey"
                        ),
                        expected_bucket_owner="expectedBucketOwner",
                        output_location="outputLocation",
                        remove_acl_configuration=False,
                        remove_encryption_configuration=False,
                        remove_expected_bucket_owner=False,
                        remove_output_location=False
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d517e947d90f3c5a384ca281c9ed0281cc55d94966a677ba8cf9bdd08218724b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recursive_delete_option", value=recursive_delete_option, expected_type=type_hints["recursive_delete_option"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument work_group_configuration", value=work_group_configuration, expected_type=type_hints["work_group_configuration"])
            check_type(argname="argument work_group_configuration_updates", value=work_group_configuration_updates, expected_type=type_hints["work_group_configuration_updates"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if recursive_delete_option is not None:
            self._values["recursive_delete_option"] = recursive_delete_option
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if work_group_configuration is not None:
            self._values["work_group_configuration"] = work_group_configuration
        if work_group_configuration_updates is not None:
            self._values["work_group_configuration_updates"] = work_group_configuration_updates

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The workgroup description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The workgroup name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recursive_delete_option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The option to delete a workgroup and its contents even if the workgroup contains any named queries.

        The default is false.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-recursivedeleteoption
        '''
        result = self._values.get("recursive_delete_option")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the workgroup: ENABLED or DISABLED.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags (key-value pairs) to associate with this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def work_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.WorkGroupConfigurationProperty"]]:
        '''The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified.

        The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfiguration
        '''
        result = self._values.get("work_group_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.WorkGroupConfigurationProperty"]], result)

    @builtins.property
    def work_group_configuration_updates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.WorkGroupConfigurationUpdatesProperty"]]:
        '''(deprecated) The configuration information that will be updated for this workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether the Amazon CloudWatch Metrics are enabled for the workgroup, whether the workgroup settings override the client-side settings, and the data usage limit for the amount of bytes scanned per query, if it is specified.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html#cfn-athena-workgroup-workgroupconfigurationupdates
        :stability: deprecated
        '''
        result = self._values.get("work_group_configuration_updates")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.WorkGroupConfigurationUpdatesProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin",
):
    '''The AWS::Athena::WorkGroup resource specifies an Amazon Athena workgroup, which contains a name, description, creation time, state, and other configuration, listed under ``WorkGroupConfiguration`` .

    Each workgroup enables you to isolate queries for you or your group from other queries in the same account. For more information, see `CreateWorkGroup <https://docs.aws.amazon.com/athena/latest/APIReference/API_CreateWorkGroup.html>`_ in the *Amazon Athena API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-athena-workgroup.html
    :cloudformationResource: AWS::Athena::WorkGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
        
        cfn_work_group_props_mixin = athena_mixins.CfnWorkGroupPropsMixin(athena_mixins.CfnWorkGroupMixinProps(
            description="description",
            name="name",
            recursive_delete_option=False,
            state="state",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            work_group_configuration=athena_mixins.CfnWorkGroupPropsMixin.WorkGroupConfigurationProperty(
                additional_configuration="additionalConfiguration",
                bytes_scanned_cutoff_per_query=123,
                customer_content_encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty(
                    kms_key="kmsKey"
                ),
                enforce_work_group_configuration=False,
                engine_configuration=athena_mixins.CfnWorkGroupPropsMixin.EngineConfigurationProperty(
                    additional_configs={
                        "additional_configs_key": "additionalConfigs"
                    },
                    classifications=[athena_mixins.CfnWorkGroupPropsMixin.ClassificationProperty(
                        name="name",
                        properties={
                            "properties_key": "properties"
                        }
                    )],
                    coordinator_dpu_size=123,
                    default_executor_dpu_size=123,
                    max_concurrent_dpus=123,
                    spark_properties={
                        "spark_properties_key": "sparkProperties"
                    }
                ),
                engine_version=athena_mixins.CfnWorkGroupPropsMixin.EngineVersionProperty(
                    effective_engine_version="effectiveEngineVersion",
                    selected_engine_version="selectedEngineVersion"
                ),
                execution_role="executionRole",
                managed_query_results_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty(
                    enabled=False,
                    encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty(
                        kms_key="kmsKey"
                    )
                ),
                monitoring_configuration=athena_mixins.CfnWorkGroupPropsMixin.MonitoringConfigurationProperty(
                    cloud_watch_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty(
                        enabled=False,
                        log_group="logGroup",
                        log_stream_name_prefix="logStreamNamePrefix",
                        log_types={
                            "log_types_key": ["logTypes"]
                        }
                    ),
                    managed_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty(
                        enabled=False,
                        kms_key="kmsKey"
                    ),
                    s3_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty(
                        enabled=False,
                        kms_key="kmsKey",
                        log_location="logLocation"
                    )
                ),
                publish_cloud_watch_metrics_enabled=False,
                requester_pays_enabled=False,
                result_configuration=athena_mixins.CfnWorkGroupPropsMixin.ResultConfigurationProperty(
                    acl_configuration=athena_mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty(
                        s3_acl_option="s3AclOption"
                    ),
                    encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty(
                        encryption_option="encryptionOption",
                        kms_key="kmsKey"
                    ),
                    expected_bucket_owner="expectedBucketOwner",
                    output_location="outputLocation"
                )
            ),
            work_group_configuration_updates=athena_mixins.CfnWorkGroupPropsMixin.WorkGroupConfigurationUpdatesProperty(
                additional_configuration="additionalConfiguration",
                bytes_scanned_cutoff_per_query=123,
                customer_content_encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty(
                    kms_key="kmsKey"
                ),
                enforce_work_group_configuration=False,
                engine_configuration=athena_mixins.CfnWorkGroupPropsMixin.EngineConfigurationProperty(
                    additional_configs={
                        "additional_configs_key": "additionalConfigs"
                    },
                    classifications=[athena_mixins.CfnWorkGroupPropsMixin.ClassificationProperty(
                        name="name",
                        properties={
                            "properties_key": "properties"
                        }
                    )],
                    coordinator_dpu_size=123,
                    default_executor_dpu_size=123,
                    max_concurrent_dpus=123,
                    spark_properties={
                        "spark_properties_key": "sparkProperties"
                    }
                ),
                engine_version=athena_mixins.CfnWorkGroupPropsMixin.EngineVersionProperty(
                    effective_engine_version="effectiveEngineVersion",
                    selected_engine_version="selectedEngineVersion"
                ),
                execution_role="executionRole",
                managed_query_results_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty(
                    enabled=False,
                    encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty(
                        kms_key="kmsKey"
                    )
                ),
                monitoring_configuration=athena_mixins.CfnWorkGroupPropsMixin.MonitoringConfigurationProperty(
                    cloud_watch_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty(
                        enabled=False,
                        log_group="logGroup",
                        log_stream_name_prefix="logStreamNamePrefix",
                        log_types={
                            "log_types_key": ["logTypes"]
                        }
                    ),
                    managed_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty(
                        enabled=False,
                        kms_key="kmsKey"
                    ),
                    s3_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty(
                        enabled=False,
                        kms_key="kmsKey",
                        log_location="logLocation"
                    )
                ),
                publish_cloud_watch_metrics_enabled=False,
                remove_bytes_scanned_cutoff_per_query=False,
                remove_customer_content_encryption_configuration=False,
                requester_pays_enabled=False,
                result_configuration_updates=athena_mixins.CfnWorkGroupPropsMixin.ResultConfigurationUpdatesProperty(
                    acl_configuration=athena_mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty(
                        s3_acl_option="s3AclOption"
                    ),
                    encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty(
                        encryption_option="encryptionOption",
                        kms_key="kmsKey"
                    ),
                    expected_bucket_owner="expectedBucketOwner",
                    output_location="outputLocation",
                    remove_acl_configuration=False,
                    remove_encryption_configuration=False,
                    remove_expected_bucket_owner=False,
                    remove_output_location=False
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Athena::WorkGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f768d560085fc738868daa9a467686bf08100bded04a0a23281867418a76758a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7bf90c1a7c5451bfdbce4f0c589789c510263184cc0e9196a7f2fa51acfa635)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f617c3ec6f27a3fbce296fd9de311b475d1e14188dcb220f8d4daccf068c6f28)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkGroupMixinProps:
        return typing.cast(CfnWorkGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_acl_option": "s3AclOption"},
    )
    class AclConfigurationProperty:
        def __init__(
            self,
            *,
            s3_acl_option: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Indicates that an Amazon S3 canned ACL should be set to control ownership of stored query results, including data files inserted by Athena as the result of statements like CTAS or INSERT INTO.

            When Athena stores query results in Amazon S3, the canned ACL is set with the ``x-amz-acl`` request header. For more information about S3 Object Ownership, see `Object Ownership settings <https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html#object-ownership-overview>`_ in the *Amazon S3 User Guide* .

            :param s3_acl_option: The Amazon S3 canned ACL that Athena should specify when storing query results, including data files inserted by Athena as the result of statements like CTAS or INSERT INTO. Currently the only supported canned ACL is ``BUCKET_OWNER_FULL_CONTROL`` . If a query runs in a workgroup and the workgroup overrides client-side settings, then the Amazon S3 canned ACL specified in the workgroup's settings is used for all queries that run in the workgroup. For more information about Amazon S3 canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-aclconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                acl_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty(
                    s3_acl_option="s3AclOption"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d264c723cb659a190079e0614341ed89d585843cdeaa34489b0aed887ef8aa13)
                check_type(argname="argument s3_acl_option", value=s3_acl_option, expected_type=type_hints["s3_acl_option"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_acl_option is not None:
                self._values["s3_acl_option"] = s3_acl_option

        @builtins.property
        def s3_acl_option(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 canned ACL that Athena should specify when storing query results, including data files inserted by Athena as the result of statements like CTAS or INSERT INTO.

            Currently the only supported canned ACL is ``BUCKET_OWNER_FULL_CONTROL`` . If a query runs in a workgroup and the workgroup overrides client-side settings, then the Amazon S3 canned ACL specified in the workgroup's settings is used for all queries that run in the workgroup. For more information about Amazon S3 canned ACLs, see `Canned ACL <https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl>`_ in the *Amazon S3 User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-aclconfiguration.html#cfn-athena-workgroup-aclconfiguration-s3acloption
            '''
            result = self._values.get("s3_acl_option")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AclConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.ClassificationProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "properties": "properties"},
    )
    class ClassificationProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''A classification refers to a set of specific configurations.

            :param name: The name of the configuration classification.
            :param properties: A set of properties specified within a configuration classification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-classification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                classification_property = athena_mixins.CfnWorkGroupPropsMixin.ClassificationProperty(
                    name="name",
                    properties={
                        "properties_key": "properties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d7bbaff94503b75776b52acaf5230425c8a7bbad179e084e8963380df0a3bf3)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if properties is not None:
                self._values["properties"] = properties

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the configuration classification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-classification.html#cfn-athena-workgroup-classification-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A set of properties specified within a configuration classification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-classification.html#cfn-athena-workgroup-classification-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClassificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "log_group": "logGroup",
            "log_stream_name_prefix": "logStreamNamePrefix",
            "log_types": "logTypes",
        },
    )
    class CloudWatchLoggingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            log_group: typing.Optional[builtins.str] = None,
            log_stream_name_prefix: typing.Optional[builtins.str] = None,
            log_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Sequence[builtins.str]]]] = None,
        ) -> None:
            '''Configuration settings for delivering logs to Amazon CloudWatch log groups.

            :param enabled: Enables CloudWatch logging.
            :param log_group: The name of the log group in Amazon CloudWatch Logs where you want to publish your logs.
            :param log_stream_name_prefix: Prefix for the CloudWatch log stream name.
            :param log_types: The types of logs that you want to publish to CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-cloudwatchloggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                cloud_watch_logging_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty(
                    enabled=False,
                    log_group="logGroup",
                    log_stream_name_prefix="logStreamNamePrefix",
                    log_types={
                        "log_types_key": ["logTypes"]
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd8117027f3559fa2756e383cc670f3b04d8b4099eb5f68c17f37c52b7345ff3)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
                check_type(argname="argument log_stream_name_prefix", value=log_stream_name_prefix, expected_type=type_hints["log_stream_name_prefix"])
                check_type(argname="argument log_types", value=log_types, expected_type=type_hints["log_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if log_group is not None:
                self._values["log_group"] = log_group
            if log_stream_name_prefix is not None:
                self._values["log_stream_name_prefix"] = log_stream_name_prefix
            if log_types is not None:
                self._values["log_types"] = log_types

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables CloudWatch logging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-cloudwatchloggingconfiguration.html#cfn-athena-workgroup-cloudwatchloggingconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''The name of the log group in Amazon CloudWatch Logs where you want to publish your logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-cloudwatchloggingconfiguration.html#cfn-athena-workgroup-cloudwatchloggingconfiguration-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_stream_name_prefix(self) -> typing.Optional[builtins.str]:
            '''Prefix for the CloudWatch log stream name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-cloudwatchloggingconfiguration.html#cfn-athena-workgroup-cloudwatchloggingconfiguration-logstreamnameprefix
            '''
            result = self._values.get("log_stream_name_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]]:
            '''The types of logs that you want to publish to CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-cloudwatchloggingconfiguration.html#cfn-athena-workgroup-cloudwatchloggingconfiguration-logtypes
            '''
            result = self._values.get("log_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key": "kmsKey"},
    )
    class CustomerContentEncryptionConfigurationProperty:
        def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the customer managed KMS key that is used to encrypt the user's data stores in Athena.

            When an AWS managed key is used, this value is null. This setting does not apply to Athena SQL workgroups.

            :param kms_key: The customer managed KMS key that is used to encrypt the user's data stores in Athena.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-customercontentencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                customer_content_encryption_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty(
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3b091ea786bb208af5c181c5d51caf69ab8412c01e15254e1b808b960e4fb00)
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''The customer managed KMS key that is used to encrypt the user's data stores in Athena.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-customercontentencryptionconfiguration.html#cfn-athena-workgroup-customercontentencryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerContentEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_option": "encryptionOption", "kms_key": "kmsKey"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_option: typing.Optional[builtins.str] = None,
            kms_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS`` ) and key information.

            :param encryption_option: Indicates whether Amazon S3 server-side encryption with Amazon S3-managed keys ( ``SSE_S3`` ), server-side encryption with KMS-managed keys ( ``SSE_KMS`` ), or client-side encryption with KMS-managed keys ( ``CSE_KMS`` ) is used. If a query runs in a workgroup and the workgroup overrides client-side settings, then the workgroup's setting for encryption is used. It specifies whether query results must be encrypted, for all queries that run in this workgroup.
            :param kms_key: For ``SSE_KMS`` and ``CSE_KMS`` , this is the KMS key ARN or ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                encryption_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty(
                    encryption_option="encryptionOption",
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__feb317ca5fd1a80660ea0ff605cd679f7593d4b10b1f1c40892f0e1fbd50c10a)
                check_type(argname="argument encryption_option", value=encryption_option, expected_type=type_hints["encryption_option"])
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_option is not None:
                self._values["encryption_option"] = encryption_option
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def encryption_option(self) -> typing.Optional[builtins.str]:
            '''Indicates whether Amazon S3 server-side encryption with Amazon S3-managed keys ( ``SSE_S3`` ), server-side encryption with KMS-managed keys ( ``SSE_KMS`` ), or client-side encryption with KMS-managed keys ( ``CSE_KMS`` ) is used.

            If a query runs in a workgroup and the workgroup overrides client-side settings, then the workgroup's setting for encryption is used. It specifies whether query results must be encrypted, for all queries that run in this workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html#cfn-athena-workgroup-encryptionconfiguration-encryptionoption
            '''
            result = self._values.get("encryption_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''For ``SSE_KMS`` and ``CSE_KMS`` , this is the KMS key ARN or ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-encryptionconfiguration.html#cfn-athena-workgroup-encryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.EngineConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_configs": "additionalConfigs",
            "classifications": "classifications",
            "coordinator_dpu_size": "coordinatorDpuSize",
            "default_executor_dpu_size": "defaultExecutorDpuSize",
            "max_concurrent_dpus": "maxConcurrentDpus",
            "spark_properties": "sparkProperties",
        },
    )
    class EngineConfigurationProperty:
        def __init__(
            self,
            *,
            additional_configs: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            classifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.ClassificationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            coordinator_dpu_size: typing.Optional[jsii.Number] = None,
            default_executor_dpu_size: typing.Optional[jsii.Number] = None,
            max_concurrent_dpus: typing.Optional[jsii.Number] = None,
            spark_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The engine configuration for the workgroup, which includes the minimum/maximum number of Data Processing Units (DPU) that queries should use when running in provisioned capacity.

            If not specified, Athena uses default values (Default value for min is 4 and for max is Minimum of 124 and allocated DPUs).

            To specify DPU values for PC queries the WG containing EngineConfiguration should have the following values: The name of the Classifications should be ``athena-query-engine-properties`` , with the only allowed properties as ``max-dpu-count`` and ``min-dpu-count`` .

            :param additional_configs: Contains additional notebook engine ``MAP<string, string>`` parameter mappings in the form of key-value pairs. To specify an Athena notebook that the Jupyter server will download and serve, specify a value for the ``StartSessionRequest$NotebookVersion`` field, and then add a key named ``NotebookId`` to ``AdditionalConfigs`` that has the value of the Athena notebook ID.
            :param classifications: The configuration classifications that can be specified for the engine.
            :param coordinator_dpu_size: The number of DPUs to use for the coordinator. A coordinator is a special executor that orchestrates processing work and manages other executors in a notebook session. The default is 1.
            :param default_executor_dpu_size: The default number of DPUs to use for executors. An executor is the smallest unit of compute that a notebook session can request from Athena. The default is 1.
            :param max_concurrent_dpus: The maximum number of DPUs that can run concurrently.
            :param spark_properties: Specifies custom jar files and Spark properties for use cases like cluster encryption, table formats, and general Spark tuning.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                engine_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.EngineConfigurationProperty(
                    additional_configs={
                        "additional_configs_key": "additionalConfigs"
                    },
                    classifications=[athena_mixins.CfnWorkGroupPropsMixin.ClassificationProperty(
                        name="name",
                        properties={
                            "properties_key": "properties"
                        }
                    )],
                    coordinator_dpu_size=123,
                    default_executor_dpu_size=123,
                    max_concurrent_dpus=123,
                    spark_properties={
                        "spark_properties_key": "sparkProperties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0596df3d33ac7708b71f3a646471951ae779902ded2d9e45fa16fe7b83465f2)
                check_type(argname="argument additional_configs", value=additional_configs, expected_type=type_hints["additional_configs"])
                check_type(argname="argument classifications", value=classifications, expected_type=type_hints["classifications"])
                check_type(argname="argument coordinator_dpu_size", value=coordinator_dpu_size, expected_type=type_hints["coordinator_dpu_size"])
                check_type(argname="argument default_executor_dpu_size", value=default_executor_dpu_size, expected_type=type_hints["default_executor_dpu_size"])
                check_type(argname="argument max_concurrent_dpus", value=max_concurrent_dpus, expected_type=type_hints["max_concurrent_dpus"])
                check_type(argname="argument spark_properties", value=spark_properties, expected_type=type_hints["spark_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_configs is not None:
                self._values["additional_configs"] = additional_configs
            if classifications is not None:
                self._values["classifications"] = classifications
            if coordinator_dpu_size is not None:
                self._values["coordinator_dpu_size"] = coordinator_dpu_size
            if default_executor_dpu_size is not None:
                self._values["default_executor_dpu_size"] = default_executor_dpu_size
            if max_concurrent_dpus is not None:
                self._values["max_concurrent_dpus"] = max_concurrent_dpus
            if spark_properties is not None:
                self._values["spark_properties"] = spark_properties

        @builtins.property
        def additional_configs(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Contains additional notebook engine ``MAP<string, string>`` parameter mappings in the form of key-value pairs.

            To specify an Athena notebook that the Jupyter server will download and serve, specify a value for the ``StartSessionRequest$NotebookVersion`` field, and then add a key named ``NotebookId`` to ``AdditionalConfigs`` that has the value of the Athena notebook ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineconfiguration.html#cfn-athena-workgroup-engineconfiguration-additionalconfigs
            '''
            result = self._values.get("additional_configs")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def classifications(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ClassificationProperty"]]]]:
            '''The configuration classifications that can be specified for the engine.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineconfiguration.html#cfn-athena-workgroup-engineconfiguration-classifications
            '''
            result = self._values.get("classifications")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ClassificationProperty"]]]], result)

        @builtins.property
        def coordinator_dpu_size(self) -> typing.Optional[jsii.Number]:
            '''The number of DPUs to use for the coordinator.

            A coordinator is a special executor that orchestrates processing work and manages other executors in a notebook session. The default is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineconfiguration.html#cfn-athena-workgroup-engineconfiguration-coordinatordpusize
            '''
            result = self._values.get("coordinator_dpu_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def default_executor_dpu_size(self) -> typing.Optional[jsii.Number]:
            '''The default number of DPUs to use for executors.

            An executor is the smallest unit of compute that a notebook session can request from Athena. The default is 1.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineconfiguration.html#cfn-athena-workgroup-engineconfiguration-defaultexecutordpusize
            '''
            result = self._values.get("default_executor_dpu_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_concurrent_dpus(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of DPUs that can run concurrently.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineconfiguration.html#cfn-athena-workgroup-engineconfiguration-maxconcurrentdpus
            '''
            result = self._values.get("max_concurrent_dpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def spark_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies custom jar files and Spark properties for use cases like cluster encryption, table formats, and general Spark tuning.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineconfiguration.html#cfn-athena-workgroup-engineconfiguration-sparkproperties
            '''
            result = self._values.get("spark_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EngineConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.EngineVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "effective_engine_version": "effectiveEngineVersion",
            "selected_engine_version": "selectedEngineVersion",
        },
    )
    class EngineVersionProperty:
        def __init__(
            self,
            *,
            effective_engine_version: typing.Optional[builtins.str] = None,
            selected_engine_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Athena engine version for running queries, or the PySpark engine version for running sessions.

            :param effective_engine_version: Read only. The engine version on which the query runs. If the user requests a valid engine version other than Auto, the effective engine version is the same as the engine version that the user requested. If the user requests Auto, the effective engine version is chosen by Athena. When a request to update the engine version is made by a ``CreateWorkGroup`` or ``UpdateWorkGroup`` operation, the ``EffectiveEngineVersion`` field is ignored.
            :param selected_engine_version: The engine version requested by the user. Possible values are determined by the output of ``ListEngineVersions`` , including AUTO. The default is AUTO.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                engine_version_property = athena_mixins.CfnWorkGroupPropsMixin.EngineVersionProperty(
                    effective_engine_version="effectiveEngineVersion",
                    selected_engine_version="selectedEngineVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c4a916b1ff47152bce0cb3de6928c9dd9725dcac1f5f2e218cef9f01f1fd148)
                check_type(argname="argument effective_engine_version", value=effective_engine_version, expected_type=type_hints["effective_engine_version"])
                check_type(argname="argument selected_engine_version", value=selected_engine_version, expected_type=type_hints["selected_engine_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if effective_engine_version is not None:
                self._values["effective_engine_version"] = effective_engine_version
            if selected_engine_version is not None:
                self._values["selected_engine_version"] = selected_engine_version

        @builtins.property
        def effective_engine_version(self) -> typing.Optional[builtins.str]:
            '''Read only.

            The engine version on which the query runs. If the user requests a valid engine version other than Auto, the effective engine version is the same as the engine version that the user requested. If the user requests Auto, the effective engine version is chosen by Athena. When a request to update the engine version is made by a ``CreateWorkGroup`` or ``UpdateWorkGroup`` operation, the ``EffectiveEngineVersion`` field is ignored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineversion.html#cfn-athena-workgroup-engineversion-effectiveengineversion
            '''
            result = self._values.get("effective_engine_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def selected_engine_version(self) -> typing.Optional[builtins.str]:
            '''The engine version requested by the user.

            Possible values are determined by the output of ``ListEngineVersions`` , including AUTO. The default is AUTO.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-engineversion.html#cfn-athena-workgroup-engineversion-selectedengineversion
            '''
            result = self._values.get("selected_engine_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EngineVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "kms_key": "kmsKey"},
    )
    class ManagedLoggingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            kms_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for delivering logs to Amazon S3 buckets.

            :param enabled: Enables mamanged log persistence.
            :param kms_key: The KMS key ARN to encrypt the logs stored in managed log persistence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-managedloggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                managed_logging_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty(
                    enabled=False,
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dfa2d33d8eb81556eecf017c927f907be2c8bfa9bca22ef5b2ce17d34e9e94b7)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables mamanged log persistence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-managedloggingconfiguration.html#cfn-athena-workgroup-managedloggingconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''The KMS key ARN to encrypt the logs stored in managed log persistence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-managedloggingconfiguration.html#cfn-athena-workgroup-managedloggingconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedLoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "encryption_configuration": "encryptionConfiguration",
        },
    )
    class ManagedQueryResultsConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for storing results in Athena owned storage, which includes whether this feature is enabled;

            whether encryption configuration, if any, is used for encrypting query results.

            :param enabled: If set to true, allows you to store query results in Athena owned storage. If set to false, workgroup member stores query results in location specified under ``ResultConfiguration$OutputLocation`` . The default is false. A workgroup cannot have the ``ResultConfiguration$OutputLocation`` parameter when you set this field to true.
            :param encryption_configuration: If you encrypt query and calculation results in Athena owned storage, this field indicates the encryption option (for example, SSE_KMS or CSE_KMS) and key information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-managedqueryresultsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                managed_query_results_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty(
                    enabled=False,
                    encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty(
                        kms_key="kmsKey"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__467aea3e35fdfbc26e40e12fb4dc7e9d683b04e88e9bb8eaa086db8b50a88c53)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to true, allows you to store query results in Athena owned storage.

            If set to false, workgroup member stores query results in location specified under ``ResultConfiguration$OutputLocation`` . The default is false. A workgroup cannot have the ``ResultConfiguration$OutputLocation`` parameter when you set this field to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-managedqueryresultsconfiguration.html#cfn-athena-workgroup-managedqueryresultsconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty"]]:
            '''If you encrypt query and calculation results in Athena owned storage, this field indicates the encryption option (for example, SSE_KMS or CSE_KMS) and key information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-managedqueryresultsconfiguration.html#cfn-athena-workgroup-managedqueryresultsconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedQueryResultsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key": "kmsKey"},
    )
    class ManagedStorageEncryptionConfigurationProperty:
        def __init__(self, *, kms_key: typing.Optional[builtins.str] = None) -> None:
            '''Indicates the encryption configuration for Athena Managed Storage.

            If not setting this field, Managed Storage will encrypt the query results with Athena's encryption key

            :param kms_key: For SSE-KMS and CSE-KMS, this is the KMS key ARN or ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-managedstorageencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                managed_storage_encryption_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty(
                    kms_key="kmsKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e67963480c4243b42018196444982c4199e1c5538a098c17ac51743bb7323c53)
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''For SSE-KMS and CSE-KMS, this is the KMS key ARN or ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-managedstorageencryptionconfiguration.html#cfn-athena-workgroup-managedstorageencryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedStorageEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.MonitoringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logging_configuration": "cloudWatchLoggingConfiguration",
            "managed_logging_configuration": "managedLoggingConfiguration",
            "s3_logging_configuration": "s3LoggingConfiguration",
        },
    )
    class MonitoringConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            managed_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the configuration settings for managed log persistence, delivering logs to Amazon S3 buckets, Amazon CloudWatch log groups etc.

            :param cloud_watch_logging_configuration: Configuration settings for delivering logs to Amazon CloudWatch log groups.
            :param managed_logging_configuration: Configuration settings for managed log persistence.
            :param s3_logging_configuration: Configuration settings for delivering logs to Amazon S3 buckets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-monitoringconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                monitoring_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.MonitoringConfigurationProperty(
                    cloud_watch_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty(
                        enabled=False,
                        log_group="logGroup",
                        log_stream_name_prefix="logStreamNamePrefix",
                        log_types={
                            "log_types_key": ["logTypes"]
                        }
                    ),
                    managed_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty(
                        enabled=False,
                        kms_key="kmsKey"
                    ),
                    s3_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty(
                        enabled=False,
                        kms_key="kmsKey",
                        log_location="logLocation"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__748dee28bc9bfd3c61d0214707f4e0f5bc22e564d582a2b921378d74bdb2491b)
                check_type(argname="argument cloud_watch_logging_configuration", value=cloud_watch_logging_configuration, expected_type=type_hints["cloud_watch_logging_configuration"])
                check_type(argname="argument managed_logging_configuration", value=managed_logging_configuration, expected_type=type_hints["managed_logging_configuration"])
                check_type(argname="argument s3_logging_configuration", value=s3_logging_configuration, expected_type=type_hints["s3_logging_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logging_configuration is not None:
                self._values["cloud_watch_logging_configuration"] = cloud_watch_logging_configuration
            if managed_logging_configuration is not None:
                self._values["managed_logging_configuration"] = managed_logging_configuration
            if s3_logging_configuration is not None:
                self._values["s3_logging_configuration"] = s3_logging_configuration

        @builtins.property
        def cloud_watch_logging_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty"]]:
            '''Configuration settings for delivering logs to Amazon CloudWatch log groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-monitoringconfiguration.html#cfn-athena-workgroup-monitoringconfiguration-cloudwatchloggingconfiguration
            '''
            result = self._values.get("cloud_watch_logging_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty"]], result)

        @builtins.property
        def managed_logging_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty"]]:
            '''Configuration settings for managed log persistence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-monitoringconfiguration.html#cfn-athena-workgroup-monitoringconfiguration-managedloggingconfiguration
            '''
            result = self._values.get("managed_logging_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty"]], result)

        @builtins.property
        def s3_logging_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty"]]:
            '''Configuration settings for delivering logs to Amazon S3 buckets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-monitoringconfiguration.html#cfn-athena-workgroup-monitoringconfiguration-s3loggingconfiguration
            '''
            result = self._values.get("s3_logging_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonitoringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.ResultConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acl_configuration": "aclConfiguration",
            "encryption_configuration": "encryptionConfiguration",
            "expected_bucket_owner": "expectedBucketOwner",
            "output_location": "outputLocation",
        },
    )
    class ResultConfigurationProperty:
        def __init__(
            self,
            *,
            acl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.AclConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            expected_bucket_owner: typing.Optional[builtins.str] = None,
            output_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location in Amazon S3 where query and calculation results are stored and the encryption option, if any, used for query and calculation results.

            These are known as "client-side settings". If workgroup settings override client-side settings, then the query uses the workgroup settings.

            :param acl_configuration: Indicates that an Amazon S3 canned ACL should be set to control ownership of stored query results. Currently the only supported canned ACL is ``BUCKET_OWNER_FULL_CONTROL`` . This is a client-side setting. If workgroup settings override client-side settings, then the query uses the ACL configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` .
            :param encryption_configuration: If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS`` ) and key information. This is a client-side setting. If workgroup settings override client-side settings, then the query uses the encryption configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` and `Override client-side settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param expected_bucket_owner: The account ID that you expect to be the owner of the Amazon S3 bucket specified by ``ResultConfiguration:OutputLocation`` . If set, Athena uses the value for ``ExpectedBucketOwner`` when it makes Amazon S3 calls to your specified output location. If the ``ExpectedBucketOwner`` account ID does not match the actual owner of the Amazon S3 bucket, the call fails with a permissions error. This is a client-side setting. If workgroup settings override client-side settings, then the query uses the ``ExpectedBucketOwner`` setting that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` .
            :param output_location: The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/`` . To run a query, you must specify the query results location using either a client-side setting for individual queries or a location specified by the workgroup. If workgroup settings override client-side settings, then the query uses the location specified for the workgroup. If no query location is set, Athena issues an error. For more information, see `Work with query results and recent queries <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ and ``EnforceWorkGroupConfiguration`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                result_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.ResultConfigurationProperty(
                    acl_configuration=athena_mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty(
                        s3_acl_option="s3AclOption"
                    ),
                    encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty(
                        encryption_option="encryptionOption",
                        kms_key="kmsKey"
                    ),
                    expected_bucket_owner="expectedBucketOwner",
                    output_location="outputLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__293b867e7a4870221dba8cc3d5bb59c883dee9ef61857f6656960d3b6c5c7702)
                check_type(argname="argument acl_configuration", value=acl_configuration, expected_type=type_hints["acl_configuration"])
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
                check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acl_configuration is not None:
                self._values["acl_configuration"] = acl_configuration
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if expected_bucket_owner is not None:
                self._values["expected_bucket_owner"] = expected_bucket_owner
            if output_location is not None:
                self._values["output_location"] = output_location

        @builtins.property
        def acl_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.AclConfigurationProperty"]]:
            '''Indicates that an Amazon S3 canned ACL should be set to control ownership of stored query results.

            Currently the only supported canned ACL is ``BUCKET_OWNER_FULL_CONTROL`` . This is a client-side setting. If workgroup settings override client-side settings, then the query uses the ACL configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-aclconfiguration
            '''
            result = self._values.get("acl_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.AclConfigurationProperty"]], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EncryptionConfigurationProperty"]]:
            '''If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS`` ) and key information.

            This is a client-side setting. If workgroup settings override client-side settings, then the query uses the encryption configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` and `Override client-side settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EncryptionConfigurationProperty"]], result)

        @builtins.property
        def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The account ID that you expect to be the owner of the Amazon S3 bucket specified by ``ResultConfiguration:OutputLocation`` .

            If set, Athena uses the value for ``ExpectedBucketOwner`` when it makes Amazon S3 calls to your specified output location. If the ``ExpectedBucketOwner`` account ID does not match the actual owner of the Amazon S3 bucket, the call fails with a permissions error.

            This is a client-side setting. If workgroup settings override client-side settings, then the query uses the ``ExpectedBucketOwner`` setting that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ``EnforceWorkGroupConfiguration`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-expectedbucketowner
            '''
            result = self._values.get("expected_bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_location(self) -> typing.Optional[builtins.str]:
            '''The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/`` .

            To run a query, you must specify the query results location using either a client-side setting for individual queries or a location specified by the workgroup. If workgroup settings override client-side settings, then the query uses the location specified for the workgroup. If no query location is set, Athena issues an error. For more information, see `Work with query results and recent queries <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ and ``EnforceWorkGroupConfiguration`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-outputlocation
            '''
            result = self._values.get("output_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResultConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.ResultConfigurationUpdatesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acl_configuration": "aclConfiguration",
            "encryption_configuration": "encryptionConfiguration",
            "expected_bucket_owner": "expectedBucketOwner",
            "output_location": "outputLocation",
            "remove_acl_configuration": "removeAclConfiguration",
            "remove_encryption_configuration": "removeEncryptionConfiguration",
            "remove_expected_bucket_owner": "removeExpectedBucketOwner",
            "remove_output_location": "removeOutputLocation",
        },
    )
    class ResultConfigurationUpdatesProperty:
        def __init__(
            self,
            *,
            acl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.AclConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            expected_bucket_owner: typing.Optional[builtins.str] = None,
            output_location: typing.Optional[builtins.str] = None,
            remove_acl_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            remove_encryption_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            remove_expected_bucket_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            remove_output_location: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The information about the updates in the query results, such as output location and encryption configuration for the query results.

            :param acl_configuration: The ACL configuration for the query results.
            :param encryption_configuration: The encryption configuration for the query results.
            :param expected_bucket_owner: The AWS account ID that you expect to be the owner of the Amazon S3 bucket specified by ` <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-outputlocation>`_ . If set, Athena uses the value for ``ExpectedBucketOwner`` when it makes Amazon S3 calls to your specified output location. If the ``ExpectedBucketOwner`` AWS account ID does not match the actual owner of the Amazon S3 bucket, the call fails with a permissions error. If workgroup settings override client-side settings, then the query uses the ``ExpectedBucketOwner`` setting that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ` <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-enforceworkgroupconfiguration>`_ and `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param output_location: The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/`` . For more information, see `Query Results <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ If workgroup settings override client-side settings, then the query uses the location for the query results and the encryption configuration that are specified for the workgroup. The "workgroup settings override" is specified in EnforceWorkGroupConfiguration (true/false) in the WorkGroupConfiguration. See ``EnforceWorkGroupConfiguration`` .
            :param remove_acl_configuration: If set to ``true`` , indicates that the previously-specified ACL configuration for queries in this workgroup should be ignored and set to null. If set to ``false`` or not set, and a value is present in the ``AclConfiguration`` of ``ResultConfigurationUpdates`` , the ``AclConfiguration`` in the workgroup's ``ResultConfiguration`` is updated with the new value. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param remove_encryption_configuration: If set to "true", indicates that the previously-specified encryption configuration (also known as the client-side setting) for queries in this workgroup should be ignored and set to null. If set to "false" or not set, and a value is present in the EncryptionConfiguration in ResultConfigurationUpdates (the client-side setting), the EncryptionConfiguration in the workgroup's ResultConfiguration will be updated with the new value. For more information, see `Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param remove_expected_bucket_owner: If set to "true", removes the AWS account ID previously specified for ` <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-expectedbucketowner>`_ . If set to "false" or not set, and a value is present in the ``ExpectedBucketOwner`` in ``ResultConfigurationUpdates`` (the client-side setting), the ``ExpectedBucketOwner`` in the workgroup's ``ResultConfiguration`` is updated with the new value. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param remove_output_location: If set to "true", indicates that the previously-specified query results location (also known as a client-side setting) for queries in this workgroup should be ignored and set to null. If set to "false" or not set, and a value is present in the OutputLocation in ResultConfigurationUpdates (the client-side setting), the OutputLocation in the workgroup's ResultConfiguration will be updated with the new value. For more information, see `Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                result_configuration_updates_property = athena_mixins.CfnWorkGroupPropsMixin.ResultConfigurationUpdatesProperty(
                    acl_configuration=athena_mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty(
                        s3_acl_option="s3AclOption"
                    ),
                    encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty(
                        encryption_option="encryptionOption",
                        kms_key="kmsKey"
                    ),
                    expected_bucket_owner="expectedBucketOwner",
                    output_location="outputLocation",
                    remove_acl_configuration=False,
                    remove_encryption_configuration=False,
                    remove_expected_bucket_owner=False,
                    remove_output_location=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb5cfaa5b74007facb4acc097468514679f27ec2d924cf89253e533d682020bd)
                check_type(argname="argument acl_configuration", value=acl_configuration, expected_type=type_hints["acl_configuration"])
                check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
                check_type(argname="argument expected_bucket_owner", value=expected_bucket_owner, expected_type=type_hints["expected_bucket_owner"])
                check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
                check_type(argname="argument remove_acl_configuration", value=remove_acl_configuration, expected_type=type_hints["remove_acl_configuration"])
                check_type(argname="argument remove_encryption_configuration", value=remove_encryption_configuration, expected_type=type_hints["remove_encryption_configuration"])
                check_type(argname="argument remove_expected_bucket_owner", value=remove_expected_bucket_owner, expected_type=type_hints["remove_expected_bucket_owner"])
                check_type(argname="argument remove_output_location", value=remove_output_location, expected_type=type_hints["remove_output_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acl_configuration is not None:
                self._values["acl_configuration"] = acl_configuration
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if expected_bucket_owner is not None:
                self._values["expected_bucket_owner"] = expected_bucket_owner
            if output_location is not None:
                self._values["output_location"] = output_location
            if remove_acl_configuration is not None:
                self._values["remove_acl_configuration"] = remove_acl_configuration
            if remove_encryption_configuration is not None:
                self._values["remove_encryption_configuration"] = remove_encryption_configuration
            if remove_expected_bucket_owner is not None:
                self._values["remove_expected_bucket_owner"] = remove_expected_bucket_owner
            if remove_output_location is not None:
                self._values["remove_output_location"] = remove_output_location

        @builtins.property
        def acl_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.AclConfigurationProperty"]]:
            '''The ACL configuration for the query results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-aclconfiguration
            '''
            result = self._values.get("acl_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.AclConfigurationProperty"]], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EncryptionConfigurationProperty"]]:
            '''The encryption configuration for the query results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EncryptionConfigurationProperty"]], result)

        @builtins.property
        def expected_bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The AWS account ID that you expect to be the owner of the Amazon S3 bucket specified by ` <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-outputlocation>`_ . If set, Athena uses the value for ``ExpectedBucketOwner`` when it makes Amazon S3 calls to your specified output location. If the ``ExpectedBucketOwner`` AWS account ID does not match the actual owner of the Amazon S3 bucket, the call fails with a permissions error.

            If workgroup settings override client-side settings, then the query uses the ``ExpectedBucketOwner`` setting that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup. See ` <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-enforceworkgroupconfiguration>`_ and `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-expectedbucketowner
            '''
            result = self._values.get("expected_bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_location(self) -> typing.Optional[builtins.str]:
            '''The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/`` .

            For more information, see `Query Results <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ If workgroup settings override client-side settings, then the query uses the location for the query results and the encryption configuration that are specified for the workgroup. The "workgroup settings override" is specified in EnforceWorkGroupConfiguration (true/false) in the WorkGroupConfiguration. See ``EnforceWorkGroupConfiguration`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-outputlocation
            '''
            result = self._values.get("output_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def remove_acl_configuration(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to ``true`` , indicates that the previously-specified ACL configuration for queries in this workgroup should be ignored and set to null.

            If set to ``false`` or not set, and a value is present in the ``AclConfiguration`` of ``ResultConfigurationUpdates`` , the ``AclConfiguration`` in the workgroup's ``ResultConfiguration`` is updated with the new value. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-removeaclconfiguration
            '''
            result = self._values.get("remove_acl_configuration")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def remove_encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to "true", indicates that the previously-specified encryption configuration (also known as the client-side setting) for queries in this workgroup should be ignored and set to null.

            If set to "false" or not set, and a value is present in the EncryptionConfiguration in ResultConfigurationUpdates (the client-side setting), the EncryptionConfiguration in the workgroup's ResultConfiguration will be updated with the new value. For more information, see `Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-removeencryptionconfiguration
            '''
            result = self._values.get("remove_encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def remove_expected_bucket_owner(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to "true", removes the AWS account ID previously specified for ` <https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-athena-workgroup-resultconfiguration.html#cfn-athena-workgroup-resultconfiguration-expectedbucketowner>`_ . If set to "false" or not set, and a value is present in the ``ExpectedBucketOwner`` in ``ResultConfigurationUpdates`` (the client-side setting), the ``ExpectedBucketOwner`` in the workgroup's ``ResultConfiguration`` is updated with the new value. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-removeexpectedbucketowner
            '''
            result = self._values.get("remove_expected_bucket_owner")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def remove_output_location(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to "true", indicates that the previously-specified query results location (also known as a client-side setting) for queries in this workgroup should be ignored and set to null.

            If set to "false" or not set, and a value is present in the OutputLocation in ResultConfigurationUpdates (the client-side setting), the OutputLocation in the workgroup's ResultConfiguration will be updated with the new value. For more information, see `Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-resultconfigurationupdates.html#cfn-athena-workgroup-resultconfigurationupdates-removeoutputlocation
            '''
            result = self._values.get("remove_output_location")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResultConfigurationUpdatesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "kms_key": "kmsKey",
            "log_location": "logLocation",
        },
    )
    class S3LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            kms_key: typing.Optional[builtins.str] = None,
            log_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for delivering logs to Amazon S3 buckets.

            :param enabled: Enables S3 log delivery.
            :param kms_key: The KMS key ARN to encrypt the logs published to the given Amazon S3 destination.
            :param log_location: The Amazon S3 destination URI for log publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-s3loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                s3_logging_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty(
                    enabled=False,
                    kms_key="kmsKey",
                    log_location="logLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59d8cf7faceb9ec6594cd089c5be1c3e8d8bead1b37e0e98d130acc30ce35e0b)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
                check_type(argname="argument log_location", value=log_location, expected_type=type_hints["log_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if kms_key is not None:
                self._values["kms_key"] = kms_key
            if log_location is not None:
                self._values["log_location"] = log_location

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables S3 log delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-s3loggingconfiguration.html#cfn-athena-workgroup-s3loggingconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''The KMS key ARN to encrypt the logs published to the given Amazon S3 destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-s3loggingconfiguration.html#cfn-athena-workgroup-s3loggingconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_location(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 destination URI for log publishing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-s3loggingconfiguration.html#cfn-athena-workgroup-s3loggingconfiguration-loglocation
            '''
            result = self._values.get("log_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.WorkGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_configuration": "additionalConfiguration",
            "bytes_scanned_cutoff_per_query": "bytesScannedCutoffPerQuery",
            "customer_content_encryption_configuration": "customerContentEncryptionConfiguration",
            "enforce_work_group_configuration": "enforceWorkGroupConfiguration",
            "engine_configuration": "engineConfiguration",
            "engine_version": "engineVersion",
            "execution_role": "executionRole",
            "managed_query_results_configuration": "managedQueryResultsConfiguration",
            "monitoring_configuration": "monitoringConfiguration",
            "publish_cloud_watch_metrics_enabled": "publishCloudWatchMetricsEnabled",
            "requester_pays_enabled": "requesterPaysEnabled",
            "result_configuration": "resultConfiguration",
        },
    )
    class WorkGroupConfigurationProperty:
        def __init__(
            self,
            *,
            additional_configuration: typing.Optional[builtins.str] = None,
            bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
            customer_content_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enforce_work_group_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            engine_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.EngineConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            engine_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.EngineVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            execution_role: typing.Optional[builtins.str] = None,
            managed_query_results_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.MonitoringConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            result_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.ResultConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of the workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether Amazon CloudWatch Metrics are enabled for the workgroup, and the limit for the amount of bytes scanned (cutoff) per query, if it is specified.

            The ``EnforceWorkGroupConfiguration`` option determines whether workgroup settings override client-side query settings.

            :param additional_configuration: Specifies a user defined JSON string that is passed to the session engine.
            :param bytes_scanned_cutoff_per_query: The upper limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan. No default is defined. .. epigraph:: This property currently supports integer types. Support for long values is planned.
            :param customer_content_encryption_configuration: Specifies the KMS key that is used to encrypt the user's data stores in Athena. This setting does not apply to Athena SQL workgroups.
            :param enforce_work_group_configuration: If set to "true", the settings for the workgroup override client-side settings. If set to "false", client-side settings are used. For more information, see `Override client-side settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .
            :param engine_configuration: The engine configuration for running queries.
            :param engine_version: The engine version that all queries running on the workgroup use.
            :param execution_role: Role used to access user resources in an Athena for Apache Spark session. This property applies only to Spark-enabled workgroups in Athena.
            :param managed_query_results_configuration: The configuration for storing results in Athena owned storage, which includes whether this feature is enabled; whether encryption configuration, if any, is used for encrypting query results.
            :param monitoring_configuration: Contains the configuration settings for managed log persistence, delivering logs to Amazon S3 buckets, Amazon CloudWatch log groups etc.
            :param publish_cloud_watch_metrics_enabled: Indicates that the Amazon CloudWatch metrics are enabled for the workgroup.
            :param requester_pays_enabled: If set to ``true`` , allows members assigned to a workgroup to reference Amazon S3 Requester Pays buckets in queries. If set to ``false`` , workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error. The default is ``false`` . For more information about Requester Pays buckets, see `Requester Pays Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html>`_ in the *Amazon Simple Storage Service Developer Guide* .
            :param result_configuration: Specifies the location in Amazon S3 where query results are stored and the encryption option, if any, used for query results. For more information, see `Work with query results and recent queries <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                work_group_configuration_property = athena_mixins.CfnWorkGroupPropsMixin.WorkGroupConfigurationProperty(
                    additional_configuration="additionalConfiguration",
                    bytes_scanned_cutoff_per_query=123,
                    customer_content_encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty(
                        kms_key="kmsKey"
                    ),
                    enforce_work_group_configuration=False,
                    engine_configuration=athena_mixins.CfnWorkGroupPropsMixin.EngineConfigurationProperty(
                        additional_configs={
                            "additional_configs_key": "additionalConfigs"
                        },
                        classifications=[athena_mixins.CfnWorkGroupPropsMixin.ClassificationProperty(
                            name="name",
                            properties={
                                "properties_key": "properties"
                            }
                        )],
                        coordinator_dpu_size=123,
                        default_executor_dpu_size=123,
                        max_concurrent_dpus=123,
                        spark_properties={
                            "spark_properties_key": "sparkProperties"
                        }
                    ),
                    engine_version=athena_mixins.CfnWorkGroupPropsMixin.EngineVersionProperty(
                        effective_engine_version="effectiveEngineVersion",
                        selected_engine_version="selectedEngineVersion"
                    ),
                    execution_role="executionRole",
                    managed_query_results_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty(
                        enabled=False,
                        encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty(
                            kms_key="kmsKey"
                        )
                    ),
                    monitoring_configuration=athena_mixins.CfnWorkGroupPropsMixin.MonitoringConfigurationProperty(
                        cloud_watch_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty(
                            enabled=False,
                            log_group="logGroup",
                            log_stream_name_prefix="logStreamNamePrefix",
                            log_types={
                                "log_types_key": ["logTypes"]
                            }
                        ),
                        managed_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty(
                            enabled=False,
                            kms_key="kmsKey"
                        ),
                        s3_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty(
                            enabled=False,
                            kms_key="kmsKey",
                            log_location="logLocation"
                        )
                    ),
                    publish_cloud_watch_metrics_enabled=False,
                    requester_pays_enabled=False,
                    result_configuration=athena_mixins.CfnWorkGroupPropsMixin.ResultConfigurationProperty(
                        acl_configuration=athena_mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty(
                            s3_acl_option="s3AclOption"
                        ),
                        encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty(
                            encryption_option="encryptionOption",
                            kms_key="kmsKey"
                        ),
                        expected_bucket_owner="expectedBucketOwner",
                        output_location="outputLocation"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d3c8cd202b370d55f3a19edf98c126c474cb2eb03d6f5e38fb2262fdb67f771)
                check_type(argname="argument additional_configuration", value=additional_configuration, expected_type=type_hints["additional_configuration"])
                check_type(argname="argument bytes_scanned_cutoff_per_query", value=bytes_scanned_cutoff_per_query, expected_type=type_hints["bytes_scanned_cutoff_per_query"])
                check_type(argname="argument customer_content_encryption_configuration", value=customer_content_encryption_configuration, expected_type=type_hints["customer_content_encryption_configuration"])
                check_type(argname="argument enforce_work_group_configuration", value=enforce_work_group_configuration, expected_type=type_hints["enforce_work_group_configuration"])
                check_type(argname="argument engine_configuration", value=engine_configuration, expected_type=type_hints["engine_configuration"])
                check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
                check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
                check_type(argname="argument managed_query_results_configuration", value=managed_query_results_configuration, expected_type=type_hints["managed_query_results_configuration"])
                check_type(argname="argument monitoring_configuration", value=monitoring_configuration, expected_type=type_hints["monitoring_configuration"])
                check_type(argname="argument publish_cloud_watch_metrics_enabled", value=publish_cloud_watch_metrics_enabled, expected_type=type_hints["publish_cloud_watch_metrics_enabled"])
                check_type(argname="argument requester_pays_enabled", value=requester_pays_enabled, expected_type=type_hints["requester_pays_enabled"])
                check_type(argname="argument result_configuration", value=result_configuration, expected_type=type_hints["result_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_configuration is not None:
                self._values["additional_configuration"] = additional_configuration
            if bytes_scanned_cutoff_per_query is not None:
                self._values["bytes_scanned_cutoff_per_query"] = bytes_scanned_cutoff_per_query
            if customer_content_encryption_configuration is not None:
                self._values["customer_content_encryption_configuration"] = customer_content_encryption_configuration
            if enforce_work_group_configuration is not None:
                self._values["enforce_work_group_configuration"] = enforce_work_group_configuration
            if engine_configuration is not None:
                self._values["engine_configuration"] = engine_configuration
            if engine_version is not None:
                self._values["engine_version"] = engine_version
            if execution_role is not None:
                self._values["execution_role"] = execution_role
            if managed_query_results_configuration is not None:
                self._values["managed_query_results_configuration"] = managed_query_results_configuration
            if monitoring_configuration is not None:
                self._values["monitoring_configuration"] = monitoring_configuration
            if publish_cloud_watch_metrics_enabled is not None:
                self._values["publish_cloud_watch_metrics_enabled"] = publish_cloud_watch_metrics_enabled
            if requester_pays_enabled is not None:
                self._values["requester_pays_enabled"] = requester_pays_enabled
            if result_configuration is not None:
                self._values["result_configuration"] = result_configuration

        @builtins.property
        def additional_configuration(self) -> typing.Optional[builtins.str]:
            '''Specifies a user defined JSON string that is passed to the session engine.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-additionalconfiguration
            '''
            result = self._values.get("additional_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bytes_scanned_cutoff_per_query(self) -> typing.Optional[jsii.Number]:
            '''The upper limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan.

            No default is defined.
            .. epigraph::

               This property currently supports integer types. Support for long values is planned.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-bytesscannedcutoffperquery
            '''
            result = self._values.get("bytes_scanned_cutoff_per_query")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def customer_content_encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty"]]:
            '''Specifies the KMS key that is used to encrypt the user's data stores in Athena.

            This setting does not apply to Athena SQL workgroups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-customercontentencryptionconfiguration
            '''
            result = self._values.get("customer_content_encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty"]], result)

        @builtins.property
        def enforce_work_group_configuration(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to "true", the settings for the workgroup override client-side settings.

            If set to "false", client-side settings are used. For more information, see `Override client-side settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-enforceworkgroupconfiguration
            '''
            result = self._values.get("enforce_work_group_configuration")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def engine_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EngineConfigurationProperty"]]:
            '''The engine configuration for running queries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-engineconfiguration
            '''
            result = self._values.get("engine_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EngineConfigurationProperty"]], result)

        @builtins.property
        def engine_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EngineVersionProperty"]]:
            '''The engine version that all queries running on the workgroup use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-engineversion
            '''
            result = self._values.get("engine_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EngineVersionProperty"]], result)

        @builtins.property
        def execution_role(self) -> typing.Optional[builtins.str]:
            '''Role used to access user resources in an Athena for Apache Spark session.

            This property applies only to Spark-enabled workgroups in Athena.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-executionrole
            '''
            result = self._values.get("execution_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def managed_query_results_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty"]]:
            '''The configuration for storing results in Athena owned storage, which includes whether this feature is enabled;

            whether encryption configuration, if any, is used for encrypting query results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-managedqueryresultsconfiguration
            '''
            result = self._values.get("managed_query_results_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty"]], result)

        @builtins.property
        def monitoring_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.MonitoringConfigurationProperty"]]:
            '''Contains the configuration settings for managed log persistence, delivering logs to Amazon S3 buckets, Amazon CloudWatch log groups etc.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-monitoringconfiguration
            '''
            result = self._values.get("monitoring_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.MonitoringConfigurationProperty"]], result)

        @builtins.property
        def publish_cloud_watch_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates that the Amazon CloudWatch metrics are enabled for the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-publishcloudwatchmetricsenabled
            '''
            result = self._values.get("publish_cloud_watch_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def requester_pays_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to ``true`` , allows members assigned to a workgroup to reference Amazon S3 Requester Pays buckets in queries.

            If set to ``false`` , workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error. The default is ``false`` . For more information about Requester Pays buckets, see `Requester Pays Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html>`_ in the *Amazon Simple Storage Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-requesterpaysenabled
            '''
            result = self._values.get("requester_pays_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def result_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ResultConfigurationProperty"]]:
            '''Specifies the location in Amazon S3 where query results are stored and the encryption option, if any, used for query results.

            For more information, see `Work with query results and recent queries <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfiguration.html#cfn-athena-workgroup-workgroupconfiguration-resultconfiguration
            '''
            result = self._values.get("result_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ResultConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_athena.mixins.CfnWorkGroupPropsMixin.WorkGroupConfigurationUpdatesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_configuration": "additionalConfiguration",
            "bytes_scanned_cutoff_per_query": "bytesScannedCutoffPerQuery",
            "customer_content_encryption_configuration": "customerContentEncryptionConfiguration",
            "enforce_work_group_configuration": "enforceWorkGroupConfiguration",
            "engine_configuration": "engineConfiguration",
            "engine_version": "engineVersion",
            "execution_role": "executionRole",
            "managed_query_results_configuration": "managedQueryResultsConfiguration",
            "monitoring_configuration": "monitoringConfiguration",
            "publish_cloud_watch_metrics_enabled": "publishCloudWatchMetricsEnabled",
            "remove_bytes_scanned_cutoff_per_query": "removeBytesScannedCutoffPerQuery",
            "remove_customer_content_encryption_configuration": "removeCustomerContentEncryptionConfiguration",
            "requester_pays_enabled": "requesterPaysEnabled",
            "result_configuration_updates": "resultConfigurationUpdates",
        },
    )
    class WorkGroupConfigurationUpdatesProperty:
        def __init__(
            self,
            *,
            additional_configuration: typing.Optional[builtins.str] = None,
            bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
            customer_content_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enforce_work_group_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            engine_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.EngineConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            engine_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.EngineVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            execution_role: typing.Optional[builtins.str] = None,
            managed_query_results_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.MonitoringConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            remove_bytes_scanned_cutoff_per_query: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            remove_customer_content_encryption_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            result_configuration_updates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkGroupPropsMixin.ResultConfigurationUpdatesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration information that will be updated for this workgroup, which includes the location in Amazon S3 where query results are stored, the encryption option, if any, used for query results, whether the Amazon CloudWatch Metrics are enabled for the workgroup, whether the workgroup settings override the client-side settings, and the data usage limit for the amount of bytes scanned per query, if it is specified.

            :param additional_configuration: Additional Configuration that are passed to Athena Spark Calculations running in this workgroup.
            :param bytes_scanned_cutoff_per_query: The upper data usage limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan.
            :param customer_content_encryption_configuration: Indicates the KMS key for encrypting notebook content.
            :param enforce_work_group_configuration: If set to "true", the settings for the workgroup override client-side settings. If set to "false", client-side settings are used
            :param engine_configuration: The engine configuration for running queries.
            :param engine_version: The Athena engine version for running queries.
            :param execution_role: The ARN of the execution role used to access user resources for Spark sessions and Identity Center enabled workgroups. This property applies only to Spark enabled workgroups and Identity Center enabled workgroups.
            :param managed_query_results_configuration: The configuration for the managed query results and encryption option. ResultConfiguration and ManagedQueryResultsConfiguration cannot be set at the same time
            :param monitoring_configuration: Contains the configuration settings for managed log persistence, delivering logs to Amazon S3 buckets, Amazon CloudWatch log groups etc.
            :param publish_cloud_watch_metrics_enabled: Indicates that the Amazon CloudWatch metrics are enabled for the workgroup.
            :param remove_bytes_scanned_cutoff_per_query: Indicates that the data usage control limit per query is removed.
            :param remove_customer_content_encryption_configuration: 
            :param requester_pays_enabled: If set to true, allows members assigned to a workgroup to reference Amazon S3 Requester Pays buckets in queries. If set to false, workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error.
            :param result_configuration_updates: The result configuration information about the queries in this workgroup that will be updated. Includes the updated results location and an updated option for encrypting query results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_athena import mixins as athena_mixins
                
                work_group_configuration_updates_property = athena_mixins.CfnWorkGroupPropsMixin.WorkGroupConfigurationUpdatesProperty(
                    additional_configuration="additionalConfiguration",
                    bytes_scanned_cutoff_per_query=123,
                    customer_content_encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty(
                        kms_key="kmsKey"
                    ),
                    enforce_work_group_configuration=False,
                    engine_configuration=athena_mixins.CfnWorkGroupPropsMixin.EngineConfigurationProperty(
                        additional_configs={
                            "additional_configs_key": "additionalConfigs"
                        },
                        classifications=[athena_mixins.CfnWorkGroupPropsMixin.ClassificationProperty(
                            name="name",
                            properties={
                                "properties_key": "properties"
                            }
                        )],
                        coordinator_dpu_size=123,
                        default_executor_dpu_size=123,
                        max_concurrent_dpus=123,
                        spark_properties={
                            "spark_properties_key": "sparkProperties"
                        }
                    ),
                    engine_version=athena_mixins.CfnWorkGroupPropsMixin.EngineVersionProperty(
                        effective_engine_version="effectiveEngineVersion",
                        selected_engine_version="selectedEngineVersion"
                    ),
                    execution_role="executionRole",
                    managed_query_results_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty(
                        enabled=False,
                        encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty(
                            kms_key="kmsKey"
                        )
                    ),
                    monitoring_configuration=athena_mixins.CfnWorkGroupPropsMixin.MonitoringConfigurationProperty(
                        cloud_watch_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty(
                            enabled=False,
                            log_group="logGroup",
                            log_stream_name_prefix="logStreamNamePrefix",
                            log_types={
                                "log_types_key": ["logTypes"]
                            }
                        ),
                        managed_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty(
                            enabled=False,
                            kms_key="kmsKey"
                        ),
                        s3_logging_configuration=athena_mixins.CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty(
                            enabled=False,
                            kms_key="kmsKey",
                            log_location="logLocation"
                        )
                    ),
                    publish_cloud_watch_metrics_enabled=False,
                    remove_bytes_scanned_cutoff_per_query=False,
                    remove_customer_content_encryption_configuration=False,
                    requester_pays_enabled=False,
                    result_configuration_updates=athena_mixins.CfnWorkGroupPropsMixin.ResultConfigurationUpdatesProperty(
                        acl_configuration=athena_mixins.CfnWorkGroupPropsMixin.AclConfigurationProperty(
                            s3_acl_option="s3AclOption"
                        ),
                        encryption_configuration=athena_mixins.CfnWorkGroupPropsMixin.EncryptionConfigurationProperty(
                            encryption_option="encryptionOption",
                            kms_key="kmsKey"
                        ),
                        expected_bucket_owner="expectedBucketOwner",
                        output_location="outputLocation",
                        remove_acl_configuration=False,
                        remove_encryption_configuration=False,
                        remove_expected_bucket_owner=False,
                        remove_output_location=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d9bacb91d05b5f68b42b56514943055d485eb90130113d1c4141f4f9c2d483a)
                check_type(argname="argument additional_configuration", value=additional_configuration, expected_type=type_hints["additional_configuration"])
                check_type(argname="argument bytes_scanned_cutoff_per_query", value=bytes_scanned_cutoff_per_query, expected_type=type_hints["bytes_scanned_cutoff_per_query"])
                check_type(argname="argument customer_content_encryption_configuration", value=customer_content_encryption_configuration, expected_type=type_hints["customer_content_encryption_configuration"])
                check_type(argname="argument enforce_work_group_configuration", value=enforce_work_group_configuration, expected_type=type_hints["enforce_work_group_configuration"])
                check_type(argname="argument engine_configuration", value=engine_configuration, expected_type=type_hints["engine_configuration"])
                check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
                check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
                check_type(argname="argument managed_query_results_configuration", value=managed_query_results_configuration, expected_type=type_hints["managed_query_results_configuration"])
                check_type(argname="argument monitoring_configuration", value=monitoring_configuration, expected_type=type_hints["monitoring_configuration"])
                check_type(argname="argument publish_cloud_watch_metrics_enabled", value=publish_cloud_watch_metrics_enabled, expected_type=type_hints["publish_cloud_watch_metrics_enabled"])
                check_type(argname="argument remove_bytes_scanned_cutoff_per_query", value=remove_bytes_scanned_cutoff_per_query, expected_type=type_hints["remove_bytes_scanned_cutoff_per_query"])
                check_type(argname="argument remove_customer_content_encryption_configuration", value=remove_customer_content_encryption_configuration, expected_type=type_hints["remove_customer_content_encryption_configuration"])
                check_type(argname="argument requester_pays_enabled", value=requester_pays_enabled, expected_type=type_hints["requester_pays_enabled"])
                check_type(argname="argument result_configuration_updates", value=result_configuration_updates, expected_type=type_hints["result_configuration_updates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if additional_configuration is not None:
                self._values["additional_configuration"] = additional_configuration
            if bytes_scanned_cutoff_per_query is not None:
                self._values["bytes_scanned_cutoff_per_query"] = bytes_scanned_cutoff_per_query
            if customer_content_encryption_configuration is not None:
                self._values["customer_content_encryption_configuration"] = customer_content_encryption_configuration
            if enforce_work_group_configuration is not None:
                self._values["enforce_work_group_configuration"] = enforce_work_group_configuration
            if engine_configuration is not None:
                self._values["engine_configuration"] = engine_configuration
            if engine_version is not None:
                self._values["engine_version"] = engine_version
            if execution_role is not None:
                self._values["execution_role"] = execution_role
            if managed_query_results_configuration is not None:
                self._values["managed_query_results_configuration"] = managed_query_results_configuration
            if monitoring_configuration is not None:
                self._values["monitoring_configuration"] = monitoring_configuration
            if publish_cloud_watch_metrics_enabled is not None:
                self._values["publish_cloud_watch_metrics_enabled"] = publish_cloud_watch_metrics_enabled
            if remove_bytes_scanned_cutoff_per_query is not None:
                self._values["remove_bytes_scanned_cutoff_per_query"] = remove_bytes_scanned_cutoff_per_query
            if remove_customer_content_encryption_configuration is not None:
                self._values["remove_customer_content_encryption_configuration"] = remove_customer_content_encryption_configuration
            if requester_pays_enabled is not None:
                self._values["requester_pays_enabled"] = requester_pays_enabled
            if result_configuration_updates is not None:
                self._values["result_configuration_updates"] = result_configuration_updates

        @builtins.property
        def additional_configuration(self) -> typing.Optional[builtins.str]:
            '''Additional Configuration that are passed to Athena Spark Calculations running in this workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-additionalconfiguration
            '''
            result = self._values.get("additional_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bytes_scanned_cutoff_per_query(self) -> typing.Optional[jsii.Number]:
            '''The upper data usage limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-bytesscannedcutoffperquery
            '''
            result = self._values.get("bytes_scanned_cutoff_per_query")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def customer_content_encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty"]]:
            '''Indicates the KMS key for encrypting notebook content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-customercontentencryptionconfiguration
            '''
            result = self._values.get("customer_content_encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty"]], result)

        @builtins.property
        def enforce_work_group_configuration(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to "true", the settings for the workgroup override client-side settings.

            If set to "false", client-side settings are used

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-enforceworkgroupconfiguration
            '''
            result = self._values.get("enforce_work_group_configuration")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def engine_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EngineConfigurationProperty"]]:
            '''The engine configuration for running queries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-engineconfiguration
            '''
            result = self._values.get("engine_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EngineConfigurationProperty"]], result)

        @builtins.property
        def engine_version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EngineVersionProperty"]]:
            '''The Athena engine version for running queries.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-engineversion
            '''
            result = self._values.get("engine_version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.EngineVersionProperty"]], result)

        @builtins.property
        def execution_role(self) -> typing.Optional[builtins.str]:
            '''The ARN of the execution role used to access user resources for Spark sessions and Identity Center enabled workgroups.

            This property applies only to Spark enabled workgroups and Identity Center enabled workgroups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-executionrole
            '''
            result = self._values.get("execution_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def managed_query_results_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty"]]:
            '''The configuration for the managed query results and encryption option.

            ResultConfiguration and ManagedQueryResultsConfiguration cannot be set at the same time

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-managedqueryresultsconfiguration
            '''
            result = self._values.get("managed_query_results_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty"]], result)

        @builtins.property
        def monitoring_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.MonitoringConfigurationProperty"]]:
            '''Contains the configuration settings for managed log persistence, delivering logs to Amazon S3 buckets, Amazon CloudWatch log groups etc.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-monitoringconfiguration
            '''
            result = self._values.get("monitoring_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.MonitoringConfigurationProperty"]], result)

        @builtins.property
        def publish_cloud_watch_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates that the Amazon CloudWatch metrics are enabled for the workgroup.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-publishcloudwatchmetricsenabled
            '''
            result = self._values.get("publish_cloud_watch_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def remove_bytes_scanned_cutoff_per_query(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates that the data usage control limit per query is removed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-removebytesscannedcutoffperquery
            '''
            result = self._values.get("remove_bytes_scanned_cutoff_per_query")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def remove_customer_content_encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-removecustomercontentencryptionconfiguration
            '''
            result = self._values.get("remove_customer_content_encryption_configuration")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def requester_pays_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to true, allows members assigned to a workgroup to reference Amazon S3 Requester Pays buckets in queries.

            If set to false, workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-requesterpaysenabled
            '''
            result = self._values.get("requester_pays_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def result_configuration_updates(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ResultConfigurationUpdatesProperty"]]:
            '''The result configuration information about the queries in this workgroup that will be updated.

            Includes the updated results location and an updated option for encrypting query results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-athena-workgroup-workgroupconfigurationupdates.html#cfn-athena-workgroup-workgroupconfigurationupdates-resultconfigurationupdates
            '''
            result = self._values.get("result_configuration_updates")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkGroupPropsMixin.ResultConfigurationUpdatesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkGroupConfigurationUpdatesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCapacityReservationMixinProps",
    "CfnCapacityReservationPropsMixin",
    "CfnDataCatalogMixinProps",
    "CfnDataCatalogPropsMixin",
    "CfnNamedQueryMixinProps",
    "CfnNamedQueryPropsMixin",
    "CfnPreparedStatementMixinProps",
    "CfnPreparedStatementPropsMixin",
    "CfnWorkGroupMixinProps",
    "CfnWorkGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__92ee2c7975f956dfc7e9b625720d72562025a14f8526a764b4dec46d90d6bcb0(
    *,
    capacity_assignment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapacityReservationPropsMixin.CapacityAssignmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_dpus: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34bbdaac95a876c2c6487794bb811243b92542acc648f6753283505377bffcee(
    props: typing.Union[CfnCapacityReservationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68bfb1bed5c98477d2c416730db01bf084e54f99f516320f93089aa7b7f81ea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9064dcc3ec5b6a56e6b2c6b15faf957fc5117757793d56c93a9adbb5dcd00f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934ddff30bb89e8563e9a97c2c35f238318d86ab3d79530b16674c1696221e7d(
    *,
    capacity_assignments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapacityReservationPropsMixin.CapacityAssignmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af04eb5b4f2ba4696cc389c365112c75632ecc739046be7569140fc4e449b316(
    *,
    workgroup_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46bb671fea4e862c9f65c8326220f4108aa3e0987c6b1ac8a584e2c02d70a608(
    *,
    connection_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    error: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570f70585b42dd2757b7bf8bac72f472548501330ea28d66ca989cf8c220e1ba(
    props: typing.Union[CfnDataCatalogMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4dc185a35fd6a945992041c91289ba4ddbb47e8c9de282f7b38c6a29cc85ca(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186cd9fce4dcd9dec5b821f70aff43a298b48ed868583e5546cb0e11ea350f46(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545562a52e4919ed105308a7a9b3d51a3ed8cb5593a528e2f6b150739f97a6ff(
    *,
    database: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    query_string: typing.Optional[builtins.str] = None,
    work_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6484b6a8b68a37521c5753db983d5fdae4fa91d0bac7cd00b3d8c1cd11a78710(
    props: typing.Union[CfnNamedQueryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4621c9d76ca901dddf6646c944a37ad76b2e43e3e136c6e2b20093e860a4348a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0338a673f732ca0b955dda1ef99ce1017db1dfdc1f8649b5cd535a8d5e21c59d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd50cb05c32ed5054c831f6b42bb9722bab71fa7c745ecc182e9ea38f5a2f2e(
    *,
    description: typing.Optional[builtins.str] = None,
    query_statement: typing.Optional[builtins.str] = None,
    statement_name: typing.Optional[builtins.str] = None,
    work_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a75ffd7e4ffba6bacbf7166f5343f5bfcce9fd77376677dbff4cbf1ce4b1469(
    props: typing.Union[CfnPreparedStatementMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145f38e9bd33e6e935d73d2a520ffe362c9462e974235a687d08f52c1279684c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d282108304ead98904b9b2c962df41e9687643601cecd5fb9296fe55e5e8237(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d517e947d90f3c5a384ca281c9ed0281cc55d94966a677ba8cf9bdd08218724b(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    recursive_delete_option: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    work_group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.WorkGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    work_group_configuration_updates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.WorkGroupConfigurationUpdatesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f768d560085fc738868daa9a467686bf08100bded04a0a23281867418a76758a(
    props: typing.Union[CfnWorkGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bf90c1a7c5451bfdbce4f0c589789c510263184cc0e9196a7f2fa51acfa635(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f617c3ec6f27a3fbce296fd9de311b475d1e14188dcb220f8d4daccf068c6f28(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d264c723cb659a190079e0614341ed89d585843cdeaa34489b0aed887ef8aa13(
    *,
    s3_acl_option: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7bbaff94503b75776b52acaf5230425c8a7bbad179e084e8963380df0a3bf3(
    *,
    name: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8117027f3559fa2756e383cc670f3b04d8b4099eb5f68c17f37c52b7345ff3(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    log_group: typing.Optional[builtins.str] = None,
    log_stream_name_prefix: typing.Optional[builtins.str] = None,
    log_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Sequence[builtins.str]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b091ea786bb208af5c181c5d51caf69ab8412c01e15254e1b808b960e4fb00(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb317ca5fd1a80660ea0ff605cd679f7593d4b10b1f1c40892f0e1fbd50c10a(
    *,
    encryption_option: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0596df3d33ac7708b71f3a646471951ae779902ded2d9e45fa16fe7b83465f2(
    *,
    additional_configs: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    classifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.ClassificationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    coordinator_dpu_size: typing.Optional[jsii.Number] = None,
    default_executor_dpu_size: typing.Optional[jsii.Number] = None,
    max_concurrent_dpus: typing.Optional[jsii.Number] = None,
    spark_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4a916b1ff47152bce0cb3de6928c9dd9725dcac1f5f2e218cef9f01f1fd148(
    *,
    effective_engine_version: typing.Optional[builtins.str] = None,
    selected_engine_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa2d33d8eb81556eecf017c927f907be2c8bfa9bca22ef5b2ce17d34e9e94b7(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467aea3e35fdfbc26e40e12fb4dc7e9d683b04e88e9bb8eaa086db8b50a88c53(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.ManagedStorageEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67963480c4243b42018196444982c4199e1c5538a098c17ac51743bb7323c53(
    *,
    kms_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748dee28bc9bfd3c61d0214707f4e0f5bc22e564d582a2b921378d74bdb2491b(
    *,
    cloud_watch_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.CloudWatchLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    managed_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.ManagedLoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_logging_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.S3LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293b867e7a4870221dba8cc3d5bb59c883dee9ef61857f6656960d3b6c5c7702(
    *,
    acl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.AclConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    output_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5cfaa5b74007facb4acc097468514679f27ec2d924cf89253e533d682020bd(
    *,
    acl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.AclConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    expected_bucket_owner: typing.Optional[builtins.str] = None,
    output_location: typing.Optional[builtins.str] = None,
    remove_acl_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    remove_encryption_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    remove_expected_bucket_owner: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    remove_output_location: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d8cf7faceb9ec6594cd089c5be1c3e8d8bead1b37e0e98d130acc30ce35e0b(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    log_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3c8cd202b370d55f3a19edf98c126c474cb2eb03d6f5e38fb2262fdb67f771(
    *,
    additional_configuration: typing.Optional[builtins.str] = None,
    bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
    customer_content_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enforce_work_group_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    engine_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.EngineConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    engine_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.EngineVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_role: typing.Optional[builtins.str] = None,
    managed_query_results_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.MonitoringConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    result_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.ResultConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9bacb91d05b5f68b42b56514943055d485eb90130113d1c4141f4f9c2d483a(
    *,
    additional_configuration: typing.Optional[builtins.str] = None,
    bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
    customer_content_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.CustomerContentEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enforce_work_group_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    engine_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.EngineConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    engine_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.EngineVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_role: typing.Optional[builtins.str] = None,
    managed_query_results_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.ManagedQueryResultsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    monitoring_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.MonitoringConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    publish_cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    remove_bytes_scanned_cutoff_per_query: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    remove_customer_content_encryption_configuration: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    requester_pays_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    result_configuration_updates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkGroupPropsMixin.ResultConfigurationUpdatesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
