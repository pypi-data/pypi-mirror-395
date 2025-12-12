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
    jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "custom_document_enrichment_configuration": "customDocumentEnrichmentConfiguration",
        "data_source_configuration": "dataSourceConfiguration",
        "description": "description",
        "index_id": "indexId",
        "language_code": "languageCode",
        "name": "name",
        "role_arn": "roleArn",
        "schedule": "schedule",
        "tags": "tags",
        "type": "type",
    },
)
class CfnDataSourceMixinProps:
    def __init__(
        self,
        *,
        custom_document_enrichment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.CustomDocumentEnrichmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        index_id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDataSourcePropsMixin.

        :param custom_document_enrichment_configuration: Configuration information for altering document metadata and content during the document ingestion process.
        :param data_source_configuration: Configuration information for an Amazon Kendra data source. The contents of the configuration depend on the type of data source. You can only specify one type of data source in the configuration. You can't specify the ``Configuration`` parameter when the ``Type`` parameter is set to ``CUSTOM`` . The ``Configuration`` parameter is required for all other data sources.
        :param description: A description for the data source connector.
        :param index_id: The identifier of the index you want to use with the data source connector.
        :param language_code: The code for a language. This shows a supported language for all documents in the data source. English is supported by default. For more information on supported languages, including their codes, see `Adding documents in languages other than English <https://docs.aws.amazon.com/kendra/latest/dg/in-adding-languages.html>`_ .
        :param name: The name of the data source.
        :param role_arn: The Amazon Resource Name (ARN) of a role with permission to access the data source. You can't specify the ``RoleArn`` parameter when the ``Type`` parameter is set to ``CUSTOM`` . The ``RoleArn`` parameter is required for all other data sources.
        :param schedule: Sets the frequency that Amazon Kendra checks the documents in your data source and updates the index. If you don't set a schedule, Amazon Kendra doesn't periodically update the index.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: The type of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
            
            cfn_data_source_mixin_props = kendra_mixins.CfnDataSourceMixinProps(
                custom_document_enrichment_configuration=kendra_mixins.CfnDataSourcePropsMixin.CustomDocumentEnrichmentConfigurationProperty(
                    inline_configurations=[kendra_mixins.CfnDataSourcePropsMixin.InlineCustomDocumentEnrichmentConfigurationProperty(
                        condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            operator="operator"
                        ),
                        document_content_deletion=False,
                        target=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                            target_document_attribute_key="targetDocumentAttributeKey",
                            target_document_attribute_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            target_document_attribute_value_deletion=False
                        )
                    )],
                    post_extraction_hook_configuration=kendra_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                        invocation_condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            operator="operator"
                        ),
                        lambda_arn="lambdaArn",
                        s3_bucket="s3Bucket"
                    ),
                    pre_extraction_hook_configuration=kendra_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                        invocation_condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            operator="operator"
                        ),
                        lambda_arn="lambdaArn",
                        s3_bucket="s3Bucket"
                    ),
                    role_arn="roleArn"
                ),
                data_source_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceConfigurationProperty(
                    confluence_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceConfigurationProperty(
                        attachment_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty(
                            attachment_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            crawl_attachments=False
                        ),
                        blog_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty(
                            blog_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        exclusion_patterns=["exclusionPatterns"],
                        inclusion_patterns=["inclusionPatterns"],
                        page_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty(
                            page_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        secret_arn="secretArn",
                        server_url="serverUrl",
                        space_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty(
                            crawl_archived_spaces=False,
                            crawl_personal_spaces=False,
                            exclude_spaces=["excludeSpaces"],
                            include_spaces=["includeSpaces"],
                            space_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        version="version",
                        vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    database_configuration=kendra_mixins.CfnDataSourcePropsMixin.DatabaseConfigurationProperty(
                        acl_configuration=kendra_mixins.CfnDataSourcePropsMixin.AclConfigurationProperty(
                            allowed_groups_column_name="allowedGroupsColumnName"
                        ),
                        column_configuration=kendra_mixins.CfnDataSourcePropsMixin.ColumnConfigurationProperty(
                            change_detecting_columns=["changeDetectingColumns"],
                            document_data_column_name="documentDataColumnName",
                            document_id_column_name="documentIdColumnName",
                            document_title_column_name="documentTitleColumnName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        connection_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConnectionConfigurationProperty(
                            database_host="databaseHost",
                            database_name="databaseName",
                            database_port=123,
                            secret_arn="secretArn",
                            table_name="tableName"
                        ),
                        database_engine_type="databaseEngineType",
                        sql_configuration=kendra_mixins.CfnDataSourcePropsMixin.SqlConfigurationProperty(
                            query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                        ),
                        vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    google_drive_configuration=kendra_mixins.CfnDataSourcePropsMixin.GoogleDriveConfigurationProperty(
                        exclude_mime_types=["excludeMimeTypes"],
                        exclude_shared_drives=["excludeSharedDrives"],
                        exclude_user_accounts=["excludeUserAccounts"],
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        secret_arn="secretArn"
                    ),
                    one_drive_configuration=kendra_mixins.CfnDataSourcePropsMixin.OneDriveConfigurationProperty(
                        disable_local_groups=False,
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        one_drive_users=kendra_mixins.CfnDataSourcePropsMixin.OneDriveUsersProperty(
                            one_drive_user_list=["oneDriveUserList"],
                            one_drive_user_s3_path=kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                                bucket="bucket",
                                key="key"
                            )
                        ),
                        secret_arn="secretArn",
                        tenant_domain="tenantDomain"
                    ),
                    s3_configuration=kendra_mixins.CfnDataSourcePropsMixin.S3DataSourceConfigurationProperty(
                        access_control_list_configuration=kendra_mixins.CfnDataSourcePropsMixin.AccessControlListConfigurationProperty(
                            key_path="keyPath"
                        ),
                        bucket_name="bucketName",
                        documents_metadata_configuration=kendra_mixins.CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty(
                            s3_prefix="s3Prefix"
                        ),
                        exclusion_patterns=["exclusionPatterns"],
                        inclusion_patterns=["inclusionPatterns"],
                        inclusion_prefixes=["inclusionPrefixes"]
                    ),
                    salesforce_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceConfigurationProperty(
                        chatter_feed_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            include_filter_types=["includeFilterTypes"]
                        ),
                        crawl_attachments=False,
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"],
                        knowledge_article_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty(
                            custom_knowledge_article_type_configurations=[kendra_mixins.CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                                document_data_field_name="documentDataFieldName",
                                document_title_field_name="documentTitleFieldName",
                                field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                    data_source_field_name="dataSourceFieldName",
                                    date_field_format="dateFieldFormat",
                                    index_field_name="indexFieldName"
                                )],
                                name="name"
                            )],
                            included_states=["includedStates"],
                            standard_knowledge_article_type_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                                document_data_field_name="documentDataFieldName",
                                document_title_field_name="documentTitleFieldName",
                                field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                    data_source_field_name="dataSourceFieldName",
                                    date_field_format="dateFieldFormat",
                                    index_field_name="indexFieldName"
                                )]
                            )
                        ),
                        secret_arn="secretArn",
                        server_url="serverUrl",
                        standard_object_attachment_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty(
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        standard_object_configurations=[kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            name="name"
                        )]
                    ),
                    service_now_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowConfigurationProperty(
                        authentication_type="authenticationType",
                        host_url="hostUrl",
                        knowledge_article_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty(
                            crawl_attachments=False,
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            filter_query="filterQuery",
                            include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                        ),
                        secret_arn="secretArn",
                        service_catalog_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty(
                            crawl_attachments=False,
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                        ),
                        service_now_build_version="serviceNowBuildVersion"
                    ),
                    share_point_configuration=kendra_mixins.CfnDataSourcePropsMixin.SharePointConfigurationProperty(
                        crawl_attachments=False,
                        disable_local_groups=False,
                        document_title_field_name="documentTitleFieldName",
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        secret_arn="secretArn",
                        share_point_version="sharePointVersion",
                        ssl_certificate_s3_path=kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                            bucket="bucket",
                            key="key"
                        ),
                        urls=["urls"],
                        use_change_log=False,
                        vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    template_configuration=kendra_mixins.CfnDataSourcePropsMixin.TemplateConfigurationProperty(
                        template="template"
                    ),
                    web_crawler_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerConfigurationProperty(
                        authentication_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty(
                            basic_authentication=[kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty(
                                credentials="credentials",
                                host="host",
                                port=123
                            )]
                        ),
                        crawl_depth=123,
                        max_content_size_per_page_in_mega_bytes=123,
                        max_links_per_page=123,
                        max_urls_per_minute_crawl_rate=123,
                        proxy_configuration=kendra_mixins.CfnDataSourcePropsMixin.ProxyConfigurationProperty(
                            credentials="credentials",
                            host="host",
                            port=123
                        ),
                        url_exclusion_patterns=["urlExclusionPatterns"],
                        url_inclusion_patterns=["urlInclusionPatterns"],
                        urls=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerUrlsProperty(
                            seed_url_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty(
                                seed_urls=["seedUrls"],
                                web_crawler_mode="webCrawlerMode"
                            ),
                            site_maps_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty(
                                site_maps=["siteMaps"]
                            )
                        )
                    ),
                    work_docs_configuration=kendra_mixins.CfnDataSourcePropsMixin.WorkDocsConfigurationProperty(
                        crawl_comments=False,
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        organization_id="organizationId",
                        use_change_log=False
                    )
                ),
                description="description",
                index_id="indexId",
                language_code="languageCode",
                name="name",
                role_arn="roleArn",
                schedule="schedule",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26de3a0a87130f6fb90b3250b97fce1493ec3da757f84e0ecd2a127523c428df)
            check_type(argname="argument custom_document_enrichment_configuration", value=custom_document_enrichment_configuration, expected_type=type_hints["custom_document_enrichment_configuration"])
            check_type(argname="argument data_source_configuration", value=data_source_configuration, expected_type=type_hints["data_source_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_document_enrichment_configuration is not None:
            self._values["custom_document_enrichment_configuration"] = custom_document_enrichment_configuration
        if data_source_configuration is not None:
            self._values["data_source_configuration"] = data_source_configuration
        if description is not None:
            self._values["description"] = description
        if index_id is not None:
            self._values["index_id"] = index_id
        if language_code is not None:
            self._values["language_code"] = language_code
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if schedule is not None:
            self._values["schedule"] = schedule
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def custom_document_enrichment_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.CustomDocumentEnrichmentConfigurationProperty"]]:
        '''Configuration information for altering document metadata and content during the document ingestion process.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration
        '''
        result = self._values.get("custom_document_enrichment_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.CustomDocumentEnrichmentConfigurationProperty"]], result)

    @builtins.property
    def data_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceConfigurationProperty"]]:
        '''Configuration information for an Amazon Kendra data source.

        The contents of the configuration depend on the type of data source. You can only specify one type of data source in the configuration.

        You can't specify the ``Configuration`` parameter when the ``Type`` parameter is set to ``CUSTOM`` .

        The ``Configuration`` parameter is required for all other data sources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-datasourceconfiguration
        '''
        result = self._values.get("data_source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the data source connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the index you want to use with the data source connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-indexid
        '''
        result = self._values.get("index_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The code for a language.

        This shows a supported language for all documents in the data source. English is supported by default. For more information on supported languages, including their codes, see `Adding documents in languages other than English <https://docs.aws.amazon.com/kendra/latest/dg/in-adding-languages.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-languagecode
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a role with permission to access the data source.

        You can't specify the ``RoleArn`` parameter when the ``Type`` parameter is set to ``CUSTOM`` .

        The ``RoleArn`` parameter is required for all other data sources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Sets the frequency that Amazon Kendra checks the documents in your data source and updates the index.

        If you don't set a schedule, Amazon Kendra doesn't periodically update the index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin",
):
    '''Creates a data source connector that you want to use with an Amazon Kendra index.

    You specify a name, data source connector type and description for your data source. You also specify configuration information for the data source connector.
    .. epigraph::

       ``CreateDataSource`` does *not* support connectors which `require a ``TemplateConfiguration`` object <https://docs.aws.amazon.com/kendra/latest/dg/ds-schemas.html>`_ for connecting to Amazon Kendra .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html
    :cloudformationResource: AWS::Kendra::DataSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
        
        cfn_data_source_props_mixin = kendra_mixins.CfnDataSourcePropsMixin(kendra_mixins.CfnDataSourceMixinProps(
            custom_document_enrichment_configuration=kendra_mixins.CfnDataSourcePropsMixin.CustomDocumentEnrichmentConfigurationProperty(
                inline_configurations=[kendra_mixins.CfnDataSourcePropsMixin.InlineCustomDocumentEnrichmentConfigurationProperty(
                    condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        ),
                        operator="operator"
                    ),
                    document_content_deletion=False,
                    target=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                        target_document_attribute_key="targetDocumentAttributeKey",
                        target_document_attribute_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        ),
                        target_document_attribute_value_deletion=False
                    )
                )],
                post_extraction_hook_configuration=kendra_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                    invocation_condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        ),
                        operator="operator"
                    ),
                    lambda_arn="lambdaArn",
                    s3_bucket="s3Bucket"
                ),
                pre_extraction_hook_configuration=kendra_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                    invocation_condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        ),
                        operator="operator"
                    ),
                    lambda_arn="lambdaArn",
                    s3_bucket="s3Bucket"
                ),
                role_arn="roleArn"
            ),
            data_source_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceConfigurationProperty(
                confluence_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceConfigurationProperty(
                    attachment_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty(
                        attachment_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        crawl_attachments=False
                    ),
                    blog_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty(
                        blog_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    exclusion_patterns=["exclusionPatterns"],
                    inclusion_patterns=["inclusionPatterns"],
                    page_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty(
                        page_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    secret_arn="secretArn",
                    server_url="serverUrl",
                    space_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty(
                        crawl_archived_spaces=False,
                        crawl_personal_spaces=False,
                        exclude_spaces=["excludeSpaces"],
                        include_spaces=["includeSpaces"],
                        space_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    version="version",
                    vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                ),
                database_configuration=kendra_mixins.CfnDataSourcePropsMixin.DatabaseConfigurationProperty(
                    acl_configuration=kendra_mixins.CfnDataSourcePropsMixin.AclConfigurationProperty(
                        allowed_groups_column_name="allowedGroupsColumnName"
                    ),
                    column_configuration=kendra_mixins.CfnDataSourcePropsMixin.ColumnConfigurationProperty(
                        change_detecting_columns=["changeDetectingColumns"],
                        document_data_column_name="documentDataColumnName",
                        document_id_column_name="documentIdColumnName",
                        document_title_column_name="documentTitleColumnName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    connection_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConnectionConfigurationProperty(
                        database_host="databaseHost",
                        database_name="databaseName",
                        database_port=123,
                        secret_arn="secretArn",
                        table_name="tableName"
                    ),
                    database_engine_type="databaseEngineType",
                    sql_configuration=kendra_mixins.CfnDataSourcePropsMixin.SqlConfigurationProperty(
                        query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                    ),
                    vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                ),
                google_drive_configuration=kendra_mixins.CfnDataSourcePropsMixin.GoogleDriveConfigurationProperty(
                    exclude_mime_types=["excludeMimeTypes"],
                    exclude_shared_drives=["excludeSharedDrives"],
                    exclude_user_accounts=["excludeUserAccounts"],
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    secret_arn="secretArn"
                ),
                one_drive_configuration=kendra_mixins.CfnDataSourcePropsMixin.OneDriveConfigurationProperty(
                    disable_local_groups=False,
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    one_drive_users=kendra_mixins.CfnDataSourcePropsMixin.OneDriveUsersProperty(
                        one_drive_user_list=["oneDriveUserList"],
                        one_drive_user_s3_path=kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    secret_arn="secretArn",
                    tenant_domain="tenantDomain"
                ),
                s3_configuration=kendra_mixins.CfnDataSourcePropsMixin.S3DataSourceConfigurationProperty(
                    access_control_list_configuration=kendra_mixins.CfnDataSourcePropsMixin.AccessControlListConfigurationProperty(
                        key_path="keyPath"
                    ),
                    bucket_name="bucketName",
                    documents_metadata_configuration=kendra_mixins.CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty(
                        s3_prefix="s3Prefix"
                    ),
                    exclusion_patterns=["exclusionPatterns"],
                    inclusion_patterns=["inclusionPatterns"],
                    inclusion_prefixes=["inclusionPrefixes"]
                ),
                salesforce_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceConfigurationProperty(
                    chatter_feed_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        include_filter_types=["includeFilterTypes"]
                    ),
                    crawl_attachments=False,
                    exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                    include_attachment_file_patterns=["includeAttachmentFilePatterns"],
                    knowledge_article_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty(
                        custom_knowledge_article_type_configurations=[kendra_mixins.CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            name="name"
                        )],
                        included_states=["includedStates"],
                        standard_knowledge_article_type_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        )
                    ),
                    secret_arn="secretArn",
                    server_url="serverUrl",
                    standard_object_attachment_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty(
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    standard_object_configurations=[kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        name="name"
                    )]
                ),
                service_now_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowConfigurationProperty(
                    authentication_type="authenticationType",
                    host_url="hostUrl",
                    knowledge_article_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty(
                        crawl_attachments=False,
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        filter_query="filterQuery",
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                    ),
                    secret_arn="secretArn",
                    service_catalog_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty(
                        crawl_attachments=False,
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                    ),
                    service_now_build_version="serviceNowBuildVersion"
                ),
                share_point_configuration=kendra_mixins.CfnDataSourcePropsMixin.SharePointConfigurationProperty(
                    crawl_attachments=False,
                    disable_local_groups=False,
                    document_title_field_name="documentTitleFieldName",
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    secret_arn="secretArn",
                    share_point_version="sharePointVersion",
                    ssl_certificate_s3_path=kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                        bucket="bucket",
                        key="key"
                    ),
                    urls=["urls"],
                    use_change_log=False,
                    vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                ),
                template_configuration=kendra_mixins.CfnDataSourcePropsMixin.TemplateConfigurationProperty(
                    template="template"
                ),
                web_crawler_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerConfigurationProperty(
                    authentication_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty(
                        basic_authentication=[kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty(
                            credentials="credentials",
                            host="host",
                            port=123
                        )]
                    ),
                    crawl_depth=123,
                    max_content_size_per_page_in_mega_bytes=123,
                    max_links_per_page=123,
                    max_urls_per_minute_crawl_rate=123,
                    proxy_configuration=kendra_mixins.CfnDataSourcePropsMixin.ProxyConfigurationProperty(
                        credentials="credentials",
                        host="host",
                        port=123
                    ),
                    url_exclusion_patterns=["urlExclusionPatterns"],
                    url_inclusion_patterns=["urlInclusionPatterns"],
                    urls=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerUrlsProperty(
                        seed_url_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty(
                            seed_urls=["seedUrls"],
                            web_crawler_mode="webCrawlerMode"
                        ),
                        site_maps_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty(
                            site_maps=["siteMaps"]
                        )
                    )
                ),
                work_docs_configuration=kendra_mixins.CfnDataSourcePropsMixin.WorkDocsConfigurationProperty(
                    crawl_comments=False,
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    organization_id="organizationId",
                    use_change_log=False
                )
            ),
            description="description",
            index_id="indexId",
            language_code="languageCode",
            name="name",
            role_arn="roleArn",
            schedule="schedule",
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
        props: typing.Union[CfnDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Kendra::DataSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76519d15071f2a3daad21e8f32dd48e667d3d824fa61000ebad87c9ff1ff7203)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48b921c40ab0908728e1425eeaa7ef95e97ad917d08bbcc4c8d13abe78dfe3b5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f715293058639fe474bfa70b8f2edfeec93b2a401cb92af5c023da92b6035c8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataSourceMixinProps:
        return typing.cast(CfnDataSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.AccessControlListConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"key_path": "keyPath"},
    )
    class AccessControlListConfigurationProperty:
        def __init__(self, *, key_path: typing.Optional[builtins.str] = None) -> None:
            '''Specifies access control list files for the documents in a data source.

            :param key_path: Path to the AWS S3 bucket that contains the access control list files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-accesscontrollistconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                access_control_list_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.AccessControlListConfigurationProperty(
                    key_path="keyPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d5056664f8f743bb93c42ddddd211bdd2f3508c2086452e9603f51c458db4ee)
                check_type(argname="argument key_path", value=key_path, expected_type=type_hints["key_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_path is not None:
                self._values["key_path"] = key_path

        @builtins.property
        def key_path(self) -> typing.Optional[builtins.str]:
            '''Path to the AWS S3 bucket that contains the access control list files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-accesscontrollistconfiguration.html#cfn-kendra-datasource-accesscontrollistconfiguration-keypath
            '''
            result = self._values.get("key_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessControlListConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.AclConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"allowed_groups_column_name": "allowedGroupsColumnName"},
    )
    class AclConfigurationProperty:
        def __init__(
            self,
            *,
            allowed_groups_column_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information about the column that should be used for filtering the query response by groups.

            :param allowed_groups_column_name: A list of groups, separated by semi-colons, that filters a query response based on user context. The document is only returned to users that are in one of the groups specified in the ``UserContext`` field of the `Query <https://docs.aws.amazon.com/kendra/latest/dg/API_Query.html>`_ operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-aclconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                acl_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.AclConfigurationProperty(
                    allowed_groups_column_name="allowedGroupsColumnName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf39320c15ecf8d7d6d42b80214ffc9cf0d14b3c2e36daf516225771c8e023db)
                check_type(argname="argument allowed_groups_column_name", value=allowed_groups_column_name, expected_type=type_hints["allowed_groups_column_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_groups_column_name is not None:
                self._values["allowed_groups_column_name"] = allowed_groups_column_name

        @builtins.property
        def allowed_groups_column_name(self) -> typing.Optional[builtins.str]:
            '''A list of groups, separated by semi-colons, that filters a query response based on user context.

            The document is only returned to users that are in one of the groups specified in the ``UserContext`` field of the `Query <https://docs.aws.amazon.com/kendra/latest/dg/API_Query.html>`_ operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-aclconfiguration.html#cfn-kendra-datasource-aclconfiguration-allowedgroupscolumnname
            '''
            result = self._values.get("allowed_groups_column_name")
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
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ColumnConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "change_detecting_columns": "changeDetectingColumns",
            "document_data_column_name": "documentDataColumnName",
            "document_id_column_name": "documentIdColumnName",
            "document_title_column_name": "documentTitleColumnName",
            "field_mappings": "fieldMappings",
        },
    )
    class ColumnConfigurationProperty:
        def __init__(
            self,
            *,
            change_detecting_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
            document_data_column_name: typing.Optional[builtins.str] = None,
            document_id_column_name: typing.Optional[builtins.str] = None,
            document_title_column_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides information about how Amazon Kendra should use the columns of a database in an index.

            :param change_detecting_columns: One to five columns that indicate when a document in the database has changed.
            :param document_data_column_name: The column that contains the contents of the document.
            :param document_id_column_name: The column that provides the document's identifier.
            :param document_title_column_name: The column that contains the title of the document.
            :param field_mappings: An array of objects that map database column names to the corresponding fields in an index. You must first create the fields in the index using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                column_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ColumnConfigurationProperty(
                    change_detecting_columns=["changeDetectingColumns"],
                    document_data_column_name="documentDataColumnName",
                    document_id_column_name="documentIdColumnName",
                    document_title_column_name="documentTitleColumnName",
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c10955cf9c6deb5467398b87e94c56a7b51ba03dc2d8f8ba5a5de6a284d23e53)
                check_type(argname="argument change_detecting_columns", value=change_detecting_columns, expected_type=type_hints["change_detecting_columns"])
                check_type(argname="argument document_data_column_name", value=document_data_column_name, expected_type=type_hints["document_data_column_name"])
                check_type(argname="argument document_id_column_name", value=document_id_column_name, expected_type=type_hints["document_id_column_name"])
                check_type(argname="argument document_title_column_name", value=document_title_column_name, expected_type=type_hints["document_title_column_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if change_detecting_columns is not None:
                self._values["change_detecting_columns"] = change_detecting_columns
            if document_data_column_name is not None:
                self._values["document_data_column_name"] = document_data_column_name
            if document_id_column_name is not None:
                self._values["document_id_column_name"] = document_id_column_name
            if document_title_column_name is not None:
                self._values["document_title_column_name"] = document_title_column_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings

        @builtins.property
        def change_detecting_columns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''One to five columns that indicate when a document in the database has changed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-changedetectingcolumns
            '''
            result = self._values.get("change_detecting_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def document_data_column_name(self) -> typing.Optional[builtins.str]:
            '''The column that contains the contents of the document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-documentdatacolumnname
            '''
            result = self._values.get("document_data_column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_id_column_name(self) -> typing.Optional[builtins.str]:
            '''The column that provides the document's identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-documentidcolumnname
            '''
            result = self._values.get("document_id_column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_title_column_name(self) -> typing.Optional[builtins.str]:
            '''The column that contains the title of the document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-documenttitlecolumnname
            '''
            result = self._values.get("document_title_column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''An array of objects that map database column names to the corresponding fields in an index.

            You must first create the fields in the index using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_field_mappings": "attachmentFieldMappings",
            "crawl_attachments": "crawlAttachments",
        },
    )
    class ConfluenceAttachmentConfigurationProperty:
        def __init__(
            self,
            *,
            attachment_field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Configuration of attachment settings for the Confluence data source.

            Attachment settings are optional, if you don't specify settings attachments, Amazon Kendra won't index them.

            :param attachment_field_mappings: Maps attributes or field names of Confluence attachments to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata. If you specify the ``AttachentFieldMappings`` parameter, you must specify at least one field mapping.
            :param crawl_attachments: ``TRUE`` to index attachments of pages and blogs in Confluence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                confluence_attachment_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty(
                    attachment_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    crawl_attachments=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4a45c837ec8158eb6e8bb092541bfbfd1f6e7ba43440626cc89a6830130887a)
                check_type(argname="argument attachment_field_mappings", value=attachment_field_mappings, expected_type=type_hints["attachment_field_mappings"])
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_field_mappings is not None:
                self._values["attachment_field_mappings"] = attachment_field_mappings
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments

        @builtins.property
        def attachment_field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty"]]]]:
            '''Maps attributes or field names of Confluence attachments to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            If you specify the ``AttachentFieldMappings`` parameter, you must specify at least one field mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmentconfiguration.html#cfn-kendra-datasource-confluenceattachmentconfiguration-attachmentfieldmappings
            '''
            result = self._values.get("attachment_field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to index attachments of pages and blogs in Confluence.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmentconfiguration.html#cfn-kendra-datasource-confluenceattachmentconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceAttachmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "date_field_format": "dateFieldFormat",
            "index_field_name": "indexFieldName",
        },
    )
    class ConfluenceAttachmentToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: typing.Optional[builtins.str] = None,
            date_field_format: typing.Optional[builtins.str] = None,
            index_field_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps attributes or field names of Confluence attachments to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confuence data source field names must exist in your Confluence custom metadata.

            :param data_source_field_name: The name of the field in the data source. You must first create the index field using the ``UpdateIndex`` API.
            :param date_field_format: The format for date fields in the data source. If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.
            :param index_field_name: The name of the index field to map to the Confluence data source field. The index field type must match the Confluence field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmenttoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                confluence_attachment_to_index_field_mapping_property = kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    date_field_format="dateFieldFormat",
                    index_field_name="indexFieldName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__205a46c026766efdba5c77b63c822ac754ebeeab704d997a918464911e14dfd4)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source_field_name is not None:
                self._values["data_source_field_name"] = data_source_field_name
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format
            if index_field_name is not None:
                self._values["index_field_name"] = index_field_name

        @builtins.property
        def data_source_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the data source.

            You must first create the index field using the ``UpdateIndex`` API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmenttoindexfieldmapping.html#cfn-kendra-datasource-confluenceattachmenttoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The format for date fields in the data source.

            If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmenttoindexfieldmapping.html#cfn-kendra-datasource-confluenceattachmenttoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the index field to map to the Confluence data source field.

            The index field type must match the Confluence field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmenttoindexfieldmapping.html#cfn-kendra-datasource-confluenceattachmenttoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceAttachmentToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"blog_field_mappings": "blogFieldMappings"},
    )
    class ConfluenceBlogConfigurationProperty:
        def __init__(
            self,
            *,
            blog_field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration of blog settings for the Confluence data source.

            Blogs are always indexed unless filtered from the index by the ``ExclusionPatterns`` or ``InclusionPatterns`` fields in the ``ConfluenceConfiguration`` object.

            :param blog_field_mappings: Maps attributes or field names of Confluence blogs to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata. If you specify the ``BlogFieldMappings`` parameter, you must specify at least one field mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                confluence_blog_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty(
                    blog_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__33e41ba4ad67f9b2832d428a7603871262be71d6495a20139d4b461e28f36e1d)
                check_type(argname="argument blog_field_mappings", value=blog_field_mappings, expected_type=type_hints["blog_field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if blog_field_mappings is not None:
                self._values["blog_field_mappings"] = blog_field_mappings

        @builtins.property
        def blog_field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty"]]]]:
            '''Maps attributes or field names of Confluence blogs to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            If you specify the ``BlogFieldMappings`` parameter, you must specify at least one field mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogconfiguration.html#cfn-kendra-datasource-confluenceblogconfiguration-blogfieldmappings
            '''
            result = self._values.get("blog_field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceBlogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "date_field_format": "dateFieldFormat",
            "index_field_name": "indexFieldName",
        },
    )
    class ConfluenceBlogToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: typing.Optional[builtins.str] = None,
            date_field_format: typing.Optional[builtins.str] = None,
            index_field_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps attributes or field names of Confluence blog to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            :param data_source_field_name: The name of the field in the data source.
            :param date_field_format: The format for date fields in the data source. If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.
            :param index_field_name: The name of the index field to map to the Confluence data source field. The index field type must match the Confluence field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogtoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                confluence_blog_to_index_field_mapping_property = kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    date_field_format="dateFieldFormat",
                    index_field_name="indexFieldName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__898ce38c507a69a70476b7a07527180d02e8c7c1a25afd91e77bfb31f8c5c514)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source_field_name is not None:
                self._values["data_source_field_name"] = data_source_field_name
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format
            if index_field_name is not None:
                self._values["index_field_name"] = index_field_name

        @builtins.property
        def data_source_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogtoindexfieldmapping.html#cfn-kendra-datasource-confluenceblogtoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The format for date fields in the data source.

            If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogtoindexfieldmapping.html#cfn-kendra-datasource-confluenceblogtoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the index field to map to the Confluence data source field.

            The index field type must match the Confluence field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogtoindexfieldmapping.html#cfn-kendra-datasource-confluenceblogtoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceBlogToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConfluenceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_configuration": "attachmentConfiguration",
            "blog_configuration": "blogConfiguration",
            "exclusion_patterns": "exclusionPatterns",
            "inclusion_patterns": "inclusionPatterns",
            "page_configuration": "pageConfiguration",
            "secret_arn": "secretArn",
            "server_url": "serverUrl",
            "space_configuration": "spaceConfiguration",
            "version": "version",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class ConfluenceConfigurationProperty:
        def __init__(
            self,
            *,
            attachment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            blog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            page_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            server_url: typing.Optional[builtins.str] = None,
            space_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            version: typing.Optional[builtins.str] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information to connect to Confluence as your data source.

            :param attachment_configuration: Configuration information for indexing attachments to Confluence blogs and pages.
            :param blog_configuration: Configuration information for indexing Confluence blogs.
            :param exclusion_patterns: A list of regular expression patterns to exclude certain blog posts, pages, spaces, or attachments in your Confluence. Content that matches the patterns are excluded from the index. Content that doesn't match the patterns is included in the index. If content matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the content isn't included in the index.
            :param inclusion_patterns: A list of regular expression patterns to include certain blog posts, pages, spaces, or attachments in your Confluence. Content that matches the patterns are included in the index. Content that doesn't match the patterns is excluded from the index. If content matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the content isn't included in the index.
            :param page_configuration: Configuration information for indexing Confluence pages.
            :param secret_arn: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password required to connect to the Confluence instance. If you use Confluence Cloud, you use a generated API token as the password. You can also provide authentication credentials in the form of a personal access token. For more information, see `Using a Confluence data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-confluence.html>`_ .
            :param server_url: The URL of your Confluence instance. Use the full URL of the server. For example, *https://server.example.com:port/* . You can also use an IP address, for example, *https://192.168.1.113/* .
            :param space_configuration: Configuration information for indexing Confluence spaces.
            :param version: The version or the type of Confluence installation to connect to.
            :param vpc_configuration: Configuration information for an Amazon Virtual Private Cloud to connect to your Confluence. For more information, see `Configuring a VPC <https://docs.aws.amazon.com/kendra/latest/dg/vpc-configuration.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                confluence_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ConfluenceConfigurationProperty(
                    attachment_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty(
                        attachment_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        crawl_attachments=False
                    ),
                    blog_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty(
                        blog_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    exclusion_patterns=["exclusionPatterns"],
                    inclusion_patterns=["inclusionPatterns"],
                    page_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty(
                        page_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    secret_arn="secretArn",
                    server_url="serverUrl",
                    space_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty(
                        crawl_archived_spaces=False,
                        crawl_personal_spaces=False,
                        exclude_spaces=["excludeSpaces"],
                        include_spaces=["includeSpaces"],
                        space_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    version="version",
                    vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00a3aaa8301110ff8d8c17070190aa6b4540fec9a90491efe2682fc7cb0602b8)
                check_type(argname="argument attachment_configuration", value=attachment_configuration, expected_type=type_hints["attachment_configuration"])
                check_type(argname="argument blog_configuration", value=blog_configuration, expected_type=type_hints["blog_configuration"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument page_configuration", value=page_configuration, expected_type=type_hints["page_configuration"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument server_url", value=server_url, expected_type=type_hints["server_url"])
                check_type(argname="argument space_configuration", value=space_configuration, expected_type=type_hints["space_configuration"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_configuration is not None:
                self._values["attachment_configuration"] = attachment_configuration
            if blog_configuration is not None:
                self._values["blog_configuration"] = blog_configuration
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if page_configuration is not None:
                self._values["page_configuration"] = page_configuration
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if server_url is not None:
                self._values["server_url"] = server_url
            if space_configuration is not None:
                self._values["space_configuration"] = space_configuration
            if version is not None:
                self._values["version"] = version
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def attachment_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty"]]:
            '''Configuration information for indexing attachments to Confluence blogs and pages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-attachmentconfiguration
            '''
            result = self._values.get("attachment_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty"]], result)

        @builtins.property
        def blog_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty"]]:
            '''Configuration information for indexing Confluence blogs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-blogconfiguration
            '''
            result = self._values.get("blog_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty"]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain blog posts, pages, spaces, or attachments in your Confluence.

            Content that matches the patterns are excluded from the index. Content that doesn't match the patterns is included in the index. If content matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the content isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain blog posts, pages, spaces, or attachments in your Confluence.

            Content that matches the patterns are included in the index. Content that doesn't match the patterns is excluded from the index. If content matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the content isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def page_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty"]]:
            '''Configuration information for indexing Confluence pages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-pageconfiguration
            '''
            result = self._values.get("page_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty"]], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password required to connect to the Confluence instance.

            If you use Confluence Cloud, you use a generated API token as the password.

            You can also provide authentication credentials in the form of a personal access token. For more information, see `Using a Confluence data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-confluence.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_url(self) -> typing.Optional[builtins.str]:
            '''The URL of your Confluence instance.

            Use the full URL of the server. For example, *https://server.example.com:port/* . You can also use an IP address, for example, *https://192.168.1.113/* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-serverurl
            '''
            result = self._values.get("server_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def space_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty"]]:
            '''Configuration information for indexing Confluence spaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-spaceconfiguration
            '''
            result = self._values.get("space_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty"]], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version or the type of Confluence installation to connect to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty"]]:
            '''Configuration information for an Amazon Virtual Private Cloud to connect to your Confluence.

            For more information, see `Configuring a VPC <https://docs.aws.amazon.com/kendra/latest/dg/vpc-configuration.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"page_field_mappings": "pageFieldMappings"},
    )
    class ConfluencePageConfigurationProperty:
        def __init__(
            self,
            *,
            page_field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration of the page settings for the Confluence data source.

            :param page_field_mappings: Maps attributes or field names of Confluence pages to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata. If you specify the ``PageFieldMappings`` parameter, you must specify at least one field mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                confluence_page_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty(
                    page_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74f6a315c1823c58589682cdd849928d09084eee80c2934290513e5e5207d5aa)
                check_type(argname="argument page_field_mappings", value=page_field_mappings, expected_type=type_hints["page_field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if page_field_mappings is not None:
                self._values["page_field_mappings"] = page_field_mappings

        @builtins.property
        def page_field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty"]]]]:
            '''Maps attributes or field names of Confluence pages to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            If you specify the ``PageFieldMappings`` parameter, you must specify at least one field mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepageconfiguration.html#cfn-kendra-datasource-confluencepageconfiguration-pagefieldmappings
            '''
            result = self._values.get("page_field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluencePageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "date_field_format": "dateFieldFormat",
            "index_field_name": "indexFieldName",
        },
    )
    class ConfluencePageToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: typing.Optional[builtins.str] = None,
            date_field_format: typing.Optional[builtins.str] = None,
            index_field_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps attributes or field names of Confluence pages to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            :param data_source_field_name: The name of the field in the data source.
            :param date_field_format: The format for date fields in the data source. If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.
            :param index_field_name: The name of the index field to map to the Confluence data source field. The index field type must match the Confluence field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepagetoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                confluence_page_to_index_field_mapping_property = kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    date_field_format="dateFieldFormat",
                    index_field_name="indexFieldName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96d5c5c74279052ceaec3377ef35c388c3f832221c7b758587e4d18ada2a4be5)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source_field_name is not None:
                self._values["data_source_field_name"] = data_source_field_name
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format
            if index_field_name is not None:
                self._values["index_field_name"] = index_field_name

        @builtins.property
        def data_source_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepagetoindexfieldmapping.html#cfn-kendra-datasource-confluencepagetoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The format for date fields in the data source.

            If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepagetoindexfieldmapping.html#cfn-kendra-datasource-confluencepagetoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the index field to map to the Confluence data source field.

            The index field type must match the Confluence field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepagetoindexfieldmapping.html#cfn-kendra-datasource-confluencepagetoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluencePageToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crawl_archived_spaces": "crawlArchivedSpaces",
            "crawl_personal_spaces": "crawlPersonalSpaces",
            "exclude_spaces": "excludeSpaces",
            "include_spaces": "includeSpaces",
            "space_field_mappings": "spaceFieldMappings",
        },
    )
    class ConfluenceSpaceConfigurationProperty:
        def __init__(
            self,
            *,
            crawl_archived_spaces: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            crawl_personal_spaces: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclude_spaces: typing.Optional[typing.Sequence[builtins.str]] = None,
            include_spaces: typing.Optional[typing.Sequence[builtins.str]] = None,
            space_field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration information for indexing Confluence spaces.

            :param crawl_archived_spaces: ``TRUE`` to index archived spaces.
            :param crawl_personal_spaces: ``TRUE`` to index personal spaces. You can add restrictions to items in personal spaces. If personal spaces are indexed, queries without user context information may return restricted items from a personal space in their results. For more information, see `Filtering on user context <https://docs.aws.amazon.com/kendra/latest/dg/user-context-filter.html>`_ .
            :param exclude_spaces: A list of space keys of Confluence spaces. If you include a key, the blogs, documents, and attachments in the space are not indexed. If a space is in both the ``ExcludeSpaces`` and the ``IncludeSpaces`` list, the space is excluded.
            :param include_spaces: A list of space keys for Confluence spaces. If you include a key, the blogs, documents, and attachments in the space are indexed. Spaces that aren't in the list aren't indexed. A space in the list must exist. Otherwise, Amazon Kendra logs an error when the data source is synchronized. If a space is in both the ``IncludeSpaces`` and the ``ExcludeSpaces`` list, the space is excluded.
            :param space_field_mappings: Maps attributes or field names of Confluence spaces to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata. If you specify the ``SpaceFieldMappings`` parameter, you must specify at least one field mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                confluence_space_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty(
                    crawl_archived_spaces=False,
                    crawl_personal_spaces=False,
                    exclude_spaces=["excludeSpaces"],
                    include_spaces=["includeSpaces"],
                    space_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7aebcebcc785d4e9986d4da79693bcc763bfc9bc81f58fb9bf72b9ca1131c5af)
                check_type(argname="argument crawl_archived_spaces", value=crawl_archived_spaces, expected_type=type_hints["crawl_archived_spaces"])
                check_type(argname="argument crawl_personal_spaces", value=crawl_personal_spaces, expected_type=type_hints["crawl_personal_spaces"])
                check_type(argname="argument exclude_spaces", value=exclude_spaces, expected_type=type_hints["exclude_spaces"])
                check_type(argname="argument include_spaces", value=include_spaces, expected_type=type_hints["include_spaces"])
                check_type(argname="argument space_field_mappings", value=space_field_mappings, expected_type=type_hints["space_field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crawl_archived_spaces is not None:
                self._values["crawl_archived_spaces"] = crawl_archived_spaces
            if crawl_personal_spaces is not None:
                self._values["crawl_personal_spaces"] = crawl_personal_spaces
            if exclude_spaces is not None:
                self._values["exclude_spaces"] = exclude_spaces
            if include_spaces is not None:
                self._values["include_spaces"] = include_spaces
            if space_field_mappings is not None:
                self._values["space_field_mappings"] = space_field_mappings

        @builtins.property
        def crawl_archived_spaces(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to index archived spaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-crawlarchivedspaces
            '''
            result = self._values.get("crawl_archived_spaces")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def crawl_personal_spaces(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to index personal spaces.

            You can add restrictions to items in personal spaces. If personal spaces are indexed, queries without user context information may return restricted items from a personal space in their results. For more information, see `Filtering on user context <https://docs.aws.amazon.com/kendra/latest/dg/user-context-filter.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-crawlpersonalspaces
            '''
            result = self._values.get("crawl_personal_spaces")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclude_spaces(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of space keys of Confluence spaces.

            If you include a key, the blogs, documents, and attachments in the space are not indexed. If a space is in both the ``ExcludeSpaces`` and the ``IncludeSpaces`` list, the space is excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-excludespaces
            '''
            result = self._values.get("exclude_spaces")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include_spaces(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of space keys for Confluence spaces.

            If you include a key, the blogs, documents, and attachments in the space are indexed. Spaces that aren't in the list aren't indexed. A space in the list must exist. Otherwise, Amazon Kendra logs an error when the data source is synchronized. If a space is in both the ``IncludeSpaces`` and the ``ExcludeSpaces`` list, the space is excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-includespaces
            '''
            result = self._values.get("include_spaces")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def space_field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty"]]]]:
            '''Maps attributes or field names of Confluence spaces to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            If you specify the ``SpaceFieldMappings`` parameter, you must specify at least one field mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-spacefieldmappings
            '''
            result = self._values.get("space_field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceSpaceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "date_field_format": "dateFieldFormat",
            "index_field_name": "indexFieldName",
        },
    )
    class ConfluenceSpaceToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: typing.Optional[builtins.str] = None,
            date_field_format: typing.Optional[builtins.str] = None,
            index_field_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps attributes or field names of Confluence spaces to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            :param data_source_field_name: The name of the field in the data source.
            :param date_field_format: The format for date fields in the data source. If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.
            :param index_field_name: The name of the index field to map to the Confluence data source field. The index field type must match the Confluence field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespacetoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                confluence_space_to_index_field_mapping_property = kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    date_field_format="dateFieldFormat",
                    index_field_name="indexFieldName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa89b3774861771231bc597dc67a0b9132acb354df03c318b4bb152b5a52cbe8)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source_field_name is not None:
                self._values["data_source_field_name"] = data_source_field_name
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format
            if index_field_name is not None:
                self._values["index_field_name"] = index_field_name

        @builtins.property
        def data_source_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespacetoindexfieldmapping.html#cfn-kendra-datasource-confluencespacetoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The format for date fields in the data source.

            If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespacetoindexfieldmapping.html#cfn-kendra-datasource-confluencespacetoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the index field to map to the Confluence data source field.

            The index field type must match the Confluence field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespacetoindexfieldmapping.html#cfn-kendra-datasource-confluencespacetoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceSpaceToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ConnectionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_host": "databaseHost",
            "database_name": "databaseName",
            "database_port": "databasePort",
            "secret_arn": "secretArn",
            "table_name": "tableName",
        },
    )
    class ConnectionConfigurationProperty:
        def __init__(
            self,
            *,
            database_host: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            database_port: typing.Optional[jsii.Number] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information that's required to connect to a database.

            :param database_host: The name of the host for the database. Can be either a string (host.subdomain.domain.tld) or an IPv4 or IPv6 address.
            :param database_name: The name of the database containing the document data.
            :param database_port: The port that the database uses for connections.
            :param secret_arn: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that stores the credentials. The credentials should be a user-password pair. For more information, see `Using a Database Data Source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-database.html>`_ . For more information about AWS Secrets Manager , see `What Is AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ in the *AWS Secrets Manager* user guide.
            :param table_name: The name of the table that contains the document data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                connection_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ConnectionConfigurationProperty(
                    database_host="databaseHost",
                    database_name="databaseName",
                    database_port=123,
                    secret_arn="secretArn",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ae80d9493741b442df2a56d0a514718855519857e55565b0501cf07fe52a5ad)
                check_type(argname="argument database_host", value=database_host, expected_type=type_hints["database_host"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument database_port", value=database_port, expected_type=type_hints["database_port"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_host is not None:
                self._values["database_host"] = database_host
            if database_name is not None:
                self._values["database_name"] = database_name
            if database_port is not None:
                self._values["database_port"] = database_port
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def database_host(self) -> typing.Optional[builtins.str]:
            '''The name of the host for the database.

            Can be either a string (host.subdomain.domain.tld) or an IPv4 or IPv6 address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-databasehost
            '''
            result = self._values.get("database_host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database containing the document data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_port(self) -> typing.Optional[jsii.Number]:
            '''The port that the database uses for connections.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-databaseport
            '''
            result = self._values.get("database_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that stores the credentials.

            The credentials should be a user-password pair. For more information, see `Using a Database Data Source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-database.html>`_ . For more information about AWS Secrets Manager , see `What Is AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ in the *AWS Secrets Manager* user guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the table that contains the document data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.CustomDocumentEnrichmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "inline_configurations": "inlineConfigurations",
            "post_extraction_hook_configuration": "postExtractionHookConfiguration",
            "pre_extraction_hook_configuration": "preExtractionHookConfiguration",
            "role_arn": "roleArn",
        },
    )
    class CustomDocumentEnrichmentConfigurationProperty:
        def __init__(
            self,
            *,
            inline_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.InlineCustomDocumentEnrichmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            post_extraction_hook_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.HookConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            pre_extraction_hook_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.HookConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information for altering document metadata and content during the document ingestion process.

            For more information, see `Customizing document metadata during the ingestion process <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html>`_ .

            :param inline_configurations: Configuration information to alter document attributes or metadata fields and content when ingesting documents into Amazon Kendra.
            :param post_extraction_hook_configuration: Configuration information for invoking a Lambda function in AWS Lambda on the structured documents with their metadata and text extracted. You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Advanced data manipulation <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#advanced-data-manipulation>`_ .
            :param pre_extraction_hook_configuration: Configuration information for invoking a Lambda function in AWS Lambda on the original or raw documents before extracting their metadata and text. You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Advanced data manipulation <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#advanced-data-manipulation>`_ .
            :param role_arn: The Amazon Resource Name (ARN) of an IAM role with permission to run ``PreExtractionHookConfiguration`` and ``PostExtractionHookConfiguration`` for altering document metadata and content during the document ingestion process. For more information, see `an IAM roles for Amazon Kendra <https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                custom_document_enrichment_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.CustomDocumentEnrichmentConfigurationProperty(
                    inline_configurations=[kendra_mixins.CfnDataSourcePropsMixin.InlineCustomDocumentEnrichmentConfigurationProperty(
                        condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            operator="operator"
                        ),
                        document_content_deletion=False,
                        target=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                            target_document_attribute_key="targetDocumentAttributeKey",
                            target_document_attribute_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            target_document_attribute_value_deletion=False
                        )
                    )],
                    post_extraction_hook_configuration=kendra_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                        invocation_condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            operator="operator"
                        ),
                        lambda_arn="lambdaArn",
                        s3_bucket="s3Bucket"
                    ),
                    pre_extraction_hook_configuration=kendra_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                        invocation_condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            operator="operator"
                        ),
                        lambda_arn="lambdaArn",
                        s3_bucket="s3Bucket"
                    ),
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f071c683f9c6368eed022b07c33a6d22a3b12faf220b046f559ada014f5091b)
                check_type(argname="argument inline_configurations", value=inline_configurations, expected_type=type_hints["inline_configurations"])
                check_type(argname="argument post_extraction_hook_configuration", value=post_extraction_hook_configuration, expected_type=type_hints["post_extraction_hook_configuration"])
                check_type(argname="argument pre_extraction_hook_configuration", value=pre_extraction_hook_configuration, expected_type=type_hints["pre_extraction_hook_configuration"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if inline_configurations is not None:
                self._values["inline_configurations"] = inline_configurations
            if post_extraction_hook_configuration is not None:
                self._values["post_extraction_hook_configuration"] = post_extraction_hook_configuration
            if pre_extraction_hook_configuration is not None:
                self._values["pre_extraction_hook_configuration"] = pre_extraction_hook_configuration
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def inline_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.InlineCustomDocumentEnrichmentConfigurationProperty"]]]]:
            '''Configuration information to alter document attributes or metadata fields and content when ingesting documents into Amazon Kendra.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration-inlineconfigurations
            '''
            result = self._values.get("inline_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.InlineCustomDocumentEnrichmentConfigurationProperty"]]]], result)

        @builtins.property
        def post_extraction_hook_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HookConfigurationProperty"]]:
            '''Configuration information for invoking a Lambda function in AWS Lambda on the structured documents with their metadata and text extracted.

            You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Advanced data manipulation <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#advanced-data-manipulation>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration-postextractionhookconfiguration
            '''
            result = self._values.get("post_extraction_hook_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HookConfigurationProperty"]], result)

        @builtins.property
        def pre_extraction_hook_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HookConfigurationProperty"]]:
            '''Configuration information for invoking a Lambda function in AWS Lambda on the original or raw documents before extracting their metadata and text.

            You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Advanced data manipulation <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#advanced-data-manipulation>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration-preextractionhookconfiguration
            '''
            result = self._values.get("pre_extraction_hook_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.HookConfigurationProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an IAM role with permission to run ``PreExtractionHookConfiguration`` and ``PostExtractionHookConfiguration`` for altering document metadata and content during the document ingestion process.

            For more information, see `an IAM roles for Amazon Kendra <https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomDocumentEnrichmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.DataSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "confluence_configuration": "confluenceConfiguration",
            "database_configuration": "databaseConfiguration",
            "google_drive_configuration": "googleDriveConfiguration",
            "one_drive_configuration": "oneDriveConfiguration",
            "s3_configuration": "s3Configuration",
            "salesforce_configuration": "salesforceConfiguration",
            "service_now_configuration": "serviceNowConfiguration",
            "share_point_configuration": "sharePointConfiguration",
            "template_configuration": "templateConfiguration",
            "web_crawler_configuration": "webCrawlerConfiguration",
            "work_docs_configuration": "workDocsConfiguration",
        },
    )
    class DataSourceConfigurationProperty:
        def __init__(
            self,
            *,
            confluence_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConfluenceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            database_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DatabaseConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            google_drive_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.GoogleDriveConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            one_drive_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.OneDriveConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.S3DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            salesforce_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SalesforceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_now_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ServiceNowConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            share_point_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SharePointConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.TemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            web_crawler_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.WebCrawlerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            work_docs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.WorkDocsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information for an Amazon Kendra data source.

            :param confluence_configuration: Provides the configuration information to connect to Confluence as your data source.
            :param database_configuration: Provides the configuration information to connect to a database as your data source.
            :param google_drive_configuration: Provides the configuration information to connect to Google Drive as your data source.
            :param one_drive_configuration: Provides the configuration information to connect to Microsoft OneDrive as your data source.
            :param s3_configuration: Provides the configuration information to connect to an Amazon S3 bucket as your data source. .. epigraph:: Amazon Kendra now supports an upgraded Amazon S3 connector. You must now use the `TemplateConfiguration <https://docs.aws.amazon.com/kendra/latest/APIReference/API_TemplateConfiguration.html>`_ object instead of the ``S3DataSourceConfiguration`` object to configure your connector. Connectors configured using the older console and API architecture will continue to function as configured. However, you won't be able to edit or update them. If you want to edit or update your connector configuration, you must create a new connector. We recommended migrating your connector workflow to the upgraded version. Support for connectors configured using the older architecture is scheduled to end by June 2024.
            :param salesforce_configuration: Provides the configuration information to connect to Salesforce as your data source.
            :param service_now_configuration: Provides the configuration information to connect to ServiceNow as your data source.
            :param share_point_configuration: Provides the configuration information to connect to Microsoft SharePoint as your data source.
            :param template_configuration: Provides a template for the configuration information to connect to your data source.
            :param web_crawler_configuration: Provides the configuration information required for Amazon Kendra Web Crawler.
            :param work_docs_configuration: Provides the configuration information to connect to WorkDocs as your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                data_source_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.DataSourceConfigurationProperty(
                    confluence_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceConfigurationProperty(
                        attachment_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty(
                            attachment_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            crawl_attachments=False
                        ),
                        blog_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty(
                            blog_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        exclusion_patterns=["exclusionPatterns"],
                        inclusion_patterns=["inclusionPatterns"],
                        page_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty(
                            page_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        secret_arn="secretArn",
                        server_url="serverUrl",
                        space_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty(
                            crawl_archived_spaces=False,
                            crawl_personal_spaces=False,
                            exclude_spaces=["excludeSpaces"],
                            include_spaces=["includeSpaces"],
                            space_field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        version="version",
                        vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    database_configuration=kendra_mixins.CfnDataSourcePropsMixin.DatabaseConfigurationProperty(
                        acl_configuration=kendra_mixins.CfnDataSourcePropsMixin.AclConfigurationProperty(
                            allowed_groups_column_name="allowedGroupsColumnName"
                        ),
                        column_configuration=kendra_mixins.CfnDataSourcePropsMixin.ColumnConfigurationProperty(
                            change_detecting_columns=["changeDetectingColumns"],
                            document_data_column_name="documentDataColumnName",
                            document_id_column_name="documentIdColumnName",
                            document_title_column_name="documentTitleColumnName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        connection_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConnectionConfigurationProperty(
                            database_host="databaseHost",
                            database_name="databaseName",
                            database_port=123,
                            secret_arn="secretArn",
                            table_name="tableName"
                        ),
                        database_engine_type="databaseEngineType",
                        sql_configuration=kendra_mixins.CfnDataSourcePropsMixin.SqlConfigurationProperty(
                            query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                        ),
                        vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    google_drive_configuration=kendra_mixins.CfnDataSourcePropsMixin.GoogleDriveConfigurationProperty(
                        exclude_mime_types=["excludeMimeTypes"],
                        exclude_shared_drives=["excludeSharedDrives"],
                        exclude_user_accounts=["excludeUserAccounts"],
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        secret_arn="secretArn"
                    ),
                    one_drive_configuration=kendra_mixins.CfnDataSourcePropsMixin.OneDriveConfigurationProperty(
                        disable_local_groups=False,
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        one_drive_users=kendra_mixins.CfnDataSourcePropsMixin.OneDriveUsersProperty(
                            one_drive_user_list=["oneDriveUserList"],
                            one_drive_user_s3_path=kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                                bucket="bucket",
                                key="key"
                            )
                        ),
                        secret_arn="secretArn",
                        tenant_domain="tenantDomain"
                    ),
                    s3_configuration=kendra_mixins.CfnDataSourcePropsMixin.S3DataSourceConfigurationProperty(
                        access_control_list_configuration=kendra_mixins.CfnDataSourcePropsMixin.AccessControlListConfigurationProperty(
                            key_path="keyPath"
                        ),
                        bucket_name="bucketName",
                        documents_metadata_configuration=kendra_mixins.CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty(
                            s3_prefix="s3Prefix"
                        ),
                        exclusion_patterns=["exclusionPatterns"],
                        inclusion_patterns=["inclusionPatterns"],
                        inclusion_prefixes=["inclusionPrefixes"]
                    ),
                    salesforce_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceConfigurationProperty(
                        chatter_feed_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            include_filter_types=["includeFilterTypes"]
                        ),
                        crawl_attachments=False,
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"],
                        knowledge_article_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty(
                            custom_knowledge_article_type_configurations=[kendra_mixins.CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                                document_data_field_name="documentDataFieldName",
                                document_title_field_name="documentTitleFieldName",
                                field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                    data_source_field_name="dataSourceFieldName",
                                    date_field_format="dateFieldFormat",
                                    index_field_name="indexFieldName"
                                )],
                                name="name"
                            )],
                            included_states=["includedStates"],
                            standard_knowledge_article_type_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                                document_data_field_name="documentDataFieldName",
                                document_title_field_name="documentTitleFieldName",
                                field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                    data_source_field_name="dataSourceFieldName",
                                    date_field_format="dateFieldFormat",
                                    index_field_name="indexFieldName"
                                )]
                            )
                        ),
                        secret_arn="secretArn",
                        server_url="serverUrl",
                        standard_object_attachment_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty(
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        ),
                        standard_object_configurations=[kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            name="name"
                        )]
                    ),
                    service_now_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowConfigurationProperty(
                        authentication_type="authenticationType",
                        host_url="hostUrl",
                        knowledge_article_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty(
                            crawl_attachments=False,
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            filter_query="filterQuery",
                            include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                        ),
                        secret_arn="secretArn",
                        service_catalog_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty(
                            crawl_attachments=False,
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                        ),
                        service_now_build_version="serviceNowBuildVersion"
                    ),
                    share_point_configuration=kendra_mixins.CfnDataSourcePropsMixin.SharePointConfigurationProperty(
                        crawl_attachments=False,
                        disable_local_groups=False,
                        document_title_field_name="documentTitleFieldName",
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        secret_arn="secretArn",
                        share_point_version="sharePointVersion",
                        ssl_certificate_s3_path=kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                            bucket="bucket",
                            key="key"
                        ),
                        urls=["urls"],
                        use_change_log=False,
                        vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    template_configuration=kendra_mixins.CfnDataSourcePropsMixin.TemplateConfigurationProperty(
                        template="template"
                    ),
                    web_crawler_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerConfigurationProperty(
                        authentication_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty(
                            basic_authentication=[kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty(
                                credentials="credentials",
                                host="host",
                                port=123
                            )]
                        ),
                        crawl_depth=123,
                        max_content_size_per_page_in_mega_bytes=123,
                        max_links_per_page=123,
                        max_urls_per_minute_crawl_rate=123,
                        proxy_configuration=kendra_mixins.CfnDataSourcePropsMixin.ProxyConfigurationProperty(
                            credentials="credentials",
                            host="host",
                            port=123
                        ),
                        url_exclusion_patterns=["urlExclusionPatterns"],
                        url_inclusion_patterns=["urlInclusionPatterns"],
                        urls=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerUrlsProperty(
                            seed_url_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty(
                                seed_urls=["seedUrls"],
                                web_crawler_mode="webCrawlerMode"
                            ),
                            site_maps_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty(
                                site_maps=["siteMaps"]
                            )
                        )
                    ),
                    work_docs_configuration=kendra_mixins.CfnDataSourcePropsMixin.WorkDocsConfigurationProperty(
                        crawl_comments=False,
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        organization_id="organizationId",
                        use_change_log=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__61e949391af1fdd73449b43a7f30537e9f2b15c15fe6bdf30e3bdf1ac9b22e2c)
                check_type(argname="argument confluence_configuration", value=confluence_configuration, expected_type=type_hints["confluence_configuration"])
                check_type(argname="argument database_configuration", value=database_configuration, expected_type=type_hints["database_configuration"])
                check_type(argname="argument google_drive_configuration", value=google_drive_configuration, expected_type=type_hints["google_drive_configuration"])
                check_type(argname="argument one_drive_configuration", value=one_drive_configuration, expected_type=type_hints["one_drive_configuration"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument salesforce_configuration", value=salesforce_configuration, expected_type=type_hints["salesforce_configuration"])
                check_type(argname="argument service_now_configuration", value=service_now_configuration, expected_type=type_hints["service_now_configuration"])
                check_type(argname="argument share_point_configuration", value=share_point_configuration, expected_type=type_hints["share_point_configuration"])
                check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
                check_type(argname="argument web_crawler_configuration", value=web_crawler_configuration, expected_type=type_hints["web_crawler_configuration"])
                check_type(argname="argument work_docs_configuration", value=work_docs_configuration, expected_type=type_hints["work_docs_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if confluence_configuration is not None:
                self._values["confluence_configuration"] = confluence_configuration
            if database_configuration is not None:
                self._values["database_configuration"] = database_configuration
            if google_drive_configuration is not None:
                self._values["google_drive_configuration"] = google_drive_configuration
            if one_drive_configuration is not None:
                self._values["one_drive_configuration"] = one_drive_configuration
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if salesforce_configuration is not None:
                self._values["salesforce_configuration"] = salesforce_configuration
            if service_now_configuration is not None:
                self._values["service_now_configuration"] = service_now_configuration
            if share_point_configuration is not None:
                self._values["share_point_configuration"] = share_point_configuration
            if template_configuration is not None:
                self._values["template_configuration"] = template_configuration
            if web_crawler_configuration is not None:
                self._values["web_crawler_configuration"] = web_crawler_configuration
            if work_docs_configuration is not None:
                self._values["work_docs_configuration"] = work_docs_configuration

        @builtins.property
        def confluence_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceConfigurationProperty"]]:
            '''Provides the configuration information to connect to Confluence as your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-confluenceconfiguration
            '''
            result = self._values.get("confluence_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConfluenceConfigurationProperty"]], result)

        @builtins.property
        def database_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DatabaseConfigurationProperty"]]:
            '''Provides the configuration information to connect to a database as your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-databaseconfiguration
            '''
            result = self._values.get("database_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DatabaseConfigurationProperty"]], result)

        @builtins.property
        def google_drive_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.GoogleDriveConfigurationProperty"]]:
            '''Provides the configuration information to connect to Google Drive as your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-googledriveconfiguration
            '''
            result = self._values.get("google_drive_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.GoogleDriveConfigurationProperty"]], result)

        @builtins.property
        def one_drive_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.OneDriveConfigurationProperty"]]:
            '''Provides the configuration information to connect to Microsoft OneDrive as your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-onedriveconfiguration
            '''
            result = self._values.get("one_drive_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.OneDriveConfigurationProperty"]], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.S3DataSourceConfigurationProperty"]]:
            '''Provides the configuration information to connect to an Amazon S3 bucket as your data source.

            .. epigraph::

               Amazon Kendra now supports an upgraded Amazon S3 connector.

               You must now use the `TemplateConfiguration <https://docs.aws.amazon.com/kendra/latest/APIReference/API_TemplateConfiguration.html>`_ object instead of the ``S3DataSourceConfiguration`` object to configure your connector.

               Connectors configured using the older console and API architecture will continue to function as configured. However, you won't be able to edit or update them. If you want to edit or update your connector configuration, you must create a new connector.

               We recommended migrating your connector workflow to the upgraded version. Support for connectors configured using the older architecture is scheduled to end by June 2024.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.S3DataSourceConfigurationProperty"]], result)

        @builtins.property
        def salesforce_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceConfigurationProperty"]]:
            '''Provides the configuration information to connect to Salesforce as your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-salesforceconfiguration
            '''
            result = self._values.get("salesforce_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceConfigurationProperty"]], result)

        @builtins.property
        def service_now_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ServiceNowConfigurationProperty"]]:
            '''Provides the configuration information to connect to ServiceNow as your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-servicenowconfiguration
            '''
            result = self._values.get("service_now_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ServiceNowConfigurationProperty"]], result)

        @builtins.property
        def share_point_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SharePointConfigurationProperty"]]:
            '''Provides the configuration information to connect to Microsoft SharePoint as your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-sharepointconfiguration
            '''
            result = self._values.get("share_point_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SharePointConfigurationProperty"]], result)

        @builtins.property
        def template_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.TemplateConfigurationProperty"]]:
            '''Provides a template for the configuration information to connect to your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-templateconfiguration
            '''
            result = self._values.get("template_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.TemplateConfigurationProperty"]], result)

        @builtins.property
        def web_crawler_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerConfigurationProperty"]]:
            '''Provides the configuration information required for Amazon Kendra Web Crawler.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-webcrawlerconfiguration
            '''
            result = self._values.get("web_crawler_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerConfigurationProperty"]], result)

        @builtins.property
        def work_docs_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WorkDocsConfigurationProperty"]]:
            '''Provides the configuration information to connect to WorkDocs as your data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-workdocsconfiguration
            '''
            result = self._values.get("work_docs_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WorkDocsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "date_field_format": "dateFieldFormat",
            "index_field_name": "indexFieldName",
        },
    )
    class DataSourceToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: typing.Optional[builtins.str] = None,
            date_field_format: typing.Optional[builtins.str] = None,
            index_field_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps a column or attribute in the data source to an index field.

            You must first create the fields in the index using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation.

            :param data_source_field_name: The name of the field in the data source. You must first create the index field using the ``UpdateIndex`` API.
            :param date_field_format: The format for date fields in the data source. If the field specified in ``DataSourceFieldName`` is a date field, you must specify the date format. If the field is not a date field, an exception is thrown.
            :param index_field_name: The name of the index field to map to the data source field. The index field type must match the data source field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcetoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                data_source_to_index_field_mapping_property = kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    date_field_format="dateFieldFormat",
                    index_field_name="indexFieldName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__23b35e946e502e0379a557043dcab4a69d774fd4172dd2cfff06bbbbebbc136e)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source_field_name is not None:
                self._values["data_source_field_name"] = data_source_field_name
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format
            if index_field_name is not None:
                self._values["index_field_name"] = index_field_name

        @builtins.property
        def data_source_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the data source.

            You must first create the index field using the ``UpdateIndex`` API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcetoindexfieldmapping.html#cfn-kendra-datasource-datasourcetoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The format for date fields in the data source.

            If the field specified in ``DataSourceFieldName`` is a date field, you must specify the date format. If the field is not a date field, an exception is thrown.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcetoindexfieldmapping.html#cfn-kendra-datasource-datasourcetoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the index field to map to the data source field.

            The index field type must match the data source field type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcetoindexfieldmapping.html#cfn-kendra-datasource-datasourcetoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class DataSourceVpcConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information to connect to an Amazon VPC.

            :param security_group_ids: A list of identifiers of security groups within your Amazon VPC. The security groups should enable Amazon Kendra to connect to the data source.
            :param subnet_ids: A list of identifiers for subnets within your Amazon VPC. The subnets should be able to connect to each other in the VPC, and they should have outgoing access to the Internet through a NAT device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcevpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                data_source_vpc_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44a38248652dacf61c2e104a521d29d50548946a2a9a4064d1ca9b9d23a6ddad)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of identifiers of security groups within your Amazon VPC.

            The security groups should enable Amazon Kendra to connect to the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcevpcconfiguration.html#cfn-kendra-datasource-datasourcevpcconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of identifiers for subnets within your Amazon VPC.

            The subnets should be able to connect to each other in the VPC, and they should have outgoing access to the Internet through a NAT device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcevpcconfiguration.html#cfn-kendra-datasource-datasourcevpcconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.DatabaseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acl_configuration": "aclConfiguration",
            "column_configuration": "columnConfiguration",
            "connection_configuration": "connectionConfiguration",
            "database_engine_type": "databaseEngineType",
            "sql_configuration": "sqlConfiguration",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class DatabaseConfigurationProperty:
        def __init__(
            self,
            *,
            acl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.AclConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            column_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ColumnConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            connection_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ConnectionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            database_engine_type: typing.Optional[builtins.str] = None,
            sql_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SqlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information to an `Amazon Kendra supported database <https://docs.aws.amazon.com/kendra/latest/dg/data-source-database.html>`_ .

            :param acl_configuration: Information about the database column that provides information for user context filtering.
            :param column_configuration: Information about where the index should get the document information from the database.
            :param connection_configuration: Configuration information that's required to connect to a database.
            :param database_engine_type: The type of database engine that runs the database.
            :param sql_configuration: Provides information about how Amazon Kendra uses quote marks around SQL identifiers when querying a database data source.
            :param vpc_configuration: Provides information for connecting to an Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                database_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.DatabaseConfigurationProperty(
                    acl_configuration=kendra_mixins.CfnDataSourcePropsMixin.AclConfigurationProperty(
                        allowed_groups_column_name="allowedGroupsColumnName"
                    ),
                    column_configuration=kendra_mixins.CfnDataSourcePropsMixin.ColumnConfigurationProperty(
                        change_detecting_columns=["changeDetectingColumns"],
                        document_data_column_name="documentDataColumnName",
                        document_id_column_name="documentIdColumnName",
                        document_title_column_name="documentTitleColumnName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    connection_configuration=kendra_mixins.CfnDataSourcePropsMixin.ConnectionConfigurationProperty(
                        database_host="databaseHost",
                        database_name="databaseName",
                        database_port=123,
                        secret_arn="secretArn",
                        table_name="tableName"
                    ),
                    database_engine_type="databaseEngineType",
                    sql_configuration=kendra_mixins.CfnDataSourcePropsMixin.SqlConfigurationProperty(
                        query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                    ),
                    vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__641a91f5c9c19f243e826ae90836b815dfd48f2c64cade6f183e6e37f7033c81)
                check_type(argname="argument acl_configuration", value=acl_configuration, expected_type=type_hints["acl_configuration"])
                check_type(argname="argument column_configuration", value=column_configuration, expected_type=type_hints["column_configuration"])
                check_type(argname="argument connection_configuration", value=connection_configuration, expected_type=type_hints["connection_configuration"])
                check_type(argname="argument database_engine_type", value=database_engine_type, expected_type=type_hints["database_engine_type"])
                check_type(argname="argument sql_configuration", value=sql_configuration, expected_type=type_hints["sql_configuration"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acl_configuration is not None:
                self._values["acl_configuration"] = acl_configuration
            if column_configuration is not None:
                self._values["column_configuration"] = column_configuration
            if connection_configuration is not None:
                self._values["connection_configuration"] = connection_configuration
            if database_engine_type is not None:
                self._values["database_engine_type"] = database_engine_type
            if sql_configuration is not None:
                self._values["sql_configuration"] = sql_configuration
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def acl_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AclConfigurationProperty"]]:
            '''Information about the database column that provides information for user context filtering.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-aclconfiguration
            '''
            result = self._values.get("acl_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AclConfigurationProperty"]], result)

        @builtins.property
        def column_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ColumnConfigurationProperty"]]:
            '''Information about where the index should get the document information from the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-columnconfiguration
            '''
            result = self._values.get("column_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ColumnConfigurationProperty"]], result)

        @builtins.property
        def connection_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConnectionConfigurationProperty"]]:
            '''Configuration information that's required to connect to a database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-connectionconfiguration
            '''
            result = self._values.get("connection_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ConnectionConfigurationProperty"]], result)

        @builtins.property
        def database_engine_type(self) -> typing.Optional[builtins.str]:
            '''The type of database engine that runs the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-databaseenginetype
            '''
            result = self._values.get("database_engine_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sql_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SqlConfigurationProperty"]]:
            '''Provides information about how Amazon Kendra uses quote marks around SQL identifiers when querying a database data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-sqlconfiguration
            '''
            result = self._values.get("sql_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SqlConfigurationProperty"]], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty"]]:
            '''Provides information for connecting to an Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_document_attribute_key": "conditionDocumentAttributeKey",
            "condition_on_value": "conditionOnValue",
            "operator": "operator",
        },
    )
    class DocumentAttributeConditionProperty:
        def __init__(
            self,
            *,
            condition_document_attribute_key: typing.Optional[builtins.str] = None,
            condition_on_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The condition used for the target document attribute or metadata field when ingesting documents into Amazon Kendra.

            You use this with `DocumentAttributeTarget to apply the condition <https://docs.aws.amazon.com/kendra/latest/dg/API_DocumentAttributeTarget.html>`_ .

            For example, you can create the 'Department' target field and have it prefill department names associated with the documents based on information in the 'Source_URI' field. Set the condition that if the 'Source_URI' field contains 'financial' in its URI value, then prefill the target field 'Department' with the target value 'Finance' for the document.

            Amazon Kendra cannot create a target field if it has not already been created as an index field. After you create your index field, you can create a document metadata field using ``DocumentAttributeTarget`` . Amazon Kendra then will map your newly created metadata field to your index field.

            :param condition_document_attribute_key: The identifier of the document attribute used for the condition. For example, 'Source_URI' could be an identifier for the attribute or metadata field that contains source URIs associated with the documents. Amazon Kendra currently does not support ``_document_body`` as an attribute key used for the condition.
            :param condition_on_value: The value used by the operator. For example, you can specify the value 'financial' for strings in the 'Source_URI' field that partially match or contain this value.
            :param operator: The condition operator. For example, you can use 'Contains' to partially match a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributecondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                document_attribute_condition_property = kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                    condition_document_attribute_key="conditionDocumentAttributeKey",
                    condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                        date_value="dateValue",
                        long_value=123,
                        string_list_value=["stringListValue"],
                        string_value="stringValue"
                    ),
                    operator="operator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__849fa15a939ef611f2628654a7c7a5cddb4849ac49ccf80d98079112658863ba)
                check_type(argname="argument condition_document_attribute_key", value=condition_document_attribute_key, expected_type=type_hints["condition_document_attribute_key"])
                check_type(argname="argument condition_on_value", value=condition_on_value, expected_type=type_hints["condition_on_value"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition_document_attribute_key is not None:
                self._values["condition_document_attribute_key"] = condition_document_attribute_key
            if condition_on_value is not None:
                self._values["condition_on_value"] = condition_on_value
            if operator is not None:
                self._values["operator"] = operator

        @builtins.property
        def condition_document_attribute_key(self) -> typing.Optional[builtins.str]:
            '''The identifier of the document attribute used for the condition.

            For example, 'Source_URI' could be an identifier for the attribute or metadata field that contains source URIs associated with the documents.

            Amazon Kendra currently does not support ``_document_body`` as an attribute key used for the condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributecondition.html#cfn-kendra-datasource-documentattributecondition-conditiondocumentattributekey
            '''
            result = self._values.get("condition_document_attribute_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def condition_on_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeValueProperty"]]:
            '''The value used by the operator.

            For example, you can specify the value 'financial' for strings in the 'Source_URI' field that partially match or contain this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributecondition.html#cfn-kendra-datasource-documentattributecondition-conditiononvalue
            '''
            result = self._values.get("condition_on_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeValueProperty"]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The condition operator.

            For example, you can use 'Contains' to partially match a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributecondition.html#cfn-kendra-datasource-documentattributecondition-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_document_attribute_key": "targetDocumentAttributeKey",
            "target_document_attribute_value": "targetDocumentAttributeValue",
            "target_document_attribute_value_deletion": "targetDocumentAttributeValueDeletion",
        },
    )
    class DocumentAttributeTargetProperty:
        def __init__(
            self,
            *,
            target_document_attribute_key: typing.Optional[builtins.str] = None,
            target_document_attribute_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The target document attribute or metadata field you want to alter when ingesting documents into Amazon Kendra.

            For example, you can delete customer identification numbers associated with the documents, stored in the document metadata field called 'Customer_ID'. You set the target key as 'Customer_ID' and the deletion flag to ``TRUE`` . This removes all customer ID values in the field 'Customer_ID'. This would scrub personally identifiable information from each document's metadata.

            Amazon Kendra cannot create a target field if it has not already been created as an index field. After you create your index field, you can create a document metadata field using ``DocumentAttributeTarget`` . Amazon Kendra then will map your newly created metadata field to your index field.

            You can also use this with `DocumentAttributeCondition <https://docs.aws.amazon.com/kendra/latest/dg/API_DocumentAttributeCondition.html>`_ .

            :param target_document_attribute_key: The identifier of the target document attribute or metadata field. For example, 'Department' could be an identifier for the target attribute or metadata field that includes the department names associated with the documents.
            :param target_document_attribute_value: The target value you want to create for the target attribute. For example, 'Finance' could be the target value for the target attribute key 'Department'.
            :param target_document_attribute_value_deletion: ``TRUE`` to delete the existing target value for your specified target attribute key. You cannot create a target value and set this to ``TRUE`` . To create a target value ( ``TargetDocumentAttributeValue`` ), set this to ``FALSE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributetarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                document_attribute_target_property = kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                    target_document_attribute_key="targetDocumentAttributeKey",
                    target_document_attribute_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                        date_value="dateValue",
                        long_value=123,
                        string_list_value=["stringListValue"],
                        string_value="stringValue"
                    ),
                    target_document_attribute_value_deletion=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c1fbacd6ff60a75dec522269c036933188e757e1ed21c6c2c44301dc8be64a9)
                check_type(argname="argument target_document_attribute_key", value=target_document_attribute_key, expected_type=type_hints["target_document_attribute_key"])
                check_type(argname="argument target_document_attribute_value", value=target_document_attribute_value, expected_type=type_hints["target_document_attribute_value"])
                check_type(argname="argument target_document_attribute_value_deletion", value=target_document_attribute_value_deletion, expected_type=type_hints["target_document_attribute_value_deletion"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_document_attribute_key is not None:
                self._values["target_document_attribute_key"] = target_document_attribute_key
            if target_document_attribute_value is not None:
                self._values["target_document_attribute_value"] = target_document_attribute_value
            if target_document_attribute_value_deletion is not None:
                self._values["target_document_attribute_value_deletion"] = target_document_attribute_value_deletion

        @builtins.property
        def target_document_attribute_key(self) -> typing.Optional[builtins.str]:
            '''The identifier of the target document attribute or metadata field.

            For example, 'Department' could be an identifier for the target attribute or metadata field that includes the department names associated with the documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributetarget.html#cfn-kendra-datasource-documentattributetarget-targetdocumentattributekey
            '''
            result = self._values.get("target_document_attribute_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_document_attribute_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeValueProperty"]]:
            '''The target value you want to create for the target attribute.

            For example, 'Finance' could be the target value for the target attribute key 'Department'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributetarget.html#cfn-kendra-datasource-documentattributetarget-targetdocumentattributevalue
            '''
            result = self._values.get("target_document_attribute_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeValueProperty"]], result)

        @builtins.property
        def target_document_attribute_value_deletion(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to delete the existing target value for your specified target attribute key.

            You cannot create a target value and set this to ``TRUE`` . To create a target value ( ``TargetDocumentAttributeValue`` ), set this to ``FALSE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributetarget.html#cfn-kendra-datasource-documentattributetarget-targetdocumentattributevaluedeletion
            '''
            result = self._values.get("target_document_attribute_value_deletion")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "date_value": "dateValue",
            "long_value": "longValue",
            "string_list_value": "stringListValue",
            "string_value": "stringValue",
        },
    )
    class DocumentAttributeValueProperty:
        def __init__(
            self,
            *,
            date_value: typing.Optional[builtins.str] = None,
            long_value: typing.Optional[jsii.Number] = None,
            string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The value of a document attribute.

            You can only provide one value for a document attribute.

            :param date_value: A date expressed as an ISO 8601 string. It is important for the time zone to be included in the ISO 8601 date-time format. For example, 2012-03-25T12:30:10+01:00 is the ISO 8601 date-time format for March 25th 2012 at 12:30PM (plus 10 seconds) in Central European Time.
            :param long_value: A long integer value.
            :param string_list_value: A list of strings. The default maximum length or number of strings is 10.
            :param string_value: A string, such as "department".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                document_attribute_value_property = kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                    date_value="dateValue",
                    long_value=123,
                    string_list_value=["stringListValue"],
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76fd95d20e9648b4a6a18f07ac1e2f005c7b7dd6cf687128e8ecac67afa0ebd2)
                check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if date_value is not None:
                self._values["date_value"] = date_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if string_list_value is not None:
                self._values["string_list_value"] = string_list_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def date_value(self) -> typing.Optional[builtins.str]:
            '''A date expressed as an ISO 8601 string.

            It is important for the time zone to be included in the ISO 8601 date-time format. For example, 2012-03-25T12:30:10+01:00 is the ISO 8601 date-time format for March 25th 2012 at 12:30PM (plus 10 seconds) in Central European Time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html#cfn-kendra-datasource-documentattributevalue-datevalue
            '''
            result = self._values.get("date_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long integer value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html#cfn-kendra-datasource-documentattributevalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of strings.

            The default maximum length or number of strings is 10.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html#cfn-kendra-datasource-documentattributevalue-stringlistvalue
            '''
            result = self._values.get("string_list_value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string, such as "department".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html#cfn-kendra-datasource-documentattributevalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_prefix": "s3Prefix"},
    )
    class DocumentsMetadataConfigurationProperty:
        def __init__(self, *, s3_prefix: typing.Optional[builtins.str] = None) -> None:
            '''Document metadata files that contain information such as the document access control information, source URI, document author, and custom attributes.

            Each metadata file contains metadata about a single document.

            :param s3_prefix: A prefix used to filter metadata configuration files in the AWS S3 bucket. The S3 bucket might contain multiple metadata files. Use ``S3Prefix`` to include only the desired metadata files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentsmetadataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                documents_metadata_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty(
                    s3_prefix="s3Prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb2902df0947b3d78acf32af1207e684537c9b835b3e23be52e79ad1500800e5)
                check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_prefix is not None:
                self._values["s3_prefix"] = s3_prefix

        @builtins.property
        def s3_prefix(self) -> typing.Optional[builtins.str]:
            '''A prefix used to filter metadata configuration files in the AWS S3 bucket.

            The S3 bucket might contain multiple metadata files. Use ``S3Prefix`` to include only the desired metadata files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentsmetadataconfiguration.html#cfn-kendra-datasource-documentsmetadataconfiguration-s3prefix
            '''
            result = self._values.get("s3_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentsMetadataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.GoogleDriveConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_mime_types": "excludeMimeTypes",
            "exclude_shared_drives": "excludeSharedDrives",
            "exclude_user_accounts": "excludeUserAccounts",
            "exclusion_patterns": "exclusionPatterns",
            "field_mappings": "fieldMappings",
            "inclusion_patterns": "inclusionPatterns",
            "secret_arn": "secretArn",
        },
    )
    class GoogleDriveConfigurationProperty:
        def __init__(
            self,
            *,
            exclude_mime_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            exclude_shared_drives: typing.Optional[typing.Sequence[builtins.str]] = None,
            exclude_user_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information to connect to Google Drive as your data source.

            :param exclude_mime_types: A list of MIME types to exclude from the index. All documents matching the specified MIME type are excluded. For a list of MIME types, see `Using a Google Workspace Drive data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-google-drive.html>`_ .
            :param exclude_shared_drives: A list of identifiers or shared drives to exclude from the index. All files and folders stored on the shared drive are excluded.
            :param exclude_user_accounts: A list of email addresses of the users. Documents owned by these users are excluded from the index. Documents shared with excluded users are indexed unless they are excluded in another way.
            :param exclusion_patterns: A list of regular expression patterns to exclude certain items in your Google Drive, including shared drives and users' My Drives. Items that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.
            :param field_mappings: Maps Google Drive data source attributes or field names to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Google Drive fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Google Drive data source field names must exist in your Google Drive custom metadata.
            :param inclusion_patterns: A list of regular expression patterns to include certain items in your Google Drive, including shared drives and users' My Drives. Items that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.
            :param secret_arn: The Amazon Resource Name (ARN) of a AWS Secrets Manager secret that contains the credentials required to connect to Google Drive. For more information, see `Using a Google Workspace Drive data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-google-drive.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                google_drive_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.GoogleDriveConfigurationProperty(
                    exclude_mime_types=["excludeMimeTypes"],
                    exclude_shared_drives=["excludeSharedDrives"],
                    exclude_user_accounts=["excludeUserAccounts"],
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea7714136dfa2254133a5ee0c94edfa6069130f50826c5f8a422a8c1b3c4f322)
                check_type(argname="argument exclude_mime_types", value=exclude_mime_types, expected_type=type_hints["exclude_mime_types"])
                check_type(argname="argument exclude_shared_drives", value=exclude_shared_drives, expected_type=type_hints["exclude_shared_drives"])
                check_type(argname="argument exclude_user_accounts", value=exclude_user_accounts, expected_type=type_hints["exclude_user_accounts"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exclude_mime_types is not None:
                self._values["exclude_mime_types"] = exclude_mime_types
            if exclude_shared_drives is not None:
                self._values["exclude_shared_drives"] = exclude_shared_drives
            if exclude_user_accounts is not None:
                self._values["exclude_user_accounts"] = exclude_user_accounts
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def exclude_mime_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of MIME types to exclude from the index. All documents matching the specified MIME type are excluded.

            For a list of MIME types, see `Using a Google Workspace Drive data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-google-drive.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-excludemimetypes
            '''
            result = self._values.get("exclude_mime_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exclude_shared_drives(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of identifiers or shared drives to exclude from the index.

            All files and folders stored on the shared drive are excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-excludeshareddrives
            '''
            result = self._values.get("exclude_shared_drives")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exclude_user_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of email addresses of the users.

            Documents owned by these users are excluded from the index. Documents shared with excluded users are indexed unless they are excluded in another way.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-excludeuseraccounts
            '''
            result = self._values.get("exclude_user_accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain items in your Google Drive, including shared drives and users' My Drives.

            Items that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''Maps Google Drive data source attributes or field names to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Google Drive fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Google Drive data source field names must exist in your Google Drive custom metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain items in your Google Drive, including shared drives and users' My Drives.

            Items that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of a AWS Secrets Manager secret that contains the credentials required to connect to Google Drive.

            For more information, see `Using a Google Workspace Drive data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-google-drive.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GoogleDriveConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.HookConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "invocation_condition": "invocationCondition",
            "lambda_arn": "lambdaArn",
            "s3_bucket": "s3Bucket",
        },
    )
    class HookConfigurationProperty:
        def __init__(
            self,
            *,
            invocation_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_arn: typing.Optional[builtins.str] = None,
            s3_bucket: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information for invoking a Lambda function in AWS Lambda to alter document metadata and content when ingesting documents into Amazon Kendra.

            You can configure your Lambda function using `PreExtractionHookConfiguration <https://docs.aws.amazon.com/kendra/latest/dg/API_CustomDocumentEnrichmentConfiguration.html>`_ if you want to apply advanced alterations on the original or raw documents. If you want to apply advanced alterations on the Amazon Kendra structured documents, you must configure your Lambda function using `PostExtractionHookConfiguration <https://docs.aws.amazon.com/kendra/latest/dg/API_CustomDocumentEnrichmentConfiguration.html>`_ . You can only invoke one Lambda function. However, this function can invoke other functions it requires.

            For more information, see `Customizing document metadata during the ingestion process <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html>`_ .

            :param invocation_condition: The condition used for when a Lambda function should be invoked. For example, you can specify a condition that if there are empty date-time values, then Amazon Kendra should invoke a function that inserts the current date-time.
            :param lambda_arn: The Amazon Resource Name (ARN) of an IAM role with permission to run a Lambda function during ingestion. For more information, see `an IAM roles for Amazon Kendra <https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html>`_ .
            :param s3_bucket: Stores the original, raw documents or the structured, parsed documents before and after altering them. For more information, see `Data contracts for Lambda functions <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#cde-data-contracts-lambda>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-hookconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                hook_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.HookConfigurationProperty(
                    invocation_condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        ),
                        operator="operator"
                    ),
                    lambda_arn="lambdaArn",
                    s3_bucket="s3Bucket"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__61c661a602d8dd4a70c56357f93f98b1e9fd3a5d62021b4a9d45a361533060e8)
                check_type(argname="argument invocation_condition", value=invocation_condition, expected_type=type_hints["invocation_condition"])
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invocation_condition is not None:
                self._values["invocation_condition"] = invocation_condition
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket

        @builtins.property
        def invocation_condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeConditionProperty"]]:
            '''The condition used for when a Lambda function should be invoked.

            For example, you can specify a condition that if there are empty date-time values, then Amazon Kendra should invoke a function that inserts the current date-time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-hookconfiguration.html#cfn-kendra-datasource-hookconfiguration-invocationcondition
            '''
            result = self._values.get("invocation_condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeConditionProperty"]], result)

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an IAM role with permission to run a Lambda function during ingestion.

            For more information, see `an IAM roles for Amazon Kendra <https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-hookconfiguration.html#cfn-kendra-datasource-hookconfiguration-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''Stores the original, raw documents or the structured, parsed documents before and after altering them.

            For more information, see `Data contracts for Lambda functions <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#cde-data-contracts-lambda>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-hookconfiguration.html#cfn-kendra-datasource-hookconfiguration-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HookConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.InlineCustomDocumentEnrichmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition": "condition",
            "document_content_deletion": "documentContentDeletion",
            "target": "target",
        },
    )
    class InlineCustomDocumentEnrichmentConfigurationProperty:
        def __init__(
            self,
            *,
            condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            document_content_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentAttributeTargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information for applying basic logic to alter document metadata and content when ingesting documents into Amazon Kendra.

            To apply advanced logic, to go beyond what you can do with basic logic, see `HookConfiguration <https://docs.aws.amazon.com/kendra/latest/dg/API_HookConfiguration.html>`_ .

            For more information, see `Customizing document metadata during the ingestion process <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html>`_ .

            :param condition: Configuration of the condition used for the target document attribute or metadata field when ingesting documents into Amazon Kendra.
            :param document_content_deletion: ``TRUE`` to delete content if the condition used for the target attribute is met.
            :param target: Configuration of the target document attribute or metadata field when ingesting documents into Amazon Kendra. You can also include a value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-inlinecustomdocumentenrichmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                inline_custom_document_enrichment_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.InlineCustomDocumentEnrichmentConfigurationProperty(
                    condition=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        condition_on_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        ),
                        operator="operator"
                    ),
                    document_content_deletion=False,
                    target=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeTargetProperty(
                        target_document_attribute_key="targetDocumentAttributeKey",
                        target_document_attribute_value=kendra_mixins.CfnDataSourcePropsMixin.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        ),
                        target_document_attribute_value_deletion=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7464a9b6abb908eaf873d1220abb95ba3bae02a1d94069f0e1f9b33465a9d12a)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument document_content_deletion", value=document_content_deletion, expected_type=type_hints["document_content_deletion"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition is not None:
                self._values["condition"] = condition
            if document_content_deletion is not None:
                self._values["document_content_deletion"] = document_content_deletion
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeConditionProperty"]]:
            '''Configuration of the condition used for the target document attribute or metadata field when ingesting documents into Amazon Kendra.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-inlinecustomdocumentenrichmentconfiguration.html#cfn-kendra-datasource-inlinecustomdocumentenrichmentconfiguration-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeConditionProperty"]], result)

        @builtins.property
        def document_content_deletion(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to delete content if the condition used for the target attribute is met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-inlinecustomdocumentenrichmentconfiguration.html#cfn-kendra-datasource-inlinecustomdocumentenrichmentconfiguration-documentcontentdeletion
            '''
            result = self._values.get("document_content_deletion")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def target(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeTargetProperty"]]:
            '''Configuration of the target document attribute or metadata field when ingesting documents into Amazon Kendra.

            You can also include a value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-inlinecustomdocumentenrichmentconfiguration.html#cfn-kendra-datasource-inlinecustomdocumentenrichmentconfiguration-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentAttributeTargetProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InlineCustomDocumentEnrichmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.OneDriveConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "disable_local_groups": "disableLocalGroups",
            "exclusion_patterns": "exclusionPatterns",
            "field_mappings": "fieldMappings",
            "inclusion_patterns": "inclusionPatterns",
            "one_drive_users": "oneDriveUsers",
            "secret_arn": "secretArn",
            "tenant_domain": "tenantDomain",
        },
    )
    class OneDriveConfigurationProperty:
        def __init__(
            self,
            *,
            disable_local_groups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            one_drive_users: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.OneDriveUsersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            tenant_domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information to connect to OneDrive as your data source.

            :param disable_local_groups: ``TRUE`` to disable local groups information.
            :param exclusion_patterns: A list of regular expression patterns to exclude certain documents in your OneDrive. Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The pattern is applied to the file name.
            :param field_mappings: A list of ``DataSourceToIndexFieldMapping`` objects that map OneDrive data source attributes or field names to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to OneDrive fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The OneDrive data source field names must exist in your OneDrive custom metadata.
            :param inclusion_patterns: A list of regular expression patterns to include certain documents in your OneDrive. Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The pattern is applied to the file name.
            :param one_drive_users: A list of user accounts whose documents should be indexed.
            :param secret_arn: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password to connect to OneDrive. The user name should be the application ID for the OneDrive application, and the password is the application key for the OneDrive application.
            :param tenant_domain: The Azure Active Directory domain of the organization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                one_drive_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.OneDriveConfigurationProperty(
                    disable_local_groups=False,
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    one_drive_users=kendra_mixins.CfnDataSourcePropsMixin.OneDriveUsersProperty(
                        one_drive_user_list=["oneDriveUserList"],
                        one_drive_user_s3_path=kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    secret_arn="secretArn",
                    tenant_domain="tenantDomain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc7d3e54315073d85c9253803f76b7480a31edd18cbcb29fe83d779e0c1648be)
                check_type(argname="argument disable_local_groups", value=disable_local_groups, expected_type=type_hints["disable_local_groups"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument one_drive_users", value=one_drive_users, expected_type=type_hints["one_drive_users"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument tenant_domain", value=tenant_domain, expected_type=type_hints["tenant_domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if disable_local_groups is not None:
                self._values["disable_local_groups"] = disable_local_groups
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if one_drive_users is not None:
                self._values["one_drive_users"] = one_drive_users
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if tenant_domain is not None:
                self._values["tenant_domain"] = tenant_domain

        @builtins.property
        def disable_local_groups(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to disable local groups information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-disablelocalgroups
            '''
            result = self._values.get("disable_local_groups")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain documents in your OneDrive.

            Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The pattern is applied to the file name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''A list of ``DataSourceToIndexFieldMapping`` objects that map OneDrive data source attributes or field names to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to OneDrive fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The OneDrive data source field names must exist in your OneDrive custom metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain documents in your OneDrive.

            Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The pattern is applied to the file name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def one_drive_users(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.OneDriveUsersProperty"]]:
            '''A list of user accounts whose documents should be indexed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-onedriveusers
            '''
            result = self._values.get("one_drive_users")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.OneDriveUsersProperty"]], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password to connect to OneDrive.

            The user name should be the application ID for the OneDrive application, and the password is the application key for the OneDrive application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tenant_domain(self) -> typing.Optional[builtins.str]:
            '''The Azure Active Directory domain of the organization.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-tenantdomain
            '''
            result = self._values.get("tenant_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OneDriveConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.OneDriveUsersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "one_drive_user_list": "oneDriveUserList",
            "one_drive_user_s3_path": "oneDriveUserS3Path",
        },
    )
    class OneDriveUsersProperty:
        def __init__(
            self,
            *,
            one_drive_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            one_drive_user_s3_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.S3PathProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''User accounts whose documents should be indexed.

            :param one_drive_user_list: A list of users whose documents should be indexed. Specify the user names in email format, for example, ``username@tenantdomain`` . If you need to index the documents of more than 10 users, use the ``OneDriveUserS3Path`` field to specify the location of a file containing a list of users.
            :param one_drive_user_s3_path: The S3 bucket location of a file containing a list of users whose documents should be indexed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveusers.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                one_drive_users_property = kendra_mixins.CfnDataSourcePropsMixin.OneDriveUsersProperty(
                    one_drive_user_list=["oneDriveUserList"],
                    one_drive_user_s3_path=kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                        bucket="bucket",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5eeb64778818ddc81e60a09611edb17ce76a43674a47dd8ce6b7add627f09e4)
                check_type(argname="argument one_drive_user_list", value=one_drive_user_list, expected_type=type_hints["one_drive_user_list"])
                check_type(argname="argument one_drive_user_s3_path", value=one_drive_user_s3_path, expected_type=type_hints["one_drive_user_s3_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if one_drive_user_list is not None:
                self._values["one_drive_user_list"] = one_drive_user_list
            if one_drive_user_s3_path is not None:
                self._values["one_drive_user_s3_path"] = one_drive_user_s3_path

        @builtins.property
        def one_drive_user_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of users whose documents should be indexed.

            Specify the user names in email format, for example, ``username@tenantdomain`` . If you need to index the documents of more than 10 users, use the ``OneDriveUserS3Path`` field to specify the location of a file containing a list of users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveusers.html#cfn-kendra-datasource-onedriveusers-onedriveuserlist
            '''
            result = self._values.get("one_drive_user_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def one_drive_user_s3_path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.S3PathProperty"]]:
            '''The S3 bucket location of a file containing a list of users whose documents should be indexed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveusers.html#cfn-kendra-datasource-onedriveusers-onedriveusers3path
            '''
            result = self._values.get("one_drive_user_s3_path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.S3PathProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OneDriveUsersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ProxyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"credentials": "credentials", "host": "host", "port": "port"},
    )
    class ProxyConfigurationProperty:
        def __init__(
            self,
            *,
            credentials: typing.Optional[builtins.str] = None,
            host: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Provides the configuration information for a web proxy to connect to website hosts.

            :param credentials: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret. You create a secret to store your credentials in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ The credentials are optional. You use a secret if web proxy credentials are required to connect to a website host. Amazon Kendra currently support basic authentication to connect to a web proxy server. The secret stores your credentials.
            :param host: The name of the website host you want to connect to via a web proxy server. For example, the host name of https://a.example.com/page1.html is "a.example.com".
            :param port: The port number of the website host you want to connect to via a web proxy server. For example, the port for https://a.example.com/page1.html is 443, the standard port for HTTPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-proxyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                proxy_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ProxyConfigurationProperty(
                    credentials="credentials",
                    host="host",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24d90bb9d6def43faed1451329c30d6849549f34839313448422042eae6649bc)
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credentials is not None:
                self._values["credentials"] = credentials
            if host is not None:
                self._values["host"] = host
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def credentials(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret.

            You create a secret to store your credentials in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_

            The credentials are optional. You use a secret if web proxy credentials are required to connect to a website host. Amazon Kendra currently support basic authentication to connect to a web proxy server. The secret stores your credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-proxyconfiguration.html#cfn-kendra-datasource-proxyconfiguration-credentials
            '''
            result = self._values.get("credentials")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''The name of the website host you want to connect to via a web proxy server.

            For example, the host name of https://a.example.com/page1.html is "a.example.com".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-proxyconfiguration.html#cfn-kendra-datasource-proxyconfiguration-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number of the website host you want to connect to via a web proxy server.

            For example, the port for https://a.example.com/page1.html is 443, the standard port for HTTPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-proxyconfiguration.html#cfn-kendra-datasource-proxyconfiguration-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProxyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.S3DataSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_control_list_configuration": "accessControlListConfiguration",
            "bucket_name": "bucketName",
            "documents_metadata_configuration": "documentsMetadataConfiguration",
            "exclusion_patterns": "exclusionPatterns",
            "inclusion_patterns": "inclusionPatterns",
            "inclusion_prefixes": "inclusionPrefixes",
        },
    )
    class S3DataSourceConfigurationProperty:
        def __init__(
            self,
            *,
            access_control_list_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.AccessControlListConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            bucket_name: typing.Optional[builtins.str] = None,
            documents_metadata_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information to connect to an Amazon S3 bucket.

            :param access_control_list_configuration: Provides the path to the S3 bucket that contains the user context filtering files for the data source. For the format of the file, see `Access control for S3 data sources <https://docs.aws.amazon.com/kendra/latest/dg/s3-acl.html>`_ .
            :param bucket_name: The name of the bucket that contains the documents.
            :param documents_metadata_configuration: Specifies document metadata files that contain information such as the document access control information, source URI, document author, and custom attributes. Each metadata file contains metadata about a single document.
            :param exclusion_patterns: A list of glob patterns (patterns that can expand a wildcard pattern into a list of path names that match the given pattern) for certain file names and file types to exclude from your index. If a document matches both an inclusion and exclusion prefix or pattern, the exclusion prefix takes precendence and the document is not indexed. Examples of glob patterns include: - - /myapp/config/** —All files inside config directory. - *** /*.png* —All .png files in all directories. - *** /*.{png, ico, md}* —All .png, .ico or .md files in all directories. - - /myapp/src/** /*.ts* —All .ts files inside src directory (and all its subdirectories). - *** /!(*.module).ts* —All .ts files but not .module.ts - **.png , *.jpg* —All PNG and JPEG image files in a directory (files with the extensions .png and .jpg). - **internal** —All files in a directory that contain 'internal' in the file name, such as 'internal', 'internal_only', 'company_internal'. - *** /*internal** —All internal-related files in a directory and its subdirectories. For more examples, see `Use of Exclude and Include Filters <https://docs.aws.amazon.com/cli/latest/reference/s3/#use-of-exclude-and-include-filters>`_ in the AWS CLI Command Reference.
            :param inclusion_patterns: A list of glob patterns (patterns that can expand a wildcard pattern into a list of path names that match the given pattern) for certain file names and file types to include in your index. If a document matches both an inclusion and exclusion prefix or pattern, the exclusion prefix takes precendence and the document is not indexed. Examples of glob patterns include: - - /myapp/config/** —All files inside config directory. - *** /*.png* —All .png files in all directories. - *** /*.{png, ico, md}* —All .png, .ico or .md files in all directories. - - /myapp/src/** /*.ts* —All .ts files inside src directory (and all its subdirectories). - *** /!(*.module).ts* —All .ts files but not .module.ts - **.png , *.jpg* —All PNG and JPEG image files in a directory (files with the extensions .png and .jpg). - **internal** —All files in a directory that contain 'internal' in the file name, such as 'internal', 'internal_only', 'company_internal'. - *** /*internal** —All internal-related files in a directory and its subdirectories. For more examples, see `Use of Exclude and Include Filters <https://docs.aws.amazon.com/cli/latest/reference/s3/#use-of-exclude-and-include-filters>`_ in the AWS CLI Command Reference.
            :param inclusion_prefixes: A list of S3 prefixes for the documents that should be included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                s3_data_source_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.S3DataSourceConfigurationProperty(
                    access_control_list_configuration=kendra_mixins.CfnDataSourcePropsMixin.AccessControlListConfigurationProperty(
                        key_path="keyPath"
                    ),
                    bucket_name="bucketName",
                    documents_metadata_configuration=kendra_mixins.CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty(
                        s3_prefix="s3Prefix"
                    ),
                    exclusion_patterns=["exclusionPatterns"],
                    inclusion_patterns=["inclusionPatterns"],
                    inclusion_prefixes=["inclusionPrefixes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e7296df89874679585465a3fa2f116f8fa14c42256ab84fdc29000415b80443)
                check_type(argname="argument access_control_list_configuration", value=access_control_list_configuration, expected_type=type_hints["access_control_list_configuration"])
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument documents_metadata_configuration", value=documents_metadata_configuration, expected_type=type_hints["documents_metadata_configuration"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_control_list_configuration is not None:
                self._values["access_control_list_configuration"] = access_control_list_configuration
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if documents_metadata_configuration is not None:
                self._values["documents_metadata_configuration"] = documents_metadata_configuration
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if inclusion_prefixes is not None:
                self._values["inclusion_prefixes"] = inclusion_prefixes

        @builtins.property
        def access_control_list_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AccessControlListConfigurationProperty"]]:
            '''Provides the path to the S3 bucket that contains the user context filtering files for the data source.

            For the format of the file, see `Access control for S3 data sources <https://docs.aws.amazon.com/kendra/latest/dg/s3-acl.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-accesscontrollistconfiguration
            '''
            result = self._values.get("access_control_list_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.AccessControlListConfigurationProperty"]], result)

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The name of the bucket that contains the documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def documents_metadata_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty"]]:
            '''Specifies document metadata files that contain information such as the document access control information, source URI, document author, and custom attributes.

            Each metadata file contains metadata about a single document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-documentsmetadataconfiguration
            '''
            result = self._values.get("documents_metadata_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty"]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of glob patterns (patterns that can expand a wildcard pattern into a list of path names that match the given pattern) for certain file names and file types to exclude from your index.

            If a document matches both an inclusion and exclusion prefix or pattern, the exclusion prefix takes precendence and the document is not indexed. Examples of glob patterns include:

            -
              - /myapp/config/** —All files inside config directory.

            - *** /*.png* —All .png files in all directories.
            - *** /*.{png, ico, md}* —All .png, .ico or .md files in all directories.
            -
              - /myapp/src/** /*.ts* —All .ts files inside src directory (and all its subdirectories).

            - *** /!(*.module).ts* —All .ts files but not .module.ts
            - **.png , *.jpg* —All PNG and JPEG image files in a directory (files with the extensions .png and .jpg).
            - **internal** —All files in a directory that contain 'internal' in the file name, such as 'internal', 'internal_only', 'company_internal'.
            - *** /*internal** —All internal-related files in a directory and its subdirectories.

            For more examples, see `Use of Exclude and Include Filters <https://docs.aws.amazon.com/cli/latest/reference/s3/#use-of-exclude-and-include-filters>`_ in the AWS CLI Command Reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of glob patterns (patterns that can expand a wildcard pattern into a list of path names that match the given pattern) for certain file names and file types to include in your index.

            If a document matches both an inclusion and exclusion prefix or pattern, the exclusion prefix takes precendence and the document is not indexed. Examples of glob patterns include:

            -
              - /myapp/config/** —All files inside config directory.

            - *** /*.png* —All .png files in all directories.
            - *** /*.{png, ico, md}* —All .png, .ico or .md files in all directories.
            -
              - /myapp/src/** /*.ts* —All .ts files inside src directory (and all its subdirectories).

            - *** /!(*.module).ts* —All .ts files but not .module.ts
            - **.png , *.jpg* —All PNG and JPEG image files in a directory (files with the extensions .png and .jpg).
            - **internal** —All files in a directory that contain 'internal' in the file name, such as 'internal', 'internal_only', 'company_internal'.
            - *** /*internal** —All internal-related files in a directory and its subdirectories.

            For more examples, see `Use of Exclude and Include Filters <https://docs.aws.amazon.com/cli/latest/reference/s3/#use-of-exclude-and-include-filters>`_ in the AWS CLI Command Reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of S3 prefixes for the documents that should be included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-inclusionprefixes
            '''
            result = self._values.get("inclusion_prefixes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DataSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.S3PathProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3PathProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information required to find a specific file in an Amazon S3 bucket.

            :param bucket: The name of the S3 bucket that contains the file.
            :param key: The name of the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3path.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                s3_path_property = kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                    bucket="bucket",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b38e1d60ff130411d2fba82cf92f45c8ab7a0acd895e3b637b114ba12674655)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket that contains the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3path.html#cfn-kendra-datasource-s3path-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3path.html#cfn-kendra-datasource-s3path-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3PathProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
            "include_filter_types": "includeFilterTypes",
        },
    )
    class SalesforceChatterFeedConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: typing.Optional[builtins.str] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            include_filter_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration information for syncing a Salesforce chatter feed.

            The contents of the object comes from the Salesforce FeedItem table.

            :param document_data_field_name: The name of the column in the Salesforce FeedItem table that contains the content to index. Typically this is the ``Body`` column.
            :param document_title_field_name: The name of the column in the Salesforce FeedItem table that contains the title of the document. This is typically the ``Title`` column.
            :param field_mappings: Maps fields from a Salesforce chatter feed into Amazon Kendra index fields.
            :param include_filter_types: Filters the documents in the feed based on status of the user. When you specify ``ACTIVE_USERS`` only documents from users who have an active account are indexed. When you specify ``STANDARD_USER`` only documents for Salesforce standard users are documented. You can specify both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                salesforce_chatter_feed_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    include_filter_types=["includeFilterTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__daa2f6e990b9aaeeee27877cd5143ab1205e4a4a28c3ba364e2839582a22386d)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument include_filter_types", value=include_filter_types, expected_type=type_hints["include_filter_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_data_field_name is not None:
                self._values["document_data_field_name"] = document_data_field_name
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if include_filter_types is not None:
                self._values["include_filter_types"] = include_filter_types

        @builtins.property
        def document_data_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the column in the Salesforce FeedItem table that contains the content to index.

            Typically this is the ``Body`` column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html#cfn-kendra-datasource-salesforcechatterfeedconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the column in the Salesforce FeedItem table that contains the title of the document.

            This is typically the ``Title`` column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html#cfn-kendra-datasource-salesforcechatterfeedconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''Maps fields from a Salesforce chatter feed into Amazon Kendra index fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html#cfn-kendra-datasource-salesforcechatterfeedconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def include_filter_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Filters the documents in the feed based on status of the user.

            When you specify ``ACTIVE_USERS`` only documents from users who have an active account are indexed. When you specify ``STANDARD_USER`` only documents for Salesforce standard users are documented. You can specify both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html#cfn-kendra-datasource-salesforcechatterfeedconfiguration-includefiltertypes
            '''
            result = self._values.get("include_filter_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceChatterFeedConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.SalesforceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "chatter_feed_configuration": "chatterFeedConfiguration",
            "crawl_attachments": "crawlAttachments",
            "exclude_attachment_file_patterns": "excludeAttachmentFilePatterns",
            "include_attachment_file_patterns": "includeAttachmentFilePatterns",
            "knowledge_article_configuration": "knowledgeArticleConfiguration",
            "secret_arn": "secretArn",
            "server_url": "serverUrl",
            "standard_object_attachment_configuration": "standardObjectAttachmentConfiguration",
            "standard_object_configurations": "standardObjectConfigurations",
        },
    )
    class SalesforceConfigurationProperty:
        def __init__(
            self,
            *,
            chatter_feed_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            knowledge_article_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            server_url: typing.Optional[builtins.str] = None,
            standard_object_attachment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            standard_object_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides the configuration information to connect to Salesforce as your data source.

            :param chatter_feed_configuration: Configuration information for Salesforce chatter feeds.
            :param crawl_attachments: Indicates whether Amazon Kendra should index attachments to Salesforce objects.
            :param exclude_attachment_file_patterns: A list of regular expression patterns to exclude certain documents in your Salesforce. Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The pattern is applied to the name of the attached file.
            :param include_attachment_file_patterns: A list of regular expression patterns to include certain documents in your Salesforce. Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The pattern is applied to the name of the attached file.
            :param knowledge_article_configuration: Configuration information for the knowledge article types that Amazon Kendra indexes. Amazon Kendra indexes standard knowledge articles and the standard fields of knowledge articles, or the custom fields of custom knowledge articles, but not both.
            :param secret_arn: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the key/value pairs required to connect to your Salesforce instance. The secret must contain a JSON structure with the following keys: - authenticationUrl - The OAUTH endpoint that Amazon Kendra connects to get an OAUTH token. - consumerKey - The application public key generated when you created your Salesforce application. - consumerSecret - The application private key generated when you created your Salesforce application. - password - The password associated with the user logging in to the Salesforce instance. - securityToken - The token associated with the user logging in to the Salesforce instance. - username - The user name of the user logging in to the Salesforce instance.
            :param server_url: The instance URL for the Salesforce site that you want to index.
            :param standard_object_attachment_configuration: Configuration information for processing attachments to Salesforce standard objects.
            :param standard_object_configurations: Configuration of the Salesforce standard objects that Amazon Kendra indexes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                salesforce_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.SalesforceConfigurationProperty(
                    chatter_feed_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        include_filter_types=["includeFilterTypes"]
                    ),
                    crawl_attachments=False,
                    exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                    include_attachment_file_patterns=["includeAttachmentFilePatterns"],
                    knowledge_article_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty(
                        custom_knowledge_article_type_configurations=[kendra_mixins.CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )],
                            name="name"
                        )],
                        included_states=["includedStates"],
                        standard_knowledge_article_type_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                date_field_format="dateFieldFormat",
                                index_field_name="indexFieldName"
                            )]
                        )
                    ),
                    secret_arn="secretArn",
                    server_url="serverUrl",
                    standard_object_attachment_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty(
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    ),
                    standard_object_configurations=[kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__82e6cc6cf20308f4f59de5599bb24ea2f119044af4f04fd880bdb9e3e0e24f80)
                check_type(argname="argument chatter_feed_configuration", value=chatter_feed_configuration, expected_type=type_hints["chatter_feed_configuration"])
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
                check_type(argname="argument exclude_attachment_file_patterns", value=exclude_attachment_file_patterns, expected_type=type_hints["exclude_attachment_file_patterns"])
                check_type(argname="argument include_attachment_file_patterns", value=include_attachment_file_patterns, expected_type=type_hints["include_attachment_file_patterns"])
                check_type(argname="argument knowledge_article_configuration", value=knowledge_article_configuration, expected_type=type_hints["knowledge_article_configuration"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument server_url", value=server_url, expected_type=type_hints["server_url"])
                check_type(argname="argument standard_object_attachment_configuration", value=standard_object_attachment_configuration, expected_type=type_hints["standard_object_attachment_configuration"])
                check_type(argname="argument standard_object_configurations", value=standard_object_configurations, expected_type=type_hints["standard_object_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if chatter_feed_configuration is not None:
                self._values["chatter_feed_configuration"] = chatter_feed_configuration
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments
            if exclude_attachment_file_patterns is not None:
                self._values["exclude_attachment_file_patterns"] = exclude_attachment_file_patterns
            if include_attachment_file_patterns is not None:
                self._values["include_attachment_file_patterns"] = include_attachment_file_patterns
            if knowledge_article_configuration is not None:
                self._values["knowledge_article_configuration"] = knowledge_article_configuration
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if server_url is not None:
                self._values["server_url"] = server_url
            if standard_object_attachment_configuration is not None:
                self._values["standard_object_attachment_configuration"] = standard_object_attachment_configuration
            if standard_object_configurations is not None:
                self._values["standard_object_configurations"] = standard_object_configurations

        @builtins.property
        def chatter_feed_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty"]]:
            '''Configuration information for Salesforce chatter feeds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-chatterfeedconfiguration
            '''
            result = self._values.get("chatter_feed_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty"]], result)

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether Amazon Kendra should index attachments to Salesforce objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclude_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain documents in your Salesforce.

            Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The pattern is applied to the name of the attached file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-excludeattachmentfilepatterns
            '''
            result = self._values.get("exclude_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain documents in your Salesforce.

            Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The pattern is applied to the name of the attached file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-includeattachmentfilepatterns
            '''
            result = self._values.get("include_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def knowledge_article_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty"]]:
            '''Configuration information for the knowledge article types that Amazon Kendra indexes.

            Amazon Kendra indexes standard knowledge articles and the standard fields of knowledge articles, or the custom fields of custom knowledge articles, but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-knowledgearticleconfiguration
            '''
            result = self._values.get("knowledge_article_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty"]], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the key/value pairs required to connect to your Salesforce instance.

            The secret must contain a JSON structure with the following keys:

            - authenticationUrl - The OAUTH endpoint that Amazon Kendra connects to get an OAUTH token.
            - consumerKey - The application public key generated when you created your Salesforce application.
            - consumerSecret - The application private key generated when you created your Salesforce application.
            - password - The password associated with the user logging in to the Salesforce instance.
            - securityToken - The token associated with the user logging in to the Salesforce instance.
            - username - The user name of the user logging in to the Salesforce instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def server_url(self) -> typing.Optional[builtins.str]:
            '''The instance URL for the Salesforce site that you want to index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-serverurl
            '''
            result = self._values.get("server_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def standard_object_attachment_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty"]]:
            '''Configuration information for processing attachments to Salesforce standard objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-standardobjectattachmentconfiguration
            '''
            result = self._values.get("standard_object_attachment_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty"]], result)

        @builtins.property
        def standard_object_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty"]]]]:
            '''Configuration of the Salesforce standard objects that Amazon Kendra indexes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-standardobjectconfigurations
            '''
            result = self._values.get("standard_object_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
            "name": "name",
        },
    )
    class SalesforceCustomKnowledgeArticleTypeConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: typing.Optional[builtins.str] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information for indexing Salesforce custom articles.

            :param document_data_field_name: The name of the field in the custom knowledge article that contains the document data to index.
            :param document_title_field_name: The name of the field in the custom knowledge article that contains the document title.
            :param field_mappings: Maps attributes or field names of the custom knowledge article to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.
            :param name: The name of the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                salesforce_custom_knowledge_article_type_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a9215ee5a9b8b13c6cd2762d4dda6895d3a710c76014b32a5872536e6317007)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_data_field_name is not None:
                self._values["document_data_field_name"] = document_data_field_name
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def document_data_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the custom knowledge article that contains the document data to index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the custom knowledge article that contains the document title.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''Maps attributes or field names of the custom knowledge article to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceCustomKnowledgeArticleTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_knowledge_article_type_configurations": "customKnowledgeArticleTypeConfigurations",
            "included_states": "includedStates",
            "standard_knowledge_article_type_configuration": "standardKnowledgeArticleTypeConfiguration",
        },
    )
    class SalesforceKnowledgeArticleConfigurationProperty:
        def __init__(
            self,
            *,
            custom_knowledge_article_type_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            included_states: typing.Optional[typing.Sequence[builtins.str]] = None,
            standard_knowledge_article_type_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information for the knowledge article types that Amazon Kendra indexes.

            Amazon Kendra indexes standard knowledge articles and the standard fields of knowledge articles, or the custom fields of custom knowledge articles, but not both

            :param custom_knowledge_article_type_configurations: Configuration information for custom Salesforce knowledge articles.
            :param included_states: Specifies the document states that should be included when Amazon Kendra indexes knowledge articles. You must specify at least one state.
            :param standard_knowledge_article_type_configuration: Configuration information for standard Salesforce knowledge articles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceknowledgearticleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                salesforce_knowledge_article_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty(
                    custom_knowledge_article_type_configurations=[kendra_mixins.CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        name="name"
                    )],
                    included_states=["includedStates"],
                    standard_knowledge_article_type_configuration=kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f71b03883c18f0e607a1432e8dc32d1366a18e02c7af0be7ba6fbae6e46a08f)
                check_type(argname="argument custom_knowledge_article_type_configurations", value=custom_knowledge_article_type_configurations, expected_type=type_hints["custom_knowledge_article_type_configurations"])
                check_type(argname="argument included_states", value=included_states, expected_type=type_hints["included_states"])
                check_type(argname="argument standard_knowledge_article_type_configuration", value=standard_knowledge_article_type_configuration, expected_type=type_hints["standard_knowledge_article_type_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_knowledge_article_type_configurations is not None:
                self._values["custom_knowledge_article_type_configurations"] = custom_knowledge_article_type_configurations
            if included_states is not None:
                self._values["included_states"] = included_states
            if standard_knowledge_article_type_configuration is not None:
                self._values["standard_knowledge_article_type_configuration"] = standard_knowledge_article_type_configuration

        @builtins.property
        def custom_knowledge_article_type_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty"]]]]:
            '''Configuration information for custom Salesforce knowledge articles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceknowledgearticleconfiguration.html#cfn-kendra-datasource-salesforceknowledgearticleconfiguration-customknowledgearticletypeconfigurations
            '''
            result = self._values.get("custom_knowledge_article_type_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty"]]]], result)

        @builtins.property
        def included_states(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the document states that should be included when Amazon Kendra indexes knowledge articles.

            You must specify at least one state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceknowledgearticleconfiguration.html#cfn-kendra-datasource-salesforceknowledgearticleconfiguration-includedstates
            '''
            result = self._values.get("included_states")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def standard_knowledge_article_type_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty"]]:
            '''Configuration information for standard Salesforce knowledge articles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceknowledgearticleconfiguration.html#cfn-kendra-datasource-salesforceknowledgearticleconfiguration-standardknowledgearticletypeconfiguration
            '''
            result = self._values.get("standard_knowledge_article_type_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceKnowledgeArticleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
        },
    )
    class SalesforceStandardKnowledgeArticleTypeConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: typing.Optional[builtins.str] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides the configuration information for standard Salesforce knowledge articles.

            :param document_data_field_name: The name of the field that contains the document data to index.
            :param document_title_field_name: The name of the field that contains the document title.
            :param field_mappings: Maps attributes or field names of the knowledge article to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                salesforce_standard_knowledge_article_type_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5498d621932e8d77cab8018aeadc9467e4367a490b98b6eb6e1e7a94f5d22d4)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_data_field_name is not None:
                self._values["document_data_field_name"] = document_data_field_name
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings

        @builtins.property
        def document_data_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field that contains the document data to index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field that contains the document title.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''Maps attributes or field names of the knowledge article to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceStandardKnowledgeArticleTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
        },
    )
    class SalesforceStandardObjectAttachmentConfigurationProperty:
        def __init__(
            self,
            *,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides the configuration information for processing attachments to Salesforce standard objects.

            :param document_title_field_name: The name of the field used for the document title.
            :param field_mappings: One or more objects that map fields in attachments to Amazon Kendra index fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectattachmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                salesforce_standard_object_attachment_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty(
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4df9bf6ac661e5af4963b063df9703b3436445caff209aa715cd744c0581aa1)
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field used for the document title.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectattachmentconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectattachmentconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''One or more objects that map fields in attachments to Amazon Kendra index fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectattachmentconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectattachmentconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceStandardObjectAttachmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
            "name": "name",
        },
    )
    class SalesforceStandardObjectConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: typing.Optional[builtins.str] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies configuration information for indexing a single standard object.

            :param document_data_field_name: The name of the field in the standard object table that contains the document contents.
            :param document_title_field_name: The name of the field in the standard object table that contains the document title.
            :param field_mappings: Maps attributes or field names of the standard object to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.
            :param name: The name of the standard object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                salesforce_standard_object_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__462a440ff1838a79d0c83ca33abea3278dad67aee390b6f585eb170cfc4e6b03)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_data_field_name is not None:
                self._values["document_data_field_name"] = document_data_field_name
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def document_data_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the standard object table that contains the document contents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the standard object table that contains the document title.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''Maps attributes or field names of the standard object to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the standard object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceStandardObjectConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ServiceNowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_type": "authenticationType",
            "host_url": "hostUrl",
            "knowledge_article_configuration": "knowledgeArticleConfiguration",
            "secret_arn": "secretArn",
            "service_catalog_configuration": "serviceCatalogConfiguration",
            "service_now_build_version": "serviceNowBuildVersion",
        },
    )
    class ServiceNowConfigurationProperty:
        def __init__(
            self,
            *,
            authentication_type: typing.Optional[builtins.str] = None,
            host_url: typing.Optional[builtins.str] = None,
            knowledge_article_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            service_catalog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_now_build_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information to connect to ServiceNow as your data source.

            :param authentication_type: The type of authentication used to connect to the ServiceNow instance. If you choose ``HTTP_BASIC`` , Amazon Kendra is authenticated using the user name and password provided in the AWS Secrets Manager secret in the ``SecretArn`` field. If you choose ``OAUTH2`` , Amazon Kendra is authenticated using the credentials of client ID, client secret, user name and password. When you use ``OAUTH2`` authentication, you must generate a token and a client secret using the ServiceNow console. For more information, see `Using a ServiceNow data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-servicenow.html>`_ .
            :param host_url: The ServiceNow instance that the data source connects to. The host endpoint should look like the following: *{instance}.service-now.com.*
            :param knowledge_article_configuration: Configuration information for crawling knowledge articles in the ServiceNow site.
            :param secret_arn: The Amazon Resource Name (ARN) of the AWS Secrets Manager secret that contains the user name and password required to connect to the ServiceNow instance. You can also provide OAuth authentication credentials of user name, password, client ID, and client secret. For more information, see `Using a ServiceNow data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-servicenow.html>`_ .
            :param service_catalog_configuration: Configuration information for crawling service catalogs in the ServiceNow site.
            :param service_now_build_version: The identifier of the release that the ServiceNow host is running. If the host is not running the ``LONDON`` release, use ``OTHERS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                service_now_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ServiceNowConfigurationProperty(
                    authentication_type="authenticationType",
                    host_url="hostUrl",
                    knowledge_article_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty(
                        crawl_attachments=False,
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        filter_query="filterQuery",
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                    ),
                    secret_arn="secretArn",
                    service_catalog_configuration=kendra_mixins.CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty(
                        crawl_attachments=False,
                        document_data_field_name="documentDataFieldName",
                        document_title_field_name="documentTitleFieldName",
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            date_field_format="dateFieldFormat",
                            index_field_name="indexFieldName"
                        )],
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                    ),
                    service_now_build_version="serviceNowBuildVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f97a239a5d8ed2b11d778bae19ca451195623f6653a1400237c15e467caf6cdd)
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
                check_type(argname="argument host_url", value=host_url, expected_type=type_hints["host_url"])
                check_type(argname="argument knowledge_article_configuration", value=knowledge_article_configuration, expected_type=type_hints["knowledge_article_configuration"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument service_catalog_configuration", value=service_catalog_configuration, expected_type=type_hints["service_catalog_configuration"])
                check_type(argname="argument service_now_build_version", value=service_now_build_version, expected_type=type_hints["service_now_build_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_type is not None:
                self._values["authentication_type"] = authentication_type
            if host_url is not None:
                self._values["host_url"] = host_url
            if knowledge_article_configuration is not None:
                self._values["knowledge_article_configuration"] = knowledge_article_configuration
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if service_catalog_configuration is not None:
                self._values["service_catalog_configuration"] = service_catalog_configuration
            if service_now_build_version is not None:
                self._values["service_now_build_version"] = service_now_build_version

        @builtins.property
        def authentication_type(self) -> typing.Optional[builtins.str]:
            '''The type of authentication used to connect to the ServiceNow instance.

            If you choose ``HTTP_BASIC`` , Amazon Kendra is authenticated using the user name and password provided in the AWS Secrets Manager secret in the ``SecretArn`` field. If you choose ``OAUTH2`` , Amazon Kendra is authenticated using the credentials of client ID, client secret, user name and password.

            When you use ``OAUTH2`` authentication, you must generate a token and a client secret using the ServiceNow console. For more information, see `Using a ServiceNow data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-servicenow.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-authenticationtype
            '''
            result = self._values.get("authentication_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_url(self) -> typing.Optional[builtins.str]:
            '''The ServiceNow instance that the data source connects to.

            The host endpoint should look like the following: *{instance}.service-now.com.*

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-hosturl
            '''
            result = self._values.get("host_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def knowledge_article_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty"]]:
            '''Configuration information for crawling knowledge articles in the ServiceNow site.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-knowledgearticleconfiguration
            '''
            result = self._values.get("knowledge_article_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty"]], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Secrets Manager secret that contains the user name and password required to connect to the ServiceNow instance.

            You can also provide OAuth authentication credentials of user name, password, client ID, and client secret. For more information, see `Using a ServiceNow data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-servicenow.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_catalog_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty"]]:
            '''Configuration information for crawling service catalogs in the ServiceNow site.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-servicecatalogconfiguration
            '''
            result = self._values.get("service_catalog_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty"]], result)

        @builtins.property
        def service_now_build_version(self) -> typing.Optional[builtins.str]:
            '''The identifier of the release that the ServiceNow host is running.

            If the host is not running the ``LONDON`` release, use ``OTHERS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-servicenowbuildversion
            '''
            result = self._values.get("service_now_build_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crawl_attachments": "crawlAttachments",
            "document_data_field_name": "documentDataFieldName",
            "document_title_field_name": "documentTitleFieldName",
            "exclude_attachment_file_patterns": "excludeAttachmentFilePatterns",
            "field_mappings": "fieldMappings",
            "filter_query": "filterQuery",
            "include_attachment_file_patterns": "includeAttachmentFilePatterns",
        },
    )
    class ServiceNowKnowledgeArticleConfigurationProperty:
        def __init__(
            self,
            *,
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            document_data_field_name: typing.Optional[builtins.str] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            filter_query: typing.Optional[builtins.str] = None,
            include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information for crawling knowledge articles in the ServiceNow site.

            :param crawl_attachments: ``TRUE`` to index attachments to knowledge articles.
            :param document_data_field_name: The name of the ServiceNow field that is mapped to the index document contents field in the Amazon Kendra index.
            :param document_title_field_name: The name of the ServiceNow field that is mapped to the index document title field.
            :param exclude_attachment_file_patterns: A list of regular expression patterns applied to exclude certain knowledge article attachments. Attachments that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.
            :param field_mappings: Maps attributes or field names of knoweldge articles to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to ServiceNow fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The ServiceNow data source field names must exist in your ServiceNow custom metadata.
            :param filter_query: A query that selects the knowledge articles to index. The query can return articles from multiple knowledge bases, and the knowledge bases can be public or private. The query string must be one generated by the ServiceNow console. For more information, see `Specifying documents to index with a query <https://docs.aws.amazon.com/kendra/latest/dg/servicenow-query.html>`_ .
            :param include_attachment_file_patterns: A list of regular expression patterns applied to include knowledge article attachments. Attachments that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                service_now_knowledge_article_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty(
                    crawl_attachments=False,
                    document_data_field_name="documentDataFieldName",
                    document_title_field_name="documentTitleFieldName",
                    exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    filter_query="filterQuery",
                    include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bdc45f30c0387e397b7831a6b4d0989a844e9eb38a70ba84fc865e0e8cb18d78)
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument exclude_attachment_file_patterns", value=exclude_attachment_file_patterns, expected_type=type_hints["exclude_attachment_file_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument filter_query", value=filter_query, expected_type=type_hints["filter_query"])
                check_type(argname="argument include_attachment_file_patterns", value=include_attachment_file_patterns, expected_type=type_hints["include_attachment_file_patterns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments
            if document_data_field_name is not None:
                self._values["document_data_field_name"] = document_data_field_name
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if exclude_attachment_file_patterns is not None:
                self._values["exclude_attachment_file_patterns"] = exclude_attachment_file_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if filter_query is not None:
                self._values["filter_query"] = filter_query
            if include_attachment_file_patterns is not None:
                self._values["include_attachment_file_patterns"] = include_attachment_file_patterns

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to index attachments to knowledge articles.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def document_data_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the ServiceNow field that is mapped to the index document contents field in the Amazon Kendra index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the ServiceNow field that is mapped to the index document title field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns applied to exclude certain knowledge article attachments.

            Attachments that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-excludeattachmentfilepatterns
            '''
            result = self._values.get("exclude_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''Maps attributes or field names of knoweldge articles to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to ServiceNow fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The ServiceNow data source field names must exist in your ServiceNow custom metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def filter_query(self) -> typing.Optional[builtins.str]:
            '''A query that selects the knowledge articles to index.

            The query can return articles from multiple knowledge bases, and the knowledge bases can be public or private.

            The query string must be one generated by the ServiceNow console. For more information, see `Specifying documents to index with a query <https://docs.aws.amazon.com/kendra/latest/dg/servicenow-query.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-filterquery
            '''
            result = self._values.get("filter_query")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns applied to include knowledge article attachments.

            Attachments that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-includeattachmentfilepatterns
            '''
            result = self._values.get("include_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowKnowledgeArticleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crawl_attachments": "crawlAttachments",
            "document_data_field_name": "documentDataFieldName",
            "document_title_field_name": "documentTitleFieldName",
            "exclude_attachment_file_patterns": "excludeAttachmentFilePatterns",
            "field_mappings": "fieldMappings",
            "include_attachment_file_patterns": "includeAttachmentFilePatterns",
        },
    )
    class ServiceNowServiceCatalogConfigurationProperty:
        def __init__(
            self,
            *,
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            document_data_field_name: typing.Optional[builtins.str] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information for crawling service catalog items in the ServiceNow site.

            :param crawl_attachments: ``TRUE`` to index attachments to service catalog items.
            :param document_data_field_name: The name of the ServiceNow field that is mapped to the index document contents field in the Amazon Kendra index.
            :param document_title_field_name: The name of the ServiceNow field that is mapped to the index document title field.
            :param exclude_attachment_file_patterns: A list of regular expression patterns to exclude certain attachments of catalogs in your ServiceNow. Item that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index. The regex is applied to the file name of the attachment.
            :param field_mappings: Maps attributes or field names of catalogs to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to ServiceNow fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The ServiceNow data source field names must exist in your ServiceNow custom metadata.
            :param include_attachment_file_patterns: A list of regular expression patterns to include certain attachments of catalogs in your ServiceNow. Item that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index. The regex is applied to the file name of the attachment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                service_now_service_catalog_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty(
                    crawl_attachments=False,
                    document_data_field_name="documentDataFieldName",
                    document_title_field_name="documentTitleFieldName",
                    exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d6af40890c0c4f262b48d050f67eefd140c16a08359969db948a1fd9d8b18d3)
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument exclude_attachment_file_patterns", value=exclude_attachment_file_patterns, expected_type=type_hints["exclude_attachment_file_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument include_attachment_file_patterns", value=include_attachment_file_patterns, expected_type=type_hints["include_attachment_file_patterns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments
            if document_data_field_name is not None:
                self._values["document_data_field_name"] = document_data_field_name
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if exclude_attachment_file_patterns is not None:
                self._values["exclude_attachment_file_patterns"] = exclude_attachment_file_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if include_attachment_file_patterns is not None:
                self._values["include_attachment_file_patterns"] = include_attachment_file_patterns

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to index attachments to service catalog items.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def document_data_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the ServiceNow field that is mapped to the index document contents field in the Amazon Kendra index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the ServiceNow field that is mapped to the index document title field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain attachments of catalogs in your ServiceNow.

            Item that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            The regex is applied to the file name of the attachment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-excludeattachmentfilepatterns
            '''
            result = self._values.get("exclude_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''Maps attributes or field names of catalogs to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to ServiceNow fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The ServiceNow data source field names must exist in your ServiceNow custom metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def include_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain attachments of catalogs in your ServiceNow.

            Item that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            The regex is applied to the file name of the attachment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-includeattachmentfilepatterns
            '''
            result = self._values.get("include_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowServiceCatalogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.SharePointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crawl_attachments": "crawlAttachments",
            "disable_local_groups": "disableLocalGroups",
            "document_title_field_name": "documentTitleFieldName",
            "exclusion_patterns": "exclusionPatterns",
            "field_mappings": "fieldMappings",
            "inclusion_patterns": "inclusionPatterns",
            "secret_arn": "secretArn",
            "share_point_version": "sharePointVersion",
            "ssl_certificate_s3_path": "sslCertificateS3Path",
            "urls": "urls",
            "use_change_log": "useChangeLog",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class SharePointConfigurationProperty:
        def __init__(
            self,
            *,
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            disable_local_groups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            share_point_version: typing.Optional[builtins.str] = None,
            ssl_certificate_s3_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.S3PathProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            urls: typing.Optional[typing.Sequence[builtins.str]] = None,
            use_change_log: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information to connect to Microsoft SharePoint as your data source.

            :param crawl_attachments: ``TRUE`` to index document attachments.
            :param disable_local_groups: ``TRUE`` to disable local groups information.
            :param document_title_field_name: The Microsoft SharePoint attribute field that contains the title of the document.
            :param exclusion_patterns: A list of regular expression patterns. Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an exclusion pattern and an inclusion pattern, the document is not included in the index. The regex is applied to the display URL of the SharePoint document.
            :param field_mappings: A list of ``DataSourceToIndexFieldMapping`` objects that map Microsoft SharePoint attributes or fields to Amazon Kendra index fields. You must first create the index fields using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation before you map SharePoint attributes. For more information, see `Mapping Data Source Fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ .
            :param inclusion_patterns: A list of regular expression patterns to include certain documents in your SharePoint. Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The regex applies to the display URL of the SharePoint document.
            :param secret_arn: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password required to connect to the SharePoint instance. For more information, see `Microsoft SharePoint <https://docs.aws.amazon.com/kendra/latest/dg/data-source-sharepoint.html>`_ .
            :param share_point_version: The version of Microsoft SharePoint that you use.
            :param ssl_certificate_s3_path: Information required to find a specific file in an Amazon S3 bucket.
            :param urls: The Microsoft SharePoint site URLs for the documents you want to index.
            :param use_change_log: ``TRUE`` to use the SharePoint change log to determine which documents require updating in the index. Depending on the change log's size, it may take longer for Amazon Kendra to use the change log than to scan all of your documents in SharePoint.
            :param vpc_configuration: Provides information for connecting to an Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                share_point_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.SharePointConfigurationProperty(
                    crawl_attachments=False,
                    disable_local_groups=False,
                    document_title_field_name="documentTitleFieldName",
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    secret_arn="secretArn",
                    share_point_version="sharePointVersion",
                    ssl_certificate_s3_path=kendra_mixins.CfnDataSourcePropsMixin.S3PathProperty(
                        bucket="bucket",
                        key="key"
                    ),
                    urls=["urls"],
                    use_change_log=False,
                    vpc_configuration=kendra_mixins.CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3be79a905b606b16d3963ec36e8567f7075623000a2bbba0d649ae93c48ee5f)
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
                check_type(argname="argument disable_local_groups", value=disable_local_groups, expected_type=type_hints["disable_local_groups"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument share_point_version", value=share_point_version, expected_type=type_hints["share_point_version"])
                check_type(argname="argument ssl_certificate_s3_path", value=ssl_certificate_s3_path, expected_type=type_hints["ssl_certificate_s3_path"])
                check_type(argname="argument urls", value=urls, expected_type=type_hints["urls"])
                check_type(argname="argument use_change_log", value=use_change_log, expected_type=type_hints["use_change_log"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments
            if disable_local_groups is not None:
                self._values["disable_local_groups"] = disable_local_groups
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if share_point_version is not None:
                self._values["share_point_version"] = share_point_version
            if ssl_certificate_s3_path is not None:
                self._values["ssl_certificate_s3_path"] = ssl_certificate_s3_path
            if urls is not None:
                self._values["urls"] = urls
            if use_change_log is not None:
                self._values["use_change_log"] = use_change_log
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to index document attachments.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def disable_local_groups(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to disable local groups information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-disablelocalgroups
            '''
            result = self._values.get("disable_local_groups")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The Microsoft SharePoint attribute field that contains the title of the document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns.

            Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an exclusion pattern and an inclusion pattern, the document is not included in the index.

            The regex is applied to the display URL of the SharePoint document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''A list of ``DataSourceToIndexFieldMapping`` objects that map Microsoft SharePoint attributes or fields to Amazon Kendra index fields.

            You must first create the index fields using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation before you map SharePoint attributes. For more information, see `Mapping Data Source Fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain documents in your SharePoint.

            Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The regex applies to the display URL of the SharePoint document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password required to connect to the SharePoint instance.

            For more information, see `Microsoft SharePoint <https://docs.aws.amazon.com/kendra/latest/dg/data-source-sharepoint.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def share_point_version(self) -> typing.Optional[builtins.str]:
            '''The version of Microsoft SharePoint that you use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-sharepointversion
            '''
            result = self._values.get("share_point_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ssl_certificate_s3_path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.S3PathProperty"]]:
            '''Information required to find a specific file in an Amazon S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-sslcertificates3path
            '''
            result = self._values.get("ssl_certificate_s3_path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.S3PathProperty"]], result)

        @builtins.property
        def urls(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Microsoft SharePoint site URLs for the documents you want to index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-urls
            '''
            result = self._values.get("urls")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def use_change_log(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to use the SharePoint change log to determine which documents require updating in the index.

            Depending on the change log's size, it may take longer for Amazon Kendra to use the change log than to scan all of your documents in SharePoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-usechangelog
            '''
            result = self._values.get("use_change_log")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty"]]:
            '''Provides information for connecting to an Amazon VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SharePointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.SqlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "query_identifiers_enclosing_option": "queryIdentifiersEnclosingOption",
        },
    )
    class SqlConfigurationProperty:
        def __init__(
            self,
            *,
            query_identifiers_enclosing_option: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that configures Amazon Kendra to use a SQL database.

            :param query_identifiers_enclosing_option: Determines whether Amazon Kendra encloses SQL identifiers for tables and column names in double quotes (") when making a database query. You can set the value to ``DOUBLE_QUOTES`` or ``NONE`` . By default, Amazon Kendra passes SQL identifiers the way that they are entered into the data source configuration. It does not change the case of identifiers or enclose them in quotes. PostgreSQL internally converts uppercase characters to lower case characters in identifiers unless they are quoted. Choosing this option encloses identifiers in quotes so that PostgreSQL does not convert the character's case. For MySQL databases, you must enable the ansi_quotes option when you set this field to ``DOUBLE_QUOTES`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sqlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                sql_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.SqlConfigurationProperty(
                    query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec0ec6919af20b3ae18db779142356fd8b6e81861859a759fd87130e2cad0c43)
                check_type(argname="argument query_identifiers_enclosing_option", value=query_identifiers_enclosing_option, expected_type=type_hints["query_identifiers_enclosing_option"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if query_identifiers_enclosing_option is not None:
                self._values["query_identifiers_enclosing_option"] = query_identifiers_enclosing_option

        @builtins.property
        def query_identifiers_enclosing_option(self) -> typing.Optional[builtins.str]:
            '''Determines whether Amazon Kendra encloses SQL identifiers for tables and column names in double quotes (") when making a database query.

            You can set the value to ``DOUBLE_QUOTES`` or ``NONE`` .

            By default, Amazon Kendra passes SQL identifiers the way that they are entered into the data source configuration. It does not change the case of identifiers or enclose them in quotes.

            PostgreSQL internally converts uppercase characters to lower case characters in identifiers unless they are quoted. Choosing this option encloses identifiers in quotes so that PostgreSQL does not convert the character's case.

            For MySQL databases, you must enable the ansi_quotes option when you set this field to ``DOUBLE_QUOTES`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sqlconfiguration.html#cfn-kendra-datasource-sqlconfiguration-queryidentifiersenclosingoption
            '''
            result = self._values.get("query_identifiers_enclosing_option")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.TemplateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"template": "template"},
    )
    class TemplateConfigurationProperty:
        def __init__(self, *, template: typing.Optional[builtins.str] = None) -> None:
            '''Provides a template for the configuration information to connect to your data source.

            :param template: The template schema used for the data source, where templates schemas are supported. See `Data source template schemas <https://docs.aws.amazon.com/kendra/latest/dg/ds-schemas.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-templateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                template_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.TemplateConfigurationProperty(
                    template="template"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__412714ebe317eab4c8831768c6ef7b27275330743acef3efca1640de7032480c)
                check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if template is not None:
                self._values["template"] = template

        @builtins.property
        def template(self) -> typing.Optional[builtins.str]:
            '''The template schema used for the data source, where templates schemas are supported.

            See `Data source template schemas <https://docs.aws.amazon.com/kendra/latest/dg/ds-schemas.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-templateconfiguration.html#cfn-kendra-datasource-templateconfiguration-template
            '''
            result = self._values.get("template")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"basic_authentication": "basicAuthentication"},
    )
    class WebCrawlerAuthenticationConfigurationProperty:
        def __init__(
            self,
            *,
            basic_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides the configuration information to connect to websites that require user authentication.

            :param basic_authentication: The list of configuration information that's required to connect to and crawl a website host using basic authentication credentials. The list includes the name and port number of the website host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerauthenticationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                web_crawler_authentication_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty(
                    basic_authentication=[kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty(
                        credentials="credentials",
                        host="host",
                        port=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1b038c8d546495184ef4c44e3ec01e6d1b7cc7533d6d0f315372011a4ebf51f)
                check_type(argname="argument basic_authentication", value=basic_authentication, expected_type=type_hints["basic_authentication"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if basic_authentication is not None:
                self._values["basic_authentication"] = basic_authentication

        @builtins.property
        def basic_authentication(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty"]]]]:
            '''The list of configuration information that's required to connect to and crawl a website host using basic authentication credentials.

            The list includes the name and port number of the website host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerauthenticationconfiguration.html#cfn-kendra-datasource-webcrawlerauthenticationconfiguration-basicauthentication
            '''
            result = self._values.get("basic_authentication")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerAuthenticationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={"credentials": "credentials", "host": "host", "port": "port"},
    )
    class WebCrawlerBasicAuthenticationProperty:
        def __init__(
            self,
            *,
            credentials: typing.Optional[builtins.str] = None,
            host: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Provides the configuration information to connect to websites that require basic user authentication.

            :param credentials: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret. You create a secret to store your credentials in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ You use a secret if basic authentication credentials are required to connect to a website. The secret stores your credentials of user name and password.
            :param host: The name of the website host you want to connect to using authentication credentials. For example, the host name of https://a.example.com/page1.html is "a.example.com".
            :param port: The port number of the website host you want to connect to using authentication credentials. For example, the port for https://a.example.com/page1.html is 443, the standard port for HTTPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerbasicauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                web_crawler_basic_authentication_property = kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty(
                    credentials="credentials",
                    host="host",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60be6361f036a4a68326bf80908225737a129f3ec03298c60ef3be7f61b29945)
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credentials is not None:
                self._values["credentials"] = credentials
            if host is not None:
                self._values["host"] = host
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def credentials(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret.

            You create a secret to store your credentials in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_

            You use a secret if basic authentication credentials are required to connect to a website. The secret stores your credentials of user name and password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerbasicauthentication.html#cfn-kendra-datasource-webcrawlerbasicauthentication-credentials
            '''
            result = self._values.get("credentials")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''The name of the website host you want to connect to using authentication credentials.

            For example, the host name of https://a.example.com/page1.html is "a.example.com".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerbasicauthentication.html#cfn-kendra-datasource-webcrawlerbasicauthentication-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number of the website host you want to connect to using authentication credentials.

            For example, the port for https://a.example.com/page1.html is 443, the standard port for HTTPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerbasicauthentication.html#cfn-kendra-datasource-webcrawlerbasicauthentication-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerBasicAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.WebCrawlerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_configuration": "authenticationConfiguration",
            "crawl_depth": "crawlDepth",
            "max_content_size_per_page_in_mega_bytes": "maxContentSizePerPageInMegaBytes",
            "max_links_per_page": "maxLinksPerPage",
            "max_urls_per_minute_crawl_rate": "maxUrlsPerMinuteCrawlRate",
            "proxy_configuration": "proxyConfiguration",
            "url_exclusion_patterns": "urlExclusionPatterns",
            "url_inclusion_patterns": "urlInclusionPatterns",
            "urls": "urls",
        },
    )
    class WebCrawlerConfigurationProperty:
        def __init__(
            self,
            *,
            authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            crawl_depth: typing.Optional[jsii.Number] = None,
            max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
            max_links_per_page: typing.Optional[jsii.Number] = None,
            max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
            proxy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.ProxyConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            urls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.WebCrawlerUrlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information required for Amazon Kendra Web Crawler.

            :param authentication_configuration: Configuration information required to connect to websites using authentication. You can connect to websites using basic authentication of user name and password. You use a secret in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ to store your authentication credentials. You must provide the website host name and port number. For example, the host name of https://a.example.com/page1.html is "a.example.com" and the port is 443, the standard port for HTTPS.
            :param crawl_depth: The 'depth' or number of levels from the seed level to crawl. For example, the seed URL page is depth 1 and any hyperlinks on this page that are also crawled are depth 2.
            :param max_content_size_per_page_in_mega_bytes: The maximum size (in MB) of a web page or attachment to crawl. Files larger than this size (in MB) are skipped/not crawled. The default maximum size of a web page or attachment is set to 50 MB.
            :param max_links_per_page: The maximum number of URLs on a web page to include when crawling a website. This number is per web page. As a website’s web pages are crawled, any URLs the web pages link to are also crawled. URLs on a web page are crawled in order of appearance. The default maximum links per page is 100.
            :param max_urls_per_minute_crawl_rate: The maximum number of URLs crawled per website host per minute. A minimum of one URL is required. The default maximum number of URLs crawled per website host per minute is 300.
            :param proxy_configuration: Configuration information required to connect to your internal websites via a web proxy. You must provide the website host name and port number. For example, the host name of https://a.example.com/page1.html is "a.example.com" and the port is 443, the standard port for HTTPS. Web proxy credentials are optional and you can use them to connect to a web proxy server that requires basic authentication. To store web proxy credentials, you use a secret in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ .
            :param url_exclusion_patterns: A list of regular expression patterns to exclude certain URLs to crawl. URLs that match the patterns are excluded from the index. URLs that don't match the patterns are included in the index. If a URL matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the URL file isn't included in the index.
            :param url_inclusion_patterns: A list of regular expression patterns to include certain URLs to crawl. URLs that match the patterns are included in the index. URLs that don't match the patterns are excluded from the index. If a URL matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the URL file isn't included in the index.
            :param urls: Specifies the seed or starting point URLs of the websites or the sitemap URLs of the websites you want to crawl. You can include website subdomains. You can list up to 100 seed URLs and up to three sitemap URLs. You can only crawl websites that use the secure communication protocol, Hypertext Transfer Protocol Secure (HTTPS). If you receive an error when crawling a website, it could be that the website is blocked from crawling. *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use Amazon Kendra Web Crawler to index your own webpages, or webpages that you have authorization to index.*

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                web_crawler_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerConfigurationProperty(
                    authentication_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty(
                        basic_authentication=[kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty(
                            credentials="credentials",
                            host="host",
                            port=123
                        )]
                    ),
                    crawl_depth=123,
                    max_content_size_per_page_in_mega_bytes=123,
                    max_links_per_page=123,
                    max_urls_per_minute_crawl_rate=123,
                    proxy_configuration=kendra_mixins.CfnDataSourcePropsMixin.ProxyConfigurationProperty(
                        credentials="credentials",
                        host="host",
                        port=123
                    ),
                    url_exclusion_patterns=["urlExclusionPatterns"],
                    url_inclusion_patterns=["urlInclusionPatterns"],
                    urls=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerUrlsProperty(
                        seed_url_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty(
                            seed_urls=["seedUrls"],
                            web_crawler_mode="webCrawlerMode"
                        ),
                        site_maps_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty(
                            site_maps=["siteMaps"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16375405779a14946b9fbe2f956a4026ba75c8539b9d6a16e43684670a3f32dc)
                check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                check_type(argname="argument crawl_depth", value=crawl_depth, expected_type=type_hints["crawl_depth"])
                check_type(argname="argument max_content_size_per_page_in_mega_bytes", value=max_content_size_per_page_in_mega_bytes, expected_type=type_hints["max_content_size_per_page_in_mega_bytes"])
                check_type(argname="argument max_links_per_page", value=max_links_per_page, expected_type=type_hints["max_links_per_page"])
                check_type(argname="argument max_urls_per_minute_crawl_rate", value=max_urls_per_minute_crawl_rate, expected_type=type_hints["max_urls_per_minute_crawl_rate"])
                check_type(argname="argument proxy_configuration", value=proxy_configuration, expected_type=type_hints["proxy_configuration"])
                check_type(argname="argument url_exclusion_patterns", value=url_exclusion_patterns, expected_type=type_hints["url_exclusion_patterns"])
                check_type(argname="argument url_inclusion_patterns", value=url_inclusion_patterns, expected_type=type_hints["url_inclusion_patterns"])
                check_type(argname="argument urls", value=urls, expected_type=type_hints["urls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_configuration is not None:
                self._values["authentication_configuration"] = authentication_configuration
            if crawl_depth is not None:
                self._values["crawl_depth"] = crawl_depth
            if max_content_size_per_page_in_mega_bytes is not None:
                self._values["max_content_size_per_page_in_mega_bytes"] = max_content_size_per_page_in_mega_bytes
            if max_links_per_page is not None:
                self._values["max_links_per_page"] = max_links_per_page
            if max_urls_per_minute_crawl_rate is not None:
                self._values["max_urls_per_minute_crawl_rate"] = max_urls_per_minute_crawl_rate
            if proxy_configuration is not None:
                self._values["proxy_configuration"] = proxy_configuration
            if url_exclusion_patterns is not None:
                self._values["url_exclusion_patterns"] = url_exclusion_patterns
            if url_inclusion_patterns is not None:
                self._values["url_inclusion_patterns"] = url_inclusion_patterns
            if urls is not None:
                self._values["urls"] = urls

        @builtins.property
        def authentication_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty"]]:
            '''Configuration information required to connect to websites using authentication.

            You can connect to websites using basic authentication of user name and password. You use a secret in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ to store your authentication credentials.

            You must provide the website host name and port number. For example, the host name of https://a.example.com/page1.html is "a.example.com" and the port is 443, the standard port for HTTPS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-authenticationconfiguration
            '''
            result = self._values.get("authentication_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty"]], result)

        @builtins.property
        def crawl_depth(self) -> typing.Optional[jsii.Number]:
            '''The 'depth' or number of levels from the seed level to crawl.

            For example, the seed URL page is depth 1 and any hyperlinks on this page that are also crawled are depth 2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-crawldepth
            '''
            result = self._values.get("crawl_depth")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_content_size_per_page_in_mega_bytes(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The maximum size (in MB) of a web page or attachment to crawl.

            Files larger than this size (in MB) are skipped/not crawled.

            The default maximum size of a web page or attachment is set to 50 MB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-maxcontentsizeperpageinmegabytes
            '''
            result = self._values.get("max_content_size_per_page_in_mega_bytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_links_per_page(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of URLs on a web page to include when crawling a website.

            This number is per web page.

            As a website’s web pages are crawled, any URLs the web pages link to are also crawled. URLs on a web page are crawled in order of appearance.

            The default maximum links per page is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-maxlinksperpage
            '''
            result = self._values.get("max_links_per_page")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_urls_per_minute_crawl_rate(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of URLs crawled per website host per minute.

            A minimum of one URL is required.

            The default maximum number of URLs crawled per website host per minute is 300.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-maxurlsperminutecrawlrate
            '''
            result = self._values.get("max_urls_per_minute_crawl_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def proxy_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ProxyConfigurationProperty"]]:
            '''Configuration information required to connect to your internal websites via a web proxy.

            You must provide the website host name and port number. For example, the host name of https://a.example.com/page1.html is "a.example.com" and the port is 443, the standard port for HTTPS.

            Web proxy credentials are optional and you can use them to connect to a web proxy server that requires basic authentication. To store web proxy credentials, you use a secret in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-proxyconfiguration
            '''
            result = self._values.get("proxy_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.ProxyConfigurationProperty"]], result)

        @builtins.property
        def url_exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain URLs to crawl.

            URLs that match the patterns are excluded from the index. URLs that don't match the patterns are included in the index. If a URL matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the URL file isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-urlexclusionpatterns
            '''
            result = self._values.get("url_exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def url_inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain URLs to crawl.

            URLs that match the patterns are included in the index. URLs that don't match the patterns are excluded from the index. If a URL matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the URL file isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-urlinclusionpatterns
            '''
            result = self._values.get("url_inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def urls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerUrlsProperty"]]:
            '''Specifies the seed or starting point URLs of the websites or the sitemap URLs of the websites you want to crawl.

            You can include website subdomains. You can list up to 100 seed URLs and up to three sitemap URLs.

            You can only crawl websites that use the secure communication protocol, Hypertext Transfer Protocol Secure (HTTPS). If you receive an error when crawling a website, it could be that the website is blocked from crawling.

            *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use Amazon Kendra Web Crawler to index your own webpages, or webpages that you have authorization to index.*

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-urls
            '''
            result = self._values.get("urls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerUrlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"seed_urls": "seedUrls", "web_crawler_mode": "webCrawlerMode"},
    )
    class WebCrawlerSeedUrlConfigurationProperty:
        def __init__(
            self,
            *,
            seed_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
            web_crawler_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information of the seed or starting point URLs to crawl.

            *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use the Amazon Kendra web crawler to index your own webpages, or webpages that you have authorization to index.*

            :param seed_urls: The list of seed or starting point URLs of the websites you want to crawl. The list can include a maximum of 100 seed URLs.
            :param web_crawler_mode: You can choose one of the following modes:. - ``HOST_ONLY`` —crawl only the website host names. For example, if the seed URL is "abc.example.com", then only URLs with host name "abc.example.com" are crawled. - ``SUBDOMAINS`` —crawl the website host names with subdomains. For example, if the seed URL is "abc.example.com", then "a.abc.example.com" and "b.abc.example.com" are also crawled. - ``EVERYTHING`` —crawl the website host names with subdomains and other domains that the web pages link to. The default mode is set to ``HOST_ONLY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerseedurlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                web_crawler_seed_url_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty(
                    seed_urls=["seedUrls"],
                    web_crawler_mode="webCrawlerMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__530bed823bedc075927aa8bcb246001bf90584abaed24dabfda9743932485964)
                check_type(argname="argument seed_urls", value=seed_urls, expected_type=type_hints["seed_urls"])
                check_type(argname="argument web_crawler_mode", value=web_crawler_mode, expected_type=type_hints["web_crawler_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if seed_urls is not None:
                self._values["seed_urls"] = seed_urls
            if web_crawler_mode is not None:
                self._values["web_crawler_mode"] = web_crawler_mode

        @builtins.property
        def seed_urls(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of seed or starting point URLs of the websites you want to crawl.

            The list can include a maximum of 100 seed URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerseedurlconfiguration.html#cfn-kendra-datasource-webcrawlerseedurlconfiguration-seedurls
            '''
            result = self._values.get("seed_urls")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def web_crawler_mode(self) -> typing.Optional[builtins.str]:
            '''You can choose one of the following modes:.

            - ``HOST_ONLY`` —crawl only the website host names. For example, if the seed URL is "abc.example.com", then only URLs with host name "abc.example.com" are crawled.
            - ``SUBDOMAINS`` —crawl the website host names with subdomains. For example, if the seed URL is "abc.example.com", then "a.abc.example.com" and "b.abc.example.com" are also crawled.
            - ``EVERYTHING`` —crawl the website host names with subdomains and other domains that the web pages link to.

            The default mode is set to ``HOST_ONLY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerseedurlconfiguration.html#cfn-kendra-datasource-webcrawlerseedurlconfiguration-webcrawlermode
            '''
            result = self._values.get("web_crawler_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerSeedUrlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"site_maps": "siteMaps"},
    )
    class WebCrawlerSiteMapsConfigurationProperty:
        def __init__(
            self,
            *,
            site_maps: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information of the sitemap URLs to crawl.

            *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use the Amazon Kendra web crawler to index your own webpages, or webpages that you have authorization to index.*

            :param site_maps: The list of sitemap URLs of the websites you want to crawl. The list can include a maximum of three sitemap URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlersitemapsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                web_crawler_site_maps_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty(
                    site_maps=["siteMaps"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2dd291d43fb1ed33ba5cac71c44300497086d8e53229da033c7e8ddf517e7a26)
                check_type(argname="argument site_maps", value=site_maps, expected_type=type_hints["site_maps"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if site_maps is not None:
                self._values["site_maps"] = site_maps

        @builtins.property
        def site_maps(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of sitemap URLs of the websites you want to crawl.

            The list can include a maximum of three sitemap URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlersitemapsconfiguration.html#cfn-kendra-datasource-webcrawlersitemapsconfiguration-sitemaps
            '''
            result = self._values.get("site_maps")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerSiteMapsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.WebCrawlerUrlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "seed_url_configuration": "seedUrlConfiguration",
            "site_maps_configuration": "siteMapsConfiguration",
        },
    )
    class WebCrawlerUrlsProperty:
        def __init__(
            self,
            *,
            seed_url_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            site_maps_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the seed or starting point URLs of the websites or the sitemap URLs of the websites you want to crawl.

            You can include website subdomains. You can list up to 100 seed URLs and up to three sitemap URLs.

            You can only crawl websites that use the secure communication protocol, Hypertext Transfer Protocol Secure (HTTPS). If you receive an error when crawling a website, it could be that the website is blocked from crawling.

            *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use the Amazon Kendra web crawler to index your own webpages, or webpages that you have authorization to index.*

            :param seed_url_configuration: Configuration of the seed or starting point URLs of the websites you want to crawl. You can choose to crawl only the website host names, or the website host names with subdomains, or the website host names with subdomains and other domains that the web pages link to. You can list up to 100 seed URLs.
            :param site_maps_configuration: Configuration of the sitemap URLs of the websites you want to crawl. Only URLs belonging to the same website host names are crawled. You can list up to three sitemap URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerurls.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                web_crawler_urls_property = kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerUrlsProperty(
                    seed_url_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty(
                        seed_urls=["seedUrls"],
                        web_crawler_mode="webCrawlerMode"
                    ),
                    site_maps_configuration=kendra_mixins.CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty(
                        site_maps=["siteMaps"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2015d42cb5a352a099b27101af2cc8c83bfef53d22bef92c780c93afd30aba6)
                check_type(argname="argument seed_url_configuration", value=seed_url_configuration, expected_type=type_hints["seed_url_configuration"])
                check_type(argname="argument site_maps_configuration", value=site_maps_configuration, expected_type=type_hints["site_maps_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if seed_url_configuration is not None:
                self._values["seed_url_configuration"] = seed_url_configuration
            if site_maps_configuration is not None:
                self._values["site_maps_configuration"] = site_maps_configuration

        @builtins.property
        def seed_url_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty"]]:
            '''Configuration of the seed or starting point URLs of the websites you want to crawl.

            You can choose to crawl only the website host names, or the website host names with subdomains, or the website host names with subdomains and other domains that the web pages link to.

            You can list up to 100 seed URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerurls.html#cfn-kendra-datasource-webcrawlerurls-seedurlconfiguration
            '''
            result = self._values.get("seed_url_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty"]], result)

        @builtins.property
        def site_maps_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty"]]:
            '''Configuration of the sitemap URLs of the websites you want to crawl.

            Only URLs belonging to the same website host names are crawled. You can list up to three sitemap URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerurls.html#cfn-kendra-datasource-webcrawlerurls-sitemapsconfiguration
            '''
            result = self._values.get("site_maps_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerUrlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnDataSourcePropsMixin.WorkDocsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crawl_comments": "crawlComments",
            "exclusion_patterns": "exclusionPatterns",
            "field_mappings": "fieldMappings",
            "inclusion_patterns": "inclusionPatterns",
            "organization_id": "organizationId",
            "use_change_log": "useChangeLog",
        },
    )
    class WorkDocsConfigurationProperty:
        def __init__(
            self,
            *,
            crawl_comments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            organization_id: typing.Optional[builtins.str] = None,
            use_change_log: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides the configuration information to connect to WorkDocs as your data source.

            WorkDocs connector is available in Oregon, North Virginia, Sydney, Singapore and Ireland regions.

            :param crawl_comments: ``TRUE`` to include comments on documents in your index. Including comments in your index means each comment is a document that can be searched on. The default is set to ``FALSE`` .
            :param exclusion_patterns: A list of regular expression patterns to exclude certain files in your WorkDocs site repository. Files that match the patterns are excluded from the index. Files that don’t match the patterns are included in the index. If a file matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the file isn't included in the index.
            :param field_mappings: A list of ``DataSourceToIndexFieldMapping`` objects that map WorkDocs data source attributes or field names to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to WorkDocs fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The WorkDocs data source field names must exist in your WorkDocs custom metadata.
            :param inclusion_patterns: A list of regular expression patterns to include certain files in your WorkDocs site repository. Files that match the patterns are included in the index. Files that don't match the patterns are excluded from the index. If a file matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the file isn't included in the index.
            :param organization_id: The identifier of the directory corresponding to your WorkDocs site repository. You can find the organization ID in the `Directory Service <https://docs.aws.amazon.com/directoryservicev2/>`_ by going to *Active Directory* , then *Directories* . Your WorkDocs site directory has an ID, which is the organization ID. You can also set up a new WorkDocs directory in the Directory Service console and enable a WorkDocs site for the directory in the WorkDocs console.
            :param use_change_log: ``TRUE`` to use the WorkDocs change log to determine which documents require updating in the index. Depending on the change log's size, it may take longer for Amazon Kendra to use the change log than to scan all of your documents in WorkDocs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                work_docs_configuration_property = kendra_mixins.CfnDataSourcePropsMixin.WorkDocsConfigurationProperty(
                    crawl_comments=False,
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra_mixins.CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        date_field_format="dateFieldFormat",
                        index_field_name="indexFieldName"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    organization_id="organizationId",
                    use_change_log=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4470f4517a7511e09624d9470b61445464e73893c9dff86e7cb71be1b338065)
                check_type(argname="argument crawl_comments", value=crawl_comments, expected_type=type_hints["crawl_comments"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
                check_type(argname="argument use_change_log", value=use_change_log, expected_type=type_hints["use_change_log"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crawl_comments is not None:
                self._values["crawl_comments"] = crawl_comments
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if organization_id is not None:
                self._values["organization_id"] = organization_id
            if use_change_log is not None:
                self._values["use_change_log"] = use_change_log

        @builtins.property
        def crawl_comments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to include comments on documents in your index.

            Including comments in your index means each comment is a document that can be searched on.

            The default is set to ``FALSE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-crawlcomments
            '''
            result = self._values.get("crawl_comments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain files in your WorkDocs site repository.

            Files that match the patterns are excluded from the index. Files that don’t match the patterns are included in the index. If a file matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the file isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]]:
            '''A list of ``DataSourceToIndexFieldMapping`` objects that map WorkDocs data source attributes or field names to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to WorkDocs fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The WorkDocs data source field names must exist in your WorkDocs custom metadata.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty"]]]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain files in your WorkDocs site repository.

            Files that match the patterns are included in the index. Files that don't match the patterns are excluded from the index. If a file matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the file isn't included in the index.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def organization_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the directory corresponding to your WorkDocs site repository.

            You can find the organization ID in the `Directory Service <https://docs.aws.amazon.com/directoryservicev2/>`_ by going to *Active Directory* , then *Directories* . Your WorkDocs site directory has an ID, which is the organization ID. You can also set up a new WorkDocs directory in the Directory Service console and enable a WorkDocs site for the directory in the WorkDocs console.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-organizationid
            '''
            result = self._values.get("organization_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_change_log(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``TRUE`` to use the WorkDocs change log to determine which documents require updating in the index.

            Depending on the change log's size, it may take longer for Amazon Kendra to use the change log than to scan all of your documents in WorkDocs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-usechangelog
            '''
            result = self._values.get("use_change_log")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkDocsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnFaqMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "file_format": "fileFormat",
        "index_id": "indexId",
        "language_code": "languageCode",
        "name": "name",
        "role_arn": "roleArn",
        "s3_path": "s3Path",
        "tags": "tags",
    },
)
class CfnFaqMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        file_format: typing.Optional[builtins.str] = None,
        index_id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        s3_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFaqPropsMixin.S3PathProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFaqPropsMixin.

        :param description: A description for the FAQ.
        :param file_format: The format of the input file. You can choose between a basic CSV format, a CSV format that includes customs attributes in a header, and a JSON format that includes custom attributes. The format must match the format of the file stored in the S3 bucket identified in the S3Path parameter. Valid values are: - ``CSV`` - ``CSV_WITH_HEADER`` - ``JSON``
        :param index_id: The identifier of the index that contains the FAQ.
        :param language_code: The code for a language. This shows a supported language for the FAQ document as part of the summary information for FAQs. English is supported by default. For more information on supported languages, including their codes, see `Adding documents in languages other than English <https://docs.aws.amazon.com/kendra/latest/dg/in-adding-languages.html>`_ .
        :param name: The name that you assigned the FAQ when you created or updated the FAQ.
        :param role_arn: The Amazon Resource Name (ARN) of a role with permission to access the S3 bucket that contains the FAQ.
        :param s3_path: The Amazon Simple Storage Service (Amazon S3) location of the FAQ input data.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
            
            cfn_faq_mixin_props = kendra_mixins.CfnFaqMixinProps(
                description="description",
                file_format="fileFormat",
                index_id="indexId",
                language_code="languageCode",
                name="name",
                role_arn="roleArn",
                s3_path=kendra_mixins.CfnFaqPropsMixin.S3PathProperty(
                    bucket="bucket",
                    key="key"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8182503e3dd74b6ea13c394076efca6b3fd80fdc2063adf75db56068b1f7ca2)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument s3_path", value=s3_path, expected_type=type_hints["s3_path"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if file_format is not None:
            self._values["file_format"] = file_format
        if index_id is not None:
            self._values["index_id"] = index_id
        if language_code is not None:
            self._values["language_code"] = language_code
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if s3_path is not None:
            self._values["s3_path"] = s3_path
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the FAQ.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the input file.

        You can choose between a basic CSV format, a CSV format that includes customs attributes in a header, and a JSON format that includes custom attributes.

        The format must match the format of the file stored in the S3 bucket identified in the S3Path parameter.

        Valid values are:

        - ``CSV``
        - ``CSV_WITH_HEADER``
        - ``JSON``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-fileformat
        '''
        result = self._values.get("file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the index that contains the FAQ.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-indexid
        '''
        result = self._values.get("index_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The code for a language.

        This shows a supported language for the FAQ document as part of the summary information for FAQs. English is supported by default. For more information on supported languages, including their codes, see `Adding documents in languages other than English <https://docs.aws.amazon.com/kendra/latest/dg/in-adding-languages.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-languagecode
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name that you assigned the FAQ when you created or updated the FAQ.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a role with permission to access the S3 bucket that contains the FAQ.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_path(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFaqPropsMixin.S3PathProperty"]]:
        '''The Amazon Simple Storage Service (Amazon S3) location of the FAQ input data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-s3path
        '''
        result = self._values.get("s3_path")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFaqPropsMixin.S3PathProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFaqMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFaqPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnFaqPropsMixin",
):
    '''Creates an new set of frequently asked question (FAQ) questions and answers.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html
    :cloudformationResource: AWS::Kendra::Faq
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
        
        cfn_faq_props_mixin = kendra_mixins.CfnFaqPropsMixin(kendra_mixins.CfnFaqMixinProps(
            description="description",
            file_format="fileFormat",
            index_id="indexId",
            language_code="languageCode",
            name="name",
            role_arn="roleArn",
            s3_path=kendra_mixins.CfnFaqPropsMixin.S3PathProperty(
                bucket="bucket",
                key="key"
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
        props: typing.Union[CfnFaqMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Kendra::Faq``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ee7a5900ed89cab6a3965c1ae35c1d180cc170d89893b00a950237f36b9452)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0848e09f4c78f09c4c2c46e2daed5c6237786721d934c09c49a119ca0fdbb68)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca73a9c9aa275bb6dbef86530eed5e86f88d52f0acd0940f4bc7845d537fa308)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFaqMixinProps:
        return typing.cast(CfnFaqMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnFaqPropsMixin.S3PathProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3PathProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information required to find a specific file in an Amazon S3 bucket.

            :param bucket: The name of the S3 bucket that contains the file.
            :param key: The name of the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-faq-s3path.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                s3_path_property = kendra_mixins.CfnFaqPropsMixin.S3PathProperty(
                    bucket="bucket",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6821bfd953c0dde3439ca0cbcfd93f694e271a6a720d07dfaf52ac8d3eca5cb5)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket that contains the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-faq-s3path.html#cfn-kendra-faq-s3path-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-faq-s3path.html#cfn-kendra-faq-s3path-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3PathProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_units": "capacityUnits",
        "description": "description",
        "document_metadata_configurations": "documentMetadataConfigurations",
        "edition": "edition",
        "name": "name",
        "role_arn": "roleArn",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "tags": "tags",
        "user_context_policy": "userContextPolicy",
        "user_token_configurations": "userTokenConfigurations",
    },
)
class CfnIndexMixinProps:
    def __init__(
        self,
        *,
        capacity_units: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.CapacityUnitsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        document_metadata_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.DocumentMetadataConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        edition: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.ServerSideEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_context_policy: typing.Optional[builtins.str] = None,
        user_token_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.UserTokenConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnIndexPropsMixin.

        :param capacity_units: Specifies additional capacity units configured for your Enterprise Edition index. You can add and remove capacity units to fit your usage requirements.
        :param description: A description for the index.
        :param document_metadata_configurations: Specifies the properties of an index field. You can add either a custom or a built-in field. You can add and remove built-in fields at any time. When a built-in field is removed it's configuration reverts to the default for the field. Custom fields can't be removed from an index after they are added.
        :param edition: Indicates whether the index is a Enterprise Edition index, a Developer Edition index, or a GenAI Enterprise Edition index.
        :param name: The name of the index.
        :param role_arn: An IAM role that gives Amazon Kendra permissions to access your Amazon CloudWatch logs and metrics. This is also the role used when you use the `BatchPutDocument <https://docs.aws.amazon.com/kendra/latest/dg/BatchPutDocument.html>`_ operation to index documents from an Amazon S3 bucket.
        :param server_side_encryption_configuration: The identifier of the AWS KMS customer managed key (CMK) to use to encrypt data indexed by Amazon Kendra. Amazon Kendra doesn't support asymmetric CMKs.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param user_context_policy: The user context policy. ATTRIBUTE_FILTER - All indexed content is searchable and displayable for all users. If you want to filter search results on user context, you can use the attribute filters of ``_user_id`` and ``_group_ids`` or you can provide user and group information in ``UserContext`` . USER_TOKEN - Enables token-based user access control to filter search results on user context. All documents with no access control and all documents accessible to the user will be searchable and displayable.
        :param user_token_configurations: Defines the type of user token used for the index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
            
            cfn_index_mixin_props = kendra_mixins.CfnIndexMixinProps(
                capacity_units=kendra_mixins.CfnIndexPropsMixin.CapacityUnitsConfigurationProperty(
                    query_capacity_units=123,
                    storage_capacity_units=123
                ),
                description="description",
                document_metadata_configurations=[kendra_mixins.CfnIndexPropsMixin.DocumentMetadataConfigurationProperty(
                    name="name",
                    relevance=kendra_mixins.CfnIndexPropsMixin.RelevanceProperty(
                        duration="duration",
                        freshness=False,
                        importance=123,
                        rank_order="rankOrder",
                        value_importance_items=[kendra_mixins.CfnIndexPropsMixin.ValueImportanceItemProperty(
                            key="key",
                            value=123
                        )]
                    ),
                    search=kendra_mixins.CfnIndexPropsMixin.SearchProperty(
                        displayable=False,
                        facetable=False,
                        searchable=False,
                        sortable=False
                    ),
                    type="type"
                )],
                edition="edition",
                name="name",
                role_arn="roleArn",
                server_side_encryption_configuration=kendra_mixins.CfnIndexPropsMixin.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_context_policy="userContextPolicy",
                user_token_configurations=[kendra_mixins.CfnIndexPropsMixin.UserTokenConfigurationProperty(
                    json_token_type_configuration=kendra_mixins.CfnIndexPropsMixin.JsonTokenTypeConfigurationProperty(
                        group_attribute_field="groupAttributeField",
                        user_name_attribute_field="userNameAttributeField"
                    ),
                    jwt_token_type_configuration=kendra_mixins.CfnIndexPropsMixin.JwtTokenTypeConfigurationProperty(
                        claim_regex="claimRegex",
                        group_attribute_field="groupAttributeField",
                        issuer="issuer",
                        key_location="keyLocation",
                        secret_manager_arn="secretManagerArn",
                        url="url",
                        user_name_attribute_field="userNameAttributeField"
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dacaddcf70331f910505ece8620a665ce2b8641e7cba5da4ecc76cb52f7136)
            check_type(argname="argument capacity_units", value=capacity_units, expected_type=type_hints["capacity_units"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument document_metadata_configurations", value=document_metadata_configurations, expected_type=type_hints["document_metadata_configurations"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_context_policy", value=user_context_policy, expected_type=type_hints["user_context_policy"])
            check_type(argname="argument user_token_configurations", value=user_token_configurations, expected_type=type_hints["user_token_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity_units is not None:
            self._values["capacity_units"] = capacity_units
        if description is not None:
            self._values["description"] = description
        if document_metadata_configurations is not None:
            self._values["document_metadata_configurations"] = document_metadata_configurations
        if edition is not None:
            self._values["edition"] = edition
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if tags is not None:
            self._values["tags"] = tags
        if user_context_policy is not None:
            self._values["user_context_policy"] = user_context_policy
        if user_token_configurations is not None:
            self._values["user_token_configurations"] = user_token_configurations

    @builtins.property
    def capacity_units(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.CapacityUnitsConfigurationProperty"]]:
        '''Specifies additional capacity units configured for your Enterprise Edition index.

        You can add and remove capacity units to fit your usage requirements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-capacityunits
        '''
        result = self._values.get("capacity_units")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.CapacityUnitsConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_metadata_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.DocumentMetadataConfigurationProperty"]]]]:
        '''Specifies the properties of an index field.

        You can add either a custom or a built-in field. You can add and remove built-in fields at any time. When a built-in field is removed it's configuration reverts to the default for the field. Custom fields can't be removed from an index after they are added.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-documentmetadataconfigurations
        '''
        result = self._values.get("document_metadata_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.DocumentMetadataConfigurationProperty"]]]], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the index is a Enterprise Edition index, a Developer Edition index, or a GenAI Enterprise Edition index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-edition
        '''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''An IAM role that gives Amazon Kendra permissions to access your Amazon CloudWatch logs and metrics.

        This is also the role used when you use the `BatchPutDocument <https://docs.aws.amazon.com/kendra/latest/dg/BatchPutDocument.html>`_ operation to index documents from an Amazon S3 bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.ServerSideEncryptionConfigurationProperty"]]:
        '''The identifier of the AWS KMS customer managed key (CMK) to use to encrypt data indexed by Amazon Kendra.

        Amazon Kendra doesn't support asymmetric CMKs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.ServerSideEncryptionConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_context_policy(self) -> typing.Optional[builtins.str]:
        '''The user context policy.

        ATTRIBUTE_FILTER

        - All indexed content is searchable and displayable for all users. If you want to filter search results on user context, you can use the attribute filters of ``_user_id`` and ``_group_ids`` or you can provide user and group information in ``UserContext`` .

        USER_TOKEN

        - Enables token-based user access control to filter search results on user context. All documents with no access control and all documents accessible to the user will be searchable and displayable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-usercontextpolicy
        '''
        result = self._values.get("user_context_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_token_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.UserTokenConfigurationProperty"]]]]:
        '''Defines the type of user token used for the index.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-usertokenconfigurations
        '''
        result = self._values.get("user_token_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.UserTokenConfigurationProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIndexMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIndexPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin",
):
    '''Creates an Amazon Kendra index.

    Once the index is active you can add documents to your index using the `BatchPutDocument <https://docs.aws.amazon.com/kendra/latest/dg/BatchPutDocument.html>`_ operation or using one of the supported data sources.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html
    :cloudformationResource: AWS::Kendra::Index
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
        
        cfn_index_props_mixin = kendra_mixins.CfnIndexPropsMixin(kendra_mixins.CfnIndexMixinProps(
            capacity_units=kendra_mixins.CfnIndexPropsMixin.CapacityUnitsConfigurationProperty(
                query_capacity_units=123,
                storage_capacity_units=123
            ),
            description="description",
            document_metadata_configurations=[kendra_mixins.CfnIndexPropsMixin.DocumentMetadataConfigurationProperty(
                name="name",
                relevance=kendra_mixins.CfnIndexPropsMixin.RelevanceProperty(
                    duration="duration",
                    freshness=False,
                    importance=123,
                    rank_order="rankOrder",
                    value_importance_items=[kendra_mixins.CfnIndexPropsMixin.ValueImportanceItemProperty(
                        key="key",
                        value=123
                    )]
                ),
                search=kendra_mixins.CfnIndexPropsMixin.SearchProperty(
                    displayable=False,
                    facetable=False,
                    searchable=False,
                    sortable=False
                ),
                type="type"
            )],
            edition="edition",
            name="name",
            role_arn="roleArn",
            server_side_encryption_configuration=kendra_mixins.CfnIndexPropsMixin.ServerSideEncryptionConfigurationProperty(
                kms_key_id="kmsKeyId"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_context_policy="userContextPolicy",
            user_token_configurations=[kendra_mixins.CfnIndexPropsMixin.UserTokenConfigurationProperty(
                json_token_type_configuration=kendra_mixins.CfnIndexPropsMixin.JsonTokenTypeConfigurationProperty(
                    group_attribute_field="groupAttributeField",
                    user_name_attribute_field="userNameAttributeField"
                ),
                jwt_token_type_configuration=kendra_mixins.CfnIndexPropsMixin.JwtTokenTypeConfigurationProperty(
                    claim_regex="claimRegex",
                    group_attribute_field="groupAttributeField",
                    issuer="issuer",
                    key_location="keyLocation",
                    secret_manager_arn="secretManagerArn",
                    url="url",
                    user_name_attribute_field="userNameAttributeField"
                )
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Kendra::Index``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9202d9318481f54a8a7fe1a12ae3160c5d696988384fb49ecbc6c106489b574a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35fb20de4a79d5a1cc6206bae95622ebf6a12d596beb4003093ba36ae360d24d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630323a9c77ec9b6228ba2e05f1b1b94494db256528bd195d20bda05fdfe53fa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIndexMixinProps:
        return typing.cast(CfnIndexMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin.CapacityUnitsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "query_capacity_units": "queryCapacityUnits",
            "storage_capacity_units": "storageCapacityUnits",
        },
    )
    class CapacityUnitsConfigurationProperty:
        def __init__(
            self,
            *,
            query_capacity_units: typing.Optional[jsii.Number] = None,
            storage_capacity_units: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies additional capacity units configured for your Enterprise Edition index.

            You can add and remove capacity units to fit your usage requirements.

            :param query_capacity_units: The amount of extra query capacity for an index and `GetQuerySuggestions <https://docs.aws.amazon.com/kendra/latest/dg/API_GetQuerySuggestions.html>`_ capacity. A single extra capacity unit for an index provides 0.1 queries per second or approximately 8,000 queries per day. You can add up to 100 extra capacity units. ``GetQuerySuggestions`` capacity is five times the provisioned query capacity for an index, or the base capacity of 2.5 calls per second, whichever is higher. For example, the base capacity for an index is 0.1 queries per second, and ``GetQuerySuggestions`` capacity has a base of 2.5 calls per second. If you add another 0.1 queries per second to total 0.2 queries per second for an index, the ``GetQuerySuggestions`` capacity is 2.5 calls per second (higher than five times 0.2 queries per second).
            :param storage_capacity_units: The amount of extra storage capacity for an index. A single capacity unit provides 30 GB of storage space or 100,000 documents, whichever is reached first. You can add up to 100 extra capacity units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-capacityunitsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                capacity_units_configuration_property = kendra_mixins.CfnIndexPropsMixin.CapacityUnitsConfigurationProperty(
                    query_capacity_units=123,
                    storage_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a98ad812b1616e1ff314ff851b8e0ca14cfa7930892f6e395cf4c414b2c6a3c0)
                check_type(argname="argument query_capacity_units", value=query_capacity_units, expected_type=type_hints["query_capacity_units"])
                check_type(argname="argument storage_capacity_units", value=storage_capacity_units, expected_type=type_hints["storage_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if query_capacity_units is not None:
                self._values["query_capacity_units"] = query_capacity_units
            if storage_capacity_units is not None:
                self._values["storage_capacity_units"] = storage_capacity_units

        @builtins.property
        def query_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The amount of extra query capacity for an index and `GetQuerySuggestions <https://docs.aws.amazon.com/kendra/latest/dg/API_GetQuerySuggestions.html>`_ capacity.

            A single extra capacity unit for an index provides 0.1 queries per second or approximately 8,000 queries per day. You can add up to 100 extra capacity units.

            ``GetQuerySuggestions`` capacity is five times the provisioned query capacity for an index, or the base capacity of 2.5 calls per second, whichever is higher. For example, the base capacity for an index is 0.1 queries per second, and ``GetQuerySuggestions`` capacity has a base of 2.5 calls per second. If you add another 0.1 queries per second to total 0.2 queries per second for an index, the ``GetQuerySuggestions`` capacity is 2.5 calls per second (higher than five times 0.2 queries per second).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-capacityunitsconfiguration.html#cfn-kendra-index-capacityunitsconfiguration-querycapacityunits
            '''
            result = self._values.get("query_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage_capacity_units(self) -> typing.Optional[jsii.Number]:
            '''The amount of extra storage capacity for an index.

            A single capacity unit provides 30 GB of storage space or 100,000 documents, whichever is reached first. You can add up to 100 extra capacity units.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-capacityunitsconfiguration.html#cfn-kendra-index-capacityunitsconfiguration-storagecapacityunits
            '''
            result = self._values.get("storage_capacity_units")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityUnitsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin.DocumentMetadataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "relevance": "relevance",
            "search": "search",
            "type": "type",
        },
    )
    class DocumentMetadataConfigurationProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            relevance: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.RelevanceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            search: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.SearchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the properties, such as relevance tuning and searchability, of an index field.

            :param name: The name of the index field.
            :param relevance: Provides tuning parameters to determine how the field affects the search results.
            :param search: Provides information about how the field is used during a search.
            :param type: The data type of the index field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                document_metadata_configuration_property = kendra_mixins.CfnIndexPropsMixin.DocumentMetadataConfigurationProperty(
                    name="name",
                    relevance=kendra_mixins.CfnIndexPropsMixin.RelevanceProperty(
                        duration="duration",
                        freshness=False,
                        importance=123,
                        rank_order="rankOrder",
                        value_importance_items=[kendra_mixins.CfnIndexPropsMixin.ValueImportanceItemProperty(
                            key="key",
                            value=123
                        )]
                    ),
                    search=kendra_mixins.CfnIndexPropsMixin.SearchProperty(
                        displayable=False,
                        facetable=False,
                        searchable=False,
                        sortable=False
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff72008171395b53a6a2c95abf349addb3f51bcec3ee706c84ac00ece6351535)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument relevance", value=relevance, expected_type=type_hints["relevance"])
                check_type(argname="argument search", value=search, expected_type=type_hints["search"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if relevance is not None:
                self._values["relevance"] = relevance
            if search is not None:
                self._values["search"] = search
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the index field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html#cfn-kendra-index-documentmetadataconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def relevance(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.RelevanceProperty"]]:
            '''Provides tuning parameters to determine how the field affects the search results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html#cfn-kendra-index-documentmetadataconfiguration-relevance
            '''
            result = self._values.get("relevance")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.RelevanceProperty"]], result)

        @builtins.property
        def search(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.SearchProperty"]]:
            '''Provides information about how the field is used during a search.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html#cfn-kendra-index-documentmetadataconfiguration-search
            '''
            result = self._values.get("search")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.SearchProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The data type of the index field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html#cfn-kendra-index-documentmetadataconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentMetadataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin.JsonTokenTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_attribute_field": "groupAttributeField",
            "user_name_attribute_field": "userNameAttributeField",
        },
    )
    class JsonTokenTypeConfigurationProperty:
        def __init__(
            self,
            *,
            group_attribute_field: typing.Optional[builtins.str] = None,
            user_name_attribute_field: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information for the JSON token type.

            :param group_attribute_field: The group attribute field.
            :param user_name_attribute_field: The user name attribute field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jsontokentypeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                json_token_type_configuration_property = kendra_mixins.CfnIndexPropsMixin.JsonTokenTypeConfigurationProperty(
                    group_attribute_field="groupAttributeField",
                    user_name_attribute_field="userNameAttributeField"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__887f427c04c7f6d73a1e93d7d5f24a1afd74028a19ecc9e679aa35bc6e551e97)
                check_type(argname="argument group_attribute_field", value=group_attribute_field, expected_type=type_hints["group_attribute_field"])
                check_type(argname="argument user_name_attribute_field", value=user_name_attribute_field, expected_type=type_hints["user_name_attribute_field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_attribute_field is not None:
                self._values["group_attribute_field"] = group_attribute_field
            if user_name_attribute_field is not None:
                self._values["user_name_attribute_field"] = user_name_attribute_field

        @builtins.property
        def group_attribute_field(self) -> typing.Optional[builtins.str]:
            '''The group attribute field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jsontokentypeconfiguration.html#cfn-kendra-index-jsontokentypeconfiguration-groupattributefield
            '''
            result = self._values.get("group_attribute_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_name_attribute_field(self) -> typing.Optional[builtins.str]:
            '''The user name attribute field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jsontokentypeconfiguration.html#cfn-kendra-index-jsontokentypeconfiguration-usernameattributefield
            '''
            result = self._values.get("user_name_attribute_field")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JsonTokenTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin.JwtTokenTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "claim_regex": "claimRegex",
            "group_attribute_field": "groupAttributeField",
            "issuer": "issuer",
            "key_location": "keyLocation",
            "secret_manager_arn": "secretManagerArn",
            "url": "url",
            "user_name_attribute_field": "userNameAttributeField",
        },
    )
    class JwtTokenTypeConfigurationProperty:
        def __init__(
            self,
            *,
            claim_regex: typing.Optional[builtins.str] = None,
            group_attribute_field: typing.Optional[builtins.str] = None,
            issuer: typing.Optional[builtins.str] = None,
            key_location: typing.Optional[builtins.str] = None,
            secret_manager_arn: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            user_name_attribute_field: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information for the JWT token type.

            :param claim_regex: The regular expression that identifies the claim.
            :param group_attribute_field: The group attribute field.
            :param issuer: The issuer of the token.
            :param key_location: The location of the key.
            :param secret_manager_arn: The Amazon Resource Name (arn) of the secret.
            :param url: The signing key URL.
            :param user_name_attribute_field: The user name attribute field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                jwt_token_type_configuration_property = kendra_mixins.CfnIndexPropsMixin.JwtTokenTypeConfigurationProperty(
                    claim_regex="claimRegex",
                    group_attribute_field="groupAttributeField",
                    issuer="issuer",
                    key_location="keyLocation",
                    secret_manager_arn="secretManagerArn",
                    url="url",
                    user_name_attribute_field="userNameAttributeField"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d4fbb4f451760de28b97cfd45b12af9e9d27ce1af51e84cfeaa6de06b7d8015)
                check_type(argname="argument claim_regex", value=claim_regex, expected_type=type_hints["claim_regex"])
                check_type(argname="argument group_attribute_field", value=group_attribute_field, expected_type=type_hints["group_attribute_field"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
                check_type(argname="argument key_location", value=key_location, expected_type=type_hints["key_location"])
                check_type(argname="argument secret_manager_arn", value=secret_manager_arn, expected_type=type_hints["secret_manager_arn"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument user_name_attribute_field", value=user_name_attribute_field, expected_type=type_hints["user_name_attribute_field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if claim_regex is not None:
                self._values["claim_regex"] = claim_regex
            if group_attribute_field is not None:
                self._values["group_attribute_field"] = group_attribute_field
            if issuer is not None:
                self._values["issuer"] = issuer
            if key_location is not None:
                self._values["key_location"] = key_location
            if secret_manager_arn is not None:
                self._values["secret_manager_arn"] = secret_manager_arn
            if url is not None:
                self._values["url"] = url
            if user_name_attribute_field is not None:
                self._values["user_name_attribute_field"] = user_name_attribute_field

        @builtins.property
        def claim_regex(self) -> typing.Optional[builtins.str]:
            '''The regular expression that identifies the claim.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-claimregex
            '''
            result = self._values.get("claim_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_attribute_field(self) -> typing.Optional[builtins.str]:
            '''The group attribute field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-groupattributefield
            '''
            result = self._values.get("group_attribute_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The issuer of the token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_location(self) -> typing.Optional[builtins.str]:
            '''The location of the key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-keylocation
            '''
            result = self._values.get("key_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_manager_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (arn) of the secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-secretmanagerarn
            '''
            result = self._values.get("secret_manager_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The signing key URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_name_attribute_field(self) -> typing.Optional[builtins.str]:
            '''The user name attribute field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-usernameattributefield
            '''
            result = self._values.get("user_name_attribute_field")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JwtTokenTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin.RelevanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration": "duration",
            "freshness": "freshness",
            "importance": "importance",
            "rank_order": "rankOrder",
            "value_importance_items": "valueImportanceItems",
        },
    )
    class RelevanceProperty:
        def __init__(
            self,
            *,
            duration: typing.Optional[builtins.str] = None,
            freshness: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            importance: typing.Optional[jsii.Number] = None,
            rank_order: typing.Optional[builtins.str] = None,
            value_importance_items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.ValueImportanceItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Provides information for tuning the relevance of a field in a search.

            When a query includes terms that match the field, the results are given a boost in the response based on these tuning parameters.

            :param duration: Specifies the time period that the boost applies to. For example, to make the boost apply to documents with the field value within the last month, you would use "2628000s". Once the field value is beyond the specified range, the effect of the boost drops off. The higher the importance, the faster the effect drops off. If you don't specify a value, the default is 3 months. The value of the field is a numeric string followed by the character "s", for example "86400s" for one day, or "604800s" for one week. Only applies to ``DATE`` fields.
            :param freshness: Indicates that this field determines how "fresh" a document is. For example, if document 1 was created on November 5, and document 2 was created on October 31, document 1 is "fresher" than document 2. Only applies to ``DATE`` fields.
            :param importance: The relative importance of the field in the search. Larger numbers provide more of a boost than smaller numbers.
            :param rank_order: Determines how values should be interpreted. When the ``RankOrder`` field is ``ASCENDING`` , higher numbers are better. For example, a document with a rating score of 10 is higher ranking than a document with a rating score of 1. When the ``RankOrder`` field is ``DESCENDING`` , lower numbers are better. For example, in a task tracking application, a priority 1 task is more important than a priority 5 task. Only applies to ``LONG`` fields.
            :param value_importance_items: An array of key-value pairs for different boosts when they appear in the search result list. For example, if you want to boost query terms that match the "department" field in the result, query terms that match this field are boosted in the result. You can add entries from the department field to boost documents with those values higher. For example, you can add entries to the map with names of departments. If you add "HR", 5 and "Legal",3 those departments are given special attention when they appear in the metadata of a document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                relevance_property = kendra_mixins.CfnIndexPropsMixin.RelevanceProperty(
                    duration="duration",
                    freshness=False,
                    importance=123,
                    rank_order="rankOrder",
                    value_importance_items=[kendra_mixins.CfnIndexPropsMixin.ValueImportanceItemProperty(
                        key="key",
                        value=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8505242df6d95cb45f8ca86b20631f952dc58b32d50e0687b8d47de109f2d3e5)
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument freshness", value=freshness, expected_type=type_hints["freshness"])
                check_type(argname="argument importance", value=importance, expected_type=type_hints["importance"])
                check_type(argname="argument rank_order", value=rank_order, expected_type=type_hints["rank_order"])
                check_type(argname="argument value_importance_items", value=value_importance_items, expected_type=type_hints["value_importance_items"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration is not None:
                self._values["duration"] = duration
            if freshness is not None:
                self._values["freshness"] = freshness
            if importance is not None:
                self._values["importance"] = importance
            if rank_order is not None:
                self._values["rank_order"] = rank_order
            if value_importance_items is not None:
                self._values["value_importance_items"] = value_importance_items

        @builtins.property
        def duration(self) -> typing.Optional[builtins.str]:
            '''Specifies the time period that the boost applies to.

            For example, to make the boost apply to documents with the field value within the last month, you would use "2628000s". Once the field value is beyond the specified range, the effect of the boost drops off. The higher the importance, the faster the effect drops off. If you don't specify a value, the default is 3 months. The value of the field is a numeric string followed by the character "s", for example "86400s" for one day, or "604800s" for one week.

            Only applies to ``DATE`` fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-duration
            '''
            result = self._values.get("duration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def freshness(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates that this field determines how "fresh" a document is.

            For example, if document 1 was created on November 5, and document 2 was created on October 31, document 1 is "fresher" than document 2. Only applies to ``DATE`` fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-freshness
            '''
            result = self._values.get("freshness")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def importance(self) -> typing.Optional[jsii.Number]:
            '''The relative importance of the field in the search.

            Larger numbers provide more of a boost than smaller numbers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-importance
            '''
            result = self._values.get("importance")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rank_order(self) -> typing.Optional[builtins.str]:
            '''Determines how values should be interpreted.

            When the ``RankOrder`` field is ``ASCENDING`` , higher numbers are better. For example, a document with a rating score of 10 is higher ranking than a document with a rating score of 1.

            When the ``RankOrder`` field is ``DESCENDING`` , lower numbers are better. For example, in a task tracking application, a priority 1 task is more important than a priority 5 task.

            Only applies to ``LONG`` fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-rankorder
            '''
            result = self._values.get("rank_order")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_importance_items(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.ValueImportanceItemProperty"]]]]:
            '''An array of key-value pairs for different boosts when they appear in the search result list.

            For example, if you want to boost query terms that match the "department" field in the result, query terms that match this field are boosted in the result. You can add entries from the department field to boost documents with those values higher.

            For example, you can add entries to the map with names of departments. If you add "HR", 5 and "Legal",3 those departments are given special attention when they appear in the metadata of a document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-valueimportanceitems
            '''
            result = self._values.get("value_importance_items")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.ValueImportanceItemProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelevanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin.SearchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "displayable": "displayable",
            "facetable": "facetable",
            "searchable": "searchable",
            "sortable": "sortable",
        },
    )
    class SearchProperty:
        def __init__(
            self,
            *,
            displayable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            facetable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            searchable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            sortable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Provides information about how a custom index field is used during a search.

            :param displayable: Determines whether the field is returned in the query response. The default is ``true`` .
            :param facetable: Indicates that the field can be used to create search facets, a count of results for each value in the field. The default is ``false`` .
            :param searchable: Determines whether the field is used in the search. If the ``Searchable`` field is ``true`` , you can use relevance tuning to manually tune how Amazon Kendra weights the field in the search. The default is ``true`` for string fields and ``false`` for number and date fields.
            :param sortable: Determines whether the field can be used to sort the results of a query. The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                search_property = kendra_mixins.CfnIndexPropsMixin.SearchProperty(
                    displayable=False,
                    facetable=False,
                    searchable=False,
                    sortable=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d31890c34d19bc5c4a21622afd8f784376fb0f4b9cea5dac544ebc0f60f1e587)
                check_type(argname="argument displayable", value=displayable, expected_type=type_hints["displayable"])
                check_type(argname="argument facetable", value=facetable, expected_type=type_hints["facetable"])
                check_type(argname="argument searchable", value=searchable, expected_type=type_hints["searchable"])
                check_type(argname="argument sortable", value=sortable, expected_type=type_hints["sortable"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if displayable is not None:
                self._values["displayable"] = displayable
            if facetable is not None:
                self._values["facetable"] = facetable
            if searchable is not None:
                self._values["searchable"] = searchable
            if sortable is not None:
                self._values["sortable"] = sortable

        @builtins.property
        def displayable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the field is returned in the query response.

            The default is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html#cfn-kendra-index-search-displayable
            '''
            result = self._values.get("displayable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def facetable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates that the field can be used to create search facets, a count of results for each value in the field.

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html#cfn-kendra-index-search-facetable
            '''
            result = self._values.get("facetable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def searchable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the field is used in the search.

            If the ``Searchable`` field is ``true`` , you can use relevance tuning to manually tune how Amazon Kendra weights the field in the search. The default is ``true`` for string fields and ``false`` for number and date fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html#cfn-kendra-index-search-searchable
            '''
            result = self._values.get("searchable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sortable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines whether the field can be used to sort the results of a query.

            The default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html#cfn-kendra-index-search-sortable
            '''
            result = self._values.get("sortable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SearchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''Provides the identifier of the AWS KMS customer master key (CMK) used to encrypt data indexed by Amazon Kendra.

            We suggest that you use a CMK from your account to help secure your index. Amazon Kendra doesn't support asymmetric CMKs.

            :param kms_key_id: The identifier of the AWS KMS key . Amazon Kendra doesn't support asymmetric keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-serversideencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                server_side_encryption_configuration_property = kendra_mixins.CfnIndexPropsMixin.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a328901c7180ad96ef1198bc11d6936ed74dad37e7f30ee0a27be6fb3a21d917)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the AWS KMS key .

            Amazon Kendra doesn't support asymmetric keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-serversideencryptionconfiguration.html#cfn-kendra-index-serversideencryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin.UserTokenConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "json_token_type_configuration": "jsonTokenTypeConfiguration",
            "jwt_token_type_configuration": "jwtTokenTypeConfiguration",
        },
    )
    class UserTokenConfigurationProperty:
        def __init__(
            self,
            *,
            json_token_type_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.JsonTokenTypeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            jwt_token_type_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIndexPropsMixin.JwtTokenTypeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides the configuration information for a token.

            .. epigraph::

               If you're using an Amazon Kendra Gen AI Enterprise Edition index and you try to use ``UserTokenConfigurations`` to configure user context policy, Amazon Kendra returns a ``ValidationException`` error.

            :param json_token_type_configuration: Information about the JSON token type configuration.
            :param jwt_token_type_configuration: Information about the JWT token type configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-usertokenconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                user_token_configuration_property = kendra_mixins.CfnIndexPropsMixin.UserTokenConfigurationProperty(
                    json_token_type_configuration=kendra_mixins.CfnIndexPropsMixin.JsonTokenTypeConfigurationProperty(
                        group_attribute_field="groupAttributeField",
                        user_name_attribute_field="userNameAttributeField"
                    ),
                    jwt_token_type_configuration=kendra_mixins.CfnIndexPropsMixin.JwtTokenTypeConfigurationProperty(
                        claim_regex="claimRegex",
                        group_attribute_field="groupAttributeField",
                        issuer="issuer",
                        key_location="keyLocation",
                        secret_manager_arn="secretManagerArn",
                        url="url",
                        user_name_attribute_field="userNameAttributeField"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb781fe0610bc65abe29e22f255e65dfc7eade19b98c7ade576b61581bb85aaf)
                check_type(argname="argument json_token_type_configuration", value=json_token_type_configuration, expected_type=type_hints["json_token_type_configuration"])
                check_type(argname="argument jwt_token_type_configuration", value=jwt_token_type_configuration, expected_type=type_hints["jwt_token_type_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if json_token_type_configuration is not None:
                self._values["json_token_type_configuration"] = json_token_type_configuration
            if jwt_token_type_configuration is not None:
                self._values["jwt_token_type_configuration"] = jwt_token_type_configuration

        @builtins.property
        def json_token_type_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.JsonTokenTypeConfigurationProperty"]]:
            '''Information about the JSON token type configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-usertokenconfiguration.html#cfn-kendra-index-usertokenconfiguration-jsontokentypeconfiguration
            '''
            result = self._values.get("json_token_type_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.JsonTokenTypeConfigurationProperty"]], result)

        @builtins.property
        def jwt_token_type_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.JwtTokenTypeConfigurationProperty"]]:
            '''Information about the JWT token type configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-usertokenconfiguration.html#cfn-kendra-index-usertokenconfiguration-jwttokentypeconfiguration
            '''
            result = self._values.get("jwt_token_type_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIndexPropsMixin.JwtTokenTypeConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserTokenConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kendra.mixins.CfnIndexPropsMixin.ValueImportanceItemProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ValueImportanceItemProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies a key-value pair of the search boost value for a document when the key is part of the metadata of a document.

            :param key: The document metadata value used for the search boost.
            :param value: The boost value for a document when the key is part of the metadata of a document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-valueimportanceitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kendra import mixins as kendra_mixins
                
                value_importance_item_property = kendra_mixins.CfnIndexPropsMixin.ValueImportanceItemProperty(
                    key="key",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7b0b7761f4fb126c36cca8ab658152bc5e9ed2e9ba671113ac22198c3d5b26e)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The document metadata value used for the search boost.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-valueimportanceitem.html#cfn-kendra-index-valueimportanceitem-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The boost value for a document when the key is part of the metadata of a document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-valueimportanceitem.html#cfn-kendra-index-valueimportanceitem-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValueImportanceItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDataSourceMixinProps",
    "CfnDataSourcePropsMixin",
    "CfnFaqMixinProps",
    "CfnFaqPropsMixin",
    "CfnIndexMixinProps",
    "CfnIndexPropsMixin",
]

publication.publish()

def _typecheckingstub__26de3a0a87130f6fb90b3250b97fce1493ec3da757f84e0ecd2a127523c428df(
    *,
    custom_document_enrichment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.CustomDocumentEnrichmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    index_id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76519d15071f2a3daad21e8f32dd48e667d3d824fa61000ebad87c9ff1ff7203(
    props: typing.Union[CfnDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48b921c40ab0908728e1425eeaa7ef95e97ad917d08bbcc4c8d13abe78dfe3b5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f715293058639fe474bfa70b8f2edfeec93b2a401cb92af5c023da92b6035c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5056664f8f743bb93c42ddddd211bdd2f3508c2086452e9603f51c458db4ee(
    *,
    key_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf39320c15ecf8d7d6d42b80214ffc9cf0d14b3c2e36daf516225771c8e023db(
    *,
    allowed_groups_column_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10955cf9c6deb5467398b87e94c56a7b51ba03dc2d8f8ba5a5de6a284d23e53(
    *,
    change_detecting_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    document_data_column_name: typing.Optional[builtins.str] = None,
    document_id_column_name: typing.Optional[builtins.str] = None,
    document_title_column_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a45c837ec8158eb6e8bb092541bfbfd1f6e7ba43440626cc89a6830130887a(
    *,
    attachment_field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConfluenceAttachmentToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205a46c026766efdba5c77b63c822ac754ebeeab704d997a918464911e14dfd4(
    *,
    data_source_field_name: typing.Optional[builtins.str] = None,
    date_field_format: typing.Optional[builtins.str] = None,
    index_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e41ba4ad67f9b2832d428a7603871262be71d6495a20139d4b461e28f36e1d(
    *,
    blog_field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConfluenceBlogToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898ce38c507a69a70476b7a07527180d02e8c7c1a25afd91e77bfb31f8c5c514(
    *,
    data_source_field_name: typing.Optional[builtins.str] = None,
    date_field_format: typing.Optional[builtins.str] = None,
    index_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a3aaa8301110ff8d8c17070190aa6b4540fec9a90491efe2682fc7cb0602b8(
    *,
    attachment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConfluenceAttachmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    blog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConfluenceBlogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    page_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConfluencePageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    server_url: typing.Optional[builtins.str] = None,
    space_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConfluenceSpaceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f6a315c1823c58589682cdd849928d09084eee80c2934290513e5e5207d5aa(
    *,
    page_field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConfluencePageToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d5c5c74279052ceaec3377ef35c388c3f832221c7b758587e4d18ada2a4be5(
    *,
    data_source_field_name: typing.Optional[builtins.str] = None,
    date_field_format: typing.Optional[builtins.str] = None,
    index_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aebcebcc785d4e9986d4da79693bcc763bfc9bc81f58fb9bf72b9ca1131c5af(
    *,
    crawl_archived_spaces: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    crawl_personal_spaces: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclude_spaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_spaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    space_field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConfluenceSpaceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa89b3774861771231bc597dc67a0b9132acb354df03c318b4bb152b5a52cbe8(
    *,
    data_source_field_name: typing.Optional[builtins.str] = None,
    date_field_format: typing.Optional[builtins.str] = None,
    index_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae80d9493741b442df2a56d0a514718855519857e55565b0501cf07fe52a5ad(
    *,
    database_host: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    database_port: typing.Optional[jsii.Number] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f071c683f9c6368eed022b07c33a6d22a3b12faf220b046f559ada014f5091b(
    *,
    inline_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.InlineCustomDocumentEnrichmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    post_extraction_hook_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.HookConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    pre_extraction_hook_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.HookConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e949391af1fdd73449b43a7f30537e9f2b15c15fe6bdf30e3bdf1ac9b22e2c(
    *,
    confluence_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConfluenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DatabaseConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    google_drive_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.GoogleDriveConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    one_drive_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.OneDriveConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.S3DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    salesforce_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SalesforceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_now_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ServiceNowConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    share_point_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SharePointConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.TemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    web_crawler_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.WebCrawlerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    work_docs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.WorkDocsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b35e946e502e0379a557043dcab4a69d774fd4172dd2cfff06bbbbebbc136e(
    *,
    data_source_field_name: typing.Optional[builtins.str] = None,
    date_field_format: typing.Optional[builtins.str] = None,
    index_field_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a38248652dacf61c2e104a521d29d50548946a2a9a4064d1ca9b9d23a6ddad(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641a91f5c9c19f243e826ae90836b815dfd48f2c64cade6f183e6e37f7033c81(
    *,
    acl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.AclConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    column_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ColumnConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connection_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ConnectionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_engine_type: typing.Optional[builtins.str] = None,
    sql_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SqlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849fa15a939ef611f2628654a7c7a5cddb4849ac49ccf80d98079112658863ba(
    *,
    condition_document_attribute_key: typing.Optional[builtins.str] = None,
    condition_on_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1fbacd6ff60a75dec522269c036933188e757e1ed21c6c2c44301dc8be64a9(
    *,
    target_document_attribute_key: typing.Optional[builtins.str] = None,
    target_document_attribute_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76fd95d20e9648b4a6a18f07ac1e2f005c7b7dd6cf687128e8ecac67afa0ebd2(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2902df0947b3d78acf32af1207e684537c9b835b3e23be52e79ad1500800e5(
    *,
    s3_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7714136dfa2254133a5ee0c94edfa6069130f50826c5f8a422a8c1b3c4f322(
    *,
    exclude_mime_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_shared_drives: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_user_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c661a602d8dd4a70c56357f93f98b1e9fd3a5d62021b4a9d45a361533060e8(
    *,
    invocation_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_arn: typing.Optional[builtins.str] = None,
    s3_bucket: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7464a9b6abb908eaf873d1220abb95ba3bae02a1d94069f0e1f9b33465a9d12a(
    *,
    condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    document_content_deletion: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentAttributeTargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7d3e54315073d85c9253803f76b7480a31edd18cbcb29fe83d779e0c1648be(
    *,
    disable_local_groups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    one_drive_users: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.OneDriveUsersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    tenant_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5eeb64778818ddc81e60a09611edb17ce76a43674a47dd8ce6b7add627f09e4(
    *,
    one_drive_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    one_drive_user_s3_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.S3PathProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d90bb9d6def43faed1451329c30d6849549f34839313448422042eae6649bc(
    *,
    credentials: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7296df89874679585465a3fa2f116f8fa14c42256ab84fdc29000415b80443(
    *,
    access_control_list_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.AccessControlListConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    documents_metadata_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DocumentsMetadataConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b38e1d60ff130411d2fba82cf92f45c8ab7a0acd895e3b637b114ba12674655(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa2f6e990b9aaeeee27877cd5143ab1205e4a4a28c3ba364e2839582a22386d(
    *,
    document_data_field_name: typing.Optional[builtins.str] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_filter_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82e6cc6cf20308f4f59de5599bb24ea2f119044af4f04fd880bdb9e3e0e24f80(
    *,
    chatter_feed_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SalesforceChatterFeedConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    knowledge_article_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SalesforceKnowledgeArticleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    server_url: typing.Optional[builtins.str] = None,
    standard_object_attachment_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SalesforceStandardObjectAttachmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    standard_object_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SalesforceStandardObjectConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9215ee5a9b8b13c6cd2762d4dda6895d3a710c76014b32a5872536e6317007(
    *,
    document_data_field_name: typing.Optional[builtins.str] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f71b03883c18f0e607a1432e8dc32d1366a18e02c7af0be7ba6fbae6e46a08f(
    *,
    custom_knowledge_article_type_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SalesforceCustomKnowledgeArticleTypeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    included_states: typing.Optional[typing.Sequence[builtins.str]] = None,
    standard_knowledge_article_type_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.SalesforceStandardKnowledgeArticleTypeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5498d621932e8d77cab8018aeadc9467e4367a490b98b6eb6e1e7a94f5d22d4(
    *,
    document_data_field_name: typing.Optional[builtins.str] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4df9bf6ac661e5af4963b063df9703b3436445caff209aa715cd744c0581aa1(
    *,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462a440ff1838a79d0c83ca33abea3278dad67aee390b6f585eb170cfc4e6b03(
    *,
    document_data_field_name: typing.Optional[builtins.str] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97a239a5d8ed2b11d778bae19ca451195623f6653a1400237c15e467caf6cdd(
    *,
    authentication_type: typing.Optional[builtins.str] = None,
    host_url: typing.Optional[builtins.str] = None,
    knowledge_article_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ServiceNowKnowledgeArticleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    service_catalog_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ServiceNowServiceCatalogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_now_build_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc45f30c0387e397b7831a6b4d0989a844e9eb38a70ba84fc865e0e8cb18d78(
    *,
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    document_data_field_name: typing.Optional[builtins.str] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    filter_query: typing.Optional[builtins.str] = None,
    include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6af40890c0c4f262b48d050f67eefd140c16a08359969db948a1fd9d8b18d3(
    *,
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    document_data_field_name: typing.Optional[builtins.str] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3be79a905b606b16d3963ec36e8567f7075623000a2bbba0d649ae93c48ee5f(
    *,
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    disable_local_groups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    share_point_version: typing.Optional[builtins.str] = None,
    ssl_certificate_s3_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.S3PathProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_change_log: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0ec6919af20b3ae18db779142356fd8b6e81861859a759fd87130e2cad0c43(
    *,
    query_identifiers_enclosing_option: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__412714ebe317eab4c8831768c6ef7b27275330743acef3efca1640de7032480c(
    *,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b038c8d546495184ef4c44e3ec01e6d1b7cc7533d6d0f315372011a4ebf51f(
    *,
    basic_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.WebCrawlerBasicAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60be6361f036a4a68326bf80908225737a129f3ec03298c60ef3be7f61b29945(
    *,
    credentials: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16375405779a14946b9fbe2f956a4026ba75c8539b9d6a16e43684670a3f32dc(
    *,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.WebCrawlerAuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    crawl_depth: typing.Optional[jsii.Number] = None,
    max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
    max_links_per_page: typing.Optional[jsii.Number] = None,
    max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
    proxy_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.ProxyConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    urls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.WebCrawlerUrlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530bed823bedc075927aa8bcb246001bf90584abaed24dabfda9743932485964(
    *,
    seed_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    web_crawler_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd291d43fb1ed33ba5cac71c44300497086d8e53229da033c7e8ddf517e7a26(
    *,
    site_maps: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2015d42cb5a352a099b27101af2cc8c83bfef53d22bef92c780c93afd30aba6(
    *,
    seed_url_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.WebCrawlerSeedUrlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    site_maps_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.WebCrawlerSiteMapsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4470f4517a7511e09624d9470b61445464e73893c9dff86e7cb71be1b338065(
    *,
    crawl_comments: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataSourcePropsMixin.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    organization_id: typing.Optional[builtins.str] = None,
    use_change_log: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8182503e3dd74b6ea13c394076efca6b3fd80fdc2063adf75db56068b1f7ca2(
    *,
    description: typing.Optional[builtins.str] = None,
    file_format: typing.Optional[builtins.str] = None,
    index_id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    s3_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFaqPropsMixin.S3PathProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ee7a5900ed89cab6a3965c1ae35c1d180cc170d89893b00a950237f36b9452(
    props: typing.Union[CfnFaqMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0848e09f4c78f09c4c2c46e2daed5c6237786721d934c09c49a119ca0fdbb68(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca73a9c9aa275bb6dbef86530eed5e86f88d52f0acd0940f4bc7845d537fa308(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6821bfd953c0dde3439ca0cbcfd93f694e271a6a720d07dfaf52ac8d3eca5cb5(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dacaddcf70331f910505ece8620a665ce2b8641e7cba5da4ecc76cb52f7136(
    *,
    capacity_units: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.CapacityUnitsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    document_metadata_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.DocumentMetadataConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    edition: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_context_policy: typing.Optional[builtins.str] = None,
    user_token_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.UserTokenConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9202d9318481f54a8a7fe1a12ae3160c5d696988384fb49ecbc6c106489b574a(
    props: typing.Union[CfnIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fb20de4a79d5a1cc6206bae95622ebf6a12d596beb4003093ba36ae360d24d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630323a9c77ec9b6228ba2e05f1b1b94494db256528bd195d20bda05fdfe53fa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98ad812b1616e1ff314ff851b8e0ca14cfa7930892f6e395cf4c414b2c6a3c0(
    *,
    query_capacity_units: typing.Optional[jsii.Number] = None,
    storage_capacity_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff72008171395b53a6a2c95abf349addb3f51bcec3ee706c84ac00ece6351535(
    *,
    name: typing.Optional[builtins.str] = None,
    relevance: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.RelevanceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    search: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.SearchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887f427c04c7f6d73a1e93d7d5f24a1afd74028a19ecc9e679aa35bc6e551e97(
    *,
    group_attribute_field: typing.Optional[builtins.str] = None,
    user_name_attribute_field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4fbb4f451760de28b97cfd45b12af9e9d27ce1af51e84cfeaa6de06b7d8015(
    *,
    claim_regex: typing.Optional[builtins.str] = None,
    group_attribute_field: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    key_location: typing.Optional[builtins.str] = None,
    secret_manager_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    user_name_attribute_field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8505242df6d95cb45f8ca86b20631f952dc58b32d50e0687b8d47de109f2d3e5(
    *,
    duration: typing.Optional[builtins.str] = None,
    freshness: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    importance: typing.Optional[jsii.Number] = None,
    rank_order: typing.Optional[builtins.str] = None,
    value_importance_items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.ValueImportanceItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31890c34d19bc5c4a21622afd8f784376fb0f4b9cea5dac544ebc0f60f1e587(
    *,
    displayable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    facetable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    searchable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sortable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a328901c7180ad96ef1198bc11d6936ed74dad37e7f30ee0a27be6fb3a21d917(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb781fe0610bc65abe29e22f255e65dfc7eade19b98c7ade576b61581bb85aaf(
    *,
    json_token_type_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.JsonTokenTypeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    jwt_token_type_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIndexPropsMixin.JwtTokenTypeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b0b7761f4fb126c36cca8ab658152bc5e9ed2e9ba671113ac22198c3d5b26e(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
