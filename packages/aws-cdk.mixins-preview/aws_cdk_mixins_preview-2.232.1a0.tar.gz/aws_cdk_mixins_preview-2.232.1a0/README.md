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
