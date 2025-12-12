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
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnClassifierMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "csv_classifier": "csvClassifier",
        "grok_classifier": "grokClassifier",
        "json_classifier": "jsonClassifier",
        "xml_classifier": "xmlClassifier",
    },
)
class CfnClassifierMixinProps:
    def __init__(
        self,
        *,
        csv_classifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClassifierPropsMixin.CsvClassifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        grok_classifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClassifierPropsMixin.GrokClassifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        json_classifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClassifierPropsMixin.JsonClassifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        xml_classifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClassifierPropsMixin.XMLClassifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnClassifierPropsMixin.

        :param csv_classifier: A classifier for comma-separated values (CSV).
        :param grok_classifier: A classifier that uses ``grok`` .
        :param json_classifier: A classifier for JSON content.
        :param xml_classifier: A classifier for XML content.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_classifier_mixin_props = glue_mixins.CfnClassifierMixinProps(
                csv_classifier=glue_mixins.CfnClassifierPropsMixin.CsvClassifierProperty(
                    allow_single_column=False,
                    contains_custom_datatype=["containsCustomDatatype"],
                    contains_header="containsHeader",
                    custom_datatype_configured=False,
                    delimiter="delimiter",
                    disable_value_trimming=False,
                    header=["header"],
                    name="name",
                    quote_symbol="quoteSymbol"
                ),
                grok_classifier=glue_mixins.CfnClassifierPropsMixin.GrokClassifierProperty(
                    classification="classification",
                    custom_patterns="customPatterns",
                    grok_pattern="grokPattern",
                    name="name"
                ),
                json_classifier=glue_mixins.CfnClassifierPropsMixin.JsonClassifierProperty(
                    json_path="jsonPath",
                    name="name"
                ),
                xml_classifier=glue_mixins.CfnClassifierPropsMixin.XMLClassifierProperty(
                    classification="classification",
                    name="name",
                    row_tag="rowTag"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a328e3e9b1c3052c60ae0bb5138bf2a22027f3814e6595a87d8dec9469588e8f)
            check_type(argname="argument csv_classifier", value=csv_classifier, expected_type=type_hints["csv_classifier"])
            check_type(argname="argument grok_classifier", value=grok_classifier, expected_type=type_hints["grok_classifier"])
            check_type(argname="argument json_classifier", value=json_classifier, expected_type=type_hints["json_classifier"])
            check_type(argname="argument xml_classifier", value=xml_classifier, expected_type=type_hints["xml_classifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if csv_classifier is not None:
            self._values["csv_classifier"] = csv_classifier
        if grok_classifier is not None:
            self._values["grok_classifier"] = grok_classifier
        if json_classifier is not None:
            self._values["json_classifier"] = json_classifier
        if xml_classifier is not None:
            self._values["xml_classifier"] = xml_classifier

    @builtins.property
    def csv_classifier(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClassifierPropsMixin.CsvClassifierProperty"]]:
        '''A classifier for comma-separated values (CSV).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-csvclassifier
        '''
        result = self._values.get("csv_classifier")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClassifierPropsMixin.CsvClassifierProperty"]], result)

    @builtins.property
    def grok_classifier(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClassifierPropsMixin.GrokClassifierProperty"]]:
        '''A classifier that uses ``grok`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-grokclassifier
        '''
        result = self._values.get("grok_classifier")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClassifierPropsMixin.GrokClassifierProperty"]], result)

    @builtins.property
    def json_classifier(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClassifierPropsMixin.JsonClassifierProperty"]]:
        '''A classifier for JSON content.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-jsonclassifier
        '''
        result = self._values.get("json_classifier")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClassifierPropsMixin.JsonClassifierProperty"]], result)

    @builtins.property
    def xml_classifier(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClassifierPropsMixin.XMLClassifierProperty"]]:
        '''A classifier for XML content.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-xmlclassifier
        '''
        result = self._values.get("xml_classifier")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClassifierPropsMixin.XMLClassifierProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClassifierMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClassifierPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnClassifierPropsMixin",
):
    '''The ``AWS::Glue::Classifier`` resource creates an AWS Glue classifier that categorizes data sources and specifies schemas.

    For more information, see `Adding Classifiers to a Crawler <https://docs.aws.amazon.com/glue/latest/dg/add-classifier.html>`_ and `Classifier Structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-classifiers.html#aws-glue-api-crawler-classifiers-Classifier>`_ in the *AWS Glue Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html
    :cloudformationResource: AWS::Glue::Classifier
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_classifier_props_mixin = glue_mixins.CfnClassifierPropsMixin(glue_mixins.CfnClassifierMixinProps(
            csv_classifier=glue_mixins.CfnClassifierPropsMixin.CsvClassifierProperty(
                allow_single_column=False,
                contains_custom_datatype=["containsCustomDatatype"],
                contains_header="containsHeader",
                custom_datatype_configured=False,
                delimiter="delimiter",
                disable_value_trimming=False,
                header=["header"],
                name="name",
                quote_symbol="quoteSymbol"
            ),
            grok_classifier=glue_mixins.CfnClassifierPropsMixin.GrokClassifierProperty(
                classification="classification",
                custom_patterns="customPatterns",
                grok_pattern="grokPattern",
                name="name"
            ),
            json_classifier=glue_mixins.CfnClassifierPropsMixin.JsonClassifierProperty(
                json_path="jsonPath",
                name="name"
            ),
            xml_classifier=glue_mixins.CfnClassifierPropsMixin.XMLClassifierProperty(
                classification="classification",
                name="name",
                row_tag="rowTag"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnClassifierMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Classifier``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9872122f3b44047300349c842dcb488f9f0fcee9d63d77f7785bd56e89fcaadb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94d8b9e84e8b65c439681de1e0dcca5ee051f847d0bb52f9478e11f42b284398)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61cfc31a346b018460bd20f118835fb9d3a11792a7bf56823713cc892949b0ac)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClassifierMixinProps:
        return typing.cast(CfnClassifierMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnClassifierPropsMixin.CsvClassifierProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_single_column": "allowSingleColumn",
            "contains_custom_datatype": "containsCustomDatatype",
            "contains_header": "containsHeader",
            "custom_datatype_configured": "customDatatypeConfigured",
            "delimiter": "delimiter",
            "disable_value_trimming": "disableValueTrimming",
            "header": "header",
            "name": "name",
            "quote_symbol": "quoteSymbol",
        },
    )
    class CsvClassifierProperty:
        def __init__(
            self,
            *,
            allow_single_column: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            contains_custom_datatype: typing.Optional[typing.Sequence[builtins.str]] = None,
            contains_header: typing.Optional[builtins.str] = None,
            custom_datatype_configured: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            delimiter: typing.Optional[builtins.str] = None,
            disable_value_trimming: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            header: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            quote_symbol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A classifier for custom ``CSV`` content.

            :param allow_single_column: Enables the processing of files that contain only one column.
            :param contains_custom_datatype: Indicates whether the CSV file contains custom data types.
            :param contains_header: Indicates whether the CSV file contains a header. A value of ``UNKNOWN`` specifies that the classifier will detect whether the CSV file contains headings. A value of ``PRESENT`` specifies that the CSV file contains headings. A value of ``ABSENT`` specifies that the CSV file does not contain headings.
            :param custom_datatype_configured: Enables the configuration of custom data types.
            :param delimiter: A custom symbol to denote what separates each column entry in the row.
            :param disable_value_trimming: Specifies not to trim values before identifying the type of column values. The default value is ``true`` .
            :param header: A list of strings representing column names.
            :param name: The name of the classifier.
            :param quote_symbol: A custom symbol to denote what combines content into a single column value. It must be different from the column delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                csv_classifier_property = glue_mixins.CfnClassifierPropsMixin.CsvClassifierProperty(
                    allow_single_column=False,
                    contains_custom_datatype=["containsCustomDatatype"],
                    contains_header="containsHeader",
                    custom_datatype_configured=False,
                    delimiter="delimiter",
                    disable_value_trimming=False,
                    header=["header"],
                    name="name",
                    quote_symbol="quoteSymbol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89bd14ce5552c3b83860159121336ccc22174ca306d09d6441c1f1dbb80a4dde)
                check_type(argname="argument allow_single_column", value=allow_single_column, expected_type=type_hints["allow_single_column"])
                check_type(argname="argument contains_custom_datatype", value=contains_custom_datatype, expected_type=type_hints["contains_custom_datatype"])
                check_type(argname="argument contains_header", value=contains_header, expected_type=type_hints["contains_header"])
                check_type(argname="argument custom_datatype_configured", value=custom_datatype_configured, expected_type=type_hints["custom_datatype_configured"])
                check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
                check_type(argname="argument disable_value_trimming", value=disable_value_trimming, expected_type=type_hints["disable_value_trimming"])
                check_type(argname="argument header", value=header, expected_type=type_hints["header"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument quote_symbol", value=quote_symbol, expected_type=type_hints["quote_symbol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_single_column is not None:
                self._values["allow_single_column"] = allow_single_column
            if contains_custom_datatype is not None:
                self._values["contains_custom_datatype"] = contains_custom_datatype
            if contains_header is not None:
                self._values["contains_header"] = contains_header
            if custom_datatype_configured is not None:
                self._values["custom_datatype_configured"] = custom_datatype_configured
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if disable_value_trimming is not None:
                self._values["disable_value_trimming"] = disable_value_trimming
            if header is not None:
                self._values["header"] = header
            if name is not None:
                self._values["name"] = name
            if quote_symbol is not None:
                self._values["quote_symbol"] = quote_symbol

        @builtins.property
        def allow_single_column(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables the processing of files that contain only one column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-allowsinglecolumn
            '''
            result = self._values.get("allow_single_column")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def contains_custom_datatype(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Indicates whether the CSV file contains custom data types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-containscustomdatatype
            '''
            result = self._values.get("contains_custom_datatype")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def contains_header(self) -> typing.Optional[builtins.str]:
            '''Indicates whether the CSV file contains a header.

            A value of ``UNKNOWN`` specifies that the classifier will detect whether the CSV file contains headings.

            A value of ``PRESENT`` specifies that the CSV file contains headings.

            A value of ``ABSENT`` specifies that the CSV file does not contain headings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-containsheader
            '''
            result = self._values.get("contains_header")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_datatype_configured(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables the configuration of custom data types.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-customdatatypeconfigured
            '''
            result = self._values.get("custom_datatype_configured")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''A custom symbol to denote what separates each column entry in the row.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disable_value_trimming(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies not to trim values before identifying the type of column values.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-disablevaluetrimming
            '''
            result = self._values.get("disable_value_trimming")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def header(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of strings representing column names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-header
            '''
            result = self._values.get("header")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the classifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def quote_symbol(self) -> typing.Optional[builtins.str]:
            '''A custom symbol to denote what combines content into a single column value.

            It must be different from the column delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-quotesymbol
            '''
            result = self._values.get("quote_symbol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsvClassifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnClassifierPropsMixin.GrokClassifierProperty",
        jsii_struct_bases=[],
        name_mapping={
            "classification": "classification",
            "custom_patterns": "customPatterns",
            "grok_pattern": "grokPattern",
            "name": "name",
        },
    )
    class GrokClassifierProperty:
        def __init__(
            self,
            *,
            classification: typing.Optional[builtins.str] = None,
            custom_patterns: typing.Optional[builtins.str] = None,
            grok_pattern: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A classifier that uses ``grok`` patterns.

            :param classification: An identifier of the data format that the classifier matches, such as Twitter, JSON, Omniture logs, and so on.
            :param custom_patterns: Optional custom grok patterns defined by this classifier. For more information, see custom patterns in `Writing Custom Classifiers <https://docs.aws.amazon.com/glue/latest/dg/custom-classifier.html>`_ .
            :param grok_pattern: The grok pattern applied to a data store by this classifier. For more information, see built-in patterns in `Writing Custom Classifiers <https://docs.aws.amazon.com/glue/latest/dg/custom-classifier.html>`_ .
            :param name: The name of the classifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                grok_classifier_property = glue_mixins.CfnClassifierPropsMixin.GrokClassifierProperty(
                    classification="classification",
                    custom_patterns="customPatterns",
                    grok_pattern="grokPattern",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1248bce53af82aa06bd6fb2c01ceee86ca3e2be30bef77b5e11716a5ca98fbb)
                check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
                check_type(argname="argument custom_patterns", value=custom_patterns, expected_type=type_hints["custom_patterns"])
                check_type(argname="argument grok_pattern", value=grok_pattern, expected_type=type_hints["grok_pattern"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if classification is not None:
                self._values["classification"] = classification
            if custom_patterns is not None:
                self._values["custom_patterns"] = custom_patterns
            if grok_pattern is not None:
                self._values["grok_pattern"] = grok_pattern
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def classification(self) -> typing.Optional[builtins.str]:
            '''An identifier of the data format that the classifier matches, such as Twitter, JSON, Omniture logs, and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html#cfn-glue-classifier-grokclassifier-classification
            '''
            result = self._values.get("classification")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_patterns(self) -> typing.Optional[builtins.str]:
            '''Optional custom grok patterns defined by this classifier.

            For more information, see custom patterns in `Writing Custom Classifiers <https://docs.aws.amazon.com/glue/latest/dg/custom-classifier.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html#cfn-glue-classifier-grokclassifier-custompatterns
            '''
            result = self._values.get("custom_patterns")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def grok_pattern(self) -> typing.Optional[builtins.str]:
            '''The grok pattern applied to a data store by this classifier.

            For more information, see built-in patterns in `Writing Custom Classifiers <https://docs.aws.amazon.com/glue/latest/dg/custom-classifier.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html#cfn-glue-classifier-grokclassifier-grokpattern
            '''
            result = self._values.get("grok_pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the classifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html#cfn-glue-classifier-grokclassifier-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrokClassifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnClassifierPropsMixin.JsonClassifierProperty",
        jsii_struct_bases=[],
        name_mapping={"json_path": "jsonPath", "name": "name"},
    )
    class JsonClassifierProperty:
        def __init__(
            self,
            *,
            json_path: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A classifier for ``JSON`` content.

            :param json_path: A ``JsonPath`` string defining the JSON data for the classifier to classify. AWS Glue supports a subset of ``JsonPath`` , as described in `Writing JsonPath Custom Classifiers <https://docs.aws.amazon.com/glue/latest/dg/custom-classifier.html#custom-classifier-json>`_ .
            :param name: The name of the classifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-jsonclassifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                json_classifier_property = glue_mixins.CfnClassifierPropsMixin.JsonClassifierProperty(
                    json_path="jsonPath",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab7efb773b0a0fe13c59aad3027f6d602a89c57b75b6894b5c185c714a6f0dde)
                check_type(argname="argument json_path", value=json_path, expected_type=type_hints["json_path"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if json_path is not None:
                self._values["json_path"] = json_path
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def json_path(self) -> typing.Optional[builtins.str]:
            '''A ``JsonPath`` string defining the JSON data for the classifier to classify.

            AWS Glue supports a subset of ``JsonPath`` , as described in `Writing JsonPath Custom Classifiers <https://docs.aws.amazon.com/glue/latest/dg/custom-classifier.html#custom-classifier-json>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-jsonclassifier.html#cfn-glue-classifier-jsonclassifier-jsonpath
            '''
            result = self._values.get("json_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the classifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-jsonclassifier.html#cfn-glue-classifier-jsonclassifier-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JsonClassifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnClassifierPropsMixin.XMLClassifierProperty",
        jsii_struct_bases=[],
        name_mapping={
            "classification": "classification",
            "name": "name",
            "row_tag": "rowTag",
        },
    )
    class XMLClassifierProperty:
        def __init__(
            self,
            *,
            classification: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            row_tag: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A classifier for ``XML`` content.

            :param classification: An identifier of the data format that the classifier matches.
            :param name: The name of the classifier.
            :param row_tag: The XML tag designating the element that contains each record in an XML document being parsed. This can't identify a self-closing element (closed by ``/>`` ). An empty row element that contains only attributes can be parsed as long as it ends with a closing tag (for example, ``<row item_a="A" item_b="B"></row>`` is okay, but ``<row item_a="A" item_b="B" />`` is not).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-xmlclassifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                x_mLClassifier_property = glue_mixins.CfnClassifierPropsMixin.XMLClassifierProperty(
                    classification="classification",
                    name="name",
                    row_tag="rowTag"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9ddec36e9ab9edde40b8061cf7096f02514c446958bda21013ead9166bf97b6)
                check_type(argname="argument classification", value=classification, expected_type=type_hints["classification"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument row_tag", value=row_tag, expected_type=type_hints["row_tag"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if classification is not None:
                self._values["classification"] = classification
            if name is not None:
                self._values["name"] = name
            if row_tag is not None:
                self._values["row_tag"] = row_tag

        @builtins.property
        def classification(self) -> typing.Optional[builtins.str]:
            '''An identifier of the data format that the classifier matches.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-xmlclassifier.html#cfn-glue-classifier-xmlclassifier-classification
            '''
            result = self._values.get("classification")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the classifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-xmlclassifier.html#cfn-glue-classifier-xmlclassifier-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def row_tag(self) -> typing.Optional[builtins.str]:
            '''The XML tag designating the element that contains each record in an XML document being parsed.

            This can't identify a self-closing element (closed by ``/>`` ). An empty row element that contains only attributes can be parsed as long as it ends with a closing tag (for example, ``<row item_a="A" item_b="B"></row>`` is okay, but ``<row item_a="A" item_b="B" />`` is not).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-xmlclassifier.html#cfn-glue-classifier-xmlclassifier-rowtag
            '''
            result = self._values.get("row_tag")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "XMLClassifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"catalog_id": "catalogId", "connection_input": "connectionInput"},
)
class CfnConnectionMixinProps:
    def __init__(
        self,
        *,
        catalog_id: typing.Optional[builtins.str] = None,
        connection_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.ConnectionInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConnectionPropsMixin.

        :param catalog_id: The ID of the data catalog to create the catalog object in. Currently, this should be the AWS account ID. .. epigraph:: To specify the account ID, you can use the ``Ref`` intrinsic function with the ``AWS::AccountId`` pseudo parameter. For example: ``!Ref AWS::AccountId`` .
        :param connection_input: The connection that you want to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # athena_properties: Any
            # connection_properties: Any
            # custom_authentication_credentials: Any
            # python_properties: Any
            # spark_properties: Any
            # token_url_parameters_map: Any
            
            cfn_connection_mixin_props = glue_mixins.CfnConnectionMixinProps(
                catalog_id="catalogId",
                connection_input=glue_mixins.CfnConnectionPropsMixin.ConnectionInputProperty(
                    athena_properties=athena_properties,
                    authentication_configuration=glue_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                        authentication_type="authenticationType",
                        basic_authentication_credentials=glue_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        custom_authentication_credentials=custom_authentication_credentials,
                        kms_key_arn="kmsKeyArn",
                        o_auth2_properties=glue_mixins.CfnConnectionPropsMixin.OAuth2PropertiesInputProperty(
                            authorization_code_properties=glue_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                                authorization_code="authorizationCode",
                                redirect_uri="redirectUri"
                            ),
                            o_auth2_client_application=glue_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                                aws_managed_client_application_reference="awsManagedClientApplicationReference",
                                user_managed_client_application_client_id="userManagedClientApplicationClientId"
                            ),
                            o_auth2_credentials=glue_mixins.CfnConnectionPropsMixin.OAuth2CredentialsProperty(
                                access_token="accessToken",
                                jwt_token="jwtToken",
                                refresh_token="refreshToken",
                                user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                            ),
                            o_auth2_grant_type="oAuth2GrantType",
                            token_url="tokenUrl",
                            token_url_parameters_map=token_url_parameters_map
                        ),
                        secret_arn="secretArn"
                    ),
                    connection_properties=connection_properties,
                    connection_type="connectionType",
                    description="description",
                    match_criteria=["matchCriteria"],
                    name="name",
                    physical_connection_requirements=glue_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                        availability_zone="availabilityZone",
                        security_group_id_list=["securityGroupIdList"],
                        subnet_id="subnetId"
                    ),
                    python_properties=python_properties,
                    spark_properties=spark_properties,
                    validate_credentials=False,
                    validate_for_compute_environments=["validateForComputeEnvironments"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14a0dd4ebf682b363d565828f16a20435253b82d94430509c4cbe80300fc9f1)
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument connection_input", value=connection_input, expected_type=type_hints["connection_input"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id
        if connection_input is not None:
            self._values["connection_input"] = connection_input

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the data catalog to create the catalog object in.

        Currently, this should be the AWS account ID.
        .. epigraph::

           To specify the account ID, you can use the ``Ref`` intrinsic function with the ``AWS::AccountId`` pseudo parameter. For example: ``!Ref AWS::AccountId`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html#cfn-glue-connection-catalogid
        '''
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_input(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.ConnectionInputProperty"]]:
        '''The connection that you want to create.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html#cfn-glue-connection-connectioninput
        '''
        result = self._values.get("connection_input")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.ConnectionInputProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionPropsMixin",
):
    '''The ``AWS::Glue::Connection`` resource specifies an AWS Glue connection to a data source.

    For more information, see `Adding a Connection to Your Data Store <https://docs.aws.amazon.com/glue/latest/dg/populate-add-connection.html>`_ and `Connection Structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-connections.html#aws-glue-api-catalog-connections-Connection>`_ in the *AWS Glue Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html
    :cloudformationResource: AWS::Glue::Connection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # athena_properties: Any
        # connection_properties: Any
        # custom_authentication_credentials: Any
        # python_properties: Any
        # spark_properties: Any
        # token_url_parameters_map: Any
        
        cfn_connection_props_mixin = glue_mixins.CfnConnectionPropsMixin(glue_mixins.CfnConnectionMixinProps(
            catalog_id="catalogId",
            connection_input=glue_mixins.CfnConnectionPropsMixin.ConnectionInputProperty(
                athena_properties=athena_properties,
                authentication_configuration=glue_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                    authentication_type="authenticationType",
                    basic_authentication_credentials=glue_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    custom_authentication_credentials=custom_authentication_credentials,
                    kms_key_arn="kmsKeyArn",
                    o_auth2_properties=glue_mixins.CfnConnectionPropsMixin.OAuth2PropertiesInputProperty(
                        authorization_code_properties=glue_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                            authorization_code="authorizationCode",
                            redirect_uri="redirectUri"
                        ),
                        o_auth2_client_application=glue_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                            aws_managed_client_application_reference="awsManagedClientApplicationReference",
                            user_managed_client_application_client_id="userManagedClientApplicationClientId"
                        ),
                        o_auth2_credentials=glue_mixins.CfnConnectionPropsMixin.OAuth2CredentialsProperty(
                            access_token="accessToken",
                            jwt_token="jwtToken",
                            refresh_token="refreshToken",
                            user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                        ),
                        o_auth2_grant_type="oAuth2GrantType",
                        token_url="tokenUrl",
                        token_url_parameters_map=token_url_parameters_map
                    ),
                    secret_arn="secretArn"
                ),
                connection_properties=connection_properties,
                connection_type="connectionType",
                description="description",
                match_criteria=["matchCriteria"],
                name="name",
                physical_connection_requirements=glue_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                    availability_zone="availabilityZone",
                    security_group_id_list=["securityGroupIdList"],
                    subnet_id="subnetId"
                ),
                python_properties=python_properties,
                spark_properties=spark_properties,
                validate_credentials=False,
                validate_for_compute_environments=["validateForComputeEnvironments"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Connection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9342d375f92c26181765ba372b72d4a888c65776b82d430b08b98b3261ce2e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edf79752abdfbfbfd8ab59bbbb1d022355efb6efb6ec6ec1437049d72e725c0b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7725c9a46b4945b8c193d47f91bbd0f1708d2b09b089e11bbcc3d9fce8b4091)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectionMixinProps:
        return typing.cast(CfnConnectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_type": "authenticationType",
            "basic_authentication_credentials": "basicAuthenticationCredentials",
            "custom_authentication_credentials": "customAuthenticationCredentials",
            "kms_key_arn": "kmsKeyArn",
            "o_auth2_properties": "oAuth2Properties",
            "secret_arn": "secretArn",
        },
    )
    class AuthenticationConfigurationInputProperty:
        def __init__(
            self,
            *,
            authentication_type: typing.Optional[builtins.str] = None,
            basic_authentication_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_authentication_credentials: typing.Any = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
            o_auth2_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.OAuth2PropertiesInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secret_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure containing the authentication configuration in the CreateConnection request.

            :param authentication_type: A structure containing the authentication configuration in the CreateConnection request.
            :param basic_authentication_credentials: The credentials used when the authentication type is basic authentication.
            :param custom_authentication_credentials: The credentials used when the authentication type is custom authentication.
            :param kms_key_arn: The ARN of the KMS key used to encrypt the connection. Only taken an as input in the request and stored in the Secret Manager.
            :param o_auth2_properties: The properties for OAuth2 authentication in the CreateConnection request.
            :param secret_arn: The secret manager ARN to store credentials in the CreateConnection request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authenticationconfigurationinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # custom_authentication_credentials: Any
                # token_url_parameters_map: Any
                
                authentication_configuration_input_property = glue_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                    authentication_type="authenticationType",
                    basic_authentication_credentials=glue_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                        password="password",
                        username="username"
                    ),
                    custom_authentication_credentials=custom_authentication_credentials,
                    kms_key_arn="kmsKeyArn",
                    o_auth2_properties=glue_mixins.CfnConnectionPropsMixin.OAuth2PropertiesInputProperty(
                        authorization_code_properties=glue_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                            authorization_code="authorizationCode",
                            redirect_uri="redirectUri"
                        ),
                        o_auth2_client_application=glue_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                            aws_managed_client_application_reference="awsManagedClientApplicationReference",
                            user_managed_client_application_client_id="userManagedClientApplicationClientId"
                        ),
                        o_auth2_credentials=glue_mixins.CfnConnectionPropsMixin.OAuth2CredentialsProperty(
                            access_token="accessToken",
                            jwt_token="jwtToken",
                            refresh_token="refreshToken",
                            user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                        ),
                        o_auth2_grant_type="oAuth2GrantType",
                        token_url="tokenUrl",
                        token_url_parameters_map=token_url_parameters_map
                    ),
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cccd6fee54bb9af757e17690876727409506f68317509bbd4856b1e45ced3ef)
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
                check_type(argname="argument basic_authentication_credentials", value=basic_authentication_credentials, expected_type=type_hints["basic_authentication_credentials"])
                check_type(argname="argument custom_authentication_credentials", value=custom_authentication_credentials, expected_type=type_hints["custom_authentication_credentials"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument o_auth2_properties", value=o_auth2_properties, expected_type=type_hints["o_auth2_properties"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_type is not None:
                self._values["authentication_type"] = authentication_type
            if basic_authentication_credentials is not None:
                self._values["basic_authentication_credentials"] = basic_authentication_credentials
            if custom_authentication_credentials is not None:
                self._values["custom_authentication_credentials"] = custom_authentication_credentials
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if o_auth2_properties is not None:
                self._values["o_auth2_properties"] = o_auth2_properties
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def authentication_type(self) -> typing.Optional[builtins.str]:
            '''A structure containing the authentication configuration in the CreateConnection request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authenticationconfigurationinput.html#cfn-glue-connection-authenticationconfigurationinput-authenticationtype
            '''
            result = self._values.get("authentication_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def basic_authentication_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty"]]:
            '''The credentials used when the authentication type is basic authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authenticationconfigurationinput.html#cfn-glue-connection-authenticationconfigurationinput-basicauthenticationcredentials
            '''
            result = self._values.get("basic_authentication_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty"]], result)

        @builtins.property
        def custom_authentication_credentials(self) -> typing.Any:
            '''The credentials used when the authentication type is custom authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authenticationconfigurationinput.html#cfn-glue-connection-authenticationconfigurationinput-customauthenticationcredentials
            '''
            result = self._values.get("custom_authentication_credentials")
            return typing.cast(typing.Any, result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key used to encrypt the connection.

            Only taken an as input in the request and stored in the Secret Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authenticationconfigurationinput.html#cfn-glue-connection-authenticationconfigurationinput-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def o_auth2_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2PropertiesInputProperty"]]:
            '''The properties for OAuth2 authentication in the CreateConnection request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authenticationconfigurationinput.html#cfn-glue-connection-authenticationconfigurationinput-oauth2properties
            '''
            result = self._values.get("o_auth2_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2PropertiesInputProperty"]], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The secret manager ARN to store credentials in the CreateConnection request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authenticationconfigurationinput.html#cfn-glue-connection-authenticationconfigurationinput-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticationConfigurationInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_code": "authorizationCode",
            "redirect_uri": "redirectUri",
        },
    )
    class AuthorizationCodePropertiesProperty:
        def __init__(
            self,
            *,
            authorization_code: typing.Optional[builtins.str] = None,
            redirect_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The set of properties required for the the OAuth2 ``AUTHORIZATION_CODE`` grant type workflow.

            :param authorization_code: An authorization code to be used in the third leg of the ``AUTHORIZATION_CODE`` grant workflow. This is a single-use code which becomes invalid once exchanged for an access token, thus it is acceptable to have this value as a request parameter.
            :param redirect_uri: The redirect URI where the user gets redirected to by authorization server when issuing an authorization code. The URI is subsequently used when the authorization code is exchanged for an access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authorizationcodeproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                authorization_code_properties_property = glue_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                    authorization_code="authorizationCode",
                    redirect_uri="redirectUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2eba12f7720b93f538af88b9fbeb1ab7ae77ad738cb468fee4f83262be64bf4d)
                check_type(argname="argument authorization_code", value=authorization_code, expected_type=type_hints["authorization_code"])
                check_type(argname="argument redirect_uri", value=redirect_uri, expected_type=type_hints["redirect_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_code is not None:
                self._values["authorization_code"] = authorization_code
            if redirect_uri is not None:
                self._values["redirect_uri"] = redirect_uri

        @builtins.property
        def authorization_code(self) -> typing.Optional[builtins.str]:
            '''An authorization code to be used in the third leg of the ``AUTHORIZATION_CODE`` grant workflow.

            This is a single-use code which becomes invalid once exchanged for an access token, thus it is acceptable to have this value as a request parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authorizationcodeproperties.html#cfn-glue-connection-authorizationcodeproperties-authorizationcode
            '''
            result = self._values.get("authorization_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def redirect_uri(self) -> typing.Optional[builtins.str]:
            '''The redirect URI where the user gets redirected to by authorization server when issuing an authorization code.

            The URI is subsequently used when the authorization code is exchanged for an access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-authorizationcodeproperties.html#cfn-glue-connection-authorizationcodeproperties-redirecturi
            '''
            result = self._values.get("redirect_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationCodePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class BasicAuthenticationCredentialsProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''For supplying basic auth credentials when not providing a ``SecretArn`` value.

            :param password: The password to connect to the data source.
            :param username: The username to connect to the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-basicauthenticationcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                basic_authentication_credentials_property = glue_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ead1ecbd398cd04a745e081a08867f97c81840b1ee6333ba99da63d17dd0e89)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password to connect to the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-basicauthenticationcredentials.html#cfn-glue-connection-basicauthenticationcredentials-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The username to connect to the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-basicauthenticationcredentials.html#cfn-glue-connection-basicauthenticationcredentials-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthenticationCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionPropsMixin.ConnectionInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "athena_properties": "athenaProperties",
            "authentication_configuration": "authenticationConfiguration",
            "connection_properties": "connectionProperties",
            "connection_type": "connectionType",
            "description": "description",
            "match_criteria": "matchCriteria",
            "name": "name",
            "physical_connection_requirements": "physicalConnectionRequirements",
            "python_properties": "pythonProperties",
            "spark_properties": "sparkProperties",
            "validate_credentials": "validateCredentials",
            "validate_for_compute_environments": "validateForComputeEnvironments",
        },
    )
    class ConnectionInputProperty:
        def __init__(
            self,
            *,
            athena_properties: typing.Any = None,
            authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            connection_properties: typing.Any = None,
            connection_type: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            match_criteria: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            physical_connection_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            python_properties: typing.Any = None,
            spark_properties: typing.Any = None,
            validate_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            validate_for_compute_environments: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A structure that is used to specify a connection to create or update.

            :param athena_properties: Connection properties specific to the Athena compute environment.
            :param authentication_configuration: The authentication properties of the connection.
            :param connection_properties: These key-value pairs define parameters for the connection.
            :param connection_type: The type of the connection. Currently, these types are supported:. - ``JDBC`` - Designates a connection to a database through Java Database Connectivity (JDBC). ``JDBC`` Connections use the following ConnectionParameters. - Required: All of ( ``HOST`` , ``PORT`` , ``JDBC_ENGINE`` ) or ``JDBC_CONNECTION_URL`` . - Required: All of ( ``USERNAME`` , ``PASSWORD`` ) or ``SECRET_ID`` . - Optional: ``JDBC_ENFORCE_SSL`` , ``CUSTOM_JDBC_CERT`` , ``CUSTOM_JDBC_CERT_STRING`` , ``SKIP_CUSTOM_JDBC_CERT_VALIDATION`` . These parameters are used to configure SSL with JDBC. - ``KAFKA`` - Designates a connection to an Apache Kafka streaming platform. ``KAFKA`` Connections use the following ConnectionParameters. - Required: ``KAFKA_BOOTSTRAP_SERVERS`` . - Optional: ``KAFKA_SSL_ENABLED`` , ``KAFKA_CUSTOM_CERT`` , ``KAFKA_SKIP_CUSTOM_CERT_VALIDATION`` . These parameters are used to configure SSL with ``KAFKA`` . - Optional: ``KAFKA_CLIENT_KEYSTORE`` , ``KAFKA_CLIENT_KEYSTORE_PASSWORD`` , ``KAFKA_CLIENT_KEY_PASSWORD`` , ``ENCRYPTED_KAFKA_CLIENT_KEYSTORE_PASSWORD`` , ``ENCRYPTED_KAFKA_CLIENT_KEY_PASSWORD`` . These parameters are used to configure TLS client configuration with SSL in ``KAFKA`` . - Optional: ``KAFKA_SASL_MECHANISM`` . Can be specified as ``SCRAM-SHA-512`` , ``GSSAPI`` , or ``AWS_MSK_IAM`` . - Optional: ``KAFKA_SASL_SCRAM_USERNAME`` , ``KAFKA_SASL_SCRAM_PASSWORD`` , ``ENCRYPTED_KAFKA_SASL_SCRAM_PASSWORD`` . These parameters are used to configure SASL/SCRAM-SHA-512 authentication with ``KAFKA`` . - Optional: ``KAFKA_SASL_GSSAPI_KEYTAB`` , ``KAFKA_SASL_GSSAPI_KRB5_CONF`` , ``KAFKA_SASL_GSSAPI_SERVICE`` , ``KAFKA_SASL_GSSAPI_PRINCIPAL`` . These parameters are used to configure SASL/GSSAPI authentication with ``KAFKA`` . - ``MONGODB`` - Designates a connection to a MongoDB document database. ``MONGODB`` Connections use the following ConnectionParameters. - Required: ``CONNECTION_URL`` . - Required: All of ( ``USERNAME`` , ``PASSWORD`` ) or ``SECRET_ID`` . - ``VIEW_VALIDATION_REDSHIFT`` - Designates a connection used for view validation by Amazon Redshift. - ``VIEW_VALIDATION_ATHENA`` - Designates a connection used for view validation by Amazon Athena. - ``NETWORK`` - Designates a network connection to a data source within an Amazon Virtual Private Cloud environment (Amazon VPC). ``NETWORK`` Connections do not require ConnectionParameters. Instead, provide a PhysicalConnectionRequirements. - ``MARKETPLACE`` - Uses configuration settings contained in a connector purchased from AWS Marketplace to read from and write to data stores that are not natively supported by AWS Glue . ``MARKETPLACE`` Connections use the following ConnectionParameters. - Required: ``CONNECTOR_TYPE`` , ``CONNECTOR_URL`` , ``CONNECTOR_CLASS_NAME`` , ``CONNECTION_URL`` . - Required for ``JDBC`` ``CONNECTOR_TYPE`` connections: All of ( ``USERNAME`` , ``PASSWORD`` ) or ``SECRET_ID`` . - ``CUSTOM`` - Uses configuration settings contained in a custom connector to read from and write to data stores that are not natively supported by AWS Glue . Additionally, a ``ConnectionType`` for the following SaaS connectors is supported: - ``FACEBOOKADS`` - Designates a connection to Facebook Ads. - ``GOOGLEADS`` - Designates a connection to Google Ads. - ``GOOGLESHEETS`` - Designates a connection to Google Sheets. - ``GOOGLEANALYTICS4`` - Designates a connection to Google Analytics 4. - ``HUBSPOT`` - Designates a connection to HubSpot. - ``INSTAGRAMADS`` - Designates a connection to Instagram Ads. - ``INTERCOM`` - Designates a connection to Intercom. - ``JIRACLOUD`` - Designates a connection to Jira Cloud. - ``MARKETO`` - Designates a connection to Adobe Marketo Engage. - ``NETSUITEERP`` - Designates a connection to Oracle NetSuite. - ``SALESFORCE`` - Designates a connection to Salesforce using OAuth authentication. - ``SALESFORCEMARKETINGCLOUD`` - Designates a connection to Salesforce Marketing Cloud. - ``SALESFORCEPARDOT`` - Designates a connection to Salesforce Marketing Cloud Account Engagement (MCAE). - ``SAPODATA`` - Designates a connection to SAP OData. - ``SERVICENOW`` - Designates a connection to ServiceNow. - ``SLACK`` - Designates a connection to Slack. - ``SNAPCHATADS`` - Designates a connection to Snapchat Ads. - ``STRIPE`` - Designates a connection to Stripe. - ``ZENDESK`` - Designates a connection to Zendesk. - ``ZOHOCRM`` - Designates a connection to Zoho CRM. For more information on the connection parameters needed for a particular connector, see the documentation for the connector in `Adding an AWS Glue connection <https://docs.aws.amazon.com/glue/latest/dg/console-connections.html>`_ in the AWS Glue User Guide. ``SFTP`` is not supported. For more information about how optional ConnectionProperties are used to configure features in AWS Glue , consult `AWS Glue connection properties <https://docs.aws.amazon.com/glue/latest/dg/connection-defining.html>`_ . For more information about how optional ConnectionProperties are used to configure features in AWS Glue Studio, consult `Using connectors and connections <https://docs.aws.amazon.com/glue/latest/ug/connectors-chapter.html>`_ .
            :param description: The description of the connection.
            :param match_criteria: A list of criteria that can be used in selecting this connection.
            :param name: The name of the connection.
            :param physical_connection_requirements: The physical connection requirements, such as virtual private cloud (VPC) and ``SecurityGroup`` , that are needed to successfully make this connection.
            :param python_properties: Connection properties specific to the Python compute environment.
            :param spark_properties: Connection properties specific to the Spark compute environment.
            :param validate_credentials: A flag to validate the credentials during create connection. Default is true.
            :param validate_for_compute_environments: The compute environments that the specified connection properties are validated against.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # athena_properties: Any
                # connection_properties: Any
                # custom_authentication_credentials: Any
                # python_properties: Any
                # spark_properties: Any
                # token_url_parameters_map: Any
                
                connection_input_property = glue_mixins.CfnConnectionPropsMixin.ConnectionInputProperty(
                    athena_properties=athena_properties,
                    authentication_configuration=glue_mixins.CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty(
                        authentication_type="authenticationType",
                        basic_authentication_credentials=glue_mixins.CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty(
                            password="password",
                            username="username"
                        ),
                        custom_authentication_credentials=custom_authentication_credentials,
                        kms_key_arn="kmsKeyArn",
                        o_auth2_properties=glue_mixins.CfnConnectionPropsMixin.OAuth2PropertiesInputProperty(
                            authorization_code_properties=glue_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                                authorization_code="authorizationCode",
                                redirect_uri="redirectUri"
                            ),
                            o_auth2_client_application=glue_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                                aws_managed_client_application_reference="awsManagedClientApplicationReference",
                                user_managed_client_application_client_id="userManagedClientApplicationClientId"
                            ),
                            o_auth2_credentials=glue_mixins.CfnConnectionPropsMixin.OAuth2CredentialsProperty(
                                access_token="accessToken",
                                jwt_token="jwtToken",
                                refresh_token="refreshToken",
                                user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                            ),
                            o_auth2_grant_type="oAuth2GrantType",
                            token_url="tokenUrl",
                            token_url_parameters_map=token_url_parameters_map
                        ),
                        secret_arn="secretArn"
                    ),
                    connection_properties=connection_properties,
                    connection_type="connectionType",
                    description="description",
                    match_criteria=["matchCriteria"],
                    name="name",
                    physical_connection_requirements=glue_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                        availability_zone="availabilityZone",
                        security_group_id_list=["securityGroupIdList"],
                        subnet_id="subnetId"
                    ),
                    python_properties=python_properties,
                    spark_properties=spark_properties,
                    validate_credentials=False,
                    validate_for_compute_environments=["validateForComputeEnvironments"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1726516f50694ab83d14d2bce6329e3d17c32df781534dc5a8130363b2186f1)
                check_type(argname="argument athena_properties", value=athena_properties, expected_type=type_hints["athena_properties"])
                check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                check_type(argname="argument connection_properties", value=connection_properties, expected_type=type_hints["connection_properties"])
                check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument match_criteria", value=match_criteria, expected_type=type_hints["match_criteria"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument physical_connection_requirements", value=physical_connection_requirements, expected_type=type_hints["physical_connection_requirements"])
                check_type(argname="argument python_properties", value=python_properties, expected_type=type_hints["python_properties"])
                check_type(argname="argument spark_properties", value=spark_properties, expected_type=type_hints["spark_properties"])
                check_type(argname="argument validate_credentials", value=validate_credentials, expected_type=type_hints["validate_credentials"])
                check_type(argname="argument validate_for_compute_environments", value=validate_for_compute_environments, expected_type=type_hints["validate_for_compute_environments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if athena_properties is not None:
                self._values["athena_properties"] = athena_properties
            if authentication_configuration is not None:
                self._values["authentication_configuration"] = authentication_configuration
            if connection_properties is not None:
                self._values["connection_properties"] = connection_properties
            if connection_type is not None:
                self._values["connection_type"] = connection_type
            if description is not None:
                self._values["description"] = description
            if match_criteria is not None:
                self._values["match_criteria"] = match_criteria
            if name is not None:
                self._values["name"] = name
            if physical_connection_requirements is not None:
                self._values["physical_connection_requirements"] = physical_connection_requirements
            if python_properties is not None:
                self._values["python_properties"] = python_properties
            if spark_properties is not None:
                self._values["spark_properties"] = spark_properties
            if validate_credentials is not None:
                self._values["validate_credentials"] = validate_credentials
            if validate_for_compute_environments is not None:
                self._values["validate_for_compute_environments"] = validate_for_compute_environments

        @builtins.property
        def athena_properties(self) -> typing.Any:
            '''Connection properties specific to the Athena compute environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-athenaproperties
            '''
            result = self._values.get("athena_properties")
            return typing.cast(typing.Any, result)

        @builtins.property
        def authentication_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty"]]:
            '''The authentication properties of the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-authenticationconfiguration
            '''
            result = self._values.get("authentication_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty"]], result)

        @builtins.property
        def connection_properties(self) -> typing.Any:
            '''These key-value pairs define parameters for the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectionproperties
            '''
            result = self._values.get("connection_properties")
            return typing.cast(typing.Any, result)

        @builtins.property
        def connection_type(self) -> typing.Optional[builtins.str]:
            '''The type of the connection. Currently, these types are supported:.

            - ``JDBC`` - Designates a connection to a database through Java Database Connectivity (JDBC).

            ``JDBC`` Connections use the following ConnectionParameters.

            - Required: All of ( ``HOST`` , ``PORT`` , ``JDBC_ENGINE`` ) or ``JDBC_CONNECTION_URL`` .
            - Required: All of ( ``USERNAME`` , ``PASSWORD`` ) or ``SECRET_ID`` .
            - Optional: ``JDBC_ENFORCE_SSL`` , ``CUSTOM_JDBC_CERT`` , ``CUSTOM_JDBC_CERT_STRING`` , ``SKIP_CUSTOM_JDBC_CERT_VALIDATION`` . These parameters are used to configure SSL with JDBC.
            - ``KAFKA`` - Designates a connection to an Apache Kafka streaming platform.

            ``KAFKA`` Connections use the following ConnectionParameters.

            - Required: ``KAFKA_BOOTSTRAP_SERVERS`` .
            - Optional: ``KAFKA_SSL_ENABLED`` , ``KAFKA_CUSTOM_CERT`` , ``KAFKA_SKIP_CUSTOM_CERT_VALIDATION`` . These parameters are used to configure SSL with ``KAFKA`` .
            - Optional: ``KAFKA_CLIENT_KEYSTORE`` , ``KAFKA_CLIENT_KEYSTORE_PASSWORD`` , ``KAFKA_CLIENT_KEY_PASSWORD`` , ``ENCRYPTED_KAFKA_CLIENT_KEYSTORE_PASSWORD`` , ``ENCRYPTED_KAFKA_CLIENT_KEY_PASSWORD`` . These parameters are used to configure TLS client configuration with SSL in ``KAFKA`` .
            - Optional: ``KAFKA_SASL_MECHANISM`` . Can be specified as ``SCRAM-SHA-512`` , ``GSSAPI`` , or ``AWS_MSK_IAM`` .
            - Optional: ``KAFKA_SASL_SCRAM_USERNAME`` , ``KAFKA_SASL_SCRAM_PASSWORD`` , ``ENCRYPTED_KAFKA_SASL_SCRAM_PASSWORD`` . These parameters are used to configure SASL/SCRAM-SHA-512 authentication with ``KAFKA`` .
            - Optional: ``KAFKA_SASL_GSSAPI_KEYTAB`` , ``KAFKA_SASL_GSSAPI_KRB5_CONF`` , ``KAFKA_SASL_GSSAPI_SERVICE`` , ``KAFKA_SASL_GSSAPI_PRINCIPAL`` . These parameters are used to configure SASL/GSSAPI authentication with ``KAFKA`` .
            - ``MONGODB`` - Designates a connection to a MongoDB document database.

            ``MONGODB`` Connections use the following ConnectionParameters.

            - Required: ``CONNECTION_URL`` .
            - Required: All of ( ``USERNAME`` , ``PASSWORD`` ) or ``SECRET_ID`` .
            - ``VIEW_VALIDATION_REDSHIFT`` - Designates a connection used for view validation by Amazon Redshift.
            - ``VIEW_VALIDATION_ATHENA`` - Designates a connection used for view validation by Amazon Athena.
            - ``NETWORK`` - Designates a network connection to a data source within an Amazon Virtual Private Cloud environment (Amazon VPC).

            ``NETWORK`` Connections do not require ConnectionParameters. Instead, provide a PhysicalConnectionRequirements.

            - ``MARKETPLACE`` - Uses configuration settings contained in a connector purchased from AWS Marketplace to read from and write to data stores that are not natively supported by AWS Glue .

            ``MARKETPLACE`` Connections use the following ConnectionParameters.

            - Required: ``CONNECTOR_TYPE`` , ``CONNECTOR_URL`` , ``CONNECTOR_CLASS_NAME`` , ``CONNECTION_URL`` .
            - Required for ``JDBC`` ``CONNECTOR_TYPE`` connections: All of ( ``USERNAME`` , ``PASSWORD`` ) or ``SECRET_ID`` .
            - ``CUSTOM`` - Uses configuration settings contained in a custom connector to read from and write to data stores that are not natively supported by AWS Glue .

            Additionally, a ``ConnectionType`` for the following SaaS connectors is supported:

            - ``FACEBOOKADS`` - Designates a connection to Facebook Ads.
            - ``GOOGLEADS`` - Designates a connection to Google Ads.
            - ``GOOGLESHEETS`` - Designates a connection to Google Sheets.
            - ``GOOGLEANALYTICS4`` - Designates a connection to Google Analytics 4.
            - ``HUBSPOT`` - Designates a connection to HubSpot.
            - ``INSTAGRAMADS`` - Designates a connection to Instagram Ads.
            - ``INTERCOM`` - Designates a connection to Intercom.
            - ``JIRACLOUD`` - Designates a connection to Jira Cloud.
            - ``MARKETO`` - Designates a connection to Adobe Marketo Engage.
            - ``NETSUITEERP`` - Designates a connection to Oracle NetSuite.
            - ``SALESFORCE`` - Designates a connection to Salesforce using OAuth authentication.
            - ``SALESFORCEMARKETINGCLOUD`` - Designates a connection to Salesforce Marketing Cloud.
            - ``SALESFORCEPARDOT`` - Designates a connection to Salesforce Marketing Cloud Account Engagement (MCAE).
            - ``SAPODATA`` - Designates a connection to SAP OData.
            - ``SERVICENOW`` - Designates a connection to ServiceNow.
            - ``SLACK`` - Designates a connection to Slack.
            - ``SNAPCHATADS`` - Designates a connection to Snapchat Ads.
            - ``STRIPE`` - Designates a connection to Stripe.
            - ``ZENDESK`` - Designates a connection to Zendesk.
            - ``ZOHOCRM`` - Designates a connection to Zoho CRM.

            For more information on the connection parameters needed for a particular connector, see the documentation for the connector in `Adding an AWS Glue connection <https://docs.aws.amazon.com/glue/latest/dg/console-connections.html>`_ in the AWS Glue User Guide.

            ``SFTP`` is not supported.

            For more information about how optional ConnectionProperties are used to configure features in AWS Glue , consult `AWS Glue connection properties <https://docs.aws.amazon.com/glue/latest/dg/connection-defining.html>`_ .

            For more information about how optional ConnectionProperties are used to configure features in AWS Glue Studio, consult `Using connectors and connections <https://docs.aws.amazon.com/glue/latest/ug/connectors-chapter.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectiontype
            '''
            result = self._values.get("connection_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_criteria(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of criteria that can be used in selecting this connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-matchcriteria
            '''
            result = self._values.get("match_criteria")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def physical_connection_requirements(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty"]]:
            '''The physical connection requirements, such as virtual private cloud (VPC) and ``SecurityGroup`` , that are needed to successfully make this connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-physicalconnectionrequirements
            '''
            result = self._values.get("physical_connection_requirements")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty"]], result)

        @builtins.property
        def python_properties(self) -> typing.Any:
            '''Connection properties specific to the Python compute environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-pythonproperties
            '''
            result = self._values.get("python_properties")
            return typing.cast(typing.Any, result)

        @builtins.property
        def spark_properties(self) -> typing.Any:
            '''Connection properties specific to the Spark compute environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-sparkproperties
            '''
            result = self._values.get("spark_properties")
            return typing.cast(typing.Any, result)

        @builtins.property
        def validate_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A flag to validate the credentials during create connection.

            Default is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-validatecredentials
            '''
            result = self._values.get("validate_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def validate_for_compute_environments(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The compute environments that the specified connection properties are validated against.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-validateforcomputeenvironments
            '''
            result = self._values.get("validate_for_compute_environments")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_managed_client_application_reference": "awsManagedClientApplicationReference",
            "user_managed_client_application_client_id": "userManagedClientApplicationClientId",
        },
    )
    class OAuth2ClientApplicationProperty:
        def __init__(
            self,
            *,
            aws_managed_client_application_reference: typing.Optional[builtins.str] = None,
            user_managed_client_application_client_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OAuth2 client app used for the connection.

            :param aws_managed_client_application_reference: The reference to the SaaS-side client app that is AWS managed.
            :param user_managed_client_application_client_id: The client application clientID if the ClientAppType is ``USER_MANAGED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2clientapplication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                o_auth2_client_application_property = glue_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                    aws_managed_client_application_reference="awsManagedClientApplicationReference",
                    user_managed_client_application_client_id="userManagedClientApplicationClientId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7d38843083b9ed03899415af369ca2f43e12164bac8734f8a9f4bfa819179fb)
                check_type(argname="argument aws_managed_client_application_reference", value=aws_managed_client_application_reference, expected_type=type_hints["aws_managed_client_application_reference"])
                check_type(argname="argument user_managed_client_application_client_id", value=user_managed_client_application_client_id, expected_type=type_hints["user_managed_client_application_client_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_managed_client_application_reference is not None:
                self._values["aws_managed_client_application_reference"] = aws_managed_client_application_reference
            if user_managed_client_application_client_id is not None:
                self._values["user_managed_client_application_client_id"] = user_managed_client_application_client_id

        @builtins.property
        def aws_managed_client_application_reference(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The reference to the SaaS-side client app that is AWS managed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2clientapplication.html#cfn-glue-connection-oauth2clientapplication-awsmanagedclientapplicationreference
            '''
            result = self._values.get("aws_managed_client_application_reference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_managed_client_application_client_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The client application clientID if the ClientAppType is ``USER_MANAGED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2clientapplication.html#cfn-glue-connection-oauth2clientapplication-usermanagedclientapplicationclientid
            '''
            result = self._values.get("user_managed_client_application_client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuth2ClientApplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionPropsMixin.OAuth2CredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "jwt_token": "jwtToken",
            "refresh_token": "refreshToken",
            "user_managed_client_application_client_secret": "userManagedClientApplicationClientSecret",
        },
    )
    class OAuth2CredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            jwt_token: typing.Optional[builtins.str] = None,
            refresh_token: typing.Optional[builtins.str] = None,
            user_managed_client_application_client_secret: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The credentials used when the authentication type is OAuth2 authentication.

            :param access_token: The access token used when the authentication type is OAuth2.
            :param jwt_token: The JSON Web Token (JWT) used when the authentication type is OAuth2.
            :param refresh_token: The refresh token used when the authentication type is OAuth2.
            :param user_managed_client_application_client_secret: The client application client secret if the client application is user managed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2credentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                o_auth2_credentials_property = glue_mixins.CfnConnectionPropsMixin.OAuth2CredentialsProperty(
                    access_token="accessToken",
                    jwt_token="jwtToken",
                    refresh_token="refreshToken",
                    user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d94d02d69c64dae18367fa9cd32d8aa5c3907bf17b35a00ce6facb17ac632d37)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument jwt_token", value=jwt_token, expected_type=type_hints["jwt_token"])
                check_type(argname="argument refresh_token", value=refresh_token, expected_type=type_hints["refresh_token"])
                check_type(argname="argument user_managed_client_application_client_secret", value=user_managed_client_application_client_secret, expected_type=type_hints["user_managed_client_application_client_secret"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if jwt_token is not None:
                self._values["jwt_token"] = jwt_token
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token
            if user_managed_client_application_client_secret is not None:
                self._values["user_managed_client_application_client_secret"] = user_managed_client_application_client_secret

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The access token used when the authentication type is OAuth2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2credentials.html#cfn-glue-connection-oauth2credentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def jwt_token(self) -> typing.Optional[builtins.str]:
            '''The JSON Web Token (JWT) used when the authentication type is OAuth2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2credentials.html#cfn-glue-connection-oauth2credentials-jwttoken
            '''
            result = self._values.get("jwt_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''The refresh token used when the authentication type is OAuth2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2credentials.html#cfn-glue-connection-oauth2credentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_managed_client_application_client_secret(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The client application client secret if the client application is user managed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2credentials.html#cfn-glue-connection-oauth2credentials-usermanagedclientapplicationclientsecret
            '''
            result = self._values.get("user_managed_client_application_client_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuth2CredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionPropsMixin.OAuth2PropertiesInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authorization_code_properties": "authorizationCodeProperties",
            "o_auth2_client_application": "oAuth2ClientApplication",
            "o_auth2_credentials": "oAuth2Credentials",
            "o_auth2_grant_type": "oAuth2GrantType",
            "token_url": "tokenUrl",
            "token_url_parameters_map": "tokenUrlParametersMap",
        },
    )
    class OAuth2PropertiesInputProperty:
        def __init__(
            self,
            *,
            authorization_code_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            o_auth2_client_application: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.OAuth2ClientApplicationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            o_auth2_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectionPropsMixin.OAuth2CredentialsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            o_auth2_grant_type: typing.Optional[builtins.str] = None,
            token_url: typing.Optional[builtins.str] = None,
            token_url_parameters_map: typing.Any = None,
        ) -> None:
            '''A structure containing properties for OAuth2 in the CreateConnection request.

            :param authorization_code_properties: The set of properties required for the the OAuth2 ``AUTHORIZATION_CODE`` grant type.
            :param o_auth2_client_application: The client application type in the CreateConnection request. For example, ``AWS_MANAGED`` or ``USER_MANAGED`` .
            :param o_auth2_credentials: The credentials used when the authentication type is OAuth2 authentication.
            :param o_auth2_grant_type: The OAuth2 grant type in the CreateConnection request. For example, ``AUTHORIZATION_CODE`` , ``JWT_BEARER`` , or ``CLIENT_CREDENTIALS`` .
            :param token_url: The URL of the provider's authentication server, to exchange an authorization code for an access token.
            :param token_url_parameters_map: A map of parameters that are added to the token ``GET`` request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2propertiesinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # token_url_parameters_map: Any
                
                o_auth2_properties_input_property = glue_mixins.CfnConnectionPropsMixin.OAuth2PropertiesInputProperty(
                    authorization_code_properties=glue_mixins.CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty(
                        authorization_code="authorizationCode",
                        redirect_uri="redirectUri"
                    ),
                    o_auth2_client_application=glue_mixins.CfnConnectionPropsMixin.OAuth2ClientApplicationProperty(
                        aws_managed_client_application_reference="awsManagedClientApplicationReference",
                        user_managed_client_application_client_id="userManagedClientApplicationClientId"
                    ),
                    o_auth2_credentials=glue_mixins.CfnConnectionPropsMixin.OAuth2CredentialsProperty(
                        access_token="accessToken",
                        jwt_token="jwtToken",
                        refresh_token="refreshToken",
                        user_managed_client_application_client_secret="userManagedClientApplicationClientSecret"
                    ),
                    o_auth2_grant_type="oAuth2GrantType",
                    token_url="tokenUrl",
                    token_url_parameters_map=token_url_parameters_map
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__498f7ac71532649748c2424404f4924cfc23742bcad4bf8690b43bbb0f3e72b0)
                check_type(argname="argument authorization_code_properties", value=authorization_code_properties, expected_type=type_hints["authorization_code_properties"])
                check_type(argname="argument o_auth2_client_application", value=o_auth2_client_application, expected_type=type_hints["o_auth2_client_application"])
                check_type(argname="argument o_auth2_credentials", value=o_auth2_credentials, expected_type=type_hints["o_auth2_credentials"])
                check_type(argname="argument o_auth2_grant_type", value=o_auth2_grant_type, expected_type=type_hints["o_auth2_grant_type"])
                check_type(argname="argument token_url", value=token_url, expected_type=type_hints["token_url"])
                check_type(argname="argument token_url_parameters_map", value=token_url_parameters_map, expected_type=type_hints["token_url_parameters_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authorization_code_properties is not None:
                self._values["authorization_code_properties"] = authorization_code_properties
            if o_auth2_client_application is not None:
                self._values["o_auth2_client_application"] = o_auth2_client_application
            if o_auth2_credentials is not None:
                self._values["o_auth2_credentials"] = o_auth2_credentials
            if o_auth2_grant_type is not None:
                self._values["o_auth2_grant_type"] = o_auth2_grant_type
            if token_url is not None:
                self._values["token_url"] = token_url
            if token_url_parameters_map is not None:
                self._values["token_url_parameters_map"] = token_url_parameters_map

        @builtins.property
        def authorization_code_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty"]]:
            '''The set of properties required for the the OAuth2 ``AUTHORIZATION_CODE`` grant type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2propertiesinput.html#cfn-glue-connection-oauth2propertiesinput-authorizationcodeproperties
            '''
            result = self._values.get("authorization_code_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty"]], result)

        @builtins.property
        def o_auth2_client_application(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2ClientApplicationProperty"]]:
            '''The client application type in the CreateConnection request.

            For example, ``AWS_MANAGED`` or ``USER_MANAGED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2propertiesinput.html#cfn-glue-connection-oauth2propertiesinput-oauth2clientapplication
            '''
            result = self._values.get("o_auth2_client_application")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2ClientApplicationProperty"]], result)

        @builtins.property
        def o_auth2_credentials(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2CredentialsProperty"]]:
            '''The credentials used when the authentication type is OAuth2 authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2propertiesinput.html#cfn-glue-connection-oauth2propertiesinput-oauth2credentials
            '''
            result = self._values.get("o_auth2_credentials")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectionPropsMixin.OAuth2CredentialsProperty"]], result)

        @builtins.property
        def o_auth2_grant_type(self) -> typing.Optional[builtins.str]:
            '''The OAuth2 grant type in the CreateConnection request.

            For example, ``AUTHORIZATION_CODE`` , ``JWT_BEARER`` , or ``CLIENT_CREDENTIALS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2propertiesinput.html#cfn-glue-connection-oauth2propertiesinput-oauth2granttype
            '''
            result = self._values.get("o_auth2_grant_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the provider's authentication server, to exchange an authorization code for an access token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2propertiesinput.html#cfn-glue-connection-oauth2propertiesinput-tokenurl
            '''
            result = self._values.get("token_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def token_url_parameters_map(self) -> typing.Any:
            '''A map of parameters that are added to the token ``GET`` request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-oauth2propertiesinput.html#cfn-glue-connection-oauth2propertiesinput-tokenurlparametersmap
            '''
            result = self._values.get("token_url_parameters_map")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OAuth2PropertiesInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "security_group_id_list": "securityGroupIdList",
            "subnet_id": "subnetId",
        },
    )
    class PhysicalConnectionRequirementsProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            security_group_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OAuth client app in GetConnection response.

            :param availability_zone: The connection's Availability Zone.
            :param security_group_id_list: The security group ID list used by the connection.
            :param subnet_id: The subnet ID used by the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-physicalconnectionrequirements.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                physical_connection_requirements_property = glue_mixins.CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty(
                    availability_zone="availabilityZone",
                    security_group_id_list=["securityGroupIdList"],
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80d0e42cf5d99d4eb55ba73623cf4c0ce89f80736c2909ab81653b4bec8f9f43)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument security_group_id_list", value=security_group_id_list, expected_type=type_hints["security_group_id_list"])
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if security_group_id_list is not None:
                self._values["security_group_id_list"] = security_group_id_list
            if subnet_id is not None:
                self._values["subnet_id"] = subnet_id

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The connection's Availability Zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-physicalconnectionrequirements.html#cfn-glue-connection-physicalconnectionrequirements-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The security group ID list used by the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-physicalconnectionrequirements.html#cfn-glue-connection-physicalconnectionrequirements-securitygroupidlist
            '''
            result = self._values.get("security_group_id_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_id(self) -> typing.Optional[builtins.str]:
            '''The subnet ID used by the connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-physicalconnectionrequirements.html#cfn-glue-connection-physicalconnectionrequirements-subnetid
            '''
            result = self._values.get("subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PhysicalConnectionRequirementsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "classifiers": "classifiers",
        "configuration": "configuration",
        "crawler_security_configuration": "crawlerSecurityConfiguration",
        "database_name": "databaseName",
        "description": "description",
        "lake_formation_configuration": "lakeFormationConfiguration",
        "name": "name",
        "recrawl_policy": "recrawlPolicy",
        "role": "role",
        "schedule": "schedule",
        "schema_change_policy": "schemaChangePolicy",
        "table_prefix": "tablePrefix",
        "tags": "tags",
        "targets": "targets",
    },
)
class CfnCrawlerMixinProps:
    def __init__(
        self,
        *,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[builtins.str] = None,
        crawler_security_configuration: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        lake_formation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.LakeFormationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        recrawl_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.RecrawlPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schema_change_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.SchemaChangePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_prefix: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.TargetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCrawlerPropsMixin.

        :param classifiers: A list of UTF-8 strings that specify the names of custom classifiers that are associated with the crawler.
        :param configuration: Crawler configuration information. This versioned JSON string allows users to specify aspects of a crawler's behavior. For more information, see `Configuring a Crawler <https://docs.aws.amazon.com/glue/latest/dg/crawler-configuration.html>`_ .
        :param crawler_security_configuration: The name of the ``SecurityConfiguration`` structure to be used by this crawler.
        :param database_name: The name of the database in which the crawler's output is stored.
        :param description: A description of the crawler.
        :param lake_formation_configuration: Specifies whether the crawler should use AWS Lake Formation credentials for the crawler instead of the IAM role credentials.
        :param name: The name of the crawler.
        :param recrawl_policy: A policy that specifies whether to crawl the entire dataset again, or to crawl only folders that were added since the last crawler run.
        :param role: The Amazon Resource Name (ARN) of an IAM role that's used to access customer resources, such as Amazon Simple Storage Service (Amazon S3) data.
        :param schedule: For scheduled crawlers, the schedule when the crawler runs.
        :param schema_change_policy: The policy that specifies update and delete behaviors for the crawler. The policy tells the crawler what to do in the event that it detects a change in a table that already exists in the customer's database at the time of the crawl. The ``SchemaChangePolicy`` does not affect whether or how new tables and partitions are added. New tables and partitions are always created regardless of the ``SchemaChangePolicy`` on a crawler. The SchemaChangePolicy consists of two components, ``UpdateBehavior`` and ``DeleteBehavior`` .
        :param table_prefix: The prefix added to the names of tables that are created.
        :param tags: The tags to use with this crawler.
        :param targets: A collection of targets to crawl.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # tags: Any
            
            cfn_crawler_mixin_props = glue_mixins.CfnCrawlerMixinProps(
                classifiers=["classifiers"],
                configuration="configuration",
                crawler_security_configuration="crawlerSecurityConfiguration",
                database_name="databaseName",
                description="description",
                lake_formation_configuration=glue_mixins.CfnCrawlerPropsMixin.LakeFormationConfigurationProperty(
                    account_id="accountId",
                    use_lake_formation_credentials=False
                ),
                name="name",
                recrawl_policy=glue_mixins.CfnCrawlerPropsMixin.RecrawlPolicyProperty(
                    recrawl_behavior="recrawlBehavior"
                ),
                role="role",
                schedule=glue_mixins.CfnCrawlerPropsMixin.ScheduleProperty(
                    schedule_expression="scheduleExpression"
                ),
                schema_change_policy=glue_mixins.CfnCrawlerPropsMixin.SchemaChangePolicyProperty(
                    delete_behavior="deleteBehavior",
                    update_behavior="updateBehavior"
                ),
                table_prefix="tablePrefix",
                tags=tags,
                targets=glue_mixins.CfnCrawlerPropsMixin.TargetsProperty(
                    catalog_targets=[glue_mixins.CfnCrawlerPropsMixin.CatalogTargetProperty(
                        connection_name="connectionName",
                        database_name="databaseName",
                        dlq_event_queue_arn="dlqEventQueueArn",
                        event_queue_arn="eventQueueArn",
                        tables=["tables"]
                    )],
                    delta_targets=[glue_mixins.CfnCrawlerPropsMixin.DeltaTargetProperty(
                        connection_name="connectionName",
                        create_native_delta_table=False,
                        delta_tables=["deltaTables"],
                        write_manifest=False
                    )],
                    dynamo_db_targets=[glue_mixins.CfnCrawlerPropsMixin.DynamoDBTargetProperty(
                        path="path",
                        scan_all=False,
                        scan_rate=123
                    )],
                    hudi_targets=[glue_mixins.CfnCrawlerPropsMixin.HudiTargetProperty(
                        connection_name="connectionName",
                        exclusions=["exclusions"],
                        maximum_traversal_depth=123,
                        paths=["paths"]
                    )],
                    iceberg_targets=[glue_mixins.CfnCrawlerPropsMixin.IcebergTargetProperty(
                        connection_name="connectionName",
                        exclusions=["exclusions"],
                        maximum_traversal_depth=123,
                        paths=["paths"]
                    )],
                    jdbc_targets=[glue_mixins.CfnCrawlerPropsMixin.JdbcTargetProperty(
                        connection_name="connectionName",
                        enable_additional_metadata=["enableAdditionalMetadata"],
                        exclusions=["exclusions"],
                        path="path"
                    )],
                    mongo_db_targets=[glue_mixins.CfnCrawlerPropsMixin.MongoDBTargetProperty(
                        connection_name="connectionName",
                        path="path"
                    )],
                    s3_targets=[glue_mixins.CfnCrawlerPropsMixin.S3TargetProperty(
                        connection_name="connectionName",
                        dlq_event_queue_arn="dlqEventQueueArn",
                        event_queue_arn="eventQueueArn",
                        exclusions=["exclusions"],
                        path="path",
                        sample_size=123
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448d370592f7619ef5f78161c0259f53c78150542d18173cb69ba57f2062d99d)
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument crawler_security_configuration", value=crawler_security_configuration, expected_type=type_hints["crawler_security_configuration"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument lake_formation_configuration", value=lake_formation_configuration, expected_type=type_hints["lake_formation_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recrawl_policy", value=recrawl_policy, expected_type=type_hints["recrawl_policy"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument schema_change_policy", value=schema_change_policy, expected_type=type_hints["schema_change_policy"])
            check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if configuration is not None:
            self._values["configuration"] = configuration
        if crawler_security_configuration is not None:
            self._values["crawler_security_configuration"] = crawler_security_configuration
        if database_name is not None:
            self._values["database_name"] = database_name
        if description is not None:
            self._values["description"] = description
        if lake_formation_configuration is not None:
            self._values["lake_formation_configuration"] = lake_formation_configuration
        if name is not None:
            self._values["name"] = name
        if recrawl_policy is not None:
            self._values["recrawl_policy"] = recrawl_policy
        if role is not None:
            self._values["role"] = role
        if schedule is not None:
            self._values["schedule"] = schedule
        if schema_change_policy is not None:
            self._values["schema_change_policy"] = schema_change_policy
        if table_prefix is not None:
            self._values["table_prefix"] = table_prefix
        if tags is not None:
            self._values["tags"] = tags
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def classifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of UTF-8 strings that specify the names of custom classifiers that are associated with the crawler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-classifiers
        '''
        result = self._values.get("classifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def configuration(self) -> typing.Optional[builtins.str]:
        '''Crawler configuration information.

        This versioned JSON string allows users to specify aspects of a crawler's behavior. For more information, see `Configuring a Crawler <https://docs.aws.amazon.com/glue/latest/dg/crawler-configuration.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def crawler_security_configuration(self) -> typing.Optional[builtins.str]:
        '''The name of the ``SecurityConfiguration`` structure to be used by this crawler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-crawlersecurityconfiguration
        '''
        result = self._values.get("crawler_security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the database in which the crawler's output is stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the crawler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lake_formation_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.LakeFormationConfigurationProperty"]]:
        '''Specifies whether the crawler should use AWS Lake Formation credentials for the crawler instead of the IAM role credentials.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-lakeformationconfiguration
        '''
        result = self._values.get("lake_formation_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.LakeFormationConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the crawler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recrawl_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.RecrawlPolicyProperty"]]:
        '''A policy that specifies whether to crawl the entire dataset again, or to crawl only folders that were added since the last crawler run.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-recrawlpolicy
        '''
        result = self._values.get("recrawl_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.RecrawlPolicyProperty"]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM role that's used to access customer resources, such as Amazon Simple Storage Service (Amazon S3) data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.ScheduleProperty"]]:
        '''For scheduled crawlers, the schedule when the crawler runs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.ScheduleProperty"]], result)

    @builtins.property
    def schema_change_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.SchemaChangePolicyProperty"]]:
        '''The policy that specifies update and delete behaviors for the crawler.

        The policy tells the crawler what to do in the event that it detects a change in a table that already exists in the customer's database at the time of the crawl. The ``SchemaChangePolicy`` does not affect whether or how new tables and partitions are added. New tables and partitions are always created regardless of the ``SchemaChangePolicy`` on a crawler.

        The SchemaChangePolicy consists of two components, ``UpdateBehavior`` and ``DeleteBehavior`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-schemachangepolicy
        '''
        result = self._values.get("schema_change_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.SchemaChangePolicyProperty"]], result)

    @builtins.property
    def table_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix added to the names of tables that are created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-tableprefix
        '''
        result = self._values.get("table_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags to use with this crawler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.TargetsProperty"]]:
        '''A collection of targets to crawl.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.TargetsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCrawlerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCrawlerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin",
):
    '''The ``AWS::Glue::Crawler`` resource specifies an AWS Glue crawler.

    For more information, see `Cataloging Tables with a Crawler <https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html>`_ and `Crawler Structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-crawling.html#aws-glue-api-crawler-crawling-Crawler>`_ in the *AWS Glue Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html
    :cloudformationResource: AWS::Glue::Crawler
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # tags: Any
        
        cfn_crawler_props_mixin = glue_mixins.CfnCrawlerPropsMixin(glue_mixins.CfnCrawlerMixinProps(
            classifiers=["classifiers"],
            configuration="configuration",
            crawler_security_configuration="crawlerSecurityConfiguration",
            database_name="databaseName",
            description="description",
            lake_formation_configuration=glue_mixins.CfnCrawlerPropsMixin.LakeFormationConfigurationProperty(
                account_id="accountId",
                use_lake_formation_credentials=False
            ),
            name="name",
            recrawl_policy=glue_mixins.CfnCrawlerPropsMixin.RecrawlPolicyProperty(
                recrawl_behavior="recrawlBehavior"
            ),
            role="role",
            schedule=glue_mixins.CfnCrawlerPropsMixin.ScheduleProperty(
                schedule_expression="scheduleExpression"
            ),
            schema_change_policy=glue_mixins.CfnCrawlerPropsMixin.SchemaChangePolicyProperty(
                delete_behavior="deleteBehavior",
                update_behavior="updateBehavior"
            ),
            table_prefix="tablePrefix",
            tags=tags,
            targets=glue_mixins.CfnCrawlerPropsMixin.TargetsProperty(
                catalog_targets=[glue_mixins.CfnCrawlerPropsMixin.CatalogTargetProperty(
                    connection_name="connectionName",
                    database_name="databaseName",
                    dlq_event_queue_arn="dlqEventQueueArn",
                    event_queue_arn="eventQueueArn",
                    tables=["tables"]
                )],
                delta_targets=[glue_mixins.CfnCrawlerPropsMixin.DeltaTargetProperty(
                    connection_name="connectionName",
                    create_native_delta_table=False,
                    delta_tables=["deltaTables"],
                    write_manifest=False
                )],
                dynamo_db_targets=[glue_mixins.CfnCrawlerPropsMixin.DynamoDBTargetProperty(
                    path="path",
                    scan_all=False,
                    scan_rate=123
                )],
                hudi_targets=[glue_mixins.CfnCrawlerPropsMixin.HudiTargetProperty(
                    connection_name="connectionName",
                    exclusions=["exclusions"],
                    maximum_traversal_depth=123,
                    paths=["paths"]
                )],
                iceberg_targets=[glue_mixins.CfnCrawlerPropsMixin.IcebergTargetProperty(
                    connection_name="connectionName",
                    exclusions=["exclusions"],
                    maximum_traversal_depth=123,
                    paths=["paths"]
                )],
                jdbc_targets=[glue_mixins.CfnCrawlerPropsMixin.JdbcTargetProperty(
                    connection_name="connectionName",
                    enable_additional_metadata=["enableAdditionalMetadata"],
                    exclusions=["exclusions"],
                    path="path"
                )],
                mongo_db_targets=[glue_mixins.CfnCrawlerPropsMixin.MongoDBTargetProperty(
                    connection_name="connectionName",
                    path="path"
                )],
                s3_targets=[glue_mixins.CfnCrawlerPropsMixin.S3TargetProperty(
                    connection_name="connectionName",
                    dlq_event_queue_arn="dlqEventQueueArn",
                    event_queue_arn="eventQueueArn",
                    exclusions=["exclusions"],
                    path="path",
                    sample_size=123
                )]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCrawlerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Crawler``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8625e58544eaef652f69eae076a4eae917caebcc365c30681d37370a4e85810f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ae14543ac46ed42b54d7f83466b3263048d73ff9fe013d41dd6a325e46a212b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feece70d61e9b64a554f797d30f85378b57cef579f182216f89f2e7c4f5313a4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCrawlerMixinProps:
        return typing.cast(CfnCrawlerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.CatalogTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_name": "connectionName",
            "database_name": "databaseName",
            "dlq_event_queue_arn": "dlqEventQueueArn",
            "event_queue_arn": "eventQueueArn",
            "tables": "tables",
        },
    )
    class CatalogTargetProperty:
        def __init__(
            self,
            *,
            connection_name: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            dlq_event_queue_arn: typing.Optional[builtins.str] = None,
            event_queue_arn: typing.Optional[builtins.str] = None,
            tables: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies an AWS Glue Data Catalog target.

            :param connection_name: The name of the connection for an Amazon S3-backed Data Catalog table to be a target of the crawl when using a ``Catalog`` connection type paired with a ``NETWORK`` Connection type.
            :param database_name: The name of the database to be synchronized.
            :param dlq_event_queue_arn: A valid Amazon dead-letter SQS ARN. For example, ``arn:aws:sqs:region:account:deadLetterQueue`` .
            :param event_queue_arn: A valid Amazon SQS ARN. For example, ``arn:aws:sqs:region:account:sqs`` .
            :param tables: A list of the tables to be synchronized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-catalogtarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                catalog_target_property = glue_mixins.CfnCrawlerPropsMixin.CatalogTargetProperty(
                    connection_name="connectionName",
                    database_name="databaseName",
                    dlq_event_queue_arn="dlqEventQueueArn",
                    event_queue_arn="eventQueueArn",
                    tables=["tables"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__23aa721b924391b8149a3a38798dcc91351364a58331b94cf382140dbaea1e84)
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument dlq_event_queue_arn", value=dlq_event_queue_arn, expected_type=type_hints["dlq_event_queue_arn"])
                check_type(argname="argument event_queue_arn", value=event_queue_arn, expected_type=type_hints["event_queue_arn"])
                check_type(argname="argument tables", value=tables, expected_type=type_hints["tables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if database_name is not None:
                self._values["database_name"] = database_name
            if dlq_event_queue_arn is not None:
                self._values["dlq_event_queue_arn"] = dlq_event_queue_arn
            if event_queue_arn is not None:
                self._values["event_queue_arn"] = event_queue_arn
            if tables is not None:
                self._values["tables"] = tables

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connection for an Amazon S3-backed Data Catalog table to be a target of the crawl when using a ``Catalog`` connection type paired with a ``NETWORK`` Connection type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-catalogtarget.html#cfn-glue-crawler-catalogtarget-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database to be synchronized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-catalogtarget.html#cfn-glue-crawler-catalogtarget-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dlq_event_queue_arn(self) -> typing.Optional[builtins.str]:
            '''A valid Amazon dead-letter SQS ARN.

            For example, ``arn:aws:sqs:region:account:deadLetterQueue`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-catalogtarget.html#cfn-glue-crawler-catalogtarget-dlqeventqueuearn
            '''
            result = self._values.get("dlq_event_queue_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_queue_arn(self) -> typing.Optional[builtins.str]:
            '''A valid Amazon SQS ARN.

            For example, ``arn:aws:sqs:region:account:sqs`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-catalogtarget.html#cfn-glue-crawler-catalogtarget-eventqueuearn
            '''
            result = self._values.get("event_queue_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tables(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of the tables to be synchronized.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-catalogtarget.html#cfn-glue-crawler-catalogtarget-tables
            '''
            result = self._values.get("tables")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CatalogTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.DeltaTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_name": "connectionName",
            "create_native_delta_table": "createNativeDeltaTable",
            "delta_tables": "deltaTables",
            "write_manifest": "writeManifest",
        },
    )
    class DeltaTargetProperty:
        def __init__(
            self,
            *,
            connection_name: typing.Optional[builtins.str] = None,
            create_native_delta_table: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            delta_tables: typing.Optional[typing.Sequence[builtins.str]] = None,
            write_manifest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies a Delta data store to crawl one or more Delta tables.

            :param connection_name: The name of the connection to use to connect to the Delta table target.
            :param create_native_delta_table: Specifies whether the crawler will create native tables, to allow integration with query engines that support querying of the Delta transaction log directly.
            :param delta_tables: A list of the Amazon S3 paths to the Delta tables.
            :param write_manifest: Specifies whether to write the manifest files to the Delta table path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-deltatarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                delta_target_property = glue_mixins.CfnCrawlerPropsMixin.DeltaTargetProperty(
                    connection_name="connectionName",
                    create_native_delta_table=False,
                    delta_tables=["deltaTables"],
                    write_manifest=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1273651a23ff9c22c4cc50d1b14c8d4878eafb799a63ff33a0b5a7bb2f6e6506)
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument create_native_delta_table", value=create_native_delta_table, expected_type=type_hints["create_native_delta_table"])
                check_type(argname="argument delta_tables", value=delta_tables, expected_type=type_hints["delta_tables"])
                check_type(argname="argument write_manifest", value=write_manifest, expected_type=type_hints["write_manifest"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if create_native_delta_table is not None:
                self._values["create_native_delta_table"] = create_native_delta_table
            if delta_tables is not None:
                self._values["delta_tables"] = delta_tables
            if write_manifest is not None:
                self._values["write_manifest"] = write_manifest

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connection to use to connect to the Delta table target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-deltatarget.html#cfn-glue-crawler-deltatarget-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def create_native_delta_table(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the crawler will create native tables, to allow integration with query engines that support querying of the Delta transaction log directly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-deltatarget.html#cfn-glue-crawler-deltatarget-createnativedeltatable
            '''
            result = self._values.get("create_native_delta_table")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def delta_tables(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of the Amazon S3 paths to the Delta tables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-deltatarget.html#cfn-glue-crawler-deltatarget-deltatables
            '''
            result = self._values.get("delta_tables")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def write_manifest(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to write the manifest files to the Delta table path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-deltatarget.html#cfn-glue-crawler-deltatarget-writemanifest
            '''
            result = self._values.get("write_manifest")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeltaTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.DynamoDBTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path", "scan_all": "scanAll", "scan_rate": "scanRate"},
    )
    class DynamoDBTargetProperty:
        def __init__(
            self,
            *,
            path: typing.Optional[builtins.str] = None,
            scan_all: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            scan_rate: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies an Amazon DynamoDB table to crawl.

            :param path: The name of the DynamoDB table to crawl.
            :param scan_all: Indicates whether to scan all the records, or to sample rows from the table. Scanning all the records can take a long time when the table is not a high throughput table. A value of ``true`` means to scan all records, while a value of ``false`` means to sample the records. If no value is specified, the value defaults to ``true`` .
            :param scan_rate: The percentage of the configured read capacity units to use by the AWS Glue crawler. Read capacity units is a term defined by DynamoDB, and is a numeric value that acts as rate limiter for the number of reads that can be performed on that table per second. The valid values are null or a value between 0.1 to 1.5. A null value is used when user does not provide a value, and defaults to 0.5 of the configured Read Capacity Unit (for provisioned tables), or 0.25 of the max configured Read Capacity Unit (for tables using on-demand mode).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-dynamodbtarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                dynamo_dBTarget_property = glue_mixins.CfnCrawlerPropsMixin.DynamoDBTargetProperty(
                    path="path",
                    scan_all=False,
                    scan_rate=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34347133197acba5a57f6cca9197ce1da2446d99a39a2d0b523dd22b17bad14f)
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument scan_all", value=scan_all, expected_type=type_hints["scan_all"])
                check_type(argname="argument scan_rate", value=scan_rate, expected_type=type_hints["scan_rate"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path is not None:
                self._values["path"] = path
            if scan_all is not None:
                self._values["scan_all"] = scan_all
            if scan_rate is not None:
                self._values["scan_rate"] = scan_rate

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The name of the DynamoDB table to crawl.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-dynamodbtarget.html#cfn-glue-crawler-dynamodbtarget-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scan_all(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether to scan all the records, or to sample rows from the table.

            Scanning all the records can take a long time when the table is not a high throughput table.

            A value of ``true`` means to scan all records, while a value of ``false`` means to sample the records. If no value is specified, the value defaults to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-dynamodbtarget.html#cfn-glue-crawler-dynamodbtarget-scanall
            '''
            result = self._values.get("scan_all")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def scan_rate(self) -> typing.Optional[jsii.Number]:
            '''The percentage of the configured read capacity units to use by the AWS Glue crawler.

            Read capacity units is a term defined by DynamoDB, and is a numeric value that acts as rate limiter for the number of reads that can be performed on that table per second.

            The valid values are null or a value between 0.1 to 1.5. A null value is used when user does not provide a value, and defaults to 0.5 of the configured Read Capacity Unit (for provisioned tables), or 0.25 of the max configured Read Capacity Unit (for tables using on-demand mode).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-dynamodbtarget.html#cfn-glue-crawler-dynamodbtarget-scanrate
            '''
            result = self._values.get("scan_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.HudiTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_name": "connectionName",
            "exclusions": "exclusions",
            "maximum_traversal_depth": "maximumTraversalDepth",
            "paths": "paths",
        },
    )
    class HudiTargetProperty:
        def __init__(
            self,
            *,
            connection_name: typing.Optional[builtins.str] = None,
            exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
            maximum_traversal_depth: typing.Optional[jsii.Number] = None,
            paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies an Apache Hudi data source.

            :param connection_name: The name of the connection to use to connect to the Hudi target. If your Hudi files are stored in buckets that require VPC authorization, you can set their connection properties here.
            :param exclusions: A list of glob patterns used to exclude from the crawl. For more information, see `Catalog Tables with a Crawler <https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html>`_ .
            :param maximum_traversal_depth: The maximum depth of Amazon S3 paths that the crawler can traverse to discover the Hudi metadata folder in your Amazon S3 path. Used to limit the crawler run time.
            :param paths: An array of Amazon S3 location strings for Hudi, each indicating the root folder with which the metadata files for a Hudi table resides. The Hudi folder may be located in a child folder of the root folder. The crawler will scan all folders underneath a path for a Hudi folder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-huditarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                hudi_target_property = glue_mixins.CfnCrawlerPropsMixin.HudiTargetProperty(
                    connection_name="connectionName",
                    exclusions=["exclusions"],
                    maximum_traversal_depth=123,
                    paths=["paths"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__567365f194d49b26201f3adb17e3fb8334c1f00b955ffc11fc0a6cbbe7fb2ebf)
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
                check_type(argname="argument maximum_traversal_depth", value=maximum_traversal_depth, expected_type=type_hints["maximum_traversal_depth"])
                check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if exclusions is not None:
                self._values["exclusions"] = exclusions
            if maximum_traversal_depth is not None:
                self._values["maximum_traversal_depth"] = maximum_traversal_depth
            if paths is not None:
                self._values["paths"] = paths

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connection to use to connect to the Hudi target.

            If your Hudi files are stored in buckets that require VPC authorization, you can set their connection properties here.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-huditarget.html#cfn-glue-crawler-huditarget-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of glob patterns used to exclude from the crawl.

            For more information, see `Catalog Tables with a Crawler <https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-huditarget.html#cfn-glue-crawler-huditarget-exclusions
            '''
            result = self._values.get("exclusions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def maximum_traversal_depth(self) -> typing.Optional[jsii.Number]:
            '''The maximum depth of Amazon S3 paths that the crawler can traverse to discover the Hudi metadata folder in your Amazon S3 path.

            Used to limit the crawler run time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-huditarget.html#cfn-glue-crawler-huditarget-maximumtraversaldepth
            '''
            result = self._values.get("maximum_traversal_depth")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def paths(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of Amazon S3 location strings for Hudi, each indicating the root folder with which the metadata files for a Hudi table resides.

            The Hudi folder may be located in a child folder of the root folder.

            The crawler will scan all folders underneath a path for a Hudi folder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-huditarget.html#cfn-glue-crawler-huditarget-paths
            '''
            result = self._values.get("paths")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HudiTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.IcebergTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_name": "connectionName",
            "exclusions": "exclusions",
            "maximum_traversal_depth": "maximumTraversalDepth",
            "paths": "paths",
        },
    )
    class IcebergTargetProperty:
        def __init__(
            self,
            *,
            connection_name: typing.Optional[builtins.str] = None,
            exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
            maximum_traversal_depth: typing.Optional[jsii.Number] = None,
            paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies Apache Iceberg data store targets.

            :param connection_name: The name of the connection to use to connect to the Iceberg target.
            :param exclusions: A list of global patterns used to exclude from the crawl.
            :param maximum_traversal_depth: The maximum depth of Amazon S3 paths that the crawler can traverse to discover the Iceberg metadata folder in your Amazon S3 path. Used to limit the crawler run time.
            :param paths: One or more Amazon S3 paths that contains Iceberg metadata folders as s3://bucket/prefix .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-icebergtarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                iceberg_target_property = glue_mixins.CfnCrawlerPropsMixin.IcebergTargetProperty(
                    connection_name="connectionName",
                    exclusions=["exclusions"],
                    maximum_traversal_depth=123,
                    paths=["paths"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a43620ebad60594d54461e6de3ec43136bbe4c6709765987366ad40bb7117fe)
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
                check_type(argname="argument maximum_traversal_depth", value=maximum_traversal_depth, expected_type=type_hints["maximum_traversal_depth"])
                check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if exclusions is not None:
                self._values["exclusions"] = exclusions
            if maximum_traversal_depth is not None:
                self._values["maximum_traversal_depth"] = maximum_traversal_depth
            if paths is not None:
                self._values["paths"] = paths

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connection to use to connect to the Iceberg target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-icebergtarget.html#cfn-glue-crawler-icebergtarget-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of global patterns used to exclude from the crawl.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-icebergtarget.html#cfn-glue-crawler-icebergtarget-exclusions
            '''
            result = self._values.get("exclusions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def maximum_traversal_depth(self) -> typing.Optional[jsii.Number]:
            '''The maximum depth of Amazon S3 paths that the crawler can traverse to discover the Iceberg metadata folder in your Amazon S3 path.

            Used to limit the crawler run time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-icebergtarget.html#cfn-glue-crawler-icebergtarget-maximumtraversaldepth
            '''
            result = self._values.get("maximum_traversal_depth")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def paths(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more Amazon S3 paths that contains Iceberg metadata folders as s3://bucket/prefix .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-icebergtarget.html#cfn-glue-crawler-icebergtarget-paths
            '''
            result = self._values.get("paths")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IcebergTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.JdbcTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_name": "connectionName",
            "enable_additional_metadata": "enableAdditionalMetadata",
            "exclusions": "exclusions",
            "path": "path",
        },
    )
    class JdbcTargetProperty:
        def __init__(
            self,
            *,
            connection_name: typing.Optional[builtins.str] = None,
            enable_additional_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
            exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a JDBC data store to crawl.

            :param connection_name: The name of the connection to use to connect to the JDBC target.
            :param enable_additional_metadata: Specify a value of ``RAWTYPES`` or ``COMMENTS`` to enable additional metadata in table responses. ``RAWTYPES`` provides the native-level datatype. ``COMMENTS`` provides comments associated with a column or table in the database. If you do not need additional metadata, keep the field empty.
            :param exclusions: A list of glob patterns used to exclude from the crawl. For more information, see `Catalog Tables with a Crawler <https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html>`_ .
            :param path: The path of the JDBC target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                jdbc_target_property = glue_mixins.CfnCrawlerPropsMixin.JdbcTargetProperty(
                    connection_name="connectionName",
                    enable_additional_metadata=["enableAdditionalMetadata"],
                    exclusions=["exclusions"],
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__25a9e73c947bd26eb31da631d6d5266721944a314f279061c5f7c8ce9d781ae9)
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument enable_additional_metadata", value=enable_additional_metadata, expected_type=type_hints["enable_additional_metadata"])
                check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if enable_additional_metadata is not None:
                self._values["enable_additional_metadata"] = enable_additional_metadata
            if exclusions is not None:
                self._values["exclusions"] = exclusions
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connection to use to connect to the JDBC target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html#cfn-glue-crawler-jdbctarget-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_additional_metadata(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify a value of ``RAWTYPES`` or ``COMMENTS`` to enable additional metadata in table responses.

            ``RAWTYPES`` provides the native-level datatype. ``COMMENTS`` provides comments associated with a column or table in the database.

            If you do not need additional metadata, keep the field empty.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html#cfn-glue-crawler-jdbctarget-enableadditionalmetadata
            '''
            result = self._values.get("enable_additional_metadata")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of glob patterns used to exclude from the crawl.

            For more information, see `Catalog Tables with a Crawler <https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html#cfn-glue-crawler-jdbctarget-exclusions
            '''
            result = self._values.get("exclusions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The path of the JDBC target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html#cfn-glue-crawler-jdbctarget-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JdbcTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.LakeFormationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "use_lake_formation_credentials": "useLakeFormationCredentials",
        },
    )
    class LakeFormationConfigurationProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            use_lake_formation_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies AWS Lake Formation configuration settings for the crawler.

            :param account_id: Required for cross account crawls. For same account crawls as the target data, this can be left as null.
            :param use_lake_formation_credentials: Specifies whether to use AWS Lake Formation credentials for the crawler instead of the IAM role credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-lakeformationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                lake_formation_configuration_property = glue_mixins.CfnCrawlerPropsMixin.LakeFormationConfigurationProperty(
                    account_id="accountId",
                    use_lake_formation_credentials=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d238624614c74bfe82e4e12acbc4a3be08e746959f96b0018eac44f9994a5171)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument use_lake_formation_credentials", value=use_lake_formation_credentials, expected_type=type_hints["use_lake_formation_credentials"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if use_lake_formation_credentials is not None:
                self._values["use_lake_formation_credentials"] = use_lake_formation_credentials

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''Required for cross account crawls.

            For same account crawls as the target data, this can be left as null.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-lakeformationconfiguration.html#cfn-glue-crawler-lakeformationconfiguration-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_lake_formation_credentials(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to use AWS Lake Formation credentials for the crawler instead of the IAM role credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-lakeformationconfiguration.html#cfn-glue-crawler-lakeformationconfiguration-uselakeformationcredentials
            '''
            result = self._values.get("use_lake_formation_credentials")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LakeFormationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.MongoDBTargetProperty",
        jsii_struct_bases=[],
        name_mapping={"connection_name": "connectionName", "path": "path"},
    )
    class MongoDBTargetProperty:
        def __init__(
            self,
            *,
            connection_name: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an Amazon DocumentDB or MongoDB data store to crawl.

            :param connection_name: The name of the connection to use to connect to the Amazon DocumentDB or MongoDB target.
            :param path: The path of the Amazon DocumentDB or MongoDB target (database/collection).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-mongodbtarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                mongo_dBTarget_property = glue_mixins.CfnCrawlerPropsMixin.MongoDBTargetProperty(
                    connection_name="connectionName",
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e89e0d127505044ef6e6ffb6b0b8de994387047a80720e3b0e2b9074cddc232)
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connection to use to connect to the Amazon DocumentDB or MongoDB target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-mongodbtarget.html#cfn-glue-crawler-mongodbtarget-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The path of the Amazon DocumentDB or MongoDB target (database/collection).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-mongodbtarget.html#cfn-glue-crawler-mongodbtarget-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MongoDBTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.RecrawlPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"recrawl_behavior": "recrawlBehavior"},
    )
    class RecrawlPolicyProperty:
        def __init__(
            self,
            *,
            recrawl_behavior: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When crawling an Amazon S3 data source after the first crawl is complete, specifies whether to crawl the entire dataset again or to crawl only folders that were added since the last crawler run.

            For more information, see `Incremental Crawls in AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/incremental-crawls.html>`_ in the developer guide.

            :param recrawl_behavior: Specifies whether to crawl the entire dataset again or to crawl only folders that were added since the last crawler run. A value of ``CRAWL_EVERYTHING`` specifies crawling the entire dataset again. A value of ``CRAWL_NEW_FOLDERS_ONLY`` specifies crawling only folders that were added since the last crawler run. A value of ``CRAWL_EVENT_MODE`` specifies crawling only the changes identified by Amazon S3 events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-recrawlpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                recrawl_policy_property = glue_mixins.CfnCrawlerPropsMixin.RecrawlPolicyProperty(
                    recrawl_behavior="recrawlBehavior"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ede704b334486490ccaa29cf2c1eaab39f6937672aa470a71da0c464724a4f8)
                check_type(argname="argument recrawl_behavior", value=recrawl_behavior, expected_type=type_hints["recrawl_behavior"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if recrawl_behavior is not None:
                self._values["recrawl_behavior"] = recrawl_behavior

        @builtins.property
        def recrawl_behavior(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to crawl the entire dataset again or to crawl only folders that were added since the last crawler run.

            A value of ``CRAWL_EVERYTHING`` specifies crawling the entire dataset again.

            A value of ``CRAWL_NEW_FOLDERS_ONLY`` specifies crawling only folders that were added since the last crawler run.

            A value of ``CRAWL_EVENT_MODE`` specifies crawling only the changes identified by Amazon S3 events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-recrawlpolicy.html#cfn-glue-crawler-recrawlpolicy-recrawlbehavior
            '''
            result = self._values.get("recrawl_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecrawlPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.S3TargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_name": "connectionName",
            "dlq_event_queue_arn": "dlqEventQueueArn",
            "event_queue_arn": "eventQueueArn",
            "exclusions": "exclusions",
            "path": "path",
            "sample_size": "sampleSize",
        },
    )
    class S3TargetProperty:
        def __init__(
            self,
            *,
            connection_name: typing.Optional[builtins.str] = None,
            dlq_event_queue_arn: typing.Optional[builtins.str] = None,
            event_queue_arn: typing.Optional[builtins.str] = None,
            exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
            path: typing.Optional[builtins.str] = None,
            sample_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies a data store in Amazon Simple Storage Service (Amazon S3).

            :param connection_name: The name of a connection which allows a job or crawler to access data in Amazon S3 within an Amazon Virtual Private Cloud environment (Amazon VPC).
            :param dlq_event_queue_arn: A valid Amazon dead-letter SQS ARN. For example, ``arn:aws:sqs:region:account:deadLetterQueue`` .
            :param event_queue_arn: A valid Amazon SQS ARN. For example, ``arn:aws:sqs:region:account:sqs`` .
            :param exclusions: A list of glob patterns used to exclude from the crawl. For more information, see `Catalog Tables with a Crawler <https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html>`_ .
            :param path: The path to the Amazon S3 target.
            :param sample_size: Sets the number of files in each leaf folder to be crawled when crawling sample files in a dataset. If not set, all the files are crawled. A valid value is an integer between 1 and 249.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                s3_target_property = glue_mixins.CfnCrawlerPropsMixin.S3TargetProperty(
                    connection_name="connectionName",
                    dlq_event_queue_arn="dlqEventQueueArn",
                    event_queue_arn="eventQueueArn",
                    exclusions=["exclusions"],
                    path="path",
                    sample_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f165693d46afb0382c356502c9343ea7e32798e28ad89b6353b67711b7010d0)
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument dlq_event_queue_arn", value=dlq_event_queue_arn, expected_type=type_hints["dlq_event_queue_arn"])
                check_type(argname="argument event_queue_arn", value=event_queue_arn, expected_type=type_hints["event_queue_arn"])
                check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument sample_size", value=sample_size, expected_type=type_hints["sample_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if dlq_event_queue_arn is not None:
                self._values["dlq_event_queue_arn"] = dlq_event_queue_arn
            if event_queue_arn is not None:
                self._values["event_queue_arn"] = event_queue_arn
            if exclusions is not None:
                self._values["exclusions"] = exclusions
            if path is not None:
                self._values["path"] = path
            if sample_size is not None:
                self._values["sample_size"] = sample_size

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of a connection which allows a job or crawler to access data in Amazon S3 within an Amazon Virtual Private Cloud environment (Amazon VPC).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html#cfn-glue-crawler-s3target-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dlq_event_queue_arn(self) -> typing.Optional[builtins.str]:
            '''A valid Amazon dead-letter SQS ARN.

            For example, ``arn:aws:sqs:region:account:deadLetterQueue`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html#cfn-glue-crawler-s3target-dlqeventqueuearn
            '''
            result = self._values.get("dlq_event_queue_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_queue_arn(self) -> typing.Optional[builtins.str]:
            '''A valid Amazon SQS ARN.

            For example, ``arn:aws:sqs:region:account:sqs`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html#cfn-glue-crawler-s3target-eventqueuearn
            '''
            result = self._values.get("event_queue_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of glob patterns used to exclude from the crawl.

            For more information, see `Catalog Tables with a Crawler <https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html#cfn-glue-crawler-s3target-exclusions
            '''
            result = self._values.get("exclusions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The path to the Amazon S3 target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html#cfn-glue-crawler-s3target-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sample_size(self) -> typing.Optional[jsii.Number]:
            '''Sets the number of files in each leaf folder to be crawled when crawling sample files in a dataset.

            If not set, all the files are crawled. A valid value is an integer between 1 and 249.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html#cfn-glue-crawler-s3target-samplesize
            '''
            result = self._values.get("sample_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule_expression": "scheduleExpression"},
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            schedule_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A scheduling object using a ``cron`` statement to schedule an event.

            :param schedule_expression: A ``cron`` expression used to specify the schedule. For more information, see `Time-Based Schedules for Jobs and Crawlers <https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html>`_ . For example, to run something every day at 12:15 UTC, specify ``cron(15 12 * * ? *)`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                schedule_property = glue_mixins.CfnCrawlerPropsMixin.ScheduleProperty(
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e85952df4a34ea31b08840c78310651818299724eecbc65f5a0becbb238f008b)
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''A ``cron`` expression used to specify the schedule.

            For more information, see `Time-Based Schedules for Jobs and Crawlers <https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html>`_ . For example, to run something every day at 12:15 UTC, specify ``cron(15 12 * * ? *)`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schedule.html#cfn-glue-crawler-schedule-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.SchemaChangePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_behavior": "deleteBehavior",
            "update_behavior": "updateBehavior",
        },
    )
    class SchemaChangePolicyProperty:
        def __init__(
            self,
            *,
            delete_behavior: typing.Optional[builtins.str] = None,
            update_behavior: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The policy that specifies update and delete behaviors for the crawler.

            The policy tells the crawler what to do in the event that it detects a change in a table that already exists in the customer's database at the time of the crawl. The ``SchemaChangePolicy`` does not affect whether or how new tables and partitions are added. New tables and partitions are always created regardless of the ``SchemaChangePolicy`` on a crawler.

            The SchemaChangePolicy consists of two components, ``UpdateBehavior`` and ``DeleteBehavior`` .

            :param delete_behavior: The deletion behavior when the crawler finds a deleted object. A value of ``LOG`` specifies that if a table or partition is found to no longer exist, do not delete it, only log that it was found to no longer exist. A value of ``DELETE_FROM_DATABASE`` specifies that if a table or partition is found to have been removed, delete it from the database. A value of ``DEPRECATE_IN_DATABASE`` specifies that if a table has been found to no longer exist, to add a property to the table that says "DEPRECATED" and includes a timestamp with the time of deprecation.
            :param update_behavior: The update behavior when the crawler finds a changed schema. A value of ``LOG`` specifies that if a table or a partition already exists, and a change is detected, do not update it, only log that a change was detected. Add new tables and new partitions (including on existing tables). A value of ``UPDATE_IN_DATABASE`` specifies that if a table or partition already exists, and a change is detected, update it. Add new tables and partitions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schemachangepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                schema_change_policy_property = glue_mixins.CfnCrawlerPropsMixin.SchemaChangePolicyProperty(
                    delete_behavior="deleteBehavior",
                    update_behavior="updateBehavior"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6bda1bdf56669a4fbed18b0784d5e52d97182c4533eb5f3bf2a8f53e52658340)
                check_type(argname="argument delete_behavior", value=delete_behavior, expected_type=type_hints["delete_behavior"])
                check_type(argname="argument update_behavior", value=update_behavior, expected_type=type_hints["update_behavior"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_behavior is not None:
                self._values["delete_behavior"] = delete_behavior
            if update_behavior is not None:
                self._values["update_behavior"] = update_behavior

        @builtins.property
        def delete_behavior(self) -> typing.Optional[builtins.str]:
            '''The deletion behavior when the crawler finds a deleted object.

            A value of ``LOG`` specifies that if a table or partition is found to no longer exist, do not delete it, only log that it was found to no longer exist.

            A value of ``DELETE_FROM_DATABASE`` specifies that if a table or partition is found to have been removed, delete it from the database.

            A value of ``DEPRECATE_IN_DATABASE`` specifies that if a table has been found to no longer exist, to add a property to the table that says "DEPRECATED" and includes a timestamp with the time of deprecation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schemachangepolicy.html#cfn-glue-crawler-schemachangepolicy-deletebehavior
            '''
            result = self._values.get("delete_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def update_behavior(self) -> typing.Optional[builtins.str]:
            '''The update behavior when the crawler finds a changed schema.

            A value of ``LOG`` specifies that if a table or a partition already exists, and a change is detected, do not update it, only log that a change was detected. Add new tables and new partitions (including on existing tables).

            A value of ``UPDATE_IN_DATABASE`` specifies that if a table or partition already exists, and a change is detected, update it. Add new tables and partitions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schemachangepolicy.html#cfn-glue-crawler-schemachangepolicy-updatebehavior
            '''
            result = self._values.get("update_behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaChangePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCrawlerPropsMixin.TargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_targets": "catalogTargets",
            "delta_targets": "deltaTargets",
            "dynamo_db_targets": "dynamoDbTargets",
            "hudi_targets": "hudiTargets",
            "iceberg_targets": "icebergTargets",
            "jdbc_targets": "jdbcTargets",
            "mongo_db_targets": "mongoDbTargets",
            "s3_targets": "s3Targets",
        },
    )
    class TargetsProperty:
        def __init__(
            self,
            *,
            catalog_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.CatalogTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            delta_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.DeltaTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            dynamo_db_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.DynamoDBTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            hudi_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.HudiTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            iceberg_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.IcebergTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            jdbc_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.JdbcTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            mongo_db_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.MongoDBTargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            s3_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCrawlerPropsMixin.S3TargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies data stores to crawl.

            :param catalog_targets: Specifies AWS Glue Data Catalog targets.
            :param delta_targets: Specifies an array of Delta data store targets.
            :param dynamo_db_targets: Specifies Amazon DynamoDB targets.
            :param hudi_targets: Specifies Apache Hudi data store targets.
            :param iceberg_targets: Specifies Apache Iceberg data store targets.
            :param jdbc_targets: Specifies JDBC targets.
            :param mongo_db_targets: A list of Mongo DB targets.
            :param s3_targets: Specifies Amazon Simple Storage Service (Amazon S3) targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                targets_property = glue_mixins.CfnCrawlerPropsMixin.TargetsProperty(
                    catalog_targets=[glue_mixins.CfnCrawlerPropsMixin.CatalogTargetProperty(
                        connection_name="connectionName",
                        database_name="databaseName",
                        dlq_event_queue_arn="dlqEventQueueArn",
                        event_queue_arn="eventQueueArn",
                        tables=["tables"]
                    )],
                    delta_targets=[glue_mixins.CfnCrawlerPropsMixin.DeltaTargetProperty(
                        connection_name="connectionName",
                        create_native_delta_table=False,
                        delta_tables=["deltaTables"],
                        write_manifest=False
                    )],
                    dynamo_db_targets=[glue_mixins.CfnCrawlerPropsMixin.DynamoDBTargetProperty(
                        path="path",
                        scan_all=False,
                        scan_rate=123
                    )],
                    hudi_targets=[glue_mixins.CfnCrawlerPropsMixin.HudiTargetProperty(
                        connection_name="connectionName",
                        exclusions=["exclusions"],
                        maximum_traversal_depth=123,
                        paths=["paths"]
                    )],
                    iceberg_targets=[glue_mixins.CfnCrawlerPropsMixin.IcebergTargetProperty(
                        connection_name="connectionName",
                        exclusions=["exclusions"],
                        maximum_traversal_depth=123,
                        paths=["paths"]
                    )],
                    jdbc_targets=[glue_mixins.CfnCrawlerPropsMixin.JdbcTargetProperty(
                        connection_name="connectionName",
                        enable_additional_metadata=["enableAdditionalMetadata"],
                        exclusions=["exclusions"],
                        path="path"
                    )],
                    mongo_db_targets=[glue_mixins.CfnCrawlerPropsMixin.MongoDBTargetProperty(
                        connection_name="connectionName",
                        path="path"
                    )],
                    s3_targets=[glue_mixins.CfnCrawlerPropsMixin.S3TargetProperty(
                        connection_name="connectionName",
                        dlq_event_queue_arn="dlqEventQueueArn",
                        event_queue_arn="eventQueueArn",
                        exclusions=["exclusions"],
                        path="path",
                        sample_size=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__063dade8b3fbfcb47287210bd3f0e92c95b6b032d37e7c57350ef3d8e5336f24)
                check_type(argname="argument catalog_targets", value=catalog_targets, expected_type=type_hints["catalog_targets"])
                check_type(argname="argument delta_targets", value=delta_targets, expected_type=type_hints["delta_targets"])
                check_type(argname="argument dynamo_db_targets", value=dynamo_db_targets, expected_type=type_hints["dynamo_db_targets"])
                check_type(argname="argument hudi_targets", value=hudi_targets, expected_type=type_hints["hudi_targets"])
                check_type(argname="argument iceberg_targets", value=iceberg_targets, expected_type=type_hints["iceberg_targets"])
                check_type(argname="argument jdbc_targets", value=jdbc_targets, expected_type=type_hints["jdbc_targets"])
                check_type(argname="argument mongo_db_targets", value=mongo_db_targets, expected_type=type_hints["mongo_db_targets"])
                check_type(argname="argument s3_targets", value=s3_targets, expected_type=type_hints["s3_targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_targets is not None:
                self._values["catalog_targets"] = catalog_targets
            if delta_targets is not None:
                self._values["delta_targets"] = delta_targets
            if dynamo_db_targets is not None:
                self._values["dynamo_db_targets"] = dynamo_db_targets
            if hudi_targets is not None:
                self._values["hudi_targets"] = hudi_targets
            if iceberg_targets is not None:
                self._values["iceberg_targets"] = iceberg_targets
            if jdbc_targets is not None:
                self._values["jdbc_targets"] = jdbc_targets
            if mongo_db_targets is not None:
                self._values["mongo_db_targets"] = mongo_db_targets
            if s3_targets is not None:
                self._values["s3_targets"] = s3_targets

        @builtins.property
        def catalog_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.CatalogTargetProperty"]]]]:
            '''Specifies AWS Glue Data Catalog targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-catalogtargets
            '''
            result = self._values.get("catalog_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.CatalogTargetProperty"]]]], result)

        @builtins.property
        def delta_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.DeltaTargetProperty"]]]]:
            '''Specifies an array of Delta data store targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-deltatargets
            '''
            result = self._values.get("delta_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.DeltaTargetProperty"]]]], result)

        @builtins.property
        def dynamo_db_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.DynamoDBTargetProperty"]]]]:
            '''Specifies Amazon DynamoDB targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-dynamodbtargets
            '''
            result = self._values.get("dynamo_db_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.DynamoDBTargetProperty"]]]], result)

        @builtins.property
        def hudi_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.HudiTargetProperty"]]]]:
            '''Specifies Apache Hudi data store targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-huditargets
            '''
            result = self._values.get("hudi_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.HudiTargetProperty"]]]], result)

        @builtins.property
        def iceberg_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.IcebergTargetProperty"]]]]:
            '''Specifies Apache Iceberg data store targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-icebergtargets
            '''
            result = self._values.get("iceberg_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.IcebergTargetProperty"]]]], result)

        @builtins.property
        def jdbc_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.JdbcTargetProperty"]]]]:
            '''Specifies JDBC targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-jdbctargets
            '''
            result = self._values.get("jdbc_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.JdbcTargetProperty"]]]], result)

        @builtins.property
        def mongo_db_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.MongoDBTargetProperty"]]]]:
            '''A list of Mongo DB targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-mongodbtargets
            '''
            result = self._values.get("mongo_db_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.MongoDBTargetProperty"]]]], result)

        @builtins.property
        def s3_targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.S3TargetProperty"]]]]:
            '''Specifies Amazon Simple Storage Service (Amazon S3) targets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-s3targets
            '''
            result = self._values.get("s3_targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCrawlerPropsMixin.S3TargetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCustomEntityTypeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "context_words": "contextWords",
        "name": "name",
        "regex_string": "regexString",
        "tags": "tags",
    },
)
class CfnCustomEntityTypeMixinProps:
    def __init__(
        self,
        *,
        context_words: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        regex_string: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnCustomEntityTypePropsMixin.

        :param context_words: A list of context words. If none of these context words are found within the vicinity of the regular expression the data will not be detected as sensitive data. If no context words are passed only a regular expression is checked.
        :param name: A name for the custom pattern that allows it to be retrieved or deleted later. This name must be unique per AWS account.
        :param regex_string: A regular expression string that is used for detecting sensitive data in a custom pattern.
        :param tags: AWS tags that contain a key value pair and may be searched by console, command line, or API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-customentitytype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # tags: Any
            
            cfn_custom_entity_type_mixin_props = glue_mixins.CfnCustomEntityTypeMixinProps(
                context_words=["contextWords"],
                name="name",
                regex_string="regexString",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c78b98a1774cb414c8653d07bf19f5b02ee7cdedd254b34b03d63234e62466)
            check_type(argname="argument context_words", value=context_words, expected_type=type_hints["context_words"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument regex_string", value=regex_string, expected_type=type_hints["regex_string"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if context_words is not None:
            self._values["context_words"] = context_words
        if name is not None:
            self._values["name"] = name
        if regex_string is not None:
            self._values["regex_string"] = regex_string
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def context_words(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of context words.

        If none of these context words are found within the vicinity of the regular expression the data will not be detected as sensitive data.

        If no context words are passed only a regular expression is checked.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-customentitytype.html#cfn-glue-customentitytype-contextwords
        '''
        result = self._values.get("context_words")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the custom pattern that allows it to be retrieved or deleted later.

        This name must be unique per AWS account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-customentitytype.html#cfn-glue-customentitytype-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex_string(self) -> typing.Optional[builtins.str]:
        '''A regular expression string that is used for detecting sensitive data in a custom pattern.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-customentitytype.html#cfn-glue-customentitytype-regexstring
        '''
        result = self._values.get("regex_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''AWS tags that contain a key value pair and may be searched by console, command line, or API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-customentitytype.html#cfn-glue-customentitytype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomEntityTypeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCustomEntityTypePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnCustomEntityTypePropsMixin",
):
    '''Creates a custom pattern that is used to detect sensitive data across the columns and rows of your structured data.

    Each custom pattern you create specifies a regular expression and an optional list of context words. If no context words are passed only a regular expression is checked.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-customentitytype.html
    :cloudformationResource: AWS::Glue::CustomEntityType
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # tags: Any
        
        cfn_custom_entity_type_props_mixin = glue_mixins.CfnCustomEntityTypePropsMixin(glue_mixins.CfnCustomEntityTypeMixinProps(
            context_words=["contextWords"],
            name="name",
            regex_string="regexString",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCustomEntityTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::CustomEntityType``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c9bf4508ce96bae654a64c71dd569f16322fa7f530934aaade20bc6ed2a525)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8da4879c694f2b429ab97c747d2f6d5c1bbd491946bf3c9a9efa71839fa326cc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42dc74282a0013d16932c88992ee3a68b14aaae041cc3577afdc4c3339eab9e1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCustomEntityTypeMixinProps:
        return typing.cast(CfnCustomEntityTypeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDataCatalogEncryptionSettingsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "catalog_id": "catalogId",
        "data_catalog_encryption_settings": "dataCatalogEncryptionSettings",
    },
)
class CfnDataCatalogEncryptionSettingsMixinProps:
    def __init__(
        self,
        *,
        catalog_id: typing.Optional[builtins.str] = None,
        data_catalog_encryption_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataCatalogEncryptionSettingsPropsMixin.DataCatalogEncryptionSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataCatalogEncryptionSettingsPropsMixin.

        :param catalog_id: The ID of the Data Catalog in which the settings are created.
        :param data_catalog_encryption_settings: Contains configuration information for maintaining Data Catalog security.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_data_catalog_encryption_settings_mixin_props = glue_mixins.CfnDataCatalogEncryptionSettingsMixinProps(
                catalog_id="catalogId",
                data_catalog_encryption_settings=glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.DataCatalogEncryptionSettingsProperty(
                    connection_password_encryption=glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.ConnectionPasswordEncryptionProperty(
                        kms_key_id="kmsKeyId",
                        return_connection_password_encrypted=False
                    ),
                    encryption_at_rest=glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.EncryptionAtRestProperty(
                        catalog_encryption_mode="catalogEncryptionMode",
                        catalog_encryption_service_role="catalogEncryptionServiceRole",
                        sse_aws_kms_key_id="sseAwsKmsKeyId"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da04c9ec316d2ba43e39316dc4881972588b007e0d2908187e79f503a2c19d4)
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument data_catalog_encryption_settings", value=data_catalog_encryption_settings, expected_type=type_hints["data_catalog_encryption_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id
        if data_catalog_encryption_settings is not None:
            self._values["data_catalog_encryption_settings"] = data_catalog_encryption_settings

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Data Catalog in which the settings are created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-catalogid
        '''
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_catalog_encryption_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCatalogEncryptionSettingsPropsMixin.DataCatalogEncryptionSettingsProperty"]]:
        '''Contains configuration information for maintaining Data Catalog security.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-datacatalogencryptionsettings
        '''
        result = self._values.get("data_catalog_encryption_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCatalogEncryptionSettingsPropsMixin.DataCatalogEncryptionSettingsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataCatalogEncryptionSettingsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataCatalogEncryptionSettingsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDataCatalogEncryptionSettingsPropsMixin",
):
    '''Sets the security configuration for a specified catalog.

    After the configuration has been set, the specified encryption is applied to every catalog write thereafter.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html
    :cloudformationResource: AWS::Glue::DataCatalogEncryptionSettings
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_data_catalog_encryption_settings_props_mixin = glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin(glue_mixins.CfnDataCatalogEncryptionSettingsMixinProps(
            catalog_id="catalogId",
            data_catalog_encryption_settings=glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.DataCatalogEncryptionSettingsProperty(
                connection_password_encryption=glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.ConnectionPasswordEncryptionProperty(
                    kms_key_id="kmsKeyId",
                    return_connection_password_encrypted=False
                ),
                encryption_at_rest=glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.EncryptionAtRestProperty(
                    catalog_encryption_mode="catalogEncryptionMode",
                    catalog_encryption_service_role="catalogEncryptionServiceRole",
                    sse_aws_kms_key_id="sseAwsKmsKeyId"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDataCatalogEncryptionSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::DataCatalogEncryptionSettings``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ef7a850fcd5a86e3830ed0876616cc1de8d13108a47a364ffa68722ea474fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d74a78455df3b59fdac8800e83d0ca6ddeee8c46d7ec2a77086f7f5b4d8b2b2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ebeccb9bf287ea144029039ab9dcd5b072ea7051af36536e7c2e78cc187781)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataCatalogEncryptionSettingsMixinProps:
        return typing.cast(CfnDataCatalogEncryptionSettingsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDataCatalogEncryptionSettingsPropsMixin.ConnectionPasswordEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_id": "kmsKeyId",
            "return_connection_password_encrypted": "returnConnectionPasswordEncrypted",
        },
    )
    class ConnectionPasswordEncryptionProperty:
        def __init__(
            self,
            *,
            kms_key_id: typing.Optional[builtins.str] = None,
            return_connection_password_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The data structure used by the Data Catalog to encrypt the password as part of ``CreateConnection`` or ``UpdateConnection`` and store it in the ``ENCRYPTED_PASSWORD`` field in the connection properties.

            You can enable catalog encryption or only password encryption.

            When a ``CreationConnection`` request arrives containing a password, the Data Catalog first encrypts the password using your AWS  key. It then encrypts the whole connection object again if catalog encryption is also enabled.

            This encryption requires that you set AWS  key permissions to enable or restrict access on the password key according to your security requirements. For example, you might want only administrators to have decrypt permission on the password key.

            :param kms_key_id: An AWS key that is used to encrypt the connection password. If connection password protection is enabled, the caller of ``CreateConnection`` and ``UpdateConnection`` needs at least ``kms:Encrypt`` permission on the specified AWS key, to encrypt passwords before storing them in the Data Catalog. You can set the decrypt permission to enable or restrict access on the password key according to your security requirements.
            :param return_connection_password_encrypted: When the ``ReturnConnectionPasswordEncrypted`` flag is set to "true", passwords remain encrypted in the responses of ``GetConnection`` and ``GetConnections`` . This encryption takes effect independently from catalog encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-connectionpasswordencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                connection_password_encryption_property = glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.ConnectionPasswordEncryptionProperty(
                    kms_key_id="kmsKeyId",
                    return_connection_password_encrypted=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d51b05e943a3d82b76f2ff6795620df7105a4836e580cbaa43ebd33b5c78a601)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument return_connection_password_encrypted", value=return_connection_password_encrypted, expected_type=type_hints["return_connection_password_encrypted"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if return_connection_password_encrypted is not None:
                self._values["return_connection_password_encrypted"] = return_connection_password_encrypted

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''An AWS  key that is used to encrypt the connection password.

            If connection password protection is enabled, the caller of ``CreateConnection`` and ``UpdateConnection`` needs at least ``kms:Encrypt`` permission on the specified AWS  key, to encrypt passwords before storing them in the Data Catalog. You can set the decrypt permission to enable or restrict access on the password key according to your security requirements.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-connectionpasswordencryption.html#cfn-glue-datacatalogencryptionsettings-connectionpasswordencryption-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def return_connection_password_encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When the ``ReturnConnectionPasswordEncrypted`` flag is set to "true", passwords remain encrypted in the responses of ``GetConnection`` and ``GetConnections`` .

            This encryption takes effect independently from catalog encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-connectionpasswordencryption.html#cfn-glue-datacatalogencryptionsettings-connectionpasswordencryption-returnconnectionpasswordencrypted
            '''
            result = self._values.get("return_connection_password_encrypted")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionPasswordEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDataCatalogEncryptionSettingsPropsMixin.DataCatalogEncryptionSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_password_encryption": "connectionPasswordEncryption",
            "encryption_at_rest": "encryptionAtRest",
        },
    )
    class DataCatalogEncryptionSettingsProperty:
        def __init__(
            self,
            *,
            connection_password_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataCatalogEncryptionSettingsPropsMixin.ConnectionPasswordEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_at_rest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataCatalogEncryptionSettingsPropsMixin.EncryptionAtRestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains configuration information for maintaining Data Catalog security.

            :param connection_password_encryption: When connection password protection is enabled, the Data Catalog uses a customer-provided key to encrypt the password as part of ``CreateConnection`` or ``UpdateConnection`` and store it in the ``ENCRYPTED_PASSWORD`` field in the connection properties. You can enable catalog encryption or only password encryption.
            :param encryption_at_rest: Specifies the encryption-at-rest configuration for the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-datacatalogencryptionsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                data_catalog_encryption_settings_property = glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.DataCatalogEncryptionSettingsProperty(
                    connection_password_encryption=glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.ConnectionPasswordEncryptionProperty(
                        kms_key_id="kmsKeyId",
                        return_connection_password_encrypted=False
                    ),
                    encryption_at_rest=glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.EncryptionAtRestProperty(
                        catalog_encryption_mode="catalogEncryptionMode",
                        catalog_encryption_service_role="catalogEncryptionServiceRole",
                        sse_aws_kms_key_id="sseAwsKmsKeyId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89c998d297b0cab8c042cfa770703deaff0bfeb74595d03e5ffd516a8a5262b9)
                check_type(argname="argument connection_password_encryption", value=connection_password_encryption, expected_type=type_hints["connection_password_encryption"])
                check_type(argname="argument encryption_at_rest", value=encryption_at_rest, expected_type=type_hints["encryption_at_rest"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_password_encryption is not None:
                self._values["connection_password_encryption"] = connection_password_encryption
            if encryption_at_rest is not None:
                self._values["encryption_at_rest"] = encryption_at_rest

        @builtins.property
        def connection_password_encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCatalogEncryptionSettingsPropsMixin.ConnectionPasswordEncryptionProperty"]]:
            '''When connection password protection is enabled, the Data Catalog uses a customer-provided key to encrypt the password as part of ``CreateConnection`` or ``UpdateConnection`` and store it in the ``ENCRYPTED_PASSWORD`` field in the connection properties.

            You can enable catalog encryption or only password encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-datacatalogencryptionsettings-connectionpasswordencryption
            '''
            result = self._values.get("connection_password_encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCatalogEncryptionSettingsPropsMixin.ConnectionPasswordEncryptionProperty"]], result)

        @builtins.property
        def encryption_at_rest(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCatalogEncryptionSettingsPropsMixin.EncryptionAtRestProperty"]]:
            '''Specifies the encryption-at-rest configuration for the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-datacatalogencryptionsettings-encryptionatrest
            '''
            result = self._values.get("encryption_at_rest")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCatalogEncryptionSettingsPropsMixin.EncryptionAtRestProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataCatalogEncryptionSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDataCatalogEncryptionSettingsPropsMixin.EncryptionAtRestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_encryption_mode": "catalogEncryptionMode",
            "catalog_encryption_service_role": "catalogEncryptionServiceRole",
            "sse_aws_kms_key_id": "sseAwsKmsKeyId",
        },
    )
    class EncryptionAtRestProperty:
        def __init__(
            self,
            *,
            catalog_encryption_mode: typing.Optional[builtins.str] = None,
            catalog_encryption_service_role: typing.Optional[builtins.str] = None,
            sse_aws_kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the encryption-at-rest configuration for the Data Catalog.

            :param catalog_encryption_mode: The encryption-at-rest mode for encrypting Data Catalog data.
            :param catalog_encryption_service_role: The role that AWS Glue assumes to encrypt and decrypt the Data Catalog objects on the caller's behalf.
            :param sse_aws_kms_key_id: The ID of the AWS key to use for encryption at rest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-encryptionatrest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                encryption_at_rest_property = glue_mixins.CfnDataCatalogEncryptionSettingsPropsMixin.EncryptionAtRestProperty(
                    catalog_encryption_mode="catalogEncryptionMode",
                    catalog_encryption_service_role="catalogEncryptionServiceRole",
                    sse_aws_kms_key_id="sseAwsKmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4653025e0b3d9f47954254d4ef8668843cf9d3ec7bb77f484a45d85525044cc)
                check_type(argname="argument catalog_encryption_mode", value=catalog_encryption_mode, expected_type=type_hints["catalog_encryption_mode"])
                check_type(argname="argument catalog_encryption_service_role", value=catalog_encryption_service_role, expected_type=type_hints["catalog_encryption_service_role"])
                check_type(argname="argument sse_aws_kms_key_id", value=sse_aws_kms_key_id, expected_type=type_hints["sse_aws_kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_encryption_mode is not None:
                self._values["catalog_encryption_mode"] = catalog_encryption_mode
            if catalog_encryption_service_role is not None:
                self._values["catalog_encryption_service_role"] = catalog_encryption_service_role
            if sse_aws_kms_key_id is not None:
                self._values["sse_aws_kms_key_id"] = sse_aws_kms_key_id

        @builtins.property
        def catalog_encryption_mode(self) -> typing.Optional[builtins.str]:
            '''The encryption-at-rest mode for encrypting Data Catalog data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-encryptionatrest.html#cfn-glue-datacatalogencryptionsettings-encryptionatrest-catalogencryptionmode
            '''
            result = self._values.get("catalog_encryption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def catalog_encryption_service_role(self) -> typing.Optional[builtins.str]:
            '''The role that AWS Glue assumes to encrypt and decrypt the Data Catalog objects on the caller's behalf.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-encryptionatrest.html#cfn-glue-datacatalogencryptionsettings-encryptionatrest-catalogencryptionservicerole
            '''
            result = self._values.get("catalog_encryption_service_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sse_aws_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the AWS  key to use for encryption at rest.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-encryptionatrest.html#cfn-glue-datacatalogencryptionsettings-encryptionatrest-sseawskmskeyid
            '''
            result = self._values.get("sse_aws_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionAtRestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDataQualityRulesetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_token": "clientToken",
        "description": "description",
        "name": "name",
        "ruleset": "ruleset",
        "tags": "tags",
        "target_table": "targetTable",
    },
)
class CfnDataQualityRulesetMixinProps:
    def __init__(
        self,
        *,
        client_token: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        ruleset: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        target_table: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataQualityRulesetPropsMixin.DataQualityTargetTableProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataQualityRulesetPropsMixin.

        :param client_token: Used for idempotency and is recommended to be set to a random ID (such as a UUID) to avoid creating or starting multiple instances of the same resource.
        :param description: A description of the data quality ruleset.
        :param name: The name of the data quality ruleset.
        :param ruleset: A Data Quality Definition Language (DQDL) ruleset. For more information see the AWS Glue Developer Guide.
        :param tags: A list of tags applied to the data quality ruleset.
        :param target_table: An object representing an AWS Glue table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-dataqualityruleset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # tags: Any
            
            cfn_data_quality_ruleset_mixin_props = glue_mixins.CfnDataQualityRulesetMixinProps(
                client_token="clientToken",
                description="description",
                name="name",
                ruleset="ruleset",
                tags=tags,
                target_table=glue_mixins.CfnDataQualityRulesetPropsMixin.DataQualityTargetTableProperty(
                    database_name="databaseName",
                    table_name="tableName"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205f2f9d0b1963d31729912c25cc8d6c50520135570f948d62e524bea101ce4c)
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ruleset", value=ruleset, expected_type=type_hints["ruleset"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_table", value=target_table, expected_type=type_hints["target_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_token is not None:
            self._values["client_token"] = client_token
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if ruleset is not None:
            self._values["ruleset"] = ruleset
        if tags is not None:
            self._values["tags"] = tags
        if target_table is not None:
            self._values["target_table"] = target_table

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''Used for idempotency and is recommended to be set to a random ID (such as a UUID) to avoid creating or starting multiple instances of the same resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-dataqualityruleset.html#cfn-glue-dataqualityruleset-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the data quality ruleset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-dataqualityruleset.html#cfn-glue-dataqualityruleset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the data quality ruleset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-dataqualityruleset.html#cfn-glue-dataqualityruleset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ruleset(self) -> typing.Optional[builtins.str]:
        '''A Data Quality Definition Language (DQDL) ruleset.

        For more information see the AWS Glue Developer Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-dataqualityruleset.html#cfn-glue-dataqualityruleset-ruleset
        '''
        result = self._values.get("ruleset")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''A list of tags applied to the data quality ruleset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-dataqualityruleset.html#cfn-glue-dataqualityruleset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def target_table(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataQualityRulesetPropsMixin.DataQualityTargetTableProperty"]]:
        '''An object representing an AWS Glue table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-dataqualityruleset.html#cfn-glue-dataqualityruleset-targettable
        '''
        result = self._values.get("target_table")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataQualityRulesetPropsMixin.DataQualityTargetTableProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataQualityRulesetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataQualityRulesetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDataQualityRulesetPropsMixin",
):
    '''The ``AWS::Glue::DataQualityRuleset`` resource specifies a data quality ruleset with DQDL rules applied to a specified AWS Glue table.

    For more information, see AWS Glue Data Quality in the AWS Glue Developer Guide.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-dataqualityruleset.html
    :cloudformationResource: AWS::Glue::DataQualityRuleset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # tags: Any
        
        cfn_data_quality_ruleset_props_mixin = glue_mixins.CfnDataQualityRulesetPropsMixin(glue_mixins.CfnDataQualityRulesetMixinProps(
            client_token="clientToken",
            description="description",
            name="name",
            ruleset="ruleset",
            tags=tags,
            target_table=glue_mixins.CfnDataQualityRulesetPropsMixin.DataQualityTargetTableProperty(
                database_name="databaseName",
                table_name="tableName"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDataQualityRulesetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::DataQualityRuleset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd2d435e6eb6029708b10bf14d23c1b6a4ca00a98b3d661079af5b2b45da79b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b53e73d6eef57aa0f5e8f3cbe94a36df5cb2661da8dd964de977203868f984ad)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87c329b52041a49705aa3593908ca2cfff4a075a5331237d47e98ad5416596b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataQualityRulesetMixinProps:
        return typing.cast(CfnDataQualityRulesetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDataQualityRulesetPropsMixin.DataQualityTargetTableProperty",
        jsii_struct_bases=[],
        name_mapping={"database_name": "databaseName", "table_name": "tableName"},
    )
    class DataQualityTargetTableProperty:
        def __init__(
            self,
            *,
            database_name: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing an AWS Glue table.

            :param database_name: The name of the database where the AWS Glue table exists.
            :param table_name: The name of the AWS Glue table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-dataqualityruleset-dataqualitytargettable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                data_quality_target_table_property = glue_mixins.CfnDataQualityRulesetPropsMixin.DataQualityTargetTableProperty(
                    database_name="databaseName",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a312630169324f684d8115babc19d2293368fe7d8fbb7d6cc17c764f5180e78)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_name is not None:
                self._values["database_name"] = database_name
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database where the AWS Glue table exists.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-dataqualityruleset-dataqualitytargettable.html#cfn-glue-dataqualityruleset-dataqualitytargettable-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS Glue table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-dataqualityruleset-dataqualitytargettable.html#cfn-glue-dataqualityruleset-dataqualitytargettable-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataQualityTargetTableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDatabaseMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "catalog_id": "catalogId",
        "database_input": "databaseInput",
        "database_name": "databaseName",
    },
)
class CfnDatabaseMixinProps:
    def __init__(
        self,
        *,
        catalog_id: typing.Optional[builtins.str] = None,
        database_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatabasePropsMixin.DatabaseInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        database_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDatabasePropsMixin.

        :param catalog_id: The AWS account ID for the account in which to create the catalog object. .. epigraph:: To specify the account ID, you can use the ``Ref`` intrinsic function with the ``AWS::AccountId`` pseudo parameter. For example: ``!Ref AWS::AccountId``
        :param database_input: The metadata for the database.
        :param database_name: The name of the catalog database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # parameters: Any
            
            cfn_database_mixin_props = glue_mixins.CfnDatabaseMixinProps(
                catalog_id="catalogId",
                database_input=glue_mixins.CfnDatabasePropsMixin.DatabaseInputProperty(
                    create_table_default_permissions=[glue_mixins.CfnDatabasePropsMixin.PrincipalPrivilegesProperty(
                        permissions=["permissions"],
                        principal=glue_mixins.CfnDatabasePropsMixin.DataLakePrincipalProperty(
                            data_lake_principal_identifier="dataLakePrincipalIdentifier"
                        )
                    )],
                    description="description",
                    federated_database=glue_mixins.CfnDatabasePropsMixin.FederatedDatabaseProperty(
                        connection_name="connectionName",
                        identifier="identifier"
                    ),
                    location_uri="locationUri",
                    name="name",
                    parameters=parameters,
                    target_database=glue_mixins.CfnDatabasePropsMixin.DatabaseIdentifierProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        region="region"
                    )
                ),
                database_name="databaseName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a467e825a079273fb6bbc086209b32b22c4ce9b7fb1916987a5b4738558ae7)
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument database_input", value=database_input, expected_type=type_hints["database_input"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id
        if database_input is not None:
            self._values["database_input"] = database_input
        if database_name is not None:
            self._values["database_name"] = database_name

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID for the account in which to create the catalog object.

        .. epigraph::

           To specify the account ID, you can use the ``Ref`` intrinsic function with the ``AWS::AccountId`` pseudo parameter. For example: ``!Ref AWS::AccountId``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html#cfn-glue-database-catalogid
        '''
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_input(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.DatabaseInputProperty"]]:
        '''The metadata for the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html#cfn-glue-database-databaseinput
        '''
        result = self._values.get("database_input")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.DatabaseInputProperty"]], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the catalog database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html#cfn-glue-database-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatabaseMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDatabasePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDatabasePropsMixin",
):
    '''The ``AWS::Glue::Database`` resource specifies a logical grouping of tables in AWS Glue .

    For more information, see `Defining a Database in Your Data Catalog <https://docs.aws.amazon.com/glue/latest/dg/define-database.html>`_ and `Database Structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-databases.html#aws-glue-api-catalog-databases-Database>`_ in the *AWS Glue Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html
    :cloudformationResource: AWS::Glue::Database
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # parameters: Any
        
        cfn_database_props_mixin = glue_mixins.CfnDatabasePropsMixin(glue_mixins.CfnDatabaseMixinProps(
            catalog_id="catalogId",
            database_input=glue_mixins.CfnDatabasePropsMixin.DatabaseInputProperty(
                create_table_default_permissions=[glue_mixins.CfnDatabasePropsMixin.PrincipalPrivilegesProperty(
                    permissions=["permissions"],
                    principal=glue_mixins.CfnDatabasePropsMixin.DataLakePrincipalProperty(
                        data_lake_principal_identifier="dataLakePrincipalIdentifier"
                    )
                )],
                description="description",
                federated_database=glue_mixins.CfnDatabasePropsMixin.FederatedDatabaseProperty(
                    connection_name="connectionName",
                    identifier="identifier"
                ),
                location_uri="locationUri",
                name="name",
                parameters=parameters,
                target_database=glue_mixins.CfnDatabasePropsMixin.DatabaseIdentifierProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    region="region"
                )
            ),
            database_name="databaseName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDatabaseMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Database``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58a29598520530cd1f6bd1f324c10299fb1e2e1a94386d2ee955bd27e710ebc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__464dd921e8933186d066db0d711af61ec404446b3193830e1fc7ae8a35ad184f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5113e2df2c5e2877d2bb82204da8f90f3f9b198f13aad4e0d657ec0eb1b8c9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDatabaseMixinProps:
        return typing.cast(CfnDatabaseMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDatabasePropsMixin.DataLakePrincipalProperty",
        jsii_struct_bases=[],
        name_mapping={"data_lake_principal_identifier": "dataLakePrincipalIdentifier"},
    )
    class DataLakePrincipalProperty:
        def __init__(
            self,
            *,
            data_lake_principal_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS Lake Formation principal.

            :param data_lake_principal_identifier: An identifier for the AWS Lake Formation principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-datalakeprincipal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                data_lake_principal_property = glue_mixins.CfnDatabasePropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a3d36392c83f4fba93c33197d0bd672563544169125cbe3ad2bdfa18c91b767)
                check_type(argname="argument data_lake_principal_identifier", value=data_lake_principal_identifier, expected_type=type_hints["data_lake_principal_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_lake_principal_identifier is not None:
                self._values["data_lake_principal_identifier"] = data_lake_principal_identifier

        @builtins.property
        def data_lake_principal_identifier(self) -> typing.Optional[builtins.str]:
            '''An identifier for the AWS Lake Formation principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-datalakeprincipal.html#cfn-glue-database-datalakeprincipal-datalakeprincipalidentifier
            '''
            result = self._values.get("data_lake_principal_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataLakePrincipalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDatabasePropsMixin.DatabaseIdentifierProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "region": "region",
        },
    )
    class DatabaseIdentifierProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that describes a target database for resource linking.

            :param catalog_id: The ID of the Data Catalog in which the database resides.
            :param database_name: The name of the catalog database.
            :param region: The Region of the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseidentifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                database_identifier_property = glue_mixins.CfnDatabasePropsMixin.DatabaseIdentifierProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92cda326aa838c7d576241421ddb731569901815a9da9a545c774679f98f2450)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the Data Catalog in which the database resides.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseidentifier.html#cfn-glue-database-databaseidentifier-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the catalog database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseidentifier.html#cfn-glue-database-databaseidentifier-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The Region of the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseidentifier.html#cfn-glue-database-databaseidentifier-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseIdentifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDatabasePropsMixin.DatabaseInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "create_table_default_permissions": "createTableDefaultPermissions",
            "description": "description",
            "federated_database": "federatedDatabase",
            "location_uri": "locationUri",
            "name": "name",
            "parameters": "parameters",
            "target_database": "targetDatabase",
        },
    )
    class DatabaseInputProperty:
        def __init__(
            self,
            *,
            create_table_default_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatabasePropsMixin.PrincipalPrivilegesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            description: typing.Optional[builtins.str] = None,
            federated_database: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatabasePropsMixin.FederatedDatabaseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            location_uri: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
            target_database: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatabasePropsMixin.DatabaseIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The structure used to create or update a database.

            :param create_table_default_permissions: Creates a set of default permissions on the table for principals. Used by AWS Lake Formation . Not used in the normal course of AWS Glue operations.
            :param description: A description of the database.
            :param federated_database: A ``FederatedDatabase`` structure that references an entity outside the AWS Glue Data Catalog .
            :param location_uri: The location of the database (for example, an HDFS path).
            :param name: The name of the database. For Hive compatibility, this is folded to lowercase when it is stored.
            :param parameters: These key-value pairs define parameters and properties of the database.
            :param target_database: A ``DatabaseIdentifier`` structure that describes a target database for resource linking.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # parameters: Any
                
                database_input_property = glue_mixins.CfnDatabasePropsMixin.DatabaseInputProperty(
                    create_table_default_permissions=[glue_mixins.CfnDatabasePropsMixin.PrincipalPrivilegesProperty(
                        permissions=["permissions"],
                        principal=glue_mixins.CfnDatabasePropsMixin.DataLakePrincipalProperty(
                            data_lake_principal_identifier="dataLakePrincipalIdentifier"
                        )
                    )],
                    description="description",
                    federated_database=glue_mixins.CfnDatabasePropsMixin.FederatedDatabaseProperty(
                        connection_name="connectionName",
                        identifier="identifier"
                    ),
                    location_uri="locationUri",
                    name="name",
                    parameters=parameters,
                    target_database=glue_mixins.CfnDatabasePropsMixin.DatabaseIdentifierProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        region="region"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__157a1dcd98bd1bde2a279406ee8abef3f868f45e024abbf346790af3b247af91)
                check_type(argname="argument create_table_default_permissions", value=create_table_default_permissions, expected_type=type_hints["create_table_default_permissions"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument federated_database", value=federated_database, expected_type=type_hints["federated_database"])
                check_type(argname="argument location_uri", value=location_uri, expected_type=type_hints["location_uri"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument target_database", value=target_database, expected_type=type_hints["target_database"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if create_table_default_permissions is not None:
                self._values["create_table_default_permissions"] = create_table_default_permissions
            if description is not None:
                self._values["description"] = description
            if federated_database is not None:
                self._values["federated_database"] = federated_database
            if location_uri is not None:
                self._values["location_uri"] = location_uri
            if name is not None:
                self._values["name"] = name
            if parameters is not None:
                self._values["parameters"] = parameters
            if target_database is not None:
                self._values["target_database"] = target_database

        @builtins.property
        def create_table_default_permissions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.PrincipalPrivilegesProperty"]]]]:
            '''Creates a set of default permissions on the table for principals.

            Used by AWS Lake Formation . Not used in the normal course of AWS Glue operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-createtabledefaultpermissions
            '''
            result = self._values.get("create_table_default_permissions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.PrincipalPrivilegesProperty"]]]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def federated_database(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.FederatedDatabaseProperty"]]:
            '''A ``FederatedDatabase`` structure that references an entity outside the AWS Glue Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-federateddatabase
            '''
            result = self._values.get("federated_database")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.FederatedDatabaseProperty"]], result)

        @builtins.property
        def location_uri(self) -> typing.Optional[builtins.str]:
            '''The location of the database (for example, an HDFS path).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-locationuri
            '''
            result = self._values.get("location_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the database.

            For Hive compatibility, this is folded to lowercase when it is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''These key-value pairs define parameters and properties of the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def target_database(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.DatabaseIdentifierProperty"]]:
            '''A ``DatabaseIdentifier`` structure that describes a target database for resource linking.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-targetdatabase
            '''
            result = self._values.get("target_database")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.DatabaseIdentifierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDatabasePropsMixin.FederatedDatabaseProperty",
        jsii_struct_bases=[],
        name_mapping={"connection_name": "connectionName", "identifier": "identifier"},
    )
    class FederatedDatabaseProperty:
        def __init__(
            self,
            *,
            connection_name: typing.Optional[builtins.str] = None,
            identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A ``FederatedDatabase`` structure that references an entity outside the AWS Glue Data Catalog .

            :param connection_name: The name of the connection to the external metastore.
            :param identifier: A unique identifier for the federated database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-federateddatabase.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                federated_database_property = glue_mixins.CfnDatabasePropsMixin.FederatedDatabaseProperty(
                    connection_name="connectionName",
                    identifier="identifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b98184b1d2aed5e3c13110e2b9dfae1b5ba8e397dc2d850b0bed2e30b22342c)
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if identifier is not None:
                self._values["identifier"] = identifier

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connection to the external metastore.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-federateddatabase.html#cfn-glue-database-federateddatabase-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def identifier(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for the federated database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-federateddatabase.html#cfn-glue-database-federateddatabase-identifier
            '''
            result = self._values.get("identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FederatedDatabaseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDatabasePropsMixin.PrincipalPrivilegesProperty",
        jsii_struct_bases=[],
        name_mapping={"permissions": "permissions", "principal": "principal"},
    )
    class PrincipalPrivilegesProperty:
        def __init__(
            self,
            *,
            permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
            principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatabasePropsMixin.DataLakePrincipalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''the permissions granted to a principal.

            :param permissions: The permissions that are granted to the principal.
            :param principal: The principal who is granted permissions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-principalprivileges.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                principal_privileges_property = glue_mixins.CfnDatabasePropsMixin.PrincipalPrivilegesProperty(
                    permissions=["permissions"],
                    principal=glue_mixins.CfnDatabasePropsMixin.DataLakePrincipalProperty(
                        data_lake_principal_identifier="dataLakePrincipalIdentifier"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca455317c3ea9aba777335c061ba67870153569bba3f01a7867250ea7a136d22)
                check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
                check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if permissions is not None:
                self._values["permissions"] = permissions
            if principal is not None:
                self._values["principal"] = principal

        @builtins.property
        def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The permissions that are granted to the principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-principalprivileges.html#cfn-glue-database-principalprivileges-permissions
            '''
            result = self._values.get("permissions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def principal(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.DataLakePrincipalProperty"]]:
            '''The principal who is granted permissions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-principalprivileges.html#cfn-glue-database-principalprivileges-principal
            '''
            result = self._values.get("principal")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.DataLakePrincipalProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrincipalPrivilegesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDevEndpointMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "arguments": "arguments",
        "endpoint_name": "endpointName",
        "extra_jars_s3_path": "extraJarsS3Path",
        "extra_python_libs_s3_path": "extraPythonLibsS3Path",
        "glue_version": "glueVersion",
        "number_of_nodes": "numberOfNodes",
        "number_of_workers": "numberOfWorkers",
        "public_key": "publicKey",
        "public_keys": "publicKeys",
        "role_arn": "roleArn",
        "security_configuration": "securityConfiguration",
        "security_group_ids": "securityGroupIds",
        "subnet_id": "subnetId",
        "tags": "tags",
        "worker_type": "workerType",
    },
)
class CfnDevEndpointMixinProps:
    def __init__(
        self,
        *,
        arguments: typing.Any = None,
        endpoint_name: typing.Optional[builtins.str] = None,
        extra_jars_s3_path: typing.Optional[builtins.str] = None,
        extra_python_libs_s3_path: typing.Optional[builtins.str] = None,
        glue_version: typing.Optional[builtins.str] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        number_of_workers: typing.Optional[jsii.Number] = None,
        public_key: typing.Optional[builtins.str] = None,
        public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        worker_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDevEndpointPropsMixin.

        :param arguments: A map of arguments used to configure the ``DevEndpoint`` . Valid arguments are: - ``"--enable-glue-datacatalog": ""`` - ``"GLUE_PYTHON_VERSION": "3"`` - ``"GLUE_PYTHON_VERSION": "2"`` You can specify a version of Python support for development endpoints by using the ``Arguments`` parameter in the ``CreateDevEndpoint`` or ``UpdateDevEndpoint`` APIs. If no arguments are provided, the version defaults to Python 2.
        :param endpoint_name: The name of the ``DevEndpoint`` .
        :param extra_jars_s3_path: The path to one or more Java ``.jar`` files in an S3 bucket that should be loaded in your ``DevEndpoint`` . .. epigraph:: You can only use pure Java/Scala libraries with a ``DevEndpoint`` .
        :param extra_python_libs_s3_path: The paths to one or more Python libraries in an Amazon S3 bucket that should be loaded in your ``DevEndpoint`` . Multiple values must be complete paths separated by a comma. .. epigraph:: You can only use pure Python libraries with a ``DevEndpoint`` . Libraries that rely on C extensions, such as the `pandas <https://docs.aws.amazon.com/http://pandas.pydata.org/>`_ Python data analysis library, are not currently supported.
        :param glue_version: The AWS Glue version determines the versions of Apache Spark and Python that AWS Glue supports. The Python version indicates the version supported for running your ETL scripts on development endpoints. For more information about the available AWS Glue versions and corresponding Spark and Python versions, see `Glue version <https://docs.aws.amazon.com/glue/latest/dg/add-job.html>`_ in the developer guide. Development endpoints that are created without specifying a Glue version default to Glue 0.9. You can specify a version of Python support for development endpoints by using the ``Arguments`` parameter in the ``CreateDevEndpoint`` or ``UpdateDevEndpoint`` APIs. If no arguments are provided, the version defaults to Python 2.
        :param number_of_nodes: The number of AWS Glue Data Processing Units (DPUs) allocated to this ``DevEndpoint`` .
        :param number_of_workers: The number of workers of a defined ``workerType`` that are allocated to the development endpoint. The maximum number of workers you can define are 299 for ``G.1X`` , and 149 for ``G.2X`` .
        :param public_key: The public key to be used by this ``DevEndpoint`` for authentication. This attribute is provided for backward compatibility because the recommended attribute to use is public keys.
        :param public_keys: A list of public keys to be used by the ``DevEndpoints`` for authentication. Using this attribute is preferred over a single public key because the public keys allow you to have a different private key per client. .. epigraph:: If you previously created an endpoint with a public key, you must remove that key to be able to set a list of public keys. Call the ``UpdateDevEndpoint`` API operation with the public key content in the ``deletePublicKeys`` attribute, and the list of new keys in the ``addPublicKeys`` attribute.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role used in this ``DevEndpoint`` .
        :param security_configuration: The name of the ``SecurityConfiguration`` structure to be used with this ``DevEndpoint`` .
        :param security_group_ids: A list of security group identifiers used in this ``DevEndpoint`` .
        :param subnet_id: The subnet ID for this ``DevEndpoint`` .
        :param tags: The tags to use with this DevEndpoint.
        :param worker_type: The type of predefined worker that is allocated to the development endpoint. Accepts a value of Standard, G.1X, or G.2X. - For the ``Standard`` worker type, each worker provides 4 vCPU, 16 GB of memory and a 50GB disk, and 2 executors per worker. - For the ``G.1X`` worker type, each worker maps to 1 DPU (4 vCPU, 16 GB of memory, 64 GB disk), and provides 1 executor per worker. We recommend this worker type for memory-intensive jobs. - For the ``G.2X`` worker type, each worker maps to 2 DPU (8 vCPU, 32 GB of memory, 128 GB disk), and provides 1 executor per worker. We recommend this worker type for memory-intensive jobs. Known issue: when a development endpoint is created with the ``G.2X`` ``WorkerType`` configuration, the Spark drivers for the development endpoint will run on 4 vCPU, 16 GB of memory, and a 64 GB disk.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # arguments_: Any
            # tags: Any
            
            cfn_dev_endpoint_mixin_props = glue_mixins.CfnDevEndpointMixinProps(
                arguments=arguments_,
                endpoint_name="endpointName",
                extra_jars_s3_path="extraJarsS3Path",
                extra_python_libs_s3_path="extraPythonLibsS3Path",
                glue_version="glueVersion",
                number_of_nodes=123,
                number_of_workers=123,
                public_key="publicKey",
                public_keys=["publicKeys"],
                role_arn="roleArn",
                security_configuration="securityConfiguration",
                security_group_ids=["securityGroupIds"],
                subnet_id="subnetId",
                tags=tags,
                worker_type="workerType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde2c948af0417f6089142e19ed3156b06da222a7d120b1729015503c6a48d44)
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument endpoint_name", value=endpoint_name, expected_type=type_hints["endpoint_name"])
            check_type(argname="argument extra_jars_s3_path", value=extra_jars_s3_path, expected_type=type_hints["extra_jars_s3_path"])
            check_type(argname="argument extra_python_libs_s3_path", value=extra_python_libs_s3_path, expected_type=type_hints["extra_python_libs_s3_path"])
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument number_of_nodes", value=number_of_nodes, expected_type=type_hints["number_of_nodes"])
            check_type(argname="argument number_of_workers", value=number_of_workers, expected_type=type_hints["number_of_workers"])
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument public_keys", value=public_keys, expected_type=type_hints["public_keys"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arguments is not None:
            self._values["arguments"] = arguments
        if endpoint_name is not None:
            self._values["endpoint_name"] = endpoint_name
        if extra_jars_s3_path is not None:
            self._values["extra_jars_s3_path"] = extra_jars_s3_path
        if extra_python_libs_s3_path is not None:
            self._values["extra_python_libs_s3_path"] = extra_python_libs_s3_path
        if glue_version is not None:
            self._values["glue_version"] = glue_version
        if number_of_nodes is not None:
            self._values["number_of_nodes"] = number_of_nodes
        if number_of_workers is not None:
            self._values["number_of_workers"] = number_of_workers
        if public_key is not None:
            self._values["public_key"] = public_key
        if public_keys is not None:
            self._values["public_keys"] = public_keys
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags
        if worker_type is not None:
            self._values["worker_type"] = worker_type

    @builtins.property
    def arguments(self) -> typing.Any:
        '''A map of arguments used to configure the ``DevEndpoint`` .

        Valid arguments are:

        - ``"--enable-glue-datacatalog": ""``
        - ``"GLUE_PYTHON_VERSION": "3"``
        - ``"GLUE_PYTHON_VERSION": "2"``

        You can specify a version of Python support for development endpoints by using the ``Arguments`` parameter in the ``CreateDevEndpoint`` or ``UpdateDevEndpoint`` APIs. If no arguments are provided, the version defaults to Python 2.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-arguments
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Any, result)

    @builtins.property
    def endpoint_name(self) -> typing.Optional[builtins.str]:
        '''The name of the ``DevEndpoint`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-endpointname
        '''
        result = self._values.get("endpoint_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_jars_s3_path(self) -> typing.Optional[builtins.str]:
        '''The path to one or more Java ``.jar`` files in an S3 bucket that should be loaded in your ``DevEndpoint`` .

        .. epigraph::

           You can only use pure Java/Scala libraries with a ``DevEndpoint`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-extrajarss3path
        '''
        result = self._values.get("extra_jars_s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_python_libs_s3_path(self) -> typing.Optional[builtins.str]:
        '''The paths to one or more Python libraries in an Amazon S3 bucket that should be loaded in your ``DevEndpoint`` .

        Multiple values must be complete paths separated by a comma.
        .. epigraph::

           You can only use pure Python libraries with a ``DevEndpoint`` . Libraries that rely on C extensions, such as the `pandas <https://docs.aws.amazon.com/http://pandas.pydata.org/>`_ Python data analysis library, are not currently supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-extrapythonlibss3path
        '''
        result = self._values.get("extra_python_libs_s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glue_version(self) -> typing.Optional[builtins.str]:
        '''The AWS Glue version determines the versions of Apache Spark and Python that AWS Glue supports.

        The Python version indicates the version supported for running your ETL scripts on development endpoints.

        For more information about the available AWS Glue versions and corresponding Spark and Python versions, see `Glue version <https://docs.aws.amazon.com/glue/latest/dg/add-job.html>`_ in the developer guide.

        Development endpoints that are created without specifying a Glue version default to Glue 0.9.

        You can specify a version of Python support for development endpoints by using the ``Arguments`` parameter in the ``CreateDevEndpoint`` or ``UpdateDevEndpoint`` APIs. If no arguments are provided, the version defaults to Python 2.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-glueversion
        '''
        result = self._values.get("glue_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        '''The number of AWS Glue Data Processing Units (DPUs) allocated to this ``DevEndpoint`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-numberofnodes
        '''
        result = self._values.get("number_of_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        '''The number of workers of a defined ``workerType`` that are allocated to the development endpoint.

        The maximum number of workers you can define are 299 for ``G.1X`` , and 149 for ``G.2X`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-numberofworkers
        '''
        result = self._values.get("number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def public_key(self) -> typing.Optional[builtins.str]:
        '''The public key to be used by this ``DevEndpoint`` for authentication.

        This attribute is provided for backward compatibility because the recommended attribute to use is public keys.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-publickey
        '''
        result = self._values.get("public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of public keys to be used by the ``DevEndpoints`` for authentication.

        Using this attribute is preferred over a single public key because the public keys allow you to have a different private key per client.
        .. epigraph::

           If you previously created an endpoint with a public key, you must remove that key to be able to set a list of public keys. Call the ``UpdateDevEndpoint`` API operation with the public key content in the ``deletePublicKeys`` attribute, and the list of new keys in the ``addPublicKeys`` attribute.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-publickeys
        '''
        result = self._values.get("public_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role used in this ``DevEndpoint`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''The name of the ``SecurityConfiguration`` structure to be used with this ``DevEndpoint`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-securityconfiguration
        '''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group identifiers used in this ``DevEndpoint`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''The subnet ID for this ``DevEndpoint`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-subnetid
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags to use with this DevEndpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def worker_type(self) -> typing.Optional[builtins.str]:
        '''The type of predefined worker that is allocated to the development endpoint.

        Accepts a value of Standard, G.1X, or G.2X.

        - For the ``Standard`` worker type, each worker provides 4 vCPU, 16 GB of memory and a 50GB disk, and 2 executors per worker.
        - For the ``G.1X`` worker type, each worker maps to 1 DPU (4 vCPU, 16 GB of memory, 64 GB disk), and provides 1 executor per worker. We recommend this worker type for memory-intensive jobs.
        - For the ``G.2X`` worker type, each worker maps to 2 DPU (8 vCPU, 32 GB of memory, 128 GB disk), and provides 1 executor per worker. We recommend this worker type for memory-intensive jobs.

        Known issue: when a development endpoint is created with the ``G.2X`` ``WorkerType`` configuration, the Spark drivers for the development endpoint will run on 4 vCPU, 16 GB of memory, and a 64 GB disk.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-workertype
        '''
        result = self._values.get("worker_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDevEndpointMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDevEndpointPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnDevEndpointPropsMixin",
):
    '''The ``AWS::Glue::DevEndpoint`` resource specifies a development endpoint where a developer can remotely debug ETL scripts for AWS Glue .

    For more information, see `DevEndpoint Structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-dev-endpoint.html#aws-glue-api-jobs-dev-endpoint-DevEndpoint>`_ in the AWS Glue Developer Guide.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html
    :cloudformationResource: AWS::Glue::DevEndpoint
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # arguments_: Any
        # tags: Any
        
        cfn_dev_endpoint_props_mixin = glue_mixins.CfnDevEndpointPropsMixin(glue_mixins.CfnDevEndpointMixinProps(
            arguments=arguments_,
            endpoint_name="endpointName",
            extra_jars_s3_path="extraJarsS3Path",
            extra_python_libs_s3_path="extraPythonLibsS3Path",
            glue_version="glueVersion",
            number_of_nodes=123,
            number_of_workers=123,
            public_key="publicKey",
            public_keys=["publicKeys"],
            role_arn="roleArn",
            security_configuration="securityConfiguration",
            security_group_ids=["securityGroupIds"],
            subnet_id="subnetId",
            tags=tags,
            worker_type="workerType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDevEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::DevEndpoint``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f74c062a7d53fbd09f2735edc939e3fb77696e217fbc978c4b9b74756bbc3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dafb75be79545cd504195e203f5e79375048e9861a781551fd8d46575a242af0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c62961f75e933cfcc3e88e541da05ed71e7aae5be4dedc97babb54a7673884)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDevEndpointMixinProps:
        return typing.cast(CfnDevEndpointMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnIdentityCenterConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "scopes": "scopes",
        "user_background_sessions_enabled": "userBackgroundSessionsEnabled",
    },
)
class CfnIdentityCenterConfigurationMixinProps:
    def __init__(
        self,
        *,
        instance_arn: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_background_sessions_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnIdentityCenterConfigurationPropsMixin.

        :param instance_arn: The IAM identity center instance arn.
        :param scopes: The downstream scopes that Glue identity center configuration can access.
        :param user_background_sessions_enabled: Enable or disable user background sessions for Glue Identity Center.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-identitycenterconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_identity_center_configuration_mixin_props = glue_mixins.CfnIdentityCenterConfigurationMixinProps(
                instance_arn="instanceArn",
                scopes=["scopes"],
                user_background_sessions_enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8f980a4305395998503cf51e60269aa3b4712f3fbdef556c73ba96fc52deae)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument user_background_sessions_enabled", value=user_background_sessions_enabled, expected_type=type_hints["user_background_sessions_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if scopes is not None:
            self._values["scopes"] = scopes
        if user_background_sessions_enabled is not None:
            self._values["user_background_sessions_enabled"] = user_background_sessions_enabled

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM identity center instance arn.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-identitycenterconfiguration.html#cfn-glue-identitycenterconfiguration-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The downstream scopes that Glue identity center configuration can access.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-identitycenterconfiguration.html#cfn-glue-identitycenterconfiguration-scopes
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_background_sessions_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enable or disable user background sessions for Glue Identity Center.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-identitycenterconfiguration.html#cfn-glue-identitycenterconfiguration-userbackgroundsessionsenabled
        '''
        result = self._values.get("user_background_sessions_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentityCenterConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdentityCenterConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnIdentityCenterConfigurationPropsMixin",
):
    '''Resource Type definition for AWS::Glue::IdentityCenterConfiguration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-identitycenterconfiguration.html
    :cloudformationResource: AWS::Glue::IdentityCenterConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_identity_center_configuration_props_mixin = glue_mixins.CfnIdentityCenterConfigurationPropsMixin(glue_mixins.CfnIdentityCenterConfigurationMixinProps(
            instance_arn="instanceArn",
            scopes=["scopes"],
            user_background_sessions_enabled=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIdentityCenterConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::IdentityCenterConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8147c74f06204d5565b2d0c3c82c67b52f0abc6833685ad1b44c4a6147a2ade)
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
            type_hints = typing.get_type_hints(_typecheckingstub__883eb9e51ca5abb2896a9341d64f8246e5f7f28b7e7d52016a1646b7e3e1d7d1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9474a9790bc6c2a11065ee5c90ac71ba05c8a25813978c82d49a2bf3f9fd7d2a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdentityCenterConfigurationMixinProps:
        return typing.cast(CfnIdentityCenterConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "additional_encryption_context": "additionalEncryptionContext",
        "data_filter": "dataFilter",
        "description": "description",
        "integration_config": "integrationConfig",
        "integration_name": "integrationName",
        "kms_key_id": "kmsKeyId",
        "source_arn": "sourceArn",
        "tags": "tags",
        "target_arn": "targetArn",
    },
)
class CfnIntegrationMixinProps:
    def __init__(
        self,
        *,
        additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        data_filter: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        integration_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.IntegrationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        integration_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        source_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIntegrationPropsMixin.

        :param additional_encryption_context: An optional set of non-secret key–value pairs that contains additional contextual information for encryption. This can only be provided if ``KMSKeyId`` is provided.
        :param data_filter: Selects source tables for the integration using Maxwell filter syntax.
        :param description: A description for the integration.
        :param integration_config: The structure used to define properties associated with the zero-ETL integration. For more information, see `IntegrationConfig structure. <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-integrations.html#aws-glue-api-integrations-IntegrationConfig>`_
        :param integration_name: A unique name for the integration.
        :param kms_key_id: The ARN of a KMS key used for encrypting the channel.
        :param source_arn: The ARN for the source of the integration.
        :param tags: Metadata assigned to the resource consisting of a list of key-value pairs.
        :param target_arn: The ARN for the target of the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_integration_mixin_props = glue_mixins.CfnIntegrationMixinProps(
                additional_encryption_context={
                    "additional_encryption_context_key": "additionalEncryptionContext"
                },
                data_filter="dataFilter",
                description="description",
                integration_config=glue_mixins.CfnIntegrationPropsMixin.IntegrationConfigProperty(
                    continuous_sync=False,
                    refresh_interval="refreshInterval",
                    source_properties={
                        "source_properties_key": "sourceProperties"
                    }
                ),
                integration_name="integrationName",
                kms_key_id="kmsKeyId",
                source_arn="sourceArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_arn="targetArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a132bfd4d44707640b924d7929633369261a3b8c2b5113c4c46847de8f072ddb)
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument data_filter", value=data_filter, expected_type=type_hints["data_filter"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument integration_config", value=integration_config, expected_type=type_hints["integration_config"])
            check_type(argname="argument integration_name", value=integration_name, expected_type=type_hints["integration_name"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if data_filter is not None:
            self._values["data_filter"] = data_filter
        if description is not None:
            self._values["description"] = description
        if integration_config is not None:
            self._values["integration_config"] = integration_config
        if integration_name is not None:
            self._values["integration_name"] = integration_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if source_arn is not None:
            self._values["source_arn"] = source_arn
        if tags is not None:
            self._values["tags"] = tags
        if target_arn is not None:
            self._values["target_arn"] = target_arn

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''An optional set of non-secret key–value pairs that contains additional contextual information for encryption.

        This can only be provided if ``KMSKeyId`` is provided.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html#cfn-glue-integration-additionalencryptioncontext
        '''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def data_filter(self) -> typing.Optional[builtins.str]:
        '''Selects source tables for the integration using Maxwell filter syntax.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html#cfn-glue-integration-datafilter
        '''
        result = self._values.get("data_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html#cfn-glue-integration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.IntegrationConfigProperty"]]:
        '''The structure used to define properties associated with the zero-ETL integration.

        For more information, see `IntegrationConfig structure. <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-integrations.html#aws-glue-api-integrations-IntegrationConfig>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html#cfn-glue-integration-integrationconfig
        '''
        result = self._values.get("integration_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.IntegrationConfigProperty"]], result)

    @builtins.property
    def integration_name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html#cfn-glue-integration-integrationname
        '''
        result = self._values.get("integration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ARN of a KMS key used for encrypting the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html#cfn-glue-integration-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the source of the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html#cfn-glue-integration-sourcearn
        '''
        result = self._values.get("source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata assigned to the resource consisting of a list of key-value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html#cfn-glue-integration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN for the target of the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html#cfn-glue-integration-targetarn
        '''
        result = self._values.get("target_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIntegrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnIntegrationPropsMixin",
):
    '''The ``AWS::Glue::Integration`` resource specifies an AWS Glue zero-ETL integration from a data source to a target.

    For more information, see `zero-ETL integration supported by AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/zero-etl-using.html>`_ and `integration structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-integrations.html>`_ in the AWS Glue developer guide.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integration.html
    :cloudformationResource: AWS::Glue::Integration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_integration_props_mixin = glue_mixins.CfnIntegrationPropsMixin(glue_mixins.CfnIntegrationMixinProps(
            additional_encryption_context={
                "additional_encryption_context_key": "additionalEncryptionContext"
            },
            data_filter="dataFilter",
            description="description",
            integration_config=glue_mixins.CfnIntegrationPropsMixin.IntegrationConfigProperty(
                continuous_sync=False,
                refresh_interval="refreshInterval",
                source_properties={
                    "source_properties_key": "sourceProperties"
                }
            ),
            integration_name="integrationName",
            kms_key_id="kmsKeyId",
            source_arn="sourceArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_arn="targetArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Integration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c30c29f3ac0f9577d1ff2c3b79ec39485c57611e025ffbb6d61a9223e0dfb4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6549d953fd5fbe8130d5cfa57d40d3fbb7ad747a350825b2aaf3127d79a1607f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0725fbf344fbc39ffeb02d3a9ef22ac624c2fd758a1c864ee855e8474a082f38)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIntegrationMixinProps:
        return typing.cast(CfnIntegrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnIntegrationPropsMixin.IntegrationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "continuous_sync": "continuousSync",
            "refresh_interval": "refreshInterval",
            "source_properties": "sourceProperties",
        },
    )
    class IntegrationConfigProperty:
        def __init__(
            self,
            *,
            continuous_sync: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            refresh_interval: typing.Optional[builtins.str] = None,
            source_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Properties associated with the integration.

            :param continuous_sync: Enables continuous synchronization for on-demand data extractions from SaaS applications to AWS data services like Amazon Redshift and Amazon S3.
            :param refresh_interval: Specifies the frequency at which CDC (Change Data Capture) pulls or incremental loads should occur. This parameter provides flexibility to align the refresh rate with your specific data update patterns, system load considerations, and performance optimization goals. Time increment can be set from 15 minutes to 8640 minutes (six days).
            :param source_properties: A collection of key-value pairs that specify additional properties for the integration source. These properties provide configuration options that can be used to customize the behavior of the ODB source during data integration operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integration-integrationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                integration_config_property = glue_mixins.CfnIntegrationPropsMixin.IntegrationConfigProperty(
                    continuous_sync=False,
                    refresh_interval="refreshInterval",
                    source_properties={
                        "source_properties_key": "sourceProperties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a70100596a15c10c2b99dd5f72e857392b7fa052e987d0d4842c6d22a53b3e58)
                check_type(argname="argument continuous_sync", value=continuous_sync, expected_type=type_hints["continuous_sync"])
                check_type(argname="argument refresh_interval", value=refresh_interval, expected_type=type_hints["refresh_interval"])
                check_type(argname="argument source_properties", value=source_properties, expected_type=type_hints["source_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if continuous_sync is not None:
                self._values["continuous_sync"] = continuous_sync
            if refresh_interval is not None:
                self._values["refresh_interval"] = refresh_interval
            if source_properties is not None:
                self._values["source_properties"] = source_properties

        @builtins.property
        def continuous_sync(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables continuous synchronization for on-demand data extractions from SaaS applications to AWS data services like Amazon Redshift and Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integration-integrationconfig.html#cfn-glue-integration-integrationconfig-continuoussync
            '''
            result = self._values.get("continuous_sync")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def refresh_interval(self) -> typing.Optional[builtins.str]:
            '''Specifies the frequency at which CDC (Change Data Capture) pulls or incremental loads should occur.

            This parameter provides flexibility to align the refresh rate with your specific data update patterns, system load considerations, and performance optimization goals. Time increment can be set from 15 minutes to 8640 minutes (six days).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integration-integrationconfig.html#cfn-glue-integration-integrationconfig-refreshinterval
            '''
            result = self._values.get("refresh_interval")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A collection of key-value pairs that specify additional properties for the integration source.

            These properties provide configuration options that can be used to customize the behavior of the ODB source during data integration operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integration-integrationconfig.html#cfn-glue-integration-integrationconfig-sourceproperties
            '''
            result = self._values.get("source_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntegrationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnIntegrationResourcePropertyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "resource_arn": "resourceArn",
        "source_processing_properties": "sourceProcessingProperties",
        "tags": "tags",
        "target_processing_properties": "targetProcessingProperties",
    },
)
class CfnIntegrationResourcePropertyMixinProps:
    def __init__(
        self,
        *,
        resource_arn: typing.Optional[builtins.str] = None,
        source_processing_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationResourcePropertyPropsMixin.SourceProcessingPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_processing_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationResourcePropertyPropsMixin.TargetProcessingPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnIntegrationResourcePropertyPropsMixin.

        :param resource_arn: The connection ARN of the source, or the database ARN of the target.
        :param source_processing_properties: The resource properties associated with the integration source.
        :param tags: An array of key-value pairs to apply to this resource.
        :param target_processing_properties: The structure used to define the resource properties associated with the integration target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integrationresourceproperty.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_integration_resource_property_mixin_props = glue_mixins.CfnIntegrationResourcePropertyMixinProps(
                resource_arn="resourceArn",
                source_processing_properties=glue_mixins.CfnIntegrationResourcePropertyPropsMixin.SourceProcessingPropertiesProperty(
                    role_arn="roleArn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_processing_properties=glue_mixins.CfnIntegrationResourcePropertyPropsMixin.TargetProcessingPropertiesProperty(
                    connection_name="connectionName",
                    event_bus_arn="eventBusArn",
                    kms_arn="kmsArn",
                    role_arn="roleArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ca6deb5a0e19e24480245587be3004b1cde980dc8da6e717db7aed098653e1)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument source_processing_properties", value=source_processing_properties, expected_type=type_hints["source_processing_properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_processing_properties", value=target_processing_properties, expected_type=type_hints["target_processing_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn
        if source_processing_properties is not None:
            self._values["source_processing_properties"] = source_processing_properties
        if tags is not None:
            self._values["tags"] = tags
        if target_processing_properties is not None:
            self._values["target_processing_properties"] = target_processing_properties

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''The connection ARN of the source, or the database ARN of the target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integrationresourceproperty.html#cfn-glue-integrationresourceproperty-resourcearn
        '''
        result = self._values.get("resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_processing_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationResourcePropertyPropsMixin.SourceProcessingPropertiesProperty"]]:
        '''The resource properties associated with the integration source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integrationresourceproperty.html#cfn-glue-integrationresourceproperty-sourceprocessingproperties
        '''
        result = self._values.get("source_processing_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationResourcePropertyPropsMixin.SourceProcessingPropertiesProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integrationresourceproperty.html#cfn-glue-integrationresourceproperty-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_processing_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationResourcePropertyPropsMixin.TargetProcessingPropertiesProperty"]]:
        '''The structure used to define the resource properties associated with the integration target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integrationresourceproperty.html#cfn-glue-integrationresourceproperty-targetprocessingproperties
        '''
        result = self._values.get("target_processing_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationResourcePropertyPropsMixin.TargetProcessingPropertiesProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationResourcePropertyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIntegrationResourcePropertyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnIntegrationResourcePropertyPropsMixin",
):
    '''The ``AWS::Glue::IntegrationResourceProperty`` resource type can be used to setup ``ResourceProperty`` of the AWS Glue connection (for the SaaS source), DynamoDB Database (for DynamoDB source), or AWS Glue database ARN (for the target).

    ResourceProperty is used to define the properties requires to setup the integration, including the role to access the connection or database, KMS keys, event bus for event notifications and VPC connection. To set both source and target properties the same API needs to be invoked twice, once with the AWS Glue connection ARN as ResourceArn with SourceProcessingProperties and next, with the AWS Glue database ARN as ResourceArn with TargetProcessingProperties respectively.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-integrationresourceproperty.html
    :cloudformationResource: AWS::Glue::IntegrationResourceProperty
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_integration_resource_property_props_mixin = glue_mixins.CfnIntegrationResourcePropertyPropsMixin(glue_mixins.CfnIntegrationResourcePropertyMixinProps(
            resource_arn="resourceArn",
            source_processing_properties=glue_mixins.CfnIntegrationResourcePropertyPropsMixin.SourceProcessingPropertiesProperty(
                role_arn="roleArn"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_processing_properties=glue_mixins.CfnIntegrationResourcePropertyPropsMixin.TargetProcessingPropertiesProperty(
                connection_name="connectionName",
                event_bus_arn="eventBusArn",
                kms_arn="kmsArn",
                role_arn="roleArn"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIntegrationResourcePropertyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::IntegrationResourceProperty``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acbc21d7c63b93df417924b078de7d6e7c45bd10236ab19f951b2f8fc51fb20b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad89bb67fd4372947bfc0fe3c8e9d5ee9599b117969b94bb438d16ea7025d6f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d825bc81663edbcee039547a616b8ce5b30a40a730e28e46a162d6d050e040f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIntegrationResourcePropertyMixinProps:
        return typing.cast(CfnIntegrationResourcePropertyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnIntegrationResourcePropertyPropsMixin.SourceProcessingPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn"},
    )
    class SourceProcessingPropertiesProperty:
        def __init__(self, *, role_arn: typing.Optional[builtins.str] = None) -> None:
            '''The structure used to define the resource properties associated with the integration source.

            :param role_arn: The IAM role to access the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integrationresourceproperty-sourceprocessingproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                source_processing_properties_property = glue_mixins.CfnIntegrationResourcePropertyPropsMixin.SourceProcessingPropertiesProperty(
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fdc7dfa6ecd1ba0a85f12987cf77f3d08e6b4b4bfc532db83bba701b2736513)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The IAM role to access the AWS Glue connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integrationresourceproperty-sourceprocessingproperties.html#cfn-glue-integrationresourceproperty-sourceprocessingproperties-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProcessingPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnIntegrationResourcePropertyPropsMixin.TargetProcessingPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_name": "connectionName",
            "event_bus_arn": "eventBusArn",
            "kms_arn": "kmsArn",
            "role_arn": "roleArn",
        },
    )
    class TargetProcessingPropertiesProperty:
        def __init__(
            self,
            *,
            connection_name: typing.Optional[builtins.str] = None,
            event_bus_arn: typing.Optional[builtins.str] = None,
            kms_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The structure used to define the resource properties associated with the integration target.

            :param connection_name: The AWS Glue network connection to configure the AWS Glue job running in the customer VPC.
            :param event_bus_arn: The ARN of an Eventbridge event bus to receive the integration status notification.
            :param kms_arn: The ARN of the KMS key used for encryption.
            :param role_arn: The IAM role to access the AWS Glue database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integrationresourceproperty-targetprocessingproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                target_processing_properties_property = glue_mixins.CfnIntegrationResourcePropertyPropsMixin.TargetProcessingPropertiesProperty(
                    connection_name="connectionName",
                    event_bus_arn="eventBusArn",
                    kms_arn="kmsArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__473649f5a749dc1cfac70aa72d1982be410b1178fd3bacf994a21613122fb73e)
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument event_bus_arn", value=event_bus_arn, expected_type=type_hints["event_bus_arn"])
                check_type(argname="argument kms_arn", value=kms_arn, expected_type=type_hints["kms_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if event_bus_arn is not None:
                self._values["event_bus_arn"] = event_bus_arn
            if kms_arn is not None:
                self._values["kms_arn"] = kms_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Glue network connection to configure the AWS Glue job running in the customer VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integrationresourceproperty-targetprocessingproperties.html#cfn-glue-integrationresourceproperty-targetprocessingproperties-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_bus_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an Eventbridge event bus to receive the integration status notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integrationresourceproperty-targetprocessingproperties.html#cfn-glue-integrationresourceproperty-targetprocessingproperties-eventbusarn
            '''
            result = self._values.get("event_bus_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the KMS key used for encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integrationresourceproperty-targetprocessingproperties.html#cfn-glue-integrationresourceproperty-targetprocessingproperties-kmsarn
            '''
            result = self._values.get("kms_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The IAM role to access the AWS Glue database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-integrationresourceproperty-targetprocessingproperties.html#cfn-glue-integrationresourceproperty-targetprocessingproperties-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProcessingPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnJobMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allocated_capacity": "allocatedCapacity",
        "command": "command",
        "connections": "connections",
        "default_arguments": "defaultArguments",
        "description": "description",
        "execution_class": "executionClass",
        "execution_property": "executionProperty",
        "glue_version": "glueVersion",
        "job_mode": "jobMode",
        "job_run_queuing_enabled": "jobRunQueuingEnabled",
        "log_uri": "logUri",
        "maintenance_window": "maintenanceWindow",
        "max_capacity": "maxCapacity",
        "max_retries": "maxRetries",
        "name": "name",
        "non_overridable_arguments": "nonOverridableArguments",
        "notification_property": "notificationProperty",
        "number_of_workers": "numberOfWorkers",
        "role": "role",
        "security_configuration": "securityConfiguration",
        "tags": "tags",
        "timeout": "timeout",
        "worker_type": "workerType",
    },
)
class CfnJobMixinProps:
    def __init__(
        self,
        *,
        allocated_capacity: typing.Optional[jsii.Number] = None,
        command: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.JobCommandProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connections: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.ConnectionsListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_arguments: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        execution_class: typing.Optional[builtins.str] = None,
        execution_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.ExecutionPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        glue_version: typing.Optional[builtins.str] = None,
        job_mode: typing.Optional[builtins.str] = None,
        job_run_queuing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        log_uri: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        non_overridable_arguments: typing.Any = None,
        notification_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.NotificationPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        number_of_workers: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        timeout: typing.Optional[jsii.Number] = None,
        worker_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnJobPropsMixin.

        :param allocated_capacity: This parameter is no longer supported. Use ``MaxCapacity`` instead. The number of capacity units that are allocated to this job.
        :param command: The code that executes a job.
        :param connections: The connections used for this job.
        :param default_arguments: The default arguments for this job, specified as name-value pairs. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes. For information about how to specify and consume your own job arguments, see `Calling AWS Glue APIs in Python <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html>`_ in the *AWS Glue Developer Guide* . For information about the key-value pairs that AWS Glue consumes to set up your job, see `Special Parameters Used by AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html>`_ in the *AWS Glue Developer Guide* .
        :param description: A description of the job.
        :param execution_class: Indicates whether the job is run with a standard or flexible execution class. The standard execution class is ideal for time-sensitive workloads that require fast job startup and dedicated resources. The flexible execution class is appropriate for time-insensitive jobs whose start and completion times may vary. Only jobs with AWS Glue version 3.0 and above and command type ``glueetl`` will be allowed to set ``ExecutionClass`` to ``FLEX`` . The flexible execution class is available for Spark jobs.
        :param execution_property: The maximum number of concurrent runs that are allowed for this job.
        :param glue_version: Glue version determines the versions of Apache Spark and Python that AWS Glue supports. The Python version indicates the version supported for jobs of type Spark. For more information about the available AWS Glue versions and corresponding Spark and Python versions, see `Glue version <https://docs.aws.amazon.com/glue/latest/dg/add-job.html>`_ in the developer guide. Jobs that are created without specifying a Glue version default to the latest Glue version available.
        :param job_mode: A mode that describes how a job was created. Valid values are:. - ``SCRIPT`` - The job was created using the AWS Glue Studio script editor. - ``VISUAL`` - The job was created using the AWS Glue Studio visual editor. - ``NOTEBOOK`` - The job was created using an interactive sessions notebook. When the ``JobMode`` field is missing or null, ``SCRIPT`` is assigned as the default value.
        :param job_run_queuing_enabled: Specifies whether job run queuing is enabled for the job runs for this job. A value of true means job run queuing is enabled for the job runs. If false or not populated, the job runs will not be considered for queueing. If this field does not match the value set in the job run, then the value from the job run field will be used.
        :param log_uri: This field is reserved for future use.
        :param maintenance_window: This field specifies a day of the week and hour for a maintenance window for streaming jobs. AWS Glue periodically performs maintenance activities. During these maintenance windows, AWS Glue will need to restart your streaming jobs. AWS Glue will restart the job within 3 hours of the specified maintenance window. For instance, if you set up the maintenance window for Monday at 10:00AM GMT, your jobs will be restarted between 10:00AM GMT to 1:00PM GMT.
        :param max_capacity: The number of AWS Glue data processing units (DPUs) that can be allocated when this job runs. A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory. Do not set ``Max Capacity`` if using ``WorkerType`` and ``NumberOfWorkers`` . The value that can be allocated for ``MaxCapacity`` depends on whether you are running a Python shell job or an Apache Spark ETL job: - When you specify a Python shell job ( ``JobCommand.Name`` ="pythonshell"), you can allocate either 0.0625 or 1 DPU. The default is 0.0625 DPU. - When you specify an Apache Spark ETL job ( ``JobCommand.Name`` ="glueetl"), you can allocate from 2 to 100 DPUs. The default is 10 DPUs. This job type cannot have a fractional DPU allocation.
        :param max_retries: The maximum number of times to retry this job after a JobRun fails.
        :param name: The name you assign to this job definition.
        :param non_overridable_arguments: Non-overridable arguments for this job, specified as name-value pairs.
        :param notification_property: Specifies configuration properties of a notification.
        :param number_of_workers: The number of workers of a defined ``workerType`` that are allocated when a job runs. The maximum number of workers you can define are 299 for ``G.1X`` , and 149 for ``G.2X`` .
        :param role: The name or Amazon Resource Name (ARN) of the IAM role associated with this job.
        :param security_configuration: The name of the ``SecurityConfiguration`` structure to be used with this job.
        :param tags: The tags to use with this job.
        :param timeout: The job timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 2,880 minutes (48 hours).
        :param worker_type: The type of predefined worker that is allocated when a job runs. AWS Glue provides multiple worker types to accommodate different workload requirements: G Worker Types (General-purpose compute workers): - G.1X: 1 DPU (4 vCPUs, 16 GB memory, 94GB disk) - G.2X: 2 DPU (8 vCPUs, 32 GB memory, 138GB disk) - G.4X: 4 DPU (16 vCPUs, 64 GB memory, 256GB disk) - G.8X: 8 DPU (32 vCPUs, 128 GB memory, 512GB disk) - G.12X: 12 DPU (48 vCPUs, 192 GB memory, 768GB disk) - G.16X: 16 DPU (64 vCPUs, 256 GB memory, 1024GB disk) R Worker Types (Memory-optimized workers): - R.1X: 1 M-DPU (4 vCPUs, 32 GB memory) - R.2X: 2 M-DPU (8 vCPUs, 64 GB memory) - R.4X: 4 M-DPU (16 vCPUs, 128 GB memory) - R.8X: 8 M-DPU (32 vCPUs, 256 GB memory)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # default_arguments: Any
            # non_overridable_arguments: Any
            # tags: Any
            
            cfn_job_mixin_props = glue_mixins.CfnJobMixinProps(
                allocated_capacity=123,
                command=glue_mixins.CfnJobPropsMixin.JobCommandProperty(
                    name="name",
                    python_version="pythonVersion",
                    runtime="runtime",
                    script_location="scriptLocation"
                ),
                connections=glue_mixins.CfnJobPropsMixin.ConnectionsListProperty(
                    connections=["connections"]
                ),
                default_arguments=default_arguments,
                description="description",
                execution_class="executionClass",
                execution_property=glue_mixins.CfnJobPropsMixin.ExecutionPropertyProperty(
                    max_concurrent_runs=123
                ),
                glue_version="glueVersion",
                job_mode="jobMode",
                job_run_queuing_enabled=False,
                log_uri="logUri",
                maintenance_window="maintenanceWindow",
                max_capacity=123,
                max_retries=123,
                name="name",
                non_overridable_arguments=non_overridable_arguments,
                notification_property=glue_mixins.CfnJobPropsMixin.NotificationPropertyProperty(
                    notify_delay_after=123
                ),
                number_of_workers=123,
                role="role",
                security_configuration="securityConfiguration",
                tags=tags,
                timeout=123,
                worker_type="workerType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe9ae06ff341e847993c18451a0bb9406108776440cca0e2e575ffa668512ca)
            check_type(argname="argument allocated_capacity", value=allocated_capacity, expected_type=type_hints["allocated_capacity"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
            check_type(argname="argument default_arguments", value=default_arguments, expected_type=type_hints["default_arguments"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument execution_class", value=execution_class, expected_type=type_hints["execution_class"])
            check_type(argname="argument execution_property", value=execution_property, expected_type=type_hints["execution_property"])
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument job_mode", value=job_mode, expected_type=type_hints["job_mode"])
            check_type(argname="argument job_run_queuing_enabled", value=job_run_queuing_enabled, expected_type=type_hints["job_run_queuing_enabled"])
            check_type(argname="argument log_uri", value=log_uri, expected_type=type_hints["log_uri"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument non_overridable_arguments", value=non_overridable_arguments, expected_type=type_hints["non_overridable_arguments"])
            check_type(argname="argument notification_property", value=notification_property, expected_type=type_hints["notification_property"])
            check_type(argname="argument number_of_workers", value=number_of_workers, expected_type=type_hints["number_of_workers"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allocated_capacity is not None:
            self._values["allocated_capacity"] = allocated_capacity
        if command is not None:
            self._values["command"] = command
        if connections is not None:
            self._values["connections"] = connections
        if default_arguments is not None:
            self._values["default_arguments"] = default_arguments
        if description is not None:
            self._values["description"] = description
        if execution_class is not None:
            self._values["execution_class"] = execution_class
        if execution_property is not None:
            self._values["execution_property"] = execution_property
        if glue_version is not None:
            self._values["glue_version"] = glue_version
        if job_mode is not None:
            self._values["job_mode"] = job_mode
        if job_run_queuing_enabled is not None:
            self._values["job_run_queuing_enabled"] = job_run_queuing_enabled
        if log_uri is not None:
            self._values["log_uri"] = log_uri
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if name is not None:
            self._values["name"] = name
        if non_overridable_arguments is not None:
            self._values["non_overridable_arguments"] = non_overridable_arguments
        if notification_property is not None:
            self._values["notification_property"] = notification_property
        if number_of_workers is not None:
            self._values["number_of_workers"] = number_of_workers
        if role is not None:
            self._values["role"] = role
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if worker_type is not None:
            self._values["worker_type"] = worker_type

    @builtins.property
    def allocated_capacity(self) -> typing.Optional[jsii.Number]:
        '''This parameter is no longer supported. Use ``MaxCapacity`` instead.

        The number of capacity units that are allocated to this job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-allocatedcapacity
        '''
        result = self._values.get("allocated_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def command(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.JobCommandProperty"]]:
        '''The code that executes a job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-command
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.JobCommandProperty"]], result)

    @builtins.property
    def connections(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ConnectionsListProperty"]]:
        '''The connections used for this job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-connections
        '''
        result = self._values.get("connections")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ConnectionsListProperty"]], result)

    @builtins.property
    def default_arguments(self) -> typing.Any:
        '''The default arguments for this job, specified as name-value pairs.

        You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.

        For information about how to specify and consume your own job arguments, see `Calling AWS Glue APIs in Python <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html>`_ in the *AWS Glue Developer Guide* .

        For information about the key-value pairs that AWS Glue consumes to set up your job, see `Special Parameters Used by AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html>`_ in the *AWS Glue Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-defaultarguments
        '''
        result = self._values.get("default_arguments")
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_class(self) -> typing.Optional[builtins.str]:
        '''Indicates whether the job is run with a standard or flexible execution class.

        The standard execution class is ideal for time-sensitive workloads that require fast job startup and dedicated resources.

        The flexible execution class is appropriate for time-insensitive jobs whose start and completion times may vary.

        Only jobs with AWS Glue version 3.0 and above and command type ``glueetl`` will be allowed to set ``ExecutionClass`` to ``FLEX`` . The flexible execution class is available for Spark jobs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-executionclass
        '''
        result = self._values.get("execution_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_property(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ExecutionPropertyProperty"]]:
        '''The maximum number of concurrent runs that are allowed for this job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-executionproperty
        '''
        result = self._values.get("execution_property")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ExecutionPropertyProperty"]], result)

    @builtins.property
    def glue_version(self) -> typing.Optional[builtins.str]:
        '''Glue version determines the versions of Apache Spark and Python that AWS Glue supports.

        The Python version indicates the version supported for jobs of type Spark.

        For more information about the available AWS Glue versions and corresponding Spark and Python versions, see `Glue version <https://docs.aws.amazon.com/glue/latest/dg/add-job.html>`_ in the developer guide.

        Jobs that are created without specifying a Glue version default to the latest Glue version available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-glueversion
        '''
        result = self._values.get("glue_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_mode(self) -> typing.Optional[builtins.str]:
        '''A mode that describes how a job was created. Valid values are:.

        - ``SCRIPT`` - The job was created using the AWS Glue Studio script editor.
        - ``VISUAL`` - The job was created using the AWS Glue Studio visual editor.
        - ``NOTEBOOK`` - The job was created using an interactive sessions notebook.

        When the ``JobMode`` field is missing or null, ``SCRIPT`` is assigned as the default value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-jobmode
        '''
        result = self._values.get("job_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_run_queuing_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether job run queuing is enabled for the job runs for this job.

        A value of true means job run queuing is enabled for the job runs. If false or not populated, the job runs will not be considered for queueing.

        If this field does not match the value set in the job run, then the value from the job run field will be used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-jobrunqueuingenabled
        '''
        result = self._values.get("job_run_queuing_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def log_uri(self) -> typing.Optional[builtins.str]:
        '''This field is reserved for future use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-loguri
        '''
        result = self._values.get("log_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(self) -> typing.Optional[builtins.str]:
        '''This field specifies a day of the week and hour for a maintenance window for streaming jobs.

        AWS Glue periodically performs maintenance activities. During these maintenance windows, AWS Glue will need to restart your streaming jobs.

        AWS Glue will restart the job within 3 hours of the specified maintenance window. For instance, if you set up the maintenance window for Monday at 10:00AM GMT, your jobs will be restarted between 10:00AM GMT to 1:00PM GMT.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-maintenancewindow
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''The number of AWS Glue data processing units (DPUs) that can be allocated when this job runs.

        A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory.

        Do not set ``Max Capacity`` if using ``WorkerType`` and ``NumberOfWorkers`` .

        The value that can be allocated for ``MaxCapacity`` depends on whether you are running a Python shell job or an Apache Spark ETL job:

        - When you specify a Python shell job ( ``JobCommand.Name`` ="pythonshell"), you can allocate either 0.0625 or 1 DPU. The default is 0.0625 DPU.
        - When you specify an Apache Spark ETL job ( ``JobCommand.Name`` ="glueetl"), you can allocate from 2 to 100 DPUs. The default is 10 DPUs. This job type cannot have a fractional DPU allocation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-maxcapacity
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry this job after a JobRun fails.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-maxretries
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name you assign to this job definition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def non_overridable_arguments(self) -> typing.Any:
        '''Non-overridable arguments for this job, specified as name-value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-nonoverridablearguments
        '''
        result = self._values.get("non_overridable_arguments")
        return typing.cast(typing.Any, result)

    @builtins.property
    def notification_property(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.NotificationPropertyProperty"]]:
        '''Specifies configuration properties of a notification.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-notificationproperty
        '''
        result = self._values.get("notification_property")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.NotificationPropertyProperty"]], result)

    @builtins.property
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        '''The number of workers of a defined ``workerType`` that are allocated when a job runs.

        The maximum number of workers you can define are 299 for ``G.1X`` , and 149 for ``G.2X`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-numberofworkers
        '''
        result = self._values.get("number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''The name or Amazon Resource Name (ARN) of the IAM role associated with this job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''The name of the ``SecurityConfiguration`` structure to be used with this job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-securityconfiguration
        '''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags to use with this job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''The job timeout in minutes.

        This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 2,880 minutes (48 hours).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def worker_type(self) -> typing.Optional[builtins.str]:
        '''The type of predefined worker that is allocated when a job runs.

        AWS Glue provides multiple worker types to accommodate different workload requirements:

        G Worker Types (General-purpose compute workers):

        - G.1X: 1 DPU (4 vCPUs, 16 GB memory, 94GB disk)
        - G.2X: 2 DPU (8 vCPUs, 32 GB memory, 138GB disk)
        - G.4X: 4 DPU (16 vCPUs, 64 GB memory, 256GB disk)
        - G.8X: 8 DPU (32 vCPUs, 128 GB memory, 512GB disk)
        - G.12X: 12 DPU (48 vCPUs, 192 GB memory, 768GB disk)
        - G.16X: 16 DPU (64 vCPUs, 256 GB memory, 1024GB disk)

        R Worker Types (Memory-optimized workers):

        - R.1X: 1 M-DPU (4 vCPUs, 32 GB memory)
        - R.2X: 2 M-DPU (8 vCPUs, 64 GB memory)
        - R.4X: 4 M-DPU (16 vCPUs, 128 GB memory)
        - R.8X: 8 M-DPU (32 vCPUs, 256 GB memory)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-workertype
        '''
        result = self._values.get("worker_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnJobPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnJobPropsMixin",
):
    '''The ``AWS::Glue::Job`` resource specifies an AWS Glue job in the data catalog.

    For more information, see `Adding Jobs in AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/add-job.html>`_ and `Job Structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-job.html#aws-glue-api-jobs-job-Job>`_ in the *AWS Glue Developer Guide.*

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html
    :cloudformationResource: AWS::Glue::Job
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # default_arguments: Any
        # non_overridable_arguments: Any
        # tags: Any
        
        cfn_job_props_mixin = glue_mixins.CfnJobPropsMixin(glue_mixins.CfnJobMixinProps(
            allocated_capacity=123,
            command=glue_mixins.CfnJobPropsMixin.JobCommandProperty(
                name="name",
                python_version="pythonVersion",
                runtime="runtime",
                script_location="scriptLocation"
            ),
            connections=glue_mixins.CfnJobPropsMixin.ConnectionsListProperty(
                connections=["connections"]
            ),
            default_arguments=default_arguments,
            description="description",
            execution_class="executionClass",
            execution_property=glue_mixins.CfnJobPropsMixin.ExecutionPropertyProperty(
                max_concurrent_runs=123
            ),
            glue_version="glueVersion",
            job_mode="jobMode",
            job_run_queuing_enabled=False,
            log_uri="logUri",
            maintenance_window="maintenanceWindow",
            max_capacity=123,
            max_retries=123,
            name="name",
            non_overridable_arguments=non_overridable_arguments,
            notification_property=glue_mixins.CfnJobPropsMixin.NotificationPropertyProperty(
                notify_delay_after=123
            ),
            number_of_workers=123,
            role="role",
            security_configuration="securityConfiguration",
            tags=tags,
            timeout=123,
            worker_type="workerType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnJobMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Job``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29297e18e4aefa300afe4ff2b3e557afdd856dfeb8aebf93f52a03f823a57362)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62f1675580dddcacb2166f0ff35918b82d0b49f2fc11da1d8842c9e27a5409c9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9da3fd8ec306564346b5fbe47c9d53273a472ec404c3421e8b462207d68d6be)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnJobMixinProps:
        return typing.cast(CfnJobMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnJobPropsMixin.ConnectionsListProperty",
        jsii_struct_bases=[],
        name_mapping={"connections": "connections"},
    )
    class ConnectionsListProperty:
        def __init__(
            self,
            *,
            connections: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the connections used by a job.

            :param connections: A list of connections used by the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-connectionslist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                connections_list_property = glue_mixins.CfnJobPropsMixin.ConnectionsListProperty(
                    connections=["connections"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__395dc2b2ad124d4a43dd74ea0f55ae6ca12a84351956b30666dd0e6d6375699b)
                check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connections is not None:
                self._values["connections"] = connections

        @builtins.property
        def connections(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of connections used by the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-connectionslist.html#cfn-glue-job-connectionslist-connections
            '''
            result = self._values.get("connections")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionsListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnJobPropsMixin.ExecutionPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"max_concurrent_runs": "maxConcurrentRuns"},
    )
    class ExecutionPropertyProperty:
        def __init__(
            self,
            *,
            max_concurrent_runs: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An execution property of a job.

            :param max_concurrent_runs: The maximum number of concurrent runs allowed for the job. The default is 1. An error is returned when this threshold is reached. The maximum value you can specify is controlled by a service limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-executionproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                execution_property_property = glue_mixins.CfnJobPropsMixin.ExecutionPropertyProperty(
                    max_concurrent_runs=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da955de9a09ecc9d5643d38077b165b9a318368aa4e9ef467df78292c68993b3)
                check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_concurrent_runs is not None:
                self._values["max_concurrent_runs"] = max_concurrent_runs

        @builtins.property
        def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of concurrent runs allowed for the job.

            The default is 1. An error is returned when this threshold is reached. The maximum value you can specify is controlled by a service limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-executionproperty.html#cfn-glue-job-executionproperty-maxconcurrentruns
            '''
            result = self._values.get("max_concurrent_runs")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnJobPropsMixin.JobCommandProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "python_version": "pythonVersion",
            "runtime": "runtime",
            "script_location": "scriptLocation",
        },
    )
    class JobCommandProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            python_version: typing.Optional[builtins.str] = None,
            runtime: typing.Optional[builtins.str] = None,
            script_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies code executed when a job is run.

            :param name: The name of the job command. For an Apache Spark ETL job, this must be ``glueetl`` . For a Python shell job, it must be ``pythonshell`` . For an Apache Spark streaming ETL job, this must be ``gluestreaming`` . For a Ray job, this must be ``glueray`` .
            :param python_version: The Python version being used to execute a Python shell job. Allowed values are 3 or 3.9. Version 2 is deprecated.
            :param runtime: In Ray jobs, Runtime is used to specify the versions of Ray, Python and additional libraries available in your environment. This field is not used in other job types. For supported runtime environment values, see `Working with Ray jobs <https://docs.aws.amazon.com/glue/latest/dg/ray-jobs-section.html>`_ in the AWS Glue Developer Guide.
            :param script_location: Specifies the Amazon Simple Storage Service (Amazon S3) path to a script that executes a job (required).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                job_command_property = glue_mixins.CfnJobPropsMixin.JobCommandProperty(
                    name="name",
                    python_version="pythonVersion",
                    runtime="runtime",
                    script_location="scriptLocation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d85eab79a04899ff3a613c6458b861e0081aace08b581ed9bbd7c9a801bd634)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
                check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
                check_type(argname="argument script_location", value=script_location, expected_type=type_hints["script_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if python_version is not None:
                self._values["python_version"] = python_version
            if runtime is not None:
                self._values["runtime"] = runtime
            if script_location is not None:
                self._values["script_location"] = script_location

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the job command.

            For an Apache Spark ETL job, this must be ``glueetl`` . For a Python shell job, it must be ``pythonshell`` . For an Apache Spark streaming ETL job, this must be ``gluestreaming`` . For a Ray job, this must be ``glueray`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html#cfn-glue-job-jobcommand-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def python_version(self) -> typing.Optional[builtins.str]:
            '''The Python version being used to execute a Python shell job.

            Allowed values are 3 or 3.9. Version 2 is deprecated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html#cfn-glue-job-jobcommand-pythonversion
            '''
            result = self._values.get("python_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def runtime(self) -> typing.Optional[builtins.str]:
            '''In Ray jobs, Runtime is used to specify the versions of Ray, Python and additional libraries available in your environment.

            This field is not used in other job types. For supported runtime environment values, see `Working with Ray jobs <https://docs.aws.amazon.com/glue/latest/dg/ray-jobs-section.html>`_ in the AWS Glue Developer Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html#cfn-glue-job-jobcommand-runtime
            '''
            result = self._values.get("runtime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def script_location(self) -> typing.Optional[builtins.str]:
            '''Specifies the Amazon Simple Storage Service (Amazon S3) path to a script that executes a job (required).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html#cfn-glue-job-jobcommand-scriptlocation
            '''
            result = self._values.get("script_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobCommandProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnJobPropsMixin.NotificationPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"notify_delay_after": "notifyDelayAfter"},
    )
    class NotificationPropertyProperty:
        def __init__(
            self,
            *,
            notify_delay_after: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies configuration properties of a notification.

            :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-notificationproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                notification_property_property = glue_mixins.CfnJobPropsMixin.NotificationPropertyProperty(
                    notify_delay_after=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0cfde3549b63b075fb2d854b35978d301bd4d13667b0d500a9d504fcce52f73)
                check_type(argname="argument notify_delay_after", value=notify_delay_after, expected_type=type_hints["notify_delay_after"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if notify_delay_after is not None:
                self._values["notify_delay_after"] = notify_delay_after

        @builtins.property
        def notify_delay_after(self) -> typing.Optional[jsii.Number]:
            '''After a job run starts, the number of minutes to wait before sending a job run delay notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-notificationproperty.html#cfn-glue-job-notificationproperty-notifydelayafter
            '''
            result = self._values.get("notify_delay_after")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnMLTransformMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "glue_version": "glueVersion",
        "input_record_tables": "inputRecordTables",
        "max_capacity": "maxCapacity",
        "max_retries": "maxRetries",
        "name": "name",
        "number_of_workers": "numberOfWorkers",
        "role": "role",
        "tags": "tags",
        "timeout": "timeout",
        "transform_encryption": "transformEncryption",
        "transform_parameters": "transformParameters",
        "worker_type": "workerType",
    },
)
class CfnMLTransformMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        glue_version: typing.Optional[builtins.str] = None,
        input_record_tables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMLTransformPropsMixin.InputRecordTablesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        number_of_workers: typing.Optional[jsii.Number] = None,
        role: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
        timeout: typing.Optional[jsii.Number] = None,
        transform_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMLTransformPropsMixin.TransformEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        transform_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMLTransformPropsMixin.TransformParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        worker_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMLTransformPropsMixin.

        :param description: A user-defined, long-form description text for the machine learning transform.
        :param glue_version: This value determines which version of AWS Glue this machine learning transform is compatible with. Glue 1.0 is recommended for most customers. If the value is not set, the Glue compatibility defaults to Glue 0.9. For more information, see `AWS Glue Versions <https://docs.aws.amazon.com/glue/latest/dg/release-notes.html#release-notes-versions>`_ in the developer guide.
        :param input_record_tables: A list of AWS Glue table definitions used by the transform.
        :param max_capacity: The number of AWS Glue data processing units (DPUs) that are allocated to task runs for this transform. You can allocate from 2 to 100 DPUs; the default is 10. A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory. For more information, see the `AWS Glue pricing page <https://docs.aws.amazon.com/glue/pricing/>`_ . ``MaxCapacity`` is a mutually exclusive option with ``NumberOfWorkers`` and ``WorkerType`` . - If either ``NumberOfWorkers`` or ``WorkerType`` is set, then ``MaxCapacity`` cannot be set. - If ``MaxCapacity`` is set then neither ``NumberOfWorkers`` or ``WorkerType`` can be set. - If ``WorkerType`` is set, then ``NumberOfWorkers`` is required (and vice versa). - ``MaxCapacity`` and ``NumberOfWorkers`` must both be at least 1. When the ``WorkerType`` field is set to a value other than ``Standard`` , the ``MaxCapacity`` field is set automatically and becomes read-only.
        :param max_retries: The maximum number of times to retry after an ``MLTaskRun`` of the machine learning transform fails.
        :param name: A user-defined name for the machine learning transform. Names are required to be unique. ``Name`` is optional:. - If you supply ``Name`` , the stack cannot be repeatedly created. - If ``Name`` is not provided, a randomly generated name will be used instead.
        :param number_of_workers: The number of workers of a defined ``workerType`` that are allocated when a task of the transform runs. If ``WorkerType`` is set, then ``NumberOfWorkers`` is required (and vice versa).
        :param role: The name or Amazon Resource Name (ARN) of the IAM role with the required permissions. The required permissions include both AWS Glue service role permissions to AWS Glue resources, and Amazon S3 permissions required by the transform. - This role needs AWS Glue service role permissions to allow access to resources in AWS Glue . See `Attach a Policy to IAM Users That Access AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/attach-policy-iam-user.html>`_ . - This role needs permission to your Amazon Simple Storage Service (Amazon S3) sources, targets, temporary directory, scripts, and any libraries used by the task run for this transform.
        :param tags: The tags to use with this machine learning transform. You may use tags to limit access to the machine learning transform. For more information about tags in AWS Glue , see `AWS Tags in AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/monitor-tags.html>`_ in the developer guide.
        :param timeout: The timeout in minutes of the machine learning transform.
        :param transform_encryption: The encryption-at-rest settings of the transform that apply to accessing user data. Machine learning transforms can access user data encrypted in Amazon S3 using KMS. Additionally, imported labels and trained transforms can now be encrypted using a customer provided KMS key.
        :param transform_parameters: The algorithm-specific parameters that are associated with the machine learning transform.
        :param worker_type: The type of predefined worker that is allocated when a task of this transform runs. Accepts a value of Standard, G.1X, or G.2X. - For the ``Standard`` worker type, each worker provides 4 vCPU, 16 GB of memory and a 50GB disk, and 2 executors per worker. - For the ``G.1X`` worker type, each worker provides 4 vCPU, 16 GB of memory and a 64GB disk, and 1 executor per worker. - For the ``G.2X`` worker type, each worker provides 8 vCPU, 32 GB of memory and a 128GB disk, and 1 executor per worker. ``MaxCapacity`` is a mutually exclusive option with ``NumberOfWorkers`` and ``WorkerType`` . - If either ``NumberOfWorkers`` or ``WorkerType`` is set, then ``MaxCapacity`` cannot be set. - If ``MaxCapacity`` is set then neither ``NumberOfWorkers`` or ``WorkerType`` can be set. - If ``WorkerType`` is set, then ``NumberOfWorkers`` is required (and vice versa). - ``MaxCapacity`` and ``NumberOfWorkers`` must both be at least 1.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # tags: Any
            
            cfn_mLTransform_mixin_props = glue_mixins.CfnMLTransformMixinProps(
                description="description",
                glue_version="glueVersion",
                input_record_tables=glue_mixins.CfnMLTransformPropsMixin.InputRecordTablesProperty(
                    glue_tables=[glue_mixins.CfnMLTransformPropsMixin.GlueTablesProperty(
                        catalog_id="catalogId",
                        connection_name="connectionName",
                        database_name="databaseName",
                        table_name="tableName"
                    )]
                ),
                max_capacity=123,
                max_retries=123,
                name="name",
                number_of_workers=123,
                role="role",
                tags=tags,
                timeout=123,
                transform_encryption=glue_mixins.CfnMLTransformPropsMixin.TransformEncryptionProperty(
                    ml_user_data_encryption=glue_mixins.CfnMLTransformPropsMixin.MLUserDataEncryptionProperty(
                        kms_key_id="kmsKeyId",
                        ml_user_data_encryption_mode="mlUserDataEncryptionMode"
                    ),
                    task_run_security_configuration_name="taskRunSecurityConfigurationName"
                ),
                transform_parameters=glue_mixins.CfnMLTransformPropsMixin.TransformParametersProperty(
                    find_matches_parameters=glue_mixins.CfnMLTransformPropsMixin.FindMatchesParametersProperty(
                        accuracy_cost_tradeoff=123,
                        enforce_provided_labels=False,
                        precision_recall_tradeoff=123,
                        primary_key_column_name="primaryKeyColumnName"
                    ),
                    transform_type="transformType"
                ),
                worker_type="workerType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35add2331241a754e7b44ce1d989ca1ad8e71b67690fb07e2855c37dffb5575d)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument input_record_tables", value=input_record_tables, expected_type=type_hints["input_record_tables"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument number_of_workers", value=number_of_workers, expected_type=type_hints["number_of_workers"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument transform_encryption", value=transform_encryption, expected_type=type_hints["transform_encryption"])
            check_type(argname="argument transform_parameters", value=transform_parameters, expected_type=type_hints["transform_parameters"])
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if glue_version is not None:
            self._values["glue_version"] = glue_version
        if input_record_tables is not None:
            self._values["input_record_tables"] = input_record_tables
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if name is not None:
            self._values["name"] = name
        if number_of_workers is not None:
            self._values["number_of_workers"] = number_of_workers
        if role is not None:
            self._values["role"] = role
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if transform_encryption is not None:
            self._values["transform_encryption"] = transform_encryption
        if transform_parameters is not None:
            self._values["transform_parameters"] = transform_parameters
        if worker_type is not None:
            self._values["worker_type"] = worker_type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A user-defined, long-form description text for the machine learning transform.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def glue_version(self) -> typing.Optional[builtins.str]:
        '''This value determines which version of AWS Glue this machine learning transform is compatible with.

        Glue 1.0 is recommended for most customers. If the value is not set, the Glue compatibility defaults to Glue 0.9. For more information, see `AWS Glue Versions <https://docs.aws.amazon.com/glue/latest/dg/release-notes.html#release-notes-versions>`_ in the developer guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-glueversion
        '''
        result = self._values.get("glue_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_record_tables(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.InputRecordTablesProperty"]]:
        '''A list of AWS Glue table definitions used by the transform.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-inputrecordtables
        '''
        result = self._values.get("input_record_tables")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.InputRecordTablesProperty"]], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''The number of AWS Glue data processing units (DPUs) that are allocated to task runs for this transform.

        You can allocate from 2 to 100 DPUs; the default is 10. A DPU is a relative measure of processing power that consists of 4 vCPUs of compute capacity and 16 GB of memory. For more information, see the `AWS Glue pricing page <https://docs.aws.amazon.com/glue/pricing/>`_ .

        ``MaxCapacity`` is a mutually exclusive option with ``NumberOfWorkers`` and ``WorkerType`` .

        - If either ``NumberOfWorkers`` or ``WorkerType`` is set, then ``MaxCapacity`` cannot be set.
        - If ``MaxCapacity`` is set then neither ``NumberOfWorkers`` or ``WorkerType`` can be set.
        - If ``WorkerType`` is set, then ``NumberOfWorkers`` is required (and vice versa).
        - ``MaxCapacity`` and ``NumberOfWorkers`` must both be at least 1.

        When the ``WorkerType`` field is set to a value other than ``Standard`` , the ``MaxCapacity`` field is set automatically and becomes read-only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-maxcapacity
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry after an ``MLTaskRun`` of the machine learning transform fails.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-maxretries
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A user-defined name for the machine learning transform. Names are required to be unique. ``Name`` is optional:.

        - If you supply ``Name`` , the stack cannot be repeatedly created.
        - If ``Name`` is not provided, a randomly generated name will be used instead.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        '''The number of workers of a defined ``workerType`` that are allocated when a task of the transform runs.

        If ``WorkerType`` is set, then ``NumberOfWorkers`` is required (and vice versa).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-numberofworkers
        '''
        result = self._values.get("number_of_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''The name or Amazon Resource Name (ARN) of the IAM role with the required permissions.

        The required permissions include both AWS Glue service role permissions to AWS Glue resources, and Amazon S3 permissions required by the transform.

        - This role needs AWS Glue service role permissions to allow access to resources in AWS Glue . See `Attach a Policy to IAM Users That Access AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/attach-policy-iam-user.html>`_ .
        - This role needs permission to your Amazon Simple Storage Service (Amazon S3) sources, targets, temporary directory, scripts, and any libraries used by the task run for this transform.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags to use with this machine learning transform.

        You may use tags to limit access to the machine learning transform. For more information about tags in AWS Glue , see `AWS Tags in AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/monitor-tags.html>`_ in the developer guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''The timeout in minutes of the machine learning transform.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def transform_encryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.TransformEncryptionProperty"]]:
        '''The encryption-at-rest settings of the transform that apply to accessing user data.

        Machine learning
        transforms can access user data encrypted in Amazon S3 using KMS.

        Additionally, imported labels and trained transforms can now be encrypted using a customer provided
        KMS key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-transformencryption
        '''
        result = self._values.get("transform_encryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.TransformEncryptionProperty"]], result)

    @builtins.property
    def transform_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.TransformParametersProperty"]]:
        '''The algorithm-specific parameters that are associated with the machine learning transform.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-transformparameters
        '''
        result = self._values.get("transform_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.TransformParametersProperty"]], result)

    @builtins.property
    def worker_type(self) -> typing.Optional[builtins.str]:
        '''The type of predefined worker that is allocated when a task of this transform runs.

        Accepts a value of Standard, G.1X, or G.2X.

        - For the ``Standard`` worker type, each worker provides 4 vCPU, 16 GB of memory and a 50GB disk, and 2 executors per worker.
        - For the ``G.1X`` worker type, each worker provides 4 vCPU, 16 GB of memory and a 64GB disk, and 1 executor per worker.
        - For the ``G.2X`` worker type, each worker provides 8 vCPU, 32 GB of memory and a 128GB disk, and 1 executor per worker.

        ``MaxCapacity`` is a mutually exclusive option with ``NumberOfWorkers`` and ``WorkerType`` .

        - If either ``NumberOfWorkers`` or ``WorkerType`` is set, then ``MaxCapacity`` cannot be set.
        - If ``MaxCapacity`` is set then neither ``NumberOfWorkers`` or ``WorkerType`` can be set.
        - If ``WorkerType`` is set, then ``NumberOfWorkers`` is required (and vice versa).
        - ``MaxCapacity`` and ``NumberOfWorkers`` must both be at least 1.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-workertype
        '''
        result = self._values.get("worker_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMLTransformMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMLTransformPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnMLTransformPropsMixin",
):
    '''The AWS::Glue::MLTransform is an AWS Glue resource type that manages machine learning transforms.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html
    :cloudformationResource: AWS::Glue::MLTransform
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # tags: Any
        
        cfn_mLTransform_props_mixin = glue_mixins.CfnMLTransformPropsMixin(glue_mixins.CfnMLTransformMixinProps(
            description="description",
            glue_version="glueVersion",
            input_record_tables=glue_mixins.CfnMLTransformPropsMixin.InputRecordTablesProperty(
                glue_tables=[glue_mixins.CfnMLTransformPropsMixin.GlueTablesProperty(
                    catalog_id="catalogId",
                    connection_name="connectionName",
                    database_name="databaseName",
                    table_name="tableName"
                )]
            ),
            max_capacity=123,
            max_retries=123,
            name="name",
            number_of_workers=123,
            role="role",
            tags=tags,
            timeout=123,
            transform_encryption=glue_mixins.CfnMLTransformPropsMixin.TransformEncryptionProperty(
                ml_user_data_encryption=glue_mixins.CfnMLTransformPropsMixin.MLUserDataEncryptionProperty(
                    kms_key_id="kmsKeyId",
                    ml_user_data_encryption_mode="mlUserDataEncryptionMode"
                ),
                task_run_security_configuration_name="taskRunSecurityConfigurationName"
            ),
            transform_parameters=glue_mixins.CfnMLTransformPropsMixin.TransformParametersProperty(
                find_matches_parameters=glue_mixins.CfnMLTransformPropsMixin.FindMatchesParametersProperty(
                    accuracy_cost_tradeoff=123,
                    enforce_provided_labels=False,
                    precision_recall_tradeoff=123,
                    primary_key_column_name="primaryKeyColumnName"
                ),
                transform_type="transformType"
            ),
            worker_type="workerType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMLTransformMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::MLTransform``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d8f4a4b391189662fe1c799d84a17dd239ff4f8592a05ce2fd75511acc1547)
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
            type_hints = typing.get_type_hints(_typecheckingstub__465fbe8a691611c80691a0a0881d36e989921c53b302d2b1be4edc65ba323b20)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ee07d3ccacf89ab1b6c2293c5de43eb22199ba0525bf119241f94d6fc8d6ff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMLTransformMixinProps:
        return typing.cast(CfnMLTransformMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnMLTransformPropsMixin.FindMatchesParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accuracy_cost_tradeoff": "accuracyCostTradeoff",
            "enforce_provided_labels": "enforceProvidedLabels",
            "precision_recall_tradeoff": "precisionRecallTradeoff",
            "primary_key_column_name": "primaryKeyColumnName",
        },
    )
    class FindMatchesParametersProperty:
        def __init__(
            self,
            *,
            accuracy_cost_tradeoff: typing.Optional[jsii.Number] = None,
            enforce_provided_labels: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            precision_recall_tradeoff: typing.Optional[jsii.Number] = None,
            primary_key_column_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The parameters to configure the find matches transform.

            :param accuracy_cost_tradeoff: The value that is selected when tuning your transform for a balance between accuracy and cost. A value of 0.5 means that the system balances accuracy and cost concerns. A value of 1.0 means a bias purely for accuracy, which typically results in a higher cost, sometimes substantially higher. A value of 0.0 means a bias purely for cost, which results in a less accurate ``FindMatches`` transform, sometimes with unacceptable accuracy. Accuracy measures how well the transform finds true positives and true negatives. Increasing accuracy requires more machine resources and cost. But it also results in increased recall. Cost measures how many compute resources, and thus money, are consumed to run the transform.
            :param enforce_provided_labels: The value to switch on or off to force the output to match the provided labels from users. If the value is ``True`` , the ``find matches`` transform forces the output to match the provided labels. The results override the normal conflation results. If the value is ``False`` , the ``find matches`` transform does not ensure all the labels provided are respected, and the results rely on the trained model. Note that setting this value to true may increase the conflation execution time.
            :param precision_recall_tradeoff: The value selected when tuning your transform for a balance between precision and recall. A value of 0.5 means no preference; a value of 1.0 means a bias purely for precision, and a value of 0.0 means a bias for recall. Because this is a tradeoff, choosing values close to 1.0 means very low recall, and choosing values close to 0.0 results in very low precision. The precision metric indicates how often your model is correct when it predicts a match. The recall metric indicates that for an actual match, how often your model predicts the match.
            :param primary_key_column_name: The name of a column that uniquely identifies rows in the source table. Used to help identify matching records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-findmatchesparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                find_matches_parameters_property = glue_mixins.CfnMLTransformPropsMixin.FindMatchesParametersProperty(
                    accuracy_cost_tradeoff=123,
                    enforce_provided_labels=False,
                    precision_recall_tradeoff=123,
                    primary_key_column_name="primaryKeyColumnName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e293d6131954f708651ae9535adf33e01d07aa6d28ad66b8e4b5a554aab63e74)
                check_type(argname="argument accuracy_cost_tradeoff", value=accuracy_cost_tradeoff, expected_type=type_hints["accuracy_cost_tradeoff"])
                check_type(argname="argument enforce_provided_labels", value=enforce_provided_labels, expected_type=type_hints["enforce_provided_labels"])
                check_type(argname="argument precision_recall_tradeoff", value=precision_recall_tradeoff, expected_type=type_hints["precision_recall_tradeoff"])
                check_type(argname="argument primary_key_column_name", value=primary_key_column_name, expected_type=type_hints["primary_key_column_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if accuracy_cost_tradeoff is not None:
                self._values["accuracy_cost_tradeoff"] = accuracy_cost_tradeoff
            if enforce_provided_labels is not None:
                self._values["enforce_provided_labels"] = enforce_provided_labels
            if precision_recall_tradeoff is not None:
                self._values["precision_recall_tradeoff"] = precision_recall_tradeoff
            if primary_key_column_name is not None:
                self._values["primary_key_column_name"] = primary_key_column_name

        @builtins.property
        def accuracy_cost_tradeoff(self) -> typing.Optional[jsii.Number]:
            '''The value that is selected when tuning your transform for a balance between accuracy and cost.

            A value of 0.5 means that the system balances accuracy and cost concerns. A value of 1.0 means a bias purely for accuracy, which typically results in a higher cost, sometimes substantially higher. A value of 0.0 means a bias purely for cost, which results in a less accurate ``FindMatches`` transform, sometimes with unacceptable accuracy.

            Accuracy measures how well the transform finds true positives and true negatives. Increasing accuracy requires more machine resources and cost. But it also results in increased recall.

            Cost measures how many compute resources, and thus money, are consumed to run the transform.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-findmatchesparameters.html#cfn-glue-mltransform-findmatchesparameters-accuracycosttradeoff
            '''
            result = self._values.get("accuracy_cost_tradeoff")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def enforce_provided_labels(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The value to switch on or off to force the output to match the provided labels from users.

            If the value is ``True`` , the ``find matches`` transform forces the output to match the provided labels. The results override the normal conflation results. If the value is ``False`` , the ``find matches`` transform does not ensure all the labels provided are respected, and the results rely on the trained model.

            Note that setting this value to true may increase the conflation execution time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-findmatchesparameters.html#cfn-glue-mltransform-findmatchesparameters-enforceprovidedlabels
            '''
            result = self._values.get("enforce_provided_labels")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def precision_recall_tradeoff(self) -> typing.Optional[jsii.Number]:
            '''The value selected when tuning your transform for a balance between precision and recall.

            A value of 0.5 means no preference; a value of 1.0 means a bias purely for precision, and a value of 0.0 means a bias for recall. Because this is a tradeoff, choosing values close to 1.0 means very low recall, and choosing values close to 0.0 results in very low precision.

            The precision metric indicates how often your model is correct when it predicts a match.

            The recall metric indicates that for an actual match, how often your model predicts the match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-findmatchesparameters.html#cfn-glue-mltransform-findmatchesparameters-precisionrecalltradeoff
            '''
            result = self._values.get("precision_recall_tradeoff")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def primary_key_column_name(self) -> typing.Optional[builtins.str]:
            '''The name of a column that uniquely identifies rows in the source table.

            Used to help identify matching records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-findmatchesparameters.html#cfn-glue-mltransform-findmatchesparameters-primarykeycolumnname
            '''
            result = self._values.get("primary_key_column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FindMatchesParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnMLTransformPropsMixin.GlueTablesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "connection_name": "connectionName",
            "database_name": "databaseName",
            "table_name": "tableName",
        },
    )
    class GlueTablesProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            connection_name: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The database and table in the AWS Glue Data Catalog that is used for input or output data.

            :param catalog_id: A unique identifier for the AWS Glue Data Catalog .
            :param connection_name: The name of the connection to the AWS Glue Data Catalog .
            :param database_name: A database name in the AWS Glue Data Catalog .
            :param table_name: A table name in the AWS Glue Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-gluetables.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                glue_tables_property = glue_mixins.CfnMLTransformPropsMixin.GlueTablesProperty(
                    catalog_id="catalogId",
                    connection_name="connectionName",
                    database_name="databaseName",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__68d2c7aa24d0274da00d1d7d0283977286aaac9c72bbd5d898fed016c554ae1a)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if connection_name is not None:
                self._values["connection_name"] = connection_name
            if database_name is not None:
                self._values["database_name"] = database_name
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for the AWS Glue Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-gluetables.html#cfn-glue-mltransform-gluetables-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the connection to the AWS Glue Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-gluetables.html#cfn-glue-mltransform-gluetables-connectionname
            '''
            result = self._values.get("connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''A database name in the AWS Glue Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-gluetables.html#cfn-glue-mltransform-gluetables-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''A table name in the AWS Glue Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-gluetables.html#cfn-glue-mltransform-gluetables-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueTablesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnMLTransformPropsMixin.InputRecordTablesProperty",
        jsii_struct_bases=[],
        name_mapping={"glue_tables": "glueTables"},
    )
    class InputRecordTablesProperty:
        def __init__(
            self,
            *,
            glue_tables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMLTransformPropsMixin.GlueTablesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A list of AWS Glue table definitions used by the transform.

            :param glue_tables: The database and table in the AWS Glue Data Catalog that is used for input or output data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-inputrecordtables.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                input_record_tables_property = glue_mixins.CfnMLTransformPropsMixin.InputRecordTablesProperty(
                    glue_tables=[glue_mixins.CfnMLTransformPropsMixin.GlueTablesProperty(
                        catalog_id="catalogId",
                        connection_name="connectionName",
                        database_name="databaseName",
                        table_name="tableName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__28b8a4e561babfdbe21bac693320f1f18dd07503d32e6e709356b1a695b1fbe9)
                check_type(argname="argument glue_tables", value=glue_tables, expected_type=type_hints["glue_tables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if glue_tables is not None:
                self._values["glue_tables"] = glue_tables

        @builtins.property
        def glue_tables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.GlueTablesProperty"]]]]:
            '''The database and table in the AWS Glue Data Catalog that is used for input or output data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-inputrecordtables.html#cfn-glue-mltransform-inputrecordtables-gluetables
            '''
            result = self._values.get("glue_tables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.GlueTablesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputRecordTablesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnMLTransformPropsMixin.MLUserDataEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_id": "kmsKeyId",
            "ml_user_data_encryption_mode": "mlUserDataEncryptionMode",
        },
    )
    class MLUserDataEncryptionProperty:
        def __init__(
            self,
            *,
            kms_key_id: typing.Optional[builtins.str] = None,
            ml_user_data_encryption_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The encryption-at-rest settings of the transform that apply to accessing user data.

            :param kms_key_id: The ID for the customer-provided KMS key.
            :param ml_user_data_encryption_mode: The encryption mode applied to user data. Valid values are:. - DISABLED: encryption is disabled. - SSEKMS: use of server-side encryption with AWS Key Management Service (SSE-KMS) for user data stored in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-mluserdataencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                m_lUser_data_encryption_property = glue_mixins.CfnMLTransformPropsMixin.MLUserDataEncryptionProperty(
                    kms_key_id="kmsKeyId",
                    ml_user_data_encryption_mode="mlUserDataEncryptionMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31799fd47b0062af14fdb1ee0a8315bc26382c7d0a546deb2b85d91d12be0213)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument ml_user_data_encryption_mode", value=ml_user_data_encryption_mode, expected_type=type_hints["ml_user_data_encryption_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if ml_user_data_encryption_mode is not None:
                self._values["ml_user_data_encryption_mode"] = ml_user_data_encryption_mode

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ID for the customer-provided KMS key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-mluserdataencryption.html#cfn-glue-mltransform-mluserdataencryption-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ml_user_data_encryption_mode(self) -> typing.Optional[builtins.str]:
            '''The encryption mode applied to user data. Valid values are:.

            - DISABLED: encryption is disabled.
            - SSEKMS: use of server-side encryption with AWS Key Management Service (SSE-KMS) for user data
              stored in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-mluserdataencryption.html#cfn-glue-mltransform-mluserdataencryption-mluserdataencryptionmode
            '''
            result = self._values.get("ml_user_data_encryption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MLUserDataEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnMLTransformPropsMixin.TransformEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ml_user_data_encryption": "mlUserDataEncryption",
            "task_run_security_configuration_name": "taskRunSecurityConfigurationName",
        },
    )
    class TransformEncryptionProperty:
        def __init__(
            self,
            *,
            ml_user_data_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMLTransformPropsMixin.MLUserDataEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            task_run_security_configuration_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The encryption-at-rest settings of the transform that apply to accessing user data.

            Machine learning
            transforms can access user data encrypted in Amazon S3 using KMS.

            Additionally, imported labels and trained transforms can now be encrypted using a customer provided
            KMS key.

            :param ml_user_data_encryption: The encryption-at-rest settings of the transform that apply to accessing user data.
            :param task_run_security_configuration_name: The name of the security configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                transform_encryption_property = glue_mixins.CfnMLTransformPropsMixin.TransformEncryptionProperty(
                    ml_user_data_encryption=glue_mixins.CfnMLTransformPropsMixin.MLUserDataEncryptionProperty(
                        kms_key_id="kmsKeyId",
                        ml_user_data_encryption_mode="mlUserDataEncryptionMode"
                    ),
                    task_run_security_configuration_name="taskRunSecurityConfigurationName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dcfaa88243c71bca5f1a4da5716da708f893533906b695cd7068da1e76fd372f)
                check_type(argname="argument ml_user_data_encryption", value=ml_user_data_encryption, expected_type=type_hints["ml_user_data_encryption"])
                check_type(argname="argument task_run_security_configuration_name", value=task_run_security_configuration_name, expected_type=type_hints["task_run_security_configuration_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ml_user_data_encryption is not None:
                self._values["ml_user_data_encryption"] = ml_user_data_encryption
            if task_run_security_configuration_name is not None:
                self._values["task_run_security_configuration_name"] = task_run_security_configuration_name

        @builtins.property
        def ml_user_data_encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.MLUserDataEncryptionProperty"]]:
            '''The encryption-at-rest settings of the transform that apply to accessing user data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformencryption.html#cfn-glue-mltransform-transformencryption-mluserdataencryption
            '''
            result = self._values.get("ml_user_data_encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.MLUserDataEncryptionProperty"]], result)

        @builtins.property
        def task_run_security_configuration_name(self) -> typing.Optional[builtins.str]:
            '''The name of the security configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformencryption.html#cfn-glue-mltransform-transformencryption-taskrunsecurityconfigurationname
            '''
            result = self._values.get("task_run_security_configuration_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransformEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnMLTransformPropsMixin.TransformParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "find_matches_parameters": "findMatchesParameters",
            "transform_type": "transformType",
        },
    )
    class TransformParametersProperty:
        def __init__(
            self,
            *,
            find_matches_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMLTransformPropsMixin.FindMatchesParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            transform_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The algorithm-specific parameters that are associated with the machine learning transform.

            :param find_matches_parameters: The parameters for the find matches algorithm.
            :param transform_type: The type of machine learning transform. ``FIND_MATCHES`` is the only option. For information about the types of machine learning transforms, see `Working with machine learning transforms <https://docs.aws.amazon.com/glue/latest/dg/console-machine-learning-transforms.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                transform_parameters_property = glue_mixins.CfnMLTransformPropsMixin.TransformParametersProperty(
                    find_matches_parameters=glue_mixins.CfnMLTransformPropsMixin.FindMatchesParametersProperty(
                        accuracy_cost_tradeoff=123,
                        enforce_provided_labels=False,
                        precision_recall_tradeoff=123,
                        primary_key_column_name="primaryKeyColumnName"
                    ),
                    transform_type="transformType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0e3a3b0ebbbd958280b240837a413562b1ecc5d09cea728692097798766df3b)
                check_type(argname="argument find_matches_parameters", value=find_matches_parameters, expected_type=type_hints["find_matches_parameters"])
                check_type(argname="argument transform_type", value=transform_type, expected_type=type_hints["transform_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if find_matches_parameters is not None:
                self._values["find_matches_parameters"] = find_matches_parameters
            if transform_type is not None:
                self._values["transform_type"] = transform_type

        @builtins.property
        def find_matches_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.FindMatchesParametersProperty"]]:
            '''The parameters for the find matches algorithm.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters.html#cfn-glue-mltransform-transformparameters-findmatchesparameters
            '''
            result = self._values.get("find_matches_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMLTransformPropsMixin.FindMatchesParametersProperty"]], result)

        @builtins.property
        def transform_type(self) -> typing.Optional[builtins.str]:
            '''The type of machine learning transform. ``FIND_MATCHES`` is the only option.

            For information about the types of machine learning transforms, see `Working with machine learning transforms <https://docs.aws.amazon.com/glue/latest/dg/console-machine-learning-transforms.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters.html#cfn-glue-mltransform-transformparameters-transformtype
            '''
            result = self._values.get("transform_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransformParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "catalog_id": "catalogId",
        "database_name": "databaseName",
        "partition_input": "partitionInput",
        "table_name": "tableName",
    },
)
class CfnPartitionMixinProps:
    def __init__(
        self,
        *,
        catalog_id: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        partition_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartitionPropsMixin.PartitionInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPartitionPropsMixin.

        :param catalog_id: The AWS account ID of the catalog in which the partion is to be created. .. epigraph:: To specify the account ID, you can use the ``Ref`` intrinsic function with the ``AWS::AccountId`` pseudo parameter. For example: ``!Ref AWS::AccountId``
        :param database_name: The name of the catalog database in which to create the partition.
        :param partition_input: The structure used to create and update a partition.
        :param table_name: The name of the metadata table in which the partition is to be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # parameters: Any
            # skewed_column_value_location_maps: Any
            
            cfn_partition_mixin_props = glue_mixins.CfnPartitionMixinProps(
                catalog_id="catalogId",
                database_name="databaseName",
                partition_input=glue_mixins.CfnPartitionPropsMixin.PartitionInputProperty(
                    parameters=parameters,
                    storage_descriptor=glue_mixins.CfnPartitionPropsMixin.StorageDescriptorProperty(
                        bucket_columns=["bucketColumns"],
                        columns=[glue_mixins.CfnPartitionPropsMixin.ColumnProperty(
                            comment="comment",
                            name="name",
                            type="type"
                        )],
                        compressed=False,
                        input_format="inputFormat",
                        location="location",
                        number_of_buckets=123,
                        output_format="outputFormat",
                        parameters=parameters,
                        schema_reference=glue_mixins.CfnPartitionPropsMixin.SchemaReferenceProperty(
                            schema_id=glue_mixins.CfnPartitionPropsMixin.SchemaIdProperty(
                                registry_name="registryName",
                                schema_arn="schemaArn",
                                schema_name="schemaName"
                            ),
                            schema_version_id="schemaVersionId",
                            schema_version_number=123
                        ),
                        serde_info=glue_mixins.CfnPartitionPropsMixin.SerdeInfoProperty(
                            name="name",
                            parameters=parameters,
                            serialization_library="serializationLibrary"
                        ),
                        skewed_info=glue_mixins.CfnPartitionPropsMixin.SkewedInfoProperty(
                            skewed_column_names=["skewedColumnNames"],
                            skewed_column_value_location_maps=skewed_column_value_location_maps,
                            skewed_column_values=["skewedColumnValues"]
                        ),
                        sort_columns=[glue_mixins.CfnPartitionPropsMixin.OrderProperty(
                            column="column",
                            sort_order=123
                        )],
                        stored_as_sub_directories=False
                    ),
                    values=["values"]
                ),
                table_name="tableName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d15f90e83eacb251a1b817ecbf932f78b16ec72871ec27acfa8199ee0d0759)
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument partition_input", value=partition_input, expected_type=type_hints["partition_input"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id
        if database_name is not None:
            self._values["database_name"] = database_name
        if partition_input is not None:
            self._values["partition_input"] = partition_input
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID of the catalog in which the partion is to be created.

        .. epigraph::

           To specify the account ID, you can use the ``Ref`` intrinsic function with the ``AWS::AccountId`` pseudo parameter. For example: ``!Ref AWS::AccountId``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-catalogid
        '''
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the catalog database in which to create the partition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_input(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.PartitionInputProperty"]]:
        '''The structure used to create and update a partition.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-partitioninput
        '''
        result = self._values.get("partition_input")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.PartitionInputProperty"]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metadata table in which the partition is to be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPartitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPartitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionPropsMixin",
):
    '''The ``AWS::Glue::Partition`` resource creates an AWS Glue partition, which represents a slice of table data.

    For more information, see `CreatePartition Action <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-partitions.html#aws-glue-api-catalog-partitions-CreatePartition>`_ and `Partition Structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-partitions.html#aws-glue-api-catalog-partitions-Partition>`_ in the *AWS Glue Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html
    :cloudformationResource: AWS::Glue::Partition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # parameters: Any
        # skewed_column_value_location_maps: Any
        
        cfn_partition_props_mixin = glue_mixins.CfnPartitionPropsMixin(glue_mixins.CfnPartitionMixinProps(
            catalog_id="catalogId",
            database_name="databaseName",
            partition_input=glue_mixins.CfnPartitionPropsMixin.PartitionInputProperty(
                parameters=parameters,
                storage_descriptor=glue_mixins.CfnPartitionPropsMixin.StorageDescriptorProperty(
                    bucket_columns=["bucketColumns"],
                    columns=[glue_mixins.CfnPartitionPropsMixin.ColumnProperty(
                        comment="comment",
                        name="name",
                        type="type"
                    )],
                    compressed=False,
                    input_format="inputFormat",
                    location="location",
                    number_of_buckets=123,
                    output_format="outputFormat",
                    parameters=parameters,
                    schema_reference=glue_mixins.CfnPartitionPropsMixin.SchemaReferenceProperty(
                        schema_id=glue_mixins.CfnPartitionPropsMixin.SchemaIdProperty(
                            registry_name="registryName",
                            schema_arn="schemaArn",
                            schema_name="schemaName"
                        ),
                        schema_version_id="schemaVersionId",
                        schema_version_number=123
                    ),
                    serde_info=glue_mixins.CfnPartitionPropsMixin.SerdeInfoProperty(
                        name="name",
                        parameters=parameters,
                        serialization_library="serializationLibrary"
                    ),
                    skewed_info=glue_mixins.CfnPartitionPropsMixin.SkewedInfoProperty(
                        skewed_column_names=["skewedColumnNames"],
                        skewed_column_value_location_maps=skewed_column_value_location_maps,
                        skewed_column_values=["skewedColumnValues"]
                    ),
                    sort_columns=[glue_mixins.CfnPartitionPropsMixin.OrderProperty(
                        column="column",
                        sort_order=123
                    )],
                    stored_as_sub_directories=False
                ),
                values=["values"]
            ),
            table_name="tableName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPartitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Partition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000bfdac516641a32b61c686e24ed2a82c371a8ada2a1ab0dd250a8e1b25251e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bed38f0c65280750c3a3222428b44b399a1fab4b69c2f5ffa2c15179861bfeba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1536a7a7d367ac54de44698ebd04d33ea85ac86e00e073d4e872bdd609024b9f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPartitionMixinProps:
        return typing.cast(CfnPartitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionPropsMixin.ColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"comment": "comment", "name": "name", "type": "type"},
    )
    class ColumnProperty:
        def __init__(
            self,
            *,
            comment: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A column in a ``Table`` .

            :param comment: A free-form text comment.
            :param name: The name of the ``Column`` .
            :param type: The data type of the ``Column`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-column.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                column_property = glue_mixins.CfnPartitionPropsMixin.ColumnProperty(
                    comment="comment",
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e4469fa91c5a6b1224dbad1ec42fe603f516f0a4b7563da8c3d963a788af8c7)
                check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comment is not None:
                self._values["comment"] = comment
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            '''A free-form text comment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-column.html#cfn-glue-partition-column-comment
            '''
            result = self._values.get("comment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the ``Column`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-column.html#cfn-glue-partition-column-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The data type of the ``Column`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-column.html#cfn-glue-partition-column-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionPropsMixin.OrderProperty",
        jsii_struct_bases=[],
        name_mapping={"column": "column", "sort_order": "sortOrder"},
    )
    class OrderProperty:
        def __init__(
            self,
            *,
            column: typing.Optional[builtins.str] = None,
            sort_order: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the sort order of a sorted column.

            :param column: The name of the column.
            :param sort_order: Indicates that the column is sorted in ascending order ( ``== 1`` ), or in descending order ( ``==0`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-order.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                order_property = glue_mixins.CfnPartitionPropsMixin.OrderProperty(
                    column="column",
                    sort_order=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ef67f1d5644903917dbd2d741b53f900648923dfa858d5c6af940befbae7d00)
                check_type(argname="argument column", value=column, expected_type=type_hints["column"])
                check_type(argname="argument sort_order", value=sort_order, expected_type=type_hints["sort_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column is not None:
                self._values["column"] = column
            if sort_order is not None:
                self._values["sort_order"] = sort_order

        @builtins.property
        def column(self) -> typing.Optional[builtins.str]:
            '''The name of the column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-order.html#cfn-glue-partition-order-column
            '''
            result = self._values.get("column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sort_order(self) -> typing.Optional[jsii.Number]:
            '''Indicates that the column is sorted in ascending order ( ``== 1`` ), or in descending order ( ``==0`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-order.html#cfn-glue-partition-order-sortorder
            '''
            result = self._values.get("sort_order")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionPropsMixin.PartitionInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameters": "parameters",
            "storage_descriptor": "storageDescriptor",
            "values": "values",
        },
    )
    class PartitionInputProperty:
        def __init__(
            self,
            *,
            parameters: typing.Any = None,
            storage_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartitionPropsMixin.StorageDescriptorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The structure used to create and update a partition.

            :param parameters: These key-value pairs define partition parameters.
            :param storage_descriptor: Provides information about the physical location where the partition is stored.
            :param values: The values of the partition. Although this parameter is not required by the SDK, you must specify this parameter for a valid input. The values for the keys for the new partition must be passed as an array of String objects that must be ordered in the same order as the partition keys appearing in the Amazon S3 prefix. Otherwise AWS Glue will add the values to the wrong keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-partitioninput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # parameters: Any
                # skewed_column_value_location_maps: Any
                
                partition_input_property = glue_mixins.CfnPartitionPropsMixin.PartitionInputProperty(
                    parameters=parameters,
                    storage_descriptor=glue_mixins.CfnPartitionPropsMixin.StorageDescriptorProperty(
                        bucket_columns=["bucketColumns"],
                        columns=[glue_mixins.CfnPartitionPropsMixin.ColumnProperty(
                            comment="comment",
                            name="name",
                            type="type"
                        )],
                        compressed=False,
                        input_format="inputFormat",
                        location="location",
                        number_of_buckets=123,
                        output_format="outputFormat",
                        parameters=parameters,
                        schema_reference=glue_mixins.CfnPartitionPropsMixin.SchemaReferenceProperty(
                            schema_id=glue_mixins.CfnPartitionPropsMixin.SchemaIdProperty(
                                registry_name="registryName",
                                schema_arn="schemaArn",
                                schema_name="schemaName"
                            ),
                            schema_version_id="schemaVersionId",
                            schema_version_number=123
                        ),
                        serde_info=glue_mixins.CfnPartitionPropsMixin.SerdeInfoProperty(
                            name="name",
                            parameters=parameters,
                            serialization_library="serializationLibrary"
                        ),
                        skewed_info=glue_mixins.CfnPartitionPropsMixin.SkewedInfoProperty(
                            skewed_column_names=["skewedColumnNames"],
                            skewed_column_value_location_maps=skewed_column_value_location_maps,
                            skewed_column_values=["skewedColumnValues"]
                        ),
                        sort_columns=[glue_mixins.CfnPartitionPropsMixin.OrderProperty(
                            column="column",
                            sort_order=123
                        )],
                        stored_as_sub_directories=False
                    ),
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e3db50af5aa28f148ffb6a4d04b68a366d04081c94b77404f0c6cb624278ef2)
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument storage_descriptor", value=storage_descriptor, expected_type=type_hints["storage_descriptor"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameters is not None:
                self._values["parameters"] = parameters
            if storage_descriptor is not None:
                self._values["storage_descriptor"] = storage_descriptor
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def parameters(self) -> typing.Any:
            '''These key-value pairs define partition parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-partitioninput.html#cfn-glue-partition-partitioninput-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def storage_descriptor(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.StorageDescriptorProperty"]]:
            '''Provides information about the physical location where the partition is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-partitioninput.html#cfn-glue-partition-partitioninput-storagedescriptor
            '''
            result = self._values.get("storage_descriptor")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.StorageDescriptorProperty"]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values of the partition.

            Although this parameter is not required by the SDK, you must specify this parameter for a valid input.

            The values for the keys for the new partition must be passed as an array of String objects that must be ordered in the same order as the partition keys appearing in the Amazon S3 prefix. Otherwise AWS Glue will add the values to the wrong keys.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-partitioninput.html#cfn-glue-partition-partitioninput-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PartitionInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionPropsMixin.SchemaIdProperty",
        jsii_struct_bases=[],
        name_mapping={
            "registry_name": "registryName",
            "schema_arn": "schemaArn",
            "schema_name": "schemaName",
        },
    )
    class SchemaIdProperty:
        def __init__(
            self,
            *,
            registry_name: typing.Optional[builtins.str] = None,
            schema_arn: typing.Optional[builtins.str] = None,
            schema_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains schema identity fields.

            Either this or the ``SchemaVersionId`` has to be
            provided.

            :param registry_name: The name of the schema registry that contains the schema.
            :param schema_arn: The Amazon Resource Name (ARN) of the schema. One of ``SchemaArn`` or ``SchemaName`` has to be provided.
            :param schema_name: The name of the schema. One of ``SchemaArn`` or ``SchemaName`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-schemaid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                schema_id_property = glue_mixins.CfnPartitionPropsMixin.SchemaIdProperty(
                    registry_name="registryName",
                    schema_arn="schemaArn",
                    schema_name="schemaName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e96c8231305fc80075c66e8b45953f99a56a5d58c5eaccb85ea8616c6b772ee6)
                check_type(argname="argument registry_name", value=registry_name, expected_type=type_hints["registry_name"])
                check_type(argname="argument schema_arn", value=schema_arn, expected_type=type_hints["schema_arn"])
                check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if registry_name is not None:
                self._values["registry_name"] = registry_name
            if schema_arn is not None:
                self._values["schema_arn"] = schema_arn
            if schema_name is not None:
                self._values["schema_name"] = schema_name

        @builtins.property
        def registry_name(self) -> typing.Optional[builtins.str]:
            '''The name of the schema registry that contains the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-schemaid.html#cfn-glue-partition-schemaid-registryname
            '''
            result = self._values.get("registry_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the schema.

            One of ``SchemaArn`` or ``SchemaName`` has to be
            provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-schemaid.html#cfn-glue-partition-schemaid-schemaarn
            '''
            result = self._values.get("schema_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_name(self) -> typing.Optional[builtins.str]:
            '''The name of the schema.

            One of ``SchemaArn`` or ``SchemaName`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-schemaid.html#cfn-glue-partition-schemaid-schemaname
            '''
            result = self._values.get("schema_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionPropsMixin.SchemaReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "schema_id": "schemaId",
            "schema_version_id": "schemaVersionId",
            "schema_version_number": "schemaVersionNumber",
        },
    )
    class SchemaReferenceProperty:
        def __init__(
            self,
            *,
            schema_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartitionPropsMixin.SchemaIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            schema_version_id: typing.Optional[builtins.str] = None,
            schema_version_number: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that references a schema stored in the AWS Glue Schema Registry.

            :param schema_id: A structure that contains schema identity fields. Either this or the ``SchemaVersionId`` has to be provided.
            :param schema_version_id: The unique ID assigned to a version of the schema. Either this or the ``SchemaId`` has to be provided.
            :param schema_version_number: The version number of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-schemareference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                schema_reference_property = glue_mixins.CfnPartitionPropsMixin.SchemaReferenceProperty(
                    schema_id=glue_mixins.CfnPartitionPropsMixin.SchemaIdProperty(
                        registry_name="registryName",
                        schema_arn="schemaArn",
                        schema_name="schemaName"
                    ),
                    schema_version_id="schemaVersionId",
                    schema_version_number=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14a5fe8b3160edb4ce744eff12088209227fcdd5f00b221f8daa0ab44a8830ac)
                check_type(argname="argument schema_id", value=schema_id, expected_type=type_hints["schema_id"])
                check_type(argname="argument schema_version_id", value=schema_version_id, expected_type=type_hints["schema_version_id"])
                check_type(argname="argument schema_version_number", value=schema_version_number, expected_type=type_hints["schema_version_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schema_id is not None:
                self._values["schema_id"] = schema_id
            if schema_version_id is not None:
                self._values["schema_version_id"] = schema_version_id
            if schema_version_number is not None:
                self._values["schema_version_number"] = schema_version_number

        @builtins.property
        def schema_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.SchemaIdProperty"]]:
            '''A structure that contains schema identity fields.

            Either this or the ``SchemaVersionId`` has to be
            provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-schemareference.html#cfn-glue-partition-schemareference-schemaid
            '''
            result = self._values.get("schema_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.SchemaIdProperty"]], result)

        @builtins.property
        def schema_version_id(self) -> typing.Optional[builtins.str]:
            '''The unique ID assigned to a version of the schema.

            Either this or the ``SchemaId`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-schemareference.html#cfn-glue-partition-schemareference-schemaversionid
            '''
            result = self._values.get("schema_version_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_version_number(self) -> typing.Optional[jsii.Number]:
            '''The version number of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-schemareference.html#cfn-glue-partition-schemareference-schemaversionnumber
            '''
            result = self._values.get("schema_version_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionPropsMixin.SerdeInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "parameters": "parameters",
            "serialization_library": "serializationLibrary",
        },
    )
    class SerdeInfoProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
            serialization_library: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a serialization/deserialization program (SerDe) that serves as an extractor and loader.

            :param name: Name of the SerDe.
            :param parameters: These key-value pairs define initialization parameters for the SerDe.
            :param serialization_library: Usually the class that implements the SerDe. An example is ``org.apache.hadoop.hive.serde2.columnar.ColumnarSerDe`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-serdeinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # parameters: Any
                
                serde_info_property = glue_mixins.CfnPartitionPropsMixin.SerdeInfoProperty(
                    name="name",
                    parameters=parameters,
                    serialization_library="serializationLibrary"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c96f3005cf7b037ddccbda6b9beaf4a8b19b24f086f48b2829772461bc6f4ca)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument serialization_library", value=serialization_library, expected_type=type_hints["serialization_library"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if parameters is not None:
                self._values["parameters"] = parameters
            if serialization_library is not None:
                self._values["serialization_library"] = serialization_library

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of the SerDe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-serdeinfo.html#cfn-glue-partition-serdeinfo-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''These key-value pairs define initialization parameters for the SerDe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-serdeinfo.html#cfn-glue-partition-serdeinfo-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def serialization_library(self) -> typing.Optional[builtins.str]:
            '''Usually the class that implements the SerDe.

            An example is ``org.apache.hadoop.hive.serde2.columnar.ColumnarSerDe`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-serdeinfo.html#cfn-glue-partition-serdeinfo-serializationlibrary
            '''
            result = self._values.get("serialization_library")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SerdeInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionPropsMixin.SkewedInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "skewed_column_names": "skewedColumnNames",
            "skewed_column_value_location_maps": "skewedColumnValueLocationMaps",
            "skewed_column_values": "skewedColumnValues",
        },
    )
    class SkewedInfoProperty:
        def __init__(
            self,
            *,
            skewed_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            skewed_column_value_location_maps: typing.Any = None,
            skewed_column_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies skewed values in a table.

            Skewed values are those that occur with very high frequency.

            :param skewed_column_names: A list of names of columns that contain skewed values.
            :param skewed_column_value_location_maps: A mapping of skewed values to the columns that contain them.
            :param skewed_column_values: A list of values that appear so frequently as to be considered skewed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-skewedinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # skewed_column_value_location_maps: Any
                
                skewed_info_property = glue_mixins.CfnPartitionPropsMixin.SkewedInfoProperty(
                    skewed_column_names=["skewedColumnNames"],
                    skewed_column_value_location_maps=skewed_column_value_location_maps,
                    skewed_column_values=["skewedColumnValues"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3b4fcfbeb7ea5a0bc9adfba611e33df091de885711c67f5ae416e47abd1f411)
                check_type(argname="argument skewed_column_names", value=skewed_column_names, expected_type=type_hints["skewed_column_names"])
                check_type(argname="argument skewed_column_value_location_maps", value=skewed_column_value_location_maps, expected_type=type_hints["skewed_column_value_location_maps"])
                check_type(argname="argument skewed_column_values", value=skewed_column_values, expected_type=type_hints["skewed_column_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if skewed_column_names is not None:
                self._values["skewed_column_names"] = skewed_column_names
            if skewed_column_value_location_maps is not None:
                self._values["skewed_column_value_location_maps"] = skewed_column_value_location_maps
            if skewed_column_values is not None:
                self._values["skewed_column_values"] = skewed_column_values

        @builtins.property
        def skewed_column_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of names of columns that contain skewed values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-skewedinfo.html#cfn-glue-partition-skewedinfo-skewedcolumnnames
            '''
            result = self._values.get("skewed_column_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def skewed_column_value_location_maps(self) -> typing.Any:
            '''A mapping of skewed values to the columns that contain them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-skewedinfo.html#cfn-glue-partition-skewedinfo-skewedcolumnvaluelocationmaps
            '''
            result = self._values.get("skewed_column_value_location_maps")
            return typing.cast(typing.Any, result)

        @builtins.property
        def skewed_column_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of values that appear so frequently as to be considered skewed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-skewedinfo.html#cfn-glue-partition-skewedinfo-skewedcolumnvalues
            '''
            result = self._values.get("skewed_column_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SkewedInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnPartitionPropsMixin.StorageDescriptorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_columns": "bucketColumns",
            "columns": "columns",
            "compressed": "compressed",
            "input_format": "inputFormat",
            "location": "location",
            "number_of_buckets": "numberOfBuckets",
            "output_format": "outputFormat",
            "parameters": "parameters",
            "schema_reference": "schemaReference",
            "serde_info": "serdeInfo",
            "skewed_info": "skewedInfo",
            "sort_columns": "sortColumns",
            "stored_as_sub_directories": "storedAsSubDirectories",
        },
    )
    class StorageDescriptorProperty:
        def __init__(
            self,
            *,
            bucket_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
            columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartitionPropsMixin.ColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compressed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            input_format: typing.Optional[builtins.str] = None,
            location: typing.Optional[builtins.str] = None,
            number_of_buckets: typing.Optional[jsii.Number] = None,
            output_format: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
            schema_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartitionPropsMixin.SchemaReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            serde_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartitionPropsMixin.SerdeInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            skewed_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartitionPropsMixin.SkewedInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sort_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPartitionPropsMixin.OrderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            stored_as_sub_directories: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes the physical storage of table data.

            :param bucket_columns: A list of reducer grouping columns, clustering columns, and bucketing columns in the table.
            :param columns: A list of the ``Columns`` in the table.
            :param compressed: ``True`` if the data in the table is compressed, or ``False`` if not.
            :param input_format: The input format: ``SequenceFileInputFormat`` (binary), or ``TextInputFormat`` , or a custom format.
            :param location: The physical location of the table. By default, this takes the form of the warehouse location, followed by the database location in the warehouse, followed by the table name.
            :param number_of_buckets: The number of buckets. You must specify this property if the partition contains any dimension columns.
            :param output_format: The output format: ``SequenceFileOutputFormat`` (binary), or ``IgnoreKeyTextOutputFormat`` , or a custom format.
            :param parameters: The user-supplied properties in key-value form.
            :param schema_reference: An object that references a schema stored in the AWS Glue Schema Registry.
            :param serde_info: The serialization/deserialization (SerDe) information.
            :param skewed_info: The information about values that appear frequently in a column (skewed values).
            :param sort_columns: A list specifying the sort order of each bucket in the table.
            :param stored_as_sub_directories: ``True`` if the table data is stored in subdirectories, or ``False`` if not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # parameters: Any
                # skewed_column_value_location_maps: Any
                
                storage_descriptor_property = glue_mixins.CfnPartitionPropsMixin.StorageDescriptorProperty(
                    bucket_columns=["bucketColumns"],
                    columns=[glue_mixins.CfnPartitionPropsMixin.ColumnProperty(
                        comment="comment",
                        name="name",
                        type="type"
                    )],
                    compressed=False,
                    input_format="inputFormat",
                    location="location",
                    number_of_buckets=123,
                    output_format="outputFormat",
                    parameters=parameters,
                    schema_reference=glue_mixins.CfnPartitionPropsMixin.SchemaReferenceProperty(
                        schema_id=glue_mixins.CfnPartitionPropsMixin.SchemaIdProperty(
                            registry_name="registryName",
                            schema_arn="schemaArn",
                            schema_name="schemaName"
                        ),
                        schema_version_id="schemaVersionId",
                        schema_version_number=123
                    ),
                    serde_info=glue_mixins.CfnPartitionPropsMixin.SerdeInfoProperty(
                        name="name",
                        parameters=parameters,
                        serialization_library="serializationLibrary"
                    ),
                    skewed_info=glue_mixins.CfnPartitionPropsMixin.SkewedInfoProperty(
                        skewed_column_names=["skewedColumnNames"],
                        skewed_column_value_location_maps=skewed_column_value_location_maps,
                        skewed_column_values=["skewedColumnValues"]
                    ),
                    sort_columns=[glue_mixins.CfnPartitionPropsMixin.OrderProperty(
                        column="column",
                        sort_order=123
                    )],
                    stored_as_sub_directories=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e744d2827fdf2260937ba701f671d1cf11611fdbe724b6e5e52803054453b7f)
                check_type(argname="argument bucket_columns", value=bucket_columns, expected_type=type_hints["bucket_columns"])
                check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
                check_type(argname="argument compressed", value=compressed, expected_type=type_hints["compressed"])
                check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument number_of_buckets", value=number_of_buckets, expected_type=type_hints["number_of_buckets"])
                check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument schema_reference", value=schema_reference, expected_type=type_hints["schema_reference"])
                check_type(argname="argument serde_info", value=serde_info, expected_type=type_hints["serde_info"])
                check_type(argname="argument skewed_info", value=skewed_info, expected_type=type_hints["skewed_info"])
                check_type(argname="argument sort_columns", value=sort_columns, expected_type=type_hints["sort_columns"])
                check_type(argname="argument stored_as_sub_directories", value=stored_as_sub_directories, expected_type=type_hints["stored_as_sub_directories"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_columns is not None:
                self._values["bucket_columns"] = bucket_columns
            if columns is not None:
                self._values["columns"] = columns
            if compressed is not None:
                self._values["compressed"] = compressed
            if input_format is not None:
                self._values["input_format"] = input_format
            if location is not None:
                self._values["location"] = location
            if number_of_buckets is not None:
                self._values["number_of_buckets"] = number_of_buckets
            if output_format is not None:
                self._values["output_format"] = output_format
            if parameters is not None:
                self._values["parameters"] = parameters
            if schema_reference is not None:
                self._values["schema_reference"] = schema_reference
            if serde_info is not None:
                self._values["serde_info"] = serde_info
            if skewed_info is not None:
                self._values["skewed_info"] = skewed_info
            if sort_columns is not None:
                self._values["sort_columns"] = sort_columns
            if stored_as_sub_directories is not None:
                self._values["stored_as_sub_directories"] = stored_as_sub_directories

        @builtins.property
        def bucket_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of reducer grouping columns, clustering columns, and bucketing columns in the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-bucketcolumns
            '''
            result = self._values.get("bucket_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.ColumnProperty"]]]]:
            '''A list of the ``Columns`` in the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-columns
            '''
            result = self._values.get("columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.ColumnProperty"]]]], result)

        @builtins.property
        def compressed(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``True`` if the data in the table is compressed, or ``False`` if not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-compressed
            '''
            result = self._values.get("compressed")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def input_format(self) -> typing.Optional[builtins.str]:
            '''The input format: ``SequenceFileInputFormat`` (binary), or ``TextInputFormat`` , or a custom format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-inputformat
            '''
            result = self._values.get("input_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''The physical location of the table.

            By default, this takes the form of the warehouse location, followed by the database location in the warehouse, followed by the table name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def number_of_buckets(self) -> typing.Optional[jsii.Number]:
            '''The number of buckets.

            You must specify this property if the partition contains any dimension columns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-numberofbuckets
            '''
            result = self._values.get("number_of_buckets")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def output_format(self) -> typing.Optional[builtins.str]:
            '''The output format: ``SequenceFileOutputFormat`` (binary), or ``IgnoreKeyTextOutputFormat`` , or a custom format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-outputformat
            '''
            result = self._values.get("output_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''The user-supplied properties in key-value form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def schema_reference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.SchemaReferenceProperty"]]:
            '''An object that references a schema stored in the AWS Glue Schema Registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-schemareference
            '''
            result = self._values.get("schema_reference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.SchemaReferenceProperty"]], result)

        @builtins.property
        def serde_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.SerdeInfoProperty"]]:
            '''The serialization/deserialization (SerDe) information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-serdeinfo
            '''
            result = self._values.get("serde_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.SerdeInfoProperty"]], result)

        @builtins.property
        def skewed_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.SkewedInfoProperty"]]:
            '''The information about values that appear frequently in a column (skewed values).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-skewedinfo
            '''
            result = self._values.get("skewed_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.SkewedInfoProperty"]], result)

        @builtins.property
        def sort_columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.OrderProperty"]]]]:
            '''A list specifying the sort order of each bucket in the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-sortcolumns
            '''
            result = self._values.get("sort_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPartitionPropsMixin.OrderProperty"]]]], result)

        @builtins.property
        def stored_as_sub_directories(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``True`` if the table data is stored in subdirectories, or ``False`` if not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-storedassubdirectories
            '''
            result = self._values.get("stored_as_sub_directories")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageDescriptorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnRegistryMixinProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name", "tags": "tags"},
)
class CfnRegistryMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRegistryPropsMixin.

        :param description: A description of the registry.
        :param name: The name of the registry.
        :param tags: AWS tags that contain a key value pair and may be searched by console, command line, or API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-registry.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_registry_mixin_props = glue_mixins.CfnRegistryMixinProps(
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4122a43f710358b5b23c136781acc74bed3fb447c35023c9cc4cb82f6a065ed)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-registry.html#cfn-glue-registry-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the registry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-registry.html#cfn-glue-registry-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''AWS tags that contain a key value pair and may be searched by console, command line, or API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-registry.html#cfn-glue-registry-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegistryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRegistryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnRegistryPropsMixin",
):
    '''The AWS::Glue::Registry is an AWS Glue resource type that manages registries of schemas in the AWS Glue Schema Registry.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-registry.html
    :cloudformationResource: AWS::Glue::Registry
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_registry_props_mixin = glue_mixins.CfnRegistryPropsMixin(glue_mixins.CfnRegistryMixinProps(
            description="description",
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
        props: typing.Union[CfnRegistryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Registry``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cae20de650720887756b13c5b3769905f58d28583cea52ef96183dad98594ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d14c5cdedd1c08f0899a143f995241ed1af63631510678da4ef577329e894fb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68efd3d60b005cc15b77b7138b32f2d45ad1d332d9eda1be46964169407d6305)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRegistryMixinProps:
        return typing.cast(CfnRegistryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSchemaMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "checkpoint_version": "checkpointVersion",
        "compatibility": "compatibility",
        "data_format": "dataFormat",
        "description": "description",
        "name": "name",
        "registry": "registry",
        "schema_definition": "schemaDefinition",
        "tags": "tags",
    },
)
class CfnSchemaMixinProps:
    def __init__(
        self,
        *,
        checkpoint_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchemaPropsMixin.SchemaVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        compatibility: typing.Optional[builtins.str] = None,
        data_format: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        registry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchemaPropsMixin.RegistryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schema_definition: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSchemaPropsMixin.

        :param checkpoint_version: Specify the ``VersionNumber`` or the ``IsLatest`` for setting the checkpoint for the schema. This is only required for updating a checkpoint.
        :param compatibility: The compatibility mode of the schema.
        :param data_format: The data format of the schema definition. Currently only ``AVRO`` is supported.
        :param description: A description of the schema if specified when created.
        :param name: Name of the schema to be created of max length of 255, and may only contain letters, numbers, hyphen, underscore, dollar sign, or hash mark. No whitespace.
        :param registry: The registry where a schema is stored.
        :param schema_definition: The schema definition using the ``DataFormat`` setting for ``SchemaName`` .
        :param tags: AWS tags that contain a key value pair and may be searched by console, command line, or API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_schema_mixin_props = glue_mixins.CfnSchemaMixinProps(
                checkpoint_version=glue_mixins.CfnSchemaPropsMixin.SchemaVersionProperty(
                    is_latest=False,
                    version_number=123
                ),
                compatibility="compatibility",
                data_format="dataFormat",
                description="description",
                name="name",
                registry=glue_mixins.CfnSchemaPropsMixin.RegistryProperty(
                    arn="arn",
                    name="name"
                ),
                schema_definition="schemaDefinition",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797ad145a2a564ed9f64b9045d1c79b1bd3057f47213268c2f391f6510112154)
            check_type(argname="argument checkpoint_version", value=checkpoint_version, expected_type=type_hints["checkpoint_version"])
            check_type(argname="argument compatibility", value=compatibility, expected_type=type_hints["compatibility"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if checkpoint_version is not None:
            self._values["checkpoint_version"] = checkpoint_version
        if compatibility is not None:
            self._values["compatibility"] = compatibility
        if data_format is not None:
            self._values["data_format"] = data_format
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if registry is not None:
            self._values["registry"] = registry
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def checkpoint_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchemaPropsMixin.SchemaVersionProperty"]]:
        '''Specify the ``VersionNumber`` or the ``IsLatest`` for setting the checkpoint for the schema.

        This is only required for updating a checkpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html#cfn-glue-schema-checkpointversion
        '''
        result = self._values.get("checkpoint_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchemaPropsMixin.SchemaVersionProperty"]], result)

    @builtins.property
    def compatibility(self) -> typing.Optional[builtins.str]:
        '''The compatibility mode of the schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html#cfn-glue-schema-compatibility
        '''
        result = self._values.get("compatibility")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_format(self) -> typing.Optional[builtins.str]:
        '''The data format of the schema definition.

        Currently only ``AVRO`` is supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html#cfn-glue-schema-dataformat
        '''
        result = self._values.get("data_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the schema if specified when created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html#cfn-glue-schema-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the schema to be created of max length of 255, and may only contain letters, numbers, hyphen, underscore, dollar sign, or hash mark.

        No whitespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html#cfn-glue-schema-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchemaPropsMixin.RegistryProperty"]]:
        '''The registry where a schema is stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html#cfn-glue-schema-registry
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchemaPropsMixin.RegistryProperty"]], result)

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The schema definition using the ``DataFormat`` setting for ``SchemaName`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html#cfn-glue-schema-schemadefinition
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''AWS tags that contain a key value pair and may be searched by console, command line, or API.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html#cfn-glue-schema-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchemaMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSchemaPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSchemaPropsMixin",
):
    '''The ``AWS::Glue::Schema`` is an AWS Glue resource type that manages schemas in the AWS Glue Schema Registry.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schema.html
    :cloudformationResource: AWS::Glue::Schema
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_schema_props_mixin = glue_mixins.CfnSchemaPropsMixin(glue_mixins.CfnSchemaMixinProps(
            checkpoint_version=glue_mixins.CfnSchemaPropsMixin.SchemaVersionProperty(
                is_latest=False,
                version_number=123
            ),
            compatibility="compatibility",
            data_format="dataFormat",
            description="description",
            name="name",
            registry=glue_mixins.CfnSchemaPropsMixin.RegistryProperty(
                arn="arn",
                name="name"
            ),
            schema_definition="schemaDefinition",
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
        props: typing.Union[CfnSchemaMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Schema``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e45ca7c9324c44105433ccf21b787d563cbfa0e124ab33c57729fd45e825097)
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
            type_hints = typing.get_type_hints(_typecheckingstub__265a1738beca109d1add72fb150fce5ee10097d839e4dc1f7fd5a962defcc237)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f8cf42d684bf9e325de978ccce5985d9868f20b6f4d43e3d7950ff625aa4be)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSchemaMixinProps:
        return typing.cast(CfnSchemaMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSchemaPropsMixin.RegistryProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "name": "name"},
    )
    class RegistryProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a registry in the AWS Glue Schema Registry.

            :param arn: The Amazon Resource Name (ARN) of the registry.
            :param name: The name of the registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schema-registry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                registry_property = glue_mixins.CfnSchemaPropsMixin.RegistryProperty(
                    arn="arn",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0e1a8fa8339508c57b19e898d905c342259a7d5c019db94fa913d14f6ed4da3)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schema-registry.html#cfn-glue-schema-registry-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schema-registry.html#cfn-glue-schema-registry-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegistryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSchemaPropsMixin.SchemaVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"is_latest": "isLatest", "version_number": "versionNumber"},
    )
    class SchemaVersionProperty:
        def __init__(
            self,
            *,
            is_latest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            version_number: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the version of a schema.

            :param is_latest: Indicates if this version is the latest version of the schema.
            :param version_number: The version number of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schema-schemaversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                schema_version_property = glue_mixins.CfnSchemaPropsMixin.SchemaVersionProperty(
                    is_latest=False,
                    version_number=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9a05d88582b4860dbdce27c09b169985d87ed0786288a4081d40c1ed6be6420)
                check_type(argname="argument is_latest", value=is_latest, expected_type=type_hints["is_latest"])
                check_type(argname="argument version_number", value=version_number, expected_type=type_hints["version_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_latest is not None:
                self._values["is_latest"] = is_latest
            if version_number is not None:
                self._values["version_number"] = version_number

        @builtins.property
        def is_latest(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates if this version is the latest version of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schema-schemaversion.html#cfn-glue-schema-schemaversion-islatest
            '''
            result = self._values.get("is_latest")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def version_number(self) -> typing.Optional[jsii.Number]:
            '''The version number of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schema-schemaversion.html#cfn-glue-schema-schemaversion-versionnumber
            '''
            result = self._values.get("version_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSchemaVersionMetadataMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "schema_version_id": "schemaVersionId",
        "value": "value",
    },
)
class CfnSchemaVersionMetadataMixinProps:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        schema_version_id: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSchemaVersionMetadataPropsMixin.

        :param key: A metadata key in a key-value pair for metadata.
        :param schema_version_id: The version number of the schema.
        :param value: A metadata key's corresponding value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schemaversionmetadata.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_schema_version_metadata_mixin_props = glue_mixins.CfnSchemaVersionMetadataMixinProps(
                key="key",
                schema_version_id="schemaVersionId",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20cda9be8abe0ed94166a3c707e6667bca2e83bed7c46c8542c323eaf6664c0a)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument schema_version_id", value=schema_version_id, expected_type=type_hints["schema_version_id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if schema_version_id is not None:
            self._values["schema_version_id"] = schema_version_id
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A metadata key in a key-value pair for metadata.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schemaversionmetadata.html#cfn-glue-schemaversionmetadata-key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_version_id(self) -> typing.Optional[builtins.str]:
        '''The version number of the schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schemaversionmetadata.html#cfn-glue-schemaversionmetadata-schemaversionid
        '''
        result = self._values.get("schema_version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A metadata key's corresponding value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schemaversionmetadata.html#cfn-glue-schemaversionmetadata-value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchemaVersionMetadataMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSchemaVersionMetadataPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSchemaVersionMetadataPropsMixin",
):
    '''The ``AWS::Glue::SchemaVersionMetadata`` is an AWS Glue resource type that defines the metadata key-value pairs for a schema version in AWS Glue Schema Registry.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schemaversionmetadata.html
    :cloudformationResource: AWS::Glue::SchemaVersionMetadata
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_schema_version_metadata_props_mixin = glue_mixins.CfnSchemaVersionMetadataPropsMixin(glue_mixins.CfnSchemaVersionMetadataMixinProps(
            key="key",
            schema_version_id="schemaVersionId",
            value="value"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSchemaVersionMetadataMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::SchemaVersionMetadata``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a7f44dd970b99a593e5657762d031f11f67ae502df506093f5a43a6c24355e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94f20618a50b265c029680471a48057fccbc6d6a854365d527089f08ae8dd9b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9799fefe16736bd874b702357957dd86e0dd33dac3f4b9b019b370fe555aba6a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSchemaVersionMetadataMixinProps:
        return typing.cast(CfnSchemaVersionMetadataMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSchemaVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema", "schema_definition": "schemaDefinition"},
)
class CfnSchemaVersionMixinProps:
    def __init__(
        self,
        *,
        schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchemaVersionPropsMixin.SchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schema_definition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSchemaVersionPropsMixin.

        :param schema: The schema that includes the schema version.
        :param schema_definition: The schema definition for the schema version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schemaversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_schema_version_mixin_props = glue_mixins.CfnSchemaVersionMixinProps(
                schema=glue_mixins.CfnSchemaVersionPropsMixin.SchemaProperty(
                    registry_name="registryName",
                    schema_arn="schemaArn",
                    schema_name="schemaName"
                ),
                schema_definition="schemaDefinition"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a1a59496157746b64b6985732bd8521e1128cdaa8fab70e78f7fcd16f9354f)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument schema_definition", value=schema_definition, expected_type=type_hints["schema_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema is not None:
            self._values["schema"] = schema
        if schema_definition is not None:
            self._values["schema_definition"] = schema_definition

    @builtins.property
    def schema(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchemaVersionPropsMixin.SchemaProperty"]]:
        '''The schema that includes the schema version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schemaversion.html#cfn-glue-schemaversion-schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchemaVersionPropsMixin.SchemaProperty"]], result)

    @builtins.property
    def schema_definition(self) -> typing.Optional[builtins.str]:
        '''The schema definition for the schema version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schemaversion.html#cfn-glue-schemaversion-schemadefinition
        '''
        result = self._values.get("schema_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchemaVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSchemaVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSchemaVersionPropsMixin",
):
    '''The ``AWS::Glue::SchemaVersion`` is an AWS Glue resource type that manages schema versions of schemas in the AWS Glue Schema Registry.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-schemaversion.html
    :cloudformationResource: AWS::Glue::SchemaVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_schema_version_props_mixin = glue_mixins.CfnSchemaVersionPropsMixin(glue_mixins.CfnSchemaVersionMixinProps(
            schema=glue_mixins.CfnSchemaVersionPropsMixin.SchemaProperty(
                registry_name="registryName",
                schema_arn="schemaArn",
                schema_name="schemaName"
            ),
            schema_definition="schemaDefinition"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSchemaVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::SchemaVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05b01e63be1aec486364775a724690b218604b1b78e1bf426f797d1826b564c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2611ce35bd64fe6a67b5e2878d61a601655c87b2eb7e5227ca67af005767458f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6f5d6fe372fdfdc556939a7510883a034dab128d2fb488bfa5be20abfe0328)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSchemaVersionMixinProps:
        return typing.cast(CfnSchemaVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSchemaVersionPropsMixin.SchemaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "registry_name": "registryName",
            "schema_arn": "schemaArn",
            "schema_name": "schemaName",
        },
    )
    class SchemaProperty:
        def __init__(
            self,
            *,
            registry_name: typing.Optional[builtins.str] = None,
            schema_arn: typing.Optional[builtins.str] = None,
            schema_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A wrapper structure to contain schema identity fields.

            Either ``SchemaArn`` , or ``SchemaName`` and ``RegistryName`` has to be provided.

            :param registry_name: The name of the registry where the schema is stored. Either ``SchemaArn`` , or ``SchemaName`` and ``RegistryName`` has to be provided.
            :param schema_arn: The Amazon Resource Name (ARN) of the schema. Either ``SchemaArn`` , or ``SchemaName`` and ``RegistryName`` has to be provided.
            :param schema_name: The name of the schema. Either ``SchemaArn`` , or ``SchemaName`` and ``RegistryName`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schemaversion-schema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                schema_property = glue_mixins.CfnSchemaVersionPropsMixin.SchemaProperty(
                    registry_name="registryName",
                    schema_arn="schemaArn",
                    schema_name="schemaName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80b8dbeef1590ee1e8c48058d3021f94c409b610daeb9e23aec70d0dd06737e9)
                check_type(argname="argument registry_name", value=registry_name, expected_type=type_hints["registry_name"])
                check_type(argname="argument schema_arn", value=schema_arn, expected_type=type_hints["schema_arn"])
                check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if registry_name is not None:
                self._values["registry_name"] = registry_name
            if schema_arn is not None:
                self._values["schema_arn"] = schema_arn
            if schema_name is not None:
                self._values["schema_name"] = schema_name

        @builtins.property
        def registry_name(self) -> typing.Optional[builtins.str]:
            '''The name of the registry where the schema is stored.

            Either ``SchemaArn`` , or ``SchemaName`` and ``RegistryName`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schemaversion-schema.html#cfn-glue-schemaversion-schema-registryname
            '''
            result = self._values.get("registry_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the schema.

            Either ``SchemaArn`` , or ``SchemaName`` and ``RegistryName`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schemaversion-schema.html#cfn-glue-schemaversion-schema-schemaarn
            '''
            result = self._values.get("schema_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_name(self) -> typing.Optional[builtins.str]:
            '''The name of the schema.

            Either ``SchemaArn`` , or ``SchemaName`` and ``RegistryName`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-schemaversion-schema.html#cfn-glue-schemaversion-schema-schemaname
            '''
            result = self._values.get("schema_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSecurityConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "name": "name",
    },
)
class CfnSecurityConfigurationMixinProps:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityConfigurationPropsMixin.EncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSecurityConfigurationPropsMixin.

        :param encryption_configuration: The encryption configuration associated with this security configuration.
        :param name: The name of the security configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_security_configuration_mixin_props = glue_mixins.CfnSecurityConfigurationMixinProps(
                encryption_configuration=glue_mixins.CfnSecurityConfigurationPropsMixin.EncryptionConfigurationProperty(
                    cloud_watch_encryption=glue_mixins.CfnSecurityConfigurationPropsMixin.CloudWatchEncryptionProperty(
                        cloud_watch_encryption_mode="cloudWatchEncryptionMode",
                        kms_key_arn="kmsKeyArn"
                    ),
                    job_bookmarks_encryption=glue_mixins.CfnSecurityConfigurationPropsMixin.JobBookmarksEncryptionProperty(
                        job_bookmarks_encryption_mode="jobBookmarksEncryptionMode",
                        kms_key_arn="kmsKeyArn"
                    ),
                    s3_encryptions=[glue_mixins.CfnSecurityConfigurationPropsMixin.S3EncryptionProperty(
                        kms_key_arn="kmsKeyArn",
                        s3_encryption_mode="s3EncryptionMode"
                    )]
                ),
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1c9367a3c8bcb3cefd8b88e3a837f8d964d78b8a6ead36bd941c96ae9efb8c)
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigurationPropsMixin.EncryptionConfigurationProperty"]]:
        '''The encryption configuration associated with this security configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigurationPropsMixin.EncryptionConfigurationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the security configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html#cfn-glue-securityconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecurityConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSecurityConfigurationPropsMixin",
):
    '''Creates a new security configuration.

    A security configuration is a set of security properties that can be used by AWS Glue . You can use a security configuration to encrypt data at rest. For information about using security configurations in AWS Glue , see `Encrypting Data Written by Crawlers, Jobs, and Development Endpoints <https://docs.aws.amazon.com/glue/latest/dg/encryption-security-configuration.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html
    :cloudformationResource: AWS::Glue::SecurityConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_security_configuration_props_mixin = glue_mixins.CfnSecurityConfigurationPropsMixin(glue_mixins.CfnSecurityConfigurationMixinProps(
            encryption_configuration=glue_mixins.CfnSecurityConfigurationPropsMixin.EncryptionConfigurationProperty(
                cloud_watch_encryption=glue_mixins.CfnSecurityConfigurationPropsMixin.CloudWatchEncryptionProperty(
                    cloud_watch_encryption_mode="cloudWatchEncryptionMode",
                    kms_key_arn="kmsKeyArn"
                ),
                job_bookmarks_encryption=glue_mixins.CfnSecurityConfigurationPropsMixin.JobBookmarksEncryptionProperty(
                    job_bookmarks_encryption_mode="jobBookmarksEncryptionMode",
                    kms_key_arn="kmsKeyArn"
                ),
                s3_encryptions=[glue_mixins.CfnSecurityConfigurationPropsMixin.S3EncryptionProperty(
                    kms_key_arn="kmsKeyArn",
                    s3_encryption_mode="s3EncryptionMode"
                )]
            ),
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSecurityConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::SecurityConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d195b8b7a23d10809a7fd8836b4b2576f071653ea546d802e7ee5bf03476fee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d50f90986a423c20b2f5b5591a50b54e56cb13db75c459b87751db59049a7c7e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274a6f3e6d3aac31fd057d8d17c5808c20e0b25c0fb19afaac5eb4f5058b4bf6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecurityConfigurationMixinProps:
        return typing.cast(CfnSecurityConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSecurityConfigurationPropsMixin.CloudWatchEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_encryption_mode": "cloudWatchEncryptionMode",
            "kms_key_arn": "kmsKeyArn",
        },
    )
    class CloudWatchEncryptionProperty:
        def __init__(
            self,
            *,
            cloud_watch_encryption_mode: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies how Amazon CloudWatch data should be encrypted.

            :param cloud_watch_encryption_mode: The encryption mode to use for CloudWatch data.
            :param kms_key_arn: The Amazon Resource Name (ARN) of the KMS key to be used to encrypt the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-cloudwatchencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                cloud_watch_encryption_property = glue_mixins.CfnSecurityConfigurationPropsMixin.CloudWatchEncryptionProperty(
                    cloud_watch_encryption_mode="cloudWatchEncryptionMode",
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fc67ee6a23cb7abe617e84146de309053f496562177f0b04ae28e06c2a7ba37)
                check_type(argname="argument cloud_watch_encryption_mode", value=cloud_watch_encryption_mode, expected_type=type_hints["cloud_watch_encryption_mode"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_encryption_mode is not None:
                self._values["cloud_watch_encryption_mode"] = cloud_watch_encryption_mode
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def cloud_watch_encryption_mode(self) -> typing.Optional[builtins.str]:
            '''The encryption mode to use for CloudWatch data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-cloudwatchencryption.html#cfn-glue-securityconfiguration-cloudwatchencryption-cloudwatchencryptionmode
            '''
            result = self._values.get("cloud_watch_encryption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the KMS key to be used to encrypt the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-cloudwatchencryption.html#cfn-glue-securityconfiguration-cloudwatchencryption-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSecurityConfigurationPropsMixin.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_encryption": "cloudWatchEncryption",
            "job_bookmarks_encryption": "jobBookmarksEncryption",
            "s3_encryptions": "s3Encryptions",
        },
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityConfigurationPropsMixin.CloudWatchEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            job_bookmarks_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityConfigurationPropsMixin.JobBookmarksEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_encryptions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityConfigurationPropsMixin.S3EncryptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies an encryption configuration.

            :param cloud_watch_encryption: The encryption configuration for Amazon CloudWatch.
            :param job_bookmarks_encryption: The encryption configuration for job bookmarks.
            :param s3_encryptions: The encyption configuration for Amazon Simple Storage Service (Amazon S3) data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                encryption_configuration_property = glue_mixins.CfnSecurityConfigurationPropsMixin.EncryptionConfigurationProperty(
                    cloud_watch_encryption=glue_mixins.CfnSecurityConfigurationPropsMixin.CloudWatchEncryptionProperty(
                        cloud_watch_encryption_mode="cloudWatchEncryptionMode",
                        kms_key_arn="kmsKeyArn"
                    ),
                    job_bookmarks_encryption=glue_mixins.CfnSecurityConfigurationPropsMixin.JobBookmarksEncryptionProperty(
                        job_bookmarks_encryption_mode="jobBookmarksEncryptionMode",
                        kms_key_arn="kmsKeyArn"
                    ),
                    s3_encryptions=[glue_mixins.CfnSecurityConfigurationPropsMixin.S3EncryptionProperty(
                        kms_key_arn="kmsKeyArn",
                        s3_encryption_mode="s3EncryptionMode"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__933a243e0c37b4012a5703cf6402b3049d11ef6a2f7786f870df9ba18335855a)
                check_type(argname="argument cloud_watch_encryption", value=cloud_watch_encryption, expected_type=type_hints["cloud_watch_encryption"])
                check_type(argname="argument job_bookmarks_encryption", value=job_bookmarks_encryption, expected_type=type_hints["job_bookmarks_encryption"])
                check_type(argname="argument s3_encryptions", value=s3_encryptions, expected_type=type_hints["s3_encryptions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_encryption is not None:
                self._values["cloud_watch_encryption"] = cloud_watch_encryption
            if job_bookmarks_encryption is not None:
                self._values["job_bookmarks_encryption"] = job_bookmarks_encryption
            if s3_encryptions is not None:
                self._values["s3_encryptions"] = s3_encryptions

        @builtins.property
        def cloud_watch_encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigurationPropsMixin.CloudWatchEncryptionProperty"]]:
            '''The encryption configuration for Amazon CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration-cloudwatchencryption
            '''
            result = self._values.get("cloud_watch_encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigurationPropsMixin.CloudWatchEncryptionProperty"]], result)

        @builtins.property
        def job_bookmarks_encryption(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigurationPropsMixin.JobBookmarksEncryptionProperty"]]:
            '''The encryption configuration for job bookmarks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration-jobbookmarksencryption
            '''
            result = self._values.get("job_bookmarks_encryption")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigurationPropsMixin.JobBookmarksEncryptionProperty"]], result)

        @builtins.property
        def s3_encryptions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigurationPropsMixin.S3EncryptionProperty"]]]]:
            '''The encyption configuration for Amazon Simple Storage Service (Amazon S3) data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration-s3encryptions
            '''
            result = self._values.get("s3_encryptions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityConfigurationPropsMixin.S3EncryptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSecurityConfigurationPropsMixin.JobBookmarksEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "job_bookmarks_encryption_mode": "jobBookmarksEncryptionMode",
            "kms_key_arn": "kmsKeyArn",
        },
    )
    class JobBookmarksEncryptionProperty:
        def __init__(
            self,
            *,
            job_bookmarks_encryption_mode: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies how job bookmark data should be encrypted.

            :param job_bookmarks_encryption_mode: The encryption mode to use for job bookmarks data.
            :param kms_key_arn: The Amazon Resource Name (ARN) of the KMS key to be used to encrypt the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-jobbookmarksencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                job_bookmarks_encryption_property = glue_mixins.CfnSecurityConfigurationPropsMixin.JobBookmarksEncryptionProperty(
                    job_bookmarks_encryption_mode="jobBookmarksEncryptionMode",
                    kms_key_arn="kmsKeyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b053996a5cfd9cb423b919ba4cc5583a070bdaa2e319f93b9a6cd95eab116db)
                check_type(argname="argument job_bookmarks_encryption_mode", value=job_bookmarks_encryption_mode, expected_type=type_hints["job_bookmarks_encryption_mode"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if job_bookmarks_encryption_mode is not None:
                self._values["job_bookmarks_encryption_mode"] = job_bookmarks_encryption_mode
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn

        @builtins.property
        def job_bookmarks_encryption_mode(self) -> typing.Optional[builtins.str]:
            '''The encryption mode to use for job bookmarks data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-jobbookmarksencryption.html#cfn-glue-securityconfiguration-jobbookmarksencryption-jobbookmarksencryptionmode
            '''
            result = self._values.get("job_bookmarks_encryption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the KMS key to be used to encrypt the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-jobbookmarksencryption.html#cfn-glue-securityconfiguration-jobbookmarksencryption-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobBookmarksEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnSecurityConfigurationPropsMixin.S3EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "kms_key_arn": "kmsKeyArn",
            "s3_encryption_mode": "s3EncryptionMode",
        },
    )
    class S3EncryptionProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            s3_encryption_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies how Amazon Simple Storage Service (Amazon S3) data should be encrypted.

            :param kms_key_arn: The Amazon Resource Name (ARN) of the KMS key to be used to encrypt the data.
            :param s3_encryption_mode: The encryption mode to use for Amazon S3 data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-s3encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                s3_encryption_property = glue_mixins.CfnSecurityConfigurationPropsMixin.S3EncryptionProperty(
                    kms_key_arn="kmsKeyArn",
                    s3_encryption_mode="s3EncryptionMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__269fa8ea2aa8c1daa8a2b3baf771664f5cd259c8254978237796b438a82b6b86)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument s3_encryption_mode", value=s3_encryption_mode, expected_type=type_hints["s3_encryption_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if s3_encryption_mode is not None:
                self._values["s3_encryption_mode"] = s3_encryption_mode

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the KMS key to be used to encrypt the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-s3encryption.html#cfn-glue-securityconfiguration-s3encryption-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_encryption_mode(self) -> typing.Optional[builtins.str]:
            '''The encryption mode to use for Amazon S3 data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-s3encryption.html#cfn-glue-securityconfiguration-s3encryption-s3encryptionmode
            '''
            result = self._values.get("s3_encryption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "catalog_id": "catalogId",
        "database_name": "databaseName",
        "open_table_format_input": "openTableFormatInput",
        "table_input": "tableInput",
    },
)
class CfnTableMixinProps:
    def __init__(
        self,
        *,
        catalog_id: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        open_table_format_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.OpenTableFormatInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.TableInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTablePropsMixin.

        :param catalog_id: The ID of the Data Catalog in which to create the ``Table`` .
        :param database_name: The name of the database where the table metadata resides. For Hive compatibility, this must be all lowercase.
        :param open_table_format_input: Specifies an ``OpenTableFormatInput`` structure when creating an open format table.
        :param table_input: A structure used to define a table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # parameters: Any
            # skewed_column_value_location_maps: Any
            
            cfn_table_mixin_props = glue_mixins.CfnTableMixinProps(
                catalog_id="catalogId",
                database_name="databaseName",
                open_table_format_input=glue_mixins.CfnTablePropsMixin.OpenTableFormatInputProperty(
                    iceberg_input=glue_mixins.CfnTablePropsMixin.IcebergInputProperty(
                        metadata_operation="metadataOperation",
                        version="version"
                    )
                ),
                table_input=glue_mixins.CfnTablePropsMixin.TableInputProperty(
                    description="description",
                    name="name",
                    owner="owner",
                    parameters=parameters,
                    partition_keys=[glue_mixins.CfnTablePropsMixin.ColumnProperty(
                        comment="comment",
                        name="name",
                        type="type"
                    )],
                    retention=123,
                    storage_descriptor=glue_mixins.CfnTablePropsMixin.StorageDescriptorProperty(
                        bucket_columns=["bucketColumns"],
                        columns=[glue_mixins.CfnTablePropsMixin.ColumnProperty(
                            comment="comment",
                            name="name",
                            type="type"
                        )],
                        compressed=False,
                        input_format="inputFormat",
                        location="location",
                        number_of_buckets=123,
                        output_format="outputFormat",
                        parameters=parameters,
                        schema_reference=glue_mixins.CfnTablePropsMixin.SchemaReferenceProperty(
                            schema_id=glue_mixins.CfnTablePropsMixin.SchemaIdProperty(
                                registry_name="registryName",
                                schema_arn="schemaArn",
                                schema_name="schemaName"
                            ),
                            schema_version_id="schemaVersionId",
                            schema_version_number=123
                        ),
                        serde_info=glue_mixins.CfnTablePropsMixin.SerdeInfoProperty(
                            name="name",
                            parameters=parameters,
                            serialization_library="serializationLibrary"
                        ),
                        skewed_info=glue_mixins.CfnTablePropsMixin.SkewedInfoProperty(
                            skewed_column_names=["skewedColumnNames"],
                            skewed_column_value_location_maps=skewed_column_value_location_maps,
                            skewed_column_values=["skewedColumnValues"]
                        ),
                        sort_columns=[glue_mixins.CfnTablePropsMixin.OrderProperty(
                            column="column",
                            sort_order=123
                        )],
                        stored_as_sub_directories=False
                    ),
                    table_type="tableType",
                    target_table=glue_mixins.CfnTablePropsMixin.TableIdentifierProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        name="name",
                        region="region"
                    ),
                    view_expanded_text="viewExpandedText",
                    view_original_text="viewOriginalText"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39efe7602b3edd447ff6a7f78f878d35dc004419a8a459f476bee165cf7cbd88)
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument open_table_format_input", value=open_table_format_input, expected_type=type_hints["open_table_format_input"])
            check_type(argname="argument table_input", value=table_input, expected_type=type_hints["table_input"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id
        if database_name is not None:
            self._values["database_name"] = database_name
        if open_table_format_input is not None:
            self._values["open_table_format_input"] = open_table_format_input
        if table_input is not None:
            self._values["table_input"] = table_input

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Data Catalog in which to create the ``Table`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-catalogid
        '''
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the database where the table metadata resides.

        For Hive compatibility, this must be all lowercase.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_table_format_input(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.OpenTableFormatInputProperty"]]:
        '''Specifies an ``OpenTableFormatInput`` structure when creating an open format table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-opentableformatinput
        '''
        result = self._values.get("open_table_format_input")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.OpenTableFormatInputProperty"]], result)

    @builtins.property
    def table_input(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.TableInputProperty"]]:
        '''A structure used to define a table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-tableinput
        '''
        result = self._values.get("table_input")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.TableInputProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTableOptimizerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "catalog_id": "catalogId",
        "database_name": "databaseName",
        "table_name": "tableName",
        "table_optimizer_configuration": "tableOptimizerConfiguration",
        "type": "type",
    },
)
class CfnTableOptimizerMixinProps:
    def __init__(
        self,
        *,
        catalog_id: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
        table_optimizer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableOptimizerPropsMixin.TableOptimizerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTableOptimizerPropsMixin.

        :param catalog_id: The catalog ID of the table.
        :param database_name: The name of the database. For Hive compatibility, this is folded to lowercase when it is stored.
        :param table_name: The table name. For Hive compatibility, this must be entirely lowercase.
        :param table_optimizer_configuration: Specifies configuration details of a table optimizer.
        :param type: The type of table optimizer. The valid values are:. - compaction - for managing compaction with a table optimizer. - retention - for managing the retention of snapshot with a table optimizer. - orphan_file_deletion - for managing the deletion of orphan files with a table optimizer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-tableoptimizer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_table_optimizer_mixin_props = glue_mixins.CfnTableOptimizerMixinProps(
                catalog_id="catalogId",
                database_name="databaseName",
                table_name="tableName",
                table_optimizer_configuration=glue_mixins.CfnTableOptimizerPropsMixin.TableOptimizerConfigurationProperty(
                    enabled=False,
                    orphan_file_deletion_configuration=glue_mixins.CfnTableOptimizerPropsMixin.OrphanFileDeletionConfigurationProperty(
                        iceberg_configuration=glue_mixins.CfnTableOptimizerPropsMixin.IcebergConfigurationProperty(
                            location="location",
                            orphan_file_retention_period_in_days=123
                        )
                    ),
                    retention_configuration=glue_mixins.CfnTableOptimizerPropsMixin.RetentionConfigurationProperty(
                        iceberg_configuration=glue_mixins.CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty(
                            clean_expired_files=False,
                            number_of_snapshots_to_retain=123,
                            snapshot_retention_period_in_days=123
                        )
                    ),
                    role_arn="roleArn",
                    vpc_configuration=glue_mixins.CfnTableOptimizerPropsMixin.VpcConfigurationProperty(
                        glue_connection_name="glueConnectionName"
                    )
                ),
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2288a590bd25426f0b125cd6c8907c27e352b057c8d245de6c081367b2df3575)
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument table_optimizer_configuration", value=table_optimizer_configuration, expected_type=type_hints["table_optimizer_configuration"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id
        if database_name is not None:
            self._values["database_name"] = database_name
        if table_name is not None:
            self._values["table_name"] = table_name
        if table_optimizer_configuration is not None:
            self._values["table_optimizer_configuration"] = table_optimizer_configuration
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        '''The catalog ID of the table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-tableoptimizer.html#cfn-glue-tableoptimizer-catalogid
        '''
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the database.

        For Hive compatibility, this is folded to lowercase when it is stored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-tableoptimizer.html#cfn-glue-tableoptimizer-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The table name.

        For Hive compatibility, this must be entirely lowercase.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-tableoptimizer.html#cfn-glue-tableoptimizer-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_optimizer_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.TableOptimizerConfigurationProperty"]]:
        '''Specifies configuration details of a table optimizer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-tableoptimizer.html#cfn-glue-tableoptimizer-tableoptimizerconfiguration
        '''
        result = self._values.get("table_optimizer_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.TableOptimizerConfigurationProperty"]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of table optimizer. The valid values are:.

        - compaction - for managing compaction with a table optimizer.
        - retention - for managing the retention of snapshot with a table optimizer.
        - orphan_file_deletion - for managing the deletion of orphan files with a table optimizer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-tableoptimizer.html#cfn-glue-tableoptimizer-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableOptimizerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTableOptimizerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTableOptimizerPropsMixin",
):
    '''An AWS Glue resource for enabling table optimizers to improve read performance for open table formats.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-tableoptimizer.html
    :cloudformationResource: AWS::Glue::TableOptimizer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_table_optimizer_props_mixin = glue_mixins.CfnTableOptimizerPropsMixin(glue_mixins.CfnTableOptimizerMixinProps(
            catalog_id="catalogId",
            database_name="databaseName",
            table_name="tableName",
            table_optimizer_configuration=glue_mixins.CfnTableOptimizerPropsMixin.TableOptimizerConfigurationProperty(
                enabled=False,
                orphan_file_deletion_configuration=glue_mixins.CfnTableOptimizerPropsMixin.OrphanFileDeletionConfigurationProperty(
                    iceberg_configuration=glue_mixins.CfnTableOptimizerPropsMixin.IcebergConfigurationProperty(
                        location="location",
                        orphan_file_retention_period_in_days=123
                    )
                ),
                retention_configuration=glue_mixins.CfnTableOptimizerPropsMixin.RetentionConfigurationProperty(
                    iceberg_configuration=glue_mixins.CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty(
                        clean_expired_files=False,
                        number_of_snapshots_to_retain=123,
                        snapshot_retention_period_in_days=123
                    )
                ),
                role_arn="roleArn",
                vpc_configuration=glue_mixins.CfnTableOptimizerPropsMixin.VpcConfigurationProperty(
                    glue_connection_name="glueConnectionName"
                )
            ),
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTableOptimizerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::TableOptimizer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98b69c81bdbf2fe8ccabc57ef0eb76f58f377d36abf0b874d713a52d8328373)
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
            type_hints = typing.get_type_hints(_typecheckingstub__567d2637f8883062193f007ddb6c26df7f2ccd508bbda2f5f762b6be0f252b27)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347bd9f930d991dfbd498d98430b1919ddb9d056742f15d6b131ba3e84823869)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTableOptimizerMixinProps:
        return typing.cast(CfnTableOptimizerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTableOptimizerPropsMixin.IcebergConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "location": "location",
            "orphan_file_retention_period_in_days": "orphanFileRetentionPeriodInDays",
        },
    )
    class IcebergConfigurationProperty:
        def __init__(
            self,
            *,
            location: typing.Optional[builtins.str] = None,
            orphan_file_retention_period_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''IcebergConfiguration is a property type within the ``AWS::Glue::TableOptimizer`` resource in AWS CloudFormation.

            This configuration is used when setting up table optimization for Iceberg tables in AWS Glue .

            :param location: Specifies a directory in which to look for orphan files (defaults to the table's location). You may choose a sub-directory rather than the top-level table location.
            :param orphan_file_retention_period_in_days: The specific number of days you want to keep the orphan files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-icebergconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                iceberg_configuration_property = glue_mixins.CfnTableOptimizerPropsMixin.IcebergConfigurationProperty(
                    location="location",
                    orphan_file_retention_period_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c2dc7a846e72daec956b132882c0d9d234011ba11208937495a60cfdb5b0db4)
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument orphan_file_retention_period_in_days", value=orphan_file_retention_period_in_days, expected_type=type_hints["orphan_file_retention_period_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if location is not None:
                self._values["location"] = location
            if orphan_file_retention_period_in_days is not None:
                self._values["orphan_file_retention_period_in_days"] = orphan_file_retention_period_in_days

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''Specifies a directory in which to look for orphan files (defaults to the table's location).

            You may choose a sub-directory rather than the top-level table location.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-icebergconfiguration.html#cfn-glue-tableoptimizer-icebergconfiguration-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def orphan_file_retention_period_in_days(self) -> typing.Optional[jsii.Number]:
            '''The specific number of days you want to keep the orphan files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-icebergconfiguration.html#cfn-glue-tableoptimizer-icebergconfiguration-orphanfileretentionperiodindays
            '''
            result = self._values.get("orphan_file_retention_period_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IcebergConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "clean_expired_files": "cleanExpiredFiles",
            "number_of_snapshots_to_retain": "numberOfSnapshotsToRetain",
            "snapshot_retention_period_in_days": "snapshotRetentionPeriodInDays",
        },
    )
    class IcebergRetentionConfigurationProperty:
        def __init__(
            self,
            *,
            clean_expired_files: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            number_of_snapshots_to_retain: typing.Optional[jsii.Number] = None,
            snapshot_retention_period_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param clean_expired_files: 
            :param number_of_snapshots_to_retain: 
            :param snapshot_retention_period_in_days: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-icebergretentionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                iceberg_retention_configuration_property = glue_mixins.CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty(
                    clean_expired_files=False,
                    number_of_snapshots_to_retain=123,
                    snapshot_retention_period_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9769028b2b696e9a2a16d657b89885d110bbcc77a6379765294d950d8fa3311b)
                check_type(argname="argument clean_expired_files", value=clean_expired_files, expected_type=type_hints["clean_expired_files"])
                check_type(argname="argument number_of_snapshots_to_retain", value=number_of_snapshots_to_retain, expected_type=type_hints["number_of_snapshots_to_retain"])
                check_type(argname="argument snapshot_retention_period_in_days", value=snapshot_retention_period_in_days, expected_type=type_hints["snapshot_retention_period_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if clean_expired_files is not None:
                self._values["clean_expired_files"] = clean_expired_files
            if number_of_snapshots_to_retain is not None:
                self._values["number_of_snapshots_to_retain"] = number_of_snapshots_to_retain
            if snapshot_retention_period_in_days is not None:
                self._values["snapshot_retention_period_in_days"] = snapshot_retention_period_in_days

        @builtins.property
        def clean_expired_files(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-icebergretentionconfiguration.html#cfn-glue-tableoptimizer-icebergretentionconfiguration-cleanexpiredfiles
            '''
            result = self._values.get("clean_expired_files")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def number_of_snapshots_to_retain(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-icebergretentionconfiguration.html#cfn-glue-tableoptimizer-icebergretentionconfiguration-numberofsnapshotstoretain
            '''
            result = self._values.get("number_of_snapshots_to_retain")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def snapshot_retention_period_in_days(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-icebergretentionconfiguration.html#cfn-glue-tableoptimizer-icebergretentionconfiguration-snapshotretentionperiodindays
            '''
            result = self._values.get("snapshot_retention_period_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IcebergRetentionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTableOptimizerPropsMixin.OrphanFileDeletionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"iceberg_configuration": "icebergConfiguration"},
    )
    class OrphanFileDeletionConfigurationProperty:
        def __init__(
            self,
            *,
            iceberg_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableOptimizerPropsMixin.IcebergConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration for removing files that are are not tracked by the Iceberg table metadata, and are older than your configured age limit.

            This configuration helps optimize storage usage and costs by automatically cleaning up files that are no longer needed by the table.

            :param iceberg_configuration: The ``IcebergConfiguration`` property helps optimize your Iceberg tables in AWS Glue by allowing you to specify format-specific settings that control how data is stored, compressed, and managed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-orphanfiledeletionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                orphan_file_deletion_configuration_property = glue_mixins.CfnTableOptimizerPropsMixin.OrphanFileDeletionConfigurationProperty(
                    iceberg_configuration=glue_mixins.CfnTableOptimizerPropsMixin.IcebergConfigurationProperty(
                        location="location",
                        orphan_file_retention_period_in_days=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51cc451365451651f57ac818436df59311ea735a7f33b00e3def427b487ccc0e)
                check_type(argname="argument iceberg_configuration", value=iceberg_configuration, expected_type=type_hints["iceberg_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iceberg_configuration is not None:
                self._values["iceberg_configuration"] = iceberg_configuration

        @builtins.property
        def iceberg_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.IcebergConfigurationProperty"]]:
            '''The ``IcebergConfiguration`` property helps optimize your Iceberg tables in AWS Glue by allowing you to specify format-specific settings that control how data is stored, compressed, and managed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-orphanfiledeletionconfiguration.html#cfn-glue-tableoptimizer-orphanfiledeletionconfiguration-icebergconfiguration
            '''
            result = self._values.get("iceberg_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.IcebergConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrphanFileDeletionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTableOptimizerPropsMixin.RetentionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"iceberg_configuration": "icebergConfiguration"},
    )
    class RetentionConfigurationProperty:
        def __init__(
            self,
            *,
            iceberg_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for a snapshot retention optimizer for Apache Iceberg tables.

            :param iceberg_configuration: The configuration for an Iceberg snapshot retention optimizer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-retentionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                retention_configuration_property = glue_mixins.CfnTableOptimizerPropsMixin.RetentionConfigurationProperty(
                    iceberg_configuration=glue_mixins.CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty(
                        clean_expired_files=False,
                        number_of_snapshots_to_retain=123,
                        snapshot_retention_period_in_days=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__755b2d9e6566b6fc82efcc513a3d36bb9059e29e9c75ac2b8e8deb7f8efab6ac)
                check_type(argname="argument iceberg_configuration", value=iceberg_configuration, expected_type=type_hints["iceberg_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iceberg_configuration is not None:
                self._values["iceberg_configuration"] = iceberg_configuration

        @builtins.property
        def iceberg_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty"]]:
            '''The configuration for an Iceberg snapshot retention optimizer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-retentionconfiguration.html#cfn-glue-tableoptimizer-retentionconfiguration-icebergconfiguration
            '''
            result = self._values.get("iceberg_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTableOptimizerPropsMixin.TableOptimizerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "orphan_file_deletion_configuration": "orphanFileDeletionConfiguration",
            "retention_configuration": "retentionConfiguration",
            "role_arn": "roleArn",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class TableOptimizerConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            orphan_file_deletion_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableOptimizerPropsMixin.OrphanFileDeletionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retention_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableOptimizerPropsMixin.RetentionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTableOptimizerPropsMixin.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies configuration details of a table optimizer.

            :param enabled: Whether the table optimization is enabled.
            :param orphan_file_deletion_configuration: ``OrphanFileDeletionConfiguration`` is a property that can be included within the TableOptimizer resource. It controls the automatic deletion of orphaned files - files that are not tracked by the table metadata, and older than the configured age limit.
            :param retention_configuration: The configuration for a snapshot retention optimizer for Apache Iceberg tables.
            :param role_arn: A role passed by the caller which gives the service permission to update the resources associated with the optimizer on the caller's behalf.
            :param vpc_configuration: An object that describes the VPC configuration for a table optimizer. This configuration is necessary to perform optimization on tables that are in a customer VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-tableoptimizerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                table_optimizer_configuration_property = glue_mixins.CfnTableOptimizerPropsMixin.TableOptimizerConfigurationProperty(
                    enabled=False,
                    orphan_file_deletion_configuration=glue_mixins.CfnTableOptimizerPropsMixin.OrphanFileDeletionConfigurationProperty(
                        iceberg_configuration=glue_mixins.CfnTableOptimizerPropsMixin.IcebergConfigurationProperty(
                            location="location",
                            orphan_file_retention_period_in_days=123
                        )
                    ),
                    retention_configuration=glue_mixins.CfnTableOptimizerPropsMixin.RetentionConfigurationProperty(
                        iceberg_configuration=glue_mixins.CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty(
                            clean_expired_files=False,
                            number_of_snapshots_to_retain=123,
                            snapshot_retention_period_in_days=123
                        )
                    ),
                    role_arn="roleArn",
                    vpc_configuration=glue_mixins.CfnTableOptimizerPropsMixin.VpcConfigurationProperty(
                        glue_connection_name="glueConnectionName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49886016b340732b0c6d11209f1170f65c644fd6c9829e2b2773dcecf528fb62)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument orphan_file_deletion_configuration", value=orphan_file_deletion_configuration, expected_type=type_hints["orphan_file_deletion_configuration"])
                check_type(argname="argument retention_configuration", value=retention_configuration, expected_type=type_hints["retention_configuration"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if orphan_file_deletion_configuration is not None:
                self._values["orphan_file_deletion_configuration"] = orphan_file_deletion_configuration
            if retention_configuration is not None:
                self._values["retention_configuration"] = retention_configuration
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether the table optimization is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-tableoptimizerconfiguration.html#cfn-glue-tableoptimizer-tableoptimizerconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def orphan_file_deletion_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.OrphanFileDeletionConfigurationProperty"]]:
            '''``OrphanFileDeletionConfiguration`` is a property that can be included within the TableOptimizer resource.

            It controls the automatic deletion of orphaned files - files that are not tracked by the table metadata, and older than the configured age limit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-tableoptimizerconfiguration.html#cfn-glue-tableoptimizer-tableoptimizerconfiguration-orphanfiledeletionconfiguration
            '''
            result = self._values.get("orphan_file_deletion_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.OrphanFileDeletionConfigurationProperty"]], result)

        @builtins.property
        def retention_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.RetentionConfigurationProperty"]]:
            '''The configuration for a snapshot retention optimizer for Apache Iceberg tables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-tableoptimizerconfiguration.html#cfn-glue-tableoptimizer-tableoptimizerconfiguration-retentionconfiguration
            '''
            result = self._values.get("retention_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.RetentionConfigurationProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''A role passed by the caller which gives the service permission to update the resources associated with the optimizer on the caller's behalf.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-tableoptimizerconfiguration.html#cfn-glue-tableoptimizer-tableoptimizerconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.VpcConfigurationProperty"]]:
            '''An object that describes the VPC configuration for a table optimizer.

            This configuration is necessary to perform optimization on tables that are in a customer VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-tableoptimizerconfiguration.html#cfn-glue-tableoptimizer-tableoptimizerconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTableOptimizerPropsMixin.VpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableOptimizerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTableOptimizerPropsMixin.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"glue_connection_name": "glueConnectionName"},
    )
    class VpcConfigurationProperty:
        def __init__(
            self,
            *,
            glue_connection_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that describes the VPC configuration for a table optimizer.

            This configuration is necessary to perform optimization on tables that are in a customer VPC.

            :param glue_connection_name: The name of the AWS Glue connection used for the VPC for the table optimizer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                vpc_configuration_property = glue_mixins.CfnTableOptimizerPropsMixin.VpcConfigurationProperty(
                    glue_connection_name="glueConnectionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a870d8c9869be1dac233af5c1a303dfca170f0bfd64e76f07f5c88223d0afa2)
                check_type(argname="argument glue_connection_name", value=glue_connection_name, expected_type=type_hints["glue_connection_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if glue_connection_name is not None:
                self._values["glue_connection_name"] = glue_connection_name

        @builtins.property
        def glue_connection_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS Glue connection used for the VPC for the table optimizer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-tableoptimizer-vpcconfiguration.html#cfn-glue-tableoptimizer-vpcconfiguration-glueconnectionname
            '''
            result = self._values.get("glue_connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnTablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin",
):
    '''The ``AWS::Glue::Table`` resource specifies tabular data in the AWS Glue data catalog.

    For more information, see `Defining Tables in the AWS Glue Data Catalog <https://docs.aws.amazon.com/glue/latest/dg/tables-described.html>`_ and `Table Structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-tables.html#aws-glue-api-catalog-tables-Table>`_ in the *AWS Glue Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html
    :cloudformationResource: AWS::Glue::Table
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # parameters: Any
        # skewed_column_value_location_maps: Any
        
        cfn_table_props_mixin = glue_mixins.CfnTablePropsMixin(glue_mixins.CfnTableMixinProps(
            catalog_id="catalogId",
            database_name="databaseName",
            open_table_format_input=glue_mixins.CfnTablePropsMixin.OpenTableFormatInputProperty(
                iceberg_input=glue_mixins.CfnTablePropsMixin.IcebergInputProperty(
                    metadata_operation="metadataOperation",
                    version="version"
                )
            ),
            table_input=glue_mixins.CfnTablePropsMixin.TableInputProperty(
                description="description",
                name="name",
                owner="owner",
                parameters=parameters,
                partition_keys=[glue_mixins.CfnTablePropsMixin.ColumnProperty(
                    comment="comment",
                    name="name",
                    type="type"
                )],
                retention=123,
                storage_descriptor=glue_mixins.CfnTablePropsMixin.StorageDescriptorProperty(
                    bucket_columns=["bucketColumns"],
                    columns=[glue_mixins.CfnTablePropsMixin.ColumnProperty(
                        comment="comment",
                        name="name",
                        type="type"
                    )],
                    compressed=False,
                    input_format="inputFormat",
                    location="location",
                    number_of_buckets=123,
                    output_format="outputFormat",
                    parameters=parameters,
                    schema_reference=glue_mixins.CfnTablePropsMixin.SchemaReferenceProperty(
                        schema_id=glue_mixins.CfnTablePropsMixin.SchemaIdProperty(
                            registry_name="registryName",
                            schema_arn="schemaArn",
                            schema_name="schemaName"
                        ),
                        schema_version_id="schemaVersionId",
                        schema_version_number=123
                    ),
                    serde_info=glue_mixins.CfnTablePropsMixin.SerdeInfoProperty(
                        name="name",
                        parameters=parameters,
                        serialization_library="serializationLibrary"
                    ),
                    skewed_info=glue_mixins.CfnTablePropsMixin.SkewedInfoProperty(
                        skewed_column_names=["skewedColumnNames"],
                        skewed_column_value_location_maps=skewed_column_value_location_maps,
                        skewed_column_values=["skewedColumnValues"]
                    ),
                    sort_columns=[glue_mixins.CfnTablePropsMixin.OrderProperty(
                        column="column",
                        sort_order=123
                    )],
                    stored_as_sub_directories=False
                ),
                table_type="tableType",
                target_table=glue_mixins.CfnTablePropsMixin.TableIdentifierProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    name="name",
                    region="region"
                ),
                view_expanded_text="viewExpandedText",
                view_original_text="viewOriginalText"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTableMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Table``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac29ac2aee8e348c107ce5e7c900056b1b41a4d0ed13f725c5b41d4c710be272)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5755d7bd23ad33beb872a24cdf149ed4eb5ac674e1e239915044466e7b9301c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__708092ebd9ff582423c84e64cf4eb057e949e0dbb69d7692f9a3ae49c3d43a49)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTableMixinProps:
        return typing.cast(CfnTableMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.ColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"comment": "comment", "name": "name", "type": "type"},
    )
    class ColumnProperty:
        def __init__(
            self,
            *,
            comment: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A column in a ``Table`` .

            :param comment: A free-form text comment.
            :param name: The name of the ``Column`` .
            :param type: The data type of the ``Column`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                column_property = glue_mixins.CfnTablePropsMixin.ColumnProperty(
                    comment="comment",
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c0872e61b96fb59ca2908ab54fb2076789e5b568bd9e0fd22b9f210f7634f0a)
                check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comment is not None:
                self._values["comment"] = comment
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            '''A free-form text comment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html#cfn-glue-table-column-comment
            '''
            result = self._values.get("comment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the ``Column`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html#cfn-glue-table-column-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The data type of the ``Column`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html#cfn-glue-table-column-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.IcebergInputProperty",
        jsii_struct_bases=[],
        name_mapping={"metadata_operation": "metadataOperation", "version": "version"},
    )
    class IcebergInputProperty:
        def __init__(
            self,
            *,
            metadata_operation: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an input structure that defines an Apache Iceberg metadata table.

            :param metadata_operation: A required metadata operation. Can only be set to CREATE.
            :param version: The table version for the Iceberg table. Defaults to 2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-iceberginput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                iceberg_input_property = glue_mixins.CfnTablePropsMixin.IcebergInputProperty(
                    metadata_operation="metadataOperation",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff52173338a2335012058eadcc7fe31070b4a0d890b65481035d0cdbe42314a4)
                check_type(argname="argument metadata_operation", value=metadata_operation, expected_type=type_hints["metadata_operation"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metadata_operation is not None:
                self._values["metadata_operation"] = metadata_operation
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def metadata_operation(self) -> typing.Optional[builtins.str]:
            '''A required metadata operation.

            Can only be set to CREATE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-iceberginput.html#cfn-glue-table-iceberginput-metadataoperation
            '''
            result = self._values.get("metadata_operation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The table version for the Iceberg table.

            Defaults to 2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-iceberginput.html#cfn-glue-table-iceberginput-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IcebergInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.OpenTableFormatInputProperty",
        jsii_struct_bases=[],
        name_mapping={"iceberg_input": "icebergInput"},
    )
    class OpenTableFormatInputProperty:
        def __init__(
            self,
            *,
            iceberg_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.IcebergInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies an ``OpenTableFormatInput`` structure when creating an open format table.

            :param iceberg_input: Specifies an ``IcebergInput`` structure that defines an Apache Iceberg metadata table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-opentableformatinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                open_table_format_input_property = glue_mixins.CfnTablePropsMixin.OpenTableFormatInputProperty(
                    iceberg_input=glue_mixins.CfnTablePropsMixin.IcebergInputProperty(
                        metadata_operation="metadataOperation",
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a11588071664058b0a74a27ad541ff4122016a11679d3028f2aa6d38a8816d7)
                check_type(argname="argument iceberg_input", value=iceberg_input, expected_type=type_hints["iceberg_input"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iceberg_input is not None:
                self._values["iceberg_input"] = iceberg_input

        @builtins.property
        def iceberg_input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.IcebergInputProperty"]]:
            '''Specifies an ``IcebergInput`` structure that defines an Apache Iceberg metadata table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-opentableformatinput.html#cfn-glue-table-opentableformatinput-iceberginput
            '''
            result = self._values.get("iceberg_input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.IcebergInputProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenTableFormatInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.OrderProperty",
        jsii_struct_bases=[],
        name_mapping={"column": "column", "sort_order": "sortOrder"},
    )
    class OrderProperty:
        def __init__(
            self,
            *,
            column: typing.Optional[builtins.str] = None,
            sort_order: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the sort order of a sorted column.

            :param column: The name of the column.
            :param sort_order: Indicates that the column is sorted in ascending order ( ``== 1`` ), or in descending order ( ``==0`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-order.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                order_property = glue_mixins.CfnTablePropsMixin.OrderProperty(
                    column="column",
                    sort_order=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78e3da3ea55aa083b9b87a06342d5dc4fd1cb14cb8d49cf0e661bdb239ec5479)
                check_type(argname="argument column", value=column, expected_type=type_hints["column"])
                check_type(argname="argument sort_order", value=sort_order, expected_type=type_hints["sort_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column is not None:
                self._values["column"] = column
            if sort_order is not None:
                self._values["sort_order"] = sort_order

        @builtins.property
        def column(self) -> typing.Optional[builtins.str]:
            '''The name of the column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-order.html#cfn-glue-table-order-column
            '''
            result = self._values.get("column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sort_order(self) -> typing.Optional[jsii.Number]:
            '''Indicates that the column is sorted in ascending order ( ``== 1`` ), or in descending order ( ``==0`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-order.html#cfn-glue-table-order-sortorder
            '''
            result = self._values.get("sort_order")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.SchemaIdProperty",
        jsii_struct_bases=[],
        name_mapping={
            "registry_name": "registryName",
            "schema_arn": "schemaArn",
            "schema_name": "schemaName",
        },
    )
    class SchemaIdProperty:
        def __init__(
            self,
            *,
            registry_name: typing.Optional[builtins.str] = None,
            schema_arn: typing.Optional[builtins.str] = None,
            schema_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains schema identity fields.

            Either this or the ``SchemaVersionId`` has to be
            provided.

            :param registry_name: The name of the schema registry that contains the schema.
            :param schema_arn: The Amazon Resource Name (ARN) of the schema. One of ``SchemaArn`` or ``SchemaName`` has to be provided.
            :param schema_name: The name of the schema. One of ``SchemaArn`` or ``SchemaName`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-schemaid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                schema_id_property = glue_mixins.CfnTablePropsMixin.SchemaIdProperty(
                    registry_name="registryName",
                    schema_arn="schemaArn",
                    schema_name="schemaName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__278a952c33518316f3375c7bc60d005b8610d9b32cbb52d594a6f69bc30cc2e3)
                check_type(argname="argument registry_name", value=registry_name, expected_type=type_hints["registry_name"])
                check_type(argname="argument schema_arn", value=schema_arn, expected_type=type_hints["schema_arn"])
                check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if registry_name is not None:
                self._values["registry_name"] = registry_name
            if schema_arn is not None:
                self._values["schema_arn"] = schema_arn
            if schema_name is not None:
                self._values["schema_name"] = schema_name

        @builtins.property
        def registry_name(self) -> typing.Optional[builtins.str]:
            '''The name of the schema registry that contains the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-schemaid.html#cfn-glue-table-schemaid-registryname
            '''
            result = self._values.get("registry_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the schema.

            One of ``SchemaArn`` or ``SchemaName`` has to be
            provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-schemaid.html#cfn-glue-table-schemaid-schemaarn
            '''
            result = self._values.get("schema_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_name(self) -> typing.Optional[builtins.str]:
            '''The name of the schema.

            One of ``SchemaArn`` or ``SchemaName`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-schemaid.html#cfn-glue-table-schemaid-schemaname
            '''
            result = self._values.get("schema_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.SchemaReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "schema_id": "schemaId",
            "schema_version_id": "schemaVersionId",
            "schema_version_number": "schemaVersionNumber",
        },
    )
    class SchemaReferenceProperty:
        def __init__(
            self,
            *,
            schema_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.SchemaIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            schema_version_id: typing.Optional[builtins.str] = None,
            schema_version_number: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that references a schema stored in the AWS Glue Schema Registry.

            :param schema_id: A structure that contains schema identity fields. Either this or the ``SchemaVersionId`` has to be provided.
            :param schema_version_id: The unique ID assigned to a version of the schema. Either this or the ``SchemaId`` has to be provided.
            :param schema_version_number: The version number of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-schemareference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                schema_reference_property = glue_mixins.CfnTablePropsMixin.SchemaReferenceProperty(
                    schema_id=glue_mixins.CfnTablePropsMixin.SchemaIdProperty(
                        registry_name="registryName",
                        schema_arn="schemaArn",
                        schema_name="schemaName"
                    ),
                    schema_version_id="schemaVersionId",
                    schema_version_number=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87dd2ad26e62732f62427cc36c213489a0fce8b8d380769e9401b91436c7c66e)
                check_type(argname="argument schema_id", value=schema_id, expected_type=type_hints["schema_id"])
                check_type(argname="argument schema_version_id", value=schema_version_id, expected_type=type_hints["schema_version_id"])
                check_type(argname="argument schema_version_number", value=schema_version_number, expected_type=type_hints["schema_version_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if schema_id is not None:
                self._values["schema_id"] = schema_id
            if schema_version_id is not None:
                self._values["schema_version_id"] = schema_version_id
            if schema_version_number is not None:
                self._values["schema_version_number"] = schema_version_number

        @builtins.property
        def schema_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SchemaIdProperty"]]:
            '''A structure that contains schema identity fields.

            Either this or the ``SchemaVersionId`` has to be
            provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-schemareference.html#cfn-glue-table-schemareference-schemaid
            '''
            result = self._values.get("schema_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SchemaIdProperty"]], result)

        @builtins.property
        def schema_version_id(self) -> typing.Optional[builtins.str]:
            '''The unique ID assigned to a version of the schema.

            Either this or the ``SchemaId`` has to be provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-schemareference.html#cfn-glue-table-schemareference-schemaversionid
            '''
            result = self._values.get("schema_version_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schema_version_number(self) -> typing.Optional[jsii.Number]:
            '''The version number of the schema.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-schemareference.html#cfn-glue-table-schemareference-schemaversionnumber
            '''
            result = self._values.get("schema_version_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.SerdeInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "parameters": "parameters",
            "serialization_library": "serializationLibrary",
        },
    )
    class SerdeInfoProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
            serialization_library: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a serialization/deserialization program (SerDe) that serves as an extractor and loader.

            :param name: Name of the SerDe.
            :param parameters: These key-value pairs define initialization parameters for the SerDe.
            :param serialization_library: Usually the class that implements the SerDe. An example is ``org.apache.hadoop.hive.serde2.columnar.ColumnarSerDe`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # parameters: Any
                
                serde_info_property = glue_mixins.CfnTablePropsMixin.SerdeInfoProperty(
                    name="name",
                    parameters=parameters,
                    serialization_library="serializationLibrary"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cae0300efffae6e2e65441157df82805e5493db03b4055cc5f9f9161b952e968)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument serialization_library", value=serialization_library, expected_type=type_hints["serialization_library"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if parameters is not None:
                self._values["parameters"] = parameters
            if serialization_library is not None:
                self._values["serialization_library"] = serialization_library

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of the SerDe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html#cfn-glue-table-serdeinfo-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''These key-value pairs define initialization parameters for the SerDe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html#cfn-glue-table-serdeinfo-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def serialization_library(self) -> typing.Optional[builtins.str]:
            '''Usually the class that implements the SerDe.

            An example is ``org.apache.hadoop.hive.serde2.columnar.ColumnarSerDe`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html#cfn-glue-table-serdeinfo-serializationlibrary
            '''
            result = self._values.get("serialization_library")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SerdeInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.SkewedInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "skewed_column_names": "skewedColumnNames",
            "skewed_column_value_location_maps": "skewedColumnValueLocationMaps",
            "skewed_column_values": "skewedColumnValues",
        },
    )
    class SkewedInfoProperty:
        def __init__(
            self,
            *,
            skewed_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            skewed_column_value_location_maps: typing.Any = None,
            skewed_column_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies skewed values in a table.

            Skewed values are those that occur with very high frequency.

            :param skewed_column_names: A list of names of columns that contain skewed values.
            :param skewed_column_value_location_maps: A mapping of skewed values to the columns that contain them.
            :param skewed_column_values: A list of values that appear so frequently as to be considered skewed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-skewedinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # skewed_column_value_location_maps: Any
                
                skewed_info_property = glue_mixins.CfnTablePropsMixin.SkewedInfoProperty(
                    skewed_column_names=["skewedColumnNames"],
                    skewed_column_value_location_maps=skewed_column_value_location_maps,
                    skewed_column_values=["skewedColumnValues"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba0420f60b7fe7d33df8f82bea58ed8deab3a5a5af2431e13ce67363fa6d90e3)
                check_type(argname="argument skewed_column_names", value=skewed_column_names, expected_type=type_hints["skewed_column_names"])
                check_type(argname="argument skewed_column_value_location_maps", value=skewed_column_value_location_maps, expected_type=type_hints["skewed_column_value_location_maps"])
                check_type(argname="argument skewed_column_values", value=skewed_column_values, expected_type=type_hints["skewed_column_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if skewed_column_names is not None:
                self._values["skewed_column_names"] = skewed_column_names
            if skewed_column_value_location_maps is not None:
                self._values["skewed_column_value_location_maps"] = skewed_column_value_location_maps
            if skewed_column_values is not None:
                self._values["skewed_column_values"] = skewed_column_values

        @builtins.property
        def skewed_column_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of names of columns that contain skewed values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-skewedinfo.html#cfn-glue-table-skewedinfo-skewedcolumnnames
            '''
            result = self._values.get("skewed_column_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def skewed_column_value_location_maps(self) -> typing.Any:
            '''A mapping of skewed values to the columns that contain them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-skewedinfo.html#cfn-glue-table-skewedinfo-skewedcolumnvaluelocationmaps
            '''
            result = self._values.get("skewed_column_value_location_maps")
            return typing.cast(typing.Any, result)

        @builtins.property
        def skewed_column_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of values that appear so frequently as to be considered skewed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-skewedinfo.html#cfn-glue-table-skewedinfo-skewedcolumnvalues
            '''
            result = self._values.get("skewed_column_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SkewedInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.StorageDescriptorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_columns": "bucketColumns",
            "columns": "columns",
            "compressed": "compressed",
            "input_format": "inputFormat",
            "location": "location",
            "number_of_buckets": "numberOfBuckets",
            "output_format": "outputFormat",
            "parameters": "parameters",
            "schema_reference": "schemaReference",
            "serde_info": "serdeInfo",
            "skewed_info": "skewedInfo",
            "sort_columns": "sortColumns",
            "stored_as_sub_directories": "storedAsSubDirectories",
        },
    )
    class StorageDescriptorProperty:
        def __init__(
            self,
            *,
            bucket_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
            columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            compressed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            input_format: typing.Optional[builtins.str] = None,
            location: typing.Optional[builtins.str] = None,
            number_of_buckets: typing.Optional[jsii.Number] = None,
            output_format: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
            schema_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.SchemaReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            serde_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.SerdeInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            skewed_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.SkewedInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sort_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.OrderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            stored_as_sub_directories: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes the physical storage of table data.

            :param bucket_columns: A list of reducer grouping columns, clustering columns, and bucketing columns in the table.
            :param columns: A list of the ``Columns`` in the table.
            :param compressed: ``True`` if the data in the table is compressed, or ``False`` if not.
            :param input_format: The input format: ``SequenceFileInputFormat`` (binary), or ``TextInputFormat`` , or a custom format.
            :param location: The physical location of the table. By default, this takes the form of the warehouse location, followed by the database location in the warehouse, followed by the table name.
            :param number_of_buckets: Must be specified if the table contains any dimension columns.
            :param output_format: The output format: ``SequenceFileOutputFormat`` (binary), or ``IgnoreKeyTextOutputFormat`` , or a custom format.
            :param parameters: The user-supplied properties in key-value form.
            :param schema_reference: An object that references a schema stored in the AWS Glue Schema Registry.
            :param serde_info: The serialization/deserialization (SerDe) information.
            :param skewed_info: The information about values that appear frequently in a column (skewed values).
            :param sort_columns: A list specifying the sort order of each bucket in the table.
            :param stored_as_sub_directories: ``True`` if the table data is stored in subdirectories, or ``False`` if not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # parameters: Any
                # skewed_column_value_location_maps: Any
                
                storage_descriptor_property = glue_mixins.CfnTablePropsMixin.StorageDescriptorProperty(
                    bucket_columns=["bucketColumns"],
                    columns=[glue_mixins.CfnTablePropsMixin.ColumnProperty(
                        comment="comment",
                        name="name",
                        type="type"
                    )],
                    compressed=False,
                    input_format="inputFormat",
                    location="location",
                    number_of_buckets=123,
                    output_format="outputFormat",
                    parameters=parameters,
                    schema_reference=glue_mixins.CfnTablePropsMixin.SchemaReferenceProperty(
                        schema_id=glue_mixins.CfnTablePropsMixin.SchemaIdProperty(
                            registry_name="registryName",
                            schema_arn="schemaArn",
                            schema_name="schemaName"
                        ),
                        schema_version_id="schemaVersionId",
                        schema_version_number=123
                    ),
                    serde_info=glue_mixins.CfnTablePropsMixin.SerdeInfoProperty(
                        name="name",
                        parameters=parameters,
                        serialization_library="serializationLibrary"
                    ),
                    skewed_info=glue_mixins.CfnTablePropsMixin.SkewedInfoProperty(
                        skewed_column_names=["skewedColumnNames"],
                        skewed_column_value_location_maps=skewed_column_value_location_maps,
                        skewed_column_values=["skewedColumnValues"]
                    ),
                    sort_columns=[glue_mixins.CfnTablePropsMixin.OrderProperty(
                        column="column",
                        sort_order=123
                    )],
                    stored_as_sub_directories=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1fe8d8c8ba6a1419d32a1f9faf06d343f7de48a1a4eeb38620d610933c3a02d4)
                check_type(argname="argument bucket_columns", value=bucket_columns, expected_type=type_hints["bucket_columns"])
                check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
                check_type(argname="argument compressed", value=compressed, expected_type=type_hints["compressed"])
                check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument number_of_buckets", value=number_of_buckets, expected_type=type_hints["number_of_buckets"])
                check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument schema_reference", value=schema_reference, expected_type=type_hints["schema_reference"])
                check_type(argname="argument serde_info", value=serde_info, expected_type=type_hints["serde_info"])
                check_type(argname="argument skewed_info", value=skewed_info, expected_type=type_hints["skewed_info"])
                check_type(argname="argument sort_columns", value=sort_columns, expected_type=type_hints["sort_columns"])
                check_type(argname="argument stored_as_sub_directories", value=stored_as_sub_directories, expected_type=type_hints["stored_as_sub_directories"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_columns is not None:
                self._values["bucket_columns"] = bucket_columns
            if columns is not None:
                self._values["columns"] = columns
            if compressed is not None:
                self._values["compressed"] = compressed
            if input_format is not None:
                self._values["input_format"] = input_format
            if location is not None:
                self._values["location"] = location
            if number_of_buckets is not None:
                self._values["number_of_buckets"] = number_of_buckets
            if output_format is not None:
                self._values["output_format"] = output_format
            if parameters is not None:
                self._values["parameters"] = parameters
            if schema_reference is not None:
                self._values["schema_reference"] = schema_reference
            if serde_info is not None:
                self._values["serde_info"] = serde_info
            if skewed_info is not None:
                self._values["skewed_info"] = skewed_info
            if sort_columns is not None:
                self._values["sort_columns"] = sort_columns
            if stored_as_sub_directories is not None:
                self._values["stored_as_sub_directories"] = stored_as_sub_directories

        @builtins.property
        def bucket_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of reducer grouping columns, clustering columns, and bucketing columns in the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-bucketcolumns
            '''
            result = self._values.get("bucket_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]]]]:
            '''A list of the ``Columns`` in the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-columns
            '''
            result = self._values.get("columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]]]], result)

        @builtins.property
        def compressed(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``True`` if the data in the table is compressed, or ``False`` if not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-compressed
            '''
            result = self._values.get("compressed")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def input_format(self) -> typing.Optional[builtins.str]:
            '''The input format: ``SequenceFileInputFormat`` (binary), or ``TextInputFormat`` , or a custom format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-inputformat
            '''
            result = self._values.get("input_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''The physical location of the table.

            By default, this takes the form of the warehouse location, followed by the database location in the warehouse, followed by the table name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def number_of_buckets(self) -> typing.Optional[jsii.Number]:
            '''Must be specified if the table contains any dimension columns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-numberofbuckets
            '''
            result = self._values.get("number_of_buckets")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def output_format(self) -> typing.Optional[builtins.str]:
            '''The output format: ``SequenceFileOutputFormat`` (binary), or ``IgnoreKeyTextOutputFormat`` , or a custom format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-outputformat
            '''
            result = self._values.get("output_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''The user-supplied properties in key-value form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def schema_reference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SchemaReferenceProperty"]]:
            '''An object that references a schema stored in the AWS Glue Schema Registry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-schemareference
            '''
            result = self._values.get("schema_reference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SchemaReferenceProperty"]], result)

        @builtins.property
        def serde_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SerdeInfoProperty"]]:
            '''The serialization/deserialization (SerDe) information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-serdeinfo
            '''
            result = self._values.get("serde_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SerdeInfoProperty"]], result)

        @builtins.property
        def skewed_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SkewedInfoProperty"]]:
            '''The information about values that appear frequently in a column (skewed values).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-skewedinfo
            '''
            result = self._values.get("skewed_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.SkewedInfoProperty"]], result)

        @builtins.property
        def sort_columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.OrderProperty"]]]]:
            '''A list specifying the sort order of each bucket in the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-sortcolumns
            '''
            result = self._values.get("sort_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.OrderProperty"]]]], result)

        @builtins.property
        def stored_as_sub_directories(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''``True`` if the table data is stored in subdirectories, or ``False`` if not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-storedassubdirectories
            '''
            result = self._values.get("stored_as_sub_directories")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageDescriptorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.TableIdentifierProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "name": "name",
            "region": "region",
        },
    )
    class TableIdentifierProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that describes a target table for resource linking.

            :param catalog_id: The ID of the Data Catalog in which the table resides.
            :param database_name: The name of the catalog database that contains the target table.
            :param name: The name of the target table.
            :param region: The Region of the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableidentifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                table_identifier_property = glue_mixins.CfnTablePropsMixin.TableIdentifierProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    name="name",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c092eb3c2f63fe6faa0752b52acdb1dedee5cbbc6e405962f8eb530ce2df6577)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if name is not None:
                self._values["name"] = name
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the Data Catalog in which the table resides.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableidentifier.html#cfn-glue-table-tableidentifier-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the catalog database that contains the target table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableidentifier.html#cfn-glue-table-tableidentifier-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the target table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableidentifier.html#cfn-glue-table-tableidentifier-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The Region of the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableidentifier.html#cfn-glue-table-tableidentifier-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableIdentifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTablePropsMixin.TableInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "name": "name",
            "owner": "owner",
            "parameters": "parameters",
            "partition_keys": "partitionKeys",
            "retention": "retention",
            "storage_descriptor": "storageDescriptor",
            "table_type": "tableType",
            "target_table": "targetTable",
            "view_expanded_text": "viewExpandedText",
            "view_original_text": "viewOriginalText",
        },
    )
    class TableInputProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            owner: typing.Optional[builtins.str] = None,
            parameters: typing.Any = None,
            partition_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.ColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            retention: typing.Optional[jsii.Number] = None,
            storage_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.StorageDescriptorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_type: typing.Optional[builtins.str] = None,
            target_table: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTablePropsMixin.TableIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            view_expanded_text: typing.Optional[builtins.str] = None,
            view_original_text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure used to define a table.

            :param description: A description of the table.
            :param name: The table name. For Hive compatibility, this is folded to lowercase when it is stored.
            :param owner: The table owner. Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations.
            :param parameters: These key-value pairs define properties associated with the table.
            :param partition_keys: A list of columns by which the table is partitioned. Only primitive types are supported as partition keys. When you create a table used by Amazon Athena, and you do not specify any ``partitionKeys`` , you must at least set the value of ``partitionKeys`` to an empty list. For example: ``"PartitionKeys": []``
            :param retention: The retention time for this table.
            :param storage_descriptor: A storage descriptor containing information about the physical storage of this table.
            :param table_type: The type of this table. AWS Glue will create tables with the ``EXTERNAL_TABLE`` type. Other services, such as Athena, may create tables with additional table types. AWS Glue related table types: - **EXTERNAL_TABLE** - Hive compatible attribute - indicates a non-Hive managed table. - **GOVERNED** - Used by AWS Lake Formation . The AWS Glue Data Catalog understands ``GOVERNED`` .
            :param target_table: A ``TableIdentifier`` structure that describes a target table for resource linking.
            :param view_expanded_text: Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations.
            :param view_original_text: Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations. If the table is a ``VIRTUAL_VIEW`` , certain Athena configuration encoded in base64.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # parameters: Any
                # skewed_column_value_location_maps: Any
                
                table_input_property = glue_mixins.CfnTablePropsMixin.TableInputProperty(
                    description="description",
                    name="name",
                    owner="owner",
                    parameters=parameters,
                    partition_keys=[glue_mixins.CfnTablePropsMixin.ColumnProperty(
                        comment="comment",
                        name="name",
                        type="type"
                    )],
                    retention=123,
                    storage_descriptor=glue_mixins.CfnTablePropsMixin.StorageDescriptorProperty(
                        bucket_columns=["bucketColumns"],
                        columns=[glue_mixins.CfnTablePropsMixin.ColumnProperty(
                            comment="comment",
                            name="name",
                            type="type"
                        )],
                        compressed=False,
                        input_format="inputFormat",
                        location="location",
                        number_of_buckets=123,
                        output_format="outputFormat",
                        parameters=parameters,
                        schema_reference=glue_mixins.CfnTablePropsMixin.SchemaReferenceProperty(
                            schema_id=glue_mixins.CfnTablePropsMixin.SchemaIdProperty(
                                registry_name="registryName",
                                schema_arn="schemaArn",
                                schema_name="schemaName"
                            ),
                            schema_version_id="schemaVersionId",
                            schema_version_number=123
                        ),
                        serde_info=glue_mixins.CfnTablePropsMixin.SerdeInfoProperty(
                            name="name",
                            parameters=parameters,
                            serialization_library="serializationLibrary"
                        ),
                        skewed_info=glue_mixins.CfnTablePropsMixin.SkewedInfoProperty(
                            skewed_column_names=["skewedColumnNames"],
                            skewed_column_value_location_maps=skewed_column_value_location_maps,
                            skewed_column_values=["skewedColumnValues"]
                        ),
                        sort_columns=[glue_mixins.CfnTablePropsMixin.OrderProperty(
                            column="column",
                            sort_order=123
                        )],
                        stored_as_sub_directories=False
                    ),
                    table_type="tableType",
                    target_table=glue_mixins.CfnTablePropsMixin.TableIdentifierProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        name="name",
                        region="region"
                    ),
                    view_expanded_text="viewExpandedText",
                    view_original_text="viewOriginalText"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d29c5babc06ddb52a0469d3737eda54170d819fc626efd7831e9d962cf380d23)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument partition_keys", value=partition_keys, expected_type=type_hints["partition_keys"])
                check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
                check_type(argname="argument storage_descriptor", value=storage_descriptor, expected_type=type_hints["storage_descriptor"])
                check_type(argname="argument table_type", value=table_type, expected_type=type_hints["table_type"])
                check_type(argname="argument target_table", value=target_table, expected_type=type_hints["target_table"])
                check_type(argname="argument view_expanded_text", value=view_expanded_text, expected_type=type_hints["view_expanded_text"])
                check_type(argname="argument view_original_text", value=view_original_text, expected_type=type_hints["view_original_text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name
            if owner is not None:
                self._values["owner"] = owner
            if parameters is not None:
                self._values["parameters"] = parameters
            if partition_keys is not None:
                self._values["partition_keys"] = partition_keys
            if retention is not None:
                self._values["retention"] = retention
            if storage_descriptor is not None:
                self._values["storage_descriptor"] = storage_descriptor
            if table_type is not None:
                self._values["table_type"] = table_type
            if target_table is not None:
                self._values["target_table"] = target_table
            if view_expanded_text is not None:
                self._values["view_expanded_text"] = view_expanded_text
            if view_original_text is not None:
                self._values["view_original_text"] = view_original_text

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The table name.

            For Hive compatibility, this is folded to lowercase when it is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def owner(self) -> typing.Optional[builtins.str]:
            '''The table owner.

            Included for Apache Hive compatibility. Not used in the normal course of AWS Glue operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-owner
            '''
            result = self._values.get("owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''These key-value pairs define properties associated with the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        @builtins.property
        def partition_keys(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]]]]:
            '''A list of columns by which the table is partitioned. Only primitive types are supported as partition keys.

            When you create a table used by Amazon Athena, and you do not specify any ``partitionKeys`` , you must at least set the value of ``partitionKeys`` to an empty list. For example:

            ``"PartitionKeys": []``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-partitionkeys
            '''
            result = self._values.get("partition_keys")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.ColumnProperty"]]]], result)

        @builtins.property
        def retention(self) -> typing.Optional[jsii.Number]:
            '''The retention time for this table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-retention
            '''
            result = self._values.get("retention")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage_descriptor(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.StorageDescriptorProperty"]]:
            '''A storage descriptor containing information about the physical storage of this table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-storagedescriptor
            '''
            result = self._values.get("storage_descriptor")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.StorageDescriptorProperty"]], result)

        @builtins.property
        def table_type(self) -> typing.Optional[builtins.str]:
            '''The type of this table.

            AWS Glue will create tables with the ``EXTERNAL_TABLE`` type. Other services, such as Athena, may create tables with additional table types.

            AWS Glue related table types:

            - **EXTERNAL_TABLE** - Hive compatible attribute - indicates a non-Hive managed table.
            - **GOVERNED** - Used by AWS Lake Formation . The AWS Glue Data Catalog understands ``GOVERNED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-tabletype
            '''
            result = self._values.get("table_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_table(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.TableIdentifierProperty"]]:
            '''A ``TableIdentifier`` structure that describes a target table for resource linking.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-targettable
            '''
            result = self._values.get("target_table")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTablePropsMixin.TableIdentifierProperty"]], result)

        @builtins.property
        def view_expanded_text(self) -> typing.Optional[builtins.str]:
            '''Included for Apache Hive compatibility.

            Not used in the normal course of AWS Glue operations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-viewexpandedtext
            '''
            result = self._values.get("view_expanded_text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def view_original_text(self) -> typing.Optional[builtins.str]:
            '''Included for Apache Hive compatibility.

            Not used in the normal course of AWS Glue operations. If the table is a ``VIRTUAL_VIEW`` , certain Athena configuration encoded in base64.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-vieworiginaltext
            '''
            result = self._values.get("view_original_text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTriggerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "description": "description",
        "event_batching_condition": "eventBatchingCondition",
        "name": "name",
        "predicate": "predicate",
        "schedule": "schedule",
        "start_on_creation": "startOnCreation",
        "tags": "tags",
        "type": "type",
        "workflow_name": "workflowName",
    },
)
class CfnTriggerMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTriggerPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        event_batching_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTriggerPropsMixin.EventBatchingConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        predicate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTriggerPropsMixin.PredicateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schedule: typing.Optional[builtins.str] = None,
        start_on_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
        workflow_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTriggerPropsMixin.

        :param actions: The actions initiated by this trigger.
        :param description: A description of this trigger.
        :param event_batching_condition: Batch condition that must be met (specified number of events received or batch time window expired) before EventBridge event trigger fires.
        :param name: The name of the trigger.
        :param predicate: The predicate of this trigger, which defines when it will fire.
        :param schedule: A ``cron`` expression used to specify the schedule. For more information, see `Time-Based Schedules for Jobs and Crawlers <https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html>`_ in the *AWS Glue Developer Guide* . For example, to run something every day at 12:15 UTC, specify ``cron(15 12 * * ? *)`` .
        :param start_on_creation: Set to true to start ``SCHEDULED`` and ``CONDITIONAL`` triggers when created. True is not supported for ``ON_DEMAND`` triggers.
        :param tags: The tags to use with this trigger.
        :param type: The type of trigger that this is.
        :param workflow_name: The name of the workflow associated with the trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # arguments_: Any
            # tags: Any
            
            cfn_trigger_mixin_props = glue_mixins.CfnTriggerMixinProps(
                actions=[glue_mixins.CfnTriggerPropsMixin.ActionProperty(
                    arguments=arguments_,
                    crawler_name="crawlerName",
                    job_name="jobName",
                    notification_property=glue_mixins.CfnTriggerPropsMixin.NotificationPropertyProperty(
                        notify_delay_after=123
                    ),
                    security_configuration="securityConfiguration",
                    timeout=123
                )],
                description="description",
                event_batching_condition=glue_mixins.CfnTriggerPropsMixin.EventBatchingConditionProperty(
                    batch_size=123,
                    batch_window=123
                ),
                name="name",
                predicate=glue_mixins.CfnTriggerPropsMixin.PredicateProperty(
                    conditions=[glue_mixins.CfnTriggerPropsMixin.ConditionProperty(
                        crawler_name="crawlerName",
                        crawl_state="crawlState",
                        job_name="jobName",
                        logical_operator="logicalOperator",
                        state="state"
                    )],
                    logical="logical"
                ),
                schedule="schedule",
                start_on_creation=False,
                tags=tags,
                type="type",
                workflow_name="workflowName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95de52946732356faccc2cdd5126a6b320fdd0b8230e18150b4734f4f5e598ab)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_batching_condition", value=event_batching_condition, expected_type=type_hints["event_batching_condition"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument start_on_creation", value=start_on_creation, expected_type=type_hints["start_on_creation"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if description is not None:
            self._values["description"] = description
        if event_batching_condition is not None:
            self._values["event_batching_condition"] = event_batching_condition
        if name is not None:
            self._values["name"] = name
        if predicate is not None:
            self._values["predicate"] = predicate
        if schedule is not None:
            self._values["schedule"] = schedule
        if start_on_creation is not None:
            self._values["start_on_creation"] = start_on_creation
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.ActionProperty"]]]]:
        '''The actions initiated by this trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.ActionProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_batching_condition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.EventBatchingConditionProperty"]]:
        '''Batch condition that must be met (specified number of events received or batch time window expired) before EventBridge event trigger fires.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-eventbatchingcondition
        '''
        result = self._values.get("event_batching_condition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.EventBatchingConditionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predicate(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.PredicateProperty"]]:
        '''The predicate of this trigger, which defines when it will fire.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-predicate
        '''
        result = self._values.get("predicate")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.PredicateProperty"]], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''A ``cron`` expression used to specify the schedule.

        For more information, see `Time-Based Schedules for Jobs and Crawlers <https://docs.aws.amazon.com/glue/latest/dg/monitor-data-warehouse-schedule.html>`_ in the *AWS Glue Developer Guide* . For example, to run something every day at 12:15 UTC, specify ``cron(15 12 * * ? *)`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_on_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Set to true to start ``SCHEDULED`` and ``CONDITIONAL`` triggers when created.

        True is not supported for ``ON_DEMAND`` triggers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-startoncreation
        '''
        result = self._values.get("start_on_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags to use with this trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of trigger that this is.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''The name of the workflow associated with the trigger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-workflowname
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTriggerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTriggerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTriggerPropsMixin",
):
    '''The ``AWS::Glue::Trigger`` resource specifies triggers that run AWS Glue jobs.

    For more information, see `Triggering Jobs in AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/trigger-job.html>`_ and `Trigger Structure <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-trigger.html#aws-glue-api-jobs-trigger-Trigger>`_ in the *AWS Glue Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html
    :cloudformationResource: AWS::Glue::Trigger
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # arguments_: Any
        # tags: Any
        
        cfn_trigger_props_mixin = glue_mixins.CfnTriggerPropsMixin(glue_mixins.CfnTriggerMixinProps(
            actions=[glue_mixins.CfnTriggerPropsMixin.ActionProperty(
                arguments=arguments_,
                crawler_name="crawlerName",
                job_name="jobName",
                notification_property=glue_mixins.CfnTriggerPropsMixin.NotificationPropertyProperty(
                    notify_delay_after=123
                ),
                security_configuration="securityConfiguration",
                timeout=123
            )],
            description="description",
            event_batching_condition=glue_mixins.CfnTriggerPropsMixin.EventBatchingConditionProperty(
                batch_size=123,
                batch_window=123
            ),
            name="name",
            predicate=glue_mixins.CfnTriggerPropsMixin.PredicateProperty(
                conditions=[glue_mixins.CfnTriggerPropsMixin.ConditionProperty(
                    crawler_name="crawlerName",
                    crawl_state="crawlState",
                    job_name="jobName",
                    logical_operator="logicalOperator",
                    state="state"
                )],
                logical="logical"
            ),
            schedule="schedule",
            start_on_creation=False,
            tags=tags,
            type="type",
            workflow_name="workflowName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTriggerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Trigger``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255824799159dc7b2939b3528c892541cebfeb63ba695e452d4d873c45f83c3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba0b1ccd11c5dad2b8f2c7a44744d02bc153de877f61ba1db1fbda83071f26c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9827e1b38914d0d74cd48d9bf8c28c697ecc55db5a05614c5087d621a99d02)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTriggerMixinProps:
        return typing.cast(CfnTriggerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTriggerPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arguments": "arguments",
            "crawler_name": "crawlerName",
            "job_name": "jobName",
            "notification_property": "notificationProperty",
            "security_configuration": "securityConfiguration",
            "timeout": "timeout",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            arguments: typing.Any = None,
            crawler_name: typing.Optional[builtins.str] = None,
            job_name: typing.Optional[builtins.str] = None,
            notification_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTriggerPropsMixin.NotificationPropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            security_configuration: typing.Optional[builtins.str] = None,
            timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines an action to be initiated by a trigger.

            :param arguments: The job arguments used when this trigger fires. For this job run, they replace the default arguments set in the job definition itself. You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes. For information about how to specify and consume your own job arguments, see `Calling AWS Glue APIs in Python <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html>`_ in the *AWS Glue Developer Guide* . For information about the key-value pairs that AWS Glue consumes to set up your job, see the `Special Parameters Used by AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html>`_ topic in the developer guide.
            :param crawler_name: The name of the crawler to be used with this action.
            :param job_name: The name of a job to be executed.
            :param notification_property: Specifies configuration properties of a job run notification.
            :param security_configuration: The name of the ``SecurityConfiguration`` structure to be used with this action.
            :param timeout: The ``JobRun`` timeout in minutes. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 2,880 minutes (48 hours). This overrides the timeout value set in the parent job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                # arguments_: Any
                
                action_property = glue_mixins.CfnTriggerPropsMixin.ActionProperty(
                    arguments=arguments_,
                    crawler_name="crawlerName",
                    job_name="jobName",
                    notification_property=glue_mixins.CfnTriggerPropsMixin.NotificationPropertyProperty(
                        notify_delay_after=123
                    ),
                    security_configuration="securityConfiguration",
                    timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a37a942b5c8f049528a177fc807628d92991f0908b1159f61c8ef0c0bb58ed5)
                check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
                check_type(argname="argument crawler_name", value=crawler_name, expected_type=type_hints["crawler_name"])
                check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                check_type(argname="argument notification_property", value=notification_property, expected_type=type_hints["notification_property"])
                check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arguments is not None:
                self._values["arguments"] = arguments
            if crawler_name is not None:
                self._values["crawler_name"] = crawler_name
            if job_name is not None:
                self._values["job_name"] = job_name
            if notification_property is not None:
                self._values["notification_property"] = notification_property
            if security_configuration is not None:
                self._values["security_configuration"] = security_configuration
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def arguments(self) -> typing.Any:
            '''The job arguments used when this trigger fires.

            For this job run, they replace the default arguments set in the job definition itself.

            You can specify arguments here that your own job-execution script consumes, in addition to arguments that AWS Glue itself consumes.

            For information about how to specify and consume your own job arguments, see `Calling AWS Glue APIs in Python <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html>`_ in the *AWS Glue Developer Guide* .

            For information about the key-value pairs that AWS Glue consumes to set up your job, see the `Special Parameters Used by AWS Glue <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html>`_ topic in the developer guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-arguments
            '''
            result = self._values.get("arguments")
            return typing.cast(typing.Any, result)

        @builtins.property
        def crawler_name(self) -> typing.Optional[builtins.str]:
            '''The name of the crawler to be used with this action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-crawlername
            '''
            result = self._values.get("crawler_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def job_name(self) -> typing.Optional[builtins.str]:
            '''The name of a job to be executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-jobname
            '''
            result = self._values.get("job_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_property(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.NotificationPropertyProperty"]]:
            '''Specifies configuration properties of a job run notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-notificationproperty
            '''
            result = self._values.get("notification_property")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.NotificationPropertyProperty"]], result)

        @builtins.property
        def security_configuration(self) -> typing.Optional[builtins.str]:
            '''The name of the ``SecurityConfiguration`` structure to be used with this action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-securityconfiguration
            '''
            result = self._values.get("security_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The ``JobRun`` timeout in minutes.

            This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. The default is 2,880 minutes (48 hours). This overrides the timeout value set in the parent job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTriggerPropsMixin.ConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crawler_name": "crawlerName",
            "crawl_state": "crawlState",
            "job_name": "jobName",
            "logical_operator": "logicalOperator",
            "state": "state",
        },
    )
    class ConditionProperty:
        def __init__(
            self,
            *,
            crawler_name: typing.Optional[builtins.str] = None,
            crawl_state: typing.Optional[builtins.str] = None,
            job_name: typing.Optional[builtins.str] = None,
            logical_operator: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a condition under which a trigger fires.

            :param crawler_name: The name of the crawler to which this condition applies.
            :param crawl_state: The state of the crawler to which this condition applies.
            :param job_name: The name of the job whose ``JobRuns`` this condition applies to, and on which this trigger waits.
            :param logical_operator: A logical operator.
            :param state: The condition state. Currently, the values supported are ``SUCCEEDED`` , ``STOPPED`` , ``TIMEOUT`` , and ``FAILED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                condition_property = glue_mixins.CfnTriggerPropsMixin.ConditionProperty(
                    crawler_name="crawlerName",
                    crawl_state="crawlState",
                    job_name="jobName",
                    logical_operator="logicalOperator",
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c13a2a104efcab72b1129d675e843b4045cfb65b71aab1e0e629c7d571a6006)
                check_type(argname="argument crawler_name", value=crawler_name, expected_type=type_hints["crawler_name"])
                check_type(argname="argument crawl_state", value=crawl_state, expected_type=type_hints["crawl_state"])
                check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                check_type(argname="argument logical_operator", value=logical_operator, expected_type=type_hints["logical_operator"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crawler_name is not None:
                self._values["crawler_name"] = crawler_name
            if crawl_state is not None:
                self._values["crawl_state"] = crawl_state
            if job_name is not None:
                self._values["job_name"] = job_name
            if logical_operator is not None:
                self._values["logical_operator"] = logical_operator
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def crawler_name(self) -> typing.Optional[builtins.str]:
            '''The name of the crawler to which this condition applies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-crawlername
            '''
            result = self._values.get("crawler_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def crawl_state(self) -> typing.Optional[builtins.str]:
            '''The state of the crawler to which this condition applies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-crawlstate
            '''
            result = self._values.get("crawl_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def job_name(self) -> typing.Optional[builtins.str]:
            '''The name of the job whose ``JobRuns`` this condition applies to, and on which this trigger waits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-jobname
            '''
            result = self._values.get("job_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logical_operator(self) -> typing.Optional[builtins.str]:
            '''A logical operator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-logicaloperator
            '''
            result = self._values.get("logical_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The condition state.

            Currently, the values supported are ``SUCCEEDED`` , ``STOPPED`` , ``TIMEOUT`` , and ``FAILED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTriggerPropsMixin.EventBatchingConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"batch_size": "batchSize", "batch_window": "batchWindow"},
    )
    class EventBatchingConditionProperty:
        def __init__(
            self,
            *,
            batch_size: typing.Optional[jsii.Number] = None,
            batch_window: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Batch condition that must be met (specified number of events received or batch time window expired) before EventBridge event trigger fires.

            :param batch_size: Number of events that must be received from Amazon EventBridge before EventBridge event trigger fires.
            :param batch_window: Window of time in seconds after which EventBridge event trigger fires. Window starts when first event is received.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-eventbatchingcondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                event_batching_condition_property = glue_mixins.CfnTriggerPropsMixin.EventBatchingConditionProperty(
                    batch_size=123,
                    batch_window=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f87217137be5b7faa6f9e55d448f6e823d58b194ecc3d28a61ca75ba094a38b7)
                check_type(argname="argument batch_size", value=batch_size, expected_type=type_hints["batch_size"])
                check_type(argname="argument batch_window", value=batch_window, expected_type=type_hints["batch_window"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if batch_size is not None:
                self._values["batch_size"] = batch_size
            if batch_window is not None:
                self._values["batch_window"] = batch_window

        @builtins.property
        def batch_size(self) -> typing.Optional[jsii.Number]:
            '''Number of events that must be received from Amazon EventBridge before EventBridge event trigger fires.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-eventbatchingcondition.html#cfn-glue-trigger-eventbatchingcondition-batchsize
            '''
            result = self._values.get("batch_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def batch_window(self) -> typing.Optional[jsii.Number]:
            '''Window of time in seconds after which EventBridge event trigger fires.

            Window starts when first event is received.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-eventbatchingcondition.html#cfn-glue-trigger-eventbatchingcondition-batchwindow
            '''
            result = self._values.get("batch_window")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBatchingConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTriggerPropsMixin.NotificationPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"notify_delay_after": "notifyDelayAfter"},
    )
    class NotificationPropertyProperty:
        def __init__(
            self,
            *,
            notify_delay_after: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies configuration properties of a job run notification.

            :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-notificationproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                notification_property_property = glue_mixins.CfnTriggerPropsMixin.NotificationPropertyProperty(
                    notify_delay_after=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3d616d66ab8b9c4599c5970db6b16aa10c12ff2266835e1a01925a2f6461a22)
                check_type(argname="argument notify_delay_after", value=notify_delay_after, expected_type=type_hints["notify_delay_after"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if notify_delay_after is not None:
                self._values["notify_delay_after"] = notify_delay_after

        @builtins.property
        def notify_delay_after(self) -> typing.Optional[jsii.Number]:
            '''After a job run starts, the number of minutes to wait before sending a job run delay notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-notificationproperty.html#cfn-glue-trigger-notificationproperty-notifydelayafter
            '''
            result = self._values.get("notify_delay_after")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnTriggerPropsMixin.PredicateProperty",
        jsii_struct_bases=[],
        name_mapping={"conditions": "conditions", "logical": "logical"},
    )
    class PredicateProperty:
        def __init__(
            self,
            *,
            conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTriggerPropsMixin.ConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            logical: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the predicate of the trigger, which determines when it fires.

            :param conditions: A list of the conditions that determine when the trigger will fire.
            :param logical: An optional field if only one condition is listed. If multiple conditions are listed, then this field is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-predicate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                predicate_property = glue_mixins.CfnTriggerPropsMixin.PredicateProperty(
                    conditions=[glue_mixins.CfnTriggerPropsMixin.ConditionProperty(
                        crawler_name="crawlerName",
                        crawl_state="crawlState",
                        job_name="jobName",
                        logical_operator="logicalOperator",
                        state="state"
                    )],
                    logical="logical"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0493e67e675afc80370195c3e9256055e68a7ea679efb74b563a89df91ddc711)
                check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
                check_type(argname="argument logical", value=logical, expected_type=type_hints["logical"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if conditions is not None:
                self._values["conditions"] = conditions
            if logical is not None:
                self._values["logical"] = logical

        @builtins.property
        def conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.ConditionProperty"]]]]:
            '''A list of the conditions that determine when the trigger will fire.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-predicate.html#cfn-glue-trigger-predicate-conditions
            '''
            result = self._values.get("conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTriggerPropsMixin.ConditionProperty"]]]], result)

        @builtins.property
        def logical(self) -> typing.Optional[builtins.str]:
            '''An optional field if only one condition is listed.

            If multiple conditions are listed, then this field is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-predicate.html#cfn-glue-trigger-predicate-logical
            '''
            result = self._values.get("logical")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredicateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnUsageProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "description": "description",
        "name": "name",
        "tags": "tags",
    },
)
class CfnUsageProfileMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUsageProfilePropsMixin.ProfileConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnUsageProfilePropsMixin.

        :param configuration: 
        :param description: A description of the usage profile.
        :param name: The name of the usage profile.
        :param tags: The tags to be applied to this UsageProfiles.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-usageprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            cfn_usage_profile_mixin_props = glue_mixins.CfnUsageProfileMixinProps(
                configuration=glue_mixins.CfnUsageProfilePropsMixin.ProfileConfigurationProperty(
                    job_configuration={
                        "job_configuration_key": glue_mixins.CfnUsageProfilePropsMixin.ConfigurationObjectProperty(
                            allowed_values=["allowedValues"],
                            default_value="defaultValue",
                            max_value="maxValue",
                            min_value="minValue"
                        )
                    },
                    session_configuration={
                        "session_configuration_key": glue_mixins.CfnUsageProfilePropsMixin.ConfigurationObjectProperty(
                            allowed_values=["allowedValues"],
                            default_value="defaultValue",
                            max_value="maxValue",
                            min_value="minValue"
                        )
                    }
                ),
                description="description",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc40b8e52b8f35ddef78ae68ca0f040c6dece6c384c73c91f84db025fa14b561)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsageProfilePropsMixin.ProfileConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-usageprofile.html#cfn-glue-usageprofile-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsageProfilePropsMixin.ProfileConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the usage profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-usageprofile.html#cfn-glue-usageprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the usage profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-usageprofile.html#cfn-glue-usageprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to be applied to this UsageProfiles.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-usageprofile.html#cfn-glue-usageprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUsageProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUsageProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnUsageProfilePropsMixin",
):
    '''Creates an AWS Glue usage profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-usageprofile.html
    :cloudformationResource: AWS::Glue::UsageProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        cfn_usage_profile_props_mixin = glue_mixins.CfnUsageProfilePropsMixin(glue_mixins.CfnUsageProfileMixinProps(
            configuration=glue_mixins.CfnUsageProfilePropsMixin.ProfileConfigurationProperty(
                job_configuration={
                    "job_configuration_key": glue_mixins.CfnUsageProfilePropsMixin.ConfigurationObjectProperty(
                        allowed_values=["allowedValues"],
                        default_value="defaultValue",
                        max_value="maxValue",
                        min_value="minValue"
                    )
                },
                session_configuration={
                    "session_configuration_key": glue_mixins.CfnUsageProfilePropsMixin.ConfigurationObjectProperty(
                        allowed_values=["allowedValues"],
                        default_value="defaultValue",
                        max_value="maxValue",
                        min_value="minValue"
                    )
                }
            ),
            description="description",
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
        props: typing.Union[CfnUsageProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::UsageProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8e81ef86667b8c4e5d7edd17bc3e52bd172b5ce7bc6ffc8cd53548a5bae551)
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
            type_hints = typing.get_type_hints(_typecheckingstub__746680411f9be11e3e7a02abc2dedbba7937908ee3e8718e3a3be1306cba8b3b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3a8ccbf8f8063d812b0f15d91c04426a0a22c196ce62d2f61bc8a82150fbf9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUsageProfileMixinProps:
        return typing.cast(CfnUsageProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnUsageProfilePropsMixin.ConfigurationObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_values": "allowedValues",
            "default_value": "defaultValue",
            "max_value": "maxValue",
            "min_value": "minValue",
        },
    )
    class ConfigurationObjectProperty:
        def __init__(
            self,
            *,
            allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            default_value: typing.Optional[builtins.str] = None,
            max_value: typing.Optional[builtins.str] = None,
            min_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the values that an admin sets for each job or session parameter configured in a AWS Glue usage profile.

            :param allowed_values: A list of allowed values for the parameter.
            :param default_value: A default value for the parameter.
            :param max_value: A maximum allowed value for the parameter.
            :param min_value: A minimum allowed value for the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-usageprofile-configurationobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                configuration_object_property = glue_mixins.CfnUsageProfilePropsMixin.ConfigurationObjectProperty(
                    allowed_values=["allowedValues"],
                    default_value="defaultValue",
                    max_value="maxValue",
                    min_value="minValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__25d63e4d2ba1a6f65812bab6d62b4a4faefe9c91a6164d85ecee37e4b246b11a)
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
                check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if default_value is not None:
                self._values["default_value"] = default_value
            if max_value is not None:
                self._values["max_value"] = max_value
            if min_value is not None:
                self._values["min_value"] = min_value

        @builtins.property
        def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of allowed values for the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-usageprofile-configurationobject.html#cfn-glue-usageprofile-configurationobject-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''A default value for the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-usageprofile-configurationobject.html#cfn-glue-usageprofile-configurationobject-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_value(self) -> typing.Optional[builtins.str]:
            '''A maximum allowed value for the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-usageprofile-configurationobject.html#cfn-glue-usageprofile-configurationobject-maxvalue
            '''
            result = self._values.get("max_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def min_value(self) -> typing.Optional[builtins.str]:
            '''A minimum allowed value for the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-usageprofile-configurationobject.html#cfn-glue-usageprofile-configurationobject-minvalue
            '''
            result = self._values.get("min_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnUsageProfilePropsMixin.ProfileConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "job_configuration": "jobConfiguration",
            "session_configuration": "sessionConfiguration",
        },
    )
    class ProfileConfigurationProperty:
        def __init__(
            self,
            *,
            job_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUsageProfilePropsMixin.ConfigurationObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            session_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUsageProfilePropsMixin.ConfigurationObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies the job and session values that an admin configures in an AWS Glue usage profile.

            :param job_configuration: A key-value map of configuration parameters for AWS Glue jobs.
            :param session_configuration: A key-value map of configuration parameters for AWS Glue sessions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-usageprofile-profileconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
                
                profile_configuration_property = glue_mixins.CfnUsageProfilePropsMixin.ProfileConfigurationProperty(
                    job_configuration={
                        "job_configuration_key": glue_mixins.CfnUsageProfilePropsMixin.ConfigurationObjectProperty(
                            allowed_values=["allowedValues"],
                            default_value="defaultValue",
                            max_value="maxValue",
                            min_value="minValue"
                        )
                    },
                    session_configuration={
                        "session_configuration_key": glue_mixins.CfnUsageProfilePropsMixin.ConfigurationObjectProperty(
                            allowed_values=["allowedValues"],
                            default_value="defaultValue",
                            max_value="maxValue",
                            min_value="minValue"
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b0ec4822304825026f0dd269239f5ef932d139ff16b4359f5924fc3f949b2a7)
                check_type(argname="argument job_configuration", value=job_configuration, expected_type=type_hints["job_configuration"])
                check_type(argname="argument session_configuration", value=session_configuration, expected_type=type_hints["session_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if job_configuration is not None:
                self._values["job_configuration"] = job_configuration
            if session_configuration is not None:
                self._values["session_configuration"] = session_configuration

        @builtins.property
        def job_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsageProfilePropsMixin.ConfigurationObjectProperty"]]]]:
            '''A key-value map of configuration parameters for AWS Glue jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-usageprofile-profileconfiguration.html#cfn-glue-usageprofile-profileconfiguration-jobconfiguration
            '''
            result = self._values.get("job_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsageProfilePropsMixin.ConfigurationObjectProperty"]]]], result)

        @builtins.property
        def session_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsageProfilePropsMixin.ConfigurationObjectProperty"]]]]:
            '''A key-value map of configuration parameters for AWS Glue sessions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-usageprofile-profileconfiguration.html#cfn-glue-usageprofile-profileconfiguration-sessionconfiguration
            '''
            result = self._values.get("session_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUsageProfilePropsMixin.ConfigurationObjectProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProfileConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnWorkflowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_run_properties": "defaultRunProperties",
        "description": "description",
        "max_concurrent_runs": "maxConcurrentRuns",
        "name": "name",
        "tags": "tags",
    },
)
class CfnWorkflowMixinProps:
    def __init__(
        self,
        *,
        default_run_properties: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for CfnWorkflowPropsMixin.

        :param default_run_properties: A collection of properties to be used as part of each execution of the workflow.
        :param description: A description of the workflow.
        :param max_concurrent_runs: You can use this parameter to prevent unwanted multiple updates to data, to control costs, or in some cases, to prevent exceeding the maximum number of concurrent runs of any of the component jobs. If you leave this parameter blank, there is no limit to the number of concurrent workflow runs.
        :param name: The name of the workflow representing the flow.
        :param tags: The tags to use with this workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
            
            # default_run_properties: Any
            # tags: Any
            
            cfn_workflow_mixin_props = glue_mixins.CfnWorkflowMixinProps(
                default_run_properties=default_run_properties,
                description="description",
                max_concurrent_runs=123,
                name="name",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f577de8ebd7c2f0fb345aad6dbca898fb0ca5b8f5ee533e46a8ae410e07ea0df)
            check_type(argname="argument default_run_properties", value=default_run_properties, expected_type=type_hints["default_run_properties"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_run_properties is not None:
            self._values["default_run_properties"] = default_run_properties
        if description is not None:
            self._values["description"] = description
        if max_concurrent_runs is not None:
            self._values["max_concurrent_runs"] = max_concurrent_runs
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_run_properties(self) -> typing.Any:
        '''A collection of properties to be used as part of each execution of the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-defaultrunproperties
        '''
        result = self._values.get("default_run_properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        '''You can use this parameter to prevent unwanted multiple updates to data, to control costs, or in some cases, to prevent exceeding the maximum number of concurrent runs of any of the component jobs.

        If you leave this parameter blank, there is no limit to the number of concurrent workflow runs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-maxconcurrentruns
        '''
        result = self._values.get("max_concurrent_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the workflow representing the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags to use with this workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkflowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkflowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_glue.mixins.CfnWorkflowPropsMixin",
):
    '''The ``AWS::Glue::Workflow`` is an AWS Glue resource type that manages AWS Glue workflows.

    A workflow is a container for a set of related jobs, crawlers, and triggers in AWS Glue . Using a workflow, you can design a complex multi-job extract, transform, and load (ETL) activity that AWS Glue can execute and track as single entity.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html
    :cloudformationResource: AWS::Glue::Workflow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_glue import mixins as glue_mixins
        
        # default_run_properties: Any
        # tags: Any
        
        cfn_workflow_props_mixin = glue_mixins.CfnWorkflowPropsMixin(glue_mixins.CfnWorkflowMixinProps(
            default_run_properties=default_run_properties,
            description="description",
            max_concurrent_runs=123,
            name="name",
            tags=tags
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Glue::Workflow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184f22b74e0715e52f1e9c5b2f7d1a78c25b0a4408d17ff5a008fab3e473a97f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a085993d451f2e318f19cfee3165b78474ef540688e436092531b9e0904b6ae)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55f7d54368d3bb2ea5a0f3cac1dd71b39c908f7d812cc0fc30499162fabfc7b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkflowMixinProps:
        return typing.cast(CfnWorkflowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnClassifierMixinProps",
    "CfnClassifierPropsMixin",
    "CfnConnectionMixinProps",
    "CfnConnectionPropsMixin",
    "CfnCrawlerMixinProps",
    "CfnCrawlerPropsMixin",
    "CfnCustomEntityTypeMixinProps",
    "CfnCustomEntityTypePropsMixin",
    "CfnDataCatalogEncryptionSettingsMixinProps",
    "CfnDataCatalogEncryptionSettingsPropsMixin",
    "CfnDataQualityRulesetMixinProps",
    "CfnDataQualityRulesetPropsMixin",
    "CfnDatabaseMixinProps",
    "CfnDatabasePropsMixin",
    "CfnDevEndpointMixinProps",
    "CfnDevEndpointPropsMixin",
    "CfnIdentityCenterConfigurationMixinProps",
    "CfnIdentityCenterConfigurationPropsMixin",
    "CfnIntegrationMixinProps",
    "CfnIntegrationPropsMixin",
    "CfnIntegrationResourcePropertyMixinProps",
    "CfnIntegrationResourcePropertyPropsMixin",
    "CfnJobMixinProps",
    "CfnJobPropsMixin",
    "CfnMLTransformMixinProps",
    "CfnMLTransformPropsMixin",
    "CfnPartitionMixinProps",
    "CfnPartitionPropsMixin",
    "CfnRegistryMixinProps",
    "CfnRegistryPropsMixin",
    "CfnSchemaMixinProps",
    "CfnSchemaPropsMixin",
    "CfnSchemaVersionMetadataMixinProps",
    "CfnSchemaVersionMetadataPropsMixin",
    "CfnSchemaVersionMixinProps",
    "CfnSchemaVersionPropsMixin",
    "CfnSecurityConfigurationMixinProps",
    "CfnSecurityConfigurationPropsMixin",
    "CfnTableMixinProps",
    "CfnTableOptimizerMixinProps",
    "CfnTableOptimizerPropsMixin",
    "CfnTablePropsMixin",
    "CfnTriggerMixinProps",
    "CfnTriggerPropsMixin",
    "CfnUsageProfileMixinProps",
    "CfnUsageProfilePropsMixin",
    "CfnWorkflowMixinProps",
    "CfnWorkflowPropsMixin",
]

publication.publish()

def _typecheckingstub__a328e3e9b1c3052c60ae0bb5138bf2a22027f3814e6595a87d8dec9469588e8f(
    *,
    csv_classifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClassifierPropsMixin.CsvClassifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    grok_classifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClassifierPropsMixin.GrokClassifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    json_classifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClassifierPropsMixin.JsonClassifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    xml_classifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClassifierPropsMixin.XMLClassifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9872122f3b44047300349c842dcb488f9f0fcee9d63d77f7785bd56e89fcaadb(
    props: typing.Union[CfnClassifierMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d8b9e84e8b65c439681de1e0dcca5ee051f847d0bb52f9478e11f42b284398(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61cfc31a346b018460bd20f118835fb9d3a11792a7bf56823713cc892949b0ac(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bd14ce5552c3b83860159121336ccc22174ca306d09d6441c1f1dbb80a4dde(
    *,
    allow_single_column: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    contains_custom_datatype: typing.Optional[typing.Sequence[builtins.str]] = None,
    contains_header: typing.Optional[builtins.str] = None,
    custom_datatype_configured: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    delimiter: typing.Optional[builtins.str] = None,
    disable_value_trimming: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    header: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    quote_symbol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1248bce53af82aa06bd6fb2c01ceee86ca3e2be30bef77b5e11716a5ca98fbb(
    *,
    classification: typing.Optional[builtins.str] = None,
    custom_patterns: typing.Optional[builtins.str] = None,
    grok_pattern: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7efb773b0a0fe13c59aad3027f6d602a89c57b75b6894b5c185c714a6f0dde(
    *,
    json_path: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ddec36e9ab9edde40b8061cf7096f02514c446958bda21013ead9166bf97b6(
    *,
    classification: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    row_tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14a0dd4ebf682b363d565828f16a20435253b82d94430509c4cbe80300fc9f1(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    connection_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.ConnectionInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9342d375f92c26181765ba372b72d4a888c65776b82d430b08b98b3261ce2e8(
    props: typing.Union[CfnConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf79752abdfbfbfd8ab59bbbb1d022355efb6efb6ec6ec1437049d72e725c0b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7725c9a46b4945b8c193d47f91bbd0f1708d2b09b089e11bbcc3d9fce8b4091(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cccd6fee54bb9af757e17690876727409506f68317509bbd4856b1e45ced3ef(
    *,
    authentication_type: typing.Optional[builtins.str] = None,
    basic_authentication_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.BasicAuthenticationCredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_authentication_credentials: typing.Any = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    o_auth2_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.OAuth2PropertiesInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eba12f7720b93f538af88b9fbeb1ab7ae77ad738cb468fee4f83262be64bf4d(
    *,
    authorization_code: typing.Optional[builtins.str] = None,
    redirect_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ead1ecbd398cd04a745e081a08867f97c81840b1ee6333ba99da63d17dd0e89(
    *,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1726516f50694ab83d14d2bce6329e3d17c32df781534dc5a8130363b2186f1(
    *,
    athena_properties: typing.Any = None,
    authentication_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.AuthenticationConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connection_properties: typing.Any = None,
    connection_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    match_criteria: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    physical_connection_requirements: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.PhysicalConnectionRequirementsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    python_properties: typing.Any = None,
    spark_properties: typing.Any = None,
    validate_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    validate_for_compute_environments: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d38843083b9ed03899415af369ca2f43e12164bac8734f8a9f4bfa819179fb(
    *,
    aws_managed_client_application_reference: typing.Optional[builtins.str] = None,
    user_managed_client_application_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94d02d69c64dae18367fa9cd32d8aa5c3907bf17b35a00ce6facb17ac632d37(
    *,
    access_token: typing.Optional[builtins.str] = None,
    jwt_token: typing.Optional[builtins.str] = None,
    refresh_token: typing.Optional[builtins.str] = None,
    user_managed_client_application_client_secret: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498f7ac71532649748c2424404f4924cfc23742bcad4bf8690b43bbb0f3e72b0(
    *,
    authorization_code_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.AuthorizationCodePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    o_auth2_client_application: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.OAuth2ClientApplicationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    o_auth2_credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectionPropsMixin.OAuth2CredentialsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    o_auth2_grant_type: typing.Optional[builtins.str] = None,
    token_url: typing.Optional[builtins.str] = None,
    token_url_parameters_map: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d0e42cf5d99d4eb55ba73623cf4c0ce89f80736c2909ab81653b4bec8f9f43(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    security_group_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448d370592f7619ef5f78161c0259f53c78150542d18173cb69ba57f2062d99d(
    *,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[builtins.str] = None,
    crawler_security_configuration: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    lake_formation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.LakeFormationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    recrawl_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.RecrawlPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_change_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.SchemaChangePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_prefix: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.TargetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8625e58544eaef652f69eae076a4eae917caebcc365c30681d37370a4e85810f(
    props: typing.Union[CfnCrawlerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae14543ac46ed42b54d7f83466b3263048d73ff9fe013d41dd6a325e46a212b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feece70d61e9b64a554f797d30f85378b57cef579f182216f89f2e7c4f5313a4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23aa721b924391b8149a3a38798dcc91351364a58331b94cf382140dbaea1e84(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    dlq_event_queue_arn: typing.Optional[builtins.str] = None,
    event_queue_arn: typing.Optional[builtins.str] = None,
    tables: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1273651a23ff9c22c4cc50d1b14c8d4878eafb799a63ff33a0b5a7bb2f6e6506(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    create_native_delta_table: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    delta_tables: typing.Optional[typing.Sequence[builtins.str]] = None,
    write_manifest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34347133197acba5a57f6cca9197ce1da2446d99a39a2d0b523dd22b17bad14f(
    *,
    path: typing.Optional[builtins.str] = None,
    scan_all: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    scan_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567365f194d49b26201f3adb17e3fb8334c1f00b955ffc11fc0a6cbbe7fb2ebf(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_traversal_depth: typing.Optional[jsii.Number] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a43620ebad60594d54461e6de3ec43136bbe4c6709765987366ad40bb7117fe(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_traversal_depth: typing.Optional[jsii.Number] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a9e73c947bd26eb31da631d6d5266721944a314f279061c5f7c8ce9d781ae9(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    enable_additional_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d238624614c74bfe82e4e12acbc4a3be08e746959f96b0018eac44f9994a5171(
    *,
    account_id: typing.Optional[builtins.str] = None,
    use_lake_formation_credentials: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e89e0d127505044ef6e6ffb6b0b8de994387047a80720e3b0e2b9074cddc232(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ede704b334486490ccaa29cf2c1eaab39f6937672aa470a71da0c464724a4f8(
    *,
    recrawl_behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f165693d46afb0382c356502c9343ea7e32798e28ad89b6353b67711b7010d0(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    dlq_event_queue_arn: typing.Optional[builtins.str] = None,
    event_queue_arn: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    sample_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85952df4a34ea31b08840c78310651818299724eecbc65f5a0becbb238f008b(
    *,
    schedule_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bda1bdf56669a4fbed18b0784d5e52d97182c4533eb5f3bf2a8f53e52658340(
    *,
    delete_behavior: typing.Optional[builtins.str] = None,
    update_behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063dade8b3fbfcb47287210bd3f0e92c95b6b032d37e7c57350ef3d8e5336f24(
    *,
    catalog_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.CatalogTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    delta_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.DeltaTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    dynamo_db_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.DynamoDBTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    hudi_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.HudiTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    iceberg_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.IcebergTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    jdbc_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.JdbcTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    mongo_db_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.MongoDBTargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    s3_targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCrawlerPropsMixin.S3TargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c78b98a1774cb414c8653d07bf19f5b02ee7cdedd254b34b03d63234e62466(
    *,
    context_words: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    regex_string: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c9bf4508ce96bae654a64c71dd569f16322fa7f530934aaade20bc6ed2a525(
    props: typing.Union[CfnCustomEntityTypeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da4879c694f2b429ab97c747d2f6d5c1bbd491946bf3c9a9efa71839fa326cc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42dc74282a0013d16932c88992ee3a68b14aaae041cc3577afdc4c3339eab9e1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da04c9ec316d2ba43e39316dc4881972588b007e0d2908187e79f503a2c19d4(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    data_catalog_encryption_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataCatalogEncryptionSettingsPropsMixin.DataCatalogEncryptionSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ef7a850fcd5a86e3830ed0876616cc1de8d13108a47a364ffa68722ea474fc(
    props: typing.Union[CfnDataCatalogEncryptionSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d74a78455df3b59fdac8800e83d0ca6ddeee8c46d7ec2a77086f7f5b4d8b2b2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ebeccb9bf287ea144029039ab9dcd5b072ea7051af36536e7c2e78cc187781(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51b05e943a3d82b76f2ff6795620df7105a4836e580cbaa43ebd33b5c78a601(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
    return_connection_password_encrypted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c998d297b0cab8c042cfa770703deaff0bfeb74595d03e5ffd516a8a5262b9(
    *,
    connection_password_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataCatalogEncryptionSettingsPropsMixin.ConnectionPasswordEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_at_rest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataCatalogEncryptionSettingsPropsMixin.EncryptionAtRestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4653025e0b3d9f47954254d4ef8668843cf9d3ec7bb77f484a45d85525044cc(
    *,
    catalog_encryption_mode: typing.Optional[builtins.str] = None,
    catalog_encryption_service_role: typing.Optional[builtins.str] = None,
    sse_aws_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205f2f9d0b1963d31729912c25cc8d6c50520135570f948d62e524bea101ce4c(
    *,
    client_token: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    ruleset: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    target_table: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataQualityRulesetPropsMixin.DataQualityTargetTableProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd2d435e6eb6029708b10bf14d23c1b6a4ca00a98b3d661079af5b2b45da79b(
    props: typing.Union[CfnDataQualityRulesetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53e73d6eef57aa0f5e8f3cbe94a36df5cb2661da8dd964de977203868f984ad(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87c329b52041a49705aa3593908ca2cfff4a075a5331237d47e98ad5416596b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a312630169324f684d8115babc19d2293368fe7d8fbb7d6cc17c764f5180e78(
    *,
    database_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a467e825a079273fb6bbc086209b32b22c4ce9b7fb1916987a5b4738558ae7(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatabasePropsMixin.DatabaseInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58a29598520530cd1f6bd1f324c10299fb1e2e1a94386d2ee955bd27e710ebc(
    props: typing.Union[CfnDatabaseMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464dd921e8933186d066db0d711af61ec404446b3193830e1fc7ae8a35ad184f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5113e2df2c5e2877d2bb82204da8f90f3f9b198f13aad4e0d657ec0eb1b8c9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3d36392c83f4fba93c33197d0bd672563544169125cbe3ad2bdfa18c91b767(
    *,
    data_lake_principal_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cda326aa838c7d576241421ddb731569901815a9da9a545c774679f98f2450(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157a1dcd98bd1bde2a279406ee8abef3f868f45e024abbf346790af3b247af91(
    *,
    create_table_default_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatabasePropsMixin.PrincipalPrivilegesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    federated_database: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatabasePropsMixin.FederatedDatabaseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    location_uri: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    target_database: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatabasePropsMixin.DatabaseIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b98184b1d2aed5e3c13110e2b9dfae1b5ba8e397dc2d850b0bed2e30b22342c(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca455317c3ea9aba777335c061ba67870153569bba3f01a7867250ea7a136d22(
    *,
    permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatabasePropsMixin.DataLakePrincipalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde2c948af0417f6089142e19ed3156b06da222a7d120b1729015503c6a48d44(
    *,
    arguments: typing.Any = None,
    endpoint_name: typing.Optional[builtins.str] = None,
    extra_jars_s3_path: typing.Optional[builtins.str] = None,
    extra_python_libs_s3_path: typing.Optional[builtins.str] = None,
    glue_version: typing.Optional[builtins.str] = None,
    number_of_nodes: typing.Optional[jsii.Number] = None,
    number_of_workers: typing.Optional[jsii.Number] = None,
    public_key: typing.Optional[builtins.str] = None,
    public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    worker_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f74c062a7d53fbd09f2735edc939e3fb77696e217fbc978c4b9b74756bbc3a(
    props: typing.Union[CfnDevEndpointMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafb75be79545cd504195e203f5e79375048e9861a781551fd8d46575a242af0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c62961f75e933cfcc3e88e541da05ed71e7aae5be4dedc97babb54a7673884(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8f980a4305395998503cf51e60269aa3b4712f3fbdef556c73ba96fc52deae(
    *,
    instance_arn: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_background_sessions_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8147c74f06204d5565b2d0c3c82c67b52f0abc6833685ad1b44c4a6147a2ade(
    props: typing.Union[CfnIdentityCenterConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883eb9e51ca5abb2896a9341d64f8246e5f7f28b7e7d52016a1646b7e3e1d7d1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9474a9790bc6c2a11065ee5c90ac71ba05c8a25813978c82d49a2bf3f9fd7d2a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a132bfd4d44707640b924d7929633369261a3b8c2b5113c4c46847de8f072ddb(
    *,
    additional_encryption_context: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    data_filter: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    integration_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.IntegrationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    integration_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c30c29f3ac0f9577d1ff2c3b79ec39485c57611e025ffbb6d61a9223e0dfb4f(
    props: typing.Union[CfnIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6549d953fd5fbe8130d5cfa57d40d3fbb7ad747a350825b2aaf3127d79a1607f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0725fbf344fbc39ffeb02d3a9ef22ac624c2fd758a1c864ee855e8474a082f38(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70100596a15c10c2b99dd5f72e857392b7fa052e987d0d4842c6d22a53b3e58(
    *,
    continuous_sync: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    refresh_interval: typing.Optional[builtins.str] = None,
    source_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ca6deb5a0e19e24480245587be3004b1cde980dc8da6e717db7aed098653e1(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    source_processing_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationResourcePropertyPropsMixin.SourceProcessingPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_processing_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationResourcePropertyPropsMixin.TargetProcessingPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acbc21d7c63b93df417924b078de7d6e7c45bd10236ab19f951b2f8fc51fb20b(
    props: typing.Union[CfnIntegrationResourcePropertyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad89bb67fd4372947bfc0fe3c8e9d5ee9599b117969b94bb438d16ea7025d6f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d825bc81663edbcee039547a616b8ce5b30a40a730e28e46a162d6d050e040f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdc7dfa6ecd1ba0a85f12987cf77f3d08e6b4b4bfc532db83bba701b2736513(
    *,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473649f5a749dc1cfac70aa72d1982be410b1178fd3bacf994a21613122fb73e(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    event_bus_arn: typing.Optional[builtins.str] = None,
    kms_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe9ae06ff341e847993c18451a0bb9406108776440cca0e2e575ffa668512ca(
    *,
    allocated_capacity: typing.Optional[jsii.Number] = None,
    command: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.JobCommandProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connections: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.ConnectionsListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_arguments: typing.Any = None,
    description: typing.Optional[builtins.str] = None,
    execution_class: typing.Optional[builtins.str] = None,
    execution_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.ExecutionPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    glue_version: typing.Optional[builtins.str] = None,
    job_mode: typing.Optional[builtins.str] = None,
    job_run_queuing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    log_uri: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[builtins.str] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    non_overridable_arguments: typing.Any = None,
    notification_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.NotificationPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    number_of_workers: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    timeout: typing.Optional[jsii.Number] = None,
    worker_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29297e18e4aefa300afe4ff2b3e557afdd856dfeb8aebf93f52a03f823a57362(
    props: typing.Union[CfnJobMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f1675580dddcacb2166f0ff35918b82d0b49f2fc11da1d8842c9e27a5409c9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9da3fd8ec306564346b5fbe47c9d53273a472ec404c3421e8b462207d68d6be(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395dc2b2ad124d4a43dd74ea0f55ae6ca12a84351956b30666dd0e6d6375699b(
    *,
    connections: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da955de9a09ecc9d5643d38077b165b9a318368aa4e9ef467df78292c68993b3(
    *,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d85eab79a04899ff3a613c6458b861e0081aace08b581ed9bbd7c9a801bd634(
    *,
    name: typing.Optional[builtins.str] = None,
    python_version: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    script_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cfde3549b63b075fb2d854b35978d301bd4d13667b0d500a9d504fcce52f73(
    *,
    notify_delay_after: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35add2331241a754e7b44ce1d989ca1ad8e71b67690fb07e2855c37dffb5575d(
    *,
    description: typing.Optional[builtins.str] = None,
    glue_version: typing.Optional[builtins.str] = None,
    input_record_tables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMLTransformPropsMixin.InputRecordTablesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    number_of_workers: typing.Optional[jsii.Number] = None,
    role: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    timeout: typing.Optional[jsii.Number] = None,
    transform_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMLTransformPropsMixin.TransformEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    transform_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMLTransformPropsMixin.TransformParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    worker_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d8f4a4b391189662fe1c799d84a17dd239ff4f8592a05ce2fd75511acc1547(
    props: typing.Union[CfnMLTransformMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465fbe8a691611c80691a0a0881d36e989921c53b302d2b1be4edc65ba323b20(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ee07d3ccacf89ab1b6c2293c5de43eb22199ba0525bf119241f94d6fc8d6ff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e293d6131954f708651ae9535adf33e01d07aa6d28ad66b8e4b5a554aab63e74(
    *,
    accuracy_cost_tradeoff: typing.Optional[jsii.Number] = None,
    enforce_provided_labels: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    precision_recall_tradeoff: typing.Optional[jsii.Number] = None,
    primary_key_column_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d2c7aa24d0274da00d1d7d0283977286aaac9c72bbd5d898fed016c554ae1a(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    connection_name: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b8a4e561babfdbe21bac693320f1f18dd07503d32e6e709356b1a695b1fbe9(
    *,
    glue_tables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMLTransformPropsMixin.GlueTablesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31799fd47b0062af14fdb1ee0a8315bc26382c7d0a546deb2b85d91d12be0213(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
    ml_user_data_encryption_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfaa88243c71bca5f1a4da5716da708f893533906b695cd7068da1e76fd372f(
    *,
    ml_user_data_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMLTransformPropsMixin.MLUserDataEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_run_security_configuration_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e3a3b0ebbbd958280b240837a413562b1ecc5d09cea728692097798766df3b(
    *,
    find_matches_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMLTransformPropsMixin.FindMatchesParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    transform_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d15f90e83eacb251a1b817ecbf932f78b16ec72871ec27acfa8199ee0d0759(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    partition_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartitionPropsMixin.PartitionInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000bfdac516641a32b61c686e24ed2a82c371a8ada2a1ab0dd250a8e1b25251e(
    props: typing.Union[CfnPartitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed38f0c65280750c3a3222428b44b399a1fab4b69c2f5ffa2c15179861bfeba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1536a7a7d367ac54de44698ebd04d33ea85ac86e00e073d4e872bdd609024b9f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4469fa91c5a6b1224dbad1ec42fe603f516f0a4b7563da8c3d963a788af8c7(
    *,
    comment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef67f1d5644903917dbd2d741b53f900648923dfa858d5c6af940befbae7d00(
    *,
    column: typing.Optional[builtins.str] = None,
    sort_order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3db50af5aa28f148ffb6a4d04b68a366d04081c94b77404f0c6cb624278ef2(
    *,
    parameters: typing.Any = None,
    storage_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartitionPropsMixin.StorageDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96c8231305fc80075c66e8b45953f99a56a5d58c5eaccb85ea8616c6b772ee6(
    *,
    registry_name: typing.Optional[builtins.str] = None,
    schema_arn: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a5fe8b3160edb4ce744eff12088209227fcdd5f00b221f8daa0ab44a8830ac(
    *,
    schema_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartitionPropsMixin.SchemaIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_version_id: typing.Optional[builtins.str] = None,
    schema_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c96f3005cf7b037ddccbda6b9beaf4a8b19b24f086f48b2829772461bc6f4ca(
    *,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    serialization_library: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b4fcfbeb7ea5a0bc9adfba611e33df091de885711c67f5ae416e47abd1f411(
    *,
    skewed_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    skewed_column_value_location_maps: typing.Any = None,
    skewed_column_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e744d2827fdf2260937ba701f671d1cf11611fdbe724b6e5e52803054453b7f(
    *,
    bucket_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartitionPropsMixin.ColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compressed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    input_format: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    number_of_buckets: typing.Optional[jsii.Number] = None,
    output_format: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    schema_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartitionPropsMixin.SchemaReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    serde_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartitionPropsMixin.SerdeInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    skewed_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartitionPropsMixin.SkewedInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sort_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPartitionPropsMixin.OrderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stored_as_sub_directories: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4122a43f710358b5b23c136781acc74bed3fb447c35023c9cc4cb82f6a065ed(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cae20de650720887756b13c5b3769905f58d28583cea52ef96183dad98594ff(
    props: typing.Union[CfnRegistryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d14c5cdedd1c08f0899a143f995241ed1af63631510678da4ef577329e894fb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68efd3d60b005cc15b77b7138b32f2d45ad1d332d9eda1be46964169407d6305(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797ad145a2a564ed9f64b9045d1c79b1bd3057f47213268c2f391f6510112154(
    *,
    checkpoint_version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchemaPropsMixin.SchemaVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    compatibility: typing.Optional[builtins.str] = None,
    data_format: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    registry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchemaPropsMixin.RegistryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_definition: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e45ca7c9324c44105433ccf21b787d563cbfa0e124ab33c57729fd45e825097(
    props: typing.Union[CfnSchemaMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265a1738beca109d1add72fb150fce5ee10097d839e4dc1f7fd5a962defcc237(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f8cf42d684bf9e325de978ccce5985d9868f20b6f4d43e3d7950ff625aa4be(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e1a8fa8339508c57b19e898d905c342259a7d5c019db94fa913d14f6ed4da3(
    *,
    arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a05d88582b4860dbdce27c09b169985d87ed0786288a4081d40c1ed6be6420(
    *,
    is_latest: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cda9be8abe0ed94166a3c707e6667bca2e83bed7c46c8542c323eaf6664c0a(
    *,
    key: typing.Optional[builtins.str] = None,
    schema_version_id: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a7f44dd970b99a593e5657762d031f11f67ae502df506093f5a43a6c24355e(
    props: typing.Union[CfnSchemaVersionMetadataMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f20618a50b265c029680471a48057fccbc6d6a854365d527089f08ae8dd9b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9799fefe16736bd874b702357957dd86e0dd33dac3f4b9b019b370fe555aba6a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a1a59496157746b64b6985732bd8521e1128cdaa8fab70e78f7fcd16f9354f(
    *,
    schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchemaVersionPropsMixin.SchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_definition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05b01e63be1aec486364775a724690b218604b1b78e1bf426f797d1826b564c(
    props: typing.Union[CfnSchemaVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2611ce35bd64fe6a67b5e2878d61a601655c87b2eb7e5227ca67af005767458f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6f5d6fe372fdfdc556939a7510883a034dab128d2fb488bfa5be20abfe0328(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b8dbeef1590ee1e8c48058d3021f94c409b610daeb9e23aec70d0dd06737e9(
    *,
    registry_name: typing.Optional[builtins.str] = None,
    schema_arn: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1c9367a3c8bcb3cefd8b88e3a837f8d964d78b8a6ead36bd941c96ae9efb8c(
    *,
    encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityConfigurationPropsMixin.EncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d195b8b7a23d10809a7fd8836b4b2576f071653ea546d802e7ee5bf03476fee(
    props: typing.Union[CfnSecurityConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50f90986a423c20b2f5b5591a50b54e56cb13db75c459b87751db59049a7c7e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274a6f3e6d3aac31fd057d8d17c5808c20e0b25c0fb19afaac5eb4f5058b4bf6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc67ee6a23cb7abe617e84146de309053f496562177f0b04ae28e06c2a7ba37(
    *,
    cloud_watch_encryption_mode: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933a243e0c37b4012a5703cf6402b3049d11ef6a2f7786f870df9ba18335855a(
    *,
    cloud_watch_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityConfigurationPropsMixin.CloudWatchEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_bookmarks_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityConfigurationPropsMixin.JobBookmarksEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_encryptions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityConfigurationPropsMixin.S3EncryptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b053996a5cfd9cb423b919ba4cc5583a070bdaa2e319f93b9a6cd95eab116db(
    *,
    job_bookmarks_encryption_mode: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269fa8ea2aa8c1daa8a2b3baf771664f5cd259c8254978237796b438a82b6b86(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    s3_encryption_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39efe7602b3edd447ff6a7f78f878d35dc004419a8a459f476bee165cf7cbd88(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    open_table_format_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.OpenTableFormatInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.TableInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2288a590bd25426f0b125cd6c8907c27e352b057c8d245de6c081367b2df3575(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    table_optimizer_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableOptimizerPropsMixin.TableOptimizerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98b69c81bdbf2fe8ccabc57ef0eb76f58f377d36abf0b874d713a52d8328373(
    props: typing.Union[CfnTableOptimizerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567d2637f8883062193f007ddb6c26df7f2ccd508bbda2f5f762b6be0f252b27(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347bd9f930d991dfbd498d98430b1919ddb9d056742f15d6b131ba3e84823869(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2dc7a846e72daec956b132882c0d9d234011ba11208937495a60cfdb5b0db4(
    *,
    location: typing.Optional[builtins.str] = None,
    orphan_file_retention_period_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9769028b2b696e9a2a16d657b89885d110bbcc77a6379765294d950d8fa3311b(
    *,
    clean_expired_files: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    number_of_snapshots_to_retain: typing.Optional[jsii.Number] = None,
    snapshot_retention_period_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cc451365451651f57ac818436df59311ea735a7f33b00e3def427b487ccc0e(
    *,
    iceberg_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableOptimizerPropsMixin.IcebergConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755b2d9e6566b6fc82efcc513a3d36bb9059e29e9c75ac2b8e8deb7f8efab6ac(
    *,
    iceberg_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableOptimizerPropsMixin.IcebergRetentionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49886016b340732b0c6d11209f1170f65c644fd6c9829e2b2773dcecf528fb62(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    orphan_file_deletion_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableOptimizerPropsMixin.OrphanFileDeletionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retention_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableOptimizerPropsMixin.RetentionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTableOptimizerPropsMixin.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a870d8c9869be1dac233af5c1a303dfca170f0bfd64e76f07f5c88223d0afa2(
    *,
    glue_connection_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac29ac2aee8e348c107ce5e7c900056b1b41a4d0ed13f725c5b41d4c710be272(
    props: typing.Union[CfnTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5755d7bd23ad33beb872a24cdf149ed4eb5ac674e1e239915044466e7b9301c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__708092ebd9ff582423c84e64cf4eb057e949e0dbb69d7692f9a3ae49c3d43a49(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0872e61b96fb59ca2908ab54fb2076789e5b568bd9e0fd22b9f210f7634f0a(
    *,
    comment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff52173338a2335012058eadcc7fe31070b4a0d890b65481035d0cdbe42314a4(
    *,
    metadata_operation: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a11588071664058b0a74a27ad541ff4122016a11679d3028f2aa6d38a8816d7(
    *,
    iceberg_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.IcebergInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e3da3ea55aa083b9b87a06342d5dc4fd1cb14cb8d49cf0e661bdb239ec5479(
    *,
    column: typing.Optional[builtins.str] = None,
    sort_order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278a952c33518316f3375c7bc60d005b8610d9b32cbb52d594a6f69bc30cc2e3(
    *,
    registry_name: typing.Optional[builtins.str] = None,
    schema_arn: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87dd2ad26e62732f62427cc36c213489a0fce8b8d380769e9401b91436c7c66e(
    *,
    schema_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.SchemaIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema_version_id: typing.Optional[builtins.str] = None,
    schema_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae0300efffae6e2e65441157df82805e5493db03b4055cc5f9f9161b952e968(
    *,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    serialization_library: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0420f60b7fe7d33df8f82bea58ed8deab3a5a5af2431e13ce67363fa6d90e3(
    *,
    skewed_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    skewed_column_value_location_maps: typing.Any = None,
    skewed_column_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe8d8c8ba6a1419d32a1f9faf06d343f7de48a1a4eeb38620d610933c3a02d4(
    *,
    bucket_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    compressed: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    input_format: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    number_of_buckets: typing.Optional[jsii.Number] = None,
    output_format: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    schema_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.SchemaReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    serde_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.SerdeInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    skewed_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.SkewedInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sort_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.OrderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stored_as_sub_directories: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c092eb3c2f63fe6faa0752b52acdb1dedee5cbbc6e405962f8eb530ce2df6577(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29c5babc06ddb52a0469d3737eda54170d819fc626efd7831e9d962cf380d23(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    partition_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.ColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    retention: typing.Optional[jsii.Number] = None,
    storage_descriptor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.StorageDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_type: typing.Optional[builtins.str] = None,
    target_table: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTablePropsMixin.TableIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    view_expanded_text: typing.Optional[builtins.str] = None,
    view_original_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95de52946732356faccc2cdd5126a6b320fdd0b8230e18150b4734f4f5e598ab(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTriggerPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    event_batching_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTriggerPropsMixin.EventBatchingConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    predicate: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTriggerPropsMixin.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    start_on_creation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
    workflow_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255824799159dc7b2939b3528c892541cebfeb63ba695e452d4d873c45f83c3d(
    props: typing.Union[CfnTriggerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0b1ccd11c5dad2b8f2c7a44744d02bc153de877f61ba1db1fbda83071f26c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9827e1b38914d0d74cd48d9bf8c28c697ecc55db5a05614c5087d621a99d02(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a37a942b5c8f049528a177fc807628d92991f0908b1159f61c8ef0c0bb58ed5(
    *,
    arguments: typing.Any = None,
    crawler_name: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    notification_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTriggerPropsMixin.NotificationPropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c13a2a104efcab72b1129d675e843b4045cfb65b71aab1e0e629c7d571a6006(
    *,
    crawler_name: typing.Optional[builtins.str] = None,
    crawl_state: typing.Optional[builtins.str] = None,
    job_name: typing.Optional[builtins.str] = None,
    logical_operator: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87217137be5b7faa6f9e55d448f6e823d58b194ecc3d28a61ca75ba094a38b7(
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    batch_window: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d616d66ab8b9c4599c5970db6b16aa10c12ff2266835e1a01925a2f6461a22(
    *,
    notify_delay_after: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0493e67e675afc80370195c3e9256055e68a7ea679efb74b563a89df91ddc711(
    *,
    conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTriggerPropsMixin.ConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    logical: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc40b8e52b8f35ddef78ae68ca0f040c6dece6c384c73c91f84db025fa14b561(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUsageProfilePropsMixin.ProfileConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8e81ef86667b8c4e5d7edd17bc3e52bd172b5ce7bc6ffc8cd53548a5bae551(
    props: typing.Union[CfnUsageProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746680411f9be11e3e7a02abc2dedbba7937908ee3e8718e3a3be1306cba8b3b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3a8ccbf8f8063d812b0f15d91c04426a0a22c196ce62d2f61bc8a82150fbf9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d63e4d2ba1a6f65812bab6d62b4a4faefe9c91a6164d85ecee37e4b246b11a(
    *,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_value: typing.Optional[builtins.str] = None,
    max_value: typing.Optional[builtins.str] = None,
    min_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0ec4822304825026f0dd269239f5ef932d139ff16b4359f5924fc3f949b2a7(
    *,
    job_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUsageProfilePropsMixin.ConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    session_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUsageProfilePropsMixin.ConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f577de8ebd7c2f0fb345aad6dbca898fb0ca5b8f5ee533e46a8ae410e07ea0df(
    *,
    default_run_properties: typing.Any = None,
    description: typing.Optional[builtins.str] = None,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184f22b74e0715e52f1e9c5b2f7d1a78c25b0a4408d17ff5a008fab3e473a97f(
    props: typing.Union[CfnWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a085993d451f2e318f19cfee3165b78474ef540688e436092531b9e0904b6ae(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55f7d54368d3bb2ea5a0f3cac1dd71b39c908f7d812cc0fc30499162fabfc7b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
