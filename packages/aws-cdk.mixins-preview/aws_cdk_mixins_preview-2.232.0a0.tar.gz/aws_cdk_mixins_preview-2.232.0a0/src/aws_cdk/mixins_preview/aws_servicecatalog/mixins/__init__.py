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
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnAcceptedPortfolioShareMixinProps",
    jsii_struct_bases=[],
    name_mapping={"accept_language": "acceptLanguage", "portfolio_id": "portfolioId"},
)
class CfnAcceptedPortfolioShareMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        portfolio_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAcceptedPortfolioSharePropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param portfolio_id: The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_accepted_portfolio_share_mixin_props = servicecatalog_mixins.CfnAcceptedPortfolioShareMixinProps(
                accept_language="acceptLanguage",
                portfolio_id="portfolioId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acee4d5260b522d899bae2d902ce569b889910929361c87bbaa7d88da6a37404)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if portfolio_id is not None:
            self._values["portfolio_id"] = portfolio_id

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html#cfn-servicecatalog-acceptedportfolioshare-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html#cfn-servicecatalog-acceptedportfolioshare-portfolioid
        '''
        result = self._values.get("portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAcceptedPortfolioShareMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAcceptedPortfolioSharePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnAcceptedPortfolioSharePropsMixin",
):
    '''Accepts an offer to share the specified portfolio.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-acceptedportfolioshare.html
    :cloudformationResource: AWS::ServiceCatalog::AcceptedPortfolioShare
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_accepted_portfolio_share_props_mixin = servicecatalog_mixins.CfnAcceptedPortfolioSharePropsMixin(servicecatalog_mixins.CfnAcceptedPortfolioShareMixinProps(
            accept_language="acceptLanguage",
            portfolio_id="portfolioId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAcceptedPortfolioShareMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::AcceptedPortfolioShare``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5256b486888764640f45b07a950cd5d5db9a1895cac58f71622f3eabbd4cb07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56cb9419abd6b9f2f4695b7525d7955e25b97891ed1de6b3d918b5063ce2bbe2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f617dccebc59471c7d280aec8d7eb4099d3cc5432e0bc5f6ddb606e0307df25)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAcceptedPortfolioShareMixinProps:
        return typing.cast(CfnAcceptedPortfolioShareMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProductMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "description": "description",
        "distributor": "distributor",
        "name": "name",
        "owner": "owner",
        "product_type": "productType",
        "provisioning_artifact_parameters": "provisioningArtifactParameters",
        "replace_provisioning_artifacts": "replaceProvisioningArtifacts",
        "source_connection": "sourceConnection",
        "support_description": "supportDescription",
        "support_email": "supportEmail",
        "support_url": "supportUrl",
        "tags": "tags",
    },
)
class CfnCloudFormationProductMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        distributor: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
        product_type: typing.Optional[builtins.str] = None,
        provisioning_artifact_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudFormationProductPropsMixin.ProvisioningArtifactPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        replace_provisioning_artifacts: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        source_connection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudFormationProductPropsMixin.SourceConnectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        support_description: typing.Optional[builtins.str] = None,
        support_email: typing.Optional[builtins.str] = None,
        support_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCloudFormationProductPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the product.
        :param distributor: The distributor of the product.
        :param name: The name of the product.
        :param owner: The owner of the product.
        :param product_type: The type of product.
        :param provisioning_artifact_parameters: The configuration of the provisioning artifact (also known as a version).
        :param replace_provisioning_artifacts: This property is turned off by default. If turned off, you can update provisioning artifacts or product attributes (such as description, distributor, name, owner, and more) and the associated provisioning artifacts will retain the same unique identifier. Provisioning artifacts are matched within the CloudFormationProduct resource, and only those that have been updated will be changed. Provisioning artifacts are matched by a combinaton of provisioning artifact template URL and name. If turned on, provisioning artifacts will be given a new unique identifier when you update the product or provisioning artifacts.
        :param source_connection: A top level ``ProductViewDetail`` response containing details about the product’s connection. AWS Service Catalog returns this field for the ``CreateProduct`` , ``UpdateProduct`` , ``DescribeProductAsAdmin`` , and ``SearchProductAsAdmin`` APIs. This response contains the same fields as the ``ConnectionParameters`` request, with the addition of the ``LastSync`` response.
        :param support_description: The support information about the product.
        :param support_email: The contact email for product support.
        :param support_url: The contact URL for product support. ``^https?:\\/\\//`` / is the pattern used to validate SupportUrl.
        :param tags: One or more tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            # info: Any
            
            cfn_cloud_formation_product_mixin_props = servicecatalog_mixins.CfnCloudFormationProductMixinProps(
                accept_language="acceptLanguage",
                description="description",
                distributor="distributor",
                name="name",
                owner="owner",
                product_type="productType",
                provisioning_artifact_parameters=[servicecatalog_mixins.CfnCloudFormationProductPropsMixin.ProvisioningArtifactPropertiesProperty(
                    description="description",
                    disable_template_validation=False,
                    info=info,
                    name="name",
                    type="type"
                )],
                replace_provisioning_artifacts=False,
                source_connection=servicecatalog_mixins.CfnCloudFormationProductPropsMixin.SourceConnectionProperty(
                    connection_parameters=servicecatalog_mixins.CfnCloudFormationProductPropsMixin.ConnectionParametersProperty(
                        code_star=servicecatalog_mixins.CfnCloudFormationProductPropsMixin.CodeStarParametersProperty(
                            artifact_path="artifactPath",
                            branch="branch",
                            connection_arn="connectionArn",
                            repository="repository"
                        )
                    ),
                    type="type"
                ),
                support_description="supportDescription",
                support_email="supportEmail",
                support_url="supportUrl",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a3ab93af8d58dd3608cd11523a8896e1de949363593343329f551092e07b5f)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument distributor", value=distributor, expected_type=type_hints["distributor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument product_type", value=product_type, expected_type=type_hints["product_type"])
            check_type(argname="argument provisioning_artifact_parameters", value=provisioning_artifact_parameters, expected_type=type_hints["provisioning_artifact_parameters"])
            check_type(argname="argument replace_provisioning_artifacts", value=replace_provisioning_artifacts, expected_type=type_hints["replace_provisioning_artifacts"])
            check_type(argname="argument source_connection", value=source_connection, expected_type=type_hints["source_connection"])
            check_type(argname="argument support_description", value=support_description, expected_type=type_hints["support_description"])
            check_type(argname="argument support_email", value=support_email, expected_type=type_hints["support_email"])
            check_type(argname="argument support_url", value=support_url, expected_type=type_hints["support_url"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description
        if distributor is not None:
            self._values["distributor"] = distributor
        if name is not None:
            self._values["name"] = name
        if owner is not None:
            self._values["owner"] = owner
        if product_type is not None:
            self._values["product_type"] = product_type
        if provisioning_artifact_parameters is not None:
            self._values["provisioning_artifact_parameters"] = provisioning_artifact_parameters
        if replace_provisioning_artifacts is not None:
            self._values["replace_provisioning_artifacts"] = replace_provisioning_artifacts
        if source_connection is not None:
            self._values["source_connection"] = source_connection
        if support_description is not None:
            self._values["support_description"] = support_description
        if support_email is not None:
            self._values["support_email"] = support_email
        if support_url is not None:
            self._values["support_url"] = support_url
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the product.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distributor(self) -> typing.Optional[builtins.str]:
        '''The distributor of the product.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-distributor
        '''
        result = self._values.get("distributor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the product.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        '''The owner of the product.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-owner
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_type(self) -> typing.Optional[builtins.str]:
        '''The type of product.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-producttype
        '''
        result = self._values.get("product_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_artifact_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProductPropsMixin.ProvisioningArtifactPropertiesProperty"]]]]:
        '''The configuration of the provisioning artifact (also known as a version).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactparameters
        '''
        result = self._values.get("provisioning_artifact_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProductPropsMixin.ProvisioningArtifactPropertiesProperty"]]]], result)

    @builtins.property
    def replace_provisioning_artifacts(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''This property is turned off by default.

        If turned off, you can update provisioning artifacts or product attributes (such as description, distributor, name, owner, and more) and the associated provisioning artifacts will retain the same unique identifier. Provisioning artifacts are matched within the CloudFormationProduct resource, and only those that have been updated will be changed. Provisioning artifacts are matched by a combinaton of provisioning artifact template URL and name.

        If turned on, provisioning artifacts will be given a new unique identifier when you update the product or provisioning artifacts.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-replaceprovisioningartifacts
        '''
        result = self._values.get("replace_provisioning_artifacts")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def source_connection(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProductPropsMixin.SourceConnectionProperty"]]:
        '''A top level ``ProductViewDetail`` response containing details about the product’s connection.

        AWS Service Catalog returns this field for the ``CreateProduct`` , ``UpdateProduct`` , ``DescribeProductAsAdmin`` , and ``SearchProductAsAdmin`` APIs. This response contains the same fields as the ``ConnectionParameters`` request, with the addition of the ``LastSync`` response.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-sourceconnection
        '''
        result = self._values.get("source_connection")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProductPropsMixin.SourceConnectionProperty"]], result)

    @builtins.property
    def support_description(self) -> typing.Optional[builtins.str]:
        '''The support information about the product.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supportdescription
        '''
        result = self._values.get("support_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_email(self) -> typing.Optional[builtins.str]:
        '''The contact email for product support.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supportemail
        '''
        result = self._values.get("support_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def support_url(self) -> typing.Optional[builtins.str]:
        '''The contact URL for product support.

        ``^https?:\\/\\//`` / is the pattern used to validate SupportUrl.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-supporturl
        '''
        result = self._values.get("support_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html#cfn-servicecatalog-cloudformationproduct-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCloudFormationProductMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCloudFormationProductPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProductPropsMixin",
):
    '''Specifies a product.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationproduct.html
    :cloudformationResource: AWS::ServiceCatalog::CloudFormationProduct
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        # info: Any
        
        cfn_cloud_formation_product_props_mixin = servicecatalog_mixins.CfnCloudFormationProductPropsMixin(servicecatalog_mixins.CfnCloudFormationProductMixinProps(
            accept_language="acceptLanguage",
            description="description",
            distributor="distributor",
            name="name",
            owner="owner",
            product_type="productType",
            provisioning_artifact_parameters=[servicecatalog_mixins.CfnCloudFormationProductPropsMixin.ProvisioningArtifactPropertiesProperty(
                description="description",
                disable_template_validation=False,
                info=info,
                name="name",
                type="type"
            )],
            replace_provisioning_artifacts=False,
            source_connection=servicecatalog_mixins.CfnCloudFormationProductPropsMixin.SourceConnectionProperty(
                connection_parameters=servicecatalog_mixins.CfnCloudFormationProductPropsMixin.ConnectionParametersProperty(
                    code_star=servicecatalog_mixins.CfnCloudFormationProductPropsMixin.CodeStarParametersProperty(
                        artifact_path="artifactPath",
                        branch="branch",
                        connection_arn="connectionArn",
                        repository="repository"
                    )
                ),
                type="type"
            ),
            support_description="supportDescription",
            support_email="supportEmail",
            support_url="supportUrl",
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
        props: typing.Union[CfnCloudFormationProductMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::CloudFormationProduct``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c84f62505ba849f783fbc6dc002943230d9cef270cf5ebc8e38caed4ba5c89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e7c6dbd54ff60347c671aaa0104529ea8705cbb65e5effe2ee1ba57b301b15c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd691e0cd3f911f738282ea8d73cbb86ece8af622ccebcd1c1b7d16d55c90785)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCloudFormationProductMixinProps:
        return typing.cast(CfnCloudFormationProductMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProductPropsMixin.CodeStarParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "artifact_path": "artifactPath",
            "branch": "branch",
            "connection_arn": "connectionArn",
            "repository": "repository",
        },
    )
    class CodeStarParametersProperty:
        def __init__(
            self,
            *,
            artifact_path: typing.Optional[builtins.str] = None,
            branch: typing.Optional[builtins.str] = None,
            connection_arn: typing.Optional[builtins.str] = None,
            repository: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The subtype containing details about the Codestar connection ``Type`` .

            :param artifact_path: The absolute path wehre the artifact resides within the repo and branch, formatted as "folder/file.json.".
            :param branch: The specific branch where the artifact resides.
            :param connection_arn: The CodeStar ARN, which is the connection between AWS Service Catalog and the external repository.
            :param repository: The specific repository where the product’s artifact-to-be-synced resides, formatted as "Account/Repo.".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-codestarparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
                
                code_star_parameters_property = servicecatalog_mixins.CfnCloudFormationProductPropsMixin.CodeStarParametersProperty(
                    artifact_path="artifactPath",
                    branch="branch",
                    connection_arn="connectionArn",
                    repository="repository"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9375600b6cf17c416e07d8de93adeac5ac615c16666f4e012481ddd09d7b8c06)
                check_type(argname="argument artifact_path", value=artifact_path, expected_type=type_hints["artifact_path"])
                check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
                check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
                check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if artifact_path is not None:
                self._values["artifact_path"] = artifact_path
            if branch is not None:
                self._values["branch"] = branch
            if connection_arn is not None:
                self._values["connection_arn"] = connection_arn
            if repository is not None:
                self._values["repository"] = repository

        @builtins.property
        def artifact_path(self) -> typing.Optional[builtins.str]:
            '''The absolute path wehre the artifact resides within the repo and branch, formatted as "folder/file.json.".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-codestarparameters.html#cfn-servicecatalog-cloudformationproduct-codestarparameters-artifactpath
            '''
            result = self._values.get("artifact_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def branch(self) -> typing.Optional[builtins.str]:
            '''The specific branch where the artifact resides.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-codestarparameters.html#cfn-servicecatalog-cloudformationproduct-codestarparameters-branch
            '''
            result = self._values.get("branch")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connection_arn(self) -> typing.Optional[builtins.str]:
            '''The CodeStar ARN, which is the connection between AWS Service Catalog and the external repository.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-codestarparameters.html#cfn-servicecatalog-cloudformationproduct-codestarparameters-connectionarn
            '''
            result = self._values.get("connection_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def repository(self) -> typing.Optional[builtins.str]:
            '''The specific repository where the product’s artifact-to-be-synced resides, formatted as "Account/Repo.".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-codestarparameters.html#cfn-servicecatalog-cloudformationproduct-codestarparameters-repository
            '''
            result = self._values.get("repository")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeStarParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProductPropsMixin.ConnectionParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"code_star": "codeStar"},
    )
    class ConnectionParametersProperty:
        def __init__(
            self,
            *,
            code_star: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudFormationProductPropsMixin.CodeStarParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides connection details.

            :param code_star: Provides ``ConnectionType`` details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-connectionparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
                
                connection_parameters_property = servicecatalog_mixins.CfnCloudFormationProductPropsMixin.ConnectionParametersProperty(
                    code_star=servicecatalog_mixins.CfnCloudFormationProductPropsMixin.CodeStarParametersProperty(
                        artifact_path="artifactPath",
                        branch="branch",
                        connection_arn="connectionArn",
                        repository="repository"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8709a70141cb0d5514b6dad896ead17ce19a03aff10a4e255c7bf09bf1ee475b)
                check_type(argname="argument code_star", value=code_star, expected_type=type_hints["code_star"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code_star is not None:
                self._values["code_star"] = code_star

        @builtins.property
        def code_star(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProductPropsMixin.CodeStarParametersProperty"]]:
            '''Provides ``ConnectionType`` details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-connectionparameters.html#cfn-servicecatalog-cloudformationproduct-connectionparameters-codestar
            '''
            result = self._values.get("code_star")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProductPropsMixin.CodeStarParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProductPropsMixin.ProvisioningArtifactPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "disable_template_validation": "disableTemplateValidation",
            "info": "info",
            "name": "name",
            "type": "type",
        },
    )
    class ProvisioningArtifactPropertiesProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            disable_template_validation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            info: typing.Any = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a provisioning artifact (also known as a version) for a product.

            :param description: The description of the provisioning artifact, including how it differs from the previous provisioning artifact.
            :param disable_template_validation: If set to true, AWS Service Catalog stops validating the specified provisioning artifact even if it is invalid.
            :param info: Specify the template source with one of the following options, but not both. Keys accepted: [ ``LoadTemplateFromURL`` , ``ImportFromPhysicalId`` ] The URL of the AWS CloudFormation template in Amazon S3 in JSON format. Specify the URL in JSON format as follows: ``"LoadTemplateFromURL": "https://s3.amazonaws.com/cf-templates-ozkq9d3hgiq2-us-east-1/..."`` ``ImportFromPhysicalId`` : The physical id of the resource that contains the template. Currently only supports AWS CloudFormation stack arn. Specify the physical id in JSON format as follows: ``ImportFromPhysicalId: “arn:aws:cloudformation:[us-east-1]:[accountId]:stack/[StackName]/[resourceId]``
            :param name: The name of the provisioning artifact (for example, v1 v2beta). No spaces are allowed.
            :param type: The type of provisioning artifact. - ``CLOUD_FORMATION_TEMPLATE`` - AWS CloudFormation template - ``TERRAFORM_OPEN_SOURCE`` - Terraform Open Source configuration file - ``TERRAFORM_CLOUD`` - Terraform Cloud configuration file - ``EXTERNAL`` - External configuration file

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
                
                # info: Any
                
                provisioning_artifact_properties_property = servicecatalog_mixins.CfnCloudFormationProductPropsMixin.ProvisioningArtifactPropertiesProperty(
                    description="description",
                    disable_template_validation=False,
                    info=info,
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54ff8178bae2564a4e820a28aec93adac4a21627b2d9cd42e76a4558d8ee615d)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument disable_template_validation", value=disable_template_validation, expected_type=type_hints["disable_template_validation"])
                check_type(argname="argument info", value=info, expected_type=type_hints["info"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if disable_template_validation is not None:
                self._values["disable_template_validation"] = disable_template_validation
            if info is not None:
                self._values["info"] = info
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the provisioning artifact, including how it differs from the previous provisioning artifact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disable_template_validation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If set to true, AWS Service Catalog stops validating the specified provisioning artifact even if it is invalid.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-disabletemplatevalidation
            '''
            result = self._values.get("disable_template_validation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def info(self) -> typing.Any:
            '''Specify the template source with one of the following options, but not both.

            Keys accepted: [ ``LoadTemplateFromURL`` , ``ImportFromPhysicalId`` ]

            The URL of the AWS CloudFormation template in Amazon S3 in JSON format. Specify the URL in JSON format as follows:

            ``"LoadTemplateFromURL": "https://s3.amazonaws.com/cf-templates-ozkq9d3hgiq2-us-east-1/..."``

            ``ImportFromPhysicalId`` : The physical id of the resource that contains the template. Currently only supports AWS CloudFormation stack arn. Specify the physical id in JSON format as follows: ``ImportFromPhysicalId: “arn:aws:cloudformation:[us-east-1]:[accountId]:stack/[StackName]/[resourceId]``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-info
            '''
            result = self._values.get("info")
            return typing.cast(typing.Any, result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the provisioning artifact (for example, v1 v2beta).

            No spaces are allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of provisioning artifact.

            - ``CLOUD_FORMATION_TEMPLATE`` - AWS CloudFormation template
            - ``TERRAFORM_OPEN_SOURCE`` - Terraform Open Source configuration file
            - ``TERRAFORM_CLOUD`` - Terraform Cloud configuration file
            - ``EXTERNAL`` - External configuration file

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-provisioningartifactproperties.html#cfn-servicecatalog-cloudformationproduct-provisioningartifactproperties-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisioningArtifactPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProductPropsMixin.SourceConnectionProperty",
        jsii_struct_bases=[],
        name_mapping={"connection_parameters": "connectionParameters", "type": "type"},
    )
    class SourceConnectionProperty:
        def __init__(
            self,
            *,
            connection_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudFormationProductPropsMixin.ConnectionParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A top level ``ProductViewDetail`` response containing details about the product’s connection.

            AWS Service Catalog returns this field for the ``CreateProduct`` , ``UpdateProduct`` , ``DescribeProductAsAdmin`` , and ``SearchProductAsAdmin`` APIs. This response contains the same fields as the ``ConnectionParameters`` request, with the addition of the ``LastSync`` response.

            :param connection_parameters: The connection details based on the connection ``Type`` .
            :param type: The only supported ``SourceConnection`` type is Codestar.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-sourceconnection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
                
                source_connection_property = servicecatalog_mixins.CfnCloudFormationProductPropsMixin.SourceConnectionProperty(
                    connection_parameters=servicecatalog_mixins.CfnCloudFormationProductPropsMixin.ConnectionParametersProperty(
                        code_star=servicecatalog_mixins.CfnCloudFormationProductPropsMixin.CodeStarParametersProperty(
                            artifact_path="artifactPath",
                            branch="branch",
                            connection_arn="connectionArn",
                            repository="repository"
                        )
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f484e9e75ee9ba93a62175665325f982dcf65414fb0270d9833d706856b5f5f9)
                check_type(argname="argument connection_parameters", value=connection_parameters, expected_type=type_hints["connection_parameters"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_parameters is not None:
                self._values["connection_parameters"] = connection_parameters
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def connection_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProductPropsMixin.ConnectionParametersProperty"]]:
            '''The connection details based on the connection ``Type`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-sourceconnection.html#cfn-servicecatalog-cloudformationproduct-sourceconnection-connectionparameters
            '''
            result = self._values.get("connection_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProductPropsMixin.ConnectionParametersProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The only supported ``SourceConnection`` type is Codestar.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationproduct-sourceconnection.html#cfn-servicecatalog-cloudformationproduct-sourceconnection-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConnectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProvisionedProductMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "notification_arns": "notificationArns",
        "path_id": "pathId",
        "path_name": "pathName",
        "product_id": "productId",
        "product_name": "productName",
        "provisioned_product_name": "provisionedProductName",
        "provisioning_artifact_id": "provisioningArtifactId",
        "provisioning_artifact_name": "provisioningArtifactName",
        "provisioning_parameters": "provisioningParameters",
        "provisioning_preferences": "provisioningPreferences",
        "tags": "tags",
    },
)
class CfnCloudFormationProvisionedProductMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path_id: typing.Optional[builtins.str] = None,
        path_name: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        product_name: typing.Optional[builtins.str] = None,
        provisioned_product_name: typing.Optional[builtins.str] = None,
        provisioning_artifact_id: typing.Optional[builtins.str] = None,
        provisioning_artifact_name: typing.Optional[builtins.str] = None,
        provisioning_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudFormationProvisionedProductPropsMixin.ProvisioningParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        provisioning_preferences: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCloudFormationProvisionedProductPropsMixin.ProvisioningPreferencesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCloudFormationProvisionedProductPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param notification_arns: Passed to AWS CloudFormation . The SNS topic ARNs to which to publish stack-related events.
        :param path_id: The path identifier of the product. This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ . .. epigraph:: You must provide the name or ID, but not both.
        :param path_name: The name of the path. This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ . .. epigraph:: You must provide the name or ID, but not both.
        :param product_id: The product identifier. .. epigraph:: You must specify either the ID or the name of the product, but not both.
        :param product_name: The name of the Service Catalog product. Each time a stack is created or updated, if ``ProductName`` is provided it will successfully resolve to ``ProductId`` as long as only one product exists in the account or Region with that ``ProductName`` . .. epigraph:: You must specify either the name or the ID of the product, but not both.
        :param provisioned_product_name: A user-friendly name for the provisioned product. This value must be unique for the AWS account and cannot be updated after the product is provisioned.
        :param provisioning_artifact_id: The identifier of the provisioning artifact (also known as a version). .. epigraph:: You must specify either the ID or the name of the provisioning artifact, but not both.
        :param provisioning_artifact_name: The name of the provisioning artifact (also known as a version) for the product. This name must be unique for the product. .. epigraph:: You must specify either the name or the ID of the provisioning artifact, but not both. You must also specify either the name or the ID of the product, but not both.
        :param provisioning_parameters: Parameters specified by the administrator that are required for provisioning the product.
        :param provisioning_preferences: StackSet preferences that are required for provisioning the product or updating a provisioned product.
        :param tags: One or more tags. .. epigraph:: Requires the provisioned product to have an `ResourceUpdateConstraint <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html>`_ resource with ``TagUpdatesOnProvisionedProduct`` set to ``ALLOWED`` to allow tag updates. If ``RESOURCE_UPDATE`` constraint is not present, tags updates are ignored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_cloud_formation_provisioned_product_mixin_props = servicecatalog_mixins.CfnCloudFormationProvisionedProductMixinProps(
                accept_language="acceptLanguage",
                notification_arns=["notificationArns"],
                path_id="pathId",
                path_name="pathName",
                product_id="productId",
                product_name="productName",
                provisioned_product_name="provisionedProductName",
                provisioning_artifact_id="provisioningArtifactId",
                provisioning_artifact_name="provisioningArtifactName",
                provisioning_parameters=[servicecatalog_mixins.CfnCloudFormationProvisionedProductPropsMixin.ProvisioningParameterProperty(
                    key="key",
                    value="value"
                )],
                provisioning_preferences=servicecatalog_mixins.CfnCloudFormationProvisionedProductPropsMixin.ProvisioningPreferencesProperty(
                    stack_set_accounts=["stackSetAccounts"],
                    stack_set_failure_tolerance_count=123,
                    stack_set_failure_tolerance_percentage=123,
                    stack_set_max_concurrency_count=123,
                    stack_set_max_concurrency_percentage=123,
                    stack_set_operation_type="stackSetOperationType",
                    stack_set_regions=["stackSetRegions"]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a3c60b859967614b29db4e436971a886b332f0ca647bc51c6ba75fe0e92fcb)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument path_id", value=path_id, expected_type=type_hints["path_id"])
            check_type(argname="argument path_name", value=path_name, expected_type=type_hints["path_name"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument product_name", value=product_name, expected_type=type_hints["product_name"])
            check_type(argname="argument provisioned_product_name", value=provisioned_product_name, expected_type=type_hints["provisioned_product_name"])
            check_type(argname="argument provisioning_artifact_id", value=provisioning_artifact_id, expected_type=type_hints["provisioning_artifact_id"])
            check_type(argname="argument provisioning_artifact_name", value=provisioning_artifact_name, expected_type=type_hints["provisioning_artifact_name"])
            check_type(argname="argument provisioning_parameters", value=provisioning_parameters, expected_type=type_hints["provisioning_parameters"])
            check_type(argname="argument provisioning_preferences", value=provisioning_preferences, expected_type=type_hints["provisioning_preferences"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if path_id is not None:
            self._values["path_id"] = path_id
        if path_name is not None:
            self._values["path_name"] = path_name
        if product_id is not None:
            self._values["product_id"] = product_id
        if product_name is not None:
            self._values["product_name"] = product_name
        if provisioned_product_name is not None:
            self._values["provisioned_product_name"] = provisioned_product_name
        if provisioning_artifact_id is not None:
            self._values["provisioning_artifact_id"] = provisioning_artifact_id
        if provisioning_artifact_name is not None:
            self._values["provisioning_artifact_name"] = provisioning_artifact_name
        if provisioning_parameters is not None:
            self._values["provisioning_parameters"] = provisioning_parameters
        if provisioning_preferences is not None:
            self._values["provisioning_preferences"] = provisioning_preferences
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Passed to AWS CloudFormation .

        The SNS topic ARNs to which to publish stack-related events.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-notificationarns
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path_id(self) -> typing.Optional[builtins.str]:
        '''The path identifier of the product.

        This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ .
        .. epigraph::

           You must provide the name or ID, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-pathid
        '''
        result = self._values.get("path_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_name(self) -> typing.Optional[builtins.str]:
        '''The name of the path.

        This value is optional if the product has a default path, and required if the product has more than one path. To list the paths for a product, use `ListLaunchPaths <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_ListLaunchPaths.html>`_ .
        .. epigraph::

           You must provide the name or ID, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-pathname
        '''
        result = self._values.get("path_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        .. epigraph::

           You must specify either the ID or the name of the product, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Service Catalog product.

        Each time a stack is created or updated, if ``ProductName`` is provided it will successfully resolve to ``ProductId`` as long as only one product exists in the account or Region with that ``ProductName`` .
        .. epigraph::

           You must specify either the name or the ID of the product, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-productname
        '''
        result = self._values.get("product_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioned_product_name(self) -> typing.Optional[builtins.str]:
        '''A user-friendly name for the provisioned product.

        This value must be unique for the AWS account and cannot be updated after the product is provisioned.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisionedproductname
        '''
        result = self._values.get("provisioned_product_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_artifact_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the provisioning artifact (also known as a version).

        .. epigraph::

           You must specify either the ID or the name of the provisioning artifact, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningartifactid
        '''
        result = self._values.get("provisioning_artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_artifact_name(self) -> typing.Optional[builtins.str]:
        '''The name of the provisioning artifact (also known as a version) for the product.

        This name must be unique for the product.
        .. epigraph::

           You must specify either the name or the ID of the provisioning artifact, but not both. You must also specify either the name or the ID of the product, but not both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningartifactname
        '''
        result = self._values.get("provisioning_artifact_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProvisionedProductPropsMixin.ProvisioningParameterProperty"]]]]:
        '''Parameters specified by the administrator that are required for provisioning the product.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameters
        '''
        result = self._values.get("provisioning_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProvisionedProductPropsMixin.ProvisioningParameterProperty"]]]], result)

    @builtins.property
    def provisioning_preferences(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProvisionedProductPropsMixin.ProvisioningPreferencesProperty"]]:
        '''StackSet preferences that are required for provisioning the product or updating a provisioned product.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences
        '''
        result = self._values.get("provisioning_preferences")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCloudFormationProvisionedProductPropsMixin.ProvisioningPreferencesProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tags.

        .. epigraph::

           Requires the provisioned product to have an `ResourceUpdateConstraint <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html>`_ resource with ``TagUpdatesOnProvisionedProduct`` set to ``ALLOWED`` to allow tag updates. If ``RESOURCE_UPDATE`` constraint is not present, tags updates are ignored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html#cfn-servicecatalog-cloudformationprovisionedproduct-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCloudFormationProvisionedProductMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCloudFormationProvisionedProductPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProvisionedProductPropsMixin",
):
    '''Provisions the specified product.

    A provisioned product is a resourced instance of a product. For example, provisioning a product based on a AWS CloudFormation template launches a AWS CloudFormation stack and its underlying resources. You can check the status of this request using `DescribeRecord <https://docs.aws.amazon.com/servicecatalog/latest/dg/API_DescribeRecord.html>`_ .

    If the request contains a tag key with an empty list of values, there is a tag conflict for that key. Do not include conflicted keys as tags, or this causes the error "Parameter validation failed: Missing required parameter in Tags[ *N* ]: *Value* ".

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html
    :cloudformationResource: AWS::ServiceCatalog::CloudFormationProvisionedProduct
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_cloud_formation_provisioned_product_props_mixin = servicecatalog_mixins.CfnCloudFormationProvisionedProductPropsMixin(servicecatalog_mixins.CfnCloudFormationProvisionedProductMixinProps(
            accept_language="acceptLanguage",
            notification_arns=["notificationArns"],
            path_id="pathId",
            path_name="pathName",
            product_id="productId",
            product_name="productName",
            provisioned_product_name="provisionedProductName",
            provisioning_artifact_id="provisioningArtifactId",
            provisioning_artifact_name="provisioningArtifactName",
            provisioning_parameters=[servicecatalog_mixins.CfnCloudFormationProvisionedProductPropsMixin.ProvisioningParameterProperty(
                key="key",
                value="value"
            )],
            provisioning_preferences=servicecatalog_mixins.CfnCloudFormationProvisionedProductPropsMixin.ProvisioningPreferencesProperty(
                stack_set_accounts=["stackSetAccounts"],
                stack_set_failure_tolerance_count=123,
                stack_set_failure_tolerance_percentage=123,
                stack_set_max_concurrency_count=123,
                stack_set_max_concurrency_percentage=123,
                stack_set_operation_type="stackSetOperationType",
                stack_set_regions=["stackSetRegions"]
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
        props: typing.Union[CfnCloudFormationProvisionedProductMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::CloudFormationProvisionedProduct``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbafc763e9f307429ee7a52b4882ea9e1d47ac4824f8ec1ce6cf03a4bae4a83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb68abac87c107da383836f1ba909ae17d3d5ccb0f94ab8a991a65e1d1c9504c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19749cfa88f9f3ffe0a9bcd2b5bb7f10f882b9233eab4b698210b0055f60a39)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCloudFormationProvisionedProductMixinProps:
        return typing.cast(CfnCloudFormationProvisionedProductMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProvisionedProductPropsMixin.ProvisioningParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ProvisioningParameterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a parameter used to provision a product.

            :param key: The parameter key.
            :param value: The parameter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
                
                provisioning_parameter_property = servicecatalog_mixins.CfnCloudFormationProvisionedProductPropsMixin.ProvisioningParameterProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0428e52a0c5faaf1cd34d222b95ca615bde85759a059ed6875993e3eac609f1d)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The parameter key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningparameter.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The parameter value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningparameter.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisioningParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnCloudFormationProvisionedProductPropsMixin.ProvisioningPreferencesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "stack_set_accounts": "stackSetAccounts",
            "stack_set_failure_tolerance_count": "stackSetFailureToleranceCount",
            "stack_set_failure_tolerance_percentage": "stackSetFailureTolerancePercentage",
            "stack_set_max_concurrency_count": "stackSetMaxConcurrencyCount",
            "stack_set_max_concurrency_percentage": "stackSetMaxConcurrencyPercentage",
            "stack_set_operation_type": "stackSetOperationType",
            "stack_set_regions": "stackSetRegions",
        },
    )
    class ProvisioningPreferencesProperty:
        def __init__(
            self,
            *,
            stack_set_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            stack_set_failure_tolerance_count: typing.Optional[jsii.Number] = None,
            stack_set_failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
            stack_set_max_concurrency_count: typing.Optional[jsii.Number] = None,
            stack_set_max_concurrency_percentage: typing.Optional[jsii.Number] = None,
            stack_set_operation_type: typing.Optional[builtins.str] = None,
            stack_set_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The user-defined preferences that will be applied when updating a provisioned product.

            Not all preferences are applicable to all provisioned product type

            One or more AWS accounts that will have access to the provisioned product.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            The AWS accounts specified should be within the list of accounts in the ``STACKSET`` constraint. To get the list of accounts in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation.

            If no values are specified, the default value is all accounts from the ``STACKSET`` constraint.

            :param stack_set_accounts: One or more AWS accounts where the provisioned product will be available. Applicable only to a ``CFN_STACKSET`` provisioned product type. The specified accounts should be within the list of accounts from the ``STACKSET`` constraint. To get the list of accounts in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation. If no values are specified, the default value is all acounts from the ``STACKSET`` constraint.
            :param stack_set_failure_tolerance_count: The number of accounts, per Region, for which this operation can fail before AWS Service Catalog stops the operation in that Region. If the operation is stopped in a Region, AWS Service Catalog doesn't attempt the operation in any subsequent Regions. Applicable only to a ``CFN_STACKSET`` provisioned product type. Conditional: You must specify either ``StackSetFailureToleranceCount`` or ``StackSetFailureTolerancePercentage`` , but not both. The default value is ``0`` if no value is specified.
            :param stack_set_failure_tolerance_percentage: The percentage of accounts, per Region, for which this stack operation can fail before AWS Service Catalog stops the operation in that Region. If the operation is stopped in a Region, AWS Service Catalog doesn't attempt the operation in any subsequent Regions. When calculating the number of accounts based on the specified percentage, AWS Service Catalog rounds down to the next whole number. Applicable only to a ``CFN_STACKSET`` provisioned product type. Conditional: You must specify either ``StackSetFailureToleranceCount`` or ``StackSetFailureTolerancePercentage`` , but not both.
            :param stack_set_max_concurrency_count: The maximum number of accounts in which to perform this operation at one time. This is dependent on the value of ``StackSetFailureToleranceCount`` . ``StackSetMaxConcurrentCount`` is at most one more than the ``StackSetFailureToleranceCount`` . Note that this setting lets you specify the maximum for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling. Applicable only to a ``CFN_STACKSET`` provisioned product type. Conditional: You must specify either ``StackSetMaxConcurrentCount`` or ``StackSetMaxConcurrentPercentage`` , but not both.
            :param stack_set_max_concurrency_percentage: The maximum percentage of accounts in which to perform this operation at one time. When calculating the number of accounts based on the specified percentage, AWS Service Catalog rounds down to the next whole number. This is true except in cases where rounding down would result is zero. In this case, AWS Service Catalog sets the number as ``1`` instead. Note that this setting lets you specify the maximum for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling. Applicable only to a ``CFN_STACKSET`` provisioned product type. Conditional: You must specify either ``StackSetMaxConcurrentCount`` or ``StackSetMaxConcurrentPercentage`` , but not both.
            :param stack_set_operation_type: Determines what action AWS Service Catalog performs to a stack set or a stack instance represented by the provisioned product. The default value is ``UPDATE`` if nothing is specified. Applicable only to a ``CFN_STACKSET`` provisioned product type. - **CREATE** - Creates a new stack instance in the stack set represented by the provisioned product. In this case, only new stack instances are created based on accounts and Regions; if new ProductId or ProvisioningArtifactID are passed, they will be ignored. - **UPDATE** - Updates the stack set represented by the provisioned product and also its stack instances. - **DELETE** - Deletes a stack instance in the stack set represented by the provisioned product.
            :param stack_set_regions: One or more AWS Regions where the provisioned product will be available. Applicable only to a ``CFN_STACKSET`` provisioned product type. The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation. If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
                
                provisioning_preferences_property = servicecatalog_mixins.CfnCloudFormationProvisionedProductPropsMixin.ProvisioningPreferencesProperty(
                    stack_set_accounts=["stackSetAccounts"],
                    stack_set_failure_tolerance_count=123,
                    stack_set_failure_tolerance_percentage=123,
                    stack_set_max_concurrency_count=123,
                    stack_set_max_concurrency_percentage=123,
                    stack_set_operation_type="stackSetOperationType",
                    stack_set_regions=["stackSetRegions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eca6b062091b3ce1180a936f9c775c5321ef8d8a5f968f654f067a30343b08c5)
                check_type(argname="argument stack_set_accounts", value=stack_set_accounts, expected_type=type_hints["stack_set_accounts"])
                check_type(argname="argument stack_set_failure_tolerance_count", value=stack_set_failure_tolerance_count, expected_type=type_hints["stack_set_failure_tolerance_count"])
                check_type(argname="argument stack_set_failure_tolerance_percentage", value=stack_set_failure_tolerance_percentage, expected_type=type_hints["stack_set_failure_tolerance_percentage"])
                check_type(argname="argument stack_set_max_concurrency_count", value=stack_set_max_concurrency_count, expected_type=type_hints["stack_set_max_concurrency_count"])
                check_type(argname="argument stack_set_max_concurrency_percentage", value=stack_set_max_concurrency_percentage, expected_type=type_hints["stack_set_max_concurrency_percentage"])
                check_type(argname="argument stack_set_operation_type", value=stack_set_operation_type, expected_type=type_hints["stack_set_operation_type"])
                check_type(argname="argument stack_set_regions", value=stack_set_regions, expected_type=type_hints["stack_set_regions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stack_set_accounts is not None:
                self._values["stack_set_accounts"] = stack_set_accounts
            if stack_set_failure_tolerance_count is not None:
                self._values["stack_set_failure_tolerance_count"] = stack_set_failure_tolerance_count
            if stack_set_failure_tolerance_percentage is not None:
                self._values["stack_set_failure_tolerance_percentage"] = stack_set_failure_tolerance_percentage
            if stack_set_max_concurrency_count is not None:
                self._values["stack_set_max_concurrency_count"] = stack_set_max_concurrency_count
            if stack_set_max_concurrency_percentage is not None:
                self._values["stack_set_max_concurrency_percentage"] = stack_set_max_concurrency_percentage
            if stack_set_operation_type is not None:
                self._values["stack_set_operation_type"] = stack_set_operation_type
            if stack_set_regions is not None:
                self._values["stack_set_regions"] = stack_set_regions

        @builtins.property
        def stack_set_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more AWS accounts where the provisioned product will be available.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            The specified accounts should be within the list of accounts from the ``STACKSET`` constraint. To get the list of accounts in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation.

            If no values are specified, the default value is all acounts from the ``STACKSET`` constraint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetaccounts
            '''
            result = self._values.get("stack_set_accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def stack_set_failure_tolerance_count(self) -> typing.Optional[jsii.Number]:
            '''The number of accounts, per Region, for which this operation can fail before AWS Service Catalog stops the operation in that Region.

            If the operation is stopped in a Region, AWS Service Catalog doesn't attempt the operation in any subsequent Regions.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            Conditional: You must specify either ``StackSetFailureToleranceCount`` or ``StackSetFailureTolerancePercentage`` , but not both.

            The default value is ``0`` if no value is specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetfailuretolerancecount
            '''
            result = self._values.get("stack_set_failure_tolerance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stack_set_failure_tolerance_percentage(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The percentage of accounts, per Region, for which this stack operation can fail before AWS Service Catalog stops the operation in that Region.

            If the operation is stopped in a Region, AWS Service Catalog doesn't attempt the operation in any subsequent Regions.

            When calculating the number of accounts based on the specified percentage, AWS Service Catalog rounds down to the next whole number.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            Conditional: You must specify either ``StackSetFailureToleranceCount`` or ``StackSetFailureTolerancePercentage`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetfailuretolerancepercentage
            '''
            result = self._values.get("stack_set_failure_tolerance_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stack_set_max_concurrency_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of accounts in which to perform this operation at one time.

            This is dependent on the value of ``StackSetFailureToleranceCount`` . ``StackSetMaxConcurrentCount`` is at most one more than the ``StackSetFailureToleranceCount`` .

            Note that this setting lets you specify the maximum for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            Conditional: You must specify either ``StackSetMaxConcurrentCount`` or ``StackSetMaxConcurrentPercentage`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetmaxconcurrencycount
            '''
            result = self._values.get("stack_set_max_concurrency_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stack_set_max_concurrency_percentage(self) -> typing.Optional[jsii.Number]:
            '''The maximum percentage of accounts in which to perform this operation at one time.

            When calculating the number of accounts based on the specified percentage, AWS Service Catalog rounds down to the next whole number. This is true except in cases where rounding down would result is zero. In this case, AWS Service Catalog sets the number as ``1`` instead.

            Note that this setting lets you specify the maximum for operations. For large deployments, under certain circumstances the actual number of accounts acted upon concurrently may be lower due to service throttling.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            Conditional: You must specify either ``StackSetMaxConcurrentCount`` or ``StackSetMaxConcurrentPercentage`` , but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetmaxconcurrencypercentage
            '''
            result = self._values.get("stack_set_max_concurrency_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stack_set_operation_type(self) -> typing.Optional[builtins.str]:
            '''Determines what action AWS Service Catalog performs to a stack set or a stack instance represented by the provisioned product.

            The default value is ``UPDATE`` if nothing is specified.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            - **CREATE** - Creates a new stack instance in the stack set represented by the provisioned product. In this case, only new stack instances are created based on accounts and Regions; if new ProductId or ProvisioningArtifactID are passed, they will be ignored.
            - **UPDATE** - Updates the stack set represented by the provisioned product and also its stack instances.
            - **DELETE** - Deletes a stack instance in the stack set represented by the provisioned product.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetoperationtype
            '''
            result = self._values.get("stack_set_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stack_set_regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more AWS Regions where the provisioned product will be available.

            Applicable only to a ``CFN_STACKSET`` provisioned product type.

            The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation.

            If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences.html#cfn-servicecatalog-cloudformationprovisionedproduct-provisioningpreferences-stacksetregions
            '''
            result = self._values.get("stack_set_regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisioningPreferencesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnLaunchNotificationConstraintMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "description": "description",
        "notification_arns": "notificationArns",
        "portfolio_id": "portfolioId",
        "product_id": "productId",
    },
)
class CfnLaunchNotificationConstraintMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        portfolio_id: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLaunchNotificationConstraintPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.
        :param notification_arns: The notification ARNs.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_launch_notification_constraint_mixin_props = servicecatalog_mixins.CfnLaunchNotificationConstraintMixinProps(
                accept_language="acceptLanguage",
                description="description",
                notification_arns=["notificationArns"],
                portfolio_id="portfolioId",
                product_id="productId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9de01afe621b580f37c05361f645d642211eb3a29ac81fd29938a2b3577340)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if portfolio_id is not None:
            self._values["portfolio_id"] = portfolio_id
        if product_id is not None:
            self._values["product_id"] = product_id

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The notification ARNs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-notificationarns
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html#cfn-servicecatalog-launchnotificationconstraint-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchNotificationConstraintMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLaunchNotificationConstraintPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnLaunchNotificationConstraintPropsMixin",
):
    '''Specifies a notification constraint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchnotificationconstraint.html
    :cloudformationResource: AWS::ServiceCatalog::LaunchNotificationConstraint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_launch_notification_constraint_props_mixin = servicecatalog_mixins.CfnLaunchNotificationConstraintPropsMixin(servicecatalog_mixins.CfnLaunchNotificationConstraintMixinProps(
            accept_language="acceptLanguage",
            description="description",
            notification_arns=["notificationArns"],
            portfolio_id="portfolioId",
            product_id="productId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLaunchNotificationConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::LaunchNotificationConstraint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38b748fc0c1402ee594887f55728e8cc98266c436547a827aa95faab3e04d003)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d39954853c4a1c9b99679aa6451745beca1c7ba571613a92e6513de63f801a4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fc712747cc3433ba4e05ebc5884bd4bc854eee2f775c414fb1c80744426037)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLaunchNotificationConstraintMixinProps:
        return typing.cast(CfnLaunchNotificationConstraintMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnLaunchRoleConstraintMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "description": "description",
        "local_role_name": "localRoleName",
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "role_arn": "roleArn",
    },
)
class CfnLaunchRoleConstraintMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        local_role_name: typing.Optional[builtins.str] = None,
        portfolio_id: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLaunchRoleConstraintPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.
        :param local_role_name: You are required to specify either the ``RoleArn`` or the ``LocalRoleName`` but can't use both. If you specify the ``LocalRoleName`` property, when an account uses the launch constraint, the IAM role with that name in the account will be used. This allows launch-role constraints to be account-agnostic so the administrator can create fewer resources per shared account. The given role name must exist in the account used to create the launch constraint and the account of the user who launches a product with this launch constraint.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param role_arn: The ARN of the launch role. You are required to specify ``RoleArn`` or ``LocalRoleName`` but can't use both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_launch_role_constraint_mixin_props = servicecatalog_mixins.CfnLaunchRoleConstraintMixinProps(
                accept_language="acceptLanguage",
                description="description",
                local_role_name="localRoleName",
                portfolio_id="portfolioId",
                product_id="productId",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f11ab899f7fccd39ac7a561b158d966743f0bdaa01b5c947cc1550495cc28b)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument local_role_name", value=local_role_name, expected_type=type_hints["local_role_name"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description
        if local_role_name is not None:
            self._values["local_role_name"] = local_role_name
        if portfolio_id is not None:
            self._values["portfolio_id"] = portfolio_id
        if product_id is not None:
            self._values["product_id"] = product_id
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_role_name(self) -> typing.Optional[builtins.str]:
        '''You are required to specify either the ``RoleArn`` or the ``LocalRoleName`` but can't use both.

        If you specify the ``LocalRoleName`` property, when an account uses the launch constraint, the IAM role with that name in the account will be used. This allows launch-role constraints to be account-agnostic so the administrator can create fewer resources per shared account.

        The given role name must exist in the account used to create the launch constraint and the account of the user who launches a product with this launch constraint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-localrolename
        '''
        result = self._values.get("local_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the launch role.

        You are required to specify ``RoleArn`` or ``LocalRoleName`` but can't use both.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html#cfn-servicecatalog-launchroleconstraint-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchRoleConstraintMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLaunchRoleConstraintPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnLaunchRoleConstraintPropsMixin",
):
    '''Specifies a launch constraint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchroleconstraint.html
    :cloudformationResource: AWS::ServiceCatalog::LaunchRoleConstraint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_launch_role_constraint_props_mixin = servicecatalog_mixins.CfnLaunchRoleConstraintPropsMixin(servicecatalog_mixins.CfnLaunchRoleConstraintMixinProps(
            accept_language="acceptLanguage",
            description="description",
            local_role_name="localRoleName",
            portfolio_id="portfolioId",
            product_id="productId",
            role_arn="roleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLaunchRoleConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::LaunchRoleConstraint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6efed8a69d6fd5cf922a34ff2fd3bd261fec45462456c33f1b7a74beb954a5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__007f487f4540b7ca1d3c52172f43fa011647742f7df8342d577ffafa7c789e63)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5eca57e476717391bd10970bd1f52dad247849071d28a601a9290c125e18d1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLaunchRoleConstraintMixinProps:
        return typing.cast(CfnLaunchRoleConstraintMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnLaunchTemplateConstraintMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "description": "description",
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "rules": "rules",
    },
)
class CfnLaunchTemplateConstraintMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        portfolio_id: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        rules: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLaunchTemplateConstraintPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param rules: The constraint rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_launch_template_constraint_mixin_props = servicecatalog_mixins.CfnLaunchTemplateConstraintMixinProps(
                accept_language="acceptLanguage",
                description="description",
                portfolio_id="portfolioId",
                product_id="productId",
                rules="rules"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb97b88ca06d4942f7d0607c52edb503fe6a656fd1f6809ec024037e9861bf51)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description
        if portfolio_id is not None:
            self._values["portfolio_id"] = portfolio_id
        if product_id is not None:
            self._values["product_id"] = product_id
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(self) -> typing.Optional[builtins.str]:
        '''The constraint rules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html#cfn-servicecatalog-launchtemplateconstraint-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchTemplateConstraintMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLaunchTemplateConstraintPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnLaunchTemplateConstraintPropsMixin",
):
    '''Specifies a template constraint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-launchtemplateconstraint.html
    :cloudformationResource: AWS::ServiceCatalog::LaunchTemplateConstraint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_launch_template_constraint_props_mixin = servicecatalog_mixins.CfnLaunchTemplateConstraintPropsMixin(servicecatalog_mixins.CfnLaunchTemplateConstraintMixinProps(
            accept_language="acceptLanguage",
            description="description",
            portfolio_id="portfolioId",
            product_id="productId",
            rules="rules"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLaunchTemplateConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::LaunchTemplateConstraint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3552ffac525b92bff9a465b4ee7a526fef012196244d0b24626b61b148ea16)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6424d9fc80016977e51cf5cd26870f03acfd48e58b90247552132172eed842f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a67aa26c2e80fab7c305613625c142a8d79ef5300288b920e69f4928f33fddc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLaunchTemplateConstraintMixinProps:
        return typing.cast(CfnLaunchTemplateConstraintMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnPortfolioMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "description": "description",
        "display_name": "displayName",
        "provider_name": "providerName",
        "tags": "tags",
    },
)
class CfnPortfolioMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        provider_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPortfolioPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the portfolio.
        :param display_name: The name to use for display purposes.
        :param provider_name: The name of the portfolio provider.
        :param tags: One or more tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_portfolio_mixin_props = servicecatalog_mixins.CfnPortfolioMixinProps(
                accept_language="acceptLanguage",
                description="description",
                display_name="displayName",
                provider_name="providerName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6519ea424c4d0e29026db47f05739ae96f56955756a9c4d30e369bd5c69430c7)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if provider_name is not None:
            self._values["provider_name"] = provider_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the portfolio.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name to use for display purposes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_name(self) -> typing.Optional[builtins.str]:
        '''The name of the portfolio provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-providername
        '''
        result = self._values.get("provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html#cfn-servicecatalog-portfolio-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortfolioMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnPortfolioPrincipalAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "portfolio_id": "portfolioId",
        "principal_arn": "principalArn",
        "principal_type": "principalType",
    },
)
class CfnPortfolioPrincipalAssociationMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        portfolio_id: typing.Optional[builtins.str] = None,
        principal_arn: typing.Optional[builtins.str] = None,
        principal_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPortfolioPrincipalAssociationPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param portfolio_id: The portfolio identifier.
        :param principal_arn: The ARN of the principal ( IAM user, role, or group).
        :param principal_type: The principal type. The supported values are ``IAM`` and ``IAM_PATTERN`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_portfolio_principal_association_mixin_props = servicecatalog_mixins.CfnPortfolioPrincipalAssociationMixinProps(
                accept_language="acceptLanguage",
                portfolio_id="portfolioId",
                principal_arn="principalArn",
                principal_type="principalType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cdff90d26d9d3ffb84af4c278c3e489bb2c842a2052d860075e4ff71897e23b)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument principal_arn", value=principal_arn, expected_type=type_hints["principal_arn"])
            check_type(argname="argument principal_type", value=principal_type, expected_type=type_hints["principal_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if portfolio_id is not None:
            self._values["portfolio_id"] = portfolio_id
        if principal_arn is not None:
            self._values["principal_arn"] = principal_arn
        if principal_type is not None:
            self._values["principal_type"] = principal_type

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-portfolioid
        '''
        result = self._values.get("portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the principal ( IAM user, role, or group).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-principalarn
        '''
        result = self._values.get("principal_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_type(self) -> typing.Optional[builtins.str]:
        '''The principal type.

        The supported values are ``IAM`` and ``IAM_PATTERN`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html#cfn-servicecatalog-portfolioprincipalassociation-principaltype
        '''
        result = self._values.get("principal_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortfolioPrincipalAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPortfolioPrincipalAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnPortfolioPrincipalAssociationPropsMixin",
):
    '''Associates the specified principal ARN with the specified portfolio.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioprincipalassociation.html
    :cloudformationResource: AWS::ServiceCatalog::PortfolioPrincipalAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_portfolio_principal_association_props_mixin = servicecatalog_mixins.CfnPortfolioPrincipalAssociationPropsMixin(servicecatalog_mixins.CfnPortfolioPrincipalAssociationMixinProps(
            accept_language="acceptLanguage",
            portfolio_id="portfolioId",
            principal_arn="principalArn",
            principal_type="principalType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPortfolioPrincipalAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::PortfolioPrincipalAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffff4a2d20e469130f5b820ebc5d576dd140dd6b21ed9078bd3aebe96bd96677)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2e74a224c60d0abda938dff01ad97601f5f5b8cf85802dc32f8f4cdc82533c6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c769e55bead0d92180d9c9d2c97344c44748a4ffbc62148d6b6d003e686dc26)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPortfolioPrincipalAssociationMixinProps:
        return typing.cast(CfnPortfolioPrincipalAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnPortfolioProductAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "source_portfolio_id": "sourcePortfolioId",
    },
)
class CfnPortfolioProductAssociationMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        portfolio_id: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        source_portfolio_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPortfolioProductAssociationPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param source_portfolio_id: The identifier of the source portfolio.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_portfolio_product_association_mixin_props = servicecatalog_mixins.CfnPortfolioProductAssociationMixinProps(
                accept_language="acceptLanguage",
                portfolio_id="portfolioId",
                product_id="productId",
                source_portfolio_id="sourcePortfolioId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693f06e00afb390c2b7898bdbc1707c654881d3de95f6a45d33f1b30bf8c85a8)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument source_portfolio_id", value=source_portfolio_id, expected_type=type_hints["source_portfolio_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if portfolio_id is not None:
            self._values["portfolio_id"] = portfolio_id
        if product_id is not None:
            self._values["product_id"] = product_id
        if source_portfolio_id is not None:
            self._values["source_portfolio_id"] = source_portfolio_id

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-portfolioid
        '''
        result = self._values.get("portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the source portfolio.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html#cfn-servicecatalog-portfolioproductassociation-sourceportfolioid
        '''
        result = self._values.get("source_portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortfolioProductAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPortfolioProductAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnPortfolioProductAssociationPropsMixin",
):
    '''Associates the specified product with the specified portfolio.

    A delegated admin is authorized to invoke this command.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioproductassociation.html
    :cloudformationResource: AWS::ServiceCatalog::PortfolioProductAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_portfolio_product_association_props_mixin = servicecatalog_mixins.CfnPortfolioProductAssociationPropsMixin(servicecatalog_mixins.CfnPortfolioProductAssociationMixinProps(
            accept_language="acceptLanguage",
            portfolio_id="portfolioId",
            product_id="productId",
            source_portfolio_id="sourcePortfolioId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPortfolioProductAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::PortfolioProductAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd87dcde7f3f6b4465ca6b3095b6d0ac54c3203f4535a9d133bfc3c0b3e4989)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f25a7be8a3e444330c5999c381a52a466582210e19958e5ee5aa12baca971549)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f402c1561ff004f3c745a179ce2b012c2dfd883b7184db54d31785c27177ff1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPortfolioProductAssociationMixinProps:
        return typing.cast(CfnPortfolioProductAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnPortfolioPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnPortfolioPropsMixin",
):
    '''Specifies a portfolio.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolio.html
    :cloudformationResource: AWS::ServiceCatalog::Portfolio
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_portfolio_props_mixin = servicecatalog_mixins.CfnPortfolioPropsMixin(servicecatalog_mixins.CfnPortfolioMixinProps(
            accept_language="acceptLanguage",
            description="description",
            display_name="displayName",
            provider_name="providerName",
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
        props: typing.Union[CfnPortfolioMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::Portfolio``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930f12765ca4e7a30e6444faa3e71ed8d996228b3aa6dbc0e366b52d7c2f8aac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff7c4a7851205345f0f8243edc0d839878640f5efc67af7f6ad2ac7093a8be8a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9bd16d632a3319c0f41834d6147dd5e725ad72bbbd0deaf64988c19b5d8fbe)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPortfolioMixinProps:
        return typing.cast(CfnPortfolioMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnPortfolioShareMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "account_id": "accountId",
        "portfolio_id": "portfolioId",
        "share_tag_options": "shareTagOptions",
    },
)
class CfnPortfolioShareMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        account_id: typing.Optional[builtins.str] = None,
        portfolio_id: typing.Optional[builtins.str] = None,
        share_tag_options: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnPortfolioSharePropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param account_id: The AWS account ID. For example, ``123456789012`` .
        :param portfolio_id: The portfolio identifier.
        :param share_tag_options: Indicates whether TagOptions sharing is enabled or disabled for the portfolio share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_portfolio_share_mixin_props = servicecatalog_mixins.CfnPortfolioShareMixinProps(
                accept_language="acceptLanguage",
                account_id="accountId",
                portfolio_id="portfolioId",
                share_tag_options=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c919ce594f487b96adb0ca840e3667023be1e5c055e38956dcfea1f48b5f97)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument share_tag_options", value=share_tag_options, expected_type=type_hints["share_tag_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if account_id is not None:
            self._values["account_id"] = account_id
        if portfolio_id is not None:
            self._values["portfolio_id"] = portfolio_id
        if share_tag_options is not None:
            self._values["share_tag_options"] = share_tag_options

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID.

        For example, ``123456789012`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-accountid
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-portfolioid
        '''
        result = self._values.get("portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_tag_options(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether TagOptions sharing is enabled or disabled for the portfolio share.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html#cfn-servicecatalog-portfolioshare-sharetagoptions
        '''
        result = self._values.get("share_tag_options")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortfolioShareMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPortfolioSharePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnPortfolioSharePropsMixin",
):
    '''Shares the specified portfolio with the specified account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-portfolioshare.html
    :cloudformationResource: AWS::ServiceCatalog::PortfolioShare
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_portfolio_share_props_mixin = servicecatalog_mixins.CfnPortfolioSharePropsMixin(servicecatalog_mixins.CfnPortfolioShareMixinProps(
            accept_language="acceptLanguage",
            account_id="accountId",
            portfolio_id="portfolioId",
            share_tag_options=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPortfolioShareMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::PortfolioShare``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49fdb9470f5b6839bf9e607a6881b88299b34afec1d93b210d9645513a36161a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__397db9203b00e64daca6b35053d0412dcbb68e2b11bb318b3eb613fc6abde808)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cd9beddb8344f0b18ab2559ba2acba25fe00b6f63b0894895d5849cd7c8adcf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPortfolioShareMixinProps:
        return typing.cast(CfnPortfolioShareMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnResourceUpdateConstraintMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "description": "description",
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "tag_update_on_provisioned_product": "tagUpdateOnProvisionedProduct",
    },
)
class CfnResourceUpdateConstraintMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        portfolio_id: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        tag_update_on_provisioned_product: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourceUpdateConstraintPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param description: The description of the constraint.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param tag_update_on_provisioned_product: If set to ``ALLOWED`` , lets users change tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource. If set to ``NOT_ALLOWED`` , prevents users from changing tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_resource_update_constraint_mixin_props = servicecatalog_mixins.CfnResourceUpdateConstraintMixinProps(
                accept_language="acceptLanguage",
                description="description",
                portfolio_id="portfolioId",
                product_id="productId",
                tag_update_on_provisioned_product="tagUpdateOnProvisionedProduct"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf7c82cb412f787e57c6a69e4a7febff7a602e7153bff8de0e734180e15ee2f)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument tag_update_on_provisioned_product", value=tag_update_on_provisioned_product, expected_type=type_hints["tag_update_on_provisioned_product"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if description is not None:
            self._values["description"] = description
        if portfolio_id is not None:
            self._values["portfolio_id"] = portfolio_id
        if product_id is not None:
            self._values["product_id"] = product_id
        if tag_update_on_provisioned_product is not None:
            self._values["tag_update_on_provisioned_product"] = tag_update_on_provisioned_product

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_update_on_provisioned_product(self) -> typing.Optional[builtins.str]:
        '''If set to ``ALLOWED`` , lets users change tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource.

        If set to ``NOT_ALLOWED`` , prevents users from changing tags in a `CloudFormationProvisionedProduct <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-cloudformationprovisionedproduct.html>`_ resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html#cfn-servicecatalog-resourceupdateconstraint-tagupdateonprovisionedproduct
        '''
        result = self._values.get("tag_update_on_provisioned_product")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceUpdateConstraintMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourceUpdateConstraintPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnResourceUpdateConstraintPropsMixin",
):
    '''Specifies a ``RESOURCE_UPDATE`` constraint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-resourceupdateconstraint.html
    :cloudformationResource: AWS::ServiceCatalog::ResourceUpdateConstraint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_resource_update_constraint_props_mixin = servicecatalog_mixins.CfnResourceUpdateConstraintPropsMixin(servicecatalog_mixins.CfnResourceUpdateConstraintMixinProps(
            accept_language="acceptLanguage",
            description="description",
            portfolio_id="portfolioId",
            product_id="productId",
            tag_update_on_provisioned_product="tagUpdateOnProvisionedProduct"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceUpdateConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::ResourceUpdateConstraint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94be76b56cb18576209cd2f018cabec9f8248e4255f0cec88fe013b485b90637)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9b9ac6857837f9ded6918194a806b54eb4506335f7c5917da92a0516b9aef20)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b7982997e99cf990d61ffcc224a51e187a154d99eafa882b37077f685d48af2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceUpdateConstraintMixinProps:
        return typing.cast(CfnResourceUpdateConstraintMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnServiceActionAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "product_id": "productId",
        "provisioning_artifact_id": "provisioningArtifactId",
        "service_action_id": "serviceActionId",
    },
)
class CfnServiceActionAssociationMixinProps:
    def __init__(
        self,
        *,
        product_id: typing.Optional[builtins.str] = None,
        provisioning_artifact_id: typing.Optional[builtins.str] = None,
        service_action_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnServiceActionAssociationPropsMixin.

        :param product_id: The product identifier. For example, ``prod-abcdzk7xy33qa`` .
        :param provisioning_artifact_id: The identifier of the provisioning artifact. For example, ``pa-4abcdjnxjj6ne`` .
        :param service_action_id: The self-service action identifier. For example, ``act-fs7abcd89wxyz`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_service_action_association_mixin_props = servicecatalog_mixins.CfnServiceActionAssociationMixinProps(
                product_id="productId",
                provisioning_artifact_id="provisioningArtifactId",
                service_action_id="serviceActionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb5eac85685c475a9d95993b6aad26bf13b0ac915b39d1df2e349dc8e9c4360)
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument provisioning_artifact_id", value=provisioning_artifact_id, expected_type=type_hints["provisioning_artifact_id"])
            check_type(argname="argument service_action_id", value=service_action_id, expected_type=type_hints["service_action_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if product_id is not None:
            self._values["product_id"] = product_id
        if provisioning_artifact_id is not None:
            self._values["provisioning_artifact_id"] = provisioning_artifact_id
        if service_action_id is not None:
            self._values["service_action_id"] = service_action_id

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        For example, ``prod-abcdzk7xy33qa`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html#cfn-servicecatalog-serviceactionassociation-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning_artifact_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the provisioning artifact.

        For example, ``pa-4abcdjnxjj6ne`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html#cfn-servicecatalog-serviceactionassociation-provisioningartifactid
        '''
        result = self._values.get("provisioning_artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_action_id(self) -> typing.Optional[builtins.str]:
        '''The self-service action identifier.

        For example, ``act-fs7abcd89wxyz`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html#cfn-servicecatalog-serviceactionassociation-serviceactionid
        '''
        result = self._values.get("service_action_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceActionAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceActionAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnServiceActionAssociationPropsMixin",
):
    '''A self-service action association consisting of the Action ID, the Product ID, and the Provisioning Artifact ID.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceactionassociation.html
    :cloudformationResource: AWS::ServiceCatalog::ServiceActionAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_service_action_association_props_mixin = servicecatalog_mixins.CfnServiceActionAssociationPropsMixin(servicecatalog_mixins.CfnServiceActionAssociationMixinProps(
            product_id="productId",
            provisioning_artifact_id="provisioningArtifactId",
            service_action_id="serviceActionId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServiceActionAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::ServiceActionAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73538c4b2ffe21486f3fbca640116b2969cb61e4195ea7bbad2c6dde7f54b22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa556585d5ea3c0d20b2b5daae3bea176ac7613f57c9292f342e63e6a0ff3957)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481dc6e0808040eddcc7049768717217676352f8dbc555e6a4cbaa3b236cb937)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceActionAssociationMixinProps:
        return typing.cast(CfnServiceActionAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnServiceActionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "definition": "definition",
        "definition_type": "definitionType",
        "description": "description",
        "name": "name",
    },
)
class CfnServiceActionMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceActionPropsMixin.DefinitionParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        definition_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnServiceActionPropsMixin.

        :param accept_language: The language code. - ``en`` - English (default) - ``jp`` - Japanese - ``zh`` - Chinese
        :param definition: A map that defines the self-service action.
        :param definition_type: The self-service action definition type. For example, ``SSM_AUTOMATION`` .
        :param description: The self-service action description.
        :param name: The self-service action name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_service_action_mixin_props = servicecatalog_mixins.CfnServiceActionMixinProps(
                accept_language="acceptLanguage",
                definition=[servicecatalog_mixins.CfnServiceActionPropsMixin.DefinitionParameterProperty(
                    key="key",
                    value="value"
                )],
                definition_type="definitionType",
                description="description",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f926f10e75206694335a02d9bd9f7c14f67ece397bd714259d88615a2ed4ecac)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument definition_type", value=definition_type, expected_type=type_hints["definition_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if definition is not None:
            self._values["definition"] = definition
        if definition_type is not None:
            self._values["definition_type"] = definition_type
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``en`` - English (default)
        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceActionPropsMixin.DefinitionParameterProperty"]]]]:
        '''A map that defines the self-service action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceActionPropsMixin.DefinitionParameterProperty"]]]], result)

    @builtins.property
    def definition_type(self) -> typing.Optional[builtins.str]:
        '''The self-service action definition type.

        For example, ``SSM_AUTOMATION`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-definitiontype
        '''
        result = self._values.get("definition_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The self-service action description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The self-service action name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html#cfn-servicecatalog-serviceaction-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceActionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceActionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnServiceActionPropsMixin",
):
    '''Creates a self-service action.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-serviceaction.html
    :cloudformationResource: AWS::ServiceCatalog::ServiceAction
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_service_action_props_mixin = servicecatalog_mixins.CfnServiceActionPropsMixin(servicecatalog_mixins.CfnServiceActionMixinProps(
            accept_language="acceptLanguage",
            definition=[servicecatalog_mixins.CfnServiceActionPropsMixin.DefinitionParameterProperty(
                key="key",
                value="value"
            )],
            definition_type="definitionType",
            description="description",
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServiceActionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::ServiceAction``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf3906b040844089ae6440d590c9c6549c9e89de682761a483f483254faa8af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__722fefd28ae40899cb14238fbdefa25b7da830e6bf24134c484458deb36e55a4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de12da084a6c3a7cc1addc89629ac92720bc832373230cc16927447c63dfb5b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceActionMixinProps:
        return typing.cast(CfnServiceActionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnServiceActionPropsMixin.DefinitionParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class DefinitionParameterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The list of parameters in JSON format.

            For example: ``[{\\"Name\\":\\"InstanceId\\",\\"Type\\":\\"TARGET\\"}] or [{\\"Name\\":\\"InstanceId\\",\\"Type\\":\\"TEXT_VALUE\\"}]`` .

            :param key: The parameter key.
            :param value: The value of the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-serviceaction-definitionparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
                
                definition_parameter_property = servicecatalog_mixins.CfnServiceActionPropsMixin.DefinitionParameterProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__440193475bcbb6df39444e906e9c3cddf6d7011b77642ed96f27f5e56837b089)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The parameter key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-serviceaction-definitionparameter.html#cfn-servicecatalog-serviceaction-definitionparameter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicecatalog-serviceaction-definitionparameter.html#cfn-servicecatalog-serviceaction-definitionparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnStackSetConstraintMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accept_language": "acceptLanguage",
        "account_list": "accountList",
        "admin_role": "adminRole",
        "description": "description",
        "execution_role": "executionRole",
        "portfolio_id": "portfolioId",
        "product_id": "productId",
        "region_list": "regionList",
        "stack_instance_control": "stackInstanceControl",
    },
)
class CfnStackSetConstraintMixinProps:
    def __init__(
        self,
        *,
        accept_language: typing.Optional[builtins.str] = None,
        account_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        admin_role: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        execution_role: typing.Optional[builtins.str] = None,
        portfolio_id: typing.Optional[builtins.str] = None,
        product_id: typing.Optional[builtins.str] = None,
        region_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_instance_control: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStackSetConstraintPropsMixin.

        :param accept_language: The language code. - ``jp`` - Japanese - ``zh`` - Chinese
        :param account_list: One or more AWS accounts that will have access to the provisioned product.
        :param admin_role: AdminRole ARN.
        :param description: The description of the constraint.
        :param execution_role: ExecutionRole name.
        :param portfolio_id: The portfolio identifier.
        :param product_id: The product identifier.
        :param region_list: One or more AWS Regions where the provisioned product will be available. Applicable only to a ``CFN_STACKSET`` provisioned product type. The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation. If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.
        :param stack_instance_control: Permission to create, update, and delete stack instances. Choose from ALLOWED and NOT_ALLOWED.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_stack_set_constraint_mixin_props = servicecatalog_mixins.CfnStackSetConstraintMixinProps(
                accept_language="acceptLanguage",
                account_list=["accountList"],
                admin_role="adminRole",
                description="description",
                execution_role="executionRole",
                portfolio_id="portfolioId",
                product_id="productId",
                region_list=["regionList"],
                stack_instance_control="stackInstanceControl"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c62fc9f6069e59fd80289fcadd025bd21b54cfca1abc3e669eff7c399a5d4d4)
            check_type(argname="argument accept_language", value=accept_language, expected_type=type_hints["accept_language"])
            check_type(argname="argument account_list", value=account_list, expected_type=type_hints["account_list"])
            check_type(argname="argument admin_role", value=admin_role, expected_type=type_hints["admin_role"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument portfolio_id", value=portfolio_id, expected_type=type_hints["portfolio_id"])
            check_type(argname="argument product_id", value=product_id, expected_type=type_hints["product_id"])
            check_type(argname="argument region_list", value=region_list, expected_type=type_hints["region_list"])
            check_type(argname="argument stack_instance_control", value=stack_instance_control, expected_type=type_hints["stack_instance_control"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accept_language is not None:
            self._values["accept_language"] = accept_language
        if account_list is not None:
            self._values["account_list"] = account_list
        if admin_role is not None:
            self._values["admin_role"] = admin_role
        if description is not None:
            self._values["description"] = description
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if portfolio_id is not None:
            self._values["portfolio_id"] = portfolio_id
        if product_id is not None:
            self._values["product_id"] = product_id
        if region_list is not None:
            self._values["region_list"] = region_list
        if stack_instance_control is not None:
            self._values["stack_instance_control"] = stack_instance_control

    @builtins.property
    def accept_language(self) -> typing.Optional[builtins.str]:
        '''The language code.

        - ``jp`` - Japanese
        - ``zh`` - Chinese

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-acceptlanguage
        '''
        result = self._values.get("accept_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more AWS accounts that will have access to the provisioned product.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-accountlist
        '''
        result = self._values.get("account_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def admin_role(self) -> typing.Optional[builtins.str]:
        '''AdminRole ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-adminrole
        '''
        result = self._values.get("admin_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the constraint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[builtins.str]:
        '''ExecutionRole name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-executionrole
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portfolio_id(self) -> typing.Optional[builtins.str]:
        '''The portfolio identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-portfolioid
        '''
        result = self._values.get("portfolio_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def product_id(self) -> typing.Optional[builtins.str]:
        '''The product identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-productid
        '''
        result = self._values.get("product_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more AWS Regions where the provisioned product will be available.

        Applicable only to a ``CFN_STACKSET`` provisioned product type.

        The specified Regions should be within the list of Regions from the ``STACKSET`` constraint. To get the list of Regions in the ``STACKSET`` constraint, use the ``DescribeProvisioningParameters`` operation.

        If no values are specified, the default value is all Regions from the ``STACKSET`` constraint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-regionlist
        '''
        result = self._values.get("region_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_instance_control(self) -> typing.Optional[builtins.str]:
        '''Permission to create, update, and delete stack instances.

        Choose from ALLOWED and NOT_ALLOWED.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html#cfn-servicecatalog-stacksetconstraint-stackinstancecontrol
        '''
        result = self._values.get("stack_instance_control")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackSetConstraintMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStackSetConstraintPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnStackSetConstraintPropsMixin",
):
    '''Specifies a StackSet constraint.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-stacksetconstraint.html
    :cloudformationResource: AWS::ServiceCatalog::StackSetConstraint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_stack_set_constraint_props_mixin = servicecatalog_mixins.CfnStackSetConstraintPropsMixin(servicecatalog_mixins.CfnStackSetConstraintMixinProps(
            accept_language="acceptLanguage",
            account_list=["accountList"],
            admin_role="adminRole",
            description="description",
            execution_role="executionRole",
            portfolio_id="portfolioId",
            product_id="productId",
            region_list=["regionList"],
            stack_instance_control="stackInstanceControl"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStackSetConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::StackSetConstraint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a4f5eea3e7a78f1f8b1b6b18354e7a373a96e1047fcd3e80c4464efbf75a11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b771def484ef220d1d5f1ca71da8a5b94b749e3a00aae68e2d6e83f5fd30d27)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef46e5caa82674d91793da9f5287315c79bf8ff024958c8774cd23d0beee8667)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStackSetConstraintMixinProps:
        return typing.cast(CfnStackSetConstraintMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnTagOptionAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"resource_id": "resourceId", "tag_option_id": "tagOptionId"},
)
class CfnTagOptionAssociationMixinProps:
    def __init__(
        self,
        *,
        resource_id: typing.Optional[builtins.str] = None,
        tag_option_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTagOptionAssociationPropsMixin.

        :param resource_id: The resource identifier.
        :param tag_option_id: The TagOption identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_tag_option_association_mixin_props = servicecatalog_mixins.CfnTagOptionAssociationMixinProps(
                resource_id="resourceId",
                tag_option_id="tagOptionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8646bd39e79d2fcd96af425790582eb1fa27f0e6df4d9f3d586b5fdd7ea38f8e)
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument tag_option_id", value=tag_option_id, expected_type=type_hints["tag_option_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if tag_option_id is not None:
            self._values["tag_option_id"] = tag_option_id

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The resource identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html#cfn-servicecatalog-tagoptionassociation-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_option_id(self) -> typing.Optional[builtins.str]:
        '''The TagOption identifier.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html#cfn-servicecatalog-tagoptionassociation-tagoptionid
        '''
        result = self._values.get("tag_option_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTagOptionAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTagOptionAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnTagOptionAssociationPropsMixin",
):
    '''Associate the specified TagOption with the specified portfolio or product.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoptionassociation.html
    :cloudformationResource: AWS::ServiceCatalog::TagOptionAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_tag_option_association_props_mixin = servicecatalog_mixins.CfnTagOptionAssociationPropsMixin(servicecatalog_mixins.CfnTagOptionAssociationMixinProps(
            resource_id="resourceId",
            tag_option_id="tagOptionId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTagOptionAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::TagOptionAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb9dae0dc5b63481500e0d09b951a22498b5586644d785b12180333435dd876)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a6698b17cce7a7dfbd7166585668c639ed04eeeb504cea1c5468e64e8818ef)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d142d9097172b7c69052edfbe20a0b23c45afee206fa6f141a4e266a47194d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTagOptionAssociationMixinProps:
        return typing.cast(CfnTagOptionAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnTagOptionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"active": "active", "key": "key", "value": "value"},
)
class CfnTagOptionMixinProps:
    def __init__(
        self,
        *,
        active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTagOptionPropsMixin.

        :param active: The TagOption active state.
        :param key: The TagOption key.
        :param value: The TagOption value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
            
            cfn_tag_option_mixin_props = servicecatalog_mixins.CfnTagOptionMixinProps(
                active=False,
                key="key",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfc6988ff0fe2dfc675471c3662b402e9beff5081a36f3053a7939647402e933)
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active is not None:
            self._values["active"] = active
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The TagOption active state.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-active
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The TagOption key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The TagOption value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html#cfn-servicecatalog-tagoption-value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTagOptionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTagOptionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_servicecatalog.mixins.CfnTagOptionPropsMixin",
):
    '''Specifies a TagOption.

    A TagOption is a key-value pair managed by AWS Service Catalog that serves as a template for creating an AWS tag.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicecatalog-tagoption.html
    :cloudformationResource: AWS::ServiceCatalog::TagOption
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_servicecatalog import mixins as servicecatalog_mixins
        
        cfn_tag_option_props_mixin = servicecatalog_mixins.CfnTagOptionPropsMixin(servicecatalog_mixins.CfnTagOptionMixinProps(
            active=False,
            key="key",
            value="value"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTagOptionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ServiceCatalog::TagOption``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3710f8f89afe787a9a7934a0b83cef42cb47e0f40b00d3238c60dd73a19b21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28e22beadfea79ff7d76b5a460f828f6b9b30dc0148b7f75d4d4e95342a880b6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc345956dbfa9d495a61fba6f65aaf15da567c275021461f5d98c0ac7bdc86b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTagOptionMixinProps:
        return typing.cast(CfnTagOptionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAcceptedPortfolioShareMixinProps",
    "CfnAcceptedPortfolioSharePropsMixin",
    "CfnCloudFormationProductMixinProps",
    "CfnCloudFormationProductPropsMixin",
    "CfnCloudFormationProvisionedProductMixinProps",
    "CfnCloudFormationProvisionedProductPropsMixin",
    "CfnLaunchNotificationConstraintMixinProps",
    "CfnLaunchNotificationConstraintPropsMixin",
    "CfnLaunchRoleConstraintMixinProps",
    "CfnLaunchRoleConstraintPropsMixin",
    "CfnLaunchTemplateConstraintMixinProps",
    "CfnLaunchTemplateConstraintPropsMixin",
    "CfnPortfolioMixinProps",
    "CfnPortfolioPrincipalAssociationMixinProps",
    "CfnPortfolioPrincipalAssociationPropsMixin",
    "CfnPortfolioProductAssociationMixinProps",
    "CfnPortfolioProductAssociationPropsMixin",
    "CfnPortfolioPropsMixin",
    "CfnPortfolioShareMixinProps",
    "CfnPortfolioSharePropsMixin",
    "CfnResourceUpdateConstraintMixinProps",
    "CfnResourceUpdateConstraintPropsMixin",
    "CfnServiceActionAssociationMixinProps",
    "CfnServiceActionAssociationPropsMixin",
    "CfnServiceActionMixinProps",
    "CfnServiceActionPropsMixin",
    "CfnStackSetConstraintMixinProps",
    "CfnStackSetConstraintPropsMixin",
    "CfnTagOptionAssociationMixinProps",
    "CfnTagOptionAssociationPropsMixin",
    "CfnTagOptionMixinProps",
    "CfnTagOptionPropsMixin",
]

publication.publish()

def _typecheckingstub__acee4d5260b522d899bae2d902ce569b889910929361c87bbaa7d88da6a37404(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    portfolio_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5256b486888764640f45b07a950cd5d5db9a1895cac58f71622f3eabbd4cb07(
    props: typing.Union[CfnAcceptedPortfolioShareMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56cb9419abd6b9f2f4695b7525d7955e25b97891ed1de6b3d918b5063ce2bbe2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f617dccebc59471c7d280aec8d7eb4099d3cc5432e0bc5f6ddb606e0307df25(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a3ab93af8d58dd3608cd11523a8896e1de949363593343329f551092e07b5f(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    distributor: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    product_type: typing.Optional[builtins.str] = None,
    provisioning_artifact_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudFormationProductPropsMixin.ProvisioningArtifactPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    replace_provisioning_artifacts: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    source_connection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudFormationProductPropsMixin.SourceConnectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    support_description: typing.Optional[builtins.str] = None,
    support_email: typing.Optional[builtins.str] = None,
    support_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c84f62505ba849f783fbc6dc002943230d9cef270cf5ebc8e38caed4ba5c89(
    props: typing.Union[CfnCloudFormationProductMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7c6dbd54ff60347c671aaa0104529ea8705cbb65e5effe2ee1ba57b301b15c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd691e0cd3f911f738282ea8d73cbb86ece8af622ccebcd1c1b7d16d55c90785(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9375600b6cf17c416e07d8de93adeac5ac615c16666f4e012481ddd09d7b8c06(
    *,
    artifact_path: typing.Optional[builtins.str] = None,
    branch: typing.Optional[builtins.str] = None,
    connection_arn: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8709a70141cb0d5514b6dad896ead17ce19a03aff10a4e255c7bf09bf1ee475b(
    *,
    code_star: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudFormationProductPropsMixin.CodeStarParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ff8178bae2564a4e820a28aec93adac4a21627b2d9cd42e76a4558d8ee615d(
    *,
    description: typing.Optional[builtins.str] = None,
    disable_template_validation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    info: typing.Any = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f484e9e75ee9ba93a62175665325f982dcf65414fb0270d9833d706856b5f5f9(
    *,
    connection_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudFormationProductPropsMixin.ConnectionParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a3c60b859967614b29db4e436971a886b332f0ca647bc51c6ba75fe0e92fcb(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path_id: typing.Optional[builtins.str] = None,
    path_name: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    product_name: typing.Optional[builtins.str] = None,
    provisioned_product_name: typing.Optional[builtins.str] = None,
    provisioning_artifact_id: typing.Optional[builtins.str] = None,
    provisioning_artifact_name: typing.Optional[builtins.str] = None,
    provisioning_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudFormationProvisionedProductPropsMixin.ProvisioningParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    provisioning_preferences: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCloudFormationProvisionedProductPropsMixin.ProvisioningPreferencesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbafc763e9f307429ee7a52b4882ea9e1d47ac4824f8ec1ce6cf03a4bae4a83(
    props: typing.Union[CfnCloudFormationProvisionedProductMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb68abac87c107da383836f1ba909ae17d3d5ccb0f94ab8a991a65e1d1c9504c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19749cfa88f9f3ffe0a9bcd2b5bb7f10f882b9233eab4b698210b0055f60a39(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0428e52a0c5faaf1cd34d222b95ca615bde85759a059ed6875993e3eac609f1d(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca6b062091b3ce1180a936f9c775c5321ef8d8a5f968f654f067a30343b08c5(
    *,
    stack_set_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_set_failure_tolerance_count: typing.Optional[jsii.Number] = None,
    stack_set_failure_tolerance_percentage: typing.Optional[jsii.Number] = None,
    stack_set_max_concurrency_count: typing.Optional[jsii.Number] = None,
    stack_set_max_concurrency_percentage: typing.Optional[jsii.Number] = None,
    stack_set_operation_type: typing.Optional[builtins.str] = None,
    stack_set_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9de01afe621b580f37c05361f645d642211eb3a29ac81fd29938a2b3577340(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    portfolio_id: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b748fc0c1402ee594887f55728e8cc98266c436547a827aa95faab3e04d003(
    props: typing.Union[CfnLaunchNotificationConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d39954853c4a1c9b99679aa6451745beca1c7ba571613a92e6513de63f801a4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fc712747cc3433ba4e05ebc5884bd4bc854eee2f775c414fb1c80744426037(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f11ab899f7fccd39ac7a561b158d966743f0bdaa01b5c947cc1550495cc28b(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    local_role_name: typing.Optional[builtins.str] = None,
    portfolio_id: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6efed8a69d6fd5cf922a34ff2fd3bd261fec45462456c33f1b7a74beb954a5d(
    props: typing.Union[CfnLaunchRoleConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007f487f4540b7ca1d3c52172f43fa011647742f7df8342d577ffafa7c789e63(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5eca57e476717391bd10970bd1f52dad247849071d28a601a9290c125e18d1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb97b88ca06d4942f7d0607c52edb503fe6a656fd1f6809ec024037e9861bf51(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    portfolio_id: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    rules: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3552ffac525b92bff9a465b4ee7a526fef012196244d0b24626b61b148ea16(
    props: typing.Union[CfnLaunchTemplateConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6424d9fc80016977e51cf5cd26870f03acfd48e58b90247552132172eed842f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a67aa26c2e80fab7c305613625c142a8d79ef5300288b920e69f4928f33fddc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6519ea424c4d0e29026db47f05739ae96f56955756a9c4d30e369bd5c69430c7(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    provider_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cdff90d26d9d3ffb84af4c278c3e489bb2c842a2052d860075e4ff71897e23b(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    portfolio_id: typing.Optional[builtins.str] = None,
    principal_arn: typing.Optional[builtins.str] = None,
    principal_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffff4a2d20e469130f5b820ebc5d576dd140dd6b21ed9078bd3aebe96bd96677(
    props: typing.Union[CfnPortfolioPrincipalAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e74a224c60d0abda938dff01ad97601f5f5b8cf85802dc32f8f4cdc82533c6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c769e55bead0d92180d9c9d2c97344c44748a4ffbc62148d6b6d003e686dc26(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693f06e00afb390c2b7898bdbc1707c654881d3de95f6a45d33f1b30bf8c85a8(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    portfolio_id: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    source_portfolio_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd87dcde7f3f6b4465ca6b3095b6d0ac54c3203f4535a9d133bfc3c0b3e4989(
    props: typing.Union[CfnPortfolioProductAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25a7be8a3e444330c5999c381a52a466582210e19958e5ee5aa12baca971549(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f402c1561ff004f3c745a179ce2b012c2dfd883b7184db54d31785c27177ff1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930f12765ca4e7a30e6444faa3e71ed8d996228b3aa6dbc0e366b52d7c2f8aac(
    props: typing.Union[CfnPortfolioMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7c4a7851205345f0f8243edc0d839878640f5efc67af7f6ad2ac7093a8be8a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9bd16d632a3319c0f41834d6147dd5e725ad72bbbd0deaf64988c19b5d8fbe(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c919ce594f487b96adb0ca840e3667023be1e5c055e38956dcfea1f48b5f97(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    account_id: typing.Optional[builtins.str] = None,
    portfolio_id: typing.Optional[builtins.str] = None,
    share_tag_options: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fdb9470f5b6839bf9e607a6881b88299b34afec1d93b210d9645513a36161a(
    props: typing.Union[CfnPortfolioShareMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397db9203b00e64daca6b35053d0412dcbb68e2b11bb318b3eb613fc6abde808(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cd9beddb8344f0b18ab2559ba2acba25fe00b6f63b0894895d5849cd7c8adcf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf7c82cb412f787e57c6a69e4a7febff7a602e7153bff8de0e734180e15ee2f(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    portfolio_id: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    tag_update_on_provisioned_product: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94be76b56cb18576209cd2f018cabec9f8248e4255f0cec88fe013b485b90637(
    props: typing.Union[CfnResourceUpdateConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b9ac6857837f9ded6918194a806b54eb4506335f7c5917da92a0516b9aef20(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b7982997e99cf990d61ffcc224a51e187a154d99eafa882b37077f685d48af2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb5eac85685c475a9d95993b6aad26bf13b0ac915b39d1df2e349dc8e9c4360(
    *,
    product_id: typing.Optional[builtins.str] = None,
    provisioning_artifact_id: typing.Optional[builtins.str] = None,
    service_action_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73538c4b2ffe21486f3fbca640116b2969cb61e4195ea7bbad2c6dde7f54b22(
    props: typing.Union[CfnServiceActionAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa556585d5ea3c0d20b2b5daae3bea176ac7613f57c9292f342e63e6a0ff3957(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481dc6e0808040eddcc7049768717217676352f8dbc555e6a4cbaa3b236cb937(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f926f10e75206694335a02d9bd9f7c14f67ece397bd714259d88615a2ed4ecac(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceActionPropsMixin.DefinitionParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    definition_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf3906b040844089ae6440d590c9c6549c9e89de682761a483f483254faa8af(
    props: typing.Union[CfnServiceActionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722fefd28ae40899cb14238fbdefa25b7da830e6bf24134c484458deb36e55a4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de12da084a6c3a7cc1addc89629ac92720bc832373230cc16927447c63dfb5b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440193475bcbb6df39444e906e9c3cddf6d7011b77642ed96f27f5e56837b089(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c62fc9f6069e59fd80289fcadd025bd21b54cfca1abc3e669eff7c399a5d4d4(
    *,
    accept_language: typing.Optional[builtins.str] = None,
    account_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    admin_role: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    execution_role: typing.Optional[builtins.str] = None,
    portfolio_id: typing.Optional[builtins.str] = None,
    product_id: typing.Optional[builtins.str] = None,
    region_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_instance_control: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a4f5eea3e7a78f1f8b1b6b18354e7a373a96e1047fcd3e80c4464efbf75a11(
    props: typing.Union[CfnStackSetConstraintMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b771def484ef220d1d5f1ca71da8a5b94b749e3a00aae68e2d6e83f5fd30d27(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef46e5caa82674d91793da9f5287315c79bf8ff024958c8774cd23d0beee8667(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8646bd39e79d2fcd96af425790582eb1fa27f0e6df4d9f3d586b5fdd7ea38f8e(
    *,
    resource_id: typing.Optional[builtins.str] = None,
    tag_option_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb9dae0dc5b63481500e0d09b951a22498b5586644d785b12180333435dd876(
    props: typing.Union[CfnTagOptionAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a6698b17cce7a7dfbd7166585668c639ed04eeeb504cea1c5468e64e8818ef(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d142d9097172b7c69052edfbe20a0b23c45afee206fa6f141a4e266a47194d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc6988ff0fe2dfc675471c3662b402e9beff5081a36f3053a7939647402e933(
    *,
    active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3710f8f89afe787a9a7934a0b83cef42cb47e0f40b00d3238c60dd73a19b21(
    props: typing.Union[CfnTagOptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e22beadfea79ff7d76b5a460f828f6b9b30dc0148b7f75d4d4e95342a880b6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc345956dbfa9d495a61fba6f65aaf15da567c275021461f5d98c0ac7bdc86b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
