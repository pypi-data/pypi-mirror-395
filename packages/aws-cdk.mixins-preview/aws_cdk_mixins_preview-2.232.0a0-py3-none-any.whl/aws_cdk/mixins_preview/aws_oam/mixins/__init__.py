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
    jsii_type="@aws-cdk/mixins-preview.aws_oam.mixins.CfnLinkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "label_template": "labelTemplate",
        "link_configuration": "linkConfiguration",
        "resource_types": "resourceTypes",
        "sink_identifier": "sinkIdentifier",
        "tags": "tags",
    },
)
class CfnLinkMixinProps:
    def __init__(
        self,
        *,
        label_template: typing.Optional[builtins.str] = None,
        link_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.LinkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        sink_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnLinkPropsMixin.

        :param label_template: Specify a friendly human-readable name to use to identify this source account when you are viewing data from it in the monitoring account. You can include the following variables in your template: - ``$AccountName`` is the name of the account - ``$AccountEmail`` is a globally-unique email address, which includes the email domain, such as ``mariagarcia@example.com`` - ``$AccountEmailNoDomain`` is an email address without the domain name, such as ``mariagarcia`` .. epigraph:: In the and Regions, the only supported option is to use custom labels, and the ``$AccountName`` , ``$AccountEmail`` , and ``$AccountEmailNoDomain`` variables all resolve as *account-id* instead of the specified variable.
        :param link_configuration: Use this structure to optionally create filters that specify that only some metric namespaces or log groups are to be shared from the source account to the monitoring account.
        :param resource_types: An array of strings that define which types of data that the source account shares with the monitoring account. Valid values are ``AWS::CloudWatch::Metric | AWS::Logs::LogGroup | AWS::XRay::Trace | AWS::ApplicationInsights::Application | AWS::InternetMonitor::Monitor`` .
        :param sink_identifier: The ARN of the sink in the monitoring account that you want to link to. You can use `ListSinks <https://docs.aws.amazon.com/OAM/latest/APIReference/API_ListSinks.html>`_ to find the ARNs of sinks.
        :param tags: An array of key-value pairs to apply to the link. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_oam import mixins as oam_mixins
            
            cfn_link_mixin_props = oam_mixins.CfnLinkMixinProps(
                label_template="labelTemplate",
                link_configuration=oam_mixins.CfnLinkPropsMixin.LinkConfigurationProperty(
                    log_group_configuration=oam_mixins.CfnLinkPropsMixin.LinkFilterProperty(
                        filter="filter"
                    ),
                    metric_configuration=oam_mixins.CfnLinkPropsMixin.LinkFilterProperty(
                        filter="filter"
                    )
                ),
                resource_types=["resourceTypes"],
                sink_identifier="sinkIdentifier",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac9e8c49ef7c68fc6efa486a9151c996a7b12805ace870578b378c6d8cc034b8)
            check_type(argname="argument label_template", value=label_template, expected_type=type_hints["label_template"])
            check_type(argname="argument link_configuration", value=link_configuration, expected_type=type_hints["link_configuration"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            check_type(argname="argument sink_identifier", value=sink_identifier, expected_type=type_hints["sink_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if label_template is not None:
            self._values["label_template"] = label_template
        if link_configuration is not None:
            self._values["link_configuration"] = link_configuration
        if resource_types is not None:
            self._values["resource_types"] = resource_types
        if sink_identifier is not None:
            self._values["sink_identifier"] = sink_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def label_template(self) -> typing.Optional[builtins.str]:
        '''Specify a friendly human-readable name to use to identify this source account when you are viewing data from it in the monitoring account.

        You can include the following variables in your template:

        - ``$AccountName`` is the name of the account
        - ``$AccountEmail`` is a globally-unique email address, which includes the email domain, such as ``mariagarcia@example.com``
        - ``$AccountEmailNoDomain`` is an email address without the domain name, such as ``mariagarcia``

        .. epigraph::

           In the  and  Regions, the only supported option is to use custom labels, and the ``$AccountName`` , ``$AccountEmail`` , and ``$AccountEmailNoDomain`` variables all resolve as *account-id* instead of the specified variable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-labeltemplate
        '''
        result = self._values.get("label_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkConfigurationProperty"]]:
        '''Use this structure to optionally create filters that specify that only some metric namespaces or log groups are to be shared from the source account to the monitoring account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-linkconfiguration
        '''
        result = self._values.get("link_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkConfigurationProperty"]], result)

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of strings that define which types of data that the source account shares with the monitoring account.

        Valid values are ``AWS::CloudWatch::Metric | AWS::Logs::LogGroup | AWS::XRay::Trace | AWS::ApplicationInsights::Application | AWS::InternetMonitor::Monitor`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-resourcetypes
        '''
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sink_identifier(self) -> typing.Optional[builtins.str]:
        '''The ARN of the sink in the monitoring account that you want to link to.

        You can use `ListSinks <https://docs.aws.amazon.com/OAM/latest/APIReference/API_ListSinks.html>`_ to find the ARNs of sinks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-sinkidentifier
        '''
        result = self._values.get("sink_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to the link.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLinkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLinkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_oam.mixins.CfnLinkPropsMixin",
):
    '''Creates a link between a source account and a sink that you have created in a monitoring account.

    Before you create a link, you must create a sink in the monitoring account. The sink must have a sink policy that permits the source account to link to it. You can grant permission to source accounts by granting permission to an entire organization, an organizational unit, or to individual accounts.

    For more information, see `CreateSink <https://docs.aws.amazon.com/OAM/latest/APIReference/API_CreateSink.html>`_ and `PutSinkPolicy <https://docs.aws.amazon.com/OAM/latest/APIReference/API_PutSinkPolicy.html>`_ .

    Each monitoring account can be linked to as many as 100,000 source accounts.

    Each source account can be linked to as many as five monitoring accounts.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html
    :cloudformationResource: AWS::Oam::Link
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_oam import mixins as oam_mixins
        
        cfn_link_props_mixin = oam_mixins.CfnLinkPropsMixin(oam_mixins.CfnLinkMixinProps(
            label_template="labelTemplate",
            link_configuration=oam_mixins.CfnLinkPropsMixin.LinkConfigurationProperty(
                log_group_configuration=oam_mixins.CfnLinkPropsMixin.LinkFilterProperty(
                    filter="filter"
                ),
                metric_configuration=oam_mixins.CfnLinkPropsMixin.LinkFilterProperty(
                    filter="filter"
                )
            ),
            resource_types=["resourceTypes"],
            sink_identifier="sinkIdentifier",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Oam::Link``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0bf9adb4646d6f4747c870b7124c994e336adbf789a7c1ea1984ef1669411ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d190ae3132e06978237f13e5e7af2ec2e0e1fda4dc723d173b002e0ad21b92ed)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e019ac486018802d6d7b88816c6095b4a8504275d21971da7ccda341cd4791c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLinkMixinProps:
        return typing.cast(CfnLinkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_oam.mixins.CfnLinkPropsMixin.LinkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_group_configuration": "logGroupConfiguration",
            "metric_configuration": "metricConfiguration",
        },
    )
    class LinkConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.LinkFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metric_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.LinkFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Use this structure to optionally create filters that specify that only some metric namespaces or log groups are to be shared from the source account to the monitoring account.

            :param log_group_configuration: Use this structure to filter which log groups are to share log events from this source account to the monitoring account.
            :param metric_configuration: Use this structure to filter which metric namespaces are to be shared from the source account to the monitoring account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-oam-link-linkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_oam import mixins as oam_mixins
                
                link_configuration_property = oam_mixins.CfnLinkPropsMixin.LinkConfigurationProperty(
                    log_group_configuration=oam_mixins.CfnLinkPropsMixin.LinkFilterProperty(
                        filter="filter"
                    ),
                    metric_configuration=oam_mixins.CfnLinkPropsMixin.LinkFilterProperty(
                        filter="filter"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa390669b3e626daa2ad1ad8b466da8157a62c9c72a5efb6f320051a109306cb)
                check_type(argname="argument log_group_configuration", value=log_group_configuration, expected_type=type_hints["log_group_configuration"])
                check_type(argname="argument metric_configuration", value=metric_configuration, expected_type=type_hints["metric_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_configuration is not None:
                self._values["log_group_configuration"] = log_group_configuration
            if metric_configuration is not None:
                self._values["metric_configuration"] = metric_configuration

        @builtins.property
        def log_group_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkFilterProperty"]]:
            '''Use this structure to filter which log groups are to share log events from this source account to the monitoring account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-oam-link-linkconfiguration.html#cfn-oam-link-linkconfiguration-loggroupconfiguration
            '''
            result = self._values.get("log_group_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkFilterProperty"]], result)

        @builtins.property
        def metric_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkFilterProperty"]]:
            '''Use this structure to filter which metric namespaces are to be shared from the source account to the monitoring account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-oam-link-linkconfiguration.html#cfn-oam-link-linkconfiguration-metricconfiguration
            '''
            result = self._values.get("metric_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.LinkFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_oam.mixins.CfnLinkPropsMixin.LinkFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"filter": "filter"},
    )
    class LinkFilterProperty:
        def __init__(self, *, filter: typing.Optional[builtins.str] = None) -> None:
            '''When used in ``MetricConfiguration`` this field specifies which metric namespaces are to be shared with the monitoring account.

            When used in ``LogGroupConfiguration`` this field specifies which log groups are to share their log events with the monitoring account. Use the term ``LogGroupName`` and one or more of the following operands.

            :param filter: When used in ``MetricConfiguration`` this field specifies which metric namespaces are to be shared with the monitoring account. When used in ``LogGroupConfiguration`` this field specifies which log groups are to share their log events with the monitoring account. Use the term ``LogGroupName`` and one or more of the following operands. Use single quotation marks (') around log group names and metric namespaces. The matching of log group names and metric namespaces is case sensitive. Each filter has a limit of five conditional operands. Conditional operands are ``AND`` and ``OR`` . - ``=`` and ``!=`` - ``AND`` - ``OR`` - ``LIKE`` and ``NOT LIKE`` . These can be used only as prefix searches. Include a ``%`` at the end of the string that you want to search for and include. - ``IN`` and ``NOT IN`` , using parentheses ``( )`` Examples: - ``Namespace NOT LIKE 'AWS/%'`` includes only namespaces that don't start with ``AWS/`` , such as custom namespaces. - ``Namespace IN ('AWS/EC2', 'AWS/ELB', 'AWS/S3')`` includes only the metrics in the EC2, ELB , and Amazon S3 namespaces. - ``Namespace = 'AWS/EC2' OR Namespace NOT LIKE 'AWS/%'`` includes only the EC2 namespace and your custom namespaces. - ``LogGroupName IN ('This-Log-Group', 'Other-Log-Group')`` includes only the log groups with names ``This-Log-Group`` and ``Other-Log-Group`` . - ``LogGroupName NOT IN ('Private-Log-Group', 'Private-Log-Group-2')`` includes all log groups except the log groups with names ``Private-Log-Group`` and ``Private-Log-Group-2`` . - ``LogGroupName LIKE 'aws/lambda/%' OR LogGroupName LIKE 'AWSLogs%'`` includes all log groups that have names that start with ``aws/lambda/`` or ``AWSLogs`` . .. epigraph:: If you are updating a link that uses filters, you can specify ``*`` as the only value for the ``filter`` parameter to delete the filter and share all log groups with the monitoring account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-oam-link-linkfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_oam import mixins as oam_mixins
                
                link_filter_property = oam_mixins.CfnLinkPropsMixin.LinkFilterProperty(
                    filter="filter"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65ee76ffbdfd07dd073a0916b959ce3e8155fc312aa1a3b188f5a4022c541abd)
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def filter(self) -> typing.Optional[builtins.str]:
            '''When used in ``MetricConfiguration`` this field specifies which metric namespaces are to be shared with the monitoring account.

            When used in ``LogGroupConfiguration`` this field specifies which log groups are to share their log events with the monitoring account. Use the term ``LogGroupName`` and one or more of the following operands.

            Use single quotation marks (') around log group names and metric namespaces.

            The matching of log group names and metric namespaces is case sensitive. Each filter has a limit of five conditional operands. Conditional operands are ``AND`` and ``OR`` .

            - ``=`` and ``!=``
            - ``AND``
            - ``OR``
            - ``LIKE`` and ``NOT LIKE`` . These can be used only as prefix searches. Include a ``%`` at the end of the string that you want to search for and include.
            - ``IN`` and ``NOT IN`` , using parentheses ``( )``

            Examples:

            - ``Namespace NOT LIKE 'AWS/%'`` includes only namespaces that don't start with ``AWS/`` , such as custom namespaces.
            - ``Namespace IN ('AWS/EC2', 'AWS/ELB', 'AWS/S3')`` includes only the metrics in the EC2, ELB , and Amazon S3 namespaces.
            - ``Namespace = 'AWS/EC2' OR Namespace NOT LIKE 'AWS/%'`` includes only the EC2 namespace and your custom namespaces.
            - ``LogGroupName IN ('This-Log-Group', 'Other-Log-Group')`` includes only the log groups with names ``This-Log-Group`` and ``Other-Log-Group`` .
            - ``LogGroupName NOT IN ('Private-Log-Group', 'Private-Log-Group-2')`` includes all log groups except the log groups with names ``Private-Log-Group`` and ``Private-Log-Group-2`` .
            - ``LogGroupName LIKE 'aws/lambda/%' OR LogGroupName LIKE 'AWSLogs%'`` includes all log groups that have names that start with ``aws/lambda/`` or ``AWSLogs`` .

            .. epigraph::

               If you are updating a link that uses filters, you can specify ``*`` as the only value for the ``filter`` parameter to delete the filter and share all log groups with the monitoring account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-oam-link-linkfilter.html#cfn-oam-link-linkfilter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinkFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_oam.mixins.CfnSinkMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "policy": "policy", "tags": "tags"},
)
class CfnSinkMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnSinkPropsMixin.

        :param name: A name for the sink.
        :param policy: The IAM policy that grants permissions to source accounts to link to this sink. The policy can grant permission in the following ways: - Include organization IDs or organization paths to permit all accounts in an organization - Include account IDs to permit the specified accounts
        :param tags: An array of key-value pairs to apply to the sink. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_oam import mixins as oam_mixins
            
            # policy: Any
            
            cfn_sink_mixin_props = oam_mixins.CfnSinkMixinProps(
                name="name",
                policy=policy,
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87cd1586fbbaea5f13323e654c11d6079f2a2a3731290aec1a82dee817c33f81)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the sink.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html#cfn-oam-sink-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The IAM policy that grants permissions to source accounts to link to this sink.

        The policy can grant permission in the following ways:

        - Include organization IDs or organization paths to permit all accounts in an organization
        - Include account IDs to permit the specified accounts

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html#cfn-oam-sink-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to the sink.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html#cfn-oam-sink-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSinkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSinkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_oam.mixins.CfnSinkPropsMixin",
):
    '''Creates or updates a *sink* in the current account, so that it can be used as a monitoring account in CloudWatch cross-account observability.

    A sink is a resource that represents an attachment point in a monitoring account, which source accounts can link to to be able to send observability data.

    After you create a sink, you must create a sink policy that allows source accounts to attach to it. For more information, see `PutSinkPolicy <https://docs.aws.amazon.com/OAM/latest/APIReference/API_PutSinkPolicy.html>`_ .

    An account can have one sink.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html
    :cloudformationResource: AWS::Oam::Sink
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_oam import mixins as oam_mixins
        
        # policy: Any
        
        cfn_sink_props_mixin = oam_mixins.CfnSinkPropsMixin(oam_mixins.CfnSinkMixinProps(
            name="name",
            policy=policy,
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSinkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Oam::Sink``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4bf5f67654df0d82cf1fbb65ae1bcebd366f99c3fa41e85cd925fbd2077e27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb9c660a2a3c90ff49d05f36a0f10dd95b95901a502e2c01155c5932211e995e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4173b786df7d024ff4ac20e58f339ed37c6c885cdc1ef6b0370bdad43cb69af)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSinkMixinProps:
        return typing.cast(CfnSinkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnLinkMixinProps",
    "CfnLinkPropsMixin",
    "CfnSinkMixinProps",
    "CfnSinkPropsMixin",
]

publication.publish()

def _typecheckingstub__ac9e8c49ef7c68fc6efa486a9151c996a7b12805ace870578b378c6d8cc034b8(
    *,
    label_template: typing.Optional[builtins.str] = None,
    link_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.LinkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    sink_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0bf9adb4646d6f4747c870b7124c994e336adbf789a7c1ea1984ef1669411ee(
    props: typing.Union[CfnLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d190ae3132e06978237f13e5e7af2ec2e0e1fda4dc723d173b002e0ad21b92ed(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e019ac486018802d6d7b88816c6095b4a8504275d21971da7ccda341cd4791c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa390669b3e626daa2ad1ad8b466da8157a62c9c72a5efb6f320051a109306cb(
    *,
    log_group_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.LinkFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metric_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.LinkFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ee76ffbdfd07dd073a0916b959ce3e8155fc312aa1a3b188f5a4022c541abd(
    *,
    filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87cd1586fbbaea5f13323e654c11d6079f2a2a3731290aec1a82dee817c33f81(
    *,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4bf5f67654df0d82cf1fbb65ae1bcebd366f99c3fa41e85cd925fbd2077e27(
    props: typing.Union[CfnSinkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9c660a2a3c90ff49d05f36a0f10dd95b95901a502e2c01155c5932211e995e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4173b786df7d024ff4ac20e58f339ed37c6c885cdc1ef6b0370bdad43cb69af(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
