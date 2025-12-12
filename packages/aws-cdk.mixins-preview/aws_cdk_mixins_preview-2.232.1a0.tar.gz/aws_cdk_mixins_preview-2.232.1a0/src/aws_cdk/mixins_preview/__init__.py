r'''
# CDK Mixins (Preview)

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This package provides two main features:

1. **Mixins** - Composable abstractions for adding functionality to constructs
2. **EventBridge Event Patterns** - Type-safe event patterns for AWS resources

---


## CDK Mixins

CDK Mixins provide a new, advanced way to add functionality through composable abstractions.
Unlike traditional L2 constructs that bundle all features together, Mixins allow you to pick and choose exactly the capabilities you need for constructs.

### Key Benefits

* **Universal Compatibility**: Apply the same abstractions to L1 constructs, L2 constructs, or custom constructs
* **Composable Design**: Mix and match features without being locked into specific implementations
* **Cross-Service Abstractions**: Use common patterns like encryption across different AWS services
* **Escape Hatch Freedom**: Customize resources in a safe, typed way while keeping the abstractions you want

### Basic Usage

Mixins use `Mixins.of()` as the fundamental API for applying abstractions to constructs:

```python
# Base form: apply mixins to any construct
bucket = s3.CfnBucket(scope, "MyBucket")
Mixins.of(bucket).apply(EncryptionAtRest()).apply(AutoDeleteObjects())
```

#### Fluent Syntax with `.with()`

For convenience, you can use the `.with()` method for a more fluent syntax:

```python
from aws_cdk.mixins_preview.with import


bucket = s3.CfnBucket(scope, "MyBucket").with(EnableVersioning()).with(AutoDeleteObjects())
```

The `.with()` method is available after importing `@aws-cdk/mixins-preview/with`, which augments all constructs with this method. It provides the same functionality as `Mixins.of().apply()` but with a more chainable API.

> **Note**: The `.with()` fluent syntax is only available in JavaScript and TypeScript. Other jsii languages (Python, Java, C#, and Go) should use the `Mixins.of(...).mustApply()` syntax instead. The import requirement is temporary during the preview phase. Once the API is stable, the `.with()` method will be available by default on all constructs and in all languages.

### Creating Custom Mixins

Mixins are simple classes that implement the `IMixin` interface (usually by extending the abstract `Mixin` class:

```python
# Simple mixin that enables versioning
@jsii.implements(IMixin)
class CustomVersioningMixin(Mixin):
    def supports(self, construct):
        return construct instanceof s3.CfnBucket

    def apply_to(self, bucket):
        bucket.versioning_configuration = {
            "status": "Enabled"
        }
        return bucket

# Usage
bucket = s3.CfnBucket(scope, "MyBucket")
Mixins.of(bucket).apply(CustomVersioningMixin())
```

### Construct Selection

Mixins operate on construct trees and can be applied selectively:

```python
# Apply to all constructs in a scope
Mixins.of(scope).apply(EncryptionAtRest())

# Apply to specific resource types
Mixins.of(scope, ConstructSelector.resources_of_type(s3.CfnBucket.CFN_RESOURCE_TYPE_NAME)).apply(EncryptionAtRest())

# Apply to constructs matching a path pattern
Mixins.of(scope, ConstructSelector.by_path("**/*-prod-*/**")).apply(ProductionSecurityMixin())
```

### Built-in Mixins

#### Cross-Service Mixins

**EncryptionAtRest**: Applies encryption to supported AWS resources

```python
# Works across different resource types
bucket = s3.CfnBucket(scope, "Bucket")
Mixins.of(bucket).apply(EncryptionAtRest())

log_group = logs.CfnLogGroup(scope, "LogGroup")
Mixins.of(log_group).apply(EncryptionAtRest())
```

#### S3-Specific Mixins

**AutoDeleteObjects**: Configures automatic object deletion for S3 buckets

```python
bucket = s3.CfnBucket(scope, "Bucket")
Mixins.of(bucket).apply(AutoDeleteObjects())
```

**EnableVersioning**: Enables versioning on S3 buckets

```python
bucket = s3.CfnBucket(scope, "Bucket")
Mixins.of(bucket).apply(EnableVersioning())
```

### Logs Delivery

Configures vended logs delivery for supported resources to various destinations:

```python
from aws_cdk.mixins_preview.with import
import aws_cdk.mixins_preview.aws_cloudfront.mixins as cloudfront_mixins

# Create CloudFront distribution
# bucket: s3.Bucket

distribution = cloudfront.Distribution(scope, "Distribution",
    default_behavior=cloudfront.BehaviorOptions(
        origin=origins.S3BucketOrigin.with_origin_access_control(bucket)
    )
)

# Create log destination
log_group = logs.LogGroup(scope, "DeliveryLogGroup")

# Configure log delivery using the mixin
distribution.with(cloudfront_mixins.CfnDistributionLogsMixin.CONNECTION_LOGS.to_log_group(log_group))
```

### L1 Property Mixins

For every CloudFormation resource, CDK Mixins automatically generates type-safe property mixins. These allow you to apply L1 properties with full TypeScript support:

```python
from aws_cdk.mixins_preview.with import


bucket = s3.Bucket(scope, "Bucket").with(CfnBucketPropsMixin(
    versioning_configuration=CfnBucketPropsMixin.VersioningConfigurationProperty(status="Enabled"),
    public_access_block_configuration=CfnBucketPropsMixin.PublicAccessBlockConfigurationProperty(
        block_public_acls=True,
        block_public_policy=True
    )
))
```

Property mixins support two merge strategies:

```python
# bucket: s3.CfnBucket


# MERGE (default): Deep merges properties with existing values
Mixins.of(bucket).apply(CfnBucketPropsMixin(CfnBucketMixinProps(versioning_configuration=CfnBucketPropsMixin.VersioningConfigurationProperty(status="Enabled")), strategy=PropertyMergeStrategy.MERGE))

# OVERRIDE: Replaces existing property values
Mixins.of(bucket).apply(CfnBucketPropsMixin(CfnBucketMixinProps(versioning_configuration=CfnBucketPropsMixin.VersioningConfigurationProperty(status="Enabled")), strategy=PropertyMergeStrategy.OVERRIDE))
```

Property mixins are available for all AWS services:

```python
from aws_cdk.mixins_preview.aws_logs.mixins import CfnLogGroupPropsMixin
from aws_cdk.mixins_preview.aws_lambda.mixins import CfnFunctionPropsMixin
from aws_cdk.mixins_preview.aws_dynamodb.mixins import CfnTablePropsMixin
```

### Error Handling

Mixins provide comprehensive error handling:

```python
# Graceful handling of unsupported constructs
Mixins.of(scope).apply(EncryptionAtRest()) # Skips unsupported constructs

# Strict application that requires all constructs to match
Mixins.of(scope).must_apply(EncryptionAtRest())
```

---


## EventBridge Event Patterns

CDK Mixins automatically generates typed EventBridge event patterns for AWS resources. These patterns work with both L1 and L2 constructs, providing a consistent interface for creating EventBridge rules.

### Event Patterns Basic Usage

```python
from aws_cdk.mixins_preview.aws_s3.events import BucketEvents
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets
# fn: lambda.Function


# Works with L2 constructs
bucket = s3.Bucket(scope, "Bucket")
bucket_events = BucketEvents.from_bucket(bucket)

events.Rule(scope, "Rule",
    event_pattern=bucket_events.object_created_pattern(
        object=BucketEvents.ObjectCreated.ObjectType(key=["uploads/*"])
    ),
    targets=[targets.LambdaFunction(fn)]
)

# Also works with L1 constructs
cfn_bucket = s3.CfnBucket(scope, "CfnBucket")
cfn_bucket_events = BucketEvents.from_bucket(cfn_bucket)

events.CfnRule(scope, "CfnRule",
    state="ENABLED",
    event_pattern=cfn_bucket_events.object_created_pattern(
        object=BucketEvents.ObjectCreated.ObjectType(key=["uploads/*"])
    ),
    targets=[events.CfnRule.TargetProperty(arn=fn.function_arn, id="L1")]
)
```

### Event Pattern Features

**Automatic Resource Injection**: Resource identifiers are automatically included in patterns

```python
from aws_cdk.mixins_preview.aws_s3.events import BucketEvents

# bucket: s3.Bucket

bucket_events = BucketEvents.from_bucket(bucket)

# Bucket name is automatically injected from the bucket reference
pattern = bucket_events.object_created_pattern()
```

**Event Metadata Support**: Control EventBridge pattern metadata

```python
from aws_cdk.mixins_preview.aws_s3.events import BucketEvents

# bucket: s3.Bucket

bucket_events = BucketEvents.from_bucket(bucket)

pattern = bucket_events.object_created_pattern(
    event_metadata=AWSEventMetadataProps(
        region=["us-east-1", "us-west-2"],
        version=["0"]
    )
)
```

### Available Events

Event patterns are generated for EventBridge events available in the AWS Event Schema Registry. Common examples:

**S3 Events**:

* `objectCreatedPattern()` - Object creation events
* `objectDeletedPattern()` - Object deletion events
* `objectTagsAddedPattern()` - Object tagging events
* `awsAPICallViaCloudTrailPattern()` - CloudTrail API calls

Import events from service-specific modules:

```python
from aws_cdk.mixins_preview.aws_s3.events import BucketEvents
```
'''
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

from ._jsii import *

__all__ = [
    "alexa_ask",
    "aws_accessanalyzer",
    "aws_acmpca",
    "aws_aiops",
    "aws_amazonmq",
    "aws_amplify",
    "aws_amplifyuibuilder",
    "aws_apigateway",
    "aws_apigatewayv2",
    "aws_appconfig",
    "aws_appflow",
    "aws_appintegrations",
    "aws_applicationautoscaling",
    "aws_applicationinsights",
    "aws_applicationsignals",
    "aws_appmesh",
    "aws_apprunner",
    "aws_appstream",
    "aws_appsync",
    "aws_apptest",
    "aws_aps",
    "aws_arcregionswitch",
    "aws_arczonalshift",
    "aws_athena",
    "aws_auditmanager",
    "aws_autoscaling",
    "aws_autoscalingplans",
    "aws_b2bi",
    "aws_backup",
    "aws_backupgateway",
    "aws_batch",
    "aws_bcmdataexports",
    "aws_bedrock",
    "aws_bedrockagentcore",
    "aws_billingconductor",
    "aws_budgets",
    "aws_cassandra",
    "aws_ce",
    "aws_certificatemanager",
    "aws_chatbot",
    "aws_cleanrooms",
    "aws_cleanroomsml",
    "aws_cloud9",
    "aws_cloudformation",
    "aws_cloudfront",
    "aws_cloudtrail",
    "aws_cloudwatch",
    "aws_codeartifact",
    "aws_codebuild",
    "aws_codecommit",
    "aws_codeconnections",
    "aws_codedeploy",
    "aws_codeguruprofiler",
    "aws_codegurureviewer",
    "aws_codepipeline",
    "aws_codestar",
    "aws_codestarconnections",
    "aws_codestarnotifications",
    "aws_cognito",
    "aws_comprehend",
    "aws_config",
    "aws_connect",
    "aws_connectcampaigns",
    "aws_connectcampaignsv2",
    "aws_controltower",
    "aws_cur",
    "aws_customerprofiles",
    "aws_databrew",
    "aws_datapipeline",
    "aws_datasync",
    "aws_datazone",
    "aws_dax",
    "aws_deadline",
    "aws_detective",
    "aws_devicefarm",
    "aws_devopsagent",
    "aws_devopsguru",
    "aws_directoryservice",
    "aws_dlm",
    "aws_dms",
    "aws_docdb",
    "aws_docdbelastic",
    "aws_dsql",
    "aws_dynamodb",
    "aws_ec2",
    "aws_ecr",
    "aws_ecs",
    "aws_efs",
    "aws_eks",
    "aws_elasticache",
    "aws_elasticbeanstalk",
    "aws_elasticloadbalancing",
    "aws_elasticloadbalancingv2",
    "aws_elasticsearch",
    "aws_emr",
    "aws_emrcontainers",
    "aws_emrserverless",
    "aws_entityresolution",
    "aws_eventschemas",
    "aws_evidently",
    "aws_evs",
    "aws_finspace",
    "aws_fis",
    "aws_fms",
    "aws_forecast",
    "aws_frauddetector",
    "aws_fsx",
    "aws_gamelift",
    "aws_gameliftstreams",
    "aws_globalaccelerator",
    "aws_glue",
    "aws_grafana",
    "aws_greengrass",
    "aws_greengrassv2",
    "aws_groundstation",
    "aws_guardduty",
    "aws_healthimaging",
    "aws_healthlake",
    "aws_iam",
    "aws_identitystore",
    "aws_imagebuilder",
    "aws_inspector",
    "aws_inspectorv2",
    "aws_internetmonitor",
    "aws_invoicing",
    "aws_iot",
    "aws_iotanalytics",
    "aws_iotcoredeviceadvisor",
    "aws_iotevents",
    "aws_iotfleethub",
    "aws_iotfleetwise",
    "aws_iotsitewise",
    "aws_iotthingsgraph",
    "aws_iottwinmaker",
    "aws_iotwireless",
    "aws_ivs",
    "aws_ivschat",
    "aws_kafkaconnect",
    "aws_kendra",
    "aws_kendraranking",
    "aws_kinesis",
    "aws_kinesisanalytics",
    "aws_kinesisanalyticsv2",
    "aws_kinesisfirehose",
    "aws_kinesisvideo",
    "aws_kms",
    "aws_lakeformation",
    "aws_lambda",
    "aws_launchwizard",
    "aws_lex",
    "aws_licensemanager",
    "aws_lightsail",
    "aws_location",
    "aws_logs",
    "aws_lookoutequipment",
    "aws_lookoutmetrics",
    "aws_lookoutvision",
    "aws_m2",
    "aws_macie",
    "aws_managedblockchain",
    "aws_mediaconnect",
    "aws_mediaconvert",
    "aws_medialive",
    "aws_mediapackage",
    "aws_mediapackagev2",
    "aws_mediastore",
    "aws_mediatailor",
    "aws_memorydb",
    "aws_mpa",
    "aws_msk",
    "aws_mwaa",
    "aws_neptune",
    "aws_neptunegraph",
    "aws_networkfirewall",
    "aws_networkmanager",
    "aws_nimblestudio",
    "aws_notifications",
    "aws_notificationscontacts",
    "aws_oam",
    "aws_observabilityadmin",
    "aws_odb",
    "aws_omics",
    "aws_opensearchserverless",
    "aws_opensearchservice",
    "aws_opsworks",
    "aws_opsworkscm",
    "aws_organizations",
    "aws_osis",
    "aws_panorama",
    "aws_paymentcryptography",
    "aws_pcaconnectorad",
    "aws_pcaconnectorscep",
    "aws_pcs",
    "aws_personalize",
    "aws_pinpoint",
    "aws_pinpointemail",
    "aws_pipes",
    "aws_proton",
    "aws_qbusiness",
    "aws_qldb",
    "aws_quicksight",
    "aws_ram",
    "aws_rbin",
    "aws_rds",
    "aws_redshift",
    "aws_redshiftserverless",
    "aws_refactorspaces",
    "aws_rekognition",
    "aws_resiliencehub",
    "aws_resourceexplorer2",
    "aws_resourcegroups",
    "aws_robomaker",
    "aws_rolesanywhere",
    "aws_route53",
    "aws_route53profiles",
    "aws_route53recoverycontrol",
    "aws_route53recoveryreadiness",
    "aws_route53resolver",
    "aws_rtbfabric",
    "aws_rum",
    "aws_s3",
    "aws_s3express",
    "aws_s3objectlambda",
    "aws_s3outposts",
    "aws_s3tables",
    "aws_s3vectors",
    "aws_sagemaker",
    "aws_sam",
    "aws_scheduler",
    "aws_sdb",
    "aws_secretsmanager",
    "aws_securityhub",
    "aws_securitylake",
    "aws_servicecatalog",
    "aws_servicecatalogappregistry",
    "aws_servicediscovery",
    "aws_ses",
    "aws_shield",
    "aws_signer",
    "aws_simspaceweaver",
    "aws_smsvoice",
    "aws_sns",
    "aws_sqs",
    "aws_ssm",
    "aws_ssmcontacts",
    "aws_ssmguiconnect",
    "aws_ssmincidents",
    "aws_ssmquicksetup",
    "aws_sso",
    "aws_stepfunctions",
    "aws_supportapp",
    "aws_synthetics",
    "aws_systemsmanagersap",
    "aws_timestream",
    "aws_transfer",
    "aws_verifiedpermissions",
    "aws_voiceid",
    "aws_vpclattice",
    "aws_waf",
    "aws_wafregional",
    "aws_wafv2",
    "aws_wisdom",
    "aws_workspaces",
    "aws_workspacesinstances",
    "aws_workspacesthinclient",
    "aws_workspacesweb",
    "aws_xray",
    "core",
    "mixins",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import alexa_ask
from . import aws_accessanalyzer
from . import aws_acmpca
from . import aws_aiops
from . import aws_amazonmq
from . import aws_amplify
from . import aws_amplifyuibuilder
from . import aws_apigateway
from . import aws_apigatewayv2
from . import aws_appconfig
from . import aws_appflow
from . import aws_appintegrations
from . import aws_applicationautoscaling
from . import aws_applicationinsights
from . import aws_applicationsignals
from . import aws_appmesh
from . import aws_apprunner
from . import aws_appstream
from . import aws_appsync
from . import aws_apptest
from . import aws_aps
from . import aws_arcregionswitch
from . import aws_arczonalshift
from . import aws_athena
from . import aws_auditmanager
from . import aws_autoscaling
from . import aws_autoscalingplans
from . import aws_b2bi
from . import aws_backup
from . import aws_backupgateway
from . import aws_batch
from . import aws_bcmdataexports
from . import aws_bedrock
from . import aws_bedrockagentcore
from . import aws_billingconductor
from . import aws_budgets
from . import aws_cassandra
from . import aws_ce
from . import aws_certificatemanager
from . import aws_chatbot
from . import aws_cleanrooms
from . import aws_cleanroomsml
from . import aws_cloud9
from . import aws_cloudformation
from . import aws_cloudfront
from . import aws_cloudtrail
from . import aws_cloudwatch
from . import aws_codeartifact
from . import aws_codebuild
from . import aws_codecommit
from . import aws_codeconnections
from . import aws_codedeploy
from . import aws_codeguruprofiler
from . import aws_codegurureviewer
from . import aws_codepipeline
from . import aws_codestar
from . import aws_codestarconnections
from . import aws_codestarnotifications
from . import aws_cognito
from . import aws_comprehend
from . import aws_config
from . import aws_connect
from . import aws_connectcampaigns
from . import aws_connectcampaignsv2
from . import aws_controltower
from . import aws_cur
from . import aws_customerprofiles
from . import aws_databrew
from . import aws_datapipeline
from . import aws_datasync
from . import aws_datazone
from . import aws_dax
from . import aws_deadline
from . import aws_detective
from . import aws_devicefarm
from . import aws_devopsagent
from . import aws_devopsguru
from . import aws_directoryservice
from . import aws_dlm
from . import aws_dms
from . import aws_docdb
from . import aws_docdbelastic
from . import aws_dsql
from . import aws_dynamodb
from . import aws_ec2
from . import aws_ecr
from . import aws_ecs
from . import aws_efs
from . import aws_eks
from . import aws_elasticache
from . import aws_elasticbeanstalk
from . import aws_elasticloadbalancing
from . import aws_elasticloadbalancingv2
from . import aws_elasticsearch
from . import aws_emr
from . import aws_emrcontainers
from . import aws_emrserverless
from . import aws_entityresolution
from . import aws_eventschemas
from . import aws_evidently
from . import aws_evs
from . import aws_finspace
from . import aws_fis
from . import aws_fms
from . import aws_forecast
from . import aws_frauddetector
from . import aws_fsx
from . import aws_gamelift
from . import aws_gameliftstreams
from . import aws_globalaccelerator
from . import aws_glue
from . import aws_grafana
from . import aws_greengrass
from . import aws_greengrassv2
from . import aws_groundstation
from . import aws_guardduty
from . import aws_healthimaging
from . import aws_healthlake
from . import aws_iam
from . import aws_identitystore
from . import aws_imagebuilder
from . import aws_inspector
from . import aws_inspectorv2
from . import aws_internetmonitor
from . import aws_invoicing
from . import aws_iot
from . import aws_iotanalytics
from . import aws_iotcoredeviceadvisor
from . import aws_iotevents
from . import aws_iotfleethub
from . import aws_iotfleetwise
from . import aws_iotsitewise
from . import aws_iotthingsgraph
from . import aws_iottwinmaker
from . import aws_iotwireless
from . import aws_ivs
from . import aws_ivschat
from . import aws_kafkaconnect
from . import aws_kendra
from . import aws_kendraranking
from . import aws_kinesis
from . import aws_kinesisanalytics
from . import aws_kinesisanalyticsv2
from . import aws_kinesisfirehose
from . import aws_kinesisvideo
from . import aws_kms
from . import aws_lakeformation
from . import aws_lambda
from . import aws_launchwizard
from . import aws_lex
from . import aws_licensemanager
from . import aws_lightsail
from . import aws_location
from . import aws_logs
from . import aws_lookoutequipment
from . import aws_lookoutmetrics
from . import aws_lookoutvision
from . import aws_m2
from . import aws_macie
from . import aws_managedblockchain
from . import aws_mediaconnect
from . import aws_mediaconvert
from . import aws_medialive
from . import aws_mediapackage
from . import aws_mediapackagev2
from . import aws_mediastore
from . import aws_mediatailor
from . import aws_memorydb
from . import aws_mpa
from . import aws_msk
from . import aws_mwaa
from . import aws_neptune
from . import aws_neptunegraph
from . import aws_networkfirewall
from . import aws_networkmanager
from . import aws_nimblestudio
from . import aws_notifications
from . import aws_notificationscontacts
from . import aws_oam
from . import aws_observabilityadmin
from . import aws_odb
from . import aws_omics
from . import aws_opensearchserverless
from . import aws_opensearchservice
from . import aws_opsworks
from . import aws_opsworkscm
from . import aws_organizations
from . import aws_osis
from . import aws_panorama
from . import aws_paymentcryptography
from . import aws_pcaconnectorad
from . import aws_pcaconnectorscep
from . import aws_pcs
from . import aws_personalize
from . import aws_pinpoint
from . import aws_pinpointemail
from . import aws_pipes
from . import aws_proton
from . import aws_qbusiness
from . import aws_qldb
from . import aws_quicksight
from . import aws_ram
from . import aws_rbin
from . import aws_rds
from . import aws_redshift
from . import aws_redshiftserverless
from . import aws_refactorspaces
from . import aws_rekognition
from . import aws_resiliencehub
from . import aws_resourceexplorer2
from . import aws_resourcegroups
from . import aws_robomaker
from . import aws_rolesanywhere
from . import aws_route53
from . import aws_route53profiles
from . import aws_route53recoverycontrol
from . import aws_route53recoveryreadiness
from . import aws_route53resolver
from . import aws_rtbfabric
from . import aws_rum
from . import aws_s3
from . import aws_s3express
from . import aws_s3objectlambda
from . import aws_s3outposts
from . import aws_s3tables
from . import aws_s3vectors
from . import aws_sagemaker
from . import aws_sam
from . import aws_scheduler
from . import aws_sdb
from . import aws_secretsmanager
from . import aws_securityhub
from . import aws_securitylake
from . import aws_servicecatalog
from . import aws_servicecatalogappregistry
from . import aws_servicediscovery
from . import aws_ses
from . import aws_shield
from . import aws_signer
from . import aws_simspaceweaver
from . import aws_smsvoice
from . import aws_sns
from . import aws_sqs
from . import aws_ssm
from . import aws_ssmcontacts
from . import aws_ssmguiconnect
from . import aws_ssmincidents
from . import aws_ssmquicksetup
from . import aws_sso
from . import aws_stepfunctions
from . import aws_supportapp
from . import aws_synthetics
from . import aws_systemsmanagersap
from . import aws_timestream
from . import aws_transfer
from . import aws_verifiedpermissions
from . import aws_voiceid
from . import aws_vpclattice
from . import aws_waf
from . import aws_wafregional
from . import aws_wafv2
from . import aws_wisdom
from . import aws_workspaces
from . import aws_workspacesinstances
from . import aws_workspacesthinclient
from . import aws_workspacesweb
from . import aws_xray
from . import core
from . import mixins
